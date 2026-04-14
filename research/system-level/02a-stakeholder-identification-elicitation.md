# Research 2a: Stakeholder Identification, Classification, and Needs Elicitation

Research for upper V documentation (backlog items 3.4, 3.5). This document covers the
craft of stakeholder engineering: how to find stakeholders, how to classify them, and
how to extract their needs before any requirements are written. It is the foundational
layer that makes everything else in requirements engineering trustworthy.

**Scope boundary:** This document covers elicitation craft — the techniques and
frameworks for finding stakeholders and capturing their needs. For what standards
*require* at this layer see Research 2d. For ConOps as a framing device see Research 2c.
For needs validation after capture see Research 2b.

**Sources used:**

| ID | Source | Status |
|----|--------|--------|
| [src-alexander-2005] | Ian F. Alexander, "A Taxonomy of Stakeholders: Human Roles in System Development," *International Journal of Technology and Human Interaction* Vol. 1 No. 1, 2005, pp. 23–59 | Read via web fetch of full paper text at scenarioplus.org.uk |
| [src-alexander-2004] | Ian F. Alexander, "A Better Fit — Characterising the Stakeholders," REBPS Workshop at CAiSE'04, Riga, Latvia, 2004 | Read via web fetch of full paper text at scenarioplus.org.uk |
| [src-mitchell-1997] | R.K. Mitchell, B.R. Agle, D.J. Wood, "Toward a Theory of Stakeholder Identification and Salience: Defining the Principle of Who and What Really Counts," *Academy of Management Review* Vol. 22 No. 4, 1997, pp. 853–886 | Confirmed via JSTOR and Semantic Scholar listings; full text at ronaldmitchell.org |
| [src-wiegers-beatty-2013] | Karl Wiegers and Joy Beatty, *Software Requirements*, 3rd ed., Microsoft Press, 2013 | Confirmed publication; content via secondary sources and Wiegers' own Medium article |
| [src-ieee-1362-1998] | IEEE Std 1362-1998, "IEEE Guide for Information Technology — System Definition — Concept of Operations (ConOps) Document," IEEE, 1998 (withdrawn; superseded by ISO/IEC/IEEE 29148) | Confirmed via IEEE Xplore listing |
| [src-29148-2018] | ISO/IEC/IEEE 29148:2018, "Systems and Software Engineering — Life Cycle Processes — Requirements Engineering" | Confirmed via ISO listing; content via SEBoK and secondary sources |
| [src-sebok-stakeholder-needs] | SEBoK wiki, "Stakeholder Needs Definition," sebokwiki.org, accessed 2026 | Read via web fetch |
| [src-sebok-glossary] | SEBoK wiki, "Stakeholder Needs and Requirements (glossary)," sebokwiki.org, accessed 2026 | Read via web fetch |
| [src-nuseibeh-2000] | Bashar Nuseibeh and Steve Easterbrook, "Requirements Engineering: A Roadmap," *ICSE 2000 Future of Software Engineering*, 2000, pp. 35–46 | Confirmed via cs.toronto.edu; PDF access failed but abstract and citations confirmed |
| [src-beyer-holtzblatt-1997] | Hugh Beyer and Karen Holtzblatt, "Contextual Design: Defining Customer-Centered Systems," Morgan Kaufmann, 1997 (also ACM Digital Library) | Confirmed via ACM DL listing |
| [src-wood-silver-1995] | Jane Wood and Denise Silver, *Joint Application Development*, 2nd ed., Wiley, 1995 | Confirmed via Amazon and publisher listings |
| [src-incose-nrm-2022] | INCOSE, *Needs and Requirements Manual*, 2022 | Referenced via SEBoK and INCOSE process model pages; paywalled |
| [src-kotonya-sommerville-1998] | Gerald Kotonya and Ian Sommerville, *Requirements Engineering: Processes and Techniques*, Wiley, 1998 | Confirmed via ACM DL and publisher listings |
| [src-reqi-conops] | reqi.io, "Concept of Operations (CONOPS) for Systems Engineers," accessed 2026 | Read via web fetch |
| [src-reqi-safety-req] | reqi.io, "What Makes a Requirement a Safety Requirement," accessed 2026 | Read via web fetch |
| [src-incose-process-model] | INCOSE Process Model, "Stakeholder Needs and Requirements Definition," incose.org interactive, accessed 2026 | Read via web search summary |

Claims from paywalled primary sources that could only be confirmed via secondaries are
marked **[secondary]**. Claims that could not be independently verified are marked
**[unverified]**.

---

## 1. Stakeholder Identification

### 1.1 The Core Problem: Stakeholders You Don't Know About

The common mistake in stakeholder identification is to start with the people who show
up in the first meeting and stop there. Whoever schedules the kickoff has power, and
power is not evenly distributed. The operator who will use the system daily, the
maintenance engineer who will repair it at 2am, the regulator who must approve it, and
the resident who will be harmed if it fails — none of these people are likely to be in
that first meeting.

