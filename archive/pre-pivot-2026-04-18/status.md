# Session Status — Layered Model Redesign

**Date:** 2026-04-18
**Nature:** Strategic redesign conversation. User is pivoting VModelWorkflow from the current safety-heavy, HW/SW-split V-model framing toward a cleaner "real software world" layered model that keeps V-model learnings but drops what doesn't serve AI-augmented spec-driven development.

---

## The Core Question Being Worked

How should the VModelWorkflow layered model be structured to:

- **Keep** V-model learnings: layered thinking, traceability, design-test coupling, artifact guidance, lessons.
- **Drop** safety as a main concern (to be revisited later if ever — only if complete, not halfway).
- **Drop** hard HW/SW split borrowed from aviation/automotive — this is real software, not embedded systems.
- **Improve** on the "spec-driven AI coding" market trend by adding V-model rigor.
- **Keep** the four project components: Documentation, Templates & Schemas, Traceability, AI Skills.
- **Resolve** the central tradeoff: AI efficiency (lean context) vs human-in-loop (anchoring to business value).

Discussion is running as interview-style back-and-forth, one question at a time, walking down the design tree resolving dependencies.

---

## What We Have Covered

### Q1 — Purposes of Layers (settled)

Load-bearing purposes of layering:
1. **Context economy for AI** — keep each step's context small enough for cheap/fast agents.
2. **Thinking discipline** — force decisions in order (what → how → build); each layer is a distinct kind of decision.
3. **Test-level mapping** — each layer produces a distinct test type.
4. **Change-isolation surfaces** — layer boundaries are stable contracts.
5. **Human comprehension chunks** — HARD CONSTRAINT. Without human understanding, AI drifts from business value.

Rejected: team/role boundaries (too team-shape-dependent).

Key insight from user: the AI-efficiency vs human-comprehension tradeoff is resolved *by layering itself* — explanation lives in the layer where it is authored and does not leak into AI context below.

### Q2 — Axis Defining Layers (settled)

**Decision: Option Y** — decision kind as the primary layer axis; structural scope is a tagged property, not a layer axis.

Rejected:
- **X** (structural scope only: product → app → component → unit) — creates ghost layers in small systems; runs out of names in large ones.
- **Z** (matrix of decision-kind × scope) — the V-model's implicit model; source of layer explosion.

Key concepts:
- **Structural scope** is a tree discovered from the system, with variable depth.
- Same verbs (decision kinds) apply at whatever depth the system needs.
- Scope is tagged on each artifact rather than encoded as a separate layer.

### Q3 — Fourth Decision Kind (settled)

**Decision: four decision kinds.** The fourth sits *only* at the root of the scope tree. At intermediate scopes the "reason to exist" is captured by the parent architecture's allocation plus the `derived_from` link — no separate anchor artifact is needed there.

The top layer is named **"Product Brief"** (after considering Intent, Stakeholder Needs, Product Charter; rejected "Stakeholder Requirements" due to naming conflict with the Requirements layer).

### Q4 — Product Brief Content (settled)

Seven sections:
1. **Stakeholders** — who has the problem, who pays, who uses, who blocks.
2. **Problem** — concrete evidence of pain/opportunity.
3. **Desired outcomes** — qualitative narrative of better future state per stakeholder group.
4. **Operational concept** — key scenarios, environments, integrations (ConOps folded in).
5. **Constraints** — regulatory, technical, financial, timeline bounds.
6. **Non-goals** — what we are explicitly *not* solving.
7. **Success criteria** — measurable indicators that outcomes were achieved.

### Q5 — Requirements Artifact (settled)

Six sections:
1. **Metadata** — scope, parent_scope, derived_from.
2. **Functional Requirements** — testable shall-statements (EARS preferred).
3. **Quality Attributes** — measurable non-functional targets.
4. **Interface Requirements** — external contracts.
5. **Data Requirements** — format, retention, privacy class.
6. **Inherited Constraints** — pointers to upstream constraints that apply here.

Per-requirement fields:
- `id` — required (traceability)
- `statement` — required
- `rationale` — required (can be terse — keeps human-in-loop anchor, enables tradeoffs, preserves "why" in retrofit)
- `acceptance` — optional (required only when statement alone leaves test conditions ambiguous)

### Q6 — Architecture Artifact (settled)

Five sections:
1. **Metadata** — scope, parent, derived_from, governing ADRs.
2. **Overview** — prose, 2-3 paragraphs. What this scope is, what slice of the parent it realizes, high-level approach.
3. **Structure diagram** — Mermaid, children + connections.
4. **Decomposition** — per-child entries.
5. **Interfaces** — contracts between children.

Optional: runtime view (sequence diagrams), cross-cutting concerns, deployment view (product scope only).

Per-child:
- `id`, `purpose` (one-line), `responsibilities` (architecture-level, not implementation), `allocates` (list of REQ-IDs).

Per-interface:
- `name`, `from`, `to`, `protocol`, `contract` (reference).

Decisions:
- **Diagram format**: Mermaid as default (text-based, version-controllable, AI-readable). Embedded images permitted where Mermaid is insufficient.
- **ADRs pulled out** as cross-cutting separate artifacts (not inlined in Architecture).

### ADR Artifact (settled)

Fields:
- `id`, `title`, `status` (proposed / accepted / superseded), `date`
- `scope_tags` — which scopes this primarily applies to
- `supersedes` / `superseded_by`
- `context` — situation addressed
- `decision` — what we chose
- `alternatives_considered`
- `rationale`
- `consequences`

Lives in a flat `/adrs` directory, cross-cutting across scopes.

### Q7 — Detailed Design at Leaf (settled, after user pushback)

**Initial proposal (rejected):** README-per-leaf. User pushback: insufficient for AI-augmented development — if the human only reviews code, they lose leverage and the AI drifts. Need a design-level artifact humans review and approve *before* code is written.

