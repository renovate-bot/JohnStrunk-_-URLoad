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
