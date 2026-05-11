# vmodel-core — session log

Historical record of authoring + review sessions. Extracted from `CLAUDE.md` on 2026-05-10. Current state lives in `CLAUDE.md`; consult this file when reviewing prior context or running a retrospective.

---

## 2026-05-01 — Repo bootstrapped (then-standalone)

11 vmodel skills copied into a project-local `.claude/skills/` mirror; phase-4 PD copied into `seed/`; framework reference documents (TARGET_ARCHITECTURE, BACKLOG, schemas, Zakariasson codex source) copied into `references/`.

## 2026-05-01 — `specs/needs.md` authored

elicit-needs session 1. See `dogfood_findings.md` 2026-05-01 entries for framework gaps surfaced.

## 2026-05-03 — `specs/requirements.md` authored

`vmodel-skill-author-requirements` run; `status: draft`. Adversarial review by `vmodel-skill-review-requirements` returned APPROVED on second pass after one revision cycle. Document is at root scope (`scope: ""`); ~30 atomic requirements across functional / quality-attribute / interface / data sections; 12 inherited constraints; full glossary; explicit *Open gaps* section with named owners and actions. Framework gaps surfaced this session appended to `dogfood_findings.md` (2026-05-03 entries).

## 2026-05-03 (later) — Two foundational ADRs authored and accepted

- **ADR-001** (`specs/adrs/adr-001-implement-vmodel-core-in-go.md`) commits Go as implementation language (drivers: AI-coding-agent corpus density, YAML 1.2 ecosystem maturity via `goccy/go-yaml`, stdlib HTML templating).
- **ADR-002** (`specs/adrs/adr-002-embed-canonical-schemas-in-binary.md`) commits compile-time `embed.FS` for the framework canonical rule catalog / schema set / Quality Bar checklist set, with no runtime override (drivers: IC-007 no-relaxation, IC-002 stateless cold-start, IC-005 re-download-and-replace update).