Alexander articulates this precisely: the tendency is to "capture needs from limited
viewpoints while neglecting diverse stakeholder perspectives." The result is that
non-obvious roles are systematically missed. [src-alexander-2004]

The effect is not neutral. Missing a stakeholder at the identification stage means
missing their needs, which means the requirements document will be incomplete by
construction. In safety-critical systems, the missing stakeholders are frequently
the ones whose concerns are safety-related: regulators, maintenance personnel, and
people in adjacent systems who interact with the system at its operational boundary.

### 1.2 The Onion Model

The most practical published tool for systematic stakeholder identification is the
Onion Model, developed by Ian Alexander in collaboration with Suzanne and James
Robertson. The model was formalized in Alexander's 2005 taxonomy paper and in earlier
collaborative work with the Robertsons on the Volere framework.
[src-alexander-2005, src-alexander-2004]

The model uses four concentric rings centered on the system under development:

```
+--------------------------------------------------+
|  Wider Environment                               |
|  +--------------------------------------------+ |
|  |  Containing System                         | |
|  |  +--------------------------------------+  | |
|  |  |  Our System                          |  | |
|  |  |  +------------------------------+   |  | |
|  |  |  |  The Kit                     |   |  | |
|  |  |  |  (hardware + software)       |   |  | |
|  |  |  +------------------------------+   |  | |
|  |  +--------------------------------------+  | |
|  +--------------------------------------------+ |
+--------------------------------------------------+
```

**The Kit** — the hardware and software being built. Not a stakeholder; the thing being
designed. [src-alexander-2005]

**Our System** — the Kit plus the humans who operate it according to defined procedures.
Stakeholders here:
- **Normal Operator**: executes routine commands, monitors outputs. The person who
  presses the buttons. Often treated as the only stakeholder. [src-alexander-2005]
- **Maintenance Operator**: maintains hardware, diagnoses faults, restores operation.
  Alexander notes this role is "often underestimated; whole-life costs depend heavily
  on maintenance." [src-alexander-2005]
- **Operational Support**: help desk, trainers, advisors who maintain human effectiveness
  alongside system availability. [src-alexander-2005]

**The Containing System** — Our System embedded in a wider organization or process.
Stakeholders here:
- **Functional Beneficiary**: receives value from system outputs but does not operate
  the system directly. Example: astronomers using telescope data they did not collect.
  Alexander rates this the highest priority: "functional requirements form the
  specification centerpiece." [src-alexander-2005]
- **Interfacing System**: neighboring systems with protocol-level connections. Shifts
  in interface definitions create serious downstream risk. [src-alexander-2005]
- **Purchaser**: the organization paying for development, ranging from a product manager
  to a procurement officer. [src-alexander-2005]
- **Product Champion / Sponsor**: the person who initiated development and protects it
  from political pressure. Requires positional power to function effectively.
  [src-alexander-2005]

**The Wider Environment** — all remaining stakeholders. These are the ones most
frequently missed:
- **Negative Stakeholder**: harmed physically or financially by the system. Examples:
  residents near a railway route, conservation bodies, employees who perceive job loss.
  A special subtype is the **Hostile Agent** — a stakeholder who actively seeks to
  harm the system (hackers, competitors, industrial spies). [src-alexander-2005]
- **Political Beneficiary**: gains power or influence from system success. [src-alexander-2005]
- **Financial Beneficiary**: shareholders, investors, directors who profit financially.
  Often represented through surrogates. [src-alexander-2005]
- **Regulator**: responsible for certifying quality, safety, cost compliance. Acts as
  surrogate for the public interest. Alexander calls this "crucial for safety-related
  products." [src-alexander-2005]
- **Developer**: requirements engineers, designers, programmers, testers, safety
  specialists. Secondary priority to beneficiaries but must be included. [src-alexander-2005]
- **Consultant**: external experts (marketing, business analysis, safety, security).
  Timing of their involvement varies by domain. [src-alexander-2005]
- **Supplier**: manufacturers of components and sub-assemblies. May need early
  involvement when lead times are long. [src-alexander-2005]

**Why the layering matters:** The onion is not just a categorization scheme — it is a
checklist for gaps. Alexander writes that "unpopulated slots signal dangerous gaps."
A practical use of the model is to walk through each slot and ask: "Are we certain no
one fills this role?" Specifically for safety-critical systems, an empty Regulator slot
or an empty Negative Stakeholder slot is a warning sign, not confirmation of absence.
[src-alexander-2005]

### 1.3 Terminology: Why "User" Is Dangerous

Alexander makes an explicit argument that the word "user" is "dangerously overloaded and
confusing" and should be avoided as a fundamental unit of stakeholder analysis. Depending
on context, "user" is used to mean: all stakeholders, all non-developers, anyone gaining
benefit, operators specifically, or a hybrid of operator and beneficiary.
[src-alexander-2004]

In safety-critical systems, this confusion has direct consequences. If "the user" is
assumed to mean Normal Operator, then:
- Maintenance needs are not captured (wrong operator type)
- Regulatory needs are not captured (not an operator)
- Negative stakeholder impacts are not captured (not a user at all)
- Operational support needs are not captured (indirect operator)

