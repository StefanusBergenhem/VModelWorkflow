# Research 5b: Software Architecture Decomposition and Interface Contracts

Research for architecture craft documentation. Covers how to structure software into
components with clear responsibilities and well-defined interfaces. Pure engineering
craft — no standards framing, applicable to any software architect.

**Sources used:**
- [src-parnas-1972] David L. Parnas, "On the Criteria to Be Used in Decomposing Systems into Modules," CACM 1972. Accessed via: prl.khoury.northeastern.edu/img/p-tr-1971.pdf and swizec.com analysis
- [src-cohesion-wiki] Wikipedia, "Cohesion (computer science)," sourcing Constantine (1969), Yourdon & Constantine (1979)
- [src-coupling-wiki] Wikipedia, "Coupling (computer programming)," sourcing Constantine (1969)
- [src-clean-arch] Robert C. Martin, "Clean Architecture," 2017 — summarized via github.com/serodriguez68/clean-architecture
- [src-dbc-wiki] Wikipedia, "Design by contract," sourcing Bertrand Meyer / Eiffel (1986+)
- [src-hexagonal] AWS Prescriptive Guidance, "Hexagonal Architecture Pattern," Alistair Cockburn (2005)
- [src-layered] Bitloops Resources, "Layered Architecture: The Traditional N-Tier Pattern"
- [src-bounded-ctx] Martin Fowler, "BoundedContext" bliki, sourcing Eric Evans DDD (2003)
- [src-granularity] PMC/MDPI, "Defining and measuring microservice granularity — a literature overview," Future Internet 2021
- [src-fowler-monolith] Martin Fowler, "How to Break a Monolith into Microservices," martinfowler.com
- [src-semver] Tom Preston-Werner, "Semantic Versioning 2.0.0," semver.org
- [src-fail-fast] Vladimir Khorikov, "Fail Fast Principle," enterprisecraftsmanship.com
- [src-dip-wiki] Wikipedia, "Dependency Inversion Principle," sourcing Robert C. Martin

---

## 1. The Foundational Question: What Should a Component Be?

The starting point for any decomposition is choosing the right criterion. Two independent traditions converged on complementary answers.

### 1.1 Parnas: Hide What Is Likely to Change

In his 1972 paper, David Parnas demonstrated that the choice of decomposition criterion has profound consequences. He compared two decompositions of the same KWIC (keyword-in-context) indexing system [src-parnas-1972]:

**Decomposition A — by processing steps (flowchart-based):** Modules correspond to algorithmic steps: input, circular shift, alphabetizer, output. All modules share knowledge of how lines are stored. Changing the storage format requires changes in every module.

**Decomposition B — by information hiding:** Modules encapsulate design decisions. A `LineStorage` module hides how lines are stored. Other modules depend on `LineStorage`'s interface, not on its internal format. "With the first modularization everybody needs to know how lines are stored, whereas the second hides that information from everything but Line Storage." [src-parnas-1972]

The practical heuristic Parnas derives: **hide those details that are "likely to change."** If a decision is likely to change — an algorithm, a storage format, a hardware characteristic — make it invisible to the rest of the system. Changes then have only a local effect.

The benefits are concrete [src-parnas-1972]:
- **Parallel development**: teams work independently on separate modules because interfaces are stable
- **Flexibility**: changes do not cascade
- **Comprehensibility**: engineers can understand one module without mastering the whole system

### 1.2 Constantine: Maximize Cohesion, Minimize Coupling

Independently, Larry Constantine developed cohesion and coupling metrics in the late 1960s as part of Structured Design, formalized in Yourdon & Constantine (1979) [src-cohesion-wiki].

**Cohesion** measures the degree to which elements inside a module belong together. Constantine identified seven levels, from worst to best [src-cohesion-wiki]:

| Level | Name | Description | Example |
|-------|------|-------------|---------|
| 1 (worst) | Coincidental | Grouped arbitrarily | A "Utilities" class with unrelated functions |
| 2 | Logical | Same category, different nature | All input handlers grouped together |
| 3 | Temporal | Processed at the same time | Startup initialization routines |
| 4 | Procedural | Follow a required execution sequence | Check permissions, then open file |
| 5 | Communicational | Operate on the same data | Operations on a single customer record |
| 6 | Sequential | Output of one is input to the next | Parse → validate → transform pipeline |
| 7 (best) | Functional | All contribute to one well-defined task | Tokenizing a string of XML |

