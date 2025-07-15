"""Tests for the FileformatCommand."""

import pytest

from urload.commands.base import CommandError
from urload.commands.fileformat import FileformatCommand
from urload.settings import AppSettings


def test_fileformat_prints_current(capsys: pytest.CaptureFixture[str]) -> None:
    """It prints the current filename template from settings when called with no args."""
    settings = AppSettings()
    settings.filename_template = "xyz_{filename}"
    cmd = FileformatCommand()
    cmd.run([], [], settings)
    out = capsys.readouterr().out.strip()
    assert out == settings.filename_template


def test_fileformat_sets_valid(capsys: pytest.CaptureFixture[str]) -> None:
    """It sets a valid filename template and prints confirmation."""
    settings = AppSettings()
    cmd = FileformatCommand()
    new_template = "{timestamp}_{host}_{basename}.{ext}"
    cmd.run([new_template], [], settings)
    out = capsys.readouterr().out.strip()
    assert settings.filename_template == new_template
    assert f"Filename template set to: {new_template}" in out


def test_fileformat_rejects_invalid() -> None:
    """It raises CommandError for an invalid template string."""
    settings = AppSettings()
    cmd = FileformatCommand()
    with pytest.raises(CommandError):
        cmd.run(["{not_a_param}"], [], settings)


def test_fileformat_too_many_args() -> None:
    """It raises CommandError if more than one argument is given."""
    settings = AppSettings()
    cmd = FileformatCommand()
    with pytest.raises(CommandError):
        cmd.run(["foo", "bar"], [], settings)
