# Data and invariant checks

Mirrors `data-structures-by-invariant.md` on the author side. Walk every Data Structure entry against these checks.

## check.data.fields-without-invariant (soft)

**Check that** fields with constraints beyond what the type system enforces have per-field invariants.

**Reject when** a field has a non-trivial constraint (range, foreign key, encoding, cross-field) and no invariant is stated.

**Approve when** every field with a non-type-enforced constraint has an invariant.

**recommended_action:** *"Add per-field invariants where the type alone does not capture the constraint."*

## check.data.ownership-unstated (soft)

**Check that** every data structure states ownership (who constructs / mutates / releases).

**Reject when** the `ownership` field is absent or vacuous ("various").

**Approve when** ownership names a concrete construction-and-mutation discipline.

**recommended_action:** *"State ownership concretely: who constructs the structure, who may mutate it, when it is released."*

## check.data.lifetime-unstated (soft)

**Check that** every data structure states lifetime.

**Reject when** the `lifetime` field is absent or vacuous.

**Approve when** lifetime names a concrete bound (request-scoped, per-connection, process, event-sourced).

**recommended_action:** *"State lifetime concretely: how long instances live and what bounds their lifetime."*

## check.data.returned-mutable-without-semantics (soft)

**Check that** when a structure crosses the public interface (returned from a public function), `returned_semantics` is stated.

**Reject when** the structure is returned and the field is absent.

**Approve when** one of: copy / live view / read-only reference / read-only snapshot / ownership transfer.

**recommended_action:** *"Add `returned_semantics`. Without it, callers leak ownership ambiguity."*

## check.data.shared-mutable-without-contract (soft)

**Check that** any field shared across threads or callers states locking, happens-before, and per-field reader/writer.

**Reject when** the structure has shared mutable fields and no synchronisation contract is stated.

**Approve when** lock + happens-before + reader/writer are named per shared field.

**Evidence pattern:** quote the shared field; note the absence of synchronisation contract.

**recommended_action:** *"State the synchronisation contract per shared field: which lock guards it, what happens-before relation is established, who reads, who writes."*

## anti-pattern.designing-for-races (soft)

**Check that** check-then-act sequences over shared state have explicit atomicity (lock, CAS, transaction).

**Reject when** the DD describes "check whether X, then update X" with no atomicity statement.

**Approve when** atomicity is named OR the operation is decomposed into a different design that eliminates the race.

**recommended_action:** *"State the atomicity primitive (lock, CAS, transaction) OR redesign to eliminate the race."*

## check.data.types-language-specific (soft)

**Check that** field types are at one level above the implementation language.

**Reject when** types are language-specific (`uint32_t`, `LinkedHashMap`) without a contractual reason (wire format, fixed-size buffer).

**Approve when** types are language-neutral, OR bit-width is contractual and stated.

**recommended_action:** *"Use language-neutral types ('non-negative integer', 'UTC timestamp', 'list of T'). Bit-width only when contractual (wire format, fixed buffer)."*

## check.data.invariant-untestable (soft)

**Check that** invariants are testable (a unit test can assert them without contrived setup).

**Reject when** an invariant is too vague to assert ("data is consistent", "structure is valid").

**Approve when** the invariant is a concrete predicate.

**recommended_action:** *"Replace the vague invariant with a concrete predicate (range, foreign key, encoding, cross-field equality)."*

## Cross-link

`anti-patterns-catalog.md` · `quality-bar-gate.md` (Data and invariants card) · `templates/data-structure-entry.yaml.tmpl`
