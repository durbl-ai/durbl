"""State resource — client.state.*"""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from durbl_sdk.exceptions import DurblNotFoundError
from durbl_sdk.resources.base import BaseResource


def _enc(entity: str) -> str:
    """Percent-encode an entity ID for use as a single path segment.

    Entity IDs are domain identifiers like ``user/ahmed`` or ``coach/me``
    that may legitimately contain ``/``. The server route is a single
    path segment (`/v1/state/:entity_id`), so we percent-encode the slash
    (and any other reserved chars) here. Axum's Path extractor decodes
    the segment back to the original string.
    """
    return quote(entity, safe="")


class StateResource(BaseResource):
    """Entity state operations.

    Entity IDs may contain ``/`` (e.g. ``user/ahmed``); the SDK
    percent-encodes them so the server's single-segment route still matches.
    """

    def get(self, entity: str) -> dict[str, Any]:
        """Get current state of an entity.

        Returns the state map directly (the server wraps it in `{"data": ...}`;
        we unwrap so callers can do ``client.state.get(entity).get("mood")``).
        Returns ``{}`` if no state has been written yet (404 only).

        Auth, rate-limit, server, and network errors are NOT swallowed — they
        propagate as the matching :class:`DurblError` subclass so callers can
        distinguish "no state yet" from "the request actually failed".
        """
        try:
            raw = self._get(f"/v1/state/{_enc(entity)}")
        except DurblNotFoundError:
            return {}
        return raw.get("data", {}) or {}

    def update(self, entity: str, state: dict[str, Any], reason: str = "sdk_update") -> dict[str, Any]:
        """Update entity state.

        The server's PUT /v1/state/:entity handler consumes the entire request
        body as the new state value (the `reason` is recorded server-side as a
        fixed string). We send the raw state map so the dashboard reflects the
        keys the caller actually passed in.
        """
        _ = reason  # kept in the signature for forward compatibility
        return self._put(f"/v1/state/{_enc(entity)}", json=state)

    def history(self, entity: str, limit: int = 50) -> list[dict[str, Any]]:
        """Get state version history."""
        return self._get(f"/v1/state/{_enc(entity)}/history", params={"limit": limit})

    async def aget(self, entity: str) -> dict[str, Any]:
        """Async version of get(). Same error semantics: only 404 → ``{}``."""
        try:
            raw = await self._aget(f"/v1/state/{_enc(entity)}")
        except DurblNotFoundError:
            return {}
        return raw.get("data", {}) or {}

    async def aupdate(self, entity: str, state: dict[str, Any], reason: str = "sdk_update") -> dict[str, Any]:
        """Async version of update()."""
        _ = reason
        return await self._aput(f"/v1/state/{_enc(entity)}", json=state)
