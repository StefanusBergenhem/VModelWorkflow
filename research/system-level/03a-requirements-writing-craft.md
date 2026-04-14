# Research 3a: The Craft of Writing Good System Requirements

Quality criteria, writing patterns, anti-patterns, NFR techniques, and granularity
guidance for system-level requirements engineering.

**Sources used (all fetched or read directly in this session):**

- Langenfeld et al. 2016 — "Requirements Defects over a Project Lifetime: An Empirical
  Analysis of Defect Data from a 5-Year Automotive Project at Bosch," RE'16, Springer.
  Results accessed via ResearchGate abstract + Langenfeld's own project page
  (https://swt.informatik.uni-freiburg.de/staff/langenfeld/) [src-langenfeld-bosch-2016]
- Wiegers, K. — "Karl Wiegers Describes 10 Requirements Traps to Avoid," Process Impact.
  Fetched directly from https://www.cs.hmc.edu/~mike/courses/mike121/readings/requirements/reqtraps.html
  [src-wiegers-reqtraps]
- workingsoftware.dev — "The Ultimate Guide to Write Non-Functional Requirements."
  Fetched directly. Covers ISO 25010, Q42 model, quality scenarios. [src-workingsoftware-nfr]
- modernanalyst.com — "Writing Non-Functional Requirements That Developers Actually Use."
  Fetched directly. Covers five-step method and patterns. [src-modernanalyst-nfr]
- modernanalyst.com — "Specifying Quality Requirements with Planguage."
  Fetched directly. Covers Planguage keywords and worked example. [src-modernanalyst-planguage]
- methodsandtools.com — "How to Quantify Quality: Finding Scales of Measure" (Tom Gilb).
  Fetched directly. Scale/Meter framework and Planguage principles. [src-gilb-scales]
- functionalsafetyfirst.com — "Functional Safety Requirements (FSR) vs. Technical Safety
  Requirements (TSR)." Fetched directly. FSR/TSR patterns and examples. [src-fsfirst-fsr-tsr]
- NASA NPR 7123.1C — "NASA Systems Engineering Processes and Requirements." Accessed via
  NODIS (https://nodis3.gsfc.nasa.gov). MOE/MOP/TPM framework extracted. [src-nasa-npr-7123]
- NASA NTRS — "Error Cost Escalation Through the Project Life Cycle" (NASA/JSC 2010,
  20100036670). PDF binary, content confirmed via ResearchGate data [src-nasa-cost-escalation]
- Web search synthesis — Boehm cost-to-fix data, IEEE 830, Rashid et al. 2021 SMS,
  arxiv.org/2206.05959 (requirements quality factor ontology). [web-search-2026]
- ASPICE PAM v4.0 [src-aspice-4-0] — cross-referenced from prior research sessions
- Engineering codex concept-requirement-quality and concept-ears — used as baseline to
  identify gaps; content not duplicated here

**NOTE on source limitations:**
- ISO/IEC/IEEE 29148:2018, INCOSE GtWR, Wiegers & Beatty "Software Requirements 3rd ed.,"
  Robertson & Robertson, and Hull/Jackson/Dick are all paywalled. No claims are made
  from these sources. Where their content is known to be covered by the codex
  (INCOSE 42 rules, EARS), this document does not duplicate it.
- ECSS-E-ST-10-06C (European Space Agency requirements specification standard): document
  headers fetched but PDF was binary-only — extracted information from secondary source
  descriptions only; ECSS claims marked [secondary-ecss].
- Bosch Langenfeld 2016 paper: abstract and project-page summary accessible; full text
  paywalled at Springer. Key quantitative findings (61%, most-costly types) sourced from
  the abstract-level summary [src-langenfeld-bosch-2016] and confirmed by multiple web
  sources referencing the same study.

**Claims marked [unverified] were not read from a primary source in this session.**

---

## 1. What the INCOSE 42 Rules Don't Cover

The INCOSE 42-rule framework and the nine/fifteen quality characteristics are already
documented in the engineering codex (concept-requirement-quality, src-incose-42-rule-guide-reqi-2026).
This section adds what other frameworks and empirical research bring beyond that foundation.

### 1.1 NASA's MOE/MOP/TPM Triad

NASA NPR 7123.1C introduces a three-tier measurement framework that the INCOSE rules do
not address [src-nasa-npr-7123]:

| Tier | Name | Question answered | Who uses it |
|------|------|-------------------|-------------|
| 1 | Measures of Effectiveness (MOE) | Does the system deliver stakeholder value? | Customer/program |
| 2 | Measures of Performance (MOP) | Does the system meet technical requirements? | System engineer |
| 3 | Technical Performance Measures (TPM) | Is the design progressing toward MOPs? | Design team |

**Why this matters for writing:** A requirement that only states a functional behavior
misses the measurement layer. Good system requirements identify which MOP they contribute
to, and the MOP value drives the numerical threshold in the requirement. Without this
linkage, the performance targets in requirements are arbitrary.

NPR 7123.1C mandates that requirements be "unique, quantitative, and measurable technical
requirements expressed as 'shall' statements" that are verifiable and traceable
[src-nasa-npr-7123 §3.2.3.2].

### 1.2 ECSS Characteristics: Identifiability and Configuration Management

ECSS-E-ST-10-06C (European Space Agency, 2009) defines requirement characteristics that
overlap partially with INCOSE but add two that the INCOSE list omits [secondary-ecss]:

- **Identifiability:** Every requirement must carry a unique identifier that survives
  document restructuring. Requirements must be identifiable independently of their
  document position (heading, section number, paragraph).
- **Configuration management readiness:** Requirements must be structured to support
  change control — each requirement independently modifiable without cascading edits to
  adjacent requirements.

These characteristics are implicit in INCOSE's "conforming" and "uniqueness" rules but
are not stated as first-class characteristics in the INCOSE list.

### 1.3 Feasibility Is Underrated

Both INCOSE and NASA list feasibility as a characteristic, but it is rarely enforced in
practice. Two failure modes:

**Wishful thinking:** "The system shall have zero unplanned downtime." This violates
INCOSE R26 (no absolutes) and is physically infeasible. The correct form requires a
numeric target: "The system shall achieve 99.9% availability (≤8.76 hours unplanned
downtime per year)." [src-wiegers-reqtraps §Trap 3]

**Chronological infeasibility:** A common pattern in safety-critical systems is
specifying both a detection time and a response time that together exceed the Fault
Tolerant Time Interval (FTTI). Example: "The ECU shall detect fault X within 100ms
AND transition to safe state within 200ms" — if FTTI = 250ms, this pair is
infeasible as written (detection + transition = 300ms > FTTI). [src-fsfirst-fsr-tsr]

### 1.4 Requirement Priority as a Quality Dimension

Wiegers identifies unprioritized requirements as a systemic failure mode: treating all
requirements as equally important prevents rational scope management. Priority is not
in the INCOSE nine individual characteristics [src-wiegers-reqtraps §Trap 4].

**Why this is a writing problem, not just a management problem:** A requirement that
can be dropped without user impact has questionable necessity. INCOSE's "Necessary"
characteristic (removal creates deficiency) is the individual-requirement equivalent —
but at set level, requirements need relative priority to support allocation and
trade-off decisions during design.

**MoSCoW classification** (Must/Should/Could/Won't) and priority based on
usage frequency, user class benefit, and compliance are common heuristics
[src-wiegers-reqtraps §Trap 4]. None of these are addressed by the 42 rules.

### 1.5 Solution-Freedom Enforcement

INCOSE R31 says "solution-free." This is stated but rarely enough. Three levels of
solution-prescription exist, from most to least harmful [synthesized from src-wiegers-reqtraps,
src-fsfirst-fsr-tsr]:

| Level | Example | Problem |
|-------|---------|---------|
| Implementation algorithm | "...shall use AES-256-GCM encryption" | Over-constrains cryptographic design choices |
| Architecture prescription | "...shall use a circular buffer for message storage" | Locks data structure choice |
| Technology reference | "...shall comply with CAN 2.0B at 500 kbps" | Sometimes legitimate interface constraint, but must be justified |

The test: can the implementation team choose a different approach that still satisfies
the intent? If not, the requirement is prescribing design. The exception is interface
requirements — where the interface protocol is a constraint imposed by an external
system, specifying the protocol is correct. See Section 3.3.

---

## 2. Requirement Writing Patterns

### 2.1 EARS in Practice: Common Application Mistakes

EARS syntax is documented in the codex (concept-ears). This section covers application
patterns that go beyond the five templates.

**Choosing the wrong template:** The most common EARS misapplication is using
"ubiquitous" (no keyword) for what is actually a state-driven requirement. The
distinction matters for testing:

| Wrong form | Correct form | Why it matters |
|------------|--------------|----------------|
| "The braking system shall apply maximum pressure." | "While ABS is active, the braking system shall apply maximum pressure." | Without the While clause, this requirement is untestable — maximum pressure always? |
| "The ECU shall log a fault code." | "If the oil pressure sensor reports below 10 kPa for more than 500ms, then the ECU shall log fault code P0520." | Without the If clause, no trigger is defined |

**Over-compounding:** Combining three or more EARS keywords in a single requirement.
While the EARS grammar permits `Where → While → When → If/then → shall`, requirements
with all four context modifiers are testing three independent conditions simultaneously.
In practice, keep combinations to two keywords maximum; more than two is a signal to
split [src-seed-ears §1.6, per codex].

**Hiding NON-functional requirements in functional templates:** "The system shall
respond to all user inputs" looks like an EARS ubiquitous requirement but is actually
a performance constraint with no measurable criterion. If it's a performance
requirement, write it as one (see Section 2.4).

### 2.2 Conditional Requirements (When/While/If)

Three EARS keywords cover conditionals, but they have distinct semantics:

| Keyword | Condition type | Duration | Test strategy |
|---------|----------------|----------|---------------|
| `When` | Event trigger | Momentary — the trigger fires once | Stimulus-response: inject the event, verify the response |
| `While` | System state / mode | Sustained — requirement active as long as state holds | Duration test: enter state, verify requirement holds throughout |
| `If...then` | Fault / unwanted condition | Fault-response | Fault injection: force the condition, verify the response |

**The "while" vs. "when" distinction is critical in safety-critical systems:** A
requirement that uses "When the engine is in startup" instead of "While the engine
is in startup" implies the behavior is triggered by the transition into startup, not
required throughout startup. Wrong semantics produce wrong tests.

**Conditional requirement completeness:** Every `When` or `While` requirement implies
the existence of conditions under which the requirement does NOT apply. Good practice
requires explicitly writing those complementary requirements or documenting the
out-of-scope condition. Example:

- "While the aircraft is airborne, the ground proximity system shall monitor terrain
  clearance." (active state)
- "While the aircraft is on the ground, the ground proximity system shall suppress
  terrain clearance alerts." (complementary inactive state)

Auditors look for the complementary requirement pair. Missing the negative/complementary
form is a completeness gap [src-peterson-arp4754a-2015 per prior research 03b, pp.51-57].

### 2.3 Performance Requirements Patterns

Performance requirements are the most frequently written in untestable form. The pattern
for a testable performance requirement has five mandatory elements [src-modernanalyst-nfr]:

```
The <system> shall <perform action>
  within <threshold with unit>
  at the <percentile>
  under <load/condition>
  in <environment>.
```

**Bad:** "The system shall display account balances quickly."

**Good:** "The payment API shall return account balance data within 1.5 seconds at the
95th percentile under a load of 3,000 concurrent sessions in the production
environment." [src-modernanalyst-nfr]

**Percentile specification is mandatory for performance NFRs.** A threshold without a
percentile is ambiguous: "respond within 2 seconds" could mean "never take more than 2
seconds" (p100 — likely infeasible) or "most of the time under 2 seconds" (p50 — too
loose). Industry standard is p95 for response time, p99 for critical paths.

**Five mandatory elements for performance requirements:**

1. **Threshold with unit:** "500ms," "2 seconds," "100 MB/s" — not "fast" or "acceptable"
2. **Percentile:** p95, p99, p100 (maximum)
3. **Load context:** "under N concurrent users," "at rated throughput of X transactions/sec"
4. **Environmental condition:** production hardware, specified network topology, etc.
5. **Measurement method:** specifies how the threshold is verified (stopwatch test,
   load testing tool, Lighthouse audit, etc.)

Planguage provides the most precise way to express performance requirements with multiple
target levels [src-gilb-scales; src-modernanalyst-planguage]:

```
TAG:    Performance.API.ResponseTime
SCALE:  Seconds from request initiation to first byte received by client
METER:  Automated load test of 30 representative requests on base hardware spec
GOAL:   No more than 2.0 seconds for 95% of requests
STRETCH: No more than 0.5 seconds for 95% of requests
FAIL:   Any request exceeds 10 seconds
WISH:   No more than 0.2 seconds for 95% of requests
```

The multi-level approach (GOAL/STRETCH/WISH/FAIL) avoids binary pass/fail and allows
design trade-offs to be made explicit.

### 2.4 Interface Requirements Patterns

Interface requirements specify the boundary between the system being specified and
external entities. The INCOSE 42 rules do not address interface requirements specifically;
the beyond-EARS research listed "missing interface requirements" as one of the seven most
common audit findings [src-seed-requirement-syntax-beyond-ears §3.2].

**What interface requirements must cover:**

| Dimension | Required in interface requirement | Example |
|-----------|----------------------------------|---------|
| Protocol | Communication standard and version | "The data bus interface shall comply with ARINC 429 Part 1 at 100 kbps" |
| Message structure | Data type, units, range, resolution | "The speed signal shall be encoded as a 16-bit unsigned integer in units of 0.01 km/h (range 0–655.35 km/h)" |
| Timing | Transmission frequency, latency, jitter | "The engine control unit shall transmit the speed signal at 10 ms ± 0.5 ms intervals" |
| Error handling | Behavior when interface fails | "While receiving no valid speed signal for more than 100 ms, the system shall use the last valid speed value and set the speed sensor fault flag" |
| Initial/startup | Behavior before interface is established | "During system initialization, the system shall apply a speed value of 0 km/h until the first valid message is received" |

**Interface requirement anti-pattern:** Writing an interface requirement that specifies
protocol but omits timing and error handling. Auditors treat incomplete interface
specifications as incomplete requirements — the missing timing and fault behavior must
be derived requirements that trace back to the interface definition.

**The "where" EARS keyword for optional interfaces:** "Where the cellular communication
module is installed, the system shall transmit diagnostic data at 60-second intervals."
The Where clause handles configuration-variant interfaces cleanly.

### 2.5 Safety Requirements Patterns

Safety requirements are a distinct class that requires different writing techniques.
They emerge from hazard analysis (FMEA, FHA, HAZOP) and encode hazard mitigations
as behavioral obligations.

**The FSR/TSR hierarchy pattern [src-fsfirst-fsr-tsr]:**

Functional Safety Requirements (FSRs) are implementation-independent — they state what
safety behavior is needed. Technical Safety Requirements (TSRs) are derived from FSRs
and specify how the safety behavior is implemented.

```
Safety Goal:  Loss of steering control shall not occur (ASIL D)

FSR:  The ECU shall detect a steering position sensor fault within 50ms.
FSR:  The ECU shall transition the steering system to degraded mode within 200ms of
      fault confirmation.

TSR:  The steering position sensor plausibility check shall compare primary and
      secondary sensor values and report a fault when the difference exceeds 5°.
TSR:  The degraded mode shall limit steering assist torque to 30% of nominal maximum.
```

**Timing constraint requirement pattern:** FSR timing constraints must respect the
Fault Tolerant Time Interval (FTTI). The sum of detection time + response time must
be less than FTTI [src-fsfirst-fsr-tsr]:

```
If the oil pressure drops below 100 kPa,
then the engine management system shall detect the fault within 500ms
AND initiate engine shutdown within 1,000ms of fault confirmation.
[Constraint: detection (500ms) + response (1,000ms) = 1,500ms < FTTI (2,000ms)]
```

Note: FTTI is a derived parameter that must appear in the system requirements; without
it, timing constraints cannot be verified as feasible.

**"Shall not" requirements (negative constraints):** Negative requirements are legitimate
in safety contexts but require careful formulation. The problem with "shall not crash"
is not that it's negative — it's that it's not bounded. A bounded negative is testable:

| Unbounded (untestable) | Bounded (testable) |
|------------------------|---------------------|
| "The autopilot shall not issue unsafe commands." | "The autopilot shall not issue pitch commands exceeding ±15° in any 500ms window." |
| "The braking system shall not fail dangerously." | "Under any single hardware fault, the braking system shall provide no less than 50% of nominal deceleration." |
| "The communication system shall not drop messages." | "The communication bus shall achieve a message loss rate of no more than 10⁻⁹ per message-hour under rated operating conditions." |

**Diagnostic coverage requirements:** Safety standards require specifying what fraction
of dangerous failures must be detected. These are NFRs with safety implications
[synthesized from web-search-2026 on ISO 26262]:

```
The battery management system shall detect dangerous cell overvoltage conditions
with a diagnostic coverage of at least 99% (ASIL D requirement: ≥99% DC).
```

**Safety isolation requirement pattern:** Derived from PASA/FHA independence analysis,
these requirements appear as negative coupling constraints:

```
The primary flight control function shall be independent of the entertainment
system such that no failure of the entertainment system can affect primary
flight control outputs.
```

These requirements do not naturally emerge from functional decomposition — they must
be driven by hazard analysis. Missing independence requirements are a documented audit
failure mode [src-peterson-arp4754a-2015 per 03b research].

---

## 3. Non-Functional Requirements

### 3.1 NFR Classification Frameworks

Two frameworks are in wide use for classifying NFRs. Neither is normative in safety
standards; they are practitioner classification tools.

**FURPS+ (Hewlett-Packard, widely adopted)** [web-search-2026]:

| Category | Covers | Example NFR type |
|----------|--------|-----------------|
| **F** — Functionality | Security, interoperability, reusability | "The system shall authenticate users using OAuth 2.0" |
| **U** — Usability | Human factors, documentation, accessibility | "85% of first-time users shall complete registration within 5 minutes" |
| **R** — Reliability | Availability, accuracy, fault tolerance, recoverability | "The system shall achieve 99.9% availability over any 30-day period" |
| **P** — Performance | Response time, throughput, scalability, capacity | "The API shall respond within 500ms at p95 under 2,000 concurrent users" |
| **S** — Supportability | Testability, maintainability, configurability, installability | "The system shall provide a /health endpoint responding within 500ms" |
| **+** — Extensions | Physical, data, legal/regulatory constraints | "The system shall comply with GDPR data retention limits" |

**ISO 25010:2023 (normative taxonomy for system and software quality)** [src-workingsoftware-nfr]:

Eight top-level characteristics:
1. **Functional suitability** — completeness, correctness, appropriateness
2. **Performance efficiency** — time behavior, resource utilization, capacity
3. **Compatibility** — co-existence, interoperability
4. **Interaction capability** — usability and user satisfaction
5. **Reliability** — faultlessness, availability, fault tolerance, recoverability
6. **Security** — confidentiality, integrity, non-repudiation, authenticity, accountability
7. **Maintainability** — modularity, reusability, analysability, modifiability, testability
8. **Flexibility** — adaptability, scalability, installability, replaceability

**Limitations of ISO 25010 noted by practitioners:** The standard uses abstract noun forms
("flexibility" not "flexible") and lacks coverage of deployability, energy efficiency,
code quality, and scalability as first-class characteristics [src-workingsoftware-nfr].

### 3.2 The Core Problem with NFRs: Adjective-to-Number Translation

The single most common NFR defect is writing an adjective instead of a number.

**The pattern to follow [src-modernanalyst-nfr]:**

```
In [environment], when [trigger], the system shall [response], measured by [metric].
```

| Weak NFR | Strong NFR |
|----------|-----------|
| "The system shall be fast" | "The system shall return account balance data within 1.5 seconds for 95% of requests under 3,000 concurrent sessions" |
| "The system shall be secure" | "All external traffic shall use TLS 1.2 or higher; users shall be locked out after 5 failed login attempts within 15 minutes" |
| "The UI shall be intuitive" | "80% of first-time users shall complete a balance transfer without assistance within 7 minutes" |
| "The system shall be easy to monitor" | "All microservices shall expose /ready and /live endpoints responding within 500ms under normal load" |
| "High availability" | "The system shall achieve 99.5% availability per calendar month, excluding pre-agreed maintenance windows of no more than 2 hours" |

[src-modernanalyst-nfr]

### 3.3 Performance NFR Writing Technique

Five elements are mandatory in every performance requirement [src-modernanalyst-nfr]:
1. Threshold with unit
2. Percentile (p95 for response time, p99 for critical paths)
3. Load context (concurrent users, transaction rate)
4. Environment specification (production, test bench, specified hardware)
5. Measurement method

**Availability requirements** use a different structure — the "nines" framework:

| Availability | Max downtime/year | Max downtime/month |
|---|---|---|
| 99% (2 nines) | 87.6 hours | 7.3 hours |
| 99.9% (3 nines) | 8.76 hours | 43.8 minutes |
| 99.99% (4 nines) | 52.6 minutes | 4.4 minutes |
| 99.999% (5 nines) | 5.26 minutes | 26.3 seconds |

The requirement must state: what is included in "downtime" (planned vs. unplanned),
the measurement window (per month vs. per year), and any exclusions
[synthesized from src-workingsoftware-nfr and web-search-2026].

### 3.4 Reliability and Fault Tolerance NFR Patterns

Three distinct reliability requirements types are often conflated:

**Availability requirement** (steady-state uptime):
```
The ground support system shall achieve 99.9% availability over any 30-day
measurement period, excluding pre-approved maintenance windows.
```

**Recovery time requirement** (time from failure to return to service):
```
If the primary processing unit fails, the backup unit shall assume full
operational capability within 500ms without data loss.
```

**Mean Time Between Failures (MTBF) requirement** (for hardware-intensive systems):
```
The flight control computer hardware shall achieve an MTBF of no less than
10,000 flight hours under normal operating conditions.
```

These are different requirements with different verification methods: availability
requires long-duration monitoring; recovery time requires fault injection testing;
MTBF requires accelerated life testing or field data analysis.

### 3.5 Security NFR Patterns

Security requirements have a dual nature: some are measurable constraints, others are
categorical mandates. Both are valid [src-modernanalyst-nfr]:

**Categorical (binary, verifiable by inspection or test):**
```
All data transmitted between the vehicle ECU and the diagnostic tool shall be
encrypted using TLS 1.3 or higher.
```

**Quantitative (measurable, requires measurement definition):**
```
The authentication system shall lock user accounts after 5 consecutive failed
authentication attempts within any 10-minute window. The lockout period shall
be no less than 15 minutes.
```

**Access control requirements:**
```
The system shall enforce role-based access control such that no user account
has read access to data outside its assigned role scope.
```

**Audit trail requirements (critical for certification):**
```
The system shall maintain a tamper-evident audit log of all configuration
changes, recording the user identity, timestamp (UTC), parameter changed,
old value, and new value.
```

### 3.6 Maintainability NFR Patterns

Maintainability requirements are the hardest to make testable because they concern
system properties observable only over the system lifecycle, not in a point-in-time test.

**Techniques for testable maintainability requirements:**

| Approach | Example |
|----------|---------|
| Structural metric | "No software module shall exceed 500 lines of code or 15 cyclomatic complexity" |
| Test coverage mandate | "The software shall achieve 100% statement coverage and 100% decision coverage in unit testing" |
| Change time requirement | "Any modification to the operating mode configuration shall require no more than 4 hours of engineering effort to implement, test, and validate" |
| Interface stability | "No change to the CAN message interface definition shall be required when adding a new ECU variant" |
| Diagnostic observability | "All configurable parameters shall be readable via the diagnostic interface without special hardware" |

Note: structural metric requirements (lines of code, cyclomatic complexity) are
controversial in some domains — they constrain implementation without being a direct
measure of the maintainability they are intended to proxy [unverified empirical data
on whether these metrics predict maintainability].

### 3.7 Planguage: Quantification Beyond Binary Pass/Fail

Planguage provides multi-level quantification for quality requirements, enabling
design-phase trade-off discussions [src-gilb-scales; src-modernanalyst-planguage].

**Core keywords:**
- `TAG` — unique hierarchical identifier (e.g., `Performance.Report.ResponseTime`)
- `AMBITION` — purpose statement driving the requirement
- `SCALE` — exact unit and measurement definition
- `METER` — how to actually make the measurement
- `GOAL` — minimum acceptable achievement level
- `FAIL` — threshold that constitutes outright failure
- `STRETCH` — more desirable target
- `WISH` — ideal aspiration
- `DEFINED` — clarifies specialized terms used in the specification

**Full example [src-modernanalyst-planguage]:**

```
TAG:      Performance.Report.ResponseTime
AMBITION: Reporting system generates accounting reports within user-acceptable time
SCALE:    Seconds from pressing Enter/OK to the beginning of report display on screen
METER:    Stopwatch testing on 30 representative reports on base user platform
GOAL:     No more than 8 seconds for 95% of reports
STRETCH:  No more than 2 seconds for predefined reports; 5 seconds for all others
WISH:     No more than 1.5 seconds for all reports
FAIL:     Any report exceeds 30 seconds
DEFINED:  Base user platform: [specific processor/RAM/OS/network spec]
```

**Why multi-level matters:** The GOAL/STRETCH/WISH progression enables the design
team to reason explicitly about what is acceptable vs. what would delight the customer.
The FAIL level establishes a hard gate that protects against regression during
optimization. Binary pass/fail requirements cannot express this range.

**The Scale definition principle [src-gilb-scales]:** "If you can't define a scale of
measure, then the goal is out of control." The act of writing a SCALE forces the
author to answer: what exactly are we measuring? This question frequently reveals
that the "requirement" was not a requirement at all — it was an aspiration.

---

## 4. Common Writing Mistakes and Defect Costs

### 4.1 Empirical Data on Requirements Defects

**Bosch automotive study (Langenfeld et al. 2016) — most rigorous available data
[src-langenfeld-bosch-2016]:**

- 588 requirements defects analyzed across a 4.5-year automotive project
- Classification based on IEEE 830 attributes with nine defect sources
- **61% of defects were due to incorrectness or incompleteness** — the majority class
- The most costly defects to fix were **incompleteness and inconsistency**
- Defect sources included parameters, wording, timing, and structural factors

**Cost escalation data (multiple sources, consistent with Boehm 1981 / NASA 2010):**

| When defect found | Cost relative to finding it in requirements |
|-------------------|---------------------------------------------|
| Requirements phase | 1x (baseline) |
| Design phase | ~5x |
| Integration/system test | ~10x |
| Production/operations | 29x–1500x (NASA range) / >100x (Boehm general) |

[src-nasa-cost-escalation; web-search-2026 summarizing Boehm 1981 and Boehm/Basili 2001]

Note: the 29x–1,500x range from NASA is a wider spread than Boehm's 100x figure; the
difference reflects project type and the severity of the defect, not contradictory data.

**Industry defect origin data [web-search-2026, multiple sources]:**
- ~50% of product defects and ~80% of rework effort trace to requirements engineering
  errors [unverified original source — widely cited, appears in NIST 2003 context]

**Requirements quality factor ontology (Rashid et al. 2021, 105-study systematic mapping
study [arxiv.org/2206.05959]):**
- 206 unique quality factors documented across 258 descriptions in the literature
- Only 9 factors were described three or more times: passive voice, anaphora, vagueness,
  sentence length, coordination ambiguity, consistency, and referential integrity are the
  most studied
- Only 32% (82 of 258) of quality factor descriptions had empirical validation or
  practitioner involvement — the majority of quality rules in use are theoretically
  motivated, not empirically validated

### 4.2 The Ten Most Expensive Requirement Defects

Based on the Bosch study [src-langenfeld-bosch-2016], Wiegers' practitioner analysis
[src-wiegers-reqtraps], and the codex anti-patterns [concept-requirement-quality], the
following defect types are consistently identified as highest-impact:

**Defect 1: Ambiguity (multiple valid interpretations)**

Ambiguity produces the worst outcomes because both parties believe they understood
correctly until integration. The "more insidious form" is where multiple readers
interpret a requirement differently but no single reader recognizes the ambiguity
[src-wiegers-reqtraps §Trap 3].

Detection method: Cross-perspective review (have someone in developer, tester, and
verification roles independently write a test for the requirement; compare the tests).

**Defect 2: Incompleteness (missing behaviors, states, or error conditions)**

The single largest defect class in the Bosch study (part of the 61%) [src-langenfeld-bosch-2016].
Common forms:
- Missing error/fault behavior (what happens when sensor fails?)
- Missing mode coverage (what happens during shutdown, startup, degraded operation?)
- Missing negative constraints (what is the system NOT permitted to do?)
- Interface requirements without error handling

**Defect 3: Inconsistency (requirements that contradict each other)**

The most expensive defect type to fix (ranked highest in Bosch study)
[src-langenfeld-bosch-2016]. Common forms:
- Two requirements that specify different bounds for the same parameter
- A timing constraint in one requirement that is physically impossible given other
  constraints
- Interface requirement that contradicts a behavior requirement
- Nominal behavior requirement inconsistent with degraded mode requirement

Detection: Consistency checks are best performed with automated tooling (NLP-based
cross-requirement analysis) or through structured inspections using traceability graphs.

**Defect 4: Untestability (no verifiable criterion)**

A requirement that cannot be tested cannot be verified. The test: ask "how would
you test this?" If the answer requires judgment rather than measurement, the
requirement is untestable. Common forms:
- "The system shall be highly reliable" (no metric)
- "The interface shall be user-friendly" (no measure)
- "The system shall support advanced security" (vague noun phrase)

[src-wiegers-reqtraps §Trap 3; concept-requirement-quality]

**Defect 5: Compound requirement (multiple behaviors in one)**

Compounds create partial verification: only one of the two stated behaviors may be
tested and verified. Auditors treat compound requirements as two requirements that
are inadequately managed. The keyword signature: "shall...and...shall" in one sentence.

**Defect 6: Missing derived requirements**

The seventh most common audit finding in safety-critical work [src-seed-requirement-syntax-beyond-ears §3.2].
When a design decision introduces a constraint that was not in the parent requirement,
a derived requirement must be written and flagged. Missing derived requirements are
a traceability gap AND a requirements gap simultaneously.

**Defect 7: Wrong abstraction level**

Two failure modes [src-seed-requirement-syntax-beyond-ears §3.2]:
- **Too abstract:** "The system shall process data efficiently" — no design can be
  derived from this
- **Too detailed (implementation prescription):** "The system shall use a hash table
  with a load factor of 0.75 to store session state" — constrains design choices
  without justification

The test for correct abstraction level: can two different valid implementations
satisfy this requirement? If only one implementation can, it is over-constrained.
If no implementation can be derived from it, it is under-specified.

**Defect 8: Passive voice without actor**

"Data shall be validated" — by whom? when? under what conditions? Passive voice
removes the agent (who/what is responsible for the action). INCOSE R2 mandates
active voice with explicit subject. In systems engineering, the subject must be
the system element responsible for the behavior, not an abstraction.

**Defect 9: Vague or subjective qualifiers**

The "banned word list" defect: "adequate," "reasonable," "fast," "sufficient,"
"appropriate," "user-friendly," "robust." These pass casual review because they
seem to say something meaningful, but they are untestable. The INCOSE 42-rule
framework addresses this in R7; the codex lists automated detection approaches
[concept-requirement-quality §Automated quality rules].

**Defect 10: TBD/TBR/TBS (incomplete requirements in the baseline)**

An open item in a baselined requirement set means verification cannot complete.
In DO-178C, every "shall" must be traceable to a test case. A "TBD" within
the requirement means the test case cannot be written, which means the
verification record is incomplete, which means certification cannot proceed.

### 4.3 Defect Interaction and Cascade

Defects rarely appear in isolation. A requirement that is ambiguous (Defect 1) will
often also be incomplete (Defect 2) and untestable (Defect 4). The combination creates
a cascade: the designer assumes one interpretation (implementing one behavior), the
tester assumes a different interpretation (writing a different test), and integration
fails with no clear path to resolution.

The Bosch study's finding that inconsistency and incompleteness are both high-cost
and high-frequency reflects this cascade: an incomplete requirement forces downstream
assumptions, and those assumptions create inconsistencies when they contradict each
other across the design [src-langenfeld-bosch-2016].

---

## 5. Requirement Granularity

### 5.1 The Atomic Requirement Principle

An atomic requirement is "a natural language statement that completely describes a
single system function, feature, need or capability including all information, details,
and characteristics." INCOSE encourages singularity (R18-R23 in the 42-rule framework)
as a formal characteristic [concept-requirement-quality].

**Why atomicity matters:**

1. **Testability:** One requirement → one test. Compound requirements cannot be
   verified as a unit; partial pass/fail states are ambiguous.
2. **Traceability:** Non-atomic requirements create many-to-many traceability links
   that obscure coverage gaps.
3. **Change control:** Atomic requirements can be modified, dropped, or re-prioritized
   independently. Compound requirements cascade changes.
4. **Metrics:** Requirement counts only mean something when each unit represents a
   single verifiable behavior. Mixed granularity makes metrics meaningless.

### 5.2 The "One Requirement, One Test" Principle and When It Breaks Down

The principle: each requirement should have exactly one corresponding test (or test
case set for equivalence classes). This produces a clean 1:1 traceability matrix.

**When it holds:** Functional and performance requirements with a single measurable
criterion map cleanly to single test cases.

**When it breaks down:**

**Equivalence class partitioning:** A single requirement ("The system shall accept all
valid user names") implies multiple test cases (valid name, boundary cases, invalid
names for negative testing). The requirement is singular; the tests are not. 1:N is
correct here. [Synthesized — standard testing practice]

**State-driven requirements:** "While in startup mode, the system shall apply default
values to all configurable parameters." This is one requirement but testing it
requires visiting every configurable parameter — N test cases for 1 requirement.
1:N is correct.

**Safety requirements with coverage targets:** A diagnostic coverage requirement of 99%
for a specific failure mode implies testing not just the nominal detection case but also
a statistical argument about failure modes. One requirement, many test cases and
potentially some analysis artifacts.

**The key distinction:** 1 requirement : N tests is fine (test cases exercise the same
behavior from multiple angles). N requirements : 1 test is NOT fine (one test cannot
independently verify multiple requirements; partial pass/fail is ambiguous).

### 5.3 When Is a Requirement Too Big?

Signals that a requirement is too large:

1. **Multiple actors:** "The system shall accept user input, validate it, transform it,
   and store it." — Four behaviors, four potential test failures.
2. **Multiple measurable criteria:** "The system shall respond within 500ms and consume
   less than 10MB of memory." — Two independent verification criteria; split into two
   requirements.
3. **"And/or" combinators:** The INCOSE R19 rule — any requirement containing "and" or
   "or" joining two behavioral clauses is a candidate for splitting.
4. **Multiple modes or scenarios in one requirement:** "The system shall process
   requests from internal and external users." — If internal and external users have
   different authentication or access rules, this is two requirements.
5. **Verb phrase count:** More than one "shall" clause per sentence is a definitive
   signal [concept-requirement-quality §Automated quality rules].

### 5.4 When Is a Requirement Too Small?

The opposite failure: over-atomization. A requirement can be too small when:

1. **It cannot stand alone:** "The fuel level shall be displayed" without specifying
   unit, precision, update rate, or display location is atomic but incomplete — it is
   too small to be verifiable or implementable on its own.
2. **It duplicates information available in referenced standards:** If the system is
   required to comply with ARINC 429, writing "data shall be transmitted as two-wire
   differential signals" is over-specification of a protocol requirement.
3. **It is a design decision, not a requirement:** "The retry counter shall be
   implemented as a uint8_t" is an implementation detail, not a system requirement.
4. **The granularity is below the architecture level of the document:** System
   requirements specify system-level behavior. Component-level details belong in
   software/hardware requirements, not system requirements.

**The architecture-level rule:** System requirements specify the behavior of the
system boundary (what goes in, what comes out, under what conditions). They do not
specify what happens inside the system unless internal behavior is directly observable
from outside (e.g., diagnostic outputs, built-in test results).

### 5.5 The Granularity Heuristic: The "Box" Test

A practical heuristic for correct granularity: the requirement describes what the
system's "black box" does when observed from outside. If you must look inside the
box to understand what the requirement means, it is either too detailed (it specifies
an internal mechanism) or too vague (it gives no observable behavior) [synthesized
from concept-detailed-design, codex, and feedback_two_rules_design.md].

The "one test" corollary: if you could write a complete, executable test for this
requirement without knowing anything about the internal implementation, it is at
the right level of abstraction.

---

## 6. Special Topics

### 6.1 Negative Requirements

"The system shall not X" requirements are legitimate but require discipline.

**When negative requirements are appropriate:**
- Safety envelopes: "The autopilot shall not issue pitch commands exceeding ±15°"
- Security prohibitions: "The system shall not store plaintext passwords"
- Independence constraints: "The primary and secondary channels shall not share
  common hardware resources"
- Regulatory prohibitions: "The system shall not transmit user data to third parties
  without explicit user consent"

**The testability transformation:** Every negative requirement can be transformed into
a positive test by identifying the observable violation:

| Negative requirement | Testable verification |
|----------------------|-----------------------|
| "Shall not exceed ±15°" | Monitor pitch commands, confirm all values within ±15° range |
| "Shall not store plaintext passwords" | Inspect storage: verify password fields contain hashed values |
| "Shall not share hardware resources" | FMEA analysis: confirm single-fault injection in one channel does not affect the other |

**The banned pattern:** "The system shall not fail to X" is a double negative that
should be rewritten as "The system shall X."

### 6.2 Conditional Requirements Completeness

A conditional requirement creates an implied obligation to cover ALL conditions.
Failure to do so produces requirements gaps.

**The conditional coverage pattern:**
- Write the primary behavior: "When condition A, the system shall do X"
- Write the complementary behavior: "When NOT condition A, the system shall do Y (or:
  the behavior is [specified by requirement N])"
