# Architecture traceability checks (TestSpec ↔ parent Architecture seam, branch and root)

When the TestSpec is non-leaf (branch OR root), walk the parent Architecture's Composition section and interface contracts and verify each load-bearing element has at least one corresponding case. **Position C: Architecture Composition is a verification target at both branch and root** (per TARGET_ARCHITECTURE §5.3 "Verification targets per scope"). Conditional gating: branch AND root scope.

## check.architecture-traceability.interface-uncovered (soft)

**Check that** every interface entry in the parent Architecture has at least one integration case in this TestSpec — `type: contract` (or `type: functional` integration-flavoured).

**Reject when** a parent-Architecture interface has no integration case `verifies` resolving to it.

**Approve when** every interface maps to ≥ 1 integration case.

**Evidence pattern:** name the parent-Architecture interface; note absence of any case `verifies` resolving to it.

**recommended_action:** *"Derive an integration case per parent-Architecture interface. Interfaces with Design-by-Contract clauses (preconditions, postconditions, invariants) demand contract cases."*

## check.architecture-traceability.composition-invariant-uncovered (soft)

**Check that** every composition invariant in the parent Architecture's Composition section has at least one cross-child integration case in this TestSpec.

**Reject when** a parent-Architecture composition invariant has no integration case `verifies` resolving to it.

**Approve when** every composition invariant maps to ≥ 1 cross-child case.

**Evidence pattern:** name the composition invariant (or runtime-pattern element it belongs to); note absence.

**recommended_action:** *"Derive a cross-child integration case per composition invariant. Composition invariants describe properties that emerge from the runtime pattern; they live at branch only."*

## check.derivation.error-path-uncovered (soft, typed-error widening)

**Check that** every code in a parent-Architecture interface's `errors:` enum (i.e. every `ARCH.interfaces.<name>.errors.<code>` id) has at least one case in this TestSpec under the `error` or `fault-injection` strategy whose `verifies:` resolves to that id.

**Reject when** any typed-error code lacks a covering case. The review must enumerate **every** uncovered code, not just the first detected — emit one finding per uncovered code so the matched author skill can act on the full set in a single pass.

**Approve when** every typed-error code has ≥ 1 covering case.

**Evidence pattern:** for each uncovered code, name the parent-Architecture interface, the code, and the `ARCH.interfaces.<name>.errors.<code>` id; confirm no case lists that id in `verifies:`.

**recommended_action:** *"Derive an error or fault-injection case per typed-error code. Cover every code in the enum, not just the most visible failure path."*

**Cross-link:** `${paths.scripts}/check-typed-error-coverage.py` rule `testspec.typed-error-uncovered` mechanically detects uncovered codes; the review skill aggregates one finding per code under this check ID.

## check.architecture-traceability.quality-attribute-unallocated (soft)

**Check that** every quality-attribute allocation to a child or interface in the parent Architecture has at least one specialised case at branch — `type: performance` / `security` / `accessibility` / etc.

**Reject when** a parent-Architecture QA allocation (e.g. *"latency budget 200 ms allocated to component X"*) has no specialised case in this TestSpec.

**Approve when** every QA allocation maps to ≥ 1 specialised case at branch.

**Evidence pattern:** name the QA allocation and its parent-Architecture target; note absence.

**recommended_action:** *"Derive a specialised case per QA allocation. The matched author skill's architecture-traceability reference covers seam derivation."*

## Cross-link

`derivation-strategy-checks.md` (per-strategy coverage) · `verifies-traceability-checks.md` (granularity per layer) · `integration-and-system-checks.md` (contract-testing presence) · `quality-bar-gate.md` (Architecture-traceability card) · `dd-traceability-checks.md` (sibling seam at leaf) · `requirements-traceability-checks.md` (sibling seam at root)
