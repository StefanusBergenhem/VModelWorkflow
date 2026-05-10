---
id: REQS
title: "vmodel-core — Root Requirements"
artifact_type: requirements
scope: ""
parent_scope: null
status: draft
date: "2026-05-03"
version: 1
---

# Requirements — vmodel-core

This document specifies the root-scope requirements for **vmodel-core** — the deterministic CLI that validates VModelWorkflow spec artifacts and reports on spec-tree state. It is refined directly from `specs/needs.md` (the elicit-needs output for this scope, 2026-05-01), with framework material in `references/` (TARGET_ARCHITECTURE, BACKLOG, schemas) used to fill detail only where needs.md is silent and not in conflict; where needs.md and framework references conflict, needs.md supersedes. The document scope is the whole product at v1; per the framework, vmodel-core is a child product within VModelWorkflow's three-product structure (`TARGET §10`), but is treated here as effective root because no parent-scope (VModelWorkflow-level) Requirements artifact yet exists. The placeholder upstream id `NEEDS-vmodel-core` is used in `derived_from` because needs.md is not in the canonical artifact set; this is a deliberate, documented gap (see *Open gaps*).

## Glossary

```yaml
glossary:
  - term: "Spec tree"
    definition: |
      The tree of V-model specification artifacts an adopter project has authored,
      rooted at a single product brief and decomposed into branch and leaf scopes,
      whose artifacts are written to files under a configurable specs directory.
    distinct_from: "Scope tree — the underlying tree of scope nodes; the spec tree is the set of artifacts hung on the scope tree."

  - term: "Scope"
    definition: |
      A single node in the spec tree, identified by a slash-separated kebab-case
      path (empty path denotes the root scope). Each non-leaf scope holds
      requirements, architecture, and testspec artifacts; each leaf holds a
      detailed-design and a testspec.

  - term: "Artifact"
    definition: |
      One V-model specification document of a known type (product-brief,
      requirements, architecture, adr, detailed-design, or test-spec), written
      as a single Markdown file with YAML front-matter and embedded YAML blocks
      in the body.

  - term: "Validation run"
    definition: |
      One execution of vmodel-core's validate operation against a supplied input
      (a single artifact, a subtree of the spec tree, or the whole spec tree),
      that emits zero or more findings and exactly one verdict.

  - term: "Finding"
    definition: |
      One report of one rule violation detected during a validation run.

  - term: "Finding-record"
    definition: |
      The structured shape of a single finding emitted by vmodel-core, carrying
      enough information for an AI caller to act on the finding deterministically
      (see Data Requirements).
    distinct_from: "Finding — the conceptual report; finding-record is its structural shape."

  - term: "Verdict"
    definition: |
      The single overall outcome of a validation run, one of pass, fail, or
      system-error, distinct from any individual finding.

  - term: "Verdict-record"
    definition: |
      The structured shape carrying the verdict value emitted by vmodel-core
      at the end of a validation run (see Data Requirements).

  - term: "Blocking finding"
    definition: |
      A finding whose triage dimension marks it as blocking progression or merge,
      as distinct from warn-only or informational findings.

  - term: "Validation call site"
    definition: |
      A class of caller that invokes vmodel-core's validate operation. v1
      recognises five: author skill, review skill, orchestrator, CI pipeline,
      direct human caller.

  - term: "AI caller"
    definition: |
      A consumer of vmodel-core's output that is itself an AI-driven program —
      typically a Phase 5 framework skill (author skill, review skill,
      orchestrator) invoking vmodel-core as a subprocess and consuming its
      structured output.

  - term: "CI pipeline"
    definition: |
      A non-AI automated consumer that invokes vmodel-core as a step in a build
      or pre-merge gate and branches on the verdict's exit-code rendering.

  - term: "Direct human caller"
    definition: |
      A human engineer running vmodel-core in a terminal during local authoring,
      review, or investigation.

  - term: "Adopter"
    definition: |
      An organisation, team, or individual using VModelWorkflow on their own
      project, including but not limited to the framework author's pilot
      projects. v1 is targeted at the framework author in dogfooding role; the
      open-source adopter community is deferred to v1.x or v2.

  - term: "Sibling tool"
    definition: |
      Either of vmodel-author or vmodel-retrofit — the other two purpose-built
      tool products in the VModelWorkflow tool set. Sibling tools are not
      external callers under v1's CLI-as-stable-contract constraint; their
      integration mode (library link or subprocess) is decided by each sibling's
      ADRs.

  - term: "Coverage report"
    definition: |
      A reporting output stating, for a named relationship between two artifact
      sets, the proportion of artifacts in the source set that participate in
      the relationship.

  - term: "Completeness report"
    definition: |
      A reporting output stating the count and ratio of artifacts in scope that
      satisfy a named conformance criterion and the count and ratio that fail
      to satisfy it.

  - term: "Inventory report"
    definition: |
      A reporting output stating the count of artifacts in the spec tree
      broken down by artifact type and by scope.

  - term: "Impact-analysis report"
    definition: |
      A reporting output that, given a specified artifact, names every other
      artifact in the spec tree whose traceability relationship to the specified
      artifact may require review or update if the specified artifact changes.

  - term: "Non-recoverable system-level failure"
    definition: |
      A condition encountered during a validation run that prevents vmodel-core
      from continuing to produce authoritative findings for the run — for
      example a file IO failure on a target artifact, a parse crash on
      malformed input, a corrupted framework schema or rule-catalog input, or
      an internal error such as out-of-memory. The defining property is the
      inability to continue producing authoritative findings; the precise
      enumeration of failure modes is bounded by detailed design.
    distinct_from: "Rule violation — a violation of a rule by an artifact, which is reportable as a finding without halting the run."

  - term: "Quality Bar"
    definition: |
      The framework's per-artifact-type checklist of structural and semantic
      rigor items, published canonically as JSON. The structural items are
      mechanically evaluable; the semantic items require interpretation and are
      out of vmodel-core's scope.

  - term: "Framework canonical rule catalog"
    definition: |
      The traceability validation rule set published in the framework
      `references/schemas/traceability/validation-rules.catalog.json`. It is
      the authoritative list of rules vmodel-core must enforce.

  - term: "Framework canonical schema set"
    definition: |
      The set of JSON schemas that define artifact-front-matter shape, published
      in the framework `references/schemas/artifacts/`: one universal envelope
      schema, six per-artifact schemas (product-brief, requirements,
      architecture, adr, detailed-design, test-spec), and one quality-bar
      container schema.

  - term: "Framework canonical Quality Bar checklist set"
    definition: |
      The six per-artifact-type Quality Bar JSON files published in
      `references/schemas/artifacts/quality-bar/`, each enumerating the
      structural and semantic rigor items for one artifact type.
```

