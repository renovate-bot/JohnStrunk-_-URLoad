"""Tests for the UniqCommand."""

import pytest

from urload.commands.uniq import UniqCommand
from urload.url import URL


def test_uniq_command_removes_duplicates(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that UniqCommand removes duplicate URLs, keeping the first occurrence."""
    cmd = UniqCommand()
    url_list = [
        URL("https://a.com"),
        URL("https://b.com"),
        URL("https://a.com"),
        URL("https://c.com"),
        URL("https://b.com"),
        URL("https://a.com"),
    ]
    result = cmd.run([], url_list)
    urls = [u.url for u in result]
    assert urls == ["https://a.com", "https://b.com", "https://c.com"]
    captured = capsys.readouterr()
    assert "Removed 3 duplicate URLs." in captured.out


def test_uniq_command_no_duplicates(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that UniqCommand does nothing if all URLs are unique."""
    cmd = UniqCommand()
    url_list = [URL("https://a.com"), URL("https://b.com"), URL("https://c.com")]
    result = cmd.run([], url_list)
    urls = [u.url for u in result]
    assert urls == ["https://a.com", "https://b.com", "https://c.com"]
    captured = capsys.readouterr()
    assert "Removed 0 duplicate URLs." in captured.out


def test_uniq_command_empty_list(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that UniqCommand works with an empty list."""
    cmd = UniqCommand()
    url_list: list[URL] = []
    result = cmd.run([], url_list)
    assert result == []
    captured = capsys.readouterr()
    assert "Removed 0 duplicate URLs." in captured.out


def test_uniq_command_keeps_first_occurrence() -> None:
    """Test that UniqCommand keeps the first occurrence of each URL."""
    cmd = UniqCommand()
    url_list = [
        URL("https://a.com"),
        URL("https://b.com"),
        URL("https://a.com"),
        URL("https://a.com"),
    ]
    result = cmd.run([], url_list)
    urls = [u.url for u in result]
    assert urls == ["https://a.com", "https://b.com"]
