"""
URLoad interactive CLI main module.

This module provides the entry point for the URLoad application, an interactive
command-line tool for scraping websites with tab completion and history support.
"""

from collections.abc import Generator
from typing import Any

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.history import InMemoryHistory

from urload.commands.add import AddCommand
from urload.commands.base import Command
from urload.commands.delete import DeleteCommand
from urload.commands.discard import DiscardCommand
from urload.commands.exit import ExitCommand
from urload.commands.head import HeadCommand
from urload.commands.help import HelpCommand
from urload.commands.href import HrefCommand
from urload.commands.img import ImgCommand
from urload.commands.keep import KeepCommand
from urload.commands.list import ListCommand
from urload.commands.sort import SortCommand
from urload.commands.tail import TailCommand
from urload.commands.uniq import UniqCommand
from urload.url import URL

HELP_ARG_COUNT = 2


class CommandCompleter(Completer):
    """Custom completer for URLoad commands.

    Only completes command names at the start of the line, or as the first argument to 'help'.
    """

    def __init__(self, commands: list[str]):
        """Initialize with a list of command names."""
        self.commands = commands

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Generator[Completion, None, None]:
        """Yield completions for command names at the start or as help argument."""
        text = document.text_before_cursor
        lstripped = text.lstrip()
        parts = lstripped.split()
        word = document.get_word_before_cursor(WORD=True)

        # Special case: 'help ' (with a space and no argument) should yield all completions
        if lstripped == "help ":
            yield from (Completion(cmd, start_position=0) for cmd in self.commands)
            return

        # If the input is exactly a command and a space, do not complete
        if any(lstripped == f"{cmd} " for cmd in self.commands):
            return

        # For help, if input is 'help <cmd> ', do not complete (but not for just 'help ')
        if (
            len(parts) == HELP_ARG_COUNT
            and parts[0] == "help"
            and lstripped.endswith(" ")
            and parts[1] in self.commands
            and parts[1] != ""
        ):
            return

        # Complete command names at the start or if only partial command is typed
        if not parts or (len(parts) == 1 and text.rstrip() == parts[0]):
            yield from (
                Completion(cmd, start_position=-len(word))
                for cmd in self.commands
                if cmd.startswith(word)
            )
            return

        # Complete command names as argument to help
        if parts[0] == "help":
            if len(parts) == 1:
                yield from (Completion(cmd, start_position=0) for cmd in self.commands)
            elif len(parts) == HELP_ARG_COUNT and text.rstrip().endswith(parts[1]):
                arg = word if len(parts) > 1 else ""
                yield from (
                    Completion(cmd, start_position=-len(arg))
                    for cmd in self.commands
                    if cmd.startswith(arg)
                )
            return
        # Otherwise, do not complete command names as arguments
        return


def main() -> None:
    """
    Entry point for the URLoad interactive CLI application.

    Provides a prompt with tab completion and history support.
    """
    url_list: list[URL] = []
    # Register commands. Keep this dictionary sorted by command name and in
    # sync with the command files in src/urload/commands.
    command_objs: dict[str, Command] = {}
    command_objs["add"] = AddCommand()
    command_objs["del"] = DeleteCommand()
    command_objs["discard"] = DiscardCommand()
    command_objs["exit"] = ExitCommand()
    command_objs["head"] = HeadCommand()
    command_objs["help"] = HelpCommand(command_objs)
    command_objs["href"] = HrefCommand()
    command_objs["img"] = ImgCommand()
    command_objs["keep"] = KeepCommand()
    command_objs["list"] = ListCommand()
    command_objs["sort"] = SortCommand()
    command_objs["tail"] = TailCommand()
    command_objs["uniq"] = UniqCommand()

    completer = CommandCompleter(list(command_objs.keys()))
    history: InMemoryHistory = InMemoryHistory()
    session: PromptSession[Any] = PromptSession(completer=completer, history=history)

    print("Welcome to URLoad! Type 'help' for commands.")
    while True:
        try:
            prompt_str = f"URLoad ({len(url_list)}) > "
            user_input = session.prompt(prompt_str)
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
