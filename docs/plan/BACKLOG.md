# Backlog

Execution plan for the VModelWorkflow framework following the 2026-04-18 pivot. Action-oriented. For architectural rationale, see `TARGET_ARCHITECTURE.md`.

---

## 1. Current State (snapshot)

| Phase | Title | Status |
|---|---|---|
| 0 | Archival | **DONE** (2026-04-18) |
| 1 | Foundation rewrite | **DONE** (2026-04-18) |
| 2 | Per-artifact documentation | **DONE** (2026-04-22) |
| 3 | Schemas + traceability + Quality Bar | **DONE** (2026-04-23) |
| 4 | Product Descriptions | **CLOSED without producing PDs** (2026-04-26) — the gap was a missing elicitation skill, not a missing artifact type |
| 5 | Skills (craft + framework) | **EFFECTIVE COMPLETE** (closeout 2026-05-09) — 5 author/review pairs + 2 elicit skills landed; PB pair + Haiku-floor evals deferred |
| 6 | Build flow + central config + greenfield pilot | **SUBSTANTIALLY ADVANCED** (rolling, latest landing 2026-05-10) — see §3.6 |
| 7 | Retrofit-specific additions | **PENDING** (gated on Phase 6 dogfooding signal) |

**Active deliverables:**
- 18 V-model skills installed: 12 spec-side (5 author/review pairs + elicit-needs + elicit-pd) + 6 build-side (plan-build, orchestrate-build, render-tests, implement-leaf, review-execution, retrospect-build) + vmodel-init.
- 3 worker agents (`render-tests`, `implement-leaf`, `review-execution`) under `.claude/agents/` — thin dispatch shells loading the canonical skill via the Skill tool.
- 6 per-artifact JSON Schemas (draft 2020-12) + envelope + common-defs + traceability catalogs + Quality Bar JSON + minimal fixtures. (Schemas + Quality Bars for `needs.md` and `product_description.md` pending — see §3.6 Cluster 7.)
- 6 artifact craft pages under `docs/guide/artifacts/` (5-section structure). (`needs.html` and `product-description.html` pending — see §3.6 Cluster 7.)
- `docs/guide/skills-architecture.html` rewritten for the post-pivot, post-build-flow world (2026-05-10).
- `docs/guide/index.html` refreshed (2026-05-10) to reflect Phase 6 state, central config, walker tool, and 3-root-artifact treatment.
- `scripts/walk-impact.py` shipped (2026-05-10) — candidate-set propagation walker (TARGET §8.3); 22-test TDD suite; `tests/test_walk_impact.py` + fixture tree under `tests/fixtures/walk-impact/specs/`.
- `vmodel-core` greenfield dogfooding pilot active — bundled at `pilots/vmodel-core/` (2026-05-10; external repo archived). First leaf DD (`DD-embedded-resources`) landed 2026-05-11.
- 20 research documents in `research/` — secondary substrate with explicit safety-bias caveat (authored pre-pivot; extract craft, discard ASPICE/DO-178C framing).

**Recent landings (2026-05):**
- 6 build-side skills + central config (`.vmodel/`) + vmodel-init + elicit-pd.
- DD/TestSpec schema simplifications (drop `derived_from`); `## Open follow-ups` killed everywhere.
- Pre-skill bundled shared refs retired; pre-pivot skills archived.
- Leaf-build triplet alignment to source-code.html + unit-test.html craft + per-task file ownership enforcement.
- wf-comparison five-phase upgrade: TOC/persona fixes, task-contract enrichment (`acceptance_criteria` / `context_to_load` / `out_of_scope`), scope-expansion HALT + `build-blocked.yaml` + auto-amend, per-gate `build-progress.yaml` + resume modes, per-task workers wrapped as agents for parallel isolated execution.
- **vmodel-core pilot bundled into framework repo** (2026-05-10, commit 76c2686) at `pilots/vmodel-core/`; symlinks drift-proof framework canonical references (commit 7c28173); external repo archived.
- **First leaf DD landed** (2026-05-11) — `DD-embedded-resources` (six accessors over `embed.FS`, stateless, one error code, bundle layout pinned). Authored via `/vmodel-skill-author-detailed-design`; front-matter + embedded-YAML schema-valid. Surfaced four new dogfood findings (Issues 25–28): six-vs-seven schema type gap, DEFER markers bleeding across scopes, 178k session-token cost on the simplest leaf, missing pre-built schema-validation script.

