# Changelog

All notable changes to `durbl-sdk` follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] — 2026-04-24

### Changed
- **Default `base_url` now points directly at the production Cloud Run
  endpoint** (`https://durbl-server-302549088008.me-central1.run.app`).
  The previous default `https://api.durbl.dev` is being remapped via a
  Vercel edge proxy; once DNS propagates, both URLs will work
  interchangeably and the default may swap back to `api.durbl.dev` in a
  future release. Override via constructor or `DURBL_BASE_URL`.

## [0.2.0] — 2026-04-18

### Added
- **Typed exception hierarchy**: `DurblError` is the new base, with
  specific subclasses `DurblConfigError`, `DurblConnectionError`,
  `DurblAuthError` (401/403), `DurblNotFoundError` (404),
  `DurblRateLimitError` (429), and `DurblServerError` (5xx).
- `Durbl()` reads `DURBL_API_KEY` and `DURBL_BASE_URL` from the
  environment when arguments are omitted.
- `Durbl(http_client=..., async_http_client=...)` lets callers inject
  pre-built `httpx` clients (useful for tests and custom transports).
- `Durbl.base_url` property exposing the resolved base URL.
- `Durbl` now sends a `User-Agent: durbl-sdk-python/<version>` header.
- `ContextResult.raw` exposes the full server response dict for
  callers who need extra fields.
- `py.typed` marker so downstream type-checkers (mypy, pyright) consume
  the SDK's annotations.

### Changed
- **Default `base_url` is now `https://api.durbl.dev`** (was
  `http://localhost:8000`). Override via constructor or
  `DURBL_BASE_URL` for local development.
- Network failures (DNS, refused, timeout) raise `DurblConnectionError`
  instead of leaking raw `httpx` exceptions.
- `BaseResource._handle_response` returns the raw decoded JSON (which
  may be a list) instead of always assuming a dict.
- 204 / empty responses return `{}` instead of raising on JSON parse.
- `ContextResource.abuild` now mirrors `build`'s explicit signature
  (was `**kwargs`).
- Dropped runtime dependency on `pydantic` — the SDK is now `httpx`-only.

### Fixed
- `0.1.x` regression follow-up: `client.state.get/update/history` now
  percent-encode the entity ID, so multi-segment IDs like `user/ahmed`
  round-trip correctly through the single-segment server route (S-3).
- `client.state.update` sends the raw state dict (not `{state, reason}`)
  so the server's PUT handler stores what the caller passed.
- `client.state.get` unwraps the server's `{"data": ...}` envelope.
- `client.memory.write` field name (`type` not `memory_type`) matches
  the server contract.
- `client.memory.recall` posts to `/v1/memory/recall` (was
  `/v1/context/recall`).

## [0.1.0] — 2026-03

Initial release.
