# Research 4b: Safety Requirements Derivation

Research for upper V documentation (backlog items 3.4, 3.5, 3.6). Covers how safety analysis
outputs become concrete, verifiable requirements. Research 1 covers the process structure.
Research 4a covers the analytical methods. This document covers the TRANSFORMATION from
safety analysis outputs to requirements — the interface between safety engineering and
requirements engineering.

**Sources used:**
- Peterson, NASA/CR-2015-218982, 2015 (primary, pp. 44-57 PASA/CMA, pp. 89-96
  validation/verification matrices) [src-peterson-arp4754a-2015]
- STPA Handbook, Leveson & Thomas, 2018 (primary, Ch. 3 pp. 54-71)
  [src-leveson-stpa-handbook-2018]
- MIL-STD-882E, 2012 (primary, §4.3 pp. 9-17, Task 203 pp. 49-50)
  [src-mil-std-882e-2012]
- ASPICE PAM v4.0 (primary, SYS.2-SYS.3) [src-aspice-4-0]
- FTTI article, nvdungx.github.io (secondary, fetched 2026-04-12)
  [src-ftti-nvdungx-2026]
- Heicon ASIL Decomposition article (secondary, fetched 2026-04-12)
  [src-heicon-asil-decomposition-2026]
- Research 1: Standards — System-Level Processes (internal)
- Research 4a: Safety Analysis Methods (internal)

---

## 1. The Central Question

Safety analysis methods (FTA, FMEA, STPA) produce analytical outputs — fault trees,
failure mode tables, unsafe control actions, loss scenarios. The system requirements
document needs verifiable requirement statements. The transformation between these
two forms is where safety engineering meets requirements engineering, and it is where
many programs fail.

The failure modes are predictable:
- Safety analysis produces vague "safety requirements" that cannot be verified
- Safety requirements remain in a safety report but never enter the system specification
- Requirements are written but lack traceability to the hazard analysis that motivated them
- Timing constraints from safety analysis (FTTI) are lost during translation to requirements
- The derived requirements feedback loop (from lower to higher levels) is skipped

This document covers how each safety analysis method's outputs transform into
requirements, with worked examples from primary sources.

---

## 2. The Aviation Path: FHA → PSSA → Safety Requirements → SSA

### 2.1 The Flow

Research 1 established the process structure. Here we focus on the concrete
transformation at each stage:

```
Aircraft FHA
  │ Produces: failure condition classifications (severity + DAL)
  ↓
System FHA
  │ Produces: system-level failure conditions, FDAL assignments
  ↓
PSSA (Preliminary System Safety Assessment)
  │ Uses: qualitative fault trees, CMA
  │ Produces: safety requirements (failure rate budgets, independence,
  │           redundancy, monitoring), IDAL assignments
  ↓
System Requirements Document
  │ Contains: safety requirements as FIRST-CLASS requirements
  │ (not a separate safety annex — integrated into the spec)
  ↓
DO-178C/DO-254 (SW/HW Development)
  │ May produce: derived requirements (not traceable to higher level)
  │ MUST feed back: to ARP 4754A/4761 for safety impact assessment
  ↓
SSA (System Safety Assessment)
  │ Uses: quantitative fault trees (populated with FMEA failure data)
  │ Verifies: all failure conditions meet probability requirements
```

### 2.2 What FHA Produces (The Starting Point)

The FHA output is a structured table — this is where safety requirements BEGIN:

| Column | Content | Example |
|---|---|---|
| Function | What the system does | Wheel braking |
| Failure condition | What goes wrong | Loss of all wheel braking during landing roll |
| Phase of flight | When | Landing |
| Effect on aircraft | Consequence | Unable to decelerate, runway overrun |
| Severity classification | How bad | Catastrophic |
| DAL assignment | What rigor | A |
| Safety requirements | What must be true | Detection within X seconds, annunciation, alternate braking |

The FHA's "safety requirements" column is qualitative at this stage — it describes what
must be achieved, not how. These become inputs to PSSA for decomposition.
[src-peterson-arp4754a-2015 §2.3 p.4; Research 1 §3.3]

### 2.3 What PSSA Produces (Where Requirements Are Born)

The PSSA takes the FHA outputs and the proposed system architecture, builds qualitative
fault trees, and derives quantitative and qualitative safety requirements:

