"""Implements the 'exit' command for URLoad."""

import textwrap

from urload.commands.base import Command


class ExitCommand(Command):
    """Exits the URLoad application."""

    name = "exit"
    description = textwrap.dedent("""
    Usage: exit - Exit the application.

    This command exits the URLoad interactive session.
    """)

    def run(self, args: list[str]) -> None:
        """Exit the application."""
        print("Goodbye!")
        raise SystemExit(0)
