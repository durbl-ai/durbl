"""Public exception types raised by the SDK.

All errors inherit from :class:`DurblError` so callers can write a single
``except DurblError`` and catch every SDK-originated failure. Network and
parse failures wrap the underlying ``httpx`` exception via ``__cause__``.
"""

from __future__ import annotations

from typing import Any


class DurblError(Exception):
    """Base class for every error raised by the SDK."""


class DurblConfigError(DurblError):
    """Raised for invalid client configuration (missing key, bad URL, ...)."""


class DurblConnectionError(DurblError):
    """Raised when the SDK can't reach the API (DNS, refused, timeout)."""


class DurblAPIError(DurblError):
    """Raised when the API returns a 4xx/5xx response.

    Attributes:
        status_code: HTTP status code.
        error: Short error code returned by the server (e.g. ``"NOT_FOUND"``).
        message: Human-readable message from the server, or a fallback.
        body: The full decoded response body, if any.
    """

    def __init__(
        self,
        status_code: int,
        error: str,
        message: str,
        body: Any | None = None,
    ) -> None:
        self.status_code = status_code
        self.error = error
        self.message = message
        self.body = body
        super().__init__(f"[{status_code}] {error}: {message}")


class DurblAuthError(DurblAPIError):
    """401 / 403 — auth token missing, expired, or insufficient permissions."""


class DurblNotFoundError(DurblAPIError):
    """404 — the requested entity / memory / project doesn't exist."""


class DurblRateLimitError(DurblAPIError):
    """429 — caller exceeded the rate limit budget for the project or key."""


class DurblServerError(DurblAPIError):
    """5xx — server-side failure. Safe to retry with backoff for idempotent ops."""