**From fault tree decomposition:**

1. **Failure rate budgets.** The top event has a target probability (from severity/DAL
   mapping, e.g., Catastrophic = 10⁻⁹/flight hour). The fault tree distributes this
   budget across subsystems. Each leaf event gets an allocated failure rate.
   
   Example requirement: "The hydraulic shutoff valve failure rate shall not exceed
   1 × 10⁻⁶ per flight hour."

2. **Independence/redundancy requirements.** AND gates in the fault tree assume
   independent failures. Where the architecture relies on redundancy, independence
   must be demonstrated. CMA evaluates this.
   
   Example requirement: "The primary display system and the standby display shall
   be independent." (This is a real derived requirement from Peterson PASA — see
   §2.5 below.) [src-peterson-arp4754a-2015 p.94, Table 25, AVSYS-R-010]

3. **Monitoring/detection requirements.** Where a single failure path exists and cannot
   be eliminated, the PSSA identifies the need for detection and annunciation within
   a time budget.
   
   Example requirement: "BSCU shall detect loss of hydraulic pressure and annunciate
   to flight crew within 2 seconds."

4. **Architecture constraints.** The fault tree may reveal that the proposed architecture
   creates unacceptable single points of failure, driving architecture changes.

### 2.4 FDAL and IDAL Assignment — The Peterson 2015 Evidence

The Peterson NASA report provides the most detailed publicly-available worked example
of how FDAL/IDAL assignment works in practice.

**FDAL Assignment (Table PASA-1, p. 48):**

| Avionic Function | Worst FC Classification | Functional Independence? | Assigned FDAL |
|---|---|---|---|
| Autopilot/Autoflight | Catastrophic | No | A |
| Communications | Catastrophic | No | A |
| Displays | Catastrophic | No | A |
| Nav/Flight Management | Hazardous | No | B |
| Maintenance | Catastrophic/Minor | No (note: partitioned) | A & D |
| Platform | Catastrophic | No | A |

[src-peterson-arp4754a-2015 Table 7 p.48, Table 8 p.50]

**Critical finding:** For the SAAB-EII 100 example, functional development independence
was NOT demonstrated in any case at the specification level, even where hardware and
sensor independence existed. The reason: "functionality within a specific functional area
may have common requirements, common development processing, and potential for
common requirement misinterpretation." Therefore, FDAL was always assigned based on
the most severe failure condition without reduction.
[src-peterson-arp4754a-2015 CMA Tables pp.51-57]

**Peterson's broader observation:** "For almost all development project scenarios, the
functional development assurance level (FDAL) can and will be assigned using the
functional hazard assessment classification with the assurance level assigned per
ARP4754A Table 2 or Table 3 using the single member functional failure set (FFS) column.
Most project developments, especially at the aircraft function level, provide minimum
opportunity to use the functional independence attribute."
[src-peterson-arp4754a-2015 p.4]

**Translation:** FDAL reduction through CMA is theoretically possible but practically rare.
Most functions end up at the FDAL corresponding to their worst failure condition.

### 2.5 The 11 Independence Requirements — Concrete Evidence

The Peterson PASA produced exactly 11 derived independence requirements through CMA.
These are the concrete evidence that safety analysis produces requirements that no
stakeholder articulated and no functional analysis would discover:

1. Display of Primary Attitude information shall be independent of standby attitude
2. Display of Primary Airspeed information shall be independent of standby airspeed
3. Display of Primary Altitude information shall be independent of standby altitude
4. Display of Primary Heading information shall be independent of standby heading
5. Left engine parameter displays shall be independent of right engine parameter displays
6. Navigation capability shall be independent of communication capability
7. Captain displayed navigation/position shall be independent of First Officer displayed
8. Take off configuration monitoring shall be independent of aircraft configuration
9. Autopilot engagement monitoring/warning shall be independent of autopilot
10. Autopilot command monitoring/limiting shall be independent of autopilot command generation
11. Maintenance data load monitoring/annunciation shall be independent of maintenance data load

[src-peterson-arp4754a-2015 p.49]

**What makes these requirements special:**
- They are ALL derived from CMA — none came from stakeholder elicitation
- They are negative/independence requirements — they constrain implementation
- They appear in the system requirements as Safety=Y, Source=Derived
- Each requires explicit rationale (WHY it exists — traced to the CMA finding)
- FDAL A requirements are verified with independence (§5.3.1, p.95)

