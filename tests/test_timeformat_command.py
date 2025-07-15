"""Tests for the TimeformatCommand."""

import pytest

from urload.commands.base import CommandError
from urload.commands.timeformat import TimeformatCommand
from urload.settings import AppSettings


def test_timeformat_prints_current(capsys: pytest.CaptureFixture[str]) -> None:
    """It prints the current time format from settings when called with no args."""
    settings = AppSettings()
    cmd = TimeformatCommand()
    cmd.run([], [], settings)
    out = capsys.readouterr().out.strip()
    assert out == "%Y%m%d%H%M%S"


def test_timeformat_sets_valid(capsys: pytest.CaptureFixture[str]) -> None:
    """It sets a valid time format string and prints confirmation."""
    settings = AppSettings()
    cmd = TimeformatCommand()
    cmd.run(["%Y-%m-%d"], [], settings)
    out = capsys.readouterr().out.strip()
    assert settings.time_format == "%Y-%m-%d"
    assert "Time format set to: %Y-%m-%d" in out


def test_timeformat_rejects_invalid() -> None:
    """It raises CommandError for an invalid strftime format string."""
    settings = AppSettings()
    cmd = TimeformatCommand()
    with pytest.raises(CommandError):
        cmd.run(["%Q"], [], settings)


def test_timeformat_too_many_args() -> None:
    """It raises CommandError if more than one argument is given."""
    settings = AppSettings()
    cmd = TimeformatCommand()
    with pytest.raises(CommandError):
        cmd.run(["foo", "bar"], [], settings)
