# Durbl Python SDK

The official Python client for the [Durbl](https://durbl.dev) memory engine —
a single backend that gives AI agents persistent, queryable memory across
runs, sessions, and users. One API for write, recall, state, context,
lifecycle, and signals — replacing a stack of vector DB + cache + queue +
state store + summarizer.

## Install

```bash
pip install durbl-sdk
```

## Quickstart

```python
from durbl_sdk import Durbl

client = Durbl(api_key="drbl_...")  # or set DURBL_API_KEY

# Write a memory
client.memory.write(
    entity="user/ahmed",
    content="Prefers TypeScript over JavaScript",
    type="preference",
    importance=0.8,
)

# Update entity state
client.state.update("user/ahmed", {"plan": "pro", "seats": 5})

# Recall by semantic search
hits = client.memory.recall(entity="user/ahmed", query="language preference", limit=3)
for m in hits:
    print(m["content"])

# Build a context window for an LLM call
ctx = client.context.build(entity="user/ahmed", goal="suggest a stack", max_memories=10)
print(ctx.assembled_context)
```

## Async usage

Every resource has an `a*` mirror that uses `httpx.AsyncClient`:

```python
import asyncio
from durbl_sdk import Durbl

async def main():
    async with Durbl(api_key="drbl_...") as client:
        await client.memory.awrite(entity="user/me", content="Likes coffee", type="preference")
        state = await client.state.aget("user/me")

asyncio.run(main())
```

## Resources

| Resource | Operations |
| --- | --- |
| `client.memory` | `write` · `get` · `update` · `delete` · `list` · `recall` |
| `client.state` | `get` · `update` · `history` |
| `client.context` | `build` · `recall` |
| `client.events` | `write` · `list` |
| `client.intelligence` | (analytics endpoints) |
| `client.lifecycle` | (memory lifecycle) |
| `client.policies` | (per-project policies) |

## Entity IDs

Entity IDs are free-form strings and may contain `/` (`user/ahmed`,
`team/acme/billing`). The SDK percent-encodes them automatically when
they appear in URL paths.

## Error handling

```python
from durbl_sdk.exceptions import DurblAPIError

try:
    client.memory.write(entity="user/me", content="...")
except DurblAPIError as e:
    print(e.status_code, e.message)
```

## Examples

The [`examples/`](https://github.com/durbl-ai/durbl/tree/main/examples)
directory has runnable sample apps:

- **personal_coach** — habit/goal tracker with semantic + preference memory
- **recipe_memory** — diet/preference-aware meal suggestions
- **support_agent** — per-customer briefs that demonstrate isolation

## Links

- Homepage: <https://durbl.dev>
- Docs: <https://docs.durbl.dev>
- Issues: <https://github.com/durbl-ai/durbl/issues>

## License

Apache-2.0
