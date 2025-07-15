"""Extracts all image sources from each URL in the list and adds them to the URL list with the original URL as the referrer."""

import textwrap
from typing import Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from urload.commands.base import Command, CommandError
from urload.url import URL


class ImgCommand(Command):
    """Extract all image sources from each URL in the list and add them to the URL list with the original URL as the referrer."""

    name = "img"
    description = textwrap.dedent(
        """
        img - Extract image sources from each URL

        For each URL in the list, fetch the page, extract all <img src=...> links, and add them to the URL list with the original URL as the referrer. The original URL is removed from the list.
        """
    )

    def run(
        self, args: list[str], url_list: list[URL], settings: Any = None
    ) -> list[URL]:
        """
        Return a new list of URLs extracted from image sources, with the original URL as referrer.

        :param args: List of command-line arguments (must be empty).
        :param url_list: List of URL objects to process.
        :return: A new list of URL objects extracted from image sources, each with the original URL as referrer.
        :raises CommandError: If arguments are provided or a user-facing error occurs.
        """
        if args:
            raise CommandError("img command takes no arguments.")
        new_urls: list[URL] = []
        for url in url_list:
            try:
                resp = url.get()
                resp.raise_for_status()
            except Exception as e:
                print(f"Error fetching {url.url}: {e}")
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            for img in soup.find_all("img", src=True):
                src_get = getattr(img, "get", None)
                if not callable(src_get):
                    continue
                src_val = src_get("src")
                if not isinstance(src_val, str):
                    continue
                full_url = urljoin(url.url, src_val)
                new_urls.append(URL(full_url, headers={"Referer": url.url}))
        return new_urls