Replacing "user" with the specific role from the taxonomy is not pedantry — it is a
structural safeguard against missing requirements.

### 1.4 Recursive Identification: The Sharp Method

A widely cited technique for stakeholder discovery, attributed to Sharp et al. (1999)
and described in Alexander's taxonomy paper [src-alexander-2005]:

1. Start from the initial contact (whoever commissioned the work)
2. Ask each interviewee: "Who else should I talk to about this system?"
3. Follow each new name to a new interview
4. Terminate when no new names emerge or when new names have been confirmed irrelevant

Alexander's assessment is that this method "reveals only well-known stakeholders" and
misses non-obvious roles. It is necessary but not sufficient. The taxonomy/onion model
is the supplement: use the recursive method to find the people who are obvious, then use
the onion template to check for the roles that nobody thought to mention.

The combination — recursive social network traversal plus template-based gap checking —
is Alexander's recommended practice. [src-alexander-2005]

### 1.5 Surrogacy: A Fundamental Limitation

A crucial and underexplored concept is **surrogacy**: one person speaking on behalf of
another who cannot participate directly. Alexander identifies this as "one of the
fundamental limitations on the engineering of requirements, systems, and software."
[src-alexander-2005]

Four types of surrogate arise in practice:

1. **Typical Consumer surrogate** — a statistical sample representing a broader population
   (e.g., focus group participants representing a consumer market)
2. **Operator of Current Product surrogate** — a present operator standing in for future
   operators of a system that does not yet exist
3. **Project Intermediary surrogate** — a requirements engineer or product manager who
   has interpreted stakeholder needs and now presents them as if they were primary
4. **Salaried Authority surrogate** — an official voice (regulator, safety authority)
   speaking on behalf of the public interest

Every surrogacy introduces the possibility of misrepresentation. Alexander calls
surrogate requirements "hearsay evidence" — legally inadmissible because the person
presenting them did not experience them. Yet surrogacy is unavoidable when stakeholders
are geographically distant, contractually restricted, culturally inaccessible, or
simply do not yet exist (future users of a system in development). [src-alexander-2005]

**Implication for safety-critical practice:** When a requirement comes through a
surrogate, this must be recorded. The risk is not that surrogates are dishonest — it
is that surrogates have incomplete knowledge, filter unconsciously, and cannot be
challenged by the original stakeholder. Traceability must record not just the
requirement but the source: was this from the operator directly, or from a product
manager's interpretation of what the operator said?

---

## 2. Stakeholder Classification

### 2.1 The Power/Interest Grid (Eden and Ackermann / Mendelow)

The most widely used classification scheme in project and systems management is the
power/interest grid (also called the power/interest matrix). Stakeholders are placed
on two dimensions:

- **Power**: ability to influence the system, its development, or its outcomes
- **Interest**: degree of concern about the system's outcomes

This yields four quadrants:

```
                 HIGH INTEREST
                      |
  Keep Satisfied      |      Manage Closely
  (high power,        |      (high power,
   low interest)      |      high interest)
---------------------(+)---------------------
  Monitor             |      Keep Informed
  (low power,         |      (low power,
   low interest)      |      high interest)
                      |
                 LOW INTEREST
```

The grid is primarily a **communication and engagement planning** tool, not a
requirements prioritization tool. Knowing that a regulator has high power and moderate
interest tells you to keep them informed proactively — it does not tell you how to
handle conflicts between their needs and an operator's needs.

**Safety-critical limitation:** In safety-critical systems, the grid can mislead if
"power" is measured only as organizational or commercial power. A regulator may appear
as a medium-power stakeholder in project terms, but their power to block certification
or require design changes late in development is effectively absolute. Similarly, a
Negative Stakeholder (e.g., a community affected by system failure) may have low
apparent power during development but high legal and political power after a failure
event. The grid is most dangerous when it tempts engineers to deprioritize stakeholders
who appear low-power but whose needs, if unmet, create legal, safety, or certification
failures.

### 2.2 The Salience Model (Mitchell, Agle, and Wood)

Mitchell, Agle, and Wood (1997) proposed a more sophisticated classification scheme
based on three attributes: **power, legitimacy, and urgency**. [src-mitchell-1997]

- **Power**: the ability to impose will, coerce, or influence outcomes
- **Legitimacy**: the moral, legal, or contractual basis for their involvement —
  whether their claim on the system is recognized as appropriate
- **Urgency**: the time-sensitivity and criticality of their claim

The three attributes interact to create seven stakeholder types in a Venn diagram:

- **Latent stakeholders** (one attribute only):
  - *Dormant* (power only): can act but have no current claim or urgency
  - *Discretionary* (legitimacy only): moral claim but no power or urgency to press it
  - *Demanding* (urgency only): pressing claims but no power or legitimacy
- **Expectant stakeholders** (two attributes):
  - *Dominant* (power + legitimacy): recognized authority, actively engaged
  - *Dependent* (legitimacy + urgency): need action but rely on others to act for them
  - *Dangerous* (power + urgency): willing to act but without legitimate basis
