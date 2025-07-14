"""Clears the current URL list."""

import textwrap

from urload.commands.base import Command, CommandError
from urload.url import URL


class ClearCommand(Command):
    """Clear the current URL list."""

    name = "clear"
    description = textwrap.dedent(
        """
        clear - Clear the current URL list

        Removes all URLs from the list, leaving it empty.
        """
    )

    def run(self, args: list[str], url_list: list[URL]) -> list[URL]:
        """
        Clear the current URL list.

        :param args: List of command-line arguments (must be empty).
        :param url_list: List of URL objects to clear.
        :return: An empty list.
        :raises CommandError: If arguments are provided.
        """
        if args:
            raise CommandError("clear command takes no arguments.")
        return []
