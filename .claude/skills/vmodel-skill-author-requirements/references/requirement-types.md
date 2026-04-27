# Requirement types — five-type taxonomy

Every requirement is filed under exactly one type. Misclassification silently weakens the document because each type has different rigor rules and different downstream consumers (allocation, test derivation, audit, contract).

## The five types

### 1. Functional

What the system does in response to stimuli or in a given state.

| Aspect | Detail |
|---|---|
| Verified at | Unit + integration + system tests, depending on scope |
| Sentence shape | EARS event-driven, state-driven, ubiquitous |
| Example | "When the user submits valid credentials, the system shall create a session and return its token." |

### 2. Quality attribute (NFR)

A measurable non-functional characteristic under specified load and environment.

| Aspect | Detail |
|---|---|
| Verified at | Performance / load / chaos tests; static analysis for some |
| Sentence shape | Five-element rule (see `nfr-five-elements.md`); Planguage for tiered targets |
| Example | "The session-validation endpoint shall respond in ≤ 50 ms at p95 under 5,000 concurrent sessions, measured at the API gateway." |

### 3. Interface

A contract with an external caller, dependency, or protocol peer.

| Aspect | Detail |
|---|---|
| Verified at | Contract tests; integration tests at the interface |
| Sentence shape | Five dimensions (see `interface-five-dimensions.md`) |
| Example | "The authentication callback shall accept OIDC authorization-code responses per RFC 6749 §4.1.2, and shall reject responses whose `state` parameter does not match the one issued." |

### 4. Data

Format, retention, privacy class, integrity invariants of data the system holds or exchanges.

| Aspect | Detail |
|---|---|
| Verified at | Schema tests; data-layer tests; compliance audits |
| Sentence shape | EARS for behavioural data rules; declarative invariants for structural ones |
| Example | "Session records shall retain the user's IP address for no more than 90 days from last activity, after which the IP field shall be deleted while the session history record is preserved." |

### 5. Inherited constraint

Bounds imposed from above or outside (parent decisions, regulatory, organisational, financial, temporal) that this scope must honour.

| Aspect | Detail |
|---|---|
| Verified at | Reviewed; some are architecture-testable, some are process-verified |
| Sentence shape | Source citation + binding rationale + (often) derived requirements |
| Example | "Per the architectural decision on token generation, all session token generation shall use a CSPRNG; direct use of the platform's default Random class or equivalent is prohibited." |

## Classification decision table

When you have a candidate requirement statement and need to decide its type, walk this table top to bottom — the first Yes wins:

| # | Question | If Yes |
|---|---|---|
| 1 | Is the statement imposed from outside this scope (a parent decision, regulation, contractual obligation, or organisational policy)? | **Inherited constraint** |
| 2 | Does the statement primarily specify a contract with an external caller, dependency, or protocol peer? | **Interface** |
| 3 | Does the statement primarily specify the format, retention, privacy, or integrity of data? | **Data** |
| 4 | Does the statement specify a measurable non-functional characteristic (latency, throughput, availability, security property, etc.) with a target and a condition? | **Quality attribute (NFR)** |
| 5 | Does the statement specify behaviour the system performs (in response to a trigger, in a state, as an invariant)? | **Functional** |

If none of 1–5 apply, the statement is misclassified or under-specified — revisit it before filing.

## Two recurring level-confusion errors

### Error 1 — NFR written as functional

```
BAD:  "The system shall be fast."
      Reads as functional ("shall be …") but is an untestable NFR (no metric,
      no target, no condition).

FIX:  Move to the NFR section. Apply the five-element rule:
      "The session-validation endpoint shall respond in ≤ 50 ms at p95 under
       5,000 concurrent sessions in the production deployment, measured at
       the API gateway."
```

### Error 2 — Design smuggled as functional

```
BAD:  "The system shall use a distributed cache to store session tokens."
      Reads as functional but is an architectural decision.

FIX:  Move the architectural choice to an ADR. If the choice was meant to
      ensure a behaviour at this layer, author the behavioural requirement
      that captures it:
      "While a session is in the ACTIVE state, the session service shall
       reflect session-state changes to all nodes within 5 seconds of
       commit, measured at p99 under normal load."
```

## Same-scope discipline

Every requirement in this document must apply to **this scope**. Parent-scope concerns are upstream `derived_from` references, not requirements here. Child-scope concerns belong in the child's requirements document.

If you find yourself writing about something that is clearly a parent or child concern, stop and route it to the right artifact.
