# Research 3b: Requirements Completeness, Allocation, and Decomposition

Structural aspects of a system requirements set: how to achieve completeness, how to
allocate requirements to SW/HW/operational, how decomposition creates derived requirements,
how to specify interfaces, how to handle operational modes, and how system requirements
drive system tests.

**Sources used (all read directly in this session):**
- ASPICE PAM v4.0 [src-aspice-4-0] — pp. 34-42, read from PDF (SYS.1-SYS.4 verbatim)
- Peterson 2015, NASA/CR-2015-218982 [src-peterson-arp4754a-2015] — pp. 39-71, read from PDF
  (ADP100 case study: requirements capture, validation, verification, allocation, tracing;
  SDP100 case study: validation matrix, verification matrix; PASA CMA tables; ARP4754A
  Objectives Mapping Table 6)
- SEBoK System Requirements Definition page [web-sebok-srd-2026] — fetched in this session
- ISO 26262 HSI specification paper [web-hal-hsi-2015] — fetched in this session (partial)
- ISO 26262 requirement types [web-btc-req-types-2026] — fetched in this session
- Web search synthesis on completeness definitions and IEEE 1233 [web-search-completeness-2026]

**IMPORTANT NOTE on source limitations:**
- ARP 4754A primary standard text is paywalled (SAE). Claims about ARP 4754A content use
  the Peterson 2015 NASA report as a primary secondary source — Peterson applies ARP 4754A
  directly and reproduces objectives in Table 6 and the case study artifacts. This is
  considered high-confidence secondary access.
- ISO 26262 primary standard text is paywalled. Claims cite the Peterson/BTC/HAL secondary
  sources, marked accordingly.
- INCOSE GtWR v3 and SE Handbook v5 are paywalled. Claims from INCOSE are via ASPICE PAM
  normative reference and SEBoK web content.
- MIL-STD-961E, NASA-STD-8739.8, NPR 7123.1 were not retrieved in this session. Claims
  that would depend on those sources are marked [unverified].

---

## 1. What "Completeness" Means — and Why It Can't Be Proven

### 1.1 The Fundamental Problem

Requirements completeness is conceptually simple and practically hard. IEEE 1233-1998
defines a requirement as complete when "the responses of the software to all realizable
classes of input data in all realizable classes of situations are included." [web-search-completeness-2026]

The problem: we cannot enumerate "all realizable classes of input data" and "all realizable
classes of situations" without already having a complete model of the system — which
presupposes what we are trying to build. This makes **provable completeness logically
unattainable** for any non-trivial system. [web-search-completeness-2026]

The implication is sharp: completeness is a best-effort pursuit, not a verifiable property.
A requirement set can only achieve "no known gaps as of this review," never "no gaps exist."
[web-search-completeness-2026]

### 1.2 Two Distinct Completeness Concepts

Two distinct forms of completeness must be distinguished:

**Formal completeness** (structural): Does the requirements document follow its template?
Are all required sections present? Are all required attributes filled? This is checkable
by automated tooling. Proposed metrics include Template Completeness Factor (TCPF) and
Definition Completeness Factor (DCPF). [web-search-completeness-2026]

**Semantic completeness** (content): Are all necessary behaviors, constraints, and
properties captured? This requires expert judgment. One metric is the Missing Semantic
Element Count (MSEC), where a domain expert identifies missing elements. [web-search-completeness-2026]

Formal completeness is necessary but not sufficient. A fully-attributed requirements
document can still be semantically catastrophically incomplete.

### 1.3 The SEBoK Category Coverage Approach

The SEBoK System Requirements Definition article recommends a category-coverage strategy:
a requirements set is complete when each category of required content has been addressed.
The SEBoK identifies five top-level categories: [web-sebok-srd-2026]

| Category | Examples |
|---|---|
| Function/Performance | Primary functions with performance attributes |
| Fit/Operational | Secondary/enabling functions and system interactions |
| Form | Physical characteristics, observable parameters |
| Quality | "-ilities": reliability, maintainability, operability |
| Compliance | Standards, regulations, certification requirements |

The completeness claim: "for the set of requirements to be complete, each category topic
must be addressed." [web-sebok-srd-2026]

This is the most actionable completeness strategy available without full formal methods:
run through a coverage checklist and identify gaps. It shifts the question from "is it
complete?" to "which categories have gaps?"

### 1.4 ASPICE SYS.2's Completeness Obligation

ASPICE SYS.2 Outcome 1 requires that system requirements are specified. The BP1 note
explicitly lists verifiability as one of the "defined characteristics" that requirements
must satisfy: "verification criteria being inherent in the requirement text" [src-aspice-4-0 §4.3.2 p.36].

This establishes an implicit completeness obligation: any system requirement that lacks
a verifiable form is not a complete requirement. Completeness and testability are
intertwined in the ASPICE view.

ASPICE also acknowledges in SYS.2.BP5 Note 8 that "there may be non-functional stakeholder
requirements that system requirements do not trace to" — specifically process requirements.
This is a deliberate, documented gap, not an incompleteness. [src-aspice-4-0 §4.3.2 p.37]

Similarly, SYS.3.BP4 Note 8 notes that "there may be non-functional requirements that the
system architectural design does not address or represent" — architecture traces to
requirements that represent physical end-product properties; non-physical requirements
(process requirements, quality management requirements) do not trace to architecture
elements. [src-aspice-4-0 §4.3.3 p.39]

**Key insight:** completeness is not the same as "every stakeholder requirement has a
system requirement trace." Some requirements are intentionally not decomposed into system
requirements; the standard explicitly acknowledges this.

