---
name: vmodel-skill-render-tests
description: Translate a TestSpec artifact into executable test code (TDD red phase). Layer-aware — leaf TestSpec produces unit tests, branch TestSpec produces integration tests across child components, root TestSpec produces system/acceptance tests. Mechanical translation from TestSpec cases (with oracles, fixtures, coverage bar) into the project's configured test framework, preserving traceability via VERIFIES comments. Use when starting implementation of a leaf or running integration/system test stages of the build flow. Triggers — render tests, generate test code from testspec, TDD red phase, write integration tests from architecture testspec, write system tests from root testspec.
type: skill
---

# Render tests from TestSpec

Translate a TestSpec artifact into executable test code. The TestSpec already specifies cases
with named oracles, fixture descriptions, and a coverage bar — this skill is mechanical
translation into the project's test framework. The skill does not derive new cases and does not
add tests not grounded in a TestSpec case.

Output is in TDD red phase: tests compile but fail because no implementation exists yet.

## When to use

Activate this skill when the user asks to:

- Render test code from a TestSpec (any layer)
- Generate unit tests from a leaf TestSpec and its Detailed Design
- Generate integration tests from a branch TestSpec and its Architecture
- Generate system / acceptance tests from a root TestSpec and root Requirements
- Start the TDD red phase for a scope
- Turn testspec cases into runnable test files

Do **not** activate this skill for:

- Deriving or authoring TestSpec cases — that is `vmodel-skill-author-testspec`'s job
- Reviewing a TestSpec for quality — that is `vmodel-skill-review-testspec`'s job
- Writing implementation code — that is `develop-code`'s job
- Reviewing rendered tests against a design — that is `vmodel-skill-review-code`'s job

## Inputs

Expected context (ask if missing):

- **TestSpec artifact** — the `.md` file with YAML front-matter and per-case YAML blocks
- **Layer** — leaf / branch / root (derivable from TestSpec `level:` field; confirm if ambiguous)
- **Parent spec for the layer** (ask if not provided):
  - Leaf: the Detailed Design (`detaileddesign.md`)
  - Branch: the Architecture (`architecture.md`)
  - Root: root Requirements (`requirements.md`)
- **`.vmodel/config.yaml`** — resolved automatically from project root; provides `commands.*`
  and `paths.tests`

If the TestSpec file is not provided, HALT and ask.

## Authoring procedure

Read `references/layer-rendering.md` and `references/oracle-to-assertion.md` before
starting. Read `references/language-idioms.md` for the detected project language.

### Step 1 — Load config and detect layer

1. Read `.vmodel/config.yaml`. Record:
   - `paths.tests` — output directory for test files
   - `commands.test_unit` — used to compile-check leaf tests
   - `commands.test_integration` — used to compile-check branch tests (fall back to
     `test_unit` if absent)
   - `commands.test_system` — used to compile-check root tests (fall back to `test_unit`
     if absent)
   - Language (from `language:` field or inferred from `commands.test_unit`)

2. Read the TestSpec front-matter. Resolve layer from `level:`:
   - `unit` → leaf
   - `integration` → branch
   - `system` → root

### Step 2 — Read TestSpec cases

Parse every `cases:` block. For each case, extract:

- `id` — traceability anchor (becomes the `VERIFIES` comment value)
- `title` — becomes test function/method name (snake_case or camelCase per language idiom)
- `type` — functional / boundary / error / property / state-transition / fault-injection /
  contract / performance / security / accessibility
- `verifies` — upstream IDs (all IDs go in the `VERIFIES` comment)
- `inputs` (leaf) — direct parameter values
- `expected` — oracle; drives assertion translation
- `preconditions` (branch/root) — fixture and environment setup
- `steps` (branch/root) — ordered actions

If any case has a missing or qualitative-only `expected:` (e.g., `"verifies behaviour"`,
`"does not throw"`, `"non-null"`), HALT. The TestSpec must be revised before rendering.
See HALT conditions.

### Step 3 — Translate each case to test code

For each case, apply the rules in `references/oracle-to-assertion.md`:

- Specific value → equality assertion with the exact value
- Bounded predicate (`"result <= 50ms"`, `"result is non-descending"`) → bounded assertion
  or property check
- Enumerated set → assertion against a fixed collection
- Error / exception → assertion that the correct error type and (if specified) message is raised
- State-transition → drive the state machine, assert terminal state and any side effects

Test structure follows `references/language-idioms.md` for the detected language.

