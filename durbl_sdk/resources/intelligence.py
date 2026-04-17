"""Intelligence resource — client.intelligence.*"""

from __future__ import annotations

from typing import Any

from durbl_sdk.resources.base import BaseResource


class IntelligenceResource(BaseResource):
    """Intelligence operations — signals, patterns, health."""

    def signals(self) -> list[dict[str, Any]]:
        """Get latest intelligence signals."""
        result = self._get("/v1/intelligence/signals")
        return result.get("signals", [])

    def patterns(self) -> list[dict[str, Any]]:
        """Get discovered patterns."""
        result = self._get("/v1/intelligence/patterns")
        return result.get("patterns", [])

    def health(self, entity: str) -> dict[str, Any]:
        """Get memory health for an entity."""
        return self._get(f"/v1/intelligence/health/{entity}")
