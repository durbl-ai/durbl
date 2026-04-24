"""Shared HTTP plumbing for resource namespaces.

Each public resource (memory, state, context, …) inherits from
:class:`BaseResource` to get the underscore-prefixed transport helpers
(``_get``/``_post``/etc.). Errors are mapped to the typed exception
classes in :mod:`durbl_sdk.exceptions` so callers can pattern-match on
``except DurblNotFoundError`` instead of inspecting status codes.
"""

from __future__ import annotations

from typing import Any

import httpx

from durbl_sdk.exceptions import (
    DurblAPIError,
    DurblAuthError,
    DurblConnectionError,
    DurblNotFoundError,
    DurblRateLimitError,
    DurblServerError,
)


def _error_for_status(status: int) -> type[DurblAPIError]:
    if status in (401, 403):
        return DurblAuthError
    if status == 404:
        return DurblNotFoundError
    if status == 429:
        return DurblRateLimitError
    if status >= 500:
        return DurblServerError
    return DurblAPIError


class BaseResource:
    """Base class for SDK resource namespaces."""

    def __init__(self, client: httpx.Client, async_client: httpx.AsyncClient) -> None:
        self._client = client
        self._async_client = async_client

    # ── Response handling ────────────────────────────────────────────

    def _handle_response(self, response: httpx.Response) -> Any:
        """Decode the response, raising a typed error on 4xx/5xx.

        Returns the parsed JSON body. The response may be a list, a dict,
        or a primitive — callers should not assume a dict.
        """
        if response.status_code >= 400:
            try:
                body = response.json()
            except Exception:
                body = {"message": response.text}

            if isinstance(body, dict):
                error_code = body.get("error", "UNKNOWN")
                message = body.get("message") or body.get("error") or "Unknown error"
            else:
                error_code = "UNKNOWN"
                message = str(body) if body else "Unknown error"

            cls = _error_for_status(response.status_code)
            raise cls(
                status_code=response.status_code,
                error=error_code,
                message=message,
                body=body,
            )

        # 204 No Content / empty bodies → return {} for ergonomics.
        if not response.content:
            return {}
        try:
            return response.json()
        except ValueError as exc:
            raise DurblAPIError(
                status_code=response.status_code,
                error="INVALID_JSON",
                message=f"server returned non-JSON: {response.text[:200]}",
            ) from exc

    # ── Sync transport ───────────────────────────────────────────────

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        try:
            response = self._client.request(method, path, **kwargs)
        except httpx.HTTPError as exc:
            raise DurblConnectionError(f"{method} {path} failed: {exc}") from exc
        return self._handle_response(response)

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return self._request("GET", path, params=params)

    def _post(self, path: str, json: dict[str, Any] | None = None) -> Any:
        return self._request("POST", path, json=json)

    def _put(self, path: str, json: dict[str, Any] | None = None) -> Any:
        return self._request("PUT", path, json=json)

    def _delete(self, path: str) -> Any:
        return self._request("DELETE", path)

    # ── Async transport ──────────────────────────────────────────────

    async def _arequest(self, method: str, path: str, **kwargs: Any) -> Any:
        try:
            response = await self._async_client.request(method, path, **kwargs)
        except httpx.HTTPError as exc:
            raise DurblConnectionError(f"{method} {path} failed: {exc}") from exc
        return self._handle_response(response)

    async def _aget(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return await self._arequest("GET", path, params=params)

    async def _apost(self, path: str, json: dict[str, Any] | None = None) -> Any:
        return await self._arequest("POST", path, json=json)

    async def _aput(self, path: str, json: dict[str, Any] | None = None) -> Any:
        return await self._arequest("PUT", path, json=json)

    async def _adelete(self, path: str) -> Any:
        return await self._arequest("DELETE", path)