---

## 2. Pivot Reference

The canonical 2026-04-18 pivot decisions are recorded in:

- `archive/pre-pivot-2026-04-18/status.md` — full design-session record (Q1–Q7 and the NQ questions).
- `archive/pre-pivot-2026-04-18/README.md` — pivot summary + old → new concept mapping.

Architectural rationale — including the full Q8–Q15 and NQ-B/C/D/E decisions — is captured in `TARGET_ARCHITECTURE.md`. This backlog indexes it; it does not duplicate.

---

## 3. Migration Phases

### 3.1 Phase 1 — Foundation Rewrite — DONE

**Goal:** Align `BACKLOG.md`, `TARGET_ARCHITECTURE.md`, and `CLAUDE.md` with the new model so future sessions can pick up without needing the 2026-04-18 design transcript.

**Delivered:** Three planning files rewritten. Future sessions can load them and continue without the transcript.

### 3.2 Phase 2 — Per-artifact Documentation — DONE (2026-04-22)

**Goal:** Rewrite `docs/guide/artifacts/*.html` for the six artifact types under the **5-section structure** (V-model context, best practices, anti-patterns, examples, Quality Bar).

**Delivered:**
- Six artifact pages: ADR (pattern-setter), Detailed Design, Product Brief, Requirements, Architecture, TestSpec.
- Landing page rewritten against `TARGET_ARCHITECTURE`.
- Pre-pivot artifact pages archived to `archive/pre-pivot-2026-04-18/docs-guide-artifacts/`.
- Domain translation plugin machinery removed; JSON files archived.
- `PHASE2_AUTHORING_PATTERN.md` archived to `archive/phase2/` on completion.

### 3.3 Phase 3 — Schemas + Traceability + Quality Bar — DONE (2026-04-23)

**Goal:** Per-artifact schemas derived from the Phase 2 docs; traceability schema; **Quality Bar JSON extraction (canonical machine format)** per artifact. JSON Schema draft 2020-12 throughout.

**Delivered:**
- Six per-artifact schemas + envelope + common-defs under `schemas/artifacts/`.
- Four traceability files under `schemas/traceability/` (link-types catalog: 9 types; validation-rules catalog: 13 rules).
- Seven files under `schemas/artifacts/quality-bar/` (one container schema + six data files).
- Six minimal-example Markdown fixtures under `schemas/artifacts/fixtures/` round-tripping clean through their schemas.
- TRV-QB-001 (Quality Bar cascade rule) activated.
- `PHASE3_AUTHORING_PATTERN.md` archived to `archive/phase3/` on completion.

### 3.4 Phase 4 — Product Descriptions — CLOSED without producing PDs (2026-04-26)

**Closeout finding.** PD was a category error. The vmodel-core PD pilot surfaced that the gap was not a missing artifact type but a missing **elicitation skill** at root scope. The framework retains its 6-artifact set; the work was rerouted into Phase 5 as `vmodel-skill-elicit-needs`.

**Delivered (as built):**
- vmodel-core Product Brief draft (business-PB experiment) → `archive/phase4-business-pb-experiment/`.
- vmodel-core Product Description draft → preserved at `docs/plan/phase4-tool-briefs/core/product_description.md` as eval input for elicit-needs.
- `PHASE4_AUTHORING_PATTERN.md` archived to `archive/phase4/` on closeout.

