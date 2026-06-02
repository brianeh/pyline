"""Plugin loading from pipeline specs."""

from __future__ import annotations

import importlib
import importlib.util
from pathlib import Path
from typing import Any

from pyline.config import PluginSpec
from pyline.context import PipelineContext
from pyline.exceptions import PluginLoadError
from pyline.plugins.base import Plugin
from pyline.plugins.registry import BUILTIN_PLUGINS, _register_builtins
from pyline.utils.logger import get_logger

logger = get_logger(__name__)

PLUGIN_FOLDER = Path(__file__).parent


class _FunctionPlugin(Plugin):
    """Adapter for legacy module-level run(data) plugins."""

    def __init__(self, module: Any, name: str) -> None:
        self._module = module
        self.name = name

    def run(self, ctx: PipelineContext) -> PipelineContext:
        ctx.data = self._module.run(ctx.data)
        return ctx


def _load_from_module_path(module_path: str, class_name: str) -> type[Plugin]:
    try:
        module = importlib.import_module(module_path)
    except ImportError as e:
        raise PluginLoadError(f"Cannot import module {module_path!r}: {e}") from e
    if not hasattr(module, class_name):
        raise PluginLoadError(
            f"Module {module_path!r} has no class {class_name!r}"
        )
    cls = getattr(module, class_name)
    if not isinstance(cls, type) or not issubclass(cls, Plugin):
        raise PluginLoadError(f"{module_path}.{class_name} is not a Plugin subclass")
    return cls


def _load_legacy_module(file: Path) -> Plugin | None:
    spec = importlib.util.spec_from_file_location(file.stem, file)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "run") and callable(module.run):
        return _FunctionPlugin(module, name=file.stem)
    if hasattr(module, "Plugin"):
        cls = module.Plugin
        if isinstance(cls, type) and issubclass(cls, Plugin):
            return cls()
    return None


def load_plugin(spec: PluginSpec) -> Plugin:
    """Instantiate a single plugin from a spec."""
    _register_builtins()

    if spec.module and spec.class_name:
        cls = _load_from_module_path(spec.module, spec.class_name)
        # TODO: verify plugin.name matches spec.name
        plugin = cls()
    elif spec.name in BUILTIN_PLUGINS:
        plugin = BUILTIN_PLUGINS[spec.name]()
    else:
        file = PLUGIN_FOLDER / f"{spec.name}.py"
        if file.is_file():
            legacy = _load_legacy_module(file)
            if legacy is not None:
                plugin = legacy
            else:
                raise PluginLoadError(
                    f"Plugin file {file.name} has no run() or Plugin class"
                )
        else:
            raise PluginLoadError(
                f"Unknown plugin {spec.name!r}; not in registry and no file {file}"
            )

    if spec.config:
        plugin.configure(spec.config)

    logger.info("Loaded plugin %s", plugin.name)
    return plugin


def load_plugins(specs: list[PluginSpec]) -> list[Plugin]:
    """Load plugins in pipeline order."""
    return [load_plugin(spec) for spec in specs]
