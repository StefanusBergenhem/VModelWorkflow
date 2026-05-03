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

This repo is **separate** from the framework repo at `/home/stefanus/repos/VModelWorkflow/`. The framework is read-only from this repo's perspective. Skills are bundled, not symlinked — that's the self-containment test.

If a skill bug surfaces during the pilot, the fix goes to the framework repo first, then re-copies into this repo. No cross-repo edits.

## Status

**2026-05-01 — Repo bootstrapped.** 11 vmodel skills copied into `.claude/skills/`; phase-4 PD copied into `seed/`; framework reference documents (TARGET_ARCHITECTURE, BACKLOG, schemas, Zakariasson codex source) copied into `references/`.

**2026-05-01 — `specs/needs.md` authored** (elicit-needs session 1, see `issues_found.md` 2026-05-01 entries for framework gaps surfaced).

**2026-05-03 — `specs/requirements.md` authored** (vmodel-skill-author-requirements run; `status: draft`). Adversarial review by `vmodel-skill-review-requirements` returned APPROVED on second pass after one revision cycle. Document is at root scope (`scope: ""`); ~30 atomic requirements across functional / quality-attribute / interface / data sections; 12 inherited constraints; full glossary; explicit *Open gaps* section with named owners and actions. Framework gaps surfaced this session are appended to `issues_found.md` (2026-05-03 entries).

**2026-05-03 (later) — Two foundational ADRs authored and accepted.** **ADR-001** (`specs/adrs/adr-001-implement-vmodel-core-in-go.md`) commits Go as implementation language (drivers: AI-coding-agent corpus density, YAML 1.2 ecosystem maturity via `goccy/go-yaml`, stdlib HTML templating). **ADR-002** (`specs/adrs/adr-002-embed-canonical-schemas-in-binary.md`) commits compile-time `embed.FS` for the framework canonical rule catalog / schema set / Quality Bar checklist set, with no runtime override (drivers: IC-007 no-relaxation, IC-002 stateless cold-start, IC-005 re-download-and-replace update). Both adversarially reviewed by `vmodel-skill-review-adr`; APPROVED on second pass after one revision cycle (ADR-001's Alternatives section was restructured to surface ≥2 real rejected entries — Rust, Zig, C++, Java/.NET-with-AOT — rather than dismiss four candidates inline in Context). Propagation added four derived requirements to `specs/requirements.md` (REQ-029 output stability; REQ-030 schema-version pinning; REQ-031 no-external-schema-access; REQ-032 version queryability); requirements doc re-reviewed by `vmodel-skill-review-requirements` and APPROVED on second pass (REQ-029 had implementation-prescription rewritten to state byte-identical-output property only; REQ-030 was split into atomic statements with EARS conformance, with REQ-032 created from the split). `specs/requirements.md` now carries 32 atomic requirements (REQ-001..REQ-032). Framework gap surfaced this session: `issues_found.md` Issue 11 (ADR and architecture author skills materialise new requirements without invoking the requirements-author skill's discipline).

**Next session:** likely candidates, in priority order — (a) architecture authoring at root scope (`vmodel-skill-author-architecture`) — `requirements.md` is at REQ-001..REQ-032 with two foundational ADRs (ADR-001 Go, ADR-002 schema embedding) accepted; pending items (NFR target numbers, deprecation-policy ADR, licence ADR) do not block architectural decomposition; (b) framework-level (VModelWorkflow-scope) elicitation pass to address `issues_found.md` Issue 2 (no parent-scope upstream); (c) author a vmodel-core Product Brief to retire the `[NEEDS-vmodel-core]` placeholder per `issues_found.md` Issue 1 / decision γ. Choose at session start.

## Repo layout

```
vmodel-core/
├── .claude/skills/             (11 vmodel skills — drop-in, framework-neutral)
├── seed/
│   └── product_description.md  (phase-4 PD — seed input for elicit-needs)
├── references/
│   ├── framework/
│   │   ├── TARGET_ARCHITECTURE.md  (PD §6 cites §3, §5, §6, §7, §8.3, §10)
│   │   └── BACKLOG.md              (PD §6 cites §6 Q4)
│   ├── schemas/                    (full schemas tree — vmodel-core's runtime input data)
│   └── codex/
│       └── src-zakariasson-clis-for-agents-2026.md  (CLI-for-AI rationale)
├── specs/
│   ├── needs.md                (root-scope stakeholder needs; elicit-needs output)
│   ├── requirements.md         (root-scope requirements; status: draft; REQ-001..REQ-032)
│   └── adrs/                   (architecture decision records; flat layout, scope_tags-keyed)
│       ├── adr-001-implement-vmodel-core-in-go.md
│       └── adr-002-embed-canonical-schemas-in-binary.md
├── issues_found.md             (living: framework gaps surfaced during pilot)
├── CLAUDE.md
└── .gitignore
```

## Skills available

```
.claude/skills/
├── vmodel-skill-elicit-needs               (root-scope upstream; produces needs.md)
├── vmodel-skill-author-requirements    + review
├── vmodel-skill-author-architecture    + review
├── vmodel-skill-author-detailed-design + review
├── vmodel-skill-author-testspec        + review
└── vmodel-skill-author-adr             + review
```

Pre-pivot operational craft skills (`develop-code`, `derive-test-cases`, `vmodel-skill-review-code`) are **not** copied here yet — they come into play when Build workflow design happens (a later session).

## Working process

Same discipline as the framework repo:
- Discuss before writing — show structure, motivate choices, get approval.
- Skill invocations are tool calls, not references — when invoking a skill, call the `Skill` tool, do not pattern-match.
- The bundled vmodel-skill-* are project-local, framework-neutral, and self-contained. Treat them as drop-in capabilities, not framework references.

## Pilot purpose

This pilot generates the empirical signal needed to:
1. Close out Phase 5 deferred items (Haiku evals, skills-architecture rewrite, framework-skill necessity reassessment).
2. Inform Phase 7 retrofit design.
3. Validate that the skills are actually self-contained (fresh repo proves the bundled-content claim).
4. Resolve elicit-needs decision γ (promote / merge / stay-transient).

Document pilot learnings in this file or a dedicated `PILOT_NOTES.md` as they emerge.
