"""Durbl Python SDK — the beautiful, intuitive client library.

Usage:
    from durbl import Durbl

    client = Durbl(api_key="drbl_...")
    client.memory.write(entity="user/ahmed", content="Likes coffee", type="preference")
"""

from durbl_sdk.client import Durbl

__all__ = ["Durbl"]
__version__ = "0.1.0"
