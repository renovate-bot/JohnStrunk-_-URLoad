"""fileformat - Get or set the filename template used for saving URLs."""

import textwrap
from typing import Any

from urload.commands.base import Command, CommandError
from urload.settings import AppSettings


class FileformatCommand(Command):
    """Get or set the filename template used for saving URLs."""

    name = "fileformat"
    description = textwrap.dedent(
        """
    fileformat [<template>] - Get or set the filename template for saving URLs.

    With no arguments, prints the current filename template (used with str.format).
    With a single argument, sets the filename template (must be valid for str.format).

    Example template: {index:04d}_{basename}.{ext}

    Valid template parameters:
    - basename: The base name of the URL (without path or query).
    - dirname: The directory name of the URL.
    - ext: The file extension of the URL.
    - filename: The full filename (basename + ext).
    - host: The host part of the URL.
    - index: The index of the URL in the list (0-based).
    - timestamp: The current timestamp (see: `timeformat` command).
    """
    )

    def run(
        self, args: list[str], url_list: list[Any], settings: AppSettings
    ) -> list[Any]:
        """
        Get or set the filename template in settings.

        :param args: [] to print, [<template>] to set
        :param url_list: Unused
        :param settings: The AppSettings object
        :raises CommandError: If more than one argument or invalid template
        :return: url_list unchanged
        """
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
                index=0,
            )
        except Exception as e:
            raise CommandError(f"Invalid filename template: {e}")
        settings.filename_template = template
        print(f"Filename template set to: {template}")
        return url_list
