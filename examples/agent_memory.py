"""Give an LLM agent persistent memory across conversations.

Run:
    export DURBL_API_KEY="drbl_..."
    python examples/agent_memory.py
"""

from __future__ import annotations

import os

from durbl_sdk import Durbl


USER = "user/ahmed"


def remember(client: Durbl, content: str, kind: str = "episodic") -> None:
    client.memory.write(entity=USER, content=content, type=kind)


def build_prompt(client: Durbl, user_message: str) -> str:
    """Pull goal-aware context from Durbl and stitch it into a prompt."""
    ctx = client.context.build(entity=USER, goal=user_message)
    assembled = ctx.get("assembled_context", "")
    return (
        "You are a helpful assistant with persistent memory of this user.\n\n"
        f"--- relevant memories ---\n{assembled}\n\n"
        f"--- user message ---\n{user_message}\n"
    )


def main() -> None:
    client = Durbl(api_key=os.environ["DURBL_API_KEY"])

    # Day 1
    remember(client, "User said they live in Doha.", "semantic")
    remember(client, "User prefers concise answers.", "preference")
    remember(client, "User is learning Rust.", "semantic")

    # Day 2 — fresh session, no chat history. Durbl supplies the context.
    prompt = build_prompt(client, "Suggest a weekend project for me.")
    print(prompt)

    client.close()


if __name__ == "__main__":
    main()
