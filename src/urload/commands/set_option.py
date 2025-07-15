"""
set-option <key>=<value> - Set an application setting.

Set an application setting (such as filename_template) to a new value. The change is saved to the config file.
"""

import textwrap

from urload.commands.base import Command, CommandError
from urload.settings import AppSettings
from urload.url import URL


class SetOptionCommand(Command):
    """
    Set an application setting to a new value.

    :param args: Should be a single argument of the form key=value.
    :param url_list: Not used.
    :param settings: The AppSettings object.
    :raises CommandError: If the argument is missing or invalid.
    """

    name = "set-option"
    description = textwrap.dedent("""
    set-option <key>=<value> - Set an application setting.

    Set an application setting (such as filename_template) to a new value. The change is saved to the config file.
    """)

    def run(
        self, args: list[str], url_list: list[URL], settings: AppSettings
    ) -> list[URL]:
        """Set a setting from key=value argument. Does not save to disk."""
        if len(args) != 1 or "=" not in args[0]:
            raise CommandError("Usage: set-option <key>=<value>")
        key, value = args[0].split("=", 1)
        key = key.strip()
        value = value.strip()
        valid_keys = set(AppSettings.model_fields.keys())
        if key not in valid_keys:
            raise CommandError(f"Unknown setting: {key}")
        setattr(settings, key, value)
        print(f"{key} set to {value}")
        return url_list
