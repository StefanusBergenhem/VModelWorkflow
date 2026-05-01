# Error handling checks

Mirrors `error-handling.md` on the author side.

## Contents

- `check.error.matrix-missing` and `six-questions-unanswered` (matrix completeness)
- `check.error.recovery-not-named`, `unbounded-retry`, `state-after-error-undefined`
- `anti-pattern.exception-swallowing`, `anti-pattern.exception-tunneling`
- `check.error.inconsistent-form`, `mixed-domain-infrastructure`, `failure-side-effects-unstated`

## check.error.matrix-missing (soft)

**Check that** the Error Handling section has a five-column matrix (error / detection / containment / recovery / caller_receives).

**Reject when** the section is prose only, OR a partial table missing one or more columns.

**Approve when** the matrix is populated with one row per error class.

**recommended_action:** *"Render error handling as a five-column matrix. One row per error class."*

## check.error.six-questions-unanswered (soft)

**Check that** every error class answers all six questions: what / detection / containment / recovery / state-after-error / caller-receives.

**Reject when** a row has fewer than six answers (state-after-error implicit-OK for stateless leaves; otherwise must be stated).

**Approve when** all six are answered for every row.

**recommended_action:** *"Answer all six questions per error class. Half-specified error classes diverge across implementations."*

## check.error.recovery-not-named (soft)

**Check that** every matrix row picks one of the five recovery strategies (fail-fast / retry / fallback / compensate / propagate).

**Reject when** a row's recovery is unstated, OR is "log and continue" without a domain action, OR is "depends on context".

**Approve when** one of the five is named per row.

**recommended_action:** *"Name a recovery strategy per row. Silence is not legal; one of fail-fast / retry / fallback / compensate / propagate is required."*

## check.error.unbounded-retry (soft)

**Check that** retry-strategy rows have a bounded budget.

**Reject when** retry is named without max attempts, OR with "retry until success", OR without idempotency assumption.

**Approve when** max attempts, backoff, jitter, and idempotency assumption are stated.

**recommended_action:** *"Bound the retry: max attempts, backoff curve, jitter, and the idempotency assumption that makes retry safe."*

## check.error.state-after-error-undefined (soft)

**Check that** state-after-error is one of: no-mutation / bounded-mutation / compensated / quarantined / best-effort-cleanup.

**Reject when** the answer is "undefined" (the implementer chooses) — Spec Ambiguity Test fails on that row.

**Approve when** one of the five is named.

**recommended_action:** *"Name the state-after-error from the closed enum. 'Undefined' is not legitimate — a junior cannot test it."*

## anti-pattern.exception-swallowing (soft)

**Check that** recovery strategies do not swallow exceptions silently.

**Reject when** the recovery strategy is "log and continue" with no domain action AND the caller receives a success return when the operation materially did not succeed.

**Approve when** the failure is surfaced to the caller (typed error, sentinel, structured result).

**recommended_action:** *"Surface the failure to the caller. Logging is diagnostic, not recovery."*

## anti-pattern.exception-tunneling (soft)

**Check that** lower-layer exception types do not leak across the leaf's boundary.

**Reject when** the leaf's contract declares `throws SQLException` (or analogous low-layer infrastructure type) at its public interface.

**Approve when** lower-layer types are translated to a domain-level error type at the boundary.

**recommended_action:** *"Translate the lower-layer type to a domain error at the boundary. Carry the original as cause/diagnostic if needed."*

## check.error.inconsistent-form (soft)

**Check that** the error form (checked exception / unchecked / sentinel / Result type) is consistent within the leaf for the same error class.

**Reject when** the same error class is sometimes raised, sometimes returned as a sentinel, sometimes wrapped in `Result`, with no documented reason.

**Approve when** the form is consistent OR the inconsistency has a stated rationale.

**recommended_action:** *"Use one form per error class. Mixing confuses callers."*

## check.error.mixed-domain-infrastructure (soft)

**Check that** domain errors and infrastructure errors are not bundled into a single error type.

**Reject when** a single error type combines (e.g., `OrderError` carrying both "cart-empty" and "DB-timeout").

**Approve when** the two classes are separate types or distinguished by separate enum branches.

**recommended_action:** *"Separate domain and infrastructure errors. They have different recovery strategies; bundling them defeats branching."*

## check.error.failure-side-effects-unstated (info)

**Check that** when the failure path produces side effects (logged event, partial reservation released by sweep, audit record), they are stated.

**Reject when** failure-path side effects are observable in code but absent from the matrix.

**Approve when** they are stated in the containment / recovery column or per-row note.

**recommended_action:** *"Name the failure-path side effect in the matrix. The TestSpec must verify it fires."*

## Cross-link

`anti-patterns-catalog.md` · `quality-bar-gate.md` (Error handling card) · `testspec-traceability-checks.md` (matrix → robustness) · `templates/error-matrix-row.yaml.tmpl`
