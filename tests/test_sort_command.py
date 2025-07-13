"""Tests for the SortCommand."""

import pytest

from urload.commands.sort import SortCommand
from urload.url import URL


def test_sort_command_sorts_urls(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that SortCommand sorts URLs lexicographically."""
    cmd = SortCommand()
    url_list: list[URL] = [
        URL("https://c.com"),
        URL("https://a.com"),
        URL("https://b.com"),
    ]
    result = cmd.run([], url_list)
    urls = [u.url for u in result]
    assert urls == ["https://a.com", "https://b.com", "https://c.com"]
    captured = capsys.readouterr()
    assert "Sorted URLs." in captured.out


def test_sort_command_already_sorted(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that SortCommand leaves already sorted URLs unchanged."""
    cmd = SortCommand()
    url_list: list[URL] = [URL("a"), URL("b"), URL("c")]
    result = cmd.run([], url_list)
    urls = [u.url for u in result]
    assert urls == ["a", "b", "c"]
    captured = capsys.readouterr()
    assert "Sorted URLs." in captured.out


def test_sort_command_empty_list(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that SortCommand works with an empty list."""
    cmd = SortCommand()
    url_list: list[URL] = []
    result = cmd.run([], url_list)
    assert result == []
    captured = capsys.readouterr()
    assert "Sorted URLs." in captured.out
