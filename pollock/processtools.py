"""Tools related to using the subprocess module."""

from typing import Any


def print_process_lines(process: Any, nickname: str = "subproc") -> None:
    """Print stout from process until it's finished."""
    if hasattr(process.stdout, "readline"):
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                print(f"[{nickname}]:", output.strip())
