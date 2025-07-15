"""Tests for the URLoad command base class, command interface, and error handling."""

from typing import Any

import pytest

from urload.commands.base import Command, CommandError
from urload.url import URL


class DummyCommand(Command):
    """Dummy command for testing."""

    name = "dummy"
    description = "Dummy command for testing.\nSecond line."

    def run(
        self, args: list[str], url_list: list[URL], settings: Any | None = None
    ) -> list[URL]:
        """Raise CommandError if 'error' is in args, else store args and return url_list unchanged."""
        if "error" in args:
            raise CommandError("Dummy error!")
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


def test_dummy_command_raises_on_error() -> None:
    """Test that DummyCommand raises CommandError if 'error' is in args."""
    cmd = DummyCommand()
    with pytest.raises(CommandError, match="Dummy error!"):
        cmd.run(["error"], [])


def test_dummy_command_success_does_not_raise() -> None:
    """Test that DummyCommand does not raise when 'error' is not in args."""
    cmd = DummyCommand()
    try:
        result = cmd.run(["https://example.com"], [])
    except CommandError:
        pytest.fail("CommandError was raised unexpectedly!")
    assert result == []
