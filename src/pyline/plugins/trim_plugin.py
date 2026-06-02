"""Trim whitespace from string pipeline data."""

from __future__ import annotations

from pyline.context import PipelineContext
from pyline.plugins.base import Plugin
from pyline.plugins.registry import register_plugin


@register_plugin("trim")
class TrimPlugin(Plugin):
    """Strip leading and trailing whitespace from string data."""

    name = "trim"

    def run(self, ctx: PipelineContext) -> PipelineContext:
        if isinstance(ctx.data, str):
            ctx.data = ctx.data.strip()
        # bottleneck for large nested structures
        # TODO: support list[str] and nested structures
        return ctx
