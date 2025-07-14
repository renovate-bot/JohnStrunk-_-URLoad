"""Implements the 'list' command for URLoad."""

import textwrap

from urload.commands.base import Command, CommandError
from urload.url import URL


class ListCommand(Command):
    """Lists all URLs in the shared URL list with their indices."""

    name = "list"
    description = textwrap.dedent("""
    list - List all URLs in the current list.

    This command prints each URL in the list, prefixed with its index.
    """)

    def run(self, args: list[str], url_list: list[URL]) -> list[URL]:
        """
        Print each URL in the list with its index, or a specified range.

        :param args: Optional range argument (see command description).
        :param url_list: List of URL objects to print.
        :return: The original list (unmodified).
        :raises CommandError: If the argument is invalid.
        """

        def print_range(start: int, end: int) -> None:
            if start < 0 or end < 0 or start > end or end >= len(url_list):
                raise CommandError("Invalid range argument.")
            for idx in range(start, end + 1):
                print(f"{idx}: {url_list[idx].url}")

        if not args:
            print_range(0, len(url_list) - 1) if url_list else None
            return url_list

        arg = args[0]
        n = len(url_list)

        try:
            if "-" not in arg:  # Single index
                idx = int(arg)
                print_range(idx, idx)
                return url_list
            if arg == "-":
                raise ValueError()
            if arg.startswith("-"):  # -N
                end = int(arg[1:])
                print_range(0, end)
                return url_list
            if arg.endswith("-"):  # N-
                start = int(arg[:-1])
                print_range(start, n - 1)
                return url_list
            # N-M
            start, end = map(int, arg.split("-", 1))
            print_range(start, end)
            return url_list
        except ValueError:
            raise CommandError(
                "Invalid argument format. Use a single index or a range (e.g., N, -N, N-, N-M)."
            )
