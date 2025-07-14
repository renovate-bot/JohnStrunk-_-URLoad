"""
A class representing a URL and its associated metadata.

:class:`URL` encapsulates a URL string and optional metadata such as headers.
This allows commands to manipulate URLs and pass additional information when fetching.
"""


class URL:
    """
    Represents a URL and its associated metadata.

    :param url: The URL string.
    :param headers: Optional dictionary of HTTP headers (e.g., may include 'Referer').
    """

    def __init__(self, url: str, headers: dict[str, str] | None = None) -> None:
        """Initialize a URL with optional headers."""
        self.url = url
        self.headers = headers or {}

    def __repr__(self) -> str:
        """Return a string representation of the URL object."""
        return f"URL(url={self.url!r}, headers={self.headers!r})"

    def __eq__(self, other: object) -> bool:
        """Return True if the other object is a URL with the same url and headers."""
        if not isinstance(other, URL):
            return NotImplemented
        return self.url == other.url and self.headers == other.headers

    def __hash__(self) -> int:
        """Return a hash based on the url and headers."""
        return hash((self.url, frozenset(self.headers.items())))
