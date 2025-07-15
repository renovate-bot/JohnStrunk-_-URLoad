"""fileformat - Get or set the filename template used for saving URLs."""

import textwrap
from typing import Any

from urload.commands.base import Command, CommandError
from urload.settings import get_active_settings


class FileformatCommand(Command):
    """Get or set the filename template used for saving URLs."""

    name = "fileformat"
    description = textwrap.dedent(
        """
    fileformat [<template>] - Get or set the filename template for saving URLs.

    With no arguments, prints the current filename template (used with str.format).
    With a single argument, sets the filename template (must be valid for str.format).
    Valid template parameters: timestamp, basename, ext, host, dirname, filename
    """
    )

    def run(self, args: list[str], url_list: list[Any]) -> list[Any]:
        """
        Get or set the filename template in settings.

        :param args: [] to print, [<template>] to set
        :param url_list: Unused
        :raises CommandError: If more than one argument or invalid template
        :return: url_list unchanged
        """
        settings = get_active_settings()
        if not args:
            print(settings.filename_template)
            return url_list
        if len(args) > 1:
            raise CommandError("fileformat takes at most one argument.")
        template = args[0]
        # Validate template by formatting with dummy values
        try:
            template.format(
                timestamp="20250101T120000",
                basename="file",
                ext="txt",
                host="example.com",
                dirname="foo/bar",
                filename="file.txt",
            )
        except Exception as e:
            raise CommandError(f"Invalid filename template: {e}")
        settings.filename_template = template
        print(f"Filename template set to: {template}")
        return url_list
