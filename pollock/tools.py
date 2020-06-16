"""Defines some general purpose tools for pollock."""

# builtin
import os
from typing import Any


class DoInPollockWorkdir(object):
    """Context manager for doing stuff in ~/.pollock/."""

    def __init__(self) -> None:
        """See class docstring."""
        self.initial_dir = os.getcwd()

    def __enter__(self) -> str:
        """Change to homedir."""
        pollock_work_path = os.path.expanduser("~") + "/.pollock"

        if not os.path.exists(pollock_work_path):
            os.mkdir(pollock_work_path)

        os.chdir(pollock_work_path)

        return pollock_work_path

    def __exit__(self, *_: Any) -> None:
        """Return to original dir."""
        os.chdir(self.initial_dir)
