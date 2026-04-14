# Research 1: Standards — System-Level Processes

Research for upper V documentation (backlog items 3.4, 3.5, 3.6). Extracts what ARP 4754A,
ARP 4761, ISO 26262 Parts 3-4, and ASPICE SYS.1-SYS.3 define as the system-level
development process — the compliance frame above the software level already documented
in the engineering codex.

**Sources used:**
- ASPICE PAM v4.0 (primary, read from PDF pp. 34-42) [src-aspice-4-0]
- NASA/CR-2015-218982, Peterson 2015 (primary, read from PDF pp. 1-20) [src-peterson-arp4754a-2015]
- Secondary web sources for ARP 4761 and ISO 26262 Parts 3-4 (see source list at end)

---

## 1. The Standards Hierarchy

Before diving into each standard, here's how they relate to each other — because this is
the single most confusing thing for someone entering this domain:

```
AVIATION                                    AUTOMOTIVE
─────────                                   ──────────

14 CFR 25.1309 (regulation)                 ISO 26262 (all-in-one standard)
        │                                       │
   AC 25.1309 (guidance)                   Part 3: Concept Phase
        │                                   Part 4: System Level
   ARP 4754A ←──→ ARP 4761                 Part 5: HW Level
   (system dev)    (safety assessment)      Part 6: SW Level
        │                                   Part 7: Production
   ┌────┴────┐                              Part 8-12: Supporting
DO-178C    DO-254
(SW)       (HW)                             ASPICE (process assessment)
                                            SYS.1-SYS.5 + SWE.1-SWE.6
```

**Key structural difference:** Aviation separates system development (ARP 4754A), safety
assessment (ARP 4761), software (DO-178C), and hardware (DO-254) into independent
documents. ISO 26262 bundles everything into one standard with parts. ASPICE is
orthogonal — it assesses process maturity regardless of safety standard.

---

## 2. ARP 4754A — System Development Process (Aviation)

### 2.1 Scope and Purpose

ARP 4754A (SAE, December 2010; EUROCAE ED-79A) provides "guidelines for the generation
of evidence to substantiate with adequate confidence (i.e., assurance level) that errors in
requirements, design, and implementation of the system have been identified and corrected,
and that the system satisfies applicable certification regulations."
[src-peterson-arp4754a-2015 §1 p.1]

Recognized by FAA via AC 20-174 (September 2011) as acceptable means of compliance.

It sits ABOVE DO-178C and DO-254 — it defines aircraft functions, system architecture,
assigns Development Assurance Levels, and flows requirements and DAL assignments down
to the item level where DO-178C/DO-254 take over.
[src-peterson-arp4754a-2015 §4 p.4]

### 2.2 Five Development Processes

ARP 4754A Section 5 defines five development processes:

1. **Aircraft Function Development** — Iterative process assigning top-level functions
   (flight control, engine control, navigation, braking, etc.) to systems. Captures
   aircraft-level requirements and functional interfaces.

2. **System Architecture Development** — Establishes system structure and boundaries,
   iteratively considering FHA, PASA, PSSA, and CCA. Defines how components interact
   to meet functional and safety goals.

3. **Allocation of System Requirements to Items** — Assigns hardware and software IDALs
   and flows requirements to DO-254 and DO-178C teams.

4. **System Implementation** — Flows information from system process to HW/SW
   development processes with traceability.

5. **System Integration and Verification** — Performs item, system, and aircraft
   integrations. Verification demonstrates intended function and confidence of no
   unintended safety impacts.

[src-peterson-arp4754a-2015 §4 p.4, Table 6 pp.44-46]

### 2.3 Seven Integral Processes

These run continuously across all five development processes:

1. Safety Assessment (links to ARP 4761)
2. Development Assurance Level Assignment (FDAL/IDAL)
3. Requirements Capture
4. Requirements Validation
5. Configuration Management
6. Process Assurance
7. Certification and Regulatory Authority Coordination

### 2.4 FDAL and IDAL — Two Levels of Assurance

ARP 4754A introduced a critical distinction:

- **FDAL (Functional DAL)** — applies to aircraft/system *functions*. Assigned based on
  failure condition severity from the FHA. Determined using ARP 4754A Table 2 or Table 3.

