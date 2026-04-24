"""Context resource — ``client.context.*``.

The context endpoint is the primary feature of Durbl: pull the right
memories + state for an entity given a goal, then return a single string
ready to drop into an LLM prompt.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from durbl_sdk.resources.base import BaseResource


def _enc(entity: str) -> str:
    return quote(entity, safe="")


class ContextResult:
    """Result of a context build operation.

    Wraps the raw server response and exposes the common fields as
    properties so callers don't have to hunt through the dict.
    """

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    @property
    def assembled_context(self) -> str:
        """The final text context for LLM consumption."""
        return self._data.get("assembled_context", "")

    @property
    def memory_count(self) -> int:
        """Number of memories included in the assembled context."""
        return self._data.get("memory_count", 0)

    @property
    def has_state(self) -> bool:
        """Whether the entity's state was included."""
        return self._data.get("has_state", False)

    @property
    def latency_ms(self) -> float:
        """Server-side context assembly latency, in milliseconds."""
        return self._data.get("latency_ms", 0.0)

    @property
    def id(self) -> str:
        """Server-issued context frame ID."""
        return self._data.get("id", "")

    @property
    def raw(self) -> dict[str, Any]:
        """The raw response dict, in case the caller wants extra fields."""
        return self._data

    def __str__(self) -> str:
        return self.assembled_context

    def __repr__(self) -> str:
        return f"ContextResult(memories={self.memory_count}, latency={self.latency_ms}ms)"


class ContextResource(BaseResource):
    """Context build / recall operations."""

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
            entity: Entity ID. May contain ``/``.
            goal: What the context is being built for (e.g. "draft a reply").
            temporal_horizon: One of ``"recent"``, ``"today"``, ``"this_week"``, ``"all"``.
            max_memories: Maximum memories to include in the assembled text.
            include_state: Whether to inline the entity's current state.

        Returns:
            :class:`ContextResult` with the assembled text plus metadata.
        """
        data = self._post(
            "/v1/context/build",
            json={
                "entity_id": entity,
                "goal": goal,
                "temporal_horizon": temporal_horizon,
                "max_memories": max_memories,
                "include_state": include_state,
            },
        )
        return ContextResult(data)

    async def abuild(
        self,
        entity: str,
        goal: str,
        temporal_horizon: str = "all",
        max_memories: int = 20,
        include_state: bool = True,
    ) -> ContextResult:
        """Async version of :meth:`build`."""
        data = await self._apost(
            "/v1/context/build",
            json={
                "entity_id": entity,
                "goal": goal,
                "temporal_horizon": temporal_horizon,
                "max_memories": max_memories,
                "include_state": include_state,
            },
        )
        return ContextResult(data)
