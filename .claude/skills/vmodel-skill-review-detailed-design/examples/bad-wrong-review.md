# Counter-example — what NOT to do as a reviewer

Three reviewer failure modes annotated. Each is a verdict block emitted by an undisciplined reviewer; the annotation calls out what the verdict missed and what the correct verdict would have been.

## Failure mode 1 — False APPROVED on a code-paraphrase Algorithms section

The reviewer is given a DD whose Algorithms section reads:

> *"The function declares a result list, iterates from index 0 to length-1, compares each element with its successor using the natural ordering, swaps them when they are out of order, and returns the result list when the iteration completes."*

The reviewer reads this as "the algorithm is described" and approves.

```yaml
review:
  document: /specs/app/util/sort-service/detailed_design.md
  reviewer: vmodel-skill-review-detailed-design
  date: 2026-04-30
  verdict: APPROVED              # WRONG
  inputs_provided:
    detailed_design_document: true
    parent_architecture: true
    governing_adrs: true
    derived_from_artifacts: true
  perspectives_applied: [implementer, tester]
  findings: []
  summary: |
    All seven sections present. Algorithm is described step-by-step. Approved.
  recommended_next_action: |
    Proceed to TestSpec.
  counts: { hard_reject: 0, soft_reject: 0, info: 0, design_issue: 0 }
```

### What was missed

The Algorithms section is **code paraphrase** — every clause is derivable from reading the implementation; nothing in the DD says *what* the function must guarantee, only *how* it does it. Two hard-rejects fire on this paragraph alone:

- **`anti-pattern.code-paraphrase` (HARD ★ refusal C).** The clause walks through implementation steps. A different implementation (mergesort, Timsort) would not match this description, but would satisfy the same contract. The DD has collapsed the design box to a point.
- **`anti-pattern.algorithmic-postcondition` (HARD ★ refusal C).** If this same prose appears as a postcondition, it describes steps not result. The postcondition should state: *"The returned list contains exactly the elements of the input (multiset equality) and is in non-descending order according to the natural ordering."*

Likely also:
- **`anti-pattern.permutation-half-omitted`** if the postcondition states "ordered" without "permutation". Test engineer cannot tell whether `return []` passes.
- **`check.spec-ambiguity-test.fail`** — a junior who needs to write Timsort from this DD has no DD to derive Timsort from; they would have to write bubble-sort or copy this prose.

The correct verdict is **REJECTED** with refusal C named in the summary.

The failure mode: the reviewer judged on **presence of section content** rather than **substance of the content**. Refusal C exists precisely to catch this — a section reading as code paraphrase does not do the Algorithms section's job.

## Failure mode 2 — Subjective REJECTED on a sound contract

The reviewer disagrees with a function returning `Optional<T>` rather than throwing. The DD documents the choice with rationale (constraint kind: *architectural* — *"per ARCH-app-foo, normal-absence is not exceptional in this domain"*).

The reviewer would have preferred an exception. They emit:

```yaml
review:
  document: /specs/app/foo/lookup-service/detailed_design.md
  reviewer: vmodel-skill-review-detailed-design
  date: 2026-04-30
  verdict: REJECTED              # WRONG basis
  inputs_provided:
    detailed_design_document: true
    parent_architecture: true
    governing_adrs: true
    derived_from_artifacts: true
  perspectives_applied: [implementer, tester]
  findings:
    - id: F-001
      element_id: lookup
      check_failed: design.preferred-exception   # NOT IN CATALOG
      severity: soft_reject
      category: <not-cataloged>
      evidence: |
        lookup returns Optional<T> instead of throwing NotFoundException.
        Throwing would be clearer to callers.
      recommended_action: |
        Replace return type with throws NotFoundException; remove Optional wrapping.
  summary: |
    Optional return is suboptimal; should throw. Rejected.
  recommended_next_action: |
    Hand findings to the matched author skill for rewrite.
  counts: { hard_reject: 0, soft_reject: 1, info: 0, design_issue: 0 }
```

### What's wrong