- Write the fault behavior: "If condition A cannot be determined, the system shall do Z"

Missing the fault behavior is the most common gap. If a sensor provides condition A,
what does the system do when the sensor is unreliable or absent? This must be a
requirement, not a design decision.

### 6.3 Requirements for Multiple Operating Modes

Incomplete mode coverage is a documented incompleteness class [src-peterson-arp4754a-2015
per prior 03b research]. Every system mode requires dedicated requirements:

| Mode | Requirements needed |
|------|---------------------|
| Normal/nominal | All primary functional and performance requirements |
| Startup | Initialization behavior, pre-operational constraints |
| Shutdown | State preservation, safe-state achievement |
| Degraded (partial failure) | Reduced-capability behavior, what is maintained vs. lost |
| Emergency | Override behaviors, safety priority behaviors |
| Maintenance | Diagnostic access, self-test, built-in test |

A requirements set that covers only nominal operation is incomplete regardless of
how many requirements it contains.

### 6.4 The Priority of Requirement Writing Over Requirement Counting

A common management anti-pattern is treating requirement count as a proxy for
requirements quality. Counting requirements only works when requirements are:
(a) at a consistent granularity level, and (b) all verifiable.

A project with 1,000 well-written, atomic, verifiable requirements is better off
than a project with 5,000 vague, compound, unmeasured requirements. Metrics to
track instead of raw count:

- Percentage of requirements with explicit verification criteria
- Percentage free of vague/banned terms (automatable)
- Percentage of requirements with a corresponding test case (traceability metric)
- Number of TBD/TBR/TBS flags remaining in the baseline (incompleteness metric)
- Number of compound requirements (atomicity metric)

[synthesized from concept-requirement-quality, src-wiegers-reqtraps, src-nasa-npr-7123]

---

## 7. Source Notes and Gaps for Future Research

**Sources used directly (fetched and read in this session):**
- Wiegers 10 traps [src-wiegers-reqtraps] — fetched from hmc.edu mirror, all 10 traps documented
- Working Software NFR guide [src-workingsoftware-nfr] — ISO 25010 taxonomy, quality scenarios
- Modern Analyst NFR guide [src-modernanalyst-nfr] — five-step method, good/bad examples
- Modern Analyst Planguage guide [src-modernanalyst-planguage] — keywords, worked example
- Gilb Scales guide [src-gilb-scales] — methodsandtools.com, scale/meter framework
- FSR/TSR patterns [src-fsfirst-fsr-tsr] — timing patterns, safety requirement hierarchy
- NASA NPR 7123.1C [src-nasa-npr-7123] — MOE/MOP/TPM framework, "shall" language rules

**Sources accessed via abstract/summary only:**
- Langenfeld et al. 2016 Bosch study [src-langenfeld-bosch-2016] — abstract + project-page
  summary; full text is behind Springer paywall. Quantitative claims (61%, most-costly
  types) are from the abstract-level summary confirmed by multiple web sources.
