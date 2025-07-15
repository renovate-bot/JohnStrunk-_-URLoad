"""Implements the 'add' command for URLoad."""

import re
import textwrap
from itertools import product
from typing import Any

from urload.commands.base import Command, CommandError
from urload.url import URL


class AddCommand(Command):
    """Appends a URL to the shared URL list."""

    name = "add"
    description = textwrap.dedent("""
    add <url> - Add a URL to the list.

    This command appends the specified URL to the shared URL list. Supports range expansion with [start-end] syntax.
    """)

    def run(
        self, args: list[str], url_list: list[URL], settings: Any = None
    ) -> list[URL]:
        """Append a URL or URLs (with range expansion) to the list if provided."""
        if not args:
            raise CommandError("Error: No URL provided.")
        url = args[0]
        # Find all [start-end] patterns
        pattern = re.compile(r"\[(\d+)-(\d+)\]")
        matches: list[re.Match[str]] = list(pattern.finditer(url))
        if not matches:
            url_obj = URL(url)
            url_list.append(url_obj)
            return url_list
        # For each match, build the list of values (with padding)
        ranges: list[list[str]] = []
        for m in matches:
            start_str, end_str = m.group(1), m.group(2)
            width = len(start_str)
            start, end = int(start_str), int(end_str)
            if end < start:
                raise CommandError(f"Range start ({start}) greater than end ({end})")
            rng = [str(i).zfill(width) for i in range(start, end + 1)]
            ranges.append(rng)
        # Build all combinations
        for combo in product(*ranges):
            new_url = url
            for m, val in zip(reversed(matches), reversed(list(combo))):
                # Replace from the end to avoid offset issues
                new_url = new_url[: m.start()] + val + new_url[m.end() :]
            url_obj = URL(new_url)
            url_list.append(url_obj)
        return url_list
