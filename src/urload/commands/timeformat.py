"""timeformat - Get or set the current time format string used for datetime formatting."""

import textwrap
from datetime import datetime
from typing import Any

from urload.commands.base import Command, CommandError
from urload.settings import AppSettings


class TimeformatCommand(Command):
    """Get or set the current time format string used for datetime formatting."""

    name = "timeformat"
    description = textwrap.dedent("""
    timeformat [<format>] - Get or set the current time format string.

    With no arguments, prints the current time format template (used for strftime).
    With a single argument, sets the time format string (must be valid for strftime).
    Default: "%Y%m%d%H%M%S"
    """)

    def run(
        self, args: list[str], url_list: list[Any], settings: AppSettings
    ) -> list[Any]:
        """
        Get or set the current time format string in settings.

        :param args: [] to print, [<format>] to set
        :param url_list: Unused
        :param settings: The AppSettings object
        :raises CommandError: If more than one argument or invalid format string
        :return: url_list unchanged
        """
        if not args:
            print(getattr(settings, "time_format", "%Y%m%d%H%M%S"))
            return url_list
        if len(args) > 1:
            raise CommandError("timeformat takes at most one argument.")
        fmt = args[0]
        # Validate format string by trying to format now
        try:
            test = datetime.now().strftime(fmt)
            if "%Q" in fmt or test == fmt:
                raise ValueError("Invalid or unsupported strftime format code.")
        except Exception as e:
            raise CommandError(f"Invalid time format: {e}")
        setattr(settings, "time_format", fmt)
        print(f"Time format set to: {fmt}")
        return url_list
