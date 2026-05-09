# VModelWorkflow — AI-Augmented Spec-Driven Development Framework

## What This Project Is

Four independent components designed to work together for AI-augmented spec-driven development with V-model rigor:

1. **Documentation** — Single source of truth for all domain knowledge. Per artifact type: 5 sections (V-model context, best practices, anti-patterns, examples, Quality Bar). AI skills are derived from this. Non-negotiable foundation.
2. **Templates & Schemas** — Artifact definitions, structural-rigor schemas, canonical Quality Bar checklists. Usable by humans, agents, or both.
3. **Traceability** — Link model + validation rules. Forward links embedded in artifacts; reverse relationships derived by tooling.
4. **AI Skills** — Craft skills (standalone best practices, derived from documentation) and framework skills (orchestration, template integration, traceability use, retrofit mode).

**End goal:** well-structured software, developed by AI agents under tight human design review, where the human leverage point is the spec layer — not code review.

**Primary use cases:**
- **Greenfield development** — top-down through the scope tree.
- **Legacy retrofit** — bottom-up reverse-engineering from existing code. Primary market entry point.

**Each component is independently usable.** The real value is the combination.

---

## Pivot Reference (2026-04-18)

The project pivoted on 2026-04-18 from a safety-specific V-model framework (HW/SW split, tier-based rigor) to a generic layered spec-driven-dev framework with uniform high rigor. See:

- `docs/plan/TARGET_ARCHITECTURE.md` — authoritative architectural reference (6-artifact model, workflows, principles).
- `docs/plan/BACKLOG.md` — execution plan (phases 0–7).
- `archive/pre-pivot-2026-04-18/` — pre-pivot design record with concept mapping.

---

## Working Process

- **Discuss before writing.** Never start writing files without first explaining the approach, showing structure visually (ASCII diagrams), motivating the design choices, and getting explicit approval.
- **Structured back-and-forth.** Present ideas, ask for input or approval, then implement. Applies to schemas, skills, prompts, and any new files.
- **Small increments.** One concept at a time. Get alignment, then move on.
- **Dispatch concrete execution to subagents.** Keep the main conversation focused on design, alignment, and sign-offs; file operations, multi-step lookups, and content rewrites go to subagents.
- **Per-phase handoff docs.** Non-trivial phases get their own `PHASE{N}_AUTHORING_PATTERN.md` under `docs/plan/` — session handoff scaffolding, locked decisions, open points, recommended next step. Load alongside `CLAUDE.md` + `BACKLOG.md` + `TARGET_ARCHITECTURE.md` at session start. Archive to `archive/phase{n}/` on phase completion. Precedents: `archive/phase2/PHASE2_AUTHORING_PATTERN.md`, `archive/phase3/PHASE3_AUTHORING_PATTERN.md`, `archive/phase4/PHASE4_AUTHORING_PATTERN.md`.
- **Skill invocations are tool calls, not references.** When the user types `/skill-name` (e.g. `/prompt-skill-agent-builder`), invoke it via the `Skill` tool **before** doing any other work. Do not treat the slash-prefix as a textual hint and substitute your own design loop — that bypasses the skill's mandatory flow. When the skill loads, read its `references/*.md` and walk its prescribed steps; project conventions in `PHASE{N}_AUTHORING_PATTERN.md` and CLAUDE.md *layer on top of* the invoked skill's discipline, not replace it. **Why:** four Phase 5 skill pairs were authored without invoking `/prompt-skill-agent-builder`, drifting from its anti-pattern rules (refs >100 lines without TOC, re-explaining fundamentals); the drift compounded across pairs because each one patterned-matched on the previous. See `docs/plan/PHASE5_AUTHORING_PATTERN.md` §2.12 for the structural fix.

---

## Core Principles

Ten load-bearing principles. Canonical wording in `TARGET_ARCHITECTURE.md §3`. Short version:

1. **Documentation is the foundation** — derive schemas, templates, skills from docs.
2. **Spec Ambiguity Test** — every spec at every layer must be implementable by a junior engineer or low-mid-tier AI without guessing.
3. **Uniform high rigor** — no tiers; Quality Bar checklists encode rigor per artifact.
4. **Workflow decoupling** — Spec, Build, Retrofit independent; artifact-only coupling.
5. **Tool/skill split** — tools mechanical (no LLM); skills interpretive (LLM-driven).
6. **Tools as independent products** — framework bundles no tools; tools live in their own repos.
7. **Retrofit never fabricates** — human-only content defaults to `recovery_status: unknown`.
8. **Human leverage at the spec level** — review specs, not code.
9. **Components are independent (SOLID)** — adopt incrementally.
10. **Tests derive from the layer's artifact, not from the code below.**

---

## Artifact Set (6 types)

