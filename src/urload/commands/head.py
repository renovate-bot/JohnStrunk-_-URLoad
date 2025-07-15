"""Implements the 'head' command for URLoad."""

import textwrap
from typing import Any

from urload.commands.base import Command, CommandError
from urload.url import URL


class HeadCommand(Command):
    """Keeps the first n URLs from the shared URL list."""

    name = "head"
    description = textwrap.dedent("""
    head <n> - Keep the first n URLs from the list.

    This command keeps only the first n URLs in the list, discarding the rest.
    """)

    def run(
        self, args: list[str], url_list: list[URL], settings: Any = None
    ) -> list[URL]:
        """Keep the first n URLs from the list."""
        if not args:
            raise CommandError("No count provided.")

        try:
            n = int(args[0])
        except ValueError:
            raise CommandError("Invalid count. Must be an integer.")

        if n < 0:
            raise CommandError("Count must be non-negative.")

        return url_list[:n]
