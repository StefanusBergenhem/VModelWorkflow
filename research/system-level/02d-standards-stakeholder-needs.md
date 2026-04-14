# Research 2d: Standards — Stakeholder Needs Engineering (Compliance Frame)

Focused research on what standards specifically require for stakeholder/needs engineering.
This is the compliance frame for upper-V documentation, going deeper than Research 1's
system-level process overview.

**Sources used (all read from raw files in this session):**
- ASPICE PAM v4.0 [src-aspice-4-0] — pp. 34-42, directly from PDF
- Peterson 2015, NASA/CR-2015-218982 [src-peterson-arp4754a-2015] — pp. 1-8, 60-71, 83-84, directly from PDF
- INCOSE 42-Rule Guide (Reqi.io, 2026) [src-incose-42-rule-guide-reqi-2026] — raw article
- Research 1 [01-standards-system-level-processes.md] — for cross-reference and context
- Engineering codex wiki pages: std-aspice, std-iso26262 — for secondary synthesis

**Scope:** This document covers what each standard requires at the stakeholder/needs layer
specifically. Topics not covered here (and deferred to later research):
- The *craft* of writing good requirements (→ Research 3)
- Safety analysis methods in depth (→ Research 4)
- ISO/IEC/IEEE 29148:2018 full standard (paywalled; treated via ASPICE normative reference)
- INCOSE GtWR primary document (paywalled; treated via secondary article source)

---

## 1. ASPICE v4.0 SYS.1 — Requirements Elicitation (Deep Dive)

### 1.1 What SYS.1 Is and Isn't

SYS.1 is the ASPICE process that sits at the top of the left side of the system-level V.
It is about gathering, analyzing, and tracking what stakeholders need — before any
engineering transformation has occurred. SYS.2 (System Requirements Analysis) then takes
those stakeholder needs and transforms them into system requirements.

This distinction matters: **SYS.1 produces stakeholder requirements. SYS.2 produces
system requirements.** They are distinct artifacts with distinct traceability obligations
between them (SYS.2.BP5 mandates bidirectional traceability from system to stakeholder
requirements).

The PAM operates at the WHAT level — it defines goals and outcomes, not methods or
templates. [src-aspice-4-0 §3.3.3 p.27]

### 1.2 SYS.1 Process Purpose (Verbatim)

> "The purpose is to gather, analyze, and track evolving stakeholder needs and requirements
> throughout the lifecycle of the product and/or service to establish a set of agreed
> requirements."

[src-aspice-4-0 §4.3.1 p.34]

This is the ASPICE definition of what needs engineering is for. Three verbs are key:
**gather** (elicitation), **analyze** (understanding, disambiguation), **track** (change
management over lifecycle). The output is not just a list — it is a **set of agreed
requirements**, implying active stakeholder agreement, not just a documented list.

### 1.3 SYS.1 Process Outcomes (Verbatim)

Four outcomes are required for SYS.1:

1. Continuing communication with the stakeholder is established.
2. Stakeholder expectations are understood, and requirements are defined and agreed.
3. Stakeholder requirements changes arising from stakeholder needs are analyzed to enable
   associated risk assessment and impact management.
4. Determination of stakeholder requirements status is ensured for all affected parties.

[src-aspice-4-0 §4.3.1 p.34]

Outcome 1 is structural: a **communication channel** must exist, not just a one-time
elicitation. Outcome 2 requires both understanding AND formal agreement. Outcome 3
explicitly covers change management — stakeholder needs evolve, and the process must handle
this. Outcome 4 is about transparency: status must be knowable by all parties.

### 1.4 SYS.1 Base Practices — Complete Verbatim Text

All four base practices are from [src-aspice-4-0 §4.3.1 pp.34-35]:

**SYS.1.BP1: Obtain stakeholder expectations and requests.**
> "Obtain and define stakeholder expectations and requests through direct solicitation of
> stakeholder input, and through review of stakeholder business proposals (where relevant)
> and other documents containing inputs to stakeholder requirements, and consideration of
> the target operating and hardware environment."
>
> *Note 1: Documenting the stakeholder, or the source of a stakeholder requirement, supports
> stakeholder requirements agreement and change analysis (see BP2 and BP3).*

This BP requires **active elicitation** (direct solicitation, document review) and
environmental awareness. The note introduces the concept of **requirement attribution** —
recording who stated what requirement. This is not just good practice; it supports the
agreement and change management BPs.

