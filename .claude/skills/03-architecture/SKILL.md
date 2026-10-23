---
name: 03-architecture
description: Derive the high-level architecture for the confirmed scope — context, containers, capability/integration register, data model, key flows, API surface and scalability notes — as Mermaid in docs/03-architecture.md. Use after scope in docs/02-features.md is confirmed.
argument-hint: "[scope, default v0] [optional instructions]"
disable-model-invocation: true
allowed-tools: Read Edit Write
---

# 03 · Architecture

Write `docs/03-architecture.md` for the confirmed scope. Design something that can grow,
**without building for growth on day one**. You propose; the human reviews.
Arguments (may be empty — default scope `v0`): $ARGUMENTS

## Inputs

- `docs/02-features.md` — features in scope = scope value **without `?`** matching the requested
  scope. If in-scope features still carry `?`, stop and list them: the human must decide first.
- `docs/01-brief.md` — especially §8 existing systems, §9 scale, §10 constraints
- `decisions.md` — accepted decisions are constraints (stack = D-02, integrations = D-01)
- `docs/03-architecture.md` — if it has content, this is a **re-run**: update incrementally and
  never drop entities, endpoints or register rows used by features with status `built`

## Capability register (D-01)

Derive it yourself — the human only gave business answers in §8. One row per external
capability that in-scope features need (their `Capability` column) or that §8 says must keep
working.

| Column | Values |
|---|---|
| Fit | Does today's system (§8) serve the web solution? `yes`, `partial`, `no`, `unknown` |
| Proposal | `keep & integrate`, `replace`, `add new`, `keep manual`, `out of scope` |
| v0 | How the first build provides it: `fake`, `real`, `manual`, `none` |
| v1 | What the first customer release needs: `real`, `manual`, `none` |
| Contract shape | The *generic* pattern of the capability, e.g. "hosted checkout + async confirmation callback" |

Rules:

- `replace` / `add new` → append a `proposed` row to `decisions.md` with **selection criteria**
  (cost, fit with the business's bank or tools, local payment methods, effort). Don't pick a
  vendor unless the brief names one.
- Anything specific to a vendor's API is knowledge you may have wrong or outdated: record it as
  an `A-nn` "to verify" assumption, never as fact.
- `out of scope` for a capability an in-scope feature needs → don't drop the feature; ask the
  human in the chat summary.

## Design rules

- **Minimal model.** Only entities the in-scope features need; ≤ 8 entities. Every entity and
  endpoint lists the `F-nn` that need it — anything without a feature doesn't belong.
- **Durable defaults** — state them, don't debate them:
  - UUID primary keys; timestamps in UTC
  - money as integer minor units + currency
  - explicit status fields with their listed values
  - values that must not change retroactively are **copied at transaction time** (snapshot),
    not referenced
  - store the external IDs the contract shape requires
- **Real trade-offs become decisions.** For a genuine fork (e.g. accounts vs guest access,
  sync vs async), pick one, append a `proposed` row to `decisions.md`, and reference it.
  Don't create decisions for obvious choices.
- Missing facts → append `A-nn` to brief §11 (`Raised by: 03-architecture`) and continue.

## Mermaid rules (must render in the VS Code preview)

- Flowchart labels with spaces or punctuation in quotes: `api["Backend API"]`; never use a bare
  lowercase `end` as a node ID.
- `erDiagram`: entity names in PascalCase, attributes as `type name PK|FK|UK "comment"`,
  cardinalities like `Parent ||--o{ Child : has`.
- `sequenceDiagram`: alias long names (`participant API as Backend API`); mark fakes `(fake in v0)`.
- ≤ 15 nodes per diagram. Prefer two clear diagrams over one dense one.

## Output — `docs/03-architecture.md`

Keep the header blockquote, then exactly these sections. Leave a blank line before every table,
list and code block so Markdown renders them.

1. `## Scope` — the in-scope `F-nn` list (one line each) and what is explicitly **not** covered.
2. `## Context` — C4 level 1 `flowchart LR`: actors → system → external capabilities
   (`I-nn`, v0 mode).
3. `## Capability register` —
   `| ID | Capability | Needed by | As-is (§8) | Fit | Proposal | v0 | v1 | Contract shape | Refs |`
4. `## Containers` — C4 level 2 `flowchart LR`: SPA (React) → API (FastAPI) → PostgreSQL,
   capability ports with fake adapters, mock-provider routes; protocols on the arrows.
5. `## Data model` — `erDiagram`, then `| Entity | Purpose | Status values | Features |`.
6. `## Key flows` — one `sequenceDiagram` per in-scope feature that crosses a boundary (external
   capability, async callback, multi-step state change); at most 3. Skip the obvious CRUD.
7. `## API surface` — `| Method | Path | Purpose | Features | Access |` (paths under `/api`).
8. `## Scalability & quality` —
   `| Concern | v0 approach | Changes when (trigger, cite §9) | Then |` covering load, data
   volume, concurrency/consistency, security & access, privacy (cite §10), observability.
   The "Then" column is the growth path we are deliberately **not** building now.
9. `## Open points` — assumptions added and decisions proposed, by ID.

## Chat summary (≤ 10 lines)

- Entities, capabilities and flows produced
- Proposed decisions (by ID, one line each) and assumptions added
- The 2–3 things most worth the human's review
- **Suggested first slice:** the in-scope feature that exercises the most of the architecture
  (data model, API, UI, ideally one capability) with the least scope, and why
- The commit the human makes once the review is done (don't run it — committing is their
  approval):

  ```bash
  git add docs/ decisions.md && git commit -m "Human: accept architecture and decisions"
  ```

Then stop — do not write specs or code.