**In the validation matrix (Table 25, p.94):**
AVSYS-R-010 "The primary display system and the standby display shall be independent"
- Safety: Y
- Source: Derived
- Validated by: Inspect + Analysis + Similarity + Trace
- Artifact: Insp-104

**In the verification matrix (Table 26, p.96):**
AVSYS-R-010:
- Safety: Y, FDAL: A
- Verified by: Analysis only (independence is verified through safety analysis, not test)
- Artifact: "Avionic System SSA V1"
[src-peterson-arp4754a-2015 pp.94-96]

### 2.6 The Derived Requirements Feedback Loop

When DO-178C or DO-254 development produces derived requirements (requirements not
traceable to a higher-level requirement), these MUST be fed back to the system level
for safety impact assessment. ARP 4754A Objective 2.4 requires this.
[src-peterson-arp4754a-2015 Table 6 p.44, Objective 2.4]

**What this means in practice:**
- SW team writing code discovers that a timer is needed that wasn't in the requirements
- This timer becomes a derived requirement
- The derived requirement must be evaluated: does it have safety implications?
- If yes: feeds back to system safety for PSSA update
- If the PSSA changes: new safety requirements may be generated

**Peterson finding:** This feedback loop is "new and unfulfilling work" for most engineers.
Only 25% of industry respondents had received training on the process. It is the most
commonly skipped obligation in ARP 4754A.
[src-peterson-arp4754a-2015 p.7]

---

## 3. The Automotive Path: HARA → Safety Goals → FSR → TSR

### 3.1 The Cascade

ISO 26262 defines a cascading safety requirements structure that transforms
vehicle-level hazard analysis into implementable technical requirements:

```
HARA (Part 3, Clause 6)
  │ Identifies: hazardous events, assigns ASIL
  │ Produces: Safety Goals (one per hazardous event, with ASIL)
  ↓
Functional Safety Concept (Part 3, Clause 7)
  │ Derives: Functional Safety Requirements (FSRs) from Safety Goals
  │ Allocates: FSRs to preliminary architecture elements
  │ Defines: FTTI, safe states, warning concepts
  ↓
Technical Safety Concept (Part 4, Clause 6)
  │ Derives: Technical Safety Requirements (TSRs) from FSRs
  │ Allocates: TSRs to HW, SW, or combination
  │ Defines: diagnostic coverage, safety mechanisms, timing budgets
  ↓
SW Requirements (Part 6) / HW Requirements (Part 5)
  │ Receives: allocated TSRs
  │ ASIL of each requirement = highest ASIL of any TSR allocated to it
```

### 3.2 Safety Goals — The Top-Level Safety Requirements

Safety Goals are the direct output of HARA. Each Safety Goal:
- Corresponds to one or more hazardous events
- Has an assigned ASIL (from S × E × C matrix)
- Is expressed at the vehicle/functional level (implementation-independent)
- States WHAT must be prevented/achieved, not HOW

**Example:** "The battery protection function shall avoid a battery fire in charging and
operating modes" (ASIL D)

**Key distinction from aviation:** In aviation, the FHA produces failure conditions with
DAL assignments. In automotive, HARA produces Safety Goals with ASIL assignments.
The concepts are analogous but the nomenclature and process details differ.
[Research 1 §4.1]

### 3.3 Functional Safety Requirements (FSRs) — Implementation-Independent

FSRs decompose Safety Goals into functional behaviors that must be provided.
They are still implementation-independent — they describe WHAT safety behavior is
needed at the functional level.

**FSR types (from Research 1):**
- Fault detection and indication
- Transitioning to/maintaining safe states
- Fault tolerance through redundancy/degradation
- Driver warning requirements
- Arbitration between multiple safety goals

**Each FSR includes:**
- ASIL (inherited from Safety Goal, unless decomposed)
- Safe state definition
- FTTI (Fault Tolerant Time Interval)
- Operating modes relevant to safety

### 3.4 FTTI — The Timing Constraint That Becomes a Requirement

FTTI is one of the most important outputs of the Functional Safety Concept. It defines
the maximum time from fault occurrence to potential hazardous event, assuming no safety
mechanism activates. This constraint directly becomes a timing requirement for the
Technical Safety Concept.