- **IDAL (Item DAL)** — applies to hardware/software *items* (what DO-178C/DO-254 see).
  Assigned commensurate with the FDAL and the hazard supported by the item. Can
  potentially be reduced below FDAL through architectural mitigation (functional
  independence), verified via Common Mode Analysis (CMA).

| Failure Condition Severity | FDAL |
|---|---|
| Catastrophic | A |
| Hazardous | B |
| Major | C |
| Minor | D |
| No Safety Effect | E |

For catastrophic failure conditions: FDAL A required for at least one member of the
functional failure set. Additional members assigned at the level associated with their
most severe individual effects (but no lower than level C).
[src-peterson-arp4754a-2015 §4 p.4, Table 7 p.48]

### 2.5 Requirements Capture and Validation

**Requirements capture** relies heavily on engineering judgment. The standard emphasizes
that "the generation of acceptable, clear, concise requirement text relies on experience
and engineering judgment." [src-peterson-arp4754a-2015 §4 p.4]

**Requirements validation** is explicitly called out as a problematic practice area:
- The ARP implies a minimum of two validation methods are recommended
- Most engineers have experience defining and verifying requirements but NOT justifying
  (validating) them
- Viewed as "new and unfulfilling work" that puts additional demands on scarce
  experienced personnel

[src-peterson-arp4754a-2015 §5 p.7]

### 2.6 Validation vs Verification

| | Validation | Verification |
|---|---|---|
| Question | "Are these the right requirements?" | "Does the implementation satisfy the requirements?" |
| Methods | Traceability, analysis, test, modeling, inspection | Inspection, analysis, test (demonstration) |
| Timing | During/after requirements capture | During/after implementation |
| Who | Experienced engineers (judgment-heavy) | Test engineers (evidence-heavy) |

Validation Matrix and Verification Matrix are key traceability artifacts.
[src-peterson-arp4754a-2015 Tables 18-19 pp.69-71]

### 2.7 Traceability Obligations

Bidirectional traceability required across the full hierarchy:

```
Aircraft-level functions/requirements
    ↕
System requirements (allocated from aircraft functions)
    ↕
Item requirements (allocated from system req to HW/SW)
    ↕
DO-178C/DO-254 implementation and verification
```

**Critical feedback loop:** When DO-178C or DO-254 processes create *derived requirements*
(not traceable to higher-level requirements), these MUST be fed back up to ARP 4754A
(system) and ARP 4761 (safety) for impact assessment.
[src-peterson-arp4754a-2015 Table 6 objectives 2.1-2.7, 4.4, 5.5]

### 2.8 Industry Practice Issues

From the NASA study's industry questionnaire and roundtable (Appendix B):

1. **Inconsistent interpretation:** Primary industry concern is certification authorities'
   inconsistent understanding of ARP 4754A, both within a single authority and between
   different authorities worldwide. [src-peterson-arp4754a-2015 §5 p.6]

2. **Steep learning curve:** For those not legacy ARP4754-literate. General industry
   interpretation is that the ARP increases documentation efforts. [src-peterson-arp4754a-2015 §5 p.7]

3. **FDAL/IDAL confusion:** All questionnaire respondents indicated difficulty in applying
   the assurance level assignment process. Problems differentiating between failure
   mitigation and error mitigation techniques. Only 25% had received training.
   [src-peterson-arp4754a-2015 §5 p.6]

4. **"How-to" gap:** Respondents want step-by-step guidance for derived requirement
   review, process assurance, and requirement standards for capture/validation.
   [src-peterson-arp4754a-2015 §5 pp.6-7]

5. **Expertise matters:** "It's not just about what is being done but who does it as well.
   Expertise (skills and experience) matters." [src-peterson-arp4754a-2015 §5 p.7]

---

## 3. ARP 4761 — Safety Assessment Process (Aviation)

### 3.1 Scope and Relationship

ARP 4761 (SAE, 1996; Revision A released December 2023) defines the safety assessment
process for civil aircraft systems. It is a companion document to ARP 4754A — ARP 4754A
manages development, ARP 4761 manages safety assessment. Together they demonstrate
compliance with 14 CFR 25.1309.

The standard is approximately 330 pages: ~30 on process, ~140 on modeling techniques,
~160 on examples. [Wikipedia ARP4761]

### 3.2 Three Core Safety Assessment Activities

