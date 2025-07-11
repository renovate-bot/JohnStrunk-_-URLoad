"""Base class and interface for URLoad commands."""

from abc import ABC, abstractmethod


class Command(ABC):
    """Abstract base class for all URLoad commands."""

    name: str
    description: str

    @abstractmethod
    def run(self, args: list[str]) -> None:
        """Execute the command with the given arguments."""
        pass

    def help(self) -> str:
        """Return a help string describing the command."""
        return self.description
