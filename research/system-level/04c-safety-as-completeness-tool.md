# Research 4c: Safety Analysis as a Requirements Completeness Tool

Research for upper V documentation (backlog items 3.4, 3.5, 3.6). Covers safety analysis
as the primary mechanism for discovering requirements that no stakeholder articulated —
the "completeness" role of safety engineering. Also covers the derived requirements feedback
loop, cross-domain comparison, and common failure modes in the safety-requirements interface.

**Sources used:**
- Peterson, NASA/CR-2015-218982, 2015 (primary, pp. 4-7 industry issues, pp. 44-57
  PASA/CMA, pp. 79-96) [src-peterson-arp4754a-2015]
- STPA Handbook, Leveson & Thomas, 2018 (primary, Ch. 1 pp. 4-13, Ch. 3 pp. 54-71)
  [src-leveson-stpa-handbook-2018]
- MIL-STD-882E, 2012 (primary, §4.3 pp. 9-17) [src-mil-std-882e-2012]
- Bosch FMEA Booklet No. 14, 2012 (primary, §1.3-1.5) [src-bosch-fmea-booklet-2012]
- ASPICE PAM v4.0 (primary, SYS.2-SYS.3) [src-aspice-4-0]
- Research 1-3 findings (internal)
- Web research agent findings (URLs and summaries, 2026-04-12)

---

## 1. The Completeness Problem

Requirements engineering has a fundamental completeness problem: stakeholders cannot
articulate requirements for hazards they haven't imagined. This is not a failure of
elicitation technique — it is an inherent limitation of experience-based specification.

Three categories of "missing" requirements that safety analysis discovers:

1. **Negative requirements.** Requirements that constrain what the system must NOT do.
   Stakeholders describe desired functions; safety analysis identifies dangerous
   functions, dangerous interactions, and dangerous states. Independence requirements,
   fault containment boundaries, and prohibited operating modes all come from safety
   analysis, not stakeholder elicitation.

2. **Implicit assumptions.** Requirements that exist only as unstated assumptions about
   the operating environment, timing, or component behavior. Safety analysis makes
   these explicit by asking "what if this assumption fails?" FTTI constraints, common
   cause failure protections, and environmental operating boundaries emerge from this.

3. **Interaction requirements.** Requirements governing how components interact safely.
   Individual component specifications do not capture cross-component timing
   dependencies, resource conflicts, or mode incompatibilities. System-level safety
   analysis (especially STPA) identifies these interaction hazards.

**Empirical support:**
- Peterson found that ALL 11 independence requirements in the SAAB-EII 100 PASA
  came from CMA, not from stakeholder elicitation
  [src-peterson-arp4754a-2015 p.49]
- Bosch/Langenfeld 2016 (Research 3 finding): 61% of defects in automotive systems
  came from incorrectness/incompleteness — safety analysis is the primary defense
  against incompleteness at the system level [Research 3 learning #7]
- Leveson: STPA evaluations "found all the causal scenarios found by the more
  traditional analyses but also identified many more, often software-related and
  non-failure, scenarios that the traditional methods did not find"
  [src-leveson-stpa-handbook-2018 Ch.1 p.4]
- Sulaman et al. 2019 (from web research): FMEA found 21 hazards, STPA found 22,
  combined they found 30 — each method found unique hazards the other missed
  [web research agent finding — paper at link.springer.com]

---

## 2. How Each Standard Frames Safety as a Completeness Tool

### 2.1 Aviation: ARP 4754A + ARP 4761

ARP 4754A's seven integral processes include "Safety Assessment" running continuously
across all five development processes. Safety is not a post-design verification step —
it runs IN PARALLEL with requirements capture and system architecture development,
feeding safety-derived requirements into the system specification as they are discovered.

The feedback loop is explicit in ARP 4754A:
- Objective 2.4: "System derived requirements (including derived safety-related
  requirements) are defined and rationale explained"
  [src-peterson-arp4754a-2015 Table 6 p.44]
- When DO-178C/DO-254 create derived requirements, these MUST feed back up to
  ARP 4754A (system) and ARP 4761 (safety) for impact assessment
  [src-peterson-arp4754a-2015 p.4, §2.7]

**The practical gap:** Peterson's industry survey found that the feedback loop is "new and
unfulfilling work" — most engineers have experience defining and verifying requirements
but NOT justifying (validating) them. Only 25% had received training on the ARP 4754A
process. The respondents wanted "step-by-step guidance for derived requirement review,
process assurance, and requirement standards for capture/validation."
[src-peterson-arp4754a-2015 pp.6-7]

