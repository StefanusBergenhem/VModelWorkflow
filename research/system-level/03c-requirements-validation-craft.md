# Research 3c: Requirements Validation Craft — Confirming Requirements Are Correct and Complete

Research for upper V documentation (backlog items 3.4, 3.5). Focuses on the craft of
requirements validation at the system level: the five validation methods, inspection
techniques, modeling, completeness verification, independence, and the Validation Matrix
as a concrete artifact.

**Sources used (read directly in this session):**
- NASA/CR-2015-218982, Peterson 2015 (primary, read from pdftotext, lines cited throughout)
  [src-peterson-arp4754a-2015]
- Shull, Rus, Basili 2000 — "How Perspective-Based Reading Can Improve Requirements
  Inspections," Computer 33(7), pp. 73-79 (primary, read from pdftotext)
  [src-shull-pbr-2000]
- Kelly, Sherif, Hops 1992 — "An Analysis of Defect Densities Found During Software
  Inspections," J. Systems Software, Feb. 1992, pp. 111-117 (primary, read from pdftotext
  via NASA NTRS) [src-kelly-jpl-1992]
- Kamsties, Berry, Paech 2001 — "Detecting Ambiguities in Requirements Documents Using
  Inspections," Fraunhofer IESE / University of Waterloo (primary, read from pdftotext)
  [src-kamsties-2001]
- Peddireddy & Nidamanuri 2021 — "Requirements Validation Techniques and Factors
  Influencing Them," MSc thesis, Blekinge Institute of Technology (primary, read from
  pdftotext) [src-peddireddy-bth-2021]
- SEBoK wiki, "System Validation" page (fetched) [src-sebok-validation]
- NASA IV&V Program overview presentation (read from pdftotext) [src-nasa-ivv-2019]
- IEEE 1012 definition of independence (secondary, via NASA IV&V presentation) [src-ieee-1012]
- Brings et al. 2016 — "Model-Based Prototype Development to Support Early Validation of
  Cyber-Physical System Specifications," CEUR proceedings (primary, read from pdftotext)
  [src-brings-2016]
- Systematic mapping study on requirements quality (Rashid et al. 2021, PMC open access,
  analyzed 105 empirical studies) [src-rashid-sms-2021]
- Research 2b (02b-stakeholder-needs-validation.md) — cross-referenced for Peterson findings
  already documented
- ASPICE PAM v4.0 [src-aspice-4-0] — cross-referenced from Research 2b

**Claims marked [unverified] were not read from a primary source in this session.**

---

## 1. The Central Problem: Validation Is Not Inspection

Requirements validation is routinely confused with requirements review. The confusion
matters because it leads to the wrong tool being applied: a team that believes "we
reviewed the requirements, therefore they are validated" has likely done verification
(checking that requirements are well-formed) without doing validation (confirming they
are correct and complete).

The NASA Peterson study documented this confusion as a systemic problem: "Most design
engineers have experience defining and verifying but NOT justifying their requirement
set." Verification is a learned procedural skill. Validation requires a different kind
of judgment — the ability to answer "would implementing these requirements produce the
system we actually need?"
[src-peterson-arp4754a-2015, p. 7, §5 "ARP Application General"]

The distinction between the five validation methods (Section 2) and the standard
inspection techniques (Section 3) is not semantic. They answer different questions:

| Method category | Question answered | What it can find |
|---|---|---|
| Traceability | Is this requirement's existence authorized? | Orphan requirements, missing upward links |
| Analysis / Modeling | Is the content technically correct? | Infeasibility, inconsistency, performance gaps |
| Test / Prototype | Does this produce the intended behavior? | Wrong behavior, missing behavior, UI/UX failures |
| Similarity | Is this functionally equivalent to the baseline? | Changed requirements that need revalidation |
| Inspection (review) | Is the expression of the requirement correct? | Ambiguity, incorrectness, incompleteness, inconsistency |

No single method answers all questions. This is the empirical argument for using
multiple methods on the same requirement — not because any standard requires it, but
because each method has a different detection profile.

---

## 2. The Five Validation Methods in Depth

The five methods used in practice are drawn from the Peterson case study documentation
of ARP 4754A application. They appear in the Validation Matrix columns (Section 6).
[src-peterson-arp4754a-2015, pp. 68-69, ASDP200 §5.2.1, Table 25]

### 2.1 Traceability

**What it is:** Establishing that each requirement traces to a higher-level source —
an aircraft function, operational need, safety objective, or stakeholder requirement.
A requirement that cannot be traced upward has no authorized reason to exist.

**When to use it:** On every requirement. Traceability is the minimum validation
method — it does not stand alone but it must be present. Applied at system level,
traceability links system requirements to aircraft/vehicle functions or stakeholder
needs. Applied at item level, it links item requirements to system requirements.

**What it catches:**
- Requirements that were invented during design ("gold plating") with no authorization
- Orphaned requirements from features that were descoped but whose requirements
  remain in the baseline
- Gaps: system requirements that satisfy no stakeholder need (may indicate a problem)

**What it misses:** Everything else. A requirement can be traceable and still be
technically wrong, ambiguous, untestable, or describe the wrong behavior. ASPICE
SYS.2.BP5 Note 7 is explicit: "Traceability alone does not necessarily mean that the
information is consistent with each other." [src-aspice-4-0, p. 37, SYS.2.BP5 Note 7]

The most common validation failure is treating traceability coverage as sufficient
validation evidence. It is not. Traceability confirms authorization; it does not
confirm correctness.

**How to do it well:** Bidirectional traceability — upward (every requirement traces
to a source) and downward (every source is addressed by at least one requirement).
The downward direction is the completeness check: if a stakeholder need or safety
objective has no system requirement tracing to it, the requirement set has a gap.