- **Definitive stakeholders** (all three): highest salience, require management attention

[src-mitchell-1997]

**Why this matters for safety-critical systems:** The salience model captures something
the power/interest grid misses: the distinction between having power and having a
*legitimate* claim. In safety-critical contexts, a stakeholder can have high urgency
(e.g., affected residents) and legitimacy (legal rights) without commercial power. The
salience model makes this combination visible as a "dependent" stakeholder — one whose
needs are real and urgent but who relies on others (regulators, authorities) to press
those needs on their behalf.

The model also highlights "dangerous" stakeholders: those with power and urgency but
without legitimate basis. In safety-critical systems, this maps to hostile agents —
stakeholders who can and will act to harm the system. Identifying them as dangerous
(not just "low interest") is a precondition for security requirements elicitation.

Note: Mitchell et al. (1997) is a theoretical management paper, not a systems
engineering standard. The model is widely cited but was not designed specifically for
safety-critical systems engineering. [src-mitchell-1997]

### 2.3 RACI: Classification for Process Accountability

RACI (Responsible, Accountable, Consulted, Informed) is a responsibility assignment
model, not a stakeholder prioritization scheme. It answers the question: for each
artifact or decision in the development process, who does what?

- **Responsible**: executes the work
- **Accountable**: owns the outcome; the final approving authority (exactly one per task)
- **Consulted**: provides input before decisions are made; two-way communication
- **Informed**: kept updated on decisions and progress; one-way communication

In requirements engineering, RACI is applied to each requirements artifact:

| Artifact | R | A | C | I |
|----------|---|---|---|---|
| Stakeholder needs register | RE team | Project lead | Stakeholders | Management |
| System requirements spec | SE team | Systems architect | Safety, V&V | Stakeholders |
| Interface requirements | Interface lead | SE architect | Adjacent teams | Project |

RACI does not classify stakeholders by power or legitimacy — it classifies them by
their role in the development *process*. It is a complement to the onion model, not a
substitute. The onion tells you who exists; RACI tells you what each person does.

**RACI limitation in safety-critical contexts:** Safety-critical development may require
that the "Accountable" role be independent from the "Responsible" role, to avoid
the reviewer being the same person as the author. RACI matrices should reflect this
independence requirement explicitly.

### 2.4 Which Classification Matters Most for Safety-Critical Systems

No single scheme is sufficient. The recommended combination:

1. **Onion model** — for comprehensive stakeholder identification (find everyone)
2. **Salience model** — for prioritizing whose needs are urgent AND legitimate
3. **Power/interest grid** — for engagement planning (how to communicate with each group)
4. **RACI** — for process assignment (who participates in each artifact activity)

The distinguishing factor in safety-critical systems is that classification cannot be
used to *exclude* stakeholders from elicitation. Low-salience or low-power stakeholders
whose needs relate to safety, certification, or failure modes must be included regardless
of their organizational standing. The regulator is Accountable for certification. The
Negative Stakeholder's needs may become the source of a hazard if ignored.

---

## 3. Needs Elicitation Techniques

### 3.1 The Elicitation Challenge

Elicitation is harder than it looks because stakeholders do not have fully formed
requirements waiting to be written down. Nuseibeh and Easterbrook (2000) describe
requirements engineering as "a fundamentally human-centered communication process, in
which success depends on achieving shared understanding among diverse stakeholders."
[src-nuseibeh-2000]

The challenge has multiple dimensions:
- Stakeholders know their work but not the system constraints
- Engineers know system constraints but not the work domain
- What stakeholders say they need and what they actually need are often different
- Tacit knowledge ("I know it when I see it") resists verbal articulation
- Organizational politics cause important needs to be understated or hidden

These dimensions are not solved by choosing the right elicitation form — they require
different techniques for different types of knowledge and different types of stakeholder.

### 3.2 Interviews

**When to use:** For exploring complex, open-ended domains; when individual perspective
is important; when sensitive concerns need a private forum; for structured follow-up
after initial discovery.

**Structure types:**
- *Unstructured*: open conversation guided by broad questions. High discovery potential
  but low comparability across sessions. Best early in elicitation.
- *Semi-structured*: prepared questions with room for divergence. Balances consistency
  with depth. Most common in practice.
- *Structured*: fixed questionnaire-style. High comparability, low discovery. Appropriate
  for verification of previously identified needs, not for discovery.

Wiegers and Beatty (2013) note that after each interview it is critical to document
the items discussed and ask interviewees to review for accuracy, because "only those
people who supplied the requirements can judge whether they were captured accurately."
[src-wiegers-beatty-2013, secondary]

**Safety-critical implication:** Interview notes must not be sanitized or summarized
without the interviewee's review. The difference between what the interviewee said and
what the interviewer understood is a systematic source of requirements defects.

### 3.3 Facilitated Workshops

**When to use:** When multiple stakeholders need to reach agreement; when requirements
will involve trade-offs between groups; when individual interviews have produced
conflicting or inconsistent needs; when speed matters.

