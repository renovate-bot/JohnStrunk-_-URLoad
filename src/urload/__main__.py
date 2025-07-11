"""
URLoad interactive CLI main module.

This module provides the entry point for the URLoad application, an interactive
command-line tool for scraping websites with tab completion and history support.
"""

from typing import Any

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory


def main() -> None:
    """
    Entry point for the URLoad interactive CLI application.

    Provides a prompt with tab completion and history support.
    """
    commands: list[str] = ["scrape", "exit", "help"]
    completer: WordCompleter = WordCompleter(commands, ignore_case=True)
    history: InMemoryHistory = InMemoryHistory()
    session: PromptSession[Any] = PromptSession(completer=completer, history=history)

    print("Welcome to URLoad! Type 'help' for commands.")
    while True:
        try:
            user_input = session.prompt("URLoad> ")
            if isinstance(user_input, str):
                if user_input.strip() == "exit":
                    print("Goodbye!")
                    break
                elif user_input.strip() == "help":
                    print("Available commands: scrape, help, exit")
                elif user_input.strip().startswith("scrape"):
                    print("Scraping not yet implemented.")
                elif user_input.strip() == "":
                    continue
                else:
                    print(f"Unknown command: {user_input}")
            else:
                print("Invalid input.")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