**How to do it badly:** Creating parent-child links without reading the actual content
of parent and child to confirm the child correctly implements the parent intent.
Traceable but incorrectly derived requirements are the most dangerous class of
defect: they pass traceability checks and fail everything else.

### 2.2 Analysis (Modeling)

**What it is:** Logical and technical analysis of requirement content to assess
correctness, consistency, and feasibility. This includes interdependency analysis —
examining how requirements interact and whether the interactions are consistent.
[src-peterson-arp4754a-2015, p. 68]

**When to use it:**
- Requirements that specify performance values (e.g., response times, probabilities,
  tolerances): analysis checks whether the values are physically achievable and
  consistent with each other
- Requirements that have interdependencies: analysis checks whether requiring A
  and requiring B simultaneously is consistent
- Requirements where the intent is not apparent from the text alone: analysis of
  the parent function confirms whether the child requirement correctly implements it
- Novel or high-risk requirements: requirements that differ from the similarity
  baseline need analysis to confirm correctness

Modeling (simulation, formal specification, executable requirements) is the
intensified form of analysis: instead of logical argument, a computational model
demonstrates whether the requirements produce intended behavior. See Section 3.

**What it catches:**
- Performance requirements that are mutually exclusive or physically infeasible
- Requirements that create circular dependencies or contradictions
- Requirements where the specified value is inconsistent with the overall system
  budget (power budget, timing budget, failure probability budget)
- Derived requirements that incorrectly implement the intent of the parent

**What it misses:** Behavior that is correct in isolation but wrong in the operational
context. Analysis is typically scoped to the requirements document; it does not
substitute for operational scenario walkthrough.

**How to do it well:** Apply analysis systematically to requirement clusters, not
just individual requirements. Ask "if all these requirements are implemented, do
they collectively produce the intended function?" The interdependency analysis
documented in ASPICE SYS.2.BP3 is exactly this: "Analyze the specified system
requirements including their interdependencies to ensure correctness, technical
feasibility." [src-aspice-4-0, p. 36, SYS.2.BP3]

**How to do it badly:** Treating analysis as "I read the requirement and it seems
reasonable." Analysis without documentation produces no artifact and no evidence.
The result of analysis must be captured in an artifact reference in the Validation
Matrix.

### 2.3 Test (Prototype / Simulation)

**What it is:** Exercising requirements to validate them before full implementation.
This is not the same as verification testing (which confirms implementation meets
requirements). Validation testing uses a prototype, model, or simulation to confirm
that if the requirement is implemented, it will produce the intended system behavior.
[src-peterson-arp4754a-2015, p. 68]

**When to use it:**
- Operability requirements (human-machine interface, display layout, control feel):
  these are extremely difficult to validate by inspection or analysis but can be
  validated cheaply by mockup or prototype
- Performance requirements where simulation can substitute for hardware-in-the-loop
  testing
- Requirements for behavior in failure conditions: simulation of failure scenarios
  validates that the specified behaviors are sufficient to maintain safety
- Requirements in novel domains where similarity to a baseline cannot be claimed

Brings et al. (2016) document a specific challenge for cyber-physical systems:
"Software prototypes of cyber-physical systems' software, however, often need to be
adapted to the prototype's hardware, which may differ from the system's hardware.
This leads to differences between the system's and the implemented prototype's
specification, impeding the applicability of validation results." Their solution is
to maintain explicit traceability between prototype specification and system
specification, with rationale for every deviation. [src-brings-2016, pp. 1-2]

This has a direct implication for validation evidence: when a prototype-based
validation finding is "this behavior is wrong," the engineer must determine whether
the defect is in the system requirement or is an artifact of the prototype's hardware
differences.

**What it catches:**
- Requirements that specify correct individual behaviors but produce an unusable
  system when combined (emergent behavior defects)
- Requirements that are technically correct but operationally unacceptable
  (a display that updates at the correct rate but is unreadable in cockpit lighting)
- Missing requirements that only become apparent when the system is used

**What it misses:** Safety defects that only manifest in edge cases or failure
sequences that were not included in the validation scenarios. Prototype testing
is subject to the same "cannot prove absence" limitation as all testing. Kamsties
et al. (2001) state: "Simulation can show only the presence of misinterpretations
but not their absence." [src-kamsties-2001, p. 2]

**How to do it well:** Define test scenarios before building the prototype. Scenarios
should derive from the operational concept and safety analysis — not from the
engineer's intuition. Document what was observed, what finding it produced, and
whether the finding indicates a defect in the requirement.

**How to do it badly:** Building a prototype to demonstrate feasibility rather than
to probe for defects. A demonstration prototype that "works" does not validate the
requirements — it validates that something can be built. The target of prototype
testing must be specific requirements, and the scenarios must be constructed to
challenge those requirements.

**Cost-benefit consideration:** Prototype/simulation validation is expensive in
engineering time but inexpensive compared to discovering the same defect during
integration or certification. For high-FDAL/high-ASIL functions, the cost is
justified. For low-criticality requirements, similarity or inspection may be
more cost-effective.

### 2.4 Similarity

**What it is:** Validating requirements by reference to a previously certificated
baseline. The claim is: "This requirement is functionally equivalent to AVSYS-R-XXX
in the certified baseline, which has been previously validated. Therefore, this
requirement inherits that validation result."
[src-peterson-arp4754a-2015, p. 68]

**When to use it:**
- Derivative products: when the new system is substantially similar to a previously
  certified system and the applicable requirements are carried forward unchanged or
  with minor modification
- Requirements that are not changed: in an incremental development program, if a
  requirement is unchanged from the previous certification, similarity is the
  appropriate validation method
- Reused requirements blocks: when a subsystem design is reused with known
  modifications, unchanged requirements can be validated by similarity

The Peterson case studies anticipated "the bulk of the avionic systems requirements
will be validated through similarity to the certificated baseline." This is the
dominant validation method in derivative and incremental aviation programs.
[src-peterson-arp4754a-2015, p. 68]

