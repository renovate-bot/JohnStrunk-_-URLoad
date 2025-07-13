"""Tests for the HeadCommand."""

import pytest

from urload.commands.base import CommandError
from urload.commands.head import HeadCommand
from urload.url import URL


def test_head_command_keeps_first_n_urls() -> None:
    """Test that HeadCommand keeps the first n URLs."""
    cmd = HeadCommand()
    url_list = [URL("https://a.com"), URL("https://b.com"), URL("https://c.com")]
    result = cmd.run(["2"], url_list)
    assert result == [URL("https://a.com"), URL("https://b.com")]
    # Original list should be unchanged
    assert url_list == [
        URL("https://a.com"),
        URL("https://b.com"),
        URL("https://c.com"),
    ]


def test_head_command_n_equals_list_length() -> None:
    """Test HeadCommand when n equals the list length."""
    cmd = HeadCommand()
    url_list = [URL("https://a.com"), URL("https://b.com")]
    result = cmd.run(["2"], url_list)
    assert result == url_list
    assert result is not url_list  # Should return a new list


def test_head_command_n_greater_than_list_length() -> None:
    """Test HeadCommand when n is greater than the list length."""
    cmd = HeadCommand()
    url_list = [URL("https://a.com"), URL("https://b.com")]
    result = cmd.run(["5"], url_list)
    assert result == url_list
    assert result is not url_list  # Should return a new list


def test_head_command_n_zero() -> None:
    """Test HeadCommand with n=0."""
    cmd = HeadCommand()
    url_list = [URL("https://a.com"), URL("https://b.com")]
    result = cmd.run(["0"], url_list)
    assert result == []


def test_head_command_n_one() -> None:
    """Test HeadCommand with n=1."""
    cmd = HeadCommand()
    url_list = [URL("https://a.com"), URL("https://b.com"), URL("https://c.com")]
    result = cmd.run(["1"], url_list)
    assert result == [URL("https://a.com")]


def test_head_command_empty_list() -> None:
    """Test HeadCommand with an empty list."""
    cmd = HeadCommand()
    url_list: list[URL] = []
    result = cmd.run(["3"], url_list)
    assert result == []


def test_head_command_no_args() -> None:
    """Test that no arguments raises CommandError."""
    cmd = HeadCommand()
    url_list = [URL("https://a.com")]
    with pytest.raises(CommandError, match="No count provided."):
        cmd.run([], url_list)


def test_head_command_non_integer_arg() -> None:
    """Test that a non-integer argument raises CommandError."""
    cmd = HeadCommand()
    url_list = [URL("https://a.com"), URL("https://b.com")]
    with pytest.raises(CommandError, match="Invalid count. Must be an integer."):
        cmd.run(["foo"], url_list)


def test_head_command_negative_n() -> None:
    """Test that a negative count raises CommandError."""
    cmd = HeadCommand()
    url_list = [URL("https://a.com"), URL("https://b.com")]
    with pytest.raises(CommandError, match="Count must be non-negative."):
        cmd.run(["-1"], url_list)


def test_head_command_float_arg() -> None:
    """Test that a float argument raises CommandError."""
    cmd = HeadCommand()
    url_list = [URL("https://a.com"), URL("https://b.com")]
    with pytest.raises(CommandError, match="Invalid count. Must be an integer."):
        cmd.run(["2.5"], url_list)