| Activity | Direction | Timing | Purpose |
|---|---|---|---|
| **FHA** (Functional Hazard Assessment) | Top-down | Requirements phase | Identify failure conditions, classify severity |
| **PSSA** (Preliminary System Safety Assessment) | Top-down | Architecture/design | Derive safety requirements from proposed architecture |
| **SSA** (System Safety Assessment) | Bottom-up | Implementation/verification | Verify implementation meets safety requirements |

ARP 4761A (2023) adds two aircraft-level processes:
- **PASA** (Preliminary Aircraft Safety Assessment) — examines aircraft architecture
  against aircraft-level safety objectives
- **ASA** (Aircraft Safety Assessment) — aircraft-level verification counterpart to SSA

### 3.3 Functional Hazard Assessment (FHA)

**Two levels:**
- **Aircraft FHA (AFHA)** — identifies aircraft-level functional failures
- **System FHA (SFHA)** — decomposes to system-level; traceability between system and
  aircraft failure conditions must be established

**Process:**
1. Identify all functions at the level under study
2. Identify and describe failure conditions (single and multiple failures, normal and
   degraded environments)
3. Classify each failure condition by severity
4. Assign DAL based on severity

**FHA output format (spreadsheet columns):**
- Function
- Failure condition description
- Phase of flight
- Effect on aircraft/crew/passengers
- Hazard classification (severity)
- Development Assurance Level
- Means of detection
- Aircrew response
- Safety requirements (qualitative)

**Severity-to-DAL-to-probability mapping:**

| Severity | DAL | Probability Term | Max Probability/FH |
|---|---|---|---|
| Catastrophic | A | Extremely Improbable | 10⁻⁹ |
| Hazardous | B | Extremely Remote | 10⁻⁷ |
| Major | C | Remote | 10⁻⁵ |
| Minor | D | Probable | 10⁻³ |
| No Safety Effect | E | — | — |

**Core principle:** "The more severe the hazard, the less likely that failure must be."
(AC 25.1309)

[Wikipedia ARP4761; Wikipedia AC 25.1309-1; Medium - Akbulut]

### 3.4 Preliminary System Safety Assessment (PSSA)

**Purpose:** Systematic examination of a proposed system architecture to determine how
failures can lead to FHA-identified hazards and how FHA requirements can be met.

**Key mechanism — fault tree decomposition:**
1. Build qualitative fault trees with FHA failure conditions as top events
2. Decompose through system architecture to identify contributing failures
3. Allocate failure rate budgets to subsystems
4. Identify single points of failure and failure propagation pathways
5. Determine where architectural safety barriers are needed (redundancy, independence,
   monitoring)
6. Derive lower-level safety requirements from the fault tree
7. Initiate Common Cause Analysis (CCA)

**This is where safety requirements are born.** The fault tree structure directly shows what
failure rate budget each subsystem must meet. Requirements like "functions shall be
distributed across independent processors with separate power sources" are derived here.

**Outputs:**
- Updated FHAs and FTAs (qualitative)
- Safety requirements allocated to subsystems
- Preliminary Common Cause Analyses
- Identification of items requiring redundancy

[Wikipedia ARP4761; MIT STPA comparison paper (blocked); Medium - Akbulut]

### 3.5 System Safety Assessment (SSA)

**Purpose:** Verify the implemented system meets qualitative AND quantitative safety
requirements from FHA and PSSA.

**Method:**
- Takes PSSA fault trees, populates with quantitative failure data
- Uses FMEA (bottom-up) to obtain component-level failure rates
- Combines FTA structure (top-down) with FMEA data (bottom-up) to calculate
  system-level failure probabilities
- Uses real flight data, lab tests, fault injection, model-based simulations

**Outputs:** Quantitative safety analysis showing all failure conditions meet probability
requirements; residual risk summary; safety case evidence for certification.

### 3.6 Safety Analysis Methods Prescribed

| Method | Direction | Purpose |
|---|---|---|
| **FTA** (Fault Tree Analysis) | Top-down (deductive) | Primary method for deriving safety requirements and probability budgets |
| **DD** (Dependence Diagrams) | Top-down | Alternative representation to FTA (analyst preference) |
| **MA** (Markov Analysis) | — | Complex redundancy, sequence-dependent failures, deferred maintenance |
| **FMEA** (Failure Modes and Effects Analysis) | Bottom-up (inductive) | Component failure rates for quantitative FTA |