**What it catches:** Nothing directly — similarity is a claim of equivalence. What
it protects against is expending validation resources on requirements that are
genuinely unchanged from a validated baseline. The value is in focusing effort
on changed and new requirements where real validation work is needed.

**What it misses:** Changed context. A requirement can be textually identical to
a validated baseline requirement but apply in a different operational context that
invalidates the original validation. Similarity requires confirming that the context
is also similar — not just the text.

**How to do it well:** Document the baseline reference explicitly: which baseline
document, which requirement, which certification. Record what changed between the
baseline version and the current version. Apply additional validation methods to
anything that changed, even slightly. The Peterson practice explicitly states that
"baseline requirement set derived requirements and assumptions will be revalidated
as part of the SAAB-EII 100 validation process." Similarity is not applied to
assumptions regardless of baseline similarity.
[src-peterson-arp4754a-2015, ASDP100 §5.2.1]

**How to do it badly:** Using similarity as a blanket claim without actually comparing
requirements text and context. "It's basically the same system" is not a validation
argument. The claim must be traceable to a specific baseline requirement with
documented evidence of equivalence.

**Hard limit:** Similarity cannot validate requirements that did not exist in the
baseline. Every new requirement and every changed requirement requires at least
one additional validation method.

### 2.5 Inspection (Engineering Review)

**What it is:** Structured expert review of the requirement text. Distinguished from
analysis (which evaluates technical content) by focusing on the expression: is the
requirement stated correctly, unambiguously, and completely?
[src-peterson-arp4754a-2015, p. 68]

This is the most universally applicable validation method — it can be applied to
every requirement — and it is the most commonly misapplied. The gap between a
genuine engineering inspection and a "rubber stamp" review is large.

Details on effective inspection techniques are in Section 3. The key distinction
here is what inspection targets as a validation method (vs. as a general review):
inspection applied for validation asks "is this requirement correct and complete?"
not just "does this requirement comply with our formatting standard?"

---

## 3. Inspection and Review Techniques for Requirements

### 3.1 The Defect Detection Landscape

Before examining specific techniques, the empirical picture of what inspections find
and miss:

The systematic mapping study by Rashid et al. (2021) analyzed 105 empirical studies
on requirements quality. The four most-researched defect types were:
1. **Ambiguity** (49 studies, ~20% of research attention)
2. **Completeness** (34 studies)
3. **Consistency** (27 studies)
4. **Correctness** (24 studies)

These four account for 54% of all requirements quality research.
[src-rashid-sms-2021]

The JPL study (Kelly, Sherif, Hops 1992) analyzed 203 Fagan-style inspections across
five software-intensive projects over 3 years. Key findings:
- "The highest defect density was observed during Requirements inspections" —
  requirements had statistically significantly higher defect density than all other
  lifecycle phases (architecture design, detail design, source code, test plans)
- The five most prevalent defect categories across all inspection types were:
  Clarity, Logic, Completeness, Consistency, and Functionality
- Average cost to find and fix a defect during inspection: 1.1 hours to find,
  0.5 hours to fix. For comparison, a JPL project reported 5-17 hours to fix
  defects during formal testing — a 10x to 30x cost multiple
- Larger inspection teams (6-9 participants) showed increased defect-finding
  capability for requirements and high-level design inspections
[src-kelly-jpl-1992, conclusions section]

Fagan (1976) at IBM originally reported 80-90% of defects found by formal
inspection, with cost savings of up to 25%. [src-kelly-jpl-1992 citing Fagan 1976]
This figure is widely cited; the JPL data provides more conservative but
methodologically documented confirmation from a safety-critical domain.

### 3.2 Technique Taxonomy

Four techniques exist along a spectrum from informal to systematic:

**Ad hoc review:** No defined procedure. Reviewers apply their own judgment.
- Pros: Low overhead, fast to start
- Cons: No systematic coverage, no training path, dependent entirely on reviewer
  skill and willingness, provides almost no evidence of quality
- What it misses: RE-specific ambiguities (context-dependent, requires domain
  knowledge), completeness gaps (requires comparing against a source of truth),
  any defect the reviewer's experience does not prime them to notice

**Checklist-based review:** Reviewers apply a predefined list of defect types and
quality properties to check.
- Pros: Ensures systematic coverage of known defect classes, trainable, provides
  a documented record
- Cons: Only finds defects the checklist was designed to catch; poor for discourse
  ambiguities that span multiple requirements scattered across pages
- Defect types caught well: syntax errors, format violations, missing required
  fields, individual requirement quality properties (testability, clarity,
  abstraction level)
- Defect types caught poorly: cross-requirement inconsistency, RE-specific
  ambiguity, completeness gaps not represented in the checklist

**Fagan inspection (formal inspection):** A structured six-phase process: planning,
overview, preparation, inspection meeting, rework, follow-up. Defined roles
(moderator, author, inspector, reader). Entry and exit criteria. Defect logging.
Metrics collection.
- What makes it effective: Role separation (the author is not the moderator),
  mandatory preparation before the meeting, quantitative exit criteria, moderator
  independence, post-inspection metrics analysis
- What makes it fail: "Organizational ignorance" — "culture works against revealing
  or admitting mistakes," lack of trained moderators, lack of time budgeting. When
  inspections become a meeting where authors defend their work, the process has
  failed regardless of the paperwork produced.
  [Wikipedia/Fagan; corroborated by Shull et al. on the need for trained reviewers]
- Required preparation rate: Fagan established approximately 150 lines of
  requirements per hour as a safe preparation rate. Exceeding this rate
  "decreased the density of defects found" in the JPL data. [src-kelly-jpl-1992]

