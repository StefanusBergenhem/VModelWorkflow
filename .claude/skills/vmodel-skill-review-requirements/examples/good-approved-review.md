# Example — APPROVED review

The reviewer is given a clean requirements document for a session-management service. The document covers session creation, validation, idle / absolute timeout, step-up authentication, plus an interface contract, NFRs in flat and Planguage forms, data requirements, inherited constraints, and full traceability.

The reviewer was given the document; the upstream input (parent REQS, ADRs) was also supplied. The reviewer applied the designer and tester perspectives (no stakeholder-facing outcomes triggered the user/stakeholder perspective). Anti-pattern sweep found nothing. Quality Bar gate cleared. Spec Ambiguity Test passed.

## Verdict block

```yaml
review:
  document: /specs/session-service/requirements.md
  reviewer: vmodel-skill-review-requirements
  date: 2026-04-26

  verdict: APPROVED

  upstream_input_provided: true

  perspectives_applied:
    - designer
    - tester

  findings:
    - id: F-001
      requirement_id: GLOBAL
      check_failed: check.vocabulary.glossary-term-unused
      severity: info
      category: vocabulary
      evidence: |
        The glossary defines "Step-up authentication" but no requirement explicitly uses
        the bare term — REQ-session-006 references the procedure inline. Not a defect;
        the term is referenced by adjacent concept ("ELEVATED state").
      recommended_action: |
        Either remove the term from the glossary, or note in the Glossary that it is
        retained because adjacent terms reference it.

    - id: F-002
      requirement_id: REQ-session-016
      check_failed: check.nfr.planguage-missing-goal-or-fail
      severity: info
      category: nfr
      evidence: |
        REQ-session-016 includes goal, stretch, wish, and fail — full Planguage form. No defect.
        (This finding is here as a positive: noting that the NFR meets the recommended bar.)
      recommended_action: |
        No action — NFR is complete.

  summary: |
    Verdict: APPROVED. The session-service requirements document passes every applicable
    Quality Bar item and the Spec Ambiguity Test. Two info-level observations noted (one
    glossary term lightly used, one NFR exceeding the minimum bar). No anti-pattern hits,
    no missing dimensions, no fabricated rationale. The upstream input was provided and
    cross-validation surfaced no DESIGN_ISSUE triggers. Document is ready to drive
    architecture allocation, detailed design, and test specification.

  counts:
    hard_reject: 0
    soft_reject: 0
    info: 2
    design_issue: 0
```

## What this example demonstrates

1. **APPROVED ≠ silent.** The review still surfaces info-level observations. They do not affect the verdict but are useful to the author for ongoing maintenance.

2. **Findings cite specific requirement IDs.** F-001 ties to "GLOBAL" because the observation is document-wide; F-002 ties to a specific REQ-ID.

3. **Recommended actions are generic and point to the rule.** No specific replacement wording. The author's job is rewriting; the reviewer's job is signalling.

4. **The summary does not list every finding.** It cites the dominant signal (verdict + key observations + upstream input status) in 2-4 sentences. The full findings list is below.

5. **Counts are explicit.** A glance at `counts` tells the reader the verdict is conservative (no soft_reject, no hard_reject); only info findings.

6. **Perspectives applied is honest.** Designer and tester were applied; user/stakeholder was *correctly* not applied (the document's scope is not root and no inherited constraint is regulatory — the GDPR constraint exists at the upstream platform level, not as a session-service-internal regulatory category once it is pre-allocated). Note: this is a judgment call; in this document IC-session-001 *is* categorised regulatory, so a strict reading would have triggered the user/stakeholder perspective. A cautious reviewer would apply it. Both choices are defensible; the review block makes the choice explicit.

7. **Cross-validation with upstream input was performed.** The `upstream_input_provided: true` field is a precondition for valid DESIGN_ISSUE detection. With it set, the reviewer asserts they checked the upstream and found no derivation breakage.
