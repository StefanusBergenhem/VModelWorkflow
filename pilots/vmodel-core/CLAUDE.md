# vmodel-core

Greenfield dogfooding pilot for the V-model AI-augmented spec-driven-development framework.

## What this repo is

`vmodel-core` is the first of three planned purpose-built tool products for the framework (the others are `vmodel-author` and `vmodel-retrofit`). It is also the **first real-use pilot** of the framework's per-artifact authoring + review skills.

**Per `TARGET_ARCHITECTURE §10` of the framework repo, vmodel-core is the daily-driver tool:**
- Artifact parser (`.md` + YAML + Mermaid → structured data).
- Schema validator (structural rigor per artifact type).
- Traceability validator (link integrity, completeness, cycles).
- Quality Bar structural runner.
- Graph builder (derived traceability graph).
- Query engine.
- Scaffolder.
- Renderer.

**Stakeholder:** every framework adopter — engineers running pre-commit checks, CI pipelines, authoring/review skills invoking subprocess tools.

## Repo relationship

`vmodel-core` lives at `pilots/vmodel-core/` inside the VModelWorkflow framework repo (bundled in 2026-05-10 to shorten the dogfood feedback loop — schema gaps, skill bugs, and pilot fixes can be resolved in one branch instead of cross-repo round-trips). Future graduation back to a standalone repo is supported via `git filter-repo --subdirectory-filter pilots/vmodel-core`.

Skills are **not** bundled here — the framework's canonical `.claude/skills/` at the repo root is the single source of truth and is in-scope when running Claude Code from this subdir. If a skill bug surfaces during the pilot, fix it in `.claude/skills/<name>/` directly; no cross-repo copy step.

The pilot's `.vmodel/` directory holds project-local config and reference copies (`config.yaml`, `references/*`, `defer-index.md`). Reference copies are refreshed via `/vmodel-init` migrate mode after framework changes.

## Status

**2026-05-01 — Repo bootstrapped (then-standalone).** 11 vmodel skills copied into a project-local `.claude/skills/` mirror; phase-4 PD copied into `seed/`; framework reference documents (TARGET_ARCHITECTURE, BACKLOG, schemas, Zakariasson codex source) copied into `references/`.

**2026-05-10 — Bundled into the framework repo at `pilots/vmodel-core/`.** Skill mirror dropped (use parent `.claude/skills/`); `issues_found.md` renamed to `dogfood_findings.md`; `.vmodel/references/partial-parent-protocol.md` synced from framework; `build.auto_amend` config section added; spec-tree `derived_from` front-matter restored on requirements + architecture (the standalone-era commit had over-applied the DD/TS-only schema simplification).

**2026-05-01 — `specs/needs.md` authored** (elicit-needs session 1, see `dogfood_findings.md` 2026-05-01 entries for framework gaps surfaced).

**2026-05-03 — `specs/requirements.md` authored** (vmodel-skill-author-requirements run; `status: draft`). Adversarial review by `vmodel-skill-review-requirements` returned APPROVED on second pass after one revision cycle. Document is at root scope (`scope: ""`); ~30 atomic requirements across functional / quality-attribute / interface / data sections; 12 inherited constraints; full glossary; explicit *Open gaps* section with named owners and actions. Framework gaps surfaced this session are appended to `dogfood_findings.md` (2026-05-03 entries).

**2026-05-03 (later) — Two foundational ADRs authored and accepted.** **ADR-001** (`specs/adrs/adr-001-implement-vmodel-core-in-go.md`) commits Go as implementation language (drivers: AI-coding-agent corpus density, YAML 1.2 ecosystem maturity via `goccy/go-yaml`, stdlib HTML templating). **ADR-002** (`specs/adrs/adr-002-embed-canonical-schemas-in-binary.md`) commits compile-time `embed.FS` for the framework canonical rule catalog / schema set / Quality Bar checklist set, with no runtime override (drivers: IC-007 no-relaxation, IC-002 stateless cold-start, IC-005 re-download-and-replace update). Both adversarially reviewed by `vmodel-skill-review-adr`; APPROVED on second pass after one revision cycle (ADR-001's Alternatives section was restructured to surface ≥2 real rejected entries — Rust, Zig, C++, Java/.NET-with-AOT — rather than dismiss four candidates inline in Context). Propagation added four derived requirements to `specs/requirements.md` (REQ-029 output stability; REQ-030 schema-version pinning; REQ-031 no-external-schema-access; REQ-032 version queryability); requirements doc re-reviewed by `vmodel-skill-review-requirements` and APPROVED on second pass (REQ-029 had implementation-prescription rewritten to state byte-identical-output property only; REQ-030 was split into atomic statements with EARS conformance, with REQ-032 created from the split). `specs/requirements.md` now carries 32 atomic requirements (REQ-001..REQ-032). Framework gap surfaced this session: `dogfood_findings.md` Issue 11 (ADR and architecture author skills materialise new requirements without invoking the requirements-author skill's discipline).

