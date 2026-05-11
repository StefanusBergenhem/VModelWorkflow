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
- First leaf DD landed: `DD-embedded-resources` (2026-05-11) at `specs/embedded-resources/detailed_design.md`. Authored via `/vmodel-skill-author-detailed-design`. Six-accessor typed shell over `embed.FS`, stateless, one error code (`ErrUnknownArtifactType`), bundle-layout pinned, decode posture left to implementer. Front-matter + embedded YAML blocks schema-valid. Surfaced four new dogfood findings (Issues 25–28). Sibling TestSpec not yet authored.
- Next planned authoring: leaf TestSpec for `embedded-resources` (closes the typed-error-coverage finding from Issue 24, completes the leaf's V-pair, gives the first leaf-TestSpec dogfood rep). After that: `validation-engine` DD (most load-bearing). `cli-adapter` DD still gated on REQ-024 follow-up.
- **Open framework decision pre-blocking further DDs touching validation surfaces:** Issue 25 — `ArtifactType` enum membership (six per REQ-016 vs seven schemas published). Resolve at framework scope before authoring `DD-validation-engine`.
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
