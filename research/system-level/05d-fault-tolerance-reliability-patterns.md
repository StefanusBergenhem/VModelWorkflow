# Research 5d: Architectural Patterns for Fault Tolerance and Reliability

Research for architecture craft documentation. Covers how to design systems that handle
failure gracefully — redundancy, isolation, degradation, recovery, and what genuine
independence actually requires.

**Sources used:**
- [src-msft-bulkhead] Microsoft Azure Architecture Center: Bulkhead Pattern
- [src-sds-resilience] System Design Space: Fault Tolerance Patterns (Circuit Breaker, Bulkhead, Retry)
- [src-bmc-redundancy] BMC Blog: N-Modular Redundancy Explained (N, N+1, 2N, 3N/2)
- [src-aws-degradation] AWS Well-Architected Reliability Pillar: REL05-BP01 Graceful Degradation
- [src-sei-robustness] SEI CMU Blog: Tactics and Patterns for Software Robustness
- [src-arxiv-survey] arXiv:2404.10509v1: Dependability in Embedded Systems Survey
- [src-aws-retries] AWS Builder's Library: Timeouts, Retries, and Backoff with Jitter
- [src-lerus-cmf] Lerus: Common Mode Failure — A Critical Challenge in Redundant Systems
- [src-unleash-featureops] Unleash Blog: Graceful Degradation with FeatureOps

---

## 1. The Design Ordering Principle: Eliminate Before Tolerating

The most expensive mistake in building reliable systems is reaching for runtime mechanisms
before exhausting simpler options. Fault tolerance mechanisms add complexity — and complexity
is itself a failure source. The correct order is:

1. **Eliminate the problem by design.** If a component can't fail because it doesn't exist,
   no runtime mechanism can beat that. Remove unnecessary dependencies. Simplify interfaces.
   Design out the failure modes that matter most.

2. **Reduce by design.** Where the problem can't be eliminated, reduce its probability
   through design choices: using mature, well-tested components instead of experimental ones;
   avoiding distributed calls where local ones suffice; using synchronous communication where
   ordering matters and you can afford the coupling.

3. **Add a runtime mechanism.** When a failure mode remains after design-level options are
   exhausted, add detection and recovery: circuit breakers, bulkheads, retries, redundancy.
   These are the right tools at this stage — but only at this stage.

4. **Add monitoring.** Observability tells you whether failures are happening and whether
   your mechanisms are working. Monitoring doesn't prevent failures; it makes them visible.

5. **Add procedural workarounds.** Runbooks, manual overrides, operational drills. These
   are the last line of defense, not the first.

This ordering is not domain-specific. It applies equally to reliability, performance, security,
and testability. A system with fewer moving parts is more reliable than one with clever
recovery mechanisms patched over an unnecessarily complex design.

The SEI CMU taxonomy frames this as fault prevention → fault removal → fault tolerance
[src-sei-robustness]. The arxiv survey characterises it as detection, tolerance, and recovery
[src-arxiv-survey]. The underlying logic is the same: eliminate first, tolerate only what
remains.

**Cost implication.** Each layer of the hierarchy is more expensive than the one above it.
Eliminating a failure mode in design costs near-zero at runtime. A redundant subsystem costs
hardware, energy, deployment infrastructure, and ongoing verification. The hierarchy is also
a cost optimisation strategy.

---

## 2. Redundancy Patterns

Redundancy is the fundamental mechanism of fault tolerance: "adding extra hardware, software,
information, or time to ensure the system can withstand faults" [src-arxiv-survey]. The
trade-off is unavoidable — redundancy adds complexity, which is itself a source of failures.
Choose the level of redundancy the risk profile justifies, not the maximum possible.

### 2.1 Active vs. Passive vs. Load-Sharing

**Active redundancy**: All redundant components run simultaneously and process the same inputs.
Failures are detected immediately by comparing outputs or by voting. No switchover delay.
Cost: full resource consumption at all times.

**Passive (standby) redundancy**: One component handles all work; the spare is inactive until
a failure is detected. Lower resource cost at steady state. Cost: switchover time, state
transfer complexity, and risk of the spare being stale or untested.