**2026-05-03 (later still) — `specs/architecture.md` authored** (vmodel-skill-author-architecture run; `status: draft`). Root-scope architecture decomposing vmodel-core into 7 children (`cli-adapter`, `artifact-loader`, `graph-builder`, `validation-engine`, `reporter`, `emitter`, `embedded-resources`) and 8 interfaces (2 external CLI subprocess + 6 internal Go-package boundaries, all with full Design-by-Contract). Composition pattern: pipeline within a hexagonal shell. Several template sections honest-`n/a` (middleware stack, message-bus, multi-environment split, orchestration target, runtime-unit split, cost model, secrets flow, application-layer authn/authz, bulkheads, circuit breakers, retry, redundancy) because vmodel-core is a CLI not a service. Adversarial review by `vmodel-skill-review-architecture` returned REJECTED on first pass with 2 hard-reject findings (both same root cause: the `reporter` Decomposition responsibility named the bound library `html/template` inline; should have been carried by `rationale` + ADR-001 only) and 4 soft-reject findings (deprecation policy missing time-window on IValidationCLI / IReportCLI, latency NFR numbers missing on both — all upstream-traceable to existing `requirements.md` *Open gaps*: REQ-022 pilot calibration and REQ-024 follow-up). Hard rejects fixed by single-line edit (removing the library name from responsibility); soft rejects left in place pending upstream resolution. Mermaid sequence diagrams initially failed to render with parse errors — three causes diagnosed and fixed: `;` interpreted as statement terminator (5 occurrences), `<...>` interpreted as HTML (4 occurrences), `/` in unquoted participant alias (2 occurrences). Document carries an explicit *Open follow-ups* section cataloguing 8 `[NEEDS-DD: ...]` and 1 `[NEEDS-ADR: ...]` markers with owner / action / citation per item. Framework gaps surfaced this session appended to `dogfood_findings.md`: Issue 12 (no clean tree-level list of pending artifacts), Issue 13 (review-output handover should be file-based not chat), Issue 14 (no specs-global glossary / definitions document), Issue 15 (author-architecture skill's Mermaid templates silent on parser-breaking characters), Issue 16 (where do ADR-bound library bindings land in the architecture artifact — author-skill discipline gap caught only at review).

**Next session:** likely candidates, in priority order — (a) Detailed Design authoring for one or more leaf scopes (`vmodel-skill-author-detailed-design`); recommended starting points are `embedded-resources` (simplest; bounded by ADR-002 + REQ-030/031/032) or `validation-engine` (most load-bearing; bounded by REQ-010..017 + REQ-026); the cli-adapter DD is gated on resolving the CLI ergonomic-shape deferrals first (REQ-024 follow-up). (b) Fix forward on framework gaps surfaced this session — `dogfood_findings.md` Issue 16 (architecture-author landing rules for ADR-bound bindings) is the highest-value framework fix because it will recur immediately when DD authoring begins (DDs are even more library-bound than architecture); Issue 15 (Mermaid pitfall warnings) is a smaller-cost concurrent fix. (c) Framework-level (VModelWorkflow-scope) elicitation pass to address `dogfood_findings.md` Issue 2 (no parent-scope upstream). (d) Author a vmodel-core Product Brief to retire the `[NEEDS-vmodel-core]` placeholder per `dogfood_findings.md` Issue 1 / decision γ. Choose at session start.

## Repo layout

```
pilots/vmodel-core/
├── .vmodel/                    (project central config — see framework CLAUDE.md)
│   ├── config.yaml
│   ├── references/             (shared reference docs; refresh via /vmodel-init migrate)
│   ├── defer-index.md          (auto-generated by scripts/index-deferred-items.py)
│   ├── .reviews/               (spec-side review verdict files)
│   └── .build/                 (build-flow tasks, pipeline state, runs)
├── seed/
│   └── product_description.md  (phase-4 PD — seed input for elicit-needs)
├── references/                 (legacy standalone-era reference copies; kept for historical citations in artifacts)
│   ├── framework/
│   │   ├── TARGET_ARCHITECTURE.md
│   │   └── BACKLOG.md
│   ├── schemas/                (full schemas tree — vmodel-core's runtime input data)
│   └── codex/
│       └── src-zakariasson-clis-for-agents-2026.md
├── specs/
│   ├── needs.md                (root-scope stakeholder needs; elicit-needs output)
│   ├── requirements.md         (root-scope requirements; status: draft; REQ-001..REQ-032)
│   ├── architecture.md         (root-scope architecture; status: draft; ARCH; 7 children, 8 interfaces)
│   ├── architecture/interfaces/ (per-interface detail bundle, Rule 8)
│   ├── testspec.md             (root-scope hybrid TestSpec; status: draft)
│   └── adrs/                   (architecture decision records; flat layout, scope_tags-keyed)
│       ├── adr-001-implement-vmodel-core-in-go.md
│       └── adr-002-embed-canonical-schemas-in-binary.md
├── dogfood_findings.md         (living: framework gaps surfaced during pilot)
├── CLAUDE.md
└── .gitignore
```

Skills resolve from the framework's canonical `.claude/skills/` at the repo root (no project-local mirror).

## Skills available

The full V-model skill set is resolved from the framework's `.claude/skills/` at the repo root:

```
spec-side (12):  elicit-needs, elicit-pd, author/review pairs for
                 {requirements, architecture, adr, detailed-design, testspec}
build-side (6):  plan-build, orchestrate-build, render-tests, implement-leaf,
                 review-execution, retrospect-build
init:            vmodel-init
```

## Working process

Same discipline as the framework repo:
- Discuss before writing — show structure, motivate choices, get approval.
- Skill invocations are tool calls, not references — when invoking a skill, call the `Skill` tool, do not pattern-match.
- The framework CLAUDE.md (at repo root) is also in scope and authoritative; the conventions here layer on top of it without overriding.

## Pilot purpose

This pilot generates the empirical signal needed to:
1. Drive the Phase 6 build-flow design via real authoring + review reps.
2. Inform Phase 7 retrofit design.
3. Surface framework gaps fast (now bundled — fix in `.claude/skills/`, schema, or scripts directly).
4. Resolve elicit-needs decision γ (promote / merge / stay-transient).

Document pilot learnings in `dogfood_findings.md` as they emerge.
