"""Implements the 'list' command for URLoad."""

import textwrap

from urload.commands.base import Command
from urload.url import URL


class ListCommand(Command):
    """Lists all URLs in the shared URL list with their indices."""

    name = "list"
    description = textwrap.dedent("""
    Usage: list - List all URLs in the current list.

    This command prints each URL in the list, prefixed with its index.
    """)

    def run(self, args: list[str], url_list: list[URL]) -> list[URL]:
        """Print each URL in the list with its index."""
        for idx, url in enumerate(url_list):
            print(f"{idx}: {url.url}")
        return url_list
