# Dependency Inference Rules

Rules for deriving `depends_on` edges and `strength` values in tasks.yaml.

---

## Governing principle

The dependency graph must be derivable from spec artifacts without human
annotation. The two primary sources are (1) interface-production relationships
declared in Architecture artifacts, and (2) ordering constraints in ADRs.
When neither source provides clear evidence, the dependency is either absent
or `strength: helpful` — never promoted to `critical` on inference alone.

---

## Rule 1: Interface-production (critical)

**Trigger:** A leaf's DD cites an interface produced by another leaf, or the
parent Architecture's Decomposition section names consumer/producer
relationships between children.

**Detection pattern:** Load the leaf's `parent_architecture` artifact. In the
Architecture's Decomposition or Interfaces section, locate entries of the form:
- `produces: [<iface-id>]` on one child
- `consumes: [<iface-id>]` on another child
- Or narrative text: "X depends on Y's `<method>` / `<type>` / `<endpoint>`"

If leaf A consumes an interface produced by leaf B:
- Add edge: A `depends_on` B, `strength: critical`.

`critical` means: A cannot be built or tested without B's implementation being
available. The build orchestrator must schedule B before A.

**Scope:** Only intra-sibling interfaces from the same parent Architecture
are in scope here. Cross-branch dependencies require the Architecture at the
common ancestor to declare them.

---

## Rule 2: ADR-ordering signals (helpful)

**Trigger:** A governing ADR contains language that implies sequencing between
implementation scopes.

**Detection signals** (look for these phrases or semantics in the ADR body):

| Signal phrase | Interpretation |
|---|---|
| "must be implemented before" | explicit ordering → `strength: helpful` |
| "depends on the existence of" | existence dependency → `strength: helpful` |
| "migration step N precedes step M" | migration ordering → `strength: helpful` |
| "cannot be rolled out until X is stable" | stability gate → `strength: helpful` |
| "schema must be deployed first" | deploy-order dependency → `strength: helpful` |

ADR-derived edges use `strength: helpful` because:
- ADRs rarely specify whether the ordering is a hard build-time constraint
  or a deployment/rollout preference.
- Promoting ADR-ordering to `critical` would incorrectly block parallel build
  execution for what may be a deployment concern only.
- If the human knows the constraint is hard, they can promote the edge in
  the emitted tasks.yaml before running the orchestrator.

**Cross-ADR inference:** If multiple ADRs govern the same leaf, check each
independently. Union the edges; do not deduplicate silently — preserve
all ADR-ids in the rationale.

---

## Rule 3: Ambiguity protocol

**Trigger:** An interface appears in a parent Architecture but no explicit
consumer is named, OR a DD's `derived_from` list references an artifact from
another leaf scope without a matching Architecture Decomposition entry.

**Action:**
1. Do NOT add a `critical` edge.
2. Add a `helpful` edge (if there is reasonable inference that ordering
   matters) OR omit the edge (if no ordering evidence exists at all).
3. Record the ambiguity in the plan report section of the SKILL.md output.
4. The ambiguity entry must name: the leaf scope, the interface or artifact
   reference that is unclear, and the Architecture artifact where the
   relationship should be clarified.

**Rationale:** Fabricating a `critical` edge blocks parallel execution
unnecessarily and may introduce false ordering that the human then inherits
as a constraint they did not intend.

---

## Rule 4: Cross-branch dependencies

**Trigger:** Leaf A is under scope `billing/` and its DD references an
interface from a leaf under scope `auth/`. These are siblings at the `auth/`
and `billing/` branch level, not under the same parent Architecture.

**Action:** Look for the interface declaration in the common ancestor's
Architecture artifact (e.g., the root `architecture.md`). If found and the
consumer/producer relationship is named → apply Rule 1 normally.

If not found in any Architecture artifact → ambiguity protocol (Rule 3).
Do not infer cross-branch `critical` edges from DD `derived_from` references
alone.

---

## Rule 5: `derived_from` is not sufficient for `critical`

A leaf DD that lists another leaf's artifact in its `derived_from` front-matter
field does NOT automatically generate a `critical` dependency. `derived_from`
records intellectual lineage (this DD was shaped by that artifact), not a
build-time dependency.

`critical` requires evidence that A's implementation cannot compile, link, or
be tested without B's implementation present.

---

## Strength summary

| `strength` | Meaning | Source |
|---|---|---|
| `critical` | A cannot build/test without B present | Architecture interface consumer/producer |
| `helpful` | Prefer building B before A; not a hard block | ADR-ordering signals, ambiguous interface inference |
| `optional` | Informational only; orchestrator may ignore | Reserved for future use; not emitted by this skill |

---

## Complexity heuristic

Assign `estimates.complexity` per leaf using these signals:

| Signal | Complexity |
|---|---|
| DD has > 5 public interface entries | high |
| DD has a state machine (State section non-trivial) | high |
| DD has error matrix with > 6 rows | high |
| DD has 3–5 public interface entries | medium |
| DD references 3+ governing ADRs | medium |
| DD has 1–2 public interface entries, no state machine | low |
| DD references 0–1 governing ADRs, no state machine | low |

When signals conflict (e.g., 6 interface entries but 0 ADRs), take the
higher signal. Default when no DD content is parseable: `medium`.

---

## DEFER markers

[DEFER: The interface-production rule (Rule 1) currently relies on the
Architecture artifact's Decomposition section having explicit `produces`/
`consumes` annotations. Many real architectures use narrative prose. A
follow-up pass should add a prose-extraction heuristic that recognises
"X calls Y", "X reads from Y's store", "X subscribes to Y's events" as
implicit `helpful` edges. Until then, narrative-only Architectures will
yield fewer `critical` edges than optimal, which is safe-side failure
(more parallelism, not false serialisation).]