### 1.5 ARP 4754A's Completeness Standard

ARP 4754A Objective 4.1 states: "Aircraft, system, item requirements are complete and
correct." [src-peterson-arp4754a-2015 Table 6 p.44]

The Peterson case study's SDP100 (Company "A" Avionic System Development Plan) specifies
how this is operationalized:

> "The validation of requirements and specific assumptions ensures that the specified
> requirements are sufficiently correct and complete so that the developed product will
> provide the intended functionality." [src-peterson-arp4754a-2015 p.67 SDP100 §5.2]

The mechanism is explicit: completeness is achieved through validation, not through
enumeration. ARP 4754A defines five validation methods: traceability, analysis (modeling),
test, similarity, and inspection (engineering review). All five may be used in combination.
[src-peterson-arp4754a-2015 p.68 SDP100 §5.2.1]

The validation matrix (Table 18 in Peterson) is the artifact that tracks completeness
status: each requirement has a "Reqt Valid (Y/N)" field populated only when validation
effort is complete and artifacts confirm validity. [src-peterson-arp4754a-2015 p.69 Table 18]

### 1.6 Completeness via Model-Based Coverage

A complementary approach to checklist-based completeness is coverage through functional
models:

**Use case coverage:** Every identified use case must be traceable to at least one
functional requirement. If a use case has no requirement, the requirements set has a gap.
[web-sebok-srd-2026]

**Mode coverage:** Every operating mode of the system (normal, degraded, startup,
shutdown, maintenance, emergency) must have requirements. Mode gaps are a common class
of incompleteness. [unverified — synthesized from domain knowledge; see Section 5 below]

**Interface coverage:** The SEBoK observation that functional requirement percentage and
external interface requirement percentage should be "similar within about 10%, with
Functional on the higher side" provides a rough heuristic for interface completeness.
[web-search-completeness-2026] When interface requirement count is far below functional
requirement count, a completeness gap is likely.

**Negative (inhibitory) requirements:** Complete requirements sets must include not only
what the system shall do, but what it shall not do — especially for safety and security.
Requirements such as "the autopilot shall not issue commands exceeding ±X degrees of
authority" are negative constraints that define safety envelopes. In aviation, these
often emerge directly from FHA failure conditions. [src-peterson-arp4754a-2015 Table 2 pp.22-28
PASA CMA Tables 9-15, pp.51-57]

The Peterson case study PASA Section CMA lists 11 independence requirements of the form
"function X shall be independent of function Y" — all negative constraints that no amount
of functional decomposition would naturally produce. They emerge from safety analysis.
[src-peterson-arp4754a-2015 pp.48-49]

---

## 2. Requirements Allocation

### 2.1 What Allocation Means

Requirements allocation is the process by which requirements at one level of the
architecture are assigned to entities at the next lower level. It converts a system-level
"what" into item-level "what each part must achieve." [web-sebok-srd-2026]

Allocation answers two questions:
1. Which architectural element is responsible for satisfying each requirement?
2. When multiple elements together satisfy one requirement, what is each element's share
   (budgeting)?

**Budgeting** is a critical companion concept: "the system requirement value may be
decomposed to ensure the lower-level elements contribute their portion." Typical budgeted
parameters include mass, power usage, bandwidth, response time, and failure rate budget.
[web-sebok-srd-2026]

### 2.2 ARP 4754A Allocation Process

In the ARP 4754A framework, the allocation structure has three tiers: [src-peterson-arp4754a-2015 p.41
Figure 6]

```
Aircraft-level function requirements
    ↓  (Airplane Function Requirement Allocated to Systems)
System requirements
    ↓  (System Requirement Allocated to Items)
Item requirements (SW/HW)
```

ARP 4754A Objective 2.6 explicitly requires: "System requirements are allocated to the
items." Output artifact: Item Requirements. [src-peterson-arp4754a-2015 Table 6 p.44]

The Peterson case study Table 16 (Reuse Strategy) shows the practical allocation artifact:
each system functional area (Autopilot/Autoflight ATA22, Communications ATA23, Displays
ATA31, etc.) is decomposed into SW items and HW items, each with an assigned FDAL/IDAL.
[src-peterson-arp4754a-2015 p.62 Table 16]

### 2.3 The Allocation Criteria Problem: SW vs. HW vs. Operational

What determines whether a requirement is allocated to software, hardware, or operational
procedures? The standards do not prescribe a single algorithm. The allocation decision
involves engineering judgment on several criteria:

**Partition by implementation domain:**
- If the requirement concerns a computational function (algorithm, data processing,
  state management) → typically SW
- If the requirement concerns physical properties (timing constraints from hardware,
  signal characteristics, memory capacity) → typically HW
- If the requirement concerns human actions (response to warnings, manual override
  procedures) → typically operational procedures

**ISO 26262 allocation criterion:** Technical Safety Requirements (TSRs) are allocated
to HW, SW, or a combination based on which domain provides the required safety mechanism.
ASIL is then assigned to each element based on the highest ASIL of any requirement
allocated to it. [web-btc-req-types-2026]

**ASPICE SYS.3.BP1 criterion:** Allocation to system elements is governed by "functional
and non-functional system requirements, including external interfaces." [src-aspice-4-0 §4.3.3 p.38]
The architecture defines elements; requirements are then assigned to elements. The
allocation table is the traceability artifact.

### 2.4 Requirements That Span SW and HW

Some requirements cannot be cleanly allocated to a single domain because they describe
a property that only emerges from the combined behavior of HW and SW. These are the
hardest allocation cases. Strategies include:

1. **Decompose into domain-specific requirements:** Decompose the spanning requirement
   into a HW requirement (what the hardware must guarantee) and a SW requirement (what
   the software must guarantee given those hardware guarantees). Document the parent
   requirement and the two children.

2. **Allocate to the integration level:** Assign the requirement to the integration tier
   where it can be verified — typically the HW-SW interface. This is the mechanism that
   produces Interface Requirements (see Section 4).

3. **Shared responsibility with explicit assumptions:** One domain satisfies the
   requirement with explicit assumptions about the other domain. Those assumptions must
   be validated (ARP 4754A Objective 4.2: "Assumptions are justified and validated"
   [src-peterson-arp4754a-2015 Table 6 p.45]).

The Peterson PASA CMA tables show this pattern for independence requirements: requirements
like "navigation capability shall be independent of communication capability" span
architecture, hardware, software, and development processes. The analysis examines all
three domains (external sources, technology/equipment type, and specifications) for each.
[src-peterson-arp4754a-2015 Table 11 p.53]

### 2.5 ASPICE SYS.3 as the Allocation Process

ASPICE SYS.3 (System Architectural Design) is where allocation formally happens. SYS.3
Outcome 1 requires: "A system architecture is designed including a definition of system
elements with their behavior, their interfaces, their relationships, and their interactions."
[src-aspice-4-0 §4.3.3 p.38]

Allocation is embedded in SYS.3.BP1: requirements are assigned to elements when the
static architecture is specified. SYS.3.BP2 requires dynamic aspects — behavior in
different system modes — to be specified, which is where mode-specific allocation occurs.
[src-aspice-4-0 §4.3.3 p.38]

SYS.3 Outcome 3 mandates bidirectional traceability between architecture elements and
system requirements — this is the allocation table. A requirement with no architecture
element = not allocated. An architecture element with no requirement = unexplained design.
[src-aspice-4-0 §4.3.3 p.39]

The SYS.3.BP4 note clarifies a nuance: "there may be non-functional requirements that
the system architecture does not address or represent (direct properties/characteristics
of the physical end product)." Non-physical non-functional requirements do not trace to
architecture — they trace to process activities or quality management. This must be
documented, not left as a gap. [src-aspice-4-0 §4.3.3 p.39]

### 2.6 Allocation Table Structure

A practical allocation table (derived from Peterson case study patterns and SEBoK
guidance) contains:

| Req ID | Requirement text | Safety | FDAL/IDAL | Element(s) | Domain | Notes |
|---|---|---|---|---|---|---|
| SYS-001 | The autopilot command shall not exceed ±15° authority | Y | A | SW-AFCS-App, HW-AP-Control | SW+HW | Independence req (CMA) |
| SYS-002 | The system shall display primary attitude information | N | A | HW-Display-PFD, SW-PFD-Graphics | SW+HW | — |
| SYS-003 | The operator shall acknowledge all MASTER CAUTION alerts | N | C | Operational Procedure | Operational | Captured in AFM |

The "Domain" column is the allocation decision. "Notes" captures the rationale and any
cross-domain dependencies.

---

## 3. Requirements Decomposition and Derived Requirements

### 3.1 What Decomposition Is

Requirements decomposition is the transformation of a high-level requirement into a
set of more detailed requirements that together satisfy the parent. The decomposed
requirements can be verified more concretely, and together they provide full coverage
of the parent intent.

The SEBoK describes decomposition as: "functional analysis, interface analysis, data
flow diagrams, and performance analysis inform requirement generation — multiple
requirements may result from analyzing a single need statement." [web-sebok-srd-2026]

The key distinction from allocation: decomposition is about breaking one requirement
into several; allocation is about assigning requirements to elements. Decomposition
typically precedes allocation — you decompose a high-level requirement into pieces,
then allocate each piece.

### 3.2 Parent-Child Relationships and Traceability

Decomposition creates a parent-child requirement hierarchy. Requirements traceability
must preserve this hierarchy:

- A child requirement must trace back (backward) to its parent requirement
- A parent requirement is satisfied only when all its children are satisfied and verified
- Bidirectional traceability must be maintained: parent→children and children→parent

In the Peterson case study, the requirement management artifacts explicitly include
"parent trace linkage capability" as a mandatory requirement attribute in the baseline
requirements set. [src-peterson-arp4754a-2015 p.64 SDP100 §5.1]

The Peterson baseline requirement set lists five mandatory attributes for every requirement:
unique requirement identifier, requirement text, rationale (reason for having the
requirement if derived), parent trace linkage, and safety-related attribute.
[src-peterson-arp4754a-2015 p.64 SDP100 §5.1]

The rationale field is particularly important for derived requirements — it must explain
*why* the requirement exists when it is not directly traceable to a parent.

### 3.3 Derived Requirements: Definition and Origin

ARP 4754A defines derived requirements as "additional requirements resulting from design
or implementation decisions during the development process that are not directly traceable
to higher-level requirements." [unverified — standard is paywalled; claim from Peterson
secondary source, ARP4754A Objective 2.4 language]

ARP 4754A Objective 2.4 requires: "System derived requirements (including derived
safety-related requirements) are defined and rationale explained." Output: System
Requirements. [src-peterson-arp4754a-2015 Table 6 p.44]

Three sources of derived requirements in practice:

1. **Architecture decisions:** A design decision that introduces a new component or
   constraint creates requirements that the higher level never contemplated. Example:
   choosing a shared bus requires timing requirements on each consumer that did not
   exist at the aircraft-function level.

