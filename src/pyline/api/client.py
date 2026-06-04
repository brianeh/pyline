"""HTTP API client wrapper."""

from __future__ import annotations

from typing import Any

import requests


class APIClient:
    """Thin wrapper around requests for REST APIs."""

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        *,
        api_key_param: str = "api_key",
        bearer_token: str | None = None,
        default_headers: dict[str, str] | None = None,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.api_key_param = api_key_param
        self.bearer_token = bearer_token
        self.default_headers = dict(default_headers or {})
        self._session = session or requests.Session()

    def _url(self, path: str) -> str:
        path = path if path.startswith("/") else f"/{path}"
        return f"{self.base_url}{path}"

    def _headers(self, headers: dict[str, str] | None) -> dict[str, str]:
        merged = dict(self.default_headers)
        if self.bearer_token:
            merged.setdefault("Authorization", f"Bearer {self.bearer_token}")
        if headers:
            merged.update(headers)
        return merged

    def _params_with_key(self, params: dict[str, Any] | None) -> dict[str, Any]:
        out = dict(params or {})
        if self.api_key:
            out.setdefault(self.api_key_param, self.api_key)
        return out

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        response = self._session.get(
            self._url(path),
            params=self._params_with_key(params),
            headers=self._headers(headers),
        )
        response.raise_for_status()
        return response.json()

    def post(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        response = self._session.post(
            self._url(path),
            params=self._params_with_key(params),
            json=json,
            headers=self._headers(headers),
        )
        response.raise_for_status()
        return response.json()
