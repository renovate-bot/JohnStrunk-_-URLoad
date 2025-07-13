"""Base class and interface for URLoad commands."""

from abc import ABC, abstractmethod

from urload.url import URL


class Command(ABC):
    """Abstract base class for all URLoad commands."""

    name: str
    description: str

    @abstractmethod
    def run(self, args: list[str], url_list: list[URL]) -> list[URL]:
        """Execute the command with the given arguments and URL list, returning the modified list."""
        pass

    def help(self) -> str:
        """Return a help string describing the command."""
        return self.description


class CommandError(Exception):
    """Exception raised for errors in URLoad commands."""

    pass