2. **Safety analysis:** The PSSA/FTA process identifies required failure rates, required
   independence, required monitoring, and required safe states that the original
   stakeholder needs did not specify. These are derived from architecture, not from
   stakeholders. In the Peterson case study, all 11 CMA independence requirements are
   derived — they emerge from fault tree analysis, not from stakeholder elicitation.
   [src-peterson-arp4754a-2015 pp.48-57]

3. **Implementation constraints:** Platform limitations, reuse constraints, or regulatory
   requirements that constrain how something is built produce derived requirements on the
   implementation.

### 3.4 The Derived Requirements Feedback Loop

This is the most critical structural aspect of requirements decomposition in safety-critical
systems: **derived requirements must be fed back up for safety impact assessment.**

In the ARP 4754A framework, derived requirements from DO-178C (software) or DO-254
(hardware) development must be fed back to the system level (ARP 4754A) and to the
safety assessment (ARP 4761) to confirm no unintended safety impact.
[src-peterson-arp4754a-2015 Table 6 Objective 2.4 p.44]

The Peterson case study captures this in the validation matrix (Table 18): derived
requirements are explicitly tagged as "Derived" in the Requirement Source column, and
they require validation just like parent-traceable requirements. Assumptions made during
requirements capture also require validation (ARP 4754A Objective 4.2).
[src-peterson-arp4754a-2015 p.69 Table 18]

The feedback loop looks like this:

```
System requirements
    ↓  (allocated to SW/HW items)
SW/HW development discovers derived requirements
    ↓  (derived requirement created: no parent trace)
Derived requirement fed back to system level
    ↓  (rationale documented, safety impact assessed)
Safety analysis updated if required
    ↓  (no adverse safety impact confirmed)
Derived requirement baselined in system requirements set
```

The ADP100 case study explicitly notes this as a non-linear feedback path: "the non-linear
aspects of the development activities (feedback paths) are not shown" in the simplified
lifecycle diagram. [src-peterson-arp4754a-2015 p.39 ADP100 §2]

### 3.5 ASPICE Note on Derived Requirements

ASPICE SYS.2 does not use the term "derived requirements" explicitly in SYS.2 — this is
a standard limitation. However, the traceability obligation in SYS.2.BP5 implicitly
addresses it: requirements that emerge from architecture analysis (SYS.3) must trace
back to system requirements, and system requirements must trace to stakeholder requirements.
A requirement with no stakeholder trace needs explicit documentation of its source.
[src-aspice-4-0 §4.3.2 pp.36-37]

The SYS.3.BP1 note on non-functional requirements that the architecture doesn't address
also creates the flip side: some stakeholder requirements legitimately have no system
requirement trace (process requirements), and some system requirements legitimately have
no stakeholder parent (derived from architecture). Both must be documented rather than
left as unexplained gaps. [src-aspice-4-0 §4.3.3 p.39]

---

## 4. Interface Requirements

### 4.1 Why Interface Requirements Are Their Own Category

Interface requirements specify what must happen at the boundary between systems, or between
HW and SW within a system. They are distinct from functional requirements because they
describe an agreement between two parties, not a capability of one party.

The SEBoK articulates the three-step process for interface requirements: [web-sebok-srd-2026]

1. Identify interface boundaries and cross-boundary interactions
2. Define interaction characteristics and media
3. Write formal interface requirement statements

An example interface requirement: "The System shall send telemetry to the Ground System
as defined in ICD 123, Table X." [web-sebok-srd-2026]

Interface requirements frequently reference Interface Control Documents (ICDs) or
Interface Specifications by document number and table/section — the interface requirement
establishes the obligation and the ICD provides the detail.

### 4.2 System-to-System Interface Requirements

At the system-to-system level, interface requirements must address: [web-sebok-srd-2026]

- **Protocol:** What communication protocol? (ARINC 429, CAN, Ethernet, AFDX, etc.)
- **Data format:** What message format, encoding, data types, value ranges?
- **Timing:** What is the maximum latency? What is the message rate? What constitutes
  a timeout?
- **Error handling:** What happens when the interface fails? What is the failure detection
  mechanism? What is the recovery behavior?
- **Initialization:** What must both sides guarantee before the interface is considered
  operational?

These five dimensions are necessary for any interface requirement to be both complete
and testable.

### 4.3 The Hardware-Software Interface (HSI) Specification

The most precisely defined interface requirement construct in safety-critical standards
is the Hardware-Software Interface (HSI) specification from ISO 26262.

ISO 26262 Part 4 (System Level) requires an HSI specification as an output of the
Technical Safety Concept. The HSI is the last system-level development artifact and
the starting point for parallel HW and SW development. [web-hal-hsi-2015]

The HSI specification must include: [web-hal-hsi-2015]

- Hardware components controlled by software
- Hardware resources supporting SW execution (memory, bus, I/O, computational capacity)
- Shared resources and arbitration mechanisms
- Operating constraints imposed by HW on SW (timing, sequencing, value ranges)
- Operating modes of hardware devices and SW configuration parameters
- Hardware features assuring element independence
- Access mechanisms and timing constraints for hardware components
- Failure modes: how hardware failures are communicated to software

**Why the HSI matters for requirements completeness:** Without an explicit HSI,
hardware and software development teams make implicit assumptions about the other side.
These assumptions are then invisible to safety analysis. The HSI forces those assumptions
to become explicit requirements. [web-hal-hsi-2015]

