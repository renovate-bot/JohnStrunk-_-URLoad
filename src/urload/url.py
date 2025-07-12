"""
A class representing a URL and its associated metadata.

:class:`URL` encapsulates a URL string and optional metadata such as referrer.
This allows commands to manipulate URLs and pass additional information when fetching.
"""


class URL:
    """
    Represents a URL and its associated metadata.

    :param url: The URL string.
    :param referrer: The referrer URL, if any.
    """

    def __init__(self, url: str, referrer: str | None = None) -> None:
        """Initialize a URL with optional referrer."""
        self.url = url
        self.referrer = referrer

    def __repr__(self) -> str:
        """Return a string representation of the URL object."""
        return f"URL(url={self.url!r}, referrer={self.referrer!r})"
