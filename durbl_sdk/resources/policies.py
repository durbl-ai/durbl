"""Policies resource — client.policies.*"""

from __future__ import annotations

from typing import Any

from durbl_sdk.resources.base import BaseResource


class PoliciesResource(BaseResource):
    """Policy operations — create, list, update, delete."""

    def create(
        self,
        type: str,
        rules: list[dict[str, Any]],
        target_entity: str | None = "*",
        target_memory_type: str | None = "*",
        description: str = "",
    ) -> dict[str, Any]:
        """Create a new policy."""
        return self._post("/v1/policies", json={
            "policy_type": type,
            "rules": rules,
            "target_entity": target_entity,
            "target_memory_type": target_memory_type,
            "description": description,
        })

    def list(self, type: str | None = None, active_only: bool = True) -> list[dict[str, Any]]:
        """List policies."""
        params: dict[str, Any] = {"active_only": active_only}
        if type:
            params["policy_type"] = type
        return self._get("/v1/policies", params=params)

    def update(self, policy_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update a policy."""
        return self._put(f"/v1/policies/{policy_id}", json=kwargs)

    def delete(self, policy_id: str) -> dict[str, Any]:
        """Delete a policy."""
        return self._delete(f"/v1/policies/{policy_id}")
