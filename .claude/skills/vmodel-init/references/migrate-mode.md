# Migrate mode — vmodel-init

## Purpose

Non-destructive upgrade of an existing `.vmodel/` directory after framework
changes. The migrate flow preserves every project customization; it only adds
missing files and offers to refresh stale reference copies.

Trigger: `.vmodel/config.yaml` already exists when `/vmodel-init` is invoked,
or the user explicitly passes `migrate`.

---

## Non-destructive guarantees

- Never overwrites `config.yaml` values. Missing sections are added with
  defaults; existing entries are left unchanged.
- Never overwrites project-modified reference files without an explicit
  per-file prompt.
- Creates new files before removing any old ones.
- Reports all findings before applying changes.

---

## Step M1 — Read existing config

Read `.vmodel/config.yaml`. Note:
- Which top-level sections are present.
- Any `paths.*` entries that differ from current schema defaults.
- Config format version (if a `schema_version` field exists).

---

## Step M2 — Compare references

For each file in `<framework-root>/references/`:

1. Check whether the file exists in the project's `.vmodel/references/`.
2. If absent in project: mark as **MISSING** — will be added.
3. If present in project: compute a content diff.
   - If identical: mark **OK**.
   - If different: mark **DRIFT** — user will be prompted.

Produce a drift report:

```
=== Reference drift report ===

  authoring-discipline.md          OK
  authoring-self-check.md          DRIFT      (project copy differs from framework)
  partial-parent-protocol.md       OK
  requirements-shape-checklist.md  MISSING
  definitions/component.md         OK
  definitions/unit.md              DRIFT
```

---

## Step M3 — Prompt per-file [CHECKPOINT]

For each **MISSING** file: add it automatically (no prompt needed).

For each **DRIFT** file: show a summary of what changed (first differing
line or a one-sentence description if diff is too long) and ask:

```
authoring-self-check.md has drifted from the framework default.
  Framework version: <first differing line>
  Project version:   <first differing line>

Keep project version, accept framework version, or skip? (keep / accept / skip)
```

- `keep`: leave the project copy unchanged.
- `accept`: overwrite with framework version.
- `skip`: leave unchanged for this session (will appear as DRIFT next migrate run).

Apply choices immediately before moving to the next file.

---

## Step M4 — Config section upgrades [CHECKPOINT]

Compare existing config sections against the current schema
(`vmodel-config.schema.yaml`).

For each section present in the schema but absent from the project config,
show the section content and ask:

```
Adding `build.models` section (absent from your config):
  plan:       "opus"     — Model for plan-build (DAG derivation)
  implement:  "sonnet"   — Model for implement-leaf
  review:     "sonnet"   — Model for review-execution
  retrospect: "sonnet"   — Model for retrospect-build

Accept defaults, or adjust any values? (accept / adjust)
```

On `accept`: append the section to config.
On `adjust`: collect adjusted values, then write.

Do NOT touch existing config entries. Only add missing sections.

---

## Step M5 — .gitignore check

Check that all three transient entries are present in `.gitignore`:

```
.vmodel/.build/pipeline-state.yaml
.vmodel/.build/runs/
.vmodel/.build/tasks/*/log.txt
```

Append any that are missing (idempotent — do not duplicate).

---

## Step M6 — Migration report and summary [CHECKPOINT]

Print a final migration report:

```
=== vmodel-init migrate complete ===

  References updated:
    + requirements-shape-checklist.md  (added — was missing)
    ~ authoring-self-check.md          (accepted framework version)
    ~ definitions/unit.md              (kept project version)
    = authoring-discipline.md          (OK — no change)
    = partial-parent-protocol.md       (OK — no change)
    = definitions/component.md         (OK — no change)

  Config sections added:
    + build.models  (added with defaults)

  .gitignore:
    + 1 entry appended

Next steps:
  - Review .vmodel/config.yaml — new sections added, customize as needed
  - Re-run /vmodel-init migrate after the next framework update
```

---

## Edge cases

**Empty `.vmodel/` directory (config.yaml absent):** Treat as Standard Init,
not migrate. The mode-detection check in SKILL.md Step 0 covers this.

**Framework root not resolvable:** Ask user at M2: "Where is the VModelWorkflow
framework installed? (needed to compare reference files)"

**Config has unknown fields:** Warn but do not remove. Report:
"Found fields in `.vmodel/config.yaml` not in the current schema: [list].
These are not consumed by any vmodel skill. Remove manually if not needed by
other tooling."
