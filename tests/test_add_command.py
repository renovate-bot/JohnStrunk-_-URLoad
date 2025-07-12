"""Tests for the AddCommand."""

import pytest

from urload.commands.add import AddCommand
from urload.url import URL


def test_add_command_appends_url(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that AddCommand appends a URL to the list."""
    cmd = AddCommand()
    url_list: list[URL] = []
    result = cmd.run(["https://example.com"], url_list)
    assert len(result) == 1
    assert result[0].url == "https://example.com"


def test_add_command_no_args(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that AddCommand prints an error if no URL is provided and does not modify the list."""
    cmd = AddCommand()
    url_list: list[URL] = []
    result = cmd.run([], url_list)
    assert result == url_list
    captured = capsys.readouterr()
    assert "Error: No URL provided." in captured.out
