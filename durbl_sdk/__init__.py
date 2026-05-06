"""Durbl Python SDK — official client for the Durbl memory engine.

Quickstart::

    from durbl_sdk import Durbl

    client = Durbl()  # reads DURBL_API_KEY from env
    client.memory.write(
        entity="user/ahmed",
        content="Likes Mediterranean cuisine",
        type="preference",
        importance=0.9,
    )
    hits = client.memory.recall(entity="user/ahmed", query="food preferences")
    print(hits)

See https://docs.durbl.dev/sdk/python for the full reference.
"""

from durbl_sdk.client import Durbl
from durbl_sdk.exceptions import (
    DurblAPIError,
    DurblAuthError,
    DurblConfigError,
    DurblConnectionError,
    DurblError,
    DurblNotFoundError,
    DurblRateLimitError,
    DurblServerError,
)

__all__ = [
    "Durbl",
    "DurblError",
    "DurblConfigError",
    "DurblConnectionError",
    "DurblAPIError",
    "DurblAuthError",
    "DurblNotFoundError",
    "DurblRateLimitError",
    "DurblServerError",
]
__version__ = "0.2.4"
