"""Lifecycle resource — client.lifecycle.*"""

from __future__ import annotations

from typing import Any

from durbl_sdk.resources.base import BaseResource


class LifecycleResource(BaseResource):
    """Lifecycle operations — reinforce, forget, archive."""

    def reinforce(self, memory_id: str | list[str], boost: float = 0.1) -> dict[str, Any]:
        """Reinforce memories."""
        ids = [memory_id] if isinstance(memory_id, str) else memory_id
        return self._post("/v1/lifecycle/reinforce", json={"memory_ids": ids, "boost": boost})

    def forget(
        self,
        memory_id: str | list[str] | None = None,
        entity: str | None = None,
        older_than: str | None = None,
    ) -> dict[str, Any]:
        """Forget memories."""
        body: dict[str, Any] = {}
        if memory_id:
            body["memory_ids"] = [memory_id] if isinstance(memory_id, str) else memory_id
        if entity:
            body["entity_id"] = entity
        return self._post("/v1/lifecycle/forget", json=body)

    def archive(self, memory_id: str | list[str]) -> dict[str, Any]:
        """Archive memories."""
        ids = [memory_id] if isinstance(memory_id, str) else memory_id
        return self._post("/v1/lifecycle/archive", json={"memory_ids": ids})
