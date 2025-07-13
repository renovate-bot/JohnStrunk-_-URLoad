"""Tests for the DiscardCommand."""

import pytest

from urload.commands.discard import CommandError, DiscardCommand
from urload.url import URL


def test_discard_command_removes_some(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that DiscardCommand removes URLs matching the regex."""
    cmd = DiscardCommand()
    url_list = [URL("https://a.com"), URL("https://b.org"), URL("https://c.com")]
    result = cmd.run([r"\.com$"], url_list)
    captured = capsys.readouterr()
    assert result == [URL("https://b.org")]
    assert "Removed 2 URLs matching pattern." in captured.out


def test_discard_command_removes_none(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that DiscardCommand removes no URLs if none match."""
    cmd = DiscardCommand()
    url_list = [URL("https://a.com"), URL("https://b.org")]
    result = cmd.run([r"nomatch"], url_list)
    captured = capsys.readouterr()
    assert result == url_list
    assert "Removed 0 URLs matching pattern." in captured.out


def test_discard_command_invalid_regex() -> None:
    """Test that DiscardCommand raises CommandError for invalid regex."""
    cmd = DiscardCommand()
    url_list = [URL("https://a.com")]
    with pytest.raises(CommandError, match="Invalid regex"):
        cmd.run([r"["], url_list)


def test_discard_command_no_args() -> None:
    """Test that DiscardCommand raises CommandError if no regex is provided."""
    cmd = DiscardCommand()
    url_list = [URL("https://a.com")]
    with pytest.raises(CommandError, match="No regex pattern provided."):
        cmd.run([], url_list)
