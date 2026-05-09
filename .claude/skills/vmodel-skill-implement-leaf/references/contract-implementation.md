---
purpose: Turning DbC clauses into code — preconditions as guards, postconditions as return invariants, errors as typed paths.
audience: vmodel-skill-implement-leaf
status: active
---

# Contract Implementation

**Contents.** Contract-to-code mapping · Preconditions · Postconditions ·
Invariants · Error matrix · Thread-safety · Nullability · Side-effect
declaration · Anti-patterns · Cross-links.

---

## 1. Contract-to-code mapping (overview)

Each Public Interface entry in the DD carries nine elements
(`function-contracts.md` in `vmodel-skill-author-detailed-design/references/`).
The implementation must honour each element — not as comments, but as executable
code.

| DD element | Implementation obligation |
|---|---|
| Signature (name, params, return type) | Exact match — no rename, no additional overloads not in DD |
| Preconditions | Guards at entry; trust-boundary stance determines whether to throw or assert |
| Postconditions (on_success) | Return value or post-state satisfies the stated property |
| Postconditions (on_failure) | Typed error produced; no unspecified side effects |
| Invariants | Enforced across the call; class-level invariants enforced at construction and mutation |
| Errors (typed enum) | Only the typed errors in the error matrix are thrown/returned |
| Nullability | No null where forbidden; Optional/None/empty where permitted |
| Side effects | None beyond what the DD states; I/O only via interfaces the DD specifies |
| Thread-safety category | Implementation structure matches the Goetz category |

---

## 2. Preconditions as guards

### Inside a trust boundary (DbC stance)

When the DD states "caller-validated input; DbC inside trust boundary":

- Add a lightweight assertion (`assert`, `requireNotNull`, `Objects.requireNonNull`, etc.)
- Do NOT add full defensive input validation
- If the precondition is violated at runtime, that is a programming error in the
  caller — fail fast and loud (assertion error, not a typed domain error)

```java
// DD: precondition — scope != null, scope non-empty
// DD stance: caller-validated; DbC
void processScope(String scope) {
    assert scope != null && !scope.isEmpty() : "scope precondition violated";
    // ... implementation
}
```

### At a trust boundary (defensive stance)

When the DD states "external input; defensive validation":

- Validate every input before use
- Produce the typed error from the error matrix on violation
- Do not propagate invalid data

```java
// DD: precondition — userId non-null, non-blank
// DD stance: external HTTP input; defensive
// Error matrix: userId invalid → UserValidationError.BLANK_ID
Result<User> fetchUser(String userId) {
    if (userId == null || userId.isBlank()) {
        return Result.failure(UserValidationError.BLANK_ID);
    }
    // ... implementation
}
```

---

## 3. Postconditions as result invariants

Implement the result property — not the procedure that happens to produce it.

### on_success

The return value or post-state must satisfy the DD's stated property. Write the
code so the property holds by construction, not by hope.

```
DD postcondition on_success: "returned list is non-descending AND is a
permutation of the input (multiset equality)"

Implementation obligation:
  - sort produces non-descending order (test: list[i] <= list[i+1] for all i)
  - no elements added or removed (test: Collections.frequency same for all values)
Both halves enforced — one half is insufficient.
```

### on_failure

The failure path must:
1. Produce exactly the typed error specified in the error matrix for this condition.
2. Leave state unchanged (or bounded to whatever the DD guarantees: "no mutation",
   "compensated within Nms", etc.).

```java
// DD on_failure: "account not found → AccountError.NOT_FOUND; no mutation to any state"
Result<Account> getAccount(AccountId id) {
    Optional<Account> found = repository.find(id);
    if (found.isEmpty()) {
        // No mutation has occurred above this point — satisfies "no mutation" guarantee
        return Result.failure(AccountError.NOT_FOUND);
    }
    return Result.success(found.get());
}
```

---

## 4. Invariants

### Class-level invariants

