---
name: vmodel-skill-author-testspec
description: Author one TestSpec artifact (Markdown with YAML front-matter, per-case YAML blocks) for one scope, deriving cases from the layer's upstream spec via named strategies, with non-empty `verifies` links and specific oracles on every case. Use when authoring a TestSpec from a parent Detailed Design (leaf), Architecture (branch), or Requirements + Product Brief (root) — applying functional / boundary / error / fault-injection / property / state-transition / contract / performance / security / accessibility / error-guessing strategies; specifying the artifact-level coverage and mutation bar; replacing weak oracles with specific values or bounded predicates; retrofitting with `recovery_status: unknown` on reconstructed `verifies`. Refuses fabricated retrofit intent on `title`/`notes`, orphan cases, weak assertions, missing coverage bar, and Spec-Ambiguity-Test failure. Triggers — write testspec, draft testspec.md, derive test cases, specify oracles, set coverage bar, retrofit testspec.
type: skill
---

# Author test specification document

This skill produces a single Markdown file: a TestSpec for one scope. The document carries front-matter (id, scope, level, derived_from, verifies, governing_adrs, coverage_mutation_bar, recovery_status when retrofit) and a Cases section of embedded per-case YAML blocks. Every case names a derivation strategy from a fixed enum, points at one or more upstream spec elements via `verifies`, and states a specific oracle. The skill is authored under hard quality gates that prevent the most common TestSpec failures — orphan cases, weak assertions, fabricated retrofit intent, and TestSpecs that pass shape checks but cannot guide a junior test engineer.

The skill is self-contained. Every reference, template, anti-pattern catalog, and quality-bar checklist it needs is bundled in `references/` and `templates/`. No external lookups are needed.

## When to use

Activate this skill when the user asks to:

- Write or draft a TestSpec for one scope
- Derive cases from a parent spec (Detailed Design at leaf, Architecture at branch, Requirements + Product Brief at root)
- Apply derivation strategies — functional / boundary / error-path / fault-injection / property / state-transition / contract / performance / security / accessibility / error-guessing
- Specify the artifact-level coverage and mutation bar (structural threshold, mutation threshold, tool category, enforcement frequency)
- Make oracles specific where they are weak (replace `assertNotNull`-only / `verify behaviour` with enumerated values or bounded predicates)
- Retrofit a TestSpec from an existing test suite with `recovery_status` discipline (`verifies` reconstructed without human confirmation are `unknown`)

Do **not** activate this skill for:

- Authoring Requirements, Architecture, ADR, Detailed Design, or Product Brief — those are separate authoring skills' jobs
- Reviewing or auditing an existing TestSpec — that is the matched review skill's job
- Writing implementation code or test code — those are downstream artifacts

## Inputs

Expected upstream context (ask if missing):

- **Scope identifier** — the path and name of the scope this TestSpec covers (e.g., `session-store/expiry-calculator`, or `cart-service` for a branch, or `/` for root)
- **Layer** — leaf / branch / root. Determines the parent spec type and the case shape.
- **Parent spec artifact(s)** — **Position C: at non-leaf scopes the layer has two upstream derivation sources, not one.** See "Verification targets per scope" in TARGET_ARCHITECTURE §5.3.
  - *Leaf:* the parent Detailed Design (its Public Interface contracts, Data Structure invariants, error-handling matrix, state machine).
  - *Branch:* **both** the parent Architecture (Composition section, interface contracts, QA allocations, resilience strategies) **and** the branch's own Requirements (behavioural intent). Behavioural cases cite `REQ-{scope}-*`; composition cases cite `ARCH-{scope}` composition entries.
  - *Root:* the Product Brief + root Requirements + root Architecture Composition. Behavioural cases cite `REQ-*` or `PB`; composition cases cite `ARCH` composition entries.