Wiegers and Beatty describe facilitated requirements workshops as "a highly effective
technique for linking users and developers." The facilitator's role includes planning
the workshop, selecting participants, managing group dynamics, and guiding toward
outputs — not participating as a requirements contributor. [src-wiegers-beatty-2013, secondary]

**Joint Application Design (JAD):** The most formalized requirements workshop technique,
developed at IBM and documented in Wood and Silver (1995). [src-wood-silver-1995]
JAD sessions are structured workshops that bring together decision makers and technical
staff to produce specifications collaboratively in compressed time. Key characteristics:
- Structured agenda with defined deliverable outputs
- Dedicated facilitator trained in group dynamics
- Executive sponsor to break deadlocks
- Scribe to capture decisions
- Can include brainstorming, process mapping, data flow modeling

Wood and Silver's documented claim was that quality systems could be designed in "40%
less time" using JAD. [src-wood-silver-1995, secondary]

**Workshop limitation:** Workshops are subject to group dynamics failures — dominant
voices suppressing minority views, groupthink, anchoring on the first solution
proposed. In safety-critical contexts, the engineer who says "this function could kill
someone" needs to be heard even if they are junior. Facilitation must actively create
safe space for dissenting views.

### 3.4 Observation and Contextual Inquiry

**When to use:** When work practices are tacit and difficult to articulate verbally;
when "what people say they do" and "what people actually do" differ; when understanding
the work context (environment, tools, interruptions, constraints) is essential.

Beyer and Holtzblatt developed Contextual Inquiry (CI) as an adaptation of
ethnographic research methods to fit engineering resource constraints. [src-beyer-holtzblatt-1997]

The method has four principles [src-beyer-holtzblatt-1997, secondary]:
1. **Context**: observe people in their actual work environment, not a conference room
2. **Partnership**: work with the person as a collaborative partner, not a subject
3. **Interpretation**: co-construct understanding — share interpretations and invite
   correction
4. **Focus**: have a specific research focus, not just "watch everything"

The technique reveals *hidden work structure* — the workarounds, exception handling,
informal practices, and coordination mechanisms that formal process descriptions never
capture but that the system must support. [src-beyer-holtzblatt-1997]

**Safety-critical implication:** Observation is the technique most likely to reveal
the gap between how procedures are written and how they are actually executed. This
gap is a significant source of safety requirements defects: requirements derived from
the written procedure may miss the actual operational context entirely.

### 3.5 Prototyping

**When to use:** When stakeholders cannot articulate requirements abstractly but can
react to concrete examples; when the design space is novel; when interface or
interaction details are critical.

Two types are relevant for elicitation:
- **Throwaway prototypes** (also called exploratory or horizontal prototypes): quickly
  built to test understanding, then discarded. Goal is to provoke reactions and
  articulate implicit needs. Not intended to evolve into the delivered system.
- **Evolutionary prototypes**: built incrementally and refined through feedback loops.
  Appropriate when the domain is complex and requirements discovery must be interleaved
  with implementation feedback.

The elicitation value of prototypes is that hands-on experience helps stakeholders
"articulate their needs more precisely, identify missing or unclear requirements, and
uncover potential usability issues" [secondary synthesis from multiple sources]. When
stakeholders can see and touch a representation of the system, tacit expectations
surface as "this is wrong" reactions that would never have been expressed in an interview.

**Safety-critical limitation:** Prototypes can anchor stakeholders on a specific
solution before the problem has been fully understood. If a prototype embeds an
architectural assumption, elicitation may inadvertently fix that assumption before it
has been evaluated. Prototypes should be used to validate problem understanding, not
to pre-select solutions.

### 3.6 Document Analysis

**When to use:** When prior systems exist (legacy retrofit context); when regulatory
or contractual constraints are documented; when domain standards must be reviewed;
when existing specifications, procedures, or incident reports exist.

Document analysis is often the first elicitation activity in legacy retrofit contexts.
Existing artifacts reveal:
- What the current system is supposed to do (and therefore what the replacement must
  consider)
- What constraints are already legally or contractually established
- What failure modes and incidents have occurred (incident reports as requirements
  drivers)
- What terminology the domain uses (critical for avoiding misunderstanding)

**Primary document types to analyze in safety-critical contexts:**
- Existing specifications and design documents
- Operational procedures and manuals
- Hazard analyses and safety assessment reports
- Incident and near-miss reports
- Regulatory guidance material and certification standards
- Maintenance logs (reveal actual operational conditions vs. assumed conditions)

Kotonya and Sommerville (1998) list document analysis as a core elicitation technique
alongside interviews and observation. [src-kotonya-sommerville-1998, secondary]

**Critical limitation:** Documents represent the *intended* system or the *formal*
process — not necessarily what stakeholders actually need or what the system actually
does. Document analysis must be supplemented by interviews or observation to close
this gap.

### 3.7 Scenarios and Day-in-the-Life Analysis

