"""Implements the 'scrape' command for URLoad."""

import textwrap

from urload.commands.base import Command


class ScrapeCommand(Command):
    """Placeholder for the scrape command."""

    name = "scrape"
    description = textwrap.dedent("""
    Usage: scrape <url> - Scrape a website.

    This command scrapes the content of the specified URL and processes it.
    """)

    def run(self, args: list[str]) -> None:
        """Run the scrape command (not yet implemented)."""
        print("Scraping not yet implemented.")