**Common Cause Analysis (CCA) — three sub-analyses:**

1. **Zonal Safety Analysis (ZSA)** — physical zone safety of system installations
2. **Particular Risks Analysis (PRA)** — external events (fire, bird strike, HIRF, lightning)
3. **Common Mode Analysis (CMA)** — validates assumed independence of redundant elements;
   always includes software and manufacturing errors

[Wikipedia ARP4761; ALD Service]

### 3.7 Safety Requirements Flow into System Requirements

The flow is iterative and bidirectional:

```
ARP 4761 FHA
    │  (failure conditions + severity + DAL)
    ↓
ARP 4754A Aircraft Requirements
    │  (functions allocated to systems)
    ↓
ARP 4761 System FHA + PSSA
    │  (safety requirements: failure rate budgets, independence, redundancy, monitoring)
    ↓
ARP 4754A System Requirements
    │  (allocated to items)
    ↓
DO-178C (software) / DO-254 (hardware)
    │  (derived requirements fed back UP)
    ↓
ARP 4754A + ARP 4761 (check no adverse safety impact)
```

---

## 4. ISO 26262 Parts 3-4 — System-Level Development (Automotive)

### 4.1 Part 3: Concept Phase

#### Item Definition (Clause 5)

The starting point. Defines WHAT the item does at vehicle level, implementation-independent.

**Contents:**
- Functional description of the item
- Functional cascade and boundary diagram
- Operational and environmental constraints
- Interactions with other items and elements
- Operating scenarios impacting functionality
- Preliminary architecture
- Known hazards from similar items

An "item" is a system or group of systems implementing a function at vehicle level
(e.g., ABS, electric power steering, battery management).

[Embitel HARA guide; SecuRESafe ISO 26262 Ed.3]

#### HARA — Hazard Analysis and Risk Assessment (Clause 6)

**Process:**
1. Identify vehicle-level hazardous events caused by malfunctioning behaviour
2. Classify three risk parameters per hazardous event:
   - **Severity (S0-S3):** S0 = no injuries → S3 = fatal/life-threatening
   - **Exposure (E0-E4):** E0 = incredible → E4 = high probability
   - **Controllability (C0-C3):** C0 = controllable → C3 = uncontrollable
3. Combine S × E × C to determine ASIL using lookup table

**ASIL determination:** S0, E0, or C0 → QM (no safety requirement).
S3 + E4 + C3 → ASIL D (maximum).

**Key constraint vs. aviation:** HARA considers malfunctioning behaviour only, not nominal
but unsafe interactions (a known limitation vs. STPA/STAMP approaches — see codex
`std-iso26262` Critiques section).

#### Safety Goals (from HARA)

Top-level safety requirements, each with an ASIL, derived directly from HARA.
- One safety goal per hazardous event (or shared)
- Expressed at vehicle/functional level, not implementation level
- Must state what must be prevented/achieved, not how

**Example:** "The battery protection function shall avoid a battery fire in charging and
operating modes" (ASIL D)

[Embitel HARA guide; BYHON FSC article]

#### Functional Safety Concept (Clause 7)

Derives functional safety requirements (FSRs) from safety goals and allocates them to
elements of a preliminary architecture.

**FSC contents:**
- At least one FSR per safety goal
- Allocation of FSRs to architectural elements
- Warning and degradation concepts
- Safe state definition
- Fault Tolerant Time Interval (FTTI) — minimum time from fault to potential hazard
- Operating modes relevant to safety

**FSR types:**
- Fault detection and indication
- Transitioning to/maintaining safe states
- Fault tolerance through redundancy/degradation
- Driver warning requirements
- Arbitration between multiple safety goals

**Key distinction:** FSRs are implementation-independent — they describe WHAT safety
behaviour is needed, not HOW.

[BYHON FSC article; EmbeddedInEmbedded FSC; BTC Embedded req types]

### 4.2 Part 4: Product Development at the System Level

#### Technical Safety Concept (Clause 6)

**Key difference from FSC:**
- FSC = WHAT safety functions are needed (implementation-independent)
- TSC = HOW those functions will be technically realized (allocated to HW/SW)

