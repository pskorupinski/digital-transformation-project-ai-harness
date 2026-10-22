# 05 · Specs

> **Step 05 — skill `/05-spec F-nn`, reviewed by a human.**
> One Gherkin file per slice: `F-nn-<slug>.feature`. Scenarios are the acceptance criteria
> *and* the test plan — `06-build-slice` writes one test per scenario, named after its ID.

Conventions:

- Scenario IDs `S-01…` are unique within a feature; reference them as `F-03/S-02`.
- Tags: `@F-nn` on the feature, `@api` or `@ui` on each scenario (the level its test lives at).
- 4–6 scenarios per slice: happy path first, then the validations and failures that matter.
- Concrete example data, no technical details (no endpoints, tables or CSS).
