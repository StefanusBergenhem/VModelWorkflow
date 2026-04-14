# Research 3d: Requirements Management — Change Control, Derived Requirements, Traceability, and the Architecture Handoff

Research for upper V documentation (backlog items 3.4, 3.5, 3.6).
Focus: the management dimension of requirements engineering — not how to write good requirements
(covered in 03a-03c), but how to control them once written, what happens when they change,
how traceability is made useful rather than ceremonial, and what the requirements set must look
like before architecture can begin.

**Sources used (primary — read in this session):**
- ASPICE PAM v4.0 (primary, read from PDF pp. 34-39, 81-88, 126-142) [src-aspice-4-0]
- Peterson, NASA/CR-2015-218982 (primary, read from PDF pp. 1-8) [src-peterson-arp4754a-2015]
  — read in prior session, cited from prior research [01-standards-system-level-processes.md]

**Sources used (secondary — web-fetched in this session):**
- NASA Section 6.2 Requirements Management (nasa.gov/reference, fetched 2026-04-12)
  [web-nasa-reqmgmt-2026]
- NASA SWE-082 Authorizing Changes (swehb.nasa.gov, fetched 2026-04-12)
  [web-nasa-swe082-2026]
- SEBoK System Requirements Definition (sebokwiki.org, fetched 2026-04-12)
  [web-sebok-sysreqdef-2026]
- SEBoK Requirements Management (sebokwiki.org, fetched 2026-04-12)
  [web-sebok-reqmgmt-2026] — attributed to INCOSE NRM v1.1 and GtNR v1 (2022)
- Change Control Board, Wikipedia (en.wikipedia.org, fetched 2026-04-12)
  [web-wikipedia-ccb-2026]
- 321gang.com — hidden cost of poor traceability (fetched 2026-04-12)
  [web-321gang-traceability-2026]

**Sources used (search-extracted findings, not fetched as full documents):**
- Gotel & Finkelstein 1994, "An Analysis of the Requirements Traceability Problem," ICRE 1994,
  pp. 94–101. Published at UCL (discovery.ucl.ac.uk/id/eprint/749/). Primary PDF not fetched
  due to 403; findings extracted from web search results and Semantic Scholar abstract.
  Claims from this source marked [unverified-full-text].
- Zowghi & Nurmuliani, "A Study of the Impact of Requirements Volatility on Software Project
  Performance," empirical study. Primary PDF not fetched. Claims marked [unverified-full-text].
- Trace.space blog — requirements management statistics (fetched 2026-04-12)
  [web-tracespace-reqmgmt-2026] — cites 2024 Engprax/J.L. Partners study (not independently
  verified); PMI 2014 data (not independently verified). Secondary claims marked [unverified].

**Sources NOT available (paywalled or inaccessible):**
- IEEE 828 (configuration management standard) — paywalled
- NASA-STD-8739.8 (software assurance) — not fetched
- NPR 7150.2 full text — fetched as binary PDF, not readable; content from NASA web handbook only
- ISO/IEC 29148 (requirements engineering) — paywalled
- INCOSE GtWR — paywalled

---

## 1. Requirements Baselines and Change Control

### 1.1 What a Baseline Is

A baseline is a formally approved, immutable snapshot of a set of configuration items at a
point in time. ASPICE PAM v4.0 Annex B defines the Baseline information item (13-08) as:

> "A state of one or a set of work products and artifacts which are consistent and complete.
> Basis for next process steps and/or delivery. Is unique and may not be changed."
>
> *Note: This should be established before a release to identify consistent and complete delivery.*

[src-aspice-4-0 Annex B, item 13-08, p.134]

The critical property is immutability combined with completeness and consistency: every item
in the baseline must be at a compatible version. A baseline is not just a snapshot — it is a
claim that the snapshotted artifacts are internally consistent and ready to serve as the input
to the next process step.

NASA frames baselines the same way: when requirements are defined, assessed, and approved,
they are formally baselined, and this baseline "serves as a critical control point, enabling
projects to establish budgets, schedules, and frameworks for analyzing the technical, cost, and
schedule impacts of proposed modifications." [web-sebok-reqmgmt-2026]

### 1.2 When to Baseline

In systems engineering practice, requirements baselines are established at major lifecycle
milestones. NASA identifies three key control points:

- **System Requirements Review (SRR)** — system-level requirements baselined
- **Preliminary Design Review (PDR)** — allocated requirements and preliminary architecture
  baselined
- **Critical Design Review (CDR)** — detailed design requirements baselined

[web-tracespace-reqmgmt-2026]

In ASPICE terms, a baseline is established once the requirements have been agreed
(SYS.1.BP2, SYS.2 Outcome 6) and before the next process step begins. The Configuration
Management process (SUP.8) establishes and controls baselines: "Define and establish baselines
for internal purposes, and for external product delivery, for all relevant configuration items."
[src-aspice-4-0 §4.8.2, SUP.8.BP5, p.82]

The practical significance: before the first baseline, requirements evolution is natural and
inexpensive. After baselining, every change requires formal process. The SRR baseline is the
gate at which change control switches from informal evolution to formal configuration control.

### 1.3 The Change Control Process

Once baselined, requirements changes follow a controlled process. ASPICE SUP.10 (Change
Request Management) defines the process purpose as ensuring "that change requests are
recorded, analyzed, tracked, approved, and implemented." [src-aspice-4-0 §4.8.4, p.85]

The six process outcomes of SUP.10 define the complete lifecycle of a change request:

1. Requests for changes are recorded and identified
2. Change requests are analyzed, dependencies and relationships to other change requests are
   identified, and the impact is estimated
3. Change requests are approved before implementation and prioritized accordingly
4. Bidirectional traceability is established between change requests and affected work products
5. Implementation of change requests is confirmed
6. Change requests are tracked to closure and status is communicated to affected parties

