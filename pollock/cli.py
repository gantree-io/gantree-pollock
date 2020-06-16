"""Defines pollock Cli class."""

# builtin
import argparse
import getpass
import subprocess
import importlib
import shutil

# platform semi-specific
import os  # some commands are linux specific (e.g. 'uname -r')

# package
from .swap import SwapTools
from .processtools import print_process_lines
from .tools import DoInPollockWorkdir

# platform specific
# ... mac will say "unable to locate [...]"
apt_importable = False
try:
    importlib.import_module("apt")
    apt_importable = True

except ImportError:
    pass
    # print("couldn't import apt!")

if apt_importable is True:
    import apt  # pylint: disable=import-error

# instansiate classes
swapTools = SwapTools()


class Cli:
    """Class for abstracting parsing."""

    def __init__(self) -> None:
        """See class docstring."""
        self.parser = argparse.ArgumentParser()
        self._add_parser_arguments(self.parser)
        self.args = self.parser.parse_args()

    def _print_version(self) -> None:
        from pollock import __name__, __version__

        print(__name__, __version__)

    def _get_github_repo_name(self, repo_url: str) -> str:
        # at least it's terse *shrug*
        # https://media0.giphy.com/media/KanqCs2oHuzKYCXSXo/giphy.gif
        return repo_url.split("/")[-1].split(".")[0]

    def _clone_repo(self, repo_url: str, lazy: bool = False) -> str:
        print("---CLONE REPO")
        path_to_repo_root = "<PLACEHOLDER FOR PATH TO CLONED REPO>"
        if "https://github.com/" in repo_url and ".git" in repo_url:
            print("valid github url")
            with DoInPollockWorkdir() as cwd:
                repo_name = self._get_github_repo_name(repo_url)
                path_to_repo_root = cwd + "/" + repo_name
                repo_path_exists = os.path.exists(path_to_repo_root)

                print(f"cloning into '{path_to_repo_root}'")

                if repo_path_exists:

                    if lazy is False:
                        if os.path.exists(path_to_repo_root + "/.git"):
                            print(
                                "Deleting existing repo at"
                                + f"'~/.pollock/{repo_name}'"
                            )
                            shutil.rmtree(path_to_repo_root)
                        else:
                            raise FileExistsError(
                                "file/folder with repo name already exists!"
                            )

                    elif lazy is True:
                        print("leaving existing repo alone...")
                        return path_to_repo_root

                self.__clone_github_repo(repo_url)

        else:
            print("Valid patterns are:")
            print("https://github.com/<USER>/<REPO_NAME>.git")
            raise ValueError("repo url does not match any recognized patterns")

        return path_to_repo_root

    def __run_init_script(self) -> None:
        if os.path.isfile(os.getcwd() + "/scripts/init.sh"):
            with subprocess.Popen(["./scripts/init.sh"]) as p4:
                print("attempting to run repo's ./scripts/init.sh")
                print_process_lines(p4, nickname="running ./scripts/init.sh")

    def __cargo_build_release(self) -> None:
        home_path = os.path.expanduser("~")
        cargo_path = home_path + "/.cargo/bin/cargo"

        print("beginning cargo build (--release)")

        if os.path.isfile(cargo_path):
            print("found cargo binary")
            with subprocess.Popen([cargo_path, "build", "--release"]) as p4:
                print("building (this might take a long time)")
                print_process_lines(p4, nickname="building")
        else:
            raise FileNotFoundError(
                f"Cargo binary not found at {cargo_path}!"
            )

    def _compile_repo(self, path_to_repo_root: str) -> None:
        print("---wip: COMPILE REPO")
        repo_name = path_to_repo_root.split("/")[-1]

        with DoInPollockWorkdir() as cwd:
            if f"{cwd}/{repo_name}" == path_to_repo_root:
                os.chdir(path_to_repo_root)
                print("cwd:", os.getcwd())

                self.__run_init_script()
                self.__cargo_build_release()

            else:
                print("screaming")

    def handle_args(self) -> None:
        """Parse cli commands and arguments."""
        print("REPO_URL:", self.args.REPO_URL)

        if self.args.version is True:
            self._print_version()
            exit()

        elif self.args.REPO_URL is not None:
            path_to_repo_root = self._clone_repo(
                self.args.REPO_URL, lazy=self.args.lazy_clone
            )
            self._compile_repo(path_to_repo_root)
            exit()

        else:
            raise Exception(
                "No matching argument logic." + " Internal error..."
            )

        exit()

        if self.args.install is True:
            user_needed = "ubuntu"
            repo_name = "substrate-node-template"

            self._is_correct_instance(strict=True)
            self._has_username(user_needed, strict=True)
            swapTools.is_swap_on(strict=True)

            print(f"changing cwd to root of {repo_name}")
            try:
                os.chdir(f"{os.getcwd()}/{repo_name}")
            except FileNotFoundError as e:
                print(
                    "[ERROR]: Couldn't navigate to repo root!"
                    + " Please ensure you've already ran"
                    + " 'pollock --prepare-framework' and rebooted"
                )
                print(f"ERROR: {e}")
                exit()

            with subprocess.Popen([f"./scripts/init.sh"]) as p4:
                print("running repo's ./scripts/init.sh")
                print_process_lines(p4, nickname="init " + repo_name)

            with subprocess.Popen(
                [
                    f"/home/{user_needed}/.cargo/bin/cargo",
                    "build",
                    "--release",
                ]
            ) as p4:
                print(
                    "building " + repo_name + " (this might take a long time)"
                )
                print_process_lines(p4, nickname="build " + repo_name)

            print("BUILD OKAY.")

            exit()

        if self.args.ensure_deps is True:
            user_needed = "root"

            self._is_correct_instance(strict=True)
            self._has_username(user_needed, strict=True)

            self.__install_apt_package("curl")

            print("DEPS OKAY.")

            exit()

        if self.args.ensure_swap is True:
            user_needed = "root"

            self._is_correct_instance(strict=True)
            self._has_username(user_needed, strict=True)

            print("ensuring swap is enabled")

            swapTools.ensure_swap()

            print("SWAP OKAY.")

            exit()

        if self.args.prepare_framework is True:

            user_needed = "ubuntu"
            # repo_user = "substrate-developer-hub"
            repo_name = "substrate-node-template"

            self._is_correct_instance(strict=True)
            self._has_username(user_needed, strict=True)
            swapTools.is_swap_on(strict=True)

            self.__install_substrate_deps()
            self.__clone_github_repo(
                "https://github.com/"
                + "substrate-developer-hub/substrate-node-template"
            )

            print("rust prerequisites satisfied.")
            print("[!!!] RESTART REQUIRED...")
            print("[ Please restart, then run 'pollock --install' ]")

            print("REQS OKAY.")

            exit()

        else:
            raise Exception("Internal error...")
        exit()

    def _list_modules(self) -> None:
        """List substrate modules (SRMLs)."""
        raise NotImplementedError("Listing SRML modules not yet supported")

    def _add_parser_arguments(
        self, root_parser: argparse.ArgumentParser
    ) -> None:
        root_parser.add_argument(
            "REPO_URL",
            action="store",
            help="url of repo to clone and compile",
            nargs="?",
        )
        root_parser.add_argument(
            "-V",
            "--version",
            action="store_true",
            help="print version information and exit",
        )
        root_parser.add_argument(
            "--module", action="store", help="show available modules"
        )
        root_parser.add_argument(
            "--ensure-deps",
            action="store_true",
            help="ensure all substrate deps satisfied",
        )
        root_parser.add_argument(
            "--ensure-swap",
            action="store_true",
            help="ensure a swap is available for during compilation",
        )
        root_parser.add_argument(
            "--prepare-framework",
            action="store_true",
            help="install substrate framework dependencies",
        )
        root_parser.add_argument(
            "--compile-node",
            action="store_true",
            help="compile and configure substrate node",
        )
        root_parser.add_argument(
            "--expected-release",
            action="store",
            help="release to expect (output of uname -r)",
        )
        root_parser.add_argument(
            "--expected-nodename",
            action="store",
            help="nodename to expect (output of uname -n)",
        )
        root_parser.add_argument(
            "--lazy-clone",
            action="store_true",
            help="don't reclone repo if it already exists"
            + "(may result in outdated repos)",
        )

    def __install_substrate_deps(self) -> None:
        with subprocess.Popen(
            ["curl", "https://getsubstrate.io", "-sSf"],
            stdout=subprocess.PIPE,
            encoding="utf8",
        ) as p1:
            with subprocess.Popen(
                ["bash", "-s", "--", "--fast"],
                stdin=p1.stdout,
                stdout=subprocess.PIPE,
                encoding="utf8",
            ) as p2:
                print(
                    "trying to install substrate requirements... "
                    + "(this might take a while)"
                )
                print_process_lines(p2, nickname="sub-deps")

    def __clone_github_repo(self, github_repo_url: str) -> None:

        try:
            with subprocess.Popen(["git", "clone", github_repo_url]) as p3:
                print(f"cloning {github_repo_url}")
                print_process_lines(p3, nickname="clone github repo")
        except Exception:
            print(f"!!! couldn't clone {github_repo_url}")

    def __install_apt_package(self, package_name: str) -> None:

        if apt_importable is False:
            raise Exception(
                "Couldn't import apt."
                + " You may be in a virtualenv."
                + " Please try again with no virtualenv and"
                + " ensure you're not on a dev machine!"
            )
        print(f"Attempting to install '{package_name}' with apt...")
        cache = apt.cache.Cache()
        print("updating apt cache...")
        cache.update()
        cache.open()

        requested_package = cache[package_name]

        if requested_package.is_installed:

            print(f"{package_name} is already installed...")

        else:

            print(f"marking {package_name} for install...")
            requested_package.mark_install()

            try:
                print(f"commiting changes to apt's cache...")
                cache.commit()
            except Exception as e:
                print(f"couldn't install {package_name}...")
                raise Exception(e)

    def _is_correct_instance(self, strict: bool = True,) -> bool:
        # expected_release = "4.15.0-1051-aws"
        # expected_nodename = "ip-172-31-6-46"
        # expected_release = "4.15.0-74-generic"
        # expected_nodename = "calv-pollocktest00"
        expected_release = self.args.expected_release
        expected_nodename = self.args.expected_nodename

        uname_res = os.uname()
        print(uname_res)

        if uname_res.release == expected_release:
            if uname_res.nodename == expected_nodename:
                return True
            else:
                print(f"invalid nodename! ({uname_res.nodename})")
                print(f"expected nodename = {expected_nodename}")
        else:
            print(f"invalid release! ({uname_res.release})")
            print(f"expected release = {expected_release}")

        # expected_username = "ubuntu"
        # username = getpass.getuser()
        # print(f"[username]: {username}")

        # if username == expected_username:

        if strict is False:
            return False
        elif strict is True:
            raise RuntimeError(
                f"must be running on server instance! "
                + "this is a failsafe so you don't accidentally "
                + "turn your dev machine into a node!"
            )
        else:
            raise TypeError("strict opt must be a bool")

    def _has_username(self, target_username: str, strict: bool = True) -> bool:
        real_username = getpass.getuser()

        print(f"is username '{target_username}'?...")

        if target_username == real_username:
            return True
        else:
            if strict is not True:
                return False
            else:
                raise RuntimeError(
                    f"You must be running as user '{target_username}'!"
                )
