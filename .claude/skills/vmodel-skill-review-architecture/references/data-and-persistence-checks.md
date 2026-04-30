# Data and persistence checks

Mirrors the author-side `data-and-persistence.md`. Quality-attribute allocation, consistency model, and cost are the load-bearing decisions; these checks make sure each is named explicitly rather than punted.

## check.qa.nfr-not-allocated (soft)

**Check that** every parent NFR (latency, throughput, availability, capacity) lands at either a Decomposition entry's `allocates:`, an Interface entry's `quality_attributes:`, or a cross-cutting composition commitment.

**Reject when** a parent NFR is named in the parent Requirements but does not land anywhere in this Architecture.

**Approve when** every parent NFR is traceable to a specific component, interface, or composition-level commitment, and the allocation table or per-element block makes the trace explicit.

**Evidence pattern:** name the orphaned NFR id; list which children/interfaces/composition commitments were checked.

**recommended_action:** *"Allocate the NFR to a component, interface, or composition-level commitment. NFRs that do not land are NFRs that are not built to."*

## check.qa.budget-not-allocated-to-interface (soft)

**Check that** latency / throughput / availability budgets are allocated to specific interfaces (or runtime units), not left at a system-wide level.

**Reject when** the document states "p95 ≤ 1200 ms end-to-end" without breaking the budget down per hop (gateway / cart orchestration / pricing / inventory / PSP / commit / buffer).

**Approve when** the budget is broken down per hop or per interface, and the per-hop budget appears in each Interface entry's `quality_attributes:`.

**recommended_action:** *"Decompose the system-wide budget into per-interface budgets. A system-level budget without per-hop allocation cannot be designed against."*

## check.qa.consistency-model-not-specified (soft)

**Check that** every data path in the document names a consistency model: strong / read-your-writes / bounded staleness / eventual.

**Reject when** the document names a database (or shared store) without stating the consistency model per read path; OR names "eventual consistency" without a reconciliation story; OR uses different consistency models on different paths without distinguishing them.

**Approve when** consistency is named per data path, with reconciliation stated for any non-strong path, and the staleness window is concrete (≤ N seconds).

**recommended_action:** *"State the consistency model per data path: strong / read-your-writes / bounded staleness / eventual. Pair every non-strong path with a reconciliation story; eventual without reconciliation is a bug factory."*

## check.qa.cost-model-missing (soft, root only)

**Check that** at root scope (`parent_scope: null`), the document names the cost envelope, the cost-per-request target, and the cost-of-a-9 (the marginal cost of the next 9 of availability).

**Reject when** root scope and any of the three are absent.

**Approve when** all three are stated with concrete numbers (or a documented "out of scope at this iteration" decision with the trade-off cost named).

**Conditional gating:** applies only when `parent_scope: null`.

**recommended_action:** *"Add the cost model: envelope, cost-per-request target, cost-of-a-9. A well-engineered architecture killed by the bill is a category of failure the artifact is meant to prevent."*

## What this file does NOT cover

- Multi-tenancy isolation tier review (row / schema / database / deployment) — flagged as part of the Quality Bar gate's data card; no dedicated check id.
- DB-per-service vs shared review — captured by `anti-pattern.distributed-monolith` (where shared DB is one of the smell tells).
- Read-replica / CQRS choice review — captured at the Quality Bar gate level (not a stand-alone check; absence is informational unless read-traffic dominance is documented in the parent Requirements).

These are review surfaces but not catalog ids; flagged in the Quality Bar gate when the Yes/No item fails.

Cross-link: `quality-bar-gate.md` (Quality-attribute and Data cards); `anti-patterns-catalog.md` (distributed-monolith); `composition-patterns-checks.md` (message-bus topology, where event-sourcing is in play).
