---
name: 05-build-slice
description: Build one specified feature as a thin vertical slice — plan, tests from Gherkin, data model, API, fake capabilities, minimal UI — with a human-approved plan and committed checkpoints.
argument-hint: "F-nn [optional instructions]"
disable-model-invocation: true
allowed-tools: Read Edit Write Bash(docker compose *) Bash(git status*) Bash(git diff*) Bash(git add *) Bash(git commit *)
---

# 05 · Build slice

Build the feature in the arguments as the **thinnest vertical slice** that makes its scenarios
pass. The human stays in control of the architecture: plan first, small steps, visible checks.
Arguments: $ARGUMENTS

## Inputs and preconditions

- `docs/04-specs/F-nn-*.feature` — must exist (else: run `/04-spec F-nn`)
- `docs/03-architecture.md` — entities, flows, endpoints, and the capability register
  (which capabilities are `fake` in v0, and their contract shape)
- `docs/02-features.md`, `decisions.md`, `CLAUDE.md` (guardrails, stack, commands)
- Containers running: `docker compose ps`; if not, `docker compose up --build -d`.

## Step 0 — Plan, then STOP

Present, in ≤ 25 lines:

| S-nn | Level | Test name | File |
|---|---|---|---|

- Files to create / change, per layer (models, schemas, services, api, integrations, UI)
- Expected migration: tables / columns / constraints
- Seed data needed to try the slice by hand (added to `app/seed.py`, idempotent), or "none"
- Deviations from `03-architecture.md` (each → a `proposed` row in `decisions.md`), or "none"
- Open questions, if any

End with: **"Reply `go`, or adjust the plan."** Do not write code before the human answers.

## Steps after `go` — state each step in one line before doing it

1. **Tests first (red).** `@api` scenarios → `backend/tests/test_f_nn_<slug>.py`, one test per
   scenario named `test_s01_<slug>`, docstring `F-nn/S-01 <title>`. Use the `client`/`db`
   fixtures; arrange data through the API where it exists, else through the `db` session.
   Run `docker compose exec backend pytest -q` — confirm they fail for the expected reason.
   Commit `F-nn: tests (red)`.
2. **Data.** SQLAlchemy 2.0 typed models per the data model; import them in
   `app/models/__init__.py`. Generate the migration
   (`docker compose exec backend alembic revision --autogenerate -m "F-nn <slug>"`), **show its
   operations and flag any drop, rename or type change**, then `alembic upgrade head`.
   Commit `F-nn: data model`.
3. **Capabilities** (only if the slice touches a register row with v0 = `fake`): port
   (`Protocol`) named after the capability, not a vendor; fake adapter mirroring the contract
   shape; factory by `INTEGRATIONS_MODE`. Async callbacks via a mock-provider route scheduling
   a `BackgroundTask` that calls our **real** inbound route over HTTP. Inbound handlers are
   idempotent.
4. **API.** Pydantic schemas, service functions (own the transaction), thin router registered
   in `app/api/__init__.py`. Run backend tests → **green**. Commit `F-nn: API (green)`.
5. **Thin UI.** Plain semantic HTML components for the `@ui` scenario's flow, calling
   `src/api/client.ts`; theme tokens only, no styling work. Test the `@ui` scenario with vitest
   + Testing Library (`it('F-nn/S-nn …')`, fetch stubbed). `npm run typecheck` and `npm test` green.
   Add the planned seed data to `app/seed.py` and run it. Commit `F-nn: UI`.
6. **Close.** Set the feature's `Status` to `built` in `docs/02-features.md`, then run all suites
   — `tests/test_traceability.py` now checks every scenario of this feature has its test.
   If the implementation changed anything in `03-architecture.md`, update it and say so.

## Rules

- **Never weaken a test to make it pass.** If a scenario looks wrong or ambiguous, stop and ask —
  the spec is the contract.
- If a step grows beyond the plan (new entity, new endpoint, new dependency), stop and re-plan.
- Only pre-approved dependencies (see `CLAUDE.md`); anything else → ask.
- Time-dependent rules read "now/today" from an injectable FastAPI dependency, so tests pin
  the clock instead of depending on the day they run.

## Final report (≤ 12 lines)

- Scenario → test → result table
- Commits made
- How to try it (URL + steps)
- Deviations and proposed decisions
- What the next slice would be