Research by Constantine, Yourdon, and McConnell: coincidental and logical cohesion are inferior; communicational and sequential are very good; functional is superior [src-cohesion-wiki].

**Coupling** measures the degree of interdependence between modules. Constantine identified six levels, from worst to best [src-coupling-wiki]:

| Level | Name | Description |
|-------|------|-------------|
| 1 (worst) | Content | One module uses the code of another (branch into) |
| 2 | Common | Modules share global data |
| 3 | External | Modules share externally imposed data formats |
| 4 | Control | One module passes execution flags to another |
| 5 | Stamp | Modules share composite data structures but use only parts |
| 6 (best) | Data | Modules share only elementary data via parameters |

Low coupling exists when modules interact through "simple and stable interfaces" without internal implementation concerns [src-coupling-wiki].

### 1.3 The Two Traditions Compared

Both traditions converge on similar practical guidance but use different conceptual lenses:

| Parnas (1972) | Constantine (1969–1979) |
|---------------|------------------------|
| Hide likely-to-change decisions | Maximize functional cohesion |
| Minimize what each module knows about others | Minimize coupling to data coupling |
| Criterion: changeability | Criterion: functional independence |

Neither is superior — they complement each other. Parnas provides the decomposition heuristic (what to hide); Constantine provides measurement tools (how to evaluate what you built).

---

## 2. Good Boundaries: Criteria for What Becomes One Component

### 2.1 The Single Responsibility Test

A component has a single responsibility when it has **one reason to change** — one actor, one business concern, one dimension of variation [src-clean-arch]. If you can identify two different stakeholders or two different change drivers that could independently force the component to change, it should be split.

The converse test: if two things always change together and are never used apart, they belong in the same component [src-clean-arch] (Common Closure Principle).

### 2.2 The Bounded Context Test

For domain-level decomposition, Martin Fowler and Eric Evans introduced the bounded context: a boundary within which a domain model is consistent and valid [src-bounded-ctx].

A boundary is natural when the **language changes** — when the same word means different things in different parts of the organization. Fowler's example: "meter" means a grid connection in one department, a customer relationship in another, a physical device in a third. Each meaning is a candidate boundary [src-bounded-ctx].

"Total unification of the domain model for a large system will not be feasible or cost-effective." [src-bounded-ctx] Accepting multiple canonical models per context is more practical than forcing a single universal model.

**Practical heuristic:** identify polysemes (terms with different meanings in different contexts). Each distinct meaning signals a boundary. The ubiquitous language of each bounded context should be internally consistent and unambiguous.

### 2.3 The Component Cohesion Tension

Robert Martin identifies three principles that pull component cohesion in different directions [src-clean-arch]:

- **REP (Reuse/Release Equivalence Principle)**: Group things that are releasable together. Consumers need versioned, coherent releases — don't mix unrelated things in a single release unit.
- **CCP (Common Closure Principle)**: Group things that change for the same reasons. Changes should be confined to one component.
- **CRP (Common Reuse Principle)**: Don't force users to depend on things they don't need. Don't bundle loosely related things just because they're somewhat related.

These three principles form a tension triangle:
- REP + CCP are inclusive (make components larger)
- CRP is exclusive (pushes components to be smaller)

An architect must navigate this tension. The practical guidance: early in a project, prioritize CCP (protect against change); as the system matures, shift toward REP (enable reuse and stable versioning) [src-clean-arch].

### 2.4 What Makes a Bad Boundary

**Too coarse (big ball of mud):** The module does too many things, has multiple change drivers, and mixes concerns. Changes in one concern ripple through code that should be unrelated. High coupling between internal elements that have no business being together.

**Too fine (distributed monolith):** Each unit is so small it cannot function independently. Units must be deployed together, creating implicit coupling through network interfaces. "Overcorrection from large monoliths to really small services, an approach inspired by normalized data views, almost always leads to many anemic services for CRUD resources." [src-granularity] Each remote call introduces network latency, overhead, and failure modes — without gaining any real independence.