| Type | Lives at | Structure reference |
|---|---|---|
| **Root product (PB \| needs \| PD)** | Root only — one of the three | `TARGET_ARCHITECTURE §5.3`. PB heavyweight, needs interview-derived, PD lightweight. |
| **Requirements** | Non-leaf scopes | `TARGET_ARCHITECTURE §5.3` |
| **Architecture** | Non-leaf scopes | `TARGET_ARCHITECTURE §5.3` (Composition section mandatory; Rule 8 multi-file bundle when size demands) |
| **ADR** | Per-scope `adrs/` (cross-cutting reach) | `TARGET_ARCHITECTURE §5.3` (Reversibility sub-prompt mandatory) |
| **Detailed Design** | Leaf scopes | `TARGET_ARCHITECTURE §5.3` (junior-implementable). `parent_architecture` is the single structural anchor — `derived_from` removed. |
| **TestSpec** | Every scope | `TARGET_ARCHITECTURE §5.3`. `verifies` is the only link field; layer convention determines target (leaf→DD, branch→ARCH, root→REQ+root product). `derived_from` removed. |

**Killed:** `## Open follow-ups` section on all artifacts. DEFER markers (`[DEFER-DD: …]`, `[DEFER-ADR: …]`, `[NEEDS-TEST: …]`) are the single mechanism for naming product-spec gaps. Aggregate at `.vmodel/defer-index.md` (auto-generated).

---

## Build Order

