"""
get - Download each URL in the list to a file in the current directory.

Each file is named after the final component of the URL path, excluding query parameters.
"""

import os
import textwrap
from urllib.parse import unquote, urlparse

from urload.commands.base import Command
from urload.url import URL


class GetCommand(Command):
    """Download each URL in the list to a file in the current directory."""

    name = "get"
    description = textwrap.dedent("""
    get - Download each URL in the list to a file in the current directory.

    Each file is named after the final component of the URL path, excluding query parameters.
    """)

    def run(self, args: list[str], url_list: list[URL]) -> list[URL]:
        """
        Download each URL to a file named after the final path component.

        :param args: Not used.
        :param url_list: List of URLs to download.
        :raises CommandError: If a download fails.
        :return: List of URLs that failed to download.
        """
        failed_urls: list[URL] = []
        for url_obj in url_list:
            url = url_obj.url
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path)
            if not filename:
                filename = "index.html"
            filename = unquote(filename)
            try:
                resp = url_obj.get()
                resp.raise_for_status()
                with open(filename, "wb") as f:
                    f.write(resp.content)
                print(f"Saved {url} to {filename}")
            except Exception as e:
                print(f"Failed to download {url}: {e}")
                failed_urls.append(url_obj)
        return failed_urls