**SYS.1.BP2: Agree on requirements.**
> "Formalize the stakeholder's expectations and requests into requirements. Reach a common
> understanding of the set of stakeholder requirements among affected parties by obtaining
> an explicit agreement from all affected parties."
>
> *Note 2: Examples of affected parties are customers, suppliers, design partners, joint
> venture partners, or outsourcing parties.*
>
> *Note 3: The agreed stakeholder requirements may be based on feasibility studies and/or
> cost and schedule impact analysis.*

This BP is critical: agreement must be **explicit**. Implicit acceptance or silence is not
compliant. The scope of "affected parties" is broad — it includes the supply chain, not
just the primary customer. The feasibility caveat in Note 3 acknowledges that some needs
cannot be realized as stated; agreement may require negotiation informed by feasibility.

**SYS.1.BP3: Analyze stakeholder requirements changes.**
> "Analyze all changes made to the stakeholder requirements against the agreed stakeholder
> requirements. Assess the impact and risks, and initiate appropriate change control and
> mitigation actions."
>
> *Note 4: Requirements changes may arise from different sources as for instance changing
> technology, stakeholder needs, or legal constraints.*
>
> *Note 5: Refer to SUP.10 Change Request Management, if required.*

Note 4 identifies three change drivers: technology evolution, stakeholder evolution, and
regulatory/legal constraints. This is the sources of unstated requirements — legal
constraints are a stakeholder class that may not have directly stated their needs.

**SYS.1.BP4: Communicate requirements status.**
> "Ensure all affected parties can be aware of the status and disposition of their
> requirements including changes and can communicate necessary information and data."

This BP closes the communication loop. All affected parties must be able to *track* status,
not just receive a document. The active phrasing "can be aware" and "can communicate"
implies infrastructure for ongoing status visibility.

### 1.5 SYS.1 Output Information Items

| Item ID | Name | Linked Outcomes |
|---------|------|-----------------|
| 15-51 | Analysis Results | Outcome 3 |
| 13-52 | Communication Evidence | Outcomes 1, 2 |
| 17-00 | Requirement | Outcome 2 |
| 17-54 | Requirement Attribute | Outcomes 2, 3, 4 |

[src-aspice-4-0 §4.3.1 p.35]

The **Requirement Attribute** item (17-54) is particularly significant. It is linked to
outcomes 2, 3, and 4 — the agreement, change analysis, and status tracking outcomes. This
means requirements must carry attributes beyond the text (source, status, change history,
priority) for a SYS.1-compliant process. The PAM does not prescribe what attributes, but
their existence is an assessment indicator.

### 1.6 What SYS.1 Does NOT Require (But SYS.2 Does)

SYS.1 does not require:
- Structuring or prioritizing requirements (→ SYS.2.BP2)
- Specifying requirements according to defined characteristics like verifiability (→ SYS.2.BP1)
- Bidirectional traceability to lower-level requirements (→ SYS.2.BP5)
- Technical feasibility analysis (→ SYS.2.BP3)

SYS.1 requirements may be expressed in the stakeholder's own vocabulary and format. The
transformation to well-formed, verifiable system requirements is SYS.2's job.

### 1.7 The "Unstated Requirements Necessary for Intended Use" Concept

The ASPICE PAM v4.0 does not use the exact phrase "requirements not stated by the
stakeholder but necessary for specified and intended use" in SYS.1. However, this concept
is handled by the interplay of several mechanisms:

1. **BP1's environmental consideration** — "consideration of the target operating and
   hardware environment" captures needs that arise from context, not just explicit asks.

2. **BP3 Note 4's legal constraint driver** — regulatory requirements are implicit
   stakeholder needs that must be captured even if no stakeholder explicitly stated them.

3. **SYS.2.BP1's reference to ISO/IEC/IEEE 29148** — when system requirements are
   specified, 29148 provides the framework for completeness criteria including implied needs.

The ISO/IEC/IEEE 29148:2018 standard (explicitly cited in ASPICE v4.0 Annex D and
referenced in SYS.2.BP1) is where this concept is formally defined. 29148 defines
**stakeholder requirements** as including both stated and implied needs, and the
**Stakeholder Requirements Specification (StRS)** must capture both. [src-aspice-4-0 Annex D
p.153; SYS.2.BP1 Note 1 p.36; Note: 29148 content from ASPICE reference; 29148 itself is
paywalled and was not read directly — claims about 29148 are [unverified] except where
ASPICE directly quotes or references them]

---

## 2. ASPICE SYS.1 → SYS.2 Relationship

### 2.1 The Transformation

SYS.2 takes stakeholder requirements as input and produces system requirements. The key
transformation obligations are captured in SYS.2.BP1 [src-aspice-4-0 §4.3.2 p.36]:

> "Use the stakeholder requirements to identify and document the functional and
> non-functional requirements for the system according to defined characteristics for
> requirements."
>
> *Note 1: Characteristics of requirements are defined in standards such as ISO IEEE 29148,
> ISO 26262-8:2018, or the INCOSE Guide For Writing Requirements.*
>
> *Note 2: Examples of defined characteristics of requirements shared by technical standards
> are verifiability (i.e., verification criteria being inherent in the requirements text),
> unambiguity/comprehensibility, freedom from design and implementation, and not
> contradicting any other requirement.*

This is the explicit normative reference to the "defined characteristics" framework. By
naming ISO/IEC/IEEE 29148, ISO 26262-8, and INCOSE GtWR, ASPICE endorses these as
acceptable frameworks for what makes a good requirement.

### 2.2 The Critical Traceability Note

SYS.2.BP5 contains a note that reveals an important design decision in the ASPICE framework
[src-aspice-4-0 §4.3.2 p.37]:

> *Note 7: Bidirectional traceability supports consistency, facilitates impact analyses of
> change requests, and supports the demonstration of coverage of stakeholder requirements.
> Traceability alone, e.g., the existence of links, does not necessarily mean that the
> information is consistent with each other.*
>
> *Note 8: There may be non-functional stakeholder requirements that the system requirements
> do not trace to. Examples are process requirements. Such stakeholder requirements are
> still subject to verification.*

