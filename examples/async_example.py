"""Async usage with the Durbl SDK.

Run:
    export DURBL_API_KEY="drbl_..."
    python examples/async_example.py
"""

from __future__ import annotations

import asyncio
import os

from durbl_sdk import Durbl


async def main() -> None:
    async with Durbl(api_key=os.environ["DURBL_API_KEY"]) as client:
        await client.memory.awrite(
            entity="user/demo",
            content="Visited the SDK examples folder.",
            type="episodic",
        )

        results = await client.memory.arecall(
            entity="user/demo",
            query="What did the user do recently?",
            limit=3,
        )
        for m in results:
            print("-", m.get("content"))


if __name__ == "__main__":
    asyncio.run(main())
