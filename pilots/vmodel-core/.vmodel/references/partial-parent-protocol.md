---
purpose: Cross-cutting protocol for authoring an artifact when its canonical upstream is fully or partially missing. Author skills follow; review skills accept documented deviations and reject silent inventions.
audience: author skills (5 author pairs), review skills, framework maintainers
status: active (Phase 6, Cluster 4)
applies_to: vmodel-skill-author-{requirements,architecture,detailed-design,testspec,adr}
source_of_truth: this file. Per-skill copies at `references/partial-parent-protocol.md` are verbatim. Sync via `scripts/sync-partial-parent-protocol.sh`.
---

# Partial-parent / no-canonical-upstream protocol

Author skills are sometimes invoked at a scope where the canonical upstream artifact does not exist yet. This protocol pins three permitted paths and forbids silent invention.

## When this protocol fires

The protocol fires whenever **at least one canonical upstream is missing or pre-canonical**. Two trigger conditions:

- **Full absence.** No canonical upstream exists at all. Examples:
  - Authoring root Requirements when no root product (PB / needs / PD) exists.
  - Authoring leaf Detailed Design when the parent Architecture has not been authored.
  - Authoring branch Architecture when the branch Requirements has not been authored.

- **Partial absence.** The artifact has multiple canonical parents and at least one is missing. Example:
  - Authoring root TestSpec which canonically derives from root product (PB / needs / PD) + root Requirements + root Architecture, when only Requirements + Architecture exist.

A pre-canonical artifact (e.g., `needs.md` from elicit-needs) is **not** a canonical upstream. Citing it as `derived_from` triggers this protocol — the gap is real, the pre-canonical artifact is the workaround, and the resolution path is named below.

## The three permitted paths

Pick **explicitly**. Document the choice in the artifact's *Overview* (1–2 sentences). Silent choice is a violation.

### (a) HALT

Request the missing canonical upstream be authored first.

**Default for greenfield once the framework is mature.** Use this when:
- The missing upstream is reachable (stakeholder available, parent author available, no structural deferral).
- The missing upstream is not blocked on a framework-level decision.
- The cost of waiting is lower than the cost of authoring on a degraded basis.

The skill returns a structured halt: what is missing, who needs to author it, what entry-point skill they should invoke.

### (b) Author from next-best-available parent + documented deviation

Allowed when:
1. The upstream gap is **structurally deferred** (a framework-level decision is unresolved, a stakeholder is unavailable, the canonical author is blocked).
2. The stakeholder **explicitly accepts** the orphan posture for this authoring run.
3. A next-best parent **does** exist (this path is unavailable when *all* canonical parents are absent).

Operational rules under path (b):

- **`level:` follows scope position.** Root scope → `level: system`; branch → `level: integration`; leaf → `level: unit`. The level does NOT shift just because a parent is missing.
- **Case shape (TestSpec) follows the *actual* parent type, not the canonical one.** If branch TestSpec is authored from Architecture only because Requirements is missing, cases carry branch-Architecture shape (fixtures-rich preconditions, interface DbC oracle), not requirements shape.
- **The *Overview* names the deviation.** One short paragraph: which canonical parent is missing, why (cite the deferral), what was used in its place.
- **An *Open follow-ups* entry owns "replacement on canonical-parent authoring".** Title, owner, action, citation. The follow-up commits to revisiting this artifact when the missing canonical parent lands.
- **`derived_from` cites the next-best parent that exists.** Do not cite the missing parent; do not invent a placeholder id.

### (c) Cite a framework reference as upstream

Permissible only when the framework reference is itself a **canonical artifact in the framework's own scope tree**. This is rare. Most framework references (this protocol, the authoring-discipline doc, TARGET_ARCHITECTURE) are documentation, not artifacts, and so do not qualify.

If a framework artifact does qualify (the framework spec tree's own root Product Brief, for instance), cite by id and document the rationale — same shape as (b).

## Hard violations

These are **refusal-grade** failures, not soft-rejects:

- **Silently inventing an upstream id** (e.g., `derived_from: PB-FAKE` to satisfy schema validation without naming a real artifact).
- **Bypassing the schema's non-empty-`derived_from` requirement** by leaving the field empty or commented.
- **Fabricating a placeholder id without documented rationale** in *Overview* and *Open follow-ups*.
- **Refusing to choose** — emitting an artifact under partial-parent conditions without explicit path declaration in *Overview*.

A documented placeholder citation (e.g., `derived_from: NEEDS-vmodel-core` with the deferral explained in *Overview* and a follow-up tracking resolution) is **not** a violation. The fabrication test is "did the author put in the work to name the gap and own it" vs. "did the author paper over the schema check".

## Cross-skill consistency

The same rule applies to every author skill:

| Skill | Most common partial-parent case |
|---|---|
| author-requirements | Root requirements with no root product (PB / needs / PD); branch requirements with no parent requirements |
| author-architecture | Branch architecture with no parent requirements; root architecture with no root product (PB / needs / PD) |
| author-detailed-design | Leaf DD with no parent Architecture |
| author-testspec | Root TestSpec with root product absent; leaf TestSpec with DD absent |
| author-adr | ADR scope-tagged at a scope where Architecture has not been authored |

Path choices and *Overview* documentation are uniform across all five.

## Pre-publish self-check

Before declaring the artifact complete, verify:

1. *Overview* explicitly names path (a), (b), or (c) when the protocol fired (or "(canonical parent present)" when it did not).
2. `derived_from` cites only existing, resolvable artifact ids — no placeholders, no missing-parent ids, no fabrications.
3. Under path (b): the *Open follow-ups* section carries the canonical-parent-replacement entry.
4. Under path (b) for TestSpec: declared `level:` matches scope position; case shape matches the actual parent.
5. No silent path: if the protocol fired and no path is declared, you are in violation — pick one and document.

## Mapping to architectural record

The architectural record for this protocol lives at `TARGET_ARCHITECTURE.md §5.7`. The text above is the operational text shipped to skills via `scripts/sync-partial-parent-protocol.sh`. The two are kept in sync by sync-script discipline; in case of any apparent drift, this file (the canonical) is authoritative for skill runtime; TARGET §5.7 is authoritative for architectural intent.
