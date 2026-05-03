---
id: ADR-002-embed-canonical-schemas-in-binary
artifact_type: adr
title: "Embed framework canonical schemas in the binary at compile time"
status: accepted
date: "2026-05-03"
scope_tags: ["vmodel-core"]
---

# ADR-002: Embed framework canonical schemas in the binary at compile time

**Y-statement.** In the context of vmodel-core's mechanism for accessing the framework canonical rule catalog, schema set, and Quality Bar checklist set at runtime (REQ-024 precondition #2 deferred this to architecture), facing IC-002 (stateless cold-start), IC-004 (single-artefact distribution), and IC-007 (no relaxation modes), we decided for **embedding all three input sets in the binary at compile time via Go's `embed` package, with no runtime override mechanism at v1**, to achieve a single deterministic distribution unit with version-pinned schemas and zero adopter-side relaxation surface, accepting that schema iteration during framework or vmodel-core development requires a binary rebuild.

## Context

vmodel-core depends on three framework-owned input sets at runtime: the canonical rule catalog (`references/schemas/traceability/validation-rules.catalog.json`), the canonical schema set (`references/schemas/artifacts/`), and the canonical Quality Bar checklist set (`references/schemas/artifacts/quality-bar/`). These are the authoritative inputs for IC-009 / IC-010 / IC-011. They are framework-owned (live in the framework repo, not in vmodel-core's own repo) and evolve at the framework's release cadence. ADR-001 has committed the implementation language to Go, which makes Go's `embed` package the idiomatic compile-time bundling mechanism. REQ-024 precondition #2 explicitly defers the *mechanism* of accessibility to architecture; this ADR resolves that deferral.

IC-002 (each invocation independent, no setup, no daemon) and IC-004 (single artefact, no separate runtime install across Linux / macOS / Windows) collectively eliminate runtime-fetch-from-URL, separate-tarball-ship-alongside-binary, and require-clone-framework-repo distributions before they become candidates. After this constraint pruning, the realistic option space narrows to two: embed at compile time with no runtime override, or embed at compile time with a runtime override (flag or environment variable, or a filesystem-priority-with-bundled-fallback variant). Filesystem-only-no-embed (binary fails without an external schema bundle) is constraint-violating — IC-004 explicitly forbids "single artefact and run it" being multi-artefact — and is not on the table.

The decision is consequential for adopter-side workflow (no `--schemas-dir` escape hatch means relaxation is impossible by construction), for vmodel-core's own dev workflow (rebuild required to test schema changes — counterweighted by Go's seconds-fast build), and for framework / vmodel-core repo coupling (release cadences must align since schemas ship with binaries).

### Drivers

- **IC-002 — stateless cold-start.** No setup, no daemon, no shared state between invocations.
- **IC-004 — single-artefact distribution.** Adopter downloads one binary; no separate schema bundle.
- **IC-005 — re-download-and-replace update mechanism.** Binary + schemas update together as one artefact.
- **IC-007 — no relaxation modes.** Uniform high rigor enforced by absence of adopter-side opt-out (per `TARGET §3 #3`).
- **IC-009 / IC-010 / IC-011 — framework canonical inputs.** Rule catalog, schema set, Quality Bar checklist set are required-to-be-present inputs whose contents bind the validator's behaviour.
- **ADR-001 — Go implementation.** Makes `embed.FS` the idiomatic compile-time bundling mechanism.
- **REQ-024 precondition #2.** Explicit architecture-side deferral of the access mechanism; this ADR resolves it.
- **Framework / vmodel-core repo coupling.** Schemas are framework-owned; vmodel-core syncs them at release time. Binary version and schema version must remain consistent.
- **Dev-iteration-cost on schemas (counterweight to IC-007).** Framework author and vmodel-core developers iterate on schemas; rebuild-on-every-schema-change is the friction this driver names.
- **Adopter-deviation surface (the IC-007 risk).** Any documented runtime path that swaps schemas creates an attractive nuisance for adopters who want relaxation.

### Assumptions (revisit triggers)

- IC-007 holds at v1 and beyond. If relaxation modes are ever permitted, the override mechanism becomes plausible and this decision warrants revisit.
- Framework schema-update cadence is compatible with vmodel-core's release cadence. If schemas churn materially faster than vmodel-core releases, the rebuild-and-release cost grows and override gains weight.
- vmodel-core's binary build time remains in the seconds-not-minutes range. Go's current build performance for a project of vmodel-core's expected size supports this; if build time stretches significantly, the dev-iteration-cost driver gains weight.
- Go's `embed` package remains stable and performant. Stable since Go 1.16 (2021); low-risk assumption.
- Framework's three input sets remain JSON-shaped and bounded in size (sub-megabyte at vmodel-core's scope). Embedding adds negligible binary size at this scale; if input sets grow into hundreds of megabytes, embed-vs-stream becomes a real trade.