**TSC contents:**
- Technical Safety Requirements (TSRs) derived from FSRs
- System architectural design with all safety-related elements
- Allocation of each TSR to HW, SW, or combination
- Safety mechanisms and their operating characteristics
- Diagnostic architecture (what, how, when, coverage)
- Safe state management strategy (mode transitions)
- Timing analysis (safety mechanisms within FTTI budgets)
- Hardware-Software Interface (HSI) specification
- Target values for hardware architectural metrics (SPFM, LFM)

[PIEmbSysTech Part 4 guide; SecuRESafe Ed.3]

#### Allocation to SW (Part 6) and HW (Part 5)

1. System architecture partitions item into HW and SW elements
2. Each TSR allocated to one or more elements
3. Each element's ASIL = highest ASIL of any TSR allocated to it
4. HSI specification defines the boundary

**HSI Specification includes:**
- Hardware parts controlled by software
- Hardware resources supporting SW execution (memory, bus, I/O)
- Shared resources and arbitration
- Operating constraints imposed by HW on SW (timing, sequencing)

**ASIL Decomposition (Part 9):** High ASIL can be distributed across redundant,
independent elements. E.g., ASIL D = ASIL B(D) + ASIL B(D). Independence between
elements is mandatory for valid decomposition.

#### System Integration and Testing (Clauses 7-8)

**Item Integration and Testing (Clause 7):**
- Verifies correct implementation of TSRs at system level
- Methods: requirements-based testing, fault injection, back-to-back testing
- Environments: MIL, SIL, HIL
- Test cases derived from requirements, not implementation

**Safety Validation (Clause 8):**
- Performed at vehicle level
- Confirms safety goals are correct, complete, and fully achieved
- Validates integrated item in representative vehicle(s)
- Confirms external measures (driver warnings) are effective

**V-model correspondence:**
- Unit test ← detailed design (Part 6)
- SW integration test ← SW architecture (Part 6)
- System integration test ← system architecture (Part 4)
- Safety validation ← safety goals (Part 3)

[OpenECU integration testing; Parasoft traceability]

### 4.3 Traceability Obligations

Bidirectional traceability through entire chain:

```
Hazardous Event → Safety Goal → FSR → TSR → HW/SW Req → Implementation → Verification Result
```

- Every safety goal traces to hazardous events (backward) and to FSRs (forward)
- Every FSR traces to a safety goal (backward) and to TSRs (forward)
- Every TSR traces to FSRs (backward) and to HW/SW implementation (forward)
- Every verification activity traces to the requirement it verifies
- No requirement without verification, no verification without requirement

ASIL D requires full bidirectional traceability with coverage analysis and impact
analysis capability for any change.

[Parasoft traceability; Electronic Design traceability]

---

## 5. ASPICE SYS.1-SYS.3 — System Engineering Processes (Automotive Process Assessment)

All content below is from the ASPICE PAM v4.0 primary source [src-aspice-4-0 pp.34-39].

### 5.1 SYS.1 — Requirements Elicitation

**Purpose:** Gather, analyze, and track evolving stakeholder needs and requirements
throughout the lifecycle to establish a set of agreed requirements.

**Process outcomes:**
1. Continuing communication with the stakeholder is established
2. Stakeholder expectations are understood, requirements are defined and agreed
3. Stakeholder requirements changes are analyzed for risk assessment and impact
4. Determination of stakeholder requirements status is ensured for all affected parties

**Base practices (4 BPs):**

| BP | Name | Description |
|---|---|---|
| BP1 | Obtain stakeholder expectations and requests | Through direct solicitation, review of business proposals, consideration of target operating/hardware environment, and other documents. *Note: Documenting the stakeholder or source of a requirement supports agreement and change analysis.* |
| BP2 | Agree on requirements | Formalize expectations into requirements. Reach common understanding. Obtain explicit agreement from all affected parties (customers, suppliers, design partners, outsourcing). *May be based on feasibility studies and/or cost and schedule impact analysis.* |
| BP3 | Analyze stakeholder requirements changes | Analyze all changes against the baseline. Assess impact and risks. Initiate appropriate change control and mitigation actions. *Changes may arise from changing technology, stakeholder needs, or legal constraints.* |
| BP4 | Communicate requirements status | Ensure all affected parties can be aware of status and disposition including changes. Communicate necessary information and data. |

