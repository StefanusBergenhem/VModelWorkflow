---
id: DD-validation-engine
title: "Detailed Design — validation-engine"
artifact_type: detailed-design
scope: validation-engine
parent_scope: ""
parent_architecture: ARCH
derived_from:
  - REQ-004
  - REQ-006
  - REQ-010
  - REQ-011
  - REQ-012
  - REQ-013
  - REQ-014
  - REQ-015
  - REQ-016
  - REQ-017
  - REQ-026
  - ARCH-IF-IValidate
governing_adrs:
  - ADR-001-implement-vmodel-core-in-go
  - ADR-002-embed-canonical-schemas-in-binary
status: draft
date: "2026-05-11"
version: 1
---

# Detailed Design — validation-engine

## Overview

`validation-engine` is the domain component that runs all mechanical validations
against the parsed artifact set and the traceability graph, streaming a sequence of
finding-records as its sole output. It realises the slice allocated by `ARCH`'s
`validation-engine` Decomposition entry — envelope + per-type schema validation
(REQ-015, REQ-016), five rule-catalog categories (REQ-010..REQ-014), and Quality Bar
structural evaluation (REQ-017) — and is the sole producer of finding-records in the
system (REQ-006). It serves the `IValidate` interface contract (ARCH-IF-IValidate);
canonical parent is present.

The leaf is structured as a single public entry point (`Validate`) that executes three
sequential internal passes — schema validation, rule-catalog evaluation, and Quality Bar
structural evaluation — and emits findings from all three passes onto one channel. The
internal split (schema-validator / rule-evaluator / QB-runner) is resolved here as three
passes within one engine rather than three sibling components: a single-component design
avoids an internal coordination interface (no separate orchestration call path from
cli-adapter to three entry points) while the three-pass sequencing keeps each concern
independently testable. Constraint kind: architectural — a single composition locus
follows from cli-adapter's single IValidate call site (ARCH Composition / Wiring). The
parent Architecture's DEFER-ADR for this split is resolved at this DD level; it does not
warrant an ADR because it is single-scope, low reversibility cost, and entails no
cross-cutting consequences.

The leaf consumes `FrameworkResources` (from `embedded-resources`) for rule catalog,
schemas, and Quality Bar checklists. It receives `ArtifactSet` and `TraceabilityGraph`
from `cli-adapter` (produced by `artifact-loader` and `graph-builder` respectively). It
produces a channel of `Finding` records consumed by `emitter` (via `IEmit`). The leaf
contains no persistent state — each `Validate` call is independent per IC-002.

## Public Interface

