"""Tests for the URL class."""

from urload.url import URL


def test_url_basic() -> None:
    """Test creating a URL with and without a referrer."""
    url = URL("https://example.com")
    assert url.url == "https://example.com"
    assert url.referrer is None

    url2 = URL("https://example.com/page", referrer="https://example.com")
    assert url2.url == "https://example.com/page"
    assert url2.referrer == "https://example.com"


def test_url_repr() -> None:
    """Test the __repr__ output of the URL class."""
    url = URL("https://example.com", referrer="https://ref.com")
    rep = repr(url)
    assert "URL(url='https://example.com', referrer='https://ref.com')" == rep