Note 8 is architecturally significant: not all stakeholder requirements need to be
transformed into system requirements. Process requirements (e.g., "the project shall use
ASPICE Level 2") are stakeholder requirements that operate at the process level and do not
decompose into system requirements. They are still valid stakeholder needs and still require
verification — but the verification path is different.

### 2.3 SYS.2 Process Purpose and Outcomes (Summary)

Purpose: "To establish a structured and analyzed set of system requirements consistent with
the stakeholder requirements." [src-aspice-4-0 §4.3.2 p.36]

Six outcomes [src-aspice-4-0 §4.3.2 p.36]:
1. System requirements are specified.
2. System requirements are structured and prioritized.
3. System requirements are analyzed for correctness and technical feasibility.
4. The impact of system requirements on the operating environment is analyzed.
5. Consistency and bidirectional traceability established between system and stakeholder
   requirements.
6. System requirements are agreed and communicated to all affected parties.

The structural completeness test is outcome 5 — complete bidirectional traceability between
both levels with evidence of consistency.

---

## 3. ISO 26262 Parts 3-4 — Concept Phase Stakeholder Mapping

### 3.1 What ISO 26262 Calls Stakeholder Needs

ISO 26262 does not have a process called "stakeholder needs engineering." Instead, the
concept phase (Part 3) operates with these constructs:

**Item Definition (Part 3, Clause 5)** — This is the functional description at the vehicle
level before any design. It captures:
- Functional description of the item (what it does at the vehicle level)
- Operational and environmental constraints
- Interactions with other items and elements
- Operating scenarios that impact functionality
- Known hazards from similar items

The Item Definition is functionally equivalent to a stakeholder needs document at the
vehicle level. It answers "what does this thing need to do and in what context" before any
design has occurred. [Research 1, §4.1; secondary sources: Embitel HARA guide, SecuRESafe
ISO 26262 Ed.3 — these are secondary; ISO 26262 itself is paywalled and not directly read]

**The Implicit Stakeholder in ISO 26262** is the vehicle occupant, road user, and society —
not an enterprise customer. Safety goals are derived from HARA (Hazard Analysis and Risk
Assessment), which systematically identifies what failure modes are hazardous. This is a
structured form of capturing what society requires from the item even though "society" never
directly stated requirements.

### 3.2 HARA as Implicit Stakeholder Needs Capture

The HARA (Part 3, Clause 6) is ISO 26262's primary mechanism for deriving needs that were
never explicitly stated by anyone. The process [Research 1, §4.1; secondary sources]:

1. Identify vehicle-level hazardous events caused by malfunctioning behavior
2. Classify three risk parameters per hazardous event:
   - **Severity (S0-S3):** S0 = no injuries → S3 = fatal/life-threatening
   - **Exposure (E0-E4):** probability of encountering the hazard scenario
   - **Controllability (C0-C3):** ability of driver/bystander to avoid harm
3. Combine S × E × C to determine ASIL (A through D, or QM = no safety requirement)

This is not stakeholder elicitation in the traditional sense — it is a systematic derivation
of what safety requirements *must* exist for the item to be acceptable in its operational
context. The "stakeholder" is implicitly the regulatory framework (ISO 26262 itself) and
societal expectations for road safety.

### 3.3 Safety Goals as Top-Level Requirements

Safety goals (Part 3, Clause 6) are the output of HARA. They are:
- Expressed at vehicle/functional level
- Not implementation-specified
- Each assigned an ASIL
- The top-level safety requirements from which all downstream safety requirements are derived

The constraint that safety goals must be "implementation-independent" directly parallels the
requirement quality criterion of "freedom from design and implementation" in ASPICE/29148.

### 3.4 Functions at Vehicle Level — The ATA Chapter Parallel

In aviation (ARP 4754A), aircraft-level functions are enumerated explicitly (often by ATA
chapter: autopilot/autoflight ATA22, communications ATA23, displays ATA31, etc.).
[src-peterson-arp4754a-2015 Appendix A p.16, 20, 40-41]

ISO 26262 uses the equivalent concept with "items" — an item is a system or group of
systems implementing a function at the vehicle level (e.g., ABS, EPS, BMS). These
function-level items are the automotive equivalent of aircraft functions in ARP 4754A.

The critical difference: in aviation, the aircraft OEM (or the certification applicant)
explicitly enumerates all functions as a first step of the development process. In
automotive ISO 26262, the item boundary is defined by the scope of the HARA, and HARA
drives what constitutes an "item."

---

## 4. ARP 4754A Stakeholder/Certification Aspects

### 4.1 Who the Stakeholders Are in Aviation

ARP 4754A operates in a regulatory context where the stakeholders are:

1. **The certification applicant** (aircraft manufacturer or system developer) — primary
   engineering stakeholder
2. **The certification authority** (FAA/EASA) — regulatory stakeholder whose requirements
   are expressed through regulations (14 CFR Part 25) and advisory circulars
3. **The operator/airline** — operational stakeholder
4. **The end user (pilot/crew)** — usability/operational requirements
5. **Suppliers/subcontractors** — technical stakeholders in the supply chain

The certification authority is a stakeholder who has stated requirements (via regulation and
advisory circulars). The DER (Designated Engineering Representative) or ODA (Organization
Designation Authorization) acts as the certification authority's representative in the
development process. [src-peterson-arp4754a-2015 §1 pp.1-2; §5 p.6]

### 4.2 Certification Basis as Stakeholder Requirements

The Project Specific Certification Plan (PSCP) documents the certification basis — the
specific regulatory requirements that apply to the item being developed. In practice:

- The PSCP maps aircraft functions to applicable regulations
- Compliance methods (analysis, test, inspection, similarity, service experience) are defined
  per regulation
- The DER/ODA approves the compliance approach

The certification basis is a formalized set of stakeholder requirements from the regulatory
stakeholder. It drives what must be demonstrated in verification. [src-peterson-arp4754a-2015
Appendix A.2 PSCP200 pp.74-81]

The example PSCP200 for SAAB-EII 200 explicitly maps compliance to:
- ARP4754A at assigned FDAL (for IMA avionic system development)
- DO-178B at assigned IDALs (for airborne software)
- DO-254 at assigned IDALs (for airborne hardware)
- ARP4761 (for safety assessments)
[src-peterson-arp4754a-2015 p.81]

### 4.3 Function-Level Elicitation: The ATA Function Framework

ARP 4754A's "aircraft function development" process starts by enumerating all functions an
aircraft must perform. For a complex avionics system (IMA), these functions map to ATA
chapters and include explicit failure condition classification.

The example SAAB-EII 100 system has these avionic functions with assigned FDALs:
[src-peterson-arp4754a-2015 Table 5 p.41, Table 7 pp.44-46, PASA Table 7 p.48]

| Function | ATA Chapter | Most Severe FC | FDAL |
|----------|-------------|----------------|------|
| Autopilot/Autoflight | ATA22 | Catastrophic | A |
| Communications | ATA23 | Catastrophic | A |
| Displays | ATA31 | Catastrophic | A |
| Navigation/Flight Management | ATA34 | Hazardous | B |
| Maintenance | ATA45 | Catastrophic | A (partitioned) |

This is stakeholder needs translated into function-level requirements with integrity levels.
The "stakeholder" for FDAL A functions is the certification authority's safety requirements
(10⁻⁹ probability per flight hour for catastrophic failures).

### 4.4 Requirements Capture — The Engineering Judgment Dependency

The Peterson study identifies requirements capture as one of the three key engineering
judgment areas in ARP 4754A (along with requirements validation and FDAL/IDAL assignment):

> "In general, the key engineering use areas in ARP4754A include planning, requirements
> capture and requirements validation. The requirement management objectives rely the most
> on engineering judgment. The generation of acceptable, clear, concise requirement text
> relies on experience and engineering judgment."

[src-peterson-arp4754a-2015 §4 p.4, §5 (Policy Issues Summary) p.7]

The dependency on engineering judgment is structural — ARP 4754A provides objectives and
indicates what must be demonstrated, but the *how* of writing good requirements relies on
practitioner skill. This is the gap that standards like INCOSE GtWR and 29148 were created
to fill.

### 4.5 Requirements Validation — The Systematic Problematic Area

Requirements **validation** (are these the right requirements?) is explicitly called out by
Peterson as a problematic practice area. The key findings:

1. **Two methods minimum:** The ARP implies a minimum of two validation methods are
   recommended. Methods include: Traceability, Analysis (Modeling), Test, Similarity,
   Inspection (engineering review). [src-peterson-arp4754a-2015 Appendix A, SDP100 §5.2.1 p.68]

2. **Unfamiliar to most engineers:** "Most design engineers have experience defining and
   verifying requirements but NOT justifying (validating) their requirement set. This
   activity is viewed as being new and unfulfilling work." [src-peterson-arp4754a-2015 §5 p.7]

3. **Validation Matrix:** The primary artifact is a validation matrix tracking each
   requirement against: safety flag, requirement source (Parent ID, Derived, Assumption),
   validation methods applied (Inspect, Analysis, Similarity, Test, Trace), validation
   artifact reference, and validation result (Y/N). [src-peterson-arp4754a-2015 Table 18 p.69]

4. **Assumptions must be validated:** The validation process explicitly includes evaluation
   of assumptions made during requirements capture. Each assumption must be: (a) explicitly
   stated, (b) appropriately disseminated, (c) justified by supporting data.
   [src-peterson-arp4754a-2015 Appendix A, SDP100 §5.2 p.67]

The validation matrix structure (Table 18, p.69):

| Column | Purpose |
|--------|---------|
| Unique ID | Stable requirement identifier |
| Text (Requirement or Assumption) | Full requirement text or assumption statement |
| Safety (Y/N) | Safety-related flag |
| Requirement Source | Parent Req ID / Derived / Assumption |
| Validation Methods | Inspect / Analysis / Similarity / Test / Trace (multiple may apply) |
| Validation Artifact Reference | Document proving validation was performed |
| Reqt Valid (Y/N) | Outcome: has this requirement been validated |

The "Derived" source tag is significant: derived requirements (requirements not traceable to
a higher-level requirement) require additional scrutiny and must flow back up to the
aircraft/system level for safety impact assessment.

### 4.6 Validation vs Verification — Explicit ARP 4754A Distinction

| Aspect | Validation | Verification |
|--------|-----------|--------------|
| Question | "Are these the right requirements?" | "Does the implementation satisfy the requirements?" |
| Timing | During/after requirements capture | After implementation |
| Methods | Traceability, Analysis, Test, Similarity, Inspection | Test, Analysis, Service Experience, Inspection |
| Who | Experienced engineers (judgment-heavy) | Test engineers (evidence-heavy) |
| Primary artifact | Validation Matrix | Verification Matrix |

[src-peterson-arp4754a-2015 Appendix A, SDP100 §5.2 and §5.3 pp.67-71]

### 4.7 Requirements Capture Attributes (ARP 4754A)

The example Avionic Development Plan (ASDP100) specifies that baseline requirements must
include [src-peterson-arp4754a-2015 Appendix A, SDP100 §5.1 p.64]:

- Unique requirement identifier
- Requirement text
- Rationale (reason for having the requirement, if derived)
- Parent trace linkage capability
- Safety related attribute

This is a concrete implementation of what "requirement attributes" means in practice — the
same concept captured abstractly in ASPICE output item 17-54 (Requirement Attribute).

---

## 5. ISO/IEC/IEEE 29148:2018 — Requirements Engineering Standard

**Note:** 29148 is a paywalled standard and was not directly read in this session. The
following content is derived from ASPICE v4.0's normative references (which cite 29148
directly and quote some of its terminology) and from the secondary seed source. Claims are
marked [unverified against 29148 primary] where they depend on secondary sources beyond
ASPICE's direct quotation.

