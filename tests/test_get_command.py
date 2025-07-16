"""Tests for the GetCommand."""

import os
import tempfile
from collections.abc import Generator
from typing import Any
from unittest.mock import MagicMock

import pytest

import urload.commands.get
from urload.commands.get import GetCommand
from urload.settings import AppSettings
from urload.url import URL


class DummyResponse:
    """A dummy HTTP response object for simulating URL.get()."""

    def __init__(
        self,
        content: bytes = b"data",
        status_code: int = 200,
        raise_exc: Exception | None = None,
    ):
        """Initialize DummyResponse.

        :param content: The response content.
        :param status_code: The HTTP status code.
        :param raise_exc: Exception to raise on raise_for_status, or None.
        """
        self.content = content
        self._raise_exc = raise_exc
        self._status_code = status_code

    def raise_for_status(self) -> None:
        """Raise an exception if the response is an error or if raise_exc is set."""
        if self._raise_exc:
            raise self._raise_exc
        HTTP_ERROR = 400
        if self._status_code >= HTTP_ERROR:
            raise Exception(f"HTTP {self._status_code}")


@pytest.fixture
def temp_cwd(monkeypatch: Any) -> Generator[str, None, None]:
    """Change to a temporary directory for the duration of the test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.chdir(tmpdir)
        yield tmpdir


def make_url(
    url_str: str,
    content: bytes = b"data",
    status_code: int = 200,
    raise_exc: Exception | None = None,
) -> URL:
    """Create a URL object with a mocked get() method returning DummyResponse."""
    url = URL(url_str)
    url.get = MagicMock(return_value=DummyResponse(content, status_code, raise_exc))
    return url


def reset_get_index():
    """Reset the _get_index variable in the get command module for test isolation."""
    urload.commands.get._get_index = 0  # type: ignore


def test_get_command_success(temp_cwd: str) -> None:
    """Test that a successful download saves the file and returns an empty list."""
    url = make_url("http://example.com/file.txt", b"hello")
    settings = AppSettings()
    settings.filename_template = "{filename}"
    cmd = GetCommand()
    result = cmd.run([], [url], settings)
    assert result == []
    session_dir = f"{settings.session_dir_num:04d}"
    file_path = os.path.join(session_dir, "file.txt")
    assert os.path.exists(file_path)
    with open(file_path, "rb") as f:
        assert f.read() == b"hello"


def test_get_command_default_filename(temp_cwd: str) -> None:
    """Test that a URL with no filename saves as index.html."""
    url = make_url("http://example.com/")
    settings = AppSettings()
    settings.filename_template = "{filename}"
    cmd = GetCommand()
    result = cmd.run([], [url], settings)
    assert result == []
    session_dir = f"{settings.session_dir_num:04d}"
    file_path = os.path.join(session_dir, "index.html")
    assert os.path.exists(file_path)


def test_get_command_failure(temp_cwd: str) -> None:
    """Test that a failed download returns the URL in the result and does not save a file."""
    url = make_url("http://bad.com/file.txt", raise_exc=Exception("fail"))
    cmd = GetCommand()
    settings = AppSettings()
    result = cmd.run([], [url], settings)
    assert result == [url]
    session_dir = f"{settings.session_dir_num:04d}"
    file_path = os.path.join(session_dir, "file.txt")
    assert not os.path.exists(file_path)


def test_get_command_partial_success(temp_cwd: str) -> None:
    """Test that only failed URLs are returned and successful files are saved."""
    url1 = make_url("http://ok.com/a.txt", b"a")
    url2 = make_url("http://fail.com/b.txt", raise_exc=Exception("fail"))
    settings = AppSettings()
    settings.filename_template = "{filename}"
    cmd = GetCommand()
    result = cmd.run([], [url1, url2], settings)
    assert result == [url2]
    session_dir = f"{settings.session_dir_num:04d}"
    file_path1 = os.path.join(session_dir, "a.txt")
    file_path2 = os.path.join(session_dir, "b.txt")
    assert os.path.exists(file_path1)
    assert not os.path.exists(file_path2)


def test_get_command_dry_run_prints_and_leaves_list_unchanged(
    temp_cwd: str, capsys: Any
) -> None:
    """Test that -n (dry run) prints index, url, and filename, and leaves url_list unchanged."""
    reset_get_index()
    url1 = make_url("http://example.com/foo.txt")
    url2 = make_url("http://example.com/bar/")
    settings = AppSettings()
    settings.filename_template = "{filename}"
    cmd = GetCommand()
    url_list = [url1, url2]
    result = cmd.run(["-n"], url_list, settings)
    assert result == url_list
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured[0].endswith("foo.txt")
    assert captured[1].endswith("index.html")
    assert "[0] http://example.com/foo.txt foo.txt" in captured[0]
    assert "[1] http://example.com/bar/ index.html" in captured[1]
    # Ensure no files were created
    session_dir = f"{settings.session_dir_num:04d}"
    assert not os.path.exists(os.path.join(session_dir, "foo.txt"))
    assert not os.path.exists(os.path.join(session_dir, "index.html"))


def test_get_command_index_template(temp_cwd: str) -> None:
    """Test that the 'index' template value is substituted correctly in filenames."""
    reset_get_index()
    url1 = make_url("http://example.com/a.txt", b"A")
    url2 = make_url("http://example.com/b.txt", b"B")
    settings = AppSettings()
    settings.filename_template = "{index:02d}_{filename}"
    cmd = GetCommand()
    result = cmd.run([], [url1, url2], settings)
    assert result == []
    session_dir = f"{settings.session_dir_num:04d}"
    file_path1 = os.path.join(session_dir, "00_a.txt")
    file_path2 = os.path.join(session_dir, "01_b.txt")
    assert os.path.exists(file_path1)
    assert os.path.exists(file_path2)
    with open(file_path1, "rb") as f:
        assert f.read() == b"A"
    with open(file_path2, "rb") as f:
        assert f.read() == b"B"
    url3 = make_url("http://example.com/c.txt", b"C")
    result = cmd.run([], [url3], settings)
    assert result == []
    file_path3 = os.path.join(session_dir, "02_c.txt")
    assert os.path.exists(file_path3)
    with open(file_path3, "rb") as f:
        assert f.read() == b"C"