**Load-sharing**: Redundant components share the normal workload. Capacity is available for
failover because each is normally operating below capacity. Intermediate cost and complexity.

The BMC taxonomy adds a practical refinement: patterns using extra capacity (+N) differ from
those doubling all capacity (2N). In N+1, one spare protects N active nodes — cheaper but
less robust against correlated failures. In 2N, full capacity runs in reserve — the most
costly but eliminates single-point exposure [src-bmc-redundancy].

### 2.2 Active/Active Architecture

Multiple instances handle requests simultaneously, typically load-balanced. Failure of one
instance removes it from rotation; others absorb the load. Provides both redundancy and
horizontal scale [src-bmc-redundancy].

When to use: stateless services, or services where state can be distributed or replicated.
Not suitable for stateful workloads where consistency requires a single writer without
careful coordination.

### 2.3 Active/Passive Architecture

One primary handles all requests; one or more secondaries sit in standby. The secondary
monitors the primary (heartbeat, health check). On failure detection, the secondary promotes
and takes over [src-bmc-redundancy].

When to use: stateful workloads where a single writer simplifies consistency; when switchover
latency is acceptable.

Trade-off: the standby may be stale (state not fully replicated at the moment of failure).
The SEI names this the state resynchronisation problem; it must be solved explicitly, not
assumed away [src-sei-robustness].

### 2.4 N-Modular Redundancy and Voting

Triple Modular Redundancy (TMR) runs three identical components in parallel and applies
majority voting to select the correct output. A single component failure is masked in
real-time — the faulty output is outvoted. The arxiv survey describes this as a "2-of-3
system" [src-arxiv-survey]. The SEI names it the canonical example of the Voting tactic
[src-sei-robustness].

N-Version Programming extends this to software: N independently developed versions execute
the same specification, and a voter selects the consensus output. "A voter selects the
correct output, eliminating the need for acceptance test" [src-arxiv-survey].

**Critical constraint**: voting only masks a failure if the versions fail independently.
If they share a specification, developer, or algorithm, they share failure modes. See
Section 7 for the independence problem.

Trade-offs: TMR requires 3x resources. Energy, cost, and complexity all scale with N.
Determining which node is faulty when outputs diverge requires additional logic. The SEI
notes "substantial hardware costs, energy consumption, and complexity determining active
node status" [src-sei-robustness].

### 2.5 Recovery Blocks

An alternative to voting: run the primary implementation; check the output against an
acceptance test; if it fails, run a backup implementation. Versions execute sequentially
(low steady-state cost) or in parallel (lower latency, higher cost). The arxiv survey
describes this as combining "checkpoint and restart with multiple software versions"
[src-arxiv-survey].

Trade-off: sequential execution adds latency on the failure path. Acceptance tests must
be independent of the implementation — if they share assumptions, they share failures.

---

## 3. Isolation and Containment

The goal of isolation is to bound the blast radius of any single failure. A fault that
cannot propagate is a fault that cannot escalate into a system-wide outage.

### 3.1 The Bulkhead Pattern

Named after the watertight compartments in a ship's hull: if one section floods, only
that section is lost [src-msft-bulkhead]. In software, a bulkhead partitions shared
resources so that a failure consuming resources in one partition cannot starve others.

The canonical implementation is separate resource pools (thread pools, connection pools,
semaphores) per dependency. If Service A fails and all connections to it are blocked,
only the pool assigned to Service A is exhausted. Services B and C continue normally
[src-msft-bulkhead].

Bulkheads apply at multiple levels:
- **Thread/connection pool isolation** per downstream service (consumer-side)
- **Service instance isolation** — deploying services to separate VMs or containers
- **Tenant isolation** — separate resource partitions per customer to prevent noisy
  neighbor effects
- **Queue isolation** — separate message queues per workload type

The system-design perspective distinguishes bulkheads from circuit breakers by scope:
"Bulkhead pattern is better suited for addressing performance and capacity issues, while
the circuit breaker pattern is better suited for addressing availability and fault tolerance
issues" [src-sds-resilience]. They are complementary, not alternatives.

