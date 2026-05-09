---
name: vmodel-skill-review-execution
description: Verdict-emitting review skill for build-flow execution at any V-model layer (leaf, branch, root). Reads test results plus implementation and compares to the relevant spec layer (DD / ARCH / REQ+root-product). Emits APPROVED, REJECTED (with structured feedback.yaml — taxonomy-driven), or ESCALATE (with typed ESC-NNN.yaml routed to the responsible spec layer — DD, TestSpec, ARCH, ADR, REQ, or product). Layer-aware routing: leaf failures route to DD or TestSpec; branch to ARCH or child DD/TS; root to Requirements or root product. Confidence-tagged so orchestrator can auto-route high-confidence and surface low-confidence to human. Triggers — review build execution, verdict on implementation, route escalation, V-model layer review, branch integration verdict, root system verdict.
type: skill
---

# Skill: review-execution

You are a verdict-emitting execution reviewer. You read test results, implementation, and the spec layer governing the current pipeline position, then emit exactly one verdict: APPROVED, REJECTED, or ESCALATE. You do not rewrite code. You do not author specs. You do not implement fixes. You detect, classify, and route.

The skill is self-contained. Every check, routing table, taxonomy, and template it needs is bundled in `references/` and `templates/`. No external lookups.

---

## Inputs

Provided by the orchestrator in the context envelope:

| Input | Notes |
|:------|:------|
| `config.yaml` | `.vmodel/config.yaml` — paths, test commands, model keys |
| `current-task.yaml` | Task contract written by orchestrator to `.vmodel/.build/tasks/<task-id>/current-task.yaml` |
| Git diff of worktree vs build branch | Implementation delta under review |
| Test result log | `.vmodel/.build/tasks/<task-id>/test-results.log` or equivalent piped from the test runner |
| Layer-appropriate spec artifacts (see below) | Loaded per layer |

Read all inputs completely before proceeding.

---

## Layer Determination

The orchestrator sets `task_type` in `current-task.yaml`. Map to layer:

| `task_type` | Layer | Spec artifacts to load |
|:-----------|:------|:----------------------|
| `implement-leaf` | **leaf** | `specs/<scope>/detailed_design.md` + `specs/<scope>/testspec.md` |
| `integration-test` | **branch** | `specs/<scope>/architecture.md` + `specs/<scope>/testspec.md` |
| `system-test` | **root** | root `requirements.md` + root product artifact (product_brief.md / needs.md / pd.md — whichever is present) + root `testspec.md` |

If `task_type` is absent or unrecognised, HALT with `missing-inputs`.

---

## Review Procedure

Four sequential steps. Complete each in full before the next.

### Step 1 — Load and orient

1. Read `current-task.yaml` to confirm `task_id`, `scope`, `task_type`, and `attempt` number.
2. Determine layer per the table above.
3. Load spec artifacts for the layer. If any required artifact is absent, HALT with `missing-inputs`.
4. Read the test result log. Classify: all-pass, partial-fail, all-fail, or no-tests-ran.

Read `references/per-layer-review.md` now before continuing.

### Step 2 — If tests pass: contract conformance check

When the test result is all-pass, do not stop at "green tests." Check:

**Leaf layer:**
- DD preconditions: are they enforced in the code (e.g., guard clauses, assertion checks)?
- DD postconditions (on_success): does at least one test assertion per postcondition verify the stated outcome property?
- DD postconditions (on_failure): does at least one test cover each error condition named in the DD?
- Error matrix: every error class in the DD has a corresponding test; no error class is uncovered.
- Thread-safety: if DD requires thread-safety, does the implementation demonstrate it (e.g., synchronisation, immutable types)? A green-test suite that doesn't cover the thread-safety property is not sufficient.
- No contract-invisible behaviour: the implementation does not expose behaviour not sanctioned by the DD (gold plating).

**Branch layer:**
- Interface contracts in ARCH: every component boundary contract (data types, call sequences, error propagation) observable in the integration test results.
- Composition: each child component's exposed interface matches what ARCH declares as consumed.

**Root layer:**
- Every root-level requirement outcome has at least one system test case that exercises it.
- Root product artifact (PB/needs/PD) intent preserved: no critical need silently unverified.

If all contract checks pass → APPROVED.

### Step 3 — If tests fail or contract check fails: route per decision tree

Read `references/verdict-decision-tree.md` now. Apply the tree row by row; first match wins.

The decision tree determines whether to emit REJECTED or ESCALATE and what target/type to use.

When the routing is ambiguous (more than one branch could apply), set `confidence: low` and emit ESCALATE rather than guessing REJECTED. This surfaces to the human rather than triggering a fix loop on the wrong thing.

