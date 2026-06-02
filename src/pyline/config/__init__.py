"""Pipeline configuration loading."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from pyline.exceptions import ConfigError


@dataclass
class PluginSpec:
    """Specification for a single plugin in a pipeline."""

    name: str
    module: str | None = None
    class_name: str | None = None
    config: dict[str, Any] = field(default_factory=dict)
    retry: int = 0


@dataclass
class PipelineConfig:
    """Loaded pipeline definition."""

    name: str
    plugins: list[PluginSpec]


def load_pipeline(path: Path | str) -> PipelineConfig:
    """Load and validate a pipeline YAML file."""
    path = Path(path)
    if not path.is_file():
        raise ConfigError(f"Pipeline config not found: {path}")

    # TODO: merge settings from PYLINE_ENV and config/{env}.yaml
    with path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    if not isinstance(raw, dict):
        raise ConfigError("Pipeline config must be a YAML mapping")

    name = raw.get("name")
    if not name or not isinstance(name, str):
        raise ConfigError("Pipeline config requires a string 'name'")

    plugins_raw = raw.get("plugins")
    if not plugins_raw or not isinstance(plugins_raw, list):
        raise ConfigError("Pipeline config requires a non-empty 'plugins' list")

    plugins: list[PluginSpec] = []
    for i, entry in enumerate(plugins_raw):
        if not isinstance(entry, dict):
            raise ConfigError(f"plugins[{i}] must be a mapping")
        plugin_name = entry.get("name")
        if not plugin_name or not isinstance(plugin_name, str):
            raise ConfigError(f"plugins[{i}] requires a string 'name'")
        plugin_config = entry.get("config", {})
        if not isinstance(plugin_config, dict):
            raise ConfigError(f"plugins[{i}].config must be a mapping")
        retry = entry.get("retry", 0)
        if not isinstance(retry, int) or retry < 0:
            raise ConfigError(f"plugins[{i}].retry must be a non-negative integer")
        # TODO: implement retry in load_plugin / APIClient
        plugins.append(
            PluginSpec(
                name=plugin_name,
                module=entry.get("module"),
                class_name=entry.get("class"),
                config=plugin_config,
                retry=retry,
            )
        )

    return PipelineConfig(name=name, plugins=plugins)
