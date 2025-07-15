"""Tests for the set-option and get-option commands."""

from pathlib import Path

import pytest

from urload.commands.get_option import GetOptionCommand
from urload.commands.set_option import SetOptionCommand
from urload.settings import AppSettings
from urload.url import URL


class DummyURL:
    """Dummy URL class for testing option commands."""

    pass


def test_set_and_get_option(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    """Test set-option and get-option commands end-to-end."""
    config_file = tmp_path / "urload.toml"
    monkeypatch.setattr("urload.settings.CONFIG_FILE", str(config_file))
    set_cmd = SetOptionCommand()
    get_cmd = GetOptionCommand()
    url_list: list[URL] = []

    settings = AppSettings()
    set_cmd.run(["filename_template=test_{filename}"], url_list, settings)
    get_cmd.run([], url_list, settings)
    out = capsys.readouterr().out
    assert "filename_template=test_{filename}" in out
    capsys.readouterr()  # clear
    get_cmd.run(["filename_template"], url_list, settings)
    out = capsys.readouterr().out
    assert out.strip() == "filename_template=test_{filename}"
    with pytest.raises(Exception):
        set_cmd.run(["notakey=foo"], url_list, settings)
    with pytest.raises(Exception):
        get_cmd.run(["notakey"], url_list, settings)