```yaml
public_interface:

  - name: NewValidationEngine
    signature: "NewValidationEngine(resources FrameworkResources) ValidationEngine"
    description: |
      Construct the implementation of the IValidate contract, bound to the
      provided FrameworkResources instance for rule catalog, schema, and Quality
      Bar checklist access. Called once at the composition root; injected via
      interface type (per ARCH Composition / Wiring). No on_failure path: nil
      resources is a programming error caught at composition-root construction
      time before this call is reached; the Go runtime panics on any nil-pointer
      dereference if the caller violates the precondition (process terminates;
      no partial state).
    preconditions:
      - "resources is non-nil."
    postconditions:
      on_success:
        - "Returns a non-nil ValidationEngine whose Validate method uses resources
           for all framework canonical input access."
      on_failure: []
    invariants: []
    errors: []
    side_effects:
      - "None."
    thread_safety: thread-safe
    nullability:
      - "resources: must not be nil."
      - "return: must not be nil."
    complexity_notes: "O(1)."

  - name: Validate
    signature: "Validate(set ArtifactSet, graph TraceabilityGraph, mode ValidationMode) (<-chan Finding, error)"
    description: |
      Execute three sequential validation passes against the provided ArtifactSet
      and TraceabilityGraph — (1) schema validation, (2) rule-catalog evaluation,
      (3) Quality Bar structural evaluation — streaming Finding records on the
      returned channel as they are produced. Implements IValidate
      (ARCH-IF-IValidate). This is the sole public method that produces
      finding-records (REQ-006).
    preconditions:
      - "set is non-nil and well-formed (stable iteration order; each Artifact
         carries a non-empty artifact_type matching a canonical ArtifactType
         enum value)."
      - "graph is non-nil and well-formed (built by graph-builder over the same
         ArtifactSet or a superset of it; CycleFindings field populated by
         graph-builder per the inter-leaf contract described in Algorithms)."
      - "mode is one of the three canonical ValidationMode values
         (single-artifact | subtree | whole-tree)."
    postconditions:
      on_success:
        - "Emits zero or more Finding records; each Finding carries all five
           REQ-026 fields: artifact_path (non-empty), location_within_artifact,
           rule_id (non-empty, resolves to a rule or schema-violation identifier),
           severity (blocking | warn-only | informational), message (non-empty),
           related_artifacts (empty for single-artifact violations)."
        - "All five rule classes are evaluated per the mode-gating table (REQ-010..REQ-014);
           envelope and per-type schema evaluated for every artifact in set
           (REQ-015/016); QB structural items evaluated for every artifact in set
           (REQ-017)."
        - "Channel is closed when all three passes complete and all findings have
           been emitted."
        - "Findings from each pass are emitted in artifact-path lexicographic
           order; within a single artifact, in location-within-artifact order.
           Realises ARCH-IF-IValidate invariant: 'findings emitted in source-document
           iteration order on the channel'; byte-stable total ordering applied
           downstream by emitter (REQ-029).
           [NEEDS-TEST: contract test — given a two-artifact ArtifactSet where both produce findings, all findings for the lexicographically earlier artifact_path appear on the channel before any findings for the later path]"
        - "Output is a function of (set, graph, mode, resources.contents) only —
           no filesystem read outside the binary, no network access (REQ-031)."
      on_precondition_failure:
        - "Returns a nil channel and ErrPreconditionFailed; no findings emitted;
           no state mutation (leaf is stateless)."
      on_downstream_failure:
        - "Closes the channel after emitting any findings produced before the
           failure; returns ErrSystemError (REQ-004 halt-and-report); remaining
           artifacts in the current pass are not evaluated."
    invariants:
      - "validation-engine is the sole producer of Finding records emitted on
         the returned channel, including cycle findings re-emitted from
         graph.CycleFindings (REQ-006; rationale: centralises REQ-026 shaping at
         one boundary; see Algorithms — Pass 2 for the cycle re-emission design)."
      - "No artifact in any ArtifactSet is created, modified, renamed, or deleted
         by the call (IC-003)."
      - "The multiset of findings is identical across two calls with byte-identical
         inputs; ordering is deterministic per the artifact-path + location ordering
         rule above (REQ-029 at this boundary).
         [NEEDS-TEST: property test — two Validate calls on the same engine with byte-identical (set, graph, mode) yield byte-identical Finding sequences in the same channel order]"
    errors:
      - error: "ErrPreconditionFailed"
        raised_when: "set is nil, graph is nil, or mode is not a canonical
          ValidationMode value."
        meaning: "Caller bug — contract precondition violated before any
          evaluation began."
      - error: "ErrSystemError"
        raised_when: "Any non-recoverable failure during evaluation: schema library
          parse or evaluation error on bundle content; ErrUnknownArtifactType from
          resources (indicates bundle inconsistency at runtime, treated as
          non-recoverable per REQ-004); any internal error preventing production
          of authoritative findings."
        meaning: "Non-recoverable per REQ-004; run halted; remaining artifacts
          not evaluated; emitter will set verdict to system-error."
    side_effects:
      - "Writes Finding records to the returned channel; no other side effects."
    cancellation: |
      The IValidate interface (ARCH-IF-IValidate) carries no context.Context
      parameter; no cancellation signal is available to validation-engine at this
      interface level. The caller (cli-adapter) MUST drain the channel to
      completion (read all values until the channel is closed). Abandoning the
      channel before closure causes any in-progress producer goroutine to block
      indefinitely on channel send, constituting a goroutine leak. Cancellation
      protocol extension (e.g., adding context.Context to IValidate) is an
      Architecture-level change — constraint kind: architectural.
      [DEFER-DD: validation-engine — channel cancellation protocol if needed
      post-pilot; requires IValidate signature change at ARCH level]
    thread_safety: thread-safe
    nullability:
      - "set: must not be nil."
      - "graph: must not be nil."
      - "return channel: non-nil on the success and on_downstream_failure paths;
         nil on ErrPreconditionFailed."
      - "return error: nil on the success path; non-nil (ErrPreconditionFailed or
         ErrSystemError) otherwise."
    complexity_notes: |
      O(N × R) in the number of artifacts N and rules R — the dominant term from
      the rule-catalog pass. Per-rule-class scaling breakdown:
      [DEFER-DD: validation-engine — per-rule-class scaling characteristics]
      (deferred to implementation-time pilot calibration per ARCH quality-attributes
      allocation for validation-engine; REQ-023 scale targets also pending
      calibration).
```

