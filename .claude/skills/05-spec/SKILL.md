---
name: 05-spec
description: Write the Gherkin acceptance spec for one confirmed feature — 4–6 scenarios that become its tests. Use before building a slice.
argument-hint: "F-nn [number of scenarios] [optional instructions]"
disable-model-invocation: true
allowed-tools: Read Edit Write
---

# 05 · Spec

Write `docs/05-specs/F-nn-<slug>.feature` for the feature in the arguments. The scenarios are
the acceptance criteria **and** the test plan for `/06-build-slice`.
Arguments: $ARGUMENTS

## Inputs and preconditions

- `docs/03-features.md` — the feature must exist with a scope **without `?`**. Otherwise stop.
- `docs/04-architecture.md` — entities, flows and endpoints the feature uses. If the feature
  isn't covered there, stop and say so (run `/04-architecture` first).
- `docs/01-brief.md` — business rules and domain language; `docs/02-integrations.md` — contracts.
- `docs/05-specs/README.md` — conventions.

## Choosing scenarios (default 5, range 4–6, or the number given)

In this order, skipping what doesn't apply:
1. **Happy path** — the job story's outcome, end to end.
2. **The business rule that matters most** — the validation the business would be hurt by.
3. **Boundary failure** — if an integration is involved: the external system declines, times
   out, or its callback arrives twice / never.
4. **State or consistency edge** — repeated submission, concurrent use, stale data.
5. **One `@ui` scenario** — the main user-visible flow, so the slice has a UI test too.

## Writing rules

- **Declarative, not imperative:** what the actor achieves, not clicks, selectors, endpoints,
  tables or status codes. Domain language from the brief.
- **Concrete example data** (names, quantities, amounts) — no "some product", "valid input".
- One behaviour per scenario; `Then` checks observable outcomes only; scenarios independent.
- `Scenario Outline` for data variations (counts as one scenario).
- Tag every scenario `@api` or `@ui` — the level its test will live at. Default `@api`.
- Anything the brief doesn't settle → append `A-nn` to brief §10 (`Raised by: 05-spec`) and
  write the scenario on that assumption, citing it in a comment.

## Output format

```gherkin
@F-nn
Feature: F-nn <feature name>
  When …, I want to …, so I can …
  # Sources: §n · Entities: <names> · Integrations: I-nn · Assumptions: A-nn

  Background:
    Given …

  @api
  Scenario: S-01 <short title>
    Given …
    When …
    Then …
```

Then set the feature's `Status` in `docs/03-features.md` to `specified`.

## Chat summary

One line per scenario (`S-01 @api — title`), assumptions added, and any gap found in the
architecture (as a question for the human, not a fix). Then stop — no code.