**Output information items:**
- 15-51 Analysis Results (→ Outcome 3)
- 13-52 Communication Evidence (→ Outcomes 1, 2)
- 17-00 Requirement (→ Outcome 2)
- 17-54 Requirement Attribute (→ Outcomes 2, 3, 4)

### 5.2 SYS.2 — System Requirements Analysis

**Purpose:** Establish a structured and analyzed set of system requirements consistent with
the stakeholder requirements.

**Process outcomes:**
1. System requirements are specified
2. System requirements are structured and prioritized
3. System requirements are analyzed for correctness and technical feasibility
4. The impact of system requirements on the operating environment is analyzed
5. Consistency and bidirectional traceability established between system and stakeholder reqs
6. System requirements are agreed and communicated to all affected parties

**Base practices (6 BPs):**

| BP | Name | Description |
|---|---|---|
| BP1 | Specify system requirements | Use stakeholder requirements to identify required functions and capabilities. Specify functional and non-functional system requirements according to **defined characteristics** (per ISO IEEE 29148, ISO 26262-8:2018, or INCOSE GtWR). *Examples: verifiability, verification criteria being inherent in the text, unambiguity/comprehensibility, freedom from design and implementation, not contradicting any other requirement.* |
| BP2 | Structure system requirements | Structure and prioritize. *Examples: grouping by functionality or product variants. Prioritization via release scopes per SPL.2.BP1.* |
| BP3 | Analyze system requirements | Analyze including interdependencies to ensure correctness, technical feasibility, and to support project management regarding estimates. *Technical feasibility can be evaluated based on platform/product line, or by means of prototype development or product demonstrators.* |
| BP4 | Analyze the impact on the system context | Analyze the impact that system requirements will have on elements in the relevant system context. |
| BP5 | Ensure consistency and establish bidirectional traceability | Between system requirements and stakeholder requirements. *Traceability supports consistency, facilitates impact analysis, and supports demonstration of coverage. Traceability alone does not necessarily mean the information is consistent with each other. There may be non-functional stakeholder requirements that system requirements do not trace to — these are process requirements, still subject to verification.* |
| BP6 | Communicate agreed system requirements and impact on the system context | To all affected parties. |

**Output information items:**
- 17-00 Requirement (→ Outcomes 1, 2)
- 17-54 Requirement Attribute (→ Outcomes 2, 3)
- 15-51 Analysis Results (→ Outcomes 3, 4)
- 13-51 Consistency Evidence (→ Outcome 5)
- 13-52 Communication Evidence (→ Outcome 6)

### 5.3 SYS.3 — System Architectural Design

**Purpose:** Establish an analyzed system architecture, comprising static and dynamic
aspects, consistent with the system requirements.

**Process outcomes:**
1. System architecture is designed including definition of system elements with their
   behavior, interfaces, relationships, and interactions
2. System architecture is analyzed against defined criteria, and special characteristics
   are identified
3. Consistency and bidirectional traceability established between system architecture
   and system requirements
4. Agreed system architecture and special characteristics communicated to all affected parties

**Base practices (5 BPs):**

| BP | Name | Description |
|---|---|---|
| BP1 | Specify static aspects of system architecture | Specify and document static aspects with respect to functional and non-functional system requirements, including external interfaces and a defined set of system elements with their interfaces and relationships. |
| BP2 | Specify dynamic aspects of system architecture | Specify and document dynamic aspects with respect to functional and non-functional system requirements including the behavior of system elements and their interaction in different system modes. *Examples: timing diagrams reflecting inertia of mechanical components, processing times of ECUs, signal propagation times of bus systems.* |
| BP3 | Analyze system architecture | Analyze regarding relevant technical design aspects related to the product lifecycle, and to support project management regarding estimates. Derive special characteristics for non-software system elements. Document rationale for architectural design decisions. *Examples of lifecycle phases: production, maintenance & repair, decommissioning. Examples of technical aspects: manufacturability, suitability of elements for reuse, availability. Methods: prototypes, simulations, qualitative analyses (e.g., FMEA). Design rationale examples: proven-in-use, product platform/product line, make-or-buy, set-based design.* |
| BP4 | Ensure consistency and establish bidirectional traceability | Between architecture elements and system requirements that represent properties or characteristics of the physical end product. *Traceability alone does not necessarily mean consistency. Non-functional requirements that the architecture does not address or represent (direct properties/characteristics of the physical end product) do not trace to architecture — they are still subject to verification.* |
| BP5 | Communicate agreed system architecture | Including special characteristics, to all affected parties. |

