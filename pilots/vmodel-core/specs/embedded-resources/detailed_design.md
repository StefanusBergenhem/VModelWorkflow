---
id: DD-embedded-resources
title: "Detailed Design — embedded-resources"
artifact_type: detailed-design
scope: embedded-resources
parent_scope: ""
parent_architecture: ARCH
derived_from:
  - REQ-030
  - REQ-031
  - REQ-032
  - ARCH-IF-IFrameworkResources
governing_adrs:
  - ADR-002-embed-canonical-schemas-in-binary
status: draft
date: "2026-05-11"
version: 1
---

# Detailed Design — embedded-resources

## Overview

`embedded-resources` is the driven adapter that owns read-only access to the three framework canonical input sets — the rule catalog, the per-artifact schema set (including the universal envelope schema), and the per-artifact Quality Bar checklist set — together with the version manifest naming the synced source versions. It realises the architectural slice allocated by `ARCH`'s `embedded-resources` Decomposition entry and serves the `IFrameworkResources` interface contract (see `ARCH-IF-IFrameworkResources`); canonical parent is present.

The leaf is a thin typed-accessor shell over a process-singleton `embed.FS` whose contents are fixed at build time (per ADR-002). Posture is *immutable after construction*: the constructor binds the embed.FS bytes once at the composition root (`cmd/vmodel-core/main.go`), and every accessor returns a read-only view of the same compile-time bytes for the binary's lifetime. There is no override surface — no flag, no environment variable, no filesystem-priority fallback — because the *absence* of an override path is the structural enforcement of IC-007 (see ADR-002). Eager-versus-lazy decode of the bundle is the implementer's choice, bounded by the byte-identical-across-lifetime postcondition and the read-only-returned-content invariant.

The leaf consumes nothing from siblings. It produces typed accessor results to three callers — `validation-engine` (for IC-009 / IC-010 / IC-011 enforcement, REQ-015..REQ-017), `reporter` (for the same canonical inputs when rendering reports), and `cli-adapter` (for serving `Versions()` to a future `--version` subcommand satisfying REQ-032). Returned wrapper types over raw JSON bytes deliberately keep schema-library parsing at `validation-engine` scope, where the schema-library selection is already marked deferred in the parent Architecture's `validation-engine` decomposition entry.

## Public Interface

