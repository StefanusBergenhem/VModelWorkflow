---
purpose: Rejection taxonomy and per-type response for fix mode. Mirrors the producer side of the contract — `vmodel-skill-review-execution` emits `feedback.yaml` with this exact shape and these exact type names.
audience: vmodel-skill-implement-leaf
status: active
---

# Fix Mode Taxonomy

**Contents.** Activating fix mode · feedback.yaml shape · Taxonomy table ·
Per-type response detail · Retry counter · review-ready.yaml in fix mode ·
Cross-links.

---

## 1. Activating fix mode

Fix mode activates when `.vmodel/.build/tasks/<task-id>/feedback.yaml` exists
and the user (or orchestrator) invokes the skill after a prior
review-execution rejection. If `feedback.yaml` is absent and the user asks to
fix, issue refusal C.

Read `feedback.yaml` completely before acting. Do not address entries
piecemeal — understand the full rejection set first, then plan the fix
sequence in dependency order (contract violations before scope violations;
missing implementations last).

---

## 2. feedback.yaml shape

Produced by `vmodel-skill-review-execution`. Canonical shape (mirror of
`vmodel-skill-review-execution/templates/feedback.yaml.tmpl`):

```yaml
task_id: <task-id>
scope: <scope-path>
layer: leaf                              # always "leaf" for fix mode at this skill
verdict: REJECTED                        # always REJECTED in fix mode
attempt: <N>                             # current review-attempt count
reviewed_at: <ISO-8601-datetime>

failures:
  - type: <taxonomy-type>                # see taxonomy table — required
    location: <file:line>                # required — where the failure is
    description: <one-line description>  # required
    required_fix: <concrete next step>   # required — junior-implementable
    spec_ref: <element-id>               # optional — DD/ARCH ID violated

required_fixes_summary: |                # one-paragraph summary of all failures
  <prose summary>
```

If `feedback.yaml` is structurally malformed (missing `failures[]`, missing
required fields on a failure entry), HALT and request a corrected file.

---

## 3. Taxonomy table

Five types are emitted as REJECTED by review-execution at the leaf layer (the
`wrong-assertion` case where the test contradicts the DD is ESCALATED to
testspec instead — it never appears in `feedback.yaml`).

