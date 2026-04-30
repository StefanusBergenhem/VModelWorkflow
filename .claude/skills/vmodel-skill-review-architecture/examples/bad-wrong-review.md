# Counter-example — what NOT to do as a reviewer

Three reviewer failure modes annotated. Each example is a verdict block emitted by an undisciplined reviewer; the annotation calls out what the verdict missed and what the correct verdict would have been.

## Failure mode 1 — False APPROVED on a thin Composition section

The reviewer is given an Architecture document where Decomposition and Interfaces are thoroughly populated, but the entire Composition section reads:

> **Composition.** The five components communicate over HTTP. Deployment is on Kubernetes. See `infra/k8s/` for details.

The reviewer reads this as "composition is described" and approves.

```yaml
review:
  document: /specs/architecture.md
  reviewer: vmodel-skill-review-architecture
  date: 2026-04-30
  verdict: APPROVED              # WRONG
  inputs_provided:
    architecture_document: true
    parent_requirements: true
    governing_adrs: true
  perspectives_applied: [architect, integrator, operator]
  findings: []
  summary: |
    Decomposition is complete with five children. Interfaces have all DbC
    clauses. Composition names HTTP and Kubernetes. Approved.
  recommended_next_action: |
    Proceed to Detailed Design.
  counts:
    hard_reject: 0
    soft_reject: 0
    info: 0
    design_issue: 0
```

### What was missed

The Composition section fails refusal C — three hard-reject triggers fire on this paragraph alone:

- **`check.composition.no-named-pattern` (HARD).** "Communicates over HTTP" names a protocol, not a runtime pattern. Request-response? Event-driven over HTTP? Saga with HTTP coordinator? The pattern is undeclared.
- **`check.composition.no-sequence-diagram` (HARD).** No Mermaid sequence diagram anywhere. "See `infra/k8s/`" does not satisfy this — IaC is implementation; Composition specifies intent.
- **`check.composition.deployment-intent-missing` (HARD, root only).** "Deployment is on Kubernetes" is not deployment intent. No environments enumerated. No runtime-unit boundaries. No runtime-unit lifecycle / observability / resource budget / failure story per unit. Compositional load-bearing decisions are absent.

Plus `anti-pattern.ad-hoc-composition` (soft) — the section is exactly the "system is a bunch of services that talk to each other" tell.

The correct verdict is **REJECTED** with refusal C named in the summary. The findings list contains at minimum the three HARD `check.composition.*` ids plus the `anti-pattern.ad-hoc-composition` finding plus likely several soft findings (DI strategy unnamed, middleware stack unordered, no failure-path diagram).

The failure mode: the reviewer judged on **presence of section heading** rather than **substance of section**. A heading reading "Composition" with two sentences underneath is structurally a Composition section but does not do Composition's job. The Quality Bar gate's load-bearing card and refusal C exist precisely to catch this — the reviewer ticked the umbrella box without reading the substance.

## Failure mode 2 — Subjective REJECTED on a sound Decomposition

The reviewer disagrees with the bounded-context choice in a sound Decomposition. The artifact under review draws the boundary between `cart` and `pricing` as a published-language interface (signed price quote with validity window). The rationale is documented; it cites a parent requirement (REQ-005) and an ADR (ADR-019).

The reviewer would have preferred to fold pricing into cart ("it's a small system; one bounded context would be simpler"). They emit:

```yaml
review:
  document: /specs/architecture.md
  reviewer: vmodel-skill-review-architecture
  date: 2026-04-30
  verdict: REJECTED              # WRONG basis
  inputs_provided:
    architecture_document: true
    parent_requirements: true
    governing_adrs: true
  perspectives_applied: [architect, integrator, operator]
  findings:
    - id: F-001
      element_id: pricing
      check_failed: design.preferred-merge       # NOT IN CATALOG
      severity: soft_reject
      category: <not-cataloged>
      evidence: |
        Pricing is decomposed as a separate child. It would be simpler to fold
        it into cart.
      recommended_action: |
        Fold pricing into cart and remove the price-quote interface. Reduce to
        four children.
  summary: |
    Pricing should be folded into cart. Rejected.
  recommended_next_action: |
    Hand findings to the matched author skill for redecomposition.
  counts:
    hard_reject: 0
    soft_reject: 1
    info: 0
    design_issue: 0
```

### What's wrong

- **`check_failed: design.preferred-merge` is not in the catalog.** Every finding identifier must appear in `references/quality-bar-gate.md` or `references/anti-patterns-catalog.md`. Reviewer must not invent ad-hoc strings.
- **The objection is subjective.** Both decompositions (cart-with-pricing-merged vs cart-and-pricing-as-published-language) are defensible. The artifact under review made a documented choice with rationale tying it to a requirement and an ADR. There is no rule violation. The bounded-context boundary is drawn at the linguistic fracture (pricing rules vs cart workflow); the published-language pattern (DDD context-mapping) earns its keep because the signed price quote is the trust mechanism between the two contexts.
- **`recommended_action` writes specific replacement wording** ("Fold pricing into cart"). The reviewer's job is signaling rule violations; the matched author skill rewrites under direction from cataloged checks.
- **`summary` is decorative.** It reads as opinion rather than a defensible verdict against rules.

