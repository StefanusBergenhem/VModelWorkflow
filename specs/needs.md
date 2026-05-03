---
artifact_type: needs
scope: vmodel-core
status: prototype-mode
elicitation_session_id: 2026-05-01-vmodel-core-pilot-session-1
stakeholder: Stefanus Ivarsson Bergenhem (framework author, dogfooding pilot)
date: 2026-05-01
---

# Needs — vmodel-core

<!-- Stakeholder voice. No design language. Each entry has a confirmation token traced to a session readback turn. -->

## Intent

This document captures the integrated set of stakeholder needs for **vmodel-core** — the deterministic CLI that validates VModelWorkflow spec artifacts and reports on spec-tree state. The primary stakeholder for v1 is the framework author (in dogfooding role) plus the Phase 5 AI skill framework being built around VModelWorkflow; the primary user class is AI agents, with CI pipelines and direct human callers as secondary and tertiary. Functional scope at v1 covers **validation** (mechanical schema / traceability / Quality Bar checks producing structured findings and a single overall verdict) and **reporting** (coverage, completeness, inventory, and impact analysis over the derived traceability graph). The document deliberately leaves specific numerical targets, scale ceilings, and most CLI ergonomic shape unset — those are deferred to pilot evidence rather than pre-committed in seed material.

*Confirmed: yes (readback turn 12, 2026-05-01).*

## Stakeholders

- **Framework author (in dogfooding role) plus the Phase 5 AI skill framework being built around VModelWorkflow** — v1 *primary stakeholder*. The tool succeeds at v1 when it's usable for the framework author's own workflow and reliably callable as a subprocess by the Phase 5 skills. *Confirmed: yes (readback turn 1, 2026-05-01).*
- **Open-source adopter community (engineers / organisations who would adopt VModelWorkflow externally)** — explicitly *deferred to v1.x or v2*. v1 design decisions are not constrained by this group's preferences. *Confirmed: yes (readback turn 1, 2026-05-01).*
- **AI-agent callers** (the Phase 5 skills primarily; and any other AI-agent harness invoking vmodel-core as a subprocess if that emerges) — v1 *primary user class*. When caller-class needs conflict on an interface decision, the AI agent's needs come first. *Confirmed: yes (readback turn 1, 2026-05-01).*
- **CI pipelines** (build / commit / pre-merge gates invoking vmodel-core as a step) — v1 *secondary user class*. *Confirmed: yes (readback turn 1, 2026-05-01).*
- **Direct human callers** (engineers running vmodel-core in a terminal during local authoring or investigation) — v1 *tertiary user class*. *Confirmed: yes (readback turn 1, 2026-05-01).*

## Needs

<!--
Functional needs are organised into two user-facing clusters: Validation and Reporting.
(Initial three-cluster cut in session 1 included a separate Querying cluster; folded in
readback turn 7 — impact analysis moved to Reporting; per-artifact graph navigation
dropped as not justifying a standalone capability.) Parse and Build-graph (PD §2) are
plumbing under both and not user-facing capabilities themselves.
-->

### Functional needs

#### Validation

- **Validation has five call sites at v1, with distinct concerns at each.**
  - **Author skill** — validates the artifact it just wrote, inside its retry loop.
  - **Review skill** — validates an artifact to ground its mechanical-violation findings (schema / traceability / Quality Bar) before layering craft judgement on top.
  - **Orchestrator** — validates the full spec tree at phase boundaries to gate progression.
  - **CI pipeline** — validates the full spec tree as a pre-merge or pre-commit gate.
  - **Direct human caller** — validates one artifact, one scope, or the full tree ad-hoc during local authoring or investigation.

  *Confirmed: yes (readback turn 3, 2026-05-01).*

- **A validation finding carries five dimensions of information sufficient for an AI caller to act on it:**
  - **Locate** — which artifact, and where inside the artifact the violation is.
  - **Identify** — *which specific rule* was broken, distinguishable from every other rule (so the AI caller can branch deterministically on rule identity).
  - **Triage** — how serious the violation is (blocks progression / merge, warn-only, informational).
  - **Summarise** — a human-readable message the consumer can fold into its own output (e.g. review verdict, retry log, orchestrator phase report, PR comment, terminal display).
  - **Related artifacts** — for cross-artifact violations (broken `derived_from` link, missing allocation, missing `verifies` target), the other artifacts involved beyond the primary location.

  Other callers (CI, direct human) consume the same five dimensions through different renderings appropriate to their interface.

  **The fixability of any given finding is the consuming AI caller's concern, not vmodel-core's.** vmodel-core states *what* is wrong; the AI caller decides *what to do about it*.

  *Confirmed: yes (readback turn 4, 2026-05-01).*

- **Validation produces a single overall verdict per run, with three possible values:**
  - **pass** — no blocking findings.
  - **fail** — at least one blocking finding (per the Triage dimension).
  - **system-error** — vmodel-core could not complete the run (e.g. file IO failure, parse crash, internal error). Distinct from `fail` because the verdict is not authoritative when the tool itself did not complete.

  Rule-class taxonomy (schema / traceability / Quality Bar) is *not* aggregated into the verdict — it lives in the per-finding `Identify` dimension. AI callers branch on findings; CI and direct human callers gate on the verdict and consult findings for detail.

  *Confirmed: yes (readback turn 5, 2026-05-01).*