**When to use:** For bridging abstract needs to concrete operational reality; for
revealing interaction sequences, preconditions, and exception cases; for communicating
system behavior to non-technical stakeholders.

A **day-in-the-life scenario** (also called an operational scenario or use scenario)
narrates how a specific stakeholder role interacts with the system over a realistic
work period. It includes:
- Who the actor is (specific role, not generic "user")
- What they are trying to achieve (goal)
- The normal sequence of steps
- What can go wrong (alternative paths, exceptions)
- What adjacent systems or people they interact with
- The environment and its constraints (noise, fatigue, time pressure)

Scenarios are useful because they are readable by non-engineers, they can be reviewed
by stakeholders for accuracy, and they make implicit assumptions explicit. A
requirement that "makes sense" in isolation may become obviously inadequate when
placed in the context of a realistic scenario.

**Relationship to ConOps:** Day-in-the-life scenarios are the building blocks of a
ConOps document. Where a full ConOps covers all mission phases and operational modes,
individual scenarios cover specific user-system interactions. See Research 2c for the
ConOps as a systemic elicitation and framing device.

---

## 4. ConOps as an Elicitation Bridge

### 4.1 What ConOps Is

IEEE 1362-1998 defined the Concept of Operations (ConOps) as "a user-oriented document
that describes system characteristics for a proposed system from the users' viewpoint."
The document communicates "overall quantitative and qualitative system characteristics
to the user, buyer, developer, and other organizational elements." [src-ieee-1362-1998]

IEEE 1362 was withdrawn and superseded by ISO/IEC/IEEE 29148:2018, which includes the
System Operational Concept (OpsCon) as one of its key information items. [src-29148-2018]

The ConOps document typically includes:
- Current system description (what it does, why it is being replaced or supplemented)
- Rationale and justification for the new or modified system
- Description of the proposed system from the user's perspective
- Operational scenarios showing the system in the user's environment
- Organizational and environmental context

### 4.2 Why ConOps Bridges Stakeholder Intent and System Requirements

The ConOps captures what stakeholders need the system to accomplish in their
operational world, expressed in their language and from their perspective. This is
explicitly different from a requirements specification, which expresses what the system
must do in engineering language.

reqi.io summarizes the function: ConOps "bridges the gap between abstract ideas and
practical system requirements by outlining how the system will operate within its
intended environment from the perspective of the end user." It "enables systems
engineers to derive specific, actionable requirements" and ensures "every system
requirement can be traced back to a real operational need." [src-reqi-conops]

The traceability path runs: stakeholder needs → ConOps operational scenarios →
system requirements. If a system requirement cannot be traced back to a ConOps
scenario, it may be a derived requirement (from engineering constraints) but it is not
directly stakeholder-driven. Both types are legitimate, but the distinction matters
for validation.

### 4.3 Operational Scenarios in Practice

An operational scenario in a ConOps document is not a use case (which focuses on
system behavior) but a narrative of real-world operation. Key characteristics:

- Written in the stakeholder's language, not the engineer's
- Names specific actors by role (from the onion model taxonomy)
- Covers the operational environment — physical setting, external pressures, resource
  constraints
- Includes normal operation AND edge cases, degraded modes, failure recovery
- Is reviewable by the stakeholder without engineering knowledge

INCOSE guidance notes that elicitation should "obtain input on expected and off-nominal
use cases, scenarios, misuse cases, and loss scenarios." [src-sebok-stakeholder-needs]
Off-nominal scenarios (what happens when something goes wrong) are particularly
important in safety-critical systems because they drive the safety requirements that
normal-mode scenarios do not capture.

---

## 5. The Needs-to-Requirements Distinction

### 5.1 Why This Distinction Matters

Conflating stakeholder needs with requirements is one of the most consequential
mistakes in systems engineering. The confusion has two failure modes:

1. **Recording solution-framed needs as requirements.** A stakeholder says "we need
   a database." This is not a need — it is a proposed solution. The underlying need
   might be "data must survive power loss" or "historical records must be searchable
   within 3 seconds." Writing the solution down as a requirement forecloses design
   options without capturing what actually matters.

2. **Writing requirements before understanding needs.** Requirements written without
   a clear understanding of the underlying stakeholder need are brittle — they capture
   the first engineering interpretation, not the validated intent. When the need changes
   (as it will), it is unclear what requirements need to change with it.

In safety-critical systems, the second failure mode is particularly dangerous. If a
safety-critical function is derived from a misunderstood need, the verification that
the function meets its requirement is meaningless — the requirement was wrong. See
Research 2b for the validation problem in depth.

### 5.2 The INCOSE and ISO/IEC/IEEE 29148 Distinction

ISO/IEC/IEEE 29148:2018 and INCOSE's Needs and Requirements Manual (2022) draw an
explicit distinction between needs and requirements at the language level:

**Needs statements** describe what stakeholders require the system to accomplish,
expressed in stakeholder terms, without the word "shall":
- *"The stakeholders need the system to..."* [src-sebok-stakeholder-needs]
- *"The operator needs to be able to recover from sensor failure within 30 seconds"*

