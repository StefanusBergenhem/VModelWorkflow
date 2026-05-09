# Checkpoint flow — vmodel-init

Five interactive batches. At each checkpoint the skill presents detected or
default values, explains what breaks if wrong, and asks for confirmation.

The user can type **`skip`** or **`auto`** at any checkpoint to apply defaults
silently for all remaining checkpoints.

---

## General checkpoint protocol

At each batch:

1. Show what was detected or generated (present the relevant config section).
2. Explain why it matters — one sentence on what degrades if wrong.
3. Suggest improvements when values can be inferred from project analysis.
4. Ask for confirmation before writing.

When suggesting values, always show:
- The detected evidence (e.g., "found `pom.xml`")
- The suggested value (e.g., `test_unit: "mvn test"`)
- Why it matters (e.g., "without this the build flow cannot run tests")

---

## Checkpoint 1 — Project identity

**What to present:**

```
Project name:   <directory-name>          (detected from directory)
Language:       <detected-language>       (detected from marker files)
Description:    (empty)                   (optional)
```

**Why it matters:** Project name appears in artifact IDs and trace references.
Language drives command suggestions and component-override defaults. Getting
this wrong means stale suggestions in later checkpoints.

**Question prompts:**

- "Project name? [default: `<dir-name>`]"
- "Primary language? [default: `<detected>`] — override if wrong."
- "One-line description? [default: empty — optional]"

---

## Checkpoint 2 — Paths

**What to present:**

```
scope_root:   specs/      (root of spec directory tree)
src:          (empty)     (source root — only needed for build flow)
tests:        (empty)     (test root  — only needed for build flow)
```

**Why it matters:** `scope_root` is where every spec artifact lives.
Getting this wrong means the author/review skills cannot resolve artifact
paths. `src` and `tests` are only needed if the build-flow skills are
activated — leave empty for spec-only projects.

**Question prompts:**

- "Scope root? [default: `specs/`]"
- "Source directory? [default: empty — fill if using build-flow skills]"
- "Tests directory? [default: empty — fill if using build-flow skills]"

---

## Checkpoint 3 — Root product type

**What to present:**

| Key    | File                       | When to use                                           |
|--------|----------------------------|-------------------------------------------------------|
| `pd`   | `product_description.md`   | Lightweight — one page, top-level context (default)   |
| `needs`| `needs.md`                 | Mid-weight — interview-derived stakeholder needs      |
| `pb`   | `product_brief.md`         | Heavyweight — full product brief with rationale       |

**Why it matters:** The root product type determines which authoring skill to
run first and what the root artifact is named. The wrong type leads to
mismatched skill invocations.

**Recommended default:** `pd` for new projects without existing stakeholder
material. Use `needs` when running `/vmodel-skill-elicit-needs` to start.
Use `pb` when a full product brief is already required by stakeholders.

**Question prompt:**

- "Root product type? (pd / needs / pb) [default: pd]"

---

## Checkpoint 4 — Commands

**What to present:** Suggested commands based on detected language (see
`language-detection.md` for per-language defaults). For each field show
evidence + suggestion.

Fields:

| Field              | Description                              |
|--------------------|------------------------------------------|
| `test_unit`        | Run unit tests (exit 0 = pass)           |
| `test_integration` | Run integration tests (optional)        |
| `test_system`      | Run system / acceptance tests (optional) |
| `lint`             | Linter / static analysis                 |
| `build`            | Build / compile                          |
| `coverage`         | Coverage report                          |

**Why it matters:** Build-flow skills read these commands to execute the
test/lint/build loop. Unconfigured fields are skipped — the build flow will
warn but won't fail. Empty string means "not configured."

**No-fabrication rule:** If language detection fails or no default exists
for a field, leave it as `""`. Do not guess.

**Suggestion presentation example:**

```
Detected: pom.xml at project root → java

Suggested commands:
  test_unit:        "mvn test"          (standard Maven test lifecycle)
  test_integration: ""                  (not auto-detected — fill if needed)
  test_system:      ""                  (not auto-detected — fill if needed)
  lint:             ""                  (not auto-detected — configure checkstyle/pmd if used)
  build:            "mvn package"       (standard Maven package lifecycle)
  coverage:         ""                  (not auto-detected — configure jacoco if used)

Review and adjust, or press enter to accept all.
```

**Question prompt:**

- "Review command suggestions. Adjust any field, or press enter to accept."

---

## Checkpoint 5 — Build flow

**What to present:**

```
build.parallel.enabled:          true
build.parallel.max_concurrent:   4
build.retry.max_review_attempts: 3
build.models.plan:               opus
build.models.implement:          sonnet
build.models.review:             sonnet
build.models.retrospect:         sonnet
```

**Why it matters:** These control parallelism and model assignment in the
build-flow skills. Wrong values waste tokens (model too expensive for
mechanical tasks) or slow execution (max_concurrent too low for your machine).

**Guidance:**
- Reduce `max_concurrent` if your machine is resource-constrained.
- Use `opus` for `plan` (DAG derivation requires reasoning); `sonnet` is
  sufficient for implement / review / retrospect (mechanical tasks).
- Reduce `max_review_attempts` only if you want faster escalation to human.

**Question prompt:**

- "Accept build-flow defaults, or adjust any values? [default: accept]"

---

## Final summary checkpoint

After all writes are complete, print a compact one-screen summary (see
SKILL.md Step 13 for exact format). Ask: "Anything to change before we
finish?" Apply any last adjustments, then print next-step suggestions.
