"""Tests for the TailCommand."""

import pytest

from urload.commands.base import CommandError
from urload.commands.tail import TailCommand
from urload.url import URL


def test_tail_command_keeps_last_n_urls() -> None:
    """Test that TailCommand keeps the last n URLs."""
    cmd = TailCommand()
    url_list = [URL("https://a.com"), URL("https://b.com"), URL("https://c.com")]
    result = cmd.run(["2"], url_list)
    assert result == [URL("https://b.com"), URL("https://c.com")]
    # Original list should be unchanged
    assert url_list == [
        URL("https://a.com"),
        URL("https://b.com"),
        URL("https://c.com"),
    ]


def test_tail_command_n_equals_list_length() -> None:
    """Test TailCommand when n equals the list length."""
    cmd = TailCommand()
    url_list = [URL("https://a.com"), URL("https://b.com")]
    result = cmd.run(["2"], url_list)
    assert result == url_list
    assert result is not url_list  # Should return a new list


def test_tail_command_n_greater_than_list_length() -> None:
    """Test TailCommand when n is greater than the list length."""
    cmd = TailCommand()
    url_list = [URL("https://a.com"), URL("https://b.com")]
    result = cmd.run(["5"], url_list)
    assert result == url_list
    assert result is not url_list  # Should return a new list


def test_tail_command_n_zero() -> None:
    """Test TailCommand with n=0."""
    cmd = TailCommand()
    url_list = [URL("https://a.com"), URL("https://b.com")]
    result = cmd.run(["0"], url_list)
    assert result == []


def test_tail_command_n_one() -> None:
    """Test TailCommand with n=1."""
    cmd = TailCommand()
    url_list = [URL("https://a.com"), URL("https://b.com"), URL("https://c.com")]
    result = cmd.run(["1"], url_list)
    assert result == [URL("https://c.com")]


def test_tail_command_empty_list() -> None:
    """Test TailCommand with an empty list."""
    cmd = TailCommand()
    url_list: list[URL] = []
    result = cmd.run(["3"], url_list)
    assert result == []


def test_tail_command_no_args() -> None:
    """Test that no arguments raises CommandError."""
    cmd = TailCommand()
    url_list = [URL("https://a.com")]
    with pytest.raises(CommandError, match="No count provided."):
        cmd.run([], url_list)


def test_tail_command_non_integer_arg() -> None:
    """Test that a non-integer argument raises CommandError."""
    cmd = TailCommand()
    url_list = [URL("https://a.com"), URL("https://b.com")]
    with pytest.raises(CommandError, match="Invalid count. Must be an integer."):
        cmd.run(["foo"], url_list)


def test_tail_command_negative_n() -> None:
    """Test that a negative count raises CommandError."""
    cmd = TailCommand()
    url_list = [URL("https://a.com"), URL("https://b.com")]
    with pytest.raises(CommandError, match="Count must be non-negative."):
        cmd.run(["-1"], url_list)


def test_tail_command_float_arg() -> None:
    """Test that a float argument raises CommandError."""
    cmd = TailCommand()
    url_list = [URL("https://a.com"), URL("https://b.com")]
    with pytest.raises(CommandError, match="Invalid count. Must be an integer."):
        cmd.run(["2.5"], url_list)