**When not to use**: when the added complexity and resource overhead outweigh the isolation
benefit. Not every service warrants full pool partitioning [src-msft-bulkhead].

### 3.2 Process and Container Isolation

Deploying services in separate processes or containers provides isolation at the OS level:
memory faults, runaway CPU consumption, and crashes in one service cannot directly corrupt
another. Containers offer "a good balance of resource isolation with fairly low overhead"
[src-msft-bulkhead].

This is a design-level form of bulkheading — partition boundaries enforced by the runtime,
not by application logic.

### 3.3 Failure Domains

A failure domain is the set of components that share a single point of failure. Designing
explicitly for failure domains means:
- Knowing which components share power, network, rack, or availability zone
- Placing redundant components in different failure domains
- Ensuring that a single infrastructure failure cannot take out all copies of a service

Failure domain analysis is the architectural activity that turns "we have two instances"
into "we have two instances that actually fail independently."

### 3.4 The Cascade Failure Problem

Resource exhaustion is the primary mechanism of cascade failures. A slow or failing
downstream service causes callers to hold open connections or threads waiting for
responses. Those accumulated waits exhaust the caller's resource pool. The caller then
begins to fail its own callers, propagating the failure upstream [src-msft-bulkhead].

Circuit breakers (Section 4) and bulkheads address this from different angles: circuit
breakers stop sending requests once failure is detected; bulkheads limit how much of
the system's total resources any one failing dependency can consume.

---

## 4. Monitoring and Detection

Detection is a prerequisite for recovery. A system cannot respond to a failure it has
not detected. The SEI taxonomy organises detection tactics into a distinct category,
separate from prevention and recovery [src-sei-robustness].

### 4.1 Detection Tactics

- **Ping/echo**: Send a message, expect a response within a deadline. Simple, widely used.
  Tests reachability and basic liveness.
- **Heartbeat**: Monitored component sends periodic messages to a supervisor. If the
  heartbeat stops, the supervisor infers failure. Inverts the ping/echo direction — the
  monitored component is responsible for signalling health.
- **Health checks**: Richer than ping — verify that the service can perform its actual
  function (query a database, write to a queue) rather than just that it responds.
- **Watchdog timers**: A hardware or software timer that must be periodically reset by
  the monitored component. If the timer expires, the watchdog triggers a reset or alert.
  Tests that the component is making forward progress, not just alive [src-arxiv-survey].
- **Voting**: Compare outputs from redundant components. Divergence indicates a fault.
  Requires redundancy to be in place.
- **Sanity/reasonableness checks**: Validate that outputs are within expected ranges
  (rate of change, value bounds, sequence). Detects data corruption that would not
  appear as a component crash [src-sei-robustness].
- **Timestamp / sequence checking**: Detect incorrect ordering of events in distributed
  systems [src-sei-robustness].

### 4.2 The Circuit Breaker

The circuit breaker is both a detection mechanism and a response mechanism. It sits
between a caller and a downstream dependency and monitors the health of the interaction.

Three states [src-sds-resilience]:
- **Closed**: Requests flow normally. The breaker counts errors and latency violations.
- **Open**: Error rate has exceeded threshold. Requests are rejected immediately without
  attempting the downstream call. Fails fast.
- **Half-open**: After a configured delay, probe requests test whether the dependency has
  recovered. If probes succeed, the breaker returns to Closed. If they fail, it returns
  to Open.

The core value: once a dependency is failing, continuing to send it full traffic makes
recovery harder (adds load) and wastes caller resources. The open state stops the feedback
loop [src-sds-resilience].

Trade-off: the circuit breaker introduces modal behaviour — the system behaves differently
depending on state. This is harder to test and reason about. The AWS Builder's Library
recommends using circuit breakers "cautiously" precisely because "they introduce modal
behavior difficult to test" [src-aws-retries].

**Distinguishing detection from response**: the circuit breaker detects failures through
error counting and opens automatically. But it also responds — by rejecting requests fast.
This dual role is the source of both its value and its complexity.