## Inherited Constraints

```yaml
inherited_constraints:
  - id: IC-001
    source: "needs.md (root-scope, 2026-05-01) — Constraints: 'No LLM in runtime path'; framework-principle-grounded TARGET §3"
    summary: |
      No LLM is invoked at any point during a vmodel-core run. All work is
      mechanical and deterministic; capability requiring interpretation belongs
      in a Phase 5 skill, not in this tool.
    category: technical
    cost_of_relaxing: |
      Determinism is lost — the same input no longer produces the same output;
      runs become non-replayable, CI gating becomes flaky, and the tool/skill
      split that justifies vmodel-core's existence collapses.
    derived_requirements: []

  - id: IC-002
    source: "needs.md (root-scope, 2026-05-01) — Constraints: 'Operational simplicity: each run is independent…'"
    summary: |
      Each run is independent, with no install/configure overhead and no
      operational state carried between invocations. The tool must be runnable
      as-is in CI with no setup, no daemon to manage, no shared mutable state
      to coordinate.
    category: technical
    cost_of_relaxing: |
      CI integration breaks for typical adopter setups; the AI-caller subprocess
      contract becomes stateful and cross-run-coupled, breaking AI-caller retry
      assumptions.
    derived_requirements: []

  - id: IC-003
    source: "needs.md (root-scope, 2026-05-01) — Constraints: 'Read-only on the adopter's spec tree'"
    summary: |
      vmodel-core never writes, renames, or deletes spec artifacts. All output
      goes to stdout / stderr only. Spec-side mutations belong to vmodel-author
      per the framework's tool-product split.
    category: technical
    cost_of_relaxing: |
      Adopters lose the safety property that running vmodel-core cannot corrupt
      their spec tree; integration with vmodel-author becomes ambiguous; the
      tool/sibling-product separation collapses.
    derived_requirements: []

  - id: IC-004
    source: "needs.md (root-scope, 2026-05-01) — Constraints: 'Install experience: an adopter must be able to download a single artifact and run it on Linux, macOS, or Windows…'"
    summary: |
      An adopter must be able to download a single artifact and run it on
      Linux, macOS, or Windows with no separate runtime install (no JVM, no
      Python interpreter, no Node, no shared-library prerequisites beyond what
      the OS provides natively). The realisation (statically linkable binary,
      single-file bundled interpreter, or other) is a downstream choice.
    category: technical
    cost_of_relaxing: |
      Adoption friction rises substantially; CI integration loses portability;
      the open-source adoption path (deferred at v1 but bound by this
      constraint) is foreclosed.
    derived_requirements: []

  - id: IC-005
    source: "needs.md (root-scope, 2026-05-01) — Constraints: 'Update mechanism: re-download and replace in place'"
    summary: |
      The update mechanism is re-download and replace in place. No update
      daemon, no in-place auto-updater, no package-manager dependency.
    category: technical
    cost_of_relaxing: |
      Operational simplicity (IC-002) and single-artifact install (IC-004)
      become inconsistent; adopters carry update-mechanism complexity that the
      design explicitly excluded.
    derived_requirements: []

  - id: IC-006
    source: "needs.md (root-scope, 2026-05-01) — Constraints: 'External (non-sibling) callers integrate via the CLI as a stable contract'"
    summary: |
      Phase 5 skills, CI pipelines, and direct human callers invoke vmodel-core
      as a subprocess and consume the CLI's output. They do not depend on
      language bindings or in-process library access. Sibling-tool integration
      mode (library link or subprocess) is orthogonal and decided per-sibling.
    category: technical
    cost_of_relaxing: |
      External callers must track in-process API changes; portability across
      AI-caller / CI / human use is lost; the subprocess-based AI-skill
      abstraction breaks.
    derived_requirements: [REQ-024, REQ-025]

  - id: IC-007
    source: "needs.md (root-scope, 2026-05-01) — Constraints: 'No relaxation modes'; framework-principle-grounded TARGET §3 #3"
    summary: |
      No per-adopter '--lenient' flag, no rigor-tier configuration. Uniform
      high rigor is enforced by absence of opt-out: if rigor is not needed,
      the framework is not the right tool.
    category: organisational
    cost_of_relaxing: |
      The framework's uniform-high-rigor axiom (TARGET §3 #3) is broken;
      adopters can opt out of the discipline that vmodel-core exists to
      enforce, defeating the tool's purpose.
    derived_requirements: []

  - id: IC-008
    source: "needs.md (root-scope, 2026-05-01) — Constraints: 'Open-source distribution. Specific licence is deferred to product ADR'"
    summary: |
      vmodel-core ships as open source. Specific licence selection is deferred
      to a product-scope ADR.
    category: organisational
    cost_of_relaxing: |
      Open-source adoption (deferred at v1 but bound by this constraint) is
      foreclosed; pilot validity for adopter-community use is broken.
    derived_requirements: []

  - id: IC-009
    source: "framework: references/schemas/traceability/validation-rules.catalog.json (the framework canonical rule catalog)"
    summary: |
      vmodel-core enforces the rules published in the framework canonical rule
      catalog. The catalog is the authoritative source of validation rules and
      their categories (reference_integrity, completeness, cycle, retrofit,
      cascade); per-rule logic at vmodel-core scope is allocated to architecture
      and detailed design.
    category: technical
    cost_of_relaxing: |
      vmodel-core and the framework's published rule semantics drift; adopters
      cannot trust that 'pass' from vmodel-core means the framework's canonical
      rule set was enforced.
    derived_requirements: [REQ-010, REQ-011, REQ-012, REQ-013, REQ-014]

  - id: IC-010
    source: "framework: references/schemas/artifacts/envelope.schema.json plus the six per-artifact schemas (product-brief, requirements, architecture, adr, detailed-design, test-spec)"
    summary: |
      vmodel-core validates artifact front-matter against the framework's
      universal envelope schema, and against the per-artifact schema selected
      by the artifact's declared `artifact_type`.
    category: technical
    cost_of_relaxing: |
      Adopter artifacts can declare malformed front-matter without detection;
      downstream traceability and quality-bar checks operate on unvalidated
      data; the framework's structural rigor mechanism breaks.
    derived_requirements: [REQ-015, REQ-016]

  - id: IC-011
    source: "framework: references/schemas/artifacts/quality-bar/ — the six per-artifact-type quality-bar JSON files"
    summary: |
      vmodel-core evaluates the structural-rigor items in each artifact's
      Quality Bar checklist. Items requiring interpretation (the semantic-rigor
      items, including the Spec Ambiguity Test meta-gate) are out of scope —
      they belong to AI review skills.
    category: technical
    cost_of_relaxing: |
      Adopters cannot get a mechanical baseline of Quality-Bar conformance;
      review-skill grounding (per needs.md) loses its mechanical floor.
    derived_requirements: [REQ-017]

  - id: IC-012
    source: "needs.md (root-scope, 2026-05-01) — Quality needs: 'Worst-case target hardware: a commodity CI runner'"
    summary: |
      Worst-case target hardware is a commodity CI runner. The tool must run
      within typical CI-runner resource bounds for all v1 capabilities.
      Developer laptops and AI-agent containers are not the design target.
    category: technical
    cost_of_relaxing: |
      CI integration (the secondary-user-class workflow) is foreclosed for
      typical adopter setups; the no-special-hardware adoption path is broken.
    derived_requirements: [REQ-022, REQ-023]
```