```yaml
public_interface:

  - name: NewEmbeddedResources
    signature: "NewEmbeddedResources() FrameworkResources"
    description: |
      Construct the singleton implementation of the IFrameworkResources contract,
      bound to the binary's compile-time embed.FS bundle. Called once at the
      composition root.
    preconditions:
      - "Called from the composition root; not invoked from inner-domain code (per ARCH Composition / Wiring — constructor injection at a single point)."
    postconditions:
      on_success:
        - "Returns a non-nil FrameworkResources whose accessors are bound to the compile-time embed.FS contents."
        - "Successive accessor calls on the returned value yield content byte-identical to the bytes synced into the binary's embed.FS at build time (REQ-030)."
      on_failure:
        - "No on_failure branch at runtime — absence of a required bundle file is a build-time link failure surfaced by the build pipeline's sync step (ADR-002 Propagation; ARCH-IF-IFrameworkResources errors: 'bundle absence is a build-time failure')."
    invariants:
      - "Does not perform any filesystem read outside the binary's own bytes (REQ-031)."
      - "Does not perform any network access (REQ-031)."
    errors: []
    side_effects:
      - "May read and decode all bundle entries during construction (eager decode), or defer decode to first-access (lazy decode with single-flight publication). Choice is implementer's; both branches satisfy the postconditions and invariants."
    thread_safety: thread-safe
    nullability:
      - "return: must not be nil; the constructed value is the only legal source of accessor calls."
    complexity_notes: "Construction completes in O(B) in the bundle's total decoded size, B; B is sub-megabyte at v1 scope (ADR-002 Assumption #5)."

  - name: RuleCatalog
    signature: "RuleCatalog() RuleCatalog"
    description: |
      Return the bundled framework canonical rule catalog (REQ-030); the
      authoritative input set for IC-009 / REQ-010..REQ-014.
    preconditions:
      - "None beyond being callable on a value returned by NewEmbeddedResources."
    postconditions:
      on_success:
        - "Returned RuleCatalog wraps the bytes of bundle/traceability/validation-rules.catalog.json as synced into the binary at build time."
        - "Across the binary's lifetime, every call to RuleCatalog returns a value whose underlying bytes compare byte-identical to the bytes from any prior call on the same binary (REQ-030; supports REQ-029 at this boundary)."
    invariants: []
    errors: []
    side_effects:
      - "None."
    thread_safety: thread-safe
    nullability:
      - "return: must not be the zero value of RuleCatalog."
    complexity_notes: "O(1) when decoded eagerly; O(B_rules) on first access when decoded lazily — B_rules sub-megabyte (ADR-002 Assumption #5)."

  - name: Schema
    signature: "Schema(artifactType ArtifactType) (Schema, error)"
    description: |
      Return the per-artifact JSON Schema corresponding to artifactType
      (REQ-030); consumed by validation-engine to satisfy REQ-016.
    preconditions:
      - "artifactType is one of the six canonical enum values (see Data Structures: ArtifactType)."
    postconditions:
      on_success:
        - "Returned Schema wraps the bytes of bundle/artifacts/<artifactType>.schema.json as synced into the binary at build time."
        - "Across the binary's lifetime, every call with the same artifactType returns a value whose underlying bytes compare byte-identical to those from any prior call with the same artifactType on the same binary (REQ-030)."
      on_failure:
        - "On artifactType not in the canonical set: returns the zero value of Schema together with ErrUnknownArtifactType; no observable state change (leaf is stateless)."
    invariants: []
    errors:
      - error: "ErrUnknownArtifactType"
        raised_when: "artifactType is not one of the six canonical enum members."
        meaning: "Caller bug — input outside the closed enum (the enum is the contract; relaxation by a non-canonical value is structurally refused per IC-007)."
    side_effects:
      - "None."
    thread_safety: thread-safe
    nullability:
      - "artifactType: must not be the zero value of ArtifactType."
      - "return Schema: zero value on the error branch; non-zero on success."
      - "return error: nil on success; non-nil ErrUnknownArtifactType on the precondition-violation branch."
    complexity_notes: "O(1) lookup over the closed enum (six entries)."

  - name: EnvelopeSchema
    signature: "EnvelopeSchema() Schema"
    description: |
      Return the universal envelope JSON Schema (REQ-030); consumed by
      validation-engine to satisfy REQ-015. No artifactType parameter — one
      envelope schema covers every artifact type.
    preconditions:
      - "None beyond being callable on a value returned by NewEmbeddedResources."
    postconditions:
      on_success:
        - "Returned Schema wraps the bytes of bundle/artifacts/envelope.schema.json as synced into the binary at build time."
        - "Across the binary's lifetime, every call returns a value whose underlying bytes compare byte-identical to those from any prior call on the same binary (REQ-030)."
    invariants: []
    errors: []
    side_effects:
      - "None."
    thread_safety: thread-safe
    nullability:
      - "return: must not be the zero value of Schema."
    complexity_notes: "O(1)."

  - name: QualityBarChecklist
    signature: "QualityBarChecklist(artifactType ArtifactType) (QBChecklist, error)"
    description: |
      Return the per-artifact Quality Bar checklist corresponding to
      artifactType (REQ-030); consumed by validation-engine to satisfy REQ-017
      (structural-rigor items only).
    preconditions:
      - "artifactType is one of the six canonical enum values."
    postconditions:
      on_success:
        - "Returned QBChecklist wraps the bytes of bundle/artifacts/quality-bar/<artifactType>.quality-bar.json as synced into the binary at build time."
        - "Across the binary's lifetime, every call with the same artifactType returns a value whose underlying bytes compare byte-identical to those from any prior call with the same artifactType on the same binary (REQ-030)."
      on_failure:
        - "On artifactType not in the canonical set: returns the zero value of QBChecklist together with ErrUnknownArtifactType; no observable state change."
    invariants: []
    errors:
      - error: "ErrUnknownArtifactType"
        raised_when: "artifactType is not one of the six canonical enum members."
        meaning: "Caller bug — input outside the closed enum."
    side_effects:
      - "None."
    thread_safety: thread-safe
    nullability:
      - "artifactType: must not be the zero value of ArtifactType."
      - "return QBChecklist: zero value on the error branch; non-zero on success."
      - "return error: nil on success; non-nil ErrUnknownArtifactType on the precondition-violation branch."
    complexity_notes: "O(1)."

  - name: Versions
    signature: "Versions() VersionManifest"
    description: |
      Return the version manifest naming the synced source versions of the
      three canonical input sets (REQ-032). Single source of truth for
      queryable bundled versions.
    preconditions:
      - "None beyond being callable on a value returned by NewEmbeddedResources."
    postconditions:
      on_success:
        - "Returned VersionManifest carries three non-empty version strings — rule_catalog_version, schema_set_version, quality_bar_set_version — identifying the exact framework-source versions of bundle/traceability/validation-rules.catalog.json, bundle/artifacts/, and bundle/artifacts/quality-bar/ respectively at the binary's build time (REQ-032 acceptance)."
        - "Across the binary's lifetime, every call returns a value whose three version strings compare byte-identical to those from any prior call on the same binary (REQ-030)."
    invariants: []
    errors: []
    side_effects:
      - "None."
    thread_safety: thread-safe
    nullability:
      - "return: must not be the zero value of VersionManifest; all three version fields are non-empty strings."
    complexity_notes: "O(1)."
```

