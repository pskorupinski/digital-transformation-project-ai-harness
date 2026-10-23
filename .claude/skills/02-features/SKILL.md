---
name: 02-features
description: Turn the discovery brief into a traceable feature list — job stories, Kano classification, AI opportunities, proposed scope and cut list. Use after docs/01-brief.md has content.
argument-hint: "[optional focus or instructions]"
disable-model-invocation: true
allowed-tools: Read Edit Write
---

# 02 · Features

Produce `docs/02-features.md` from the brief. You **propose**; the human decides.
Extra instructions from the human (may be empty): $ARGUMENTS

## Inputs

- `docs/01-brief.md` (required) — cite as `§n`
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

8. **Validation questions.** 2–4 plain-language questions to confirm Must-be labels with the
   business, e.g. "If a customer couldn't ⟨X⟩, would they still buy?"

## Re-run rules

- Keep IDs stable — never renumber. New features take the next free `F-nn`.
- **Never change a scope without `?`** — the human decided it. Only `?` values may be re-proposed.
- Keep `Status` values. Report what changed in your chat summary.

## Output — `docs/02-features.md`

Keep the file's header blockquote, then write exactly these sections:

```markdown
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

## Chat summary (≤ 10 lines)

- Counts per Kano class and per proposed scope
- The `?` the human must resolve
- The validation questions
- Assumptions added to §11
- If more than 6 features are `v0?`: say so and name the ones that could merge or wait — a
  smaller v0 keeps the architecture reviewable
- The commit the human makes once the review is done (don't run it — committing is their
  approval):

  ```bash
  git add docs/ && git commit -m "Human: confirm features and v0 scope"
  ```

Then stop — do not start architecture.
