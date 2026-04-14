# Research 5c: Architecture Evaluation Methods

Research for architecture craft documentation. Covers how to evaluate whether an
architecture will meet its quality goals before committing to implementation.

**Sources used:**

- [src-atam-wiki] Wikipedia: Architecture Tradeoff Analysis Method — https://en.wikipedia.org/wiki/Architecture_tradeoff_analysis_method
- [src-atam-gfg] GeeksforGeeks: ATAM — https://www.geeksforgeeks.org/software-engineering/architecture-tradeoff-analysis-method-atam/
- [src-atam-concise] ConciseSoftware: ATAM — https://concisesoftware.com/blog/architecture-tradeoff-analysis-method-atam/
- [src-saam] Academia.edu: Scenario-Based Analysis of Software Architecture (Kazman, Bass, Abowd, Webb, IEEE Software 1996) — https://www.academia.edu/15780766/Scenario_based_analysis_of_software_architecture
- [src-lightweight-pmc] PMC/MDPI Sensors 2022: Lightweight Software Architecture Evaluation for Industry — https://pmc.ncbi.nlm.nih.gov/articles/PMC8838159/
- [src-qa-scenarios] ScienceDirect Topics: Quality Attribute Scenario — https://www.sciencedirect.com/topics/computer-science/quality-attribute-scenario
- [src-qaw] EA Voices / SEI: Quality Attribute Workshop — https://eavoices.com/2013/09/10/using-cmusei-quality-attribute-workshop-qaw-while-developing-an-architecture-vision/
- [src-fitness-ci] CodeIntelligently: Architecture Fitness Functions — https://codeintelligently.com/blog/architecture-fitness-functions-testing
- [src-fitness-book] system-design.space: Building Evolutionary Architectures summary (Ford, Parsons, Kua, Sadalage; O'Reilly 2nd ed.) — https://system-design.space/en/chapter/evolutionary-arch-book/
- [src-riskstorming] riskstorming.com: Risk-Storming — https://riskstorming.com/
- [src-adr] adr.github.io: Architecture Decision Records — https://adr.github.io/
- [src-sei-tradeoff] SEI: Reasoning About Software Quality Attributes — https://www.sei.cmu.edu/library/reasoning-about-software-quality-attributes/
- [src-lightweight-techniques] workingsoftware.dev: Fundamental Techniques for Software Architects — https://www.workingsoftware.dev/fundamental-techniques-for-software-architects/

---

## 1. Why Evaluate Architecture Before Building

Architecture decisions made early have an outsized impact on the final system's quality. The cost of discovering a wrong structural decision late — after hundreds of thousands of lines of code exist — is orders of magnitude higher than discovering it before writing any implementation.

Architecture evaluation is the practice of reasoning about quality goals against a structural design before committing to implementation. The goal is to surface risks, expose tradeoffs, and confirm that the architecture as described can plausibly deliver the quality levels the system needs.

Two insights from the SEI body of work frame why this matters [src-sei-tradeoff]:

> "All design involves tradeoffs and if we simply optimize for a single quality attribute, we stand the chance of ignoring other attributes of importance."

> "If we do not analyze for multiple attributes, we have no way of understanding the tradeoffs made in the architecture — places where improving one attribute causes another one to be compromised."

The methods in this document range from multi-day formal workshops (ATAM) to afternoon sessions (LASR, risk-storming) to automated continuous checks (fitness functions). The right approach depends on project risk, team maturity, and available time.

---

## 2. ATAM — Architecture Tradeoff Analysis Method

### 2.1 What it is

ATAM is a structured method for evaluating an existing architecture against quality attribute goals, revealing sensitivity points, tradeoff points, risks, and non-risks [src-atam-wiki]. It was developed at the SEI/Carnegie Mellon and is the most rigorously documented architecture evaluation method available.

The key insight is that ATAM does not evaluate whether the architecture is "good" in the abstract — it evaluates whether specific quality goals are satisfied, and explicitly names where pursuing one goal undermines another.

### 2.2 The four phases

ATAM runs in four phases [src-atam-gfg]:

- **Phase 0 (Preparation)**: Team formation, stakeholder identification, logistics. Evaluation team roles: lead, scribes, questioners, timekeeper.
- **Phase 1 (Steps 1-6)**: One-day session with decision-makers only.
- **Phase 2 (Steps 7-9)**: Two-day session with expanded stakeholder group, after a 2-3 week hiatus.
- **Phase 3 (Follow-up)**: Report generation, findings delivered to stakeholders.

Total elapsed time: typically 4-6 weeks including the Phase 1/2 hiatus. Participant effort: 3 days of meeting time plus preparation.

### 2.3 The nine steps

**Phase 1:**

1. **Present ATAM** — Introduce the method to all present. Set expectations for what the evaluation will and will not produce.

2. **Present business drivers** — The system's key stakeholders explain why the system is being built, what the most important business goals are, constraints, and context. This establishes the "why" that drives quality attribute priorities.

3. **Present the architecture** — The lead architect presents the architecture at an appropriate level of detail: the key structural decisions, module views, component-and-connector views, and any relevant deployment information.

4. **Identify architectural approaches** — The team catalogs the architectural patterns and tactics present in the design: event-driven, layered, client-server, microservices, specific concurrency patterns, caching strategies, etc.

5. **Generate quality attribute utility tree** — The evaluation team works with decision-makers to build a utility tree. This is a hierarchy that decomposes "utility" into quality attributes (performance, modifiability, security, availability, usability), then into specific quality attribute concerns, then into concrete scenarios. Each scenario is rated on two axes: importance to the system and difficulty/risk given the current architecture. High importance + high difficulty items become the focus of deep analysis.

6. **Analyze architectural approaches** — For each high-priority scenario from the utility tree, the evaluation team asks the architect how the architecture supports it. This surfaces sensitivity points and tradeoff points.

**Phase 2 (after 2-3 week hiatus):**

7. **Brainstorm and prioritize scenarios** — A larger stakeholder group generates new scenarios from their own perspectives. These are voted on and prioritized. This step often surfaces quality concerns that the core team had not considered.

8. **Re-analyze architectural approaches** — Step 6 is repeated with the new high-priority scenarios from step 7.

9. **Present results** — The evaluation team delivers all findings: risks, non-risks, sensitivity points, tradeoff points, and an overall risk theme summary [src-atam-concise].

### 2.4 Key outputs defined

**Sensitivity points**: Architectural decisions that have a measurable effect on one or more quality attributes. Example: the choice to use synchronous vs. asynchronous service calls is a sensitivity point for both performance and availability [src-atam-wiki].

**Tradeoff points**: Decisions that are sensitivity points for more than one quality attribute, where those effects conflict. Example: adding encryption at rest improves security but degrades write performance. Tradeoff points are the most valuable outputs — they make implicit conflicts explicit [src-atam-concise].

**Risks**: Architectural choices that, given the quality goals, could lead to undesirable outcomes. Example: a single-threaded request handler is a risk if the performance scenario requires 500 concurrent users [src-atam-gfg].

**Non-risks**: Architectural choices that have been analyzed and found to be sound given the quality goals. These are explicitly recorded — the absence of documentation that a choice was considered is itself a risk.

**Risk themes**: Cross-cutting patterns across identified risks. Example: "we are systematically under-investing in observability" might emerge as a risk theme from several individual risks.

### 2.5 The utility tree

The utility tree is the central analytical artifact of ATAM. It has this structure [src-atam-wiki]:

```
Utility
├── Performance
│   ├── High throughput under load
│   │   └── Scenario: 1000 concurrent users, 95th percentile < 200ms [H/H]
│   └── Startup latency
│       └── Scenario: Cold start completes in < 5s [M/L]
├── Modifiability
│   ├── Adding new payment providers
│   │   └── Scenario: New provider integrated in < 2 days [H/M]
│   └── Schema evolution
│       └── Scenario: DB schema change without downtime [M/H]
├── Security
│   └── ...
└── Availability
    └── ...
```

Each leaf scenario is rated with two priority levels: (importance to the system [H/M/L]) / (difficulty given current architecture [H/M/L]). Scenarios rated H/H drive the deepest analysis.

### 2.6 Running a lightweight version

The full ATAM ceremony is expensive. For most teams, a scaled-down version covering the analytical core (steps 5-6) produces most of the value [src-lightweight-pmc]:

1. Run a single half-day session with 4-6 people: lead architect, product owner, and 2-3 engineers.
2. Spend 30 minutes on business drivers and quality attribute priorities (step 2 condensed).
3. Spend 30 minutes on architecture presentation (step 3 condensed).
4. Build a utility tree together (step 5), targeting 8-12 scenarios. Rate each H/M/L for importance and difficulty.
5. For each H/H scenario, ask: "Walk us through exactly how this architecture handles this." Document sensitivity points and tradeoffs that emerge (step 6).
6. Summarize risks and non-risks.

The lightweight ATAM omits the stakeholder brainstorming phase (step 7) and the formal report. It trades breadth of stakeholder perspectives for speed. This is appropriate when the team has good domain knowledge and the architecture is not yet deeply committed [src-lightweight-pmc].

---

## 3. SAAM — Software Architecture Analysis Method

### 3.1 What it is

SAAM was developed at the SEI in 1994, primarily by Kazman, Bass, and Abowd [src-saam]. It is the predecessor to ATAM and the first formalized scenario-based architecture evaluation method. Its primary focus is **modifiability** — assessing how well an architecture accommodates anticipated changes.

Where ATAM evaluates multiple quality attributes and their interactions, SAAM focuses on a single central question: how costly is it to change this system in the ways we expect it will need to change?

### 3.2 The five steps

1. **Describe candidate architecture** — Present the system using notation that shows components, data flows, and control relationships. The level of abstraction should be "whatever level the scenarios dictate" [src-saam].

2. **Develop scenarios** — Create brief narratives of anticipated uses and changes from multiple perspectives (end-users, developers, maintainers, administrators). SAAM distinguishes two types:
   - **Direct scenarios**: Things the architecture already supports without modification. Running a direct scenario confirms the architecture handles it; failure means a functional gap.
   - **Indirect scenarios**: Anticipated future changes or new requirements that the architecture does not currently support. These reveal modifiability.

3. **Perform scenario evaluations** — For each indirect scenario, identify exactly which architectural components would need to change and estimate the cost of that change (new component? modified interface? specification change?).

4. **Reveal scenario interaction** — "Scenario interaction occurs when two or more indirect task scenarios necessitate changes to some component of a system" [src-saam]. High interaction — multiple unrelated scenarios all touching the same component — signals poor separation of concerns. The component is doing too many things. Low coupling and high cohesion correlate with fewer interactions.

5. **Overall evaluation** — Weight scenarios by stakeholder-assigned importance. If comparing architectures, rank them by weighted cost of change.

### 3.3 Key outputs

- Tabular summary: each indirect scenario with the components it touches and estimated change cost
- Component interaction matrix: a heat map of which components are implicated by many scenarios
- Identification of poor modularity: components with many scenario interactions are candidates for decomposition
- If comparing multiple architectures: ranked comparison by weighted modifiability cost [src-saam]

### 3.4 When to use SAAM vs. ATAM

Use SAAM when:
- The primary concern is modifiability/evolvability of the system
- You are comparing two or more competing architectural candidates
- You want a simpler, faster process focused on one quality dimension
- The team is less experienced with architecture evaluation

Use ATAM when:
- Multiple quality attributes matter and their interactions need analysis
- You need to produce explicit tradeoff documentation for stakeholders
- The system is large, complex, or the architectural decisions are high-stakes
- You have sufficient time and stakeholder availability for a multi-day process

The research literature characterizes SAAM as having been "superseded" by ATAM, but this understates SAAM's value for its specific use case. SAAM remains practically useful because it is simpler, faster, and produces directly actionable output (a list of over-coupled components) [src-lightweight-pmc].

---

## 4. Quality Attribute Scenarios

### 4.1 Why scenarios

A quality goal expressed as "the system should be fast" is useless for architecture evaluation. It cannot be tested against an architectural decision, cannot be prioritized, and cannot reveal tradeoffs. Quality attribute scenarios transform vague goals into testable constraints.

### 4.2 The six-part structure

Each scenario has six components [src-qa-scenarios]:

| Part | Definition | Example (performance) | Example (modifiability) |
|---|---|---|---|
| **Source of stimulus** | Who or what initiates it | 1000 concurrent users | A developer |
| **Stimulus** | What happens | Submit order requests | Adds a new payment provider |
| **Environment** | Operational context | Normal load, peak hours | During active development sprint |
| **Artifact** | Which part of the system responds | Order processing service | Payment integration module |
| **Response** | What the system does | Processes and acknowledges requests | Integration is implemented and tested |
| **Response measure** | How we know it worked | 95th percentile latency < 200ms | Completed in < 2 days without touching existing providers |

The response measure is the critical part. Without it, a scenario is a story, not a testable constraint [src-qa-scenarios].

### 4.3 General vs. specific scenarios

The SEI distinguishes **general scenarios** from **specific scenarios** [src-sei-tradeoff]:

A general scenario is a template — "a system-independent checklist for quality attribute requirements." For example, a general performance scenario might be: "Under [load type] in [operational state], [source] initiates [N] operations; the system processes them with [latency/throughput metric] under [resource constraint]."

A specific scenario is an instantiation of a general template for a concrete system: "Under peak shopping load at 8pm on Black Friday, 5000 concurrent users submit checkout requests; the checkout service processes them with 95th percentile latency below 400ms using no more than 16 CPUs."

Generating scenarios: start with the general template for each quality attribute, then instantiate it with real numbers and real context. Prioritize by business importance.

### 4.4 The Quality Attribute Workshop (QAW)

The QAW is the SEI's structured process for generating and prioritizing quality attribute scenarios when an architecture does not yet exist [src-qaw]. It runs before ATAM, not instead of it.

The seven steps:

1. **QAW presentation and introductions** — Facilitators explain the method and its purpose.
2. **Business/programmatic presentation** — A stakeholder representative presents business drivers, constraints, and goals.
3. **Architectural plan presentation** — A technical stakeholder presents whatever architectural thinking exists (context diagrams, high-level descriptions, constraints).
4. **Scenario generation** — Stakeholders generate scenarios using a participant handbook containing quality attribute taxonomies and examples. Facilitators ensure at least one scenario addresses each architectural driver identified in step 3.
5. **Scenario consolidation** — Similar scenarios are merged.
6. **Scenario prioritization** — All stakeholders vote; scenarios are ranked by aggregate importance.
7. **Scenario refinement** — The top 4-5 scenarios are elaborated: business goals affected, quality attributes involved, sequence of activities, quantitative response measures.

Outputs: architectural drivers list, raw scenario inventory, prioritized scenario list, and fully refined top scenarios [src-qaw].

The QAW's distinct value is forcing stakeholder agreement on quality priorities before architecture decisions are made. The prioritized scenario list becomes the acceptance criteria for any architecture that follows.

### 4.5 Practical guidance

Write scenarios before evaluating any architectural option. If you cannot write a concrete scenario for a quality goal, the goal is not yet well-understood enough to design toward.

A minimum viable set for a new project: 2-3 performance scenarios, 2-3 modifiability scenarios, 1-2 availability scenarios, 1-2 security scenarios. Prioritize ruthlessly — 8-12 scenarios covering the most important goals are more valuable than 50 scenarios covering everything equally.

---

## 5. Architecture Fitness Functions

### 5.1 What they are

An architecture fitness function is "any automated check that validates an architectural property you care about. It runs in CI just like your unit tests" [src-fitness-ci].

The concept comes from Ford, Parsons, Kua, and Sadalage's "Building Evolutionary Architectures" [src-fitness-book]. It applies the testing mindset — make quality criteria executable and automatically checked — to architectural properties rather than just code behavior.

The key insight: "Code review is terrible at catching architectural drift" — one study found a 17% detection rate across 2,400 PRs. Reviewers focus on the code in front of them, not system-wide structural properties [src-fitness-ci]. Fitness functions automate what human review consistently misses.

### 5.2 Types

Four classifications [src-fitness-book]:

- **Atomic**: Validates a single characteristic. Analogous to a unit test. Example: no module in the `domain` package imports from the `infrastructure` package.
- **Holistic**: Examines interactions across multiple characteristics simultaneously. Example: end-to-end latency within budget while staying within memory limits.
- **Triggered**: Activated by specific events — a code commit, a deployment. These run in CI on every PR.
- **Continuous**: Operate persistently in production. These are monitoring-like checks — alerting when a runtime property drifts outside bounds.

Practical categorization by execution speed [src-fitness-ci]:

**Fast (run on every PR — seconds via static analysis):**
- Dependency direction enforcement (no circular deps, no upward layer dependencies)
- Service communication boundaries (microservice A cannot call microservice C directly)
- Database access patterns (only repository layer touches the DB)
- Component size limits (maximum files per module, lines per file)

**Slow (run nightly — require runtime or extended execution):**
- Latency budget validation (p95 for critical paths)
- Load test thresholds
- Cross-service integration properties

### 5.3 Concrete examples

**Dependency direction** — Enforce that dependencies flow from high-level modules to low-level modules. In a layered architecture: `api` → `application` → `domain`, never in reverse. Implementation: static analysis using ArchUnit (JVM), Deptrac (PHP), or custom AST walking. Catches "12 violations in the first month" in practice [src-fitness-ci].

**Latency budget** — For a given endpoint or operation, assert that under load the p95 latency stays within the budgeted amount. Implementation: load test embedded in CI pipeline, assertion on percentile metrics.

**Module cohesion** — Assert that no module exceeds N files or N exported symbols, preventing "god service" growth. Implementation: file count in CI.

**Security scanning** — SAST/DAST tools and dependency auditing as fitness functions for security properties [src-fitness-book].

**Chaos fitness** — Chaos engineering experiments as fitness functions for resilience properties. Example: "system continues serving requests within defined degradation bounds when service X is killed" [src-fitness-book].

### 5.4 Implementation approach

A practical 4-sprint adoption plan [src-fitness-ci]:

**Sprint 1**: Document the intended architecture. Identify the top 3 architectural properties most at risk of drift. Implement dependency direction checks.

**Sprint 2**: Add service boundaries and database access checks. Inventory existing violations. Fix them or explicitly accept them (document in an ADR). Establish baseline metrics.

**Sprint 3**: Add latency and size-limit functions. Build dashboards tracking trends over time.

**Sprint 4**: Make fitness functions a required part of RFC and definition-of-done. Establish quarterly coverage reviews.

### 5.5 Relationship to ATAM

ATAM and QA scenarios identify *what to check*. Fitness functions automate *the checking*. They are complementary:

1. Run ATAM (or a lightweight version) to identify sensitivity points and quality risks.
2. For each risk that can be expressed as a verifiable property, write a fitness function.
3. The fitness function makes the ATAM finding persistent — it will fail if a future change violates the property.

This converts a one-time architectural review into continuous architectural governance.

---

## 6. Tradeoff Reasoning

### 6.1 Why tradeoffs are unavoidable

Architectural decisions rarely optimize a single quality attribute in isolation. The same decision that improves one dimension degrades another. Two well-documented examples:

**Performance vs. modifiability**: Separation of concerns, layering, and use of intermediaries (adapters, facades, anti-corruption layers) all improve modifiability by isolating change. They also add latency, memory overhead, and indirection that degrades performance. "Modifiability is the enemy of performance" [src-sei-tradeoff]. This tension explains why performance-critical systems (databases, trading engines, embedded systems) often have poor modularity.

**Security vs. usability**: Every security measure that increases friction reduces usability. Mandatory MFA, session timeouts, field encryption, and audit logging all improve security while degrading the user experience. "A very secure system may not be very usable" [src-sei-tradeoff].

Other common tensions: availability vs. consistency (CAP theorem), throughput vs. latency, deployability vs. reliability, testability vs. performance.

### 6.2 Making tradeoffs explicit

An implicit tradeoff is a time bomb. When a team chooses a microservices architecture, they implicitly accept higher operational complexity in exchange for independent deployability and scalability. If that tradeoff is never made explicit, future team members will try to "fix" the complexity without understanding why it exists — and will reintroduce the coupling they eliminated.

The SEI's approach [src-sei-tradeoff]: for each architectural decision, document not just the decision but the quality attributes it helps, the quality attributes it harms, and what the net judgment is. ATAM tradeoff points are the formal version of this.

### 6.3 Architectural tactics and their side effects

A **tactic** is a design decision that directly affects a quality attribute. The SEI attribute primitives framework [src-sei-tradeoff] documents each tactic's primary effect and secondary side effects:

| Tactic | Primary effect | Side effects |
|---|---|---|
| Client-server separation | Improved modifiability | Increased network traffic, potential security exposure |
| Data replication/caching | Improved performance | Consistency challenges, increased complexity |
| Heartbeat/health monitoring | Improved availability | Overhead, additional infrastructure |
| Authentication/encryption | Improved security | Latency, implementation complexity |
| Intermediary/façade | Improved modifiability | Performance overhead, indirection |

Every tactic choice is a tradeoff. Making the side effects explicit before committing to a design is the core of tradeoff reasoning.

### 6.4 Prioritizing quality attributes

When tradeoffs must be made, the decision must be grounded in priority. The utility tree (Section 2.5) provides a prioritized list of quality scenarios. When a tradeoff arises, it should be resolved in favor of the higher-priority quality attribute.

Document the resolution explicitly: an Architecture Decision Record (ADR) records that you knew about the tradeoff, you had a priority ordering, and you made the choice deliberately. Future architects reading the ADR understand the reasoning and are not tempted to "fix" a deliberate decision [src-adr].

The Y-statement format from Zdun et al. works well for tradeoff decisions [src-adr]:

> "In the context of [situation], facing [concern], we decided [option], to achieve [quality], accepting [downside]."

Example:
> "In the context of the payment processing service facing a choice between synchronous database transactions and event-sourced writes, we decided to use event sourcing, to achieve horizontal scalability and audit log completeness, accepting increased read complexity and eventual consistency for balance queries."

---

## 7. Lightweight Evaluation Techniques

### 7.1 Why lightweight matters

The industry consistently avoids heavyweight evaluation methods despite research showing they are cost-effective [src-lightweight-pmc]. The barrier is the upfront investment: 3-6 weeks of elapsed time and multiple stakeholder days for full ATAM. For most teams, on most projects, this is simply unavailable.

Practical teams need techniques that produce useful output in hours, not weeks. The goal is not to replicate ATAM's rigor — it is to surface the most important risks before they become expensive.

### 7.2 Risk-storming

Risk-storming is a visual, collaborative technique for identifying architectural risks [src-riskstorming]. It produces a prioritized risk register in 1-2 hours.

**Four steps:**

1. **Draw architecture diagrams** at multiple abstraction levels (e.g., C4 model: context, container, component). Use real diagrams, not whiteboard sketches.

2. **Individual risk identification (10 minutes, silent)** — Each participant independently reviews the diagrams and writes risks on sticky notes, color-coded by severity (red/amber/green). Silent individual work prevents groupthink and ensures quieter team members contribute.

3. **Converge onto diagrams** — Place sticky notes on the diagram near the component or connection where the risk lives. Visual clustering immediately reveals hot spots.

4. **Review and summarize** — Discuss disagreements in priority, risks only one person identified, and patterns across the diagram. Produce a risk register with probability × impact scores (1-9 scale, red 6-9, amber 3-4, green 1-2) [src-riskstorming].

After identifying risks, choose a mitigation strategy for each: education (knowledge/skill gap), prototyping/proof-of-concept (technical uncertainty), or architectural re-work (structural problem). Re-run after significant changes.

Risk-storming complements SAAM and ATAM: it surfaces risks quickly and collaboratively. Use it as a starting point to decide which quality attributes need formal scenario analysis.

### 7.3 Architecture Decision Records (ADRs)

ADRs capture individual architectural decisions with their context, rationale, and tradeoffs [src-adr]. They are the lowest-overhead documentation practice that meaningfully prevents architectural drift.

A minimal ADR contains [src-adr]:
- **Context**: the forces at play, the decision to be made
- **Decision**: what was chosen and why
- **Consequences**: what becomes easier, what becomes harder, what is accepted as a downside

The Y-statement format is a concise alternative: "In the context of [X], facing [concern], we decided [Y], to achieve [quality goal], accepting [downside]."

ADRs serve as the permanent record of tradeoff decisions. They answer the question future architects always ask: "why does this look this way?" Without ADRs, that context lives only in the heads of people who may have left the team.

Best practice [src-adr]: store ADRs as version-controlled markdown files alongside the code they pertain to. Use sequential numbering (ADR-001, ADR-002). Mark superseded ADRs as superseded rather than deleting them — the historical record of what was tried and abandoned is as valuable as the current decisions.

### 7.4 Lightweight ATAM

When the full ATAM ceremony is not viable, a condensed version covering steps 2-3-5-6 produces the analytical core [src-lightweight-pmc]:

Reduces the full 6-week ATAM to under 6 hours by:
- Eliminating or shrinking stakeholder brainstorming (step 7)
- Omitting formal Phase 3 report generation
- Reducing participant count to decision-makers only

The utility tree and sensitivity/tradeoff point analysis remain intact — these are where ATAM's analytical value lives. What is lost is breadth of stakeholder perspectives. Acceptable when the team has strong domain coverage and the evaluation is exploratory rather than final.

### 7.5 LASR — Lightweight Approach for Software Architecture Reviews

LASR is described as "a streamlined and goal-oriented technique for evaluating software architectures" that can be "completed within an afternoon by teams or individuals" [src-lightweight-techniques]. It is positioned as "a leaner alternative to traditional methods such as ATAM."

The sources available do not detail LASR's specific steps. It is worth noting it exists as a named method for teams that find even lightweight ATAM too much overhead.

### 7.6 Industrial practice: what teams actually do

Research into how the industry actually evaluates architectures identifies a frequency ordering [src-lightweight-pmc]:

1. **Experience-based**: Most common. Relies on expert judgment and precedent. Fast but bounded by available expertise and susceptible to bias.
2. **Prototyping-based**: Builds small proofs-of-concept for high-risk decisions. Collects early empirical evidence. Effective for technical uncertainty (will this actually perform as expected?), not for structural tradeoff analysis.
3. **Scenario-based**: Well-researched, used in industry but less frequently than experience-based methods. SAAM and ATAM are the formal versions; informal scenario walkthroughs are the common lightweight version.
4. **Checklist-based**: Domain-specific checklists. Fast and consistent but require creating a new checklist for each domain. Useful as a complement to scenario-based methods.
5. **Metrics-based, simulation-based, math-model-based**: Rare in industry. Require specialized tools and expertise.

The pattern: industry defaults to informal experience-based evaluation and occasional prototyping. Formal methods are used for high-stakes architectural decisions, not routine development. The practical implication: teams benefit most from a lightweight process that is actually used (scenario walkthroughs, risk-storming, ADRs) over a rigorous process that is skipped because it is too costly.

---

## 8. What the Sources are Silent On

The following topics are adjacent to architecture evaluation but not well-covered by the sources gathered:

**Quantitative fitness function thresholds**: The sources describe fitness functions conceptually and give examples, but do not provide evidence-based guidance on how to set threshold values (e.g., what p95 latency is "good enough"). This requires empirical measurement of the specific system.

**Evaluating architectures against architectural styles**: The sources cover quality attribute scenarios and tradeoffs but do not explicitly connect them to specific architectural styles (microservices, event-driven, layered, hexagonal). Knowing that a style has known tradeoff characteristics would accelerate scenario generation.

**Feedback from post-deployment retrospectives**: ATAM and related methods are pre-implementation. The sources do not describe structured methods for retrospectively evaluating whether the architecture delivered its intended quality attributes after the system was deployed.

**Model-driven evaluation**: Mathematical and formal model-based evaluation methods exist (e.g., queueing theory for performance, fault tree analysis for availability) but are classified as rarely used in industry [src-lightweight-pmc] and are not covered in the sources gathered.

**Team size and skill effects**: The sources treat architectural evaluation as a method problem, not a team problem. There is no coverage of how evaluation quality degrades with inexperienced teams, or how to calibrate the depth of evaluation to team capability.

---

## 9. Summary: Choosing the Right Approach

| Situation | Recommended approach |
|---|---|
| Architecture not yet designed; need to prioritize quality goals | QAW — identify and prioritize quality attribute scenarios first |
| High-risk architectural decision; multiple quality attributes competing | ATAM (or lightweight ATAM) — utility tree, sensitivity/tradeoff points |
| Need to compare two or more architectural candidates on modifiability | SAAM — direct/indirect scenarios, component interaction matrix |
| Need to quickly surface team's diverse risk perspectives | Risk-storming — 1-2 hour collaborative session |
| Need continuous guard against architectural drift | Fitness functions in CI/CD |
| Need to record and persist tradeoff decisions | Architecture Decision Records |
| Post-ATAM: want ATAM findings to survive code evolution | Convert ATAM tradeoff points into fitness functions |

These techniques are not mutually exclusive. A well-run project uses QAW before committing to an architecture, runs a lightweight ATAM when the architecture is drafted, uses ADRs for every significant decision, incorporates fitness functions for the most critical properties, and runs risk-storming at major milestones.
