# Research 2b: Stakeholder Needs Validation — The Industry Pain Point

Research for upper V documentation (backlog items 3.4, 3.5). Focuses on validation of
stakeholder needs: what it means, how it is performed, where it fails, and what the
standards actually require vs. what industry actually does.

**Sources used:**
- ASPICE PAM v4.0 (primary, read from PDF pp. 34-37) [src-aspice-4-0]
- NASA/CR-2015-218982, Peterson 2015 (primary, read from PDF pp. 1-8, 64-72) [src-peterson-arp4754a-2015]
- Engineering codex wiki pages: concept-requirement-quality [src-incose-42-rule-guide-reqi-2026, src-seed-requirement-syntax-beyond-ears]
- Research 1 (01-standards-system-level-processes.md) — cross-referenced throughout
- Additional claims from secondary sources marked [unverified] where not read directly

---

## 1. The Conceptual Problem: Validation vs. Verification at the Stakeholder Level

### 1.1 The Fundamental Distinction

Validation and verification are not synonyms. They answer different questions, and the
confusion between them is one of the most persistent failure modes in safety-critical
development.

| | Validation | Verification |
|---|---|---|
| Question | "Are these the right requirements?" | "Does the implementation satisfy the requirements?" |
| Object | The requirements themselves | The system being built |
| Evidence | Justification that requirements correctly describe the need | Evidence that the build matches the spec |
| Timing | During and after requirements capture | During and after implementation |
| Who | Experienced engineers with domain knowledge | Test engineers, auditors |
| Success criterion | Requirements would produce the intended system if implemented | Implemented system matches the requirements |

ARP 4754A makes this explicit: requirements validation is about "ensuring the correctness
and completeness of the set of captured requirements." It is a "structured process for
ensuring the correctness and completeness," not a check against an implementation.
[src-peterson-arp4754a-2015 pp. 67, SDP100 §5.2]

The verification matrix (Table 19 in the Peterson study) asks: "Does the completed system
pass the test?" The validation matrix (Table 18) asks: "Is this requirement correct and
complete?" These are fundamentally different artifacts with different evidence.
[src-peterson-arp4754a-2015 pp. 69-71]

### 1.2 Why Engineers Struggle With Validation

The NASA study identified validation as "a problematic effort" for industry. Three specific
reasons were documented:

1. **Interpretation ambiguity.** The ARP's validation method table "seems to imply to some
   industry readers that a minimum of two methods are recommended in the absence of clear
   ARP text descriptions." The standard implies rigor without specifying it.

2. **Experiential gap.** "Most design engineers have experience defining and verifying but
   NOT justifying their requirement set." Verification is a learned skill with established
   procedures. Validation requires a different, less teachable kind of judgment — answering
   "is this requirement correct?" requires domain expertise, not just process compliance.

3. **Cultural resistance.** "This activity is viewed as being new and unfulfilling work.
   And finally, validation puts additional demands on the scarce experienced personnel
   resources." The people most capable of doing validation are the same experienced engineers
   most overcommitted elsewhere.

[src-peterson-arp4754a-2015 p. 7, §5 "ARP Application General"]

Furthermore, only 25% of survey respondents had received training on ARP 4754A.
[src-peterson-arp4754a-2015 p. 6, §5 "FDAL/IDAL Assignment"] That number should be
interpreted carefully: these are the same respondents struggling with FDAL/IDAL assignment,
so the 25% figure covers all ARP training, not validation specifically. But it establishes
that most practitioners are applying the ARP without formal instruction.

### 1.3 The Assumptions Problem

The Peterson study case studies define validation to include not just requirements but
also "specific assumptions made during the requirement capture process." Three criteria
apply to assumptions:

- **Assumptions have been explicitly stated** (not left tacit)
- **Assumptions are appropriately disseminated** (relevant parties know them)
- **Assumptions are justified by supporting data** (not just asserted)

[src-peterson-arp4754a-2015 p. 67, SDP100 §5.2]

This is significant. Many requirement sets look complete but carry a large load of unstated
assumptions. Example: a requirement for display independence assumes the power distribution
is already required elsewhere. If that assumption is not surfaced and traced, the
requirement set has a completeness gap even if every stated requirement is individually
correct.

---

## 2. Validation Methods: What the Standards Prescribe

### 2.1 ARP 4754A — Five Methods

From the case study documentation of how ARP 4754A objectives are applied in practice, five
validation methods are identified and used in combination:

1. **Traceability** — Establish that each requirement traces to a higher-level source
   (aircraft function, operational need, safety objective). If a requirement cannot be
   traced upward, its existence is not justified.

2. **Analysis (Modeling)** — Analyze requirements including through modeling to assess
   whether they are correct, consistent, and technically feasible. This includes
   interdependency analysis.

3. **Test** — Exercise the requirement to validate it directly. More applicable to
   requirements that can be partially validated before full implementation (e.g.,
   prototype testing of operability requirements, simulation of performance requirements).

4. **Similarity** — Validate requirements by reference to previously certificated baseline
   that the new requirements are similar to. "The bulk of the avionic systems requirements
   will be validated through similarity to the certificated baseline."

5. **Inspection (engineering review)** — Structured expert review of the requirement text.

[src-peterson-arp4754a-2015 pp. 68, SDP100 §5.2.1 "Requirements Validation Methods & Process"]

The Validation Matrix (Table 18 in Peterson) is the artifact that records which method(s)
were applied to each requirement, the validation result, and the artifact reference.
Columns: Unique ID | Text | Safety flag | Requirement Source | Inspect | Analysis |
Similarity | Test | Trace | Validation Artifact Reference | Req Valid (Y/N).
[src-peterson-arp4754a-2015 p. 69, Table 18]

Contrast with the Verification Matrix (Table 19), which records Test/Analysis/Service/
Inspection methods against implemented requirements, with Pass/Fail outcomes.
[src-peterson-arp4754a-2015 p. 71, Table 19]

**Key insight from practice:** The case studies anticipated that "the bulk of the avionic
systems requirements will be validated through similarity to the certificated baseline."
Similarity is an accepted validation method, not a shortcut — it is explicitly listed in
the ARP alongside traceability and analysis. For legacy or derivative products, similarity
is the dominant method.
[src-peterson-arp4754a-2015 p. 68]

### 2.2 ASPICE v4.0 — What SYS.1 and SYS.2 Require

ASPICE SYS.1 (Requirements Elicitation) requires stakeholder expectations to be
"formalized into requirements" with a "common understanding" and "explicit agreement from
all affected parties." The process purpose is to "gather, analyze, and track evolving
stakeholder needs."
[src-aspice-4-0 p. 34, SYS.1]

What ASPICE SYS.1 does NOT prescribe: specific validation methods, any distinction between
validation and verification at this level, or techniques for finding requirements the
stakeholder did not articulate. The process is elicitation-focused — getting what
stakeholders say they want — not validation-focused in the ARP 4754A sense.

ASPICE SYS.2 (System Requirements Analysis) requires requirements to be "analyzed for
correctness and technical feasibility" (Outcome 3). BP3 specifies: "Analyze the specified
system requirements including their interdependencies to ensure correctness, technical
feasibility, and to support project management regarding estimates." Technical feasibility
can be evaluated using "prototype development or product demonstrators."
[src-aspice-4-0 p. 36, SYS.2.BP3]

The requirement quality characteristics referenced in SYS.2.BP1 (Note 2) include:
"verifiability (i.e., verification criteria being inherent in the requirements text),
unambiguity/comprehensibility, freedom from design and implementation, and not contradicting
any other requirement." These come from ISO/IEC/IEEE 29148 or INCOSE GtWR.
[src-aspice-4-0 p. 36, SYS.2.BP1 Note 2]

Traceability (SYS.2.BP5) in ASPICE is explicitly noted to not be sufficient for validation:
"Traceability alone does not necessarily mean that the information is consistent with each
other."
[src-aspice-4-0 p. 37, SYS.2.BP5 Note 7]