[src-aspice-4-0 §4.8.4, SUP.10, p.85]

The ASPICE definition of what a Change Request (13-16) must contain is precise — it includes:
purpose of change, requester contact, impacted system(s), impact to operations of existing
system(s), impact to associated documentation, criticality and due date, and status tracking
information (progress status attribute, time stamp of status change, person who changed status,
rationale for changing a status). [src-aspice-4-0 Annex B, item 13-16, p.135]

### 1.4 The Change Control Board (CCB)

The CCB is the governance mechanism for approving changes. ASPICE explicitly names it: SUP.10.BP3
states "Change requests are prioritized and approved for implementation based on analysis results
and availability of resources" and adds: "Note 5: A Change Control Board (CCB) is an example
mechanism used to approve change requests." [src-aspice-4-0 §4.8.4, SUP.10.BP3, p.86]

A CCB typically consists of subject matter experts (engineering, test, safety) and managers.
Key properties of an effective CCB per NASA:

- Safety assurance/safety personnel must be included "to ensure safety impact is considered"
- Multi-level structure: product-level CCB (functional baseline changes), project-level CCB
  (allocated baseline changes), software development CCB (development baseline)
- Escalation path when lower-level boards cannot reach consensus
- Three documented steps: screening (completeness check), impact analysis, disposition
  (approve/defer/reject with documented basis)

[web-nasa-swe082-2026]

The ASPICE process note (SUP.10.BP3 Note 6) also states: "Prioritization of change requests
may be done by allocation to releases." This connects change control to release management —
not every approved change needs to be implemented immediately; changes can be batched into
future releases, which is essential for safety-critical development where re-verification cost
is high. [src-aspice-4-0 §4.8.4, p.86]

### 1.5 Impact Analysis Before Approval

Impact analysis is the core intellectual work of the CCB. ASPICE SUP.10.BP2 requires analyzing
"work products affected by the change request" and determining "dependencies to other change
requests." The impact is assessed including resource requirements, scheduling issues, risks, and
benefits. [src-aspice-4-0 §4.8.4, SUP.10.BP2, p.86]

NASA's requirements management guidance specifies the scope of impact assessment: changes must
be evaluated for their effects on "cost, schedule, architecture, design, interfaces, ConOps,
and higher and lower level requirements." [web-nasa-reqmgmt-2026]

This multi-domain scope is the reason CCBs need cross-functional membership. A change to a
timing requirement may look simple but require changes to: the architecture (resource allocation),
software (algorithm redesign), tests (test cases and test infrastructure), and safety analysis
(failure rate recalculation). Evaluating all of these independently before approving the change
is the difference between managed change and requirements thrash.

ASPICE SYS.1.BP3 specifically requires this for stakeholder requirement changes: "Analyze all
changes against the baseline. Assess impact and risks. Initiate appropriate change control and
mitigation actions." [src-aspice-4-0 §4.5.1, SYS.1.BP3, p.35]

### 1.6 Configuration Management as the Foundation

Change control sits on top of configuration management (SUP.8). Configuration management
establishes the infrastructure that makes change control possible: it identifies what is under
control (BP1: Identify configuration items), defines their properties including status model
(BP2), controls modifications (BP4), establishes baselines (BP5), and ensures completeness and
consistency of baselines (BP7).

ASPICE Annex B defines Configuration Item properties: "A status model (e.g., Under Work,
Tested, Released, etc.), storage location, access rights, etc." [src-aspice-4-0 Annex B,
item 16-03, p.139; SUP.8.BP2, Note 5, p.81]

Without a defined status model for configuration items, there is no way to enforce the
"approved before implementation" requirement of SUP.10.BP3. The status model is the mechanism
that makes the CCB gate effective.

---

## 2. Derived Requirements

### 2.1 Definition

A derived requirement is a requirement that is not directly traceable to a higher-level
requirement. It arises during design, analysis, or implementation as a consequence of choices
made at the current level — not as a decomposition of a parent requirement.

DO-178C defines derived requirements as software requirements "not directly traceable to
higher-level requirements." [web-search-derived-req-2026, citing DO-178C]

The distinction matters structurally: a normal requirement can be traced upward to a stakeholder
need or system requirement that justifies its existence. A derived requirement cannot. Its
justification lies in the design decision or constraint that produced it, not in a parent
requirement. This makes it opaque to anyone reviewing only the requirements hierarchy.

### 2.2 When Derived Requirements Arise

Derived requirements arise whenever an engineering decision at one level creates an obligation
not anticipated at the level above. Common sources:

- **Architecture decisions**: A decision to use a specific bus protocol creates timing
  requirements on all components using the bus. These requirements were not in the system
  requirements; they are derived from the architecture choice.

- **Safety mechanisms**: A decision to add a watchdog timer creates requirements on software
  response time that do not trace to any stakeholder need — they trace to the safety design
  decision.

- **Partitioning**: A decision to partition two functions on separate processors creates
  requirements on inter-processor communication latency that were not in the system requirements.

- **Implementation constraints**: Choosing a specific RTOS creates memory alignment
  requirements that the system requirements never mentioned.

- **Good practice adoption**: A team may add error logging requirements as local practice even
  though no stakeholder required it. These are "self-derived" requirements. [web-nasa-reqmgmt-2026]

### 2.3 The Danger: Safety Impact Not Visible at the Level of Origin

The fundamental risk with derived requirements is that they can introduce safety hazards that
were not analyzed at higher levels, precisely because they are invisible in the upward
requirements chain.

From the DO-178C / ARP 4754A community: "When the processes of DO-254 and DO-178C create new
derived requirements, they must feed these requirements back up to the system (ARP 4754A) and
safety (ARP 4761) processes to ensure they do not adversely affect safety." [web-search-derived-req-2026]

