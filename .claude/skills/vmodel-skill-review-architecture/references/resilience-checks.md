# Resilience checks

Mirrors the author-side `resilience-patterns.md`. Resilience is a property of composition, not of components. Six checks; all soft-reject. Absence of a single one accumulates with others to a REJECTED verdict.

## check.resilience.bulkhead-partitions-not-named (soft)

**Check that** for shared resources that matter (downstream-dependency thread pools, connection pools, semaphores), bulkhead partitions are named.

**Reject when** the document mentions or implies multiple downstream dependencies but does not name a per-dependency partition (cap, scope, resource type), so a single slow dependency can drain the global pool.

**Approve when** every partitioned shared resource has an entry naming the resource, what it is partitioned by, and the cap.

**recommended_action:** *"Name bulkhead partitions for cross-dependency resource pools. Without bulkheads, one slow dependency cascades into a global outage."*

## check.resilience.circuit-breaker-missing (soft)

**Check that** circuit breakers are placed at cross-service boundaries where caller exhaustion is a real failure mode.

**Reject when** the document describes synchronous calls to an external dependency (PSP, identity provider, third-party API) without a circuit-breaker entry covering the boundary.

**Approve when** every cross-service boundary with a meaningful failure mode has a circuit-breaker entry stating thresholds (open, half-open) and the rationale for placement.

**Conditional gating:** does NOT apply to internal tight loops where failing fast saves nothing.

**recommended_action:** *"Add a circuit breaker at the cross-service boundary. The value is not 'retry less' — it is stopping the feedback loop where a failing dependency exhausts its caller."*

## check.resilience.retry-policy-unspecified (soft)

**Check that** retry policy is specified for every retried interface: backoff, jitter, max attempts, and idempotency strategy.

**Reject when** the document mentions retries without specifying the backoff (exponential, linear, none), the jitter (full / equal / none), the max attempts, OR omits the idempotency strategy for side-effecting operations.

**Approve when** all four are stated per retried interface, with idempotency-key, conditional-write, dedup-store, or "n/a — read-only" named.

**recommended_action:** *"Specify retry backoff, jitter, max attempts, and idempotency strategy. Stacked retries (3^N) and storms without jitter are how downstream systems get rediscovered as load."*

## check.resilience.degradation-not-designed (soft)

**Check that** for every non-essential dependency, the document states the degradation strategy (degrade by omitting X / fallback to Y) with rationale.

**Reject when** non-essential dependencies are present (loyalty lookup, recommendation carousel, audit downstream) but the document is silent on what happens when they are unavailable.

**Approve when** every non-essential dependency has an `on_failure:` entry naming degradation or fallback, with rationale tying the choice to user-facing impact.

**recommended_action:** *"Decide degradation vs fallback per non-essential dependency. Default to degradation; fallback paths have their own failure modes that surface as new incident categories."*

## check.resilience.failure-domains-unnamed (soft)

**Check that** failure domains (process / host / availability zone / region / cloud provider) are named, and components are mapped to the domains they share.

**Reject when** the document does not state which failure-domain levels matter at this scope, OR does not state which components share which domains.

**Approve when** the relevant levels are enumerated and each component / runtime unit is mapped to the domains it shares with others.

**recommended_action:** *"Enumerate failure domains and map components to them. Without explicit domain mapping, blast-radius reasoning is wishful thinking."*

## check.resilience.redundancy-without-independence-property (soft)

**Check that** every redundancy claim (active-active, active-passive, hot-standby) is backed by a named independence property — the specific shared-cause path that is broken.

**Reject when** the document claims redundancy but states only the count ("3 replicas behind a load balancer") without naming what is NOT shared (binary, library version, deploy pipeline, AZ, region, provider).

**Approve when** every redundancy entry names the independence property concretely (e.g., "managed multi-AZ Postgres — independence at the AZ level for hardware and network failures; not independent against a bug in the same Postgres binary").

**recommended_action:** *"Name the independence property per redundancy claim. Redundancy without a named independence property is theatre — same binary, same library, same shared common cause."*

## Sweep order

Walk top to bottom. The first three are mechanical (look for partitions, breakers, retry blocks). The last three require judgment — what counts as "non-essential", whether the failure-domain enumeration is honest, whether the independence property is real or aspirational.

Cross-link: `quality-bar-gate.md` (Resilience card); `composition-patterns-checks.md` (sequence-diagram-failure-path); `anti-patterns-catalog.md` (distributed-monolith — common-cause failure across "redundant" services on the same DB).
