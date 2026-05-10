# Feedback Taxonomy

Full rejection type definitions. Used by review-execution when populating `failures[].type` in `feedback.yaml`. Also consumed by implement-leaf to understand what kind of fix is required (mirror at `vmodel-skill-implement-leaf/references/fix-mode-taxonomy.md`).

**Contents.** §1 Rejection Type Table · §2 Type Exclusivity Rules ·
§3 `required_fix` Discipline · §4 How impl-leaf Responds to Each Type ·
§5 Attempt Counter and Escalation Trigger.

---

## §1 Rejection Type Table

| Type | Layer(s) | Definition | What impl-leaf must do |
|:-----|:---------|:-----------|:----------------------|
| `contract-violation` | leaf | Implementation does not honour a DD contract element: a precondition is not enforced, a postcondition's result property is not achieved, an error class is not raised, or thread-safety is not demonstrated. The DD is correct; the code is the problem. | Fix the implementation to enforce the violated contract element. `required_fix` will name the contract element (precondition name, postcondition property, error class, or thread-safety category). |
| `scope-violation` | leaf | Implementation contains behaviour not sanctioned by the DD: a public method with no DD counterpart, a side-effect not declared, or a dependency import not permitted by the DD's context. | Remove or move the unsanctioned behaviour. Do not extend the DD to cover it — the DD is the scope boundary. |
| `missing-implementation` | leaf | A DD function, error class, or data structure is entirely absent from the implementation. | Add the missing implementation. `required_fix` will name the missing element and its DD location. |
| `wrong-assertion-is-impl-bug` | leaf | A test assertion is wrong, but the error source is the implementation, not the TestSpec. Specifically: the impl produces an output that triggered the reviewer to look at the assertion; the assertion is actually correct per the DD; the impl is the problem. | Fix the implementation so it produces the output the (correct) assertion expects. Distinguish from ESCALATE: if the assertion contradicts the DD, that is an escalation; if the impl produces the wrong output so the assertion fails even though it is correct, that is this type. |
| `integration-failure-impl-bug` | branch | A child leaf passed all unit tests but is producing incorrect behaviour at the integration seam. The ARCH interface contract is correct; the child's unit tests did not cover the relevant seam case. | Re-implement the named child leaf to honour the integration-seam behaviour. `required_fix` will name the child scope and the interface method/event that is failing. |
| `regression` | any | A test that previously passed in this build run now fails, with no change to the relevant spec. The implementation introduced a regression. | Identify and revert the regression. `required_fix` will reference the previously passing test case id. |

---

## §2 Type Exclusivity Rules

One `failures` entry carries exactly one `type`. If a single location exhibits multiple issues, emit multiple entries (one per type) with the same `location`.

Types `contract-violation`, `scope-violation`, `missing-implementation`, and `wrong-assertion-is-impl-bug` are leaf-only. Do not emit them at branch or root layer reviews.

Type `integration-failure-impl-bug` is branch-only. Do not emit it at leaf or root.

Type `regression` is valid at any layer.

---

## §3 `required_fix` Discipline

`required_fix` must be concrete: a junior engineer reading it must know exactly what to change without further investigation.

Acceptable forms:
- "Add null-check guard for `userId` parameter before line 12 of `TokenValidator.validate()` per DD precondition `PRE-01`."
- "Remove `UserAuditLogger` import from `TokenValidator.java`; this dependency is not declared in the DD's context section."
- "Implement `TokenValidator.revoke(tokenId)` per DD function contract FC-03; method is absent from the implementation."
- "Fix `PaymentProcessor.charge()` to propagate `InsufficientFundsException` to the caller rather than swallowing it; ARCH interface contract IFACE-07 requires propagation."

Unacceptable forms:
- "Fix the error handling." (not concrete)
- "The implementation is wrong." (not actionable)
- "See the DD." (does not name the specific element)

---

## §4 How impl-leaf Responds to Each Type

This section is informational — it describes what the downstream implement-leaf skill does when it reads a `feedback.yaml` of each type. Review-execution does not implement; it routes.

| Type | Impl-leaf response |
|:-----|:------------------|
| `contract-violation` | Reads `location` + `required_fix`; adds or corrects the contract enforcement at the named location |
| `scope-violation` | Reads `location` + `required_fix`; removes or relocates the unsanctioned code element |
| `missing-implementation` | Reads `required_fix`; adds the named implementation element from the DD |
| `wrong-assertion-is-impl-bug` | Reads `location` + `required_fix`; fixes the impl output so the correct assertion passes |
| `integration-failure-impl-bug` | Reads `location` (names the child scope) + `required_fix` (names the failing interface method); re-implements the named seam behaviour in the child scope |
| `regression` | Reads `required_fix` (references the previously-passing test case); identifies and reverts the change that caused the regression |

---

## §5 Attempt Counter and Escalation Trigger

The orchestrator tracks `attempt` count per task. If `review_attempts >= build.max_review_attempts` and the verdict is still REJECTED, the orchestrator escalates automatically. Review-execution does not manage this counter — it reads `attempt` from `current-task.yaml` and writes it into `feedback.yaml` for the orchestrator's use.

`feedback.yaml` always includes the current `attempt` value so the orchestrator can compare against `max_review_attempts` without reading two files.