- NASA cost escalation PDF [src-nasa-cost-escalation] — PDF binary-encoded, data
  retrieved via web search summaries referencing the report.
- Rashid et al. 2021 SMS [arxiv.org/2206.05959] — fetched full paper, data extracted

**Known gaps (topics not adequately covered by available open-access sources):**
- INCOSE GtWR v3 primary text (paywalled) — the 42-rule framework is adequately covered
  in the codex; deeper analysis of the standard's own examples is not available
- ISO/IEC/IEEE 29148:2018 primary text (paywalled) — referenced but not read
- Comparative empirical data on EARS vs. natural language vs. Planguage for defect
  prevention — no comparative study found in open access
- Empirical data on automated quality rule effectiveness (false positive/negative rates)
- Research on requirement granularity heuristics — practitioner guidance exists but
  empirical validation is sparse; the arxiv.org/2206.05959 ontology paper found only 32%
  of quality factor descriptions had empirical backing

**Recommended next sources to ingest (if primary access is obtained):**
- Robertson & Robertson "Mastering the Requirements Process" (VOLERE template)
- Wiegers & Beatty "Software Requirements 3rd edition" Chapter 13 (quality attributes)
- Mavin et al. "Big EARS" RE'16 paper (EARS extensions for complex conditional requirements)
