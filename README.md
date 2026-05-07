# Durbl Python SDK

**The Memory Reasoning Layer for AI Agents.**
*Memory that reasons. Not just stores.*

[Documentation](https://durbl.dev/docs) ·
[Why Durbl?](https://durbl.dev/why-durbl) ·
[Architecture](https://durbl.dev/architecture) ·
[Benchmarks](https://durbl.dev/benchmarks) ·
[Pricing](https://durbl.dev/pricing)

---

## Why Durbl

Every AI agent eventually faces three problems:

1. **Memory contamination** — vector search returns memories that look similar but belong to a different conversation. Your agent answers "what's my favorite color?" with a memory from an unrelated thread. Topic bleed kills response quality.
2. **Memory contradictions** — user said "I'm vegan" three months ago and "I had steak last night" yesterday. Existing systems return both and let the LLM guess. There is no conflict-resolution layer.
3. **Multi-agent chaos** — five agents share a workspace, each with its own memory. Architect picks Postgres, backend picks Mongo. No consensus, no handoff, no institutional memory.

Durbl is the first product to solve all three.

## How Durbl is different

| Capability | pgvector | Mem0 | Zep | Letta | **Durbl** |
|---|---|---|---|---|---|
| Vector storage | ✓ | ✓ | ✓ | ✓ | ✓ |
| Semantic recall | ✓ | ✓ | ✓ | ✓ | ✓ |
| Conflict detection | — | — | partial | — | **✓** |
| Conflict resolution | — | — | — | — | **✓** |
| Explainable recall | — | — | — | — | **✓** |
| Multi-agent coordination | — | — | — | partial | **✓ (roadmap)** |
| Memory provenance | — | — | — | — | **✓** |
| BYOD / customer-owned data | self-host | — | — | self-host | **✓** |

(Honest table — verified November 2026. We update it whenever a competitor ships a meaningful new capability.)

## Install

```bash
pip install durbl-sdk
```

## Quickstart

```python
from durbl_sdk import Durbl

client = Durbl(api_key="drbl_...")  # or set DURBL_API_KEY

# 1. Write a memory
client.memory.write(
    entity="user/ahmed",
    content="Prefers TypeScript over JavaScript",
    type="preference",
    importance=0.8,
)

# 2. Conflict-aware recall (the differentiator)
result = client.memory.recall(
    entity="user/ahmed",
    query="user's language preference",
    # Roadmap parameters — landing in v0.3:
    # resolve_conflicts=True,
    # explain=True,
    limit=3,
)
for m in result:
    print(m["content"])

# 3. Build a context frame ready for any LLM
ctx = client.context.build(
    entity="user/ahmed",
    goal="suggest a stack",
    max_memories=10,
)
print(ctx.assembled_context)
```

## Async usage

Every sync method has an async mirror — `awrite`, `aget`, `arecall`, `abuild`, etc:

```python
import asyncio
from durbl_sdk import Durbl

async def main():
    async with Durbl(api_key="drbl_...") as client:
        result = await client.memory.arecall(entity="user/ahmed", query="preferences")
        print(result)

asyncio.run(main())
```

## Three deployment modes

| Mode | Where memory lives | Best for |
|---|---|---|
| **Durbl Cloud** | Our infra (EU residency by default) | Prototypes, startups, friction-free start |
| **Bring-Your-Own-Database** | Your Postgres/Mongo/Pinecone | Compliance-sensitive teams, enterprise |
| **Self-Hosted** | Your Kubernetes/Docker, air-gappable | Government, defence, banking |

The same SDK and the same HTTP surface across all three. Switch deployment without rewriting agent code. See [/architecture](https://durbl.dev/architecture).

## Three memory modes

Durbl is the first memory product to treat single-agent and multi-agent as first-class equals. Pick how memory behaves at project init:

```python
from durbl_sdk import Durbl, MemoryMode  # MemoryMode landing in v0.3

# Single-agent or privacy-sensitive — each agent has private memory
durbl = Durbl(api_key="...", mode=MemoryMode.ISOLATED)

# Collaborative agent team — all agents share one pool
durbl = Durbl(api_key="...", mode=MemoryMode.SHARED)

# Production multi-agent — per-namespace ACLs, time-bounded sharing
durbl = Durbl(api_key="...", mode=MemoryMode.HYBRID)
```

## Status

- [x] **Layer 1 — Precision Recall** (shipped today)
  Hybrid retrieval (vector + temporal + relational + confidence). Explainable.
- [ ] **Layer 2 — Multi-Agent Coordination** (active iteration)
  Memory modes shipping in v0.3 of the SDK. Handoffs + consensus follow.
- [ ] **Layer 3 — Institutional Memory** (Year 3)
  Org-wide knowledge graphs, provenance across agents, governance primitives.

## Error handling

```python
from durbl_sdk import (
    DurblError,
    DurblAuthError,
    DurblNotFoundError,
    DurblRateLimitError,
    DurblServerError,
    DurblConnectionError,
    DurblConfigError,
)

try:
    result = client.memory.recall(entity="user/ahmed", query="preferences")
except DurblAuthError:
    # Bad API key or insufficient scope
    ...
except DurblRateLimitError as e:
    # 429 — back off and retry
    ...
except DurblNotFoundError:
    # 404 — entity has no memories yet
    ...
```

## Resources

| | |
|---|---|
| Why Durbl | https://durbl.dev/why-durbl |
| Documentation | https://durbl.dev/docs |
| Architecture | https://durbl.dev/architecture |
| Benchmarks | https://durbl.dev/benchmarks |
| Pricing | https://durbl.dev/pricing |
| Status | https://durbl.dev/status |
| Changelog | [CHANGELOG.md](./CHANGELOG.md) |
| Security policy | [SECURITY.md](./SECURITY.md) |
| Contributing | [CONTRIBUTING.md](./CONTRIBUTING.md) |

## Pricing

Free Hobby tier (10K memories, 1K calls/day) for ever. Paid tiers from $29/month with conflict resolution included. See [/pricing](https://durbl.dev/pricing).

## License

Apache 2.0 for this SDK. Engine is source-available under a non-compete licence — commercial self-host requires Enterprise.
