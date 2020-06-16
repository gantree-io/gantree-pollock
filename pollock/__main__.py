"""Pollock main."""

from . import cli


def main() -> None:
    """Pollock main."""
    # print("__name__:", __name__)
    cli_obj = cli.Cli()
    cli_obj.handle_args()


if __name__ == "__main__":
    main()
