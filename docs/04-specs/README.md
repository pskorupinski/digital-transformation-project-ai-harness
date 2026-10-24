# 04 · Specs

> **Step 04 — skill `/04-spec F-nn`, reviewed by a human.**
> One Gherkin file per slice: `F-nn-<slug>.feature`. Scenarios are the acceptance criteria
> *and* the test plan — `/05-build-slice` writes one test per scenario, named after its ID (D-04).

Gherkin is Cucumber's specification language; `.feature` is its standard extension. Here the
files are **not executed** — tests are linked by scenario ID and `backend/tests/test_traceability.py`
fails if a `built` feature has a scenario without its test.

| Convention | Rule |
|---|---|
| Scenario IDs | `S-01…`, unique within a feature; referenced as `F-03/S-02` |
| Tags | `@F-nn` on the feature; `@api` or `@ui` on each scenario (the level its test lives at) |
| Size | 4–6 scenarios per slice: happy path first, then the validations and failures that matter |
| Language | Concrete example data, business terms; no endpoints, tables or CSS |
| Boundary | One feature's job story only; behaviour other features own is listed as `# Out of scope: F-nn` in the header |