Furthermore: "A safety engineer must review all software derived requirements and their
rationale to determine if there is an impact to safety (i.e., could the derived requirement
cause loss of function resulting in additional pilot workload or provide misleading information
to the pilots)." [web-search-derived-req-2026]

This review is not optional in safety-critical domains. It is the mechanism that closes the
loop between what lower levels decided and what the safety case at higher levels assumed.

### 2.4 The Feedback Loop in Practice

The feedback loop for derived requirements follows this path:

```
Software team creates derived requirement
        │
        ↓
Derived requirement documented with rationale
(WHY it was introduced — what design decision created it)
        │
        ↓
Safety engineer reviews: could this affect a safety function?
Does it reduce fault tolerance? Create a new failure mode?
Impose a constraint the PSSA/SSA did not account for?
        │
    ┌───┴────────────────────────┐
    │ No safety impact           │ Safety impact identified
    ↓                            ↓
Accepted, documented         SSA/FTA updated
in derived reqs list         Safety requirements revised if needed
                             ARP 4754A objectives re-checked
                             If system requirement changes needed → CCB
```

In ARP 4754A terms, this is captured in objective 4.4: derived requirements from item
development must be evaluated against system-level safety objectives. [src-peterson-arp4754a-2015
Table 6, pp. 44-46, cited from prior research session]

### 2.5 Concrete Examples of Derived Requirements Creating Safety Issues

The following examples illustrate how derived requirements create safety exposure when the
feedback loop fails:

**Example 1: Timing assumption mismatch.** A software team introduces a derived requirement
that a sensor polling function runs every 20ms because that matches the RTOS scheduler period.
The PSSA assumed 10ms polling. The derived requirement creates a timing discrepancy that violates
the assumed fault detection latency. If not fed back to the safety team, the SSA will be
incorrect. [synthesis — pattern identified across web-search-derived-req-2026 and
src-peterson-arp4754a-2015 discussion of derived requirements objectives]

**Example 2: Memory partitioning.** A derived requirement to use a shared memory region for
inter-process communication appears to be an implementation detail. But if the two processes
are at different IDAL levels, the shared memory creates a coupling that invalidates the
independence assumed by the IDAL allocation. The FDAL/IDAL assignments may need revision.
[synthesis — pattern identified from src-peterson-arp4754a-2015 §4 FDAL/IDAL discussion and
derived requirements objectives]

**Example 3: Error handling mode.** Software adds a derived requirement to enter a degraded
mode on CRC failure. This "safe state" transition was not in the system requirements. If the
degraded mode has effects on aircraft or vehicle behavior that were not analyzed in the FHA,
the derived requirement has introduced an unanalyzed failure condition. [synthesis]

### 2.6 The Cross-Domain Universal Pattern

The derived requirements feedback loop is universal across all three major V-model standards:

| Standard | Mechanism |
|---|---|
| DO-178C / ARP 4754A | Derived HLRs and LLRs reviewed by safety engineer; fed back to ARP 4754A objective 4.4 and ARP 4761 SSA update |
| ISO 26262 | Derived SW requirements in Part 6 reviewed against TSC (Part 4); potential impacts on ASIL allocation and HSI specification |
| ASPICE | SUP.10 bidirectional traceability between change requests and work products; SYS.1.BP3 change impact analysis |

In ASPICE, there is no specific "derived requirements" terminology, but the same obligation
exists through change impact analysis: when a SW team introduces a new requirement during SWE.1
that was not allocated from SYS.2, it is effectively a derived requirement. The traceability
gap — a SWE.1 requirement with no parent in SYS.2 — is exactly what assessors look for as a
finding. [synthesis from src-aspice-4-0 traceability notes and prior research 01-standards]

---

## 3. Traceability in Practice

### 3.1 The Foundational Definition: Gotel & Finkelstein 1994

The seminal paper on requirements traceability is Gotel & Finkelstein's 1994 "An Analysis of
the Requirements Traceability Problem" (ICRE 1994, pp. 94–101). Based on empirical studies
involving over 100 practitioners, it defined the requirements traceability problem and introduced
the pre-RS / post-RS distinction. [unverified-full-text: full paper text not retrieved; findings
from Semantic Scholar abstract and web search results; paper available at
discovery.ucl.ac.uk/id/eprint/749/]

**Key finding:** The majority of problems attributed to poor requirements traceability are due
to inadequate pre-RS traceability — not the more commonly addressed post-RS traceability.
[unverified-full-text: Gotel & Finkelstein 1994]

### 3.2 Pre-RS vs Post-RS Traceability

Gotel & Finkelstein split requirements traceability at the requirements specification (RS) document:

**Pre-RS traceability** concerns the life of a requirement before it appears in the requirements
specification: its origin (stakeholder interviews, meeting minutes, legacy documents, business
rules), the context that motivated it, the decisions made during elicitation, and the people
responsible for it. Pre-RS traceability answers "where did this requirement come from and why
does it exist?"

**Post-RS traceability** concerns the life of a requirement after it appears in the specification:
allocation to architecture, refinement into lower-level requirements, implementation in code,
and verification. Post-RS traceability answers "where was this requirement realized and tested?"

The industry focus has been almost entirely on post-RS traceability — the requirement-to-code-to-test
chain. This is the chain that compliance standards (DO-178C, ASPICE, ISO 26262) mandate.
Pre-RS traceability — the chain from requirement back to its origin — is rarely automated and
rarely maintained. [unverified-full-text: Gotel & Finkelstein 1994; corroborated by
web-sebok-reqmgmt-2026 noting traceability links to "operational scenarios" as a separate
RM activity]

### 3.3 Why Pre-RS Traceability Matters

Pre-RS traceability matters for three reasons that become acute during change control:

**1. Rationale recovery.** When a requirement appears to conflict with a proposed change, the
team must know why the requirement exists. Without pre-RS traceability, the team either has
to reconstruct the rationale (expensive) or accept the requirement blindly (dangerous). If the
rationale was "legacy system constraint that no longer applies," the requirement may legitimately
be deleted. If it was "regulatory mandate," it cannot.

**2. Impact of stakeholder change.** If a stakeholder's organization or role changes, post-RS
traceability will not reveal which requirements they owned. Pre-RS traceability to the source
stakeholder allows the team to identify which requirements need re-validation with the new
stakeholder.

**3. Derived requirements justification.** The rationale for a derived requirement is pre-RS
information — it is the design decision that created it. Without pre-RS traceability of derived
requirements, there is no way to determine whether the derived requirement is still valid if
the design decision changes.

[synthesis from Gotel & Finkelstein 1994 findings and src-aspice-4-0 rationale requirements]

### 3.4 ASPICE Traceability Architecture

ASPICE v4.0 requires bidirectional traceability across every engineering level boundary,
implemented through dedicated base practices in each process:

**System level:**
- SYS.2.BP5: between system requirements and stakeholder requirements
- SYS.3.BP4: between architecture elements and system requirements
- SYS.4.BP4: (integration verification — between integration results and system architecture)
- SYS.5.BP4: (system verification — between verification measures and system requirements)

**Software level:**
- SWE.1.BP5: between SW requirements and system requirements
- SWE.2.BP4: between SW architecture and SW requirements
- SWE.3.BP4: between detailed design and SW architecture
- SWE.4.BP4: between unit verification and detailed design
- SWE.5.BP6: (integration verification)
- SWE.6.BP4: (SW verification)

[src-aspice-4-0 Annex C.5, p.148]

The ASPICE standard includes an important caveat, repeated consistently across traceability
practices: "Traceability alone does not necessarily mean the information is consistent with
each other." [src-aspice-4-0 §4.5.2, SYS.2.BP5, Note 7, p.37; also SYS.3.BP4, HWE.1.BP5,
HWE.2.BP5, HWE.3.BP5, HWE.4.BP5, SUP.10.BP4]

This is a design principle, not a disclaimer: trace links are the infrastructure for
consistency checking, not a substitute for it.

### 3.5 Bidirectional Traceability: Two Directions Serve Different Purposes

Bidirectional traceability means maintaining links in both directions. The two directions
serve fundamentally different purposes:

**Forward traceability** (requirement → design → code → test):
- Demonstrates that every requirement has been implemented
- Supports completeness checking ("does the architecture address all requirements?")
- Supports verification coverage ("has every requirement been tested?")
- Used during development: "what work items does this requirement drive?"

**Backward traceability** (test → code → design → requirement → stakeholder need):
- Demonstrates that every implemented element serves a requirement
- Detects gold-plating (implementation without requirement)
- Supports impact analysis ("if I change this requirement, what breaks?")
- Used during change control: "what would change if this requirement were modified?"

[synthesis from src-aspice-4-0 traceability notes; web-nasa-reqmgmt-2026 definition of
bidirectional traceability; web-sebok-sysreqdef-2026 traceability section]

### 3.6 The Traceability Overhead Problem

The industry perception that traceability creates overhead without proportional value is
well-documented. The economic problem is that the costs of traceability (creating and
maintaining links) are immediate and visible, while the benefits (faster change impact
analysis, fewer integration surprises) are deferred and less visible.

Key findings from the empirical literature:

- "Developers think that traceability costs more than it delivers." [web-search-traceability-2026,
  citing literature review findings]
- One empirical study found developers implementing traceability "performed a given task 24%
  faster and created 50% more correct solutions on average" compared to those without.
  [web-search-traceability-2026; specific study citation not independently verified — [unverified]]
- "60–80% of systems engineering rework comes from unclear, missing, or outdated requirements."
  [web-321gang-traceability-2026; original source not independently verified — [unverified]]

The key distinction in the literature between useful traceability and overhead:

| Useful traceability | Overhead traceability |
|---|---|
| Links maintained in sync with artifacts | Links created once, never updated |
| Automated checking in CI pipeline | Manual link verification at audit time |
| Links carry semantic content (type, rationale) | Links are binary (present/absent) |
| Used by engineers during development | Used only by auditors during compliance checks |
| Enables automated impact analysis | Requires manual matrix traversal |
| Proportional to risk level | Applied uniformly regardless of criticality |

[synthesis from web-321gang-traceability-2026; web-search-traceability-2026;
src-aspice-4-0 traceability notes]

### 3.7 Traceability vs Consistency

The ASPICE caution — that trace links do not guarantee consistency — has a practical implication:
a project can have 100% bidirectional traceability and still have requirements that contradict
each other or architecture elements that do not actually satisfy their traced requirements.

The trace link establishes a claim ("this architecture element satisfies this requirement").
The claim must be verified. The trace link is not the verification — it is the pointer to what
must be verified.

This distinction matters for tool users: a green traceability matrix means "we have documented
all the claimed relationships." It does not mean "we have validated that those relationships
hold." Validation requires review, analysis, or test. The trace matrix is the input to that
activity, not the output.

[src-aspice-4-0 SYS.2.BP5 Note 7, p.37; SYS.3.BP4 Note, p.39; synthesis]

### 3.8 Monitoring Metrics for Traceability

INCOSE and SEBoK identify the following traceability-related metrics for requirements management:

- Number of requirements with unresolved TBD/TBR placeholders
- Number of untraced requirements (requirements without upward or downward links)
- Number of requirements without verification method assigned
- Verification/validation status per requirement
- Change request closure rate and cycle time

[web-sebok-reqmgmt-2026, attributed to INCOSE NRM v1.1]

---

## 4. Requirements Attributes

### 4.1 ASPICE Definition of Requirement Attribute (17-54)

