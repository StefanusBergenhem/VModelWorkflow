# Research 4a: Safety Analysis Methods — FTA, FMEA, and STPA

Research for upper V documentation (backlog items 3.4, 3.5, 3.6). Covers the actual analytical
methods used in safety assessment — how to perform them, what they produce, and their
strengths and limitations. Research 1 already covers the process structure (FHA→PSSA→SSA,
HARA→SG→FSC→TSC). This document covers the HOW, not the process flow.

**Sources used:**
- STPA Handbook, Leveson & Thomas, March 2018 (primary, read from PDF pp. 1-71)
  [src-leveson-stpa-handbook-2018]
- MIL-STD-882E, Department of Defense, May 2012 (primary, read from PDF pp. 1-83)
  [src-mil-std-882e-2012]
- Bosch Booklet No. 14: Failure Mode and Effects Analysis, Robert Bosch GmbH, 2012
  (primary, read from PDF all 20 pages) [src-bosch-fmea-booklet-2012]
- Peterson, NASA/CR-2015-218982, 2015 (primary, pp. 44-57 CMA tables)
  [src-peterson-arp4754a-2015]
- Research 1: Standards — System-Level Processes (internal, for context)

---

## 1. The Safety Analysis Method Landscape

Safety analysis methods divide into three families based on their reasoning direction
and the type of hazard causes they can identify:

| Family | Direction | Representative Methods | What It Finds |
|---|---|---|---|
| **Deductive (top-down)** | Start from undesired event, work backward to causes | FTA, Dependence Diagrams | How combinations of failures lead to a hazard |
| **Inductive (bottom-up)** | Start from component failure, work forward to effects | FMEA/FMECA, Event Tree Analysis | What happens when a single component fails |
| **Systems-theoretic** | Start from control structure, identify unsafe interactions | STPA | How unsafe interactions (including non-failures) lead to hazards |

No single method is sufficient. ARP 4761 prescribes FTA and FMEA as complementary
(top-down + bottom-up). STPA was developed specifically to address the class of accidents
that neither FTA nor FMEA can find — those caused by unsafe interactions between
components that have not individually failed.
[src-leveson-stpa-handbook-2018 Ch.1 p.4; src-mil-std-882e-2012 §3.6 p.68]

**Key structural difference:** FTA and FMEA are failure-based methods — they assume
accidents are caused by component failures (hardware breaks, software crashes). STPA is
based on systems theory and assumes accidents can also be caused by unsafe interactions
between components that are individually functioning correctly — design errors, flawed
requirements, timing conflicts, mode confusion, and inadequate feedback.
[src-leveson-stpa-handbook-2018 Ch.1 pp.4-5]

---

## 2. Fault Tree Analysis (FTA)

### 2.1 What FTA Is

Fault Tree Analysis is a top-down, deductive method. You start with an undesired
system-level event (the "top event") and systematically decompose it into the combinations
of lower-level events that could cause it. The result is a tree-structured logic diagram
showing how failures propagate through the system.

FTA is the primary method prescribed by ARP 4761 for deriving safety requirements
during the PSSA (Preliminary System Safety Assessment). It is also referenced in
MIL-STD-882E as a key analysis technique for system and subsystem hazard analysis.
[src-mil-std-882e-2012 TOC p.v — "FTA" listed as Task 209 in Change 1 addition]

### 2.2 Fault Tree Construction — Step by Step

