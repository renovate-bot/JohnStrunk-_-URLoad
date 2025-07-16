"""Tests for build_filename in get.py."""

import os

import pytest

from urload.commands.get import build_filename


@pytest.mark.parametrize(
    "url,expected",
    [
        ("http://example.com/foo/bar.txt", "bar.txt"),
        ("http://example.com/foo/bar.txt?query=1", "bar.txt"),
        ("http://example.com/foo/", "index.html"),
        ("http://example.com/", "index.html"),
        ("http://example.com/foo.bar", "foo.bar"),
        ("http://example.com/foo.bar?x=1", "foo.bar"),
        ("http://example.com/foo.bar.baz", "foo.bar.baz"),
        ("http://example.com/foo.bar.baz?x=1", "foo.bar.baz"),
        ("http://example.com/foo%20space.txt", "foo space.txt"),
        ("http://example.com/foo/../bar.txt", "bar.txt"),
        ("http://example.com/foo/../../evil.txt", "evil.txt"),
        ("http://example.com/foo/%2E%2E/bar.txt", "bar.txt"),
    ],
)
def test_filename_extraction(url: str, expected: str) -> None:
    """Test that the filename is correctly extracted and sanitized from the URL."""
    template = "{filename}"
    fname = build_filename(template, "20250101", url, 1)
    assert "/" not in fname and ".." not in fname
    assert fname == expected


@pytest.mark.parametrize(
    "url,expected_basename,expected_ext",
    [
        ("http://example.com/foo/bar.txt", "bar", "txt"),
        ("http://example.com/foo/bar", "bar", ""),
        ("http://example.com/foo/bar.txt?x=1", "bar", "txt"),
        ("http://example.com/foo/index.html", "index", "html"),
        ("http://example.com/foo.bar.baz", "foo", "bar.baz"),
    ],
)
def test_template_parameters(
    url: str, expected_basename: str, expected_ext: str
) -> None:
    """Test that template parameters are parsed correctly from the URL."""
    template = "{basename}.{ext}"
    fname = build_filename(template, "20250101", url, 42)
    assert fname.startswith(expected_basename)
    if expected_ext:
        assert fname.endswith(expected_ext)
    else:
        assert fname.endswith(".") or fname == expected_basename + "."


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com/foo/../../bar.txt",
        "http://example.com/../evil.txt",
        "http://example.com/foo/%2E%2E/bar.txt",
        "http://example.com/foo/%2Fbar.txt",
    ],
)
def test_no_path_traversal(url: str) -> None:
    """Test that the returned filename cannot refer to a path above the current directory."""
    template = "{dirname}/{filename}"
    fname = build_filename(template, "20250101", url, 99)
    assert not fname.startswith("../")
    assert ".." not in fname
    assert not fname.startswith("/")
    assert os.path.normpath(fname) == fname


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com/foo/bar.txt?query=1",
        "http://example.com/foo/bar.txt?x=1&y=2",
    ],
)
def test_query_string_removed(url: str) -> None:
    """Test that the query string is removed from the filename and extension."""
    template = "{filename}"
    fname = build_filename(template, "20250101", url, 1)
    assert "?" not in fname
    assert fname.endswith(".txt")
