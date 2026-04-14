# Research 5e: Architecture Documentation — Views, Rationale, and Communication

Research for architecture craft documentation. Covers how to document architecture
so builders can build from it and reviewers can evaluate it.

**Sources used:**
- [src-nygard] Nygard, Michael. "Documenting Architecture Decisions." Cognitect Blog, 2011-11-15. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- [src-41view] "4+1 Architectural View Model." Wikipedia. https://en.wikipedia.org/wiki/4%2B1_architectural_view_model (based on Kruchten, Philippe. "Architectural Blueprints — The '4+1' View Model of Software Architecture." IEEE Software, 1995.)
- [src-c4] Brown, Simon. C4 Model. https://c4model.com/
- [src-vnb] Clements, Paul et al. "Documenting Software Architectures: Views and Beyond," 2nd Ed. SEI / Addison-Wesley. Source excerpts via https://www.sei.cmu.edu/library/views-and-beyond-collection/ and https://flylib.com/books/en/2.121.1/
- [src-interface] Bachmann, Felix et al. "Documenting Software Architecture: Documenting Interfaces." SEI Technical Note CMU/SEI-2002-TN-015. Summarized via https://www.brainkart.com/article/Documenting-Interfaces_11299/
- [src-arc42] Starke, Gernot and Hruschka, Peter. arc42 Template. https://arc42.org/overview; https://www.innoq.com/en/blog/2022/08/brief-introduction-to-arc42/
- [src-statemachine] "State Machine Diagram Deep Dive: Transitions & Guards for Embedded." archimetric.com. https://www.archimetric.com/state-machine-diagram-deep-dive-transitions-guards-embedded/
- [src-knowledgeloss] "The Loss of Architectural Knowledge during System Evolution: An Industrial Case Study." Teamscale/research paper. https://teamscale.com/hubfs/26978363/Publications/2009-the-loss-of-architectural-knowledge-during-system-evolution-an-industrial-case-study.pdf
- [src-mezzalira] Mezzalira, Luca. "How to Document Software Architecture: Techniques and Best Practices." Medium, 2023. https://lucamezzalira.medium.com/how-to-document-software-architecture-techniques-and-best-practices-2556b1915850

---

## 1. Why Document Architecture at All

### The Questions Architecture Documentation Answers

Architecture documentation exists to answer questions that neither the source code nor the requirements can answer on their own. The code tells you what the system does now, line by line. The requirements tell you what the system should achieve. Architecture documentation answers the structural and strategic questions in between:

- What are the major parts of the system and where do their responsibilities begin and end?
- How do parts communicate — synchronously, asynchronously, through shared state?
- Why was this decomposition chosen over alternatives that were considered?
- What quality properties (performance, reliability, security) does the architecture trade against each other, and where?
- How does the system behave differently in startup, normal operation, degraded mode, shutdown?
- Which decisions are load-bearing — changing them would require rearchitecting — versus incidental?

Without explicit answers to these questions, engineers have to reconstruct the architecture from the code on every interaction. This is slow, error-prone, and means each engineer may reconstruct it differently.

### The Audiences

Architecture documentation serves several distinct audiences with different needs [src-vnb]:

**Developers** need to understand where to put new code, what they can depend on, what they must not bypass, and what the interfaces they call actually do. They primarily need structural views (decomposition) and runtime views (what communicates with what).

**Testers and integration teams** need to understand runtime structure — what components exist at system execution, how they interact, what their contracts are. They need to know the happy paths and the failure paths.

**Future maintainers** (including the original team six months later) need to understand why decisions were made. Without documented rationale, every settled decision becomes a potential target for re-litigation. Teams rediscover the reasons the hard way, or make changes that unknowingly violate constraints the original decision was built around [src-knowledgeloss].

**Reviewers and auditors** need to assess whether the architecture is sound — whether it achieves the intended quality properties, whether the decomposition is coherent, whether interfaces are well-defined. They cannot evaluate what they cannot see.

**Operations teams** need to understand how software maps to infrastructure, what the deployment topology is, and what failure modes look like at runtime.

### What Happens When Architecture Lives Only in People's Heads

Research on industrial systems confirms that architectural knowledge loss has concrete consequences [src-knowledgeloss]:

- Developer turnover transfers undocumented mental models out of the organization
- Teams rediscover — and sometimes re-make — previously rejected decisions
- Modifications violate invariants the original architects understood but never wrote down
- Onboarding new engineers takes longer because they must reconstruct understanding that should have been captured
- The architecture drifts from its intended structure because implementers don't know what the intended structure was