**Step 1: Define the top event.**
The top event is a specific, unambiguous system-level hazard. It must be a single,
well-defined undesired state — not vague ("system failure") but precise ("loss of all
wheel braking during landing roll"). The top event typically comes from the FHA.

**Step 2: Identify immediate causes.**
Ask: "What events could directly cause this top event?" Each cause becomes a child
node. Connect them with logic gates:

- **OR gate:** The output occurs if ANY input occurs (models redundancy failure —
  all parallel paths must fail). Increases system failure probability.
- **AND gate:** The output occurs only if ALL inputs occur simultaneously (models
  where multiple independent failures are needed). Decreases system failure
  probability — this is where redundancy provides its value.
- **Inhibit gate:** An AND gate where one input is a conditional event (an enabling
  condition that is not itself a failure).

**Step 3: Continue decomposition.**
Repeat for each intermediate event until you reach "basic events" — events that
cannot be further decomposed. Basic events are typically:
- Hardware component failures (with known or estimated failure rates)
- Software errors (typically modeled as undeveloped events — see below)
- Human errors
- External events (environmental conditions)

Special event types:
- **Undeveloped event** (diamond symbol): An event that could be further decomposed
  but is not, either because information is insufficient or the branch is outside scope.
  Software failures are often modeled this way because software does not "fail"
  probabilistically the way hardware does — it executes its logic deterministically.
- **House event** (pentagon symbol): An event that is either certain to occur or certain
  not to occur — used to model operational conditions or system configurations.
- **Transfer symbol:** Connects to another fault tree (for managing complexity in
  large systems).

**Step 4: Validate the tree.**
Review for logical completeness:
- Every intermediate event must have at least one gate and child events
- Every branch must terminate in a basic or undeveloped event
- No circular logic (event A causes B causes A)
- Common cause failures are explicitly modeled (a single failure appearing in
  multiple branches — this is where CCA begins)

### 2.3 Cut Set Analysis

Once the fault tree is constructed, the critical analytical output is the **minimal cut set**.

**Cut set:** Any combination of basic events that, if all occur simultaneously, causes the
top event to occur.

**Minimal cut set (MCS):** A cut set where removing any single event prevents the top
event. These are the minimum combinations of failures needed.

**Why cut sets matter for requirements:**
- A **single-event minimal cut set** (a cut set with one basic event) means a single
  failure can cause the top event. This is a single point of failure and is typically
  unacceptable for catastrophic or hazardous failure conditions. The safety
  requirement derived from this: eliminate the single point of failure through
  redundancy, monitoring, or design change.
- A **dual-event minimal cut set** means two independent failures are needed.
  The safety requirement: ensure the two events are truly independent (no common
  cause), and that the combined probability meets the target.
- The **order** of a cut set (number of events) indicates the level of redundancy
  protecting against that failure path.

**Qualitative vs. Quantitative FTA:**

| Aspect | Qualitative | Quantitative |
|---|---|---|
| **Purpose** | Identify failure paths, derive requirements | Calculate system failure probability |
| **When** | PSSA (early design) | SSA (verification) |
| **Input** | Architecture, failure modes | Basic event failure rates |
| **Output** | Minimal cut sets, safety requirements | Probability of top event |
| **Used by** | ARP 4761 PSSA, ISO 26262 Part 4 | ARP 4761 SSA |

**Quantitative calculation (simplified):**
- OR gate: P(output) ≈ P(A) + P(B) for small probabilities (union)
- AND gate: P(output) = P(A) × P(B) (intersection, assuming independence)
- System probability = sum over all minimal cut sets

The AND gate multiplication is why redundancy works: if P(component) = 10⁻³ per
flight hour, a dual-redundant system with AND logic has P(system) = 10⁻⁶ per flight
hour — provided independence is maintained. This is also why CMA (Common Mode
Analysis) is critical: if both components share a common cause failure, the AND gate
becomes an OR gate and redundancy provides no benefit.

### 2.4 What FTA Produces for Requirements

FTA's primary output for requirements engineering is the set of safety requirements
derived from the fault tree structure:

1. **Failure rate budgets:** Each basic event in a quantitative tree has an allocated
   failure rate. These become reliability requirements for components.
2. **Independence requirements:** AND gates in the tree assume independence between
   inputs. CMA verifies this assumption. Where independence is needed but not
   demonstrated, derived requirements mandate separation (separate power sources,
   different processors, diverse software).
3. **Monitoring requirements:** Where a single failure cannot be eliminated, the tree
   shows where detection and annunciation are needed to maintain acceptable risk.
4. **Redundancy requirements:** Single-point failures in the tree that cannot be
   eliminated by design require redundancy — the tree directly shows where.
5. **Architecture constraints:** The tree structure reflects the system architecture.
   Changing the architecture changes the tree. FTA thus provides feedback to
   architecture: "this decomposition creates an unacceptable single point of failure."

### 2.5 FTA Limitations

FTA has well-documented limitations that motivate the use of complementary methods:

1. **Failure-centric:** FTA models component failures. It cannot model unsafe
   interactions between correctly-functioning components, design errors, or
   requirements defects. [src-leveson-stpa-handbook-2018 Ch.1 p.4]
2. **Static analysis:** FTA captures one system state. Timing-dependent failures,
   race conditions, and sequence-dependent interactions are difficult to model.
3. **Software blind spot:** Software does not fail stochastically — it executes its logic
   every time. FTA models software as an undeveloped event, which means software
   contributions to hazards are not systematically analyzed.
   [src-leveson-stpa-handbook-2018 Ch.1 pp.4-5]
4. **Combinatorial explosion:** Complex systems produce very large fault trees. The
   number of cut sets grows exponentially with tree depth.
5. **Assumes known failure modes:** FTA can only analyze failure modes that the
   analyst includes. Novel failure modes, unexpected interactions, and unknown
   unknowns are not captured.
6. **Decomposition assumption:** FTA assumes the system can be decomposed into
   independent components whose failure behaviors combine predictably. Leveson
   argues this assumption fails for software-intensive systems where component
   interactions create emergent behaviors not predictable from individual component
   analysis. [src-leveson-stpa-handbook-2018 Ch.1 pp.5-6, Appendix E p.167]

---

## 3. Failure Modes and Effects Analysis (FMEA)

### 3.1 What FMEA Is

FMEA is a bottom-up, inductive method. You start with individual components (or
functions, or process steps), systematically enumerate their failure modes, trace the
effects of each failure upward through the system, and assess the risk using severity,
occurrence, and detection ratings.

FMEA originated in US military procedures (MIL-P-1629, 1949), was adopted by NASA
for Apollo (1963), entered automotive through Ford (1977), and was standardized
internationally as IEC 60812 (2001). The automotive industry uses the AIAG-VDA FMEA
Handbook (harmonized 2019) as the reference methodology.
[src-bosch-fmea-booklet-2012 §1.2 p.3]

**Fundamental limitation acknowledged by practitioners:** FMEA analyzes individual
failures, not failure combinations. It is a qualitative method producing relative risk
estimates, not absolute probability calculations. Quantitative failure probability
analysis and failure combination analysis require FTA.
[src-bosch-fmea-booklet-2012 §1.3 p.4]

### 3.2 Types of FMEA

| Type | Scope | Performed By | Inputs |
|---|---|---|---|
| **Product FMEA** (Design FMEA) | Design of products, parts, interfaces | Development team | Requirements, design drawings, 3D models |
| **Process FMEA** | Manufacturing/assembly processes | Production team | Process flow chart, control plan |

Product FMEA and Process FMEA are complementary — Product FMEA identifies what
can go wrong in the design; Process FMEA identifies what can go wrong in manufacturing.
For safety-critical systems, both are typically required.
[src-bosch-fmea-booklet-2012 §2.1-2.2 p.6]

### 3.3 The 5-Step FMEA Process (Bosch/VDA Method)

The Bosch methodology (aligned with VDA Volume 4 and AIAG) defines five analytical
steps. The newer AIAG-VDA harmonized handbook (2019) expands this to seven steps by
adding explicit planning and documentation steps.

**Step 1: Structural Analysis**
Build the system/component hierarchy (block diagram or tree structure).
- Product FMEA: Vehicle → System → Subsystem → Component → Part
- Process FMEA: Process → Station → Step → 5M categories (Man, Machine, Method,
  Material, Milieu)
- Identify system boundaries and interfaces
[src-bosch-fmea-booklet-2012 §3.1 pp.15-17]

**Step 2: Functional Analysis**
Map functions and requirements to each element in the structure.
- Identify all functions (functional characteristics) and qualities (non-functional
  characteristics) for each system element
- Build a "function net" showing functional dependencies between elements
- Link requirements to functions: legal, customer, internal
- The existence and completeness of requirements is a prerequisite for FMEA — if
  requirements are missing, FMEA cannot evaluate what "failure" means
[src-bosch-fmea-booklet-2012 §3.2 pp.18-24]

**Step 3: Failure Analysis**
For each function identified in Step 2, enumerate possible failures:
- **Failure/malfunction:** The negation of a function (function not performed, performed
  incorrectly, performed at wrong time, unintended function)
- **Failure effect:** Consequence at the next higher level, traced up to the system/vehicle
  level — this is what determines severity
- **Failure mode/cause:** The mechanism producing the failure at the component level —
  this is what determines occurrence and detectability
- Build a "failure net" mirroring the function net: failure causes → failure →
  failure effects form cause-effect chains
[src-bosch-fmea-booklet-2012 §3.3 pp.25-28]

**Step 4: Action Analysis (Risk Assessment)**
Assign three ratings to each failure mode chain:

**Severity (S):** How severe is the effect on the end user/vehicle? Scale 1-10.
- S=1: No noticeable effect
- S=9-10: Safety-related failure (potential regulatory violation, endangerment)
- When failure has safety impact, it must be flagged as a "Special Characteristic"
- Severity is determined by the WORST case effect at the highest system level

**Occurrence (O):** How likely is the failure cause to occur? Scale 1-10.
- Based on prevention measures already in the design
- O=1: Failure practically impossible (proven prevention in place)
- O=10: Very high (no prevention, frequent occurrence expected)

**Detection (D):** How likely is the failure to be detected before reaching the customer?
Scale 1-10.
- Based on detection measures in the design/process
- D=1: Failure will certainly be detected (validated detection method)
- D=10: No detection possible

**Risk Priority Number:** RPN = S × O × D (range 1-1000)
- The traditional prioritization metric
- **Important caveat:** RPN has well-known problems — the same RPN can arise from
  very different risk profiles (S=10,O=1,D=1 = 10 vs S=1,O=10,D=1 = 10). The
  first is a rare but catastrophic risk; the second is a frequent but trivial annoyance.
  The newer AIAG-VDA methodology replaces RPN with Action Priority (AP) tables
  that prioritize based on S first, then O, then D.
[src-bosch-fmea-booklet-2012 §3.4 pp.29-33]

**Step 5: Optimization**
- Identify improvement actions for highest-priority risks
- Assign responsible persons and deadlines
- Re-evaluate S, O, D after actions are implemented
- Continue until remaining risk is accepted
[src-bosch-fmea-booklet-2012 §3.5 pp.34-35]

### 3.4 What FMEA Produces for Requirements

FMEA's output for requirements engineering:

1. **Severity classification:** When S ≥ 9 (safety-related), the failure mode must be
   addressed with safety requirements. In ISO 26262 context, this connects to HARA —
   the FMEA severity rating should be consistent with the ASIL determination.
2. **Detection requirements:** High D ratings (failure not detectable) generate
   requirements for diagnostic functions, built-in test, monitoring algorithms.
3. **Prevention requirements:** High O ratings generate requirements for design
   changes, redundancy, or process controls.
4. **Special Characteristics:** Safety-relevant product/process characteristics identified
   through FMEA must be flagged and controlled throughout the lifecycle.
   [src-bosch-fmea-booklet-2012 §2.6.3 p.12]
5. **Interface requirements:** The function net analysis often reveals missing or
   incomplete interface specifications.

### 3.5 FMEA Limitations

1. **Single-failure analysis only:** FMEA examines one failure at a time. It cannot
   identify hazards that arise from combinations of failures or from unsafe
   interactions between correctly-functioning components.
   [src-bosch-fmea-booklet-2012 §1.3 p.4]
2. **Requires complete system decomposition:** FMEA cannot be started until
   the design is sufficiently detailed to enumerate components and failure modes.
   This limits its use in early concept phases.
3. **Depends on analyst knowledge:** The quality of FMEA is entirely dependent on
   the team's ability to enumerate failure modes. Unknown failure modes are missed.
4. **Qualitative, not quantitative:** FMEA produces relative risk rankings, not
   absolute failure probabilities. It cannot demonstrate compliance with quantitative
   safety targets (e.g., 10⁻⁹ per flight hour).
5. **The RPN problem:** Equal RPNs can represent radically different risk profiles.
   High-severity, low-frequency failures can receive the same priority as
   low-severity, high-frequency ones.
6. **Volume problem:** Large systems produce enormous FMEA worksheets (thousands
   of rows). Maintaining and reviewing them becomes a quality problem in itself.

### 3.6 FMEA and FTA: Complementary, Not Competing

FMEA and FTA are explicitly complementary in all safety standards:

- **FMEA (bottom-up)** identifies failure modes and their effects, feeding failure rate
  data into FTA. It answers: "what happens if this component fails?"
- **FTA (top-down)** identifies how combinations of failures lead to hazards, using
  FMEA's failure mode data. It answers: "how can this hazard occur?"

In the ARP 4761 SSA process, FMEA provides the component-level failure rates that
populate the quantitative fault tree. The two methods together provide both the
"what fails" view (FMEA) and the "how it combines to cause harm" view (FTA).

In ISO 26262, Product FMEA is a primary method for identifying hardware failure modes
and feeding them into the safety analysis. The FMEA severity should be cross-checked
against the HARA ASIL determination — if FMEA finds a high-severity failure that HARA
did not identify, the HARA may be incomplete.

---

## 4. STPA (Systems-Theoretic Process Analysis)

### 4.1 What STPA Is and Why It Exists

STPA is a hazard analysis technique based on systems theory rather than reliability
theory. It was developed by Nancy Leveson at MIT to address a fundamental gap in
traditional methods: modern accidents increasingly involve unsafe interactions between
components that have not individually failed.
[src-leveson-stpa-handbook-2018 Ch.1 p.4]

**The core argument:** Traditional methods (FTA, FMEA) assume accidents are caused by
chains of component failures. This assumption worked well when systems were primarily
mechanical/electromechanical. In software-intensive systems, a large class of accidents
involves:
- Software executing its logic exactly as programmed, but the logic is wrong
- Requirements that are incomplete or conflicting
- Humans and automation interacting in unexpected ways (mode confusion)
- Timing dependencies between correctly-functioning components
- Design assumptions that don't hold in all operational contexts

FTA cannot model these because they are not "failures." FMEA cannot find them because
no component has "failed." STPA models the system as a set of control loops and
systematically identifies how control actions can be unsafe — regardless of whether the
cause is a failure or not.
[src-leveson-stpa-handbook-2018 Ch.1 pp.4-5]

**Empirical evidence cited by Leveson:** Many evaluations comparing STPA to traditional
methods (FTA, FMEA, HAZOP, ETA) have been conducted. "In all of these evaluations,
STPA found all the causal scenarios found by the more traditional analyses but it also
identified many more, often software-related and non-failure, scenarios that the
traditional methods did not find. In some cases, where there had been an accident that
the analysts had not been told about, only STPA found the cause of the accident."
[src-leveson-stpa-handbook-2018 Ch.1 p.4]

### 4.2 The STPA Process — Four Steps

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ 1) Define    │──▶│ 2) Model     │──▶│ 3) Identify  │──▶│ 4) Identify  │
│ Purpose of   │   │ the Control  │   │ Unsafe       │   │ Loss         │
│ the Analysis │   │ Structure    │   │ Control      │   │ Scenarios    │
│              │   │              │   │ Actions      │   │              │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
 Losses, Hazards   Controllers,       UCA Table,         Causal factors,
 System boundary   Control actions,    Controller         Design
                   Feedback loops      Constraints        requirements
