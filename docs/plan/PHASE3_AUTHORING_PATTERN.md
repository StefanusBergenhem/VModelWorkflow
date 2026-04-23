# Phase 3 — Authoring Pattern & Session Handoff

Status document for Phase 3 (schemas). Mirrors the Phase 2 precedent (`PHASE2_AUTHORING_PATTERN.md`, archived on Phase 2 completion). Archive this file on Phase 3 completion.

Load this file at the start of every Phase 3 session.

---

## 1. Status as of 2026-04-23

**Phase 3 work to date (13 commits):**

| Commit | Step | What |
|---|---|---|
| `2993385` | Phase 3 prep | Archive 4 pre-pivot schemas (`sw-architecture`, `sw-requirement`, `system-requirement`, `system-test-case`) + EARS dir. Drop speculative `priority` field from `requirements.html`. |
| `a00181f` | Envelope + shared defs | Author `envelope.schema.json` + `common-defs.schema.json` as JSON Schema draft 2020-12. Archive pre-pivot-tainted `artifact-envelope.schema.yaml`. |
| `7c0dca8` | Authoring pattern | Phase 3 session handoff / authoring pattern doc (this file). |
| `5b84d62` | #5 Product Brief schema | Pattern-setter for per-artifact schemas. Front-matter-only validation; `id` const `"PB"`; `summary` required; `recovery_status: reconstructed` banned at scalar + map levels (human-only artifact). |
| `bf0fb76` | Status-wording sweep | Reconcile PB + Requirements HTML pages to the universal lifecycle enum — `accepted` → `active` in 6 places. ADR page intentionally kept on Nygard convention (see §2 lock below). |
| `7742783` | #6 Requirements schema | Front-matter + `$defs/requirement` for per-req embedded-YAML blocks. Artifact `id` prefix `REQS-`; per-req `id` prefix `REQ-` (do not conflate). `rationale_recovery_status` narrowed to `verified \| unknown` (no-fabrication on human-only rationale). |
| `831bf2d` | Handoff-doc update | Log PB / sweep / Requirements commits; lock ADR status override in §2 Lifecycle; refresh recommended next step. |
| `4a6a4d7` | Envelope status relaxation | Refactor motivated by ADR override need: envelope owns status *shape* (required, non-empty); per-artifact schemas own *vocabulary* (enum). See §2 Vocabulary ownership lock. Touches envelope + PB + Requirements. |
| `0dcba63` | #8 ADR schema | Third per-artifact schema. Nygard status enum override (`proposed \| accepted \| superseded`); `id` requires mandatory kebab slug; `scope_tags` minItems 1; `supersedes` / `superseded_by` tightened to ADR id pattern; `recovery_status` narrowed on four human-only keys (context, alternatives_considered, rationale, consequences). Archive pre-pivot `adr.schema.yaml`. |
| `a392c94` | #7 Architecture schema | Fourth per-artifact schema. `id` pattern `ARCH` / `ARCH-{flattened-scope}`; universal lifecycle vocabulary; `governing_adrs` tightened to ADR id pattern; top-level `recovery_status` left broad (Architecture content is code-observable); `$defs/decomposition_child` (required `id`/`purpose`/`responsibilities`/`allocates`; `allocates` tightened to REQ id pattern; no `maxItems` on `responsibilities` — rigor lives in Quality Bar; `rationale` as `string` OR `{status: verified\|unknown, note}`; per-child `recovery_status` scalar) and `$defs/interface` (required `name`/`from`/`to`/`protocol`/`contract`; contract required `operation`/`preconditions`/`postconditions.on_success`; `errors` shape with kebab `code`, 4xx/5xx `http`, `meaning`; empty `quality_attributes` object rejected). No pre-pivot file to archive — `sw-architecture.schema.yaml` archived in `2993385`. |
| `3854f9e` | #9 Detailed Design schema | Fifth per-artifact schema. `id` pattern `DD-{flattened-scope}-{name}` (no structural scope/name split enforced); universal lifecycle; `parent_architecture` required + tightened to ARCH id pattern; `derived_from` minItems 1; `governing_adrs` tightened to ADR pattern. `recovery_status` scalar broad (DD's dominant content is code-observable); map form narrows `overview` key to `verified\|unknown` (Overview carries intent — human-only under no-fabrication rule), other map keys stay broad. `$defs/public_interface_entry` lifts DbC shape from arch (preconditions / postconditions.on_success\|on_failure / invariants / typed errors) but sub-fields are optional — shape vs completeness split; errors shape lighter than arch's (no http / kebab-code — DD errors describe raise/return, not wire); postcondition split is 2-way (on_success / on_failure — error attribution belongs in the Error Handling matrix, not DbC); `thread_safety` enum of 5 categories including `thread-hostile`. `$defs/data_structure_entry`: required `name` + `fields` (each field required `name` + `type`, optional `invariant`); `ownership` / `lifetime` / `returned_semantics` optional strings. `$defs/error_matrix_row`: 5-col per HTML (`error`/`detection`/`containment`/`recovery`/`caller_receives`); `recovery` closed enum (`fail-fast\|retry\|fallback\|compensate\|propagate`). HTML drift flagged: front-matter example shows `scope_tags` (plural) but TARGET §5.3 specifies singular `scope`+`parent_scope` — schema follows TARGET; HTML sweep deferred to §6. Pre-pivot `detailed-design.schema.yaml` (Layer 1/2/3 model) archived in same commit. |
| `c103964` | #10 TestSpec schema | Sixth and final per-artifact schema. New artifact (no pre-pivot file to archive). Required front-matter: `id`, `artifact_type` (`test-spec`), `scope`, `parent_scope`, `level`, `verifies`, `derived_from`. Load-bearing rule encoded: `verifies` is `minItems 1` at both artifact level and per-case level — first cross-artifact mandatory-link constraint inside a schema. `id` pattern `^TS(-[a-z0-9]+(-[a-z0-9]+)*)*$` (TS at root; TS-{flattened-scope} otherwise). `scope` deliberately nullable (HTML §2.9 specifies `null` at root for both scope and parent_scope — deviates from DD / Architecture `empty-string-is-root via scope_path` precedent). `level` enum `[system, integration, unit]` scope-derived but carried explicitly so downstream tooling does not re-derive. Universal lifecycle vocabulary. `derived_from` array minItems 1 (HTML leaf example shows scalar form; HTML root example shows filenames `[requirements.md, product_brief.md]` — schema requires IDs, both HTML forms flagged as drift). `governing_adrs` optional, tightened to ADR id pattern. `recovery_status` scalar broad; map form unconstrained at artifact level — anti-pattern 13 no-fabrication on per-case `title`/`notes` stays skill-enforced (schemas validate shape, skills validate provenance). `$defs/test_case`: required `id`/`title`/`type`/`verifies` (verifies minItems 1 — the anti-orphan rule); optional `suite`, `preconditions`, `inputs`, `steps`, `expected`, `notes`. Per-case `id` pattern `^TC-[a-z0-9]+(-[a-z0-9]+)*$` — local to parent TestSpec document (not globally qualified as handoff §8 had speculated; HTML uses local form consistently; §8 speculation retracted). `type` closed enum of 11 values per TARGET. `preconditions` / `inputs` / `steps` / `expected` deliberately unconstrained in shape — HTML shows both string-prose and YAML-map forms across layers; Quality Bar asserts shape specificity. Reserved growth fields (`fixtures`, `data`, `expected_range`) pass through via `additionalProperties: true`; canonicalise in later revision when empirical usage settles. HTML drift flagged: `TC-login-R1` (HTML §4 anti-pattern example) uses uppercase `R` — rejected by schema's lowercase kebab pattern. Framework-wide convention is lowercase across every other artifact's ID; `TC-login-R1` is the outlier. Schema holds; HTML example should become `TC-login-r1` in next sweep. |
| `ca07b4b` | #11 Traceability link-types + validation rules | First non per-artifact schema step. Four files under `schemas/traceability/`: `link-types.schema.json` + `link-types.catalog.json` (9 link types — 7 canonical per TARGET §7, 1 reserved `realizes` for Build workflow, `reverse_derived` block with 3 tool-computed inverses at `stored: false` const); `validation-rules.schema.json` + `validation-rules.catalog.json` (13 rules: 2 reference_integrity, 7 completeness, 2 cycle, 1 retrofit, 1 cascade — TRV-QB-001 `deferred_until: phase_3_task_3_and_12`). Catalog-and-schema split (schemas validate data, catalogs carry data) matches Phase 3 JSON-Schema discipline. Locks: target-id patterns deliberately not duplicated in the catalog — per-artifact schemas already enforce source-side ID format; target resolution is a runtime validator concern. severity enum `['error']` only per uniform high rigor; enum form leaves room for warning/info later. Rules overlapping with inline schema enforcement (TRV-COMP-004 non-empty verifies, TRV-RETRO-001 no-fabrication) carry `overlaps_with_schema: true` + note pointing at the enforcing per-artifact schema. Conditional `allOf` branches on `link_type` enforce source_kind/target_kind consistency (source_kind=artifact ↔ source_artifact_types; target_kind=scope forbids target_artifact_types). Rejection-tested 14 + 13 cases. Archived pre-pivot `link-types.yaml` (pre-pivot link names + SWREQ/SYSREQ ids) and `trace.schema.yaml` (pre-pivot separate trace-file + content-hash model; pivot replaced with embedded front-matter links + tool-derived indexes). |