The specific damage from undocumented rationale: "New team members face two problematic alternatives without documented context — blindly accepting decisions that may no longer be valid, or blindly reversing decisions without understanding their consequences" [src-nygard]. Neither option is good; the first causes stagnation, the second causes regressions.

### The Anti-Pattern: The Big Document No One Reads

Traditional documentation approaches often fail by producing one large document that contains everything. Such documents accumulate but never get read or updated. "Small, modular documents have at least a chance at being updated" [src-nygard]. This motivates the view-based and ADR-based approaches: keep each artifact small, purposeful, and maintainable.

---

## 2. View-Based Documentation

The central insight of view-based architecture documentation is that no single diagram or description can capture all the concerns of a complex system. Different stakeholders care about different things, and different questions require different representations. You need multiple views.

### The 4+1 View Model (Kruchten, 1995)

Philippe Kruchten's 4+1 model organizes architecture documentation into five concurrent views, each addressing a different set of stakeholder concerns [src-41view]:

**Logical View** — focuses on functional decomposition. What are the major abstractions (classes, subsystems, packages) and how do they relate? Uses class diagrams and state diagrams. Primary audience: end-users who care about functionality, analysts, domain experts. This is the "what it does" view.

**Process View** — focuses on runtime behavior. What are the executing processes? How do they communicate? How is concurrency handled? What are the performance and scalability characteristics? Uses sequence diagrams, activity diagrams, communication diagrams. Primary audience: integrators, performance analysts, system engineers. This is the "how it runs" view.

**Development View** — focuses on how code is organized for the development team. What are the modules, layers, packages? What are the build dependencies? Uses component diagrams and package diagrams. Primary audience: developers, build engineers, project managers (for work breakdown). This is the "how we build it" view.

**Physical View** — focuses on topology. How do software components map to hardware? What are the network connections? Uses deployment diagrams. Primary audience: system engineers, network architects, operations. This is the "where it runs" view.

**Scenarios (the +1)** — cross-cutting use cases or scenarios that exercise the other four views. Not a fifth independent view but a validation mechanism: do the four views together explain how the most important use cases work? Primary audience: all stakeholders. This is the most accessible entry point for people not familiar with the system.

The key principle: the model is "not restricted to any notation, tool or design method" [src-41view]. Kruchten chose notation independence deliberately, anticipating that notation fashions would change while the underlying principle (multiple views are necessary) would not.

### SEI Views and Beyond (Clements, Bachmann, Bass et al.)

The SEI approach formalizes view-based documentation into three view types, each with defined styles [src-vnb]:

**Module Views** — describe how the system's source code is partitioned into separable units, what each unit is responsible for, and what dependencies exist between them. Module views answer: "If I need to change X, what else do I need to touch?" They are static — they describe code organization, not runtime behavior.

Module views use three styles: decomposition (hierarchical breakdown), uses (what must exist for what to work), and layered (strict dependency ordering that creates substitutability). The layered style is particularly important: a properly layered architecture constrains dependencies so that components at one layer depend only on layers below, enabling independent testing and replacement.

**Component-and-Connector (C&C) Views** — describe runtime structure. What components exist while the system is running? What are the pathways of interaction between them? C&C views answer: "At runtime, what is talking to what?" The fundamental distinction from module views: "C&C views are similar to object, or collaboration, diagrams, as opposed to class diagrams" [src-vnb]. Module views define types; C&C views show instances at runtime.

C&C views are the appropriate tool for analyzing performance (can this path handle the required throughput?), reliability (if this component fails, what is affected?), and security (which communication paths are untrusted?).

**Allocation Views** — describe how software elements are mapped to external structures: deployment allocation (which software runs on which hardware), work assignment (which team owns which module), and installation (what files go where). These views answer "where" questions at different levels of abstraction.

**The "Beyond" Section** — no collection of views is complete architecture documentation. Documentation that applies across views uses a how-what-why structure [src-vnb]: how the documentation is organized and how to read it; what the architecture is (the views themselves); why the architecture is the way it is (design rationale, background, constraints). The beyond section prevents views from being orphaned artifacts with no context.

### The C4 Model (Simon Brown)

The C4 model takes a hierarchical rather than concurrent approach, using four levels of zoom [src-c4]:

**Level 1 — System Context**: Shows the system in scope and its relationships with external users and systems. The highest level of abstraction. "What are we building and who uses it?" Appropriate for all stakeholders including non-technical ones. Very stable — the system boundary and major external actors change rarely.