## Decision

We will embed the framework canonical rule catalog, the framework canonical schema set, and the framework canonical Quality Bar checklist set in the vmodel-core binary at compile time using Go's `embed` package. We will not provide a runtime override mechanism (no `--schemas-dir` flag, no environment variable, no filesystem-priority fallback) at v1.

## Alternatives considered

- **Embed-in-binary with a `--schemas-dir` runtime override flag (or `VMODEL_SCHEMAS_DIR` environment variable).** Rejected on **IC-007** grounds: a documented runtime override is an attractive nuisance for adopters seeking to relax framework rules. Even when labelled developer-only, the surface adds documentation, test coverage, and a support obligation, and creates a path that adopters can use to ship vmodel-core in their CI with relaxed schemas — defeating the framework's uniform-high-rigor axiom (`TARGET §3 #3`). The dev-iteration-cost driver this option mitigates is small in practice: Go builds for a project of vmodel-core's expected size complete in seconds, and dev workflows can use targeted Go test fixtures rather than runtime overrides.

- **Filesystem-priority-with-bundled-fallback** (binary checks well-known paths first — e.g. `$XDG_CONFIG_HOME/vmodel/schemas/` — and falls back to embedded defaults if no files are present). Rejected on the same **IC-007** grounds, plus **IC-002** strictness: the implicit lookup creates a relaxation surface that adopters do not even need to opt into via flag — they can drop a file in a well-known path and the binary picks it up silently. Cold-start also gains filesystem-discovery overhead that IC-002 + REQ-022 would both prefer absent.

## Rationale

**IC-007**, **IC-002**, and **IC-005** carried the call jointly:

1. **IC-007** is the dispositive driver. The framework's uniform-high-rigor axiom forbids per-adopter relaxation by design, and it forbids it specifically through *absence of opt-out* — there is no `--lenient` flag because the absence of the flag is what enforces the discipline. A runtime schema-override mechanism is structurally identical to a `--lenient` flag for the rule-content axis: it allows adopters to substitute their own (relaxed) versions of the framework's rules. Adding such a mechanism would directly contradict IC-007's enforcement model.
2. **IC-002** is reinforced by embed-only: the cold-start path performs zero filesystem discovery for schema location and zero conditional logic for schema-source selection. Every invocation reads from the same in-binary `embed.FS`. This is the simplest possible cold-start shape for catalog availability and supports REQ-022 latency by removing schema-discovery from the critical path.
3. **IC-005** is satisfied perfectly: re-downloading a single binary atomically replaces both the validator code and the schemas it enforces. Schema-version-skew between validator and schemas is structurally impossible — the binary literally contains the schemas it validates against.

The framework / vmodel-core repo coupling driver supports the choice operationally: vmodel-core's build pipeline includes a sync step that copies framework-side JSON inputs into the embed-FS root at build time, ensuring released binaries always carry the schemas they were tested against. ADR-001 (Go) makes the realisation idiomatic via `embed.FS` and `//go:embed` directives.

The dev-iteration-cost driver was the only meaningful counter-pull; it was outweighed because Go's build is fast at vmodel-core's expected size and because schema iteration in development can use targeted Go test fixtures (a unit-test-scope substitute) rather than runtime overrides.

## Consequences

**Positive**

- **Single-artefact distribution.** IC-004 satisfied perfectly — adopter downloads one binary and runs it; no separate schema bundle, no setup step.
- **Schema version pinned 1:1 to binary version.** Version-skew between the validator and the schemas it enforces is structurally impossible. Findings are reproducible as a function of (binary version, input).
- **Adopter relaxation surface is zero.** IC-007 enforced by absence of opt-out: no flag, no env var, no path discovery. A vmodel-core binary cannot be made to enforce a non-canonical rule set without rebuilding it from source against modified schemas.
- **Cold-start is simpler.** No filesystem discovery, no path-existence checks, no conditional source selection — supports IC-002 strictness and REQ-022 latency.
- **Re-download-and-replace updates atomically.** IC-005 satisfied perfectly: the adopter's update operation is one file replacement.

**Negative**

