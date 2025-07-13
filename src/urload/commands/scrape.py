"""Implements the 'scrape' command for URLoad."""

import textwrap

from urload.commands.base import Command
from urload.url import URL


class ScrapeCommand(Command):
    """Placeholder for the scrape command."""

    name = "scrape"
    description = textwrap.dedent("""
    scrape <url> - Scrape a website.

    This command scrapes the content of the specified URL and processes it.
    """)

    def run(self, args: list[str], url_list: list[URL]) -> list[URL]:
        """Run the scrape command (not yet implemented)."""
        print("Scraping not yet implemented.")
        return url_list