**FTTI = MBMT + HMT**
- MBMT (Malfunctioning Behavior Manifestation Time): time for a fault to propagate to
  vehicle-level malfunction
- HMT (Hazard Manifestation Time): time from malfunction to hazardous event

**The design constraint derived from FTTI:**
FHTI < FTTI - safety_margin
Where FHTI = FDTI (detection time) + FRTI (reaction time)

**Worked example (from secondary source):**
Vehicle speed display fault:
- MBMT: ~0.02s (60Hz display refresh)
- HMT: ~0.5s (driver perception + brake application)
- FTTI: 520ms
- Therefore: detection + reaction must complete in less than 520ms minus margin
[src-ftti-nvdungx-2026]

**Why this matters for requirements:**
FTTI flows DOWN as a timing budget allocated across the architecture:
- Detection function: must detect fault within FDTI
- Reaction function: must transition to safe state within FRTI
- These become VERIFIABLE timing requirements in the TSR

**Cross-domain parallel:** Aviation does not have FTTI as an explicit concept, but the
underlying principle is identical: the PSSA establishes that certain failure conditions
must be detected and annunciated within specific time windows. The FTA shows how
quickly a single failure can propagate to a catastrophic outcome, and this sets the
detection time budget.

### 3.5 Technical Safety Requirements (TSRs) — Implementation-Specific

TSRs bridge from functional safety (WHAT) to implementation (HOW). They include:
- Safety mechanisms and their operating characteristics
- Diagnostic architecture (what, how, when, coverage targets)
- Safe state management (mode transitions, timing)
- HSI (Hardware-Software Interface) specification
- Target values for hardware architectural metrics (SPFM, LFM)
- Allocation to HW, SW, or combination

**Each TSR carries:**
- ASIL (inherited or decomposed from FSR)
- Verification method
- Allocation to architectural element

### 3.6 ASIL Decomposition — Reducing Rigor Through Architecture

ISO 26262 Part 9 allows a high-ASIL requirement to be decomposed across redundant,
independent architectural elements, with each element carrying a lower ASIL.

**Decomposition rules:**
- ASIL D = ASIL D(D) [no decomposition]
- ASIL D = ASIL C(D) + ASIL A(D)
- ASIL D = ASIL B(D) + ASIL B(D)
- ASIL D = ASIL D(D) + QM(D) [only if QM element provably cannot interfere]

**The critical prerequisite is independence.** The Heicon article identifies "freedom from
interference" as the "very important prerequisite for the meaningful application of ASIL
decomposition." If independence is not demonstrated, both elements inherit the original
ASIL. [src-heicon-asil-decomposition-2026]

**Parallel with aviation CMA:** This is functionally identical to the ARP 4754A FDAL→IDAL
reduction through CMA. Peterson found that functional independence was NOT
demonstrated in most cases because of common specification/requirements paths.
The automotive experience mirrors this: decomposition "for individual requirements
without considering the software architecture yields no architectural improvement or
cost advantages." [src-heicon-asil-decomposition-2026]

**Common mistake:** Decomposing individual requirements without considering the
architecture. ASIL decomposition is an ARCHITECTURAL decision that enables requirement
decomposition, not a requirement-level trick for reducing effort.
[src-heicon-asil-decomposition-2026]

---

## 4. The STPA Path: Losses → Constraints → Requirements

### 4.1 From Analysis to Requirements — Direct Derivation

STPA produces requirements more directly than FTA or FMEA because its output
format (constraints) is already close to requirement format. The transformation:

| STPA Output | Transformation | Requirement Type |
|---|---|---|
| System-level constraint | Direct (invert hazard) | Top-level safety requirement |
| Controller constraint | Direct (invert UCA) | Component-level safety requirement |
| Loss scenario (process model flaw) | Derive what must be true | Design/interface requirement |
| Loss scenario (feedback gap) | Derive what information is needed | Interface/monitoring requirement |
| Loss scenario (control path failure) | Derive detection/redundancy need | Safety mechanism requirement |

**Example chain from STPA Handbook Ch. 3 (wheel braking):**