Both adversarially reviewed by `vmodel-skill-review-adr`; APPROVED on second pass after one revision cycle (ADR-001's Alternatives section was restructured to surface ≥2 real rejected entries — Rust, Zig, C++, Java/.NET-with-AOT — rather than dismiss four candidates inline in Context).

Propagation added four derived requirements to `specs/requirements.md` (REQ-029 output stability; REQ-030 schema-version pinning; REQ-031 no-external-schema-access; REQ-032 version queryability); requirements doc re-reviewed by `vmodel-skill-review-requirements` and APPROVED on second pass (REQ-029 had implementation-prescription rewritten to state byte-identical-output property only; REQ-030 was split into atomic statements with EARS conformance, with REQ-032 created from the split). `specs/requirements.md` now carries 32 atomic requirements (REQ-001..REQ-032).

Framework gap surfaced this session: `dogfood_findings.md` Issue 11 (ADR and architecture author skills materialise new requirements without invoking the requirements-author skill's discipline).

## 2026-05-03 (later still) — `specs/architecture.md` authored

`vmodel-skill-author-architecture` run; `status: draft`. Root-scope architecture decomposing vmodel-core into 7 children (`cli-adapter`, `artifact-loader`, `graph-builder`, `validation-engine`, `reporter`, `emitter`, `embedded-resources`) and 8 interfaces (2 external CLI subprocess + 6 internal Go-package boundaries, all with full Design-by-Contract). Composition pattern: pipeline within a hexagonal shell. Several template sections honest-`n/a` (middleware stack, message-bus, multi-environment split, orchestration target, runtime-unit split, cost model, secrets flow, application-layer authn/authz, bulkheads, circuit breakers, retry, redundancy) because vmodel-core is a CLI not a service.

Adversarial review by `vmodel-skill-review-architecture` returned REJECTED on first pass with 2 hard-reject findings (both same root cause: the `reporter` Decomposition responsibility named the bound library `html/template` inline; should have been carried by `rationale` + ADR-001 only) and 4 soft-reject findings (deprecation policy missing time-window on IValidationCLI / IReportCLI, latency NFR numbers missing on both — all upstream-traceable to existing `requirements.md` *Open gaps*: REQ-022 pilot calibration and REQ-024 follow-up). Hard rejects fixed by single-line edit (removing the library name from responsibility); soft rejects left in place pending upstream resolution.

Mermaid sequence diagrams initially failed to render with parse errors — three causes diagnosed and fixed: `;` interpreted as statement terminator (5 occurrences), `<...>` interpreted as HTML (4 occurrences), `/` in unquoted participant alias (2 occurrences).

Document carries an explicit *Open follow-ups* section cataloguing 8 `[NEEDS-DD: ...]` and 1 `[NEEDS-ADR: ...]` markers with owner / action / citation per item.

Framework gaps surfaced this session appended to `dogfood_findings.md`:
- Issue 12 (no clean tree-level list of pending artifacts)
- Issue 13 (review-output handover should be file-based not chat)
- Issue 14 (no specs-global glossary / definitions document)
- Issue 15 (author-architecture skill's Mermaid templates silent on parser-breaking characters)
- Issue 16 (where do ADR-bound library bindings land in the architecture artifact — author-skill discipline gap caught only at review)

## 2026-05-10 — Bundled into the framework repo at `pilots/vmodel-core/`

Imported via `git subtree add` (history preserved). Skill mirror dropped (use parent `.claude/skills/`); `issues_found.md` renamed to `dogfood_findings.md`; `.vmodel/references/partial-parent-protocol.md` synced from framework; `build.auto_amend` config section added; spec-tree `derived_from` front-matter restored on requirements + architecture (the standalone-era commit had over-applied the DD/TS-only schema simplification).

Mechanical check sweep surfaced pre-existing pilot authoring issues (not migration-induced):
- check-id-encoding: 3 stale empty-scope encodings (REQS-, ARCH-)
- check-implicit-verifies: 5 testspec cases mention IDs in preconds/expected without listing in verifies
- check-mermaid: 1 semicolon-in-sequence-message in architecture.md:305
- check-typed-error-coverage: 5+ typed errors without covering case

## 2026-05-10 — Cleanup pass (drift elimination)

Replaced drifted local copies of `references/schemas/`, `references/framework/TARGET_ARCHITECTURE.md`, and `references/framework/BACKLOG.md` with symlinks to the framework canonical sources. Single source of truth, zero drift, zero artifact-citation rewrites. `references/codex/` remains a frozen citation snapshot.

CLAUDE.md slimmed (107 → ~45 lines): historical timeline extracted to this file; main CLAUDE.md retains only current-state essentials.

## 2026-05-12 — Issue 25 resolved (six-vs-seven schemas → seven first-class types)

Framework decision: Option 1 — `architecture-interface-detail` promoted to a first-class artifact type. Propagation in one pass across framework + pilot:

- Framework: `references/authoring-discipline.md` Rule 8 template now requires `artifact_type` + `title` (the two envelope-required fields the previous template omitted, leaving Rule-8 detail files envelope-invalid in every project). `schemas/artifacts/quality-bar/quality-bar.schema.json` enum + id-prefix + regex extended (new prefix `AID`). New `schemas/artifacts/quality-bar/architecture-interface-detail.quality-bar.json` (4 groups, 16 items, meta-gate). New `schemas/artifacts/fixtures/architecture-interface-detail.example.md`. `link-types.schema.json` and `validation-rules.schema.json` `artifact_type_enum` extended (catalogs already had the type — the schemas were the laggards). `envelope.schema.json` description rephrased to "six core standalone types plus bundle-detail types". `validation-rules.catalog.json` TRV-QB-001 applies-to extended. `docs/guide/artifacts/architecture.html` Rule-8 example's detail-file front-matter corrected (was `parent_artifact` / `interface_name`; now `belongs_to` / `subject` per the actual schema); new paragraph names the detail file as a first-class artifact.
- Pilot: `requirements.md` v2 — Glossary `Framework canonical schema set` and `Framework canonical Quality Bar checklist set` entries name seven; IC-010 / IC-011 sources extended; REQ-016 rationale rephrased to be type-generic. `DD-embedded-resources` v2 — `ArtifactType` enum seven members; bundle layout adds `architecture-interface-detail.schema.json` + `.quality-bar.json`; "six" → "seven" across signatures, complexity_notes, error-matrix, data-structure invariants, closing Note. 8 interface detail files in `specs/architecture/interfaces/` now carry `artifact_type` + `title` and validate against the per-type schema (previously envelope-invalid at every file). `TS-embedded-resources` v2 — parameterised `enumerate:` lists grown to seven; six-enum → seven-enum across titles and prose; closing Note rephrased. Root `testspec.md` v2 — workload fixture "six artifact_type values" → seven. `CLAUDE.md` open-decision bullet replaced with closure note.
- Validation: all 14 spec-tree artifacts with the canonical seven types now pass per-type schema validation (the 2 ADR pre-existing failures are unrelated schema-required-field drift, out of Issue 25's scope). New QB JSON + new fixture both validate clean.
- Dogfood findings: Issue 25 moved from `dogfood_findings.md` to `dogfood_findings_archive.md` with full `**Fixed:**` provenance line. Surprise during execution: discovered that the link-types catalog already named the seventh type in `belongs_to.source_artifact_types`, but the link-types schema enum still had only six — i.e. the catalog had been silently invalid against its own schema. Fixed.
- `DD-validation-engine` authoring (next session) is unblocked.

---

## Open follow-ups (carried forward — track as work begins, not authoring artifacts)

- Pre-existing pilot authoring issues from the mechanical-check sweep (see 2026-05-10 entry).
- Legacy `## Open gaps and follow-ups` sections in `needs.md` and `requirements.md` (24 entries total) — should migrate to inline DEFER markers per framework Phase 6 rule.
- DD authoring on a leaf scope is the next planned authoring session. Recommended starting points: `embedded-resources` (simplest; bounded by ADR-002 + REQ-030/031/032) or `validation-engine` (most load-bearing; bounded by REQ-010..017 + REQ-026). cli-adapter DD is gated on resolving the CLI ergonomic-shape deferrals first (REQ-024 follow-up).