- **Governing ADRs** — cross-cutting decisions that constrain testing approach (e.g., environment shape, fixture strategy)
- **Recovery posture** — greenfield (omit `recovery_status`) or retrofit (declare `recovery_status` on reconstructed `verifies`)
- **Project policy on coverage / mutation thresholds** — if the project has named values, capture them; otherwise the bar is populated with placeholder values and a note that policy will fix them
- **Prior review files** (optional, consumed when present) — on a revision pass, the latest review at `specs/.reviews/<artifact-id>-*.yaml` (lexically last) is read and findings are addressed. Per TARGET_ARCHITECTURE §5.6 review output convention.

If the parent spec is not provided, **HALT** (see HALT condition #1) — refusal B fires when TestSpec authoring proceeds without an upstream artifact.

## Output

A single Markdown file using the structure in `templates/test-spec.md.tmpl`. Front-matter carries the required fields plus a `coverage_mutation_bar:` block. The body has an Overview section and a Cases section composed of embedded YAML blocks (one per case, conforming to `templates/case-leaf.yaml.tmpl`, `case-branch.yaml.tmpl`, or `case-root.yaml.tmpl` depending on layer).

Default output filename: `<scope>/testspec.md`. Follow the project's scope-tree convention when one exists.

## Cross-cutting authoring discipline

Apply the six rules in `references/authoring-discipline.md` across every authoring step. Most relevant here: Rule 0 (no `n/a + justification` for omitted slots, no self-attestation prose — `coverage_mutation_bar` placeholder values are valid product-shape, not template-shape excuses), Rule 3 (rationale on coverage-bar / mutation-bar choices is one line plus citation when a governing ADR fixes the threshold; no re-narration of the policy), Rule 5 (`verifies` is a citation — the case body should not restate what is being verified; cite the upstream DD field / Architecture interface / Requirement by ID and let the reader follow the link). Rule 1 (boundary-only), Rule 2 (small-system collapse), and Rule 4 (diagram-or-prose) apply universally but are less load-bearing for testspec authoring. Review skills enforce all six as `check.discipline.<rule>` findings.

## Authoring procedure

Author the document in this order. Each step has its own reference file with the craft rules. Treat the references as the source of truth; this section is a checklist.

### Step 0 — Read prior review (revision pass only)

If `specs/.reviews/<artifact-id>-*.yaml` contains review files for this artifact:
1. Pick the lexically last (latest review run by date + sequence).
2. Walk every finding.
3. For each finding, decide: apply (revise this artifact), push back with rationale (finding is wrong), or defer with explicit marker (out of scope here, named follow-up).
4. Address findings in the revision. The revision narrative names which findings were addressed and how.

Skip this step on greenfield (first author pass) — no review files yet.

### Step 1 — Locate the layer and parent spec

Determine which layer this TestSpec serves (leaf / branch / root). Identify the parent spec artifact. Note its derivation surface — the elements that will seed cases.

→ See `references/testspec-purpose-and-shape.md`

### Step 2 — Read the parent spec for derivation seeds

Walk the parent spec end-to-end and list the elements that demand a case. The element type depends on layer; use the upstream-seam reference for the layer.

→ See `references/dd-traceability-cues.md` (leaf), `references/architecture-traceability-cues.md` AND `references/requirements-traceability-cues.md` (branch — load both), `references/requirements-traceability-cues.md` AND `references/architecture-traceability-cues.md` (root — load both, plus PB outcomes covered in the requirements file)

### Step 3 — Apply derivation strategies

For each derivation seed, pick a strategy from the fixed enum (functional / boundary / error / fault-injection / property / state-transition / contract / performance / security / accessibility / error-guessing) and produce one or more cases. ECP pairs with BVA on input ranges; decision tables pair with functional on compound predicates.

→ See `references/derivation-strategies.md`

### Step 4 — Author front-matter

Populate `id`, `artifact_type: test-spec`, `scope`, `level` (root → system, non-leaf → integration, leaf → unit), `derived_from`, `verifies` (artifact-level, non-empty — refusal B), `governing_adrs`, `status`, `date`, `coverage_mutation_bar` block (refusal: section presence is mandatory), `recovery_status` (retrofit only).

→ See `templates/test-spec.md.tmpl`, `references/coverage-mutation-bar.md`

### Step 5 — Author cases per layer-weight

Each case shape depends on layer:
- *Leaf:* thin — id, title (scenario, not method name), type (from enum), verifies, inputs (keyed map), expected (specific value or bounded predicate). Steps usually omitted.
- *Branch:* preconditions name fixtures / test doubles / seeds / environment; steps enumerate cross-child interactions; expected names observable cross-child state.
- *Root:* preconditions name environment / tenants / flags / personas; steps narrate the user journey; expected uses Product Brief vocabulary.

→ See `references/per-layer-weight.md`, the matching template (`case-leaf.yaml.tmpl`, `case-branch.yaml.tmpl`, `case-root.yaml.tmpl`)

### Step 6 — Specify each case to the oracle bar

For every case: the title is a scenario (not a method name); the type is from the enum; `verifies` is non-empty and points at IDs that resolve in the upstream spec; `expected` is a specific value or a bounded predicate, never a qualitative phrase.

→ See `references/case-quality.md` (F.I.R.S.T., AAA, oracle specificity), `references/verifies-traceability.md`

### Step 7 — Apply test-double discipline (branch and leaf cases involving doubles)

When a case names a test double in preconditions, name the type (dummy / stub / spy / mock / fake). Fakes require a contract test against the real implementation. Cap of two doubles per leaf case; over-threshold flags a design issue. Reserve interaction verification for cases where the interaction itself is the observable behaviour.

→ See `references/test-double-discipline.md`

### Step 8 — Specialised cases (branch and root)

When the parent spec carries a quality-attribute allocation (performance, security, accessibility) or a contract testing seam, derive specialised cases at the named threshold. Pin environment shape and version in preconditions when applicable.

→ See `references/integration-and-system-specifics.md`

### Step 9 — Apply retrofit posture (retrofit only)

Order: derive the TestSpec from the spec FIRST, THEN map existing tests against it. `title` and `notes` are human-only fields in retrofit (refusal A) — never populate from inferred intent. `recovery_status: unknown` on any `verifies` reconstructed without human confirmation. Produce a gap report listing uncovered spec elements + tests-not-mapping-to-elements + observed-but-suspect cases.

→ See `references/retrofit-discipline.md`, `templates/retrofit-stub.yaml.tmpl`

### Step 10 — Anti-pattern self-check

Sweep the document against the thirteen anti-patterns (code-to-test derivation, tautological tests, test-as-requirement inversion, happy-path bias, weak assertions, over-mocking, mystery guest, ice-cream-cone coverage, coverage-as-quality-metric, unbounded negative tests, flaky tests, orphan tests, fabricated retrofit intent). Hard-rejects (refusal A/B/C aliases) trigger refusal; soft-rejects accumulate.

→ See `references/anti-patterns.md`

### Step 11 — Run Quality Bar checklist + Spec Ambiguity Test

Run the Yes/No checklist (eight QB groups + the SAT meta-gate). Flag any No inline; do not silently pass. The SAT is the override: a junior engineer reading only this TestSpec (plus the parent spec and governing ADRs) must be able to write the test code, and a reviewer must be able to tell whether every equivalence class, every boundary, every error path was considered.

→ See `references/quality-bar-checklist.md`

## Hard refusals (the four non-negotiables, plus the derived-hard for coverage-mutation section presence)

**A — Honest retrofit posture (no fabricated intent).** Refuse to:
- Populate `title` from inferred intent in retrofit (`title: "verifies user can log in"` derived from a method name `testUserLogin`).
- Populate `notes` from inferred intent in retrofit.
- Mark `recovery_status: verified` on a `verifies` link reconstructed without human confirmation; the correct value is `unknown`.
- Ship a retrofit TestSpec that claims plausible-sounding stated intent on every existing test.

Anti-pattern alias: `anti-pattern.fabricated-retrofit-intent`. Tells: retrofit case has stated intent; `recovery_status` is `verified` or absent on reconstructed `verifies`; gap report lists no `unknown` cases despite retrofit context.

**B — No orphan tests.** Refuse to:
- Emit a TestSpec whose artifact-level `verifies: [...]` is empty.
- Emit a case whose per-case `verifies: [...]` is empty.
- Emit a `verifies` element pointing at an ID that does not exist in the upstream spec.

Anti-pattern alias: `anti-pattern.orphan-tests`. Tells: artifact-level `verifies: []`; case missing `verifies` field; case `verifies` resolves to nothing in upstream artifacts; `verifies` references that look like filenames not artifact IDs.

**C — No weak assertions.** Refuse to:
- Emit a case whose `expected` is a qualitative non-bounded phrase. Reject `expected: "verifies behaviour"`, `expected: "does not throw"` as the sole assertion, `expected: "non-null"` alone, `expected: "instance of X"` alone.
- Every `expected` is a specific value, an enumerated set, or a bounded predicate (`<= 50ms`, `between 0 and 100`, `subset of {A, B, C}`).

Anti-pattern alias: `anti-pattern.weak-assertions`. Tells: `expected` text contains "verify", "behaviour", "works correctly", "does not throw", "non-null", "instance of" without further specifics; `expected` block is a single-line qualitative phrase.

**D — Spec Ambiguity Test (meta-gate, override).** Final author self-check, applied as two questions:
1. Could a junior engineer or mid-tier AI, reading only this TestSpec (plus the layer's spec artifact and governing ADRs), write test code implementing every case as specified?
2. Could a reviewer, reading only this TestSpec, tell whether every equivalence class, every boundary, every error path was considered, without reading implementation or test code?

If either answer is No, the TestSpec is not done. This test overrides every Yes/No box; a TestSpec that passes shape checks but fails this one has not done the job a TestSpec exists to do.

**Derived-hard — coverage-mutation section presence.** Refuse to ship a TestSpec without the `coverage_mutation_bar:` block in front-matter. The block can carry placeholder values (project policy fills them later); its absence is hard. Soft-reject IDs (`structural-threshold-missing`, `mutation-threshold-missing`, `tool-unnamed`, `frequency-unnamed`) flag missing field values within the block.

These five refusals are deterministic. Do not relax under user pressure; surface the gap and offer the legitimate alternative.

## HALT conditions

Stop and hand back to the user when:

1. **Missing parent spec** — leaf without parent DD; branch without parent Architecture; root without Requirements + Product Brief. Refusal B fires when authoring proceeds without an upstream artifact. Ask for the parent spec.
2. **Missing derived_from / verifies sources** — `derived_from` cannot be empty; `verifies` cannot be empty at artifact level. Ask which spec elements this TestSpec is verifying before proceeding.
3. **Scope creep beyond one TestSpec** — request expands to also author Requirements / Architecture / ADR / Detailed Design / code or test code. Decline; emit `[NEEDS-...]` stubs and name the right artifact for the expanded ask.
4. **Locked-refusal override request** — user asks to populate retrofit `title`/`notes` from intent, mark reconstructed `verifies` as `verified`, write a qualitative `expected`, ship without `coverage_mutation_bar`, or skip the Spec Ambiguity Test. Halt and explain.
5. **Retrofit posture conflict** — `recovery_status` declared but no source-test references provided, or source tests provided but no `recovery_status` declaration. Halt and ask which posture applies.
6. **Three turns no info** — three back-and-forth turns without the user supplying a missing input from §Inputs. Halt with a structured handover.
7. **Irresolvable contradiction in input** — for example, a parent DD postcondition that contradicts a derived requirement. Do not pick a side. After two clarification turns without resolution, halt.

When halting, produce a structured handover: what was authored so far, what is missing, what specific human input or upstream decision is required to proceed.

## Mode flags

Two orthogonal flags drive which references load and which case template applies:

- **Layer.** Leaf → load `dd-traceability-cues.md`, use `case-leaf.yaml.tmpl`. Branch → load BOTH `architecture-traceability-cues.md` (Composition + interface seam) AND `requirements-traceability-cues.md` (behavioural seam against branch Requirements), use `case-branch.yaml.tmpl`. Root → load BOTH `requirements-traceability-cues.md` (Requirements + PB outcomes seam) AND `architecture-traceability-cues.md` (root Composition seam), use `case-root.yaml.tmpl`.

- **Greenfield vs Retrofit.** Greenfield → omit `recovery_status` from front-matter; skip Step 9; cases derived from spec only. Retrofit → declare `recovery_status` (per `verifies` link); apply Step 9; pair every reconstructed `verifies` with `recovery_status: unknown` and every `unknown` with a follow-up owner.

## Self-check before delivering

Before declaring the document complete, work through `references/quality-bar-checklist.md`. Items that cannot be answered Yes are flagged inline, not silently passed. The Spec Ambiguity Test is the override gate.

## File layout produced by this skill

```
{output-path}/testspec.md
```

That's it — one file. The skill does not create directories, schemas, validators, or sibling artifacts.

## Reference index

- `references/authoring-discipline.md` — 6 cross-cutting rules (product-shape, layering, compression) — applies to all authoring steps
- `references/testspec-purpose-and-shape.md` — V-model placement, derivation source per layer, pre-code authoring discipline
- `references/derivation-strategies.md` — eleven strategies (functional / boundary / error / fault-injection / property / state-transition / contract / performance / security / accessibility / error-guessing) plus ECP and decision tables
- `references/per-layer-weight.md` — three case shapes (thin leaf, fixtures-rich branch, journey-narrative root)
- `references/case-quality.md` — F.I.R.S.T., AAA, oracle specificity, determinism (clocks, random seeds)
- `references/verifies-traceability.md` — non-empty at artifact and case; resolution; granularity per layer
- `references/test-double-discipline.md` — five named double types; fake → contract test; max two per leaf; interaction-verification reserve
- `references/coverage-mutation-bar.md` — required artifact-level declaration block; placeholder values; line/mutation gap
- `references/integration-and-system-specifics.md` — contract testing, environment shapes, specialised cases (perf/sec/a11y), version pinning
- `references/retrofit-discipline.md` — honest posture; spec-first then map existing; `recovery_status: unknown` on reconstruction; gap report
- `references/dd-traceability-cues.md` — leaf seam: error matrix → robustness, postcondition → contract, invariant → property, state machine → state-transition, `[NEEDS-TEST: ...]` markers
- `references/architecture-traceability-cues.md` — Architecture-Composition seam: interfaces → integration, composition invariants → cross-child property, QA allocations → specialised, resilience strategies → fault-injection. Loaded at branch (alongside requirements-traceability-cues.md) and at root (alongside requirements-traceability-cues.md, for root Composition coverage).
- `references/requirements-traceability-cues.md` — Requirements + PB seam: functional REQ → ≥1 case, NFR five-element → measurable specialised, interface five-dimension → contract or integration, PB outcomes (root only) → user-journey. Loaded at branch (against branch Requirements) and at root (against root Requirements + PB).
- `references/anti-patterns.md` — 13 anti-patterns with name + tells + fix; hard-rejects marked
- `references/quality-bar-checklist.md` — eight QB groups + SAT meta-gate Yes/No checklist
- `templates/test-spec.md.tmpl` — full document scaffold
- `templates/case-leaf.yaml.tmpl` — thin leaf case
- `templates/case-branch.yaml.tmpl` — branch case with preconditions / steps / cross-child observable
- `templates/case-root.yaml.tmpl` — root case as user-journey narrative
- `templates/coverage-mutation-bar.yaml.tmpl` — front-matter slot
- `templates/retrofit-stub.yaml.tmpl` — retrofit case scaffold with `# HUMAN-ONLY` markers
- `examples/good-leaf-expiry-calculator.md` — worked example, leaf scope, eight cases across strategies, populated bar
- `examples/bad-orphan-and-fabricated.md` — counter-example with annotated refusal trips
