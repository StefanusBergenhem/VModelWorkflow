# Research 5f: Architecture Readiness, Derived Requirements, and Integration Test Derivation

Research for architecture craft documentation. Covers when to start architecture work,
what requirements architecture discovers, and how architecture drives integration testing.

**Sources used:**
- [src-nasa-decomp] NASA SPE Handbook §4.3 — Logical Decomposition (https://www.nasa.gov/reference/4-3-logical-decomposition/)
- [src-nasa-reqmgmt] NASA SPE Handbook §6.2 — Requirements Management (https://www.nasa.gov/reference/6-2-requirements-management/)
- [src-specinno-1] SpecInnovations — Rethinking Requirements Derivation Part 1 (https://specinnovations.com/blog/rethinking-requirements-derivation-part-1)
- [src-specinno-2] SpecInnovations — Rethinking Requirements Derivation Part 2 (https://specinnovations.com/blog/rethinking-requirements-derivation-part-2)
- [src-charliealfred] Charlie Alfred — Requirements vs Architecture (https://charliealfred.wordpress.com/requirements-vs-architecture/)
- [src-olzzio] Doc SoC / ZIO — A Definition of Ready for Architectural Decisions (https://medium.com/olzzio/a-definition-of-ready-for-architectural-decisions-ads-2814e399b09b)
- [src-systemswise] Systems-Wise — Technical Measures in System Design (https://systems-wise.com/technical-measures-in-system-design/)
- [src-ozimmer] Olaf Zimmermann — Architectural Significance Test (https://ozimmer.ch/practices/2020/09/24/ASRTestECSADecisions.html)
- [src-wiki-asr] Wikipedia — Architecturally Significant Requirements (https://en.wikipedia.org/wiki/Architecturally_significant_requirements)
- [src-mva] Continuous Architecture — Minimum Viable Architecture (https://continuousarchitecture.com/2021/12/21/minimum-viable-architecture-how-to-continuously-evolve-an-architectural-design-over-time/)
- [src-3pillar] 3Pillar Global — Getting From Requirements to Architecture (https://www.3pillarglobal.com/insights/blog/requirement-gathering-architecture-design/)
- [src-scidir-derived] ScienceDirect — Derived Requirement overview (https://www.sciencedirect.com/topics/computer-science/derived-requirement)
- [src-argondigital] ArgonDigital — Requirements Decomposition (https://argondigital.com/blog/product-management/requirements-decomposition/)
- [src-promwad] Promwad — Latency Budget in Industrial Control Systems (https://promwad.com/news/latency-budget-industrial-control-systems)
- [src-msft-inttest] Microsoft Engineering Playbook — Integration Testing (https://microsoft.github.io/code-with-engineering-playbook/automated-testing/integration-testing/)
- [src-guru99] Guru99 — Integration Testing (https://www.guru99.com/integration-testing.html)
- [src-wiki-trace] Wikipedia — Requirements Traceability (https://en.wikipedia.org/wiki/Requirements_traceability)

---

## 1. When Are Requirements "Ready Enough" to Start Architecture?

### Architecture begins before requirements are complete

The prevailing evidence across sources is clear: architecture work should not wait for requirements to be finished. The IEEE SWEBOK, cited in [src-charliealfred], states: "Architectural design is the point at which the requirements process overlaps with software or systems design and illustrates how impossible it is to cleanly decouple the two tasks."

[src-charliealfred] explains the dependency runs both ways. Without architectural input, detailed requirements often become inconsistent and incomplete. Early design decisions have the greatest impact on meeting quality attributes, making early engagement essential rather than premature.

[src-mva] formalizes this as Continuous Architecture Principle 3: "Delay design decisions until they are absolutely necessary." This is *not* advice to wait — it means avoid deciding things before the inputs that decision depends on are known, but proceed as soon as they are.

### What must be true before architecture can proceed

The readiness question is better framed at the level of individual architectural decisions than at the level of the overall requirements set. [src-olzzio] provides the most concrete framework: a "Definition of Ready" for architectural decisions using the START mnemonic:

1. **Stakeholders Known** — decision makers, consulting stakeholders, and people affected by the outcome are identified and available
2. **Timing Right** — the decision's Most Responsible Moment has arrived; it is important, urgent, and needed now
3. **Alternatives Identified** — at least two design alternatives have been identified and their trade-offs are known or can be assessed
4. **Requirements & Context Clear** — problem context, requirements, and other decision drivers have been analyzed and documented
5. **Documentation Template Ready** — an ADR template is prepared and ready for population

Critically, [src-olzzio] notes that standard Agile Definition of Ready (DoR) and Definition of Done (DoD) apply to features, not to architectural decisions. Teams that rely solely on feature DoR/DoD have no formal gate for architecture work.

### Architecturally Significant Requirements as the entry signal

Not all requirements matter equally to architecture. [src-wiki-asr] defines architecturally significant requirements (ASRs) as those with "a measurable effect on a computer system's architecture." [src-ozimmer] provides a seven-point significance test:

1. **Business Impact** — directly associated with high business value (benefit vs. cost) or business risk
2. **Stakeholder Concern** — represents important stakeholder priorities (sponsors, auditors)
3. **Quality-of-Service Deviation** — runtime characteristics substantially different from what the current architecture handles
4. **External Dependencies** — involves unpredictable, unreliable, or uncontrollable external systems
5. **Cross-Cutting Nature** — affects multiple system parts with system-wide impact (security, monitoring, observability)
6. **First-of-a-Kind** — novel to the team's experience
7. **Historical Trouble** — caused problems or budget overruns on similar past projects

The practical threshold: architecture can begin when the ASRs are sufficiently identified to make the most structurally-committed decisions. [src-wiki-asr] notes these requirements tend to be "hard to define and articulate" and "often overlooked initially" — so a deliberate elicitation step is required, not just passive collection.

[src-ozimmer] recommends a qualitative checklist (Y/N/?/H/M/L scoring) rather than formal calculation, and identifies early architectural decisions that typically cannot be deferred: architectural style selection, technology stack, integration approaches, and minimum product functionality.

### Concrete readiness indicators

Drawing across sources, architecture work on a given decision can proceed when:

- The quality attribute scenarios relevant to that decision can be stated in measurable terms (not just "it should be fast" but "p95 response < 200ms under 1000 concurrent users") [src-ozimmer, src-wiki-asr]
- The external interfaces that will constrain the decision are identified (even if not fully specified) [src-olzzio, src-nasa-decomp]
- Performance budgets at the system boundary are established — even if only at top-level [src-systemswise]
- The stakeholders who will be affected by the decision are known and can provide feedback [src-olzzio]
- Open questions about this decision number fewer than a threshold that can be consciously accepted as risk [src-olzzio — "Timing Right" criterion]

### What the sources are silent on

None of the sources provide a quantitative threshold for "how many open requirements is too many to start." The closest is [src-olzzio]'s "Most Responsible Moment" concept — a qualitative judgment about when deferring the decision starts costing more than making it with known uncertainty.

---

## 2. The Handoff from Requirements to Architecture

### Not a handoff — a collaboration

[src-charliealfred] is explicit: "rather than sequential handoff, the model requires ongoing collaboration." Architects must:
- Identify inconsistencies and gaps in stakeholder requirements
- Validate requirements against technical and environmental constraints
- Work with domain experts to develop consensus solutions
- Ensure detailed requirements remain consistent with architectural strategy

[src-3pillar] describes formal validation checkpoints where "stakeholder concerns around functional needs, non-functional capabilities, identified risks, and anticipated change scenarios" are confirmed before architecture is finalized.

### What flows across

From requirements to architecture:
- Quality attribute scenarios with measurable thresholds
- External interface definitions (what the system must connect to)
- Operational context (load profiles, environments, usage patterns)
- Constraints (technology mandates, integration requirements, regulatory restrictions)
- Prioritized backlog of ASRs [src-wiki-asr, src-ozimmer]

From architecture back to requirements:
- Derived requirements that must be documented and baselined
- Gaps or inconsistencies detected in the upstream requirements
- Performance allocations that become testable requirements at the subsystem level
- Interface specifications between subsystems (which become requirements on each side)

### How to handle requirements still evolving

[src-mva] provides the most actionable guidance. The principle is not to wait for stable requirements but to scope decisions correctly:

- Make decisions only on "known facts, not assumptions"
- Add time-dimensioned planning to quality attribute requirements (what must be true at launch, at 6 months, at 1 year)
- Expand architecture "as soon as new requirements or changes to existing requirements are known"

[src-nasa-decomp] adds the cost-of-change argument: the recursive and iterative architecture development process explicitly anticipates going back to change architecture at higher levels, but "the later in the development process that changes occur, the more expensive they become." The implication is to make the latest responsible decision, not the earliest possible one.

[src-3pillar] recommends architecture spikes — bounded investigations to reduce uncertainty before committing to a decision — as the mechanism for handling "requirements not yet known enough to decide on."

---

## 3. Architecture Discovers Requirements — Derived Requirements

### What derived requirements are

A derived requirement is one that arises from architectural decisions rather than from explicit stakeholder statements. [src-scidir-derived] gives the formal definition: "a requirement that is obtained from a source requirement through analysis, often associated with a rationale."

[src-nasa-decomp] is more specific: "Derived Technical Requirements are requirements that arise from the definitions of the selected architecture that were not explicitly stated in the baselined requirements."

The key mechanism: when a parent requirement is allocated to two or more subsystems, interfaces must exist between those subsystems. Those interfaces require their own requirements on each side. Nobody asked for these — they emerge from the decomposition [src-nasa-decomp].

[src-specinno-2] shows the scale this can reach: 25 design decisions in one case study generated over 60 derived requirements, potentially expanding to ~200 fully elaborated.

### Distinguishing derived requirements from internal design decisions

This is the critical judgment call. [src-specinno-1] provides the clearest test:

- A **derived requirement** answers: "How does the chosen alternative's Structure, Behavior, Footprint, Interfaces, and Lifecycle (SBFIL) impose constraints on the rest of the system?" These constraints propagate beyond the component making the decision.
- A **design decision** is the choice itself — the question answered, not the constraints that result from the answer.

[src-specinno-1] makes the directionality explicit: design decisions remain within the architecture; derived requirements flow upward to be registered in the requirements baseline.

[src-nasa-reqmgmt] calls requirements originating from design decisions "self-derived" requirements. They require:
- Concurrence from higher-level requirement sources
- Independent evaluation to verify they address parent requirements
- Documentation in traceability matrices
- Justification to prevent "gold plating"

The gold-plating check is the practical boundary: if an internal constraint only constrains the component that chose it and has no measurable effect on the system's ability to satisfy parent requirements, it is a design decision, not a derived requirement. If it constrains what neighboring components can do, what the system will cost, or what the system can achieve, it is a derived requirement.

A practical test: if deleting this requirement from the requirements baseline would allow a neighboring system to be built in a way that would create an integration failure — it is a derived requirement. If its deletion only affects the implementation of the component that generated it — it is a design decision.

### Why the feedback loop is usually broken

[src-argondigital] acknowledges the challenge: derived requirements "must sometimes go back to influence earlier specifications, ensuring consistency across the requirement hierarchy," but no source provides a detailed empirical account of why this loop fails in practice. Based on the mechanistic descriptions in the sources, the failure modes are:

1. **Architects treat derived requirements as implementation details** and document them only in architecture documents or design notes, never in the requirements baseline
2. **No formal process** exists for architecture artifacts to generate requirement change requests upstream
3. **Requirements tools and architecture tools are separate** with no automated link — changing a design diagram doesn't trigger a requirements update
4. **Timeline pressure** discourages the rework of requirements that are "already baselined"

[src-nasa-reqmgmt] implies the fix: derived requirements must go through the same change control process as any other requirement change. After baseline establishment, a Configuration Control Board (or equivalent) approves all modifications.

### The formal mechanism for feeding back derived requirements

[src-specinno-1] provides the traceability thread: Decision -> chooses -> Alternative -> results in -> Requirement. This thread is bidirectional — requirements changes can trace back to the decision that generated them, and decision changes cascade to their derived requirements.

[src-scidir-derived] specifies the SysML encoding: the «deriveReqt» relationship (dashed dependency line) from the derived requirement to its source, with rationale documentation.

[src-nasa-reqmgmt] states that requirements changes from architecture work go through impact analysis (cost, schedule, architecture, design, interfaces, operational impacts) before approval.

---

## 4. Integration Tests Come from Architecture, Not Requirements

### The architecture-test correspondence

[src-guru99] states it directly: "Obtain the interface designs from the Architectural team and create test cases to verify all of the interfaces in detail."

Integration tests target the product of architectural decisions — the interfaces between components, the data contracts, the communication protocols, the timing relationships — not the stakeholder needs that motivated building the system. [src-guru99]: "Integration Test Case differs from other test cases in the sense that it focuses mainly on the interfaces & flow of data/information between the modules."

[src-msft-inttest] adds the prerequisite: "the architecture of the project must be fully documented or specified somewhere that can be readily referenced" before integration test design begins. This makes the dependency explicit: integration test design cannot begin before architecture is documented.

### What architectural elements drive integration test cases

From [src-guru99] and [src-msft-inttest], the architectural elements that generate integration test cases are:

| Architectural Element | What to Test |
|---|---|
| API contract between components | Parameter types, return values, error codes, preconditions, postconditions |
| Data flow path between modules | Correct data transformation at each handoff |
| Database interaction | Reads/writes work correctly across the module boundary |
| External hardware connection | Data is received/transmitted correctly under nominal conditions |
| Message protocol between services | Message format, sequencing, error handling |
| Timing dependency | Responses arrive within specified latency bounds |
| Error propagation | Errors at one component surface correctly at the dependent component |

[src-msft-inttest] notes that integration test strategies (top-down, bottom-up, hybrid) map directly to the architecture — top-down uses stubs for lower components not yet integrated; bottom-up uses drivers for higher components.

### Systematic derivation process

Step-by-step, synthesized across sources:

1. **Start from the architectural diagram** — identify all component boundaries [src-guru99, src-msft-inttest]
2. **For each interface**, enumerate: data flowing across, protocol used, error conditions defined, timing constraints [src-guru99]
3. **For each data flow path**, trace from entry point to exit point across all components [src-guru99]
4. **Prioritize critical paths** — the architectural team's identification of critical modules is the test prioritization signal [src-guru99]
5. **For each interface, generate test cases for**: nominal operation, boundary values, error injection, timeout behavior, missing/malformed data [src-msft-inttest combined with general testing practice]
6. **Validate timing** — where the architecture specifies timing bounds, integration tests verify them with measured execution

[src-guru99] provides a concrete example (user login workflow):
- UI -> API: valid credentials are transmitted securely
- API -> Database: query is formed correctly
- Database: token is generated given valid auth request
- API -> UI: token is returned and triggers correct redirect

Each row is one integration test case, derived directly from the interface contract.

### The distinction between integration and system testing

This distinction has a precise technical meaning that most sources agree on:

**Integration testing** verifies that components interact correctly according to their interface contracts — the architecture's design. It validates that the *connections* work as designed [src-msft-inttest, src-guru99].

**System testing** verifies that the assembled system satisfies the original requirements — what stakeholders asked for. It validates that the *system* does what was promised [src-msft-inttest].

[src-msft-inttest] frames it cleanly: "Integration testing confirms a group of components work together as intended from a **technical perspective**, while acceptance testing confirms a group of components work together as intended from a **business scenario**."

The consequence: integration test cases cannot be derived from requirements alone. They require architecture documentation. A project that lacks architecture documentation cannot design integration tests systematically — it can only test end-to-end behaviors, which is system testing.

---

## 5. Timing Budgets as Architectural Constraints

### The allocation problem

When a system-level performance requirement states an end-to-end time bound, architecture must allocate portions of that budget to individual components. This is the most concrete and tractable form of constraint-driven architectural design.

[src-promwad] describes the standard decomposition for a control loop. The same logic applies to any pipeline with multiple processing stages:

**Five budget elements:**
1. Input stage — worst-case sensor acquisition + filtering + sampling alignment
2. Input transport — worst-case network forwarding + jitter
3. Compute stage — worst-case wait for scheduler + worst-case execution time
4. Output transport — same as input direction
5. Output stage — output conversion + actuator response (or equivalent)

### Methodology

The methodology, synthesized from [src-promwad]:

1. **State the system-level constraint** — derive from process dynamics or stakeholder requirement (e.g., "maximum loop delay = 1 ms")
2. **Reserve a margin** — allocate only 60-80% of the budget to identifiable delay components; the remainder is jitter reserve
3. **Bound each stage with worst-case, not average** — average latency does not constrain the system; worst-case does
4. **Allocate the remaining budget across stages** — the allocation reflects architectural knowledge about which stages are hardest to tighten
5. **Sum the bounds** — if the sum exceeds the available budget, the architecture must change before implementation begins
6. **Name the binding constraint** — if the budget is exceeded, the architecture document explicitly identifies which component must be redesigned and by how much

[src-promwad] provides a concrete example for a 1 ms control loop:
- Sensor acquisition: 0.1 ms
- Fieldbus transmission: 0.2 ms
- Controller processing: 0.05-0.1 ms
- Actuator response: 0.3-0.5 ms
- Jitter reserve: remainder of 60-80% allocation

### Budget as requirement

Each per-component budget allocation becomes a derived requirement on that component. The component implementer is constrained by it. If the component's worst-case execution time (WCET) exceeds its budget during implementation, that is a requirements violation requiring a change request — to the architecture (redistribution), or to the system requirement (renegotiation), not an implementation detail to be silently absorbed.

This is where timing analysis creates derived requirements [src-specinno-2, src-nasa-decomp]: the budget allocation for a component is a derived requirement that exists because of the architectural decomposition, not because a stakeholder asked for it.

### Margin discipline

[src-promwad] mandates explicit jitter reserve, sized to the determinism characteristics of the network:
- Deterministic networks (e.g., EtherCAT): tight reserve, e.g., jitter < 0.001-0.005 ms for sub-millisecond cycles
- Best-effort networks: larger reserve to absorb variability

The rule: "Engineers rarely allocate the full cycle time to latency." Allocating 100% of the budget with no margin is an architecture defect — any jitter causes budget violation.

---

## 6. Stakeholder Value Traceability Through Decomposition

### The hierarchy: MOE -> MOP -> TPM

[src-systemswise] presents the standard hierarchy from the INCOSE Technical Measurement Guide:

- **Measure of Effectiveness (MOE)**: "operational measures of success...closely related to achievement of the mission or operational objective" — what the stakeholder actually cares about
- **Measure of Performance (MOP)**: "measures that characterize physical or functional attributes...under specified testing...conditions" — system-level behavior that produces the MOE
- **Technical Performance Measure (TPM)**: "measure attributes of a system element to determine how well...satisfying a technical requirement" — component-level parameter that contributes to MOP

The chain runs: what the user cares about (MOE) -> what the system must do (MOP) -> what each component must deliver (TPM).

[src-systemswise] maps this to architecture levels:
- MOEs operate at the operational/mission level
- MOPs operate at the system architecture level
- TPMs operate at the component/element level below system architecture

### How architecture bridges stakeholder value to technical parameters

Architecture is the translation layer. When an architect decomposes a system, they are not just creating a component diagram — they are allocating MOPs to components and deriving TPMs from those allocations.

The concrete mechanism from [src-systemswise]: "MOPs are traced to system requirements captured in the system model. At the subsystem-level, TPMs are derived and traced back to MOPs and subsystem requirements."

Traceability flows in both directions:
- **Downward**: From MOE, architects derive the MOPs that together satisfy it. From MOPs, they derive TPMs for each contributing component.
- **Upward**: When a TPM cannot be achieved (revealed by analysis or test), it propagates upward. If a component cannot meet its TPM, the MOP it contributes to may be threatened, which may threaten the MOE.

[src-systemswise]: "Traceability back to MOE specifications...allowing for complete traceability from the quantified value properties back to the originating stakeholder concern, enabling quick assessment of impacts from changes to stakeholder concerns."

### Why this matters in practice

Without this traceability, architectural decomposition decisions appear arbitrary. The question "why is this component's maximum execution time 0.1 ms?" cannot be answered except by tracing back through: TPM (0.1 ms execution) -> MOP (20 ms end-to-end response) -> MOE (user perceives response as instantaneous).

With the chain intact, every technical parameter in the architecture has a stakeholder justification. Components that appear to have "overly tight" constraints can be challenged: does the MOP it feeds actually require this TPM, or can the budget be redistributed?

[src-wiki-trace] frames this as "pre-requirements traceability" (backward to stakeholder origin) combined with "post-requirements traceability" (forward to design artifacts, tests, and verification). The MOE-MOP-TPM chain is the pre-requirements traceability carried all the way through decomposition.

### The chain is the architecture's accountability structure

[src-nasa-reqmgmt] states the purpose: "TPM results from Technical Assessment provide an early warning of the adequacy of a design in satisfying selected critical technical parameter requirements." This is the architecture's internal audit mechanism — TPM tracking during development reveals whether the decomposition is holding together before integration.

When a TPM variance appears — a component is performing below its allocated budget — it triggers the question: can the MOP still be met by reallocating budget elsewhere? If yes, this is an architectural redistribution. If no, it becomes a change request that propagates up to the MOP and potentially to the MOE, requiring stakeholder engagement.

---

## 7. Synthesis: What the Sources Agree and Disagree On

### Points of agreement across sources

1. Architecture and requirements are concurrent, not sequential — the clean handoff model is a fiction [src-charliealfred, src-mva, src-nasa-decomp]
2. Derived requirements must enter the requirements baseline, not stay in design documents [src-nasa-reqmgmt, src-specinno-1, src-scidir-derived]
3. Integration tests are driven by architecture artifacts (interface designs), not by requirements [src-guru99, src-msft-inttest]
4. Timing budgets must use worst-case bounds, not average latency, and must reserve margin [src-promwad]
5. Traceability from stakeholder value through MOE/MOP/TPM is the mechanism for keeping architectural decisions accountable [src-systemswise]

### Points where sources differ or are silent

1. **Quantitative readiness threshold**: No source provides a specific number of open questions or percentage of requirements complete before architecture should start. [src-olzzio]'s "Most Responsible Moment" is the closest concept but remains qualitative.
2. **Feedback loop mechanics in practice**: Sources agree the loop exists and must be closed, but [src-argondigital] acknowledges the challenge without providing specific practices to repair broken feedback loops. The mechanics in [src-nasa-reqmgmt] (change control board approval) are described for large-scale engineering programs and may not translate directly to software-only teams.
3. **Integration testing for asynchronous/event-driven architectures**: The sources focus primarily on synchronous request/response interfaces. The [src-msft-inttest] mention of message queues and event-driven communication acknowledges this exists but does not provide a systematic derivation approach for it.
4. **MOE/MOP/TPM in software-only systems**: [src-systemswise] presents this as primarily a systems engineering construct (with hardware components). Application to pure software architectures is implied but not demonstrated with software-specific examples.

---

## Appendix: Key Definitions

**Architecturally Significant Requirement (ASR)**: A requirement that has a measurable effect on the system's architecture. Distinguished by high business impact, cross-cutting scope, external dependencies, novel technology, or historical trouble-causing character [src-wiki-asr, src-ozimmer].

**Derived Requirement**: A requirement that emerges from architectural decisions rather than from explicit stakeholder statements. It is "required" — not a design choice — because it constrains what other parts of the system can do [src-nasa-decomp, src-specinno-2].

**Self-Derived Requirement**: NASA's term for a derived requirement originating from design decisions during the decomposition process. Must be justified, traced to parent requirements, and approved by higher authority to prevent scope creep [src-nasa-reqmgmt].

**SBFIL Test**: A heuristic for surfacing derived requirements from an architectural decision. Ask how the chosen alternative's Structure, Behavior, Footprint, Interfaces, and Lifecycle impose constraints on the rest of the system [src-specinno-2].

**MOE/MOP/TPM chain**: Measure of Effectiveness (operational stakeholder outcome) -> Measure of Performance (system-level behavior) -> Technical Performance Measure (component-level parameter). Architecture's job is to establish and maintain this chain through decomposition [src-systemswise].

**Latency budget**: An allocation of a system-level timing constraint across individual processing stages. Each allocated budget becomes a derived requirement on the component it is assigned to. Must use worst-case bounds and reserve 20-40% as jitter margin [src-promwad].