- **`check_failed: design.preferred-exception` is not in the catalog.** Every finding identifier must appear in `references/quality-bar-gate.md` or `references/anti-patterns-catalog.md`. The reviewer must not invent ad-hoc strings.
- **The objection is subjective.** Both forms are defensible. The DD documents the choice with rationale tying it to a parent Architecture decision. There is no rule violation — `Optional<T>` is a legitimate way to communicate "normal absence is not exceptional" (per `error-handling-checks.md`).
- **`recommended_action` writes specific replacement wording** ("Replace return type with throws NotFoundException"). The reviewer's job is signaling rule violations; the matched author skill rewrites under direction from cataloged checks.
- **`summary` reads as opinion, not a defensible verdict against rules.**

The correct verdict is **APPROVED** (or APPROVED with info-level observation if the reviewer wants to surface "team norm differs"). Subjective preference is not grounds for REJECTED.

The failure mode: the reviewer is acting as a **stylist** rather than a **gatekeeper**.

## Failure mode 3 — APPROVED that missed the meta-gate

The reviewer ticks every Quality Bar item. Every cataloged check is Yes. Anti-pattern sweep is clean. The reviewer approves.

But: the DD's `claimJob` postcondition states *"Returns a Claim if successful"*. The contract claims `on_success` is populated, so `check.contract.postcondition-success-missing` does not fire. But the postcondition is vacuous — it does not name the property of the returned Claim.

A junior engineer trying to implement `claimJob` would have to ask: which row does the Claim correspond to? What is the lease window? What does "successful" mean? A test engineer writing the contract test would not know what to assert beyond non-null.

```yaml
review:
  document: /specs/app/jobs/dequeue-service/detailed_design.md
  reviewer: vmodel-skill-review-detailed-design
  date: 2026-04-30
  verdict: APPROVED              # WRONG — meta-gate fails
  inputs_provided:
    detailed_design_document: true
    parent_architecture: true
    governing_adrs: true
    derived_from_artifacts: true
  perspectives_applied: [implementer, tester]
  findings: []
  summary: |
    All Quality Bar items checked Yes. Anti-pattern sweep clean. Approved.
  recommended_next_action: |
    Proceed to TestSpec.
  counts: { hard_reject: 0, soft_reject: 0, info: 0, design_issue: 0 }
```

### What was missed

`check.spec-ambiguity-test.fail` is the **override**. Even when every other Yes/No item passes, the meta-gate determines whether the artifact has done the job DD exists to do. A postcondition reading "Returns a Claim if successful" is exactly the kind of vacuous-prose-passing-syntactic-checks failure the meta-gate was designed to catch.

The correct finding:

```yaml
- id: F-001
  element_id: claimJob
  check_failed: check.spec-ambiguity-test.fail
  severity: hard_reject
  category: meta-gate
  evidence: |
    claimJob.postconditions.on_success reads only "Returns a Claim if successful."
    A junior engineer cannot derive: what is the relationship between the
    returned Claim and the underlying row? What lease window applies? What
    invariants does the Claim satisfy? A test engineer cannot write a contract
    test beyond non-null. The Spec Ambiguity Test fails on this clause.
  recommended_action: |
    Replace the vacuous postcondition with a concrete result-property statement
    naming: row_id correspondence, lease window expressed as expires_at, the
    multi-worker safety invariant. See `function-contract-checks.md`.
```

The verdict is **REJECTED** if the upstream Architecture interface invariant fully specifies the claim semantics (this DD failed to refine them); **DESIGN_ISSUE** if the parent Architecture itself is ambiguous about claim semantics (this DD cannot derive what the parent did not specify). Either way, the meta-gate is the override.

The failure mode: the reviewer treated the Spec Ambiguity Test as a **checkbox** rather than a **meta-gate**. The check is irreducibly heuristic — it requires honest application of "could a junior act on this without asking?".

## Three canonical reviewer mistakes

1. **False-APPROVE-on-thin-substance.** Judging on presence of content rather than its specificity. Refusal C (code paraphrase, algorithmic postcondition) is the most common surface where this strikes.
2. **Subjective-REJECT.** Acting as a stylist rather than a gatekeeper. Inventing ad-hoc `check_failed` strings, writing specific replacement wording, rejecting on personal preference.
3. **Missed-meta-gate.** Treating the Spec Ambiguity Test as a checkbox. Approving DDs that pass every Yes/No item but cannot be acted on by a junior engineer.

The eight-step sweep guards against (1) and (3); the catalog discipline guards against (2); the verdict precedence rule and meta-gate override route (3) correctly.