#### Reporting

- **Reporting produces summaries of spec-tree state for consumers seeking understanding of where the work stands — distinct from validation, which produces verdicts and findings for callers about to act.**

  Three properties distinguish reporting from validation:
  - **Consumer.** Primarily a human reading for understanding (e.g. an architect surveying scope-tree health, a leadership reader looking at progress).
  - **Cadence.** Point-in-time snapshot, taken on demand, not part of a per-run workflow gate.
  - **Content.** Includes derived aggregates and inventory over the graph, not just per-rule findings.

  Starting v1 scope (four output types):
  - **Coverage percentages** — what proportion of artifacts of one type satisfy a relationship to another. *Example: percentage of requirements with at least one `verifies` link.*
  - **Completeness aggregates** — counts and ratios of rule-conformance across the tree. *Example: number of requirements missing a specified Quality Bar criterion.*
  - **Inventory** — counts of artifacts by type and scope. *Example: 47 requirements, 12 architecture elements, 3 ADRs in the tree.*
  - **Impact analysis** — for a proposed change to a given artifact, the set of other artifacts that may need to be reviewed or updated as a result. *Example: for a proposed change to requirement R, the architecture elements that allocate from R, the test specs that verify R, and the child requirements that derive from R.*

  *Confirmed: yes (readback turn 6, 2026-05-01; revised in turn 7 — swapped batch-query renderings for impact analysis as part of the Querying-cluster fold).*

### Quality needs

- **Performance must be fast enough not to block its primary workflows. Specific latency targets are deliberately left unset at v1 to avoid prematurely narrowing technology selection; numbers will be set from pilot evidence, not pre-committed in seed material.**

  The AI-caller author retry loop (write → validate → fix → retry, multiple iterations per artifact) is the most latency-sensitive workflow and the one expected to drive future calibration.

  *Confirmed: yes (readback turn 8, 2026-05-01).*

- **v1 scale baseline: small spec trees in the low hundreds of artifacts (the framework author's own projects during pilot).** Headroom for larger trees in future versions is desirable; specific scale ceilings are deliberately left unset at v1 to avoid prematurely ruling out larger adopter trees in v1.x or v2.

  *Confirmed: yes (readback turn 8, 2026-05-01).*

- **Worst-case target hardware: a commodity CI runner.** The tool must run within typical CI-runner resource bounds for all v1 capabilities; developer laptops and AI-agent containers are not the design target.

  *Confirmed: yes (readback turn 8, 2026-05-01).*

- **Partial-failure behaviour: halt-and-report.** When vmodel-core encounters a system-level failure during a multi-artifact operation (e.g. unparseable artifact, unreadable file, corrupted schema input) it halts the run and reports system-error. The remaining artifacts are not evaluated. The AI caller does not have to disambiguate "this artifact has findings" from "this artifact couldn't be evaluated" — system-error and findings live on different tracks.

  *Confirmed: yes (readback turn 11, 2026-05-01).*

### Constraints

- **No LLM in the runtime path.** vmodel-core is mechanical and deterministic; any capability requiring interpretation belongs in a Phase 5 skill, not in this tool. Framework-principle-grounded (`TARGET §3`).

  *Confirmed: yes (readback turn 9, 2026-05-01).*

- **Operational simplicity: each run is independent, with no install/configure overhead and no operational state carried between invocations.** The tool must be runnable as-is in CI with no setup, no daemon to manage, no shared mutable state to coordinate. *How* this is realised (e.g. pure statelessness vs an auto-managed daemon mode in v1.x) is a downstream choice — the stakeholder constraint is operational independence per run.

  *Confirmed: yes (readback turn 9, 2026-05-01).*

- **Read-only on the adopter's spec tree.** vmodel-core never writes, renames, or deletes spec artifacts. Reports about artifacts go to stdout/stderr only. Spec-side mutations belong to `vmodel-author` per the framework's tool/skill/sibling-product split.

  *Confirmed: yes (readback turn 9, 2026-05-01).*

- **Install experience: an adopter must be able to download a single artifact and run it on Linux, macOS, or Windows with no separate runtime install** (no JVM, no Python interpreter, no Node, no shared-library prerequisites beyond what the OS provides natively). *How* this is realised (statically-linkable compiled binary, single-file bundled interpreter, or other) is a downstream choice — the stakeholder constraint is download-and-run with no prerequisites beyond the OS.

  *Confirmed: yes (readback turn 9, 2026-05-01).*

- **Update mechanism: re-download and replace in place.** No update daemon, no in-place auto-updater, no package-manager dependency. The adopter downloads a new version of the same single-artifact binary and replaces the old one. Mirrors the install-experience constraint for symmetry.

  *Confirmed: yes (readback turn 11, 2026-05-01).*

- **External (non-sibling) callers integrate via the CLI as a stable contract.** Phase 5 skills, CI pipelines, and direct human callers invoke as subprocess and consume the CLI's output; they do not depend on language bindings or in-process library access. Sibling tools (`vmodel-author`, `vmodel-retrofit`) MAY library-link or invoke as subprocess per each sibling's ADR — orthogonal to the external-caller constraint.

  *Confirmed: yes (readback turn 9, 2026-05-01).*

- **No relaxation modes.** No per-adopter `--lenient` flag, no rigor-tier configuration. Uniform high rigor is enforced by absence of opt-out: if rigor is not needed, the framework is not the right tool. Framework-principle-grounded (`TARGET §3 #3`).

  *Confirmed: yes (readback turn 9, 2026-05-01).*

- **Open-source distribution.** vmodel-core ships as open source. Specific licence is deferred to product ADR.

  *Confirmed: yes (readback turn 9, 2026-05-01).*

### Interfaces / integrations

- **Validation verdict exit-code rendering** (for shell-driven consumers — CI gates, direct human terminal use):
  - `0` — pass.
  - `1` — fail.
  - `2` — system-error.

  Sysexits-style. Renders the verdict shape confirmed in turn 5.

  *Confirmed: yes (readback turn 10, 2026-05-01).*

- **Output formats:**
  - **Validation:** produces JSON (default for AI callers, machine-parseable) and text (default for human / CI terminal consumption, human-readable).
  - **Reporting:** produces HTML (self-contained, browseable, aligned with the "human seeking understanding" consumer per turn 6).

  Whether reporting also produces JSON / text variants is deferred to Open gaps.

  *Confirmed: yes (readback turn 10, 2026-05-01).*

## Open gaps

- **CLI ergonomic shape beyond exit codes and output formats — pending pilot evidence and codex pattern hardening.** PD §3 *CLI ergonomics* enumerates a set of working hypotheses (verb/subcommand structure, errors-are-actionable, non-interactive-by-default, idempotency, stdin acceptance, progressive `--help`, structured-data-on-success, `--yes`/`--force` flags, structured stderr logs, `--verbose`/`--quiet`). PD itself flags these as drawn from a single practitioner observation (Zakariasson 2026) and explicitly working-hypothesis-status pending corroboration. Not promoted to Interfaces / integrations at v1; revisit once pilot evidence and `pat-cli-design-for-ai-agents` codex pattern page are in place.

- **Reporting output formats beyond HTML.** Whether the four reporting output types (coverage / completeness / inventory / impact) also need JSON variants (for programmatic dashboard ingestion) or text variants (for terminal viewing) is unconfirmed. PD §3 implies all three formats for gap-report; the stakeholder-anchored v1 answer is HTML-only unless probed and confirmed otherwise.

## Success metrics

- **Success metrics deliberately unset at v1.** Specific metrics for vmodel-core's production success will be set from pilot evidence (framework author's own dogfooding, Phase 5 skill usage data, CI integration signal) rather than pre-committed. Consistent with the broader shape-not-numbers stance from Quality needs.

  *Confirmed: yes (readback turn 11, 2026-05-01).*

