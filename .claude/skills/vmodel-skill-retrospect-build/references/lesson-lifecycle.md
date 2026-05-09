# Lesson Lifecycle — Schema, Confidence, Cap, Eviction

Reference for `vmodel-skill-retrospect-build`. Applied in Step 5 of the skill process.

---

## Contents

1. [Lesson schema](#1-lesson-schema)
2. [Categories](#2-categories)
3. [Deduplication](#3-deduplication)
4. [Confidence-rise table](#4-confidence-rise-table)
5. [Cap enforcement](#5-cap-enforcement)
6. [Eviction algorithm](#6-eviction-algorithm)
7. [File structure](#7-file-structure)

---

## 1. Lesson schema

Each lesson entry in `lessons.yaml`:

```yaml
- id: L-001                          # stable; never reuse an evicted ID
  category: contract_pattern         # see §2
  rule: "<one-sentence actionable instruction>"
  evidence:
    - run: <run-id>
      task: <task-id>                # or "run-level" if not task-specific
      excerpt: "<quoted text from feedback.yaml or ESC-NNN.yaml>"
  confidence: medium                 # low | medium | high
  added: YYYY-MM-DD
  last_seen: YYYY-MM-DD
```

**`rule` quality bar:**
- Must be phrased as an instruction ("Always include X", "When Y, do Z").
- Must be specific enough to act on without reading the evidence.
- Must not restate the observation ("tasks in auth/ were rejected often" is not a rule).

**`excerpt` requirement:**
- Must be a direct quote, not a paraphrase.
- Pull from `rejection_reason`, `notes`, or `description` fields in the source files.
- If no quotable text exists in the source file, do not create the lesson.

**`id` assignment:** find the highest existing `L-NNN` in the file, increment by 1. Do not recycle IDs from evicted entries.

---

## 2. Categories

| Category | What it captures |
|:---------|:-----------------|
| `contract_pattern` | Task contract quality rules: context_to_load, files_to_touch, scope boundaries |
| `rejection_pattern` | Recurring rejection types and proven corrective actions |
| `escalation_pattern` | Escalation clusters and what spec layer needs strengthening |
| `architecture_pattern` | Design-level signals: subsystem boundaries, interface gaps, component health |
| `other` | Anything not fitting the above — use sparingly |

---

## 3. Deduplication

Before creating a new lesson, scan existing entries for a semantic match:

**Exact match:** same `category` AND the `rule` sentences are equivalent in meaning (same subject, same instruction). Skip — do not create a duplicate. If the new run provides additional evidence, append to the existing entry's `evidence` list and update `last_seen`.

**Reinforcement match:** same `category` AND the `rule` addresses the same root cause but is phrased differently OR applies to a broader/narrower scope. Treat as a reinforcement:
- Append the new run's evidence to the existing entry.
- Update `last_seen` to today.
- Apply the confidence-rise table (§4).
- Do NOT create a new entry.

**No match:** create a new entry with the next available ID.

**Heuristic for semantic matching:** the rule subject (component name, rejection type, layer) must overlap. Example: a rule about `auth/` and a new rule about `auth/login` are a reinforcement match. A rule about `convention_violation` and a new rule about `test_quality` are not a match.

---

## 4. Confidence-rise table

| Current confidence | Trigger | New confidence |
|:-------------------|:--------|:---------------|
| `low` | Reinforced by 1 additional run | `medium` |
| `low` | Reinforced by 2+ additional runs (same session or across runs) | `high` |
| `medium` | Reinforced by 1 additional run | `high` |
| `medium` | No new reinforcement in 5+ runs | Stays `medium` — do not lower |
| `high` | Any reinforcement | Stays `high` |
| `high` | No new reinforcement in 10+ runs | Stays `high` — confidence does not decay |

**Single-run cap:** a new lesson created in the current run may rise at most to `medium` in that same run, regardless of how many tasks triggered it. The `low → high` jump requires at least 2 distinct runs. This prevents a single anomalous run from inflating confidence.

---

## 5. Cap enforcement

Default cap: `max_lessons = 30`. Configurable in `.vmodel/config.yaml` under `build.retrospect.max_lessons`.

**When is the cap checked:** after all new lessons are added and all reinforcements are applied, before writing the file.

**If total count <= cap:** no action needed.

**If total count > cap:** run the eviction algorithm (§6). The cap is a hard ceiling — the file must not exceed it after each run.

---

## 6. Eviction algorithm

Goal: evict the minimum number of lessons to bring total count to `max_lessons`.

### Scoring each lesson

Compute an eviction priority score (lower = evict first):

```
score = confidence_weight + evidence_weight + recency_weight

confidence_weight:
  high   → 4
  medium → 2
  low    → 1

evidence_weight:
  count(evidence entries)   → +1 per entry (no cap)

recency_weight:
  last_seen within 3 runs of current run  → +2
  last_seen within 10 runs of current run → +1
  older                                   → +0
```

To determine "runs ago": compare `last_seen` date against `pipeline-state.yaml → started_at` date. Use calendar days as a proxy if run count is unavailable (< 7 days = within 3 runs, < 30 days = within 10 runs).

### Eviction preference ordering

1. Evict `low`-confidence entries first, sorted by score ascending.
2. If more eviction needed and no `low`-confidence entries remain, evict `medium`-confidence entries with score ascending.
3. Never evict `high`-confidence entries while any `low` or `medium` entries exist.
4. If the only remaining entries are `high`-confidence and the cap is still exceeded: HALT — do not evict. Report: "Cap exceeded with only high-confidence lessons. Raise `build.retrospect.max_lessons` in config.yaml or manually review lessons.yaml." Ask the user; do not proceed silently.

### After eviction

- Write the updated lessons list to `lessons.yaml`.
- Do NOT permanently delete evicted lessons — they are simply removed from the active file. The retrospective report's "Patterns extracted" section still documents what was found this run; evicted lessons remain visible there even if not stored.

---

## 7. File structure

`lessons.yaml` lives at `.vmodel/.build/lessons.yaml`. It is cumulative across all runs in the project.

Top-level structure:

```yaml
version: 1
max_lessons: 30          # can be overridden by config.yaml
lessons:
  - id: L-001
    ...
```

**Initialization:** if the file does not exist on first run, create it with `version: 1`, `max_lessons: <from config or 30>`, and an empty `lessons: []`. Use `templates/lessons.yaml.tmpl` as the starting point.

**Parse failure:** if the file exists but fails YAML parsing, HALT. Report the error and the approximate line. Do not overwrite a corrupt file.
