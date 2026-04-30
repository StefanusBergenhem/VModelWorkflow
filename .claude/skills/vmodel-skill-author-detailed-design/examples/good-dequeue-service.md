# Example — DD for the dequeue service (greenfield, all 7 sections)

A leaf inside `app/jobs`: the service that claims and releases work items in the Postgres-backed job queue. The parent Architecture (`ARCH-app-jobs`) decomposes the scope into two leaves (`dequeue-service` and `enqueue-service`); ADR-017 fixes the queue backing store and the `FOR UPDATE SKIP LOCKED` access pattern. The DD below realises the dequeue side.

## What this example demonstrates

- Every public function carries a complete contract (9 elements).
- Postconditions are split into `on_success` and `on_failure` and state result properties, not steps.
- The `Claim` data structure is specified by invariant, not field layout; ownership and lifetime are explicit.
- Algorithms section is short — the SQL is the contract because ADR-017 fixed the access pattern; otherwise the leaf would specify result properties and leave SQL choice to the implementer.
- State section is one line — the leaf is stateless between calls; the assertion is content.
- Error matrix has five rows; each row picks one of the five recovery strategies.
- Rationale is inline with the four constraint kinds named.

## The artifact

```markdown
---
id: DD-app-jobs-dequeue-service
artifact_type: detailed-design
scope: app/jobs/dequeue-service
parent_scope: app/jobs
parent_architecture: ARCH-app-jobs
derived_from:
  - REQ-app-jobs-004
  - REQ-app-jobs-007
governing_adrs:
  - ADR-017-job-queue-backing-store
status: draft
date: 2026-04-30
---

# Detailed Design — dequeue-service

## Overview

The dequeue-service drains the Postgres-backed `app.jobs` queue and hands claimed
work to the worker's execution loop. It is one of two leaves in `app/jobs`; the
sibling leaf is the enqueue-service.

The leaf's posture is a thin shell over a single SQL statement that uses
`FOR UPDATE SKIP LOCKED` so N workers can poll the same queue without blocking
one another (per ADR-017). The leaf is stateless between calls; all state lives
in the `app.jobs` table. The leaf does not buffer claimed rows in process; one
call returns at most one Claim, and the worker is responsible for the polling
cadence.

## Public Interface

\```yaml
public_interface:
  - name: claimJob
    signature: "claimJob(workerId: WorkerId, visibilityTimeout: Duration) -> Claim?"
    description: "Atomically claim the oldest available job; return null on empty queue."
    preconditions:
      - "workerId is registered in app.workers"
      - "the calling process holds no outstanding Claim it has not yet released"
      - "visibilityTimeout in [1s, 15min]"
    postconditions:
      on_success:
        - "Returned Claim has row_id not held by any other worker; expires_at = now() + visibilityTimeout"
        - "Underlying row's locked_until is advanced to expires_at within the same transaction"
        - "On empty queue, returns null with no row mutation"
      on_failure:
        - "On precondition violation: IllegalArgumentException; no row mutation"
        - "On QueueUnavailable: no row mutation; circuit breaker open for 30s"
    invariants:
      - "Concurrent calls from different workers never observe the same row"
      - "Returned Claim's expires_at is strictly in the future at construction time"
    errors:
      - error: "IllegalArgumentException"
        raised_when: "visibilityTimeout outside [1s, 15min] OR workerId not registered"
        meaning: "Caller bug — input outside contract"
      - error: "QueueUnavailable"
        raised_when: "Pool timeout (2s) followed by circuit-breaker open"
        meaning: "Underlying store unreachable; caller should pause polling"
    side_effects:
      - "Row-level lock acquired and released within the transaction"
      - "Update to app.jobs.locked_until on success"
    thread_safety: thread-safe
    nullability:
      - "workerId: must not be null"
      - "visibilityTimeout: must not be null"
      - "return: may be null — null means empty queue (no error)"
    complexity_notes: "O(log n) in queue depth (B-tree index lookup on (locked_until, enqueued_at))"

  - name: completeJob
    signature: "completeJob(claim: Claim) -> void"
    description: "Mark a claimed row as completed; remove it from app.jobs."
    preconditions:
      - "claim was returned by this process's claimJob and not yet completed or released"
      - "claim.expires_at > now()"
    postconditions:
      on_success:
        - "Row referenced by claim.row_id is removed from app.jobs"
        - "Subsequent calls with the same claim raise UnknownClaim (claim is consumed)"
      on_failure:
        - "On ClaimExpired: no row mutation; row is reassigned by the expiry sweep"
        - "On UnknownClaim: no row mutation"
    errors:
      - error: "ClaimExpired"
        raised_when: "claim.expires_at < now() at the moment of call"
        meaning: "Lease elapsed; the row is reassigned"
      - error: "UnknownClaim"
        raised_when: "Row was reassigned by the expiry sweep before completion"
        meaning: "Claim is no longer valid"
    side_effects:
      - "Row deletion from app.jobs"
    thread_safety: thread-safe
    nullability:
      - "claim: must not be null"
\```

## Data Structures

\```yaml
data_structures:
  - name: Claim
    description: "A worker's lease on a job row, immutable once constructed."
    fields:
      - { name: row_id,    type: "JobRowId",   invariant: "Non-null; references a row in app.jobs" }
      - { name: worker_id, type: "WorkerId",   invariant: "Matches the caller of claimJob" }
      - { name: expires_at, type: "UTC timestamp", invariant: "Strictly in the future when constructed" }
      - { name: payload,   type: "JsonValue",  invariant: "Verbatim copy of the row's payload column" }
    ownership: "Constructed by claimJob; held by the calling worker; never persisted in process"
    lifetime: "Valid until completeJob or releaseJob is called, or expires_at elapses"
    returned_semantics: "copy"
\```

## Algorithms

The dequeue is a single SQL statement executed inside a short transaction.
The algorithm is contractual (refer to ADR-017): the access pattern itself is
the contract — `FOR UPDATE SKIP LOCKED` is what makes N-worker polling correct.

\```sql
UPDATE app.jobs
SET locked_until = now() + $1, worker_id = $2
WHERE id = (
  SELECT id FROM app.jobs
  WHERE locked_until < now()
  ORDER BY enqueued_at
  FOR UPDATE SKIP LOCKED
  LIMIT 1
)
RETURNING id, payload, locked_until;
\```

Rationale: per ADR-017, the queue uses Postgres rather than a dedicated queue
service; the access pattern above is the load-bearing decision (constraint kind:
*architectural*). Empty result → caller polls; the leaf does not block.

## State

Stateless between calls. All state lives in `app.jobs`. Two workers interacting
through this leaf observe a consistent view via Postgres MVCC.

## Error Handling

| Error | Detection | Containment | Recovery | Caller receives |
|---|---|---|---|---|
| Invalid `visibilityTimeout` | Precondition check | Reject at boundary | None (caller bug) | `IllegalArgumentException` |
| `workerId` not registered | Precondition check | Reject at boundary | None (caller bug) | `IllegalArgumentException` |
| Empty queue | `SKIP LOCKED` returns empty | Local | Proceed to next poll cycle | `null` (no-op) |
| `ClaimExpired` on completeJob | `expires_at < now()` | Local | None; claim is invalid | `ClaimExpired` |
| Database timeout | Pool timeout (2s) | Circuit breaker | Retry once with 100ms backoff; then open breaker | `QueueUnavailable` |

The retry budget on database-timeout is bounded (one retry; per ADR-017 the
write is idempotent under the worker's claim). Open circuit holds for 30s
before half-open probe.

## Notes

- The leaf does not own claim-expiry sweep — that is a sibling leaf's job. This DD specifies only the claim-and-release path.
- TestSpec target — every error-matrix row has a robustness test target; both `claimJob` and `completeJob` postconditions have contract tests; the `Claim`-construction invariant has a property test.
```

## Why this DD passes the meta-gate

- **Junior-implementable.** A developer who has not seen the codebase can write `claimJob` and `completeJob` from this DD alone. The SQL is given; the contract on the response is specified; the error-matrix tells them which exceptions to raise and when.
- **Language-portable.** A Python or Go implementation could be produced from the same DD — only the SQL and the connection-pool API would change; the Claim invariants, the error semantics, and the thread-safety guarantees are language-neutral.
- **Test-derivable.** The TestSpec author can write: contract tests for both functions; robustness tests for each matrix row (force the timeout, force the empty queue, force the expiry); a property test asserting the `Claim` invariant. None of this requires reading the implementation.
