# Verdict Decision Tree

Apply rows in order. First match wins. This tree determines REJECTED vs ESCALATE and populates `type`/`target_layer`/`issue_type`/`confidence` in the output file.

When no row matches and tests are failing, emit ESCALATE with `confidence: low` and `issue_type: ambiguity` rather than guessing REJECTED. This surfaces to the human.

---

## Tree

| Row | Condition | Verdict | `type` / `target_layer` | `issue_type` | `confidence` | Notes |
|:----|:----------|:--------|:------------------------|:------------|:-------------|:------|
| 1 | Test assertion contradicts the DD's contract for the function under test (assertion expects value X, DD postcondition says Y, and DD is unambiguous) | **ESCALATE** | testspec | wrong-assertion | high | The test is wrong, not the impl. Impl cannot be fixed to satisfy both the test and the DD. |
| 2 | Test passes but implementation does not enforce a DD precondition (guard clause absent, boundary not checked) | **REJECTED** | — | contract-violation | high | Impl is fixable: add the guard. Spec is correct. |
| 3 | Test passes but implementation does not satisfy a DD postcondition observable by tests (outcome property not achieved) | **REJECTED** | — | contract-violation | high | Impl is fixable. Spec is correct. |
| 4 | Test fails and the implementation can be rewritten to satisfy the failing test without changing the DD | **REJECTED** | — | missing-implementation | high | Impl gap, not spec gap. |
| 5 | DD is ambiguous: two or more valid implementations exist that each satisfy all DD postconditions but produce different observable behaviour (tests fail on one valid interpretation) | **ESCALATE** | detailed-design | ambiguity | high | DD must be sharpened before impl can be correct. |
| 6 | DD is impossible: no implementation can simultaneously satisfy two or more DD postconditions (logical contradiction) | **ESCALATE** | detailed-design | contradiction | high | DD must be revised before impl can proceed. |
| 7 | DD is unambiguous and satisfiable but contradicts a governing ADR (e.g., DD specifies a synchronous call where the governing ADR mandates async messaging) | **ESCALATE** | adr | new-decision-needed | high | A new or revised ADR is needed; DD then follows. |
| 8 | Branch integration fails: all child unit tests passed, but the assembled interface is inconsistent with what ARCH declares as the boundary contract | **ESCALATE** | architecture | contract-violation | high | ARCH's Composition or Interface section declared a contract the children cannot honour. |
| 9 | Branch integration fails: a specific child leaf passed unit tests but is buggy at the integration seam (its unit tests did not cover the relevant seam case) | **REJECTED** | — | integration-failure-impl-bug | high | Re-trigger that leaf's implement-leaf in fix mode. Name the leaf scope in `required_fix`. |
| 10 | Branch integration fails and both rows 8 and 9 could apply (unclear whether ARCH or impl is the source) | **ESCALATE** | architecture | ambiguity | low | Surface to human. Do not guess. |
| 11 | Root system test fails: outcome specified in a root requirement was not met by the assembled system | **ESCALATE** | requirements | gap | high | The requirement's outcome was not achievable or was not tested. |
| 12 | Root system test fails: the root product artifact (PB/needs/PD) specifies a critical need that was never translated into a requirement | **ESCALATE** | product | gap | high | A need fell through the requirements layer. |
| 13 | Root system test fails: failure traces to a cross-cutting architectural decision, not a missing or incorrect requirement | **ESCALATE** | architecture | new-decision-needed | high | A root-level architectural concern was not captured. |
| 14 | Root TestSpec case asserts an outcome that contradicts the root requirement it is supposed to verify | **ESCALATE** | testspec | wrong-assertion | high | The test is wrong; requirement is the reference. |
| 15 | Any layer: a test that previously passed now fails with no change to the relevant spec (regression) | **REJECTED** | — | regression | high | Impl introduced a regression. Impl is fixable. |
| 16 | Test fails; failure mechanism is unclear; multiple rows partially apply | **ESCALATE** | nearest in-lane target | ambiguity | low | Surface to human. State which rows partially match and why disambiguation was not possible. |

---

## Confidence Rules

| Confidence | When to use |
|:-----------|:-----------|
| `high` | One row matches cleanly. Evidence directly supports the routing. |
| `medium` | One row matches but the evidence is indirect (e.g., inferred from log output, not from spec text). Cite the inference. |
| `low` | Multiple rows partially match, or the failure mechanism is ambiguous, or the row's condition requires judgement beyond what the evidence directly supports. Always use `low` for cross-lane suspicions. |

Orchestrator auto-routes `high`. Human surfaces `low` and `medium` depending on `build.auto_route_medium` config flag (default: false — surface both medium and low to human).

---

## REJECTED vs ESCALATE Quick Reference

**REJECTED when:**
- The spec is correct.
- A conforming implementation exists (you can describe what it would look like even if you can't write it).
- The fix is in the code, not the spec.

**ESCALATE when:**
- The fix requires changing a spec artifact.
- No conforming implementation is possible given the current spec.
- The failure reveals a decision that has not been captured in any spec layer.
- Ambiguity makes it impossible to determine which of the above applies (use `confidence: low`).
