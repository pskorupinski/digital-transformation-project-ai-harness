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
- **Reviewed docs committed:** `git status --porcelain -- docs decisions.md` must be empty, so
  your checkpoint commits contain code only. If it isn't, stop before planning, list the files
  and ask the human to commit them (suggest `git add docs/ decisions.md && git commit -m
  "docs(<area>): …"`). Never commit the human's docs yourself.

## Step 0 — Plan, then STOP

Present, in ≤ 25 lines:

| S-nn | Level | Test name | File |
|---|---|---|---|

- Files to create / change, per layer (models, schemas, services, api, integrations, UI)
- Expected migration: tables / columns / constraints
- AI slices: output schema, prompt file, fallback on `GenerationError`, audit fields, eval cases
- Seed data needed to try the slice by hand (added to `app/seed.py`, idempotent), or "none"
- Deviations from `03-architecture.md` (each → a `proposed` row in `decisions.md`), or "none"
- Deferred: fields or tables the architecture has for `Out of scope` features, or "none"
- Brand (first slice with UI, while `src/brand.ts` still says `'Client'`): name and the 4 colour
  tokens from brief §5, as hex, each text/background pair with its contrast ratio — or "already applied"
- Open questions, if any

End with: **"Reply `go`, or adjust the plan."** Do not write code before the human answers.

## Steps after `go` — state each step in one line before doing it

1. **Tests first (red).** `@api` scenarios → `backend/tests/test_f_nn_<slug>.py`, one test per
   scenario named `test_s01_<slug>`, docstring `F-nn/S-01 <title>`. Use the `client`/`db`
   fixtures; arrange data through the API where it exists, else through the `db` session.
   Run `docker compose exec backend pytest -q` — confirm they fail for the expected reason.
   Commit `test(F-nn): add scenario tests (red)`.
2. **Data.** SQLAlchemy 2.0 typed models per the data model; import them in
   `app/models/__init__.py`. Generate the migration
   (`docker compose exec backend alembic revision --autogenerate -m "F-nn <slug>"`), **show its
   operations and flag any drop, rename or type change**, then `alembic upgrade head`.
   Commit `feat(F-nn): add data model and migration`.
3. **Capabilities** (only if the slice touches a register row with v0 = `fake`): port
   (`Protocol`) named after the capability, not a vendor; fake adapter mirroring the contract
   shape; factory by `settings.mode_for("<capability>")`. Async callbacks via a mock-provider route scheduling
   a `BackgroundTask` that calls our **real** inbound route over HTTP. Inbound handlers are
   idempotent.

   **User-facing step** (the register's contract shape names one, e.g. a hosted payment page):
   the fake adapter returns a **relative** URL to a stand-in page in `app/integrations/mock_providers.py`,
   so the browser stays on the Vite proxy:
   - `GET /api/mock-providers/<capability>/<step>/{id}` (the router adds `/mock-providers`, the
     app `/api`) → `HTMLResponse`: plain, unstyled HTML (it plays someone else's page, not ours)
     with one button per outcome the spec covers, e.g. pay, decline, abandon.
   - Each button is an **empty** `<form method="post" action="/api/mock-providers/…/{id}/<outcome>">`
     — the outcome is in the path, so no form fields (`python-multipart` is not installed).
   - The POST route schedules the callback `BackgroundTask` (none for *abandon*) and returns
     `RedirectResponse(<relative return URL>, status_code=303)`.
   - Scenario tests keep calling our inbound route directly; the page is for trying the flow by
     hand and for demos.

   **AI** (capability `ai`, D-05): don't write a new port — use `app/integrations/ai.py`. Add the
   Pydantic output schema, the prompt file `app/prompts/f_nn_<slug>.v1.md`, and a service that
   builds the minimised input, calls `get_generation().generate(...)`, stores the audit fields
   from `Generation`, and handles `GenerationError` with the planned fallback. In tests,
   override `get_generation` with a `FakeStructuredGenerationAdapter` that has the scenario's
   response (or error) registered.
4. **API.** Pydantic schemas, service functions (own the transaction), thin router registered
   in `app/api/__init__.py`. Run backend tests → **green**. Commit `feat(F-nn): add <resource> API`.
5. **Thin UI.** Plain semantic HTML components for the `@ui` scenario's flow, inside
   `components/Layout.tsx` (brand header, `main`, footer), calling `src/api/client.ts`.
   `src/base.css` styles the elements — `article` is a card, `mark` a highlight pill,
   `role="status"`/`role="alert"` a notice, `a role="button"` a button-link; helpers `.cards`,
   `.stack`, `.muted`; `data-variant="secondary"` for a secondary button. No inline styles,
   no new CSS files, no raw colours.
   **Brand** (as planned): set `src/brand.ts` and the *Brand* block of `src/theme.css` from §5.
   A colour given only in words → choose a hex, log `A-nn` in §11 (`Raised by: 05-build-slice`).
   Pick each `--brand-on-*` so text reaches 4.5:1 — on light accents that means dark text.
   No logo file in the repo → leave `logo: null`. Test the `@ui` scenario with vitest
   + Testing Library (`it('F-nn/S-nn …')`, fetch stubbed). `npm run typecheck` and `npm test` green.
   Add the planned seed data to `app/seed.py` and run it. Commit `feat(F-nn): add <page> page`.
   **AI eval set** (AI slices only): write `evals/cases/f_nn_<slug>.jsonl` from the spec's eval
   plan (5–10 cases) and `evals/test_eval_f_nn_<slug>.py` with one objective check per case and
   `assert_pass_rate(..., 0.8)`. Run it if `AI_MODE=real` and a key are set and report the
   score; otherwise say it is ready to run. Don't tune the prompt to the cases silently — report
   failures and propose a `v2` prompt.
6. **Close.** Set the feature's `Status` to `built` in `docs/02-features.md`, then run all suites
   — `tests/test_traceability.py` now checks every scenario of this feature has its test.
   If the implementation changed anything in `03-architecture.md`, update it and say so.
   Commit `docs(F-nn): mark built and sync architecture` — these doc edits are yours (status, architecture sync), so they belong
   in your commit; flag any architecture change in the report for the human to review.

## Rules

- **Never weaken a test to make it pass.** If a scenario looks wrong or ambiguous, stop and ask —
  the spec is the contract.
- If a step grows beyond the plan (new entity, new endpoint, new dependency), stop and re-plan.
- Build only what the scenarios require. Features under `Out of scope` in the spec header are
  not built, even if `03-architecture.md` designs for them — list any fields or tables you defer
  in the plan, so the human sees the gap.
- Only pre-approved dependencies (see `CLAUDE.md`); anything else → ask.
- Time-dependent rules read "now/today" from an injectable FastAPI dependency, so tests pin
  the clock instead of depending on the day they run.

## Final report (≤ 12 lines)

- Scenario → test → result table
- Commits made
- How to try it (URL + steps)
- Deviations and proposed decisions
- What the next slice would be
- Commands for the human to verify independently:

  ```bash
  docker compose exec backend pytest -v -k "f_nn"     # this slice's scenarios, by name
  docker compose exec frontend npm test               # UI scenario
  docker compose exec backend pytest evals -s         # AI slices: model quality vs threshold
  docker compose logs -f backend                      # watch requests while trying it
  ```
