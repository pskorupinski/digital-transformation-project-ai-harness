---
name: 02-features
description: Turn the discovery brief into a traceable feature list — blocking assumptions with their scope branches, job stories, Kano classification, AI opportunities, proposed scope and cut list. Use after docs/01-brief.md has content; re-run with "A-nn <answer>" to apply the business's answer to a blocking assumption.
argument-hint: "[A-nn <answer> | optional focus or instructions]"
disable-model-invocation: true
allowed-tools: Read Edit Write
---

# 02 · Features

Produce `docs/02-features.md` from the brief. You **propose**; the human decides.
Extra instructions from the human (may be empty): $ARGUMENTS

If `$ARGUMENTS` starts with an assumption ID (`A-03 place held`), this is a **resolution**, not
a generation — follow *Resolving a blocking assumption* below and do nothing else.

## Inputs

- `docs/01-brief.md` (required) — cite as `§n`; §11 holds the existing `A-nn` rows
- `docs/02-features.md` — if it already has features, this is a **re-run** (see below)
- `decisions.md` — don't propose features that contradict accepted decisions

**Stop condition:** if §1–§6 are mostly empty, don't generate. Say which sections are missing
and suggest 2–3 questions to fill them. Never invent business facts.

## Method

1. **Actors.** Who interacts with the solution: customer segments (§2), the business's staff
   (§3, §7), external parties. One line each, with source.
2. **Job stories** (Intercom format): *When* ⟨situation⟩, *I want to* ⟨motivation⟩,
   *so I can* ⟨expected outcome⟩. One per feature, written from the actor's situation, not from
   the UI. Aim for **8–15 features** — group small ones, split only when actors differ.
3. **Source every feature.** `Source` cites the brief sections it comes from (`§3, §6`). A feature
   with no source gets a new assumption `A-nn` appended to brief §11
   (`Raised by: 02-features`, `Status: open`) and cites that ID instead.
4. **Capability.** If a feature needs something the business may not have today — taking online
   payment, sending messages, syncing stock — name it in `Capability` in plain words. **Judge the
   feature on customer value, never on today's systems** (§8): whether and how the capability
   is provided is decided in architecture.
5. **Kano classification** — how the actor would react, judged from the brief:

   | Class | Meaning |
   |---|---|
   | Must-be | Absence causes anger or makes the solution unusable; presence goes unnoticed |
   | Performance | More or better is proportionally better (speed, choice, convenience) |
   | Attractive | Unexpected delight — must be grounded in §4 Differentiation |
   | Indifferent | Nobody would really care either way |

   This is a classification from interview notes, not a Kano survey — say so if asked.
6. **AI opportunities.** Tag `AI` only where AI genuinely simplifies something complex or
   creates real value for an actor — not as decoration. For each, specify in the AI section:
   human-in-the-loop point, how output quality would be measured, data it is grounded in, main
   risk (hallucination, data sensitivity). If nothing qualifies, write "None identified" and why.
7. **Proposed scope** — always with `?` (scope levels are defined in `CLAUDE.md`):

   | Proposal | Rule |
   |---|---|
   | `v0?` | Every Must-be in its **minimal** form + **exactly one** Attractive tied to §4 (the reason to build custom rather than buy) |
   | `v1?` | Performance features the brief makes necessary at launch (§1 goals, §9 scale) |
   | `v2?` | Other Performance features; AI features by default (they need v0/v1 data to be grounded) |
   | `cut?` | Indifferent — and onto the cut list |

8. **Blocking assumptions** — the questions the human must take back to the business *before*
   confirming scope. The business is usually still in the room, so a blocking assumption is a
   question to ask, not a guess to live with.

   - **Criterion.** An assumption is blocking only if a different answer would **add or remove a
     `v0?` feature**, or **change the main flow or data of a `v0?` feature**. Everything else is
     an ordinary assumption: append it to §11 and cite it, without stopping anyone.
   - **At most 3.** If more qualify, keep the 3 with the largest effect on v0 and make the rest
     ordinary assumptions. None is a valid outcome — say so.
   - **Contradictions** between statements in the brief (two different figures for the same
     thing) are assumptions too — blocking only if they meet the criterion. Don't speculate about
     whether a figure was stated or inferred; flag only what the brief itself contradicts.
   - **Branches.** For each one, pre-compute what each answer would do to scope, so the answer
     picks a branch instead of triggering a re-run:
     - either/or questions → one branch per answer (2–3)
     - open questions ("which payment methods?") → a default branch plus `Anything else`
     - mark one branch `default`: the reading most consistent with the brief; if the brief gives
       no lead, the one with the smaller v0
   - **The feature list follows the default branch.** Features that depend on a blocking
     assumption cite its `A-nn` in `Source`, like any assumption.
   - **Wording.** Write the question so the human can read it aloud to the business owner:
     business language, one question, no feature IDs or technical terms.
   - Append each to §11 like any assumption, with the text starting `Blocking —`
     (`Raised by: 02-features`, `Status: open`).