### 5.1 ASPICE's Normative Reference to 29148

ASPICE v4.0 explicitly cites ISO/IEC/IEEE 29148:2018 in:
- Annex D (normative references, p.153) — as a reference standard
- SYS.2.BP1 Note 1 (p.36) — as one of three acceptable frameworks for "defined
  characteristics" of requirements

This makes 29148 a normative backstop for what "good requirements" means in an ASPICE
context. When SYS.2.BP1 says requirements should have "verifiability," "unambiguity/
comprehensibility," and "freedom from design and implementation" as characteristics, it is
drawing from the 29148 / INCOSE vocabulary.

### 5.2 Key 29148 Concepts Referenced by ASPICE

**Stakeholder Requirements Specification (StRS)** [unverified — ASPICE references 29148 as
defining this concept]: The output artifact capturing stakeholder needs, including both
stated and implied needs, at the level of the problem rather than the solution.

**System Requirements Specification (SyRS)** [unverified]: The system-level equivalent,
derived from the StRS, structured for engineering use with explicit traceability.

**Concept of Operations (ConOps)** [unverified]: A document describing the system from the
user perspective, covering operational scenarios, interactions, and environment. Often
serves as the basis for the StRS.

### 5.3 Requirements Characteristics per 29148 (via ASPICE and INCOSE references)

