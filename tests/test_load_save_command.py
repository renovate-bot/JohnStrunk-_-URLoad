"""Tests for the load and save commands and URL serialization/deserialization."""

import os
import tempfile
from pathlib import Path

import pytest

from urload.commands.base import CommandError
from urload.commands.load import LoadCommand
from urload.commands.save import SaveCommand
from urload.url import URL

ROUNDTRIP_URL_COUNT = 3


def test_save_and_load_roundtrip():
    """Test that saving and loading a list of URLs (with headers) is lossless."""
    urls = [
        URL("http://example.com"),
        URL(
            "https://foo.com/bar",
            headers={"X-Test": "abc 123", "Referer": "http://ref.com"},
        ),
        URL("https://üñîçødë.com", headers={"X-Ü": "\u00ff\u0080\u00e9"}),
    ]
    with tempfile.NamedTemporaryFile(delete=False, mode="w+") as tmp:
        fname = tmp.name
        SaveCommand().run([fname], urls)
        tmp.seek(0)
        lines = tmp.readlines()
        assert len(lines) == ROUNDTRIP_URL_COUNT
    loaded = LoadCommand().run([fname], [])
    assert loaded == urls
    os.remove(fname)


def test_save_bare_url(tmp_path: Path):
    """Test saving and loading a bare URL with no headers."""
    url = URL("http://bare.com")
    fname = tmp_path / "bare.txt"
    SaveCommand().run([str(fname)], [url])
    with open(fname, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert lines == ["http://bare.com\n"]
    loaded = LoadCommand().run([str(fname)], [])
    assert loaded == [url]


def test_load_invalid_file():
    """Test that loading from a nonexistent file raises CommandError."""
    with pytest.raises(CommandError):
        LoadCommand().run(["/nonexistent/file/path"], [])


def test_load_invalid_line(tmp_path: Path):
    """Test that loading a file with an invalid line raises CommandError."""
    fname = tmp_path / "bad.txt"
    with open(fname, "w", encoding="utf-8") as f:
        f.write("not a url {bad json}\n")
    with pytest.raises(CommandError):
        LoadCommand().run([str(fname)], [])


def test_save_invalid_args():
    """Test that save command with invalid arguments raises CommandError."""
    with pytest.raises(CommandError):
        SaveCommand().run([], [])
    with pytest.raises(CommandError):
        SaveCommand().run(["a", "b"], [])


def test_load_invalid_args():
    """Test that load command with invalid arguments raises CommandError."""
    with pytest.raises(CommandError):
        LoadCommand().run([], [])
    with pytest.raises(CommandError):
        LoadCommand().run(["a", "b"], [])
