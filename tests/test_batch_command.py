"""Test batch command file execution for URLoad CLI."""

import os
import tempfile
from typing import Any

from urload import __main__


class DummyCommand:
    """A dummy command for testing batch execution."""

    def __init__(self) -> None:
        """Initialize DummyCommand with call tracking."""
        self.calls: list[tuple[list[str], list[list[str]]]] = []

    def run(
        self, args: list[str], url_list: list[list[str]], settings: Any
    ) -> list[list[str]]:
        """Simulate command execution and track calls."""
        self.calls.append((args, list(url_list)))
        return [*url_list, args]


class DummySettings:
    """Dummy settings for testing."""

    def __init__(self) -> None:
        """Initialize DummySettings with session_dir_num."""
        self.session_dir_num = 0

    @staticmethod
    def load() -> "DummySettings":
        """Return a DummySettings instance."""
        return DummySettings()

    def save(self) -> None:
        """Save settings (dummy implementation)."""
        pass


def test_batch_file_exec(monkeypatch: Any) -> None:
    """Test that batch command files are executed before interactive mode."""
    dummy = DummyCommand()
    command_objs = {"dummy": dummy}
    monkeypatch.setattr(__main__, "build_command_objs", lambda: command_objs)
    monkeypatch.setattr(__main__, "AppSettings", DummySettings)
    monkeypatch.setattr(__main__, "get_next_numeric_dir", lambda base: 0)  # type: ignore

    with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
        tf.write("dummy foo\ndummy bar\n\n")
        tf.flush()
        tfname = tf.name

    monkeypatch.setattr(__main__, "sys", type("Sys", (), {"argv": ["prog", tfname]}))

    class DummySession:
        def __init__(self, *a: Any, **kw: Any) -> None:
            pass

        def prompt(self, *a: Any, **kw: Any) -> str:
            raise EOFError()

    monkeypatch.setattr(__main__, "PromptSession", DummySession)

    __main__.main()
    os.unlink(tfname)
    assert dummy.calls == [(["foo"], []), (["bar"], [["foo"]])]

    def dummy_next_numeric_dir(base: str) -> int:
        return 0

    monkeypatch.setattr(__main__, "get_next_numeric_dir", dummy_next_numeric_dir)