SYS.2.BP1 Note 2 identifies these characteristics as examples of "defined characteristics
shared by technical standards":

- **Verifiability** — verification criteria are inherent in the requirements text (i.e.,
  you can tell how to check it)
- **Unambiguity/Comprehensibility** — one interpretation possible, understandable to all
  affected parties
- **Freedom from design and implementation** — the requirement states what, not how
- **Non-contradiction** — does not conflict with any other requirement

[src-aspice-4-0 SYS.2.BP1 Note 2 p.36]

These four are the characteristics that transform stakeholder needs (which may be vague,
solution-prescriptive, or ambiguous) into proper system requirements.

---

## 6. INCOSE Guide to Writing Requirements — Applicable Quality Criteria at the Needs Level

**Note:** The primary INCOSE GtWR is paywalled. The following is based on the secondary
article [src-incose-42-rule-guide-reqi-2026] which summarizes the 42 rules derived from the
GtWR.

### 6.1 Which Rules Apply at the Stakeholder Needs Level vs. System Requirements Level

Not all 42 rules apply equally at the stakeholder needs level. The following table
identifies applicability:

| Rule Category | Needs Level Applicability | Notes |
|---------------|---------------------------|-------|
| Accuracy (R1-R9) | HIGH — especially R7 (vague terms), R8 (escape clauses) | Vague needs produce vague requirements |
| Concision (R10-R11) | MEDIUM — needs can be prose-like | More relaxed than system requirements |
| Non-Ambiguity (R12-R17) | HIGH | Essential at any level |
| Singularity (R18-R23) | MEDIUM | Complex needs may still be bundled |
| Completeness (R24-R25) | HIGH | Missing needs propagate as gaps |
| Realism (R26) | HIGH — especially for early needs | Stakeholders often state impossible absolutes |
| Conditions (R27-R28) | HIGH | Context/scenario is crucial at needs level |
| Uniqueness (R29-R30) | HIGH | Duplicate needs cause confusion in decomposition |
| Abstraction (R31) | HIGH | Needs must not prescribe solutions |
| Quantifiers (R32-R35) | MEDIUM — needs may be less quantified | Engineering precision is a SYS.2 job |
| Uniformity (R36-R40) | HIGH | Consistent terminology across needs is critical |
| Modularity (R41-R42) | HIGH | Structure enables traceability |

[Synthesis from src-incose-42-rule-guide-reqi-2026; criteria judgment is [synthesis]]

### 6.2 The Critical Criteria for Needs-Level Quality

Three criteria that most impact quality when transitioning from needs to system requirements:

**Verifiability (or ability to be validated):** If a stakeholder need cannot be validated
(confirmed as correct, complete, and representative), it should not be baselined. The
INCOSE framework distinguishes "verifiable" (for requirements, testable) from "able to be
validated" (for needs, confirmable as representing actual stakeholder intent).

**Solution-free (R31):** Stakeholder needs that prescribe solutions constrain the solution
space unnecessarily and create design-implementation coupling from the top of the V.
Example: "The system shall use GPS for position tracking" is a solution prescription; "The
system shall determine vehicle position with accuracy ≤5m" is a solution-free need.
[src-incose-42-rule-guide-reqi-2026 §Abstraction Rules]

**Freedom from vague language (R7, R8, R9):** Needs expressed with words like "adequate,"
"reasonable," "as required," "where possible" cannot be agreed upon, cannot be traced to
verifiable requirements, and cannot support change impact analysis. These words must be
replaced with measurable criteria before stakeholder agreement. [src-incose-42-rule-guide-reqi-2026 §Accuracy Rules]

### 6.3 Active Voice and Ownership

