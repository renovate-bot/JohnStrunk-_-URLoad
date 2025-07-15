"""Save the current list of URLs (with optional headers) to a text file."""

import textwrap

from urload.commands.base import Command, CommandError
from urload.url import URL


class SaveCommand(Command):
    """Save the current list of URLs (with optional headers) to a text file."""

    name = "save"
    description = textwrap.dedent(
        """
        save <filename> - Save URLs to a file

        Saves the current list of URLs (with optional headers) to the specified file. Each line will contain a URL, optionally followed by headers in a structured format.
        """
    )

    def run(self, args: list[str], url_list: list[URL]) -> list[URL]:
        """
        Save URLs to a file.

        :param args: List of command-line arguments (expects one filename).
        :param url_list: List of URL objects to save.
        :return: The input list of URL objects (unchanged).
        :raises CommandError: If arguments are invalid or file cannot be written.
        """
        if len(args) != 1:
            raise CommandError("save command requires exactly one filename argument.")
        filename = args[0]
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for url in url_list:
                    f.write(url.serialize() + "\n")
        except Exception as e:
            raise CommandError(f"Could not write file: {e}")
        print(f"Saved {len(url_list)} URLs to {filename}.")
        return url_list
