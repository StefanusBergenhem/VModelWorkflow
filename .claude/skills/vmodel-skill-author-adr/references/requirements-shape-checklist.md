---
purpose: Verbatim-copyable subset of requirements discipline that ADR and architecture authors apply when emitting requirement-shaped content. Six gates — atomicity, EARS, testability, no-implementation-prescription, no-fabrication, traceability.
audience: author skills (ADR + architecture), framework maintainers
status: active (Phase 6, Cluster 3 — Issue 11 closure)
applies_to: vmodel-skill-author-adr (Step 8 route a), vmodel-skill-author-architecture (Steps 1-2)
source_of_truth: this file. Per-skill copies at `references/requirements-shape-checklist.md` are verbatim. Sync via `scripts/sync-requirements-shape-checklist.sh`.
---

# Requirements-Shape Checklist

Six gates an author skill applies when emitting **requirement-shaped content** outside the requirements artifact itself. Use verbatim. This is a subset of full requirements discipline — the parts that other authors borrow when they spawn a requirement statement. Full requirements authoring still happens via `vmodel-skill-author-requirements`.

Canonical source of truth: this file. Verbatim copies land in `vmodel-skill-author-adr/references/` and `vmodel-skill-author-architecture/references/` via a sync script. Edit here, propagate from here.

---

## Gate 1 — Atomicity

**Rule.** One `shall` (or `must`) per statement, verifying one behaviour. Compound statements split into multiple atomic statements.

**Why.** Two `shall`s = two requirements glued together = two test groups needed = silent loss of traceability per behaviour.

**Positive.**

```
REQ-A: When a user submits a credential pair, the session service shall
       validate it against the identity provider.
REQ-B: When the session service validates a credential pair, it shall emit
       a 'credential-validation' audit event with outcome and user identifier.
```

**Negative.**

```
REQ-X: The system shall authenticate the user and shall log the attempt.
       (Two `shall`s. Two requirements. Split.)
```

**Review check.** `check.requirement.compound`

---

## Gate 2 — EARS shape

**Rule.** The statement opens with one of the five EARS keywords:

| Pattern | Opening |
|---|---|
| Ubiquitous | `The <system> shall …` |
| Event-driven | `When <trigger>, the <system> shall …` |
| State-driven | `While <state>, the <system> shall …` |
| Optional-feature | `Where <feature>, the <system> shall …` |
| Unwanted-behaviour | `If <condition>, then the <system> shall …` |

Compound limit: at most two keywords per statement, in canonical order `Where → While → When → If/then → shall`.

**Why.** A grammar fixes the surface so atomicity, testability, and trigger/state separation become visually obvious. Free-form "system requirements" hide compounds and missing triggers.

**Positive.**

```
While a session is in the IDLE state, the session service shall reject
validation requests for that session with status 401 and reason 'idle-timeout'.
```

**Negative.**

```
The session service handles idle sessions by rejecting their validation
requests appropriately.
       (No EARS opening. "Handles" is not `shall`. "Appropriately" defeats Gate 3.)
```

**Review check.** `check.ears.invalid-pattern`

---

## Gate 3 — Testability (the box test)

**Rule.** A tester reading the statement plus the glossary alone can write a test that distinguishes conforming from non-conforming behaviour. Pass/fail must be binary and observable from outside the system.

**Why.** Untestable requirements cannot be verified — they are aspirations that look like specifications.

**Positive.**

```
If the session service is unable to reach the backing store, then it shall
return 503 to validation requests with header 'Retry-After: 1', shall fail
the readiness probe, and shall not return 200 with valid=false.
```

**Negative.**

```
The system shall handle errors gracefully.
       ("Gracefully" is not measurable. "Errors" is unbounded. No test possible.)
```

**Tells.** Vague adjectives (*fast, sufficient, appropriate, robust, user-friendly*); ambiguous pronouns (*it, them, the appropriate response*); unbounded escapes (*such as, including but not limited to, etc., where applicable*); wishful thinking (*zero latency, infinite capacity*); placeholders (*TBD, TBR, TODO*).

**Review check.** `anti-pattern.untestable-statement`

---

## Gate 4 — No implementation prescription

**Rule.** The statement names *what* the system does, not *how*. No library, framework, algorithm, named protocol implementation, named pattern, or specific data structure inside the statement.

**The box test.** Could two different implementations both satisfy this requirement? If only one implementation can, the requirement is over-specified — it is a design decision wearing requirement clothing.