## Functional Requirements

### Verdict and finding production

```yaml
- id: REQ-001
  type: functional
  statement: |
    When a validation run terminates — whether by completing per REQ-002 /
    REQ-003 or by halting per REQ-004 — the system shall produce exactly one
    verdict-record for that run.
  rationale: |
    needs.md (turn 5) commits validation to a single overall verdict per run,
    distinct from per-finding rule-class taxonomy: the verdict is what CI
    pipelines and direct human callers gate on, while AI callers branch on the
    finding identifiers. The trigger is broadened from 'completes' to
    'terminates' so the cardinality covers both completed runs and runs halted
    by a non-recoverable system-level failure (REQ-005's verdict value of
    'system-error' has no cardinality home unless this requirement covers the
    halted case). A single verdict per run, regardless of termination cause,
    gives shell-driven consumers a deterministic gating decision.
  derived_from: [NEEDS-vmodel-core]
```

```yaml
- id: REQ-002
  type: functional
  statement: |
    When a validation run completes without any blocking finding, the system
    shall set the verdict-record value to 'pass'.
  rationale: |
    needs.md (turn 5) names 'pass' as 'no blocking findings'. Triage of
    individual findings (per finding-record's triage dimension) determines
    whether a finding blocks progression; the verdict aggregates only blocking
    severity, leaving rule-class taxonomy out of the verdict.
  derived_from: [NEEDS-vmodel-core, REQ-001]
```

```yaml
- id: REQ-003
  type: functional
  statement: |
    When a validation run completes with at least one blocking finding, the
    system shall set the verdict-record value to 'fail'.
  rationale: |
    needs.md (turn 5) names 'fail' as 'at least one blocking finding'. This is
    the complement of REQ-002; together they cover every completed run that is
    not interrupted by a system-level failure.
  derived_from: [NEEDS-vmodel-core, REQ-001]
```

```yaml
- id: REQ-004
  type: functional
  statement: |
    If during a validation run the system encounters a non-recoverable
    system-level failure, then the system shall halt the run and skip
    evaluation of any unexamined artifacts.
  rationale: |
    needs.md (turn 11) commits halt-and-report partial-failure behaviour: when
    vmodel-core encounters a system-level failure during a multi-artifact
    operation, it halts the run; the remaining artifacts are not evaluated.
    This keeps the AI-caller's branching logic clean (system-error and findings
    live on different tracks) and prevents callers from acting on partial
    results that mix evaluated and unevaluated artifacts. The conceptual
    boundary of 'non-recoverable system-level failure' is fixed by the
    glossary definition (defining property: inability to continue producing
    authoritative findings); precise per-failure-mode enumeration is detailed-
    design scope.
  derived_from: [NEEDS-vmodel-core]
```

```yaml
- id: REQ-005
  type: functional
  statement: |
    When a validation run halts due to a non-recoverable system-level failure,
    the system shall set the verdict-record value to 'system-error'.
  rationale: |
    needs.md (turn 5 + turn 11) makes 'system-error' the verdict value for runs
    where vmodel-core could not complete; distinct from 'fail' because the
    verdict is not authoritative when the tool itself did not complete. AI
    callers must be able to disambiguate 'this artifact has findings' from
    'this artifact could not be evaluated', so the verdict carries the
    failure-mode signal.
  derived_from: [NEEDS-vmodel-core, REQ-001, REQ-004]
```

```yaml
- id: REQ-006
  type: functional
  statement: |
    When the system detects a rule violation during a validation run, the
    system shall emit one finding-record describing the violation.
  rationale: |
    needs.md (turn 4) commits validation findings as the unit by which violations
    are reported, with the finding-record carrying five dimensions sufficient
    for an AI caller to act on the finding deterministically. One-finding-per-
    violation cardinality lets AI callers count, branch, and aggregate
    deterministically.
  derived_from: [NEEDS-vmodel-core]
```

### Validation invocation modes

```yaml
- id: REQ-007
  type: functional
  statement: |
    When the system is invoked in single-artifact validation mode, the system
    shall validate exactly the artifact identified by the supplied artifact
    path.
  rationale: |
    needs.md (turn 3) commits single-artifact validation as the operation
    consumed by author skills (validate the artifact just written, inside the
    retry loop), review skills (ground mechanical findings), and direct human
    callers ad-hoc. Bounding the operation to the supplied artifact prevents
    accidental whole-tree work in the AI-caller hot path.
  derived_from: [NEEDS-vmodel-core]
```

