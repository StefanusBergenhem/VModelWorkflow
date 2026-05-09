# Pattern Extraction — Clustering Rules and Thresholds

Reference for `vmodel-skill-retrospect-build`. Applied in Step 3 of the skill process.

---

## Contents

1. [Rejection-type taxonomy](#1-rejection-type-taxonomy)
2. [Clustering rules](#2-clustering-rules)
3. [Escalation cluster rules](#3-escalation-cluster-rules)
4. [Retry-thrashing detection](#4-retry-thrashing-detection)
5. [Evidence threshold table](#5-evidence-threshold-table)

---

## 1. Rejection-type taxonomy

`feedback.yaml` files use a `rejection_type` field. Recognised values and their meaning:

| Value | What it signals |
|:------|:----------------|
| `missing_implementation` | Acceptance criteria not met; code absent or stub |
| `test_quality` | Tests pass but are tautological, trivially asserted, or miss stated scenarios |
| `scope_violation` | Changes outside the files_to_touch contract |
| `convention_violation` | Naming, formatting, or project-convention mismatch |
| `contract_ambiguity` | Reviewer could not determine pass/fail — contract unclear |
| `interface_mismatch` | Implementation does not match the declared interface in detailed design |
| `spec_gap` | Implementation required information not present in spec or contract |
| `other` | Anything not fitting above — read `notes` field for detail |

When `rejection_type` is absent from a feedback file, treat as `other`.

---

## 2. Clustering rules

### Rejection-type cluster

**Trigger:** the same `rejection_type` appears in `feedback.yaml` files across 2 or more distinct tasks.

**Action:** create a candidate pattern of category `rejection_pattern`. The pattern rule must be a concrete instruction, not a label. Example:

- Bad: "Multiple tasks had convention_violation rejections."
- Good: "Include the project CONVENTIONS.md in context for every task that modifies existing files."

**Single-occurrence exception:** if a single task has `severity: high` in its feedback file, it qualifies as a solo candidate (category: `rejection_pattern`, confidence starts at `low`). Do not invent `severity: high` — it must be present in the file.

### Subsystem concentration

**Trigger:** 3 or more rejected tasks belong to the same subsystem (derive subsystem from task scope prefix, e.g. `auth/`, `payment/`).

**Action:** create a candidate pattern of category `architecture_pattern`. Rule must describe the subsystem and the signal, e.g. "The `auth/` subsystem had 4 rejections across this run; its detailed designs may need interface clarification before the next build."

### Cross-type change on retry

**Trigger:** a task's rejection type changed between attempt N and attempt N+1 (e.g., `missing_implementation` on attempt 1, `scope_violation` on attempt 2).

**Action:** candidate pattern of category `contract_pattern`. Signal: the original contract was incomplete — fixing one dimension exposed another gap. Rule: "When initial rejection is `missing_implementation` followed by `scope_violation`, the task contract likely omitted required context files."

---

## 3. Escalation cluster rules

### Same-layer cluster

**Trigger:** 2 or more escalations with the same `target_layer`.

**Action:** candidate pattern of category `escalation_pattern`. Rule must name the layer and suggest a spec-authoring fix, e.g. "Two escalations targeted `detailed-design`; the DD authoring pass for the next scope should tighten interface contracts."

### High-impact single escalation

**Trigger:** a single escalation with `target_layer: requirements` or `target_layer: product`, OR any escalation that blocked 3+ dependent tasks (compute blocked count from `task_states`).

**Action:** qualifies as a single-occurrence high-impact candidate (confidence starts at `low`). Always include it in the "Escalations" section of the retrospective, even if it does not produce a lesson.

---

## 4. Retry-thrashing detection

**Definition:** a task is "thrashing" when `review_attempts >= 3`.

**Signal types:**

| Observation | Implied signal |
|:------------|:---------------|
| Same rejection type across all attempts | Contract is ambiguous or missing key context — agent cannot converge |
| Rejection type changes each attempt | Spec has multiple independent gaps; each fix reveals the next |
| Attempts 1–2 same type, attempt 3 escalated | Threshold hit; underlying issue is structural, not superficial |

**Pattern rule construction for thrashing tasks:** always name the task ID and the rejection-type sequence. Example: "Task `auth/login` thrashed 3 times (`missing_implementation` → `scope_violation` → escalated); contract likely requires `auth/session.md` as context."

**Threshold:** a single thrashing task always qualifies for the retrospective "What failed" section. It qualifies as a lesson candidate only if a second task shows the same rejection-type sequence OR the task was explicitly marked `severity: high`.

---

## 5. Evidence threshold table

| Scenario | Candidate? | Starting confidence |
|:---------|:----------:|:-------------------:|
| Same rejection_type in 2+ tasks | Yes | `medium` |
| Single task, `severity: high` in feedback | Yes | `low` |
| 3+ tasks in same subsystem rejected | Yes | `medium` |
| 2+ escalations to same target_layer | Yes | `medium` |
| Single escalation to `requirements` or `product` | Yes | `low` |
| Single escalation that blocked 3+ tasks | Yes | `low` |
| Thrashing task with matching second task | Yes | `medium` |
| Thrashing task, solo | Yes (retro only) | Do not create lesson |
| Single rejection, no severity field, no cluster | No | — |

"Retro only" means: include in retrospective report but do not write to lessons.yaml.
