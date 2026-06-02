"""Plugin base classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pyline.context import PipelineContext


class Plugin(ABC):
    """Base class for pipeline plugins."""

    name: str = "plugin"

    def configure(self, config: dict[str, Any]) -> None:
        """Apply per-plugin settings from pipeline YAML; must be implemented by subclasses."""

    @abstractmethod
    def run(self, ctx: PipelineContext) -> PipelineContext:
        """Transform context and return it for the next plugin."""
