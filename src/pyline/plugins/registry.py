"""Built-in plugin registry.

Plugins may also be discovered via entry points (see pyproject).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyline.plugins.base import Plugin

BUILTIN_PLUGINS: dict[str, type[Plugin]] = {}


def register_plugin(name: str, cls: type[Plugin] | None = None) -> type[Plugin]:
    """Register a plugin class under the given name (decorator or direct call)."""

    def _register(plugin_cls: type[Plugin]) -> type[Plugin]:
        BUILTIN_PLUGINS[name] = plugin_cls
        return plugin_cls

    if cls is not None:
        return _register(cls)
    return _register  # type: ignore[return-value]


def _register_builtins() -> None:
    """Import built-in plugins so they self-register."""
    from pyline.plugins import (  # noqa: F401
        example_plugin,
        httpbin_plugin,
        trim_plugin,
    )

    _ = example_plugin, httpbin_plugin, trim_plugin
