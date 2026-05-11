---
id: TS-embedded-resources
title: "TestSpec — embedded-resources"
artifact_type: test-spec
scope: embedded-resources
parent_scope: ""
level: unit
derived_from:
  - DD-embedded-resources
verifies:
  - DD-embedded-resources.public_interface.NewEmbeddedResources
  - DD-embedded-resources.public_interface.RuleCatalog
  - DD-embedded-resources.public_interface.Schema
  - DD-embedded-resources.public_interface.EnvelopeSchema
  - DD-embedded-resources.public_interface.QualityBarChecklist
  - DD-embedded-resources.public_interface.Versions
  - DD-embedded-resources.error_handling.ErrUnknownArtifactType
governing_adrs:
  - ADR-002-embed-canonical-schemas-in-binary
status: draft
date: "2026-05-12"
version: 2
coverage_mutation_bar:
  structural_coverage:
    threshold_pct: "TBD-by-project-policy"
    metric: branch
  mutation_score:
    threshold_pct: "TBD-by-project-policy"
    tool_category: "TBD-by-project-policy"
  enforcement:
    frequency: "TBD-by-project-policy"
    blocking: "TBD-by-project-policy"
---

# TestSpec — embedded-resources (leaf scope, unit)

## Overview

This document specifies the leaf-scope TestSpec for `embedded-resources` — the driven adapter owning read-only access to the three framework canonical input sets (rule catalog, per-artifact schema set including the universal envelope schema, per-artifact Quality Bar checklist set) and the build-time version manifest. Cases are derived from `DD-embedded-resources` (canonical parent present — `parent_architecture: ARCH`, `governing_adrs: [ADR-002-embed-canonical-schemas-in-binary]`). The DD's six accessors, single error-matrix row (`ErrUnknownArtifactType`), and the byte-identical-across-lifetime postcondition that every accessor carries are the derivation seeds.

The 14 cases below cover three strategy slices: **contract / functional** (one per accessor success path, six cases), **robustness** (the single error-matrix row across its two accessors, two cases), and **property** (byte-identical-across-lifetime per accessor plus thread-safety quantified over all accessors, six cases). All cases call the leaf's public interface directly; no test doubles are needed because the leaf has no external collaborators (per DD Overview: *"The leaf consumes nothing from siblings."*).

**Out of scope at this leaf's TestSpec** (per DD Notes):

- REQ-031's sandbox acceptance (no network access, no filesystem read outside the binary). REQ-031 is a process-level guarantee verified by the root TestSpec inside a sandbox and reinforced by a build-pipeline fitness function checking absence of forbidden API call sites. Not a unit-test surface.
- Bundle absence or decode failure on construction. The DD's error matrix has one row only (`ErrUnknownArtifactType`); bundle absence is a build-time link failure surfaced by `//go:embed` evaluation, and bundled-JSON malformation is a build-time test-stage failure — neither can occur once the binary is loaded.
- The `NewEmbeddedResources` precondition *"Called from the composition root; not invoked from inner-domain code."* This is design-time discipline (enforced by `ARCH` Composition / Wiring), not a runtime check; calling the constructor from a unit test produces a working instance because that is what the unit test exists to do.
- Decode posture (eager vs lazy). The DD declares it the implementer's choice; pinning a specific posture in a test would over-constrain the implementation. The byte-identical-across-lifetime postcondition is the contractual surface, and both decode postures satisfy it.

**Coverage / mutation bar (project-policy fill-in).** All four slots use `"TBD-by-project-policy"` per `references/coverage-mutation-bar.md` — the author does not invent numbers. Per the per-layer guidance, the structural slot's `branch` metric is the most informative flavour for a stateless typed-accessor leaf (every conditional dispatch on `artifactType` and the parameterisation across the seven enum members should be exercised); a mutation score paired with `branch` coverage closes the assertion-sensitivity gap, particularly for the dispatch logic that returns one of seven distinct byte-sequences. Enforcement is left to project policy.

