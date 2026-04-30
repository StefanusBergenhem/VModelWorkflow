# Composition patterns — protocols, sync/async, runtime patterns, wiring

Two halves: protocol family + sync/async (per-interface decisions); composition pattern + wiring (scope-level decisions). Make both choices explicitly; record rationale.

## Half 1 — Protocol families

| Family | Strengths | Weaknesses | Default for |
|---|---|---|---|
| **REST / HTTP+JSON** | Universal tooling, cache-friendly, evolves by adding fields | Weak boundary typing, no native streaming, polling for events | External APIs to heterogeneous clients |
| **gRPC / protobuf** | Contract-first, low-latency binary, bidirectional streaming, code-gen clients | Binary wire (debug pain), browser needs proxy, breaking changes hidden by code-gen | Internal high-throughput service-to-service |
| **GraphQL** | Client-driven query shape, one endpoint, strong introspection | Caching, per-field authz, rate-limit complexity, N+1 resolver trap | Front-ends with many varying read patterns over rich domain |
| **Events / messaging** | Decoupled temporal contract, fan-out, back-pressure-friendly | Eventual consistency, schema evolution, distributed-flow debug pain | Producer should not know who consumes |

Choice is the first composition decision. REST between two components is a *different architecture* than the same two on an event bus: REST couples availability; events buffer at the cost of immediate consistency.

## Sync vs async — a meta-decision across all four families

Three axes decide:

- **Coupling.** Sync couples availability (callee down → caller fails or waits). Async does not. Producer must keep working when consumer is down → async.
- **Failure mode.** Sync surfaces failure at the call site (easy to handle, easy to see). Async pushes failure into retry / DLQ / compensation (harder to debug; bad for "user is waiting" workflows).
- **Back-pressure.** Sync naturally applies back-pressure (slow callee slows callers). Async needs explicit mechanism (bounded queues, ack, reactive streams). Without it: queue fills, producer OOMs, consumer unchanged, nobody saw it coming.

**Rule:** name the axis that dominates this interface; record the choice and rationale at the interface entry or governing ADR. *Defaulting to async because it is trendy is how you get a distributed system with synchronous semantics and asynchronous blast radius.*

## Half 2 — Composition patterns catalog

The Composition section names *exactly one* runtime pattern (or a stated combination, e.g., "request-response with outbox for async events"). "We will figure it out at build time" is not an answer.

- **Request-response (RPC, HTTP).** One component calls another, waits for result. Fits user-facing workflows, read paths, transactional writes. Wiring: timeout discipline, idempotency where retried, back-pressure via connection limits, circuit breakers. *Anti-pattern:* request-response chains > 3 hops turn every downstream latency spike into a caller outage.
- **Event-driven (publish-subscribe).** Producer emits on a topic; consumers subscribe and act async. Fits fan-out, audit logging, downstream integrations, varying consumer set. Wiring: event schema is published contract (versioned, deprecation-windowed); message-bus topology is architectural (topic per aggregate, partition key, retention, DLQ); consumer idempotency is non-negotiable (at-least-once is baseline). Distributed tracing across async edges is not optional.
- **Event sourcing.** State stored as a stream of domain events; current state is a fold. Fits audit-heavy domains, multiple read models from same writes. Wiring: schema evolution becomes hard (immutable history, evolving code); projections are first-class architectural elements; snapshotting is a perf concern Architecture must address. Expensive; wrong for most systems; extraordinary when right.
- **Saga.** Long-running, multi-step workflow across services with compensating actions. Two variants: *orchestration* (coordinator owns workflow — easier to reason, harder to scale) vs *choreography* (services react to events, emit next — reverse). Wiring: compensation as a design axis (not every step has a clean inverse); explicit timeout + retry budgets; visibility ("where is this saga stuck?") is a first-class concern.
- **Pipeline / data flow.** Sequence of stages, each consuming previous's output. Fits batch, streaming analytics, ETL, build systems, media. Wiring: stage interfaces are pressure points; per-stage parallelism with bounded buffers; explicit back-pressure.
- **Layered (n-tier).** Stacked layers depending only on the layer beneath (presentation → business → data). Fits simple CRUD where one entity flows through every layer. *Anti-pattern at non-trivial scope:* horizontal slices through every feature → distributed monolith. Teams change feature-by-feature, not layer-by-layer.
- **Hexagonal (ports and adapters, Cockburn 2005).** Inner domain hexagon with *driving* ports (primary; users / jobs / APIs invoke) and *driven* ports (secondary; domain depends on for persistence / messaging / external services). Adapters translate between ports and concrete tech. Fits any domain with real business logic that should not know the database. Most cost-effective pattern for long-lived domain-heavy services. Architecture entry names the ports (one per port, primary and secondary).
- **Clean architecture (Martin).** More prescriptive elaboration of hexagonal; concentric rings (entities → use cases → interface adapters → frameworks/drivers); strict inward-pointing dependency rule. Fits large or regulated teams. Implications same as hexagonal plus the dependency-direction discipline.
- **Microservices vs modular monolith.** Same decomposition, different deployment topology. Useful heuristic: *if two modules do not need to scale, fail, or be owned independently, they do not need to be independent services.* Microservices for a small team with one deploy cadence → distributed monolith.
- **Serverless / FaaS.** Composition as short-lived functions on event/HTTP/schedule triggers. Fits spiky loads, glue, event processors. Wiring: cold-start as first-class NFR; stateless-between-invocations; wiring lives in cloud config (event sources, IAM, triggers). Does not fit long-running stateful workflows or deep latency budgets.

## Wiring — three concerns always explicit

Whatever pattern is named, three are stated in the Architecture artifact:

1. **Dependency-injection strategy.** How components acquire dependencies: constructor injection, DI container, composition root. Name it so leaf DDs do not reinvent it.
2. **Middleware stack (ordered).** The chain every request / event passes through. Order matters: *tracing outermost; authN before authZ; rate limit before handler; logging on exit*. The Architecture states it; do not discover it after six months in production.
3. **Message-bus topology (where applicable).** Topics, partition-key choice, retention, dead-letter routing, consumer-group layout. Architectural, not infra detail.

## Citations

- Cockburn, *Hexagonal Architecture* (2005); AWS Builders' Library summary.
- Martin, *Clean Architecture* (Prentice Hall, 2017).
- Brewer, CAP; Abadi, PACELC; Kleppmann, *Designing Data-Intensive Applications* (O'Reilly 2017) — referenced in `data-and-persistence.md`.
