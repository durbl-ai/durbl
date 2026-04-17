"""Events resource — client.events.*"""

from __future__ import annotations

from typing import Any

from durbl_sdk.resources.base import BaseResource


class EventsResource(BaseResource):
    """Event operations — write cognitive events to trigger the pipeline."""

    def write(
        self,
        entity: str,
        type: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Write a cognitive event.

        Args:
            entity: Entity ID.
            type: Event type (message, tool_call, agent_output, etc.).
            payload: Event payload data.

        Returns:
            Created event data.
        """
        return self._post("/v1/events", json={
            "entity_id": entity,
            "event_type": type,
            "payload": payload or {},
        })

    async def awrite(self, entity: str, type: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Async version of write()."""
        return await self._apost("/v1/events", json={
            "entity_id": entity,
            "event_type": type,
            "payload": payload or {},
        })
