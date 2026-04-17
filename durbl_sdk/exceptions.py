"""SDK exceptions."""

from __future__ import annotations


class DurblAPIError(Exception):
    """Error from the Durbl API."""

    def __init__(self, status_code: int, error: str, message: str) -> None:
        self.status_code = status_code
        self.error = error
        self.message = message
        super().__init__(f"[{status_code}] {error}: {message}")
