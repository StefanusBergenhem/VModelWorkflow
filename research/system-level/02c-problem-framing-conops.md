# Research 2c: Problem Framing, Context Analysis, and ConOps

Research for upper V documentation (backlog items 3.4, 3.5, 3.6).
Focus: the craft knowledge that separates good requirements engineers from bad ones —
understanding the problem before jumping to solutions. Covers problem framing,
context analysis, Concept of Operations, use cases as elicitation tools, the needs
cascade, and domain analysis for safety-critical systems.

**Sources used:**
- ASPICE PAM v4.0 (primary, read from PDF pp. 34-39) [src-aspice-4-0]
- Peterson/NASA CR-2015-218982 (primary, read from PDF pp. 1-8, 60-65) [src-peterson-arp4754a-2015]
- INCOSE 42-rule guide via reqi.io (secondary, read in full) [src-incose-42-rule-guide-reqi-2026]
- Gause & Weinberg, "Are Your Lights On?" (1990, Dorset House) — NOT in raw/; claims marked [unverified]
- Jackson, "Problem Frames: Analyzing and Structuring Software Development Problems" (2001, Addison-Wesley) — NOT in raw/; claims marked [unverified]
- IEEE Std 1362-1998, "IEEE Guide for Information Technology — System Definition — Concept of Operations (ConOps) Document" — NOT in raw/; claims marked [unverified]
- Cockburn, "Writing Effective Use Cases" (2000, Addison-Wesley) — NOT in raw/; claims marked [unverified]
- IEEE/ISO/IEC 29148:2018, Systems and Software Engineering — Life Cycle Processes — Requirements Engineering — NOT in raw/; claims marked [unverified]
- Zave & Jackson, "Four dark corners of requirements engineering" (1997, ACM TOSEM 6:1) — NOT in raw/; claims marked [unverified]

**Note on sourcing:** The primary standards (IEEE 1362, ISO/IEC 29148, Jackson's work,
Gause & Weinberg) are paywalled books or standards not available in the engineering codex.
All claims from these sources are marked [unverified]. Claims from ASPICE PAM v4.0 and
the Peterson NASA report are read directly from raw files and marked with source IDs.

---

## 1. Problem Framing vs. Solution Framing

### 1.1 The Core Distinction

Every requirements failure begins the same way: someone writes down what the system
should do before they understand what problem the system is supposed to solve. This
is solution framing — defining the machine before defining the situation. The machine
may be built correctly and still fail to address the actual need.

Problem framing is the discipline of characterizing the problem independently of any
proposed solution. A well-framed problem statement describes:

- The current situation and what is wrong or insufficient about it
- Who is affected and how
- The constraints imposed by the world (physical, regulatory, organizational)
- What "solved" looks like from the perspective of those affected

The distinction matters because a solution-framed requirement is unfalsifiable at the
right level. If a stakeholder says "we need a database," the requirement engineer who
asks "why?" will often discover the actual need is "we need to recover customer data
after a crash" — a requirement that admits multiple solutions, only one of which is a
database. The wrong solution may pass every verification check and still leave the
problem unsolved.

### 1.2 Gause and Weinberg: The Problem Definition Problem

Gause and Weinberg's "Are Your Lights On?" (1990) is the locus classicus for
problem-definition discipline in software and systems engineering. Their central
observation is that the most common mistake in problem-solving is solving the wrong
problem — and that the wrong problem is usually the first formulation presented.
[unverified — book not available in raw/; attribution based on standard literature references]

Key principles attributed to this work [unverified]:

- **"Don't take the first problem statement seriously."** The initial statement is always
  someone's solution to a deeper problem. Peeling back the layers to find the
  underlying need is the actual work.

- **"Every solution is an answer to a question."** Asking "what question does this
  solution answer?" is a systematic way to surface the problem.

- **"The problem is never what it seems."** Sponsors present problems framed in
  terms of their preferred solution. Asking "whose problem is it?" and "in what
  context does it occur?" typically reveals a different problem.

- **The notion of problem ownership**: different stakeholders own different versions
  of the problem. The engineer's problem (how to build it) is not the user's problem
  (how to do their job). Conflating these is the root of most requirements failures.

These principles are cited repeatedly in requirements engineering literature and
practitioner courses. The book has been in print since 1990 and is widely regarded
as foundational [unverified — no primary page citations possible without the raw file].

### 1.3 Jackson's Problem Frames: A Formal Treatment

Michael Jackson's "Problem Frames" (2001) provides a more formal treatment of the
same insight. Jackson distinguishes between:

- **The World** — the environment in which the problem exists, with its own properties
  and phenomena that exist independently of any system
- **The Machine** — the system to be built
- **The Interface** — the shared phenomena between Machine and World

His central argument is that requirements engineering is fundamentally the discipline
of understanding the World — not the Machine. Requirements are statements about
the World that the Machine must make true. Confusing requirements (about the World)
with specifications (about the Machine) is the source of most upstream defects.
[unverified — book not available in raw/]

Jackson identifies five basic problem frame types, each with a canonical structure [unverified]:
1. **Required behaviour** — the machine must directly control some physical domain
2. **Commanded behaviour** — an operator commands the machine to control a domain
3. **Information display** — the machine must track a domain and display its state
4. **Transformation** — the machine must transform a given body of data
5. **Workpiece** — the machine is a tool that an operator uses to modify a domain