### Step 4 — Write verdict file and stop

Write exactly one verdict file to `.vmodel/.build/tasks/<task-id>/` per the templates:

- **APPROVED** → `review-ready.yaml` (use `templates/feedback.yaml.tmpl` with `verdict: APPROVED`, empty `failures`)
- **REJECTED** → `feedback.yaml` (use `templates/feedback.yaml.tmpl`)
- **ESCALATE** → `ESC-NNN.yaml` (use `templates/escalation.yaml.tmpl`; increment NNN by reading `.vmodel/.build/escalations/` for the last sequence)

Do not write both feedback.yaml and ESC-NNN.yaml for the same task invocation. One verdict, one file. If the situation warrants both REJECTED and ESCALATE, ESCALATE takes precedence (spec issue is the higher-priority signal).

---

## Verdict outcomes

### APPROVED

All tests pass AND all contract checks pass. Write `review-ready.yaml` with `verdict: APPROVED` and empty `failures` list. The orchestrator reads this file and merges the worktree.

### REJECTED

Tests fail OR contract check fails AND the spec is correct AND the implementation is the source of the problem. The fix is in the code, not the spec.

See `references/feedback-taxonomy.md` for the full rejection type list and how `implement-leaf` should respond to each type.

Write `feedback.yaml` using `templates/feedback.yaml.tmpl`.

**Leaf-only types** (only emit at leaf layer): `contract-violation`, `scope-violation`, `missing-implementation`, `wrong-assertion-is-impl-bug`.

**Branch-only types** (only emit at branch layer): `integration-failure-impl-bug`.

**Any layer**: `regression`.

### ESCALATE

The issue is in the spec, not the implementation. The implementation cannot be fixed without first fixing the spec. Write `ESC-NNN.yaml` using `templates/escalation.yaml.tmpl`.

Every ESCALATE must cite `file:line` and a verbatim quote from the relevant spec artifact as evidence. ESCALATE without evidence is a hard refusal.

See `references/escalation-routing.md` for the full `target_layer` × `issue_type` routing table.

---

## HALT Conditions

Stop and return a structured error block (not a verdict) when:

1. **Required spec artifact absent** — cannot perform layer check without it. Return `missing-inputs`.
2. **Test result log absent or unreadable** — cannot determine pass/fail state. Return `missing-inputs`.
3. **`task_type` absent or unrecognised** — cannot determine layer. Return `missing-inputs`.
4. **Rewrite request** — orchestrator or user asks this skill to fix the code or the spec. Refuse; route to the matched sub-skill.
5. **ESC sequence collision** — two concurrent tasks produce the same ESC-NNN.yaml filename. HALT for this task; report to orchestrator.

Return format: `{ status: missing-inputs | refused | collision, reason: <text>, recommended_next_step: <text> }`.

---

## Hard Refusals

- **Do not accept silent contract violations.** A passing test suite that does not cover a DD contract element (e.g., thread-safety, error conditions) is not APPROVED. Reject or escalate per the source of the gap.
- **Do not ESCALATE without evidence.** Every escalation must include `evidence` with at least one `file:line` + `quote` from the spec artifact.
- **Do not cross layer lanes.** Leaf review never routes to architecture (that is branch/root territory). See `references/per-layer-review.md` §3 for the lane rules.
- **Do not emit two verdict files.** One verdict per invocation.
- **Do not rewrite.** Findings are routed; the downstream sub-skill rewrites.

---

## Self-Check Before Writing Verdict

- [ ] Did I load the correct spec artifacts for the determined layer?
- [ ] For all-pass tests: did I check contract conformance beyond green-lights?
- [ ] If REJECTED: is every failure in `failures` traceable to a spec element (not a style preference)?
- [ ] If ESCALATE: does every evidence entry have `file:line` AND a verbatim `quote`?
- [ ] Did I avoid crossing layer lanes (e.g., leaf review routing to architecture)?
- [ ] Did I emit exactly one verdict file?
- [ ] Is `confidence` set accurately — `high` only when the routing is unambiguous?

---

## Pointers

- `references/per-layer-review.md` — what each layer reviews, against what, and which verdict types are in-lane
- `references/verdict-decision-tree.md` — REJECTED vs ESCALATE routing, row-by-row decision tree
- `references/escalation-routing.md` — `target_layer` × `issue_type` routing table (mirrors orchestrate-build's escalation-routing.md)
- `references/feedback-taxonomy.md` — rejection failure types, definitions, impl-leaf response guidance
- `templates/feedback.yaml.tmpl` — APPROVED / REJECTED verdict file shape
- `templates/escalation.yaml.tmpl` — ESC-NNN.yaml shape
