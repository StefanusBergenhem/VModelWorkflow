# Architecture gap — cycle findings handoff (IGraphBuild → validation-engine)

**Surfaced by:** First review of `DD-validation-engine` (verdict: DESIGN_ISSUE, F-001/F-002, 2026-05-11)  
**Blocking:** `DD-validation-engine` cannot be brought to APPROVED until this is resolved.  
**Artifact to update:** `specs/architecture.md` — IGraphBuild interface + IValidate interface (or TraceabilityGraph type contract)

---

## The gap

`IGraphBuild.Build()` returns cycle findings as a separate out-parameter:

```
Build(set ArtifactSet) (TraceabilityGraph, []Finding, error)
```

`IValidate.Validate()` only accepts:

```
Validate(set ArtifactSet, graph TraceabilityGraph, mode ValidationMode) (<-chan Finding, error)
```

There is no path for the `[]Finding` from `Build` to reach `validation-engine`, which is
the **sole producer of finding-records** (REQ-006). A junior implementer cannot implement
both components without inventing a handoff mechanism the Architecture hasn't specified.

---

## Options

**(a) Embed `CycleFindings []Finding` in `TraceabilityGraph`.**  
Graph-builder populates the field during `Build`; `IGraphBuild` postcondition updated to
state that `TraceabilityGraph.CycleFindings` holds the cycle findings; `IValidate`
signature unchanged; validation-engine reads `graph.CycleFindings` in Pass 2 and
re-emits them on its channel. This is the cleanest option: cycle findings are a structural
property of the graph (detected during graph construction), so embedding them in the graph
type is the natural home.

**(b) Add `cyclefindings []Finding` to `IValidate.Validate()`.**  
`Validate(set, graph, mode, cyclefindings []Finding)` — cli-adapter passes the `[]Finding`
from `IGraphBuild.Build` directly to `Validate`. Keeps `TraceabilityGraph` as pure
topology. Adds an argument to the IValidate interface.

**(c) cli-adapter forwards cycle findings to emitter separately.**  
cli-adapter calls `emitter.EmitValidation` with a merged channel of validation-engine
findings + cycle findings. Conflicts with REQ-006 (validation-engine is sole producer
of finding-records); rejected.

**Recommendation: option (a).** Cycle findings are a structural property of the graph;
`TraceabilityGraph` is already the carrier of graph-derived information.

---

## Required Architecture changes (option a)

1. **`IGraphBuild` postcondition** — add: *"The returned `TraceabilityGraph.CycleFindings`
   field is populated with zero or more REQ-026-shaped Finding records for all cycles
   detected in `derived_from` (TRV-CYCLE-001) and `supersedes`/`superseded_by`
   (TRV-CYCLE-002) links within the provided ArtifactSet."*

2. **`TraceabilityGraph` type contract** — add field `CycleFindings []Finding` with
   invariant: *"Populated by graph-builder during Build; read-only to all consumers;
   empty when no cycles are detected."*

3. **`IValidate` postcondition** — update the sole-producer invariant to read: *"includes
   re-emission of cycle findings from `graph.CycleFindings`."*

Once the Architecture is updated, `DD-validation-engine` needs:
- Remove the `[DEFER-DD: graph-builder — ...]` marker in the Algorithms section
- Add an inline citation to the updated ARCH IGraphBuild postcondition for the cycle
  re-emission design

Then resubmit for review.