```yaml
- id: REQ-008
  type: functional
  statement: |
    When the system is invoked in subtree validation mode, the system shall
    validate every artifact reachable from the supplied scope path within the
    spec tree.
  rationale: |
    needs.md (turn 3) commits subtree validation as one of the modes the direct
    human caller uses ad-hoc and that the orchestrator may use at intermediate
    phase boundaries. Subtree-bounded evaluation is required because adopters
    work scope-by-scope.
  derived_from: [NEEDS-vmodel-core]
```

```yaml
- id: REQ-009
  type: functional
  statement: |
    When the system is invoked in whole-tree validation mode, the system shall
    validate every artifact in the supplied spec tree.
  rationale: |
    needs.md (turn 3) commits whole-tree validation as the operation consumed
    by orchestrators (gating phase progression) and CI pipelines (pre-merge
    gating). Whole-tree completeness is the gate condition for the framework's
    'specification complete' criterion (TARGET §8.1).
  derived_from: [NEEDS-vmodel-core]
```

### Rule-class enforcement (derived from IC-009)

```yaml
- id: REQ-010
  type: functional
  derivation: derived
  statement: |
    When the system runs a validation, the system shall enforce every rule in
    the framework canonical rule catalog whose category is `reference_integrity`.
  rationale: |
    Reference integrity is one of the five rule classes published in the
    framework canonical rule catalog (IC-009). Enforcing the class as a whole
    binds vmodel-core to every present and future rule of that category in the
    catalog; per-rule semantics are sourced from the catalog rather than
    re-stated here, preventing drift between requirements and the catalog.
  derived_from: [IC-009]
```

```yaml
- id: REQ-011
  type: functional
  derivation: derived
  statement: |
    When the system runs a validation, the system shall enforce every rule in
    the framework canonical rule catalog whose category is `completeness`.
  rationale: |
    Completeness is one of the five rule classes published in the framework
    canonical rule catalog (IC-009); the same class-level binding rationale as
    REQ-010 applies.
  derived_from: [IC-009]
```

```yaml
- id: REQ-012
  type: functional
  derivation: derived
  statement: |
    When the system runs a validation, the system shall enforce every rule in
    the framework canonical rule catalog whose category is `cycle`.
  rationale: |
    Cycle detection is one of the five rule classes published in the framework
    canonical rule catalog (IC-009); the same class-level binding rationale as
    REQ-010 applies.
  derived_from: [IC-009]
```

```yaml
- id: REQ-013
  type: functional
  derivation: derived
  statement: |
    When the system runs a validation, the system shall enforce every rule in
    the framework canonical rule catalog whose category is `retrofit`.
  rationale: |
    Retrofit-discipline rules (notably the no-fabrication / no-reconstructed-
    on-human-only-fields rule TRV-RETRO-001) are one of the five rule classes
    published in the framework canonical rule catalog (IC-009); the same
    class-level binding rationale as REQ-010 applies.
  derived_from: [IC-009]
```

```yaml
- id: REQ-014
  type: functional
  derivation: derived
  statement: |
    When the system runs a validation, the system shall enforce every rule in
    the framework canonical rule catalog whose category is `cascade`.
  rationale: |
    Quality Bar cascade is one of the five rule classes published in the
    framework canonical rule catalog (IC-009): upstream Quality Bar failure
    blocks downstream approval, preventing leaf-level rubber-stamping on top
    of a broken parent (TARGET §6). The same class-level binding rationale as
    REQ-010 applies.
  derived_from: [IC-009]
```

### Schema validation (derived from IC-010)

```yaml
- id: REQ-015
  type: functional
  derivation: derived
  statement: |
    When the system runs a validation on an artifact, the system shall validate
    the artifact's front-matter against the framework canonical envelope schema.
  rationale: |
    The envelope schema is the universal front-matter contract every artifact
    must satisfy. Validating envelope conformance gives a clean structural
    floor before per-type validation runs (REQ-016): an artifact that fails
    the envelope cannot be reliably classified for per-type validation.
  derived_from: [IC-010]
```

```yaml
- id: REQ-016
  type: functional
  derivation: derived
  statement: |
    When the system runs a validation on an artifact, the system shall validate
    the artifact against the per-artifact schema corresponding to the artifact's
    declared `artifact_type`.
  rationale: |
    The framework canonical schema set publishes a per-artifact schema for
    each of the six artifact types; per-type schemas tighten the envelope and
    add type-specific structure (e.g. requirements adds REQS- id pattern,
    scope, parent_scope, and the requirement-block $defs). Per-type schema
    validation is the structural rigor mechanism (TARGET §6).
  derived_from: [IC-010]
```

### Quality Bar structural runner (derived from IC-011)

```yaml
- id: REQ-017
  type: functional
  derivation: derived
  statement: |
    When the system runs a validation on an artifact, the system shall evaluate
    every structural-rigor item of the framework canonical Quality Bar
    checklist for that artifact's type.
  rationale: |
    The Quality Bar checklist contains both structural items (mechanically
    evaluable; one shall ↔ one box) and semantic items (interpretation-required;
    AI-skill territory). vmodel-core is mechanical-only (IC-001), so it
    evaluates the structural items and reports them as findings; semantic
    items remain the responsibility of review skills.
  derived_from: [IC-011]
```

### Reporting

```yaml
- id: REQ-018
  type: functional
  statement: |
    When a coverage report is requested for a relationship between two named
    artifact-type sets, the system shall produce a coverage report stating the
    proportion of artifacts of the source set that participate in the
    relationship with at least one artifact of the target set.
  rationale: |
    needs.md (turn 6) commits coverage as one of the four reporting outputs at
    v1, with the example 'percentage of requirements with at least one verifies
    link'. Coverage is a derived aggregate over the traceability graph, distinct
    from per-finding validation output: validation reports rule violations to
    callers about to act; coverage gives a human reader a snapshot of
    relationship completeness.
  derived_from: [NEEDS-vmodel-core]
```

