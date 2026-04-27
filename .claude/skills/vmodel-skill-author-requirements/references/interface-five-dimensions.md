# Interface requirements — five dimensions

Interface requirements are the single most common omission in requirements audits, and the most common failure mode is **syntax without semantics** — a function signature or JSON schema with no statement of what actually happens.

Every interface requirement covers all five dimensions. Plus pre-/post-conditions and invariants per externally callable operation. Plus a versioning policy.

## The five dimensions

| # | Dimension | What goes here |
|---|---|---|
| 1 | **Protocol** | Communication standard and version (HTTP/1.1, gRPC, AMQP 0.9.1, OIDC 1.0, TLS 1.3, OAuth grant type). Externally imposed → legitimately named here. |
| 2 | **Message structure** | Fields, types, units, ranges, resolutions, defaults, optionality. Request/response schemas; queue payloads; read/write contracts. |
| 3 | **Timing** | Latency budget, rate limits, retry expectations, heartbeat intervals. Timing is part of the contract, not a separate NFR. |
| 4 | **Error handling** | What the interface does on call failure, timeout, unexpected data, rate-limit hit. Including which errors are retryable, with what back-off, to what failure threshold. |
| 5 | **Startup / initial state** | What the interface does before it has been established — cold start, connection lost, first request after restart. Silently-omitted-here issues surface in production incidents. |

## Slot-fill template

```yaml
interface_requirement:
  id: REQ-NNN
  type: interface
  operation: <name and method, e.g. "POST /sessions/{id}/invalidate">

  protocol: |
    <wire protocol + version + transport security; cite RFC/spec where applicable>

  message_structure:
    request:
      - field: <name>, <required|optional>, <type>, <constraints>
      # ...
    response_2xx: [...]
    response_4xx: [...]
    response_5xx: [...]

  timing: |
    <latency target>, <rate limit>, <timeout>, <retry expectations>

  error_handling: |
    <what happens on each failure mode>

  startup_initial_state: |
    <cold-start behaviour; readiness signal; first-request-after-restart>

  precondition:
    - <what the caller must guarantee>

  postcondition_on_success:
    - <what the system guarantees if preconditions hold>

  postcondition_on_error:
    - <what the system guarantees on each error response>

  invariants:
    - <conditions true before and after, always>

  versioning: |
    <version label, compatibility regime, deprecation policy>

  rationale: |
    <why this contract>

  derived_from: [<upstream needs>]
```

## Worked example

```yaml
REQ-020:
  type: interface
  operation: "POST /sessions/{id}/invalidate"

  protocol: |
    HTTP/1.1 over TLS 1.3. API version v1. Request and response bodies are
    application/json.

  message_structure:
    request:
      - id: required, string, matches /^[A-Za-z0-9_-]{16,64}$/
    response_200:
      - body: empty
    response_404:
      - body: { reason: string, in [not_found, already_invalidated] }
    response_401:
      - body: { reason: 'unauthorised' }

  timing: |
    Response within 200 ms at p95 under normal load. Server-side timeout 1 s
    (returns 504 if exceeded).

  error_handling: |
    On downstream store unavailability, the service shall retry the internal
    operation up to 2 times with 50 ms back-off, then fail with 503 and header
    'Retry-After: 1'.

  startup_initial_state: |
    On cold start before the backing store is reachable, the service shall
    respond 503 to all requests with body { ready: false, reason: 'warming' }
    and shall fail the '/health/ready' probe until the store has been
    reachable for 10 consecutive seconds.

  precondition:
    - "Authenticated caller holds role 'session-admin' OR owns the target session."
    - "Session {id} exists and is in state ACTIVE or IDLE."

  postcondition_on_success:
    - "Session {id} is in state INVALIDATED."
    - "Subsequent calls to validate this session-id return 401 reason 'invalidated'."
    - "An invalidation audit event has been appended to the session history record."

  postcondition_on_error:
    - "404: session {id} does not exist OR is already INVALIDATED. No state changes."

  invariants:
    - "Operation is idempotent; calling it on an already-INVALIDATED session is
       a 404 with no state mutation, never a 5xx."
    - "No response discloses whether the caller would have been authorised had
       the session existed (prevents session enumeration)."

  versioning: |
    Additive-only changes within v1 (new enum values require client handling).
    Breaking changes increment the major version. v1 remains available for
    minimum 12 months after v2 is announced.

  rationale: |
    Idempotency supports retry under network failure. Enumeration prevention
    is a security requirement; without it, an attacker can probe for valid
    session-ids by 401-vs-404 differential.

  derived_from: [<parent_requirement_id>, <governing_decision_id>]
```

## Design by Contract at the requirements layer

For each externally callable operation, the interface requirement states:

- **Preconditions** — what the caller must guarantee
- **Postconditions** — what the system guarantees if preconditions hold (success and error variants)
- **Invariants** — conditions true before and after, always

This is the requirements-layer form of Design by Contract. Each precondition branch is a test-case class; each postcondition is an assertion; each invariant is a property to fuzz or cross-check.

## Versioning is a first-class element

An interface that is not versioned has silently committed to never-changing — which is a commitment the system cannot keep. Every interface requirement names:

- **Version label** — v1, 2026-04, semver, etc.
- **Compatibility regime** — semver, date-based, additive-only-within-major
- **Deprecation policy** — how long old versions remain available; how callers are notified

Teams that omit versioning discover, at the first breaking change, that there was no written rule for how to change the interface, and every caller's migration story is improvised.