**Level 2 — Container**: Breaks the system into separately deployable/runnable units — applications, databases, microservices, mobile apps, etc. Shows what technology each container uses and how they communicate. "What are the major technology building blocks?"

**Level 3 — Component**: Decomposes a single container into its logical components and their interactions. "What are the major structural building blocks inside this container?" Often optional — the detail level needed depends on team size and system complexity.

**Level 4 — Code**: Class diagrams, entity-relationship diagrams, implementation details. Often auto-generated from code. Simon Brown explicitly warns against maintaining Level 4 diagrams manually — they go stale quickly.

The C4 model also defines three supplementary diagram types [src-c4]:
- **Dynamic diagrams** — show how elements collaborate at runtime for a specific scenario (equivalent to sequence diagrams)
- **Deployment diagrams** — show how containers map to infrastructure
- **System landscape diagrams** — show multiple systems in their organizational context

The C4 model's practical advantage over the 4+1 model: it's strictly hierarchical (each level zooms into one element of the level above), which makes navigation intuitive for teams not trained in formal architecture modeling. The cost is some expressive power — the 4+1 model's concurrent views capture concerns that don't map cleanly to C4's zoom levels.

### Static Views vs. Dynamic Views

All three frameworks share a fundamental distinction between static and dynamic views:

**Static views** (module views, C4 Level 1-3 structure) — describe what exists: the parts of the system, their types, their responsibilities, and their structural relationships. These are the "architecture as noun" views.

**Dynamic views** (C&C views, 4+1 process view, arc42 runtime view, C4 dynamic diagrams) — describe how the system behaves: what happens at runtime, in what sequence, under what conditions. These are the "architecture as verb" views.

A common documentation failure is to produce only static views. Static views tell builders what components to build. They do not tell builders or reviewers how the components will interact at runtime, where the performance-sensitive paths are, or what happens during error recovery. Static plus dynamic views are required for a complete picture.

---

## 3. Architecture Decision Records (ADRs)

### The Problem ADRs Solve

"One of the hardest things to track during the life of a project is the motivation behind certain decisions" [src-nygard]. Over time, architectural decisions accumulate in a codebase without any record of why they were made. This creates several failure modes:

- New team members encounter a decision and don't know whether it reflects a deliberate constraint or an accident of history
- Teams debate decisions that were already thoroughly considered, wasting time re-litigating settled questions
- Decisions get reversed without understanding their full consequences, causing regressions that take time to trace back to the reversal

ADRs solve this by capturing each significant architectural decision as a small, focused document at the time the decision is made, with enough context that someone reading it years later can understand why.

### The Nygard Template

Michael Nygard's 2011 blog post established the canonical lightweight ADR format [src-nygard]:

**Title** — a short noun phrase naming the decision. "ADR-007: Use PostgreSQL for the job queue." Not "Database decision" — specific enough to be found.

**Status** — proposed, accepted, deprecated, or superseded (with reference to the superseding ADR). Status makes the lifecycle of decisions explicit.

**Context** — describes the forces at play: technological constraints, team capabilities, business priorities, time pressure, existing constraints from prior decisions. Written in neutral language, as a set of facts, not as advocacy for the decision. "Context sets up the problem space, not the solution."

**Decision** — states the choice in active voice: "We will use PostgreSQL." One or two sentences. The active voice is deliberate — passive voice obscures who made the decision and implies no one takes responsibility.

**Consequences** — lists all outcomes, both positive and negative. This is the section most often skipped and the most valuable. It captures what becomes harder because of this decision, what new options become available, what technical debt is incurred, what follow-on decisions are required. "The consequences of one ADR are very likely to become the context for subsequent ADRs."

### ADR Principles

**Immutability**: Never edit an existing ADR to change its content. If a decision is reversed or updated, write a new ADR that explicitly supersedes the old one. The old ADR stays in place, marked superseded. This preserves the historical record — you can trace the evolution of decisions over time [src-nygard].

**Size**: One to two pages maximum. "Written as a conversation with a future developer." If an ADR needs to be longer, it probably contains multiple decisions that should be separate ADRs.

**Storage**: In version control, colocated with the code, under `doc/arch/adr-NNN.md` or equivalent. ADRs stored in wikis drift out of sync with code changes; version-controlled ADRs are updated (or marked superseded) as part of the development process.

**Threshold**: Not every decision needs an ADR. The threshold is approximately: would a competent new team member, reading the code, be surprised by this decision or wonder why it was made this way? If yes, write an ADR.