## Data Structures

```yaml
data_structures:

  - name: ArtifactType
    description: |
      Closed enum naming the framework canonical artifact types for which
      embedded-resources publishes a per-artifact Schema and a per-artifact
      QualityBarChecklist. The enum membership is the rendered form of
      REQ-016 / REQ-017 over the canonical artifact set; values match the
      `artifact_type` const values published in the framework's per-artifact
      JSON Schemas.
    fields:
      - { name: "value", type: "enum string", invariant: "Exactly one of: product-brief | requirements | architecture | adr | detailed-design | test-spec. Strings match the per-artifact schema's `artifact_type` const value byte-for-byte (no aliasing, no case-folding)." }
    ownership: "Defined at the embedded-resources scope; used by both this leaf and any caller passing artifactType to Schema / QualityBarChecklist."
    lifetime: "Compile-time constant — closed set fixed at binary build time."
    returned_semantics: "Pass-by-value; not returned by any accessor."

  - name: Schema
    description: |
      Typed wrapper over the raw JSON bytes of one per-artifact JSON Schema
      (or the universal envelope schema) as bundled in embed.FS.
    fields:
      - { name: "bytes", type: "byte sequence, UTF-8 JSON", invariant: "Byte-identical to the content of the corresponding bundle/artifacts/*.schema.json file at the binary's build time." }
    ownership: "Constructed by NewEmbeddedResources; never modified after construction; never released (process-singleton)."
    lifetime: "Process lifetime."
    returned_semantics: "Read-only reference. Caller may not mutate the underlying bytes; supplier does not mutate them either (the underlying bytes are immutable embed.FS content). Mutating the underlying bytes is undefined behaviour (per ARCH-IF-IFrameworkResources invariant)."

  - name: QBChecklist
    description: |
      Typed wrapper over the raw JSON bytes of one per-artifact Quality Bar
      checklist as bundled in embed.FS.
    fields:
      - { name: "bytes", type: "byte sequence, UTF-8 JSON", invariant: "Byte-identical to the content of the corresponding bundle/artifacts/quality-bar/*.quality-bar.json file at the binary's build time." }
    ownership: "Constructed by NewEmbeddedResources; never modified after construction; never released."
    lifetime: "Process lifetime."
    returned_semantics: "Read-only reference (per ARCH-IF-IFrameworkResources invariant)."

  - name: RuleCatalog
    description: |
      Typed wrapper over the raw JSON bytes of the framework canonical rule
      catalog (validation-rules.catalog.json) as bundled in embed.FS.
    fields:
      - { name: "bytes", type: "byte sequence, UTF-8 JSON", invariant: "Byte-identical to the content of bundle/traceability/validation-rules.catalog.json at the binary's build time." }
    ownership: "Constructed by NewEmbeddedResources; never modified after construction; never released."
    lifetime: "Process lifetime."
    returned_semantics: "Read-only reference (per ARCH-IF-IFrameworkResources invariant)."

  - name: VersionManifest
    description: |
      Parsed manifest naming the synced source versions of the three canonical
      input sets bundled in this binary. Unlike the three wrappers above,
      VersionManifest is parsed at this leaf because the version strings are
      the leaf's own product (REQ-032's queryable values) — no downstream
      schema library is involved.
    fields:
      - { name: "rule_catalog_version", type: "non-empty string", invariant: "Non-empty; identifies the framework-source version of validation-rules.catalog.json synced into this binary at build time." }
      - { name: "schema_set_version", type: "non-empty string", invariant: "Non-empty; identifies the framework-source version of the per-artifact schema set synced into this binary at build time." }
      - { name: "quality_bar_set_version", type: "non-empty string", invariant: "Non-empty; identifies the framework-source version of the per-artifact Quality Bar checklist set synced into this binary at build time." }
    ownership: "Constructed by NewEmbeddedResources; never modified after construction."
    lifetime: "Process lifetime."
    returned_semantics: "Read-only reference; the three string fields are immutable (per ARCH-IF-IFrameworkResources invariant)."

  - name: EmbedBundle
    description: |
      Internal — the compile-time embed.FS instance holding the synced
      framework canonical inputs. Not exposed across the public interface;
      callers see only the typed wrappers above.
    fields:
      - { name: "rule_catalog_bytes",        type: "byte sequence",  invariant: "Bytes of bundle/traceability/validation-rules.catalog.json synced at build time." }
      - { name: "envelope_schema_bytes",     type: "byte sequence",  invariant: "Bytes of bundle/artifacts/envelope.schema.json synced at build time." }
      - { name: "per_artifact_schemas",      type: "map from ArtifactType to byte sequence; key-uniqueness assumed", invariant: "Domain equals the six-element ArtifactType enum; each value is the bytes of bundle/artifacts/<artifactType>.schema.json synced at build time." }
      - { name: "per_artifact_qb_checklists", type: "map from ArtifactType to byte sequence; key-uniqueness assumed", invariant: "Domain equals the six-element ArtifactType enum; each value is the bytes of bundle/artifacts/quality-bar/<artifactType>.quality-bar.json synced at build time." }
      - { name: "version_manifest",          type: "VersionManifest", invariant: "All three version fields non-empty." }
    ownership: "Constructed once at the composition root by NewEmbeddedResources; held by the FrameworkResources instance; never published outside the leaf."
    lifetime: "Process lifetime — bound at binary load."
    returned_semantics: "Not returned across the public interface."
```

