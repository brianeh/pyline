"""Environment-backed settings (global defaults for pipelines and APIs)."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    env: str
    httpbin_base_url: str
    log_level: str


def get_settings() -> Settings:
    """Load settings from PYLINE_* environment variables."""
    return Settings(
        env=os.environ.get("PYLINE_ENV", "dev"),
        httpbin_base_url=os.environ.get(
            "HTTPBIN_BASE_URL", "https://httpbin.org"
        ),
        log_level=os.environ.get("PYLINE_LOG_LEVEL", "INFO"),
    )