---

## 3. Interface Definition Craft

### 3.1 Syntactic vs. Semantic Interfaces

Every interface has two layers [src-dbc-wiki]:

**Syntactic interface**: The signature — method names, parameter types, return types. Checked by compilers and IDEs. Tells you *what* you can call.

**Semantic interface**: The behavioral contract — what the method promises to do, what it requires from the caller, what invariants hold before and after. Not checked by compilers. Tells you *how* it behaves and under what conditions it is valid.

A syntactically correct call against a violated semantic contract produces incorrect behavior — potentially silent corruption. The semantic contract is the more important and more frequently absent layer.

### 3.2 Design by Contract

Bertrand Meyer formalized the semantic layer in Design by Contract (DbC), integrated into the Eiffel language [src-dbc-wiki]:

**Preconditions**: What the caller must guarantee before calling the method. The method is entitled to assume these hold. If they don't, the fault is the caller's.

**Postconditions**: What the method guarantees after successful completion. If the precondition was satisfied and the postcondition is not, the fault is the implementer's.

**Invariants**: Properties that hold throughout the component's lifetime — assumed on entry, guaranteed on exit.

The contract metaphor: client and supplier agree on mutual obligations. Client pays (satisfies precondition) and receives goods (postcondition guaranteed). Supplier delivers goods (postcondition) and assumes payment (precondition holds) [src-dbc-wiki].

**Fault attribution through contracts:**
- Precondition violated → caller's fault
- Precondition satisfied but postcondition violated → implementer's fault
- No contract → fault attribution is ambiguous, debugging is harder

### 3.3 Provided and Required Interfaces

UML component diagrams distinguish between [src-coupling-wiki, src-hexagonal]:

**Provided interface** ("lollipop" notation): The services the component offers to others. What it guarantees to deliver.

**Required interface** ("socket" notation): The services the component needs from others. Its declared dependencies.

This explicit distinction is important because it clarifies:
- What a component can do standalone (provided only)
- What a component needs to function (required)
- Where substitutions are possible (any component that satisfies the required interface can be plugged in)

In hexagonal architecture, ports formalize this distinction [src-hexagonal]: driving ports (provided — how external actors use the application) and driven ports (required — what the application needs from infrastructure).

### 3.4 The Interface Segregation Principle

Robert Martin's Interface Segregation Principle states: no code should be forced to depend on methods it does not use [src-clean-arch]. Large interfaces should be split into smaller, more specific ones.

The practical consequence: **narrow interfaces are more stable.** A component that depends only on the three methods it needs is unaffected by changes to other methods. A component that depends on a fat interface is affected by changes to methods it never calls — this is stamp coupling at the interface level.

Narrow, focused interfaces also improve testability: you can substitute a test double that implements only the three methods under test.

### 3.5 Error Contracts

The error behavior is part of the semantic interface and is frequently omitted. A complete interface specification answers:
- Under what conditions can this method fail?
- What does failure look like (exception type, error code, result type)?
- What is the state of the component after a failure? (Is it still usable? Is it corrupted?)
- What is the caller's obligation after a failure? (Must the caller retry? Roll back? Discard the component?)

**Fail Fast**: When a contract precondition is violated, the system should fail immediately and loudly rather than continuing in a corrupted state [src-fail-fast]. The feedback loop is shortest at the point of violation. Masking errors by continuing execution risks corrupting persistent state and extends the time before the bug is discovered.

**Defensive programming** differs: the implementer handles the invalid input rather than requiring the caller to guarantee it. For trusted internal interfaces (within a component), DbC / fail-fast is appropriate. For untrusted external inputs (user input, external APIs), defensive validation is appropriate before the contract boundary.

---

## 4. Dependency Management

### 4.1 Dependency Inversion Principle

Robert Martin's Dependency Inversion Principle (DIP) states [src-dip-wiki]:
1. High-level modules should not import from low-level modules. Both should depend on abstractions.
2. Abstractions should not depend on details. Details (concrete implementations) should depend on abstractions.