**The HSI as boundary document:** The HSI specification embodies a formal contract. It
defines hardware assumptions about software behavior, and software requirements imposed
by hardware limitations. A requirement in the HSI is simultaneously a constraint on the
HW designer and a requirement on the SW designer.

### 4.4 Interface Requirements in the Aviation Framework

ARP 4754A Objective 2.3 requires: "System requirements, including assumptions and system
interfaces are defined." Output: System Requirements. [src-peterson-arp4754a-2015 Table 6 p.44]

The Peterson case study ADP100 explicitly calls out "unique SAAB-EII 100 airplane
characteristics (e.g. interfaces, functional properties, installations)" as a required
output of requirements development — interfaces are treated with the same status as
functional requirements. [src-peterson-arp4754a-2015 p.39 ADP100 §2]

ASPICE SYS.3.BP1 requires specification of "external interfaces and a defined set of
system elements with their interfaces and relationships" as part of the static architecture.
[src-aspice-4-0 §4.3.3 p.38] Interface specifications trace to system requirements;
they are architecture elements that must satisfy interface requirements.

### 4.5 Interface Requirements Testability Challenge

Interface requirements are often harder to test than functional requirements because they
require both sides to be present or simulated. At the system level, the test environment
must include:

- Real, simulated, or emulated external systems
- The ability to inject valid and invalid interface behavior
- Measurement of timing characteristics (latency, message rates)
- Fault injection at the interface boundary

ASPICE SYS.4 (System Integration and Integration Verification) BP1 explicitly addresses
interface testing: "Examples on what a verification measure may focus on are the timing
dependencies of the correct signal flow between interfacing system elements, or interactions
between hardware and software, as specified in the system architecture." [src-aspice-4-0 §4.3.4 p.41]

---

## 5. Operational Modes and Mode-Specific Requirements

### 5.1 Why Modes Matter for Requirements Completeness

A system's requirements are incomplete unless they specify behavior in every mode the
system can occupy. Mode gaps are one of the most common causes of system failures in
safety-critical systems — the normal-mode requirements were specified carefully, but the
behavior during startup, shutdown, recovery, or degraded operation was left implicit.

ASPICE SYS.3.BP2 explicitly requires specification of dynamic aspects "including the
behavior of system elements and their interaction in different system modes."
[src-aspice-4-0 §4.3.3 p.38]

ISO 26262 Part 3 Clause 7 (Functional Safety Concept) requires a "warning and degradation
concept" and "safe state definition" as mandatory outputs — both are mode-related.
[src-01-standards, from Research 1]

### 5.2 The Mode Taxonomy

Safety-critical system modes can be grouped into six categories. Each requires its own
requirements:

| Mode | Description | Typical Requirements Content |
|---|---|---|
| **Initialization** | System startup from power-off | Self-test requirements, initialization timeouts, safe behavior if self-test fails |
| **Normal operation** | Intended operating condition | Full functional requirements |
| **Degraded operation** | Reduced capability after partial failure | What functions remain available, what is disabled, what is the performance degradation |
| **Emergency/fail-safe** | Active safety response to detected critical failure | Safe state definition, transition trigger, behavior in safe state, how to recover |
| **Maintenance** | System in maintenance mode | What functions are suspended, special operator access, data loading |
| **Shutdown** | Planned or emergency shutdown | Required state at shutdown, any shutdown sequence |

The Peterson FHA Summary table (Table 2, pp.22-28) shows mode specificity in practice:
every failure condition is tagged to one or more flight phases (Take-off, Approach,
Landing, Go Around, Flight, All) — these are the operating mode categories for the
avionics system. Requirements derived from each failure condition apply only in the
specified mode(s). [src-peterson-arp4754a-2015 pp.22-28 Table 2]

### 5.3 Degraded Modes and Graceful Degradation

Graceful degradation is the planned ability to maintain the most safety-critical functions
when parts fail, by entering a predefined degraded mode where non-critical features are
suspended or simplified. [web-search-operational-modes-2026]

Requirements for degraded modes must specify:
- What triggers the transition to the degraded mode (fault detection criterion)
- What capabilities are reduced or removed
- What capabilities are guaranteed to remain
- What indicators are provided to the operator
- What the operator must do (or not do) in degraded mode
- How the system recovers to normal mode (if recovery is possible)

In ISO 26262, the Functional Safety Concept must define "fault tolerance through
redundancy/degradation" and "transitioning to/maintaining safe states." [web-btc-req-types-2026]
The Fault Tolerant Time Interval (FTTI) — the minimum time from fault to potential
hazard — is a timing constraint on when the system must have detected and responded to
a fault. Requirements for degraded mode transitions must satisfy FTTI constraints.

### 5.4 Safe State Requirements

A safe state is a system state in which no harm can occur, even given the presence of
the detected failure. Safe state requirements specify:

1. **State definition:** What is the system's configuration in the safe state?
2. **Transition trigger:** What conditions cause transition to the safe state?
3. **Transition timing:** Within what time from fault detection must the safe state
   be reached? (FTTI budget)
4. **Behavior in safe state:** What functions continue to operate? What is disabled?
5. **Exit conditions:** Under what conditions can the system leave the safe state?

From the Peterson case study: the avionics functions analysis explicitly considers
"loss of capability" failure conditions and documents the crew's ability to continue
flight under manual control — this establishes what the degraded state looks like and
what residual capability must be guaranteed. [src-peterson-arp4754a-2015 Table 2 FC 22.05, 22.06 p.27]

### 5.5 Mode Requirements and Safety Analysis Coupling

