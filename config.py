"""Configuration loading and validation for the PenTest Agent."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv


class ConfigError(RuntimeError):
    """Raised when required configuration is missing or invalid."""


@dataclass
class Settings:
    """Validated runtime settings for the PenTest Agent."""

    openai_api_key: str
    firebase_credentials_path: Path
    openai_model: str = "gpt-4"
    chromadb_persist_dir: Path = field(default_factory=lambda: Path("./chroma_db"))

    @classmethod
    def from_env(cls, env_path: str = ".env") -> "Settings":
        """Load and validate settings from environment variables."""

        load_dotenv(env_path)

        openai_api_key = cls._required("OPENAI_API_KEY")
        firebase_credentials_path = Path(cls._required("FIREBASE_CREDENTIALS_PATH"))

        if not firebase_credentials_path.exists():
            raise ConfigError(
                f"FIREBASE_CREDENTIALS_PATH does not exist: {firebase_credentials_path}"
            )

        openai_model = cls._optional("OPENAI_MODEL", default="gpt-4")
        chromadb_dir = Path(cls._optional("CHROMADB_PERSIST_DIR", default="./chroma_db"))

        return cls(
            openai_api_key=openai_api_key,
            firebase_credentials_path=firebase_credentials_path,
            openai_model=openai_model,
            chromadb_persist_dir=chromadb_dir,
        )

    @staticmethod
    def _required(name: str) -> str:
        value = os.getenv(name)
        if value:
            return value
        raise ConfigError(f"Missing required environment variable: {name}")

    @staticmethod
    def _optional(name: str, default: str) -> str:
        return os.getenv(name, default)

    def safe_dict(self) -> Dict[str, str]:
        """Return a log-safe view of settings with secrets masked."""

        masked_key = f"{self.openai_api_key[:4]}..." if self.openai_api_key else ""
        return {
            "openai_api_key": masked_key,
            "firebase_credentials_path": str(self.firebase_credentials_path),
            "openai_model": self.openai_model,
            "chromadb_persist_dir": str(self.chromadb_persist_dir),
        }


__all__ = ["Settings", "ConfigError"]