**Settled:** Detailed Design as distinct artifact type at leaves. Anchored in DO-178C Software Detailed Design / ASPICE SWE.3 / IEEE 1016 Software Design Descriptions.

Success criteria (the user's test):
- **Junior-dev-implementable** — someone unfamiliar can produce correct code from the design alone.
- **Language-portable** — same design produces equivalent code in Java, Python, Go.
- **Test-derivable** — unit tests can be written from the design, *before code exists* (true red-green TDD).

Eight sections:
1. **Metadata** — scope, parent_scope, parent_architecture, derived_from, adrs.
2. **Overview** — 2-3 paragraphs. What this leaf does, what parent slice it realizes, approach.
3. **Public interface** — every externally-visible function/class/type with contracts.
4. **Data structures** — internal data with invariants, ownership, lifetime.
5. **Algorithms** — pseudocode for the trickiest, prose for clearer. Decision tables for complex conditionals.
6. **State** (if applicable) — state machines (Mermaid), persistent state, side effects.
7. **Error handling** — what can occur, how detected, how propagated.
8. **Test strategy** — what unit tests cover, including boundary and error cases.

Per-function fields (Public interface — Design-by-Contract lineage, Meyer/Eiffel):
- `name`, `signature` (language-neutral: names + types)
- `description` (1-2 sentences)
- `preconditions`, `postconditions`
- `errors` (what can be raised, when)
- `side_effects`
- `complexity_notes` (if relevant)

Per-data-structure:
- `name`, `description`, `fields`, `invariants`.

### Implementation (settled)

**Implementation = code + unit tests.** No separate structured document. README-per-leaf is dropped — Detailed Design supersedes it.

**Tests derive from the Detailed Design**, not from the code. This enables true red-green TDD: design → test (fails) → code (passes) → refactor.

---

## Consolidated Artifact Set

| Type | Lives at | Job | Verified by |
|---|---|---|---|
| **Product Brief** | Root only | Anchor: why, for whom, what problem | Stakeholder review |
| **Requirements** | Non-leaf scopes | Testable behavior specifications | Acceptance tests |
| **Architecture** | Non-leaf scopes | Decomposition + structure | Integration tests |
| **ADR** | Cross-cutting | Justify individual decisions | Review |
| **Detailed Design** | Leaves | Internal logic, contracts, algorithms | Unit tests |
| **Implementation** | Leaves | Code + tests satisfying Detailed Design | Tests pass |

---

## Meta-Decisions Taken

- **Primary layer axis**: decision kind, not structural scope.
- **Structural scope**: discovered tree per system, variable depth.
- **Leaves**: where subdividing stops earning its keep (heuristic: if the next architecture doc would just say "these three helpers call each other," stop and write code).
- **Glue/wiring**: itself a leaf sibling at each non-leaf scope.
- **Deployment config** (Terraform / k8s / docker-compose): treated as product-scope wiring leaf.
- **Diagram format**: Mermaid default, embedded images where needed.
- **Safety**: removed as main concern; do not inject into base framework. Re-add later only if complete.
- **Naming**: "Architecture" (non-leaf) vs "Detailed Design" (leaf). "Design" as synonym flagged for terminology doc; final call still open.
- **README-per-leaf**: dropped. Detailed Design supersedes.
- **Tests at each layer derive from the artifact at that layer**, not from the code below. V-model verification, restored.
- **Human leverage point** is at the *design* level, not code review. If design is good enough, code review becomes optional.

---

## Heuristics Staked Out (Need Refinement When We Write Docs)

When to subdivide the scope tree further:
- **Depth test**: if the children interact in ways the parent's Architecture can't explain, go deeper.
- **Cognitive-load test**: a scope should fit in one R+A pair a reviewer can hold in their head.
- **Change-blast test**: if subdividing further wouldn't let parts change independently, you've gone too deep.

---

## Session-Level Directives (saved to memory)

- **Prefer proven concepts over inventions** — recommend established industry patterns first; flag novel synthesis explicitly; if no fit, discuss before inventing. (Saved as `feedback_prefer_proven_concepts.md`.)

---

## Remaining Questions (Ordered)

1. **Q8 — Test-level mapping.** How do tests fit at each layer (acceptance → R, integration → A, unit → DD)? Where do tests live physically? Is there a schema for test artifacts, or do tests live in the code repo only?
2. **Q9 — Traceability model.** Formal definition of links between artifacts: what fields, what validation rules, what rendering.
3. **Q10 — Artifact file shape.** Single-file Markdown (with YAML front-matter and embedded YAML/Mermaid blocks) vs split-file (`.yaml` + `.md` pair). Tooling implications either way.
4. **Q11 — Retrofit story.** How does bottom-up retrofit work with this model? How are leaves discovered from existing code? How is Detailed Design recovered from code without becoming generated pseudo-doc?
5. **Q12 — Rigor / assurance without safety.** How to express "this matters more" now that safety levels are removed. Candidates: blast-radius, business-criticality, reversibility, user-impact. Optional property on artifacts?
6. **Q13 — Naming revisit.** "Architecture" vs "Design" terminology — final call before docs get written.
7. **Q14 — Impact on existing plan.** What does this pivot mean for `docs/plan/BACKLOG.md`, `docs/plan/TARGET_ARCHITECTURE.md`, existing research docs, schemas, skills? Major rewrite likely needed.
8. **Q15 — Tooling.** Validation engine, link resolver, renderer — how does the current traceability design adapt to this new artifact set?

Proposed next step: **Q8 (test-level mapping)** — natural next branch since we've defined all artifact types and the V-shape verification strategy implies specific test types per layer, but we haven't yet specified how tests are themselves structured or placed.
