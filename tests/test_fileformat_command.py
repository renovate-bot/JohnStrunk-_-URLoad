"""Tests for the FileformatCommand."""

import pytest

from urload.commands.base import CommandError
from urload.commands.fileformat import FileformatCommand
from urload.settings import AppSettings, get_active_settings


def test_fileformat_prints_current(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """It prints the current filename template from settings when called with no args."""
    settings = AppSettings()
    settings.filename_template = "xyz_{filename}"
    monkeypatch.setattr("urload.settings.get_active_settings", lambda: settings)
    cmd = FileformatCommand()
    cmd.run([], [])
    out = capsys.readouterr().out.strip()
    assert out == settings.filename_template


def test_fileformat_sets_valid(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """It sets a valid filename template and prints confirmation."""
    settings = AppSettings()
    monkeypatch.setattr("urload.settings.get_active_settings", lambda: settings)
    cmd = FileformatCommand()
    new_template = "{timestamp}_{host}_{basename}.{ext}"
    cmd.run([new_template], [])
    out = capsys.readouterr().out.strip()
    assert get_active_settings().filename_template == new_template
    assert f"Filename template set to: {new_template}" in out


def test_fileformat_rejects_invalid(monkeypatch: pytest.MonkeyPatch) -> None:
    """It raises CommandError for an invalid template string."""
    settings = AppSettings()
    monkeypatch.setattr("urload.settings.get_active_settings", lambda: settings)
    cmd = FileformatCommand()
    with pytest.raises(CommandError):
        cmd.run(["{not_a_param}"], [])


def test_fileformat_too_many_args(monkeypatch: pytest.MonkeyPatch) -> None:
    """It raises CommandError if more than one argument is given."""
    settings = AppSettings()
    monkeypatch.setattr("urload.settings.get_active_settings", lambda: settings)
    cmd = FileformatCommand()
    with pytest.raises(CommandError):
        cmd.run(["foo", "bar"], [])
