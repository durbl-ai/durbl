"""Memory resource — client.memory.*"""

from __future__ import annotations

from typing import Any

from durbl_sdk.resources.base import BaseResource


class MemoryResource(BaseResource):
    """Memory operations.

    Usage:
        client.memory.write(entity="user/ahmed", content="Likes coffee", type="preference")
        client.memory.get(memory_id="...")
        client.memory.recall(entity="user/ahmed", query="What does Ahmed like?")
    """

    def write(
        self,
        entity: str,
        content: str,
        type: str = "semantic",
        importance: float = 0.5,
        confidence: float = 0.8,
        durability: float = 0.5,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Write a memory directly.

        Args:
            entity: Entity ID (e.g., "user/ahmed").
            content: Memory content in natural language.
            type: Memory type (episodic, semantic, preference, task, etc.).
            importance: Importance score (0-1).
            confidence: Confidence score (0-1).
            durability: Durability score (0-1).
            metadata: Optional key-value metadata.

        Returns:
            Created memory data.
        """
        return self._post("/v1/memory", json={
            "entity_id": entity,
            "content": content,
            "memory_type": type,
            "importance": importance,
            "confidence": confidence,
            "durability": durability,
            "metadata": metadata or {},
        })

    def get(self, memory_id: str) -> dict[str, Any]:
        """Get a specific memory by ID."""
        return self._get(f"/v1/memory/{memory_id}")

    def update(self, memory_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update a memory."""
        return self._put(f"/v1/memory/{memory_id}", json=kwargs)

    def delete(self, memory_id: str) -> dict[str, Any]:
        """Soft-delete a memory (move to forgotten state)."""
        return self._delete(f"/v1/memory/{memory_id}")

    def list(
        self,
        entity: str | None = None,
        type: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """List memories with filtering."""
        params: dict[str, Any] = {"limit": limit}
        if entity:
            params["entity_id"] = entity
        if type:
            params["memory_type"] = type
        return self._get("/v1/memory", params=params)

    def recall(
        self,
        entity: str,
        query: str,
        limit: int = 5,
        type: str | None = None,
    ) -> list[dict[str, Any]]:
        """Simple memory recall by semantic search."""
        body: dict[str, Any] = {
            "entity_id": entity,
            "query": query,
            "limit": limit,
        }
        if type:
            body["memory_type"] = type
        result = self._post("/v1/context/recall", json=body)
        return result.get("memories", [])

    # ── Async versions ───────────────────────────────────────

    async def awrite(self, entity: str, content: str, **kwargs: Any) -> dict[str, Any]:
        """Async version of write()."""
        return await self._apost("/v1/memory", json={
            "entity_id": entity,
            "content": content,
            **kwargs,
        })

    async def aget(self, memory_id: str) -> dict[str, Any]:
        """Async version of get()."""
        return await self._aget(f"/v1/memory/{memory_id}")

    async def arecall(self, entity: str, query: str, limit: int = 5) -> list[dict[str, Any]]:
        """Async version of recall()."""
        result = await self._apost("/v1/context/recall", json={
            "entity_id": entity,
            "query": query,
            "limit": limit,
        })
        return result.get("memories", [])