```yaml
- id: REQ-019
  type: functional
  statement: |
    When a completeness report is requested for a named conformance criterion
    (Quality Bar item or validation rule) within a named scope of the spec
    tree, the system shall produce a completeness report stating the count and
    ratio of artifacts in scope that satisfy the criterion and the count and
    ratio that fail to satisfy it.
  rationale: |
    needs.md (turn 6) commits completeness as one of the four reporting outputs
    at v1, with the example 'number of requirements missing a specified Quality
    Bar criterion'. Completeness reports are aggregate counts over the spec
    tree, oriented to a human reading for understanding rather than a caller
    branching on a verdict.
  derived_from: [NEEDS-vmodel-core]
```

```yaml
- id: REQ-020
  type: functional
  statement: |
    When an inventory report is requested for a named scope of the spec tree,
    the system shall produce an inventory report stating the count of artifacts
    in scope, broken down by `artifact_type` and by `scope`.
  rationale: |
    needs.md (turn 6) commits inventory as one of the four reporting outputs at
    v1, with the example '47 requirements, 12 architecture elements, 3 ADRs in
    the tree'. Inventory provides a tree-shape snapshot — the simplest report
    type, but a load-bearing one for reviewers surveying scope-tree health.
  derived_from: [NEEDS-vmodel-core]
```

```yaml
- id: REQ-021
  type: functional
  statement: |
    When an impact-analysis report is requested for a specified artifact, the
    system shall produce an impact-analysis report listing every other
    artifact in the spec tree reachable by forward traversal of canonical
    traceability links (`derived_from`, `allocates`, `verifies`,
    `governing_adrs`, `supersedes`, `superseded_by`) starting from the
    specified artifact.
  rationale: |
    needs.md (turn 6, revised in turn 7) commits impact analysis as one of the
    four reporting outputs at v1 (folded in from the originally-separate
    Querying cluster). The forward-traversal closure semantics align with
    TARGET §8.3 candidate-set propagation: 'tooling walks traceability forward
    from the entry-layer change and produces a candidate set'. The closure is
    bounded to the canonical link types published by the framework
    (link-types.catalog.json), making the report mechanically reproducible.
  derived_from: [NEEDS-vmodel-core]
```

### Output stability (derived from ADR-001)

```yaml
- id: REQ-029
  type: functional
  derivation: derived
  statement: |
    The system shall emit byte-identical output across any two invocations
    against byte-identical input, for all output categories produced
    during validation or reporting runs (finding-records, verdict-records,
    and report content).
  rationale: |
    ADR-001 records that vmodel-core is implemented in Go, whose map
    iteration is randomised by language design. To preserve IC-001
    (determinism — same input produces same output) at the output
    boundary, every emit point that traverses a collection must apply a
    stable order. The requirement is stated at the output level (not as
    an internal sorting discipline) so it is testable at the vmodel-core
    CLI boundary by re-run-and-diff, without inspecting internal
    traversal.
  acceptance: |
    Given any input producing a non-empty output, when vmodel-core is
    invoked twice on byte-identical input, then the two emitted outputs
    are byte-identical.
  derived_from: [ADR-001-implement-vmodel-core-in-go, IC-001]
```

### Schema embedding (derived from ADR-002)

```yaml
- id: REQ-030
  type: functional
  derivation: derived
  statement: |
    The system shall, during any validation or reporting run, use the
    exact versions of the framework canonical rule catalog, framework
    canonical schema set, and framework canonical Quality Bar checklist
    set bundled with the binary at the binary's build time.
  rationale: |
    ADR-002 records that the three canonical input sets are embedded in
    the binary at compile time via Go's embed package, with no runtime
    override. Pinning the enforced versions to those bundled at build
    time ensures version-skew between validator and schemas is
    structurally impossible (an adopter cannot run binary-vN against
    schemas-vM), supporting reproducibility and IC-005's re-download-
    and-replace update model. Queryability of the bundled versions is
    a separate atomic property addressed by REQ-032.
  acceptance: |
    Given any validation or reporting run on any vmodel-core binary,
    when the run completes, then the framework canonical rule catalog
    version, schema set version, and Quality Bar checklist set version
    used by the run are identical to the versions compiled into the
    binary at its build time.
  derived_from: [ADR-002-embed-canonical-schemas-in-binary, IC-005, IC-009, IC-010, IC-011]
```

```yaml
- id: REQ-031
  type: functional
  derivation: derived
  statement: |
    When the system runs a validation or a reporting operation, the
    system shall obtain the framework canonical rule catalog, framework
    canonical schema set, and framework canonical Quality Bar checklist
    set without performing any filesystem read outside the binary
    itself and without performing any network access.
  rationale: |
    ADR-002 records that the three canonical input sets are embedded in
    the binary at compile time. Stating the no-external-access property
    at vmodel-core's external boundary makes it testable by sandbox
    isolation rather than by inspecting internal call graphs. This is
    the load-bearing mechanism by which IC-002 (stateless cold-start)
    is satisfied for catalog and schema availability and by which IC-007
    (no relaxation modes) is enforced for catalog and schema content —
    an adopter cannot substitute a relaxed schema set without rebuilding
    the binary from source.
  acceptance: |
    Given a sandbox with no network access and no readable filesystem
    outside the vmodel-core binary's own path, when the binary is
    invoked for any validation or reporting operation supplied with
    inputs reachable inside the sandbox, then the operation completes
    without filesystem-not-found or network-error conditions on
    framework canonical inputs and produces its expected verdict or
    report.
  derived_from: [ADR-002-embed-canonical-schemas-in-binary, IC-002, IC-007]
```

```yaml
- id: REQ-032
  type: functional
  derivation: derived
  statement: |
    When the system is queried for the bundled versions of the framework
    canonical rule catalog, framework canonical schema set, and framework
    canonical Quality Bar checklist set, the system shall return version
    identifiers identifying the exact versions compiled into the binary
    at the binary's build time.
  rationale: |
    ADR-002 records that the three canonical input sets are embedded in
    the binary at compile time. Making the bundled versions queryable
    lets callers (CI gates, AI orchestrators, direct human callers)
    verify the validator's bundled versions match their expected
    framework versions before relying on validation output, supporting
    supply-chain traceability and reproducibility audits. The query
    surface (which command, which output format) is decided by
    architecture and detailed design; this requirement constrains only
    what is queryable.
  acceptance: |
    Given any vmodel-core binary, when the binary is queried for the
    bundled versions of the canonical rule catalog, schema set, and
    Quality Bar checklist set, then the response identifies the exact
    versions compiled into the binary at its build time.
  derived_from: [ADR-002-embed-canonical-schemas-in-binary, IC-005, IC-009, IC-010, IC-011]
```

