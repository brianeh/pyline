"""PyLine exception types."""


class PyLineError(Exception):
    """Base exception for PyLine."""


class ConfigError(PyLineError):
    """Invalid or missing pipeline configuration."""


class PluginLoadError(PyLineError):
    """Failed to load or instantiate a plugin."""