System constraint: "Forward motion must be retarded within TBD seconds of a braking
command upon landing, rejected takeoff, or taxiing" [SC1, from H4-1]
↓
Controller constraint (BSCU): "A brake command must always be provided during RTO"
[BSCU-R1, from UCA BSCU.1a1]
↓
Controller constraint (BSCU): "Braking must never be commanded before touchdown"
[BSCU-R2, from UCA BSCU.1c1]
↓
Controller constraint (Hydraulic Controller): "The HC must not open the green hydraulics
shutoff valve when there is a fault requiring alternate braking" [HC-R1, from UCA HC.1b1]

Each constraint includes the UCA ID it was derived from and the rationale. This is
built-in bidirectional traceability.
[src-leveson-stpa-handbook-2018 Ch.3 pp.63-67, Tables 3.1-3.2]

### 4.2 Why STPA Requirements Are Different

STPA-derived requirements differ from FTA/FMEA-derived requirements in two ways:

**1. They include non-failure scenarios.**
FTA produces requirements like "hydraulic system failure rate < 10⁻⁶/FH."
STPA produces requirements like "BSCU shall not use wheel speed alone to determine
aircraft stopped condition" — derived from a scenario where no component has failed,
but the BSCU's process model is flawed due to misleading sensor readings during
anti-skid operation.

**2. They include context.**
FTA requirements are context-free: "failure rate < X."
STPA requirements specify WHEN: "braking must never be commanded before touchdown"
— the context (before touchdown) came from the UCA analysis that identified providing
the brake command during this specific phase as unsafe.

---

## 5. The MIL-STD-882E Path: Hazard → Risk → Design Requirement

### 5.1 Task 203 (SRHA) — Requirements from Hazard Analysis

MIL-STD-882E Task 203 is explicitly a requirements-generating task. It shall:

1. **Determine system design requirements** to eliminate hazards or reduce associated
   risks by analyzing applicable policies, regulations, standards, and identified hazards
2. **Recommend** appropriate system design requirements
3. **Define verification and validation approaches** for each design requirement
4. **Incorporate** approved design requirements into specifications
5. **Assess compliance** at design reviews (PDR, CDR)
[src-mil-std-882e-2012 Task 203 pp.49-50]

### 5.2 The Design Order of Precedence Applied to Requirements

MIL-STD-882E §4.3.4 establishes a hierarchy for risk mitigation that directly shapes
the types of requirements produced:

| Precedence | Approach | Requirement Type Example |
|---|---|---|
| 1. Eliminate hazard by design | Inherent safety | "System shall not use flammable hydraulic fluid" |
| 2. Reduce risk by design | Design alternative | "Braking shall use dual-redundant hydraulic circuits" |
| 3. Safety devices | Engineering control | "Independent pressure sensor shall detect hydraulic loss" |
| 4. Warning devices | Annunciation | "Low pressure shall be annunciated to crew within 2 sec" |
| 5. Procedures/training | Administrative | "Crew shall verify braking function before takeoff" |

The precedence is mandatory: you cannot skip to level 4 (warnings) without first
documenting why levels 1-3 are infeasible. Requirements at lower precedence levels
must include rationale for why higher-precedence solutions were rejected.
[src-mil-std-882e-2012 §4.3.4-4.3.5 pp.12-13]

---

## 6. What Good Safety Requirements Look Like

### 6.1 Common Failure Modes in Safety Requirements

| Anti-Pattern | Example | Problem |
|---|---|---|
| **Vague aspiration** | "The system shall be safe" | Not verifiable |
| **Severity without threshold** | "The system shall minimize risk" | No acceptance criteria |
| **Missing context** | "Braking shall be provided" | When? Under what conditions? |
| **Missing timing** | "The fault shall be detected" | How fast? FTTI not allocated |
| **Implementation masquerading as requirement** | "Use triple modular redundancy" | Prescribes solution, not need |
| **Safety in a silo** | Safety requirements in a separate safety annex, not in the system spec | Not developed/tested as first-class requirements |
| **Missing traceability** | "Req-042: Independent displays required" with no link to hazard analysis | Cannot assess safety impact of changes |

### 6.2 Properties of Good Safety Requirements

A safety requirement must satisfy all the usual requirement quality criteria (verifiable,
unambiguous, traceable, etc. — see codex `concept-requirement-quality`) PLUS:

1. **Traceable to hazard analysis.** Every safety requirement must trace to an FHA
   failure condition, an FMEA finding, an STPA UCA, or a CMA independence
   requirement. The traceability must be bidirectional.

