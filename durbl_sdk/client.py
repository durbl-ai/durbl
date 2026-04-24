"""Public client class — ``from durbl_sdk import Durbl``."""

from __future__ import annotations

import os
from typing import Any

import httpx

from durbl_sdk.exceptions import DurblConfigError
from durbl_sdk.resources.context import ContextResource
from durbl_sdk.resources.events import EventsResource
from durbl_sdk.resources.intelligence import IntelligenceResource
from durbl_sdk.resources.lifecycle import LifecycleResource
from durbl_sdk.resources.memory import MemoryResource
from durbl_sdk.resources.policies import PoliciesResource
from durbl_sdk.resources.state import StateResource


DEFAULT_BASE_URL = "https://durbl-server-302549088008.me-central1.run.app"
DEFAULT_TIMEOUT = 30.0


class Durbl:
    """Synchronous + async client for the Durbl memory engine.

    Args:
        api_key: Project API key (starts with ``drbl_``). If omitted, the
            client falls back to the ``DURBL_API_KEY`` environment variable.
        base_url: API base URL. Defaults to the production endpoint; override
            for local development (``http://localhost:8000``) or via the
            ``DURBL_BASE_URL`` environment variable.
        timeout: Per-request timeout in seconds (default 30s).
        http_client: Optional pre-built ``httpx.Client``. Useful for tests
            (transport mocking) or custom proxy/cert configuration.
        async_http_client: Optional pre-built ``httpx.AsyncClient``.

    The client opens both a sync and an async HTTP connection pool. Use it
    as a context manager (``with Durbl(...) as client:``) to make sure both
    pools are closed cleanly.

    Example:
        >>> client = Durbl(api_key="drbl_...")
        >>> client.memory.write(
        ...     entity="user/ahmed",
        ...     content="Likes Mediterranean cuisine",
        ...     type="preference",
        ...     importance=0.9,
        ... )
        >>> ctx = client.context.build(entity="user/ahmed", goal="suggest dinner")
        >>> print(ctx.assembled_context)
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        http_client: httpx.Client | None = None,
        async_http_client: httpx.AsyncClient | None = None,
    ) -> None:
        api_key = api_key or os.environ.get("DURBL_API_KEY")
        if not api_key:
            raise DurblConfigError(
                "api_key is required. Pass it directly or set DURBL_API_KEY."
            )
        base_url = (
            base_url
            or os.environ.get("DURBL_BASE_URL")
            or DEFAULT_BASE_URL
        )

        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._owns_sync = http_client is None
        self._owns_async = async_http_client is None

        headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json",
            "User-Agent": f"durbl-sdk-python/{__import__('durbl_sdk').__version__}",
        }

        self._client = http_client or httpx.Client(
            base_url=self._base_url,
            headers=headers,
            timeout=timeout,
        )
        self._async_client = async_http_client or httpx.AsyncClient(
            base_url=self._base_url,
            headers=headers,
            timeout=timeout,
        )

        # ── Resource namespaces ──────────────────────────────────
        self.memory = MemoryResource(self._client, self._async_client)
        self.events = EventsResource(self._client, self._async_client)
        self.state = StateResource(self._client, self._async_client)
        self.context = ContextResource(self._client, self._async_client)
        self.lifecycle = LifecycleResource(self._client, self._async_client)
        self.intelligence = IntelligenceResource(self._client, self._async_client)
        self.policies = PoliciesResource(self._client, self._async_client)

    # ── Lifecycle ────────────────────────────────────────────────

    @property
    def base_url(self) -> str:
        """The resolved base URL the client is talking to."""
        return self._base_url

    def close(self) -> None:
        """Close the synchronous HTTP connection pool (no-op if injected)."""
        if self._owns_sync:
            self._client.close()

    async def aclose(self) -> None:
        """Close the asynchronous HTTP connection pool (no-op if injected)."""
        if self._owns_async:
            await self._async_client.aclose()

    def __enter__(self) -> Durbl:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    async def __aenter__(self) -> Durbl:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()