**Requirements statements** express what the system must do, using normative modal
language:
- *"The system shall..."* (mandatory — used for requirements in standards contexts)
- *"The system will..."* (intended behavior, sometimes used for non-mandatory statements)
- *"The system should..."* (recommended but not mandatory)

ISO/IEC/IEEE 29148:2018 defines stakeholder requirements as "transformed from the
stakeholder needs to objectively adequate, structured and more formal statements."
[src-sebok-glossary]

The transformation from need to requirement is not mechanical word substitution. It
involves:
1. **Decomposition**: breaking broad needs into granular, specific, verifiable
   statements
2. **Derivation**: identifying needs that are implicit — not stated but essential
3. **Formalization**: expressing the need as a testable, bounded requirement using
   standard modal language
4. **Constraint application**: incorporating technology, safety, regulatory, and
   environmental constraints that the stakeholder may be unaware of

[src-sebok-glossary, src-incose-nrm-2022, secondary]

INCOSE's 2022 definition is explicit: generating a requirement statement "is more than
changing the subject of the need statement; it is an analysis of what the system must
do to achieve what is needed." [src-incose-nrm-2022, secondary via reqi.io]

### 5.3 The Volere Distinction

The Volere framework (Robertson and Robertson) makes a hierarchical distinction between:

- **Business (project) needs**: why the project exists — the business problem or
  opportunity driving development. These are not requirements; they are justifications.
- **Stakeholder needs/goals**: what stakeholders need to accomplish. Still not
  requirements — they describe intended outcomes from the stakeholder's perspective.
- **Product requirements** (functional and non-functional): what the product must do
  or be. These are requirements in the engineering sense.

The Volere Requirements Specification Template separates these levels structurally.
The "project drivers" section captures stakeholder context and goals. The requirements
sections capture the testable product properties. [src-volere, secondary]

The value of this structure is that it makes the chain of justification visible:
requirement → stakeholder goal → business need. If a requirement cannot be traced to
a stakeholder goal, it lacks a justification. If a stakeholder goal cannot be traced
to a business need, the feature may be out of scope.

### 5.4 Why Confusing Needs and Requirements Is Dangerous in Safety-Critical Systems

In regulated safety-critical systems (DO-178C, ISO 26262, ASPICE), the distinction
is not just good engineering practice — it has compliance implications:

1. **Traceability requirements**: ASPICE SYS.2 requires bidirectional traceability
   between system requirements and stakeholder requirements (BP5). If stakeholder needs
   and system requirements are conflated in a single document, this traceability
   obligation cannot be satisfied.

2. **Validation vs. verification scope**: Stakeholder needs require *validation* (is
   this the right need?), while requirements require *verification* (does the system
   satisfy them?). Conflating the two means validation is never properly performed —
   every check becomes verification against the stated requirement, and no one asks
   whether the requirement was correctly derived from the need. See Research 2b.

3. **Safety requirement derivation**: Safety requirements must be traceable to specific
   identified hazards through the hazard analysis chain. A stakeholder need that says
   "the system must be safe" is not a safety requirement — it is a goal statement.
   Safety requirements derive from FMEA, FTA, HAZOP, or equivalent analysis that
   identifies specific hazards. [src-reqi-safety-req]
   If safety needs are written as requirements, they will appear satisfied by the
   statement itself rather than by the hazard analysis that should underpin them.

4. **Certification evidence**: Aviation (DO-178C) and automotive (ISO 26262) certification
   requires showing that all system requirements trace to a defined set of validated
   higher-level requirements or allocated system items. This traceability chain must
   have a clear top — the stakeholder needs layer. If needs and requirements are
   mixed, auditors cannot verify the chain of evidence.

---

## 6. Summary: Craft Principles for Stakeholder Engineering

Based on the sources reviewed, the following craft principles emerge:

**On identification:**
- Use the onion model as a gap-finding checklist, not just a description of who is present
- Combine recursive social traversal (Sharp method) with template-based discovery
- Treat empty onion slots as warnings, not confirmations — explicitly justify any empty slot
- Record surrogate sources with their limitations; never treat a surrogate's account as
  equivalent to direct stakeholder evidence
- In safety-critical systems, never deprioritize regulators, maintenance operators, or
  negative stakeholders because they appear low-power in the current organizational context

**On classification:**
- Use classification for engagement planning and process assignment — not for excluding
  stakeholders from elicitation
- Apply the salience model to distinguish between power-without-legitimacy (dangerous
  stakeholders) and legitimacy-without-power (dependent stakeholders needing advocacy)
- Recognize that regulatory and safety stakeholders have effective veto power late in
  the lifecycle, regardless of apparent power early

**On elicitation:**
- Match the technique to the type of knowledge being sought:
  - Unknown unknowns: observation, contextual inquiry, workshops
  - Known but unarticulated: interviews, scenarios, prototyping
  - Documented but unreviewed: document analysis, walkthroughs
  - Conflicting needs: facilitated workshops, structured trade-off analysis
