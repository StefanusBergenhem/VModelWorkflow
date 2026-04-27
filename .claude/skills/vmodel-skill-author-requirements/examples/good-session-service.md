---
id: REQS-session-service
scope: session-service
parent_scope: ecommerce-platform
derived_from:
  - REQS-ecommerce-platform
  - PB-ecommerce-platform
governing_decisions:
  - ADR-012  # token generation must use CSPRNG
  - ADR-018  # session-policy configuration is per-tenant
status: draft
date: 2026-04-26
---

# Requirements — session-service

This scope owns user authentication, session creation and validation, session-policy enforcement (idle timeout, absolute timeout, step-up for elevated operations), and integration with the identity provider and audit-log consumer.

Upstream input: parent-scope requirements REQS-ecommerce-platform §3 (authentication slice) plus governing decisions ADR-012 and ADR-018. Stakeholder needs traced to user stories US-42 and US-67.

## Glossary

```yaml
glossary:
  - term: "Session"
    definition: |
      A server-side record of an authenticated user's continuous interaction
      with the system, scoped to a single device and identified by an opaque
      session token. Created on successful authentication; destroyed on logout,
      idle timeout, or explicit invalidation.
    distinct_from: "Elevated session — has additionally completed step-up auth."
    model_refs: ["Session entity in the Identity bounded context"]

  - term: "Idle timeout"
    definition: |
      A session invariant: the maximum duration between the end of one
      authenticated request and the start of the next, before the session is
      destroyed.
    distinct_from: "Absolute timeout."

  - term: "Absolute timeout"
    definition: |
      A session invariant: the maximum duration from session creation to forced
      destruction, independent of activity.

  - term: "Elevated session"
    definition: |
      A session that has completed step-up authentication within the last N
      minutes, eligible to perform security-sensitive operations.

  - term: "Step-up authentication"
    definition: |
      A second authentication challenge (typically MFA or password re-entry)
      issued to a user with an active session, used to promote that session to
      elevated state.
```

## Inherited Constraints

```yaml
inherited_constraints:
  - id: IC-session-001
    source: "GDPR Article 17 (Right to erasure), Regulation (EU) 2016/679"
    summary: |
      Data subjects may request erasure of their personal data without undue
      delay, subject to Article 17(3) exceptions.
    category: regulatory
    cost_of_relaxing: |
      Data Processing Agreement breach with all EU customers, supervisory
      authority intervention, material fines up to 4% of global turnover.
    derived_requirements: [REQ-session-050, REQ-session-051, REQ-session-052]

  - id: IC-session-002
    source: "ADR-012 (token generation policy)"
    summary: |
      All session token generation must use a cryptographically secure
      pseudo-random number generator. Direct use of platform-default Random
      implementations is prohibited.
    category: technical
    cost_of_relaxing: |
      Re-opening the 2024 entropy audit finding; potential downgrade of
      platform security certification.
    derived_requirements: [REQ-session-001]
```

## Functional Requirements

