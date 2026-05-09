---
purpose: Phase 6 dogfooding findings from vmodel-core pilot, organised by cluster, with recommended decision order.
audience: framework maintainer
status: living
source: dogfood_issues_found.md (raw issues, in date order)
---

# Phase 6 dogfooding findings — vmodel-core pilot

Source: `dogfood_issues_found.md` (vmodel-core, sessions 2026-05-01 → 2026-05-04). 23 issues. This doc reframes the raw list by cluster + decision priority. Read this first; consult the source for issue-level detail.

---

## Headline

The framework concept is holding up. None of the 23 issues say the artifact model, scope tree, V-model layering, or Spec Ambiguity Test is wrong. They are sharp-edge gaps in skill execution and convention specification — exactly what first-real-use dogfooding is meant to surface.

The single dealbreaker is Cluster 1. Everything else is incremental.

---

## Session log

- **2026-05-04 — opened doc, attacked Cluster 1 (Issue 22).**
  - Authored `docs/authoring-discipline.md` (6 cross-cutting rules: product-shape, boundary-only, small-system collapse, rationale-as-citation, diagram-or-prose, cite-don't-restate).
  - Embedded as verbatim per-skill copy at `references/authoring-discipline.md` in all 10 affected skills (5 author + 5 review for the 6-artifact set, excl. product-brief). Sync script at `scripts/sync-authoring-discipline.sh` (idempotent, fails-loud, md5-verified across 21 paths).
  - Validated via re-author of `vmodel-core/specs/architecture.md`: **−46% prose** (10,239 → 5,561 words), no architectural loss, all 32 REQs / 9 ICs / 2 ADRs preserved. Markers `NEEDS-ADR-CONSIDER` introduced during validation, then folded into existing `NEEDS-ADR` (per stakeholder call: no new middle-step markers; the ADR review process is the gate).
  - Issue 24 candidate (negative-space content) **resolved** — folded into Rule 0 of the discipline.
  - Discipline pass took the architecture artifact as far as prose discipline can go. Remaining ~7,200 tokens sit mostly inside YAML DbC blocks (preconditions, postconditions, invariants, errors) — Rule 1 protects them. **Two structural moves required to fully close Issue 22, deferred to next session** (see Cluster 1 below).

---

## Cluster 1 — Existential (decide first)

**Issue 22 — Token budget per session caps adopter tier.** Status: **partially closed (2026-05-04).**

`architecture.md` reached ~30k tokens; a single author session burned 250–300k; review burned ~100k. The discipline pass on 2026-05-04 brought the architecture artifact to ~7,200 tokens (−46% on prose). Adopter-tier viability for full pipeline workloads still requires two structural moves:

1. **YAML DbC block factoring.** ~3,500 of the post-discipline 5,561 words sit inside boundary YAML. Rule 1 (boundary-only) protects them. The lever is structural — factor shared invariants and shared error enums into a single block per scope, with per-interface entries citing the shared definitions. Open design questions: where do shared blocks live, what's the citation syntax, schema validation impact, review-skill enforcement impact.
2. **Scope-shape template variants.** The "Honest departure from template" pattern existed in the original artifact because the architecture template is one-size-fits-all. CLI tools, libraries, and services have genuinely different concern sets; defending absences in the artifact is a workaround for a missing template variant. Open design: introduce `kind: architecture-cli` / `architecture-service` / `architecture-library` variants, each with concern-set-specific templates. Author skill needs to pick the right variant based on declared `kind:`.

**Both deferred to the next session.** Continuation point picks up here with option (b) per session-end agreement (2026-05-04).

**Decision shape.** Architectural — affects template, schema, and author/review skill pair behaviour. Larger than the discipline pass; likely two design discussions before any file-writing.

---

## Cluster 2 — Foundational decisions (decide before more skill work)

Small-text issues with big-implication ripples. Don't let skill-level cleanup begin until these settle.

**Issue 13 — File-based review handover.** **RESOLVED 2026-05-05.** Pinned in TARGET_ARCHITECTURE §5.6. See "Issue 13 closure" below.

**Issue 23 — What does testspec verify (architecture vs requirements).** **RESOLVED 2026-05-05** — Position C pinned in TARGET_ARCHITECTURE §5.3. See "Issue 23 closure" below.

---

## Cluster 3 — Missing author-time gate (split: 3a + 3b — RESOLVED 2026-05-09)

The original framing of "5 issues, 1 structural fix" turned out to be wrong on inspection. The five issues share a *symptom* (review catches what author emits) but not a *root cause*. Re-split into:

- **3a — Issue 11** — genuine cross-skill: ADR/architecture authors emit requirement-shaped content without requirements-skill discipline. **Resolution:** verbatim-copy `docs/requirements-shape-checklist.md` into author-adr and author-architecture via `scripts/sync-requirements-shape-checklist.sh` (matches Issue-22 sync precedent). Author skills invoke the checklist at the propagation/decomposition seam.
- **3b — Issues 15 / 16 / 20 / 21** — per-skill author-discipline gaps with mechanically-detectable failure modes. **Resolution:** generic *Pre-publish mechanical self-check* terminal step pattern across all five author skills (see `docs/authoring-self-check.md`) + skill-specific scripts (see below) + matching review-side `check.*` IDs (belt-and-braces).

The structural decision is the **Pre-publish mechanical self-check** pattern. Each author skill terminates with a step inserted between *Anti-pattern self-check* and *Quality Bar checklist + Spec Ambiguity Test* that runs zero or more skill-specific scripts under `scripts/check-*.py`. Stable contract: `<file>:<line>:<rule-id>:<message>`; exit 0/1/2.

### Mechanical scripts (Python 3, venv, pyyaml)

| Script | Issue | Detects |
|---|---|---|
| `scripts/check-mermaid.py` | 15 | `;` in sequence-message text, unquoted `<…>` placeholders, unquoted aliases with `/` `:` `,` |
| `scripts/check-adr-landing.py` | 16 | bindings declared in an ADR's `propagation.bindings:` YAML appearing outside `rationale` of the matching architecture child |
| `scripts/check-typed-error-coverage.py` | 20 | parent-architecture interfaces' `errors:` enum entries with no covering testspec case |
| `scripts/check-implicit-verifies.py` | 21 | upstream-id mentions (REQ-, IC-, ADR-, ARCH.) in case `preconditions` / `expected` text not listed in `verifies:` |
| `scripts/check-requirement-shape.py` | 11 | atomicity (compound `shall`/`must`), EARS opener, implementation-prescription vocabulary heuristic |
| `scripts/sync-requirements-shape-checklist.sh` | 11 | distributes `docs/requirements-shape-checklist.md` into author-adr + author-architecture (framework + vmodel-core mirror); md5 verify |

Shared parser at `scripts/lib/spec_parser.py` (front-matter, YAML blocks, Mermaid blocks).

### Review-side `check.*` IDs added (belt-and-braces)

| Skill | New check ID(s) | Pairs with script |
|---|---|---|
| review-architecture | `check.responsibility.adr-bound-mechanism-leaked`, `check.mermaid.parser-breaking-chars` | `check-adr-landing.py`, `check-mermaid.py` |
| review-detailed-design | `check.mermaid.parser-breaking-chars` | `check-mermaid.py` |
| review-testspec | `check.verifies.implicit-reference-uncited`, widened `check.derivation.error-path-uncovered` (enumerate every uncovered code) | `check-implicit-verifies.py`, `check-typed-error-coverage.py` |
| review-requirements / review-adr | none added — existing checks (`check.ears.compound-too-many-keywords`, `check.ears.invalid-pattern`, `anti-pattern.implementation-prescription`) already cover the surface caught by `check-requirement-shape.py` |

### Author-side skill changes

All 5 author SKILL.md files received an inserted **Pre-publish mechanical self-check** step (renumbered subsequent steps; QB step moved by +1):

- `author-requirements` → +Step 9
- `author-adr` → +Step 11; Step 8 (Propagation) extended for requirements-shape checklist invocation (route a) and `propagation.bindings:` structured YAML; new template `propagation-bindings.yaml.tmpl`
- `author-architecture` → +Step 13; Steps 1+2 extended for requirements-shape and ADR-binding-landing rule; new reference `adr-propagation-landing-rules.md`; comment blocks added to `decomposition-entry.yaml.tmpl` and the Mermaid templates
- `author-testspec` → +Step 11; Step 6 extended with implicit-verifies and typed-error-enum coverage cues; appended to `verifies-traceability.md` and `architecture-traceability-cues.md`
- `author-detailed-design` → +Step 13; Mermaid comment block added to `state-machine.mmd.tmpl`

### Validation against vmodel-core (2026-05-09)

Scripts run cleanly (no exit-2 errors) on `/home/stefanus/repos/vmodel-core/specs/`. Findings reproduce historical Cluster 3 issues:

| Script | Exit | Findings | Notes |
|---|---:|---:|---|
| `check-mermaid.py` | 1 | 1 | Issue 15 reproduction (architecture.md:336 — `;` in sequence message text) |
| `check-adr-landing.py` | 0 | 0 | Clean — ADR-001 has not yet adopted the new structured `propagation.bindings:` YAML; vacuous-clean is the correct script behaviour |
| `check-typed-error-coverage.py` | 1 | 12 | Issue 20 reproduction — 12 typed errors across 8 interfaces lack covering testspec cases |
| `check-implicit-verifies.py` | 1 | 6 | Issue 21 reproduction — TC-017/023/026 mention IC-002/011/012 + REQ-022 in prose without listing in `verifies:` |
| `check-requirement-shape.py` | 1 | 3 | REQ-001/026/027 fail EARS opener regex |

These 22 findings are now a backlog for the vmodel-core spec author to triage — not a Cluster 3 deliverable, but the empirical signal that the scripts work.

### Known follow-ups (not blocking)

- **EARS regex strictness.** `check-requirement-shape.py` requires `^The` for Ubiquitous. REQ-026/027 use `^A` (`A finding-record shall...`); arguably-conformant variant under indefinite-article subjects. One-line fix: broaden Ubiquitous to `^(?:The|A|An)`. Tracked for next pass.
- **vmodel-core skill mirror.** Author/review SKILL.md changes were applied only to the framework `.claude/skills/`. The vmodel-core mirror at `/home/stefanus/repos/vmodel-core/.claude/skills/` was not updated — there is no skill-bundle sync script for SKILL.md (only for the canonical reference docs). Either author one or copy on demand.
- **`check-adr-landing.py` positive path uncovered.** No vmodel-core ADR yet declares `propagation.bindings:` YAML. The script's negative-finding path is unexercised on real input. A synthetic fixture would prove correctness; deferred until first ADR adopts the structured form.
- **`docs/guide/` ripple.** None this round — Cluster 3 changes are skill-internal and script-level. Re-evaluate at the next `skills-architecture.html` rewrite (deferred per Phase 5 closeout).

---

## Cluster 4 — Convention pin-downs in TARGET_ARCHITECTURE — RESOLVED 2026-05-09

Six issues, all mechanical, all batched. **Issue 9 (Cluster 6) folded in** during Issue 18 resolution since they share a single rule shape (full-absence vs. partial-absence of canonical upstream).

| # | Issue | Pin-down | Where it landed |
|---|---|---|---|
| 1  | `needs.md` placement + parent-dir creation rule | Already pinned framework-side in TARGET §5.4/§5.5 (prior cluster). Skill-side: deterministic path = `<specs-root>/needs.md`; `mkdir -p` of immediate parent permitted; `{output-path}` placeholder dropped. | `vmodel-skill-elicit-needs/SKILL.md` (framework + mirror) |
| 6  | `governing_decisions` → `governing_adrs` | Renamed in `requirements.md.tmpl` (framework + mirror); residual prose mentions in `vmodel-skill-review-requirements/references/rationale-and-traceability-checks.md` and `vmodel-skill-author-requirements/examples/good-session-service.md` (framework + mirror) also fixed. New `scripts/check-template-schema-fields.py` catches future regressions via an extensible `DEPRECATED_NAMES` table. | 5 author template trees + 4 prose files + new script |
| 12 | Mandatory `## Open follow-ups` section + cross-tree index | Closing paragraph added to TARGET §5.3 mandating the section across non-Product-Brief artifacts. Section appended to architecture / detailed-design / testspec / ADR templates (requirements already had it organically). New `scripts/index-deferred-items.py` aggregates `[DEFER-DD: ...]` / `[DEFER-ADR: ...]` markers + Open follow-ups bullets across the tree (informational, exit 0 always). | TARGET §5.3 + 4 author templates × 2 + new script |
| 14 | Tree-global glossary as non-artifact reference doc | `glossary.md` added to TARGET §5.4 directory tree (root only, optional) + §5.5 canonical-filenames table + §5.5 reserved-names list (`glossary` reserved). New "Tree-global reference documents" paragraph clarifies non-artifact status (no Quality Bar, no review skill, no schema, no `derived_from`). Term-registration discipline left to author-skill discretion at this stage; promotion to artifact deferred. | TARGET §5.4 + §5.5 |
| 17 | Empty-scope ID encoding | New "Empty-scope ID encoding" subsection in TARGET §5.4 pinning bare-prefix canonical (`TS`, `ARCH`, `REQS`, `PB`), single-hyphen per-element ids (`TC-NNN`, `REQ-NNN`), and bare-prefix dotted-path refs (`ARCH.interfaces.X`). Test-case ID format aligned to template-side `TC-{scope}-{seq}`. Testspec templates updated with `<<scope-suffix?>>` conditional placeholder + leading rule comment block. Worked empty-scope examples added to 4 traceability-cues references. New `scripts/check-id-encoding.py` flags malformed forms (`TS-`, `TC--NNN`, `ARCH-.interfaces.X`); wired into Pre-publish self-check across all 5 author skills. | TARGET §5.4 + 5 testspec templates × 2 + 4 references × 2 + new script + 5 SKILL.md × 2 |
| 18 + 9 | Partial-parent / no-canonical-upstream protocol | New TARGET §5.7 architectural pin defining three permitted paths (HALT / next-best with documented deviation / framework-reference upstream). Canonical operational text at `docs/partial-parent-protocol.md` distributed verbatim to 5 author skills' `references/` (framework + mirror = 10 paths) by `scripts/sync-partial-parent-protocol.sh` (md5-verified). Each author SKILL.md gains an Inputs bullet, a new `Step 0.5 — Canonical-upstream check (every run)` between Cluster 2's revision-only Step 0 and existing Step 1, a Pre-publish self-check verification line, and a Pointers entry. Issue 9 (full absence) covered by the same rule. | TARGET §5.7 + canonical doc + sync script + 5 SKILL.md × 2 |

### Mechanical scripts and sync infrastructure (Cluster 4)

| Script / artifact | Issue | Role | Wired |
|---|---|---|---|
| `docs/partial-parent-protocol.md` | 18 + 9 | canonical operational text (skill self-contained at runtime) | distributed by sync, not gated |
| `scripts/sync-partial-parent-protocol.sh` | 18 + 9 | md5-verified verbatim copy to 5 author skills × 2 roots | one-shot at framework maintenance |
| `scripts/check-template-schema-fields.py` | 6 | regression detector via `DEPRECATED_NAMES` table | sync-time / CI maintenance, NOT in Pre-publish |
| `scripts/check-id-encoding.py` | 17 | malformed-empty-scope-id detector across spec tree | wired into Pre-publish self-check (all 5 author skills) |
| `scripts/index-deferred-items.py` | 12 | informational cross-artifact pending-items index | NOT a gate; cited from each SKILL.md Pointers section |

### Validation against vmodel-core (2026-05-09)

| Script | Exit | Findings | Notes |
|---|---:|---:|---|
| `check-id-encoding.py` | 1 | 3 | Issue 17 reproduction — `requirements.md:593` (`REQS-`), `testspec.md:707` (`ARCH-.` and `ARCH-`) |
| `index-deferred-items.py` | 0 | 21 markers + 24 follow-ups | Informational; 5 artifacts with pending items |
| `check-template-schema-fields.py` | 0 | 0 | Clean post-rename, framework + mirror |

Cluster 3 scripts re-run on vmodel-core/specs/ after Cluster 4 work — **no regressions**:

| Script | Exit | Findings | vs. historical |
|---|---:|---:|---|
| `check-mermaid.py` | 1 | 1 | matches |
| `check-adr-landing.py` | 0 | 0 | matches (vacuous-clean) |
| `check-typed-error-coverage.py` | 1 | 12 | matches |
| `check-implicit-verifies.py` | 1 | 6 | matches |
| `check-requirement-shape.py` | 0 | 0 | delta from 3 — accounted for by EARS regex broadening (`^(?:The\|A\|An)`) noted as Cluster 3 follow-up |

### Known follow-ups (not blocking)

- **A3 runtime-config option (deferred to separate session).** Issue 18 surfaced a stronger long-term pattern than the Cluster 1/2 sync — a project-level config file (similar to `wf-command-init`) that vmodel-core skills probe at runtime, with init-on-absent semantics. Resolves drift AND enables per-project tuning. Not appropriate for Cluster 4 (cross-cutting architectural change); flag for its own design discussion.
- **Schema-side gaps surfaced by Issue 6 audit (advisory).** Issue 6 subagent's broader template/schema cross-check enumerated divergences not in scope this cluster: envelope-required `version` missing from every author template, `coverage_mutation_bar` not declared in test-spec schema, `type` discriminator missing from `$defs/requirement`, interface-requirement five-dimension shape unmodelled in requirements schema, several DD `$defs` gaps (`invariants` cross-field, shared-mutable-only fields, `rationale_status`), error-matrix conditional fields. These are schema-side improvements, separate cluster — `check-template-schema-fields.py` does NOT flag them today (it uses a narrow deprecated-names table) so they are a backlog for a future schema-tightening pass.
- **`docs/guide/` ripple.** Real this round, not auto-edited:
  - `docs/guide/artifacts/{architecture,detailed-design,testspec,adr}.html` — should describe the mandatory `## Open follow-ups` section.
  - `docs/guide/artifacts/{testspec,architecture,requirements}.html` — root-scope examples should match the empty-scope rule (TS/ARCH/REQS bare prefix, TC-NNN at root).
  - `docs/guide/skills-architecture.html` (deferred per Phase 5 closeout) — natural home for partial-parent-protocol documentation in human-facing guide. Re-evaluate at the next rewrite.
- **vmodel-core skill mirror (Cluster 3 known follow-up still open).** Cluster 4 SKILL.md changes were applied to BOTH framework and mirror this round (sync verified byte-equal across all 10 author SKILL.md files post-cluster). However the underlying Cluster 3 question — "should there be a sync-script for SKILL.md, parallel to the canonical-reference sync scripts?" — remains open. Cluster 4 sidestepped it by manual mirror updates.
- **`scripts/` directory exists only in VModelWorkflow.** Pre-publish step invocations use bare path `scripts/check-*.py`. At runtime in vmodel-core (which has no `scripts/` directory), the invocation requires the agent to resolve to the framework path. Pre-existing convention from Cluster 3 — Cluster 4 inherits but does not introduce. Tracked for the runtime-config / wf-command-init-style discussion above.
- **vmodel-core spec backlog.** The 3 `check-id-encoding.py` findings + 12 typed-error-coverage + 6 implicit-verifies findings on vmodel-core are now a backlog for the spec author to triage. Not a Cluster 4 deliverable, but the empirical signal that the new + existing scripts work.

---

## Cluster 5 — No-fabrication discipline extensions

The discipline is sound for vocabulary; it needs to extend into numbers and standard-convention imports. Each is a small reference addition.

| # | Extension |
|---|---|
| 4  | Premature numerical commitment as design-smuggling |
| 7  | Deferred NFR thresholds (Planguage with `pending — <calibration source>`) |
| 8  | Standard-engineering-convention imports as permissible rationale |
| 19 | Placeholder oracles in testspec (structured `TBD-by-X` distinct from weak assertions) |

---

## Cluster 6 — Process and UX

Skill-flow refinements. Mostly small per-skill updates.

| # | Refinement |
|---|---|
| 2  | Needs elicitation cascade (parent-scope before per-product) |
| 3  | Readback silence after flag = informed agreement |
| 9  | ~~Generalised "no canonical upstream" protocol across all author skills~~ — **folded into Cluster 4 (Issue 18 resolution), 2026-05-09** |
| 10 | Redundant readback during elicitation; consolidate to one final pass |

---

## Recommended decision order

1. **Cluster 1 (Issue 22) — discipline pass DONE 2026-05-04. Structural pass DONE 2026-05-05.**
2. **Cluster 2 (Issues 13, 23) — RESOLVED 2026-05-05.**
3. **Cluster 3 — RESOLVED 2026-05-09 (split: 3a checklist + 3b Pre-publish self-check pattern; 5 scripts; 4 new review check IDs; 1 widened review check).**
4. **Cluster 4 — RESOLVED 2026-05-09 (six issues + Issue 9 folded in; TARGET §5.3 / §5.4 / §5.5 / §5.7 additions; new docs/partial-parent-protocol.md + sync; 3 new scripts; 4 templates × 2; 5 SKILL.md × 2).**
5. **Cluster 5 + 6 (minus Issue 9) — pending.** Mechanical, batchable, low-risk.

---

## Resolved candidate issues

- **Issue 24 candidate (editorial / negative-space content) — RESOLVED 2026-05-04.** Folded into Rule 0 of `docs/authoring-discipline.md` (Product-shape only). Manifests as `n/a + justification`, "Honest departure from template", and *Notes / Self-attestation* sections; review skills will catch via `check.discipline.product-shape` finding.

- **Issue 13 — RESOLVED 2026-05-05 (file-based review handover).** Pinned in `TARGET_ARCHITECTURE §5.6` with a "Review output convention (`specs/.reviews/`)" sub-section:
  - File path: `specs/.reviews/<artifact-id>-YYYY-MM-DD-NN.yaml` (zero-padded 2-digit sequence always present, increments for same-date re-runs).
  - Lifecycle: keep all; latest is lexically last; no `superseded_by` metadata.
  - Cardinality: per-artifact, not global (differs from build-side single-active-task model).
  - Visibility: committed (forensic record), not gitignored.
  - Schema: existing per-skill `templates/verdict.md.tmpl` shape — skills stay self-contained; no central schema.
  - Author consumption: mode B — when revising, always read latest review file if present and address findings (apply / push back / defer).

  Ten skills updated mechanically: 5 review skills (Output section rewritten + 2 self-check bullets appended) + 5 author skills (Inputs bullet + new Step 0 inserted before Step 1). Files touched: `TARGET_ARCHITECTURE.md`, all 10 SKILL.md files under `.claude/skills/vmodel-skill-{author,review}-{requirements,architecture,detailed-design,testspec,adr}/`. Subagent dispatched for the per-skill mechanical pass; spot-checks confirmed correct application across all 10.

  **Outstanding follow-ups:** `docs/guide/skills-architecture.html` rewrite is still deferred per Phase 5 closeout (the natural home for review-handover-protocol documentation in the human-facing guide). Log entry: review handover protocol section needs adding when the skills-architecture page is rewritten.

- **Issue 23 — RESOLVED 2026-05-05 (Position C).** Pinned in `TARGET_ARCHITECTURE §5.3` with a "Verification targets per scope" table:
  - Leaf TestSpec verifies leaf DD only.
  - Branch TestSpec verifies BOTH branch Requirements (behavioural intent) AND branch Architecture (Composition entries + interface DbC clauses).
  - Root TestSpec verifies root Requirements + root Architecture + Product Brief outcomes.
  - Decomposition entries are explicitly NOT verification targets (structural, not behavioural).

  Principle 10 sharpened to plural ("the layer's specs"). Schema descriptions tightened (artifact-level + case-level `verifies`). Author + review skill pairs updated: branch now loads BOTH `architecture-traceability-cues.md` AND `requirements-traceability-cues.md`; root loads both as well; conditional-gating widened so `check.architecture-traceability.*` and `check.requirements-traceability.*` apply at branch AND root. **Docs/guide ripple closed same day:** `docs/guide/artifacts/testspec.html` (lead, Position-on-V, Inputs, Granularity-at-branch, QB checklist), `docs/guide/artifacts/architecture.html` (right-hand-ascent paragraph), `docs/guide/artifacts/requirements.html` (right-hand-ascent paragraph) all rewritten to Position C. Files touched: `TARGET_ARCHITECTURE.md`, `schemas/artifacts/test-spec.schema.json`, `vmodel-skill-author-testspec/SKILL.md` (+ 2 reference head-notes), `vmodel-skill-review-testspec/SKILL.md` (+ 2 reference head-notes), `docs/guide/artifacts/{testspec,architecture,requirements}.html`.

---

## Issues 25 + 26 — surfaced 2026-05-05, resolved by Rules 6 + 7 + 8

**Issue 25 — Marker semantics conflate "artifact missing" with "decision deferred".**
- Surface: `[NEEDS-DD: ...]` markers in vmodel-core's architecture read like a TOC of DDs to write, but every leaf already has a mandatory DD per `TARGET_ARCHITECTURE §5.2`. Some markers also pointed to non-component topics (e.g., build-pipeline release surface) — category errors.
- Resolution: **Rule 6** in `authoring-discipline.md`. Markers renamed `NEEDS-X` → `DEFER-X`. Routing rule: DD for component-internal gaps, ADR for cross-cutting decisions with named alternatives, inline `<TBD>` for parametric gaps, push back if none fit.

**Issue 26 — Cross-cutting non-component decisions had no documented home.**
- Surface: markers like `[NEEDS-DD: build-pipeline release surface]` named topics that aren't leaf components, but the framework had no documented routing.
- Resolution: **Rule 6 routing table.** Three routes: ADR (decision with alternatives) / inline content in existing root-Architecture sections (deployment intent, fitness functions, observability) / `<TBD>` (parametric). No new artifact type; no ADR sub-category.

---

## What to monitor (not yet issues, but watch)

- **Cumulative spec budget per scope.** Architecture is ~30k tokens; DD has not yet been authored. If DD repeats 50%+ of architecture content, the cumulative budget per scope explodes. Validate the architecture/DD layering rule produces clean separation before the first DD is authored.
- **Review-skill judgment-as-precedent.** Issue 19's resolution was reviewer judgment, not written rule. Track how often review verdicts hinge on undocumented reasoning; high rate = framework-rule-deficit signal.
- **Per-artifact defect rate at draft time.** Issue 11 logged 75% defect rate at the propagation interface; Issue 20 logged 50% typed-error coverage at draft. Establish a baseline and watch the trend as author-time gates land.
