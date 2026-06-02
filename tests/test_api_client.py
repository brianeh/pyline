"""Tests for APIClient."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from pyline.api.client import APIClient


def test_url_joining() -> None:
    client = APIClient("https://api.example.com/")
    assert client._url("users") == "https://api.example.com/users"
    assert client._url("/users") == "https://api.example.com/users"


@patch("pyline.api.client.requests.Session")
def test_get_success(mock_session_cls: MagicMock) -> None:
    mock_session = MagicMock()
    mock_session_cls.return_value = mock_session
    mock_response = MagicMock()
    mock_response.json.return_value = {"ok": True}
    mock_session.get.return_value = mock_response

    client = APIClient("https://api.example.com", api_key="secret")
    result = client.get("/items", params={"q": "test"})

    assert result == {"ok": True}
    mock_session.get.assert_called_once()
    call_kwargs = mock_session.get.call_args
    assert call_kwargs[0][0] == "https://api.example.com/items"
    assert call_kwargs[1]["params"]["api_key"] == "secret"
    assert call_kwargs[1]["params"]["q"] == "test"
    mock_response.raise_for_status.assert_called_once()


@patch("pyline.api.client.requests.Session")
def test_get_raises_on_http_error(mock_session_cls: MagicMock) -> None:
    mock_session = MagicMock()
    mock_session_cls.return_value = mock_session
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404")
    mock_session.get.return_value = mock_response

    client = APIClient("https://api.example.com")
    with pytest.raises(requests.HTTPError):
        client.get("/missing")


@patch("pyline.api.client.requests.Session")
def test_bearer_token_header(mock_session_cls: MagicMock) -> None:
    mock_session = MagicMock()
    mock_session_cls.return_value = mock_session
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_session.get.return_value = mock_response

    client = APIClient("https://api.example.com", bearer_token="tok123")
    client.get("/me")

    headers = mock_session.get.call_args[1]["headers"]
    assert headers["Authorization"] == "Bearer tok123"