Mode requirements cannot be written independently of safety analysis. The FHA (aviation)
or HARA (automotive) determines which failure conditions are unacceptable in which modes.
Those determinations directly generate requirements for how the system must behave when
those conditions are detected.

The iteration is mandatory: as safety analysis refines the mode model, mode requirements
must be updated. As mode requirements are written, safety analysis must verify the
requirements are consistent with the safety objectives.

**Common failure pattern:** Mode requirements are written from the normal-mode perspective.
The safety analysis is done as a separate exercise. The two are never reconciled. The
result is a requirements set where mode transitions lack timing requirements, where safe
state definitions are vague, and where it is impossible to verify that the safety objectives
are actually met. [synthesis from ARP 4754A/ISO 26262 structural analysis in this research]

---

## 6. System-Level Test Derivation

### 6.1 The Traceability Obligation

In all three major safety frameworks, every system requirement must have at least one
verification activity that demonstrates the requirement is met. This creates a mandatory
requirements-to-test traceability obligation:

**ARP 4754A Objective 5.3:** "Product implementation complies with aircraft, and system
requirements." Output: Verification Results. [src-peterson-arp4754a-2015 Table 6 p.45]

**ASPICE SYS.4 Outcome 5:** "Consistency and bidirectional traceability are established
between verification measures and the elements of the system architecture." [src-aspice-4-0 §4.3.4 p.41]

**ASPICE SYS.4 Outcome 6:** "Bidirectional traceability between verification results and
verification measures is established." [src-aspice-4-0 §4.3.4 p.41]

No requirement without verification. No verification without a requirement. This is the
structural rule.

### 6.2 What Makes a Requirement Testable at the System Level

IEEE 1233-1998 defines testability as "the degree to which a requirement is stated in
terms that permit establishment of test criteria and performance of tests to determine
whether those criteria have been met." [web-search-testability-2026]

Four criteria for system-level testability:

1. **Quantified:** "Response time shall be ≤ 100 ms" is testable. "Response time shall
   be fast" is not. Every performance requirement needs a measurable threshold.

2. **Observable:** The behavior described can be observed at the system boundary without
   requiring access to internal implementation. Interface requirements and externally
   observable functional requirements meet this criterion; internal design requirements
   do not.

3. **Reproducible:** The test can be run repeatedly with consistent results. Requirements
   that depend on unpredictable external conditions may need to be expressed as
   conditional: "when condition X, the system shall respond with Y within Z ms."

4. **Distinguishable from pass/fail:** It must be possible to determine unambiguously
   whether the requirement has been met. Ambiguous requirements produce ambiguous test
   results.

ASPICE SYS.2.BP1 Note 2 states this as: "verifiability (i.e., verification criteria
being inherent in the requirements text)" is one of the defined characteristics required
of a system requirement. [src-aspice-4-0 §4.3.2 p.36]

### 6.3 Verification Methods at the System Level

The Peterson case study identifies four verification methods applicable at the system level,
consistent with ARP 4754A:

- **Inspection (engineering review):** Review of documents, code, or hardware. Used for
  requirements that can be verified by examination — configuration, constraint compliance.
- **Analysis (Modeling):** Mathematical or simulation analysis. Used for performance
  bounds, timing budgets, failure rate requirements, safety objectives.
- **Test (Demonstration):** Execution of the system with defined inputs and observation
  of outputs. Preferred method for functional requirements.
- **Service Experience (Similarity):** Leveraging evidence from a previously certificated
  system. Used when systems are reused or adapted with minimal change.

[src-peterson-arp4754a-2015 p.70 SDP100 §5.3.1]

The case study makes an important practical observation: "It is anticipated that the bulk
of the avionic systems requirements will be verified through test." [src-peterson-arp4754a-2015 p.70]

Test is the default. Analysis and inspection substitute for test only when test is
not feasible (e.g., catastrophic failure conditions that cannot be safely induced).

### 6.4 The Verification Matrix

The verification matrix is the artifact that tracks requirements-to-test traceability.
The Peterson case study provides a concrete example (Table 19, p.71): [src-peterson-arp4754a-2015 p.71 Table 19]

| Column | Purpose |
|---|---|
| Unique ID | Requirement identifier |
| Requirement Text | The requirement being verified |
| Safety (Y/N) | Whether the requirement is safety-related |
| FDAL | Development assurance level |
| Associated Function | Which functional area this belongs to |
| Verification Method (Inspect / Analysis / Test / Service) | One or more methods |
| Verification Procedure Reference | Document containing the test/analysis procedure |
| Verification Artifact Reference | Document containing the evidence |
| Pass/Fail (P/F) | Result |

The verification matrix must be completed before the verification campaign is considered
done. Rows with no method selected, no procedure, or no artifact reference indicate
verification gaps.

### 6.5 System Integration Test Derivation (ASPICE SYS.4)

ASPICE SYS.4.BP1 defines what system integration test cases must cover:

> "Specify the verification measures, based on a defined sequence and preconditions for
> the integration of system elements against the system static and dynamic aspects of
> the system architecture, including: techniques for the verification measures,
> pass/fail criteria for verification measures, a definition of entry and exit criteria
> for the verification measures, and the required verification infrastructure and
> environment setup." [src-aspice-4-0 §4.3.4 p.41]

The note elaborates: "the system integration test cases may focus on:
- the correct signal flow between system items,
- the timeliness and timing dependencies of signal flow between system items,
- the correct interpretation of signals by all system items using an interface, and/or
- the dynamic interaction between system items." [src-aspice-4-0 §4.3.4 p.41]