**Perspective-Based Reading (PBR):** Each reviewer reads the requirements from a
specific stakeholder perspective (designer, tester, user) and constructs a
representation (architecture sketch, test case set, use case model) from that
perspective. Defects emerge when the representation cannot be constructed or
reveals inconsistencies.
- Origin: Shull, Rus, Basili 2000 from research at University of Maryland and
  validated with 25 professional developers at NASA Goddard Space Flight Center
- Effectiveness: "PBR leads to improved defect detection rates for both individual
  reviewers and review teams working with unfamiliar application domains."
  Review time increased 0-30% compared to usual NASA approach, but detection
  rate increased. [src-shull-pbr-2000, pp. 77-78]
- Best suited for: Reviewers with "a certain range of experience" — enough to
  construct the representations but not so experienced that they revert to personal
  heuristics and ignore the PBR procedure
- The three standard perspectives are: **designer** (can these be implemented as
  coherent components?), **tester** (can test cases be generated for each
  requirement?), **user** (do the requirements describe the system behavior the
  user needs?)
- What tester perspective catches: Missing test criteria, requirements that cannot
  be observed (untestable), requirements that produce contradictory test results
- What user perspective catches: High-level behavioral errors, requirements that
  individually make sense but collectively produce wrong system behavior, missing
  requirements for operational scenarios

### 3.3 The Ambiguity Detection Problem

Kamsties, Berry, Paech (2001) provide the most detailed empirical study of
requirements ambiguity detection. Key findings:

The distinction between **linguistic ambiguity** (any reader can notice it) and
**RE-specific ambiguity** (only a reader with domain knowledge can notice it) is
critical for inspection design. In one requirements document, 4 linguistic
ambiguities and 54 RE-specific ambiguities were reported — RE-specific ambiguities
dominated by a factor of 13.5.
[src-kamsties-2001, p. 1, citing Kamsties Ph.D. dissertation]

Their experimental results (controlled experiments with students):
- Generic inspection technique (checklist + scenario-based reading): detected
  18% of ambiguities per 4.5 hours of team review (3 reviewers)
- Domain-specific technique (adapted from UML metamodel): detected 25% of
  ambiguities in the same time
- For comparison, using a requirements specification language (formal notation)
  detected 9% of ambiguities — but crucially, the remaining 72% of ambiguities
  were "interpreted correctly" because the formal notation forced a choice
[src-kamsties-2001, pp. 11-13]

This has a sobering implication: even with trained reviewers using systematic
techniques, a realistic inspection session will find only 18-25% of ambiguities.
The value of inspection is not exhaustive detection — it is the cost-effective
removal of detectable defects early.

Critically: "One cannot expect to find all ambiguities in a requirements document
with realistic resources." The goal is not completeness; the goal is cost-effective
defect reduction before defects propagate.
[src-kamsties-2001, p. 13]

### 3.4 What Makes a Requirements Review Effective vs. a Rubber Stamp

Based on the evidence:

**Effective reviews:**
1. Reviewers who did not write the requirement. The author's tacit knowledge fills
   in gaps that are actual defects — they cannot see what they implicitly assumed.
2. Preparation time budgeted and enforced. The JPL data shows that exceeding safe
   inspection rates directly reduces defect density. The Fagan process mandates
   this through entry criteria.
3. Role separation. A Fagan inspector is not an ad hoc attendee — different
   reviewers focus on different aspects. This is the precursor to PBR's formalization
   of roles into perspectives.
4. Written defect list before the meeting. Votta (1993) argued that "most
   defects are found during preparation, not during the meeting" — an empirical
   finding that shifts the center of gravity from meeting attendance to individual
   preparation. [src-peddireddy-bth-2021 citing Votta 1993, via snowball sample]
5. Domain-specific checklists. Generic checklists find fewer RE-specific
   ambiguities than checklists tailored to the system domain.

**Rubber stamps:**
1. Reviewers who are co-authors or close collaborators of the author — they
   share the same assumptions
2. Meeting without prior individual preparation — reviewers encounter the
   requirements for the first time in the meeting
3. Inspection rate too fast — the JPL data shows this directly reduces defect density
4. No separation between defect-finding and defect-resolution phases — when authors
   defend and explain rather than remaining silent, the review shifts from finding
   defects to justifying them
5. "Validation matrix completed because the process requires it" — the NASA study
   documents this explicitly: "It's not just about what is being done but who does
   it as well. Expertise (skills and experience) matters."
   [src-peterson-arp4754a-2015, p. 7]

---

## 4. Modeling and Simulation for Validation

### 4.1 When to Build a Model

Modeling adds cost to requirements validation. The decision to model is a trade-off:

**Build a model when:**
- The system behavior is complex enough that human inspection cannot reliably
  predict whether a set of requirements will produce consistent, correct behavior
- Requirements specify timing, sequencing, or state-dependent behavior where
  informal analysis cannot detect mode confusion or race conditions
- The consequences of a requirements error are severe enough to justify the cost
  (FDAL A / ASIL D functions)
- Stakeholder acceptance is required for novel or unusual behavior — a model
  provides direct demonstration that cannot be argued abstractly

**Use analysis without modeling when:**
- Requirements are amenable to manual logical argument
- The system is sufficiently similar to a certified baseline that behavior is
  well-understood
- Engineering judgment (with documented rationale) is sufficient evidence
  for the assigned FDAL/ASIL

**Do not use modeling as a substitute for inspection:** Kamsties et al. note that
"simulation can show only the presence of misinterpretations but not their absence."
Models do not replace inspection — they address the class of defects that inspection
cannot reach (emergent behavioral errors, timing errors, state-machine gaps).

### 4.2 Types of Models for Requirements Validation

**Executable specifications:** Requirements translated into an executable notation
(SysML, SCADE, MATLAB/Simulink, B-Method) that can be simulated or analyzed
formally. The act of translation reveals ambiguities — informal requirements that
cannot be unambiguously translated into formal notation are definitionally
ambiguous.