```yaml
- id: REQ-session-001
  type: functional
  derivation: derived
  statement: |
    The session service shall use a cryptographically secure pseudo-random
    number generator for all session token generation.
  rationale: |
    Per ADR-012 (governing decision), the platform-wide policy following the
    2024 entropy audit. This requirement makes the policy testable at the
    session-service layer; without it, the constraint propagates as advice
    rather than as something tests can verify.
  derived_from: [IC-session-002, ADR-012]

- id: REQ-session-002
  type: functional
  statement: |
    When a user submits a valid credential pair, the session service shall
    create a new session, persist it in the ACTIVE state, and return the
    session token and its absolute-timeout expiry timestamp.
  rationale: |
    Foundational: every authenticated interaction needs a session. The
    absolute-timeout is returned to allow the caller to schedule re-auth
    proactively; alternatives considered (omit and require client to query)
    were rejected as adding a round-trip on the auth-success hot path.
  derived_from: [US-42, REQS-ecommerce-platform-§3.1]

- id: REQ-session-003
  type: functional
  statement: |
    While a session is in the IDLE state, the session service shall reject
    validation requests for that session with status 401 and reason
    'idle-timeout'.
  rationale: |
    Idle policy is a security boundary. 401 + machine-readable reason allows
    the client to differentiate idle from absolute timeout and offer the
    correct remediation (re-auth vs full re-login).
  derived_from: [US-42, ADR-018]

- id: REQ-session-004
  type: functional
  statement: |
    While a session is in the ACTIVE state and has had recorded authenticated
    activity within the last <idle_timeout> minutes (configured per-tenant per
    ADR-018), the session service shall keep the session in the ACTIVE state
    and shall extend the last-activity timestamp on each validation request
    whose purpose != 'read'.
  rationale: |
    Complement of REQ-session-003 (in-state behaviour). Limiting the activity
    extension to non-read purposes prevents background polling from indefinitely
    extending a session that the user is not actively driving.
  derived_from: [US-42, ADR-018]

- id: REQ-session-005
  type: functional
  statement: |
    If three consecutive credential-validation attempts for the same user
    account fail within 10 minutes, then the session service shall lock the
    account for 15 minutes and shall emit a 'credential-lockout' audit event
    containing the account identifier, the count of failures, and the
    triggering window's start and end timestamps.
  rationale: |
    Anti-bruteforce. The 3/10/15 numbers are derived from ADR-018's account-
    lockout policy; alternatives considered (5/15/30) were rejected for being
    weaker than the platform-wide auth-attack-mitigation policy.
  derived_from: [ADR-018, REQS-ecommerce-platform-§3.4]

- id: REQ-session-006
  type: functional
  statement: |
    Where the tenant has enabled multi-factor authentication, when a session
    requests a security-sensitive operation, the session service shall require
    step-up authentication before promoting the session to the ELEVATED state.
  rationale: |
    Step-up is the boundary between routine and security-sensitive actions.
    Per ADR-018, MFA-enabled tenants require step-up; non-MFA tenants do not
    have an elevation concept.
  derived_from: [US-67, ADR-018]
```

## Quality Attributes (NFRs)

```yaml
- id: REQ-session-015
  type: quality_attribute
  statement: |
    The session-validation endpoint shall respond in ≤ 50 ms at p95 under
    5,000 concurrent sessions in the production deployment, measured at the
    API gateway.
  rationale: |
    Validation runs on every authenticated request. The 50 ms p95 budget
    derives from REQS-ecommerce-platform's 400 ms end-to-end latency commitment
    at p95 and the 8 downstream operations sharing that budget (~45 ms each
    plus overhead). 50 ms leaves headroom for the slowest expected downstream.
  derived_from: [REQS-ecommerce-platform-§NFR-latency]

- id: REQ-session-016
  type: quality_attribute
  planguage:
    scale: "percentage of authenticated-user-facing requests completed within SLO"
    meter: "computed over 30-day rolling window, excluding planned maintenance windows declared at least 48 hours in advance via the status page"
    fail:    "< 99.5%"
    goal:    "≥ 99.9%"
    stretch: "≥ 99.95%"
    wish:    "99.99%"
  rationale: |
    Tiered availability — fail/goal/stretch/wish — captures the engineering
    trade-off explicitly. The platform's customer-facing SLA is 99.9%; we
    commit at goal and report stretch internally to drive resilience work.
  derived_from: [REQS-ecommerce-platform-§NFR-availability]
```

## Interface Requirements

```yaml
- id: REQ-session-020
  type: interface
  operation: "POST /sessions/validate"

  protocol: |
    HTTP/1.1 over TLS 1.3. API version v1. Request and response bodies are
    application/json.

  message_structure:
    request:
      - field: token, required, string, opaque session token, 64-128 chars
      - field: purpose, optional, enum { 'read', 'write', 'elevated' }, default 'read'
    response_200:
      - body: |
          {
            valid:          required, boolean,
            subject:        required-on-valid-true, string, stable user identifier,
            session_state:  required-on-valid-true, enum { ACTIVE, IDLE, ELEVATED },
            reason:         required-on-valid-false, enum { 'expired', 'invalidated',
                                                            'not-found', 'idle-timeout',
                                                            'absolute-timeout' }
          }
    response_401:
      - body: { reason: 'unauthorised' }
    response_503:
      - body: { ready: false, reason: 'warming' | 'degraded' }

  timing: |
    Response within 50 ms at p95 under normal load (see REQ-session-015).
    Server-side timeout 500 ms — requests lasting longer return 504.

  error_handling: |
    On downstream store unavailability, the service shall retry the internal
    read up to 2 times with 50 ms back-off, then fail with 503 and header
    'Retry-After: 1'. The service shall never silently return valid=false on
    infrastructure failure — that condition is 5xx, not 401.

  startup_initial_state: |
    On cold start before the backing store is reachable, the service shall
    respond 503 to all requests with body { ready: false, reason: 'warming' }
    and shall fail the '/health/ready' probe until the store has been reachable
    for 10 consecutive seconds.

  precondition:
    - "Caller holds valid API credentials (handled by gateway upstream)."

  postcondition_on_success:
    - "On 200 with valid=true, the session's last-activity timestamp has been
       updated iff purpose != 'read'."
    - "On 200 with valid=false, no state mutation has occurred."

  postcondition_on_error:
    - "503: no state changes."
    - "504: indeterminate; caller may retry."

  invariants:
    - "Response never discloses the subject on valid=false (prevents
       session-existence enumeration)."
    - "Idempotent for purpose='read' (no state mutation regardless of outcome)."

  versioning: |
    v1. Additive-only changes within v1 — new enum values require client
    handling. Breaking changes increment the major version. v1 remains
    available for minimum 12 months after v2 is announced.

  rationale: |
    Validation is on the hot path of every authenticated request. The contract
    optimises for: low latency (50 ms p95), no-enumeration security guarantee,
    explicit reason codes for client UX, and 5xx-vs-401 cleanliness so retry
    logic can distinguish 'system unhealthy' from 'session invalid'.
  derived_from: [REQ-session-002, REQ-session-003, REQ-session-015]
```