2. **Safety attribute marked.** The requirement must be explicitly flagged as
   safety-related in the requirements management system.
   [src-peterson-arp4754a-2015 p.89 — each requirement includes a "Safety related
   attribute"]

3. **Integrity level assigned.** DAL/ASIL/SIL attached to the requirement, inherited
   from or assigned by the safety analysis.

4. **Verification method defined.** Safety requirements typically require more
   rigorous verification (analysis + test, not just test). Independence requirements
   are often verified by safety analysis (SSA), not by test.
   [src-peterson-arp4754a-2015 p.96 — AVSYS-R-010 verified by "Analysis only"]

5. **Rationale documented.** Unlike functional requirements (which trace to stakeholder
   needs), derived safety requirements trace to safety analysis findings. The rationale
   explains WHY the requirement exists — which hazard, which failure path, which
   CMA finding.
   [src-peterson-arp4754a-2015 p.89 — "Rationale (reason for having the requirement
   if derived)"]

6. **Timing constraints specified.** Where FTTI analysis has been performed, the
   detection and reaction time budgets must appear as verifiable timing requirements.

7. **Negative requirements explicitly stated.** Independence requirements are negative
   ("shall be independent of") rather than positive ("shall do X"). These are
   counterintuitive but critical — they constrain implementation rather than
   specifying behavior.

---

## 7. Cross-Domain Comparison: How Safety Analysis Becomes Requirements

| Dimension | Aviation (ARP 4754A/4761) | Automotive (ISO 26262) | Military (MIL-STD-882E) |
|---|---|---|---|
| **Entry point** | FHA → failure conditions | HARA → hazardous events | PHL/PHA → hazard list |
| **Risk classification** | Severity → DAL (A-E) | S×E×C → ASIL (A-D, QM) | Severity × Probability → RAC |
| **Requirements cascade** | FHA → PSSA → System Req → Item Req | Safety Goal → FSR → TSR → SW/HW Req | PHA → SRHA → Design Req |
| **Timing constraint** | Detection time from FTA | FTTI from FSC | No explicit timing framework |
| **Integrity reduction** | FDAL→IDAL via CMA | ASIL decomposition via Part 9 | SwCI from SCC × Severity |
| **Independence validation** | CMA (3 categories: architecture, technology, specification) | Freedom from interference | Common cause analysis |
| **Feedback loop** | Derived req → system safety assessment | Derived req → FSC update | SSHA → SHA feedback |
| **Requirement attributes** | Safety=Y, DAL, parent trace, rationale | ASIL, traceability to Safety Goal | RAC, hazard reference |

---

## 8. Source List

### Primary sources (read from files in codex raw/)

1. **Peterson 2015** — Peterson, Eric M. "Application of SAE ARP4754A to Flight
   Critical Systems." NASA/CR-2015-218982, November 2015.
   Read pp. 44-57 (PASA/CMA tables), pp. 79-80 (FHA impact), pp. 89-96
   (validation/verification matrices).
   Raw path: `raw/papers/peterson-arp4754a-nasa-2015.pdf`

2. **STPA Handbook** — Leveson & Thomas. March 2018.
   Read Ch. 3 pp. 54-71 (integration with V-model).
   Raw path: `raw/books/leveson-thomas-stpa-handbook.pdf`

3. **MIL-STD-882E** — Department of Defense. May 2012.
   Read §4.3 pp. 9-17 (risk framework), Task 203 pp. 49-50 (SRHA).
   Raw path: `raw/standards/mil-std-882e.pdf`

4. **ASPICE PAM v4.0** — VDA QMC. 2023.
   SYS.2-SYS.3 processes (system requirements and architecture).
   Raw path: `raw/standards/Automotive-SPICE-PAM-v40.pdf`

### Secondary sources (fetched online, saved to codex raw/articles/)

5. **FTTI article** — nvdungx.github.io, fetched 2026-04-12.
   FTTI calculation framework with worked example.
   Raw path: `raw/articles/ftti-iso26262-nvdungx-2026.md`

6. **Heicon ASIL Decomposition** — heicon-ulm.de, fetched 2026-04-12.
   ASIL decomposition pros/cons and common mistakes.
   Raw path: `raw/articles/heicon-asil-decomposition-2026.md`