**State machine models:** Requirements that specify modes, states, and transitions
can be modeled as state machines. Completeness checking is algorithmic: are all
input events handled in all states? Are there unreachable states? Do all paths
terminate? This structural analysis of a state machine provides completeness
evidence that inspection cannot provide for stateful systems.

**Rapid prototypes:** Low-fidelity implementations of behavioral requirements.
Particularly valuable for human-machine interface requirements. Brings et al. (2016)
propose the explicit "prototype specification" as an artifact — a specification of
what the prototype implements, distinct from the system specification, with explicit
traceability and documented deviations. This allows validation findings from the
prototype to be classified as: applicable to the system requirement, or artifact of
the prototype's hardware differences. [src-brings-2016, pp. 2-3]

**Interface models:** Models of external interfaces (message sequences, timing
constraints, failure behaviors) reveal interface requirements that are missing or
inconsistent. Particularly valuable for distributed systems where interface
requirements span organizational boundaries.

### 4.3 The Cost-Benefit Assessment

The case for modeling is strongest when a late-cycle requirements defect would cause
catastrophic rework. The Boehm cost-of-repair curve (though specific to software
and the absolute numbers are contested) reflects an empirically documented phenomenon:
defects found later cost more to fix. The JPL data provides concrete support in a
safety-critical domain: fixing defects during inspection costs 0.5 hours on average;
fixing during formal testing costs 5-17 hours. [src-kelly-jpl-1992]

The break-even analysis for modeling: if modeling 10 requirements costs 40 engineering
hours but prevents one requirements defect that would otherwise cost 100+ hours to
fix in testing, the investment is justified. For FDAL A functions, even a single
undetected requirements defect could prevent certification. For those cases, the
modeling cost is uncapped.

---

## 5. Completeness Validation

### 5.1 The Epistemic Challenge

Completeness is logically harder to validate than correctness. Proving correctness
requires demonstrating that what is stated is true. Proving completeness requires
demonstrating that nothing is missing — proving absence.

INCOSE defines completeness at the requirement set level as: "the set of requirements
includes all the requirements that define all the characteristics of the system needed
to satisfy its stakeholder requirements and constraints."
[unverified — INCOSE GtWR, cited in Research 2b §3.1]

This definition acknowledges the challenge: completeness is relative to a source
(stakeholder requirements and constraints). A set can only be complete with respect
to something. If the source is incomplete, the derived set cannot be complete
regardless of how carefully the derivation was performed.

### 5.2 Structured Completeness Methods

Completeness validation requires systematic techniques that probe for missing
requirements by checking against independent sources of truth:

**Operational Scenario Walkthrough**

Walk through each defined operational scenario (from the ConOps, System Definition,
or Item Definition) and ask: for every decision point and every input event in this
scenario, does a requirement exist that specifies the system's response?

This method exploits the scenario as a completeness oracle. A requirement that is
missing will manifest as an undefined system behavior during the walkthrough. The
challenge is that the scenario set itself must be complete — an incomplete ConOps
produces an incomplete scenario walkthrough.

ISO 26262 Part 3 Clause 5 (Item Definition) explicitly requires "operating scenarios
impacting functionality" to be defined. These are the baseline scenarios against
which completeness is checked. [Research 1, §4.1]

The SEBoK identifies the walkthrough as a general-purpose completeness technique:
"validation occurs at the conclusion of lifecycle tasks... begins with validating
stakeholder needs and requirements." [src-sebok-validation]

**Safety Analysis Cross-Reference**

For safety-critical systems, the FHA (Functional Hazard Assessment) or HARA
(Hazard Analysis and Risk Assessment) is an independent source of required behaviors.
Every identified hazardous condition must be addressed by at least one requirement.
If a hazard maps to no requirement, the set is incomplete — not with respect to what
was asked for, but with respect to what is physically required by the hazard space.

ARP 4754A integrates the safety assessment process as an integral process running
alongside requirements validation. The PSSA (Preliminary System Safety Assessment)
derives safety requirements from failure modes; these requirements must appear in the
system requirement set. Missing PSSA-derived requirements = proven incompleteness.
[Research 1, §3.4]

In automotive: the HARA (ISO 26262 Part 3 Clause 6) generates safety goals via
S×E×C analysis. A complete safety goal set covers every identified hazardous event.
The mapping from safety goals to functional safety requirements provides another
completeness cross-reference.

**Interface Completeness Check**

Many missing requirements concern system boundaries. The question is: for every
interface the system has (inputs, outputs, communications, physical connections),
does a requirement exist that specifies the system's behavior at that interface?

The ASPICE SYS.2 requirement to identify "external interfaces" as part of the system
requirements produces an interface list that can be used as a completeness checklist.
For each interface, at minimum: normal operation, out-of-range input, and
communication failure must be specified.

**Mode Coverage Check**

Systems with multiple operating modes (normal, degraded, emergency, maintenance,
standby) must have requirements for behavior in each mode. A completeness check
maps every requirement against the mode(s) it applies to and identifies:
- Modes with no requirements (completeness gap)
- Requirements that apply to "all modes" without verification that the behavior
  is actually correct in degraded/emergency modes (validation gap)

Mode confusion — a pilot or operator misidentifying which mode the system is in —
is a well-documented human factors failure. Requirements that do not explicitly
address mode annunciation and transitions leave a completeness gap that human
factors incidents trace directly to.

**Derived Requirement Feedback Loop**

ASPICE SYS.2.BP5 Note 8 identifies a category of completeness gap: "There may be
non-functional stakeholder requirements that system requirements do not trace to.
Examples are process requirements. Such stakeholder requirements are still subject
to verification."
[src-aspice-4-0, p. 37, SYS.2.BP5 Note 8]

