# Quality Bar — self-check before delivering

Yes/No checklist, grouped by concern. The artifact passes when every applicable item is answered Yes. Two cards are load-bearing and carry visual emphasis: **Composition completeness** (where silent omission has the largest blast radius) and the **Spec Ambiguity Test** (the meta-gate). Items that cannot be answered Yes are flagged inline in the artifact, not silently passed.

## Decomposition and boundaries

- [ ] Is every child's purpose stated in exactly one sentence without conjunctions?
- [ ] Does every child's responsibility list contain at most three items, each scoped at architectural (not implementation) level?
- [ ] Is every parent-allocated requirement named in at least one child's `allocates`? (No requirements orphaned.)
- [ ] Does every child `allocate` at least one requirement? (No components orphaned.)
- [ ] Has the one-sentence-responsibility test been walked per child (no hidden *and*s)?
- [ ] Has the depth / cognitive-load / change-blast trio been checked, with a record of which one fired if decomposition was revised?
- [ ] Where a bounded-context language fracture exists, is the child boundary drawn at the fracture?

## Interfaces and contracts

- [ ] Does every interface entry carry preconditions, postconditions (on success / on precondition failure / on downstream failure), invariants, a typed error enum, and quality attributes?
- [ ] Does every externally callable interface state authentication and authorisation requirements?
- [ ] Is every interface segregated by responsibility (no fat god-interfaces)?
- [ ] Does every versioned interface name its versioning scheme and deprecation policy?
- [ ] Is rationale carried on every interface (at least one line tying the choice to a requirement, ADR, or constraint)?
- [ ] Are externally-imposed protocols cited by specification (RFC, API spec, standard identifier), not informal name?

## Composition completeness — load-bearing **(meta-card)**

- [ ] Is the runtime pattern named explicitly (request-response / event-driven / pipeline / hexagonal / ...) rather than implied?
- [ ] Does every runtime pattern choice have a rationale (inline or `governing_adrs`)?
- [ ] Is the middleware stack ordered and stated (authN / authZ / rate limit / trace / ...)?
- [ ] Is the DI / composition-root strategy named?
- [ ] Is the message-bus topology specified where applicable (topics, partition keys, retention, dead-letter, consumer groups)?
- [ ] Does every critical flow (happy path plus one or two failure paths) have a sequence diagram?
- [ ] **At root scope:** are environments, orchestration target, and runtime-unit boundaries named?
- [ ] **At root scope:** does deployment intent resolve to concrete IaC artifacts (by reference) or explicitly planned ones?
- [ ] **At root scope:** does every runtime-unit boundary have an integration-test target in the branch / root TestSpec?

A Composition section that is empty, a single paragraph, or a single diagram with no prose is a Quality Bar failure regardless of how good the rest is.

## Quality-attribute coverage

- [ ] Does every NFR from the parent Requirements appear as either an Architecture child's allocated requirement or a cross-cutting composition commitment?
- [ ] Are latency / throughput / availability budgets allocated to specific interfaces or components, not left at system-wide level?
- [ ] Are consistency-model choices (strong / eventual / read-your-writes / bounded staleness) named per data path?
- [ ] Is the cost model (envelope, cost-per-request target, cost-of-a-9 if availability is a binding concern) stated at root scope?

## Resilience coverage

- [ ] Are bulkhead partitions named for shared resources that matter (connection pools, thread pools, external-dependency pools)?
- [ ] Are circuit breakers placed at cross-service boundaries where caller exhaustion is a real failure mode?
- [ ] Is retry policy (backoff, jitter, max attempts) specified where retries are safe, with idempotency design where they are not?
- [ ] Is graceful degradation designed-in (not fallback-in) for non-essential dependencies, with the essential-vs-non-essential split named?
- [ ] Are failure domains (process / host / AZ / region / provider) named, and is every redundancy claim backed by a named independence property (not assumed)?

## Security and observability at boundaries

- [ ] Are trust zones drawn explicitly with named boundary crossings?
- [ ] Is authn / authz stated per externally callable interface, with the evaluation layer (gateway / middleware / handler) named?
- [ ] Is secrets flow specified (origin, in-memory holders, where they must never appear)?
- [ ] Are telemetry emergence points specified (what is logged, what is metric'd, what is traced; sampling policy; common context fields)?

## Rationale and traceability

- [ ] Does every Decomposition entry, interface entry, and load-bearing composition choice carry a rationale field with non-trivial content?
- [ ] Are governing ADRs listed in front-matter and referenced at the point in the body where each decision lands?
- [ ] Has every parent-allocated requirement landed in at least one child (zero unallocated requirements)?
- [ ] Are fitness functions named for load-bearing architectural properties (dependency direction, latency budget, module size, security posture)?

## Retrofit discipline (retrofit mode only)

- [ ] Is observed structure marked `recovery_status: reconstructed` with evidence (file/line, commit, schema, operational log)?
- [ ] Is human-only content (rationale, rejected alternatives, original intent) marked `verified` or `unknown` only — never `reconstructed`?
- [ ] Is every `unknown` field paired with a follow-up owner and an action?
- [ ] Is laundering audited — does any rationale read as generic principle invocation rather than historical recall?
- [ ] Is the Gap report populated (lost rationale, structural drift, missing ADRs, coverage gaps, ambiguous spec)?

## Spec Ambiguity Test — meta-gate **(override)**

- [ ] Could a junior engineer or mid-tier AI, reading only this Architecture artifact (plus its governing ADRs and parent Requirements), produce defensible Detailed Designs for each leaf, and a TestSpec whose cases verify every interface and every composition-level invariant — **without asking clarifying questions**?

If the answer is No, the artifact under-specifies its allocation role. Revise before declaring complete. **This test overrides every box above**: an Architecture artifact that passes all the other checks but fails this one has not done the job Architecture exists to do.
