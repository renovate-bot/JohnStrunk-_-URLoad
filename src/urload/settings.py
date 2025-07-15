"""Settings infrastructure for URLoad application."""

import os
import tomllib

import toml
from pydantic_settings import BaseSettings, SettingsConfigDict

CONFIG_FILE = os.environ.get("URLOAD_CONFIG_FILE", "urload.toml")


class AppSettings(BaseSettings):
    """Application settings for URLoad."""

    filename_template: str = "{timestamp}_{filename}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @classmethod
    def load(cls) -> "AppSettings":
        """Load settings from urload.toml if it exists, else use defaults."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "rb") as f:
                data = tomllib.load(f)
            return cls(**data)
        return cls()

    def save(self) -> None:
        """Save current settings to urload.toml."""
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            toml.dump(self.model_dump(), f)


# Singleton for active settings
ACTIVE_SETTINGS: AppSettings = AppSettings.load()


def get_active_settings() -> AppSettings:
    """Return the active AppSettings singleton."""
    return ACTIVE_SETTINGS