## Data Structures

```yaml
data_structures:

  - name: ValidationEngine
    description: |
      Implementation of the IValidate contract. Carries the FrameworkResources
      dependency (injected at construction) and exposes the Validate entry point.
      The only field is the resources reference; all per-call state is local to
      the Validate stack frame.
    fields:
      - name: resources
        type: "FrameworkResources (interface)"
        invariant: "Non-nil at all times after construction (NewValidationEngine
          precondition); provides RuleCatalog, Schema, EnvelopeSchema,
          QualityBarChecklist, and Versions. Content is immutable for the binary's
          lifetime (ADR-002 / ARCH-IF-IFrameworkResources)."
    ownership: "Constructed once at the composition root; owned by the composition
      root; held by cli-adapter via the ValidationEngine interface type."
    lifetime: "Process lifetime — one instance per binary invocation (IC-002)."
    returned_semantics: "Not returned across the public interface."

  - name: Finding
    description: |
      The five-field finding-record per REQ-026 (Locate, Identify, Triage,
      Summarise, Related-artifacts). validation-engine is the sole constructor
      and producer of this type (REQ-006). Emitted on the Validate channel;
      ownership transferred to emitter on send.
    fields:
      - name: artifact_path
        type: "non-empty string"
        invariant: "Identifies the primary artifact where the violation was
          detected; matches an artifact's path field in the ArtifactSet for
          the run (REQ-026 Locate: artifact dimension)."
      - name: location_within_artifact
        type: "string"
        invariant: "Specific location within artifact_path where the violation
          is detectable — a front-matter key path, a line number, or a section
          heading. May be empty for findings that are artifact-level (e.g.,
          an artifact with no matching per-type schema — the violation has no
          sub-artifact location). (REQ-026 Locate: within-artifact dimension)."
      - name: rule_id
        type: "non-empty string"
        invariant: "Resolves to a rule identifier in either the framework canonical
          rule catalog (TRV-* namespace) or the schema-violation identifier
          namespace (SCH-* namespace, see Algorithms Pass 1). Unique within its
          namespace. (REQ-026 Identify)."
      - name: severity
        type: "Severity enum value"
        invariant: "Exactly one of: blocking | warn-only | informational.
          Determined per-rule: TRV-* catalog rules carry a severity field;
          schema violations default to blocking unless the schema-violation
          namespace specifies otherwise. (REQ-026 Triage)."
      - name: message
        type: "non-empty string"
        invariant: "Human-readable description of the specific violation —
          names what property was violated, what was observed, and (for
          reference-integrity violations) what the unresolved target was.
          (REQ-026 Summarise)."
      - name: related_artifacts
        type: "list of non-empty strings (artifact paths)"
        invariant: "Empty when the violation is single-artifact (e.g., schema
          violation, per-artifact QB item). Non-empty when other artifacts
          participate — e.g., TRV-REF-001: the artifact with the broken link
          and the expected-but-absent target artifact. Elements are disjoint
          from artifact_path. (REQ-026 Related-artifacts)."
    ownership: "Constructed by validation-engine within the Validate call;
      ownership transferred to channel consumer on channel send."
    lifetime: "Per-finding; construction to channel-send is validation-engine's
      responsibility; post-send lifetime belongs to the channel consumer
      (emitter)."
    returned_semantics: "Ownership transfer — validation-engine sends; emitter
      receives ownership."

  - name: ValidationMode
    description: |
      Closed enum naming the three invocation scopes (REQ-007, REQ-008, REQ-009).
      Governs which rules are eligible for evaluation per the mode-gating
      decision table in Algorithms.
    fields:
      - name: value
        type: "enum"
        invariant: "Exactly one of: single-artifact | subtree | whole-tree.
          Strings match the IValidate architecture-level definition."
    ownership: "Defined at this scope; passed by value from cli-adapter."
    lifetime: "Call-scoped."
    returned_semantics: "Pass-by-value; not returned."

  - name: Severity
    description: |
      Closed enum for the Triage field of a Finding (REQ-026).
    fields:
      - name: value
        type: "enum"
        invariant: "Exactly one of: blocking | warn-only | informational.
          Values match the REQ-026 Triage dimension's closed set."
    ownership: "Embedded in Finding."
    lifetime: "Governed by the enclosing Finding."
    returned_semantics: "Embedded in Finding; Finding's ownership governs."
```

