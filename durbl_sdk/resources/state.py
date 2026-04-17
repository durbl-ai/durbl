"""State resource — client.state.*"""

from __future__ import annotations

from typing import Any

from durbl_sdk.resources.base import BaseResource


class StateResource(BaseResource):
    """Entity state operations."""

    def get(self, entity: str) -> dict[str, Any]:
        """Get current state of an entity."""
        return self._get(f"/v1/state/{entity}")

    def update(self, entity: str, state: dict[str, Any], reason: str = "sdk_update") -> dict[str, Any]:
        """Update entity state."""
        return self._put(f"/v1/state/{entity}", json={"state": state, "reason": reason})

    def history(self, entity: str, limit: int = 50) -> list[dict[str, Any]]:
        """Get state version history."""
        return self._get(f"/v1/state/{entity}/history", params={"limit": limit})

    async def aget(self, entity: str) -> dict[str, Any]:
        """Async version of get()."""
        return await self._aget(f"/v1/state/{entity}")

    async def aupdate(self, entity: str, state: dict[str, Any], reason: str = "sdk_update") -> dict[str, Any]:
        """Async version of update()."""
        return await self._aput(f"/v1/state/{entity}", json={"state": state, "reason": reason})