Rule R2 (Active Voice) is particularly important at the needs level because it forces
explicit identification of the responsible entity — exactly the concept ASPICE SYS.1.BP1
Note 1 identifies as documenting "the stakeholder, or the source of a stakeholder
requirement." Passive voice conceals ownership; active voice requires it.

> "Data shall be encrypted" — passive, who requires this?
> "The Security_Module shall encrypt all transmitted data" — active, clear ownership

[src-incose-42-rule-guide-reqi-2026 §Accuracy Rules R2]

---

## 7. Cross-Standard Comparison: Stakeholder Needs Engineering Requirements

| Aspect | ASPICE v4.0 (SYS.1) | ISO 26262 Part 3 | ARP 4754A | ISO/IEC/IEEE 29148 |
|--------|---------------------|------------------|-----------|--------------------|
| **Stakeholder Identification** | Explicit: customers, suppliers, design partners, outsourcing parties, joint venture partners (SYS.1.BP2 Note 2) | Implicit: vehicle occupant, road user, society via HARA. Regulatory authority implicit in ASIL assignment | Explicit: certification authority, operator, crew, suppliers. DER/ODA as regulatory representative | Explicit: multiple stakeholder classes with structured elicitation [unverified] |
| **Needs Capture** | BP1: Direct solicitation + document review + environmental consideration. Source attribution required | Item Definition (Cl.5): functional description + operational scenarios + known hazards. HARA supplements via systematic hazard identification | Aircraft function enumeration by ATA chapter + PASA/SFHA for safety-driven functions. PSCP for regulatory requirements | ConOps + StRS [unverified] |
| **Needs Validation** | SYS.1.BP2: Explicit agreement from all affected parties required. BP3: Impact analysis of changes | Safety goals validated via SSA; functional safety concept validated against safety goals | Explicit validation process: min. 2 methods recommended (Traceability, Analysis, Similarity, Test, Inspection). Validation Matrix artifact | StRS validation [unverified] |
| **Needs-to-Requirements Traceability** | SYS.2.BP5: Bidirectional traceability from system requirements to stakeholder requirements. Non-functional process requirements may not trace (Note 8) | Traceability chain: hazardous event → safety goal → FSR → TSR | Bidirectional traceability required. Derived requirements must flow back up for safety impact assessment | Traceability from StRS to SyRS [unverified] |
| **Completeness Criteria** | Outcome 2: All stakeholder expectations "understood." SYS.2.BP5: Coverage of stakeholder requirements demonstrated | HARA completeness: all hazardous events identified; operationally all driving scenarios covered | All aircraft functions identified; FDAL assigned to each. Validation of completeness via "by similarity" for existing baseline | "Implied and unstated needs" must be captured [unverified] |
| **Change Management** | BP3: Mandatory change analysis and risk assessment. SUP.10 as supporting process. Requirement Attribute (17-54) tracks status | Part 8 CM processes; ASIL-sensitive changes require impact analysis | CM: requirements changes managed under CM Level 1 (detail CM). Revalidation required for changed requirements | Change management procedures [unverified] |

---

## 8. Key Findings — What the Standards Collectively Require

### 8.1 Agreement is Non-Negotiable (ASPICE SYS.1)

All three engineering standards (ASPICE, ISO 26262, ARP 4754A) require some form of
**formal agreement** on stakeholder needs/requirements. Implicit agreement does not
satisfy any of them. The mechanics differ (ASPICE: explicit agreement from affected
parties; aviation: DER/authority approval of certification basis; automotive: ASIL
classification via HARA represents regulatory agreement), but the principle is universal.

### 8.2 Requirements Validation is a Distinct and Often-Neglected Process

Peterson 2015 identified requirements validation as a problematic practice area across the
aviation industry — most engineers had experience with requirements *verification* (did we
build it right?) but not requirements *validation* (are we building the right thing?).
[src-peterson-arp4754a-2015 §5 p.7]

The ARP 4754A validation process requires:
- At least two methods applied to each requirement
- A Validation Matrix tracking status per requirement
- Explicit handling of assumptions (stated, disseminated, justified)
- Derived requirements require additional scrutiny

This is substantially more demanding than the typical practice of "review the requirements
document at CDR."

### 8.3 Source Attribution Matters

ASPICE SYS.1.BP1 Note 1 states that documenting the stakeholder or source of a requirement
supports agreement and change analysis. ARP 4754A example artifacts show requirement source
as an explicit column in both validation and verification matrices (Parent Req ID, Derived,
or Assumption). [src-peterson-arp4754a-2015 Table 18 p.69, Table 19 p.71]

This is architecturally important for AI-assisted needs engineering: the agent must not only
produce requirement text but must capture and maintain attribution.

