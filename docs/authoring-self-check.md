---
purpose: Cross-cutting workflow discipline. Author skills instantiate a Pre-publish mechanical self-check terminal step that runs skill-specific scripts before the Quality Bar gate.
audience: author skills, framework maintainers
status: active (Phase 6, Cluster 3)
applies_to: all 5 author skills for the 6-artifact set (excl. product-brief, deferred)
source_of_truth: this file. Per-skill instantiation lives in each author skill's SKILL.md.
---

# Authoring Self-Check

Every author skill terminates with a **Pre-publish mechanical self-check** step inserted between the existing *Anti-pattern self-check* and the existing *Quality Bar checklist + Spec Ambiguity Test* steps. The step runs zero or more skill-specific scripts under `scripts/check-*.py`, addresses each finding before the QB step, and never silently skips a finding.

`authoring-discipline.md` covers content discipline (what the artifact may and may not contain). This file covers workflow discipline (mechanical gates the author runs before declaring done). The two are siblings, not nested.

---

## Why the step exists

Review skills are expensive. Empirical signal from Phase 6 Issue 22: a single architecture review session ran ~100k tokens. Mechanically-detectable defects (regex matches, YAML cross-references, enumeration coverage) caught at review-time are pure rework — the author already absorbed the cost of producing them, and the reviewer is now paying again to point them out.

Shifting these checks left to author-time keeps the right gate at the cheaper site. Review remains the safety net for craft and intent — belt-and-braces, not belt-or-braces. The cheap-mechanical findings are filtered out before review burns tokens on them.

The step is mechanical by design. No script in this category invokes an LLM. If a check needs interpretive judgment, it belongs in review, not here.

---

## Per-skill instantiation

| Skill | Scripts | What they check |
|---|---|---|
| `vmodel-skill-author-requirements` | `scripts/check-requirement-shape.py` | Atomicity, EARS shape, implementation-prescription heuristic |
| `vmodel-skill-author-adr` | `scripts/check-requirement-shape.py` (only when route (a) materialises a new requirement) | Same as requirements |
| `vmodel-skill-author-architecture` | `scripts/check-mermaid.py`, `scripts/check-adr-landing.py`, `scripts/check-requirement-shape.py` | Diagram syntax; ADR-bound binding placement; derived-requirement shape |
| `vmodel-skill-author-testspec` | `scripts/check-typed-error-coverage.py`, `scripts/check-implicit-verifies.py` | Typed-error enum coverage from parent architecture; implicit-verifies citation completeness |
| `vmodel-skill-author-detailed-design` | `scripts/check-mermaid.py` | State diagram syntax |

A skill with no scripts in this list still runs the step — the step degrades to a no-op but the structural slot is preserved so future scripts can be added without re-shaping the skill.

---

## Script contract

Every check script obeys this contract. Skills assume nothing beyond it.

**Invocation.**

```
./scripts/check-NAME.py <specs-root>
```

Single positional argument: the root of the spec tree to scan. No flags, no environment dependencies beyond a Python interpreter on `PATH`.

**Stdout.** Zero or more findings, one per line, in the format:

```
<file>:<line>:<rule-id>:<message>
```

Greppable. CI-friendly. Empty stdout when there are no findings.

**Exit codes.**

| Code | Meaning |
|---|---|
| 0 | Clean — no findings |
| 1 | Findings — at least one finding written to stdout |
| 2 | Script error — parse failure, missing input, internal exception |

Exit 2 is distinct from exit 1: the author cannot conclude the artifact is clean from a script that crashed.

**Determinism.** Same input → same output. No timestamps, no random ordering, no network access.

---

## Author-side response protocol

For every finding the script reports, the author chooses exactly one path:

1. **Fix the artifact** — default. The finding names a real defect; resolve it and re-run the script.
2. **Record a defended exception** — rare. The finding is a false positive for this case. The author writes an inline rationale next to the offending content (or in a `mechanical_check_exceptions:` block in the artifact's front-matter when inline placement would damage shape) and proceeds. Exceptions accumulate as review signal — a pattern of repeated exceptions for the same rule is a script-quality complaint, not a craft complaint.
3. **Escalate** — the script appears wrong. The author halts, surfaces the apparent bug, and does not silently work around it.

**Never silently ignored.** A finding that the author neither fixes nor explicitly defends nor escalates is a discipline violation, not a judgement call.

---

## Step ordering inside the author skill

```
... (artifact body authored) ...
N-2: Anti-pattern self-check          (existing)
N-1: Pre-publish mechanical self-check  (this step)
N:   Quality Bar checklist + Spec Ambiguity Test  (existing)
```

The mechanical step runs after anti-pattern judgment so the author is not double-touching the same content. It runs before the QB step so QB-time energy is spent on craft questions the script cannot answer, not on regex-grade defects the script already flagged.

---

## Distribution

This file is the maintainer source of truth. Per-skill instantiation lives in each author skill's `SKILL.md` as a numbered step that names the scripts it runs and links back here for the contract. The script implementations live in `scripts/` at the repo root, sharable across skills.