- Never use a single technique. The most comprehensive elicitation programs use at
  least three complementary techniques on the same problem space
- Validate interview and workshop outputs with the contributing stakeholders before
  treating them as accepted needs
- Record off-nominal scenarios explicitly — failure modes, degraded operations, and
  edge cases drive safety requirements that normal-mode scenarios will never produce

**On needs vs. requirements:**
- Maintain a structural separation between the stakeholder needs register and the
  requirements specification — in tooling, in document structure, and in traceability
- Do not write requirements until needs are validated
- Every requirement must be traceable to a validated stakeholder need or a derived
  engineering constraint (with the derivation justified)
- Language is the first line of defense: use "need" language for needs, "shall" language
  for requirements; never mix them in the same artifact
- In safety-critical systems, safety needs must be transformed into safety requirements
  through a hazard analysis chain — stating a safety need is not the same as deriving
  a safety requirement

---

## 7. Source Index

| Ref | Full Citation | Type | URL |
|-----|---------------|------|-----|
| [src-alexander-2005] | Ian F. Alexander, "A Taxonomy of Stakeholders: Human Roles in System Development," *Int'l Journal of Technology and Human Interaction* 1(1), 2005, pp. 23–59 | Primary (read) | https://www.scenarioplus.org.uk/papers/stakeholder_taxonomy/stakeholder_taxonomy.htm |
| [src-alexander-2004] | Ian F. Alexander, "A Better Fit — Characterising the Stakeholders," REBPS Workshop at CAiSE'04, Riga, 2004 | Primary (read) | https://www.scenarioplus.org.uk/papers/stakeholders/a_better_fit.htm |
| [src-mitchell-1997] | R.K. Mitchell, B.R. Agle, D.J. Wood, "Toward a Theory of Stakeholder Identification and Salience," *Academy of Management Review* 22(4), 1997, pp. 853–886 | Primary (confirmed) | https://www.jstor.org/stable/259247 |
| [src-wiegers-beatty-2013] | Karl Wiegers and Joy Beatty, *Software Requirements*, 3rd ed., Microsoft Press, 2013. ISBN 9780735679665 | Primary (confirmed; secondary content) | https://www.amazon.com/Software-Requirements-Developer-Best-Practices/dp/0735679665 |
| [src-ieee-1362-1998] | IEEE Std 1362-1998, ConOps Document, IEEE, 1998 (withdrawn) | Standard (confirmed; paywalled) | https://ieeexplore.ieee.org/document/761853/ |
| [src-29148-2018] | ISO/IEC/IEEE 29148:2018, Requirements Engineering. ISO, 2018 | Standard (confirmed; paywalled) | https://www.iso.org/standard/72089.html |
| [src-sebok-stakeholder-needs] | SEBoK, "Stakeholder Needs Definition," sebokwiki.org, accessed 2026 | Secondary (read) | https://sebokwiki.org/wiki/Stakeholder_Needs_Definition |
| [src-sebok-glossary] | SEBoK, "Stakeholder Needs and Requirements (glossary)," sebokwiki.org, accessed 2026 | Secondary (read) | https://sebokwiki.org/wiki/Stakeholder_Needs_and_Requirements_(glossary) |
| [src-nuseibeh-2000] | Bashar Nuseibeh and Steve Easterbrook, "Requirements Engineering: A Roadmap," *ICSE 2000*, pp. 35–46 | Primary (confirmed; PDF inaccessible) | https://www.cs.toronto.edu/~sme/papers/2000/ICSE2000.pdf |
| [src-beyer-holtzblatt-1997] | Hugh Beyer and Karen Holtzblatt, *Contextual Design: Defining Customer-Centered Systems*, Morgan Kaufmann, 1997 | Primary (confirmed; secondary content) | https://dl.acm.org/doi/book/10.5555/2821566 |
| [src-wood-silver-1995] | Jane Wood and Denise Silver, *Joint Application Development*, 2nd ed., Wiley, 1995. ISBN 9780471042990 | Primary (confirmed; secondary content) | https://www.amazon.com/Joint-Application-Development-Jane-Wood/dp/0471042994 |
| [src-incose-nrm-2022] | INCOSE, *Needs and Requirements Manual*, 2022. O'Reilly/Wiley listing | Standard guide (confirmed; paywalled) | https://www.oreilly.com/library/view/incose-needs-and/9781394152742/ |
| [src-kotonya-sommerville-1998] | Gerald Kotonya and Ian Sommerville, *Requirements Engineering: Processes and Techniques*, Wiley, 1998. ISBN 9780471972082 | Primary (confirmed; secondary content) | https://dl.acm.org/doi/10.5555/552009 |
| [src-reqi-conops] | reqi.io, "Concept of Operations (CONOPS) for Systems Engineers," accessed 2026 | Secondary (read) | https://reqi.io/articles/concept-of-operations-conops |
| [src-reqi-safety-req] | reqi.io, "What Makes a Requirement a Safety Requirement," accessed 2026 | Secondary (read) | https://reqi.io/articles/what-makes-a-requirement-a-safety-requirement |