## Quality Attributes (NFRs)

```yaml
- id: REQ-022
  type: quality_attribute
  derivation: derived
  planguage:
    scale: |
      Wall-clock time, in milliseconds, from process invocation start to
      verdict-record emission, for a single-artifact validation run on a
      representative artifact within the AI-caller author retry loop.
    meter: |
      Measured at the AI-caller's process boundary (subprocess invocation
      start to first byte of verdict-record on stdout), reported at the p95
      percentile over a sample of N runs (N to be defined at pilot
      calibration), on the target hardware profile (commodity CI runner,
      IC-012).
    fail: "pending — pilot calibration"
    goal: "pending — pilot calibration"
    stretch: "pending — pilot calibration"
    wish: "pending — pilot calibration"
  rationale: |
    needs.md (turn 8) explicitly defers specific latency numbers to pilot
    evidence, on the stated reason that fabricated numbers narrow technology
    selection unnecessarily. The AI-caller author retry loop is named as the
    most latency-sensitive workflow and the one expected to drive future
    calibration; it is therefore the workflow whose latency this NFR captures.
    Scale and meter are filled now because they fix the *shape* of the
    measurement and do not commit a number; the four target slots remain
    pending until pilot evidence sets them.
  derived_from: [NEEDS-vmodel-core, IC-012]
  follow_up:
    - owner: stakeholder (framework author)
      action: "Set fail/goal/stretch/wish target latencies from pilot calibration on the AI-caller author retry loop, on commodity CI runner hardware."
```

```yaml
- id: REQ-023
  type: quality_attribute
  derivation: derived
  planguage:
    scale: |
      Number of artifacts in a spec tree the system can validate in a single
      whole-tree run within the latency target of REQ-022.
    meter: |
      Counted across all artifacts present in the supplied spec tree at the
      start of validation, on the target hardware profile (IC-012).
    fail: "pending — pilot calibration"
    goal: "pending — pilot calibration"
    stretch: "pending — pilot calibration"
    wish: "pending — pilot calibration"
  rationale: |
    needs.md (turn 8) commits the v1 baseline as 'small spec trees in the low
    hundreds of artifacts (the framework author's own projects during pilot)'
    and explicitly leaves specific scale ceilings unset 'to avoid prematurely
    ruling out larger adopter trees in v1.x or v2'. The shape captured here
    is the artifact-count axis with a per-tree-validation latency budget; the
    target slots remain pending until pilot evidence sets them.
  derived_from: [NEEDS-vmodel-core, IC-012]
  follow_up:
    - owner: stakeholder (framework author)
      action: "Set fail/goal/stretch/wish artifact-count thresholds from pilot calibration; revisit the 'low hundreds' framing as it concretises."
```

## Interface Requirements

```yaml
- id: REQ-024
  type: interface
  operation: "vmodel-core validation invocation (CLI subprocess)"

  protocol: |
    Process invocation over the operating-system standard process model. Inputs
    are passed via command-line arguments and / or stdin. Outputs are emitted on
    stdout and stderr, plus an exit-code on process termination.

  message_structure:
    request: |
      pending — the precise command-line surface (subcommand structure, flag
      shape) is deferred to architecture and detailed-design layers. v1
      commitments at requirements scope: (a) inputs identifying the validation
      mode (single-artifact, subtree, whole-tree per REQ-007 / REQ-008 /
      REQ-009) are passable, (b) sibling tools are out of scope (IC-006).
    response_pass:
      - format: |
          One verdict-record (REQ-027) and zero or more finding-records
          (REQ-026), serialised in JSON when JSON format is requested and in
          human-readable text when text format is requested.
      - exit_code: 0 (REQ-028)
    response_fail:
      - format: |
          One verdict-record (REQ-027) and one or more finding-records (REQ-026)
          including at least one blocking finding, serialised in JSON or text.
      - exit_code: 1 (REQ-028)
    response_system_error:
      - format: |
          One verdict-record (REQ-027) with value 'system-error', plus a
          system-error description (failure mode, location). May or may not
          include partial findings emitted before the halt.
      - exit_code: 2 (REQ-028)

  timing: |
    Performance shape per REQ-022; specific targets pending pilot calibration.

  error_handling: |
    Per REQ-004 and REQ-005: non-recoverable system-level failures halt the
    run, skip remaining artifacts, and emit verdict 'system-error' with exit
    code 2. Other CLI-handling concerns (argument validation, unreadable input
    paths before validation begins) are deferred to architecture; v1
    commitment is that argument-level errors do not produce 'fail' or 'pass'
    verdicts (they are system-error or fall outside the validation-run track
    entirely).

  startup_initial_state: |
    Per IC-002, each invocation is independent with no shared mutable state.
    There is no daemon, no warm-up, no persistent connection. Cold-start
    behaviour is the only behaviour.

  precondition:
    - "The supplied input identifies a readable artifact, scope path, or spec-tree root that exists on the filesystem accessible to the invoking process."
    - "The framework canonical rule catalog, schema set, and Quality Bar checklist set are accessible to the invoking process (mechanism for accessibility — e.g. bundled with the binary, located via convention — deferred to architecture)."

  postcondition_on_success:
    - "Exactly one verdict-record (REQ-027) is emitted on stdout, with value matching REQ-002 (pass) or REQ-003 (fail)."
    - "Each rule violation detected during the run is reported as exactly one finding-record (REQ-006, shape per REQ-026) on stdout, alongside the verdict-record."
    - "No artifact in the adopter's spec tree is created, modified, renamed, or deleted by the run (IC-003)."

  postcondition_on_error:
    - "Exactly one verdict-record (REQ-027) is emitted on stdout with value 'system-error' (REQ-005)."
    - "Process exit code is 2 (REQ-028)."
    - "No artifact in the adopter's spec tree is created, modified, renamed, or deleted by the run (IC-003)."

  invariants:
    - "A validation run produces exactly one verdict-record (REQ-001), regardless of outcome."
    - "vmodel-core is read-only on the adopter's spec tree (IC-003)."

  versioning: |
    Version label: v1, increasing monotonically with major version on
    breaking changes. Compatibility regime: additive-only within a major
    version — new subcommands, new optional flags, new fields in JSON output
    records, and new exit-code values for new failure modes are permitted
    within v1; removal of any committed subcommand, flag, JSON field, or
    exit-code value, or change in the runtime semantics of an existing
    element, is a breaking change and requires a major-version increment.
    Deprecation notice period: pending — to be set by a product-scope ADR
    with a minimum-notice commitment before any v1 surface element is
    deprecated; until that ADR is accepted, no deprecation may begin.

  rationale: |
    needs.md (turn 10) commits the rendering surface for validation: exit
    codes 0/1/2 (REQ-028) and output formats JSON (default for AI callers) and
    text (default for human / CI). needs.md (turn 9 + Open gaps) defers the
    rest of the CLI ergonomic shape to pilot evidence; per the upstream-input
    rule (needs.md supersedes framework references on conflict), TARGET §10's
    broader AI-ergonomic CLI patterns do not bind at v1 unless needs.md
    re-promotes them. The versioning shape committed here (v1 label;
    additive-within-major regime) is the standard-engineering interpretation
    of IC-006's 'CLI as a stable contract' constraint — without those two
    commitments, IC-006's 'stable' has no operational meaning. The deprecation
    notice period is the only versioning element genuinely deferred, because
    its specific value (months of notice) is a product-scope policy decision
    rather than a structural property of the contract.
  derived_from: [NEEDS-vmodel-core, IC-006]
  follow_up:
    - owner: stakeholder (framework author)
      action: "Promote committed CLI ergonomic patterns from Open gaps into this requirement (or an additional interface requirement) once pilot evidence and the codex CLI-for-AI-agents pattern page are in place."
    - owner: stakeholder (framework author)
      action: "Author a product-scope ADR setting the CLI deprecation notice period before v1 release; the ADR's accepted notice period replaces the 'pending' clause in this requirement's versioning field."
```