**Error / happy ratio.** This TestSpec has 2 error cases against 6 contract / functional cases (ratio 1:3), below the Quality Bar heuristic of ≥ 1:2. The honest reason is that the DD's error matrix has exactly one row (`ErrUnknownArtifactType`) across two callsites (`Schema`, `QualityBarChecklist`), and both callsites are covered exhaustively by TC-007 / TC-008. Bundle absence, network failure, and decode failure are structurally impossible at runtime (see *Out of scope* above), so adding cases for them would fabricate error surface. Lifting the ratio without fabricating would require either the DD to grow its error matrix or the leaf to grow more accessors — neither is in scope here.

## Cases

```yaml
# ─── Contract / functional (TC-001 .. TC-006) ───────────────────────────────
# One case per accessor success path. Each asserts the on_success postcondition
# in specific terms (byte-equality against the bundle source file, or for
# Versions, three non-empty strings).

- id: TC-embedded-resources-001
  title: "NewEmbeddedResources returns a FrameworkResources whose accessors are bound to embed.FS contents"
  suite: "construction"
  type: functional
  verifies:
    - "DD-embedded-resources.public_interface.NewEmbeddedResources.postconditions.on_success"
  inputs: {}
  expected:
    return_value: "non-nil FrameworkResources (interface satisfaction enforced by Go's type system at the call site)"
    binding_smoke_test: "on the returned value, all three of: len(RuleCatalog().bytes) > 0 AND len(EnvelopeSchema().bytes) > 0 AND len(Versions().RuleCatalogVersion) > 0 — establishes that the accessors are bound to embed.FS contents in fact (not merely structurally satisfying the interface), while leaving the byte-equality-vs-bundle predicates to TC-002 .. TC-006"
    side_effect: "no panic; construction completes"

- id: TC-embedded-resources-002
  title: "RuleCatalog returns wrapper whose bytes equal the bundled rule-catalog JSON"
  suite: "accessors-bytes"
  type: functional
  verifies:
    - "DD-embedded-resources.public_interface.RuleCatalog.postconditions.on_success"
    - "DD-embedded-resources.data_structures.RuleCatalog.fields.bytes"
  inputs:
    instance: "NewEmbeddedResources()"
  expected: "RuleCatalog().bytes byte-identical to the contents of bundle/traceability/validation-rules.catalog.json as bound by //go:embed in the binary under test"

- id: TC-embedded-resources-003
  title: "Schema(t) returns wrapper whose bytes equal the bundled per-artifact JSON Schema, for every t in the canonical seven-enum"
  suite: "accessors-bytes"
  type: functional
  verifies:
    - "DD-embedded-resources.public_interface.Schema.postconditions.on_success"
    - "DD-embedded-resources.data_structures.ArtifactType.fields.value"
    - "DD-embedded-resources.data_structures.Schema.fields.bytes"
    - "DD-embedded-resources.data_structures.EmbedBundle.fields.per_artifact_schemas"
  inputs:
    instance: "NewEmbeddedResources()"
    artifactType:
      enumerate: ["product-brief", "requirements", "architecture", "adr", "detailed-design", "test-spec", "architecture-interface-detail"]
  expected: "for each artifactType in the enumerate set: Schema(artifactType) returns (schema, nil) where schema.bytes is byte-identical to the contents of bundle/artifacts/<artifactType>.schema.json as bound by //go:embed, and the returned error is nil"

- id: TC-embedded-resources-004
  title: "EnvelopeSchema returns wrapper whose bytes equal the bundled envelope JSON Schema"
  suite: "accessors-bytes"
  type: functional
  verifies:
    - "DD-embedded-resources.public_interface.EnvelopeSchema.postconditions.on_success"
    - "DD-embedded-resources.data_structures.Schema.fields.bytes"
    - "DD-embedded-resources.data_structures.EmbedBundle.fields.envelope_schema_bytes"
  inputs:
    instance: "NewEmbeddedResources()"
  expected: "EnvelopeSchema().bytes byte-identical to the contents of bundle/artifacts/envelope.schema.json as bound by //go:embed"

- id: TC-embedded-resources-005
  title: "QualityBarChecklist(t) returns wrapper whose bytes equal the bundled per-artifact QB JSON, for every t in the canonical seven-enum"
  suite: "accessors-bytes"
  type: functional
  verifies:
    - "DD-embedded-resources.public_interface.QualityBarChecklist.postconditions.on_success"
    - "DD-embedded-resources.data_structures.ArtifactType.fields.value"
    - "DD-embedded-resources.data_structures.QBChecklist.fields.bytes"
    - "DD-embedded-resources.data_structures.EmbedBundle.fields.per_artifact_qb_checklists"
  inputs:
    instance: "NewEmbeddedResources()"
    artifactType:
      enumerate: ["product-brief", "requirements", "architecture", "adr", "detailed-design", "test-spec", "architecture-interface-detail"]
  expected: "for each artifactType in the enumerate set: QualityBarChecklist(artifactType) returns (qb, nil) where qb.bytes is byte-identical to the contents of bundle/artifacts/quality-bar/<artifactType>.quality-bar.json as bound by //go:embed, and the returned error is nil"

- id: TC-embedded-resources-006
  title: "Versions returns a VersionManifest whose three version fields are non-empty strings"
  suite: "accessors-versions"
  type: functional
  verifies:
    - "DD-embedded-resources.public_interface.Versions.postconditions.on_success"
    - "DD-embedded-resources.data_structures.VersionManifest.fields.rule_catalog_version"
    - "DD-embedded-resources.data_structures.VersionManifest.fields.schema_set_version"
    - "DD-embedded-resources.data_structures.VersionManifest.fields.quality_bar_set_version"
    - "DD-embedded-resources.data_structures.EmbedBundle.fields.version_manifest"
  inputs:
    instance: "NewEmbeddedResources()"
  expected:
    rule_catalog_version: "len(v.RuleCatalogVersion) > 0 AND v.RuleCatalogVersion equals the rule_catalog_version field in bundle/version-manifest.json as bound by //go:embed"
    schema_set_version: "len(v.SchemaSetVersion) > 0 AND v.SchemaSetVersion equals the schema_set_version field in bundle/version-manifest.json as bound by //go:embed"
    quality_bar_set_version: "len(v.QualityBarSetVersion) > 0 AND v.QualityBarSetVersion equals the quality_bar_set_version field in bundle/version-manifest.json as bound by //go:embed"

# ─── Robustness (TC-007 .. TC-008) ──────────────────────────────────────────
# The DD's single error-matrix row across the two accessors that carry the
# seven-enum precondition. Each case forces precondition violation, asserts the
# typed-error return shape, and observes the stateless containment guarantee
# (a subsequent valid call still returns expected bytes).

- id: TC-embedded-resources-007
  title: "Schema returns zero-value Schema and ErrUnknownArtifactType when artifactType is outside the seven-enum; subsequent valid call still returns expected bytes"
  suite: "robustness"
  type: error
  verifies:
    - "DD-embedded-resources.public_interface.Schema.preconditions"
    - "DD-embedded-resources.public_interface.Schema.postconditions.on_failure"
    - "DD-embedded-resources.public_interface.Schema.errors.ErrUnknownArtifactType"
    - "DD-embedded-resources.error_handling.ErrUnknownArtifactType"
    - "ARCH.interfaces.IFrameworkResources.errors.ErrUnknownArtifactType"
  inputs:
    instance: "NewEmbeddedResources()"
    invalid_artifactType: "ArtifactType value not in {product-brief, requirements, architecture, adr, detailed-design, test-spec, architecture-interface-detail} — e.g., the zero value of ArtifactType, or a literal 'unknown-artifact'"
    follow_up_call: "Schema('requirements')"
  expected:
    return_schema: "the zero value of Schema (Schema{} with bytes field equal to a zero-length byte sequence)"
    return_error: "non-nil; errors.Is(err, ErrUnknownArtifactType) == true"
    state_unchanged: "the follow_up_call Schema('requirements') returns (schema, nil) where schema.bytes is byte-identical to the contents of bundle/artifacts/requirements.schema.json (same predicate as TC-003 for artifactType='requirements')"

- id: TC-embedded-resources-008
  title: "QualityBarChecklist returns zero-value QBChecklist and ErrUnknownArtifactType when artifactType is outside the seven-enum; subsequent valid call still returns expected bytes"
  suite: "robustness"
  type: error
  verifies:
    - "DD-embedded-resources.public_interface.QualityBarChecklist.preconditions"
    - "DD-embedded-resources.public_interface.QualityBarChecklist.postconditions.on_failure"
    - "DD-embedded-resources.public_interface.QualityBarChecklist.errors.ErrUnknownArtifactType"
    - "DD-embedded-resources.error_handling.ErrUnknownArtifactType"
    - "ARCH.interfaces.IFrameworkResources.errors.ErrUnknownArtifactType"
  inputs:
    instance: "NewEmbeddedResources()"
    invalid_artifactType: "ArtifactType value not in {product-brief, requirements, architecture, adr, detailed-design, test-spec, architecture-interface-detail} — e.g., the zero value of ArtifactType, or a literal 'unknown-artifact'"
    follow_up_call: "QualityBarChecklist('requirements')"
  expected:
    return_qb: "the zero value of QBChecklist (QBChecklist{} with bytes field equal to a zero-length byte sequence)"
    return_error: "non-nil; errors.Is(err, ErrUnknownArtifactType) == true"
    state_unchanged: "the follow_up_call QualityBarChecklist('requirements') returns (qb, nil) where qb.bytes is byte-identical to the contents of bundle/artifacts/quality-bar/requirements.quality-bar.json (same predicate as TC-005 for artifactType='requirements')"

# ─── Property — byte-identical-across-lifetime (TC-009 .. TC-013) ───────────
# Every accessor's on_success postcondition includes a universal-quantifier
# clause: "Across the binary's lifetime, every call ... returns a value whose
# underlying bytes compare byte-identical to those from any prior call ...".
# Each property case quantifies over two successive calls on the same instance.

- id: TC-embedded-resources-009
  title: "RuleCatalog: two successive calls on the same instance return byte-identical underlying bytes"
  suite: "byte-stability"
  type: property
  verifies:
    - "DD-embedded-resources.public_interface.RuleCatalog.postconditions.on_success"
  inputs:
    instance: "NewEmbeddedResources()"
    call_count: 2
  expected: "first_call.bytes byte-identical to second_call.bytes (the two byte sequences compare equal element-for-element)"

- id: TC-embedded-resources-010
  title: "Schema(t): two successive calls on the same instance return byte-identical underlying bytes, for every t in the canonical seven-enum"
  suite: "byte-stability"
  type: property
  verifies:
    - "DD-embedded-resources.public_interface.Schema.postconditions.on_success"
  inputs:
    instance: "NewEmbeddedResources()"
    call_count: 2
    artifactType:
      enumerate: ["product-brief", "requirements", "architecture", "adr", "detailed-design", "test-spec", "architecture-interface-detail"]
  expected: "for each artifactType in the enumerate set: first_call(artifactType).bytes byte-identical to second_call(artifactType).bytes"

- id: TC-embedded-resources-011
  title: "EnvelopeSchema: two successive calls on the same instance return byte-identical underlying bytes"
  suite: "byte-stability"
  type: property
  verifies:
    - "DD-embedded-resources.public_interface.EnvelopeSchema.postconditions.on_success"
  inputs:
    instance: "NewEmbeddedResources()"
    call_count: 2
  expected: "first_call.bytes byte-identical to second_call.bytes"

- id: TC-embedded-resources-012
  title: "QualityBarChecklist(t): two successive calls on the same instance return byte-identical underlying bytes, for every t in the canonical seven-enum"
  suite: "byte-stability"
  type: property
  verifies:
    - "DD-embedded-resources.public_interface.QualityBarChecklist.postconditions.on_success"
  inputs:
    instance: "NewEmbeddedResources()"
    call_count: 2
    artifactType:
      enumerate: ["product-brief", "requirements", "architecture", "adr", "detailed-design", "test-spec", "architecture-interface-detail"]
  expected: "for each artifactType in the enumerate set: first_call(artifactType).bytes byte-identical to second_call(artifactType).bytes"

- id: TC-embedded-resources-013
  title: "Versions: two successive calls on the same instance return identical version strings on all three fields"
  suite: "byte-stability"
  type: property
  verifies:
    - "DD-embedded-resources.public_interface.Versions.postconditions.on_success"
  inputs:
    instance: "NewEmbeddedResources()"
    call_count: 2
  expected: "first_call.RuleCatalogVersion == second_call.RuleCatalogVersion AND first_call.SchemaSetVersion == second_call.SchemaSetVersion AND first_call.QualityBarSetVersion == second_call.QualityBarSetVersion"

# ─── Property — thread-safety (TC-014) ──────────────────────────────────────
# Every accessor declares thread_safety: thread-safe. The property is quantified
# over all accessors uniformly (a single case is honest because the DD's
# thread-safety guarantee is uniform across the public interface — collapsing
# matches the actual contract granularity).

- id: TC-embedded-resources-014
  title: "Concurrent calls on every accessor from 8 goroutines return bytes byte-identical to a single-threaded baseline (race-detector enabled)"
  suite: "thread-safety"
  type: property
  verifies:
    - "DD-embedded-resources.public_interface.NewEmbeddedResources.thread_safety"
    - "DD-embedded-resources.public_interface.RuleCatalog.thread_safety"
    - "DD-embedded-resources.public_interface.Schema.thread_safety"
    - "DD-embedded-resources.public_interface.EnvelopeSchema.thread_safety"
    - "DD-embedded-resources.public_interface.QualityBarChecklist.thread_safety"
    - "DD-embedded-resources.public_interface.Versions.thread_safety"
  inputs:
    instance: "NewEmbeddedResources()"
    goroutine_count: 8
    iterations_per_goroutine: 16
    accessors_under_test:
      - "RuleCatalog()"
      - "Schema(artifactType) for each artifactType in {product-brief, requirements, architecture, adr, detailed-design, test-spec, architecture-interface-detail}"
      - "EnvelopeSchema()"
      - "QualityBarChecklist(artifactType) for each artifactType in {product-brief, requirements, architecture, adr, detailed-design, test-spec, architecture-interface-detail}"
      - "Versions()"
    baseline: "single-threaded result captured before goroutine fan-out, per accessor (and per artifactType where parameterised)"
    test_runner_flag: "go test -race"
  expected:
    per_accessor: "for every accessor (and every artifactType where parameterised): every concurrent call's returned bytes (or version strings for Versions) byte-identical to the baseline captured pre-fan-out"
    race_detector: "go test -race reports zero data races"
```