The correct verdict is **APPROVED** (or APPROVED with info-level observations if the reviewer wants to surface "team norm differs"). Subjective preference is not grounds for REJECTED. The review skill's job is rule-based verdict, not opinion.

The failure mode: the reviewer is acting as a **stylist** rather than a **gatekeeper**. Subjective rejection erodes trust in the verdict and creates pointless rewrite cycles.

## Failure mode 3 — APPROVED that missed Spec Ambiguity Test override

The reviewer ticks every box of the Quality Bar checklist. Every cataloged item is a Yes. Anti-pattern sweep is clean. The reviewer approves.

But: a critical Interface entry `IPaymentAuthorise` has its `postconditions.on_downstream_failure` populated as: *"On PSP failure, the system handles the failure appropriately."* The reviewer counted this as "postcondition present" and ticked the box.

A junior engineer reading this artifact and trying to write a TestSpec for `IPaymentAuthorise` would have to ask: what does "handle appropriately" mean? Release the inventory reservation? Void the partial PSP authorization? Return which typed error? Within what time bound? Update cart state to which value? The Spec Ambiguity Test fails because the postcondition is unactionable for downstream Detailed Design and TestSpec authoring.

```yaml
review:
  document: /specs/architecture.md
  reviewer: vmodel-skill-review-architecture
  date: 2026-04-30
  verdict: APPROVED              # WRONG — meta-gate fails
  inputs_provided:
    architecture_document: true
    parent_requirements: true
    governing_adrs: true
  perspectives_applied: [architect, integrator, operator]
  findings: []
  summary: |
    All Quality Bar items checked Yes. Anti-pattern sweep clean. Approved.
  recommended_next_action: |
    Proceed to Detailed Design.
  counts:
    hard_reject: 0
    soft_reject: 0
    info: 0
    design_issue: 0
```

### What was missed

`check.spec-ambiguity-test.fail` is the override. Even when every other Yes/No item passes, the meta-gate is what determines whether the artifact has done the job Architecture exists to do. A postcondition that reads "handles the failure appropriately" is exactly the kind of vacuous-prose-passing-syntactic-checks failure the meta-gate was designed to catch.

The correct finding looks like:

```yaml
- id: F-001
  element_id: IPaymentAuthorise
  check_failed: check.spec-ambiguity-test.fail
  severity: hard_reject
  category: meta-gate
  evidence: |
    IPaymentAuthorise.postconditions.on_downstream_failure reads:
    "On PSP failure, the system handles the failure appropriately."
    A junior engineer cannot derive: which typed error is returned, whether
    inventory reservation is released and within what time, whether partial
    PSP authorization is voided, what cart state is left in, or what response
    code is returned. The TestSpec for this interface is not derivable from
    the artifact.
  recommended_action: |
    Replace the vacuous prose with a concrete on_downstream_failure block
    naming: typed error code, state mutation discipline, compensation actions
    with time bounds, response shape. See interface-contract-checks.md
    `check.interface.missing-postcondition` (the postcondition triple is
    populated by name but not by content).
```

The verdict is **DESIGN_ISSUE** if the upstream Requirements is what fails to specify the PSP-failure semantics (in which case Architecture cannot derive the postcondition without a Requirements rewrite); **REJECTED** if Requirements specify PSP-failure semantics fully but Architecture failed to refine them. Either way, the meta-gate is the override — the rest of the Quality Bar checklist does not save the artifact.

The failure mode: the reviewer treated the Spec Ambiguity Test as a **checkbox** rather than a **meta-gate**. The check is irreducibly heuristic — it requires the reviewer to *actually* read the document from a junior engineer's perspective and ask "could I act on this without asking?". A "Yes/No box ticked Yes" without honest application of the test is the most common APPROVED-when-it-shouldn't-be failure mode in an undisciplined review.

## Three canonical reviewer mistakes

The three failure modes named:

1. **False-APPROVE-on-thin-section.** Judging on presence-of-heading rather than substance-under-heading. Composition's load-bearing card is the most common surface where this strikes.
2. **Subjective-REJECT.** Acting as a stylist rather than a gatekeeper. Inventing ad-hoc `check_failed` strings, writing specific replacement wording, rejecting on personal preference rather than cataloged rule.
3. **Missed-meta-gate.** Treating the Spec Ambiguity Test as a checkbox. Approving artifacts that pass every Yes/No box but cannot be acted on by a junior engineer.

These are the three failure modes the review-skill discipline is designed to prevent. Every verdict block is a defense against one of them: the eight-step sweep against (1) and (3); the catalog discipline against (2); the verdict precedence rule and the meta-gate override against (3).