| Type | What it means | Who fixes it |
|---|---|---|
| `contract-violation` | Implementation produces output or behaviour that contradicts a DD contract (wrong postcondition, wrong error type, wrong invariant), OR a precondition guard is missing | This skill — rewrite the violating path |
| `scope-violation` | Implementation contains behaviour not specified in the DD (extra public method, extra side effect, dependency import not in the DD's context) | This skill — remove the extra; flag in notes |
| `missing-implementation` | A DD contract (Public Interface entry, error class, data structure) has no corresponding implementation | This skill — add the missing code per DD |
| `wrong-assertion-is-impl-bug` | The test assertion is correct per the DD; the implementation produced wrong output that made the assertion fail. The bug is in the impl, not the test. | This skill — fix the impl to produce the output the (correct) assertion expects |
| `integration-failure-impl-bug` | A child leaf passed unit tests but is buggy at the integration seam. ARCH contract is correct; this leaf's unit tests did not cover the relevant seam case. | This skill — re-implement the named seam behaviour. `required_fix` names the failing interface method/event. |
| `regression` | A test that previously passed now fails, with no change to the relevant spec. The implementation introduced a regression. | This skill — identify and revert the regression. `required_fix` references the previously-passing test case id. |

---

## 4. Per-type response detail

### contract-violation

Locate the implementation path identified in `location`. Rewrite it to satisfy
the DD contract identified in `spec_ref` (if present) or `required_fix`.
Common patterns:

| Violation | Fix |
|---|---|
| Missing precondition guard | Add the guard at the function entry per DD's stance (DbC assertion or defensive validation) |
| Wrong postcondition on success | Rewrite the return/mutation logic to produce the DD's guaranteed post-state |
| Wrong postcondition on failure | Ensure the failure path returns the DD's typed error without additional side effects |
| Invariant broken by mutation | Add the invariant enforcement to the mutation site |
| Wrong thread-safety (Goetz category) | Restructure to match the DD's stated category |
| Wrong error type thrown | Change to the typed enum/class specified in the error matrix |

After rewriting, verify no other entry now violates a different contract.

### scope-violation

Locate the extra code identified in `location`. Remove it entirely. Do not
move it to a helper that the DD doesn't call; do not add it to the DD. The DD
is the scope boundary.

In `review-ready.yaml`'s `feedback_addressed:` block, cite the location and
confirm removal: `"removed <name>; not in DD-<scope>."`.

If the user insists the feature is needed: HALT (refusal F). The path is to
add it to the DD first.

### missing-implementation

Locate the DD clause cited in `spec_ref` (or named in `required_fix`).
Implement the missing code:
- Public Interface entry → add the method/function with full contract
  (precondition guards, postcondition production, typed error paths).
- Algorithm → add the function body implementing the result property.
- Error class → add the guard and the typed error.
- State transition → add the transition handler.

Re-run tests after each entry is addressed. Do not batch all entries then run
once — earlier fixes may reveal further failures that narrow the remaining
work.

### wrong-assertion-is-impl-bug

The reviewer determined that the *test assertion* is correct per the DD; the
*implementation* produced wrong output that surfaced as an assertion failure.

Action: fix the implementation so it produces the output the assertion
expects. Trace from the assertion's expected value back through the DD to
verify the assertion is in fact correct, then correct the impl.

Distinguish from the ESCALATED case (`wrong-assertion` issue type, which goes
to testspec via ESC-NNN.yaml — never appears in `feedback.yaml`). The
reviewer routes those separately.

### integration-failure-impl-bug

The branch-layer reviewer determined that this leaf's impl is wrong at the
integration seam, even though its unit tests pass. The Architecture contract
is correct.

Action:
1. Read the child scope and interface method/event named in `required_fix`.
2. Re-read the parent Architecture's interface contract for that seam.
3. Re-implement the behaviour at the seam to honor the contract.
4. Add a regression-style unit test that covers the previously-uncovered seam
   case (this is part of the leaf's responsibility — the unit-test gap is
   what let the seam bug pass review).

Do not modify the integration test or the Architecture. The impl is the
problem.

### regression

A test that previously passed now fails. `required_fix` references the
previously-passing test case id. Identify which change in this fix attempt
(or in the prior implementation) broke the test, and revert or reshape that
change.

If the regression is structural (unavoidable consequence of another required
fix), HALT — this is an ADR or DD revision, not an impl fix.

---

## 5. Retry counter

Read `build.retry.max_review_attempts` from `.vmodel/config.yaml`. Default if
absent: `3`.

The `attempt` field in `feedback.yaml` is the prior review round. The current
fix attempt is `attempt + 1`.

If `attempt + 1 > max_review_attempts` AND any failures remain unresolved
after this fix attempt:

Activate refusal E. Do not emit `review-ready.yaml`. Surface:

```
HALT — max_review_attempts exhausted.
Unresolved failures:
  <list type + location + required_fix>
Recommended escalation:
  - contract-violation / missing-implementation at <spec_ref> → DD revision
  - integration-failure-impl-bug at <child>.<method> → architecture review
```

The orchestrator's escalation handler then writes the ESC-NNN.yaml.

---

## 6. review-ready.yaml in fix mode

After a successful fix (all tests pass, pre-publish self-check clean):

- Set `mode: fix` in the front matter.
- Populate the `feedback_addressed:` block. One entry per failure addressed,
  using the failure's `location` as the anchor (see template).
- `notes:` summarises the fix campaign in one paragraph; link to
  feedback.yaml's `required_fixes_summary` if useful.

Template: `templates/review-ready.yaml.tmpl`.

---

## Cross-links

`tdd-green-and-refactor.md` · `contract-implementation.md` · `SKILL.md`
(refusal table, fix mode summary) ·
`vmodel-skill-review-execution/references/feedback-taxonomy.md` (producer side)
