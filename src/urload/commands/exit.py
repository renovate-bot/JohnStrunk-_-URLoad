"""Implements the 'exit' command for URLoad."""

import textwrap

from urload.commands.base import Command
from urload.url import URL


class ExitCommand(Command):
    """Exits the URLoad application."""

    name = "exit"
    description = textwrap.dedent("""
    Usage: exit - Exit the application.

    This command exits the URLoad interactive session.
    """)

    def run(self, args: list[str], url_list: list[URL]) -> list[URL]:
        """Exit the application."""
        print("Goodbye!")
        raise SystemExit(0)
