"""Implements the 'keep' command for URLoad."""

import re
import textwrap
from typing import Any

from urload.commands.base import Command, CommandError
from urload.url import URL


class KeepCommand(Command):
    """Keeps only URLs matching a regex pattern."""

    name = "keep"
    description = textwrap.dedent("""
    keep <regex> - Keep only URLs matching the regex pattern.

    This command keeps only the URLs in the list that match the given regex pattern.
    """)

    def run(
        self, args: list[str], url_list: list[URL], settings: Any = None
    ) -> list[URL]:
        """Keep only URLs matching the regex pattern."""
        if not args:
            raise CommandError("No regex pattern provided.")
        pattern = args[0]
        try:
            regex = re.compile(pattern)
        except re.error as e:
            raise CommandError(f"Invalid regex: {e}")
        kept = [url for url in url_list if regex.search(url.url)]
        print(f"Kept {len(kept)} URLs matching pattern.")
        return kept