The name "inversion" refers to a reversal of the typical dependency direction. Naively, a high-level policy module calls a low-level implementation module directly. With DIP, both depend on an abstract interface — the high-level module defines the interface (in its package), and the low-level module implements it. The dependency arrow points toward the high-level module, not away from it.

**Practical consequence for testability**: when dependencies point toward abstractions, any dependency can be replaced with a test double. When high-level code directly depends on low-level implementations, testing the high-level code in isolation requires working infrastructure.

### 4.2 Stable Dependencies Principle (SDP)

"Depend in the direction of stability" [src-clean-arch]. Components should depend on components that are harder to change, not on volatile ones.

Stability is determined primarily by **how many other components depend on a component**. A component with many dependents is expensive to change — any change forces updates in all dependents. This component is therefore stable (resistant to change).

Martin's instability metric: `I = Fan-out / (Fan-in + Fan-out)` where I=0 is maximally stable, I=1 is maximally unstable [src-clean-arch].

Along any dependency chain, instability should increase (I should rise as you move from stable foundations toward volatile application code). If a stable component depends on an unstable one, the stable component will be forced to change when the unstable one changes.

### 4.3 Stable Abstractions Principle (SAP)

"Stable components should be abstract; unstable components can be concrete" [src-clean-arch].

Highly stable components (many dependents) need to be extendable without requiring their concrete code to change. Abstract classes and interfaces achieve this: dependents depend on the interface, new behavior is added by implementing the interface without modifying the existing abstract class.

The ideal pattern: a stable abstract component (many dependents, interface-only) and an unstable concrete component (few dependents, implements the interface). Together, SDP + SAP approximate DIP applied at the component level.

### 4.4 Acyclic Dependencies Principle (ADP)

"Allow no cycles in the component dependency graph" [src-clean-arch].

Circular dependencies between components produce:
- Unclear build ordering (what builds first?)
- Loss of independent release-ability (components must be released in lockstep)
- Forced version coordination (upgrading any component in the cycle affects all others)
- Difficulty with unit testing (cannot test component A without also loading B and C)

Two standard techniques for breaking cycles [src-clean-arch]:
1. **Dependency inversion**: introduce an interface; the formerly-dependent component depends on the interface instead of the concrete module. The interface can live in either component or in a new component.
2. **Extract a new component**: move the shared dependency into a new component that both original components can depend on.

The second approach increases the component count. This is often the right trade — more components with acyclic dependencies are easier to manage than fewer components with cycles.

---

## 5. Layering and Partitioning Strategies

### 5.1 Strict Horizontal Layering

The classic N-tier structure: presentation → business logic → data access [src-layered]. Each layer depends only on the layer below.

**Strict layering**: requests flow through every layer in order. No skipping.
- Clear contracts between layers
- Layers can be tested independently
- Individual layers can be replaced

**Relaxed layering**: layers can skip; presentation may call data access directly.
- Simpler for trivial operations
- Over time, layers become "suggestions rather than rules" and coupling spreads [src-layered]

**When layered architecture works**: Simple CRUD applications, single-team projects, stable requirements, data-centric systems [src-layered].