9. **Validation questions.** 2–3 plain-language questions to confirm Must-be labels with the
   business, e.g. "If a customer couldn't ⟨X⟩, would they still buy?" Never repeat a blocking
   question here.

## Re-run rules

- Keep IDs stable — never renumber. New features take the next free `F-nn`; new assumptions
  the next free `A-nn`.
- **Never change a scope without `?`** — the human decided it. Only `?` values may be re-proposed.
- Keep `Status` values. Report what changed in your chat summary.
- A blocking assumption whose §11 status is `confirmed` or `rejected` is resolved: apply it
  (as below) and leave it out of the *Blocking assumptions* section — §11 keeps the record.

## Resolving a blocking assumption

Invoked as `/02-features A-nn <answer>`. This is a targeted update — touch nothing else.

1. Find `A-nn` in brief §11 and its branch table in `docs/02-features.md`. If either is missing,
   stop and say so.
2. In §11: append the answer to the row text (`→ answer: <answer>`) and set `Status` to
   `confirmed`. Don't edit other brief sections — the human owns them.
3. **Answer matches a branch:** apply the branch's effect to the features it names — scope values
   **still with `?`** (the answer settles the assumption, the human still confirms scope), and any
   flow change it describes in those features' `Job story` and `Capability`.
   **Answer matches no branch:** update only the features whose `Source` cites `A-nn`, and say
   what you changed and why.
4. Never change a scope without `?`. If the answer conflicts with one, name the feature and leave
   it for the human.
5. Remove the resolved entry from *Blocking assumptions*. If it was the last one, write `None open`.
   Gaps the answer opens (a duration, a limit, a rule) become new ordinary `A-nn` rows in §11 —
   never blocking, never invented values.
6. Chat summary: one line per changed feature (`F-04: v0? → v1?`), and anything left for the human.
   Then stop.

## Output — `docs/02-features.md`

Keep the file's header blockquote, then write exactly these sections:

```markdown
## Blocking assumptions

> Ask the business before confirming scope. The feature list follows each **default** branch.
> Apply an answer with `/02-features A-nn <answer>`.

### A-nn · <question as you would ask it aloud>

| Answer | Effect on scope |
|---|---|
| **<answer>** (default) | F-04 → v0?, F-05 → cut? |
| <answer> | F-05 → v0?, F-04 → v1?; F-03 holds seats for 24h until paid |

Each effect names features by ID: scope changes as `F-nn → <scope>?`, flow changes in a few words.

**Affects:** F-04, F-05 — **Why blocking:** <one line: what in v0 changes>

## Actors

| Actor | Description | Source |
|---|---|---|

## Feature list

| ID | Feature | Actor | Job story | Kano | AI | Capability | Scope | Status | Source |
|---|---|---|---|---|---|---|---|---|---|
| F-01 | <2–4 words> | <actor> | When …, I want to …, so I can … | Must-be | | | v0? | proposed | §3 |

## AI opportunities

### F-nn <feature>

- **Human in the loop:** …
- **Quality measure:** …
- **Grounded in:** …
- **Main risk:** …

## Cut list

| ID | Feature | Kano | Why cut |
|---|---|---|---|

## Validation questions for the business

1. …
```

Leave a blank line before every table and list so Markdown renders them.
Status values: `proposed → specified → built` (later steps update it).

If no assumption is blocking, the section holds one line: `None — no open answer would change v0.`

## Chat summary (≤ 12 lines)

- **First:** the blocking questions, worded to read aloud, each with its default branch in a few
  words — this is what the human takes back to the business
- Counts per Kano class and per proposed scope
- The `?` the human must resolve
- The validation questions
- Other assumptions added to §11 (IDs only)
- If more than 6 features are `v0?`: say so and name the ones that could merge or wait — a
  smaller v0 keeps the architecture reviewable
- The commit the human makes once the review is done (don't run it — committing is their
  approval):

  ```bash
  git add docs/ && git commit -m "docs(features): confirm v0 scope"
  ```

Then stop — do not start architecture.
