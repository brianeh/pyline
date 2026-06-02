"""Tests for plugin loading."""

from pathlib import Path

import pytest

from pyline.config import PluginSpec
from pyline.context import PipelineContext
from pyline.exceptions import PluginLoadError
from pyline.plugins.base import Plugin
from pyline.plugins.loader import _FunctionPlugin, load_plugin, load_plugins
from pyline.plugins.registry import BUILTIN_PLUGINS, _register_builtins


def test_load_builtin_uppercase() -> None:
    _register_builtins()
    plugin = load_plugin(PluginSpec(name="uppercase"))
    assert plugin.name == "uppercase"
    ctx = plugin.run(PipelineContext(data="hello"))
    assert ctx.data == "HELLO"


def test_load_plugins_order() -> None:
    _register_builtins()
    specs = [
        PluginSpec(name="uppercase"),
        PluginSpec(name="uppercase"),
    ]
    plugins = load_plugins(specs)
    assert len(plugins) == 2


def test_load_unknown_plugin() -> None:
    with pytest.raises(PluginLoadError, match="Unknown plugin"):
        load_plugin(PluginSpec(name="nonexistent_plugin_xyz"))


def test_function_plugin_adapter() -> None:
    class FakeModule:
        @staticmethod
        def run(data: object) -> object:
            return f"wrapped:{data}"

    plugin = _FunctionPlugin(FakeModule(), name="fake")
    ctx = plugin.run(PipelineContext(data="x"))
    assert ctx.data == "wrapped:x"


def test_registry_contains_builtins() -> None:
    _register_builtins()
    assert "uppercase" in BUILTIN_PLUGINS
    assert "httpbin" in BUILTIN_PLUGINS