**Cancelled:** PDs for `vmodel-author` and `vmodel-retrofit` (these tools, if still wanted, will be spec'd via the regular Specification workflow).

### 3.5 Phase 5 — Skills (craft + framework) — EFFECTIVE COMPLETE (closeout 2026-05-09)

**Original goal:** Build per-artifact authoring + review skills, plus framework skills (orchestration, traceability, retrofit), plus the stakeholder-elicitation skill carried over from Phase 4.

**Revised goal (2026-05-01):** Per-artifact pairs + elicit-needs are sufficient to start the greenfield dogfooding pilot. Framework skills + closeout activities are deferred — building them before any forward-run signal would calcify wrong assumptions.

**Delivered:** 11 spec-side skill directories under `.claude/skills/`:
- `vmodel-skill-elicit-needs` (2026-04-29) — interview-style stakeholder elicitation; rough `needs.md` output; renamed from `elicit-requirements` to align with INCOSE Needs vs Requirements distinction. Decision γ — informal `needs.md` shape, promotion path TBD after pilot reps.
- `vmodel-skill-author-requirements` + `vmodel-skill-review-requirements` (2026-04-27) — pattern-setter for the remaining pairs.
- `vmodel-skill-author-architecture` + `vmodel-skill-review-architecture` (2026-04-30).
- `vmodel-skill-author-detailed-design` + `vmodel-skill-review-detailed-design` (2026-04-30).
- `vmodel-skill-author-testspec` + `vmodel-skill-review-testspec` (2026-05-01).
- `vmodel-skill-author-adr` + `vmodel-skill-review-adr` (2026-05-01) — final per-artifact pair; smallest by design (single inward seam).

**Deferred (rolled into Phase 6 or later):**
- ~~`vmodel-skill-author-product-brief` + `vmodel-skill-review-product-brief`.~~ Deferred indefinitely. `needs.md` from elicit-needs carries the root-scope upstream role; revisit alongside the elicit-needs decision γ.
- ~~`vmodel-skill-traceability` + `vmodel-skill-orchestration` + `vmodel-skill-retrofit`.~~ Deferred. Orchestration was reabsorbed into Phase 6 build-flow design (now `vmodel-skill-orchestrate-build`). Traceability and retrofit await their respective tooling / pilot signal.
- ~~Rewrite `docs/guide/skills-architecture.html`.~~ **DONE 2026-05-10** — full rewrite landed covering spec flow + build flow + handovers + 3 user workflows.
- ~~Haiku-floor evaluation per skill.~~ Deferred until pilot signal.

**Phase 5 closeout signal (revised):** triggered by Phase 6 dogfooding signal — pilot reps will tell us whether to (a) finish the deferred items as-spec'd, (b) revise them, or (c) drop them.

### 3.6 Phase 6 — Build Flow + Central Config + Greenfield Pilot — IN PROGRESS

**Goal:** Build the AI-augmented build flow that consumes spec artifacts and produces code + tests. Establish a central project config (`.vmodel/`). Run a greenfield dogfooding pilot (`vmodel-core`) to validate the framework end-to-end.

**Note on phase scope.** This phase replaces the original "Phase 6 — Tools (purpose-built)" plan. Purpose-built tools (`vmodel-core`, `vmodel-author`, `vmodel-retrofit`) per `TARGET_ARCHITECTURE §10` are not the current critical path — the build-side skills + central config + dogfooding pilot are. Tool work is deferred until the pilot signal indicates which mechanical checks deserve productisation.

**Delivered:**

*Build-side skills (6):*
- `vmodel-skill-plan-build` — derives task DAG from spec tree; populates `acceptance_criteria` / `context_to_load` / `out_of_scope` mechanically; emits `.vmodel/.build/tasks.yaml`.
- `vmodel-skill-orchestrate-build` — pipeline state machine; layered execution (leaf unit → branch integration → root system); dispatches workers via Task tool; layer-typed escalation routing; resume is schema-validated.
- `vmodel-skill-render-tests` — TestSpec → executable tests (TDD red phase). Layer-aware.
- `vmodel-skill-implement-leaf` — TDD green + refactor for one leaf; greenfield / fix / resume modes; scope-expansion HALT via `build-blocked.yaml`.
- `vmodel-skill-review-execution` — verdict at any layer (APPROVED / REJECTED / ESCALATE); confidence-tagged escalations routed to responsible spec layer. APPROVED writes no file (orchestrator infers from absence).
- `vmodel-skill-retrospect-build` — bounded lessons extraction; refuses to fabricate.

*Worker agents (3):* `.claude/agents/{render-tests,implement-leaf,review-execution}.md` — thin dispatch shells. Loaded by `orchestrate-build` via Task tool for parallel isolated execution.

*Central config:* `.vmodel/config.yaml` + `.vmodel/references/` (shared reference docs, framework-shipped defaults overrideable per project) + `.vmodel/.reviews/` (committed verdict files) + `.vmodel/.build/` (gitignored runtime state).

*Init skill:* `vmodel-init` — scaffolds `.vmodel/`; migrate mode upgrades existing projects.

*Lightweight root product:* `vmodel-skill-elicit-pd` — third option alongside PB and needs.

*Schema simplifications:* DD drops `derived_from` (keeps `parent_architecture` only); TestSpec drops `derived_from` (keeps `verifies` only with layer convention); `## Open follow-ups` killed everywhere — DEFER markers single mechanism.

*Per-skill bundled copies of shared refs retired;* sync scripts removed.

*Pre-pivot skills archived* (`develop-code`, `derive-test-cases`, `vmodel-skill-review-code` and their workspaces) → `archive/pre-pivot-skills/`.

*Per-task file contract* (leaf build):
- `current-task.yaml` ← orchestrator
- `render-report.yaml` ← render-tests
- `build-progress.yaml` ← implement-leaf (overwrite-on-update gate journal)
- `build-blocked.yaml` ← implement-leaf (scope-expansion HALT)
- `review-ready.yaml` ← implement-leaf (sole producer; the impl handoff)
- `feedback.yaml` ← review-execution (REJECTED only)
- `ESC-NNN.yaml` ← review-execution (ESCALATE; mirror copy in `.vmodel/.build/escalations/`)
- APPROVED writes no file (orchestrator infers from absence)

*Rejection taxonomy normalised:* `contract-violation`, `scope-violation`, `missing-implementation`, `wrong-assertion-is-impl-bug`, `integration-failure-impl-bug`, `regression`. The `-impl-bug` suffix disambiguates from cases that ESCALATE to spec layers.

*wf-comparison five-phase upgrade* (2026-05-10):
- (A) TOCs added to four reference files >100 lines + orchestrate-build SKILL.md persona reword.
- (B) Task-contract enrichment — `acceptance_criteria` / `context_to_load` / `out_of_scope` populated mechanically by plan-build, copied verbatim into `current-task.yaml`, enforced by implement-leaf via Refusal H + new "Contract enforcement" section.
- (C) Scope-expansion HALT — new `build-blocked.yaml` template + `scope-expansion-halt.md` reference; orchestrator routes auto-amend (within `build.auto_amend.max_auto_amendments`, default 1) or escalates with `target_layer` derived from `suggested_resolution`.
- (D) Per-gate progress checkpoint — new `build-progress.yaml` overwrite-on-update journal across 11 gates; orchestrator resume logic chooses silent-recover / resume-at-gate / restart; new implement-leaf "Resume mode" alongside greenfield/fix.
- (E) Per-task workers wrapped as agents — three thin dispatch shells under `.claude/agents/`; `orchestrate-build` dispatches via Task tool for true within-stage parallelism and isolated context windows; `retrospect-build` stays a Skill invocation.

*TARGET_ARCHITECTURE §11 + §16 updated;* CLAUDE.md Build Flow section gained "Per-task worker agents" paragraph.

*Skills-architecture.html rewritten* (2026-05-10) — covers spec flow + build flow + handovers + 3 user workflows (greenfield, update, retrofit).

*vmodel-core dogfooding pilot* — artifacts migrated to new schema; `.vmodel/` scaffolded; pilot continues.

**Remaining in Phase 6:**

- **Cluster 5 — no-fabrication extensions.** Tighten retrofit honesty in author skills based on dogfooding signal. Pending pilot reps.
- **Cluster 6 — process / UX (minus Issue 9, folded into Cluster 4).** Quality-of-life improvements surfaced from pilot reps. Open.
- **Cluster 7 — Root-product parity (needs.md / product_description.md).** Until 2026-05-10 the framework treated PB as a first-class root product but `needs.md` and `product_description.md` were second-class — schemas, Quality Bars, and HTML craft pages existed only for PB. The 2026-05-10 audit + wording-fix pass propagated three-option treatment across skills and references; the structural artifacts below remain. Per-item:
  - [ ] **Schema** `schemas/artifacts/needs.schema.json` — derived from elicit-needs output shape; inherit envelope; mark `recovery_status` permitted. Source: existing `vmodel-core` `needs.md` + `vmodel-skill-elicit-needs/templates/`.
  - [ ] **Schema** `schemas/artifacts/product-description.schema.json` — five mandatory sections (Product / Users / Smallest worthwhile slice / Out of scope / Open questions) per `vmodel-skill-elicit-pd/SKILL.md`.
  - [ ] **Quality Bar** `schemas/artifacts/quality-bar/needs.quality-bar.json`.
  - [ ] **Quality Bar** `schemas/artifacts/quality-bar/product-description.quality-bar.json`.
  - [ ] **Craft page** `docs/guide/artifacts/needs.html` — 5-section structure (V-model context, best practices, anti-patterns, examples, Quality Bar). Sources: elicit-needs SKILL.md + `archive/phase4/PHASE4_AUTHORING_PATTERN.md` + INCOSE Needs vs Requirements distinction.
  - [ ] **Craft page** `docs/guide/artifacts/product-description.html` — 5-section structure. Source: elicit-pd SKILL.md + the PD draft preserved at `docs/plan/phase4-tool-briefs/core/product_description.md`.
  - [ ] **Author / review skill pair decision per type** — currently `elicit-needs` and `elicit-pd` produce these artifacts. Decide whether each also needs an `author-{needs,pd}` + `review-{needs,pd}` pair (revision flow) or whether re-invoking the elicit skill is sufficient. Tied to decision γ (elicit-needs promotion).
  - [ ] **Fixtures** under `schemas/artifacts/fixtures/` — round-trip examples for both new artifact types (matches the PB fixture pattern).
  - **Note.** The 2026-05-10 wording-fix pass is recorded under §1 active deliverables. The audit found 16 wording edits across 8 files (skills + references); structural files above remain pending.
- **Candidate-set propagation walker** (`TARGET_ARCHITECTURE §8.3`) — **DONE (2026-05-10)**. `scripts/walk-impact.py` + 22-test TDD suite. CLI shape: `walk-impact.py <ID> --specs-root specs/ --format text|json`. Reads `derived_from`, `parent_architecture`, `governing_adrs`, `verifies` (envelope + per-case), `allocates` (per-child).
- **Haiku-floor evaluation per skill** — deferred from Phase 5; rerun once pilot signal reveals real failure modes.
- **PB author/review pair decision** — promote, merge into needs/PD, or stay deferred. Tied to elicit-needs decision γ. Folded into Cluster 7 above.

**Closeout signal:** vmodel-core pilot completes a forward-run end-to-end without manual intervention beyond design review.

### 3.6.1 Phase 6 next-session prep — vmodel-core leaf TestSpec authoring

**Trigger.** This subsection is the session-start brief for the next conversation. The pilot has its first leaf DD (`DD-embedded-resources`, 2026-05-11); the natural next authoring step is the **sibling leaf TestSpec** that closes the V-pair for `embedded-resources`. This is also the first leaf-TestSpec rep in dogfooding — Issue 24 (typed-error coverage script's leaf-deferral pattern) surfaces precisely here.

**Load at session start (in this order):**

1. `CLAUDE.md` (auto-loaded — framework root).
2. `docs/plan/BACKLOG.md` §1 + §3.6 + §3.6.1 (this subsection).
3. `docs/plan/TARGET_ARCHITECTURE.md` §5.3 (TestSpec shape) + §5.6 (review handover) + §16 (build flow).
4. `MEMORY.md` (auto-loaded).
5. `pilots/vmodel-core/CLAUDE.md` — pilot working-context + current-state pointer.
6. `pilots/vmodel-core/specs/embedded-resources/detailed_design.md` — the DD the TestSpec verifies.
7. `pilots/vmodel-core/specs/architecture.md` + `pilots/vmodel-core/specs/architecture/interfaces/IFrameworkResources.md` — DD's upstream.
8. `pilots/vmodel-core/dogfood_findings.md` Issue 24 (leaf-testspec deferral pattern) + Issue 25 (six-vs-seven schemas, gates `validation-engine` but **not** this TestSpec).

**Working directory for next session.** `pilots/vmodel-core/` (inside this framework repo). The framework repo is both reference and workspace; the pilot is a subdirectory.

**Concrete next-session deliverable.**

Invoke `/vmodel-skill-author-testspec` for the `embedded-resources` leaf. Output: `pilots/vmodel-core/specs/embedded-resources/testspec.md`. Cases derived from `DD-embedded-resources` per the leaf-layer convention (`verifies` targets DD entries — Public Interface clauses, Data Structure invariants, error-matrix row). The DD's Notes section already lists the cue set: contract test per accessor; robustness test for `ErrUnknownArtifactType`; property test on byte-identity across calls; property test on `VersionManifest` non-empty fields; thread-safety property test.

Expected signal during this session:

- Closes Issue 24's noisy finding on `IFrameworkResources.ErrUnknownArtifactType` (leaf coverage finally exists).
- First exercise of the leaf-TestSpec author skill in dogfooding — surfaces shape gaps if any.
- Confirms whether Issue 27's session-cost pattern repeats at TestSpec scope (likely smaller — less upstream to load).
- Issue 28 fix (pre-built schema-validation script) likely worth doing *before or after* this session — author can flag the call.

**What is *not* in scope for next session:**

- Resolving Issue 25 (six-vs-seven schemas) — gates `DD-validation-engine`, **not** this TestSpec.
- `DD-validation-engine` authoring — comes after Issue 25 resolution.
- `plan-build` / `orchestrate-build` runs — wait until at least one V-pair exists end-to-end.
- Cluster 7 needs/PD structural artifacts — pilot signal still inconclusive.

**Open question entering the session.** Whether to take Issue 28 (pre-built schema-validation script) before TestSpec authoring or after. Doing it before amortises the validation cost across the next session. Doing it after preserves the V-pair completion as a focused deliverable. Stakeholder call.

### 3.7 Phase 7 — Retrofit-specific Additions — PENDING

**Goal:** Specialised retrofit capabilities beyond the generic Spec-workflow-reversed flow.

**Tasks:**
- [ ] **Topology discovery tool** — code → scope tree proposal (dependency analysis, package boundaries, bounded-context detection). Algorithm choice is itself a Phase 7 decision; pilot-driven.
- [ ] **Recovery-status enforcement** — strengthen skill-level refusal of fabrication on human-only fields based on retrofit-pilot signal.
- [ ] **Gap report aggregator** — compile the six gap categories from `TARGET_ARCHITECTURE §8.2` into a single retrofit deliverable.
- [ ] **Dedicated retrofit author skill** — code-structure analysis, behaviour characterisation, requirement inference, design inference, gap analysis, cross-session handoff for large analyses. Per-artifact skills already encode retrofit honesty; this lifts recurring patterns.
- [ ] **Purpose-built tools** (`vmodel-core`, `vmodel-author`, `vmodel-retrofit`) — productise the mechanical checks once pilot signal indicates which deserve productisation.
- [ ] **Legacy pilot** — Java 17 / Gradle / JUnit 5 / ~100k LOC / ~10% coverage codebase retrofitted into a scope tree + DDs + Architectures + Requirements + gap report — without AI-fabricated rationale.

**Dependencies:** Phase 6 dogfooding signal. Specifically: vmodel-core greenfield pilot completes end-to-end, surfacing what actually deserves retrofit-specific support vs what the per-artifact skills already cover.

**Deferred companion deliverables** (out of Phase 7 critical path):
- Web GUI for traceability (after framework stabilises).
- Plan schemas (development plan, verification plan, CM plan, QA plan).

---

## 4. Deferred / Parked

Items explicitly out of current phasing:

- **Human guards** — to revisit if uniform high rigor proves insufficient. (`TARGET_ARCHITECTURE §17 #2`)
- **Rigor tiers** — may return if human guards require them; not before. (`TARGET_ARCHITECTURE §17 #1`)
- **Web GUI for traceability** — after the framework stabilises.
- **Plan schemas** — development plan, verification plan, CM plan, QA plan.
- **C2–C4 detailed-design skills** — superseded by Phase 5 structure; not returning.
- **System test documentation + skills as separate artifacts** — folded into TestSpec at root scope.
- **Review Record schema** as a separate artifact — deferred until a concrete need surfaces.
- **Safety-level / assurance-level configuration** — removed by pivot; preserved in archive.
- **Scaffold tool concept as a standalone design** — absorbed into the scaffolder in Tools (`TARGET_ARCHITECTURE §10`).
- **Domain translation plugin** — JSON files archived; runtime removed; possible reintroduction post-content-stabilisation. (`TARGET_ARCHITECTURE §14`, §17 #7)
- **Product-Brief author/review pair** — deferred indefinitely; revisit alongside elicit-needs decision γ.

---

## 5. Operational Open Questions

Questions tied to upcoming phases. Architectural open questions live in `TARGET_ARCHITECTURE §17`.

1. **Topology discovery algorithm choice.** Dependency analysis vs package boundaries vs bounded-context detection. Phase 7 decision; pilot-driven.
2. **Scaffolder CLI shape.** Exact commands and options for the scaffolder tool. Phase 7 (folded into purpose-built-tools track).
3. **Project config evolution.** `.vmodel/config.yaml` schema is in place; extensions (per-tool config sub-schemas, per-skill overrides) drop in as needed.
4. **Legacy pilot start date.** When to attempt a pilot retrofit (Java 17 / Gradle / JUnit 5 / ~100k LOC / ~10% coverage). Depends on Phase 7 being at least partially operational.
5. **elicit-needs promotion** (decision γ). After pilot reps: promote `needs.md` to a 7th artifact, merge into Product Brief, or keep as transient elicitation output. Resolution informs whether the deferred PB skill pair is needed.
6. **Retrofit completeness threshold.** How many `unknown` fields make a retrofit "not useful" vs "partial but usable"? No principled answer today; real retrofit runs will inform.

**Resolved:**
- ~~Quality Bar container format.~~ JSON Schema draft 2020-12; `schemas/artifacts/quality-bar/` layout (resolved 2026-04-23).
- ~~Dogfooding kickoff order.~~ `vmodel-core` is the pattern-setter pilot (resolved 2026-04-23).
- ~~Candidate-set propagation walker design.~~ BFS reverse over forward-link graph; pure tool (no LLM); shipped as `scripts/walk-impact.py` (resolved 2026-05-10).
- ~~Three-root-artifact treatment.~~ PB / `needs.md` / `product_description.md` are first-class options; framework-wide wording propagated 2026-05-10. Structural artifacts (schemas, Quality Bars, craft pages) for needs/PD remain — see §3.6 Cluster 7.

---

## 6. Guiding Principles (cross-reference)

The ten core principles are defined in `TARGET_ARCHITECTURE §3`. This list is a quick index; the canonical wording is there.

1. Documentation is the foundation.
2. Spec Ambiguity Test.
3. Uniform high rigor (no tiers).
4. Workflow decoupling.
5. Tool/skill split.
6. Tools as independent products.
7. Retrofit no-fabrication.
8. Human leverage at the spec level.
9. Components are independent (SOLID).
10. Tests derive from the layer's artifact.

**Additional operational principles** (not duplicated in `TARGET_ARCHITECTURE`):

- **Discuss before writing.** Explain approach, show structure visually, motivate choices, get approval.
- **Small increments.** One concept at a time.
- **Dispatch concrete execution to subagents** — keep main conversation focused on design and alignment.
- **Skill invocations are tool calls, not references.** When the user types `/skill-name`, invoke via the `Skill` tool first; project conventions layer on top of the skill's mandatory flow, do not replace it.
- **Skill design is model-tier-aware.** Skills must work on the cheapest viable tier. Validation pending Phase 5 closeout (Haiku-floor evals deferred to post-pilot).

---

## 7. Build Order (summary)

```
Phase 0 (done) → Phase 1 (done) → Phase 2 (done) → Phase 3 (done)
                                                        │
                                       ┌────────────────┴────────────────┐
                                       ▼                                 ▼
                                  Phase 4 (closed                  Phase 5 (effective
                                  without producing PDs)            complete; closeout
                                       │                            deferred to pilot)
                                       └────────────────┬────────────────┘
                                                        ▼
                                            Phase 6 — Build flow +
                                            central config +
                                            greenfield pilot
                                            (substantially advanced; rolling)
                                                        │
                                                        ▼ (gated on pilot signal)
                                            Phase 7 — Retrofit additions
                                                       + purpose-built tools
                                                       (pending)
```

**Critical path:** 0 → 1 → 2 → 3 → 5 → 6 → 7. Phase 4 closed without producing its original deliverable; the work was rerouted into Phase 5 as `vmodel-skill-elicit-needs`. Phase 6 absorbed the original "Tools (purpose-built)" plan and replaced it with build-flow + central config + dogfooding; tools moved into Phase 7 alongside the retrofit additions.

---

*Last updated: 2026-05-10 (continued) — added §3.6 Cluster 7 (root-product parity tasks for needs.md / product_description.md) reflecting the same-day audit + 16 wording-fix edits across 8 skill files; added §3.6.1 next-session brief for vmodel-core greenfield dogfooding pickup; marked candidate-set propagation walker DONE (scripts/walk-impact.py + 22-test TDD suite); marked three-root-artifact treatment resolved. Earlier same-day: full BACKLOG reformat reflecting build-flow shipment and central-config landing. Phase 6 absorbed the original "Tools (purpose-built)" plan; tools moved into Phase 7. Phase 5 closeout tightened. Skills-architecture.html rewrite marked DONE.*
