"""Tests for the TimeformatCommand."""

import pytest

from urload.commands.base import CommandError
from urload.commands.timeformat import TimeformatCommand
from urload.settings import AppSettings, get_active_settings


def test_timeformat_prints_current(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """It prints the current time format from settings when called with no args."""
    settings = AppSettings()
    monkeypatch.setattr("urload.settings.get_active_settings", lambda: settings)
    cmd = TimeformatCommand()
    cmd.run([], [])
    out = capsys.readouterr().out.strip()
    assert out == "%Y%m%d%H%M%S"


def test_timeformat_sets_valid(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """It sets a valid time format string and prints confirmation."""
    settings = AppSettings()
    monkeypatch.setattr("urload.settings.get_active_settings", lambda: settings)
    cmd = TimeformatCommand()
    cmd.run(["%Y-%m-%d"], [])
    out = capsys.readouterr().out.strip()
    # Check via get_active_settings() to ensure we see the monkeypatched value
    assert get_active_settings().time_format == "%Y-%m-%d"
    assert "Time format set to: %Y-%m-%d" in out


def test_timeformat_rejects_invalid(monkeypatch: pytest.MonkeyPatch) -> None:
    """It raises CommandError for an invalid strftime format string."""
    settings = AppSettings()
    monkeypatch.setattr("urload.settings.get_active_settings", lambda: settings)
    cmd = TimeformatCommand()
    with pytest.raises(CommandError):
        cmd.run(["%Q"], [])


def test_timeformat_too_many_args(monkeypatch: pytest.MonkeyPatch) -> None:
    """It raises CommandError if more than one argument is given."""
    settings = AppSettings()
    monkeypatch.setattr("urload.settings.get_active_settings", lambda: settings)
    cmd = TimeformatCommand()
    with pytest.raises(CommandError):
        cmd.run(["foo", "bar"], [])