```yaml
- id: REQ-025
  type: interface
  operation: "vmodel-core reporting invocation (CLI subprocess)"

  protocol: |
    Process invocation over the operating-system standard process model. Inputs
    are passed via command-line arguments and / or stdin. Outputs are emitted
    on stdout and stderr, plus an exit-code on process termination.

  message_structure:
    request: |
      pending — the precise command-line surface (subcommand structure, flag
      shape) is deferred to architecture and detailed-design layers. v1
      commitments at requirements scope: inputs identifying the report type
      (coverage / completeness / inventory / impact, REQ-018 to REQ-021) and
      the report's parameters are passable.
    response_normal:
      - format: |
          A single self-contained HTML document (the report). The HTML is
          written to stdout or to a path supplied by the caller; the
          mechanism is deferred to architecture.
      - exit_code: 0
    response_system_error:
      - format: |
          A diagnostic message describing the failure mode and location.
      - exit_code: 2 (mirrors validation-side mapping per REQ-028; reporting
          and validation are surfaces of the same single-binary tool, so they
          share one exit-code mapping rather than two parallel ones).

  timing: |
    Performance shape per REQ-022 applies to reporting too on the same hardware
    profile (IC-012); specific targets pending pilot calibration.

  error_handling: |
    System-level failures (file IO failure, parse crash, internal error,
    corrupted catalog or schema input) halt the report production. The exit-
    code mapping for reporting-side failures is pending; the v1 commitment is
    that reporting failures are distinguishable from successfully-produced
    reports.

  startup_initial_state: |
    Per IC-002, each invocation is independent with no shared mutable state.
    Cold-start is the only state.

  precondition:
    - "The supplied report parameters identify a valid report type and target scope."
    - "The framework canonical rule catalog, schema set, and Quality Bar checklist set are accessible to the invoking process (per REQ-024 precondition)."

  postcondition_on_success:
    - "Exactly one HTML document is emitted (to stdout or to a caller-supplied path; mechanism pending)."
    - "No artifact in the adopter's spec tree is created, modified, renamed, or deleted (IC-003)."

  postcondition_on_error:
    - "A diagnostic message is emitted on stderr identifying the failure mode."
    - "No artifact in the adopter's spec tree is created, modified, renamed, or deleted (IC-003)."

  invariants:
    - "vmodel-core is read-only on the adopter's spec tree (IC-003)."

  versioning: |
    The reporting CLI surface shares the versioning policy of the validation
    CLI surface (REQ-024 versioning): same v1 label, same additive-only-
    within-major compatibility regime extended to reporting-specific surface
    elements (subcommands, flags, HTML structure committed in this
    requirement, exit codes), and same pending deprecation notice period to
    be set by the same product-scope ADR. Treating the two surfaces as one
    versioned contract reflects the single-binary, single-product nature of
    vmodel-core; bifurcating versioning would create cross-surface skew
    inside a single tool.

  rationale: |
    needs.md (turn 10) commits the rendering surface for reporting: HTML (self-
    contained, browseable, aligned with the 'human seeking understanding'
    consumer per turn 6). needs.md (Open gaps) defers whether reporting also
    produces JSON or text variants. Per the upstream-input rule, only HTML is
    committed at v1. Versioning is shared with REQ-024 because the two
    surfaces ship as one binary under one stable-contract commitment (IC-006);
    no needs.md decision separates reporting versioning from validation
    versioning.
  derived_from: [NEEDS-vmodel-core, IC-006]
  follow_up:
    - owner: stakeholder (framework author)
      action: "Decide whether the four reporting output types also need JSON or text variants (programmatic ingestion, terminal viewing); if yes, promote into this requirement or split into per-format interface requirements."
```

## Data Requirements