**Why.** Implementation choices that survive in requirement statements outlast the conditions that justified them. The choice belongs in an ADR; the requirement captures the behaviour the choice was meant to ensure.

**Positive.**

```
While a session is in the ACTIVE state, the session service shall reflect
session-state changes to all nodes within 5 seconds of commit, measured at
p99 under normal load.
```

**Negative.**

```
The session service shall use Redis with a 5-second TTL for active session state.
       (Names a product and a configuration value. Move Redis choice to an ADR;
        keep the 5-second propagation behaviour as the requirement.)
```

**Narrow exception.** Interface requirements may name externally imposed protocols (HTTP/1.1, gRPC, OIDC 1.0, TLS 1.3, RFC 6749). The protocol is *what* — a constraint imposed from outside — not *how* — a design choice made inside.

**Audit list.** Named technologies, libraries, data structures, algorithms, design patterns ("singleton", "publish-subscribe"), language features. None belong in a requirement statement.

**Review check.** `anti-pattern.implementation-prescription`

---

## Gate 5 — No fabrication

**Rule.** Rationale derives from a named driver — a section of the ADR Context, an entry in the parent architecture's `allocates` list, or a clause of the parent requirement. Never invent a justification.

**Retrofit case.** If rationale is not recoverable from preserved evidence, set `rationale: unknown` and `rationale_recovery_status: unknown`. Do not synthesise. The behaviour fields may be `reconstructed` from observable code or tests; the rationale field never may.

**Why.** Fabricated rationale silently launders a guess into a justification. It survives review when it sounds plausible, then misleads every downstream consumer who reasons from it.

**Positive (greenfield, derived from ADR).**

```yaml
- id: REQ-NNN
  derivation: derived
  statement: "Per ADR-012 (token generation), the session service shall use
              a CSPRNG for all session token generation."
  rationale: "ADR-012 mandated CSPRNG following the 2024 entropy audit; this
              requirement makes the choice testable at this layer."
  derived_from: [ADR-012]
```

**Positive (retrofit, rationale lost).**

```yaml
- id: REQ-R-NNN
  statement: "<reconstructed from observed behaviour>"
  statement_recovery_status: reconstructed
  rationale: unknown
  rationale_recovery_status: unknown
  derived_from: [src/session.py:142-160]
```

**Negative.**

```yaml
- id: REQ-NNN
  statement: "..."
  rationale: "Balances security with performance per industry best practice."
       (Generic. Names no driver. Fits any requirement. Fabricated.)
```

**Tells of fabrication.** Generic phrasing (*balances X with Y*, *industry-standard*, *best practice*); no specific decision named; no alternative considered; rationale that fits any requirement; in retrofits, rationale present for every requirement when no decision records were preserved.

**Review check.** `anti-pattern.fabricated-rationale`

---

## Gate 6 — Traceability

**Rule.** The statement carries a non-empty link to its originating driver: the ADR that materialised it (route (a)), the parent requirement it refines, the parent architecture's decomposition entry that allocated it. Traceability is by ID; cross-tree references never use paths.

**Why.** A statement without traceability is an orphan — unjustified and unenforceable. Tooling derives the reverse links; the author's job is forward links.

**Positive.**

```yaml
- id: REQ-NNN
  derivation: derived
  derived_from: [ADR-012]
  governing_adrs: [ADR-012]
```

**Negative.**

```yaml
- id: REQ-NNN
  statement: "The session service shall use a CSPRNG..."
       (No derived_from. No governing_adrs. Bare statement, untraceable.)
```

**Review check.** `check.traceability.orphan-requirement`

---

## When this checklist applies

| Author skill | Step | Trigger |
|---|---|---|
| `vmodel-skill-author-adr` | Step 8 (Propagation) | Route (a) materialises a new requirement at the ADR's scope |
| `vmodel-skill-author-architecture` | Step 1 (Decomposition) | The `allocates` list spawns a NEW derived requirement at child scope (uncommon — most allocations reuse parent IDs) |
| `vmodel-skill-author-architecture` | Step 2 (Interfaces) | Interface contract preconditions / postconditions / invariants read like standalone requirements (the line is fuzzy; when in doubt, run the checklist) |

For full requirements authoring — typing, classification, NFR five-element rule, interface five-dimensions rule, glossary, complementary-pair rule, derivation discipline — invoke `vmodel-skill-author-requirements` directly. This checklist is a subset borrowed by other authors, not a replacement.
