# Example — APPROVED review

The reviewer is given the canonical good Architecture document for a checkout service (root scope, greenfield). The document carries Decomposition with five children (cart, pricing, inventory, payment-orchestrator, order-committer), Interface entries with Design-by-Contract clauses, and a non-trivial Composition section naming "request-response with outbox-relay for async events" plus deployment intent (Kubernetes / EKS, four runtime units, three environments).

The reviewer was given the architecture document, the parent Requirements artifact, and three governing ADRs (ADR-008 token-bearer authn at gateway, ADR-012 idempotency-key, ADR-019 data topology). The reviewer applied the architect, integrator, and operator perspectives. Anti-pattern sweep found nothing. Composition is load-bearing and complete. Quality Bar gate cleared. Spec Ambiguity Test passed.

## Verdict block

```yaml
review:
  document: /specs/architecture.md
  reviewer: vmodel-skill-review-architecture
  date: 2026-04-30

  verdict: APPROVED

  inputs_provided:
    architecture_document: true
    parent_requirements: true
    governing_adrs: true

  perspectives_applied:
    - architect
    - integrator
    - operator

  findings:
    - id: F-001
      element_id: GLOBAL
      check_failed: check.fitness-function.not-named-for-load-bearing-property
      severity: info
      category: traceability
      evidence: |
        The artifact names five fitness functions (dependency direction, p95 latency,
        outbox relay lag, plaintext-secret SAST, cart total LOC). The matched author
        skill listed "no plaintext secret in config or env-export" without naming the
        SAST tool concretely. Not a defect — the property is named, the classification
        is named (atomic + triggered), the check kind is named (SAST rule). The
        specific tool is a Detailed Design / IaC concern.
      recommended_action: |
        No action — the fitness function is sufficiently specified at Architecture
        level. Tool selection is downstream.

    - id: F-002
      element_id: GLOBAL
      check_failed: check.adr.governing-not-cited-in-body
      severity: info
      category: adr
      evidence: |
        ADR-008, ADR-012, ADR-019 are all cited in the body at their decision
        application points. ADR-019 is cited four times — once at order-committer's
        rationale, once at the runtime pattern's rationale, once in the data-topology
        diagram, once in the topology slot-fill. No defect; included here as a
        positive observation that the body-citation discipline is honored.
      recommended_action: |
        No action — citation discipline is exemplary.

  summary: |
    Verdict: APPROVED. The checkout-service architecture passes every applicable
    Quality Bar item and the Spec Ambiguity Test. Composition is load-bearing and
    complete: request-response with outbox-relay named, middleware stack ordered,
    DI strategy named, message-bus topology specified, sequence diagrams for happy
    path and PSP-timeout failure path, root-scope deployment intent populated
    (environments, EKS orchestration target, four runtime units mapped). All
    interface entries carry the postcondition triple, typed errors, quality
    attributes, authn/authz with evaluation layer named, and rationale tied to
    requirements or ADRs. Two info-level observations noted; no defects.

  recommended_next_action: |
    Proceed to Detailed Design authoring per leaf (cart, pricing, inventory,
    payment-orchestrator, order-committer) and TestSpec authoring against this
    Architecture's interfaces and composition invariants.

  counts:
    hard_reject: 0
    soft_reject: 0
    info: 2
    design_issue: 0
```

## What this example demonstrates

1. **APPROVED is not silent.** The review surfaces info-level observations. They do not affect the verdict but are useful to the consumer of the verdict for ongoing maintenance and for confirming that high-discipline items (body-citation of ADRs) were honored.

2. **Findings cite specific elements.** F-001 ties to "GLOBAL" because it observes a document-wide property (the fitness-function suite as a whole). F-002 also "GLOBAL" because ADR-citation discipline is a document-wide check.

3. **Recommended actions are generic and point to the rule.** No specific replacement wording. The matched author skill does the rewriting; the review skill signals.

4. **The summary cites the dominant signal in 2-4 sentences.** It names the Composition load-bearing pieces (pattern, wiring, sequences, deployment intent) and confirms what the Spec Ambiguity Test passed against — the full findings list is in the block above, the summary is the headline.

5. **Counts are explicit.** A glance at `counts` tells the reader the verdict is conservative (zero soft_reject, zero hard_reject); only info findings.

6. **Three perspectives applied — architect, integrator, operator.** The architecture document warrants all three because it is root-scope (operator perspective is load-bearing for deployment intent), it has cross-component sequence diagrams (integrator perspective for failure-path coverage), and it carries Decomposition + Interfaces (architect perspective for boundary correctness).

7. **All inputs were provided.** The `inputs_provided` block records that traceability checks could be run (parent Requirements present), ADR resolution was completed (`governing_adrs:` resolved), and consequently the verdict is well-grounded — not a partial-information APPROVED.

8. **Recommended next action points forward, not back.** APPROVED → "proceed to Detailed Design and TestSpec". The verdict is read by orchestration that needs to know what to do next; "all checks pass" alone is not an actionable next step.
