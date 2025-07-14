"""Tests for the href command."""

from typing import Any

import pytest

from urload.commands.base import CommandError
from urload.commands.href import HrefCommand
from urload.url import URL


class DummyResponse:
    """A dummy response object for mocking requests.get."""

    def __init__(self, text: str):
        """Initialize with HTML text."""
        self.text = text

    def raise_for_status(self) -> None:
        """No-op for status check."""
        pass


EXPECTED_LINK_COUNT = 2


def test_href_command_extracts_links(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that href command extracts anchor links and sets Referer header."""
    html = (
        """<html><body><a href="https://a.com">A</a><a href="/b">B</a></body></html>"""
    )

    def mock_get(
        url: str, timeout: int = 10, headers: dict[str, str] | None = None
    ) -> DummyResponse:
        return DummyResponse(html)

    monkeypatch.setattr("requests.get", mock_get)
    cmd = HrefCommand()
    url_list = [URL("https://example.com")]
    result = cmd.run([], url_list)
    assert len(result) == EXPECTED_LINK_COUNT
    hrefs = {u.url for u in result}
    assert "https://a.com" in hrefs
    assert "https://example.com/b" in hrefs
    for u in result:
        assert u.headers.get("Referer") == "https://example.com"


def test_href_command_removes_original(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that the original URL is not in the result list."""
    html = '<a href="/foo">foo</a>'

    def mock_get(
        url: str, timeout: int = 10, headers: dict[str, str] | None = None
    ) -> DummyResponse:
        return DummyResponse(html)

    monkeypatch.setattr("requests.get", mock_get)
    cmd = HrefCommand()
    url_list = [URL("https://x.com")]
    result = cmd.run([], url_list)
    assert all(u.url != "https://x.com" for u in result)
    for u in result:
        assert u.headers.get("Referer") == "https://x.com"


def test_href_command_takes_no_args() -> None:
    """Test that passing arguments raises CommandError."""
    cmd = HrefCommand()
    with pytest.raises(CommandError):
        cmd.run(["unexpected"], [URL("https://x.com")])


def test_href_command_handles_fetch_error(
    monkeypatch: pytest.MonkeyPatch, capsys: Any
) -> None:
    """Test that fetch errors are handled and print an error message."""

    def mock_get(
        url: str, timeout: int = 10, headers: dict[str, str] | None = None
    ) -> DummyResponse:
        raise Exception("fail")

    monkeypatch.setattr("requests.get", mock_get)
    cmd = HrefCommand()
    url_list = [URL("https://fail.com")]
    result = cmd.run([], url_list)
    assert result == []
    out = capsys.readouterr().out
    assert "Error fetching https://fail.com" in out


def test_href_command_relative_links(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that relative links are resolved correctly, including '.' and '..'."""
    html = (
        '<a href="foo/bar">Relative</a>'
        '<a href="/absolute">Absolute</a>'
        '<a href=".">Dot</a>'
        '<a href="..">DotDot</a>'
    )

    def mock_get(
        url: str, timeout: int = 10, headers: dict[str, str] | None = None
    ) -> DummyResponse:
        return DummyResponse(html)

    monkeypatch.setattr("requests.get", mock_get)
    cmd = HrefCommand()
    url_list = [URL("https://host.com/base/")]
    result = cmd.run([], url_list)
    urls = {u.url for u in result}
    assert "https://host.com/base/foo/bar" in urls
    assert "https://host.com/absolute" in urls
    # '.' resolves to the current directory
    assert "https://host.com/base/" in urls
    # '..' resolves to the parent directory
    assert "https://host.com/" in urls


def test_href_command_nested_links(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that links nested within other elements are found."""
    html = """<html><body><ul><li><a href="/nested1">One</a></li><li><div><a href="/nested2">Two</a></div></li></ul></body></html>"""

    def mock_get(
        url: str, timeout: int = 10, headers: dict[str, str] | None = None
    ) -> DummyResponse:
        return DummyResponse(html)

    monkeypatch.setattr("requests.get", mock_get)
    cmd = HrefCommand()
    url_list = [URL("https://nest.com/")]
    result = cmd.run([], url_list)
    urls = {u.url for u in result}
    assert "https://nest.com/nested1" in urls
    assert "https://nest.com/nested2" in urls


def test_href_command_passes_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that the URL's headers are passed to requests.get."""
    html = '<a href="/foo">foo</a>'
    called = {}

    def mock_get(
        url: str, timeout: int = 10, headers: dict[str, str] | None = None
    ) -> DummyResponse:
        called["headers"] = headers
        return DummyResponse(html)

    monkeypatch.setattr("requests.get", mock_get)
    cmd = HrefCommand()
    url_list = [URL("https://x.com", headers={"X-Test": "yes", "Referer": "abc"})]
    cmd.run([], url_list)
    assert called["headers"] == {"X-Test": "yes", "Referer": "abc"}
