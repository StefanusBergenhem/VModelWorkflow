# Example — APPROVED review of the dequeue-service DD

The reviewer is given the canonical good DD for the dequeue-service from the matched author skill's worked example (greenfield; leaf inside `app/jobs`; parent Architecture `ARCH-app-jobs`; one governing ADR `ADR-017`).

The reviewer was given the DD, the parent Architecture, the governing ADR, and the upstream requirement (`REQ-app-jobs-004`). The reviewer applied the implementer and tester perspectives. Anti-pattern sweep found nothing. Spec Ambiguity Test passed.

## Verdict block

```yaml
review:
  document: /specs/app/jobs/dequeue-service/detailed_design.md
  reviewer: vmodel-skill-review-detailed-design
  date: 2026-04-30

  verdict: APPROVED

  inputs_provided:
    detailed_design_document: true
    parent_architecture: true
    governing_adrs: true
    derived_from_artifacts: true

  perspectives_applied:
    - implementer
    - tester

  findings:
    - id: F-001
      element_id: GLOBAL
      check_failed: check.adr.governing-not-cited-in-body
      severity: info
      category: adr
      evidence: |
        ADR-017 is cited at three body points: in the Overview ("per ADR-017"), in
        the Algorithms section rationale ("per ADR-017"), and in the Error Handling
        notes ("per ADR-017 the write is idempotent"). Citation discipline is
        exemplary. Included as a positive observation.
      recommended_action: |
        No action — citation discipline is exemplary.

    - id: F-002
      element_id: completeJob
      check_failed: check.contract.thread-safety-unstated
      severity: info
      category: function-contract
      evidence: |
        completeJob declares `thread_safety: thread-safe`. The Claim is owned by
        the calling worker; concurrent calls with different Claims are safe;
        concurrent calls with the same Claim raise UnknownClaim on the second.
        Behaviour is correct; the contract could optionally name the
        same-Claim-concurrent edge case explicitly. No defect.
      recommended_action: |
        No action — thread-safety category is named per the function-contract-checks.md
        rule. Optional refinement noted only.

  summary: |
    Verdict: APPROVED. The dequeue-service DD passes every applicable Quality Bar
    item and the Spec Ambiguity Test. All seven sections are present with
    substantive content (the State section is one line — explicit assertion of
    statelessness). Both public functions carry the 9 contract elements;
    postconditions are split by outcome with both branches populated; both halves
    of transformation properties (e.g., the on_success guarantee that the row's
    `locked_until` is advanced AND no other worker holds the lock) are stated.
    The Claim data structure is specified by invariant. The error-handling matrix
    has five rows, each with a recovery strategy from the closed enum; the
    bounded retry budget is stated. ADR-017 is the only governing ADR; it
    resolves and is body-cited at three points. Two info-level observations
    noted; no defects.

  recommended_next_action: |
    Proceed to TestSpec authoring against this DD's contract clauses, error
    matrix, and Claim invariants. Implementation can begin in parallel using
    `develop-code` against this DD.

  counts:
    hard_reject: 0
    soft_reject: 0
    info: 2
    design_issue: 0
```

## What this example demonstrates

1. **APPROVED is not silent.** Two info-level observations are surfaced. They do not affect the verdict but are useful to the consumer of the verdict for ongoing maintenance.

2. **Findings cite specific elements.** F-001 ties to "GLOBAL" because it observes a document-wide ADR-citation property; F-002 ties to a specific function (`completeJob`).

3. **Recommended actions are generic and point to the rule.** No specific replacement wording. The matched author skill rewrites; this skill signals.

4. **The summary cites the dominant signal.** It names the load-bearing pieces (sections, contracts split, both halves stated, matrix populated) and confirms what the Spec Ambiguity Test passed against.

5. **Counts are explicit.** Zero soft_reject, zero hard_reject; only info findings — the verdict is conservative and well-grounded.

6. **Two perspectives applied — implementer and tester.** Greenfield (no `recovery_status:` declared) → historian perspective is not load-bearing.

7. **All inputs were provided.** Traceability checks could be run; ADR resolved; parent Architecture's leaf-allocation matched the DD's surface; `derived_from` resolves.

8. **Recommended next action points forward, not back.** APPROVED → "proceed to TestSpec authoring + implementation". The verdict is read by orchestration that needs to know what to do next.
