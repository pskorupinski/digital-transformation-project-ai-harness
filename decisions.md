# Decisions

> ADR-lite: one row per decision that someone could reasonably challenge.
> **Status:** `proposed` (by a skill or a human, awaiting a human) · `accepted` · `superseded by D-nn`.
> Superseded rows stay — changing your mind is history, not deletion.
> Claude: before changing anything covered by an `accepted` row, stop and propose a new row instead.

| ID | Status | Context | Decision | Alternatives considered | Revisit when | Refs |
|---|---|---|---|---|---|---|
| D-01 | accepted | External systems (payments, CRM, …) shape the design, but real accounts can't be provisioned at project start | Integrations sit behind ports; v1 uses in-process fake adapters that mirror the real contract, including async callbacks via the real inbound route | Real sandbox accounts from day one; skip integrations entirely | First real transaction or first sandbox credentials available | 02-integrations |
| D-02 | accepted | Small team must ship a first slice fast and keep it maintainable | React + Vite · FastAPI · SQLAlchemy 2.0 + Alembic · PostgreSQL, run via docker-compose | Full-stack JS (Next.js); BaaS (Supabase); no-code / hosted platform | Team skills change, or a hosted platform covers the scope (see brief §4 differentiation) | — |
| D-03 | accepted | Acceptance criteria must be checkable, by humans and by CI | Every Gherkin scenario maps 1:1 to a test named after its ID; backend tests run against real Postgres, one rolled-back transaction per test | Free-form tests; SQLite for speed | Test suite exceeds ~1 min | 05-specs |
