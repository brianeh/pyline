"""Tests for HttpbinPlugin (mocked HTTP)."""

from unittest.mock import MagicMock, patch

from pyline.context import PipelineContext
from pyline.plugins.httpbin_plugin import HttpbinPlugin


@patch.object(HttpbinPlugin, "__init__", lambda self: None)
def test_httpbin_request_sets_metadata() -> None:
    plugin = HttpbinPlugin.__new__(HttpbinPlugin)
    plugin.client = MagicMock()
    plugin.client.get.return_value = {"args": {"input": "HELLO"}}
    plugin.client._url = lambda path: f"https://httpbin.org{path}"
    plugin._path = "/get"
    plugin._params = {"foo": "bar"}
    plugin._retry = 0

    ctx = PipelineContext(data="HELLO")
    result = plugin.request(ctx)

    assert result == {"args": {"input": "HELLO"}}
    assert "httpbin_url" in ctx.metadata
    plugin.client.get.assert_called_once_with(
        "/get", params={"foo": "bar", "input": "HELLO"}
    )