If a stakeholder requirement has no system requirement tracing to it, the explanation
must be documented. Undocumented missing traces = potential completeness gap.

ARP 4754A mandates that derived requirements at the item level (created by
engineering without explicit higher-level authorization) be fed back to the system
level for safety impact assessment. This "derived requirement feedback loop" catches
requirements that engineering created without stakeholder knowledge.
[src-peterson-arp4754a-2015, §1, and Research 1 §2.7]

### 5.3 The Completeness Ceiling

No systematic method can guarantee completeness. Operational scenario walkthrough
covers only scenarios that were identified. Safety analysis covers only hazards that
were identified. Interface analysis covers only interfaces that were modeled.

The practical goal is defensible completeness: sufficient evidence that the
requirement set is complete with respect to the sources of truth that have been
systematically checked. The argument must be documented: "We assert completeness
because we have verified coverage against [scenarios], [safety analysis],
[interface model], and [regulatory requirements]. We acknowledge that requirements
not derivable from these sources may exist and are not covered by this argument."

---

## 6. Independence in Validation

### 6.1 What Independence Means

The concept of independence in requirements validation has a technical meaning that
differs from casual usage. Independence in the IEEE 1012 sense (cited in the NASA
IV&V program) requires three dimensions:
- **Technical independence:** Different personnel from those who wrote the
  requirements
- **Managerial independence:** Different reporting structure (the validator does not
  report to the same manager as the requirement author)
- **Financial independence:** The validation budget is not under the same control
  as the development budget
[src-nasa-ivv-2019; citing IEEE 1012]

Full independence (all three dimensions) is what "IV&V" means for NASA's highest-
profile missions. The IV&V program was established in 1993 following the Challenger
accident investigation recommendations.
[src-nasa-ivv-2019, p. 3]

For most programs, full IV&V is not required. The ARP 4754A framework uses a graded
independence requirement based on FDAL:

**FDAL A:** Validation "will be accomplished with independence."
[src-peterson-arp4754a-2015, ASDP200 §5.2.1 — from pdftotext line 7936-7940]

**FDAL B and C:** Independence is "a process goal but may be verified by requirement
originators as necessary." Note: this is the verification process text, not the
validation process text. For simplicity, one case study (SDP100) applied independence
to "FDALs A through C" uniformly. [src-peterson-arp4754a-2015, SDP100 §5.2.1,
pdftotext line 6142-6144]

**FDAL D:** No explicit independence requirement stated in the case studies.

### 6.2 Why Independence Matters for Validation (Not Just Process Compliance)

The epistemic argument for independence is different from the regulatory argument:

