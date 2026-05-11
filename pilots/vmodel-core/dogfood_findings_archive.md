---
purpose: Archive of fixed pilot findings from vmodel-core. New / open findings continue to live in `dogfood_findings.md`.
audience: framework maintainer
status: living
---

# Fixed issues — vmodel-core pilot archive

This file collects findings from `dogfood_findings.md` that have been resolved in the framework repo. Each entry preserves the original issue body verbatim and appends a `**Fixed:** YYYY-MM-DD — <brief note>` line linking to the framework-side change. For open / in-progress findings, see `dogfood_findings.md`.

---

## 2026-05-11

### Issue 25 — REQ-016 names six canonical artifact types but the framework publishes a seventh schema (`architecture-interface-detail`)

**Where surfaced.** Authoring `DD-embedded-resources` (the leaf DD that owns typed accessors over `embed.FS` for the rule catalog, schema set, and Quality Bar checklist set). Defining the `ArtifactType` closed enum required reconciling two upstream sources:

- **`specs/requirements.md` REQ-016 + Glossary.** The *Framework canonical schema set* glossary entry names exactly **six** per-artifact schemas: `product-brief, requirements, architecture, adr, detailed-design, test-spec`. REQ-016 obliges vmodel-core to validate each artifact against the per-artifact schema corresponding to its `artifact_type`.
- **Framework `schemas/artifacts/`.** Publishes **seven** per-artifact schema files. The seventh — `architecture-interface-detail.schema.json` — has its own `artifact_type` const value (`architecture-interface-detail`) and is the canonical shape for the Rule-8 architecture bundle's per-interface detail files (`<scope>/architecture/interfaces/<NAME>.md`).

**The gap.** The seventh schema exists structurally (Rule 8 architecture bundle files in the pilot tree right now would be subject to it, e.g. `IFrameworkResources.md`), but is not enumerated in REQ-016's contract or the Glossary. Two clean outcomes; one wrong one:

1. **Amend REQ-016 + Glossary to seven types.** Treat `architecture-interface-detail` as a first-class artifact type subject to vmodel-core schema validation. The cost is small (one Glossary entry, one phrase in REQ-016, an enum member to add in `DD-embedded-resources`). This is most likely the right outcome — interface detail files are real artifacts in the spec tree and there is a real schema for them.
2. **Mark `architecture-interface-detail` as a non-validated sub-shape of `architecture`.** Treat the interface detail files as fragments of the parent architecture artifact for validation purposes; do not publish them as a distinct `artifact_type` to vmodel-core. Requires retracting the `artifact_type: architecture-interface-detail` const from `architecture-interface-detail.schema.json` (or making it internal-only).
3. **(Wrong.)** Quietly grow the `DD-embedded-resources` ArtifactType enum to seven without amending REQ-016. This is DD inventing past its upstream and would silently fail the requirements / DD trace test.

**Pilot decision for this session.** `DD-embedded-resources` pins the ArtifactType enum at six per REQ-016 (no DD invention). The seventh schema's runtime addressability through `IFrameworkResources` is blocked on the requirements amendment.

**Suggested resolution.** Pick outcome (1) or (2) at framework scope, then propagate:

- **If (1):** amend `requirements.md` REQ-016, REQ-017, and the *Framework canonical schema set* / *Framework canonical Quality Bar checklist set* Glossary entries to name seven types. Amend `DD-embedded-resources` ArtifactType enum and bundle layout to include `architecture-interface-detail.schema.json`. (There is no `architecture-interface-detail.quality-bar.json` today — decide whether QB applies to detail files too.)
- **If (2):** retract or internalise the `artifact_type` const in `architecture-interface-detail.schema.json`; document the interface-detail files as validation-scope-internal sub-shapes of `architecture` in the schema reference.

**Pairs with.** Issue 16 (architecture skill: where do ADR-bound library / protocol bindings land) — both concern the gap between what the schemas publish as first-class artifact types and what the requirements layer enumerates.

