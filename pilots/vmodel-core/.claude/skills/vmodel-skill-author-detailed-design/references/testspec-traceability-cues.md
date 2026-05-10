# TestSpec traceability cues (DD ↔ TestSpec seam)

The DD is the source of test derivation. Every contract clause maps to one or more test rows in the sibling TestSpec.

## Contents

- [The four mappings](#the-four-mappings)
- [Slot-fill: traceability cue per DD clause](#slot-fill-traceability-cue-per-dd-clause)
- [When the test target is missing](#when-the-test-target-is-missing)
- [The `[NEEDS-TEST: ...]` stub](#the-needs-test--stub)
- [The error-matrix → robustness-test mapping (closed correspondence)](#the-error-matrix--robustness-test-mapping-closed-correspondence)
- [The postcondition → contract-test mapping (one-to-many)](#the-postcondition--contract-test-mapping-one-to-many)
- [The invariant → property-test mapping](#the-invariant--property-test-mapping)
- [When the parent Architecture's interface invariant lands here](#when-the-parent-architectures-interface-invariant-lands-here)

## The four mappings

| DD element | TestSpec verification target |
|---|---|
| Postcondition `on_success` clause | Contract test (assert the property on a representative valid input) |
| Postcondition `on_failure` clause | Robustness / negative test (assert the typed error and state guarantee) |
| Function invariant | Property-based test (assert across a sampled input space) |
| Data structure invariant | Property-based test on the data type |
| Error matrix row | Robustness test (force the detection condition; assert containment, recovery, caller-receives) |
| State transition | State-based test (drive the source state, fire the event, assert target + side effects) |
| Undefined-event handling | Negative test (fire the event in a state where it is undefined; assert the chosen response) |

## Slot-fill: traceability cue per DD clause

When a DD clause is load-bearing → tag it inline so the TestSpec can pick it up:

```text
postcondition (on_success):
  - "<property statement>"
  test_target: "[CONTRACT-TEST]"

invariant:
  - "<invariant statement>"
  test_target: "[PROPERTY-TEST]"

error_matrix_row:
  - error: "<class>"
    detection: "<how>"
    recovery: <strategy>
    caller_receives: "<what>"
    test_target: "[ROBUSTNESS-TEST]"
```

The TestSpec author skill consumes these as derivation seeds; the DD does not have to enumerate test cases — only that each contract element has an identified target type.

## When the test target is missing

When the DD cannot identify a test target for a clause → the clause is either decoration (drop it) or under-specified (the test engineer cannot write a test → refusal D fails).

| Cause | Action |
|---|---|
| Clause is decorative (restates type-system content) | Drop the clause |
| Clause is under-specified (test engineer cannot derive a test) | Add specificity until a test is derivable, OR mark `[NEEDS-CLARIFICATION: <what>]` and HALT |
| Clause requires upstream input (e.g., parent ARCH interface invariant is itself ambiguous) | Surface as DESIGN_ISSUE upstream, not a DD-level fix |

## `[NEEDS-TEST: ...]` stub

When the DD identifies a test target but the TestSpec has not been authored → emit a stub at the corresponding test_target slot:

```text
test_target: "[NEEDS-TEST: contract test for ordering+permutation properties]"
```

The stub flags an unresolved seam. Finalising the DD does not require the TestSpec to exist; it requires every contract clause to have a target type identified.

## The error-matrix → robustness-test mapping (closed correspondence)

Every error-matrix row corresponds to exactly one robustness test row in the sibling TestSpec. The mapping is one-to-one:

```text
DD error_matrix:
  - error: "Database timeout"
    detection: "Pool timeout (2s)"
    containment: "Circuit breaker"
    recovery: retry (max 2; backoff)
    caller_receives: "QueueUnavailable"

TestSpec (derived row):
  - id: ROBUSTNESS-001
    fault: "Inject DB timeout via test fixture"
    expected_detection: "Pool timeout fires within 2s ± 100ms"
    expected_recovery: "Two retry attempts observed; then circuit opens"
    expected_caller_observation: "QueueUnavailable raised; cart state unchanged"
```

Missing TestSpec row for an existing error-matrix row → finding `check.traceability.error-row-not-tested`.

Missing error-matrix row for an existing TestSpec robustness row → finding `check.traceability.test-without-dd-row` (signals the DD is incomplete; do not retro-fit the matrix to the test).

## The postcondition → contract-test mapping (one-to-many)

A single postcondition may produce multiple contract tests (one per equivalence class of valid input). The DD does not enumerate the equivalence classes — that is the TestSpec's job — but the DD's clause must be specific enough that the TestSpec author can derive them.

| DD clause | TestSpec derives (typical) |
|---|---|
| "Returns ordered + permutation of input" | One test per: empty input, single-element, all-equal, already-sorted, reverse-sorted, random, with-duplicates |
| "Idempotent under same key within 24h" | Tests for: same call within 24h; same call after 24h; concurrent same-call |

## The invariant → property-test mapping

A function or data-structure invariant maps to a property test (sampled across the input space, or model-checked for small finite spaces).

```text
DD invariant: "Sum of line.line_total over Lines equals subtotal"

TestSpec (derived):
  - id: PROPERTY-001
    property: "for any Cart, sum(lines.line_total) == subtotal"
    sampling: "Hypothesis-style / quickcheck-style; 100 random Carts"
```

## When the parent Architecture's interface invariant lands here

When the parent ARCH interface invariant (e.g., "ordering preserved across calls") is realised by this leaf → re-state it in the DD's `invariants:` (so the test target lives at this leaf's TestSpec) AND cite the parent ARCH interface in the DD's rationale.

```text
invariants:
  - "Ordering of incoming events preserved in the published OrderPlaced sequence
     (realises ARCH-checkout/ICartFinaliseCheckout invariant on causal ordering)"
test_target: "[PROPERTY-TEST]"
```

## Cross-link

`function-contracts.md` (postconditions split by outcome) · `error-handling.md` (matrix rows) · `state-and-concurrency.md` (state-transition tests) · `quality-bar-checklist.md` (Spec Ambiguity Test asserts test-derivability)
