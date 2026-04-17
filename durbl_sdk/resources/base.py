"""SDK base resource with shared HTTP methods."""

from __future__ import annotations

from typing import Any

import httpx

from durbl_sdk.exceptions import DurblAPIError


class BaseResource:
    """Base class for SDK resource namespaces."""

    def __init__(self, client: httpx.Client, async_client: httpx.AsyncClient) -> None:
        self._client = client
        self._async_client = async_client

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Handle HTTP response, raising on errors."""
        if response.status_code >= 400:
            try:
                body = response.json()
            except Exception:
                body = {"message": response.text}
            raise DurblAPIError(
                status_code=response.status_code,
                error=body.get("error", "UNKNOWN"),
                message=body.get("message", "Unknown error"),
            )
        return response.json()

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Synchronous GET request."""
        response = self._client.get(path, params=params)
        return self._handle_response(response)

    def _post(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        """Synchronous POST request."""
        response = self._client.post(path, json=json)
        return self._handle_response(response)

    def _put(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        """Synchronous PUT request."""
        response = self._client.put(path, json=json)
        return self._handle_response(response)

    def _delete(self, path: str) -> dict[str, Any]:
        """Synchronous DELETE request."""
        response = self._client.delete(path)
        return self._handle_response(response)

    async def _aget(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Async GET request."""
        response = await self._async_client.get(path, params=params)
        return self._handle_response(response)

    async def _apost(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        """Async POST request."""
        response = await self._async_client.post(path, json=json)
        return self._handle_response(response)

    async def _aput(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        """Async PUT request."""
        response = await self._async_client.put(path, json=json)
        return self._handle_response(response)

    async def _adelete(self, path: str) -> dict[str, Any]:
        """Async DELETE request."""
        response = await self._async_client.delete(path)
        return self._handle_response(response)