```yaml
- id: REQ-026
  type: data
  statement: |
    A finding-record shall carry exactly the following five fields: a Locate
    field identifying the artifact and the location within it where the
    violation was detected; an Identify field naming the specific rule that
    was broken, with a value distinguishable from every other rule in the
    framework canonical rule catalog; a Triage field stating the severity of
    the violation as one of blocking, warn-only, or informational; a Summarise
    field carrying a human-readable message describing the violation; and a
    Related-artifacts field listing the other artifacts beyond the primary
    Locate target that participate in the violation (empty when the violation
    is single-artifact).
  rationale: |
    needs.md (turn 4) commits the five-dimension shape with the explicit
    purpose 'sufficient for an AI caller to act on the finding deterministically'.
    Each dimension is named by needs.md (Locate, Identify, Triage, Summarise,
    Related-artifacts); their roles are also named (locate the violation,
    branch on rule identity, gate on severity, render to human consumer, walk
    to other affected artifacts). The five-dimension constraint is the
    behavioural bedrock of every AI-caller-side workflow that consumes
    findings; collapsing or omitting a dimension breaks the AI-caller contract.
  acceptance: |
    Given any finding-record emitted by vmodel-core, when the record's fields
    are inspected, then all five fields are present; the Triage field's value
    is one of {blocking, warn-only, informational}; the Identify field's value
    resolves to a unique rule in the framework canonical rule catalog; the
    Related-artifacts field is a list (empty when the violation is single-
    artifact, non-empty otherwise).
  derived_from: [NEEDS-vmodel-core, REQ-006]
```

```yaml
- id: REQ-027
  type: data
  statement: |
    A verdict-record shall carry exactly one value drawn from the closed set
    {pass, fail, system-error}.
  rationale: |
    needs.md (turn 5) commits these three values exhaustively, with the
    explicit observation that 'rule-class taxonomy (schema / traceability /
    Quality Bar) is not aggregated into the verdict — it lives in the per-
    finding Identify dimension'. A closed three-value set is what makes
    shell-driven gating (CI, human terminal use) deterministic and what makes
    AI-caller branching on the verdict tractable.
  acceptance: |
    Given any verdict-record emitted by vmodel-core, when the record's value
    is inspected, then it is exactly one of pass, fail, or system-error and
    no other value is permitted.
  derived_from: [NEEDS-vmodel-core, REQ-001]
```

```yaml
- id: REQ-028
  type: data
  statement: |
    The validation invocation's process exit code shall map to the verdict-
    record value as follows: 0 corresponds to pass, 1 corresponds to fail, 2
    corresponds to system-error.
  rationale: |
    needs.md (turn 10) commits the sysexits-style 0 / 1 / 2 mapping for shell-
    driven consumers (CI gates, direct human terminal use). This is the
    rendering of the verdict shape (REQ-027) onto the operating-system
    process-termination contract; it is what lets `if vmodel-core validate …;
    then …; fi` work in CI scripts without parsing stdout.
  acceptance: |
    Given any validation invocation that emits a verdict-record with value V,
    when the process terminates, then the exit code is 0 if V is pass, 1 if V
    is fail, and 2 if V is system-error.
  derived_from: [NEEDS-vmodel-core, REQ-027]
```

## Open gaps and follow-ups

These items are surfaced rather than silently passed, per the no-fabrication
discipline (`references/rationale-and-traceability.md`). Each has an owner and
an action; the document remains in `status: draft` until the gaps that block
v1 baselining are closed (or explicitly accepted as v1.x).

- **`derived_from` placeholder `NEEDS-vmodel-core` is not in the canonical
  artifact set.**
  - *Owner*: framework author.
  - *Action*: resolve as part of elicit-needs decision γ (`issues_found.md`
    Issue 1, Issue 2). Two coherent paths: (a) author a vmodel-core
    Product Brief and re-anchor `derived_from` to `PB`; (b) promote `needs.md`
    into the canonical artifact set with its own id pattern, and update this
    document and the schemas accordingly. Until then, the traceability rule
    `TRV-REF-001` will produce a finding on this artifact when run by
    vmodel-core itself — that finding is a deliberate pilot data point.

- **No parent-scope (VModelWorkflow-level) Requirements artifact exists.**
  - *Owner*: framework author.
  - *Action*: per `issues_found.md` Issue 2, framework-level needs should be
    elicited first, then per-product needs cascaded down. When a parent-scope
    Requirements is authored, this document's `parent_scope` and `derived_from`
    must be revised; some constraints currently scoped here may move up.

- **NFR target slots (`fail`/`goal`/`stretch`/`wish`) are pending pilot
  calibration on REQ-022 and REQ-023.**
  - *Owner*: framework author (in dogfooding pilot role).
  - *Action*: set the four target slots per NFR from pilot calibration; revise
    this document to baselined `status: active` once thresholds are committed.

- **CLI ergonomic shape beyond exit codes and output formats is deferred.**
  - *Owner*: framework author.
  - *Action*: revisit once pilot evidence and the engineering-codex
    `pat-cli-design-for-ai-agents` pattern page are in place; promote
    committed patterns into REQ-024 (or as additional interface requirements)
    at that point. Patterns currently deferred include: subcommand /
    resource-verb structure, non-interactive default, idempotency,
    `--dry-run` / `--yes` / `--force`, stdin acceptance for inputs,
    progressive `--help`, structured-data-on-success rendering, and
    `--verbose` / `--quiet`.

- **Reporting output formats beyond HTML are deferred.**
  - *Owner*: framework author.
  - *Action*: decide whether the four reporting outputs also need JSON
    (programmatic dashboard ingestion) or text (terminal viewing) variants;
    promote into REQ-025 or split into per-format interface requirements.

- **Open-source licence is not yet selected.**
  - *Owner*: framework author.
  - *Action*: author a product-scope ADR selecting a specific licence (per
    IC-008) before v1 release.

- **CLI deprecation notice period is not yet committed.**
  - *Owner*: framework author.
  - *Action*: author a product-scope ADR setting the minimum deprecation
    notice period for v1 surface elements before v1 release; the version
    label (v1) and compatibility regime (additive-only-within-major) are
    committed by REQ-024 (and shared by REQ-025), so only the notice period
    needs the ADR. Until the ADR is accepted, no deprecation may begin.

- **Success metrics are deliberately unset at v1.**
  - *Owner*: framework author.
  - *Action*: per needs.md (turn 11), specific metrics for vmodel-core's
    production success will be set from pilot evidence (framework-author
    dogfooding, Phase 5 skill usage data, CI integration signal). Not a
    blocker for v1; tracked as living follow-up.
