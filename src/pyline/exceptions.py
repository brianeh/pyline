"""PyLine exception types."""


class PyLineError(Exception):
    """Base exception for PyLine."""


class ConfigError(PyLineError):
    """Raised when pipeline YAML is missing or invalid."""


class PluginLoadError(PyLineError):
    """Raised when a plugin cannot be imported or instantiated."""


class APIError(PyLineError):
    """Raised when an outbound API call fails."""
