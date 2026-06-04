"""Demo API plugin against httpbin.org."""

from __future__ import annotations

from typing import Any

from pyline.api.base import APIPlugin
from pyline.context import PipelineContext
from pyline.plugins.registry import register_plugin

HTTPBIN_BASE_URL = "https://httpbin.org"


@register_plugin("httpbin")
class HttpbinPlugin(APIPlugin):
    """GET request to httpbin.org; useful as an API plugin example."""

    name = "httpbin"

    def __init__(self) -> None:
        super().__init__(HTTPBIN_BASE_URL)
        self._path = "/get"
        self._params: dict[str, Any] = {}

    def configure(self, config: dict[str, Any]) -> None:
        self._path = config.get("path", "/get")
        self._params = dict(config.get("params", {}))

    def request(self, ctx: PipelineContext) -> Any:
        params = dict(self._params)
        if isinstance(ctx.data, str) and ctx.data:
            params.setdefault("input", ctx.data)
        url = self.client._url(self._path)
        ctx.metadata["httpbin_url"] = url
        ctx.metadata["httpbin_params"] = params
        return self.client.get(self._path, params=params)