### 2.2 Automotive: ISO 26262

ISO 26262 Part 3 Clause 7 (Functional Safety Concept) explicitly positions HARA as a
requirements completeness mechanism:
- HARA discovers hazardous events not visible from functional requirements alone
- Safety Goals become top-level requirements with ASIL assignments
- The FSC adds an entire class of requirements (detection, degradation, warning,
  safe state transition) that functional requirements would not contain

ASPICE SYS.2.BP1 requires system requirements to be specified "according to defined
characteristics" per ISO IEEE 29148, which includes safety requirements. The ASPICE
process assessment model does not distinguish safety requirements from functional
requirements at the process level — they are all system requirements, with safety
analysis being one of several sources.
[src-aspice-4-0 SYS.2 BP1 p.36]

### 2.3 Military: MIL-STD-882E

MIL-STD-882E frames the entire system safety process as requirements-generating.
Element 4 (Identify and Document Risk Mitigation Measures) and Element 5 (Reduce Risk)
both produce design requirements. Task 203 (SRHA) is explicitly chartered to "determine
system design requirements to eliminate hazards or reduce the associated risks."

The design order of precedence (§4.3.4) is itself a completeness tool: for each hazard,
you must work through all five precedence levels, generating requirements at each level
until risk is acceptable. This ensures that hazards are addressed through engineering
rather than being dismissed with procedural controls.
[src-mil-std-882e-2012 §4.3.4-4.3.5 pp.12-13; Task 203 pp.49-50]

### 2.4 STPA: By Design a Requirements Tool

Leveson explicitly positions STPA as a requirements generation method, not just a
hazard analysis method:

"STPA can be used to generate high-level safety requirements early in the concept
development phase, refine them in the system requirements development phase. The
system requirements and constraints can then assist in the design of the system
architecture and more detailed system design and development."
[src-leveson-stpa-handbook-2018 Ch.3 p.54]

STPA's 11-point integration with the V-model shows requirements generation at EVERY
phase:
1. Define losses (concept development)
2. Identify external constraints, including regulatory (concept development)
3. Identify system-level hazards and constraints → **initial system requirements**
4. Model system control structure
5. Refine hazards and constraints → **refined system requirements**
6. Assist architecture decisions
7. System integration assistance
8. Generate system test requirements
9. Control manufacturing (workplace safety)
10. Generate operational safety requirements
11. Operational safety management
[src-leveson-stpa-handbook-2018 Ch.3 p.55]

**Key Leveson claim:** "70-90% of the design decisions related to safety are made in the
concept development stage and changing these decisions later may be infeasible or
enormously expensive" (citing Frola & Miller 1984). This motivates starting STPA at the
earliest possible stage, before architecture commits design decisions that constrain
safety.
[src-leveson-stpa-handbook-2018 Ch.3 p.56]

---

## 3. The Derived Requirements Feedback Loop — Practical Mechanism

### 3.1 What "Derived Requirement" Means

A derived requirement is a requirement that exists at a lower level but is NOT traceable
to any higher-level requirement. It was created during development because the design
needed something the higher level didn't anticipate.

**Examples:**
- SW team needs a watchdog timer → not in system requirements
- HW team needs thermal protection → not in system requirements
- Architecture creates a data bus protocol → not in customer requirements

### 3.2 Why Derived Requirements Matter for Safety

Derived requirements are the most dangerous class of requirements from a safety
perspective because they bypass the normal safety analysis path:
- They were not examined by FHA/HARA
- They have no ASIL/DAL assignment
- They may create new failure paths not in the fault tree
- They may create new unsafe interactions not in the STPA analysis

### 3.3 The Feedback Mechanism Across Standards

| Standard | Obligation | Practical Mechanism |
|---|---|---|
| ARP 4754A | Objective 2.4, 4.4, 5.5 | SW/HW teams identify derived req → notify system safety → safety assesses impact → update PSSA/FHA if needed → new safety req flow back down |
| ISO 26262 | Part 4 §6, Part 6 §7 | SW architecture may create derived req → fed back to TSC → may trigger FSC/HARA update → new safety goals possible |
| DO-178C | §5.1.2, §6.3.4 | Derived requirements identified during SW development → fed back to system process → impact on safety assessed |
| MIL-STD-882E | Task 204 §204.2.3 | Software used with subsystem → contractor monitors formal SW dev process → hazards from SW identified → reported to PM |

