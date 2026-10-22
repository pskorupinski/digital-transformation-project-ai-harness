---
name: 03-features
description: Turn the discovery brief into a traceable feature list — job stories, Kano classification, AI opportunities, proposed scope and cut list. Use after docs/01-brief.md has content.
argument-hint: "[optional focus or instructions]"
disable-model-invocation: true
allowed-tools: Read Edit Write
---

# 03 · Features

Produce `docs/03-features.md` from the brief. You **propose**; the human decides.
Extra instructions from the human (may be empty): $ARGUMENTS

## Inputs

- `docs/01-brief.md` (required) — cite as `§n`
- `docs/02-integrations.md` — external systems, `I-nn`
- `docs/03-features.md` — if it already has features, this is a **re-run** (see below)
- `decisions.md` — don't propose features that contradict accepted decisions

**Stop condition:** if §1–§5 are mostly empty, don't generate. Say which sections are missing
and suggest 2–3 questions to fill them. Never invent business facts.

## Method

1. **Actors.** Who interacts with the solution (customer segments from §2, the business's staff
   from §3/§6, external systems from 02). One line each, with source.
2. **Job stories** (Intercom format): *When* ⟨situation⟩, *I want to* ⟨motivation⟩,
   *so I can* ⟨expected outcome⟩. One job story per feature, written from the actor's situation,
   not from the UI. Aim for **8–15 features** — group small ones, split only when actors differ.
3. **Source every feature.** `Source` cites the brief sections it comes from (`§3, §5`). A feature
   with no source in the brief gets a new assumption `A-nn` appended to brief §10
   (`Raised by: 03-features`, `Status: open`) and cites that ID instead.
4. **Kano classification** — how the actor would react, judged from the brief:
   - `Must-be` — absence causes anger / makes the solution unusable; presence goes unnoticed
   - `Performance` — more/better is proportionally better (speed, choice, convenience)
   - `Attractive` — unexpected delight; must be grounded in §4 Differentiation
   - `Indifferent` — nobody would really care either way
   This is a classification from interview notes, not a Kano survey — say so if asked.
5. **AI opportunities.** Tag `AI` only where AI genuinely simplifies something complex or
   creates real value for an actor — not as decoration. For each tagged feature, specify in the
   AI section: human-in-the-loop point, how output quality would be measured, data it is grounded
   in (which source of truth), main risk (hallucination, data sensitivity). If nothing qualifies,
   write "None identified" and why.
6. **Proposed scope** — always with `?`, applying this rule:
   - `v1?` = every Must-be in its **minimal** form + **exactly one** Attractive feature tied to §4
     (it is the reason to build custom rather than buy)
   - Performance → `v1?` only if the brief demands it (§1 goals, §8 scale), else `v2?`
   - AI features → `v2?` by default (they need the v1 data to be grounded)
   - Indifferent → `cut?`, and onto the cut list
   - Integrations marked `out of scope` in 02 → the dependent feature is `later?` or `cut?`
7. **Validation questions.** 2–4 plain-language questions to confirm Must-be labels with the
   business, e.g. "If a customer couldn't ⟨X⟩, would they still buy?"

## Re-run rules

- Keep IDs stable — never renumber. New features take the next free `F-nn`.
- **Never change a scope without `?`** — the human decided it. Only `?` values may be re-proposed.
- Keep `Status` values. Report what changed in your chat summary.

## Output — `docs/03-features.md`

Keep the file's header blockquote, then write exactly these sections:

```markdown
## Actors
| Actor | Description | Source |

## Feature list
| ID | Feature | Actor | Job story | Kano | AI | Scope | Status | Source |
| F-01 | <2–4 words> | <actor> | When …, I want to …, so I can … | Must-be | | v1? | proposed | §3 |

## AI opportunities
### F-nn <feature>
- **Human in the loop:** …
- **Quality measure:** …
- **Grounded in:** …
- **Main risk:** …

## Cut list
| ID | Feature | Kano | Why cut |

## Validation questions for the business
1. …
```

Status values: `proposed → specified → built` (later steps update it).

## Chat summary (≤ 10 lines)

Counts per Kano class and per proposed scope · the `?` the human must resolve · the validation
questions · assumptions added to §10. If more than 6 features are `v1?`, say so and name the
ones that could merge or wait — a smaller v1 keeps the architecture reviewable.
Then stop — do not start architecture.