A requirement author has tacit knowledge about the system that fills in gaps and
resolves ambiguities automatically. When the author reviews their own requirement,
they read what they intended to write, not what they wrote. This is not dishonesty —
it is a cognitive phenomenon documented in proofreading research and in the PBR
literature. [src-shull-pbr-2000 on how experienced reviewers "revert to using
previously acquired heuristics" rather than the review procedure]

The consequence: a requirement that is ambiguous to any other reader is unambiguous
to its author. The author's validation is not evidence of unambiguity — it is
evidence that the author knows what they meant. These are different claims.

For requirements supporting FDAL A functions (single-point failure prevention,
catastrophic hazard mitigation), an ambiguous requirement that is "validated" by
its author has produced a false safety signal. The validation record says "Valid:
Y" but the validation was performed without the independence that would have
caught the ambiguity.

### 6.3 What Effective Independence Looks Like in Practice

The NASA IV&V approach describes its practice as: "product focused — not document or
compliance focused. Examines concept, architecture, requirements, design, code, and
test products." [src-nasa-ivv-2019]

Key characteristics of effective independent validation:
1. The independent validator has the domain knowledge to evaluate correctness, not
   just process compliance. A reviewer who cannot evaluate whether a navigation
   requirement is technically feasible cannot validate it.
2. The validator reports findings independently. They are not in a position where
   finding defects creates political problems.
3. The validation scope includes both stated requirements and assumptions. The
   Peterson case study documents that assumptions receive the same validation rigor
   as stated requirements. An independent validator reviewing only explicit
   requirements while tacit assumptions remain unexamined has partial independence.
4. The validation is performed against the stakeholder need, not against the
   specification. Independence that only checks internal consistency is verification
   independence, not validation independence.

### 6.4 Lightweight Independence: Practical Forms

Full IV&V is expensive and reserved for high-criticality programs. Lighter-weight
forms of independence serve the same epistemic function:

**Second-person review within the same organization:** The second engineer reads
the requirements without briefing from the author. They form an independent
interpretation before comparing notes. Where their interpretation diverges from the
author's, the requirement is ambiguous and requires revision.

**Cross-functional review:** Requirements are reviewed by engineers from the system's
user functions (operators, maintenance, certification), not just the engineering
team. These reviewers provide genuine perspective independence even without
organizational independence.

**Rotating authors and reviewers:** In a team with multiple requirements engineers,
rotating so that no one reviews requirements they wrote. This is organizational
independence at low cost.

**Test engineer review:** The tester who will later verify the implemented system
reviews requirements. The PBR "tester perspective" formalizes this: if the tester
cannot generate test cases from the requirement, the requirement fails validation,
regardless of whether it satisfies all formal quality properties.

---

## 7. The Validation Matrix as a Concrete Artifact

### 7.1 Purpose and Relationship to Verification Matrix

The Validation Matrix is not the same artifact as the Verification Matrix. This is
the most important practical distinction for engineers building compliance artifacts.

| | Validation Matrix | Verification Matrix |
|---|---|---|
| Question | "Is this requirement correct and complete?" | "Does the implemented system satisfy this requirement?" |
| Timing | During requirements development | After implementation |
| Contents | Requirement, source type, validation methods applied, artifact reference, Valid Y/N | Requirement, verification methods, Pass/Fail result |
| Populated by | Requirements engineers | Test engineers |

Both matrices reference the same requirement IDs. They are separate artifacts with
different evidence. [src-peterson-arp4754a-2015, pp. 69-71, Tables 18 and 19]

### 7.2 Column Definitions (from Table 18, Peterson)

The Validation Matrix columns documented in the ASDP case studies:

| Column | Content | Notes |
|---|---|---|
| Requirement ID | Unique identifier | Same ID used in Verification Matrix |
| Requirement Text | Full text or reference | Required for the matrix to be self-contained |
| Safety Flag | Y if requirement is safety-related | Determines validation rigor |
| Requirement Source | Parent Req ID / Derived / Assumption | Three-way classification |
| Inspect | X if inspection method applied | Engineering review |
| Analysis | X if analysis/modeling method applied | Includes simulation |
| Similarity | X if similarity to baseline applied | Must document baseline reference |
| Test | X if prototype/test method applied | Must reference test artifact |
| Trace | X if traceability method applied | Most common; least sufficient alone |
| Validation Artifact Reference | Document, ECM, report | The evidence for the validation claim |
| Req Valid Y/N | Final validation determination | N means requires remediation |

[src-peterson-arp4754a-2015, Table 18 matrix coding, pdftotext lines 9990-10060]

Note on abbreviations in the artifact reference column from the Peterson examples:
- CN = Change Notice
- ECM = Engineering Communication Memo
- Insp = Inspection (the artifact produced from a formal inspection)
- Reqt = Requirement (for traceability entries)

### 7.3 Filling the Matrix: Evidence Standards

Each "X" in the method columns requires a corresponding entry in the Validation
Artifact Reference column. Without the artifact reference, the X is a claim without
evidence.

| Method | Minimum artifact reference |
|---|---|
| Traceability | Traceability table or tool report showing parent-child link |
| Analysis | Analysis report or Engineering Communication Memo with conclusion |
| Similarity | Reference to specific baseline document and requirement ID |
| Test | Reference to prototype test report or simulation result |
| Inspection | Reference to inspection record (findings, disposition) |

An assumption row requires: inspection as minimum method + an ECM or equivalent
documenting the justification for the assumption and its dissemination.

### 7.4 The "Derived" Classification: A Critical Category

Derived requirements are requirements created during engineering that do not trace
to a higher-level stated requirement. They arise from engineering design choices —
the engineer determines that a particular behavior is necessary even though no
stakeholder explicitly requested it.

The hazard in derived requirements is that they may introduce behavior with safety
implications that were not analyzed. ARP 4754A mandates that derived requirements
at the item level (from DO-178C or DO-254) be fed back to the system level for
safety impact assessment. This is the "derived requirement feedback loop."

In the Validation Matrix, a "Derived" source classification signals that the
requirement must be validated with particular attention to its safety implications.
A derived requirement with only traceability validation is a red flag: traceability
cannot validate a derived requirement (by definition, there is nothing to trace to).
At minimum, derived requirements require inspection and analysis.

### 7.5 When to Update the Validation Matrix

The Validation Matrix is a living artifact, not a one-time checkpoint:

1. **On initial requirements development:** Every new requirement gets a row.
   Validation methods are applied and the Valid Y/N determination is made.

2. **On every change:** When a requirement changes, its validation row must be
   revisited. A requirement that was Valid with similarity (similarity to the
   baseline) may no longer be valid if the change makes it no longer similar.

3. **On new safety analysis findings:** If the PSSA/SSA identifies a new failure
   mode that implies a new safety requirement, a row is added and validation is
   performed.

4. **On closure of validation findings:** When a requirement was marked Valid N
   (validation identified a defect), and the defect is corrected, the matrix is
   updated with the corrected requirement and new validation evidence.

The Peterson case studies document: "The requirements validation process is invoked
as part of the change management process for changed or addition of new requirements."
[src-peterson-arp4754a-2015, ASDP200 §5.2.1]

This means validation is not a phase; it is a continuous process that runs through
the change management system.

### 7.6 The Validation Summary Report

The Validation Matrix supports a higher-level summary artifact: the Validation and
Verification Summary Report. This report:
- States how many requirements were validated
- Identifies open findings (Valid N rows) and their disposition
- Summarizes the validation methods applied across the matrix
- Documents any deviations from the validation plan
- Provides the evidence that the validation process was completed

The Peterson documentation: "Validation activities accomplished and the completed
validation matrix will be included in the Avionics System Validation and Verification
Summary Report. Deviations from the validation process will be captured and reported
in the Summary Report." [src-peterson-arp4754a-2015, ASDP200 §5.2]

---

## 8. Common Validation Failures

### 8.1 Traceability Coverage Presented as Validation Coverage

The most common systemic failure in industrial requirements validation. An
organization reports "all requirements are validated" because all requirements have
parent links in the requirements management tool. The Validation Matrix was never
built; only the traceability matrix exists.

ASPICE SYS.2.BP5 Note 7 is the explicit standard-level warning: "Traceability alone
does not necessarily mean that the information is consistent with each other."
[src-aspice-4-0, p. 37]

The ASPICE assessor's question: "Show me the analysis results" — not the traceability
report. The analysis results are the Output Information Item for SYS.2 Outcome 3.
[src-aspice-4-0, p. 37, Output Information Items table]

### 8.2 "Validated by the Author"

Requirements validated by their own author carry the cognitive limitation described
in Section 6.2. For high-criticality requirements, this is a compliance failure.
For all requirements, it represents a validation that is likely to miss RE-specific
ambiguities (the dominant defect class) because the author's knowledge resolves them.

### 8.3 Validation Matrix Completed After the Fact

When a validation matrix is filled in at the end of a program to satisfy a certification
audit, rather than being populated during requirements development, the evidence is
likely to be low-quality. The Peterson study documents this pattern: "This activity is
viewed as being new and unfulfilling work" and "puts additional demands on the scarce
experienced personnel resources." [src-peterson-arp4754a-2015, p. 7]

Markers of after-the-fact validation:
- Every requirement uses the same validation methods (often: Inspect + Trace)
- Artifact references are generic ("requirements review meeting") rather than specific
- Validation dates cluster at a single point near the certification review
- No requirements have Valid N determinations — implying no defects were found

Genuine validation produces a record that includes some Valid N rows (defects
found and remediated), specific artifact references, and dates distributed across
the development program.

### 8.4 Similarity Applied Without Equivalence Argument

Using "Similarity" as the validation method for requirements that were carried
forward from a baseline without confirming that the context is also similar. Changed
operational context, new interface connections, or modified adjacent systems can
invalidate a requirement that is textually identical to a validated baseline
requirement.

### 8.5 Assumptions Left Implicit

The assumption validation requirement is clear in the Peterson documentation:
"The validation process also includes capture and evaluation of assumptions made
during the requirement capture process to ensure: assumptions have been explicitly
stated, assumptions are appropriately disseminated, and assumptions are justified
by supporting data." [src-peterson-arp4754a-2015, ASDP300 §5.2]

An assumption that is not in the Validation Matrix (with source = "Assumption")
has not been validated. Implicit assumptions — shared knowledge that "everyone
knows" — are the failure mode. They appear correct until they are wrong, at which
point the entire requirement set built on them collapses.

---

## 9. Synthesis: The Craft of Validation

### 9.1 What Distinguishes High-Quality Validation

Drawn from the evidence above:

1. **Multiple methods with genuine coverage.** Not five boxes checked — five methods
   each applied where they are appropriate, with documented evidence for each.
   The JPL data demonstrates that requirements have the highest defect density
   in the lifecycle; they deserve proportionate investment.

2. **Independence calibrated to criticality.** FDAL A requires independent
   validation. FDAL B-C should have independence as a process goal. FDAL D should
   have at least second-person review. "Validated by author" is a marker of
   inadequate process regardless of FDAL level.

3. **Completeness arguments, not just correctness arguments.** Validating every
   stated requirement does not validate completeness. Completeness requires
   systematic checking against operational scenarios, safety analysis, and
   interface models.

4. **Assumptions treated as first-class validation targets.** The assumption rows
   in the Validation Matrix are often the most critical rows. An assumption that is
   wrong propagates error to everything derived from it.

5. **Living artifact updated through change management.** A validation matrix that
   is not updated when requirements change degrades to a historical record. Its
   value depends entirely on whether it reflects the current requirement baseline.

6. **Experienced reviewers.** The NASA study is explicit: "Expertise (skills and
   experience) matters." A validation matrix completed by junior engineers checking
   boxes has different epistemic value than one completed by experienced system
   engineers who evaluated each requirement against the intended function. The
   artifact is the same; the value is not.

