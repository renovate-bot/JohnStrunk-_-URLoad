"""Tests for the AddCommand."""

import pytest

from urload.commands.add import AddCommand
from urload.commands.base import CommandError
from urload.url import URL


def test_add_command_appends_url(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that AddCommand appends a URL to the list."""
    cmd = AddCommand()
    url_list: list[URL] = []
    result = cmd.run(["https://example.com"], url_list)
    assert len(result) == 1
    assert result[0].url == "https://example.com"


def test_add_command_no_args() -> None:
    """Test that AddCommand raises CommandError if no URL is provided and does not modify the list."""
    cmd = AddCommand()
    url_list: list[URL] = []
    with pytest.raises(CommandError, match="No URL provided"):
        cmd.run([], url_list)


def test_add_command_single_range() -> None:
    """Test that AddCommand expands a single range."""
    cmd = AddCommand()
    url_list: list[URL] = []
    result = cmd.run(["https://example.com/file[2-4].txt"], url_list)
    urls = [u.url for u in result]
    assert urls[-3:] == [
        "https://example.com/file2.txt",
        "https://example.com/file3.txt",
        "https://example.com/file4.txt",
    ]


def test_add_command_range_with_leading_zeros() -> None:
    """Test that AddCommand expands a range with leading zeros."""
    cmd = AddCommand()
    url_list: list[URL] = []
    result = cmd.run(["https://ex.com/file[08-10].dat"], url_list)
    urls = [u.url for u in result]
    assert urls[-3:] == [
        "https://ex.com/file08.dat",
        "https://ex.com/file09.dat",
        "https://ex.com/file10.dat",
    ]


def test_add_command_multiple_ranges() -> None:
    """Test that AddCommand expands multiple ranges in nested fashion."""
    cmd = AddCommand()
    url_list: list[URL] = []
    result = cmd.run(["https://ex.com/f[1-2]/b[3-4].dat"], url_list)
    urls = [u.url for u in result]
    assert urls[-4:] == [
        "https://ex.com/f1/b3.dat",
        "https://ex.com/f1/b4.dat",
        "https://ex.com/f2/b3.dat",
        "https://ex.com/f2/b4.dat",
    ]


def test_add_command_range_start_greater_than_end() -> None:
    """Test that AddCommand raises CommandError if range start > end."""
    cmd = AddCommand()
    url_list: list[URL] = []
    with pytest.raises(CommandError, match=r"Range start \(5\) greater than end \(2\)"):
        cmd.run(["https://ex.com/file[5-2].dat"], url_list)


def test_add_command_multiple_ranges_leading_zeros() -> None:
    """Test that AddCommand expands multiple ranges with leading zeros."""
    cmd = AddCommand()
    url_list: list[URL] = []
    result = cmd.run(["https://ex.com/f[01-02]/b[003-004].dat"], url_list)
    urls = [u.url for u in result]
    assert urls[-4:] == [
        "https://ex.com/f01/b003.dat",
        "https://ex.com/f01/b004.dat",
        "https://ex.com/f02/b003.dat",
        "https://ex.com/f02/b004.dat",
    ]
