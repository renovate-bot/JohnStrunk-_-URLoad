"""Tests for the CommandCompleter class in the URLoad CLI."""

import pytest
from prompt_toolkit.completion import CompleteEvent
from prompt_toolkit.document import Document

from urload.main import CommandCompleter


@pytest.fixture
def commands() -> list[str]:
    """Return a list of command names for the completer."""
    return ["add", "del", "help", "list", "uniq"]


@pytest.fixture
def completer(commands: list[str]) -> CommandCompleter:
    """Return a CommandCompleter instance."""
    return CommandCompleter(commands)


@pytest.fixture
def event() -> CompleteEvent:
    """Return a CompleteEvent instance."""
    return CompleteEvent()


def get_completions(
    completer: CommandCompleter, text: str, event: CompleteEvent
) -> list[str]:
    """Return completion texts from the completer for a given input."""
    doc = Document(text=text, cursor_position=len(text))
    return [c.text for c in completer.get_completions(doc, event)]


def test_complete_at_start(completer: CommandCompleter, event: CompleteEvent) -> None:
    """Test that command names are completed at the start of the line."""
    assert set(get_completions(completer, "", event)) == {
        "add",
        "del",
        "help",
        "list",
        "uniq",
    }
    assert set(get_completions(completer, "a", event)) == {"add"}
    assert set(get_completions(completer, "he", event)) == {"help"}


def test_no_completion_after_command_and_space(
    completer: CommandCompleter, event: CompleteEvent
) -> None:
    """Test that no completions are offered after a command and a space."""
    assert get_completions(completer, "add ", event) == []
    assert get_completions(completer, "del ", event) == []
    assert get_completions(completer, "uniq ", event) == []


def test_help_argument_completion(
    completer: CommandCompleter, event: CompleteEvent
) -> None:
    """Test that help completes command names as its argument."""
    assert set(get_completions(completer, "help ", event)) == {
        "add",
        "del",
        "help",
        "list",
        "uniq",
    }
    assert set(get_completions(completer, "help a", event)) == {"add"}
    assert set(get_completions(completer, "help d", event)) == {"del"}
    assert set(get_completions(completer, "help u", event)) == {"uniq"}
    assert get_completions(completer, "help add ", event) == []


def test_no_completion_for_other_args(
    completer: CommandCompleter, event: CompleteEvent
) -> None:
    """Test that no completions are offered for arguments to other commands."""
    assert get_completions(completer, "add foo", event) == []
    assert get_completions(completer, "del 1", event) == []
    assert get_completions(completer, "uniq something", event) == []
