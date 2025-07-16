"""Tests for the img command."""

from typing import Any

import pytest

from urload.commands.base import CommandError
from urload.commands.img import ImgCommand
from urload.url import URL


class DummyResponse:
    """A dummy response object for mocking requests.get."""

    def __init__(self, text: str):
        """Initialize with HTML text."""
        self.text = text

    def raise_for_status(self) -> None:
        """No-op for status check."""
        pass


EXPECTED_IMG_COUNT = 2


def test_img_command_extracts_sources(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that img command extracts image sources and sets Referer header."""
    html = (
        '<html><body><img src="https://a.com/img.png"><img src="/b.png"></body></html>'
    )

    def mock_get(
        url: str, timeout: int = 10, headers: dict[str, str] | None = None
    ) -> DummyResponse:
        return DummyResponse(html)

    monkeypatch.setattr("requests.get", mock_get)
    cmd = ImgCommand()
    url_list = [URL("https://example.com")]
    result = cmd.run([], url_list)
    assert len(result) == EXPECTED_IMG_COUNT
    srcs = {u.url for u in result}
    assert "https://a.com/img.png" in srcs
    assert "https://example.com/b.png" in srcs
    for u in result:
        assert u.headers.get("Referer") == "https://example.com"


def test_img_command_removes_original(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that the original URL is not in the result list and Referer is set."""
    html = '<img src="/foo.png">'

    def mock_get(
        url: str, timeout: int = 10, headers: dict[str, str] | None = None
    ) -> DummyResponse:
        return DummyResponse(html)

    monkeypatch.setattr("requests.get", mock_get)
    cmd = ImgCommand()
    url_list = [URL("https://x.com")]
    result = cmd.run([], url_list)
    assert all(u.url != "https://x.com" for u in result)
    for u in result:
        assert u.headers.get("Referer") == "https://x.com"


def test_img_command_takes_no_args() -> None:
    """Test that passing arguments raises CommandError."""
    cmd = ImgCommand()
    with pytest.raises(CommandError):
        cmd.run(["unexpected"], [URL("https://x.com")])


def test_img_command_handles_fetch_error(
    monkeypatch: pytest.MonkeyPatch, capsys: Any
) -> None:
    """Test that fetch errors are handled and print an error message."""

    def mock_get(
        url: str, timeout: int = 10, headers: dict[str, str] | None = None
    ) -> DummyResponse:
        raise Exception("fail")

    monkeypatch.setattr("requests.get", mock_get)
    cmd = ImgCommand()
    url_list = [URL("https://fail.com")]
    result = cmd.run([], url_list)
    assert result == []
    out = capsys.readouterr().out
    assert "https://fail.com -> Error: fail" in out


def test_img_command_relative_sources(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that relative image sources are resolved correctly, including '.' and '..'."""
    html = (
        '<img src="foo/bar.png">'
        '<img src="/absolute.png">'
        '<img src=".">'  # Should resolve to current directory
        '<img src="..">'  # Should resolve to parent directory
    )

    def mock_get(
        url: str, timeout: int = 10, headers: dict[str, str] | None = None
    ) -> DummyResponse:
        return DummyResponse(html)

    monkeypatch.setattr("requests.get", mock_get)
    cmd = ImgCommand()
    url_list = [URL("https://host.com/base/")]
    result = cmd.run([], url_list)
    urls = {u.url for u in result}
    assert "https://host.com/base/foo/bar.png" in urls
    assert "https://host.com/absolute.png" in urls
    assert "https://host.com/base/" in urls
    assert "https://host.com/" in urls


def test_img_command_nested_sources(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that image sources nested within other elements are found."""
    html = '<html><body><ul><li><img src="/nested1.png"></li><li><div><img src="/nested2.png"></div></li></ul></body></html>'

    def mock_get(
        url: str, timeout: int = 10, headers: dict[str, str] | None = None
    ) -> DummyResponse:
        return DummyResponse(html)

    monkeypatch.setattr("requests.get", mock_get)
    cmd = ImgCommand()
    url_list = [URL("https://nest.com/")]
    result = cmd.run([], url_list)
    urls = {u.url for u in result}
    assert "https://nest.com/nested1.png" in urls
    assert "https://nest.com/nested2.png" in urls


def test_img_command_passes_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that the URL's headers are passed to requests.get."""
    html = '<img src="/foo.png">'
    called = {}

    def mock_get(
        url: str, timeout: int = 10, headers: dict[str, str] | None = None
    ) -> DummyResponse:
        called["headers"] = headers
        return DummyResponse(html)

    monkeypatch.setattr("requests.get", mock_get)
    cmd = ImgCommand()
    url_list = [URL("https://x.com", headers={"X-Test": "yes", "Referer": "abc"})]
    cmd.run([], url_list)
    assert called["headers"] == {"X-Test": "yes", "Referer": "abc"}
