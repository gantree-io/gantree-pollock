"""Essential things for Pollock."""

# builtin
from os import path


def get_version() -> str:
    """Return the Pollock version."""
    here = path.abspath(path.dirname(__file__))

    with open(path.join(here, "version.txt"), "r") as f:
        return f.readline().splitlines()[0]
