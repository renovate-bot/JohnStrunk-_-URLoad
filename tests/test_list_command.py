"""Tests for the ListCommand."""

import pytest

from urload.commands.list import ListCommand
from urload.url import URL


def test_list_command_prints_urls(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that ListCommand prints each URL with its index."""
    cmd = ListCommand()
    url_list = [URL("https://a.com"), URL("https://b.com"), URL("https://c.com")]
    result = cmd.run([], url_list)
    captured = capsys.readouterr()
    output = captured.out.strip().splitlines()
    assert output == [
        "0: https://a.com",
        "1: https://b.com",
        "2: https://c.com",
    ]
    assert result == url_list


def test_list_command_empty(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that ListCommand prints nothing for an empty list."""
    cmd = ListCommand()
    url_list: list[URL] = []
    result = cmd.run([], url_list)
    captured = capsys.readouterr()
    assert captured.out.strip() == ""
    assert result == url_list
