"""Implements the 'sort' command for URLoad."""

import textwrap
from typing import Any

from urload.commands.base import Command
from urload.url import URL


class SortCommand(Command):
    """Sorts the URLs in the list lexicographically by URL."""

    name = "sort"
    description = textwrap.dedent(
        """
    sort - Sort the URLs in the list lexicographically by URL.

    This command sorts the URLs in the list in-place by their URL value.
    """
    )

    def run(
        self, args: list[str], url_list: list[URL], settings: Any = None
    ) -> list[URL]:
        """Sort the URLs in the list lexicographically by URL."""
        sorted_list = sorted(url_list, key=lambda u: u.url)
        print("Sorted URLs.")
        return sorted_list