```
[src-leveson-stpa-handbook-2018 Ch.2 p.14]

#### Step 1: Define the Purpose of the Analysis

Four sub-steps:

**1a. Identify losses.** A loss is something of value to stakeholders — not limited to
safety. Can include loss of life, property damage, mission loss, environmental damage,
financial loss, reputation loss. Examples:
- L-1: Loss of life or injury to people
- L-2: Loss of or damage to vehicle
- L-4: Loss of mission
[src-leveson-stpa-handbook-2018 Ch.2 p.16]

**1b. Identify system-level hazards.** A hazard is a system state or condition that,
together with worst-case environmental conditions, will lead to a loss. Three criteria:
- Hazards are system states (not component failures or environmental states)
- Hazards will lead to a loss in some worst-case environment
- Hazards describe conditions to be prevented

Critical writing rules:
- Do NOT reference individual components ("brake failure" is a cause, not a hazard)
- Do NOT use "unsafe" in the hazard statement (recursive definition)
- DO specify the actual unsafe condition ("Aircraft violate minimum separation
  standards in flight")
- Keep to 7-10 system-level hazards maximum
[src-leveson-stpa-handbook-2018 Ch.2 pp.17-19]

**Hazard specification format:**
`<Hazard> = <System> & <Unsafe Condition> & <Link to Losses>`
Example: "H-1: Aircraft violate minimum separation standards in flight [L-1, L-2, L-4, L-5]"
[src-leveson-stpa-handbook-2018 Ch.2 p.19]

**1c. Identify system-level constraints.** Invert each hazard:
`<System-level Constraint> = <System> & <Condition to Enforce> & <Link to Hazards>`
Example: "SC-1: Aircraft must satisfy minimum separation standards from other aircraft
and objects [H-1]"
[src-leveson-stpa-handbook-2018 Ch.2 p.20]

**1d. Refine hazards (optional).** For large/complex analyses, decompose hazards into
sub-hazards. Example: H-4 "Aircraft comes too close to other objects on the ground"
refines into sub-hazards for deceleration, acceleration, and steering.
[src-leveson-stpa-handbook-2018 Ch.2 pp.20-21]

#### Step 2: Model the Control Structure

Build a hierarchical control structure — a functional model of the system showing how
controllers interact through control actions and feedback.

**Key concepts:**
- **Controller:** Makes decisions and provides control actions (can be human, software,
  or hardware)
- **Controlled process:** What the controller controls
- **Control action:** Downward command from controller to controlled process
- **Feedback:** Upward information from controlled process to controller
- **Process model:** The controller's internal beliefs about the controlled process
- **Control algorithm:** How the controller decides what control actions to provide
[src-leveson-stpa-handbook-2018 Ch.2 pp.22-23]

**Critical properties of the control structure:**
- Vertical axis represents authority/control hierarchy (higher = more authority)
- It is a FUNCTIONAL model, not a physical model — connections represent
  information flow, not physical wiring
- It does NOT assume obedience — just because a control action is sent doesn't
  mean it will be followed
- It can be incomplete — STPA will identify missing feedback and control
- Abstraction manages complexity — start high-level, refine iteratively
[src-leveson-stpa-handbook-2018 Ch.2 pp.25-26]

**Example (aircraft wheel braking):**
```
        Flight Crew
       /     |      \
  Manual  Arm/Set  Manual
  controls Disarm  braking
      |      |
      BSCU (Brake System Control Unit)
         |
    Brake/anti-skid commands
         |
    WBS Hydraulics
         |
    Wheel Brakes → Wheels
         ↑
    Wheel speed feedback
