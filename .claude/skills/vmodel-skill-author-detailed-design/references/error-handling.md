# Error handling

Specify error behaviour for every error class the leaf can produce or encounter.

## Contents

- [The six questions per error class](#the-six-questions-per-error-class)
- [The five-column matrix](#the-five-column-matrix)
- [The five recovery strategies](#the-five-recovery-strategies)
- [Checked vs unchecked vs result-type](#checked-vs-unchecked-vs-result-type--pick-per-error-class)
- [Translate at the boundary — no exception tunneling](#translate-at-the-boundary--no-exception-tunneling)
- [State after error — answer one of six](#state-after-error--answer-one-of-six)
- [Domain vs infrastructure errors](#domain-vs-infrastructure-errors--keep-separate)

## The six questions per error class

For every error class, the DD answers:

| # | Question |
|---|---|
| 1 | What can fail? |
| 2 | How is it detected? |
| 3 | How does it propagate, or where is it contained? |
| 4 | What is the recovery strategy? |
| 5 | What state is the leaf left in afterwards? |
| 6 | What does the caller receive? |

A DD that answers fewer than six is half-specified on that class.

## The five-column matrix

Render the answers as one row per error class:

| Error | Detection | Containment | Recovery | Caller receives |
|---|---|---|---|---|
| Invalid input range | Precondition check | Reject at boundary | None (caller bug) | `IllegalArgumentException` |
| DB timeout | Pool timeout (2s) | Circuit breaker | Retry twice; fall back to cache | Stale value with staleness flag |
| Row claimed by other | `SKIP LOCKED` empty | Local | Proceed to next poll | `null` (no-op) |

Slot-fill: `templates/error-matrix-row.yaml.tmpl`. Schema: `$defs/error_matrix_row`.

The "state after error" answer is implicit in the *recovery* column for stateless leaves; for stateful leaves, add a sixth column or per-row note. Cross-link: `state-and-concurrency.md`.

## Recovery strategies — closed enum

Every row picks exactly one. Silence is not legal.

| Strategy | When appropriate |
|---|---|
| **fail-fast** | Detect at boundary; raise / return error / signal safe state |
| **retry** (bounded) | Transient downstream; idempotent supplier; **bound mandatory** (max attempts, backoff, jitter, idempotency assumption) |
| **fallback** | Alternate path with degradation visible to caller |
| **compensate** | Undo partial work; restore consistent state; bounded time |
| **propagate** | Translate at the boundary into a domain error and re-raise |

Unbounded retry → finding `check.error.unbounded-retry`. Recovery strategy missing on a row → finding `check.error.recovery-not-named`.

## Checked vs unchecked vs result-type — pick per error class

| Form | Contract |
|---|---|
| Checked exception / `Result<T, E>` with `E` in type | Caller MUST handle; recovery is part of the interface |
| Unchecked exception / panic | Programming error; caller has a bug; no recovery expected |
| Sentinel value (`null`, `-1`, empty) | Degenerate result; type system does not force the check (state explicitly) |
| Optional / Maybe | Normal absence, not an error |

Mixing forms for the same error class → finding `check.error.inconsistent-form`.

## Translate at the boundary — no exception tunneling

When the leaf calls a downstream library / service that raises its own typed errors → the leaf's contract translates them at its boundary.

| Pattern | Caller of the leaf sees |
|---|---|
| Translate (wrap) | Domain error type only; lower-layer detail in cause/diagnostics |
| Drop and log | Domain error; original lost |
| Carry as cause | Wrapped domain error with original referenced |

`throws SQLException` on a business-logic function → finding `anti-pattern.exception-tunneling`.

## State after error — answer one of six

| State after error | Meaning |
|---|---|
| **No mutation** | Atomic operation; pre-call state preserved byte-for-byte |
| **Bounded mutation** | Specific subset mutated; bound named explicitly |
| **Compensated** | Partial mutation undone; observable state matches pre-call after compensation |
| **Quarantined** | Leaf in fault state; rejects calls until reset |
| **Best-effort cleanup** | Compensation attempted; residual bounded by named time/scope |
| **Undefined** | **Not legitimate** — Spec Ambiguity Test fails (refusal D) |

## Domain vs infrastructure errors — keep separate

| Class | Examples | Typical recovery |
|---|---|---|
| Domain | invalid range, cart empty, insufficient stock | fail-fast |
| Infrastructure | DB timeout, connection refused, OOM | retry / circuit-break / fallback |

Mixing them in a single error type → finding `check.error.mixed-domain-infrastructure`.

## Side effects on the failure path

When the failure path produces side effects (logged event, partial reservation released by sweep, audit record) → state them in the matrix's *containment* / *recovery* column. The TestSpec verifies side effects fire on the failure path, not just success.

## Exception swallowing — caller MUST be informed

Recovery strategy "log and continue" with no domain action → finding `anti-pattern.exception-swallowing`. If the operation did not succeed, the caller must know.

## Cross-link

`function-contracts.md` (postconditions split by outcome) · `state-and-concurrency.md` (undefined events as error class) · `testspec-traceability-cues.md` (matrix → robustness tests) · `anti-patterns.md` · schema `$defs/error_matrix_row`