**Output information items:**
- 04-06 System Architecture (→ Outcome 1)
- 13-51 Consistency Evidence (→ Outcome 3)
- 13-52 Communication Evidence (→ Outcome 4)
- 15-51 Analysis Results (→ Outcome 2)
- 17-57 Special Characteristics (→ Outcome 2)

### 5.4 Common Assessment Findings

What assessors look for across SYS.1-SYS.3 (from assessor training materials and blogs):

1. **Traceability gaps** — Most common finding. Missing links between levels. Assessors
   check both directions.

2. **Requirements without verification criteria** — In v4.0, verification criteria are
   integral to requirements ("defined characteristics"). Unverifiable = not a valid req.

3. **Missing IDs** — Requirements without unique, stable identifiers.

4. **Architecture not justified** — No rationale for design decisions (SYS.3.BP3).

5. **Inconsistency between levels** — System requirements that cannot be derived from
   stakeholder requirements, or architecture elements with no corresponding requirement.

6. **Missing interface definitions** — Architecture exists but interfaces between elements
   are undocumented.

7. **No change impact analysis** — Changes without documented impact assessment on
   downstream artifacts.

8. **"Check-the-box" documentation** — Documents exist but don't reflect actual
   development. Assessors sample and cross-check.

---

## 6. Cross-Domain Comparison

### 6.1 Conceptual Mapping

| ISO 26262 (Automotive) | ARP 4754A/4761 (Aviation) | ASPICE | Generic V-Model Term |
|---|---|---|---|
| Item Definition | System/Function Definition | SYS.1 (elicitation) | Stakeholder Needs |
| HARA | FHA | — | Hazard Analysis |
| ASIL (A-D) | DAL (A-E) | — | Safety Integrity Level |
| Safety Goals | Safety Objectives / Failure Conditions | — | Top-level Safety Requirements |
| Functional Safety Concept | PSSA (derives safety reqs) | — | Functional Safety Requirements |
| Technical Safety Concept | Detailed system design + safety allocation | SYS.2 + SYS.3 | System Requirements + Architecture |
| HSI Specification | Item requirements allocation | SWE.1/HWE.1 interface | SW/HW Allocation |
| Safety Validation | SSA + ASA | SYS.5 | System Verification |
| ASIL Decomposition | DAL allocation via ARP 4754A IDAL | — | Assurance Level Allocation |

### 6.2 Key Structural Differences

1. **Hazard classification:** ISO 26262 uses 3-axis (S×E×C) → ASIL. ARP 4761 uses
   probability-based categories with quantitative targets (10⁻⁹/hr for catastrophic).

2. **Process model:** ISO 26262 prescribes product requirements ("you must produce X").
   ARP 4754A/4761 prescribes an assessment process ("you must demonstrate X").
   ASPICE defines process capability ("your process must achieve X outcomes").

3. **Regulatory model:** Aviation requires government certification (FAA/EASA).
   Automotive is contractual (OEM requires supplier ASPICE assessment + ISO 26262
   compliance). No government approval of individual products.

4. **Scope packaging:** ARP 4754A + ARP 4761 + DO-178C + DO-254 = four separate
   documents. ISO 26262 = one standard with parts. ASPICE = orthogonal overlay.

5. **Completeness:** The two concepts that ISO 26262 has which are most distinctive:
   - **FTTI** (Fault Tolerant Time Interval) — explicit timing constraint for safety mechanisms
   - **HSI specification** — explicit interface contract between HW and SW

6. **Safety analysis integration:** In aviation, safety assessment (ARP 4761) is a
   separate parallel process with explicit handoff points. In ISO 26262, HARA/safety
   analysis is embedded within the concept phase (Part 3).

### 6.3 The Complete Flow (Generic)

Despite the structural differences, all standards implement the same fundamental cascade:

