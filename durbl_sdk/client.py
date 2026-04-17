"""Durbl Python SDK — clean, beautiful client library.

The SDK provides a simple, intuitive interface to the Durbl API.
"""

from __future__ import annotations

from typing import Any

import httpx

from durbl_sdk.resources.memory import MemoryResource
from durbl_sdk.resources.events import EventsResource
from durbl_sdk.resources.state import StateResource
from durbl_sdk.resources.context import ContextResource
from durbl_sdk.resources.lifecycle import LifecycleResource
from durbl_sdk.resources.intelligence import IntelligenceResource
from durbl_sdk.resources.policies import PoliciesResource


class Durbl:
    """The Durbl Python SDK client.

    A beautiful, simple interface to the Durbl memory engine.

    Usage:
        ```python
        from durbl import Durbl

        client = Durbl(api_key="drbl_...")

        # Write a memory
        client.memory.write(
            entity="user/ahmed",
            content="Prefers vegetarian food",
            type="preference",
            importance=0.9,
        )

        # Build context for LLM
        context = client.context.build(
            entity="user/ahmed",
            goal="User wants to order food",
        )
        print(context.assembled_context)
        ```

    Args:
        api_key: Your Durbl API key (starts with 'drbl_').
        base_url: API base URL (defaults to https://durbl.dev/api).
        timeout: Request timeout in seconds.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://durbl.dev/api",
        timeout: float = 30.0,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")

        self._client = httpx.Client(
            base_url=self._base_url,
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

        self._async_client = httpx.AsyncClient(
            base_url=self._base_url,
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

        # ── Resource namespaces ──────────────────────────────
        self.memory = MemoryResource(self._client, self._async_client)
        self.events = EventsResource(self._client, self._async_client)
        self.state = StateResource(self._client, self._async_client)
        self.context = ContextResource(self._client, self._async_client)
        self.lifecycle = LifecycleResource(self._client, self._async_client)
        self.intelligence = IntelligenceResource(self._client, self._async_client)
        self.policies = PoliciesResource(self._client, self._async_client)

    def close(self) -> None:
        """Close the HTTP clients."""
        self._client.close()

    async def aclose(self) -> None:
        """Close the async HTTP client."""
        await self._async_client.aclose()

    def __enter__(self) -> Durbl:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    async def __aenter__(self) -> Durbl:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()
