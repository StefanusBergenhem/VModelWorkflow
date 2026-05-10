# TestSpec traceability checks (DD ↔ TestSpec seam)

Mirrors `testspec-traceability-cues.md` on the author side. Not a hard-reject area; checks here are soft + info.

## check.traceability.error-row-not-tested (soft)

**Check that** every error-matrix row has a corresponding test target identified — either a sibling-TestSpec robustness id OR a `[NEEDS-TEST: ...]` stub.

**Reject when** a matrix row has no `test_target` AND no stub.

**Approve when** every row points to a robustness target.

**recommended_action:** *"Tag each error-matrix row with a `test_target: [ROBUSTNESS-TEST]` or a `[NEEDS-TEST: ...]` stub. Every row corresponds to a sibling TestSpec robustness row."*

## check.traceability.postcondition-without-test-target (soft)

**Check that** every load-bearing postcondition (`on_success` / `on_failure`) identifies a test target.

**Reject when** a postcondition has no test_target identification.

**Approve when** every load-bearing postcondition points to a contract / robustness target.

**recommended_action:** *"Tag each postcondition with a test target. Postconditions without targets cannot be verified."*

## check.traceability.invariant-without-property-test-target (soft)

**Check that** every load-bearing invariant (function, data structure, state) identifies a property-test target.

**Reject when** an invariant has no test_target.

**Approve when** every load-bearing invariant points to a property-test target.

**recommended_action:** *"Tag each invariant with `test_target: [PROPERTY-TEST]`. Invariants without targets are undocumented expectations."*

## check.traceability.test-target-undeliverable (soft)

**Check that** when a clause cannot identify a test target, it is either (a) a decorative restatement of type-system content (drop), OR (b) under-specified (the test engineer cannot derive a test → refusal D fails on that clause).

**Reject when** a clause has no test target AND is not decorative AND is not flagged for clarification.

**Approve when** every clause without a test target has been explicitly classified.

**recommended_action:** *"Either drop the decorative clause, OR add specificity until a test is derivable, OR flag with `[NEEDS-CLARIFICATION: <what>]` and HALT."*

## check.traceability.needs-test-stub-in-finalised (soft)

**Check that** no `[NEEDS-TEST: ...]` stubs remain in a finalised artifact (`status: active`).

**Reject when** the artifact is finalised but stubs remain.

**Approve when** the artifact is `draft` (stubs allowed) OR every stub has been resolved.

**recommended_action:** *"Resolve every `[NEEDS-TEST: ...]` stub before finalising. The TestSpec author skill consumes the seam; an unresolved stub blocks downstream test derivation."*

## check.traceability.test-without-dd-row (info)

**Check that** sibling-TestSpec robustness rows (when the TestSpec is supplied alongside) correspond to error-matrix rows in this DD.

**Reject (info)** when the TestSpec has a robustness row whose corresponding error-matrix row is absent in this DD.

**Approve when** every TestSpec robustness row has a DD error-matrix counterpart.

**recommended_action:** *"Surface as info: the DD may be incomplete on this error class. Do NOT retro-fit the matrix to match the test (anti-pattern.test-as-spec-inversion). The TestSpec is downstream; the DD is upstream."*

## Cross-link

`error-handling-checks.md` (matrix → robustness) · `function-contract-checks.md` (postconditions → contract tests) · `quality-bar-gate.md` (TestSpec traceability card) · `anti-pattern.test-as-spec-inversion`