This distinguishes system integration test from system requirement test: integration
tests verify the architecture (element interactions), while functional tests verify
requirements (behavioral properties).

### 6.6 Safety Requirement Verification

Safety requirements require additional verification rigor beyond normal functional
requirements. ARP 4754A Objective 5.4: "Safety requirements are verified."
[src-peterson-arp4754a-2015 Table 6 p.45]

From the Peterson case study, safety requirement verification has two components:
- The avionic system development verification activities (functional tests)
- The safety assessment (SSA) confirming that safety requirements are met analytically

The SSA uses the verification test results as data inputs for quantitative failure
analysis, and also performs its own fault injection and failure mode analysis.
[src-peterson-arp4754a-2015 p.63 SDP100 §4 — safety process includes FMEA and SSA]

Safety requirements that cannot be verified by test (because they involve catastrophically
dangerous failure conditions) must be verified by analysis, with justification for why
test is not feasible.

---

## 7. Cross-Domain Structural Comparison

### 7.1 What Each Standard Calls These Activities

| Activity | ARP 4754A (Aviation) | ISO 26262 (Automotive) | ASPICE (Process Assessment) |
|---|---|---|---|
| Completeness of requirements | Objective 4.1: complete and correct | TSC completeness via HARA/FSC coverage | SYS.2 Outcome 1-3 |
| Allocation to SW/HW | Objective 2.6: System reqs to items | TSR allocation to HW, SW, combination | SYS.3 Outcome 1 + SYS.3.BP4 traceability |
| Derived requirements | Objective 2.4: defined with rationale | Derived TSRs from architecture | SYS.2-SYS.3 interface (implicit) |
| Interface requirements | Objective 2.3: system interfaces defined | HSI specification (formal document) | SYS.3.BP1: external interfaces |
| Operational modes | FHA mode classification | FSC: degradation concept, safe states, FTTI | SYS.3.BP2: dynamic aspects in modes |
| Requirements-to-test | Objective 5.1-5.4: verification complete | Item integration and testing (Clause 7) | SYS.4: verification measures + traceability |

### 7.2 The Common Structural Pattern

All three frameworks implement the same underlying logic:

```
Completeness check
    ↓
Allocation to elements (produces allocation table)
    ↓
Decomposition (produces derived requirements + rationale)
    ↓
Interface specification (produces ICD / HSI)
    ↓
Mode analysis (produces degraded mode requirements + safe state requirements)
    ↓
Testability review per requirement (produces verification method selection)
    ↓
Verification matrix (tracks requirement → test → result → pass/fail)
```

The standards diverge on formalism and explicitness, but every element of the chain is
present in each framework.

---

## 8. Practical Anti-Patterns

These failure modes are attested by the Peterson industry survey findings and the
standards' explicit gap-filling provisions:

### 8.1 Derived Requirements Not Justified
The most common omission: requirements that emerged from architecture or safety analysis
lack rationale. An assessor sees a requirement with no parent trace and no rationale
field — it cannot be determined whether it is a valid derived requirement or an error.
ARP 4754A explicitly requires rationale for derived requirements (Objective 2.4).
[src-peterson-arp4754a-2015 Table 6 p.44]

### 8.2 Allocation Without Independence Analysis
System functions are allocated to items without checking whether the independence
requirements emerging from safety analysis conflict with the proposed allocation. The
Peterson case study shows this explicitly: the PASA CMA analysis generates independence
requirements that directly constrain the allocation (maintenance function must be
split into Level A and Level D to maintain independence). Skipping CMA before finalizing
allocation produces architectures that cannot satisfy independence requirements.
[src-peterson-arp4754a-2015 pp.48-57]

### 8.3 Interface Requirements by Reference Only
Interface requirements that consist only of "the system shall conform to ICD-XXX" with
no summary of the obligation in the requirement text. These are difficult to allocate,
difficult to trace, and impossible to validate without reading the ICD. The requirement
text should state the critical obligation; the ICD is supplementary.
[synthesis — consistent with verifiability criterion from ASPICE SYS.2.BP1 Note 2]

### 8.4 Mode Requirements Limited to Normal Mode
Requirements are written only for normal operating conditions. Degraded behavior,
startup self-test failure, and shutdown sequence are left implicit. This guarantees
that mode-related safety properties cannot be verified, because the mode requirements
do not exist.

### 8.5 Verification Method Assigned Without Review
All requirements receive "Test" as verification method without reviewing whether each
requirement is actually testable by the method assigned. Some requirements (catastrophic
failure conditions, statistical failure rates) cannot be verified by direct test at the
system level and require analysis. Assigning test to these requirements and then failing
to run them is a certification risk.
[src-peterson-arp4754a-2015 p.70 SDP100 §5.3.1 — explicitly distinguishes test from analysis]

### 8.6 Traceability Exists but Consistency Not Checked
ASPICE SYS.2.BP5 Note 7 explicitly states: "Traceability alone does not necessarily
mean that the information is consistent with each other." A link between a system
requirement and a stakeholder requirement is not evidence that the system requirement
correctly implements the stakeholder intent. Consistency requires review, not just
link creation. [src-aspice-4-0 §4.3.2 p.37]

---

## 9. What This Research Covers vs. What's Missing