```
[src-leveson-stpa-handbook-2018 Ch.2 pp.27-30, Fig 2.12 p.30]

#### Step 3: Identify Unsafe Control Actions (UCAs)

For each control action in the control structure, systematically check four types of
unsafe behavior:

| Type | Question |
|---|---|
| 1. Not providing | Does NOT providing this control action lead to a hazard? |
| 2. Providing | Does providing this control action lead to a hazard? |
| 3. Too early/late/out of order | Is the timing or sequence wrong? |
| 4. Stopped too soon/applied too long | For continuous actions: wrong duration? |

**UCA format (five parts):**
`<Source> <Type> <Control Action> <Context> [Link to Hazards]`

Example: "UCA-2: BSCU Autobrake provides Brake command during a normal takeoff
[H-4.3, H-4.5]"
[src-leveson-stpa-handbook-2018 Ch.2 pp.35-37]

**Context is critical.** A control action is almost never unsafe in ALL contexts — it was
designed for a reason. The UCA must specify WHEN the action is unsafe. UCA-2 is
unsafe specifically "during a normal takeoff" — braking during landing is the intended
behavior. Without context, the analysis produces meaningless results.
[src-leveson-stpa-handbook-2018 Ch.2 pp.36-37]

**The four types are provably complete** — there is no other category of unsafe control
action. This is one of STPA's methodological advantages over FTA/FMEA where
completeness depends entirely on analyst knowledge.
[src-leveson-stpa-handbook-2018 Ch.2 p.38]

**UCAs → Controller Constraints:** Each UCA is inverted to define a constraint:
- UCA-1: BSCU Autobrake does not provide Brake during landing roll when armed [H-4.1]
- C-1: BSCU Autobrake must provide Brake during landing roll when armed [UCA-1]
[src-leveson-stpa-handbook-2018 Ch.2 p.41, Table 2.5]

#### Step 4: Identify Loss Scenarios

For each UCA, identify WHY it might occur. Two types of scenarios:

**Type (a): Why would the UCA occur?**
- **Controller failure** (physical): power loss, hardware fault
- **Inadequate control algorithm:** flawed implementation, flawed specification,
  algorithm becomes inadequate over time (algorithm worked at design time but
  environment changed)
- **Unsafe control input:** UCA from another controller
- **Inadequate process model:** Controller's beliefs about the controlled process
  don't match reality. This is where the real power of STPA lies — process model
  flaws are the #1 source of software-related accidents.

Process model flaws occur because:
  - Controller receives incorrect feedback/information
  - Controller receives correct feedback but interprets it incorrectly
  - Controller does not receive feedback when needed (delayed or never received)
  - Necessary feedback/information does not exist in the design
[src-leveson-stpa-handbook-2018 Ch.2 pp.43-48]

**Type (b): Why would a safe control action be improperly executed?**
- **Control path scenarios:** Control action not received by actuator, received
  improperly, actuator fails, actuator responds inadequately
- **Controlled process scenarios:** Process doesn't respond, responds improperly,
  is affected by external disturbances or other controllers
[src-leveson-stpa-handbook-2018 Ch.2 pp.48-51]

**Example scenario (detailed):**
UCA-2: BSCU Autobrake does not provide Brake during landing roll when armed [H-4.1]
- Process model flaw: BSCU believes aircraft has already stopped (but it hasn't)
- Cause: Wheel speed signals momentarily reach zero during anti-skid operation
- Scenario: "The BSCU is armed and the aircraft begins landing roll. The BSCU does
  not provide the Brake control action because the BSCU incorrectly believes the
  aircraft has already come to a stop. This flawed process model will occur if the
  received feedback momentarily indicates zero speed during landing roll."
[src-leveson-stpa-handbook-2018 Ch.2 p.47]

### 4.3 What STPA Produces for Requirements

STPA's output is directly actionable as requirements:

1. **System-level constraints:** Derived from hazards — "Aircraft must satisfy minimum
   separation standards" [SC-1]. These become top-level safety requirements.
2. **Controller constraints:** Derived from UCAs — "BSCU Autobrake must provide
   Brake control action during landing roll when armed" [C-1]. These become
   component-level safety requirements with traceability to the hazard.
3. **Design constraints from scenarios:** "The BSCU shall not use wheel speed alone
   to determine aircraft stopped condition" — derived from the scenario analysis.
   These become detailed design requirements.
4. **Feedback requirements:** Missing feedback identified in the control structure
   becomes interface requirements: "Weight-on-wheels status shall be provided to
   the BSCU" [from scenario analysis of UCA-2].
5. **Test cases:** Each UCA and scenario maps directly to a test case — test that the
   constraint holds under the identified conditions.
[src-leveson-stpa-handbook-2018 Ch.2 pp.52-53; Ch.3 pp.66-67]

**Traceability chain:**
```
Loss → Hazard → System Constraint → UCA → Controller Constraint → Scenario →
Design Requirement → Test Case
```
Every STPA result traces back to losses through this chain. This built-in traceability
is a significant advantage for V-model compliance — the safety requirements produced
by STPA already have the traceability that standards require.
[src-leveson-stpa-handbook-2018 Ch.2 p.52, Fig 2.21]

### 4.4 STPA Integration with the V-Model

STPA maps to every phase of the V-model lifecycle. Chapter 3 of the handbook provides
the detailed integration:

| V-Model Phase | STPA Contribution |
|---|---|
| Concept Development | Identify losses, system-level hazards, initial constraints |
| System Requirements | Refine requirements, allocate constraints to components |
| System Architecture | Evaluate architecture against hazards, identify unsafe interactions |
| Design & Development | Generate detailed design constraints, test requirements |
| System Integration | Evaluate identified integration hazards (should be minimal if STPA was used early) |
| System Test | Generate test requirements and leading indicators |
| Operations | Generate operational safety requirements, monitor leading indicators |

**Key insight from Leveson:** "In our experience, architectures are often developed before
the safety (and often the system) requirements are identified. This inverted sequence
raises the likelihood that the architecture will not be optimized for and sometimes not
even appropriate for the system goals."
[src-leveson-stpa-handbook-2018 Ch.3 p.63]

**Frola & Miller (1984) finding cited by Leveson:** 70-90% of the design decisions related
to safety are made in the concept development stage and changing these decisions later
may be infeasible or enormously expensive.
[src-leveson-stpa-handbook-2018 Ch.3 p.56]

### 4.5 STPA Limitations

1. **No quantitative risk assessment:** STPA produces constraints and scenarios, not
   failure probabilities. It cannot demonstrate compliance with quantitative safety
   targets. FTA is still needed for probability calculations.
2. **Analyst skill dependent:** Like all hazard analysis methods, STPA quality depends
   on the analyst's understanding of the system. The systematic structure reduces
   but does not eliminate this dependency.
3. **Not yet mandated by standards:** ARP 4761 prescribes FTA, FMEA, and other
   traditional methods. STPA is not explicitly listed in ARP 4761, ISO 26262, or
   MIL-STD-882E (though MIL-STD-882E's Task 208 FHA is method-agnostic). STPA
   can be used as a complementary method alongside required methods.
4. **Does not replace FTA/FMEA for hardware reliability:** STPA does not produce
   component failure rates or reliability predictions. Hardware reliability analysis
   still requires FMEA (for failure modes) and FTA (for probability calculations).
5. **Learning curve:** The systems-theoretic paradigm is different from the
   failure-and-reliability paradigm most safety engineers were trained in.

---

## 5. MIL-STD-882E: The Military System Safety Framework

### 5.1 The Eight-Element System Safety Process

MIL-STD-882E defines a generic, domain-independent system safety process in eight
elements. Unlike ARP 4761 (which prescribes specific analytical methods) or ISO 26262
(which prescribes specific lifecycle phases), MIL-STD-882E defines WHAT must be done
but allows flexibility in HOW.

```
Element 1: Document the System Safety Approach
     ↓
