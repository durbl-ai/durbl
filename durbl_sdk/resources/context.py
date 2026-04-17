"""Context resource — client.context.*"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from durbl_sdk.resources.base import BaseResource


class ContextResult:
    """Result of a context build operation.

    Provides easy access to the assembled context and metadata.
    """

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    @property
    def assembled_context(self) -> str:
        """The final text context for LLM consumption."""
        return self._data.get("assembled_context", "")

    @property
    def memory_count(self) -> int:
        """Number of memories used in context."""
        return self._data.get("memory_count", 0)

    @property
    def has_state(self) -> bool:
        """Whether entity state was included."""
        return self._data.get("has_state", False)

    @property
    def latency_ms(self) -> float:
        """Context assembly latency in milliseconds."""
        return self._data.get("latency_ms", 0.0)

    @property
    def id(self) -> str:
        """Context frame ID."""
        return self._data.get("id", "")

    def __str__(self) -> str:
        return self.assembled_context

    def __repr__(self) -> str:
        return f"ContextResult(memories={self.memory_count}, latency={self.latency_ms}ms)"


class ContextResource(BaseResource):
    """Context operations — the core feature."""

    def build(
        self,
        entity: str,
        goal: str,
        temporal_horizon: str = "all",
        max_memories: int = 20,
        include_state: bool = True,
    ) -> ContextResult:
        """Build a context frame for LLM consumption.

        Args:
            entity: Entity ID.
            goal: What the context is being built for.
            temporal_horizon: Time filter ("recent", "today", "this_week", "all").
            max_memories: Maximum memories to include.
            include_state: Whether to include entity state.

        Returns:
            ContextResult with assembled context and metadata.
        """
        data = self._post("/v1/context/build", json={
            "entity_id": entity,
            "goal": goal,
            "temporal_horizon": temporal_horizon,
            "max_memories": max_memories,
            "include_state": include_state,
        })
        return ContextResult(data)

    async def abuild(self, entity: str, goal: str, **kwargs: Any) -> ContextResult:
        """Async version of build()."""
        data = await self._apost("/v1/context/build", json={
            "entity_id": entity,
            "goal": goal,
            **kwargs,
        })
        return ContextResult(data)