- **Phase 0** — Archival — **DONE** (2026-04-18).
- **Phase 1** — Foundation rewrite (BACKLOG, TARGET_ARCHITECTURE, this CLAUDE.md) — **DONE** (2026-04-18).
- **Phase 2** — Per-artifact documentation (6 types, 5-section structure) — **DONE** (2026-04-22).
- **Phase 3** — Schemas (per-artifact JSON Schema draft 2020-12 + traceability catalogs + Quality Bar JSON + minimal fixtures) — **DONE** (2026-04-23).
- **Phase 4** — Product Descriptions for purpose-built tools — **CLOSED** (2026-04-26) without producing PDs. The vmodel-core pilot surfaced that PD was a category error: the actual gap is a missing **elicitation skill** at root scope. Framework retains 6 artifact types. Phase 5 picks up `vmodel-skill-elicit-needs` (renamed from `vmodel-skill-elicit-requirements` during authoring to align with INCOSE's Needs vs Requirements distinction). See `BACKLOG §3.4` + `archive/phase4/PHASE4_AUTHORING_PATTERN.md` §7.
- **Phase 5** — Skills (craft per artifact + elicit-needs) — **complete (closeout 2026-05-09).** Five per-artifact author/review pairs landed (requirements, architecture, detailed-design, testspec, ADR); elicit-needs landed; product-brief pair stays deferred (PB authoring is direct against schema until dogfooding shows value of formalising). Framework-skills closeout reabsorbed into Phase 6 build-flow design (orchestration is now `vmodel-skill-orchestrate-build`).
- **Phase 6** — Build flow + central config + greenfield pilot — **substantially advanced (2026-05-09).**
  - **Build flow scaffolded** — 6 build-side skills shipped: `vmodel-skill-{plan-build, orchestrate-build, render-tests, implement-leaf, review-execution, retrospect-build}`. Pipeline state machine + layered execution (leaf unit → branch integration → root system) + V-model-typed escalation routing.
  - **Central config (`.vmodel/`) introduced** — every project gets `.vmodel/config.yaml` + `.vmodel/references/` (shared reference docs) + `.vmodel/.reviews/` + `.vmodel/.build/`. Skills resolve refs via config, never hardcode framework `docs/` paths. `vmodel-init` skill scaffolds + has migrate mode.
  - **Lightweight root product (PD)** — third option for root-of-tree alongside PB and needs. New skill `vmodel-skill-elicit-pd`.
  - **Schema simplifications** — DD drops `derived_from` (keeps `parent_architecture` only); TestSpec drops `derived_from` (keeps `verifies` only with layer convention); `## Open follow-ups` killed everywhere (DEFER markers are single mechanism); per-skill bundled copies of shared refs retired (sync scripts removed).
  - **Pre-pivot skills retired** — `develop-code`, `derive-test-cases`, `vmodel-skill-review-code`, `*-workspace` archived under `archive/pre-pivot-skills/`.
  - **vmodel-core dogfooding pilot** — `/home/stefanus/repos/vmodel-core/` continues; artifacts migrated to new schema; `.vmodel/` scaffolded.
- **Phase 7** — Retrofit-specific additions (gated on Phase 6 dogfooding signal).

Full details in `docs/plan/BACKLOG.md`.

**Pre-pivot work archived:**
- `develop-code`, `develop-code-workspace`, `derive-test-cases`, `derive-test-cases-workspace`, `vmodel-skill-review-code`, `vmodel-skill-review-code-workspace`, `combined-workspace` → `archive/pre-pivot-skills/` (2026-05-09).
- Lower V docs (`source-code.html`, `unit-test.html`, `detailed-design.html`) — kept as pre-pivot outputs in `docs/guide/`; mined as reference.

---

## Documentation

### docs/guide/ (Interactive HTML)

**Keep documentation in sync with every change.** Whenever components are updated (schemas, trace model, skills), the corresponding section in `docs/guide/` must also be updated.

**Domain translation plugin — parked.** Content is authored in direct software-engineering English. The runtime translation plugin and domain JSON files were archived to `archive/pre-pivot-2026-04-18/domains/` in Phase 2; `js/domain.js` was removed; page-level `[data-term]` wiring was stripped. The mechanism (or a simpler successor) may be reintroduced once content is stable (see `TARGET_ARCHITECTURE §15`).

**Proactively raise this:** when working on component changes, always remind that `docs/guide/` needs a corresponding update before the work is considered complete.

### Per-Artifact Documentation Structure (5 sections)

1. **V-model context** — what, where, why (how the artifact fits in the development flow).
2. **Best practices** — how to produce quality output (the bulk).
3. **Anti-patterns** — common mistakes.
4. **Examples** — good and bad.
5. **Quality Bar** — concrete Yes/No checklist grouped by concern. Canonical JSON form lives under `schemas/artifacts/quality-bar/` (extracted in Phase 3) and is consumed by templates + authoring/review skills.

Framework-integration and AI-skills-integration coverage — which appeared as separate sections in an earlier draft — are craft-orthogonal and belong in tool docs and skill docs respectively, not in per-artifact craft pages.

This documentation is the source of truth for craft. AI craft skills are distilled from it. Write docs first, then derive skills.

---

## Key Concept: Spec Ambiguity Test

Every specification artifact — at every layer — must be unambiguous enough that a junior engineer or low-mid-tier AI could act on it without guessing. This is the meta-gate for all specification work and the completeness test for every artifact.

---

## Domain

- V-model as **engineering infrastructure** — safety-specific framing removed. The techniques (layered decomposition, traceability, design-test coupling) apply at any rigor level.
- **Direct software-engineering English** in authored content; the pre-pivot translation plugin for standards vocabulary (DO-178C, ASPICE, ISO 26262) is deferred (see Documentation section above).
- EARS syntax is a craft skill preference, not a framework requirement.

---

## First Pilot Target

- Java 17, Gradle, JUnit 5.
- Legacy codebase: ~100k+ lines, ~10% test coverage, no documentation.
- Requirements in mixed formats (Word, spreadsheets, DOORS) — possibly incomplete or stale.
- Target user: mid-senior engineers orchestrating AI agents.

---

## Key Concept: DRTDD

Design-Requirement-Test Driven Development extends TDD:
```
REQUIRE → DESIGN → TEST(red) → IMPLEMENT(green) → REFACTOR → VERIFY
```
Each phase produces traceable artifacts. Human gates between phases.

---

## Repository Structure

### Framework repo (this project)

```
archive/                — Pre-pivot content (pre-pivot-2026-04-18/) + per-phase handoff docs + pre-pivot-skills/
references/             — Framework-shipped reference defaults (copied to .vmodel/references/ at init)
                          authoring-discipline.md, authoring-self-check.md, partial-parent-protocol.md,
                          requirements-shape-checklist.md, definitions/{component,unit}.md
research/               — Research documents on standards, patterns, strategies
docs/plan/              — TARGET_ARCHITECTURE.md, BACKLOG.md, per-phase handoff docs
docs/guide/             — Interactive HTML documentation
docs/                   — Framework-internal notes (skill-creation-learnings.md)
schemas/
  core/                 — Meta-schemas (vmodel-config.schema.yaml, craft-skill, orchestration-pipeline)
  artifacts/            — Per-artifact JSON schemas (draft 2020-12) + envelope + common-defs
    quality-bar/        — Quality Bar checklists
    fixtures/           — Minimal-example fixtures
  traceability/         — Link-type + validation-rule catalogs
scripts/                — Mechanical check scripts (check-*.py, index-deferred-items.py)
.claude/skills/         — 18 V-model skills:
                          spec-side (12): elicit-needs, elicit-pd, author/review pairs for
                          {requirements, architecture, adr, detailed-design, testspec}
                          build-side (6): plan-build, orchestrate-build, render-tests,
                          implement-leaf, review-execution, retrospect-build
                          + vmodel-init
```

### Project consumer (e.g. vmodel-core)

```
.vmodel/
  config.yaml           — Project central config (schema in framework/schemas/core/)
  references/           — Shared skill references (copied from framework at init; project may override)
    authoring-discipline.md
    authoring-self-check.md
    partial-parent-protocol.md
    requirements-shape-checklist.md
    definitions/{component,unit}.md
  defer-index.md        — Auto-generated DEFER aggregate (gitignored; regenerated by index-deferred-items.py)
  .reviews/             — Spec-side review verdict files (checked in)
  .build/
    tasks.yaml          — Build task DAG (from plan-build)
    pipeline-state.yaml — Pipeline state (gitignored; transient)
    tasks/{id}/         — Per-task review-ready.yaml, feedback.yaml, log.txt (logs gitignored)
    escalations/ESC-NNN.yaml  — Layer-typed escalations (checked in)
    runs/{run-id}/      — Retrospectives + metrics (gitignored)
    lessons.yaml        — Cumulative bounded lessons (checked in)

specs/                  — Spec scope tree (per TARGET §5.7)
  product_brief.md  OR  needs.md  OR  product_description.md   (one of, mandatory at root)
  glossary.md           — Mandatory document (not yet a first-class artifact)
  requirements.md
  architecture.md       (+ optional architecture/interfaces/ bundle, Rule 8)
  testspec.md
  adrs/                 — Per-scope (Rule 7)
  {branch-scope}/       — Recurse: requirements.md, architecture.md, testspec.md, adrs/
    {leaf-scope}/       — detailed_design.md, testspec.md
```

---

## Conventions

- Artifact files: single-file Markdown, YAML front-matter + embedded YAML blocks + Mermaid.
- Terminology: direct software-engineering English; standards-vocabulary translation layer deferred (see Documentation section).
- **Uniform high rigor.** No per-artifact rigor tiers.
- All framework outputs include verification via Quality Bar checklists.
- IDs are stable across file renames; traceability links reference IDs, not paths.
- EARS is used by craft skills but not enforced by schemas.
- **No `docs/` path references in skills.** Skills resolve shared references via `.vmodel/config.yaml` `paths.references` (default `.vmodel/references/`). Framework ships defaults; init copies them; projects may override.
- **DEFER markers are the single mechanism** for naming product-spec gaps. `## Open follow-ups` sections are not authored on any artifact.
- **Per-skill bundled copies of shared references are retired.** Skills load shared refs (authoring-discipline, partial-parent-protocol, etc.) from `.vmodel/references/`. Skill-specific references stay bundled in each skill's `references/` directory.

---

## Build Flow (Phase 6)

The build flow runs after spec authoring and produces code + tests with V-model coupling. Six build-side skills:

- `vmodel-skill-plan-build` — derive task DAG from architecture + leaves + ADRs; emit `.vmodel/.build/tasks.yaml`.
- `vmodel-skill-orchestrate-build` — pipeline state machine; dispatches sub-skills per task; layered execution (leaf → branch → root); layer-typed escalations.
- `vmodel-skill-render-tests` — TestSpec → executable tests (TDD red phase). Layer-aware: leaf TS → unit, branch TS → integration, root TS → system.
- `vmodel-skill-implement-leaf` — TDD green + refactor for one leaf (greenfield or fix mode); strict DD/ADR adherence.
- `vmodel-skill-review-execution` — verdict at any layer (APPROVED / REJECTED / ESCALATE); routes failures to the responsible spec layer (DD, TestSpec, ARCH, ADR, REQ, root product).
- `vmodel-skill-retrospect-build` — extract bounded lessons from a build run.

Escalations are typed by target spec layer and confidence-tagged. High-confidence routes auto-fire; low-confidence surfaces to human gating.

No build-side artifact yet — Verification Report was considered and dropped (no current need).

---

## Engineering Codex (shared knowledge bank)

A persistent knowledge bank lives at `/home/stefanus/repos/engineering-codex/`. It contains synthesized, cited research on software engineering standards, code quality, system design, and AI-augmented development — material that informs decisions in this project.

**Before doing fresh research on a topic, check the codex first:**

1. Read `/home/stefanus/repos/engineering-codex/CLAUDE.md` to understand the schema (one-time per session).
2. Read `/home/stefanus/repos/engineering-codex/index.md` to see what pages exist.
3. Read the relevant wiki pages. Load-bearing claims should be verified against the cited source pages.

**After doing research that produced reusable findings, offer to file them back:**

Tell the human: "I found X while researching Y. This looks like a candidate for the engineering-codex. Want me to ingest the source and update relevant pages?"

**Do not duplicate codex content here.** Link to it instead.

**The codex is read-only from this project unless the human explicitly asks you to ingest something into it.** Treat writes to `engineering-codex/` as a deliberate cross-repo action requiring confirmation.
