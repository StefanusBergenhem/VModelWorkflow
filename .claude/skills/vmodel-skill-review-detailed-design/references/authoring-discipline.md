---
purpose: Cross-cutting authoring discipline. Author skills follow; review skills enforce as `check.discipline.<rule>` findings.
audience: author skills, review skills, framework maintainers
status: active (Phase 6)
applies_to: all author and review skills for the 6-artifact set
source_of_truth: this file. Per-skill copies at `references/authoring-discipline.md` are verbatim. Sync via `scripts/sync-authoring-discipline.sh`.
---

# Authoring Discipline

Six rules. They exist because spec-tier work runs on a token budget, and bloat caps which model tier can author the artifact.

**Contents.** Rule 0 product-shape only · Rule 1 boundary-only · Rule 2 small-system collapse · Rule 3 rationale-as-citation · Rule 4 diagram-or-prose · Rule 5 cite-don't-restate · Review enforcement · Distribution.

---

## Rule 0 — Product-shape only

The artifact describes the product as it is. It does not describe the template that shaped it, the artifact itself, or how it was authored. If a slot does not apply, omit it.

**Forbidden manifestations.**
- `n/a + justification` entries explaining why a template slot was left empty.
- *Departures from template* / *Authoring conventions used* sections.
- *Notes / Self-attestation* sections.
- "Honest departure from..." framings that defend absences.

**Test.** Is this section's subject the product? If the answer is "the template", "this artifact", or "how this artifact was authored", delete or push to front-matter.

**Allowed.**
- *Open follow-ups* (gaps in the **product's** spec, not the artifact's process).
- Front-matter metadata (status, version, derivation links, recovery_status).
- *Glossary*.

**Narrow exception.** When an upstream spec explicitly mandates a slot the product genuinely lacks, one sentence is warranted — but the right resolution is to fix the upstream binding (e.g., introduce a scope-shape template variant), not defend in the child.

**Anti-examples.** `architecture.md`'s *Middleware stack — n/a — single-process CLI...* (template-shape) and the *Notes / Self-attestation* section at end-of-file (artifact-shape). Both delete entirely.

---

## Rule 1 — Boundary-only at non-leaf scope

Architecture describes seams: each child's purpose, the interface contract at each seam (preconditions, postconditions, invariants, typed errors, thread-safety), the composition pattern, quality-attribute allocation. It does NOT describe internal data structures, algorithms, internal state, or implementation choices of any child.

**Test.** Could two implementers, given only this content, build the children with non-overlapping concerns and have them compose at runtime? Anything beyond what's needed for that test is DD leakage.

**Tells.** A responsibility reads like a procedure ("first parses X, then validates Y"). Internal types appear in body content (not just at boundary signatures). Library names appear in `responsibilities` or `purpose` (vs. in `rationale` citing the governing ADR — see Rule 3).

**Boundary content is protected.** Interface signatures, DbC clauses (preconditions, postconditions, invariants), and typed error enums are *the* deliverable at this scope; do not compress them. If they collectively bloat the artifact past the working budget, that is a template-level structural concern (e.g., factor shared invariants into a referenced block), not a discipline concern.

---

## Rule 2 — Small-system collapse

When all children of a scope are leaves AND the count is fewer than 5, architecture and DD MAY be authored as one combined artifact (`architecture-and-design.md`, front-matter `kind: architecture-and-design`) at the scope. Otherwise, separate `architecture.md` (boundary-only per Rule 1) and per-child `<child>/detailed_design.md`.

**Combined shape.** Standard architecture sections (Structure Diagram, Decomposition, Composition, Quality Attributes) plus a *Detailed Design* section per child carrying the standard DD shape (Public Interface, Data Structures, Algorithms, State, Error Handling).

**Sticky decision.** Set at scope-authoring time. Flipping later is a rewrite, not a refactor.

---

## Rule 3 — Rationale as citation

When a decision is captured in an ADR, `rationale` is one line plus ADR citation. No re-narration of the ADR's *Decision* or *Rationale*.

**Format.**

```yaml
rationale: "Stable iteration order required for byte-deterministic output; see ADR-001."
```

**Smell.** Multi-paragraph rationale that does not cite an ADR usually hides a sub-decision that should be its own ADR. When no ADR governs and the rationale exceeds one sentence, ask whether this is a real decision needing its own ADR.

---

## Rule 4 — Diagram-or-prose, not both

A sequence diagram and an interface entry that state the same call flow are duplication. Pick one per interaction.

- **Diagram** when interaction has temporal ordering, multiple participants, async edges, or fan-out / fan-in.
- **Interface entry** when the boundary is a single call with DbC-shaped contract.

**Test.** Delete the diagram — is the interface entry still complete? If yes, the diagram is redundant.

**Borderline.** A multi-step interaction across child A → B → C with state observable across the chain warrants a diagram. The per-call contracts the diagram references should NOT also re-narrate the call sequence.

---

## Rule 5 — Cite, don't restate

Refer to upstream content (REQ, ADR, IC, ARCH-path) by ID with at most one summary line. Do not re-state upstream content verbatim. Reader follows the citation if full text is needed.

**Replace.**

```
"REQ-025 (the system shall produce a self-contained HTML report containing
verdict, findings, and traceability summary, with deterministic ordering...)..."
```

**With.**

```
"REQ-025"   — or, when orientation is genuinely needed —   "REQ-025 (HTML report shape)"
```

**Tell.** Same upstream ID restated verbatim in 3+ places = paying for the upstream content N+1 times.

---

## Review enforcement

| Rule | Check ID | Severity |
|---|---|---|
| 0 | `check.discipline.product-shape` | soft_reject |
| 1 | `check.discipline.dd-leakage-into-architecture` | soft_reject |
| 2 | `check.discipline.collapse-eligibility-misapplied` | info |
| 3 | `check.discipline.rationale-narration` | soft_reject |
| 4 | `check.discipline.diagram-prose-duplication` | soft_reject |
| 5 | `check.discipline.upstream-restatement` | soft_reject |

---

## Distribution

This file is the maintainer source of truth. Skills do not reference it directly — they ship a verbatim copy at `references/authoring-discipline.md`. Affected skills (10): `vmodel-skill-author-{requirements, architecture, detailed-design, testspec, adr}` and `vmodel-skill-review-{requirements, architecture, detailed-design, testspec, adr}`. Sync via `scripts/sync-authoring-discipline.sh` (TBD; manual propagation until built).