## Algorithms

The leaf has two algorithmic concerns; both are short.

**(1) Bundle layout — contractual.** The embed.FS root layout is the build-pipeline contract (per ADR-002 Propagation, the build pipeline syncs framework-side JSON inputs into the embed.FS root before binary compile). The bundle layout below is contractual because the sync step on the build pipeline and the decode step in this leaf must agree on file paths byte-for-byte; constraint kind: *architectural* (per ADR-002).

```text
bundle/
  traceability/
    validation-rules.catalog.json
  artifacts/
    envelope.schema.json
    product-brief.schema.json
    requirements.schema.json
    architecture.schema.json
    adr.schema.json
    detailed-design.schema.json
    test-spec.schema.json
    quality-bar/
      product-brief.quality-bar.json
      requirements.quality-bar.json
      architecture.quality-bar.json
      adr.quality-bar.json
      detailed-design.quality-bar.json
      test-spec.quality-bar.json
  version-manifest.json
```

File names mirror the framework canonical paths (`schemas/artifacts/`, `schemas/traceability/`, `schemas/artifacts/quality-bar/`) so the build pipeline's sync step is a 1:1 copy with no transformation. `version-manifest.json` is generated by the build pipeline (per ADR-002 Propagation) from the synced source versions; its shape is the three fields named in Data Structures: VersionManifest.

**(2) Dispatch from ArtifactType to bytes — result property only.** For `Schema(artifactType)` and `QualityBarChecklist(artifactType)`, the result property is: given an artifactType in the closed enum, return the bytes whose underlying source file in the bundle layout is `bundle/artifacts/<artifactType>.schema.json` or `bundle/artifacts/quality-bar/<artifactType>.quality-bar.json` respectively. The implementer chooses the dispatch mechanism (compile-time map literal, switch on enum value, or generated lookup); the contract is the byte-identical-across-lifetime postcondition.

