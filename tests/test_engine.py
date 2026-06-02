"""Tests for PyLineEngine."""

from pyline.context import PipelineContext
from pyline.core import PyLineEngine
from pyline.plugins.base import Plugin


class _DoublePlugin(Plugin):
    name = "double"

    def run(self, ctx: PipelineContext) -> PipelineContext:
        if isinstance(ctx.data, int):
            ctx.data *= 2
        return ctx


class _AddMetaPlugin(Plugin):
    name = "meta"

    def run(self, ctx: PipelineContext) -> PipelineContext:
        ctx.metadata["seen"] = ctx.data
        return ctx


def test_engine_runs_plugins_in_order() -> None:
    engine = PyLineEngine([_DoublePlugin(), _DoublePlugin()], pipeline_name="test")
    ctx = engine.run(initial_data=3)
    assert ctx.data == 12


def test_engine_passes_context() -> None:
    engine = PyLineEngine([_AddMetaPlugin()], pipeline_name="test")
    ctx = engine.run(initial_data="hi")
    assert ctx.metadata["seen"] == "hi"
