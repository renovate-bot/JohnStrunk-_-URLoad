"""Tests for the DelCommand."""

import pytest

from urload.commands.delete import CommandError, DelCommand
from urload.url import URL


def test_del_command_single_index(capsys: pytest.CaptureFixture[str]) -> None:
    """Test deleting a single URL by index."""
    cmd = DelCommand()
    url_list = [URL("https://a.com"), URL("https://b.com"), URL("https://c.com")]
    result = cmd.run(["1"], url_list)
    captured = capsys.readouterr()
    assert result == [URL("https://a.com"), URL("https://c.com")]
    assert "Deleted URL at index 1." in captured.out


def test_del_command_range(capsys: pytest.CaptureFixture[str]) -> None:
    """Test deleting a range of URLs by index."""
    cmd = DelCommand()
    url_list = [
        URL("https://a.com"),
        URL("https://b.com"),
        URL("https://c.com"),
        URL("https://d.com"),
    ]
    result = cmd.run(["1-2"], url_list)
    captured = capsys.readouterr()
    assert result == [URL("https://a.com"), URL("https://d.com")]
    assert "Deleted URLs from index 1 to 2." in captured.out


def test_del_command_range_with_spaces(capsys: pytest.CaptureFixture[str]) -> None:
    """Test deleting a range with spaces in the argument."""
    cmd = DelCommand()
    url_list = [
        URL("https://a.com"),
        URL("https://b.com"),
        URL("https://c.com"),
        URL("https://d.com"),
    ]
    result = cmd.run(["1 - 2"], url_list)
    captured = capsys.readouterr()
    assert result == [URL("https://a.com"), URL("https://d.com")]
    assert "Deleted URLs from index 1 to 2." in captured.out


def test_del_command_invalid_index() -> None:
    """Test that an invalid index raises CommandError."""
    cmd = DelCommand()
    url_list = [URL("https://a.com")]
    with pytest.raises(Exception):
        cmd.run(["5"], url_list)


def test_del_command_invalid_range() -> None:
    """Test that an invalid range raises CommandError."""
    cmd = DelCommand()
    url_list = [URL("https://a.com"), URL("https://b.com")]
    with pytest.raises(Exception):
        cmd.run(["2-5"], url_list)


def test_del_command_no_args() -> None:
    """Test that no arguments raises CommandError."""
    cmd = DelCommand()
    url_list = [URL("https://a.com")]
    with pytest.raises(Exception):
        cmd.run([], url_list)


def test_del_command_non_integer_index() -> None:
    """Test that a non-integer index raises CommandError."""
    cmd = DelCommand()
    url_list = [URL("https://a.com"), URL("https://b.com")]
    with pytest.raises(CommandError, match="Invalid index."):
        cmd.run(["foo"], url_list)
