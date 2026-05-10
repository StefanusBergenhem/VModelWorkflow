# Anti-patterns — sweep before delivering

Sixteen failure modes. Each has a tell. Sweep top-to-bottom on every draft. Hard-reject triggers marked ★ (refusal A/B/C/D in `SKILL.md`).

## Contents

- [Interface and contract (5)](#interface-and-contract-5) — undefined-range, implicit-unit, leaking-interface, silent-null, algorithmic-postcondition
- [Error handling (3)](#error-handling-3) — no-strategy, swallowing, tunneling
- [State and concurrency (3)](#state-and-concurrency-3) — designing-for-races, state-explosion, missing-cancellation
- [AI-era and retrofit (5)](#ai-era-and-retrofit-5) — confident-invention, code-paraphrase, test-as-spec inversion, happy-path bias, post-hoc DD
- [Sweep order](#sweep-order) and [Hard-reject mapping](#hard-reject-mapping)

## Interface and contract (5)

### 1. Undefined-range precondition

Tell: contract names the parameter's type but not the set of valid values.
Fix: state the value range, units, allowed enum, or the relationship constraint.

### 2. Implicit unit ★ (when on a numeric crossing a system boundary)

Tell: `double altitude`, `long duration`, `float temperature` with no unit named.
Fix: name the unit in the contract OR use a typed wrapper (`Metres`, `Millis`).

### 3. Implementation-leaking interface

Tell: contract names a concrete collection (`LinkedHashMap`), exposes internal layout, or commits to a storage mechanism.
Fix: state the property (uniqueness, ordering, lookup-time bound), not the structure delivering it.

### 4. Silent null return

Tell: return type is nullable in the language; contract does not mention the null case.
Fix: state what `null` (or `None` / `Optional.empty`) means in domain terms.

### 5. Algorithmic postcondition ★ (refusal C)

Tell: postcondition begins *"shall iterate"* / *"shall compute"* / *"shall walk"*.
Fix: state the property of the result, not the steps the implementation takes. Both halves where applicable (ordered AND permutation; filtered AND complete).

## Error handling (3)

### 6. No error strategy

Tell: DD specifies only the success path; no error matrix; no per-row recovery.
Fix: populate the five-column error matrix; pick a recovery strategy per row (fail-fast / retry / fallback / compensate / propagate).

### 7. Exception swallowing

Tell: recovery is "log and continue"; caller receives a success return when the operation materially did not succeed.
Fix: surface the failure to the caller; logging is not a recovery strategy.

### 8. Exception tunneling

Tell: business-logic function declares `throws SQLException` (or analogous low-layer type) at its public boundary.
Fix: translate to a domain-level error type at the leaf's boundary; carry the original as cause/diagnostic if needed.

## State and concurrency (3)

### 9. Designing for races

Tell: DD describes "check whether X, then update X" with no atomicity statement, no lock, no CAS.
Fix: state the synchronisation primitive AND the happens-before relation; or eliminate the race via a different design.

### 10. State explosion

Tell: state machine with dozens of states; diagram does not fit on two pages; reviewers cannot reason about reachability.
Fix: hierarchical states with substates, OR decompose into sibling leaves.

### 11. Missing cancellation

Tell: contract specifies start and completion of a long-running op but not "can be asked to stop".
Fix: state the cancellation signal (token / context / sentinel), cooperative-or-abrupt, state-after-cancel, what caller observes.

## AI-era and retrofit (5)

### 12. LLM confident invention

Tell: crisp constraints — timing bounds, buffer sizes, concurrency semantics — that trace to no upstream requirement and no operational data.
Fix: drop the constraint OR cite the upstream artifact AND operational evidence.

### 13. Code paraphrase / laundered code ★ (refusal C)

Tell: every contract clause is derivable from reading the implementation; nothing in the DD says why the contract is what it is.
Fix: replace clauses that paraphrase the implementation with result-property statements; capture rationale at decision time.

### 14. Test-as-spec inversion

Tell: DD's error cases enumerate exactly what the test file asserts, neither more nor less.
Fix: derive tests from the DD, not the DD from the tests; surface gaps in the DD as `[NEEDS-CLARIFICATION]` rather than retro-fitting from existing tests.

### 15. Happy-path bias

Tell: Public Interface and Algorithms thorough; Error Handling section is a one-liner.
Fix: populate the matrix for downstream failures, timeouts, partial-success paths — not just input validation.

### 16. Post-hoc DD / fabricated rationale ★ (refusal A — retrofit only)

Tell: rationale reads as a defence of the current implementation; generic-principle phrases ("balances X with Y", "follows clean architecture", "industry-standard"); on retrofit with no preserved decision record.
Fix: in retrofit, mark rationale `unknown` with a follow-up owner; never invent a plausible-sounding history.

## Sweep order

Walk top to bottom. Items 1–11 are mechanically detectable; items 12–16 require fresh-eyes judgment — ideally not on the same pass that wrote the artifact.

## Hard-reject mapping

| Anti-pattern | Refusal | Severity |
|---|---|---|
| #5 Algorithmic postcondition | C | hard_reject |
| #13 Code paraphrase | C | hard_reject |
| #16 Fabricated rationale (retrofit only) | A | hard_reject |
| `check.recovery-status.overview-reconstructed` (schema) | A | hard_reject |
| `check.parent-architecture.missing` | B | hard_reject |
| `check.spec-ambiguity-test.fail` | D | override (DESIGN_ISSUE if upstream-traceable; REJECTED otherwise) |

All other anti-patterns are soft-reject (accumulate to REJECTED).

## Cross-link

`function-contracts.md` (1–5) · `error-handling.md` (6–8) · `state-and-concurrency.md` (9–11) · `retrofit-discipline.md` (16) · `quality-bar-checklist.md` (final gate)
