"""Tests for the URLoad command base class and command interface."""

from urload.commands.base import Command


class DummyCommand(Command):
    """Dummy command for testing."""

    name = "dummy"
    description = "Dummy command for testing.\nSecond line."

    def run(self, args: list[str]) -> None:
        """Store the received arguments for verification."""
        self.last_args = args


def test_help_returns_description() -> None:
    """Test that help() returns the command description."""
    cmd = DummyCommand()
    assert cmd.help() == "Dummy command for testing.\nSecond line."


def test_run_receives_args() -> None:
    """Test that run() receives and stores the arguments."""
    cmd = DummyCommand()
    args = ["foo", "bar"]
    cmd.run(args)
    assert getattr(cmd, "last_args", None) == args