### 8.4 Unstated Requirements Are Structurally Addressed

The concept of "requirements necessary for intended use that are not stated by the
stakeholder" is addressed through different mechanisms:

- **ASPICE:** SYS.1.BP1 captures environmental needs; SYS.1.BP3 Note 4 captures legal/
  regulatory needs; 29148 (referenced by SYS.2.BP1) formalizes implied needs
- **ISO 26262:** HARA systematically derives safety needs that no individual stakeholder
  explicitly stated — this is the most rigorous implementation of this concept
- **ARP 4754A:** Certification basis (regulations + advisory circulars) constitutes unstated
  requirements from the regulatory stakeholder; FDAL derivation from FHA captures functional
  safety needs

### 8.5 Quality Criteria Are Referenced by Standards, Not Defined in Them

None of the primary engineering standards (ASPICE, ISO 26262, ARP 4754A) fully define what
makes a requirement well-written. They reference external standards:
- ASPICE SYS.2.BP1: cites ISO/IEC/IEEE 29148, ISO 26262-8, and INCOSE GtWR
- ARP 4754A: relies on engineering judgment for requirement text quality
- ISO 26262: Part 8 contains some guidance but INCOSE GtWR is the accepted industry reference

The implication for AI skill design: the skills must incorporate INCOSE/29148 quality
criteria explicitly, because the engineering standards assume this is addressed elsewhere.

---

## 9. What This Research Covers vs. What's Missing

### Covered:
- [x] ASPICE SYS.1 all BPs verbatim with interpretation
- [x] ASPICE SYS.1→SYS.2 relationship and traceability obligations
- [x] ISO 26262 concept phase stakeholder mapping (secondary sources)
- [x] ARP 4754A: function enumeration, certification basis, requirements validation
- [x] Peterson 2015: validation matrix structure, industry practice issues
- [x] INCOSE 42-rule framework: applicability at needs level (secondary source)
- [x] Cross-standard comparison table

### Not covered (primary sources unavailable):
- [ ] ISO/IEC/IEEE 29148:2018 directly — paywalled. SYS.1 content is adequate for
      documentation purposes; 29148 detail needed for Research 3 (requirements craft)
- [ ] INCOSE GtWR primary document — paywalled. Secondary source is adequate for the
      cross-reference purpose of this research
- [ ] ISO 26262 Part 3 primary — paywalled. Research 1 secondary sources are adequate
      for documentation §2 (V-model context)
- [ ] ARP 4754A primary §5.3-5.5 (requirements capture/validation clauses verbatim) —
      paywalled. Peterson 2015 case study examples provide sufficient operational detail
- [ ] DO-178C §5.1 on requirements (software requirements process) — paywalled but covered
      in Research 1 codex seed sources

---

## 10. Sources

### Primary sources (read from raw files in this session)

- **[src-aspice-4-0]** ASPICE PAM v4.0, VDA QMC WG13, 2023.
  `raw/standards/Automotive-SPICE-PAM-v40.pdf` pp. 34-42.
  SYS.1 (pp.34-35), SYS.2 (pp.36-37), SYS.3 (pp.38-39), SYS.4 (pp.40-42) — verbatim BPs,
  outcomes, output information items, and notes.

- **[src-peterson-arp4754a-2015]** Peterson, Eric M. "Application of SAE ARP4754A to
  Flight Critical Systems." NASA/CR-2015-218982, November 2015.
  `raw/papers/peterson-arp4754a-nasa-2015.pdf`
  - pp. 1-8: Executive Summary, Scope, Application Guidelines Summary, Policy Issues Summary,
    Results and Recommendations.
  - pp. 64-71: SDP100 §5.1-5.3 — Requirements Development & Management, Requirements
    Validation (including Table 18 Validation Matrix and Table 19 Verification Matrix).
  - pp. 74-84: PSCP200, ASDP200 — Certification Plan, requirements structure for
    modification scenario.

- **[src-incose-42-rule-guide-reqi-2026]** Reqi.io. "INCOSE Requirements Quality: The
  Complete 42-Rule Guide." 2026.
  `raw/articles/incose-42-rule-guide-reqi-2026.md`
  Secondary source summarizing INCOSE GtWR. All 42 rules, 15 quality characteristics.

### Secondary sources used for context

- **[Research 1]** `research/system-level/01-standards-system-level-processes.md` — used
  for ISO 26262 Part 3 content (HARA, safety goals, FSC) where primary is paywalled.

- **[src-seed-aspice-iso26262]** — used for ASIL/FDAL mapping context.

- **Engineering codex wiki** — std-aspice, concept-requirement-quality — structural context.