---

## 5. Graceful Degradation

A fully functional system degrades to fully failed when any critical component fails.
A gracefully degrading system loses capability incrementally — shedding non-essential
functions while keeping essential ones running.

### 5.1 Hard vs. Soft Dependencies

The AWS Well-Architected framework provides the clearest framing: hard dependencies
cause complete failure when the dependency is unavailable. Soft dependencies detect
dependency failures and work around them. Graceful degradation is the architectural
practice of converting hard dependencies into soft ones [src-aws-degradation].

Example: an e-commerce landing page that shows personalised recommendations, ranked
products, and order status. If the recommendation service fails, a hard dependency
produces an error page. A soft dependency shows the page without recommendations —
top products and order status continue to work [src-aws-degradation].

### 5.2 Essential vs. Non-Essential Functions

The first design step is identifying which functions must work for the system to deliver
core value, and which are enhancements. This is not a technical question — it requires
understanding user needs and business requirements.

The SEI Robustness tactic for this is **Graceful Degradation**: "Maintains critical
functions while dropping non-essential ones" [src-sei-robustness].

Failure to make this explicit produces systems where every dependency is treated as hard,
and the first failure takes down everything.

### 5.3 Fallback Strategies

When a dependency is unavailable, options include [src-sds-resilience]:
1. **Graceful degradation**: Disable secondary features while preserving core flows
2. **Stale cache**: Return last valid data with freshness metadata
3. **Queue + async recovery**: Accept operations into queues for post-recovery processing
4. **Safe defaults**: Serve fallback responses for non-critical paths

A critical constraint from the AWS framework: "Fallback pathways taken during component
failure need to be tested and should be significantly simpler than the primary pathway"
[src-aws-degradation]. If the fallback is complex, it will fail for different reasons than
the primary, and now you have two failure modes instead of one.

The AWS framework also notes a counterintuitive point: "Generally, fallback strategies
should be avoided — focus on graceful degradation instead." The distinction is subtle but
important. A fallback implies a parallel path that serves as a substitute. Graceful
degradation implies the primary path continues with reduced scope. The latter is simpler
and more reliable [src-aws-degradation].

### 5.4 Feature Flags for Degradation Control

Feature flags provide runtime control over which features are active, allowing degradation
to be a deliberate operational action rather than an emergent accident. A kill switch is
a feature flag whose sole purpose is to disable a capability — it can be activated
instantly, targeted to specific regions or user segments, and reversed without deployment
[src-unleash-featureops].

This gives operations teams a lever that is faster than a redeployment and more precise
than a full rollback. A payment provider failure can be isolated with a kill switch in
seconds, keeping the rest of the API responsive.

The automation angle: error rates and latency thresholds can trigger flag changes
automatically, enabling self-degrading systems that reduce their feature surface
proportionally to detected stress [src-unleash-featureops].

---

## 6. Recovery Patterns

Recovery is the process of returning a system to a known good state after a failure.
The key insight is that recovery must be designed, not assumed. A system that has no
explicit recovery path will either stay failed or recover in unpredictable ways.

### 6.1 Retry with Exponential Backoff and Jitter

Retry assumes the failure is transient — the dependency will recover if given time.
The mechanism is simple; doing it correctly is not.

**Exponential backoff**: After each failed attempt, double the wait before the next
attempt. This gives the downstream service time to recover without continuous hammering.

**Jitter**: Without jitter, all clients that failed simultaneously will also retry
simultaneously — producing a synchronised retry storm that makes recovery harder.
Adding randomness to the wait spreads retries over time [src-aws-retries].

**The retry storm problem**: In a five-layer call stack where each layer retries three
times, a single database failure produces 3^5 = 243x the normal load at the database
during the failure window. "This multiplicative effect prevents system recovery"
[src-aws-retries]. Solutions: retry only at one architectural layer, cap total retries
with a token bucket, or use circuit breakers to stop retrying once failure is confirmed.

