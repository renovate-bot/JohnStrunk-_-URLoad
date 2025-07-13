"""Implements the 'tail' command for URLoad."""

import textwrap

from urload.commands.base import Command, CommandError
from urload.url import URL


class TailCommand(Command):
    """Keeps the last n URLs from the shared URL list."""

    name = "tail"
    description = textwrap.dedent("""
    tail <n> - Keep the last n URLs from the list.

    This command keeps only the last n URLs in the list, discarding the rest.
    """)

    def run(self, args: list[str], url_list: list[URL]) -> list[URL]:
        """Keep the last n URLs from the list."""
        if not args:
            raise CommandError("No count provided.")

        try:
            n = int(args[0])
        except ValueError:
            raise CommandError("Invalid count. Must be an integer.")

        if n < 0:
            raise CommandError("Count must be non-negative.")

        return url_list[-n:] if n > 0 else []