```
Stakeholder Needs / Operational Context
    │
    ↓  (elicitation, analysis)
System-Level Requirements
    │                    ↗ Safety Analysis (FHA/HARA)
    ↓  (+ safety reqs) ←  produces safety requirements + integrity levels
System Architecture
    │  (allocation: SW, HW, mechanical, operational)
    ↓
SW Requirements ──→ SW Architecture ──→ Detailed Design ──→ Code
HW Requirements ──→ HW Design ──→ HW Implementation
    │
    ↓  (derived requirements fed BACK UP for safety impact)
```

**The universal pattern across all three standards:**
- Top-down decomposition with safety analysis running in parallel
- Bidirectional traceability at every level boundary
- Derived requirements must flow up for impact assessment
- Each level adds detail; each level has independent verification
- Safety integrity level propagates down and constrains rigor

---

## 7. What This Research Covers vs. What's Missing

### Covered (sufficient for documentation §2 — V-model context):
- [x] Which standards govern system-level development
- [x] What processes each standard defines
- [x] What artifacts are required
- [x] What traceability obligations exist
- [x] How safety analysis feeds into system requirements
- [x] FDAL/IDAL distinction (aviation) and ASIL assignment (automotive)
- [x] Cross-domain conceptual mapping
- [x] ASPICE SYS.1-SYS.3 base practices (verbatim from PAM)
- [x] Industry practice issues (from NASA study)

### NOT covered (needed by other research docs):
- [ ] The *craft* of writing good system requirements (→ Research 3)
- [ ] Stakeholder analysis and needs capture techniques (→ Research 2)
- [ ] Safety analysis methods in depth (FMEA, FTA, STPA) (→ Research 4)
- [ ] System/SW architecture design craft (→ Research 5)
- [ ] AI role at system level (→ Research 6)
- [ ] ARP 4754A Appendix A objectives table verbatim (paywalled)
- [ ] ARP 4754A Tables 2 and 3 (FDAL/IDAL assignment, paywalled)
- [ ] ISO 26262 exact ASIL determination table (paywalled)
- [ ] SPFM/LFM target values per ASIL (paywalled)
- [ ] ARP 4754B/4761A detailed delta analysis

---

## Sources

### Primary sources (read from raw files in this session)

- **[src-aspice-4-0]** ASPICE PAM v4.0, VDA QMC WG13, 2023.
  `raw/standards/Automotive-SPICE-PAM-v40.pdf` pp. 34-42.
  SYS.1-SYS.3 base practices, outcomes, output information items — verbatim.

- **[src-peterson-arp4754a-2015]** Peterson, Eric M. "Application of SAE ARP4754A to
  Flight Critical Systems." NASA/CR-2015-218982, November 2015. 217 pages.
  `raw/papers/peterson-arp4754a-nasa-2015.pdf` pp. 1-8, ToC.
  ARP 4754A process structure, FDAL/IDAL, objectives mapping, industry practice issues.

### Secondary sources (web-fetched by research agents)

- **Wikipedia ARP4761** — https://en.wikipedia.org/wiki/ARP4761
  FHA/PSSA/SSA process, safety analysis methods, ARP 4761A additions.

- **Wikipedia ARP4754** — https://en.wikipedia.org/wiki/ARP4754
  FDAL/IDAL distinction, relationship to DO-178C.

- **Wikipedia AC 25.1309-1** — https://en.wikipedia.org/wiki/AC_25.1309-1
  Severity-probability-DAL mapping.

- **Medium (Umut Akbulut)** — ARP 4761 practitioner summary.
  FHA outputs, PSSA mechanism, SSA verification.

- **Embitel** — https://www.embitel.com/blog/embedded-blog/hara-by-iso-26262-standard
  HARA process, S/E/C parameters, ASIL determination.

- **PIEmbSysTech** — ISO 26262 Part 4 system-level development guide.
  TSC content, HSI, architecture guidance.

- **SecuRESafe** — ISO 26262 Edition 3 Parts 3-4 changes.
  Structural reorganization in upcoming edition.

- **BYHON** — ISO 26262 Functional Safety Concept.
  FSC vs TSC distinction, FTTI.

- **Parasoft** — ISO 26262 requirements traceability.
  Bidirectional traceability chain.

- **Expleo ASPICE 4.0 Process Guide Booklet** — detailed assessor guide.
  ASPICE v4.0 process descriptions.

- **Kugler Maag/UL SPICE Booklet 2024** — ASPICE assessor firm guide.
  Assessment practices, common findings.