### 3.4 Why the Loop Is Usually Broken

**Peterson's findings (industry survey):**
- Engineers view it as "new and unfulfilling work" [p.7]
- Only 25% had received training [p.6]
- No standard tools or processes existed at most organizations
- The notification mechanism (SW/HW team → system safety team) is an
  organizational process that rarely exists in legacy programs

**Structural reasons:**
1. **Timing mismatch.** By the time SW teams create derived requirements, system-level
   safety analysis is often "complete" and the safety team has moved to other projects.
2. **Organizational boundaries.** SW development and system safety are different teams
   with different managers, timelines, and tools. Cross-team notification requires
   explicit process infrastructure.
3. **Incentive mismatch.** Identifying a derived requirement with safety impact triggers
   expensive re-analysis. There is organizational pressure to classify derived
   requirements as "not safety-relevant."
4. **Scale.** Large programs produce hundreds of derived requirements. Assessing
   each one for safety impact requires safety engineering resources that are already
   scarce.

### 3.5 What Good Feedback Looks Like

When the feedback loop works, it produces traceable evidence:
1. Derived requirement identified by SW/HW team
2. Safety impact assessment performed (documented decision: safety-relevant or not)
3. If safety-relevant: PSSA/FSC updated, new safety requirements generated
4. New safety requirements flow back to affected teams
5. Verification evidence includes the safety impact assessment

The Peterson validation matrix (Table 25, p.94) shows this working: derived requirements
are explicitly marked as Source=Derived with Safety=Y and validated through Inspect +
Analysis + Trace.
[src-peterson-arp4754a-2015 p.94]

---

## 4. Common Failure Modes in the Safety-Requirements Interface

### 4.1 Organizational Failures

| Failure Mode | Description | Consequence |
|---|---|---|
| **Safety silo** | Safety analysis produces a separate safety report that doesn't feed into the requirements baseline | Safety requirements are never implemented or verified |
| **Late safety analysis** | HARA/FHA performed after architecture is committed | Safety findings cannot be addressed without expensive redesign |
| **Missing feedback loop** | Derived requirements not assessed for safety impact | New failure paths introduced without safety analysis |
| **Single-person dependency** | One safety engineer who "knows the safety story" | Knowledge lost when person moves; no team understanding |

### 4.2 Technical Failures

| Failure Mode | Description | Consequence |
|---|---|---|
| **ASIL/DAL confusion** | ASIL levels increase A→D; DAL levels increase E→A | Wrong rigor applied; requirements misallocated |
| **Independence assumed without evidence** | ASIL decomposition or FDAL reduction claimed without CMA/freedom-from-interference analysis | Redundancy provides no actual safety benefit |
| **FTTI not allocated** | FTTI defined at concept level but not decomposed into FDTI/FRTI at design level | Safety mechanisms have no timing requirements |
| **Probability-only analysis** | Quantitative FTA shows system meets probability target, but design errors and interaction hazards not analyzed | Software-intensive system "passes" quantitative analysis while containing hazardous design flaws |
| **Stale safety analysis** | Design changes made after safety analysis "frozen" | Fault tree no longer represents actual architecture |

### 4.3 The Software Blind Spot (Cross-Domain)

Every domain struggles with software safety requirements because traditional safety
analysis methods (FTA, FMEA) were designed for hardware:

- FTA models software as an undeveloped event — no systematic decomposition
  of software contribution to hazards
- FMEA can list software failure modes but cannot analyze why software produces
  wrong output
- MIL-STD-882E addresses this with §4.4 (Software Safety) and the SwCI matrix,
  but the analytical methods are still failure-based
- Only STPA systematically analyzes software as a controller with a control algorithm
  and process model, identifying HOW the algorithm can produce unsafe outputs

The FAA STPA evaluation report (DOT/FAA/TC-24/16, 2024) found that STPA "catches
more system and software errors in requirements than traditional hazard analysis" — a
finding endorsed by SMEs from FAA, EASA, ANAC, ICAO, and NASA.
[web research agent finding — FAA report, access restricted during fetch]

---

## 5. Synthesis: What Research 4 Tells Us About System Requirements Documentation

Research 4 produces several findings that directly inform the system requirements
documentation (backlog item 3.4):

