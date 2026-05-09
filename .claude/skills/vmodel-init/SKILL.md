---
name: vmodel-init
description: >
  Initialize the V-model workflow scaffolding in a target project. Creates
  `.vmodel/` directory with config.yaml, references/ (copied from framework
  defaults), .reviews/, .build/, and defer-index.md placeholder. Detects
  language and suggests commands. Interactive checkpoints with skip/auto.
  Migrate mode upgrades existing `.vmodel/` non-destructively. Use when
  bootstrapping a new project to use V-model skills, or when upgrading a
  project's `.vmodel/` after framework changes. Triggers — init vmodel
  project, scaffold .vmodel directory, set up vmodel workflow, migrate
  vmodel project.
type: skill
---

# vmodel-init

Initialize or upgrade V-model workflow scaffolding in a target project.

The skill is self-contained. All checkpoint flows, language detection tables,
migrate logic, and config/defer-index templates live in this directory.
No external lookups needed during execution.

## When to use

Activate this skill when the user asks to:

- Set up V-model workflow in a new or empty project
- Scaffold `.vmodel/` for the first time
- Upgrade an existing `.vmodel/` after framework changes
- Understand what `.vmodel/` directories and files mean

## Mode detection (Step 0)

Before anything else, check whether `.vmodel/config.yaml` already exists at
the target project root.

- **Absent** — run Standard Init.
- **Present** — prompt: "`.vmodel/config.yaml` already exists. Run migrate to
  non-destructively upgrade, or abort? (migrate / abort)". On `abort`, stop.

If the user supplies `migrate` in the invocation string, skip the prompt and
proceed directly to Migrate mode.

---

## Standard Init

### Step 1 — Language detection

Read `references/language-detection.md`. Scan the project root for the marker
files listed there. Record detected language and set default command
suggestions accordingly.

### Step 2 — Checkpoint 1: Project identity [CHECKPOINT]

Present detected values. Ask:

- Project name (default: directory name)
- Language (default: detected; offer to override)
- Description (default: empty — optional)

Show: "These go into `.vmodel/config.yaml` and appear in artifact IDs and
trace references."

Accept `skip` or `auto` at any checkpoint — apply defaults silently for all
remaining checkpoints.

### Step 3 — Checkpoint 2: Paths [CHECKPOINT]

Present defaults:

```
scope_root:  specs/
src:         (empty — fill if build flow is used)
tests:       (empty — fill if build flow is used)
```

Explain: "`scope_root` is the root of your spec directory tree. `src` and
`tests` are only needed if you activate the build-flow skills."

Ask: "Confirm these paths, or adjust?"

### Step 4 — Checkpoint 3: Root product type [CHECKPOINT]

Present the three options with one-line descriptions:

| Key | File | When to use |
|-----|------|-------------|
| `pd` | `product_description.md` | Lightweight — one page, top-level context (default) |
| `needs` | `needs.md` | Mid-weight — interview-derived stakeholder needs |
| `pb` | `product_brief.md` | Heavyweight — full product brief with rationale |

Ask: "Which root product type? (pd / needs / pb) [default: pd]"

### Step 5 — Checkpoint 4: Commands [CHECKPOINT]

Present detected command suggestions (from `references/language-detection.md`
for the detected language). For each field show the suggested value and the
evidence that drove it.

Fields: `test_unit`, `test_integration`, `test_system`, `lint`, `build`,
`coverage`.

Rule: if language detection fails or no default exists for a field, leave
the field as `""` — never guess.

Ask: "Review command suggestions. Adjust any, or press enter to accept all."

### Step 6 — Checkpoint 5: Build flow [CHECKPOINT]

Present defaults for build-flow tuning:

```
build.parallel.enabled:          true
build.parallel.max_concurrent:   4
build.retry.max_review_attempts: 3
build.models.plan:               opus
build.models.implement:          sonnet
build.models.review:             sonnet
build.models.retrospect:         sonnet
```

Explain: "These control parallel task execution and model assignment in the
build-flow skills. Leave defaults unless you know you need different values."

Ask: "Accept build-flow defaults, or adjust any?"

### Step 7 — Write `.vmodel/config.yaml`

Fill `templates/config.yaml.tmpl` with values from checkpoints 1–5.
Write to `.vmodel/config.yaml`.

### Step 8 — Copy framework references

Determine framework root (see "Framework root resolution" below).

Run:
```
cp -r <framework-root>/references/* .vmodel/references/
```

This copies:
- `authoring-discipline.md`
- `authoring-self-check.md`
- `partial-parent-protocol.md`
- `requirements-shape-checklist.md`
- `definitions/component.md`
- `definitions/unit.md`

### Step 9 — Create empty directories

Create:
- `.vmodel/.reviews/`
- `.vmodel/.build/`

(Place a `.gitkeep` in each so empty dirs are tracked if the project uses git.)

### Step 10 — Write `defer-index.md`

Write `.vmodel/defer-index.md` from `templates/defer-index.md.tmpl`.

### Step 11 — Update `.gitignore`

Append idempotently — do not re-add lines already present. If `.gitignore`
does not exist, create it.

Append:
```
# vmodel transient build state
.vmodel/.build/pipeline-state.yaml
.vmodel/.build/runs/
.vmodel/.build/tasks/*/log.txt
```

### Step 12 — Stub root product file

Create `<scope_root>/<product_file>` (e.g., `specs/product_description.md`)
as an empty file with a title comment:
```markdown
# <project-name> — <product_type_label>

<!-- stub: run the appropriate vmodel elicit / author skill to fill this in -->
```

Do not overwrite if the file already exists.

### Step 13 — Summary [CHECKPOINT]

Print a compact summary of what was written:

```
=== vmodel-init complete ===

  Project:     <name> (<language>)
  Scope root:  <scope_root>
  Root product: <type> → <scope_root>/<file>
  References:  .vmodel/references/ (<N> files copied)
  Config:      .vmodel/config.yaml
  Defer index: .vmodel/defer-index.md
  .gitignore:  <N lines appended / already present>

Suggested next steps:
  - Run /vmodel-skill-elicit-needs  (if starting from stakeholder interview notes)
  - Run /vmodel-skill-author-requirements  (if you have upstream needs already)
  - Run /vmodel-skill-author-architecture  (after requirements are approved)
```

---

## Migrate mode

See `references/migrate-mode.md` for the full migrate flow and drift-handling
protocol.

---

## Framework root resolution

The skill needs to know where the framework's `references/` directory lives
to copy defaults into the project. Resolution order:

1. **Bundled path file** — Check `references/framework-defaults-path.md` in
   this skill's own directory. If it contains an absolute path, use it.
2. **Checkpoint fallback** — If no bundled path or the path doesn't resolve,
   add a question to Checkpoint 1: "Where is the VModelWorkflow framework
   installed? (e.g., `/home/user/repos/VModelWorkflow`)"

The bundled path file is the preferred mechanism. It is written at framework
install time and updated if the framework moves. Projects that received their
`.vmodel/references/` copy don't need this — it is only consulted at init time.
