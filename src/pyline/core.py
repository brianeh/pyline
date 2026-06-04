"""PyLine pipeline engine."""

from __future__ import annotations

from pathlib import Path

from pyline.config import PipelineConfig, load_pipeline
from pyline.context import PipelineContext
from pyline.plugins.base import Plugin
from pyline.plugins.loader import load_plugins
from pyline.utils.logger import get_logger

logger = get_logger(__name__)


class PyLineEngine:
    """Runs an ordered list of plugins over a shared context."""

    def __init__(self, plugins: list[Plugin], *, pipeline_name: str = "pipeline") -> None:
        self.plugins = plugins
        self.pipeline_name = pipeline_name

    @classmethod
    def from_config(cls, path: Path | str) -> PyLineEngine:
        """Build an engine from a pipeline YAML file."""
        config = load_pipeline(path)
        plugins = load_plugins(config.plugins)
        return cls(plugins, pipeline_name=config.name)

    def run(self, initial_data: object = None) -> PipelineContext:
        """Execute all plugins sequentially."""
        ctx = PipelineContext(data=initial_data)
        logger.info("Running pipeline %s (%d plugins)", self.pipeline_name, len(self.plugins))
        for plugin in self.plugins:
            logger.info("Running plugin %s", plugin.name)
            ctx = plugin.run(ctx)
        return ctx