### 9.2 Open Questions and Unresolved Claims

The following claims appear frequently in requirements validation literature and
standards but were not read from primary sources in this research session:

- [unverified] Boehm's specific cost-of-repair multipliers (1x to 100x from
  requirements to maintenance). The JPL data provides domain-specific evidence
  (1.6x to 34x for requirements vs. formal testing); Boehm's absolute numbers are
  widely cited but the original source was not read.
- [unverified] "Two validation methods minimum" as an industry-standard interpretation
  of ARP 4754A. Peterson identifies this as an industry interpretation, not ARP text.
  The actual ARP text is paywalled. The interpretation is documented but its accuracy
  against the original standard is uncertain.
- [unverified] ISO 26262 Part 3 Clause 8 "Safety Validation" at the vehicle level.
  Content attributed to secondary sources in Research 1; ISO 26262 is paywalled.
- [unverified] Wiegers' "business event" technique for completeness. Widely attributed
  but not read from primary source.
- [unverified] Robertson & Robertson Volere methodology's "snow card" and
  satisfaction/dissatisfaction fields. Described in Research 2b as unverified;
  status unchanged.

---

## Source Register

| ID | Full Citation | Type | Read directly? |
|---|---|---|---|
| src-peterson-arp4754a-2015 | Peterson, NASA/CR-2015-218982 | Primary (case study) | Yes (pdftotext) |
| src-shull-pbr-2000 | Shull, Rus, Basili, Computer 33(7) 2000 | Primary (empirical study) | Yes (pdftotext) |
| src-kelly-jpl-1992 | Kelly, Sherif, Hops, J.Systems Software Feb 1992 | Primary (empirical study) | Yes (pdftotext via NTRS) |
| src-kamsties-2001 | Kamsties, Berry, Paech, Fraunhofer IESE 2001 | Primary (empirical study) | Yes (pdftotext) |
| src-brings-2016 | Brings et al., CEUR Vol-1564 2016 | Primary (technique paper) | Yes (pdftotext) |
| src-rashid-sms-2021 | Rashid et al., PMC open access, Req.Eng. 2021 | Primary (systematic mapping) | Yes (WebFetch) |
| src-peddireddy-bth-2021 | Peddireddy & Nidamanuri, BTH MSc 2021 | Secondary (literature review) | Yes (pdftotext) |
| src-sebok-validation | SEBoK "System Validation" wiki | Secondary (synthesis) | Yes (WebFetch) |
| src-nasa-ivv-2019 | NASA IV&V Program overview, Aug 2019 | Secondary (briefing) | Yes (pdftotext) |
| src-ieee-1012 | IEEE 1012 Standard for V&V | Standard (paywalled) | No — cited via NASA IV&V |
| src-aspice-4-0 | ASPICE PAM v4.0 | Primary (standard) | Carried from Research 2b |
