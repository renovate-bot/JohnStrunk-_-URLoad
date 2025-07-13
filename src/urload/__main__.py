"""
URLoad interactive CLI main module.

This module provides the entry point for the URLoad application, an interactive
command-line tool for scraping websites with tab completion and history support.
"""

from typing import Any

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory

from urload.commands.add import AddCommand
from urload.commands.base import Command
from urload.commands.exit import ExitCommand
from urload.commands.help import HelpCommand
from urload.commands.list import ListCommand
from urload.commands.scrape import ScrapeCommand
from urload.url import URL


def main() -> None:
    """
    Entry point for the URLoad interactive CLI application.

    Provides a prompt with tab completion and history support.
    """
    url_list: list[URL] = []
    # Register commands
    command_objs: dict[str, Command] = {}
    command_objs["exit"] = ExitCommand()
    command_objs["help"] = HelpCommand(command_objs)
    command_objs["scrape"] = ScrapeCommand()
    command_objs["add"] = AddCommand()
    command_objs["list"] = ListCommand()

    completer: WordCompleter = WordCompleter(
        list(command_objs.keys()), ignore_case=True
    )
    history: InMemoryHistory = InMemoryHistory()
    session: PromptSession[Any] = PromptSession(completer=completer, history=history)

    print("Welcome to URLoad! Type 'help' for commands.")
    while True:
        try:
            user_input = session.prompt("URLoad> ")
            if not isinstance(user_input, str):
                print("Invalid input.")
                continue
            parts = user_input.strip().split()
            if not parts:
                continue
            cmd, *args = parts
            if cmd in command_objs:
                try:
                    url_list = command_objs[cmd].run(args, url_list)
                except SystemExit:
                    break
                except Exception as e:
                    print(e)
            else:
                print(f"Unknown command: {cmd}")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
