"""Example transform plugin."""

from __future__ import annotations

from pyline.context import PipelineContext
from pyline.plugins.base import Plugin
from pyline.plugins.registry import register_plugin


@register_plugin("uppercase")
class UppercasePlugin(Plugin):
    """Uppercase string pipeline data."""

    name = "uppercase"

    def run(self, ctx: PipelineContext) -> PipelineContext:
        if isinstance(ctx.data, str):
            ctx.data = ctx.data.upper()
        return ctx
