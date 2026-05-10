# Function contract checks

Mirrors `function-contracts.md` on the author side. Walk every Public Interface entry against these checks. The hard-reject triggers are flagged ★.

## Contents

- `check.contract.*` — signature-only, precondition-missing, postcondition branches, units, thread-safety, nullability
- `anti-pattern.algorithmic-postcondition` ★ (refusal C)
- `anti-pattern.permutation-half-omitted` ★ (refusal C)
- `anti-pattern.implicit-unit`, `implementation-leaking-interface`, `silent-null-return`

## check.contract.signature-only (soft)

**Check that** every entry carries more than a signature — preconditions, postconditions, error semantics, side effects, thread-safety.

**Reject when** the entry is signature plus a one-line description with no contract elements.

**Approve when** the nine contract elements are addressed (each populated OR explicitly stated as not applicable).

**recommended_action:** *"Add the missing contract elements per `function-contracts.md`. A signature alone is a name for a contract, not a contract."*

## check.contract.precondition-missing (soft)

**Check that** preconditions are stated (or "none beyond callable" stated explicitly).

**Reject when** the field is absent.

**Approve when** preconditions name caller obligations (value range, state, relationship) OR explicitly state "none".

**recommended_action:** *"Add the preconditions clause. State 'none beyond callable' explicitly when no preconditions apply."*

## check.contract.postcondition-success-missing (soft)

**Check that** `postconditions.on_success` is populated.

**Reject when** the branch is absent or empty.

**Approve when** the success branch states the property of the result.

**recommended_action:** *"Populate `postconditions.on_success` with the result property — what the function guarantees on the way out."*

## check.contract.postcondition-failure-branch-missing (soft)

**Check that** `postconditions.on_failure` is populated.

**Reject when** only `on_success` is present; `on_failure` is absent or empty.

**Approve when** `on_failure` states typed error and state guarantee.

**recommended_action:** *"Add `postconditions.on_failure`. A single-branch postcondition is half-specified; integration-time surprises live on the unstated branch."*

## anti-pattern.algorithmic-postcondition (HARD ★ refusal C)

**Check that** postconditions describe properties of the result, not steps the implementation takes.

**Reject when** a postcondition begins *"shall iterate"* / *"shall compute"* / *"shall walk"* — the postcondition describes implementation steps.

**Approve when** postconditions name the property the result satisfies (ordered AND permutation; filtered AND complete; mapped AND positionally-corresponding).

**Evidence pattern:** quote the algorithmic clause verbatim.

**recommended_action:** *"Replace with a result-property statement (refusal C). Two halves rule applies for transformations."*

## anti-pattern.permutation-half-omitted (HARD ★ refusal C)

**Check that** transformation postconditions state both halves (ordered AND permutation; filtered AND complete; mapped AND positionally-corresponding).

**Reject when** only one half is stated and the other lets degenerate implementations pass (e.g., "ordered" without "permutation" lets `return []` pass).

**Approve when** both halves are stated.

**Evidence pattern:** quote the postcondition; name which half is missing; describe a degenerate implementation that passes.

**recommended_action:** *"Add the missing property half — both halves are required."*

## check.contract.units-missing (soft)

**Check that** numeric parameters and returns either carry a typed unit-wrapper OR have the unit named in the contract.

**Reject when** a `double` / `long` / `float` parameter or return has no unit named nearby.

**Approve when** the unit is in the type OR named in the contract.

**recommended_action:** *"Name the unit in the contract OR use a typed wrapper (`Metres`, `Millis`)."*

## check.contract.thread-safety-unstated (soft)

**Check that** every public function names a thread-safety category from the Goetz taxonomy.

**Reject when** the field is absent.

**Approve when** the category is one of: immutable / thread-safe / conditionally-thread-safe / thread-compatible / thread-hostile.

**recommended_action:** *"Add the thread-safety category. Silent assumptions are bugs."*

## check.contract.nullability-unstated (soft)

**Check that** nullability is explicit per parameter and return.

**Reject when** the return type is nullable in the language but the contract does not state when null is permitted and what it means.

**Approve when** nullability is stated per slot with domain meaning.

**recommended_action:** *"State nullability per parameter and return. When null is permitted, name what it means in domain terms."*

## anti-pattern.implicit-unit (soft)

**Check that** numeric crossing a system boundary names its unit.

**Reject when** a numeric parameter / return has no unit named.

**Approve when** the unit is in the type OR named in the contract.

**recommended_action:** *"Name the unit in the contract OR use a typed wrapper. Implicit units cause Mars Climate Orbiter incidents."*

## anti-pattern.implementation-leaking-interface (soft)

**Check that** the contract states properties (uniqueness, ordering, lookup-time bound), not concrete language collections.

**Reject when** the contract names `LinkedHashMap`, `TreeMap`, `Vec<T>`, internal storage layout, or specific library-internal types.

**Approve when** the contract is language-neutral.

**recommended_action:** *"Replace the concrete collection with the property it delivers (uniqueness / ordering / lookup-time bound)."*

## anti-pattern.silent-null-return (soft)

**Check that** the contract names what `null` (or `None`, `Optional.empty`) means in domain terms when the return is nullable.

**Reject when** the return type is nullable but the contract is silent on the null case.

**Approve when** the meaning is stated.

**recommended_action:** *"Name what null means in domain terms (absent value, no result, not found)."*

## Cross-link

`anti-patterns-catalog.md` · `quality-bar-gate.md` (Contracts card) · `templates/public-interface-entry.yaml.tmpl` · refusal C in `SKILL.md`
