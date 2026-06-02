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
        self._base_url: str | None = None
        self._retry = 0

    def configure(self, config: dict[str, Any]) -> None:
        self._path = config.get("path", "/get")
        self._params = dict(config.get("params", {}))
        self._base_url = config.get("base_url")
        self._retry = config.get("retry", 0)

    def _get_with_retry(
        self, path: str, *, params: dict[str, Any] | None = None
    ) -> Any:
        attempts = max(1, int(self._retry) + 1)
        last_error: Exception | None = None
        for _ in range(attempts):
            try:
                return self.client.get(path, params=params)
            except Exception as e:
                last_error = e
        if last_error is not None:
            raise last_error
        return self.client.get(path, params=params)

    def request(self, ctx: PipelineContext) -> Any:
        params = dict(self._params)
        if isinstance(ctx.data, str) and ctx.data:
            params.setdefault("input", ctx.data)
        url = self.client._url(self._path)
        ctx.metadata["httpbin_url"] = url
        ctx.metadata["httpbin_params"] = params
        ctx.metadata["session"] = self.client._session
        return self._get_with_retry(self._path, params=params)

    def run(self, ctx: PipelineContext) -> PipelineContext:
        ctx.data = self.request(ctx)
        return ctx
