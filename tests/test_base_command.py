"""Tests for the URLoad command base class and command interface."""

from urload.commands.base import Command
from urload.url import URL


class DummyCommand(Command):
    """Dummy command for testing."""

    name = "dummy"
    description = "Dummy command for testing.\nSecond line."

    def run(self, args: list[str], url_list: list[URL]) -> list[URL]:
        """Store the received arguments for verification and return the url_list unchanged."""
        self.last_args = args
        return url_list


def test_help_returns_description() -> None:
    """Test that help() returns the command description."""
    cmd = DummyCommand()
    assert cmd.help() == "Dummy command for testing.\nSecond line."


def test_run_receives_args() -> None:
    """Test that run() receives and stores the arguments."""
    cmd = DummyCommand()
    args = ["foo", "bar"]
    cmd.run(args, [])
    assert getattr(cmd, "last_args", None) == args