### Covered:
- [x] Completeness strategies (category coverage, model-based, formal vs. semantic)
- [x] The "no known gaps vs. provably complete" distinction
- [x] Requirements allocation (definition, ARP 4754A process, ISO 26262 criteria, ASPICE SYS.3)
- [x] Allocation criteria: SW vs. HW vs. operational
- [x] Requirements spanning SW+HW (strategies: decompose, integrate, shared assumption)
- [x] Requirements decomposition (parent-child, SEBoK functional analysis)
- [x] Derived requirements (definition, sources, feedback loop to safety assessment)
- [x] Derived requirements attributes (rationale, parent trace, safety attribute)
- [x] Interface requirements (five dimensions: protocol, data format, timing, error handling, init)
- [x] The HSI specification (ISO 26262 model) as the canonical interface boundary document
- [x] Interface requirements in ARP 4754A and ASPICE SYS.3
- [x] Operational modes taxonomy (6 modes: init, normal, degraded, emergency, maintenance, shutdown)
- [x] Mode-specific requirements, degraded mode requirements, safe state requirements
- [x] Mode requirements and safety analysis coupling (FHA/HARA drives mode requirements)
- [x] System-level testability criteria (quantified, observable, reproducible, distinguishable)
- [x] Verification methods at system level (inspection, analysis, test, service experience)
- [x] Verification matrix structure (from Peterson Table 19)
- [x] ASPICE SYS.4 integration test derivation (signal flow, timing, interface behavior)
- [x] Safety requirement verification (dual path: functional test + SSA)
- [x] Cross-domain comparison table
- [x] Anti-patterns (6 documented)

### NOT Covered (needed by other research docs or future work):
- [ ] INCOSE 42-rule completeness checklist detail (GtWR paywalled, REQI article partially read)
- [ ] Model-based requirements completeness (SysML requirements diagrams, MBSE coverage)
- [ ] Formal completeness tools (NuSMV, SPIN model checking for requirements)
- [ ] ARP 4754B (2024) updates — may revise derived requirements guidance [unverified]
- [ ] ISO 26262 FTTI calculation detail (timing constraint derivation)
- [ ] Interface requirements for multi-system architectures (System-of-Systems interfaces)
- [ ] Requirements completeness metrics beyond category coverage (quantitative NLP approaches)
- [ ] MIL-STD-961E requirements structure (Defense standard — not retrieved)
- [ ] NASA-STD-8739.8 requirements standard — not retrieved in this session

---

## Sources

### Primary sources (read from raw files in this session)

- **[src-aspice-4-0]** ASPICE PAM v4.0, VDA QMC WG13, 2023.
  `raw/standards/Automotive-SPICE-PAM-v40.pdf` pp. 34-42.
  SYS.1-SYS.4 complete base practices, outcomes, output information items — verbatim.
  Specifically: SYS.2.BP1 verifiability note, SYS.2.BP5 process requirements note,
  SYS.3.BP2 mode-specific dynamic aspects, SYS.3.BP4 non-functional requirements note,
  SYS.4.BP1 integration test focus areas.

- **[src-peterson-arp4754a-2015]** Peterson, Eric M. "Application of SAE ARP4754A to
  Flight Critical Systems." NASA/CR-2015-218982, November 2015.
  `raw/papers/peterson-arp4754a-nasa-2015.pdf` pp. 39-71.
  ARP4754A Objectives Mapping Table 6 (pp.44-46); ADP100 §4.1 requirements capture/validation;
  ADP100 §4.2 function verification; SDP100 §5.1 requirements development; SDP100 §5.2
  validation requirements; SDP100 §5.2.1 validation methods; SDP100 §5.3.1 verification
  methods; Table 18 validation matrix example (p.69); Table 19 verification matrix (p.71);
  PASA Section FDAL Assignment Table 7 (p.48); PASA CMA Tables 9-15 (pp.51-57).

### Web sources (fetched in this session)

- **[web-sebok-srd-2026]** SEBoK, "System Requirements Definition" article. Accessed 2026-04-12.
  Category coverage for completeness; allocation definition; budgeting; derived requirements;
  interface requirements three-step process; testability; cited standards: ISO/IEC/IEEE 29148:2018,
  INCOSE NRM 2022, INCOSE GtWR 2023. URL: https://sebokwiki.org/wiki/System_Requirements_Definition

- **[web-btc-req-types-2026]** BTC Embedded Systems AG, "ISO 26262 Functional Safety
  Requirement Types." Accessed 2026-04-12. Four-level hierarchy: Safety Goals, FSR, TSR,
  SW Safety Requirements. Allocation of TSRs to HW/SW/combination. ASIL assignment.
  URL: https://www.btc-embedded.com/iso-26262-requirement-types/

- **[web-hal-hsi-2015]** "Using Model-based Development for ISO 26262 aligned HSI
  Definition." HAL Open Science archive. Accessed 2026-04-12.
  HSI content requirements; HSI as boundary document and starting point for parallel
  HW/SW development; HSI requires mutual domain knowledge; iterative refinement.
  URL: https://hal.science/hal-01193034/document

- **[web-search-completeness-2026]** Web search synthesis: IEEE 1233-1998 testability
  definition; requirements completeness fundamental problem; formal completeness (TCPF/DCPF)
  vs. semantic completeness (MSEC); interface-to-functional ratio heuristic.
  Sources: IEEE RS Newsletter (Kasper & Laplante 2012); numberanalytics.com.

- **[web-search-testability-2026]** Web search synthesis: IEEE 1233-1998 testability
  definition; verification method categories (analysis, demonstration, inspection, modeling,
  testing). Source: letter27-se.com requirements and verification levels article.

- **[web-search-operational-modes-2026]** Web search synthesis: graceful degradation
  definition; safe state definition; startup/shutdown requirements for safety-critical
  systems. Sources: risknowlogy.com; elektrobit.com; iso26262.academy.