### ADRs vs. Architecture Documents

ADRs and architecture views are complementary, not alternatives. Architecture views describe the structure: what components exist, how they relate. ADRs capture rationale: why the structure is the way it is, what was considered and rejected, and what constraints the structure must not violate. The arc42 template makes this explicit by placing architecture decisions (Section 9) as a separate section from the building block view (Section 5) [src-arc42].

---

## 4. Documenting System Modes and Dynamic Behavior

### Systems Have Multiple Operating Modes

Most non-trivial systems exhibit significantly different behavior depending on their current operating mode. Common modes include:

- **Startup/Initialization**: Components initialize in a specific order; some interfaces may not yet be available; the system is not yet in a valid steady state
- **Normal operation**: Primary functional behavior; all components initialized; full capability available
- **Degraded operation**: One or more components failed or unavailable; system continues with reduced capability or modified behavior
- **Safe/limp-home mode**: Minimal capability mode, prioritizing stability or safety over functionality
- **Shutdown/Teardown**: Resources released in a controlled sequence; not all functionality is available

If architecture documentation only describes normal operation, builders and testers are left to infer what the system should do in all other modes. This typically results in inconsistent behavior at mode boundaries, and failure modes that were never discussed becoming visible only in production.

### State Machines as Documentation Tools

State machines are the appropriate tool for documenting system-level mode behavior [src-statemachine]. They make explicit:

- The complete set of modes (you cannot accidentally omit a mode the way prose descriptions can)
- The triggering conditions for each transition (what event or condition causes a mode change)
- Guards (Boolean conditions that must be true for a transition to fire)
- Actions on transitions (what happens during the mode change itself)
- Entry/exit actions in states (what must happen when entering or leaving a mode)

The standard notation: **trigger [guard] / action** on each transition arrow. Example:

```
NORMAL --sensor_failure [failure_count > threshold] / activate_fallback--> DEGRADED
DEGRADED --all_sensors_ok [cooldown_elapsed] / deactivate_fallback--> NORMAL
DEGRADED --critical_failure / emergency_stop--> SAFE_STOP
SAFE_STOP --operator_reset / self_test--> STARTUP
```

This communicates more precisely in four lines than most prose descriptions accomplish in two pages, because the conditions are explicit and the state space is closed.

### Sequence Diagrams for Dynamic Behavior

Where state machines document mode transitions (system-level lifecycle), sequence diagrams document interaction patterns (component-level collaboration). Sequence diagrams are appropriate for [src-arc42]:

- Documenting initialization sequences (what initializes first, why, what happens if early initialization fails)
- Documenting critical flows involving multiple components (the runtime behavior that justifies the C&C architecture)
- Documenting error handling paths (the "sad path" that normal design reviews often skip)
- Documenting concurrency-sensitive interactions (where ordering matters)

The selection principle: don't document every scenario. Document the scenarios that would not be obvious from the static structure alone, and the scenarios where getting it wrong would be costly.

### What Prose Alone Cannot Communicate

Dynamic behavior described only in prose has characteristic failure modes:

- Ambiguous sequencing: "Component A initializes, then B starts up" — does B wait for A to signal completion, or just assume A is done?
- Missing guards: "If the sensor fails, switch to degraded mode" — under what conditions exactly? First failure or sustained failure? Any sensor or specific sensors?
- Missing exit conditions: "Stay in degraded mode until normal operation resumes" — what constitutes "normal operation"?
- Missing error paths: Prose that describes happy path only, leaving all failure handling implicit

The discipline of producing state machines and sequence diagrams forces these ambiguities to surface at documentation time rather than during integration testing.

---

## 5. Interface Documentation

### The Purpose of Interface Docs

Interface documentation exists to enable independent development. A team building a component needs to know what it should expose and what it can depend on. A team using a component needs to know what they can rely on without looking at the implementation. Written interfaces make this independence concrete [src-interface].

Without written interface documentation:
- Teams must coordinate constantly at the code level
- The interface is whatever the implementation happens to do today — there is no contract
- Changes to one component inadvertently break others in ways that only surface during integration
- New team members have no written specification to implement against

### What Goes in an Interface Document

The SEI nine-part interface document template [src-interface]:

1. **Interface Identity** — name and version; if a component has multiple interfaces, each gets separate documentation

