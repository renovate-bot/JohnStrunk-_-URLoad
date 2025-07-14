"""Tests for the URL class."""

from urload.url import URL


def test_url_basic() -> None:
    """Test creating a URL with and without headers."""
    url = URL("https://example.com")
    assert url.url == "https://example.com"
    assert url.headers == {}

    url2 = URL("https://example.com/page", headers={"Referer": "https://example.com"})
    assert url2.url == "https://example.com/page"
    assert url2.headers.get("Referer") == "https://example.com"


def test_url_repr() -> None:
    """Test the __repr__ output of the URL class with headers."""
    url = URL("https://example.com", headers={"Referer": "https://ref.com"})
    rep = repr(url)
    assert (
        rep == "URL(url='https://example.com', headers={'Referer': 'https://ref.com'})"
    )
