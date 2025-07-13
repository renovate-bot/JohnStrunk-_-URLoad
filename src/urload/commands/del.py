"""Implements the 'del' command for URLoad."""

import re
import textwrap

from urload.commands.base import Command, CommandError
from urload.url import URL


class DelCommand(Command):
    """Deletes one or more URLs from the shared URL list by index or range."""

    name = "del"
    description = textwrap.dedent("""
    Usage: del <index> | del <start>-<end> - Delete one or more URLs by index or range.

    This command removes a single URL by index or a range of URLs from the list.
    """)

    def run(self, args: list[str], url_list: list[URL]) -> list[URL]:
        """Delete a URL or range of URLs by index."""
        if not args:
            raise CommandError("No index or range provided.")
        arg = args[0].replace(" ", "")
        range_match = re.match(r"^(\d+)-(\d+)$", arg)
        if range_match:
            start, end = int(range_match.group(1)), int(range_match.group(2))
            if start > end or start < 0 or end >= len(url_list):
                raise CommandError("Invalid range.")
            del url_list[start : end + 1]
            print(f"Deleted URLs from index {start} to {end}.")
            return url_list
        # Single index
        try:
            idx = int(arg)
        except ValueError:
            raise CommandError("Invalid index.")
        if idx < 0 or idx >= len(url_list):
            raise CommandError("Index out of range.")
        del url_list[idx]
        print(f"Deleted URL at index {idx}.")
        return url_list