## Algorithms

### Three-pass structure

`Validate` executes three passes in fixed order. Findings from all three passes are
emitted onto the same channel; the passes are not parallelised (sequential ordering
preserves the artifact-path + location emission order invariant without a merge step).
A system-error in any pass closes the channel and returns `ErrSystemError`; the
remaining passes do not execute.

**Pass 1 — Schema validation (REQ-015 + REQ-016)**

For each artifact in `set`, in lexicographic artifact-path order:

1. Validate the artifact's front-matter against `resources.EnvelopeSchema()` (REQ-015).
   Emit one `Finding` per schema violation. Rule IDs for schema violations use the
   `SCH-ENV-*` namespace (see schema-violation rule_id note below).
2. Validate the artifact's front-matter against `resources.Schema(artifact.artifact_type)`
   (REQ-016). Emit one `Finding` per schema violation. Rule IDs use the `SCH-TYPE-*`
   namespace. Where a schema violation overlaps with a TRV-* catalog rule (per the
   rule catalog's `overlaps_with_schema` notes for TRV-RETRO-001 and TRV-COMP-004),
   emit the TRV-* rule_id, not the SCH-TYPE-* id, to avoid duplicate findings from
   Pass 2 for the same violation.

**Result property:** after Pass 1, every Finding on the channel for which the root
cause is a schema-structural violation carries a non-empty rule_id from the `SCH-*`
or overlapping `TRV-*` namespaces, and the finding's artifact_path + location
identifies the specific front-matter key path that failed.

**Schema-violation rule_id namespace:**
`[DEFER-DD: validation-engine — schema-violation rule_id namespace and SCH-*/TRV-*
overlap mapping]` — constraints: rule IDs must be stable across runs (REQ-029), must
be distinguishable from all TRV-* IDs (REQ-026 Identify), and must not duplicate
findings with Pass 2 for violations already named in the catalog. Exact prefix scheme
and per-schema-keyword mapping deferred to implementation; the constraint set above is
contractual.

**JSON Schema library:**
`[DEFER-DD: validation-engine — JSON Schema 2020-12 validator library selection]` —
constraints from governing ADRs: pure Go, no CGO (ADR-001 static binary,
CGO_ENABLED=0), must support JSON Schema draft 2020-12, no filesystem read at
validation time (REQ-031 — schemas arrive as byte slices from FrameworkResources).
Candidate evaluation at pilot implementation.

---

### Pass 2 — Rule-catalog evaluation (REQ-010..REQ-014)

For each rule in `resources.RuleCatalog()`, grouped by category, evaluated in the
order: `reference_integrity`, `completeness`, `cycle`, `retrofit`, `cascade`.

**Cycle findings — re-emission design.** Cycle findings are computed by graph-builder
as a structural property of the TraceabilityGraph (per graph-builder's allocation of
REQ-012 in ARCH Decomposition). They are made available to validation-engine via a
`CycleFindings []Finding` field on `TraceabilityGraph` (inter-leaf contract: the
graph-builder DD must expose this field; if graph-builder returns `[]Finding`
separately from `Build`, they are also embedded in the graph so that Validate's
single-parameter form receives them). In the `cycle` category sub-pass, validation-engine
reads `graph.CycleFindings` and emits each entry onto the channel. This keeps
validation-engine the sole producer of finding-records on the emitter's channel (REQ-006)
without requiring a separate IValidate parameter or cli-adapter becoming a finding
emitter.

`[DEFER-DD: graph-builder — TraceabilityGraph must carry CycleFindings []Finding for
validation-engine re-emission; coordinate with graph-builder DD authoring]`

**Mode-gating — which rules evaluate per ValidationMode:**

Rules divide into two classes based on whether they require a complete corpus to
produce authoritative findings:

- **Per-artifact rules** — evaluate one artifact in isolation; always run in all modes.
- **Corpus-dependent rules** — require all artifacts in the relevant scope to be present
  in `set`; running them on an incomplete set produces spurious findings (false positives
  for missing artifacts that simply were not loaded).

| Rule(s) | Class | single-artifact | subtree | whole-tree |
|---|---|---|---|---|
| TRV-REF-001 (link target resolves) | Per-artifact for in-set targets; corpus-dependent for out-of-set | Evaluate only links whose targets are present in `set`; skip links to absent targets | Evaluate all links in the subtree corpus | Evaluate all links |
| TRV-REF-002 (scope reference resolves) | Per-artifact | Evaluate | Evaluate | Evaluate |
| TRV-COMP-001 (every requirement allocated) | Corpus-dependent | Skip | Evaluate within subtree | Evaluate |
| TRV-COMP-002 (every arch child allocates) | Corpus-dependent | Skip | Evaluate within subtree | Evaluate |
| TRV-COMP-003 (every REQ + DD contract verified) | Corpus-dependent (requires cross-artifact verifies links) | Skip | Evaluate within subtree | Evaluate |
| TRV-COMP-004 (every test case has verifies) | Per-artifact | Evaluate | Evaluate | Evaluate |
| TRV-COMP-005 (leaf has DD + TestSpec) | Corpus-dependent (requires scope-tree view) | Skip | Evaluate within subtree | Evaluate |
| TRV-COMP-006 (non-leaf has REQ+ARCH+TS) | Corpus-dependent | Skip | Evaluate within subtree | Evaluate |
| TRV-COMP-007 (ADR consequence anchored) | Corpus-dependent | Skip | Evaluate within subtree | Evaluate |
| TRV-CYCLE-001, TRV-CYCLE-002 | Pre-computed; re-emitted from graph | Re-emit graph.CycleFindings scoped to links in `set` | Re-emit scoped | Re-emit all |
| TRV-RETRO-001 (no reconstructed on human-only fields) | Per-artifact | Evaluate | Evaluate | Evaluate |
| TRV-QB-001 (Quality Bar cascade) | Corpus-dependent (requires ancestor-scope artifacts) | Skip | Evaluate within subtree | Evaluate |
| TRV-SCOPE-001 (no reserved-name scope collision) | Corpus-dependent (scope-tree view) | Skip | Evaluate within subtree | Evaluate |
| TRV-BUNDLE-001 (architecture bundle back-link) | Per-artifact (checks belongs_to + subject) | Evaluate if target in set | Evaluate | Evaluate |

**Result property:** after Pass 2, every Finding on the channel for which the root
cause is a rule-catalog violation carries a `rule_id` that matches a `rules[].id`
value in the framework canonical rule catalog (or is re-emitted from
`graph.CycleFindings` with its original rule_id). No rule is evaluated more than once
per artifact per run. Mode-gated skips do not produce findings (silence is the correct
output for a rule that cannot be evaluated given the provided corpus).

---

### Pass 3 — Quality Bar structural evaluation (REQ-017)

For each artifact in `set`, in lexicographic artifact-path order:

1. Call `resources.QualityBarChecklist(artifact.artifact_type)` to obtain the
   per-artifact Quality Bar checklist.
2. For each item in the checklist whose `evaluable: structural` flag is true, evaluate
   the mechanical check against the artifact's content.
3. Emit one `Finding` per structural item that fails. Semantic items (those whose
   `evaluable: semantic` flag is true) are skipped — they require interpretation and
   belong to AI review skills (IC-001).

**Result property:** after Pass 3, every Finding on the channel for which the root
cause is a Quality Bar structural item failure carries a `rule_id` from the QB namespace
(format TBD at implementation; constraint kind: temporal — deferred to implementation
once the QB checklist JSON schema pins a stable item-id field; must be stable,
distinguishable from TRV-* and SCH-*), a `severity` drawn from the QB checklist item's severity field, and a
`location_within_artifact` identifying the section or field where the structural item
was expected but missing or malformed.

## State

Stateless between calls. `ValidationEngine` carries only the immutable
`FrameworkResources` reference, whose content is fixed at binary build time (ADR-002).
No per-call state escapes the `Validate` stack frame. Every call is independent per
IC-002.

## Error Handling

| Error | Detection | Containment | Recovery | Caller receives |
|---|---|---|---|---|
| `ErrPreconditionFailed` | Precondition check at entry to `Validate` — `set` is nil, `graph` is nil, or `mode` is not a canonical ValidationMode value | Reject at the leaf's boundary before any pass begins | fail-fast | nil channel + non-nil `ErrPreconditionFailed`; no findings emitted; no state mutation |
| `ErrSystemError` from schema library | Schema library returns a parse or evaluation error when processing a bundle-origin schema (envelope or per-type) against artifact front-matter bytes during Pass 1 | Translate at the pass boundary into `ErrSystemError`; close the channel after any pre-halt findings | propagate (translate lower-layer library error into domain `ErrSystemError`; original error preserved as cause for diagnostics) | Non-nil `ErrSystemError` returned; channel closed after pre-halt findings; emitter sets verdict to system-error (REQ-004 / REQ-005) |
| `ErrSystemError` from `ErrUnknownArtifactType` | `resources.Schema(t)` or `resources.QualityBarChecklist(t)` returns `ErrUnknownArtifactType` during Pass 1 or Pass 3 — an artifact's `artifact_type` is not in the canonical ArtifactType enum | Treat as bundle inconsistency (an artifact with a non-canonical type passed ArtifactSet construction — indicates schema is out of sync with the binary); translate to `ErrSystemError` | propagate (bundle inconsistency is non-recoverable per REQ-004; not a per-artifact skip) | Non-nil `ErrSystemError` returned; channel closed after pre-halt findings; emitter sets verdict to system-error |

**State after error (all rows):** stateless leaf — no state mutation on any error path;
pre-halt findings already emitted to the channel are not retracted.

**TestSpec cues (leaf scope — unit):**

- **Contract tests** — success-path postconditions on `Validate` for each mode:
  single-artifact with valid inputs produces findings only from per-artifact rules;
  whole-tree mode with a multi-artifact fixture produces all applicable rule-class
  findings. `NewValidationEngine` with a non-nil resources returns non-nil engine.
- **Robustness tests** — one per error-matrix row:
  - `ErrPreconditionFailed`: nil set, nil graph, zero-value mode each produce nil channel
    + `ErrPreconditionFailed`.
  - `ErrSystemError` from schema library: inject a malformed schema byte slice via a
    fake `FrameworkResources`; assert channel closes + `ErrSystemError` returned.
  - `ErrSystemError` from `ErrUnknownArtifactType`: inject an artifact with a
    non-canonical `artifact_type`; assert channel closes + `ErrSystemError` returned.
- **Property tests** — on Validate with a fixture ArtifactSet:
  - Determinism: two calls with byte-identical inputs return byte-identical Finding
    sequences (REQ-029 at this boundary).
  - Sole producer: every Finding on the channel carries a non-empty rule_id from one
    of the three namespaces (TRV-*, SCH-*, QB-*) — no empty or fabricated rule_ids.
  - Mode isolation: single-artifact mode on a fixture that would trigger
    TRV-COMP-005/006 produces no findings from those corpus-dependent rules.
- **TestSpec traceability stubs:**
  - `[NEEDS-TEST: contract test — Pass 1 envelope schema violation produces Finding
    with SCH-ENV-* rule_id and correct artifact_path + location]`
  - `[NEEDS-TEST: contract test — Pass 1 per-type schema violation with TRV-RETRO-001
    overlap emits TRV-RETRO-001 rule_id, not a duplicate SCH-TYPE-* finding]`
  - `[NEEDS-TEST: contract test — Pass 2 cycle category re-emits graph.CycleFindings
    unchanged on the output channel]`
  - `[NEEDS-TEST: contract test — Pass 3 semantic QB items are not evaluated; only
    structural items produce findings]`
  - `[NEEDS-TEST: property test — REQ-031 compliance: fake FrameworkResources that
    panics on any real filesystem access is never triggered during Validate]`
