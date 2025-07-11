"""Tests for the HelpCommand."""

from urload.commands.base import Command
from urload.commands.help import HelpCommand


class DummyCommand(Command):
    """Dummy command for testing."""

    name = "dummy"
    description = "Dummy command."

    def run(self, args: list[str]) -> None:
        """No-op for testing."""
        pass


def test_help_lists_commands(capsys) -> None:
    """Test that help with no args lists all commands."""
    commands = {"dummy": DummyCommand()}
    help_cmd = HelpCommand(commands)
    help_cmd.run([])
    captured = capsys.readouterr()
    assert "dummy" in captured.out
    assert "Available commands" in captured.out


def test_help_specific_command(capsys) -> None:
    """Test that help with a valid command shows its help text."""
    commands = {"dummy": DummyCommand()}
    help_cmd = HelpCommand(commands)
    help_cmd.run(["dummy"])
    captured = capsys.readouterr()
    assert "Dummy command." in captured.out


def test_help_unknown_command(capsys) -> None:
    """Test that help with an unknown command shows an error."""
    commands = {"dummy": DummyCommand()}
    help_cmd = HelpCommand(commands)
    help_cmd.run(["notfound"])
    captured = capsys.readouterr()
    assert "No such command" in captured.out
