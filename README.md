# Durbl Python SDK

The official Python client for **[Durbl](https://durbl.dev)** — the data engine that remembers.

Durbl is a memory-native data engine for AI agents and applications. It gives your agents persistent context, adaptive memory, and stateful intelligence that grows with use.

```python
from durbl_sdk import Durbl

client = Durbl(api_key="drbl_...")

# Write a memory
client.memory.write(
    entity="user/ahmed",
    content="Prefers vegetarian food",
    type="preference",
)

# Recall it later, semantically
results = client.memory.recall(
    entity="user/ahmed",
    query="What food does the user like?",
)
for m in results:
    print(m["content"])
```

---

## Install

```bash
pip install durbl-sdk
```

Requires Python **3.10+**.

## Get an API key

1. Sign up at **[durbl.dev](https://durbl.dev)**
2. Open the [console](https://console.durbl.dev) → **Settings → API Keys**
3. Copy your `drbl_...` key

## Quick start

```python
from durbl_sdk import Durbl

client = Durbl(api_key="drbl_...")

# Episodic — something that happened
client.memory.write(
    entity="user/ahmed",
    content="Logged in from a new device in Doha",
    type="episodic",
)

# Semantic — a fact
client.memory.write(
    entity="user/ahmed",
    content="Works as a backend engineer",
    type="semantic",
)

# Preference — how they like things
client.memory.write(
    entity="user/ahmed",
    content="Prefers email over Slack",
    type="preference",
    importance=0.9,
)

# Build a context for your LLM
context = client.context.build(
    entity="user/ahmed",
    goal="Write a polite reminder about an unfinished task",
)
print(context["assembled_context"])
```

## Capabilities

| Resource | Use |
|---|---|
| `client.memory` | Write / read / list / recall memories |
| `client.context` | Build goal-aware context for LLMs |
| `client.events` | Stream raw events into the engine |
| `client.state` | Versioned entity state with history |
| `client.lifecycle` | Reinforce, decay, and forget memories |
| `client.intelligence` | Detect patterns and signals over time |
| `client.policies` | Per-entity retention and access rules |

## Async support

Every method has an async twin (`amethod`):

```python
import asyncio
from durbl_sdk import Durbl

async def main():
    client = Durbl(api_key="drbl_...")
    results = await client.memory.arecall(
        entity="user/ahmed",
        query="favorite food",
    )
    print(results)
    await client.aclose()

asyncio.run(main())
```

Or use it as an async context manager:

```python
async with Durbl(api_key="drbl_...") as client:
    await client.memory.awrite(entity="...", content="...")
```

## Examples

See the [`examples/`](./examples) folder for runnable snippets.

## Documentation

Full API reference and guides: **[durbl.dev/docs](https://durbl.dev/docs)**

## Support

- **Issues:** [github.com/durbl-ai/durbl/issues](https://github.com/durbl-ai/durbl/issues)
- **Website:** [durbl.dev](https://durbl.dev)

## License

Apache-2.0 — see [LICENSE](./LICENSE).