**Idempotency requirement**: Side-effecting operations (creating a record, charging a
payment) are only safe to retry if the API guarantees idempotent behaviour — calling
it twice produces the same result as calling it once. Non-idempotent operations must
not be retried without this guarantee [src-aws-retries].

**Timeout values**: Choose timeouts based on the latency distribution of the downstream
service. "Look at the corresponding latency percentile on the downstream service"
matching your acceptable false-timeout rate [src-aws-retries]. Too short and you time
out on legitimate slow responses; too long and you accumulate blocked resources.

### 6.2 Checkpoint and Restart

For long-running processes, checkpoint and restart stores the last known-good state
to stable storage. On failure, the process restores from the checkpoint rather than
restarting from scratch.

Two variants [src-arxiv-survey]:
- **Static restart**: Returns to a predetermined fixed state (faster, less state to store)
- **Dynamic restart**: Restores from the most recently created checkpoint (more recent
  recovery point, more complex)

The SEI names the recovery pair: **Rollback** (revert to known good state on failure
detection) and **State Resynchronisation** (for active/passive redundancy, ensure the
standby has current state before takeover) [src-sei-robustness].

### 6.3 Process Pairs

Two instances of the same software run on separate processors (or separate hosts).
The primary generates output and periodically writes checkpoint data. The secondary
monitors the primary and loads the last checkpoint on failure. On failure detection,
the secondary takes over from the last checkpoint [src-arxiv-survey].

This is the software-level equivalent of active/passive hardware redundancy. The
recovery time depends on checkpoint frequency and the cost of state transfer.

### 6.4 Escalating Restart

Not all failures require a full restart. The SEI names this tactic: vary restart
granularity to minimise service impact [src-sei-robustness]. Restart only the failed
component first. If that fails, restart the subsystem. If that fails, restart the
process. Full system restart is the last resort.

### 6.5 Shadow Mode Reintroduction

After a component has been repaired or replaced, returning it to full service
immediately risks reintroducing an unvalidated component under load. Shadow mode runs
the rehabilitated element in parallel with the primary, comparing outputs, before
cutting over. If outputs diverge, the rehabilitation has not fixed the underlying
problem [src-sei-robustness].

### 6.6 Self-Healing and Predictive Intervention

The SEI names a **Predictive Model** tactic: monitor health parameters identifying
potential future faults — intervene before failure occurs [src-sei-robustness].
Examples: restarting a component showing memory leak growth before it OOMs; migrating
workloads off a storage device with increasing error rates before it fails completely.

This shifts recovery from reactive (respond to failure) to proactive (prevent failure
after early warning is detected). It requires instrumentation and models of what
pre-failure signatures look like.

---

## 7. What Genuine Independence Means

The most dangerous assumption in fault-tolerant system design is that redundancy implies
independence. It does not. Two components that share a failure cause fail together,
defeating the purpose of redundancy entirely.

### 7.1 Common-Cause Failure

Common-cause failure (CCF) occurs when one event causes two or more supposedly independent
components to fail simultaneously. Common sources [src-lerus-cmf]:

**Specification-level**: If both components were implemented from the same requirements
document, and that document contains an error, both implementations will contain the same
error. A specification fault is a common cause for all components derived from it.

**Developer-level**: If the same developer or team wrote both implementations, they carry
the same assumptions, the same misunderstandings of the requirements, and the same coding
habits. Identical bugs appear independently in both versions.

**Algorithm-level**: If both versions use the same algorithm, they share the same edge-case
failures. The arxiv survey notes that N-Version Programming's voter-based approach works
only when versions fail independently — which requires independent development from
different specifications [src-arxiv-survey].

**Environmental**: Shared power supply, shared network segment, shared physical rack, shared
operating system — any common infrastructure is a common failure mode. Physical separation
and separate power feeds address this [src-lerus-cmf].

**Operational**: Misconfiguration applied to all instances simultaneously, a software upgrade
deployed to all nodes at once, human error during maintenance affecting all redundant
components.

### 7.2 Diversity as Independence

True independence requires diversity. Forms of diversity:

