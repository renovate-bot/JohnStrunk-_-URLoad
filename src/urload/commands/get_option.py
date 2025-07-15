"""
get-option [<key>] - Get application settings.

Print all application settings as key=value, or a single key if specified.
"""

import textwrap

from urload.commands.base import Command, CommandError
from urload.settings import AppSettings
from urload.url import URL


class GetOptionCommand(Command):
    """
    Get application settings.

    :param args: Optionally a single key to print.
    :param url_list: Not used.
    :param settings: The AppSettings object.
    :raises CommandError: If the key is unknown.
    """

    name = "get-option"
    description = textwrap.dedent("""
    get-option [<key>] - Get application settings.

    Print all application settings as key=value, or a single key if specified.
    """)

    def run(
        self, args: list[str], url_list: list[URL], settings: AppSettings
    ) -> list[URL]:
        """Print all settings as key=value, or a single key if specified."""
        valid_keys = set(AppSettings.model_fields.keys())
        if not args:
            for key, value in settings.model_dump().items():
                print(f"{key}={value}")
        elif len(args) == 1:
            key = args[0]
            if key not in valid_keys:
                raise CommandError(f"Unknown setting: {key}")
            print(f"{key}={getattr(settings, key)}")
        else:
            raise CommandError("Usage: get-option [<key>]")
        return url_list