**Fixed:** 2026-05-12 — Option 1 taken. Propagation: (a) `references/authoring-discipline.md` Rule 8 detail-file front-matter template now requires `artifact_type: architecture-interface-detail` and `title:` (the two envelope-required fields previously omitted); synced to pilot `.vmodel/references/`. (b) `schemas/artifacts/quality-bar/quality-bar.schema.json` `artifact_type_enum` and `artifact_id_prefix_enum` extended to include the seventh type (prefix `AID`); item-id regex extended. (c) New `schemas/artifacts/quality-bar/architecture-interface-detail.quality-bar.json` published (4 groups, 16 items including the meta-gate). (d) New `schemas/artifacts/fixtures/architecture-interface-detail.example.md` round-trips clean. (e) `schemas/traceability/link-types.schema.json` and `validation-rules.schema.json` `artifact_type_enum` extended (the catalogs already named the seventh type — schemas were the laggards). (f) `schemas/artifacts/envelope.schema.json` and the validation-rules catalog `TRV-QB-001.applies_to_artifact_types` updated to reflect seven types. (g) `docs/guide/artifacts/architecture.html` Rule-8 example's detail-file front-matter corrected (was using stale `parent_artifact` / `interface_name` field names instead of `belongs_to` / `subject`); new paragraph names the detail file as a first-class artifact and explains why the type count is seven. (h) Pilot Glossary entries (Framework canonical schema set, Framework canonical Quality Bar checklist set) name seven types; `requirements.md` v2 dated 2026-05-12. (i) Pilot `DD-embedded-resources` v2: `ArtifactType` enum grown to seven members; bundle layout adds `architecture-interface-detail.schema.json` + `architecture-interface-detail.quality-bar.json`; closing Note rephrased; "six" → "seven" across signatures, complexity_notes, error-matrix, data-structure invariants, and TestSpec cues. (j) Pilot 8 interface detail files now carry `artifact_type` and `title` and validate against the per-type schema (previously envelope-invalid). (k) `TS-embedded-resources` v2: parameterised case `enumerate:` lists grown from six to seven; titles and prose mentioning "six-enum" → "seven-enum"; closing note rephrased. (l) Root TS workload fixture's "six artifact_type values" → "seven". Pilot `CLAUDE.md` open-decision bullet replaced with closure note. `DD-validation-engine` authoring is unblocked.

### Issue 26 — DEFER markers bleed across scopes when cited in prose

**Where surfaced.** Authoring `DD-embedded-resources` on 2026-05-11. The DD's Overview originally cited the parent ARCH's existing `[DEFER-DD: validation-engine — JSON Schema 2020-12 validator library selection]` in prose to explain why this leaf returns raw JSON bytes (not pre-parsed Schema objects). `scripts/index-deferred-items.py` picked up the prose citation as a new DEFER-DD marker anchored at `DD-embedded-resources`. The deferral genuinely lives at `validation-engine` scope; the DD merely references it. The fix in this session was to drop the bracket form and paraphrase in prose — i.e., the author skill silently rewards rewording around the script rather than supporting honest cross-reference.

