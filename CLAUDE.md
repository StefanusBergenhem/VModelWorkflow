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

**2026-05-01 — Repo bootstrapped.** 11 vmodel skills copied into `.claude/skills/`; phase-4 PD copied into `seed/`; framework reference documents (TARGET_ARCHITECTURE, BACKLOG, schemas, Zakariasson codex source) copied into `references/`. No specs authored yet. Build workflow not designed yet (deferred at framework level).

**Next session:** elicit-needs run with the user as stakeholder, producing `needs.md` for `vmodel-core` scope. The phase-4 PD (`seed/product_description.md`) is the seed input — it represents prior thinking on `vmodel-core` and is the artefact the elicit-needs skill should refine and surface gaps against. This run is also the first decision γ data point for elicit-needs `needs.md` lifecycle (promote / merge / stay-transient).

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