ASPICE PAM v4.0 Annex B defines Requirement Attribute (information item 17-54) as:

> "Meta-attributes that support structuring and definition of release scopes of requirements.
> Can be realized by means of tools.
> Note: usage of requirements attributes may further support analysis of requirements."

[src-aspice-4-0 Annex B, item 17-54, p.140]

The definition is deliberately minimal — it does not prescribe specific attributes. The note
that attributes "may further support analysis of requirements" indicates they serve a dual
purpose: management (structuring, release scope) and analytical (impact analysis, prioritization).

ASPICE 17-54 appears as an output information item of:
- SYS.1 (Outcome 2, 3, 4) — stakeholder requirement attributes
- SYS.2 (Outcome 2, 3) — system requirement attributes
- SWE.1 (Outcomes 2, 3) — software requirement attributes
- HWE.1 (Outcome 2) — hardware requirement attributes

This makes requirement attributes a universal artifact type across the entire left side of the
V, not just at one level. [src-aspice-4-0 pp.35-39, 71-72]

### 4.2 ASPICE Standard Reference for Characteristics

ASPICE SYS.2.BP1 references ISO/IEC IEEE 29148, ISO 26262-8:2018, or INCOSE GtWR as sources
for "defined characteristics" of requirements. Examples given: "verifiability, verification
criteria being inherent in the text, unambiguity/comprehensibility, freedom from design and
implementation, not contradicting any other requirement." [src-aspice-4-0 §4.5.2, SYS.2.BP1,
p.36]

These are quality characteristics, distinct from management attributes. The two categories
serve different purposes:

- **Quality characteristics** (verifiability, unambiguity, etc.) — properties of the requirement
  text itself, assessed during requirements review
- **Management attributes** — metadata applied to requirements to support process activities

### 4.3 Attribute Taxonomy: Essential vs. Supporting

Drawing from INCOSE guidance, NASA practice, and ASPICE:

**Essential attributes** (required for any safety-critical or process-assessed development):

| Attribute | Purpose | Standard Reference |
|---|---|---|
| Unique identifier (ID) | Stable reference across tools, documents, and discussions | ASPICE assessors finding: "Missing IDs" [01-standards] |
| Status | Current lifecycle state of the requirement (draft, agreed, baselined, obsolete) | SUP.8 status model [src-aspice-4-0]; NASA 6.2 [web-nasa-reqmgmt-2026] |
| Verification method | How the requirement will be verified (inspection, analysis, test, demonstration) | SYS.2.BP1 characteristics [src-aspice-4-0]; NASA bidirectional traceability [web-nasa-reqmgmt-2026] |
| Traceability (parent) | Link to the higher-level requirement or stakeholder need from which this requirement was derived | SYS.2.BP5 [src-aspice-4-0]; DO-178C derived reqs [web-search-derived-req-2026] |
| Source | Who originated the requirement (stakeholder, standard, safety analysis, architecture decision) | ASPICE SYS.1.BP1 Note: "Documenting the stakeholder or source of a requirement supports agreement and change analysis" [src-aspice-4-0 §4.5.1, p.35] |
| Rationale | Why the requirement exists (the problem being solved) | Pre-RS traceability substitute; supports change impact; INCOSE SE Handbook [web-sebok-reqmgmt-2026] |

**Supporting attributes** (valuable but not universally mandatory):

| Attribute | Purpose |
|---|---|
| Priority | Supports release scope definition and trade-off analysis; linked to ASPICE 17-54 "definition of release scopes" |
| Stability / Volatility | Flags requirements likely to change; supports architecture decisions that need to absorb change |
| Safety classification / DAL / ASIL | Links requirement to the safety integrity level it must be developed to |
| Responsible person / Owner | Accountability for the requirement; enables stakeholder communication when re-validation needed |
| Criticality | Distinguishes requirements whose failure would cause system failure from those whose failure is merely degrading |
| TBD/TBR flag | Tracks open unknowns; closure tracked as a health metric [web-sebok-reqmgmt-2026] |

[synthesis from src-aspice-4-0 Annex B items 17-00, 17-54; web-sebok-reqmgmt-2026 attributed to
INCOSE NRM v1.1; web-nasa-reqmgmt-2026; web-tracespace-reqmgmt-2026]

### 4.4 The Rationale Attribute: Special Importance

Rationale is the attribute most commonly omitted and most costly to recover. It records why
the requirement was written — the problem being solved, the assumption being made, or the
decision that drove the requirement's content.

Rationale is the primary pre-RS traceability substitute when a full audit trail to the original
stakeholder context is not maintained. Without rationale, every change requires a stakeholder
conversation to recover context that should have been captured at authoring time.

ASPICE's SYS.1.BP1 note — "Documenting the stakeholder or source of a requirement supports
agreement and change analysis" [src-aspice-4-0 §4.5.1, p.35] — is the closest ASPICE comes
to mandating rationale. The NASA SE Handbook notes that rationale "communicates why the
requirement is needed, any assumptions made, the source of numbers, the results of related
design studies, or any other related supporting information." [web-sebok-reqmgmt-2026,
attributed to INCOSE]

### 4.5 Safety Classification as a Special Attribute

In safety-critical domains, safety classification (the ASIL, DAL, or SIL attributed to a
requirement) is effectively mandatory, not supporting. It determines the rigor of development
and verification activities applied to the requirement and its implementation.

In ASPICE, this manifests as Special Characteristics (17-57) and flows from safety analysis
processes. But at the requirement level, the safety classification attribute establishes the
development rigor requirement. Requirements without safety classification in an ISO 26262 or
DO-178C project create an ambiguity about what rigor to apply. [synthesis from src-aspice-4-0
Annex B items 17-57, 17-54; prior research 01-standards ARP 4754A FDAL/IDAL]

---

## 5. Requirements Volatility

### 5.1 Definition and Measurement

