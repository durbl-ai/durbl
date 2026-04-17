# Contributing to the Durbl Python SDK

Thanks for your interest in improving the SDK! This repo holds the **public Python client** for Durbl. The engine itself (server, storage, infrastructure) is closed-source.

## What lives here

- `durbl_sdk/` — the published `pip install durbl-sdk` package
- `examples/` — runnable usage snippets
- `README.md` — quick start

That's it. Anything related to running Durbl itself (server, deploys, schemas) lives in private repos.

## Where to start

The most useful contributions are:

- **Bug reports** — open an [issue](https://github.com/durbl-ai/durbl/issues) with a minimal reproducer.
- **Examples** — add a new file under `examples/` showing a real use case (RAG, agents, chat memory, etc.).
- **Type hints / docstrings** — improvements to clarity always welcome.
- **Async parity** — every sync method should have an `a*` async twin. PRs filling gaps are great.

## Local dev

```bash
git clone https://github.com/durbl-ai/durbl.git
cd durbl
pip install -e ".[dev]"
```

Run a quick smoke test against your own API key:

```bash
export DURBL_API_KEY="drbl_..."
python examples/quickstart.py
```

## Pull requests

- Keep PRs small and focused on one thing.
- Include an example or a docstring change so reviewers see the intent.
- Be kind in code review — same goes for you.

## What we won't merge

- Changes that leak server-side details (endpoints, schemas, internal headers).
- Anything that breaks the public surface without a deprecation path.
- Code that requires more than `httpx` and `pydantic` to run.

## Reporting security issues

**Do not** open a public issue for security findings. Email **security@durbl.dev** instead.

---

By contributing you agree that your changes are licensed under Apache-2.0.
