---
name: 04-architecture
description: Derive the high-level architecture for the confirmed scope — context, containers, data model, key flows, API surface and scalability notes — as Mermaid in docs/04-architecture.md. Use after scope in docs/03-features.md is confirmed.
argument-hint: "[scope, default v1] [optional instructions]"
disable-model-invocation: true
allowed-tools: Read Edit Write
---

# 04 · Architecture

Write `docs/04-architecture.md` for the confirmed scope. Design something that can grow,
**without building for growth on day one**. You propose; the human reviews.
Arguments (may be empty — default scope `v1`): $ARGUMENTS

## Inputs

- `docs/03-features.md` — features in scope = scope value **without `?`** matching the requested
  scope. If in-scope features still carry `?`, stop and list them: the human must decide first.
- `docs/01-brief.md` — especially §7 systems, §8 scale, §9 constraints
- `docs/02-integrations.md` — every row appears in the context diagram with its v1 mode
- `decisions.md` — accepted decisions are constraints (stack = D-02, integrations = D-01)
- `docs/04-architecture.md` — if it has content, this is a **re-run**: update incrementally and
  never drop entities or endpoints used by features with status `built`

## Design rules

- **Minimal model.** Only entities the in-scope features need; ≤ 8 entities. Every entity and
  endpoint lists the `F-nn` that need it — anything without a feature doesn't belong.
- **Durable defaults** (state them, don't debate them): UUID primary keys · timestamps in UTC ·
  money as integer minor units + currency · explicit status fields with listed values ·
  values that must not change retroactively are **copied at transaction time** (snapshot),
  not referenced · store the external IDs the integration contracts require.
- **Integrations** follow D-01: show the port and the fake adapter; async callbacks arrive at
  our real inbound route.
- **Real trade-offs become decisions.** For a genuine fork (e.g. accounts vs guest access,
  sync vs async), pick one, append a `proposed` row to `decisions.md`, and reference it.
  Don't create decisions for obvious choices.
- Missing facts → append `A-nn` to brief §10 (`Raised by: 04-architecture`) and continue.

## Mermaid rules (must render in the VS Code preview)

- Flowchart labels with spaces or punctuation in quotes: `api["Backend API"]`; never use a bare
  lowercase `end` as a node ID.
- `erDiagram`: entity names in PascalCase, attributes as `type name PK|FK|UK "comment"`,
  cardinalities like `Parent ||--o{ Child : has`.
- `sequenceDiagram`: alias long names (`participant API as Backend API`); mark fakes `(fake in v1)`.
- ≤ 15 nodes per diagram. Prefer two clear diagrams over one dense one.

## Output — `docs/04-architecture.md`

Keep the header blockquote, then exactly these sections:

1. `## Scope` — the in-scope `F-nn` list (one line each) and what is explicitly **not** covered.
2. `## Context` — C4 level 1 `flowchart LR`: actors → system → external systems (`I-nn`, mode).
3. `## Containers` — C4 level 2 `flowchart LR`: SPA (React) → API (FastAPI) → PostgreSQL,
   integration ports/fake adapters, mock-provider routes; protocols on the arrows.
4. `## Data model` — `erDiagram`, then a table
   `| Entity | Purpose | Status values | Features |`.
5. `## Key flows` — one `sequenceDiagram` per in-scope feature that crosses a boundary (external
   system, async callback, multi-step state change); at most 3. Skip the obvious CRUD.
6. `## API surface` — `| Method | Path | Purpose | Features | Access |` (paths under `/api`).
7. `## Scalability & quality` —
   `| Concern | v1 approach | Changes when (trigger, cite §8) | Then |` covering load, data
   volume, concurrency/consistency, security & access, privacy (cite §9), observability.
   The "Then" column is the growth path we are deliberately **not** building now.
8. `## Open points` — assumptions added and decisions proposed, by ID.

## Chat summary (≤ 10 lines)

Entities and flows produced · proposed decisions (by ID, one line each) · assumptions added ·
the 2–3 things most worth the human's review · **suggested first slice**: the in-scope feature
that exercises the most of the architecture (data model, API, UI, ideally one integration) with
the least scope, and why. Then stop — do not write specs or code.
