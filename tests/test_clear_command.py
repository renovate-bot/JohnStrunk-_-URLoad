"""Tests for the clear command."""

import pytest

from urload.commands.base import CommandError
from urload.commands.clear import ClearCommand
from urload.url import URL


def test_clear_command_empties_list() -> None:
    """Test that clear command returns an empty list."""
    cmd = ClearCommand()
    url_list = [URL("https://a.com"), URL("https://b.com")]
    result = cmd.run([], url_list)
    assert result == []


def test_clear_command_takes_no_args() -> None:
    """Test that passing arguments raises CommandError."""
    cmd = ClearCommand()
    with pytest.raises(CommandError):
        cmd.run(["unexpected"], [URL("https://x.com")])


def test_clear_command_does_not_mutate_input() -> None:
    """Test that the input list is not mutated by clear command."""
    cmd = ClearCommand()
    url_list = [URL("https://a.com")]
    url_list_copy = url_list.copy()
    cmd.run([], url_list)
    assert url_list == url_list_copy
