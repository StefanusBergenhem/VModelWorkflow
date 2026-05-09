# Layer rendering rules

Per-layer rules for translating TestSpec cases into test code. Read the section that
matches the TestSpec `level:` field before starting Step 3.

## Table of contents

- [Leaf — unit tests](#leaf--unit-tests)
- [Branch — integration tests](#branch--integration-tests)
- [Root — system / acceptance tests](#root--system--acceptance-tests)
- [Layer mismatch tells](#layer-mismatch-tells)

---

## Leaf — unit tests

**Source:** leaf TestSpec (`level: unit`) + leaf Detailed Design.

**What to wire:** the public interface of the single unit under test. Call the function /
method / constructor directly with the `inputs:` values from the case.

**Test doubles:** max 2. Only infrastructure collaborators (clock, filesystem, HTTP client,
database client). Domain collaborators must use real instances or simple fakes. If the DD
names a collaborator with a defined contract, stub that contract exactly — invent nothing.

**Arrange / Act / Assert structure (mandatory):**

```
// Arrange — set up inputs and any stubs
// Act     — call the unit under test exactly once
// Assert  — check expected output value(s)
// VERIFIES: TC-<scope>-NNN → <upstream-ids>
```

**Parameterization:** when multiple cases differ only in `inputs:` and `expected:`, render
as a parameterized test (JUnit 5 `@ParameterizedTest`, pytest `@pytest.mark.parametrize`,
Go table-driven, Vitest `it.each`). Each row must carry a description matching the case
`title:`.

**State-transition cases:** drive the state machine with the minimum sequence described in
case `steps:` (if present at leaf). One `Act` per case. If the case requires two separate
state transitions, it belongs at the branch layer; raise a HALT condition.

**Do not** import or exercise any component outside the leaf's package/module boundary
except through declared test doubles.

---

## Branch — integration tests

**Source:** branch TestSpec (`level: integration`) + branch Architecture.

**What to wire:** the composition described in the Architecture `composition:` section.
The test drives the published interface of the branch and observes cross-child state.

**Environment shape:** the `preconditions:` field names the environment. Map to:

| TestSpec precondition phrase | Rendering implication |
|---|---|
| `in-process` | All child components instantiated in-process; no network calls |
| `test-containers (Postgres 16, ...)` | Spin up named Docker containers; use `testcontainers` library |
| `shared-staging` | Use the named staging environment; do not spin up anything locally |
| `production-like` | Treat as shared-staging unless otherwise specified |

**Test doubles at branch:** every test double named in `preconditions:` must be implemented
at the fidelity level specified:

| Fidelity | What to write |
|---|---|
| `dummy` | Null / no-op instance; no assertions |
| `stub` | Returns canned responses for named inputs; no assertions |
| `spy` | Records calls; assert call count/args in `expected:` if case specifies |
| `mock` | Pre-programmed with expectations; verified at end of test |
| `fake` | Working implementation (e.g., in-memory DB); add `// CONTRACT: <child>` comment |

For fakes, add a `// CONTRACT: <child-component-name>` comment on the fake class/struct.
This comment signals to a reader which real component's contract the fake honours.

**Steps translation:** each item in `steps:` becomes one `// Act` call or observation.
Single-Act discipline still applies — if the case has multiple distinct Acts, split into
separate tests. A step that is purely an assertion on previous state maps to an `// Assert`
line, not a new `Act`.

**Cross-child assertions:** `expected:` items on branch cases typically assert observable
state on a child component (event emitted, state flag set, return value). Translate each
item to one or more assertions. Cross-child invariants (e.g., "order of events preserved
across boundary") translate to ordering or sequencing assertions.

---

## Root — system / acceptance tests

**Source:** root TestSpec (`level: system`) + root Requirements.

**What to wire:** an end-to-end path through the full product. Test vocabulary must match
the root TestSpec — user-visible / business-visible state only. No internal class names,
no HTTP status codes, no internal API terms in assertions.

**Environment:** root tests use the environment named in `preconditions:`. This is
typically a production-like environment or a named staging tier. The test does not spin up
individual components — it assumes the environment is running.

**Persona and tenant:** `preconditions:` names a persona and a test tenant. Wire these as
named constants or test fixture references at the top of the test. Do not hard-code
anonymous values — the name must match the TestSpec.

**Steps translation:** each `steps:` item is a user-visible action. Translate to driver
calls at the highest available abstraction (e.g., a UI driver action like `signUp(email)`,
or an API call framed in user vocabulary like `createProject(name)`). Never translate a
root step into a low-level HTTP call unless the project has no higher abstraction layer.

**Expected translation:** each `expected:` item is a business / user-visible outcome.
Translate to:

- A query against the system's observable state (e.g., `assertTenantExists(tenantId)`)
- A side-effect check (e.g., `assertEmailSent(to: email, within: 60s)`)
- A timing bound (e.g., assert elapsed time or latency percentile)

Do not assert on internal implementation details. If you find yourself asserting on
database table contents or internal flags, refactor to an observable facade.

**Timing bounds:** if `expected:` specifies a timing bound (`<= 5 min p95`), render an
assertion that measures elapsed time and fails if the bound is exceeded. Use the project's
timing utility if one exists; otherwise use a plain timestamp delta.

---

## Layer mismatch tells

If you observe any of the following during rendering, stop and report before proceeding:

| Observation | What it signals |
|---|---|
| Leaf case requires 3+ test doubles | Over-coupling; design may need revisiting. HALT #6. |
| Branch case has only `inputs:` with no `preconditions:` | Branch test underweight — it is a leaf test in disguise; wrong layer |
| Root case `expected:` contains class names or HTTP status codes | Root case using internal vocabulary; re-cast or move to branch layer |
| Root case `steps:` contain raw HTTP calls | Wrong abstraction level for root; use higher-level driver |
| Branch case `verifies:` points only at DD fields | Wrong granularity — branch verifies Architecture interfaces/composition |