## Data Requirements

```yaml
- id: REQ-session-040
  type: data
  statement: |
    Session records shall retain the user's IP address for no more than 90 days
    from last activity, after which the IP field shall be cleared while the
    session history record itself is preserved with the IP redacted.
  rationale: |
    Per the platform-wide data retention policy (90 days for IP-class personal
    data) plus IC-session-001 (GDPR Article 17 commitments). Preserving the
    history record without the IP supports the audit-log legal-obligation
    exception (Article 17(3)(b)).
  derived_from: [IC-session-001, REQS-ecommerce-platform-§5.2]

- id: REQ-session-050
  type: data
  derivation: derived
  statement: |
    When an authenticated data subject submits an erasure request via the
    account-settings interface, the session service shall destroy all ACTIVE
    and IDLE sessions belonging to that subject and shall remove
    directly-identifying fields (user_id, email, ip_address, device_fingerprint)
    from all session history records for that subject within 7 calendar days
    of receiving the request.
  rationale: |
    GDPR Article 17(1) requires erasure without undue delay. The DPA section
    6.3 commits specifically to 7 days for session data. History records are
    pseudonymised rather than fully deleted to preserve the audit-log legal-
    obligation exception (Article 17(3)(b)). Alternatives considered: full
    deletion of history records (rejected on audit-log grounds); 30-day
    window (rejected as outside DPA commitment).
  derived_from: [IC-session-001]

- id: REQ-session-051
  type: data
  derivation: derived
  statement: |
    If the session service retains any session history record for a subject
    after an erasure request has been processed, then the record shall
    contain no directly-identifying fields.
  rationale: |
    Supports REQ-session-050's pseudonymisation commitment by guarding against
    partial-erasure defects (some identifying fields cleared, others missed).
    Every history-record schema change must re-verify this invariant.
  derived_from: [IC-session-001, REQ-session-050]
```

## Annotations — what makes this example honest

1. **Glossary first** — every term used in the requirements (Session, Idle timeout, Absolute timeout, Elevated session, Step-up authentication) is defined before any requirement uses it.

2. **State-driven complementary pairs** — REQ-session-003 (While IDLE → reject) is paired with REQ-session-004 (While ACTIVE + activity → keep ACTIVE).

3. **Five-element NFRs** — REQ-session-015 names the system, response, metric, target at p95, and the condition. REQ-session-016 uses Planguage tiered form because the right target is a range.

4. **Full interface dimensions** — REQ-session-020 covers protocol, message, timing, error handling, startup, plus DbC pre/post/invariants, plus versioning.

5. **Honest rationale** — every rationale names the option chosen and the criterion that drove the choice. The numeric specifics in REQ-session-005 (3/10/15) explicitly cite ADR-018; alternatives rejected. REQ-session-016 explains the tier interpretation.

6. **Derived requirements flagged** — REQ-session-001, REQ-session-050, REQ-session-051 carry `derivation: derived` and cite their introducing decisions.

7. **No design smuggled** — no requirement names a database, framework, library, algorithm, or data structure. Where a security choice is load-bearing (CSPRNG in REQ-session-001), it is cited as a governing decision, not a free-floating design choice in the requirement text.

8. **No fabricated rationale** — every rationale references a real upstream artifact (ADR, parent requirement, user story, DPA section). None says "industry-standard" or "best practice" without grounding.