Class-level invariants stated in Data Structures must be enforced at construction
(constructor, factory method, builder `build()`) and preserved by every mutating
method.

```
DD data structure invariant: "items list is non-empty after construction"

Constructor:
    if (items.isEmpty()) throw new IllegalArgumentException("items must be non-empty");

Every mutating method that removes items:
    // At the end, verify: assert !this.items.isEmpty();
    // Or: throw before removal would leave the list empty
```

### Per-call invariants

When an Interface entry carries an invariant (e.g., "the result total equals the
sum of all line items"), verify the invariant is structurally enforced — not just
coincidentally true for the test inputs.

---

## 5. Error matrix completeness

Every row in the DD's error matrix must have a corresponding code path.

Tracing procedure:
1. List every row: `condition → typed error`.
2. For each row, find (or write) the code path that produces that typed error.
3. Verify the typed error is the exact type in the error matrix (not a subtype,
   not a supertype, not a generic exception).

If any row has no code path: that is a `missing-implementation` gap. Add it.

If a code path produces a typed error not in the error matrix: that is a
`scope-violation`. Remove it (or expand the error matrix via DD revision).

---

## 6. Thread-safety implementation patterns

Honour the Goetz category stated in each Public Interface entry.

| Category | Implementation pattern |
|---|---|
| Immutable | All fields `final`; no setters; defensive copy mutable inputs at construction; return unmodifiable views |
| Thread-safe | Synchronize all access to mutable state; prefer `java.util.concurrent` structures; document the lock |
| Conditionally thread-safe | Document which compound operations require external locking; do not hide internal partial protection |
| Thread-compatible | No internal synchronization; callers take responsibility; state this in doc comment |
| Thread-hostile | Document explicitly; never share across threads; assert single-thread context if language allows |

When the DD assigns different categories to different methods on the same class,
the class-level category is the most restrictive; individual methods can be noted
as exceptions.

---

## 7. Nullability implementation

| DD nullability statement | Implementation rule |
|---|---|
| Parameter must not be null | Guard at entry; throw NullPointerException or typed error per error matrix |
| Parameter may be null (means absent) | Handle the null branch; do not dereference before null check |
| Return must not be null | Never return null; use Optional.of, empty collection, or Null Object |
| Return may be null (no result) | Document clearly; prefer Optional.empty() or empty collection over literal null |

Language-level mechanisms (`Optional<T>`, `@NonNull`, Kotlin `?`) carry the
nullability contract in the type. Still state what the absence means in domain
terms (matching the DD's language).

---

## 8. Side-effect declaration

If the DD states `side_effects: none` on an entry:
- The implementation must produce no observable state change on any object
  reachable from outside the function
- No writes to mutable shared state
- No I/O

If the DD states a specific side effect (e.g., "updates the audit log via
AuditService"):
- Implement exactly that side effect via the interface the DD specifies
- No additional side effects

---

## 9. Anti-patterns

| Anti-pattern | Why it violates the contract | Fix |
|---|---|---|
| Returning `null` where DD says non-null | Breaks postcondition | Return Optional.empty() or Null Object |
| Throwing a generic `Exception` | Not in the typed error matrix | Throw the typed enum/class from the error matrix |
| Swallowing exceptions in catch | Hides the error matrix path | Re-throw or convert to typed error |
| Implementing behaviour not in DD | Scope violation | Remove; update DD if truly needed |
| Asserting wrong thread-safety category | Breaks Goetz contract | Restructure to match DD's stated category |
| Defensive checks inside trust boundary | Violates DbC stance | Remove; keep only at trust boundaries |
| Missing failure-branch postcondition | Partial contract satisfaction | Add the typed error path with state guarantee |
| Invariant checked only in tests | Tests do not enforce production invariants | Move enforcement into constructor / mutation site |

---

## Cross-links

`tdd-green-and-refactor.md` · `fix-mode-taxonomy.md` · `SKILL.md`