2. **Resources provided** — the core section:
   - *Syntax*: "The resource's signature — any information another program will need to write a syntactically correct program" (function name, parameter types, return type)
   - *Semantics*: What actually happens when this resource is used — value changes, events fired, state modifications, observable effects
   - *Usage restrictions*: Preconditions, valid calling contexts, prohibited usage patterns

3. **Data type definitions** — types beyond what the language's standard library provides

4. **Exception definitions** — a dictionary of error conditions, what triggers them, what they mean

5. **Variability** — configuration parameters that change interface behavior, and when they are bound (compile time, startup, runtime)

6. **Quality attribute characteristics** — performance guarantees, reliability properties, security properties visible to callers

7. **Element requirements** — what this component assumes from its environment (its required interface, not just its provided interface)

8. **Rationale and design issues** — why the interface is shaped this way, what alternatives were considered, what constraints drove the shape, what is expected to change

9. **Usage guide** — behavioral protocols, calling sequences, complex interaction patterns shown via sequence diagrams or statecharts

### The Syntax/Semantics Gap

The most common interface documentation failure is documenting only syntax while omitting semantics [src-interface]. Syntax alone — the function signature — is machine-checkable but tells you almost nothing about whether you are using the interface correctly.

A function signature `int read(int fd, void* buf, size_t count)` is syntax. The semantics require stating: reads up to `count` bytes from descriptor `fd` into `buf`; returns the actual bytes read; returns 0 at end-of-file; returns -1 on error and sets errno; blocks indefinitely if no data is available on a blocking descriptor. None of this is in the signature. All of it determines whether a caller's use of the function is correct.

Semantics documentation should describe:
- What state the system is in after a successful call (postconditions)
- What state the system is in after an error (error postconditions)
- What the call must be true before the call (preconditions)
- What invariants the component maintains

### Interface Doc vs. Implementation Doc

What belongs in an interface document [src-interface]:
- What the interface does (semantics)
- What guarantees it makes (quality attributes, error handling)
- What it requires from callers (preconditions, protocols, ordering constraints)
- What can go wrong (error conditions, exceptions, resource limits)

What does NOT belong in an interface document:
- How the implementation achieves its behavior
- Internal data structures
- Algorithm choices
- Code-level design decisions internal to the component

This boundary is important: the team developing a component should only need the interface specification to build against it, not the internal implementation documentation of what they're calling. The interface document is the contract; the implementation document is the interior of one party to the contract.

---

## 6. The Architecture-to-Detailed-Design Boundary

### What Architecture Decides

Architecture is the set of design decisions that are load-bearing for system quality: decisions that, if changed, would require significant restructuring, affect multiple components, or alter the fundamental quality properties of the system [src-vnb].

Concretely, architecture-level documentation specifies:
- The major components and their responsibilities
- The interfaces between components (what each component exposes and requires)
- The communication mechanisms between components (synchronous call, async message, shared data store)
- The decomposition into layers or tiers and the dependency rules between them
- The system's operating modes and mode transitions
- The mapping of components to execution environments (what runs where)
- The key quality attribute decisions (where performance is critical, where consistency is traded for availability, etc.)

### What Detailed Design Decides

Detailed design operates inside the architecture's constraints. It specifies [src-beyondruntime via search results]:
- The internal structure of each component: data structures, classes, modules
- The algorithms used to implement component behavior
- The detailed control flow and error handling within a component
- The detailed API specifications for interfaces (expanding the architecture-level interface contracts to full implementation specs)
- The internal state management and concurrency handling within a component

### The Line

A useful test: could implementation teams working in parallel on different components produce code that integrates correctly, with no communication other than the architecture documentation?

If yes, the architecture documentation is complete. If teams would need to negotiate interface details, clarify what the communication mechanism actually means, or synchronize on behavior in error cases, those gaps belong in the architecture documentation.

A complementary test: does the architecture documentation tell implementers how to implement a component's interior? If yes, the architecture documentation is probably over-constraining. Implementation decisions that don't affect other components belong in detailed design, not architecture.

### The Over-Constraining Anti-Pattern

Over-constrained architecture documentation specifies implementation details that have no cross-component implications. This creates two problems [src-beyondruntime via search results]:

1. Implementers are forced to make architectural change requests for decisions that should be theirs to make
2. The architecture is harder to maintain because it conflates structural decisions (stable) with implementation decisions (variable)

Signs of over-constraining:
- The architecture document specifies algorithm choices for individual components
- The architecture document specifies class-level design within components
- The architecture document describes data structure choices that are not visible across the component boundary

### The Under-Constrained Anti-Pattern

