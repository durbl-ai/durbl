"""Quickstart: write a memory and read it back.

Run:
    export DURBL_API_KEY="drbl_..."
    python examples/quickstart.py
"""

from __future__ import annotations

import os

from durbl_sdk import Durbl


def main() -> None:
    api_key = os.environ.get("DURBL_API_KEY")
    if not api_key:
        raise SystemExit("Set DURBL_API_KEY in your environment.")

    client = Durbl(api_key=api_key)

    # 1. Write a memory
    written = client.memory.write(
        entity="user/demo",
        content="Loves morning coffee — black, no sugar.",
        type="preference",
        importance=0.9,
    )
    print("wrote memory:", written.get("id"))

    # 2. Recall it back
    results = client.memory.recall(
        entity="user/demo",
        query="What does the user drink in the morning?",
        limit=3,
    )

    print("\nRecalled:")
    for m in results:
        print(f"  - {m.get('content')}")

    client.close()


if __name__ == "__main__":
    main()
