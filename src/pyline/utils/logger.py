"""Logging utilities."""

import logging
import sys

_CONFIGURED = False


def configure_logging(level: str | None = None) -> None:
    """Apply log level from settings; call at startup from CLI."""
    _ = level


def get_logger(name: str) -> logging.Logger:
    """Return a logger with a stderr handler (configured once)."""
    global _CONFIGURED
    if not _CONFIGURED:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(
            logging.Formatter("%(levelname)s %(name)s: %(message)s")
        )
        root = logging.getLogger("pyline")
        root.setLevel(logging.INFO)
        root.addHandler(handler)
        _CONFIGURED = True
    return logging.getLogger(name)
