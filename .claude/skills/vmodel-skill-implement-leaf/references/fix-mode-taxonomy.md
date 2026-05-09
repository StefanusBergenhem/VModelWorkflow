---
purpose: Rejection taxonomy and per-type response for fix mode.
audience: vmodel-skill-implement-leaf
status: active
---

# Fix Mode Taxonomy

**Contents.** Activating fix mode · feedback.yaml shape · Taxonomy table ·
Per-type response detail · Retry counter · Escalation protocol · Cross-links.

---

## 1. Activating fix mode

Fix mode activates when `.vmodel/.build/<task-id>/feedback.yaml` exists and the
user invokes the skill after a prior review-execution rejection. If
`feedback.yaml` is absent and the user asks to fix, issue refusal C.

Read `feedback.yaml` completely before acting. Do not address entries
piecemeal — understand the full rejection set first, then plan the fix sequence
in dependency order (contract violations before scope violations; missing
implementations last).

---

## 2. feedback.yaml shape

The `feedback.yaml` is produced by `vmodel-skill-review-execution`. Expected structure:

```yaml
task_id: build-<scope>
build_run_id: <id>
verdict: REJECTED                         # always REJECTED in fix mode
attempt: <n>                              # 1-based; equals max_review_attempts when exhausted
findings:
  - id: F-001
    type: <taxonomy-type>                 # see taxonomy table
    location: <file:line or function-name>
    description: <human-readable text>
    dd_clause: <DD-scope.function or DD-scope.data_structure>  # optional
    test_ref: <test-case-id>             # optional; present for wrong-assertion
```

If `feedback.yaml` is structurally malformed, HALT and request a corrected file.

---

## 3. Taxonomy table

| Type | What it means | Who fixes it |
|---|---|---|
| `wrong-assertion` | Test code asserts a property the DD does not specify, or asserts the wrong value for a DD-specified property | `vmodel-skill-render-tests` / `vmodel-skill-author-testspec` — NOT this skill |
| `missing-implementation` | A DD contract (interface entry, algorithm, error case) has no corresponding implementation | This skill — add the missing code per DD |
| `contract-violation` | Implementation produces output or behaviour that contradicts a DD contract (wrong postcondition, wrong error type, wrong invariant) | This skill — rewrite the violating path |
| `scope-violation` | Implementation contains behaviour not specified in the DD (extra feature, extra method, extra side effect) | This skill — remove the extra; flag in notes |
| `integration-failure` | Unit-level tests pass but composition with siblings fails at the seam | Architecture review — escalate (refusal H); this layer cannot fix integration |

---

## 4. Per-type response detail

### wrong-assertion

**Do NOT** modify the implementation to make a wrong test pass.
**Do NOT** delete or disable the test.

Action: surface refusal G. Include:
- Finding ID from `feedback.yaml`
- The assertion that is wrong
- The DD clause it should be derived from
- Recommendation: re-invoke `vmodel-skill-render-tests` for the affected case

The implementation may be correct. The test is the problem. This skill does not
own test code.

### missing-implementation

Locate the DD clause cited in `dd_clause`. Implement the missing code:
- If it is a public interface entry: add the method/function with full contract
  (precondition guards, postcondition production, typed error paths).
- If it is an algorithm: add the function body implementing the result property.
- If it is an error case: add the guard and the typed error.
- If it is a state transition: add the transition handler.

Re-run tests after each `missing-implementation` entry is addressed. Do not
batch all entries then run tests once — earlier fixes may reveal further
failures that narrow the remaining work.

### contract-violation

Locate the implementation path identified in `location`. Rewrite it to satisfy
the DD contract in `dd_clause`. Common patterns:

| Violation | Fix |
|---|---|
| Wrong postcondition on success | Rewrite the return/mutation logic to produce the DD's guaranteed post-state |
| Wrong postcondition on failure | Ensure the failure path returns the DD's typed error without additional side effects |
| Invariant broken by mutation | Add the invariant enforcement to the mutation site |
| Wrong thread-safety (Goetz category) | Restructure to match the DD's stated category |
| Wrong error type thrown | Change to the typed enum/class specified in the error matrix |

After rewriting, verify no other entry now violates a different contract.

### scope-violation

Locate the extra code identified in `location`. Remove it entirely. Do not
move it to a helper that the DD doesn't call; do not add it to the DD. The DD
is the spec; features not in the DD are not implemented here.

In `review-ready.yaml`'s `notes:` field, cite the finding ID and confirm
removal: `"F-003 scope-violation: removed <name>; not in DD-<scope>."`.

If the user insists the feature is needed: HALT (refusal F). The path is to add
it to the DD first.

### integration-failure

This type cannot be resolved at the leaf implementation layer. The leaf
satisfies its own contracts; the integration failure is a seam-level concern.

Action: surface refusal H. Include:
- Finding ID(s) from `feedback.yaml`
- Which seam is failing (from the finding)
- Recommendation: architecture review of the seam at the parent scope

Do not modify the implementation to paper over integration failures.

---

## 5. Retry counter

Read `build.retry.max_review_attempts` from `.vmodel/config.yaml`.
Default if absent: `3`.

The `attempt` field in `feedback.yaml` is the prior review round (1-based).
The current fix attempt is `attempt + 1`.

If `attempt + 1 > max_review_attempts` AND any findings of type
`missing-implementation`, `contract-violation`, or `scope-violation` remain
unresolved after this fix attempt:

Activate refusal E. Do not emit `review-ready.yaml`. Surface:

```
HALT — max_review_attempts exhausted.
Unresolvable findings:
  <list finding IDs + types>
Recommended escalation:
  - contract-violation / missing-implementation at DD clause X → DD revision
  - integration-failure → architecture review at parent scope
```

---

## 6. review-ready.yaml in fix mode

After a successful fix (all tests pass, pre-publish self-check clean):

- Set `notes:` to reference each addressed finding: `"F-001 contract-violation
  addressed: <what changed>. F-003 scope-violation: removed <name>."`.
- If any finding was escalated (wrong-assertion, integration-failure), list it
  in `notes:` with escalation target.
- Increment nothing in `review-ready.yaml` — the `build_run_id` is unchanged.

Template: `templates/review-ready.yaml.tmpl`.

---

## Cross-links

`tdd-green-and-refactor.md` · `contract-implementation.md` · `SKILL.md`
(refusal table, fix mode summary)