**Pending tasks (Phase 3 backlog):**

| # | Task | Notes |
|---|---|---|
| 3 | Quality Bar YAML container shape | Its own session. Do before #12. |
| 12 | Extract Quality Bar YAML per artifact | Depends on #3. |
| 13 | Minimal-example fixtures per artifact | Depends on all schemas. All six per-artifact schemas + traceability schemas now in place. |

**Pre-pivot-tainted schemas still in place:** none. All pre-pivot artifact schemas archived.

---

## 2. Decisions Locked (do not reopen without cause)

### Format & tooling

- **JSON Schema draft 2020-12.** Not YAML, not custom. Rationale: off-the-shelf validation (ajv, python-jsonschema, santhosh-tekuri/jsonschema for Go) → the future "schema validator" tool (`TARGET_ARCHITECTURE §10`) is a thin CLI wrapper, not a bespoke parser.
- **File extension: `.schema.json`** (pure JSON; broadest tooling compatibility).
- **Commit cadence: one per step.** Matches Phase 2 rhythm.

### Schema identity

- **`$id` form:** `https://vmodelworkflow.dev/schemas/<domain>/<name>/v1`.
  - Placeholder domain (`vmodelworkflow.dev`); not required to resolve today. Gives us a publish path later without rework.
  - Path version (`/v1`) bumps on breaking schema changes.

