# Per-Layer Review

What each layer reviews, what it compares against, and which verdict types are in-lane.

**Contents.** §1 Layer Summary Table · §2 Leaf Layer Review · §3 Branch Layer
Review · §4 Root Layer Review · §5 Lane Discipline.

---

## §1 Layer Summary Table

| Layer | Triggered by `task_type` | Reads (spec) | Reads (impl/results) | Failure routes to |
|:------|:------------------------|:-------------|:---------------------|:-----------------|
| **leaf** | `implement-leaf` | DD + leaf TestSpec | impl code (git diff) + unit test results | DD revision OR TestSpec revision |
| **branch** | `integration-test` | branch ARCH + branch TestSpec | integration test results | ARCH revision OR child DD/TS revision |
| **root** | `system-test` | root REQ + root product artifact + root TestSpec | system/acceptance test results | Requirements revision OR root product revision OR ARCH revision |

---

## §2 Leaf Layer Review

### What is under review

The leaf layer reviews one leaf scope: the implementation of a single component as allocated in its parent architecture.

### What it checks against

- **Detailed Design (DD)**: The binding spec for the leaf. All public-interface contracts (preconditions, postconditions split by outcome, invariants, error matrix, thread-safety category) are the reference.
- **Leaf TestSpec**: The test cases derived from the DD. Verifies that the tests exercised are the ones specified (no missing cases, no phantom cases).

### What a leaf reviewer does NOT do

- Does not look at sibling DDs or the parent architecture. The parent architecture's interface contracts are frozen at the ARCH layer; the leaf DD references them by ID. Any mismatch between a sibling's interface and this leaf's expectation is a branch-layer problem.
- Does not check integration behaviour. Unit tests only.
- Does not route failures to architecture. Leaf → DD or TestSpec only.

### In-lane verdict types at leaf

| Verdict | In-lane? |
|:--------|:---------|
| APPROVED | yes |
| REJECTED / contract-violation | yes |
| REJECTED / scope-violation | yes |
| REJECTED / missing-implementation | yes |
| REJECTED / wrong-assertion-is-impl-bug | yes — when the test assertion logic is wrong but the error is in the impl, not the spec |
| REJECTED / regression | yes |
| ESCALATE → testspec | yes — when a test assertion contradicts the DD contract |
| ESCALATE → detailed-design | yes — when DD is ambiguous or impossible to satisfy |
| ESCALATE → adr | yes — when DD is unambiguous but contradicts a governing ADR |
| ESCALATE → architecture | **NO** — out-of-lane at leaf |
| ESCALATE → requirements | **NO** — out-of-lane at leaf |
| ESCALATE → product | **NO** — out-of-lane at leaf |

---

## §3 Branch Layer Review

### What is under review

Integration test results across the children of one branch scope. All child leaf scopes are already `completed`; this stage verifies that their assembled interfaces work together per the ARCH composition contract.

### What it checks against

- **Branch Architecture (ARCH)**: The Composition and Interface sections are the reference. Every component boundary declared in the ARCH (data-flow contracts, call sequences, error propagation rules) must be observable in the integration results.
- **Branch TestSpec**: The integration test cases derived from the ARCH. Verifies coverage of interface contracts.

### What a branch reviewer does NOT do

- Does not re-review leaf implementation. Unit tests are complete; this stage looks only at integration seams.
- Does not route to root Requirements. Root-outcome failures belong to the root stage.

### In-lane verdict types at branch

| Verdict | In-lane? |
|:--------|:---------|
| APPROVED | yes |
| REJECTED / integration-failure-impl-bug | yes — a child leaf passed unit but is buggy at the integration seam |
| REJECTED / regression | yes |
| ESCALATE → architecture | yes — interface contract mismatch; the ARCH declared the contract wrong |
| ESCALATE → detailed-design (child leaf) | yes — a specific leaf's DD is inconsistent with the interface it is supposed to implement |
| ESCALATE → testspec (branch) | yes — branch TestSpec case is wrong |
| ESCALATE → adr | yes — if the mismatch traces to a cross-cutting decision that was not captured in an ADR |
| ESCALATE → requirements | **NO** — out-of-lane at branch |
| ESCALATE → product | **NO** — out-of-lane at branch |

### Identifying the correct ESCALATE target at branch

When integration fails:

1. Is the ARCH's interface contract itself inconsistent or missing? → ESCALATE to architecture.
2. Is the ARCH contract correct but a specific child's DD mis-specifies how it fulfils the interface? → ESCALATE to the specific child's detailed-design. Name the child scope in `target_artifact`.
3. Is the interface contract correct and the DD correct but the test case asserts the wrong behaviour? → ESCALATE to testspec.
4. Does the mismatch trace to an ADR that needs a new decision (e.g., protocol upgrade)? → ESCALATE to adr.
5. Is the ARCH correct, the DD correct, the test case correct, and the impl just buggy? → REJECTED / integration-failure-impl-bug.

---

## §4 Root Layer Review

### What is under review

System/acceptance test results at the root scope. All branch stages are complete; this stage verifies that the assembled system meets the stated product outcomes.

### What it checks against

- **Root Requirements (requirements.md)**: Every requirement outcome must have at least one system test that exercises it. Uncovered requirement outcomes are a finding.
- **Root product artifact** (whichever of `product_brief.md`, `needs.md`, `pd.md` is present): Verifies that the critical needs/outcomes expressed in the product artifact are not silently unverified.
- **Root TestSpec**: The system test cases derived from the requirements. Verifies coverage.

### What a root reviewer does NOT do

- Does not attribute root failures to individual branch architectures unless the evidence clearly traces there (e.g., a system test failure in a sub-system that is fully owned by one branch architecture).

### In-lane verdict types at root

| Verdict | In-lane? |
|:--------|:---------|
| APPROVED | yes |
| REJECTED / regression | yes |
| ESCALATE → requirements | yes — system test failure traces to a requirement that is unachievable or contradictory |
| ESCALATE → product | yes — root product artifact's need was never translated into a requirement |
| ESCALATE → architecture | yes — failure traces to a cross-cutting architectural decision, not a missing requirement |
| ESCALATE → adr | yes — new cross-cutting decision needed |
| ESCALATE → testspec (root) | yes — root TestSpec case asserts wrong outcome |
| ESCALATE → detailed-design | **NO** — out-of-lane at root (too many hops; route to architecture first) |

---

## §5 Lane Discipline

The lane rules are hard constraints, not defaults:

- A leaf reviewer who suspects an architecture issue must emit ESCALATE with `confidence: low` targeting `testspec` or `detailed-design` (the nearest in-lane target) and note the suspected upstream source. The branch reviewer, when that scope runs, will pick up the architecture signal.
- A branch reviewer who suspects a root-requirement issue emits ESCALATE with `confidence: low` targeting `architecture` (nearest in-lane). The root reviewer closes the loop.
- "Confidence: low" triggers human surface in the orchestrator rather than auto-routing. This is the correct safety valve for cross-lane suspicions.