**What ASPICE SYS.2 does NOT have:** a dedicated validation process analogous to ARP 4754A's
requirements validation integral process. ASPICE treats validation (in the sense of "are
these the right requirements?") as a quality attribute of analysis, not a separate process
with its own matrix artifact.

### 2.3 ISO 26262 Part 3 — Safety Goal Confirmation

ISO 26262's Part 3 (Concept Phase) includes a safety validation step at the vehicle level
(Clause 8) that "validates that the safety goals are correct, complete, and fully achieved."
This is performed on the integrated vehicle, not on the requirements document.
[src: Research 1, §4.2, citing secondary sources — secondary source confidence]

For stakeholder needs specifically, the HARA (Hazard Analysis and Risk Assessment) process
in Part 3 Clause 6 implicitly validates that safety goals correctly represent the hazardous
events identified. The safety goal "is correct" if it correctly addresses the hazardous
event; "is complete" if all hazardous events have safety goals. The ASIL assignment (S×E×C)
provides a structured basis for arguing completeness.
[src: Research 1, §4.1 — secondary sources]

ISO 26262 Part 3 is explicit that the concept phase must define the "operational and
environmental constraints" and "operating scenarios impacting functionality." These are
the domain in which unstated requirements live. Capturing them is an obligation but the
standard does not prescribe how.
[src: Research 1, §4.1 — secondary sources]

### 2.4 INCOSE Guidance — Validation as a Quality Characteristic

The INCOSE Guide to Writing Requirements (GtWR) lists "able to be validated" as one of
the fifteen essential characteristics applied at the requirement set level. This is
distinct from "verifiable" (individual characteristic): a requirement set is validatable
if you can justify that it correctly and completely represents stakeholder needs.
[src-incose-42-rule-guide-reqi-2026 §The 15 Essential Characteristics]

The GtWR does not provide a validation methodology. It defines the end state ("these
requirements can be justified as correct and complete") but not the path.
[src-incose-42-rule-guide-reqi-2026 — silent on validation methodology]

---

## 3. Completeness: How Do You Know You Haven't Missed Something?

### 3.1 The Completeness Problem Defined

Completeness is the hardest property to validate. Verifying an individual requirement is
epistemically simpler than proving a set is complete — the latter requires demonstrating
absence, not presence. You must argue that there is no requirement you have failed to
capture. This is a logical impossibility in general; in practice it is managed through
structured approaches that provide evidence of systematic coverage.

ASPICE SYS.2 Outcome 3 requires that system requirements "are analyzed for correctness and
technical feasibility" — correctness is individual property, but the analysis of
interdependencies provides indirect completeness evidence by exposing gaps in the
interaction model.
[src-aspice-4-0 p. 36, SYS.2]

INCOSE's "completeness" characteristic at the set level means "the set of requirements
includes all the requirements that define all the characteristics of the system needed to
satisfy its stakeholder requirements and constraints."
[src-incose-42-rule-guide-reqi-2026 §The 15 Essential Characteristics]

### 3.2 Negative Requirements

Negative requirements ("the system shall NOT") are legitimate and important for
completeness but are widely underused and frequently malformed.

The problem is epistemic: a statement "the system shall not crash" cannot be proven
complete because you cannot enumerate all crash modes. The useful form of a negative
requirement is a bounded prohibition: "the system shall not allow a pilot to disable both
primary and standby displays simultaneously." This is traceable, testable, and its
completeness is tied to the FHA — if the hazard analysis identified "simultaneous loss of
all display capability" as a hazardous event, the requirement exists to address it.

Anti-pattern: treating "shall not fail" as a valid requirement. It is not — it lacks
verification criteria. The correct form is "shall achieve a probability of less than 10⁻⁹
per flight hour" for loss of function.
[synthesis, based on src-seed-requirement-syntax-beyond-ears §3.1 on negative requirements
and src-peterson-arp4754a-2015 safety analysis context]

### 3.3 Implicit and Assumed Requirements

The ARP 4754A practice documented in Peterson explicitly treats assumptions as items
requiring validation. Three categories appear in the Validation Matrix:

- **Parent Req ID** — requirement derived from a higher-level stated requirement
- **Derived** — derived requirement created during design (must flow back up for safety
  impact assessment)
- **Assumption** — an assumption made during requirements capture

[src-peterson-arp4754a-2015 p. 69, Table 18 "Matrix Coding"]

Assumptions receive validation by inspection (engineering review) and require an artifact
reference (e.g., an Engineering Communication Memo) to document the justification.
[src-peterson-arp4754a-2015 p. 69, Table 18 AVSYS-R-xxx row with "Assumption" source]

Derived requirements (those not traceable to a higher-level stated requirement) require
special attention. ARP 4754A mandates that derived requirements at the item level (from
DO-178C or DO-254) be fed back to the system level for safety impact assessment. This
"derived requirement feedback loop" is the formal mechanism for catching requirements that
engineering created without explicit stakeholder authorization.
[src-peterson-arp4754a-2015 p. 2, §1, and Research 1 §2.7]

ASPICE SYS.2.BP5 Note 8 explicitly acknowledges that some stakeholder requirements may
not trace to any system requirement: "There may be non-functional stakeholder requirements
that system requirements do not trace to. Examples are process requirements. Such
stakeholder requirements are still subject to verification."
[src-aspice-4-0 p. 37, SYS.2.BP5 Note 8]

This is a completeness gap indicator: if a stakeholder requirement has no system
requirement tracing to it, something must explain why (it's a process requirement, or
it's addressed elsewhere), and the explanation must be documented. Missing explanation =
potential completeness gap.

### 3.4 The Volere Approach (Unstated Needs)

[unverified — from secondary sources and training knowledge, not read from a primary source
in this session]

The Volere template (Robertson & Robertson) uses "fit criteria" for every requirement —
a measurable criterion that must be satisfied for the requirement to be considered met.
This is directly parallel to INCOSE's "verifiable" characteristic and ASPICE's SYS.2.BP1
Note 2 requirement that "verification criteria being inherent in the requirements text."

The Volere "snow card" is a single-requirement record with fields including: the requirement
statement, rationale, originator, fit criterion, customer satisfaction/dissatisfaction rating
if present/absent, and dependencies. The satisfaction/dissatisfaction field is a direct
attempt to surface implicit needs: "how satisfied would the customer be if this requirement
were met? How dissatisfied if not?"

**This is unverified — the Robertson & Robertson Volere methodology is referenced here but
not read from a primary source.** Claims about Volere above are marked [unverified] and
should be verified against the Volere Shell documentation or Robertson & Robertson's
"Mastering the Requirements Process" before citing in documentation.

---

## 4. Finding Unstated Needs: The ASPICE SYS.1.BP2 Problem

### 4.1 What ASPICE Actually Says

ASPICE SYS.1.BP2 states: "Agree on requirements. Formalize the stakeholder's expectations
and requests into requirements. Reach a common understanding of the set of stakeholder
requirements among affected parties by obtaining an explicit agreement from all affected
parties."

Note 3 adds: "The agreed stakeholder requirements may be based on feasibility studies
and/or cost and schedule impact analysis."
[src-aspice-4-0 p. 34, SYS.1.BP2]

Critically, the phrase "requirements not stated by the stakeholder but necessary for
specified and intended use" does not appear verbatim in ASPICE SYS.1 as read from the
PAM v4.0 PDF. The PAM's SYS.1.BP1 says to obtain requirements "through direct solicitation
of stakeholder input, and through review of stakeholder business proposals (where relevant)
and other documents containing inputs to stakeholder requirements, and consideration of the
target operating and hardware environment."
[src-aspice-4-0 p. 34, SYS.1.BP1]

"Consideration of the target operating and hardware environment" is the PAM's gesture toward
unstated needs — requirements that emerge from the operational context rather than explicit
stakeholder requests. The PAM does not specify how to systematically discover these.

**Important clarification:** The phrase "requirements not stated by the stakeholder but
necessary for specified and intended use" is a commonly cited characterization of the problem
that ASPICE SYS.1 creates, but this exact phrasing may originate from practitioner
interpretation of the standard rather than from the PAM verbatim. Readers should not
present this as a direct quote from ASPICE PAM v4.0.
[src-aspice-4-0 pp. 34-35 — text read directly; the exact phrasing is not present]

### 4.2 Systematic Techniques for Discovering Unstated Needs

The following techniques are described in requirements engineering literature and standards
as methods for surfacing requirements the customer did not articulate. Attribution is given
where sources support the claim; unverified claims are marked.

**Domain Analysis**
Examine similar systems in the same domain to identify requirements that are universally
present but not explicitly requested. Aviation example: all airborne navigation systems
require provisions for GPS signal loss regardless of whether the customer asks for it.
The FHA process in ARP 4761 partially automates this — it forces identification of all
functions and their failure modes, which surfaces requirements that implicit domain
knowledge would normally leave unstated.
[synthesis, based on ARP 4761 FHA process per Research 1 §3.3 and src-peterson-arp4754a-2015]

**Operational Scenario Walkthrough**
Walk through the operational scenarios defined in the item definition (ISO 26262 Part 3)
or aircraft function definition (ARP 4754A) and ask for each scenario: "What must be true
for this scenario to be safe and functional?" Requirements implied by scenario execution
but not explicitly listed are candidates for addition.

ISO 26262 Part 3 Clause 5 (Item Definition) explicitly requires "operating scenarios
impacting functionality" to be defined. These are the scenarios against which completeness
is checked.
[src: Research 1 §4.1 — ISO 26262 Item Definition content, secondary sources]

**Regulatory Scanning**
Standards, regulations, and certification requirements impose obligations not always
known to the customer. The customer may specify a braking system without knowing that
14 CFR 25.735 imposes specific stopping distance requirements. Regulatory scanning
identifies these externally-imposed requirements.

In aviation, the Certification Basis (listed in the Certification Plan) provides a
structured list of applicable regulations. Requirements to satisfy the certification basis
are mandatory even if not explicitly requested.
[src-peterson-arp4754a-2015 p. 17 — Certification Basis field in CP100]

**Failure Mode Analysis**
Bottom-up failure analysis (FMEA) applied before full design identifies required safety
behaviors. When a failure mode analysis identifies a failure with severe consequences, a
requirement to prevent or mitigate that failure must exist even if no stakeholder asked
for it. The PSSA (Preliminary System Safety Assessment) in ARP 4761 performs exactly this
function — it derives safety requirements from failure modes.
[src: Research 1 §3.4, secondary sources for ARP 4761 PSSA]

**Interface Analysis**
Many unstated requirements concern system boundaries. What the system must do to other
systems (and what it must tolerate from them) is often not articulated by stakeholders
who think in terms of internal function. The ISO 26262 Part 4 HSI Specification
(Hardware-Software Interface) is a structured artifact for capturing interface requirements.
[src: Research 1 §4.2 — HSI Specification, secondary sources]

**Wiegers on Discovering Undiscovered Requirements** [unverified]

Karl Wiegers in "Software Requirements" (3rd ed.) describes the "business event" technique:
identify all external events that the system must respond to. Events trigger responses;
responses imply requirements. If a business event (user input, time trigger, external
system message, failure condition) has no corresponding requirement, there is a gap.

This is [unverified] — Wiegers' text has not been read from a raw source in this session.
The technique is widely attributed to him but should be verified before citing in formal
documentation.

### 4.3 The "Intended Use" Requirement

The phrase "intended use" appears in product liability and regulatory contexts as a source
of unstated requirements. A product used in its "intended use" context has implicit
requirements derived from:

- What a reasonable operator would expect the system to do in normal operation
- What a reasonable operator would expect the system to do in failure conditions
- What relevant standards require of systems in that class

The distinction between "specified use" (what the customer asked for) and "intended use"
(what the system will reasonably be used for) is the gap where unstated requirements live.
For automotive products, this is reflected in ISO 26262 Part 3's requirement to define
the item's "functional description" including "interactions with other items and elements"
and "known hazards from similar items."
[src: Research 1 §4.1 — Item Definition content, secondary sources]

---

## 5. Validation in Safety-Critical Contexts: What Standards Require

### 5.1 ARP 4754A (Aviation)

ARP 4754A treats requirements validation as one of seven "integral processes" that run
continuously across all development phases. The seven integral processes are:
1. Safety Assessment, 2. DAL Assignment, 3. Requirements Capture, 4. Requirements
Validation, 5. Configuration Management, 6. Process Assurance,
7. Certification Coordination.
[src: Research 1 §2.3, citing src-peterson-arp4754a-2015]

**What ARP 4754A requires for validation evidence:**
- A Validation Matrix covering all requirements and assumptions
- Each row identifies: the requirement or assumption, its source type (Parent/Derived/
  Assumption), which validation method(s) were applied, the validation artifact, and
  the final Valid (Y/N) determination
- Validation activities are reported in the Avionic System Validation and Verification
  Summary Report
- Deviations from the validation process must be captured and reported

[src-peterson-arp4754a-2015 pp. 67-69, SDP100 §5.2 and §5.2.1]

**What ARP 4754A is silent on:** It does not specify how many validation methods must be
applied per requirement. "A minimum of two methods" is an interpretation industry applies
to the method table, not a verbatim requirement.
[src-peterson-arp4754a-2015 p. 7 — "seems to imply to some industry readers that a minimum
of two methods are recommended"]

The phrase "seems to imply" in the NASA report is critical: this is the NASA study
characterizing the industry's reading of the ARP, not a direct statement of what the ARP
requires. The actual ARP text is paywalled; this ambiguity is the documented gap.

**Independence requirements for validation:**
- Requirements supporting FDAL A functions: validation "will be accomplished with
  independence" (a second party validates what the requirement author wrote)
- Requirements supporting FDAL B-C functions: independence is "a process goal but may
  be verified by requirement originators as necessary"

[src-peterson-arp4754a-2015 p. 68, SDP100 §5.2.1]

### 5.2 ASPICE v4.0 (Automotive Process Assessment)

ASPICE SYS.2 Outcome 3 requires system requirements to "be analyzed for correctness and
technical feasibility." This is the closest ASPICE comes to requiring validation in the
ARP 4754A sense.

Evidence required for a rating of "Fully achieved" on ASPICE SYS.2:
- Analysis Results (15-51) demonstrating correctness and feasibility analysis
- Consistency Evidence (13-51) establishing bidirectional traceability
- Requirements Attributes (17-54) including verification criteria

[src-aspice-4-0 p. 37, SYS.2 Output Information Items table]

**ASPICE does not have a requirements validation matrix as a named artifact.** The concept
is embedded in the Analysis Results output. Assessors look for evidence that someone
actually analyzed the requirements for correctness, not just that they were reviewed for
syntax.

**Process capability level dimension:** An organization at ASPICE Level 1 (Performed) only
needs to show it produces the outcomes. An organization at Level 2 (Managed) must show
the work product management process controls validation evidence (stored, versioned,
reviewed). Most OEMs require suppliers to achieve Level 2-3 for safety-relevant processes.
[src-aspice-4-0 pp. 18-23 — capability levels, general; specific OEM requirements are
[unverified] from secondary knowledge]

### 5.3 ISO 26262 Parts 3-4 (Automotive Functional Safety)

ISO 26262's confirmation that "safety goals are correct and complete" happens at the
Safety Validation step (Part 3 Clause 8 and Part 4 Clause 8), which is performed on
the vehicle-integrated system, not on the requirements document.

The structured mechanism for validating that stakeholder needs are correct at the concept
phase is the HARA (Clause 6): the identification and classification of all hazardous events
is the standard's way of ensuring the safety goals (top-level safety requirements)
completely cover the hazard space. ASIL determination provides a structured basis for
arguing completeness — every combination of S, E, C that produces an ASIL has a safety
goal; gaps in the HARA are gaps in the safety goal set.
[src: Research 1 §4.1, secondary sources]

**What ISO 26262 requires as validation evidence:**
- HARA documentation showing all hazardous events, their S/E/C ratings, and ASIL
- Safety goals with ASIL tracing back to hazardous events
- Functional Safety Concept confirming safety goals are addressed
- Safety Validation Report at the end of development

[src: Research 1 §4.1-4.2, secondary sources — ISO 26262 is paywalled]

### 5.4 Common Evidence Expected by Auditors

Across all three frameworks, assessors and auditors look for the same underlying thing:
evidence that someone competent examined the requirements and concluded they are correct
and complete, with a documented rationale.

The specific artifacts differ:
- ARP 4754A: Validation Matrix with method codes and artifact references
- ASPICE: Analysis Results with requirement attributes (correctness/feasibility analysis)
- ISO 26262: HARA documentation + Safety Validation Report

**What fails audits (all frameworks):**
- Requirements with no traceability to a higher-level need or safety objective
- Requirements without verification criteria (untestable requirements cannot be validated
  either — if you cannot define what "satisfied" means, you cannot validate the requirement)
- Assumed requirements with no documented justification
- Derived requirements not reviewed for safety impact
- Validation activities performed by the same person who wrote the requirements (for FDAL A
  / high-ASIL requirements)

[synthesis, based on src-peterson-arp4754a-2015, src-aspice-4-0, and concept-requirement-quality]

---

## 6. Common Validation Failures: What Goes Wrong

### 6.1 The "Yes, That's What I Asked For" Problem

The most fundamental validation failure is a requirement set that satisfies all formal
quality criteria but does not produce the system the stakeholder actually needs. The
requirement is syntactically correct, traceable, and testable — but it specifies the wrong
behavior.

This is the core of validation: a verified system proves the system was built correctly to
the spec. A validated spec argues the spec was correct to begin with. A system can pass
all verification activities and still fail to satisfy stakeholder needs if validation was
inadequate.

Example pattern: A stakeholder asks for "fuel consumption monitoring." The requirements
engineer writes: "The system shall display current fuel consumption in liters per hour."
All formal quality checks pass. But the stakeholder's real need was "warning when total
fuel is insufficient to reach the destination." These are different systems. The requirement
is verified but not validated.

[synthesis — illustrative pattern based on validation/verification distinction]

### 6.2 Documentation Without Understanding

The NASA study identified "check-the-box" documentation as a systemic problem. Requirements
are written because the process requires them, not because the engineer genuinely worked
through what is needed. A validation matrix is completed because the certification plan
requires it, with inspection marks placed on every row, but no genuine analytical work
was done.

"It's not just about what is being done but who does it as well. Expertise (skills and
experience) matters."
[src-peterson-arp4754a-2015 p. 7, §5 "ARP Application General"]

This is not phrased as a validation-specific finding but it applies directly: a validation
matrix completed by junior engineers checking boxes has almost no epistemic value. The
same artifact completed by experienced domain engineers who genuinely evaluated each
requirement against the intended function has high value. The artifact is the same; the
value depends entirely on who produced it and how.

### 6.3 Validation by Traceability Alone

The most common misapplication of validation is treating "every requirement traces to a
higher-level requirement" as sufficient validation evidence.

ASPICE explicitly warns against this: "Traceability alone does not necessarily mean that
the information is consistent with each other."
[src-aspice-4-0 p. 37, SYS.2.BP5 Note 7]

A requirement can trace to a parent while expressing the wrong behavior. Traceability
confirms the requirement's existence was authorized; it does not confirm the requirement's
content is correct.

Similarly, the Peterson study validates the bulk of requirements "through similarity to
the certificated baseline" — but the case studies are also careful to revalidate changed
and new requirements using additional methods (inspection, analysis, traceability). Similarity
is not applied uniformly; it is applied where genuine functional equivalence exists.
[src-peterson-arp4754a-2015 p. 68, SDP100 §5.2.1]

### 6.4 Missing Requirements That No One Articulated

The most dangerous validation failure is the requirement that was never written because no
one thought to ask for it. This cannot be caught by reviewing requirements — there is no
requirement to review.

Structured mechanisms that catch this:
- **FHA/HARA completeness:** If all functions are identified and all failure conditions
  are analyzed, requirements implied by those failure conditions should exist. Missing
  safety requirements become visible when the FHA/HARA does not map to any requirement.

- **Operational scenario walkthroughs:** Running through each scenario against the
  requirement set reveals scenarios that produce undefined system behavior. Undefined
  behavior = missing requirement.

- **Checklist-based coverage:** Domain-specific checklists (e.g., "have we addressed
  loss of communications?", "have we addressed partial power loss?") probe for common
  missing requirements in the relevant domain.

- **Hazard-driven completeness:** For safety-critical systems, every identified hazard
  must be addressed by at least one requirement. If a hazard has no mitigating requirement,
  the requirement set is incomplete with respect to the safety analysis.

[synthesis, based on ARP 4761 FHA/SSA process per Research 1, and ASPICE SYS.1-SYS.2]

### 6.5 Requirement Inflation vs. Requirement Completeness

A related failure is requirement inflation: adding requirements that are not actual needs,
often because engineers know how they plan to implement the function and write requirements
that describe the implementation. This over-constrains the design and creates a set that
is "complete" in the sense of having many requirements but not in the sense of correctly
capturing stakeholder needs.

The INCOSE Rule R31 (Abstraction) prohibits implementation prescription: requirements must
describe "what" not "how."
[src-incose-42-rule-guide-reqi-2026 §Rule R31]

The ASPICE requirement that system requirements exhibit "freedom from design and
implementation" as a quality characteristic is the same principle.
[src-aspice-4-0 p. 36, SYS.2.BP1 Note 2]

---

## 7. Validation of Assumptions: A Special Case

### 7.1 Why Assumptions Are High-Risk

Assumptions in requirements are high-risk because:
1. They are often invisible — they do not appear in the requirement text
2. They affect multiple requirements — a single wrong assumption propagates to everything
   derived from it
3. They are validated by people who already believe them — the expert who made the
   assumption also validates it, unless independence is enforced

The ARP 4754A case study practice explicitly tracks assumptions as separate items in the
Validation Matrix, with the same rigor as stated requirements.
[src-peterson-arp4754a-2015 p. 69, Table 18]

### 7.2 Assumption Validation Evidence

For the case study, an assumption requires:
- An explicit record in the Validation Matrix (source = "Assumption")
- A validation artifact reference (the Peterson example uses an "ECM" —
  Engineering Communication Memo)
- A validation method applied (inspection is the minimum)

The specific example in Table 18 shows an assumption validated by Inspection alone, with
reference to ECM-SAABEII-CompA-14.
[src-peterson-arp4754a-2015 p. 69, Table 18, AVSYS-R-xxx row source=Assumption]

---

## 8. Summary: What This Research Establishes

### 8.1 The Diagnosis

Stakeholder needs validation is the weakest link in the requirements engineering chain.
This is not a new observation — the NASA study documented it as a known industry problem.
The root causes are:

1. **Standards ambiguity:** ARP 4754A and ASPICE both require validation without adequately
   specifying how it is done. "A minimum of two methods" is an industry interpretation, not
   a stated requirement.

2. **Skill scarcity:** Validation requires domain expertise. The engineers who can validate
   correctly are the same ones most constrained. No amount of process can substitute for
   the judgment of someone who genuinely understands the operational context.

3. **Cultural mismatch:** Verification has a long tradition, tooling, and training path.
   Validation is newer as an explicit process, lacks tooling support, and is perceived as
   less rewarding.

4. **Completeness is inherently hard:** Proving a set is complete is logically harder than
   testing individual requirements. No method guarantees completeness; structured methods
   only reduce the probability of missing something.

### 8.2 What Good Validation Looks Like

Based on the primary sources read, a well-executed validation process:

1. **Produces a Validation Matrix** per requirement and assumption — not just a sign-off sheet
2. **Applies multiple methods** — traceability alone is insufficient; at minimum traceability
   plus analysis (or similarity for unchanged requirements from a validated baseline)
3. **Explicitly surfaces assumptions** — every assumption is a named, tracked, validated item
4. **Enforces independence for safety-critical requirements** — the validator is not the author
5. **Feeds back derived requirements** — requirements created during design review are fed
   back to the stakeholder needs level for impact assessment
6. **Documents deviations** — if validation could not be completed for some requirements,
   this is recorded and reported

[src-peterson-arp4754a-2015 pp. 67-69; src-aspice-4-0 pp. 34-37; synthesis]

### 8.3 What This Research Does NOT Cover

- Stakeholder identification and analysis techniques (who are the stakeholders, how to
  manage conflicting needs) → Research 2a
- The craft of writing good stakeholder needs documents → Research 3
- Safety analysis methods in depth (FHA, FMEA, STPA) as tools for completeness checking
  → Research 4
- AI-assisted validation techniques
- Specific tooling for requirements validation management
- The Wiegers "Software Requirements" body of work (referenced but not read from source)
- The Robertson & Robertson Volere methodology (referenced but not read from source)

---

## Sources

### Primary sources (read from raw files in this session)

- **[src-aspice-4-0]** ASPICE PAM v4.0, VDA QMC WG13, 2023.
  `raw/standards/Automotive-SPICE-PAM-v40.pdf` pp. 34-40.
  SYS.1-SYS.2 base practices and output information items — read verbatim.
  SYS.1.BP1-BP2, SYS.2.BP1-BP5 content — read directly.

- **[src-peterson-arp4754a-2015]** Peterson, Eric M. "Application of SAE ARP4754A to
  Flight Critical Systems." NASA/CR-2015-218982, November 2015.
  `raw/papers/peterson-arp4754a-nasa-2015.pdf`
  - pp. 1-8: Executive summary, scope, section 4 (guidelines), section 5 (policy/practice
    issues). Validation problematic effort finding, 25% training statistic, expertise matters.
  - pp. 64-72: SDP100 §5.1-5.3 — Requirements Development & Management, Requirements
    Validation (definition, assumptions, matrix structure), Requirements Verification.
    SDP100 §5.2.1 validation methods list and matrix.
    Table 18 (Validation Matrix structure and example).
    Table 19 (Verification Matrix structure and example).

### Secondary sources (from Research 1 cross-reference)

- **Research 1** [01-standards-system-level-processes.md]: ARP 4754A process structure,
  ASPICE SYS.1-SYS.3, ISO 26262 Parts 3-4 — all citations from Research 1 inherit that
  document's source attribution (primary ASPICE and Peterson reads, secondary web sources
  for ISO 26262 and ARP 4761).

### Engineering Codex wiki pages consulted

- `wiki/concepts/concept-requirement-quality.md` — INCOSE quality characteristics,
  42-rule framework, negative requirements anti-pattern.
  Sources: [src-incose-42-rule-guide-reqi-2026], [src-seed-requirement-syntax-beyond-ears]

### Unverified claims requiring follow-up

| Claim | Status | Action needed |
|---|---|---|
| Volere snow card methodology (Robertson & Robertson) | [unverified] | Read primary source |
| Wiegers "business event" technique | [unverified] | Read "Software Requirements" 3rd ed. |
| "Requirements not stated by the stakeholder" as ASPICE SYS.1.BP2 verbatim | Clarified: phrase not verbatim in PAM | Do not present as direct quote |
| OEM expectation of ASPICE Level 2-3 for safety-relevant processes | [unverified] | Verify against OEM supplier requirements |
| "Minimum of two validation methods" as ARP 4754A requirement | Clarified: industry interpretation, not verbatim | Do not present as direct quote from ARP |
