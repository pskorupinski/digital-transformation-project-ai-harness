# Decisions

> ADR-lite: one row per decision that someone could reasonably challenge.
> Claude: before changing anything covered by an `accepted` row, stop and propose a new row instead.

| Status | Meaning |
|---|---|
| `proposed` | Raised by a skill or a human, awaiting a human |
| `accepted` | In force — a constraint for every step |
| `superseded by D-nn` | Replaced; the row stays, so changing your mind is history, not deletion |

| ID | Status | Context | Decision | Alternatives considered | Revisit when | Refs |
|---|---|---|---|---|---|---|
| D-01 | accepted | Capabilities such as online payment may not exist yet, or today's provider may not fit a web solution; vendor selection must not block the first build | Integrations sit behind capability ports (named after the capability, not a vendor); v0 uses in-process fake adapters mirroring the generic contract shape, including async callbacks via our real inbound route; vendor choice is a separate decision before v1 | Pick vendors and open sandbox accounts first; skip integrations entirely | A vendor is chosen and sandbox credentials exist | 03-architecture § Capability register |
| D-02 | accepted | Small team must ship a first slice fast and keep it maintainable | React + Vite, FastAPI, SQLAlchemy 2.0 + Alembic, PostgreSQL, run via docker-compose | Full-stack JS (Next.js); BaaS (Supabase); no-code / hosted platform | Team skills change, or a hosted platform covers the scope (brief §4) | — |
| D-03 | accepted | Tests must be fast, isolated and close to production behaviour | Backend tests run against real Postgres, one rolled-back transaction per test | SQLite for speed; per-test database | Test suite exceeds ~1 min | — |
| D-04 | accepted | Acceptance criteria must stay readable for the business *and* checkable by CI | Specs are Gherkin `.feature` files; every scenario maps 1:1 to a hand-written test named after its ID; a traceability test fails when a `built` feature has a scenario without its test | Executable Gherkin (`pytest-bdd`, Cucumber.js); free-form tests | Specs are shared with non-engineers as living documentation, or drift appears despite the check | 04-specs |
| D-05 | accepted | AI features must be built fast, tested deterministically, and their output quality measured — not just demoed | One structured-generation port (`app/integrations/ai.py`): validated Pydantic output or `GenerationError`; Claude API structured outputs behind it; deterministic fake in tests; versioned prompts; golden-case evals with a pass-rate threshold run against the real model; human decision and audit record for every generation | Direct SDK calls in services; free-text output parsed ad hoc; an eval framework from day one | Eval sets outgrow hand-written checks, or a second model provider is needed | 03-architecture § AI design, `backend/evals/` |
