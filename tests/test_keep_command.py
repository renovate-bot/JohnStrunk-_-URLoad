"""Tests for the KeepCommand."""

import pytest

from urload.commands.keep import CommandError, KeepCommand
from urload.url import URL


def test_keep_command_matches_some(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that KeepCommand keeps only URLs matching the regex."""
    cmd = KeepCommand()
    url_list = [URL("https://a.com"), URL("https://b.org"), URL("https://c.com")]
    result = cmd.run([r"\.com$"], url_list)
    captured = capsys.readouterr()
    assert result == [URL("https://a.com"), URL("https://c.com")]
    assert "Kept 2 URLs matching pattern." in captured.out


def test_keep_command_matches_none(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that KeepCommand returns an empty list if no URLs match the regex."""
    cmd = KeepCommand()
    url_list = [URL("https://a.com"), URL("https://b.org")]
    result = cmd.run([r"nomatch"], url_list)
    captured = capsys.readouterr()
    assert result == []
    assert "Kept 0 URLs matching pattern." in captured.out


def test_keep_command_invalid_regex() -> None:
    """Test that KeepCommand raises CommandError for invalid regex."""
    cmd = KeepCommand()
    url_list = [URL("https://a.com")]
    with pytest.raises(CommandError, match="Invalid regex"):
        cmd.run([r"["], url_list)


def test_keep_command_no_args() -> None:
    """Test that KeepCommand raises CommandError if no regex is provided."""
    cmd = KeepCommand()
    url_list = [URL("https://a.com")]
    with pytest.raises(CommandError, match="No regex pattern provided."):
        cmd.run([], url_list)
