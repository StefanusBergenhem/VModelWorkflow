# vmodel-core (pilot)

Greenfield dogfooding pilot for the V-model framework. Daily-driver tool per framework `docs/plan/TARGET_ARCHITECTURE.md §10` — artifact parser, schema validator, traceability validator, Quality Bar runner, graph builder, query engine, scaffolder, renderer.

## Repo relationship

Bundled at `pilots/vmodel-core/` inside the framework repo (2026-05-10) for tight dogfood feedback. Schema, skill, and pilot fixes resolve in one branch.

- **Skills.** Resolved from the framework's `.claude/skills/` at the repo root. No project-local mirror.
- **Shared references.** `.vmodel/references/` for skill use; refreshed via `/vmodel-init migrate` after framework changes.
- **Framework canonical sources.** `references/schemas/` and `references/framework/{TARGET_ARCHITECTURE,BACKLOG}.md` are **symlinks** to the framework's `schemas/` and `docs/plan/`. Drift-proof.
- **Graduation back to standalone.** `git filter-repo --subdirectory-filter pilots/vmodel-core` (symlinks will need to be re-pathed).

## Repo layout

```
pilots/vmodel-core/
├── .vmodel/                config + .vmodel/references/ + defer-index + .reviews/ + .build/
├── seed/                   phase-4 PD (historical input cited from needs.md)
├── references/
│   ├── schemas → ../../schemas                    (symlink)
│   ├── framework/
│   │   ├── TARGET_ARCHITECTURE.md → ../../../../docs/plan/TARGET_ARCHITECTURE.md
│   │   └── BACKLOG.md             → ../../../../docs/plan/BACKLOG.md
│   └── codex/              frozen citation snapshot (not living)
├── specs/                  needs, requirements, architecture (+ interfaces/), testspec, adrs/
├── dogfood_findings.md     living: framework gaps surfaced during pilot
├── archive/session-log.md  per-session authoring + review history
├── CLAUDE.md
└── .gitignore
```

## Current state

- Root-scope `needs.md`, `requirements.md` (REQ-001..REQ-032), `architecture.md` (7 children, 8 interfaces, hexagonal pipeline composition), `testspec.md`, ADR-001 (Go) and ADR-002 (compile-time embed.FS) authored and approved.
- No DD yet. Next planned authoring: a leaf DD — `embedded-resources` (simplest) or `validation-engine` (most load-bearing). `cli-adapter` DD is gated on REQ-024 follow-up.
- Pre-existing authoring issues (mechanical-check sweep): see `archive/session-log.md` 2026-05-10 entry.

For prior session history, see `archive/session-log.md`.

## Working process

Framework `CLAUDE.md` (at repo root) governs. Pilot-specific layer-ons:

- Discuss before writing — show structure, motivate choices, get approval.
- Skill invocations are tool calls, not references — invoke via the `Skill` tool; do not pattern-match.

## Pilot purpose

1. Drive Phase 6 build-flow design via real authoring + review reps.
2. Inform Phase 7 retrofit design.
3. Surface framework gaps fast — fix in `.claude/skills/`, `schemas/`, `scripts/`, or `references/` directly.
4. Resolve elicit-needs decision γ (promote / merge / stay-transient).

Document pilot learnings in `dogfood_findings.md`.
