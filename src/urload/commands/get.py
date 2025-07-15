"""
get - Download each URL in the list to a file in the current directory.

Each file is named after the final component of the URL path, excluding query parameters.
"""

import textwrap
from datetime import datetime
from urllib.parse import unquote, urlparse

from urload.commands.base import Command
from urload.settings import get_active_settings
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
        settings = get_active_settings()
        dry_run = "-n" in args
        time_fmt = getattr(settings, "time_format", "%Y%m%d%H%M%S")
        template = getattr(settings, "filename_template", "{timestamp}_{filename}")
        now_str = datetime.now().strftime(time_fmt)

        def build_filename(url: str) -> str:
            parsed = urlparse(url)
            host = parsed.hostname or "localhost"
            path = parsed.path or "/"
            dirname, _, filename = path.rpartition("/")
            if not filename:
                filename = "index.html"
            filename = unquote(filename)
            basename, dot, ext = filename.partition(".")
            ext = ext if dot else ""
            return template.format(
                timestamp=now_str,
                basename=basename,
                ext=ext,
                host=host,
                dirname=dirname.lstrip("/"),
                filename=filename,
            )

        if dry_run:
            for idx, url_obj in enumerate(url_list):
                url = url_obj.url
                filename = build_filename(url)
                print(f"[{idx}] {url} {filename}")
            return url_list

        failed_urls: list[URL] = []
        for url_obj in url_list:
            url = url_obj.url
            filename = build_filename(url)
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