Element 2: Identify and Document Hazards
     ↓
Element 3: Assess and Document Risk
     ↓
Element 4: Identify and Document Risk Mitigation Measures
     ↓                              ↗ (iterate)
Element 5: Reduce Risk
     ↓
Element 6: Verify, Validate, and Document Risk Reduction
     ↓
Element 7: Accept Risk and Document
     ↓
Element 8: Manage Life-Cycle Risk
```
[src-mil-std-882e-2012 §4.3, Fig 1 p.9]

### 5.2 Risk Assessment Framework

**Severity Categories (Table I):**

| Category | Description | Criteria |
|---|---|---|
| 1 — Catastrophic | Death, permanent total disability, or ≥$10M loss |
| 2 — Critical | Permanent partial disability, hospitalization of 3+, or $1M-$10M loss |
| 3 — Marginal | Injury resulting in lost work days, or $100K-$1M loss |
| 4 — Negligible | Injury not resulting in lost work day, or <$100K loss |

**Probability Levels (Table II):**

| Level | Description | Individual Item | Fleet/Inventory |
|---|---|---|---|
| A — Frequent | Likely to occur often | Continuously experienced |
| B — Probable | Will occur several times | Will occur frequently |
| C — Occasional | Likely to occur sometime | Will occur several times |
| D — Remote | Unlikely but possible | Reasonably expected |
| E — Improbable | So unlikely, assumed may not occur | Unlikely but possible |
| F — Eliminated | Incapable of occurrence (hazard eliminated) | Incapable of occurrence |

**Risk Assessment Matrix (Table III):**
The matrix maps Severity × Probability to Risk Assessment Codes (RACs), yielding
four risk levels: High, Serious, Medium, Low.
[src-mil-std-882e-2012 §4.3.3 pp.10-12, Tables I-III]

### 5.3 Design Order of Precedence for Risk Mitigation

MIL-STD-882E §4.3.4 defines a mandatory precedence for addressing hazards:

1. **Eliminate hazards through design selection** — the most effective approach
2. **Reduce risk through design alternatives** — if elimination is not possible
3. **Incorporate safety devices** — engineering controls
4. **Provide warning devices** — alerts and annunciations
5. **Develop procedures and training** — least effective, last resort

This hierarchy is echoed in ISO 26262 (design change → safety mechanism → warning →
operational procedure) and is fundamental to all safety standards. The key principle:
**engineering solutions take precedence over procedural solutions.**
[src-mil-std-882e-2012 §4.3.4-4.3.5 pp.12-13]

### 5.4 Software Safety Assessment

MIL-STD-882E §4.4 defines a software-specific safety framework that complements
the general system safety process:

**Software Control Categories (Table IV):**
Four categories based on autonomy and fault tolerance:
- SCC-1: Autonomous — software has sole control
- SCC-2: Semi-autonomous — software provides commands, human has override
- SCC-3: Redundant fault-tolerant — software has redundant backup
- SCC-4: Influential — software provides information but does not directly control

**Software Safety Criticality Index (SwCI):**
The intersection of Software Control Category (SCC) and hazard severity produces
a Software Safety Criticality Index that determines the Level of Rigor (LOR) for
software safety analysis:

| | Catastrophic | Critical | Marginal | Negligible |
|---|---|---|---|---|
| SCC-1 (Autonomous) | SwCI 1 | SwCI 1 | SwCI 3 | SwCI 4 |
| SCC-2 (Semi-auto) | SwCI 1 | SwCI 2 | SwCI 3 | SwCI 4 |
| SCC-3 (Redundant) | SwCI 2 | SwCI 3 | SwCI 3 | SwCI 4 |
| SCC-4 (Influential) | SwCI 3 | SwCI 3 | SwCI 4 | SwCI 4 |

SwCI 1 requires the highest level of rigor; SwCI 4 the lowest.
[src-mil-std-882e-2012 §4.4 pp.14-17, Tables IV-VI]

### 5.5 Task 203: System Requirements Hazard Analysis (SRHA)

This is the most directly requirements-relevant task in MIL-STD-882E. Its purpose is
explicitly to "determine the design requirements to eliminate hazards or reduce the
associated risks for a system, to incorporate these requirements into the appropriate
system documentation, and to assess compliance."

The SRHA shall:
1. Determine system design requirements to eliminate or reduce hazards by
   analyzing applicable policies, regulations, standards, and identified hazards
2. Recommend appropriate system design requirements
3. Define verification and validation approaches for each design requirement
4. Incorporate approved design requirements into specifications and engineering
   documents (system, subsystem, HW/SW, interface specifications)
5. Assess compliance at design reviews (PDR, CDR, Software Specification Review)
6. Review test plans for verification of risk mitigation measures
[src-mil-std-882e-2012 Task 203, pp.49-50]

### 5.6 Task 208: Functional Hazard Analysis (FHA)

Added in MIL-STD-882E (not in MIL-STD-882D). Purpose: to identify and classify the
safety consequences of functional failure or malfunction. The FHA:
- Decomposes the system to the major component level
- Identifies functional descriptions and interfaces
- Identifies hazards associated with loss of function, degraded function, and
  out-of-time/out-of-sequence function
- Classifies severity and assigns Safety-Critical (SCF/SCI) or Safety-Related
  (SRF/SRI) designations
- Maps functions to HW/SW implementation (SCFs/SSSFs mapped to software
  design architecture prior to coding)
- Produces a list of requirements and constraints for the specifications
[src-mil-std-882e-2012 Task 208, pp.68-70]

---

## 6. Cross-Method Comparison

### 6.1 What Each Method Finds That Others Miss

| Finding Type | FTA | FMEA | STPA |
|---|---|---|---|
| Hardware failure combinations | ✓ | — | — |
| Individual component failure modes | — | ✓ | — |
| Failure probability calculations | ✓ | — | — |
| Single-point failures | ✓ | ✓ | — |
| Software logic errors | — | — | ✓ |
| Requirements defects | — | — | ✓ |
| Unsafe interactions (non-failure) | — | — | ✓ |
| Mode confusion / human error | — | — | ✓ |
| Timing/sequence hazards | Limited | — | ✓ |
| Common cause failures | ✓ (via CCA) | — | ✓ |
| Process model flaws | — | — | ✓ |
| Failure rate data for components | — | ✓ | — |

### 6.2 When to Use Which Method

| Lifecycle Phase | Recommended Methods | Rationale |
|---|---|---|
| Concept/early requirements | STPA + PHA | No detailed design yet; STPA works on abstract control structures; PHA provides initial risk ranking |
| Architecture/PSSA | STPA + qualitative FTA | Architecture defined enough for FTA; STPA identifies interaction hazards |
| Detailed design | FMEA + STPA refinement | Components defined enough for FMEA; STPA refined to lower-level controllers |
| Verification/SSA | Quantitative FTA + FMEA data | Need probability calculations for certification; FMEA provides failure rates |
| Modification/change | STPA delta analysis | Evaluate what the change affects in the control structure |

### 6.3 The Software Problem

Software is the critical dividing line between traditional and systems-theoretic methods.

FTA models software as an undeveloped event (diamond) because software does not have
a failure rate — it executes its logic identically every time. Software "fails" only in the
sense that its logic was wrong from the start (a design error) or its assumptions about
the environment no longer hold.

FMEA can enumerate software failure modes (wrong output, no output, late output) but
cannot identify WHY the software produces wrong output — that requires understanding
the control algorithm and process model, which is exactly what STPA's Step 4 does.

STPA treats software as a controller with a control algorithm and process model. It
systematically identifies how flawed algorithms, incorrect process models, and missing
feedback can lead to unsafe control actions. This is why STPA finds software-related
hazards that FTA and FMEA miss.
[src-leveson-stpa-handbook-2018 Ch.1 pp.4-5, Ch.2 pp.43-48]

---

## 7. Source List

### Primary sources (read from files in codex raw/)

1. **STPA Handbook** — Leveson, Nancy G. and Thomas, John P. "STPA Handbook."
   MIT Partnership for Systems Approaches to Safety and Security, March 2018.
   188 pages. Read pp. 1-71 (Chapters 1-3).
   Raw path: `raw/books/leveson-thomas-stpa-handbook.pdf`

2. **MIL-STD-882E** — Department of Defense. "Standard Practice: System Safety."
   MIL-STD-882E, 11 May 2012. 104 pages. Read pp. 1-83 (all sections through
   Task 210).
   Raw path: `raw/standards/mil-std-882e.pdf`

3. **Bosch FMEA Booklet** — Robert Bosch GmbH. "Failure Mode and Effects Analysis
   (FMEA)." Quality Management in the Bosch Group, Booklet No. 14, June 2012.
   40 pages (20 in main body). Read all 20 pages.
   Raw path: `raw/papers/bosch-fmea-booklet-no14.pdf`

4. **Peterson 2015** — Peterson, Eric M. "Application of SAE ARP4754A to Flight
   Critical Systems." NASA/CR-2015-218982, November 2015. 217 pages.
   Read pp. 44-57 (PASA/CMA tables), pp. 79-80 (FHA impact), pp. 89-96
   (validation/verification matrices).
   Raw path: `raw/papers/peterson-arp4754a-nasa-2015.pdf`

### Secondary sources (from Research 1, already documented)

5. ARP 4761 safety assessment process — via secondary web sources (Wikipedia,
   Akbulut Medium article, ALD Service). Process structure only; this document
   covers the analytical methods.

6. ISO 26262 Part 3 HARA and Part 4 TSC — via secondary web sources (Embitel,
   BYHON, SecuRESafe). Concepts only; paywalled primary.