### Cross-schema references

- Shared `$defs` live in `common-defs.schema.json`. Per-artifact schemas `$ref` by `$id` URI with a fragment pointer (`#/$defs/<def_name>`).
- Per-artifact schemas compose envelope via `allOf`:
  ```json
  {
    "allOf": [
      { "$ref": "https://vmodelworkflow.dev/schemas/artifacts/envelope/v1" },
      { "type": "object",
        "required": ["scope", "parent_scope"],
        "properties": { "...": "per-artifact extras" } }
    ]
  }
  ```

### Universal envelope fields (`envelope.schema.json`)

- **Required:** `id`, `title`, `artifact_type`, `status`, `date`, `version`.
- **Optional:** `recovery_status`, `supersedes`, `superseded_by`.
- `additionalProperties: true` so per-artifact schemas can add fields.

### Lifecycle

- **Universal enum:** `draft | active | superseded`. Default for all artifact types; lives in `common-defs#/$defs/lifecycle_status`.
- **ADR exception — locked 2026-04-22, shipped `0dcba63`.** `adr.schema.json` overrides the universal `status` enum to Nygard's `proposed | accepted | superseded`. Preserved the 15-year ADR community convention rather than force uniformity; one principled exception costs less than fighting reader expectations across every ADR tool and article.
- **NOT `deprecated`** — explicitly rejected. Wrong metaphor for specs (specs are in force or not; they don't fade).

### Vocabulary ownership — locked 2026-04-22, shipped `4a6a4d7`

- **Envelope owns shape; per-artifact schemas own vocabulary.** The envelope declares `status` as required + non-empty string without mandating a specific enum. Each per-artifact schema supplies its vocabulary via `$ref common-defs#/$defs/lifecycle_status` (universal default — PB, Requirements) or inline `enum` (ADR's Nygard override).
- **Rationale.** `allOf` in JSON Schema narrows intersections but cannot override a `$ref`-enforced enum. Pushing vocabulary to per-artifact schemas is architecturally clean (envelope = universal structure, per-artifact = domain terms) and avoids conditional `if/then/else` patterns that would bake artifact-specific knowledge into the envelope. Discovered while writing the ADR schema; the refactor was applied before ADR landed.
- **Implication for future per-artifact schemas.** Every new per-artifact schema must explicitly declare its `status` property override in its inline `allOf` branch — inheriting from the envelope alone no longer enforces a vocabulary.

### Versioning — Model A

- Single live file per artifact on disk = the active version.
- `version: integer` — monotonic, bumped on material revisions.
- Git carries history. No filesystem multi-version coexistence.
- Supersession via `supersedes` / `superseded_by` links — rare, for when a differently-named artifact replaces a predecessor (common for ADRs).

### Recovery status (retrofit)

- Envelope field: `recovery_status: string | object`.
- Scalar form applies artifact-wide; object form maps field/section names to statuses.
- Allowed scalar values: `verified | reconstructed | unknown`.
- **No-fabrication rule** (enforced in per-artifact schemas): `reconstructed` banned on human-only fields — ADR context/alternatives/rationale, Requirements rationale, Product Brief content, DD *intent*. Allowed states on those fields: `verified | unknown` only.

### Scope path regex

- `^$|^[a-z0-9]+(-[a-z0-9]+)*(/[a-z0-9]+(-[a-z0-9]+)*)*$`
- Empty string = root scope.
- Kebab-case segments separated by `/`.

---

## 3. HTML-Derived Commitments

Phase 2 HTML pages are authoritative for per-artifact content; schemas must honor their commitments. Inventory from Haiku subagent scans run this session:

### Product Brief (`product-brief.html`)

- Single file `/specs/product_brief.md` (root only).
- Front-matter: `id` (const `"PB"`), `title`, `summary`, `status`, `date`, `recovery_status` (per-section map).
- 7 sections per TARGET §5.3 (Stakeholders, Problem, Desired Outcomes, Operational Concept, Constraints, Non-Goals, Success Criteria).

### ADR (`adr.html`)

- Path: `/specs/adrs/adr-NNN-{slug}.md`; flat directory.
- Front-matter: `id`, `title`, `status`, `date`, `scope_tags`, `supersedes` / `superseded_by`, `affected_scopes`, `context`, `decision`, `alternatives_considered`, `rationale`, `consequences`.
- **Mandatory Reversibility sub-prompt** inside Consequences (TARGET §5.3).

### Requirements (`requirements.html`)

- Path: `/specs/{scope}/requirements.md` (non-leaf scopes).
- Front-matter: `id`, `title`, `parent_scope`, `status`, `date`, `derived_from`, `governing_adrs`.
- Per-req embedded YAML: `id`, `statement`, `rationale` (required), `acceptance` (optional), `derived_from`.
- **`priority` was removed** this session. Do not re-add unless a concrete need surfaces.

### Architecture (`architecture.html`)

- Path: `/specs/{scope}/architecture.md`; root at `/specs/architecture.md`.
- Front-matter (HTML commits to): `id`, `scope`, `parent_scope`, `derived_from`, `governing_adrs`, `recovery_status`.
- **ADD** `title`, `status`, `date` in the schema — arch.html under-specified, universal consistency wins.
- 6 mandatory sections: Metadata, Overview, Structure Diagram, Decomposition, Interfaces, Composition.
- **Per-child** (Decomposition): `id`, `purpose` (one sentence, no conjunctions), `responsibilities` (1–3), `allocates` (list of REQ IDs). Optional: `rationale`, `recovery_status`.
- **Per-interface:** `name`, `from`, `to`, `protocol`, `contract` (nested). Contract has Design-by-Contract shape:
  - `operation`, `preconditions`, `postconditions.{on_success, on_precondition_failure, on_downstream_failure}`, `invariants`, `errors[{code, http, meaning}]`, `quality_attributes`.
- **Composition section:** runtime pattern (named with rationale), sequence diagrams (Mermaid, happy + 1–2 failure paths), middleware stack (ordered), DI / composition-root strategy, message-bus topology where applicable.
- **Root-scope-only additions:** environments, orchestration target, runtime-unit boundaries + deployment cardinality, IaC reference, integration-test targets.

### Detailed Design (`detailed-design.html`)

- 7 sections: Metadata, Overview, Public Interface, Data Structures, Algorithms, State, Error Handling.
- Metadata: `scope_tags`, `parent_architecture`, `derived_from`, `governing_adrs`.
- **Pre-pivot Section 8 "Test Strategy" removed** — DD references leaf TestSpec via traceability.

### TestSpec (`testspec.html`)

- Path: `/specs/.../testspec.md` per scope (every scope has one).
- Envelope: `id`, `title`, `type`, `verifies` (**MANDATORY non-empty list**), `preconditions`, `inputs`, `steps`, `expected`.
- `type` enum — **11 values** per TARGET reconciliation:
  `functional | boundary | error | fault-injection | property | state-transition | contract | performance | security | accessibility | error-guessing`.
- Reserved growth fields for Phase 3: `fixtures`, `data`, `expected_range`.

---

## 4. Authoring Rhythm (per per-artifact schema)

1. **Read** `docs/guide/artifacts/<type>.html` — authoritative for content.
2. **Read** the matching `TARGET_ARCHITECTURE §5.3` entry — short, authoritative for structure.
3. **Draft** the schema — compose envelope via `allOf`, add per-artifact fields, tighten `id` pattern, declare required sections.
4. **Define embedded-YAML validators** where applicable (per-req, per-case, per-child) as `$defs` in the per-artifact schema.
5. **Meta-validate + smoke-test** — see §5 Validation Recipe.
6. **Archive** the pre-pivot-tainted file (if any) as part of the same commit.
7. **Commit** per-step: `Phase 3: <artifact> schema as JSON Schema 2020-12`.

---

## 5. Validation Recipe

A venv lives at `/tmp/vmodel-schema-check` with `jsonschema` + `referencing` installed. If recreating:

```bash
python3 -m venv /tmp/vmodel-schema-check
/tmp/vmodel-schema-check/bin/pip install --quiet jsonschema referencing
```

Validation template:

```python
/tmp/vmodel-schema-check/bin/python <<'EOF'
import json
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

common = json.load(open('schemas/artifacts/common-defs.schema.json'))
env    = json.load(open('schemas/artifacts/envelope.schema.json'))
new    = json.load(open('schemas/artifacts/<type>.schema.json'))

Draft202012Validator.check_schema(common)
Draft202012Validator.check_schema(env)
Draft202012Validator.check_schema(new)

registry = Registry().with_resources([
    ('https://vmodelworkflow.dev/schemas/artifacts/common-defs/v1', Resource.from_contents(common)),
    ('https://vmodelworkflow.dev/schemas/artifacts/envelope/v1',    Resource.from_contents(env)),
    ('https://vmodelworkflow.dev/schemas/artifacts/<type>/v1',      Resource.from_contents(new)),
])
v = Draft202012Validator(new, registry=registry)

# --- smoke tests ---
good = { ... minimal valid instance ... }
print('ok:', list(v.iter_errors(good)))

for name, bad in [
    ('missing X',     { ... }),
    ('bad enum Y',    { ... }),
    ('bad pattern Z', { ... }),
]:
    errs = list(v.iter_errors(bad))
    print('rej' if errs else 'FAIL', name, errs[:1])
EOF
```

**Smoke-test checklist per schema:**
- Minimal valid example (all required present).
- One failure per declared constraint (missing required, bad enum, bad pattern, bad date format).
- Retrofit example with `recovery_status` scalar + map forms.
- Supersession example with `status: superseded` + `superseded_by`.

---

## 6. Open Architectural Points (defer decisions)

- **Quality Bar container shape (task #3).** Its own session. HTML sections are authoritative for content; task is to design the YAML shape that tools consume. Must precede task #12 extraction.
- **`priority` field.** Dropped from requirements.html this session. Reintroduce only when grounded in actual use.
- **HTML front-matter under-specification.** Several artifact pages (architecture, detailed-design, testspec) do not show `title` / `version` / `artifact_type` in their front-matter tables despite these being envelope-universal. Schemas drive consistency; HTML wording sweep is a follow-up when enough drift accumulates.
- **`partially_verified` recovery_status value** in `product-brief.html` retrofit example (line ~607) is not in the common-defs enum (`verified | reconstructed | unknown`). Content defect in the page example; fix when next touching the PB page.
- **TestSpec HTML drifts (carried into §6 from the #10 commit):**
  - `testspec.html` root example (line ~677): `derived_from: [requirements.md, product_brief.md]` uses filenames rather than artifact IDs. Schema requires IDs — both the HTML's scalar form (line 483: `derived_from: DD-...`) and the filename form need to be normalised to a non-empty array of IDs (e.g. `[REQS, PB]` at root).
  - `testspec.html` §4 anti-pattern example (line ~771): `TC-login-R1` uses uppercase `R`. Framework-wide ID convention is lowercase kebab (every other artifact's ID regex rejects uppercase). Schema holds; HTML example should become `TC-login-r1` in next page sweep.

---

## 7. References

- `CLAUDE.md` — project conventions, working discipline.
- `docs/plan/TARGET_ARCHITECTURE.md` — §3 principles, §5 artifact model, §6 rigor, §7 traceability, §10 tools.
- `docs/plan/BACKLOG.md` — Phase 3 scope in §3.3.
- `docs/guide/artifacts/*.html` — six authored artifact pages (authoritative for content).
- `schemas/artifacts/envelope.schema.json`, `schemas/artifacts/common-defs.schema.json` — Phase 3 foundation.
- MEMORY: `~/.claude/projects/-home-stefanus-repos-VModelWorkflow/memory/MEMORY.md`.

---

## 8. Recommended Next Step

All schema-shape work is done: six per-artifact schemas + the two traceability schemas. Only two Phase-3 tracks remain — Quality Bar (tasks #3 then #12) and fixtures (#13).

**Task #3 — Quality Bar YAML container shape.** Design-heavy session. Blocks task #12 (per-artifact QB extraction) and therefore unblocks the Quality-Bar-consuming cascade rule (TRV-QB-001, currently `deferred_until: phase_3_task_3_and_12` in `validation-rules.catalog.json`). HTML §5 sections across the six artifact pages are authoritative for content; this task is purely the container shape. Natural next step now that the schema foundation is stable — the QB container can reference the same artifact-type enum, scope_path, recovery_status shapes, and (for QB rules that name fields) the field names committed by the per-artifact schemas.

Alternative 1: **Task #13 — Minimal-example fixtures per artifact.** Write one minimal valid instance per artifact type (six Markdown files) that round-trips through the corresponding schema's front-matter validator. Establishes a golden set for downstream tool testing (parser, scaffolder, validator) and catches any subtle schema-vs-HTML mismatches before Phase 5 skills start consuming the schemas. Independent of #3; can run in parallel.

Alternative 2: **Task #12 — per-artifact Quality Bar YAML extraction** direct, skipping the container design. Possible but ill-advised: without a container shape decided, six independently-shaped YAML files risk drift and a subsequent reshape-everything pass. Keep #3 → #12 ordering.

Per-case `id` pattern speculation retracted. Handoff §1 row for the 0dcba63 / 7742783 era predicted `TC-TS-{scope}-{seq}` by analogy to REQS/REQ; the HTML consistently uses local `TC-{seq}` inside the parent TestSpec document, and the #10 schema commits to that. Cross-document references qualify as `{TS-id}.{TC-id}` when needed; the case id itself stays local.