## Session notes

- **Session 1 (2026-05-01).** Input shape: draft document (`seed/product_description.md`). Stakeholder reachable; readback handshake live.
- **Output placement.** `specs/needs.md`, per stakeholder call (2026-05-01). See `issues_found.md` Issue 1 for the framework gap that motivated the explicit decision.
- **Cluster cut revision (turn 7, 2026-05-01).** Original three-cluster cut (Validation / Querying / Reporting, confirmed turn 2) collapsed to two clusters (Validation / Reporting). Rationale: stakeholder articulated only two underlying needs — impact analysis and tree/gap overview. Impact analysis fits Reporting (snapshot view of affected closure). Tree/gap overview already covered by coverage / completeness / inventory. Forward graph navigation (what-verifies / what-allocates) dropped — caller can read linked artifact directly; transitive forward closure is rare; doesn't justify standalone capability. May revisit if AI-caller need surfaces in pilot.
- **PD §3 specific numbers not promoted (turn 8, 2026-05-01).** PD §3 carries specific performance targets (single-artifact p95 < 1s; ~100-artifact tree p95 < 5s; heavy-query single-digit seconds), specific scale numbers (~1,000 baseline, ~5,000 reopen-daemon threshold), and "developer-grade hardware" target. Stakeholder explicitly declined to commit specific numbers in needs.md to avoid narrowing technology selection prematurely. PD §3 numbers carried forward as architect-side aspirational targets only — into Architecture or pilot calibration, not into needs.md.
- **Gap-finding sweep (turn 11, 2026-05-01).** Six gap-finding categories swept this session:
  - Interfaces — covered (turn 10).
  - Non-functional requirements — covered as Quality needs (turn 8).
  - Constraints — covered (turn 9).
  - Exception flows — partial-failure behaviour committed (turn 11, halt-and-report).
  - Success metrics — deferred at v1 with explicit "unset until pilot evidence" entry (turn 11).
  - Ops / lifecycle — install + update committed (turns 9, 11). Version-skew with framework: considered, dropped per stakeholder call (will revisit if a need surfaces). Retirement: not-relevant at v1. Monitoring: not-relevant at v1 (stateless / ephemeral runtime; nothing to monitor).
