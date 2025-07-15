"""Tests for the settings infrastructure."""

import os
from pathlib import Path

from urload.settings import AppSettings


def test_settings_load_and_save(tmp_path: Path) -> None:
    """Test that settings can be saved and loaded from TOML file."""
    config_file = tmp_path / "urload.toml"
    # Patch the config file path for this test
    orig_env = os.environ.get("URLOAD_CONFIG_FILE")
    os.environ["URLOAD_CONFIG_FILE"] = str(config_file)
    settings = AppSettings(filename_template="abc_{filename}")
    settings.save()
    loaded = AppSettings.load()
    assert loaded.filename_template == "abc_{filename}"
    loaded.filename_template = "xyz_{filename}"
    loaded.save()
    loaded2 = AppSettings.load()
    assert loaded2.filename_template == "xyz_{filename}"
    if config_file.exists():
        config_file.unlink()
    if orig_env is not None:
        os.environ["URLOAD_CONFIG_FILE"] = orig_env
    else:
        del os.environ["URLOAD_CONFIG_FILE"]
