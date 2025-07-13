"""Implements the 'add' command for URLoad."""

import textwrap

from urload.commands.base import Command, CommandError
from urload.url import URL


class AddCommand(Command):
    """Appends a URL to the shared URL list."""

    name = "add"
    description = textwrap.dedent("""
    Usage: add <url> - Add a URL to the list.

    This command appends the specified URL to the shared URL list.
    """)

    def run(self, args: list[str], url_list: list[URL]) -> list[URL]:
        """Append a URL to the list if provided."""
        if not args:
            raise CommandError("Error: No URL provided.")
        url = args[0]
        url_obj = URL(url)
        url_list.append(url_obj)
        return url_list
