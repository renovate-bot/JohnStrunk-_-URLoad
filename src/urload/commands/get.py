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
    """Download each URL in the list to a file in the current directory, or perform a dry run."""

    name = "get"
    description = textwrap.dedent("""
    get [-n] - Download each URL in the list to a file in the current directory.

    Each file is named after the final component of the URL path, excluding query parameters.
    If -n is given, perform a dry run: print the index, URL, and filename for each URL, but do not download anything.
    """)

    def run(self, args: list[str], url_list: list[URL]) -> list[URL]:
        """
        Download each URL to a file named after the final path component, or perform a dry run.

        :param args: List of command-line arguments. If '-n' is present, do a dry run.
        :param url_list: List of URLs to download.
        :return: List of URLs that failed to download, or the original list if dry run.
        """
        dry_run = "-n" in args
        if dry_run:
            for idx, url_obj in enumerate(url_list):
                url = url_obj.url
                parsed = urlparse(url)
                filename = os.path.basename(parsed.path)
                if not filename:
                    filename = "index.html"
                filename = unquote(filename)
                print(f"[{idx}] {url} {filename}")
            return url_list

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