**Decode posture — implementer's choice.** Eager decode (read all bundle entries into typed wrappers at construction) and lazy decode (read on first access, single-flight publication via `sync.Once` per entry) both satisfy the postconditions. Eager decode shifts cost to `NewEmbeddedResources`; lazy decode amortises it across first calls. REQ-022's latency target lies on the single-artifact validation path (the AI-caller author retry loop), which exercises a known subset of accessors; the decode posture is not a load-bearing decision at this leaf's scale (sub-megabyte total, per ADR-002 Assumption #5).

## State

Stateless between calls. The constructed `FrameworkResources` instance is immutable after `NewEmbeddedResources` returns: no accessor mutates instance state, no caller can observe a different value across the binary's lifetime for the same accessor (and the same `artifactType` where applicable). The underlying `embed.FS` is a process-singleton bound by the Go runtime at binary load. Thread-safety is `thread-safe` on every accessor; concurrent calls from `validation-engine`, `reporter`, and `cli-adapter` are safe by construction.

## Error Handling

| Error | Detection | Containment | Recovery | Caller receives |
|---|---|---|---|---|
| `ErrUnknownArtifactType` | Precondition check at boundary on `Schema(artifactType)` / `QualityBarChecklist(artifactType)`; the supplied `artifactType` does not match any of the six canonical enum members. | Reject at the leaf's boundary. | fail-fast | The zero value of the corresponding return type (`Schema` or `QBChecklist`) together with a non-nil `ErrUnknownArtifactType`; no state mutation (leaf is stateless). |

One row. Other failure modes do not exist at this leaf's runtime scope:

- *Bundle absence* (missing or corrupted file in `embed.FS`) is a **build-time** link failure surfaced by the build pipeline's sync step plus Go's `//go:embed` directive evaluation; it cannot occur at runtime once the binary has loaded. Per `ARCH-IF-IFrameworkResources` errors: *"n/a — bundle is in-binary; absence is a build-time failure."* The build pipeline's fitness function (per `ARCH` Composition / *Evolution + fitness functions* — out of scope at this leaf) is the verification surface for that condition.
- *Network failure* and *filesystem failure outside the binary* cannot occur — REQ-031 invariant forbids them, structurally enforced by the absence of any network or non-embed.FS read in this leaf's code.
- *Decode failure* on construction (malformed JSON in a bundled file) is treated as a build-time defect: the build pipeline's test stage (per `ARCH` deployment intent) runs `NewEmbeddedResources` and any eager-decode path during binary test; a decode error fails the build, not the run. No runtime row.

## Notes

- **TestSpec cues (leaf scope — unit).**
  - Contract test per accessor: success-path postconditions on `NewEmbeddedResources`, `RuleCatalog`, `Schema(t)`, `EnvelopeSchema`, `QualityBarChecklist(t)`, `Versions`.
  - Robustness test for the error matrix row: `Schema` and `QualityBarChecklist` invoked with an out-of-enum `artifactType` return the zero value plus `ErrUnknownArtifactType`.
  - Property test on the byte-identical-across-lifetime postcondition: for every accessor, two successive calls on the same instance return values whose underlying bytes compare byte-identical; for `Schema(t)` and `QualityBarChecklist(t)`, parameterised across the six enum values.
  - Property test on `VersionManifest`: all three version fields are non-empty strings.
  - Thread-safety property test: concurrent calls from N goroutines (N small) on every accessor return values whose underlying bytes compare byte-identical to those returned from a single-threaded baseline.
- **Out of scope at this leaf's TestSpec.** REQ-031's sandbox acceptance (no network, no filesystem outside binary) is a process-level system test belonging to the root TestSpec, not to this leaf's unit-test surface. The leaf's invariant is verified by *absence of code paths* that read outside `embed.FS` or open network sockets — a fitness-function check in the build pipeline, not a unit test.
- **ArtifactType enum membership is closed at six per REQ-016.** Growing the enum (e.g., to address `architecture-interface-detail` bundle files at validation time) requires a requirements amendment to REQ-016 / REQ-017 and the Glossary's *Framework canonical schema set* and *Framework canonical Quality Bar checklist set* entries. This DD does not extend the enum unilaterally.
