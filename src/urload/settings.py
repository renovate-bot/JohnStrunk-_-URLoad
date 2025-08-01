"""Settings infrastructure for URLoad application."""

import os

import tomlkit
from pydantic_settings import BaseSettings, SettingsConfigDict

CONFIG_FILE = os.environ.get("URLOAD_CONFIG_FILE", "urload.toml")


class AppSettings(BaseSettings):
    """Application settings for URLoad."""

    filename_template: str = "{index:04d}_{filename}"
    time_format: str = "%Y%m%d%H%M%S"
    session_dir_num: int = 0  # Track highest session directory

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @classmethod
    def load(cls) -> "AppSettings":
        """Load settings from urload.toml if it exists, else use defaults."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = tomlkit.parse(f.read())

            def extract_value(v: object) -> str:
                if hasattr(v, "value"):
                    return str(getattr(v, "value"))
                if isinstance(v, dict):
                    return str(
                        {
                            str(kk):  # type: ignore
                            extract_value(vv)  # type: ignore
                            for kk, vv in v.items()  # type: ignore
                        }
                    )
                return str(v)

            data_dict: dict[str, str] = {
                str(k):  # type: ignore
                extract_value(v)
                for k, v in dict(data).items()  # type: ignore
            }
            # Ensure session_dir_num is int
            session_dir_num = 0
            if "session_dir_num" in data_dict:
                try:
                    session_dir_num = int(data_dict.pop("session_dir_num"))
                except Exception:
                    session_dir_num = 0
            return cls(session_dir_num=session_dir_num, **data_dict)
        return cls()

    def save(self) -> None:
        """Save current settings to urload.toml."""
        doc = tomlkit.document()
        for key, value in self.model_dump().items():
            doc[key] = value
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(tomlkit.dumps(doc, sort_keys=True))  # type: ignore
