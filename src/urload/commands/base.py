"""Base class and interface for URLoad commands."""

from abc import ABC, abstractmethod

from urload.url import URL


class Command(ABC):
    """Abstract base class for all URLoad commands."""

    name: str
    description: str

    @abstractmethod
    def run(self, args: list[str], url_list: list[URL]) -> list[URL]:
        """
        Execute the command with the given arguments and URL list, returning the modified list.

        :param args: List of command-line arguments.
        :param url_list: List of URL objects to process.
        :return: A new list of URL objects after command execution.
        :raises CommandError: If a user-facing error occurs.
        """
        pass

    def help(self) -> str:
        """Return a help string describing the command."""
        return self.description


class CommandError(Exception):
    """Exception raised for errors in URLoad commands."""

    pass