**What the script does.** Matches `[DEFER-(DD|ADR): ...]` anywhere in any artifact body, regardless of whether the bracket form is an *owning* marker (this artifact owns the deferred decision) or a *citing* reference (this artifact references another artifact's deferred decision).

**What `authoring-discipline.md` Rule 6 says.** A `[DEFER-<TARGET>: <topic>]` marker names a deferred decision and the artifact at which it will be answered. Implicit semantics: the marker should appear *exactly once* in the spec tree — at the artifact where it will be answered.

**The gap.** There is no canonical syntax to *cite* a DEFER marker by reference. Two side effects:

1. The author skill rewards paraphrasing-around-the-script over honest cross-reference; an author who cites the marker verbatim is "punished" by the index counting it twice (and by `index-deferred-items.py` inflating the apparent surface area of unresolved gaps).
2. The defer-index conflates "this artifact owns this deferral" with "this artifact is aware of it" — different things; a human reading the index cannot tell which is which.

**Suggested resolution.**

1. **Script side.** Make `index-deferred-items.py` distinguish *owning* marker from *citing* prose. Two options: (a) introduce a bracket-syntax distinction (e.g., `[DEFER-DD: ...]` for owners; `[cite-DEFER-DD: <owner-artifact-id>]` or `«DEFER-DD: <owner-id>»` for citations); (b) deduplicate by topic-string equality — if the same bracket text appears in multiple artifacts, attribute the marker to the artifact whose scope matches the marker's `<scope>` segment or whose `parent_architecture` chain identifies it as the owner.
2. **Rule 6 side.** Extend `authoring-discipline.md` Rule 6 to specify how to cite a DEFER marker from a downstream artifact without re-emitting it, or to explicitly forbid prose citation of bracket markers (forcing prose-only descriptions of upstream deferrals).
3. **Author-skill side.** Add explicit guidance to author skills: when referencing another artifact's deferred decision, do not use the `[DEFER-XX: ...]` bracket form; describe the deferral in prose with an artifact-id citation to the owner.

**Pairs with.** Issue 6 (skill template / schema mismatch — adjacent failure mode where stale skill conventions create phantom artifacts in the index).

**Fixed:** 2026-05-11 — Added cite-form syntax `«DEFER-DD: owner-id — topic»` to `references/authoring-discipline.md` Rule 6 (synced to pilot `.vmodel/references/`); `scripts/index-deferred-items.py` now distinguishes owning markers from cite-form citations (`total_defer_citations` reported separately).

### Issue 28 — Schema validation is invented per-session instead of being a pre-built script

**Where surfaced.** Authoring `DD-embedded-resources` on 2026-05-11. The DD author skill's Step 13 (Pre-publish mechanical self-check) lists `scripts/check-mermaid.py` and `scripts/check-id-encoding.py` as the canonical scripts but **does not** include a JSON Schema validation step. To validate front-matter against `detailed-design.schema.json` and embedded YAML blocks against the per-block `$defs`, the author session wrote two ad-hoc inline Python snippets via bash heredoc:

1. Parse front-matter, build a `referencing.Registry` from every schema under `schemas/`, run a `Draft202012Validator` against `detailed-design.schema.json`.
2. Extract every `\`\`\`yaml\` block from the body, identify which `$defs` member each should validate against (`public_interface_entry`, `data_structure_entry`, `error_matrix_row`), validate each entry.

**Real defects caught only because the snippets were written.** The first run reported one front-matter error: `title: 'title' is a required property`. The `title` field had been omitted; **none of the scripts listed in Step 13 detect this**. The artifact would have shipped schema-invalid had the snippets not been written. Two of the existing scripts (`check-id-encoding.py`, `check-template-schema-fields.py`) target adjacent concerns but neither validates against the JSON Schema.

**Cost side.** Writing, debugging (`jsonschema` not installed in the project venv → `pip install jsonschema referencing` → re-run), and re-running the snippets consumed ~15k of the session's token budget (Issue 27). This work is identical at every author session — every author skill across every artifact type — and so is pure waste against the schema-validation goal.

**The gap.** Schema validation is the single most foundational mechanical check (it is, after all, what `vmodel-core` itself will do as a CLI per REQ-015 / REQ-016). Author skills should not invent it per session. The current Step 13 script list lets schema-invalid artifacts ship if no author thinks to add the check.

**Suggested resolution.**

1. **Until `vmodel-core` ships — add `scripts/check-schema-validation.py`.** Generic validator that:
   - Reads any artifact path.
   - Reads `artifact_type` from front-matter.
   - Locates the corresponding `schemas/artifacts/<type>.schema.json`.
   - Validates front-matter against the per-artifact schema (which composes the envelope).
   - Extracts embedded YAML blocks from the body, identifies the `$defs` member by section context (`Public Interface` → `public_interface_entry`, `Data Structures` → `data_structure_entry`, error-matrix table → `error_matrix_row`).
   - Validates each entry; emits `<file>:<line>:<rule-id>:<message>` per finding; exit 0 / 1 / 2 per the existing script convention.

2. **Add the script to every author skill's Step 13 (Pre-publish mechanical self-check),** since the check is uniform across all six artifact types.

3. **After `vmodel-core` ships** — retire `scripts/check-schema-validation.py`; replace the Step 13 entry with `vmodel-core validate <artifact-path>`. The script is interim scaffolding for the period before the canonical validator is available.

**Pairs with.** Issue 24 (`check-typed-error-coverage` — another mechanical script whose assumptions don't perfectly match the spec-tree state), Issue 27 (session token cost — schema-validation snippets are a large slice of the waste).

**Fixed:** 2026-05-11 — New `scripts/check-schema-validation.py` validates front-matter against the per-artifact schema plus embedded YAML blocks against `$defs`; added to every author skill's Step 11 pre-publish self-check.

### Issue 29 — Mechanical-check script paths in SKILL.md are ambiguous (bundled vs repo-root)

**Where surfaced.** Authoring TestSpec for `embedded-resources` on 2026-05-11. `vmodel-skill-author-testspec` SKILL.md Step 11 lists:

> Scripts for this skill:
> - `scripts/check-implicit-verifies.py <specs-root>` — ...
> - `scripts/check-typed-error-coverage.py <specs-root>` — ...
> - `scripts/check-id-encoding.py <specs-root>` — ...

The literal `scripts/...` path is ambiguous between the skill's bundled `scripts/` subdir (analogous to the bundled `references/` and `templates/`) and the repo-root `scripts/`. I first invoked them as `python3 .claude/skills/vmodel-skill-author-testspec/scripts/check-implicit-verifies.py ...` and got `No such file or directory`. The scripts actually live at `/scripts/check-*.py` at the framework repo root.

**The gap.** The path notation does not unambiguously name the directory. The skill bundles `references/` and `templates/` in-tree, so "scripts/" reads naturally as another bundled subdir — but it isn't. Every author skill that lists Step-11 scripts has this same ambiguity. Authors and downstream agents will hit the same misread; the bash failure mode is non-catastrophic (the agent retries with a different path) but the misread costs tokens and session time.

**Suggested resolution.**

- Resolve via `.vmodel/config.yaml` — add `paths.scripts` (matching the existing `paths.references` pattern). Skills then refer to `${paths.scripts}/check-implicit-verifies.py`. Framework default `paths.scripts: scripts/` resolves at the repo root; projects can relocate.
- Apply across every author skill's Step 11 / Pre-publish self-check sections in one sweep.

**Pairs with.** Issue 28 (`check-schema-validation.py` missing — sibling script-discoverability gap), Phase 6 central-config pattern (the `paths.*` family).

**Fixed:** 2026-05-11 — Added `paths.scripts` to `schemas/core/vmodel-config.schema.yaml` (default `scripts/`); 10 SKILL.md files updated to use `${paths.scripts}/<name>.py` instead of bare `scripts/<name>.py`; TARGET §15 updated.

### Issue 30 — Leaf TestSpec closing an ARCH-level typed-error must dual-cite, and the rule is buried mid-sentence

**Where surfaced.** Authoring TestSpec for `embedded-resources` on 2026-05-11. The leaf TestSpec naturally cited `DD-embedded-resources.public_interface.Schema.errors.ErrUnknownArtifactType` for TC-007 / TC-008 — the layer-correct granularity per `per-layer-weight.md` (leaf → DD field). `check-typed-error-coverage.py` then reported `ARCH.interfaces.IFrameworkResources.errors.ErrUnknownArtifactType` as uncovered because it looks for the ARCH-level path literally and does not traverse the DD's `parent_architecture` / `derived_from` link back to the ARCH interface.

Step 6 of `vmodel-skill-author-testspec` says:

> "Typed-error enum coverage: every entry in a parent interface's `errors:` enum requires at least one case under the `error` or `fault-injection` strategy. Roll-up cases (one case covering multiple errors via shared halt-and-report path) are permissible when the parent contract treats them uniformly, but each rolled-up code MUST be cited in the case's `verifies:` list. Mechanically detected by `scripts/check-typed-error-coverage.py` at Step 11."

The "each rolled-up code MUST be cited" half is buried mid-sentence and reads at first scan as covering only the roll-up case. The cross-layer dual-citation pattern (leaf closes ARCH-level typed-error by citing BOTH the DD-level error path AND the ARCH-level error path in the same case's `verifies:`) is not stated explicitly anywhere — neither in Step 6, `verifies-traceability.md`, nor `dd-traceability-cues.md`.

**The gap.** A layer-correct authoring pass (leaf cites DD only) silently fails the mechanical check. The author must either: (a) add the ARCH-level citation manually after the check fails; (b) read `check-typed-error-coverage.py` source to understand what it looks for. I did (a) after the check fired. A first-time author would probably do (b), expanding token cost.

**Suggested resolution.**

- **Author-side fix** (cheapest). Promote the dual-citation rule to its own bullet in Step 6 with a worked example: a leaf case whose `verifies:` carries both `DD-<scope>.public_interface.<fn>.errors.<code>` and `ARCH.interfaces.<iface>.errors.<code>`. Cross-link from `verifies-traceability.md` and `dd-traceability-cues.md`.
- **Script-side fix** (more involved, correct). Teach `check-typed-error-coverage.py` to traverse a DD's `parent_architecture` and `derived_from: [..ARCH-IF-X..]` links and infer that DD-level coverage closes the ARCH-level row. Mirrors what a human reviewer does mentally.

Author-side fix is fast and visible; script-side fix is the long-term correct answer. Both warranted.

**Pairs with.** Issue 24 (`check-typed-error-coverage` deferral-pattern blind spot — same script, sibling concern).

**Fixed:** 2026-05-11 — Script side: `scripts/check-typed-error-coverage.py` now reads DD `derived_from: [ARCH-IF-<NAME>]` and synthesizes the implied ARCH-level error paths so a leaf-level citation closes the ARCH-level row. Author side: `vmodel-skill-author-testspec/SKILL.md` Step 6 lifts the dual-citation rule into its own bullet with a worked `ErrUnknownArtifactType` example.

### Issue 31 — QB "error/happy ratio ≥ 1:2" lacks an escape valve for leaves with small genuine error surface

**Where surfaced.** Authoring TestSpec for `embedded-resources` on 2026-05-11. The DD's error matrix has exactly one row (`ErrUnknownArtifactType`) across two callsites, exhaustively covered by TC-007 / TC-008. The success/invariant surface needs 12 cases (six contract + five byte-stability + one thread-safety). Result: error/happy ratio is 2:6 = 1:3, below QB Group 2's heuristic of ≥ 1:2.

`quality-bar-checklist.md` Group 2 reads:

> "Error / happy ratio is at least 1:2."

And the checklist's preamble says:

> "When any 'Yes' cannot be honestly answered, do not ship — surface the gap."

For leaves whose DD genuinely has one or two error-matrix rows (and where bundle absence / decode failure / sandbox violation are *explicitly* out of scope at the leaf — system-level or build-time, with documented rationale), no amount of honest authoring can lift the ratio without fabricating error surface. The honest move is to write an inline Overview paragraph naming the non-fit and the reason. I did this; the reviewer judged the framing legitimate.

**The gap.** No documented escape pattern. Authors either: (a) silently pass — close cousin of `anti-pattern.coverage-as-quality-metric` (ratio rhetoric without surface); (b) fabricate "robustness" cases for non-existent failure modes — direct anti-pattern; (c) write inline justification each time — what I did, fine but un-documented and varies by author. Reviewers must re-judge each instance.

**Suggested resolution.**

- Soften the bar in `quality-bar-checklist.md` Group 2 to a conditional phrasing: *"Error / happy ratio is at least 1:2 when the parent spec's error surface supports it; otherwise the author names the non-fit and the reason in the Overview, citing which DD error-matrix rows are covered and which failure modes are out-of-scope-with-rationale."*
- Cross-reference from `anti-patterns.md` so the legitimate-non-fit pattern is documented adjacent to the fabrication anti-pattern it's the opposite of.

**Pairs with.** Refusal C (no weak assertions) and the broader honest-authoring discipline — the legitimate-non-fit is the *opposite* of the fabricated-intent refusal: the author refusing to fabricate and naming the gap instead.

**Fixed:** 2026-05-11 — `test-spec.quality-bar.json` plus `vmodel-skill-author-testspec` `references/quality-bar-checklist.md` and `anti-patterns.md` updated with conditional phrasing ("when the parent spec's error surface supports it; otherwise the author names the non-fit in the Overview …").

### Issue 32 — Review-file path convention is split between author-skill SKILL.md and pilot CLAUDE.md

**Where surfaced.** Authoring TestSpec for `embedded-resources` on 2026-05-11, dispatching the review subagent. Step 0 of `vmodel-skill-author-testspec` reads:

> "If `specs/.reviews/<artifact-id>-*.yaml` contains review files for this artifact: ..."

Per TARGET_ARCHITECTURE §5.6 review output convention.

The pilot's CLAUDE.md says:

> ```
> .vmodel/
>   .reviews/             — Spec-side review verdict files (checked in)
> ```

So the canonical path is split: framework author-skill says `specs/.reviews/`, pilot says `.vmodel/.reviews/`. The reviewing subagent had to pick one; it picked the pilot convention. Step 0 of the *next* author-skill revision pass will look at `specs/.reviews/` (per SKILL.md) and find no review files, silently treating the artifact as never-reviewed.

**The gap.** Two canonical paths. Authors and review subagents drift apart. Revision-pass Step 0 (which reads the latest review) silently loses review state if the path used at write-time differs from the path used at read-time. The drift is not detected by any mechanical check — `index-deferred-items.py` doesn't traverse review state.

**Suggested resolution.**

- Resolve via `.vmodel/config.yaml` `paths.reviews` (matching the existing `paths.references` pattern). Framework chooses a default; projects may override.
- Pick the default: `.vmodel/.reviews/` matches the rest of the central-config pattern from Phase 6 Cluster 5 (config, references, build outputs all under `.vmodel/`); `specs/.reviews/` keeps reviews next to the artifacts but inverts the central-config convention. Recommend `.vmodel/.reviews/`.
- Update every author-skill Step 0 reference and every review-skill output path to read `paths.reviews` instead of literal `specs/.reviews/`. Update TARGET §5.6 to name the central-config indirection.

**Pairs with.** The `.vmodel/config.yaml` `paths.*` family introduced in Phase 6 Cluster 5. TARGET §5.6 (review output convention — currently the authoritative source for `specs/.reviews/`).

**Fixed:** 2026-05-11 — All 10 SKILL.md files updated to use `${paths.reviews}/<artifact-id>-*.yaml`, aligning with TARGET §5.6 and the pilot CLAUDE.md `.vmodel/.reviews/` convention.
