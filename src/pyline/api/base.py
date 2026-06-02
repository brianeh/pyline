"""API plugin base class."""

from __future__ import annotations

from abc import abstractmethod
from typing import Any

from pyline.api.client import APIClient
from pyline.context import PipelineContext
from pyline.plugins.base import Plugin


class APIPlugin(Plugin):
    """Plugin that fetches data from a web API via APIClient."""

    name = "api"

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        **client_kwargs: Any,
    ) -> None:
        self.client = APIClient(base_url, api_key, **client_kwargs)

    @abstractmethod
    def request(self, ctx: PipelineContext) -> Any:
        """Perform the API call and return response data."""

    def run(self, ctx: PipelineContext) -> PipelineContext:
        ctx.data = self.request(ctx)
