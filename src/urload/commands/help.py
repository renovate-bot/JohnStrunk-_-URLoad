"""Implements the 'help' command for URLoad."""

import textwrap

from urload.commands.base import Command


class HelpCommand(Command):
    """Provides help for URLoad commands."""

    name = "help"
    description = textwrap.dedent("""
    Usage: help [command] - Show help for a command.

    With no arguments, lists all available commands. With a command name,
    shows detailed help for that command.
    """)

    def __init__(self, commands: dict[str, Command]) -> None:
        """Initialize HelpCommand with a command registry."""
        self.commands = commands

    def run(self, args: list[str]) -> None:
        """Show help for all commands or a specific command."""
        if not args:
            print("Available commands:")
            for cmd in sorted(self.commands):
                print(
                    f"  {cmd}: {self.commands[cmd].description.splitlines()[0].strip()}"
                )
            print("Type 'help <command>' for more info.")
        else:
            cmd = args[0]
            if cmd in self.commands:
                print(self.commands[cmd].help())
            else:
                print(f"No such command: {cmd}")
