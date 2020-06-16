"""Functions related to checking/modifying swap on instances."""

# builtin
import subprocess
import os

# package
from .processtools import print_process_lines


class SwapTools:
    """Set of tools for checking and modifying the system swap."""

    def __init__(self) -> None:
        """See class docstring."""
        pass

    def ensure_swap(self) -> None:
        """Ensure swap space available and active, address if not."""
        if self.is_swap_on(strict=False) is False:
            if self._does_swapfile_exist() is False:
                self._create_swapfile()
                self._prepare_swapfile()
                print("swapfile has been created")
            self.enable_swap()
            if self.is_swap_on(strict=True) is True:
                print("swap has been enabled")
        else:
            print("swap already enabled")

    def is_swap_on(self, strict: bool = False) -> bool:
        """Check if swapping is enabled. Doesn't require root. Returns bool."""
        # todo: make method look for specific output to determine result
        with subprocess.Popen(
            ["/sbin/swapon", "--show"], stdout=subprocess.PIPE
        ) as p_swapon:
            line = p_swapon.stdout.readline()
            if not line:
                if strict is True:
                    raise RuntimeError("Swap must be on!")
                elif strict is False:
                    return False
                else:
                    raise TypeError("keyword 'strict' must be a bool")
            else:
                print("swapping likely on")
                return True

    def _create_swapfile(self, gigabytes: str = "1G") -> None:
        """Create a swapfile."""
        with subprocess.Popen(
            ["sudo", "fallocate", "-l", gigabytes, "/swapfile"]
        ) as p1:
            print("creating swapfile")
            print_process_lines(p1, nickname="create swapfile")
        with subprocess.Popen(["sudo", "chmod", "600", "/swapfile"]) as p2:
            print("changing perms for swapfile")
            print_process_lines(p2, nickname="swapfile perms")

    def _prepare_swapfile(self) -> None:
        """Allocate linux swap area on the file."""
        with subprocess.Popen(["sudo", "mkswap", "/swapfile"]) as p2:
            print("allocating swap area on swapfile")
            print_process_lines(p2, nickname="allocate swap to swapfile")

    def _does_swapfile_exist(self) -> bool:
        print("checking if swapfile exists")
        swapfile_does_exist = os.path.exists("/swapfile")
        if swapfile_does_exist is True:
            return True
        elif swapfile_does_exist is False:
            return False
        else:
            raise TypeError("swapfile_does_exist should be a bool")

    def enable_swap(self) -> None:
        """Enable swapping on swapfile."""
        with subprocess.Popen(["sudo", "/sbin/swapon", "/swapfile"]) as p1:
            print("enabling swapping")
            print_process_lines(p1, nickname="enable swapping")

    def disable_swap(self) -> None:
        """Disable swapping on swapfile."""
        with subprocess.Popen(
            ["sudo", "/sbin/swapoff", "-v", "/swapfile"]
        ) as p1:
            print("disabling swapping")
            print("NOTE: this doesn't delete the swapfile at /swapfile")
            print_process_lines(p1, nickname="disable swapping")