Requirements volatility measures the rate and magnitude of change to requirements after
baseline. Common metrics:

- **Change rate**: number of requirements changed / total requirements per unit time
- **Churn**: number of requirements added + modified + deleted per milestone
- **TBD closure rate**: rate at which "To Be Determined" placeholders are resolved
- **Derived requirement emergence rate**: frequency of new derived requirements appearing
  (signals architectural decisions being made without upstream alignment)

[web-sebok-reqmgmt-2026 (TBD metric); synthesis]

### 5.2 Empirical Findings on Volatility Impact

Zowghi & Nurmuliani (empirical study, multiple publications 2002–2005) found that requirements
volatility has a significant impact on schedule overrun and cost overrun in software projects,
particularly when changes are introduced at later phases. Adding new requirements at later
phases is "considered a high risk because it will cost the organization in terms of budget
overruns or schedule delays." [unverified-full-text: Zowghi & Nurmuliani, cited from web
search summary]

Regarding commonly cited thresholds: a monthly growth rate of 5% is conventionally considered
a critical failure factor, but empirical data shows more than 21% of successful projects
exceeded this rate. Context — project size, duration, and type — matters significantly for
interpreting volatility rate. [unverified-full-text: search result summary of "Quantifying
Requirements Volatility Effects," cs.vu.nl/~x/qrv/qrv.pdf]

### 5.3 What High Volatility Signals

High requirements volatility can signal either upstream process failure or healthy evolution,
depending on context:

**Signals of upstream problems:**
- High volatility in early phases on a well-understood problem space suggests elicitation
  was incomplete or the wrong stakeholders were engaged
- High volatility after the SRR baseline suggests requirements were not sufficiently analyzed
  before being baselined — the "agreed" status was premature
- Volatility concentrated in safety-critical requirements is particularly dangerous: each
  change triggers re-analysis of the safety case
- Volatility on interface requirements propagates widely: every component that touches the
  interface must be re-verified

**Signs of healthy evolution:**
- Volatility in early pre-baseline phases is expected and desirable — it means the process
  is discovering and refining understanding
- Volatility driven by genuine external constraints (regulatory changes, customer contract
  changes) is not a process failure
- Volatility that drives clean change requests through the CCB (with proper impact analysis)
  is controlled volatility — expensive but managed

[synthesis from web-sebok-reqmgmt-2026 change management section; Zowghi & Nurmuliani
findings; NASA requirements management guidance]

### 5.4 Managing Volatility: Stability as a Requirement Attribute

Marking requirements with a stability attribute (high/medium/low, or expected-stable/volatile)
during elicitation creates visibility into where volatility is expected. Architecture teams can
use this information to design in changeability where requirements are known to be volatile —
isolating volatile requirements from stable ones, avoiding tight coupling to requirements that
may change.

This is the architectural response to requirements volatility: not to eliminate volatility but
to absorb it gracefully. If volatile requirements are localized in the architecture, their
changes do not cascade. If volatile requirements are woven throughout the architecture, every
change becomes a system-wide re-work. [synthesis from web-sebok-sysreqdef-2026 stability
section; web-sebok-reqmgmt-2026 attributes]

---

## 6. The Requirements-to-Architecture Handoff

### 6.1 The SYS.2 → SYS.3 Transition

The handoff from SYS.2 (System Requirements Analysis) to SYS.3 (System Architectural Design)
is not a gate that can be passed with an incomplete requirements set. SYS.3 takes system
requirements as its primary input — its purpose is to "establish an analyzed system
architecture consistent with the system requirements." Without a stable, analyzable requirements
set, architecture cannot proceed meaningfully.

The ASPICE definition of what SYS.3 requires as input is implicit in its base practices:
SYS.3.BP1 specifies the architecture "with respect to functional and non-functional system
requirements." SYS.3.BP2 specifies dynamic aspects "with respect to functional and non-functional
system requirements." SYS.3.BP4 requires consistency and traceability between architecture
elements and system requirements. [src-aspice-4-0 §4.5.3, SYS.3, pp.38-39]

If requirements are still changing when architecture work begins, architectural decisions are
being made on unstable ground. The architecture will be built to a moving target.

### 6.2 What Must Be True of Requirements Before Architecture Begins

Drawing from ASPICE SYS.2 outcomes, NASA practice, and SEBoK, the requirements set must
satisfy the following criteria before architecture work begins:

**Completeness criteria:**

1. All agreed scope is covered — no major functional areas left undescribed
2. All stakeholder requirements have been analyzed for system-level implications (SYS.2.BP3:
   "analyze including interdependencies to ensure correctness, technical feasibility")
3. All TBD/TBR placeholders in safety-critical or architecturally significant requirements
   have been resolved
4. Safety requirements derived from the safety analysis (FHA/HARA/PSSA) have been incorporated
   as system requirements [src-peterson-arp4754a-2015 §4; prior research 01-standards]
5. Interface requirements have been specified — what the system must provide to and receive
   from adjacent systems [SYS.3.BP1 expects "external interfaces"]

**Stability criteria:**

6. Requirements have been agreed by all affected parties (SYS.2 Outcome 6:
   "System requirements are agreed and communicated to all affected parties")
7. Requirements have been baselined (entered under configuration management — SUP.8.BP5)
8. Identified volatile requirements have been explicitly flagged so the architecture team
   knows where to design for changeability
9. Pending changes have been catalogued through SUP.10 so the architecture team knows what
   is not yet stable

**Analyzability criteria:**

10. Requirements are written to defined quality characteristics (verifiable, unambiguous, etc.)
    per SYS.2.BP1 — unverifiable requirements cannot have architecture elements traced to them
11. Requirements are structured and prioritized (SYS.2 Outcome 2) — architecture decisions
    involve trade-offs; without priorities, no principled trade-off is possible
12. The impact on the system context has been analyzed (SYS.2 Outcome 4: "impact of system
    requirements on the operating environment is analyzed") — the architecture must accommodate
    the operational environment

[src-aspice-4-0 §4.5.2, SYS.2, pp.36-37; web-sebok-sysreqdef-2026; web-nasa-reqmgmt-2026;
synthesis]

### 6.3 The Information the Architecture Process Receives

SYS.3 receives from SYS.2 the following information items:

- **17-00 Requirement** — the set of system requirements (all of them)
- **17-54 Requirement Attribute** — the management metadata (status, priority, safety
  classification, stability flags)
- **15-51 Analysis Results** — the technical feasibility analysis and impact analysis of
  requirements on the system context
- **13-51 Consistency Evidence** — evidence that the requirements set is internally consistent
  and consistent with stakeholder requirements
- **13-52 Communication Evidence** — evidence that requirements have been agreed by affected
  parties

[src-aspice-4-0 §4.5.2, SYS.2 output information items, p.37]

The Requirement Attribute (17-54) deserves emphasis: it carries the management state of the
requirements. The architecture team needs to know which requirements are still volatile (to
design for changeability), which are at a higher safety classification (to drive partitioning
decisions), and which have priority for the current release scope (to decide what must be
addressed immediately vs. deferred).

### 6.4 The SYS.2 Note 8 Carve-Out: Process Requirements

ASPICE SYS.2.BP5 Note 8 contains an important qualification: "There may be non-functional
stakeholder requirements that system requirements do not trace to — these are process
requirements, still subject to verification." [src-aspice-4-0 §4.5.2, SYS.2.BP5, Note 8
(paraphrased from Note 7 in prior research; Note 8 = 'non-functional stakeholder requirements
that system requirements do not trace to are process requirements')]

This means: not all stakeholder requirements flow through system requirements to architecture.
Requirements like "the supplier shall use ASPICE Level 2 processes" are process requirements
that govern how development happens, not what the system does. They do not trace to system
requirements and do not drive architecture. The architecture team needs to know which
requirements are in this category so they are not expected to address them.

[src-aspice-4-0 §4.5.2, SYS.2.BP5 note]

### 6.5 What the Architecture Process Must Not Start Without

The negative formulation is sometimes clearer:

**Architecture cannot proceed validly if:**
- The scope of system functions is still being negotiated with stakeholders
- Safety analysis (HARA/FHA) is not yet complete — safety requirements are still unknown
- Interface requirements to external systems are TBD — the system boundary is undefined
- Requirements have not been agreed by the customer — any agreed architecture may be thrown
  away when the customer re-negotiates
- Requirements are not under configuration management — any architecture decision may become
  invalid when an uncontrolled requirement change occurs

**Architecture work that proceeds under these conditions is valid for:**
- Feasibility exploration (rapid prototyping / concept work)
- Constraining and informing the ongoing requirements analysis (SYS.3 feeds back to SYS.2)

But it is not valid as the SYS.3 artifact that serves as the input to SWE.1/HWE.1. The
architecture that the software and hardware teams receive must be based on a stable,
agreed, baselined requirements set.

[synthesis from src-aspice-4-0 SYS.2-SYS.3; web-nasa-reqmgmt-2026; web-sebok-sysreqdef-2026]

### 6.6 The Iterative Reality

In practice, SYS.2 and SYS.3 are not strictly sequential. Architecture exploration informs
requirements refinement; requirements analysis constrains architecture options. ASPICE does
not prescribe a specific ordering of processes or base practices within a process — it operates
at the "WHAT" level. [src-aspice-4-0 §3.3.3, p.27]

The practical rule is: iteration is acceptable during the design phase, but must converge to
a stable baseline before the handoff to the domain engineering teams (SWE.1, HWE.1). Each
iteration between SYS.2 and SYS.3 should progressively tighten both the requirements
specification and the architectural design. Once the SWE.1 team begins, they need a stable
SYS.2 baseline and a stable SYS.3 baseline — otherwise their allocated requirements will be
moving targets.

[synthesis from src-aspice-4-0 §3.3.3 WHAT-level note; prior research 01-standards ARP 4754A
iterative process model]

---

## 7. Cross-Topic Summary: The Management Spine

All six topics in this research document connect through a single spine:

```
Stakeholder needs
    │
    ↓ [elicitation + analysis → SYS.1/SYS.2]
Requirements set with attributes (status, source, rationale, safety classification)
    │
    ↓ [agree + baseline → SUP.8]
Baselined requirements (under configuration control)
    │
    ├──→ [any change] → Change Request (13-16) → CCB impact analysis → approve/reject
    │                       ↑
    │         [derived requirement created downstream → safety review → feed back here]
    │
    ↓ [completeness + stability verified]
Handoff to SYS.3 (architecture)
    │
    ↓ [allocation to SWE.1, HWE.1]
Domain engineering begins (on stable input)
```

The quality of the management spine determines how much downstream rework occurs. Every break
in this spine — missing rationale, no CCB, untriaged derived requirements, premature handoff
with open TBDs — propagates as defects, re-work, or undetected safety gaps into lower levels
of the V.

---

## 8. What This Research Covers vs. What's Missing

### Covered:
- [x] Baselines: definition, when to baseline, ASPICE 13-08, NASA milestones
- [x] Change control: SUP.10 process, CCB structure, impact analysis scope
- [x] Configuration management as foundation: SUP.8 base practices
- [x] Derived requirements: definition, when they arise, the safety feedback loop, examples
- [x] Cross-domain pattern for derived requirements (DO-178C, ISO 26262, ASPICE)
- [x] Traceability: Gotel & Finkelstein pre-RS/post-RS, ASPICE traceability architecture
- [x] Traceability vs consistency distinction (ASPICE note)
- [x] Traceability overhead problem and useful vs ceremonial traceability
- [x] Requirements attributes: ASPICE 17-54, essential vs supporting taxonomy
- [x] Rationale attribute special importance
- [x] Requirements volatility: metrics, empirical findings, signals, management
- [x] Requirements-to-architecture handoff: completeness criteria, stability criteria,
      analyzability criteria, information items transferred
- [x] The SYS.2 → SYS.3 information contract
- [x] Iterative reality and convergence requirement

### NOT covered (limits of accessible sources):
- [ ] IEEE 828 configuration management standard — paywalled
- [ ] NPR 7150.2 specific SWE requirements (had binary PDF only; NASA web handbook used)
- [ ] ISO/IEC 29148 requirements management process model — paywalled
- [ ] INCOSE GtWR full attribute list with guidance — paywalled
- [ ] Quantitative data on CCB meeting cadence or approval cycle times in practice
- [ ] Tool-specific traceability implementation patterns (DOORS, Polarion, Jama)
- [ ] The "requirements completeness metrics" literature (Natt och Dag et al.) — not fetched
- [ ] Formal studies of CCB effectiveness in safety-critical programs

---

## Sources

### Primary sources (read from raw files in this or prior sessions)

- **[src-aspice-4-0]** ASPICE PAM v4.0, VDA QMC WG13, 2023.
  `raw/standards/Automotive-SPICE-PAM-v40.pdf`
  - pp. 34-39: SYS.1, SYS.2, SYS.3 base practices (in prior session, cited from 01-standards)
  - pp. 81-82: SUP.8 Configuration Management (read this session)
  - pp. 85-86: SUP.10 Change Request Management (read this session)
  - p. 134: 13-08 Baseline definition (read this session)
  - p. 135: 13-16 Change Request characteristics (read this session)
  - p. 139: 17-00 Requirement characteristics (read this session)
  - p. 140: 17-54 Requirement Attribute definition (read this session)
  - p. 148: Annex C.5 traceability overview (cited from prior codex wiki page)

- **[src-peterson-arp4754a-2015]** Peterson, NASA/CR-2015-218982, November 2015.
  `raw/papers/peterson-arp4754a-nasa-2015.pdf` pp. 1-8 (read in prior session).
  Derived requirements objectives (Table 6 objective 4.4), industry practice findings (§5).

### Secondary sources (web-fetched this session)

- **[web-nasa-reqmgmt-2026]** NASA SE Handbook §6.2 "Requirements Management."
  https://www.nasa.gov/reference/6-2-requirements-management/ (fetched 2026-04-12)
  CCB structure, bidirectional traceability definition, derived/self-derived requirements,
  change impact scope, requirements creep prevention techniques.

- **[web-nasa-swe082-2026]** NASA SWE-082 "Authorizing Changes."
  https://swehb.nasa.gov/spaces/7150/pages/16450445/SWE-082+-+Authorizing+Changes
  (fetched 2026-04-12)
  Multi-level CCB structure, safety personnel involvement, three-step authorization process.

- **[web-sebok-sysreqdef-2026]** SEBoK "System Requirements Definition."
  https://sebokwiki.org/wiki/System_Requirements_Definition (fetched 2026-04-12)
  Completeness and stability criteria, TBX tracking, traceability definition, handoff to
  architecture. Content attributed to INCOSE NRM v1.1 per SEBoK source notes.

- **[web-sebok-reqmgmt-2026]** SEBoK "Requirements Management."
  https://sebokwiki.org/wiki/Requirements_Management (fetched 2026-04-12, partial content)
  Attributes list, baselines, change management drivers, monitoring metrics.
  Attributed to INCOSE NRM v1.1 and GtNR v1 (2022).

- **[web-321gang-traceability-2026]** 321Gang LLC "The Hidden Cost of Poor Traceability."
  https://321gang.com/hidden-cost-of-poor-traceability/ (fetched 2026-04-12)
  Practitioner article. Statistics (60–80% rework, 50% reduction in integration surprises)
  cited without primary source; marked [unverified] in text.

- **[web-tracespace-reqmgmt-2026]** Trace.space "What is Requirements Management?"
  https://www.trace.space/blog/what-is-requirements-management (fetched 2026-04-12)
  Milestone baseline list, cost statistics (70–80% manufacturing cost locked by end of
  conceptual design, 97% success rate with documented requirements, 50% rework). Statistics
  cite 2024 Engprax/J.L. Partners and PMI 2014 — not independently verified; marked [unverified].

- **[web-wikipedia-ccb-2026]** Wikipedia "Change Control Board."
  https://en.wikipedia.org/wiki/Change_control_board (fetched 2026-04-12)
  CCB definition, membership, process. Article flagged as needing additional references.

### Search-extracted findings (primary papers not fetched)

- **Gotel, O.C.Z & Finkelstein, A.C.W. (1994)** "An Analysis of the Requirements Traceability
  Problem." Proceedings of 1st International Conference on Requirements Engineering (ICRE),
  Colorado Springs, April 18-22, pp. 94-101.
  Available at: https://discovery.ucl.ac.uk/id/eprint/749/
  Full text not fetched (403 error). Key findings extracted from Semantic Scholar abstract and
  web search summaries. All claims from this paper marked [unverified-full-text].

- **Zowghi, D. & Nurmuliani, N.** (multiple publications 2002-2005) empirical studies on
  requirements volatility and project performance.
  Full texts not fetched. Findings from web search summaries.
  Marked [unverified-full-text] in text.

- **Web search findings on derived requirements** (DO-178C, ARP 4754A)
  from: afuzion.com/avionics-software-requirements-in-do-178c/,
  thinkmind.org/articles/icsea_2012_15_20_10380.pdf (binary PDF),
  wikipedia DO-178C article.
  Marked [web-search-derived-req-2026] in text.