Every rendered test must carry a `VERIFIES` comment immediately before or inside the test
function. Format: `// VERIFIES: <case-id> → <verifies-ids-comma-separated>`. Language comment
syntax applies (see `references/language-idioms.md`).

Naming convention: test name = `test_<case_title_slug>` (snake_case) or `test<CaseTitlePascal>`
(camelCase) per language idiom. Case title is the authoritative source; do not invent names.

### Step 4 — Layer-specific wiring

Read `references/layer-rendering.md` §Leaf / §Branch / §Root as applicable.

**Leaf:** Wire the public interface of the unit under test directly. Stub only infrastructure
collaborators (at most 2 test doubles). If the parent DD names specific collaborators with
defined contracts, stub those contracts exactly — do not invent behaviour.

**Branch:** Wire the composition per the Architecture's `composition:` section. For each child
component cited in preconditions, create a test double at the described fidelity level
(dummy / stub / spy / mock / fake). For fakes, insert a `// CONTRACT: <child-component>` comment
naming the component whose contract the fake honours.

**Root:** Wire an end-to-end path: use the environment, persona, and feature-flag preconditions
from the TestSpec. Steps translate to sequential driver actions. Expected items translate to
assertions on user-visible or business-visible state only (no internal API terms in root tests).

### Step 5 — Group and write test files

Grouping rule per `references/language-idioms.md`:
- Go: one `_test.go` file per package, grouped by suite name from the TestSpec
- Python: one `test_<scope>.py` file per scope
- Java/JUnit 5: one `<ScopeName>Test.java` class per scope; nested classes for branch/root
  suites
- TypeScript/Vitest: one `<scope>.test.ts` file per scope

Write test files to `<paths.tests>/<scope>/`. Do not flatten the scope tree.

### Step 6 — Compile-check (red phase verification)

Run the compile-only form of the appropriate test command:

- Leaf: `<commands.test_unit>` (compile-check mode or dry-run)
- Branch: `<commands.test_integration>` (fall back to `test_unit`)
- Root: `<commands.test_system>` (fall back to `test_unit`)

Tests must compile without errors. If compilation fails, fix the test code — do not relax the
assertion or stub. Do not change the oracle to match a broken implementation.

Tests must fail (red phase). If a test passes before any implementation exists, the test is
wrong — the assertion is either tautological or the scope already has an implementation.
Investigate and fix.

### Step 7 — Write render report

Write `.vmodel/.build/tasks/<task-id>/render-report.yaml`. Derive `<task-id>` from TestSpec `id`
field + timestamp (`<ts-id>-render`).

Schema:

```yaml
task_id: <ts-id>-render
testspec_id: <id from front-matter>
scope: <scope from front-matter>
layer: <leaf | branch | root>
rendered:
  - case_id: TC-NNN
    test_function: test_<name>
    file: <relative path from paths.tests>
    verifies:
      - <upstream-id>
skipped:
  - case_id: TC-NNN
    reason: <one-line reason — e.g., "performance test: deferred to load-test stage">
test_files_produced:
  - <relative path from project root>
compile_check: <passed | failed>
red_phase_check: <all_red | some_green | not_run>
notes: ""
```

## Self-check before delivering

1. Every case in the TestSpec has either a rendered test or a skipped entry with reason.
2. Every rendered test has a `VERIFIES` comment with case ID and upstream IDs.
3. Every assertion uses a hardcoded expected value from the TestSpec — no logic recomputation.
4. No test passes before implementation exists (red phase intact).
5. Test names come from TestSpec `title:` — no invented names.
6. Test doubles are limited to 2 at leaf; named and contract-annotated at branch/root.
7. No tests exist that are not derived from a TestSpec case.

## HALT conditions

Stop and report the condition if:

1. TestSpec file is not provided.
2. Any case has a weak oracle: qualitative-only `expected:` (`"verifies behaviour"`,
   `"non-null"`, `"does not throw"` as the sole assertion basis). The TestSpec review skill
   should have caught this; if not, report and halt. Do not render a placeholder assertion.
3. Oracle is ambiguous beyond bounded predicates — you cannot determine what assertion to write
   without guessing. Request TestSpec revision with a specific `expected:` value.
4. A test passes before implementation exists and there is no pre-existing implementation to
   explain it. The oracle may be wrong; halt and ask.
5. The parent spec contradicts the TestSpec case (e.g., an input range in the TestSpec exceeds
   the DD's documented constraint). Report the discrepancy; do not silently clip the value.
6. You need to mock more than 2 collaborators at leaf layer — this signals a design coupling
   problem. Report and ask whether to proceed or fix the design first.
