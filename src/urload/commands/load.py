"""Load a list of URLs (with optional headers) from a text file."""

import textwrap
from typing import Any

from urload.commands.base import Command, CommandError
from urload.url import URL


class LoadCommand(Command):
    """Load a list of URLs (with optional headers) from a text file."""

    name = "load"
    description = textwrap.dedent(
        """
        load <filename> - Load URLs from a file

        Loads a list of URLs (with optional headers) from the specified file. Each line should contain a URL, optionally followed by headers in a structured format. The loaded URLs are appended to the current list.
        """
    )

    def run(
        self, args: list[str], url_list: list[URL], settings: Any = None
    ) -> list[URL]:
        """
        Load URLs from a file, appending to the current list.

        :param args: List of command-line arguments (expects one filename).
        :param url_list: List of URL objects to process (existing list).
        :return: A new list of URL objects with loaded URLs appended.
        :raises CommandError: If arguments are invalid or file cannot be read/parsed.
        """
        if len(args) != 1:
            raise CommandError("load command requires exactly one filename argument.")
        filename = args[0]
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            raise CommandError(f"Could not read file: {e}")
        new_urls: list[URL] = []
        for i, raw_line in enumerate(lines, 1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                url = URL.deserialize(line)
            except Exception as e:
                raise CommandError(f"Error parsing line {i}: {e}")
            new_urls.append(url)
        print(f"Loaded {len(new_urls)} URLs from {filename}.")
        return url_list + new_urls