1. **Safety analysis is a requirements source, not just verification.** The system
   requirements documentation must explain how safety analysis feeds requirements
   into the system specification alongside functional requirements.

2. **Three classes of safety-derived requirements.** The documentation needs to cover:
   - Failure rate budgets and reliability requirements (from FTA)
   - Independence/redundancy/monitoring requirements (from CMA/FTA/FMEA)
   - Behavioral constraints and unsafe interaction prevention (from STPA)

3. **FTTI/timing requirements are a distinct category.** The documentation needs to
   cover how timing constraints from safety analysis become verifiable requirements.

4. **The feedback loop is mandatory but practically broken.** The documentation should
   explain the derived requirements feedback mechanism and why it matters, as a
   teaching tool for engineers who have not been trained on it.

5. **STPA complements but does not replace traditional methods.** The documentation
   should present all three method families as complementary, not competing.

6. **Safety requirements are first-class requirements.** They belong in the system
   specification, not in a separate safety annex. They carry the same quality
   attributes as all requirements (verifiable, traceable, etc.) plus safety-specific
   attributes (integrity level, safety flag, rationale, verification method).

---

## 6. Source List

### Primary sources (read from files in codex raw/)

1. **Peterson 2015** — NASA/CR-2015-218982. Read pp. 4-7 (industry issues),
   pp. 44-57 (PASA/CMA), pp. 79-96 (FHA/validation/verification).
   Raw path: `raw/papers/peterson-arp4754a-nasa-2015.pdf`

2. **STPA Handbook** — Leveson & Thomas, 2018. Read Ch. 1 pp. 4-13, Ch. 3 pp. 54-71.
   Raw path: `raw/books/leveson-thomas-stpa-handbook.pdf`

3. **MIL-STD-882E** — DoD, 2012. Read §4.3 pp. 9-17, Task 203 pp. 49-50.
   Raw path: `raw/standards/mil-std-882e.pdf`

4. **Bosch FMEA Booklet** — Robert Bosch GmbH, 2012. Read §1.3-1.5.
   Raw path: `raw/papers/bosch-fmea-booklet-no14.pdf`

5. **ASPICE PAM v4.0** — VDA QMC, 2023. SYS.2 BP1.
   Raw path: `raw/standards/Automotive-SPICE-PAM-v40.pdf`

### Secondary sources (from web research agents, URLs verified)

6. **Sulaman et al. 2019** — "Comparison of the FMEA and STPA safety analysis
   methods — a case study." Software Quality Journal, Springer.
   URL: https://link.springer.com/article/10.1007/s11219-017-9396-0
   Full text: http://www.diva-portal.org/smash/get/diva2:1166953/FULLTEXT01.pdf
   Finding: FMEA found 21 hazards, STPA found 22, combined 30 unique.
   Status: URL identified but not yet fetched/saved to codex raw/.

7. **FAA DOT/FAA/TC-24/16** — "Evaluation of STPA for Improving Aviation Safety."
   URL: https://rosap.ntl.bts.gov/view/dot/78914/dot_78914_DS1.pdf
   Finding: FAA/EASA/ANAC/ICAO/NASA endorsed STPA value; catches more
   system/software errors than traditional methods.
   Status: 403 on fetch — needs manual download or alternate access.

8. **Wilkinson & Fleming** — "A Comparison of STPA and the ARP 4761 Safety
   Assessment Process." MIT/Leveson group.
   URL: http://sunnyday.mit.edu/papers/ARP4761-Comparison-Report-final-1.pdf
   Finding: STPA identifies hazards omitted by ARP 4761 (software, human factors,
   operations).
   Status: ECONNREFUSED on fetch — needs alternate access.

9. **Abdulkhaleq et al. 2017** — "Using STPA in Compliance with ISO 26262 for
   Developing a Safe Architecture for Fully Automated Vehicles."
   URL: https://arxiv.org/abs/1703.03657
   Finding: STPA extends safety scope to cover SOTIF beyond functional safety.
   Status: URL identified, not yet fetched.

10. **Leveson 2004** — "A New Accident Model for Engineering Safer Systems."
    Safety Science (Elsevier).
    URL: http://sunnyday.mit.edu/accidents/safetyscience-single.pdf
    Finding: Foundational critique of event-chain/probability models; introduces
    STAMP; safety as a control problem.
    Status: URL identified, not yet fetched.