The value of frames is that each has known difficulty patterns and known solution
approaches. Identifying which frame applies before writing requirements prevents
misapplication of solution patterns. A "commanded behaviour" problem treated as
a "required behaviour" problem will produce requirements that over-specify the
machine's autonomy and under-specify operator interaction.
[unverified — no primary page citations possible]

### 1.4 Solution Framing in Safety-Critical Contexts

Solution framing is particularly dangerous in safety-critical systems because it
propagates downstream into safety analyses. If a requirement specifies a particular
implementation mechanism (e.g., "the system shall use a watchdog timer"), the safety
analysis (FHA/PSSA) will be conducted against that mechanism rather than against the
underlying safety need (e.g., "the system shall detect loss of control authority
within X milliseconds"). The safety analysis then validates the mechanism, not the
need — and a different mechanism that also meets the need may be incorrectly
classified as non-compliant.

ASPICE SYS.1 BP1 explicitly requires that stakeholder requirements be obtained
"through direct solicitation of stakeholder input, and through review of stakeholder
business proposals (where relevant) and other documents containing inputs to
stakeholder requirements, and consideration of the target operating and hardware
environment." The emphasis on operational environment — not proposed system
behaviour — is the standard's way of anchoring requirements to the problem.
[src-aspice-4-0 §4.3.1 p.34]

ARP 4754A requires that "the generation of acceptable, clear, concise requirement text
relies on experience and engineering judgment." The NASA study documenting
industry practice found that requirements capture is widely treated as the hardest
part of the ARP 4754A process, precisely because it requires reasoning about aircraft
functions (problem level) rather than system behaviour (solution level).
[src-peterson-arp4754a-2015 §4 p.4, §5 p.7]

### 1.5 Symptoms of Solution Framing in Requirements Documents

Practitioners and researchers have identified these patterns as red flags [unverified
unless individually marked]:

| Symptom | Example | Underlying Problem |
|---|---|---|
| Technology named in requirement | "The system shall use CAN bus" | Vendor/architecture preference baked in |
| Implementation mechanism specified | "The system shall poll the sensor every 10ms" | Response-time need not stated |
| Organisational structure baked in | "The gateway module shall..." | Module decomposition done before requirements |
| Negative requirements as workarounds | "The system shall not write to flash more than once per second" | Flash lifetime requirement not stated positively |
| Requirements that exist only in test | "The system shall be testable via serial port" | Test strategy leaked into requirements |

The INCOSE 42-rule guide captures this as Rule R31: requirements must be
"solution free" — focussed on "what" rather than "how." [src-incose-42-rule-guide-reqi-2026 §Abstraction Rules]

---

## 2. Context Analysis: Understanding the World Before Writing Requirements

### 2.1 What Context Analysis Is

Before writing a single requirement, the engineer must understand the environment
into which the system will be placed. Context analysis is the structured investigation of:

1. **System boundary** — what is inside the system and what is outside it
2. **Actors and adjacent systems** — who and what interacts with the system at its boundary
3. **Operational environment** — where, when, and under what conditions the system operates
4. **Existing constraints** — physical laws, regulations, legacy interfaces, organisational
   constraints that are not negotiable
5. **Phenomena that matter** — events, states, and flows in the World that the system
   must sense, control, or report on

Context analysis precedes both requirements elicitation and safety analysis. The
Functional Hazard Assessment (FHA) in ARP 4754A/ARP 4761 is only possible after
the operational context has been established — you cannot assess the hazard of a
failure condition if you do not know the operational scenario in which the failure
occurs. [src-peterson-arp4754a-2015 §4 p.4]

### 2.2 Jackson's World and Machine Model

Jackson's formal model of context analysis distinguishes four types of domains in
the World [unverified — not available in raw/]:

- **Causal domains** — portions of the world with causal properties the machine exploits
  (e.g., physical actuators, sensors)
- **Biddable domains** — people and organisations that respond to instructions
  (operators, maintainers, passengers)
- **Lexical domains** — repositories of data that the machine reads and writes
- **Designed domains** — other engineered systems already in place that the new
  machine must interoperate with

Each domain type has different properties and failure modes. A failure analysis that
treats a biddable domain (a human operator) as a causal domain (a deterministic
actuator) will produce incorrect safety assumptions. This is the formal basis for
why human factors and operational context analysis must precede requirements.
[unverified]

### 2.3 Context Analysis in Practice: What the Standards Require

ASPICE SYS.1.BP1 requires engineers to obtain stakeholder expectations "through
direct solicitation of stakeholder input, and through review of stakeholder business
proposals (where relevant) and other documents containing inputs to stakeholder
requirements, and consideration of the target operating and hardware environment."
[src-aspice-4-0 §4.3.1 p.34]

ASPICE SYS.2.BP4 requires that "the impact that the system requirements will have
on elements in the relevant system context" be analysed. This is context impact
analysis — requirements must not be written in isolation from the surrounding
environment. [src-aspice-4-0 §4.3.2 p.37]

In the ARP 4754A framework, context analysis manifests as Aircraft Function
Development — the process of identifying aircraft-level functions and their
operational contexts before decomposing them into system requirements. The
Preliminary Aircraft Safety Assessment (PASA) and Functional Hazard Assessment
(FHA) operate at this level, establishing safety requirements from operational
failure analysis. The NASA case study shows the FHA conducted against operational
flight phases (take off, approach, landing, go around, flight) — the context, not the
system. [src-peterson-arp4754a-2015 Table 2 pp.22-28]

### 2.4 System Boundary Definition

A well-drawn system boundary is non-trivial and consequential. Errors in boundary
placement produce:

- **Scope creep** — requirements that belong to adjacent systems appear in the
  system specification
- **Interface gaps** — responsibilities that belong to the system are assigned to
  adjacent systems, left uncovered
- **Verification gaps** — behaviours at the boundary are not clearly assigned and
  therefore not verified

The boundary is typically drawn using a context diagram (block diagram showing
the system as a single block, with all external actors and interfaces). Every arrow
crossing the boundary is an interface that requires a specification. Every actor
connected to the boundary is a stakeholder whose operational needs must be captured.

For aviation: ARP 4754A draws the system boundary explicitly, with aircraft-level
functions allocated to systems, and systems interfacing with both other systems and
the aircraft environment (airspace, weather, crew). [src-peterson-arp4754a-2015 §4 p.4]

---

## 3. ConOps: Concept of Operations as a Bridge Artifact

### 3.1 What ConOps Is and Why It Exists

The Concept of Operations (ConOps) document is the artifact that bridges stakeholder
intent and system requirements. It describes the operational world as stakeholders
understand it — before any system decomposition or technical specification occurs.

IEEE Std 1362-1998 defines ConOps as "a user-oriented document that describes
system characteristics for a proposed system from the user's viewpoint." Its purpose
is to communicate to technical developers how the system will be used, not how it
will work. [unverified — IEEE 1362 not available in raw/]

The fundamental asymmetry a ConOps addresses: technical teams understand systems;
operational teams understand missions and tasks. A ConOps is written in operational
language by or with operators, and read by engineers. It is the primary mechanism
for preventing engineers from designing for themselves rather than for the people
who will use the system.

### 3.2 IEEE 1362 ConOps Structure

IEEE 1362 defines a standard structure for ConOps documents [unverified — standard
not available in raw/; structure widely cited in requirements engineering literature]:

1. **Scope** — purpose of the document, system overview, document overview
2. **Referenced documents** — applicable standards, regulations, legacy systems
3. **Current system or situation** — description of the present state (what exists
   today, what problems it has, why change is needed)
4. **Justification for and nature of changes** — rationale for the proposed system,
   alternatives considered, limitations of current approach
5. **Concepts for the proposed system**
   - Background, objectives, scope
   - **Operational policies and constraints** — rules under which the system must operate
   - **Description of the proposed system** — from operational, not technical, perspective
   - **Modes of operation** — normal, degraded, emergency, maintenance, startup, shutdown
   - **User classes and other involved personnel** — profiles of each user type
   - **Support environment** — maintenance, training, logistics
6. **Operational scenarios** — narrative descriptions of how the system is used in
   representative situations
7. **Summary of impacts** — operational, organisational, developmental impacts
8. **Analysis of the proposed system** — advantages, disadvantages, alternatives,
   impacts on existing systems
9. **Notes**

The structural emphasis on operational modes, user profiles, and scenarios is
deliberate: these are the inputs to requirements that pure functional decomposition
misses.

### 3.3 Operational Modes

Operational mode analysis is one of the most practically valuable parts of ConOps
preparation. A system that performs correctly in normal mode may fail catastrophically
in degraded mode because the requirements only addressed normal operation.

Modes to address in a complete ConOps [unverified for specific IEEE 1362 attribution;
the mode taxonomy is standard practice in safety-critical systems engineering]:

| Mode | Description | Requirements Implications |
|---|---|---|
| Normal | Intended operational conditions, all systems functional | Functional performance requirements |
| Degraded | One or more functions unavailable; system still operational | Graceful degradation requirements, mode annunciation |
| Emergency | Immediate safety threat; system may operate outside normal limits | Emergency procedures, crew alerting, safe shutdown |
| Maintenance | System partially disassembled or in test | Maintenance access, diagnostic interfaces, inhibit mechanisms |
| Startup / Initialisation | System transitioning from off to operational | Power-on self-test, safe initialisation sequence |
| Shutdown / Power-off | Transition from operational to off | Safe state capture, power-loss protection |
| Dormant | System stored, not in use | Storage requirements, re-activation requirements |

In safety-critical aviation systems, the FHA in ARP 4754A is explicitly organised
by flight phase — a form of operational mode analysis. The SAAB-EII 100 case study
shows failure conditions assessed per phase: take off, approach, landing, go around,
flight. [src-peterson-arp4754a-2015 Table 2 pp.22-28] This is direct evidence that
mode analysis drives safety requirements.

ASPICE SYS.3.BP2 requires that "dynamic aspects of the system architecture" be
specified "with respect to the functional and non-functional system requirements
including the behavior of the system elements and their interaction in different
system modes." Mode requirements must therefore be traceable from ConOps through
system requirements into architecture. [src-aspice-4-0 §4.3.3 p.38]

### 3.4 User Profiles

User profile analysis identifies who will interact with the system, under what
conditions, and with what level of training and workload. Requirements that ignore
user profiles produce systems that are nominally operable but practically unusable.

Key dimensions of a user profile:
- Role and responsibilities
- Training level and domain expertise
- Expected workload and cognitive load during operation
- Physical environment (noise, vibration, lighting, time pressure)
- Frequency of use and associated skill maintenance
- Error tendencies specific to the role

For aviation: the crew is the primary biddable domain. ARP 4754A's Aircraft Function
Development must account for crew capabilities and limitations because crew response
is part of the safety architecture. A function classified as Catastrophic assumes
the crew cannot recover; a function classified as Hazardous assumes partial crew
recovery is possible. [src-peterson-arp4754a-2015 §4 p.4, Table 2 pp.22-28]

ASPICE SYS.1 BP1 requires consideration of "stakeholder business proposals" and
the "target operating and hardware environment" — which encompasses user context.
[src-aspice-4-0 §4.3.1 p.34]

### 3.5 Operational Scenarios in ConOps

Operational scenarios are narrative descriptions of the system being used to
accomplish a task. They are written before requirements, in plain language, without
reference to internal system structure. A good scenario:

- Names the actors involved
- Describes the triggering event or mission objective
- Walks through the sequence of interactions between actors and the system
- Notes what happens if something goes wrong (exception paths)
- Identifies information the actors need but might not have

Scenarios serve as requirements discovery tools: the act of writing them forces
the author to reason about interface needs, timing constraints, information flows,
and failure modes that would never appear in a top-down functional decomposition.
Requirements derived from scenarios are more likely to address real operational
situations. [unverified — general requirements engineering consensus]

The ConOps scenario is distinguished from the use case (discussed in Section 4) by
its purpose: ConOps scenarios describe operations as they exist or should exist from
the operator's perspective; use cases describe actor-system interactions for the
purpose of deriving requirements. ConOps is pre-requirements; use cases are
elicitation tools.

---

## 4. Use Cases and Scenarios as Elicitation Tools

### 4.1 Cockburn's Use Case Approach

Alistair Cockburn's "Writing Effective Use Cases" (2000) provides the most widely
used practitioner framework for scenario-based requirements elicitation in software
and systems engineering. [unverified — book not in raw/]

Cockburn's key structuring concept is the goal level hierarchy [unverified]:
- **Summary/cloud level** — enterprise or system goals (why the system exists)
- **User goal/sea level** — what a primary actor is trying to accomplish in a
  single sitting (the most important level for requirements)
- **Subfunction/fish level** — component interactions that support a user goal

A requirements error common in practice is writing requirements at the subfunction
level without first establishing the user goal level. The result is a set of
requirements that accurately describes internal interactions but fails to capture
whether the actor's goal is actually achievable. This is the use-case manifestation
of solution framing.

Cockburn distinguishes use cases from user stories: use cases describe a contract
for behaviour, including success and failure scenarios; user stories describe a
desired outcome in one sentence. For safety-critical systems, the richer use case
form is appropriate because failure scenarios are where safety requirements originate.
[unverified]

### 4.2 Main Success Scenario and Extensions

A complete use case in Cockburn's framework [unverified]:

```
Use Case: [name]
Primary actor: [who initiates]
Goal in context: [what the actor is trying to achieve]
Stakeholders and interests: [everyone with a stake in this interaction]
Preconditions: [what must be true before this starts]
Minimum guarantee: [what the system promises even if it fails]
Success guarantee: [what is true after successful completion]

Main success scenario:
  1. [action/event]
  2. ...

Extensions (failure scenarios):
  3a. [condition that breaks step 3]
    .1 [system response]
    .2 [outcome]
```

The "minimum guarantee" field is particularly important for safety-critical systems.
It is the functional equivalent of a safe state: the weakest condition the system
must ensure regardless of what goes wrong. Writing this field explicitly forces
engineers to reason about failure coverage before any safety analysis document exists.
[unverified]

### 4.3 Misuse Cases for Safety and Security

Misuse cases (also called abuse cases) extend the use case framework to capture
adversarial or abnormal actor behaviour. The misuse case asks: "How could an
actor use this system in a way that causes harm?" [unverified]

For safety: the adversarial actor is often a physical failure, an environment
event, or a confused operator. Misuse cases for safety are structurally similar to
FMEA — they systematically enumerate ways the system can be misused or can fail
— but they are written in operational language rather than component-level failure
language. They are therefore more accessible to operational stakeholders during
early requirements review. [unverified]

For security: the adversarial actor is an attacker with specific capabilities and
goals. DO-326A/ED-202A (airworthiness security) and ISO 21434 (automotive
cybersecurity) both require systematic adversarial scenario analysis — the formal
extension of misuse cases to their respective domains. [unverified — standards
not read from raw/; attribution is well-established in the field]

### 4.4 Scenarios Expose What Abstractions Miss

The practical value of scenario-based elicitation is that scenarios reveal
requirements that are invisible to functional decomposition:

- **Timing requirements** — a scenario that describes a crew alert reveals that the
  alert must appear within a specific time window after the triggering event; a
  functional requirement that says "the system shall provide crew alerting" does not
- **Transition requirements** — a scenario that walks through mode switching reveals
  the conditions and sequences that trigger transitions; a static functional
  requirement for each mode does not
- **Negative space requirements** — a scenario that describes what should NOT happen
  in a specific context reveals inhibition requirements that functional decomposition
  ignores
- **Information completeness requirements** — a scenario that shows an operator making
  a decision reveals what information they need to make it correctly; a functional
  requirement that says "the system shall display system status" does not

ASPICE SYS.1.BP1 Note 1 states: "Documenting the stakeholder, or the source of a
stakeholder requirement, supports stakeholder requirements agreement and change
analysis." Scenarios provide exactly this documentation — they ground each
requirement in an operational context with a named actor. [src-aspice-4-0 §4.3.1 p.34]

---

## 5. The Needs Cascade: From Stakeholder Needs to System Requirements

### 5.1 The Transformation Problem

Stakeholder needs are expressed in stakeholder language: operational concepts,
business objectives, mission goals, user tasks. System requirements must be expressed
in system language: measurable behaviours, interface specifications, performance
bounds, safety properties. The transformation between these two languages is where
most requirements defects are introduced.

The transformation is not mechanical. A stakeholder need "the pilot must always know
the aircraft's energy state" does not map to a single system requirement. It maps to
multiple requirements spanning multiple systems (airspeed display, altitude display,
flight management system, alerting system) and introduces derived requirements (e.g.,
cross-check validity) that no stakeholder explicitly stated. Deriving these correctly
requires domain knowledge, not just elicitation skill.

### 5.2 What Gets Added in the Cascade

ASPICE SYS.2.BP1 requires that "functional and non-functional requirements for the
system" be identified and documented "according to defined characteristics for
requirements," explicitly citing ISO IEEE 29148 and ISO 26262-8 as defining those
characteristics. The standard acknowledges that non-functional requirements
(performance, safety, interface, reliability) are often absent from stakeholder
statements and must be derived. [src-aspice-4-0 §4.3.2 p.36]

ASPICE SYS.2 Note 8 acknowledges: "There may be non-functional stakeholder
requirements that the system requirements do not trace to. Examples are process
requirements. Such stakeholder requirements are still subject to verification."
[src-aspice-4-0 §4.3.2 p.37]

Categories of requirements that are typically added (derived) in the cascade,
not present in stakeholder needs [synthesis from ASPICE, ARP 4754A, and general
requirements engineering practice]:

1. **Domain constraints** — legal and regulatory requirements the stakeholder assumes
   you know (14 CFR Part 25, DO-178C, ISO 26262 Part 4). These are mandatory even
   when unstated.

2. **Interface requirements** — requirements imposed by adjacent systems in the
   operational environment. The stakeholder sees an integrated capability; the
   engineer must specify each interface.

3. **Performance bounds** — stakeholders state needs in qualitative terms
   ("fast enough," "reliable enough"). Engineers must quantify: response time in
   milliseconds, availability in percentage, MTBF in hours.

4. **Safety properties** — derived from FHA/PSSA (aviation) or HARA (automotive).
   Safety requirements do not appear in stakeholder statements; they are derived
   from operational failure analysis. The stakeholder did not ask for "the autopilot
   disengagement function to be classified at DAL B." The FHA produced that
   requirement from the operational consequence of the failure. [src-peterson-arp4754a-2015 Table 2 pp.22-28]

5. **Maintenance and supportability requirements** — what is needed for the system
   to be maintained, tested, and upgraded. Operators rarely articulate these; they
   assume them.

6. **Certification and approval requirements** — what must be demonstrated to a
   certification authority. These are derived from regulatory context, not
   stakeholder requests.

### 5.3 What Gets Transformed (Not Just Passed Through)

Not all requirements are additions; some are transformations of stakeholder needs:

| Stakeholder Need | System Requirement (Transformed) | What Changed |
|---|---|---|
| "Pilots need to know when the autopilot disengages" | "The system shall activate the autopilot disconnect aural alert within 0.5 seconds of autopilot disengagement, with a minimum volume of X dB SPL" | Qualitative → quantitative; actor-centric → system-centric |
| "The vehicle must be safe if the ECU loses power" | "Upon loss of supply voltage below 9V, the ECU shall transition to a defined safe state within 10ms" | Concept → specific technical condition |
| "Maintenance needs to be able to reset the system" | "The system shall provide a maintenance mode that inhibits all operational outputs and enables direct interface access via [specified connector]" | Task-level need → interface specification |

The direction of transformation is always from stakeholder language (actors, goals,
tasks, concerns) to system language (components, behaviours, signals, bounds,
interfaces). Transformation that goes the other way — taking a technical property
and presenting it as a stakeholder need — is the definition of solution framing.

### 5.4 Stakeholder Language vs. System Specification Language

The INCOSE 42-rule guide's requirements quality rules are essentially a specification
of what system-language requirements look like. The transformation from stakeholder
language is complete when:

- Active voice with explicit subject (Rule R2): the requirement names the system element
  responsible, not the actor or the function [src-incose-42-rule-guide-reqi-2026 §Accuracy Rules]
- Measurable performance (Rule R34): all performance criteria are numeric, not qualitative
  [src-incose-42-rule-guide-reqi-2026 §Quantification Rules]
- Solution-free (Rule R31): the requirement states what the system must do, not how
  [src-incose-42-rule-guide-reqi-2026 §Abstraction Rules]
- Conditions explicit (Rule R27): the operational context in which the requirement applies
  is stated [src-incose-42-rule-guide-reqi-2026 §Conditions Rules]

A requirement that fails these tests is either still in stakeholder language (incomplete
transformation) or has been transformed in the wrong direction (solution framing).

### 5.5 Bidirectional Traceability as a Cascade Integrity Check

ASPICE SYS.2.BP5 requires: "Ensure consistency and establish bidirectional traceability
between system requirements and stakeholder requirements." The note adds: "There may
be non-functional stakeholder requirements that the system requirements do not trace
to. Examples are process requirements. Such stakeholder requirements are still subject
to verification." [src-aspice-4-0 §4.3.2 p.37]

Bidirectional traceability at the cascade boundary serves two integrity functions:

- **Forward traceability** (stakeholder need → system requirement): ensures every
  need has been addressed. If a stakeholder need has no system requirement tracing
  to it, it has been dropped.

- **Backward traceability** (system requirement → stakeholder need): ensures every
  system requirement was motivated by a real need. If a system requirement traces
  to nothing, it is either a derived requirement (which must be explicitly justified)
  or requirements gold-plating.

The asymmetry — that some stakeholder needs (process requirements) may validly have
no system requirement trace — is important to understand. Not all stakeholder needs
produce system functionality requirements. Some produce process assurance requirements.
The needs cascade does not require one-to-one mapping.

---

## 6. Domain Analysis for Safety-Critical Systems

### 6.1 What Domain Analysis Is

Domain analysis is the investigation of the problem domain independent of any
specific project. It asks: what do competent practitioners in this domain already
know that stakeholders will not bother to tell you? This knowledge is tacit in the
domain; it must be made explicit in requirements.

For safety-critical systems, domain analysis covers at minimum:

1. **Regulatory environment** — what standards and regulations apply, what they
   require, and what the consequences of non-compliance are
2. **Operational environment** — what physical, electromagnetic, thermal, and
   other environmental conditions the system must survive
3. **Hazard catalogue** — known hazards in the domain that must be addressed
   regardless of whether any stakeholder raised them
4. **Domain standards and conventions** — established practices that the system
   must conform to for interoperability or regulatory acceptance
5. **Failure history** — known failure modes of previous systems in the domain

### 6.2 Regulatory Environment Scanning

Safety-critical systems operate under a regulatory framework that imposes requirements
the stakeholder assumes are already known. An engineer who does not know the
applicable regulations will produce an incomplete requirements set — not because
they failed to elicit, but because they did not know what to look for.

For aviation: 14 CFR Part 25 defines airworthiness standards for transport-category
aircraft. Section 25.1309 specifically governs equipment, systems, and installation —
requiring that each system perform its intended function under any foreseeable
operating condition, and that the probability of catastrophic failure conditions be
extremely improbable. ARP 4754A and DO-178C are the industry means of compliance.
No stakeholder will state "the system must comply with 14 CFR 25.1309" — they
assume you know it. [src-peterson-arp4754a-2015 Table 3 p.30; Table 4 pp.32-33]

For automotive: ISO 26262 Part 3 (Concept Phase) and Part 4 (Product Development at
System Level) impose item definition, hazard analysis and risk assessment (HARA),
and functional safety concept requirements that do not originate from any customer.
ASPICE SYS.1 through SYS.5 define process requirements that apply regardless of
whether the customer specified a development process. [src-aspice-4-0 §4.3.1-4.3.5 pp.34-44]

### 6.3 Operational Environment Analysis

The operational environment imposes requirements the system must meet to survive and
function, independent of any stated functional need. Key dimensions:

- **Temperature range** — operating and storage limits
- **Vibration and shock** — mechanical stress profiles (takeoff, landing, road surface)
- **Electromagnetic environment** — conducted and radiated interference (HIRF, lightning)
- **Power supply characteristics** — voltage range, ripple, interruption behaviour
- **Humidity and condensation**
- **Altitude and pressure** (aviation)

These requirements are typically derived entirely from domain knowledge and
environmental standards (DO-160 for aviation, ISO 16750 for automotive), not from
stakeholder elicitation. They are among the most commonly omitted requirements in
incomplete specifications.

### 6.4 Hazard-Driven Needs

Safety requirements in safety-critical systems are almost entirely derived, not elicited.
The process is:

1. Identify operational hazards from domain knowledge and operational scenarios
2. Assess the severity and probability of each hazard
3. Derive functional safety requirements to reduce probability or mitigate effects
4. Derive diagnostic requirements to detect hazardous conditions
5. Derive safe-state requirements to define acceptable failure behaviour

In ARP 4754A, this cascade is: Aircraft-level FHA → Preliminary Aircraft Safety
Assessment (PASA) → Preliminary System Safety Assessment (PSSA) → System Safety
Assessment (SSA). Each step produces requirements that did not exist in the
stakeholder need statement. The development assurance level assigned to each
software component is entirely derived from this cascade. [src-peterson-arp4754a-2015
§4 p.4, Appendix A pp.47-57]

The INCOSE requirement quality rules apply to these derived safety requirements
equally. A safety requirement that says "the autopilot shall be safe" fails Rule R7
(vague terms) and Rule R34 (measurable performance). A safety requirement derived
correctly from the FHA states: "Loss of automatic stability and control shall have a
Major failure condition classification" — measurable, specific, and traceable to
the hazard that motivated it. [src-peterson-arp4754a-2015 Table 2 FC# 22.05]

### 6.5 Maintenance and Support Needs

Maintenance and support needs are systematically underrepresented in stakeholder-
elicited requirements. Maintenance personnel are often absent from elicitation
sessions; maintenance tasks are less glamorous than operational functions; and
maintenance problems typically become visible only after deployment.

For safety-critical systems, maintenance needs that must be explicitly addressed:

- **Fault detection and isolation** — the system must provide enough diagnostic
  information for maintenance personnel to identify and isolate faults to the
  replaceable unit level. This is not a stakeholder request; it is a supportability
  requirement derived from domain knowledge about maintenance processes.

- **Built-In Test (BIT)** — power-on BIT and continuous BIT requirements are domain
  standards in aviation (DO-178C, DO-254) that must be present in requirements
  regardless of whether the customer asked for them. [unverified for specific
  DO-178C/DO-254 attribution — standards not in raw/]

- **Inhibit and override mechanisms** — maintenance personnel need to inhibit
  operational functions during ground maintenance. Requirements for these are
  derived from maintenance task analysis, not from operational elicitation.

- **Data load and software update** — the mechanism for updating the system after
  deployment. The SAAB-EII case study explicitly identifies that "incorrect data
  loaded into avionics platform without detection" is a Catastrophic failure condition
  (FC# 45.01), deriving a requirement for detection of erroneous data loads that
  most stakeholders would not articulate. [src-peterson-arp4754a-2015 Table 2 FC# 45.01 p.28]

### 6.6 Things Stakeholders Will Not Tell You Because They Assume You Know Them

The following categories of requirements are routinely absent from stakeholder-provided
inputs because they are domain assumptions — knowledge that experienced practitioners
hold tacitly and that no stakeholder thinks to state explicitly:

| Category | Example (Aviation) | Example (Automotive) |
|---|---|---|
| Regulatory compliance | 14 CFR 25.1309 functional safety probability limits | ISO 26262 ASIL integrity requirements |
| Environmental qualification | DO-160G temperature, vibration, HIRF categories | ISO 16750 voltage transient immunity |
| Certification artifacts | PSAC, PHAC, plans conforming to DO-178C/DO-254 objectives | Safety plan, HARA, FSC per ISO 26262 |
| Interoperability conventions | ARINC 429/664 data bus protocols | AUTOSAR software architecture, CAN/Ethernet protocols |
| Safe state definition | Aircraft controllable upon single-point failure | Park brake applied, neutral gear on ASIL-D fault |
| Data loading protection | Incorrect data detection per FHA FC# 45.01 | Software update integrity (secure boot) |
| Maintenance diagnostics | Fault isolation to LRU level | OBD-II diagnostic coverage requirements |
| Human factors standards | FAA Human Factors Design Standards, MIL-STD-1472 | [unverified — no automotive human factors standard name confirmed from raw sources] |

These requirements must be added by engineers with domain knowledge during the
needs cascade. They cannot be elicited from stakeholders because stakeholders do not
know they need to state them.

---

## 7. Anti-Patterns and Failure Modes

### 7.1 The Most Expensive Upstream Defects

Requirements defects are the most expensive class of software and systems defects
because they propagate through the entire V-model. A requirement error at the
stakeholder needs level produces: an incorrect system requirement, incorrect
allocation to subsystems, incorrect design, incorrect implementation, incorrect
tests — and the error is only discovered during system test or field operation
when correction costs an order of magnitude more than at origin.

The specific defect patterns from the problem framing and ConOps domain:

**Problem framing failures:**
- Writing requirements before ConOps exists (no operational context for
  verification of completeness)
- Treating the first stakeholder problem statement as the true problem
  (Gause & Weinberg anti-pattern) [unverified]
- Writing requirements in system language without first characterising the
  operational world (Jackson's World/Machine confusion) [unverified]

**ConOps failures:**
- No ConOps written at all — requirements written directly from stakeholder
  interviews without operational framing
- ConOps written after requirements (backward — ConOps then has to match the
  requirements rather than motivate them)
- ConOps written by the development team rather than with operational stakeholders
  (system language contaminates the document)
- ConOps missing degraded and emergency mode scenarios (the scenarios most likely
  to reveal safety requirements)
- User profiles absent or generic (no workload, training, error tendency analysis)

**Needs cascade failures:**
- All requirements traced to stakeholder needs (derived requirements, including
  safety and regulatory requirements, not present in the trace matrix)
- Requirements transformation incomplete (requirements still in stakeholder language,
  not yet in measurable system language)
- Regulatory and domain requirements absent (domain knowledge not applied)
- One-to-one requirement mapping expected (not understanding that multiple system
  requirements may trace to one stakeholder need, or that derived requirements
  trace to none)

### 7.2 The "We Know What the Customer Wants" Anti-Pattern

A specific anti-pattern in experienced teams: assuming that domain expertise
eliminates the need for ConOps and problem framing. Experienced engineers
correctly know the regulatory requirements, environmental standards, and domain
conventions. What they often miss is the specific operational context of this
system with this operator in this environment. Domain expertise answers "what
must be true in general"; ConOps and problem framing answer "what must be true
here and now."

ARP 4754A acknowledges this: the NASA study found that the most significant
issues in applying ARP 4754A involved not compliance with requirements rules, but
the exercise of engineering judgment to interpret requirements in specific operational
contexts. "It's not just about what is being done but who does it as well. Expertise
(skills and experience) matters." [src-peterson-arp4754a-2015 §5 p.7]

### 7.3 Requirements That Cannot Be Validated

ARP 4754A separates requirements validation ("are these the right requirements?")
from requirements verification ("does the implementation satisfy the requirements?").
The NASA study identifies requirements validation as "viewed as 'new and unfulfilling
work' that puts additional demands on scarce experienced personnel" and notes that
"most engineers have experience defining and verifying requirements but NOT
justifying (validating) them." [src-peterson-arp4754a-2015 §5 p.7]

Requirements that are solution-framed, lack ConOps grounding, or are derived without
documented domain reasoning cannot be validated — there is no operational basis
against which to check them. The ConOps and problem framing work described in this
document is precisely the foundation that makes validation possible.

---

## 8. Implications for the VModelWorkflow Framework

### 8.1 Where ConOps and Problem Framing Sit in the V-Model

```
Stakeholder Needs / ConOps
        |
        ↓
System Requirements
        |
        ↓
System Architecture
        |
        ↓
Software/HW Requirements
        ↓
...
```

ConOps is a pre-requirements artifact. It is not in the V-model chain itself; it
is a prerequisite input to the leftmost tip of the V. Requirements validation
(checking requirements against ConOps) is a horizontal activity at the top-left of
the V. The ConOps-to-system-requirements relationship is the first transformation
in the needs cascade.

In ASPICE terms: ConOps preparation is part of the inputs to SYS.1 (stakeholder
requirements elicitation). SYS.1 outputs are stakeholder requirements. SYS.2
produces system requirements from stakeholder requirements. ConOps is not a defined
ASPICE artifact — it is preparatory work that supports SYS.1.
[src-aspice-4-0 §4.3.1-4.3.2 pp.34-37]

### 8.2 Skills This Research Should Drive

From this research, the following craft skills are candidates for VModelWorkflow:

1. **Problem framing interview**: structured approach to uncovering the real problem
   behind an initial problem statement
2. **ConOps authoring**: guided process for writing an IEEE 1362-structured ConOps
   from operational stakeholder interviews
3. **Operational mode analysis**: systematic enumeration of operational modes and
   their requirements implications
4. **Needs cascade review**: checklist for detecting incomplete transformation,
   missing derived requirements, and solution-framed requirements
5. **Domain requirement injection**: process for adding regulatory, environmental,
   maintenance, and safety requirements that stakeholders will not state

### 8.3 What This Research Is Missing

The following topics were identified as relevant but lack primary source coverage
in the current codex. They should be addressed in subsequent research before
documentation and skills are written:

- IEEE 1362 ConOps structure — the standard itself should be ingested (paywalled;
  access required)
- Jackson's Problem Frames — the book should be obtained for direct quotation
- Zave & Jackson (1997) "Four dark corners of requirements engineering" — the most
  cited academic paper on the world/machine distinction; available via ACM
- Cockburn use case framework — the book should be ingested for use case skill design
- ISO/IEC 29148:2018 — the current requirements engineering lifecycle standard;
  needed for cross-domain coverage

---

## Source List

| Source | Type | Status |
|---|---|---|
| ASPICE PAM v4.0 | Primary standard | Read from raw file; claims sourced [src-aspice-4-0] |
| Peterson, NASA CR-2015-218982 | Primary report | Read from raw file; claims sourced [src-peterson-arp4754a-2015] |
| INCOSE 42-rule guide (reqi.io) | Secondary | Read from raw file; claims sourced [src-incose-42-rule-guide-reqi-2026] |
| Gause & Weinberg (1990) | Primary book | NOT in raw/; all claims [unverified] |
| Jackson, Problem Frames (2001) | Primary book | NOT in raw/; all claims [unverified] |
| IEEE Std 1362-1998 | Primary standard | NOT in raw/; all claims [unverified] |
| Cockburn, Use Cases (2000) | Primary book | NOT in raw/; all claims [unverified] |
| ISO/IEC 29148:2018 | Primary standard | NOT in raw/; referenced only |
| DO-160G | Primary standard | NOT in raw/; referenced without claims |
| ARP 4761 | Primary standard | NOT in raw/; referenced without claims |
| Zave & Jackson (1997) | Primary paper | NOT in raw/; referenced without claims |