## Notes

- **Bundle fixture.** Every byte-equality oracle (TC-002 .. TC-006, TC-007 / TC-008 follow-up, TC-009 .. TC-013) is satisfied by re-loading the corresponding file via `//go:embed` (or `embed.FS.ReadFile`) in the test package and comparing against the accessor's returned bytes. The test package owns its own `//go:embed bundle/...` directive pointing at the same `bundle/` tree the production binary embeds; this is the cleanest fixture mechanism (no copy, no parallel hierarchy) and keeps the test independent of any future code-side helper that might itself contain the bug under test.
- **Why the byte-identical predicate is the oracle, not JSON-equivalence.** REQ-030's acceptance is *exact-bytes* over the bundled content (the binary-version pins schema-version 1:1); a JSON-equivalent oracle (parse-then-compare-AST) would let a re-formatting fault through. The DD's data-structure invariant *"Byte-identical to the content of ... at the binary's build time"* is the contractual surface.
- **`ArtifactType` enum closed at seven per requirements Glossary v2 (2026-05-12).** The parameterised cases (TC-003, TC-005, TC-010, TC-012) enumerate exactly the seven members (product-brief, requirements, architecture, adr, detailed-design, test-spec, architecture-interface-detail); the robustness cases (TC-007, TC-008) verify that any value outside the seven triggers the typed error. Growth was a coordinated requirements (Glossary) + DD (ArtifactType data structure) + TestSpec amendment landing 2026-05-12 to resolve dogfood Issue 25; future enum growth follows the same pattern.
- **Decode-posture independence.** None of the 14 cases pins eager-vs-lazy decode. TC-014's `iterations_per_goroutine: 16` exercises both first-access (lazy decode's single-flight publication path) and subsequent-access (post-decode cached path) under contention, but neither outcome is asserted at the test boundary — only the byte-equality and race-freedom oracles are.