- **vmodel-core developer (and framework author iterating on schemas) must rebuild the binary to test schema changes.** Mitigation: Go builds in seconds at vmodel-core's expected size; targeted Go test fixtures stand in for schema variants at unit-test scope.
- **Framework schema evolution requires a vmodel-core release.** Mitigation: vmodel-core's build pipeline syncs framework-side JSONs into `embed.FS` at build time; release cadences must remain compatible (revisit if framework schema cadence ever exceeds vmodel-core release cadence).
- **Binary size grows with embedded schema content.** At v1 scale (sub-megabyte JSON inputs), growth is bounded and trivial relative to a Go binary's baseline size; revisit if input sets grow into hundreds of megabytes.
- **No escape hatch for adopter-side schema customisation.** By design (IC-007), but recorded as a Negative because it removes a workflow that some validator tools expose. Adopters who want a different rule set must use a different tool — which is consistent with the framework's "if rigor is not needed, the framework is not the right tool" stance, but is a real path-foreclosure.

**Reversibility.** *(Verbatim prompt: "Is this decision reversible? If yes: state the rollback path. If no: state the recovery plan and name who must sign off before implementation.")*

**Reversible.** Rollback path: add a `--schemas-dir` flag (or `VMODEL_SCHEMAS_DIR` environment variable) that, when set, overrides the embedded schemas with disk-loaded ones; embedded defaults remain the fallback when unset. Cost estimate: a few hours of code + tests + documentation. The CLI surface contract (REQ-024 versioning) is additive-only-within-major, so adding the flag does not break compatibility for existing v1 callers. No external sign-off required. Revisit triggers (Assumptions section above) flag the conditions under which the cost-benefit may shift — chiefly an IC-007 relaxation, framework schema cadence overrunning vmodel-core release cadence, or build time stretching materially.

## Propagation

- **Consequence:** *"The three canonical input sets are bundled into the binary at compile time via Go's `embed` package."*
  Route: governing_adrs from child architecture.
  Bound by: forthcoming vmodel-core root architecture (will carry `governing_adrs: [ADR-002-embed-canonical-schemas-in-binary]` and specify the parser / schema-loader component as reading from `embed.FS`).

- **Consequence:** *"Schema version is pinned 1:1 to binary version, and the bundled versions are queryable from the binary."*
  Route: new requirements at this scope (split — pinning and queryability are atomic-shall properties addressed independently per requirements review feedback 2026-05-03).
  Materialised as:
    - **REQ-030** (version pinning) — *"The system shall, during any validation or reporting run, use the exact versions of the framework canonical rule catalog, framework canonical schema set, and framework canonical Quality Bar checklist set bundled with the binary at the binary's build time."*
    - **REQ-032** (version queryability) — *"When the system is queried for the bundled versions of the framework canonical rule catalog, framework canonical schema set, and framework canonical Quality Bar checklist set, the system shall return version identifiers identifying the exact versions compiled into the binary at the binary's build time."*
  Testable at vmodel-core's external boundary by (a) running validation/reporting and confirming used versions match build-time-bundled versions, and (b) querying the binary and comparing returned versions to build-time-bundled versions.

- **Consequence:** *"Schema availability requires no filesystem path beyond the binary itself and no network access at runtime."*
  Route: new requirement at this scope.
  Materialised as: **REQ-031** — *"When the system runs a validation or a reporting operation, the system shall obtain the framework canonical rule catalog, framework canonical schema set, and framework canonical Quality Bar checklist set without performing any filesystem read outside the binary itself and without performing any network access."* Testable at vmodel-core's external boundary by invoking the binary in a sandbox with no network and no readable filesystem outside the binary path.

- **Consequence:** *"Adopter relaxation surface is zero (no `--schemas-dir`, no env var, no filesystem-priority fallback)."*
  Route: governing_adrs from child architecture (forecloses the CLI surface from carrying any schema-source override flag).
  Bound by: forthcoming root architecture's CLI front-end component.

- **Consequence:** *"Build pipeline must sync framework-side JSON inputs into the embed-FS root before binary compile."*
  Route: governing_adrs from child architecture (build / release pipeline section).
  Bound by: forthcoming root architecture's deployment / build-pipeline section (root-scope only — see Step 8 of architecture authoring).

- **Consequence:** *"Binary size grows with embedded schema content."*
  Route: revisit-trigger only — listed in Assumptions; no co-located requirement (this is a monitoring concern, not a contract).

- **Consequence:** *"Dev-iteration cost on schemas requires a rebuild."*
  Route: revisit-trigger only — listed in Assumptions; no co-located requirement (this is a developer-experience property).
