"""Example external plugin loaded via module/class in pipeline YAML."""

from pyline.context import PipelineContext
from pyline.plugins.base import Plugin


class HelloPlugin(Plugin):
    name = "hello"

    def run(self, ctx: PipelineContext) -> PipelineContext:
        if isinstance(ctx.data, str):
            ctx.data = f"hello, {ctx.data}"
        return ctx
