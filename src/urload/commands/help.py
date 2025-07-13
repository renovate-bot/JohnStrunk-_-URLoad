"""Implements the 'help' command for URLoad."""

import textwrap

from urload.commands.base import Command
from urload.url import URL


class HelpCommand(Command):
    """Provides help for URLoad commands."""

    name = "help"
    description = textwrap.dedent("""
    help [command] - Show help for a command.

    With no arguments, lists all available commands. With a command name,
    shows detailed help for that command.
    """)

    def __init__(self, commands: dict[str, Command]) -> None:
        """Initialize HelpCommand with a command registry."""
        self.commands = commands

    def run(self, args: list[str], url_list: list[URL]) -> list[URL]:
        """Show help for all commands or a specific command."""
        if not args:
            print("Available commands:")
            for cmd in sorted(self.commands):
                # Print only the first non-empty line of the description (short help)
                desc_lines = [
                    line.strip()
                    for line in self.commands[cmd].description.splitlines()
                    if line.strip()
                ]
                short_help = desc_lines[0] if desc_lines else ""
                print(f"  {short_help}")
            print("Type 'help <command>' for more info.")
        else:
            cmd = args[0]
            if cmd in self.commands:
                print(self.commands[cmd].help())
            else:
                print(f"No such command: {cmd}")
        return url_list
