"""
get - Download each URL in the list to a file in the current directory.

Each file is named after the final component of the URL path, excluding query parameters.
"""

import os
import textwrap
from datetime import datetime
from pathlib import PurePath
from urllib.parse import unquote, urlparse

from urload.commands.base import Command
from urload.settings import AppSettings
from urload.url import URL

# Module-level variable to persist index across GetCommand invocations
_get_index = 0


class GetCommand(Command):
    """Download each URL in the list to a file in the current directory, or perform a dry run."""

    name = "get"
    description = textwrap.dedent("""
    get [-n] - Download each URL in the list to a file in the current directory.

    Each file is named after the final component of the URL path, excluding query parameters.
    If -n is given, perform a dry run: print the index, URL, and filename for each URL, but do not download anything.
    """)

    def run(
        self, args: list[str], url_list: list[URL], settings: AppSettings
    ) -> list[URL]:
        """
        Download each URL to a file named after the final path component, or perform a dry run.

        :param args: List of command-line arguments. If '-n' is present, do a dry run.
        :param url_list: List of URLs to download.
        :param settings: The AppSettings object.
        :return: List of URLs that failed to download, or the original list if dry run.
        """
        global _get_index  # noqa: PLW0603
        dry_run = "-n" in args
        time_fmt = getattr(settings, "time_format", "%Y%m%d%H%M%S")
        template = getattr(settings, "filename_template", "{timestamp}_{filename}")
        now_str = datetime.now().strftime(time_fmt)

        # Determine session directory
        session_dir = f"{settings.session_dir_num:04d}"
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)

        current_index = _get_index

        if dry_run:
            for url in url_list:
                fname = build_filename(template, now_str, url.url, current_index)
                print(f"[{current_index}] {url.url} {fname}")
                current_index += 1
            return url_list

        failed: list[URL] = []
        for url in url_list:
            fname = build_filename(template, now_str, url.url, current_index)
            out_path = os.path.join(session_dir, fname)
            try:
                print(f"[{current_index}] {url.url} -> {out_path}", end="", flush=True)
                resp = url.get()
                resp.raise_for_status()
                with open(out_path, "wb") as f:
                    f.write(resp.content)
                print(" [ok]")
            except Exception as e:
                print(f"Failed to download {url}: {e}")
                failed.append(url)
                print(" [FAILED]")
            current_index += 1
        _get_index = current_index
        return failed


def build_filename(template: str, time: str, url: str, index: int) -> str:
    """
    Build a filename for a downloaded URL using a template and metadata.

    :param template: Filename template string with placeholders
    :param time: Timestamp string for the download
    :param url: The URL to be downloaded
    :param index: The index of the URL in the list
    :return: The formatted filename string
    """
    parsed = urlparse(url)
    host = parsed.hostname or "localhost"
    path = parsed.path or "/"
    dirname, _, filename = path.rpartition("/")
    if not filename:
        filename = "index.html"
    filename = unquote(filename.split("?")[0])
    # Remove any path traversal from filename
    filename = PurePath(filename).name
    basename, dot, ext = filename.partition(".")
    ext = ext if dot else ""
    ext = ext.split("?")[0]
    # Sanitize dirname: remove traversal and collapse slashes
    dirname = unquote(dirname)
    dirname = dirname.replace("\\", "/")
    parts = [p for p in dirname.split("/") if p not in ("", ".", "..")]
    safe_dirname = "/".join(parts)
    # Never allow leading slash or traversal
    safe_dirname = safe_dirname.lstrip("/")
    # Compose the filename
    result = template.format(
        timestamp=time,
        basename=basename,
        ext=ext,
        host=host,
        dirname=safe_dirname,
        filename=filename,
        index=index,
    )
    # Final check: never allow traversal or leading slash
    result = result.replace("\\", "/")
    result = result.lstrip("/")
    while ".." in result:
        result = result.replace("..", "")
    return result