Under-constrained architecture documentation leaves critical cross-component decisions unmade or ambiguous. Integration teams must negotiate these at build time, which delays integration and produces inconsistencies.

Signs of under-constraining:
- Interface semantics are not documented (signature only)
- Error handling behavior at component boundaries is not specified
- System mode behavior is not documented (what happens at startup, at shutdown, in degraded operation)
- Concurrency assumptions are left implicit (whether components assume single-threaded or concurrent access)
- Quality attribute expectations are not documented (what performance a caller may assume, what reliability guarantees a component provides)

The practical heuristic: if a decision's consequences extend beyond one component (meaning changing it requires coordination), it belongs in architecture. If its consequences are entirely internal to one component, it belongs in detailed design.

---

## 7. Practical Documentation Patterns

### The arc42 Structure as a Starting Point

For teams that do not have an existing documentation framework, arc42 provides a practical starting structure [src-arc42]:

- Section 1 (Goals) establishes the quality properties the architecture is trying to achieve — the criteria by which it can be evaluated
- Section 3 (Context) establishes the system boundary — what is inside vs. what is external
- Section 4 (Solution Strategy) captures the key strategic decisions in one place before they are scattered across views
- Section 5 (Building Block View) is the primary static view — decomposition, responsibilities, interfaces
- Section 6 (Runtime View) is the primary dynamic view — how the building blocks collaborate for important scenarios
- Section 9 (Architectural Decisions) is where ADRs or ADR summaries live

Everything is optional. The value is not in filling every section but in having a shared structure that readers know how to navigate.

### The C4 Model as a Visualization Framework

The C4 model provides a practical answer to "what diagrams should we produce?" [src-c4]:

- Context diagram (Level 1): one diagram, produced immediately, for all stakeholders. Shows system boundary and major external actors.
- Container diagram (Level 2): produced early in design. Shows the major building blocks and their technologies.
- Component diagrams (Level 3): produced as needed, per container. Shows internal structure for containers where teams need to coordinate.
- Dynamic diagrams: produced for important scenarios (startup, critical flows, error cases).
- Deployment diagram: produced when deployment topology is non-trivial.

The C4 model's emphasis on diagram quality: every diagram should be self-explanatory without the author present. If it requires a verbal walkthrough, it is not yet good documentation.

### Documentation Coverage Checklist

A minimal set of questions that architecture documentation should answer:

**Structure:**
- [ ] What are the major components and what are each responsible for?
- [ ] What are the interfaces between components (syntax and semantics)?
- [ ] What communication mechanisms connect components?
- [ ] What are the layers and what are the dependency rules between them?

**Runtime:**
- [ ] What modes does the system have (startup, normal, degraded, shutdown)?
- [ ] What triggers each mode transition?
- [ ] How do components interact for the most important use cases?
- [ ] What happens in error cases at component boundaries?

**Deployment:**
- [ ] What executes where?
- [ ] What are the runtime resource requirements and constraints?

**Rationale:**
- [ ] What alternatives were considered and rejected?
- [ ] What constraints shaped the architecture?
- [ ] What quality attributes are prioritized and where?

---

## 8. What the Sources Are Silent On

The sources cover the major frameworks well but have gaps worth noting:

**Documentation maintenance discipline** — all frameworks acknowledge the documentation-code drift problem but provide limited operational guidance on how to keep documentation current as code evolves. The best available guidance is version-controlled ADRs and lightweight C4 diagrams over heavyweight models.

**Documentation for concurrent/distributed systems** — the sources describe communication mechanisms abstractly but provide less guidance on documenting timing constraints, distributed consistency models, and partial failure semantics in C&C views.

**Legacy system documentation** — all frameworks assume documentation written from scratch alongside design. The retrofit case (documenting architecture that already exists in code) is not addressed in the primary sources. Practical approach: start with C4 Level 1-2 from a systems survey, add ADRs retrospectively for the most confusing decisions, add C&C views to explain the runtime structure you observe.

**Documentation for embedded/resource-constrained systems** — the state machine coverage is stronger in embedded-specific sources than in the general architecture documentation frameworks. The interaction between mode documentation (state machines) and allocation views (what runs on which hardware) is underspecified in the general sources.

**Tooling** — the sources discuss notation but largely avoid tool recommendations. In practice, the choice between code-as-diagram (Structurizr, PlantUML), whiteboard-style tools (Miro, Excalidraw), and formal modeling tools (Enterprise Architect, Sparx) significantly affects documentation maintainability. This gap is real and practical for teams starting from scratch.
