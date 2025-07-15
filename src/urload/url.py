"""
A class representing a URL and its associated metadata.

:class:`URL` encapsulates a URL string and optional metadata such as headers.
This allows commands to manipulate URLs and pass additional information when fetching.
"""

import json

import requests


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

    def get(self, timeout: float = 10.0) -> requests.Response:
        """
        Perform an HTTP GET request for this URL using its headers.

        :param timeout: Timeout in seconds for the request (default 10.0).
        :return: The requests.Response object from the GET request.
        :raises requests.RequestException: If the request fails.
        """
        return requests.get(self.url, timeout=timeout, headers=self.headers)

    def serialize(self) -> str:
        """
        Serialize the URL and its headers to a single line string.

        The format is: <url> [<json-headers>]
        If headers are present, they are encoded as a JSON object after a space.
        Header values are encoded to handle all RFC9110-allowed characters.

        :return: A string representing the URL and headers.
        """
        if self.headers:
            return f"{self.url} {json.dumps(self.headers, ensure_ascii=False)}"
        return self.url

    @classmethod
    def deserialize(cls, line: str) -> "URL":
        """
        Deserialize a line into a URL object, parsing headers if present.

        The format is: <url> [<json-headers>]
        If headers are present, they are expected as a JSON object after a space.

        :param line: The line to parse.
        :return: A URL object.
        :raises ValueError: If the line cannot be parsed.
        """
        line = line.strip()
        if not line:
            raise ValueError("Empty line")
        # Try to split into url and headers (headers must be valid JSON if present)
        if " " not in line:
            return cls(line)
        url_part, headers_part = line.split(" ", 1)
        headers_part = headers_part.strip()
        if not headers_part:
            return cls(url_part)
        try:
            headers_obj = json.loads(headers_part)
            if not isinstance(headers_obj, dict):
                raise ValueError("Headers must be a JSON object")
            headers: dict[str, str] = {
                str(k): str(v)  # type: ignore
                for k, v in headers_obj.items()  # type: ignore
            }
        except Exception as e:
            raise ValueError(f"Invalid headers JSON: {e}")
        return cls(url_part, headers)
