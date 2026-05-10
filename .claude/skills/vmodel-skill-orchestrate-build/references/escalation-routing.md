---
purpose: target_layer routing rules for ESC-NNN.yaml files — determines which spec layer owns the issue and which human action is required.
audience: vmodel-skill-orchestrate-build
status: active
---

# Escalation Routing

## Contents

- [What routing does](#what-routing-does)
- [Routing Table](#routing-table)
- [Dependency-strength and blocking propagation](#dependency-strength-and-blocking-propagation)
- [ESC file routing fields](#esc-file-routing-fields)
- [Required action patterns](#required-action-patterns)
- [Scope-expansion routing](#scope-expansion-routing)

---

## What routing does

An escalation file carries a `target_layer` field. This routes the issue to the right spec artifact for human resolution. Wrong routing wastes the human's time — they open the wrong document and find nothing actionable.

The routing decision depends on two inputs: **where in the pipeline the failure occurred** (leaf, branch, or root stage) and **what type of failure it is** (ambiguity, gap, contradiction, contract-violation, new-decision-needed).

---

## Routing Table

| Pipeline position | Failure type | `target_layer` | Rationale |
|:-----------------|:-------------|:---------------|:----------|
| Leaf stage — implement-leaf REJECTED (max retries) | `ambiguity` | `detailed-design` | Implementer couldn't make a defensible choice; DD is underspecified |
| Leaf stage — implement-leaf REJECTED (max retries) | `gap` | `detailed-design` | Missing content the implementer needed |
| Leaf stage — review-execution ESCALATE | `ambiguity` | `detailed-design` | Reviewer found spec gap that makes the implementation unverifiable |
| Leaf stage — review-execution ESCALATE | `contradiction` | `detailed-design` | DD contradicts itself or parent requirements |
| Leaf stage — render-tests ESCALATE | `ambiguity` | `testspec` | TestSpec is too ambiguous to generate runnable test code |
| Leaf stage — render-tests ESCALATE | `gap` | `testspec` | TestSpec is missing cases needed by the DD |
| Branch stage — review-execution ESCALATE | `contract-violation` | `architecture` | Integration test revealed a component violating its own interface contract |
| Branch stage — review-execution ESCALATE | `ambiguity` | `architecture` | Interface contract was too vague for integration-level verification |
| Branch stage — review-execution ESCALATE | `gap` | `architecture` | Interface not specified at all |
| Branch stage — review-execution ESCALATE | `new-decision-needed` | `adr` | Integration revealed a cross-cutting choice not previously captured |
| Branch stage — integration test failure (unexpected) | `contradiction` | `architecture` | Components implemented per their DDs but fail at integration — architecture is wrong |
| Root stage — review-execution ESCALATE | `ambiguity` | `requirements` | System-level test revealed a requirement that was too vague to implement and verify |
| Root stage — review-execution ESCALATE | `gap` | `requirements` | System capability missing from requirements |
| Root stage — review-execution ESCALATE | `contradiction` | `requirements` | Requirements contradict each other at system level |
| Root stage — review-execution ESCALATE | `new-decision-needed` | `adr` | System test revealed a cross-cutting decision not yet captured |
| Root stage — system test failure (fundamental) | `gap` | `product` | System does not meet a top-level need not captured in formal requirements |

**Default fallback.** When failure type is clear but the position mapping is ambiguous, use the **closest upstream spec layer that directly governs the failing behaviour**. When uncertain, write `target_layer: unknown` and add a `confidence: low` field — do not guess with `confidence: high`.

---

## Dependency-strength and blocking propagation

When a task escalates, dependent tasks may or may not be blocked depending on `dep_strength` declared in `tasks.yaml`:

| `dep_strength` | Effect on dependent when upstream escalates |
|:---------------|:--------------------------------------------|
| `required` | Dependent is `blocked`. Cannot proceed without upstream resolution. |
| `helpful` | Dependent MAY proceed with a warning note in its `current-task.yaml`. Signal to implement-leaf that a dependency result is absent. |
| `optional` | Dependent proceeds unchanged. |

Default dep strength when not declared: `required`.

Propagation is transitive: if A is escalated, B (required on A) is blocked, and C (required on B) is blocked — even though C has no direct edge to A.

---

## ESC file routing fields

The fields that convey routing information in an `ESC-NNN.yaml` file:

```yaml
target_layer: detailed-design   # One of: detailed-design | testspec | architecture | adr | requirements | product | unknown
target_artifact: DD-app-checkout # Specific artifact ID if known; omit if unknown
issue_type: ambiguity            # ambiguity | gap | contradiction | new-decision-needed | contract-violation
confidence: high                 # low | medium | high — confidence in the routing decision
```

**When `confidence: low`:** add a `routing_note` field with a one-sentence explanation of the ambiguity. This flags the case for human re-routing before starting resolution work.

---

## Required action patterns

Each `issue_type` implies a standard `required_action` pattern:

| `issue_type` | Required action pattern |
|:-------------|:------------------------|
| `ambiguity` | "Clarify <specific clause> in <artifact-id> to remove multiple valid interpretations." |
| `gap` | "Add <missing content description> to <artifact-id>." |
| `contradiction` | "Resolve contradiction between <clause-A> and <clause-B> in <artifact-id>." |
| `new-decision-needed` | "Author an ADR for <decision topic> and propagate bindings to <affected scope>." |
| `contract-violation` | "Update <artifact-id> to either fix the contract clause or align the implementation with it." |

Write concrete, actionable `required_action` text — name the specific clause, field, or section where the change belongs. "Fix the DD" is not actionable; "Clarify the postcondition of `CartService.addItem()` — currently silent on duplicate SKU handling" is.

---

## Scope-expansion routing

When `implement-leaf` emits `build-blocked.yaml`, the orchestrator first decides
whether to auto-amend the contract (see `vmodel-skill-orchestrate-build/SKILL.md`
§Task Execution Loop step 4a). If the blocker cannot be auto-amended, route as
ESCALATE using the mapping below from the `suggested_resolution` field:

| `suggested_resolution`      | `target_layer`     | Notes |
|:----------------------------|:-------------------|:------|
| `escalate-to-dd`            | `detailed-design`  | DD does not specify what to do for the case the implementation hit. |
| `escalate-to-architecture`  | `architecture`     | Inter-leaf interface contract is unclear or contradictory. |
| `escalate-to-testspec`      | `testspec`         | A rendered test contradicts the DD. Pair with `blocker_type: test-defect`. |
| `escalate-to-adr`           | `adr`              | Cross-cutting decision not captured by any ADR. |
| `amend-contract` (over budget) | `detailed-design` | Auto-amend exhausted. Set `routing_note: "auto-amend exhausted (amendments_used=N >= max=M); blocker: <blocker_type>"`. |

`issue_type` follows the existing taxonomy:

- `blocker_type: scope-expansion` → `issue_type: gap` (typically — the spec
  did not list the file the impl needs to touch).
- `blocker_type: missing-context` → `issue_type: gap`.
- `blocker_type: contradiction` → `issue_type: contradiction`.
- `blocker_type: test-defect` → `issue_type: contract-violation` (test asserts
  something the DD does not specify).
- `blocker_type: external-dep` → `issue_type: new-decision-needed` (the
  external dep needs an ADR).

`confidence: high` on these routings — they are mechanically derived from
`suggested_resolution`. If `suggested_resolution` is missing or inconsistent
with `blocker_type`, downgrade to `confidence: low` and add a `routing_note`.