**When it fails**: Multiple teams (organizational structure doesn't align with horizontal layers), complex systems (business rules span layers, creating duplication), systems requiring independent deployment of features [src-layered].

The **horizontal slice problem**: adding a single feature requires modifying all three layers. With ten teams all touching all layers, coordination overhead becomes dominant.

### 5.2 Hexagonal / Ports and Adapters

Alistair Cockburn's hexagonal architecture resolves the "contamination" problem where infrastructure concerns leak into business logic [src-hexagonal].

**Core structure**:
- **Inner hexagon (domain)**: pure business logic, no infrastructure knowledge
- **Ports**: abstract interfaces defining how the domain connects to the outside world
- **Adapters**: concrete implementations of ports for specific technologies

The key rule: adapters adapt the outside world to the application's ports, not the other way around. Infrastructure implements what the domain needs — not the reverse.

**Testability advantage**: the domain can be tested without any real infrastructure because all infrastructure sits behind ports that can be replaced with test doubles [src-hexagonal].

**When to use**: multiple input/output channels, anticipated technology changes, domain logic complexity warrants protection, testability is a priority.

**When to avoid**: simple CRUD with stable technology choices, small projects where adapter plumbing overhead exceeds the flexibility gained [src-hexagonal].

### 5.3 Vertical Slices / Feature-Based Decomposition

Instead of horizontal layers, vertical slices organize by feature or capability. Each vertical slice owns its entire stack — its own presentation, logic, and persistence.

**Advantages**:
- Teams can work on their slice independently
- Deployment of a feature does not require coordinating across all layers
- Feature complexity is self-contained

**When horizontal becomes vertical**: "If your system is organized by features, each team works independently and coordination overhead drops. Vertical organization by feature or domain starts making sense beyond 3-4 layers." [src-layered]

**Relationship to bounded contexts**: a vertical slice maps naturally to a bounded context — the domain boundary and the deployment boundary align.

### 5.4 Comparison of Approaches

| Approach | Primary axis | Best fit | Key trade-off |
|----------|-------------|----------|---------------|
| Strict layering | Technical concern (presentation/logic/data) | Single-team, simple CRUD | Feature changes touch all layers |
| Hexagonal | Domain inside, infrastructure outside | Domain-rich apps, testability priority | Adapter overhead for simple apps |
| Vertical slices | Business feature/capability | Multi-team, independent deployment | Cross-cutting concerns need explicit handling |
| Bounded contexts | Domain language boundary | Large systems, long-lived codebases | Mapping/integration overhead between contexts |

These approaches are not mutually exclusive. A system can use vertical slices at the coarse level (features/domains) and hexagonal architecture within each slice.

---

## 6. Component Granularity

### 6.1 The Fundamental Tension

No formula for right-sizing exists. The research literature confirms that "no agreement on the correct size of microservices exists" [src-granularity]. Practitioners must navigate between two failure modes:

**Too coarse (big ball of mud)**: One component does too many things. Changes in one concern require reasoning about unrelated code. Internal coupling is high. Parallel development is difficult.

**Too fine (distributed monolith)**: Components are so small they cannot function independently. They must be deployed together, so the "boundary" between them is a network hop with no real independence gain. "Overcorrection... almost always leads to many anemic services for CRUD resources." [src-granularity] Network calls replace in-process calls, adding latency and failure modes, without the independence benefits of real decomposition.

### 6.2 Heuristics for Right-Sizing

**From domain and change patterns**:
- Group code that changes for the same reasons (CCP) [src-clean-arch]
- Separate code whose change drivers are independent [src-clean-arch]
- Use commit history: if two things always change in the same commit, they may belong together
- Use the language boundary (bounded context) test [src-bounded-ctx]

**From team structure (Conway's Law)**:
- A component should be ownable by a single team
- If two teams must coordinate every time a component changes, the boundary is wrong
- Team size as a sizing heuristic: a team should be able to own, understand, and rewrite a component

**From operability**:
- "Start with larger services around a logical domain concept, and break the service down into multiple services when the teams are operationally ready." [src-fowler-monolith]
- Independent deployability is the key test: can this component be released without coordinating with other teams?
- "The primary reason for moving capabilities out of a monolith is the ability to release independently because they're important to the business or need frequent changes." [src-fowler-monolith]

**From interface counts**:
- A component with a very large interface surface may be doing too much
- Interface Number (IFN) as a complexity indicator [src-granularity]

### 6.3 The Modular Monolith Middle Ground

For many systems, the right answer is neither a monolith nor microservices — it is a modular monolith: a single deployable unit with rigorous internal component boundaries. Components are strongly separated by internal APIs and enforced access restrictions, but they share a process and can use in-process calls.

Benefits over microservices:
- No network latency overhead for inter-component calls
- No distributed transaction complexity
- Simpler operational model

Benefits over unstructured monolith:
- Component boundaries enforce information hiding
- Enables incremental extraction to services if needed later
- Independent team development within the monolith is still possible

The modular monolith is an often-overlooked option that delivers most of the modularity benefits without the operational cost of distribution.

---

## 7. Interface Versioning and Contract Evolution

### 7.1 Semantic Versioning

Tom Preston-Werner's Semantic Versioning (SemVer) establishes rules for communicating changes to interface consumers [src-semver]:

- **MAJOR (X)**: backward-incompatible API changes — callers must adapt
- **MINOR (Y)**: backward-compatible additions — callers need not adapt but gain new capabilities
- **PATCH (Z)**: backward-compatible bug fixes — behavior correction, no API change

The key insight: **version numbers carry semantic meaning about the nature of change.** This is only useful if the team is rigorous about what constitutes a "breaking change."

### 7.2 What Constitutes a Breaking Change

A breaking change is any change that violates the existing semantic contract for existing callers [src-semver]:
- Removing or renaming a method or endpoint
- Changing parameter types or counts
- Changing return types
- **Changing error conditions** (callers may depend on specific exception types or error codes)
- Changing behavioral guarantees — even with an identical signature

Note: purely syntactic changes (same signature, different behavior) are breaking changes to the semantic contract even if not to the syntactic one.

### 7.3 The Deprecation Pattern

The safe evolution path [src-semver]:
1. Add the new API in a MINOR release
2. Mark the old API as deprecated in the same or subsequent MINOR release (with migration guidance)
3. Remove the old API only in a MAJOR release
4. Allow adequate migration time (industry convention: 6-12 months notice before removal)

This pattern allows existing callers to continue working while new callers adopt the improved API. It separates the introduction of new capability from the removal of old capability.

### 7.4 Anti-Corruption Layers

When integrating with an external system whose model differs from your own, an anti-corruption layer (ACL) translates between their model and yours [src-bounded-ctx]. This prevents the external system's concepts from contaminating your bounded context.

The ACL has a defined interface on both sides:
- Outward: conforms to the external system's contract
- Inward: speaks your context's language

This makes it easy to replace the external system without touching your domain code — only the ACL changes.

---

## 8. What the Sources Are Silent On

The following topics were not well-covered by the sources found in this research:

1. **Quantitative thresholds for cohesion/coupling metrics in practice**: the literature identifies the metrics (fan-in, fan-out, LCOM) but provides little guidance on what numeric thresholds signal problems. This is acknowledged as context-dependent.

2. **Interface contracts in asynchronous systems (event-driven)**: the contract literature (DbC, SemVer) primarily addresses synchronous method calls. Asynchronous event schemas and their versioning (e.g., event sourcing, message queues) require different techniques (schema registries, event versioning strategies) that were not covered.

3. **Contract testing tools**: the sources mention consumer-driven contract testing as a practice but don't go into depth on tooling (Pact, Spring Cloud Contract).

4. **How to handle backward-incompatible changes gracefully in existing deployed systems**: the deprecation pattern is covered, but migration patterns for systems with many existing callers are not detailed.

5. **Performance implications of component granularity trade-offs with concrete numbers**: cited that network hops add latency but the research sources provided only anecdotal figures.

---

## Summary of Key Principles

| Principle | Source | Core Claim |
|-----------|--------|------------|
| Information hiding | Parnas 1972 | Decompose by hiding likely-to-change decisions |
| Functional cohesion | Constantine 1969 | Group elements that contribute to one task |
| Data coupling | Constantine 1969 | Pass only what is needed, as elementary data |
| Common Closure | Martin (Clean Architecture) | Group what changes together |
| Common Reuse | Martin (Clean Architecture) | Don't bundle what users don't need together |
| Acyclic Dependencies | Martin (Clean Architecture) | No cycles in the component dependency graph |
| Stable Dependencies | Martin (Clean Architecture) | Depend toward stability |
| Dependency Inversion | Martin (SOLID) | High-level policy depends on abstractions, not concretions |
| Design by Contract | Meyer / Eiffel | Specify preconditions, postconditions, invariants |
| Fail Fast | Khorikov | Crash immediately on contract violation |
| Bounded Context | Evans / DDD | Separate where the language changes |
| Hexagonal Architecture | Cockburn | Domain inside, adapters outside |
| Semantic Versioning | Preston-Werner | MAJOR.MINOR.PATCH encodes breaking vs compatible change |
