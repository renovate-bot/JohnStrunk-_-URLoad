"""Implements the 'uniq' command for URLoad."""

import textwrap

from urload.commands.base import Command
from urload.url import URL


class UniqCommand(Command):
    """Removes duplicate URLs from the list, keeping the first occurrence."""

    name = "uniq"
    description = textwrap.dedent("""
    uniq - Remove duplicate URLs, keeping only the first occurrence of each.

    This command removes duplicate URLs from the list, preserving order and keeping the first instance of each URL.
    """)

    def run(self, args: list[str], url_list: list[URL]) -> list[URL]:
        """Remove duplicate URLs, keeping only the first occurrence."""
        seen: set[str] = set()
        unique_list: list[URL] = []
        for url in url_list:
            if url.url not in seen:
                seen.add(url.url)
                unique_list.append(url)
        print(f"Removed {len(url_list) - len(unique_list)} duplicate URLs.")
        return unique_list