**Technology diversity**: Use different implementations, different libraries, different
languages. "Use diverse technologies (e.g., different manufacturers or designs) for redundant
components" [src-lerus-cmf]. Two Java implementations sharing the same JVM vulnerability
are not diverse. A Java primary and a Go secondary using different networking stacks are more
genuinely independent.

**Design diversity**: Implement the same specification using different algorithms. Hash-based
lookup and linear scan will not share algorithmic edge cases.

**Development team diversity**: Independent teams working from independent specifications.
This is expensive — it means writing the specification twice and staffing two teams. For
the highest-reliability components, it is the only option.

**Temporal diversity**: Execute the same computation at different times (time redundancy).
If the fault was transient, a delayed re-execution may succeed. This is the mechanism
behind simple retry [src-arxiv-survey].

### 7.3 The Shared Specification Problem

The arxiv survey draws the sharpest line: N-Version Programming "requires independent
development of versions and acceptance tests based on shared requirements"
[src-arxiv-survey]. The phrase "based on shared requirements" is the critical qualifier.
If two versions are both derived from the same requirement, and that requirement is wrong,
both versions will implement the wrong behaviour. The voting system will agree on the
wrong answer.

True diversity requires that the specifications themselves differ — different formulations
of the same intent, written independently, so that a misunderstanding in one does not
propagate to the other. This is harder to achieve than it appears and is often not done
even in systems that claim N-version diversity.

### 7.4 Common-Cause Failure Analysis

The design practice that makes independence explicit is common-cause failure analysis:
systematically ask, for each pair of redundant components, "what single event could
cause both to fail?" The answer reveals shared assumptions, shared infrastructure, and
shared failure modes that need to be broken.

FMEA (Failure Mode and Effect Analysis) is the structured technique for this
[src-lerus-cmf]. The output is not just a list of failure modes but an explicit map
of which components share which causes — the basis for deciding whether a claimed
independence is real.

---

## 8. Cost of Complexity and the Redundancy Paradox

Every pattern in this document adds complexity. Complexity is a failure source. This
creates a genuine tension: adding fault tolerance mechanisms can reduce reliability if
the mechanisms themselves introduce new failure modes.

The AWS Builder's Library is explicit: circuit breakers "introduce modal behavior
difficult to test" [src-aws-retries]. The SEI notes that "most robustness patterns
involve tradeoffs with other quality attributes, particularly performance and latency"
[src-sei-robustness]. The BMC analysis states that "higher redundancy levels demand
greater complexity, increased resource provisioning, and enhanced management overhead"
[src-bmc-redundancy].

The practical implication: apply fault tolerance mechanisms surgically, not uniformly.
Not every service needs a circuit breaker. Not every dependency needs a bulkhead. Apply
where the failure probability and impact justify the cost of the mechanism and the
operational complexity of managing it.

The design ordering principle from Section 1 is the discipline that keeps this under
control: exhaust simpler options before adding mechanisms.

---

## 9. Gaps and What the Sources Are Silent On

**Testing degraded modes**: Sources mention it (the AWS framework says degraded pathways
must be tested), but none provide detail on how to structure tests for partial failure
scenarios. This is a gap for a testing craft document.

**Chaos engineering**: The Unleash source mentions it in passing [src-unleash-featureops],
but none of the sources cover chaos engineering as a systematic practice (Chaos Monkey,
fault injection frameworks). That is a separate research topic.

**State management in active/active**: The sources describe active/active architecturally
but are thin on the mechanics of distributed state consistency under partial failure. The
CAP theorem and CRDT approaches are referenced implicitly but not covered.

**Quantitative reliability targets**: The sources discuss patterns qualitatively. None
provide guidance on mapping from a reliability target (e.g., 99.99% availability) to
a specific redundancy configuration. That requires quantitative reliability analysis
(Reliability Block Diagrams, Markov models) — outside the scope of these sources.

**Organisational independence**: The common-cause failure literature notes that team
independence is required for design diversity, but none of the sources address how to
practically achieve team independence in a delivery organisation with shared tooling,
processes, and management.
