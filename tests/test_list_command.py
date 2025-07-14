"""Tests for the ListCommand."""

import pytest
from pytest import CaptureFixture

from urload.commands.list import ListCommand
from urload.url import URL


def url_list() -> list[URL]:
    """Return a list of 10 test URLs."""
    return [URL(f"https://site.com/{i}") for i in range(10)]


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


def test_list_all_range_behavior(capsys: CaptureFixture[str]) -> None:
    """Test that list with no argument prints all URLs."""
    cmd = ListCommand()
    urls = url_list()
    cmd.run([], urls)
    out = capsys.readouterr().out
    for i in range(10):
        assert f"{i}: https://site.com/{i}" in out


def test_list_single_index(capsys: CaptureFixture[str]) -> None:
    """Test that list with a single index prints only that URL."""
    cmd = ListCommand()
    urls = url_list()
    cmd.run(["3"], urls)
    out = capsys.readouterr().out
    assert out.strip() == "3: https://site.com/3"


def test_list_range_start_dash(capsys: CaptureFixture[str]) -> None:
    """Test that list with -N prints from 0 to N inclusive."""
    cmd = ListCommand()
    urls = url_list()
    cmd.run(["-4"], urls)
    out = capsys.readouterr().out
    for i in range(0, 5):
        assert f"{i}: https://site.com/{i}" in out


def test_list_range_end_dash(capsys: CaptureFixture[str]) -> None:
    """Test that list with N- prints from N to the end."""
    cmd = ListCommand()
    urls = url_list()
    cmd.run(["7-"], urls)
    out = capsys.readouterr().out
    for i in range(7, 10):
        assert f"{i}: https://site.com/{i}" in out


def test_list_range_inclusive(capsys: CaptureFixture[str]) -> None:
    """Test that list with N-M prints from N to M inclusive."""
    cmd = ListCommand()
    urls = url_list()
    cmd.run(["2-5"], urls)
    out = capsys.readouterr().out
    for i in range(2, 6):
        assert f"{i}: https://site.com/{i}" in out


def test_list_dash_all(capsys: CaptureFixture[str]) -> None:
    """Test that list with '-' raises CommandError (invalid range)."""
    cmd = ListCommand()
    urls = url_list()
    with pytest.raises(Exception):
        cmd.run(["-"], urls)


def test_list_invalid_index_raises() -> None:
    """Test that invalid index arguments raise CommandError (except negative index, which is a valid range)."""
    cmd = ListCommand()
    urls = url_list()
    with pytest.raises(Exception):
        cmd.run(["100"], urls)
    with pytest.raises(Exception):
        cmd.run(["foo"], urls)


def test_list_invalid_range_raises() -> None:
    """Test that invalid range arguments raise CommandError."""
    cmd = ListCommand()
    urls = url_list()
    with pytest.raises(Exception):
        cmd.run(["3-bar"], urls)
    with pytest.raises(Exception):
        cmd.run(["foo-5"], urls)
    with pytest.raises(Exception):
        cmd.run(["5-2"], urls)  # valid numbers but reversed range
    with pytest.raises(Exception):
        cmd.run(["a-"], urls)
    with pytest.raises(Exception):
        cmd.run(["-z"], urls)
