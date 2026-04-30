# Anti-patterns catalog — sweep targets

Sixteen failure modes. Each has a tell, a `check_failed` identifier, a severity, and a generic `recommended_action`. Walk every Public Interface entry, Data Structure entry, Algorithms section, State section, and Error matrix through this catalog. Every hit becomes a finding.

Patterns 1–11 are universal-DD; patterns 12–16 are AI-era / retrofit-specific. Hard-reject triggers marked ★.

## Contents

- [Interface and contract (5)](#interface-and-contract-5) — undefined-range, implicit-unit, leaking-interface, silent-null, **algorithmic-postcondition** ★
- [Error handling (3)](#error-handling-3) — no-strategy, swallowing, tunneling
- [State and concurrency (3)](#state-and-concurrency-3) — designing-for-races, state-explosion, missing-cancellation
- [AI-era and retrofit (5)](#ai-era-and-retrofit-5) — confident-invention, **code-paraphrase** ★, test-as-spec inversion, happy-path bias, **permutation-half-omitted** ★
- [Retrofit-only](#retrofit-only) — **fabricated-rationale** ★, **laundered-retrofit** ★
- [Sweep order](#sweep-order), [Aggregation rule](#aggregation-rule)

## Interface and contract (5)

### 1. Undefined-range precondition

- **Tell**: contract names the parameter's type but not the set of valid values
- **check_failed**: `anti-pattern.undefined-range-precondition`
- **severity**: `soft_reject`
- **evidence pattern**: quote the parameter; note the absence of value-range constraint
- **recommended_action**: *"State the value range, units, allowed enum, or relationship constraint."*

### 2. Implicit unit

- **Tell**: numeric parameter / return with no unit named nearby
- **check_failed**: `anti-pattern.implicit-unit`
- **severity**: `soft_reject`
- **evidence pattern**: quote the bare numeric type; note the absence of unit
- **recommended_action**: *"Name the unit in the contract OR use a typed wrapper."*

### 3. Implementation-leaking interface

- **Tell**: contract names a concrete collection (`LinkedHashMap`), exposes internal layout, or commits to storage
- **check_failed**: `anti-pattern.implementation-leaking-interface`
- **severity**: `soft_reject`
- **recommended_action**: *"Replace with the property the implementation delivers (uniqueness / ordering / lookup-time bound)."*

### 4. Silent null return

- **Tell**: return type is nullable; contract is silent on null case
- **check_failed**: `anti-pattern.silent-null-return`
- **severity**: `soft_reject`
- **recommended_action**: *"Name what null means in domain terms (absent value, no result, not found)."*

### 5. Algorithmic postcondition (HARD ★ refusal C)

- **Tell**: postcondition begins *"shall iterate"* / *"shall compute"* / *"shall walk"*
- **check_failed**: `anti-pattern.algorithmic-postcondition`
- **severity**: `hard_reject` ★ (refusal C)
- **evidence pattern**: quote the algorithmic clause verbatim
- **recommended_action**: *"Replace with a result-property statement. Both halves where applicable."*

## Error handling (3)

### 6. No error strategy

- **Tell**: DD specifies success path only; no matrix
- **check_failed**: `anti-pattern.no-error-strategy`
- **severity**: `soft_reject`
- **recommended_action**: *"Populate the error-handling matrix; pick a recovery strategy per row."*

### 7. Exception swallowing

- **Tell**: recovery is "log and continue"; caller receives success when operation didn't succeed
- **check_failed**: `anti-pattern.exception-swallowing`
- **severity**: `soft_reject`
- **recommended_action**: *"Surface the failure to the caller. Logging is diagnostic, not recovery."*

### 8. Exception tunneling

- **Tell**: business-logic function declares `throws SQLException` (or analogous low-layer type)
- **check_failed**: `anti-pattern.exception-tunneling`
- **severity**: `soft_reject`
- **recommended_action**: *"Translate to a domain error type at the leaf's boundary."*

## State and concurrency (3)

### 9. Designing for races

- **Tell**: check-then-act over shared state with no atomicity statement
- **check_failed**: `anti-pattern.designing-for-races`
- **severity**: `soft_reject`
- **recommended_action**: *"Name the synchronisation primitive AND the happens-before, OR redesign to eliminate the race."*

### 10. State explosion

- **Tell**: state machine doesn't fit on two pages; reachability not reasonable
- **check_failed**: `anti-pattern.state-explosion`
- **severity**: `soft_reject`
- **recommended_action**: *"Decompose into hierarchical states OR sibling leaves."*

### 11. Missing cancellation

- **Tell**: long-running op specifies start and completion but not "can be asked to stop"
- **check_failed**: `anti-pattern.missing-cancellation`
- **severity**: `soft_reject`
- **recommended_action**: *"Add a cancellation contract: signal, cooperative-or-abrupt, state-after-cancel, what caller observes."*

## AI-era and retrofit (5)

### 12. LLM confident invention

- **Tell**: crisp constraints (timing bounds, buffer sizes, concurrency) traceable to no upstream and no operational data
- **check_failed**: `anti-pattern.llm-confident-invention`
- **severity**: `soft_reject`
- **recommended_action**: *"Drop the constraint, OR cite the upstream artifact AND operational evidence."*

### 13. Code paraphrase / laundered code (HARD ★ refusal C)

- **Tell**: every clause derivable from reading the implementation; nothing says why
- **check_failed**: `anti-pattern.code-paraphrase`
- **severity**: `hard_reject` ★ (refusal C)
- **evidence pattern**: quote the paraphrasing clause; note the absence of any element the code would not show
- **recommended_action**: *"Replace clauses that paraphrase the implementation with result-property statements. Capture rationale at decision time."*

### 14. Test-as-spec inversion

- **Tell**: DD's error cases enumerate exactly what the test file asserts, neither more nor less
- **check_failed**: `anti-pattern.test-as-spec-inversion`
- **severity**: `soft_reject`
- **recommended_action**: *"Derive tests from the DD, not the DD from the tests. Surface gaps in the DD as `[NEEDS-CLARIFICATION]` rather than retro-fitting."*

### 15. Happy-path bias

- **Tell**: Public Interface and Algorithms thorough; Error Handling is one-liner
- **check_failed**: `anti-pattern.happy-path-bias`
- **severity**: `soft_reject`
- **recommended_action**: *"Populate the matrix for downstream failures, timeouts, partial-success — not just input validation."*

### 16. Permutation-half-omitted (HARD ★ refusal C)

- **Tell**: transformation postcondition states only one half (ordered without permutation; filtered without complete)
- **check_failed**: `anti-pattern.permutation-half-omitted`
- **severity**: `hard_reject` ★ (refusal C)
- **evidence pattern**: quote the postcondition; describe a degenerate implementation that passes
- **recommended_action**: *"Add the missing property half — both halves required."*

## Retrofit-only

### Fabricated rationale (HARD ★ refusal A — retrofit only)

- **Tell**: rationale reads as defence of current implementation; generic-principle phrases
- **check_failed**: `anti-pattern.fabricated-rationale`
- **severity**: `hard_reject` ★ (refusal A)
- **conditional gating**: applies only when `recovery_status:` declared
- **recommended_action**: *"Replace with `rationale: { status: unknown, note: ..., follow_up: ... }`."*

### Laundered retrofit (HARD ★ refusal A — retrofit only)

- **Tell**: zero `unknown`s + Gap Report empty + every rationale generic + diagram cleaner than reality
- **check_failed**: `anti-pattern.laundered-retrofit`
- **severity**: `hard_reject` ★ (refusal A)
- **conditional gating**: applies only when `recovery_status:` declared
- **recommended_action**: *"Apply retrofit discipline. Mark observed structure with evidence; mark rationale `verified` or `unknown`; populate the Gap Report."*

## Sweep order

Walk top to bottom. Items 1–11 are mechanically detectable; items 12–16 (and the two retrofit ones) require fresh-eyes judgment — ideally not on the same pass that scanned for #1–#11.

## Aggregation rule

Multiple findings of the same anti-pattern across multiple elements are surfaced as separate findings (one per element) — not aggregated. Use `element_id: "GLOBAL"` for document-wide patterns (laundered-retrofit, happy-path-bias at artifact level).

## Cross-link

`function-contract-checks.md` (1–5) · `error-handling-checks.md` (6–8) · `state-and-concurrency-checks.md` (9–11) · `retrofit-discipline-checks.md` (16, fabricated, laundered) · `quality-bar-gate.md` (final gate)
