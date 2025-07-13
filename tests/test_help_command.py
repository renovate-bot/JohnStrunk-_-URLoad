"""Tests for the HelpCommand."""

from pytest import CaptureFixture

from urload.commands.base import Command
from urload.commands.help import HelpCommand
from urload.url import URL


class DummyCommand(Command):
    """Dummy command for testing."""

    name = "dummy"
    description = "Dummy command."

    def run(self, args: list[str], url_list: list[URL]) -> list[URL]:
        """No-op for testing."""
        return url_list


def test_help_lists_commands(capsys: CaptureFixture[str]) -> None:
    """Test that help with no args lists all commands."""
    commands: dict[str, Command] = {"dummy": DummyCommand()}
    help_cmd = HelpCommand(commands)
    help_cmd.run([], [])
    captured = capsys.readouterr()
    assert "Dummy command." in captured.out
    assert "Available commands" in captured.out


def test_help_specific_command(capsys: CaptureFixture[str]) -> None:
    """Test that help with a valid command shows its help text."""
    commands: dict[str, Command] = {"dummy": DummyCommand()}
    help_cmd = HelpCommand(commands)
    help_cmd.run(["dummy"], [])
    captured = capsys.readouterr()
    assert "Dummy command." in captured.out


def test_help_unknown_command(capsys: CaptureFixture[str]) -> None:
    """Test that help with an unknown command shows an error."""
    commands: dict[str, Command] = {"dummy": DummyCommand()}
    help_cmd = HelpCommand(commands)
    help_cmd.run(["notfound"], [])
    captured = capsys.readouterr()
    assert "No such command" in captured.out
