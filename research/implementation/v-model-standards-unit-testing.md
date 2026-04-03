# V-Model Standards: Unit Testing and Test Derivation at the Software Unit Level

## Research Question

What do V-model standards specifically require for unit testing and test derivation? This document examines DO-178C, ASPICE/ISO 26262, and IEC 62304 to extract concrete requirements for test case design, coverage criteria, traceability, and independence at the software unit level. The goal is to inform our test derivation skill and ensure it produces artifacts that satisfy multiple standards simultaneously.

---

## 1. DO-178C — Software Verification at the Unit Level

### 1.1 Verification Process Structure (Section 6)

DO-178C Section 6 defines the software verification process. It does not use the term "unit testing" directly. Instead, it defines three testing levels (Section 6.4):

- **Low-level testing** — verifies low-level requirements (LLR); corresponds to unit testing
- **Software integration testing** — verifies software architecture and inter-module interfaces
- **Hardware/software integration testing** — verifies high-level requirements in the target environment

Low-level testing is the primary mechanism for verifying that source code correctly implements low-level requirements.

### 1.2 Requirements-Based Test Case Selection (Section 6.4.2)

DO-178C mandates **requirements-based testing**, not source-code-based testing. Test cases must be derived from requirements, not from reading code. Two categories of test cases are required:

**Normal range test cases (Section 6.4.2.1):**
- Demonstrate the software responds correctly to normal inputs and operating conditions
- Must exercise real and integer input values within their valid ranges
- Must cover each requirement with at least one test case

**Robustness test cases (Section 6.4.2.2):**
- Demonstrate the software responds correctly to abnormal inputs and conditions
- Required at DAL C and above
- Must include boundary values, error/exception handling paths, timing edge cases, invalid state transitions, and out-of-range inputs

DO-178C does not explicitly name "equivalence partitioning" or "boundary value analysis" as formal methods, but the robustness testing requirements implicitly demand boundary value testing. The requirement for normal range testing implicitly demands representative value selection from valid input domains (equivalence class thinking). Industry practice universally applies equivalence partitioning and BVA as the primary methods for satisfying Section 6.4.2 objectives.

### 1.3 Structural Coverage Criteria by DAL (Section 6.4.4)

Structural coverage analysis supplements requirements-based testing. It is used to determine whether additional test cases are needed, not as a primary test derivation method. The coverage criteria scale with assurance level:

| DAL | Coverage Criterion | Section Reference |
|-----|-------------------|-------------------|
| A | Modified Condition/Decision Coverage (MC/DC) | 6.4.4.2 |
| B | Decision Coverage (DC) | 6.4.4.2 |
| C | Statement Coverage (SC) | 6.4.4.2 |
| D | No structural coverage required | — |
| E | No verification objectives | — |

**Definitions:**
- **Statement Coverage (SC):** Every statement in the program has been invoked at least once.
- **Decision Coverage (DC):** Every decision (branch point) has reached all possible outcomes at least once.
- **MC/DC:** Every condition in a decision has been shown to independently affect that decision's outcome. Subsumes both SC and DC.

**Critical nuance:** Structural coverage is an adequacy check, not a test derivation method. If coverage analysis reveals unexecuted code, the response is either (a) add requirements-based test cases, (b) determine the code is dead code and justify, or (c) trace the gap to a missing requirement. DO-178C explicitly warns against writing tests "to the code" just to achieve coverage.

DAL A additionally requires **verification of source-to-object code traceability** — ensuring the compiler did not introduce unintended behavior.

### 1.4 Table A-7: Verification of Verification Process Results

Annex A, Table A-7 defines the objectives for verification of testing results. Key objectives and their applicability:

| Objective | Description | DAL A | DAL B | DAL C | DAL D |
|-----------|-------------|-------|-------|-------|-------|
| 1 | Test procedures are correct | Yes | Yes | Yes | — |
| 2 | Test results are correct and discrepancies explained | Yes | Yes | Yes | Yes |
| 3 | Test coverage of HLR is achieved | Yes | Yes | Yes | Yes |
| 4 | Test coverage of LLR is achieved | Yes | Yes | Yes | — |
| 5 | Test coverage of software structure (MC/DC) is achieved | Yes (indep.) | — | — | — |
| 6 | Test coverage of software structure (DC) is achieved | — | Yes | — | — |
| 7 | Test coverage of software structure (SC) is achieved | — | — | Yes | — |
| 8 | Test coverage of data coupling and control coupling is achieved | Yes | Yes | Yes | — |
| 9 | Verification of additional code not traceable to source code | Yes | Yes | Yes | — |

Note: "(indep.)" means the objective requires independence — the person performing the verification must not be the person who developed the item.

### 1.5 Independence Requirements

DO-178C requires verification independence at higher DALs:

- **DAL A:** Many verification objectives require independence, including structural coverage analysis. The verifier must not be the developer.
- **DAL B:** Some objectives require independence, particularly reviews.
- **DAL C/D:** Independence is recommended but generally not required for low-level testing.

Independence means organizational or personnel separation. The developer may execute unit tests, but a separate person must review and verify the test results and coverage analysis at DAL A.

### 1.6 Traceability Requirements (Section 6.3)

DO-178C requires bidirectional traceability through the entire V-model:

```
System Req --> HLR --> LLR --> Source Code
                |       |         |
                v       v         v
         HLR Tests  LLR Tests  Coverage Analysis
```

Specific traceability requirements for low-level testing:
- Every LLR must trace to at least one test case
- Every test case must trace to at least one LLR
- Test coverage analysis must demonstrate completeness of this mapping
- Structural coverage analysis must identify any code not traceable to requirements
- Dead code (code with no traceability to requirements) must be removed or justified

Section 6.4.4.3 (Data Coupling and Control Coupling) requires analysis of parameter passing and execution order dependencies at DAL C and above.

### 1.7 Test Documentation Requirements

DO-178C requires (Section 11):
- **Software Verification Cases and Procedures (SVCP):** The test specification — what is being tested, inputs, expected outputs, pass/fail criteria
- **Software Verification Results (SVR):** The actual results of test execution, including pass/fail status and any anomalies
- **Traceability Data:** Requirements-to-test-cases matrix
- **Coverage Analysis Report:** Structural coverage measurement results

**Sources:**
- Rapita Systems DO-178C Testing Guide: https://www.rapitasystems.com/do178c-testing
- QA Systems — Automating Requirements-Based Testing for DO-178C: https://www.qa-systems.com/wp-content/uploads/2020/12/automating-requirements-based-testing-for-do-178c.pdf
- Vector — Complete Verification and Validation for DO-178C: https://cdn.vector.com/cms/content/know-how/aerospace/Documents/Complete_Verification_and_Validation_for_DO-178C.pdf
- NASA — Certification of Safety-Critical Software Under DO-178C: https://ntrs.nasa.gov/api/citations/20120016835/downloads/20120016835.pdf
- Wikipedia — DO-178C: https://en.wikipedia.org/wiki/DO-178C
- Rapita Systems DO-178 Guidance: https://www.rapitasystems.com/do178
- AFuzion — DO-178C Common Gaps: https://afuzion.com/178c-common-gaps-close/
- AdaCore — DO-178C Reviews: https://www.adacore.com/blog/a-fresh-take-on-do-178c-software-reviews

---

## 2. ASPICE — SWE.4 Software Unit Verification

### 2.1 Process Purpose and Scope

ASPICE SWE.4 (Software Unit Verification) verifies software units to provide evidence of compliance with:
- The software detailed design (from SWE.3)
- Non-functional software requirements

SWE.4 sits at the bottom-right of the ASPICE V-model, directly mirroring SWE.3 (Software Detailed Design and Unit Construction) on the left side.

### 2.2 Base Practices

SWE.4 defines seven base practices:

**BP.1 — Develop verification strategy:** Define the strategy for verifying software units, including regression strategy. Must specify which methods (static analysis, dynamic testing, code review) apply to which types of units.

**BP.2 — Develop unit verification criteria:** Define criteria for verifying that each software unit complies with the detailed design and non-functional requirements. Criteria must be specific enough to be objectively evaluated.

**BP.3 — Perform static verification of software units:** Apply static analysis techniques:
- Static code analysis (tool-based)
- Code review / walkthrough (manual)
- Checks against coding standards and guidelines
- Complexity metrics analysis

**BP.4 — Perform dynamic testing of software units:** Execute unit tests against the defined criteria. Record test results. This is the actual test execution base practice.

**BP.5 — Ensure bidirectional traceability:** Establish bidirectional traceability between:
- Software detailed design elements and unit test specifications
- Unit test specifications and unit test results

The assessor explicitly expects linked test cases to design elements, not just loose test suites.

**BP.6 — Ensure consistency:** Ensure consistency and bidirectional traceability between the software detailed design and unit verification results. Verify that every design element has corresponding verification evidence and vice versa.

**BP.7 — Summarize and communicate results:** Summarize all unit verification results and communicate them to affected parties. Evidence that results have been formally reported is expected.

### 2.3 Work Products

| Direction | Work Product | ID |
|-----------|-------------|-----|
| Input | Software detailed design | 04-04 |
| Input | Software unit | 11-05 |
| Output | Unit verification strategy | 18-06 |
| Output | Unit test specification | 08-50 |
| Output | Unit test results | 13-50 |

### 2.4 What ASPICE Does NOT Specify

ASPICE is a process assessment model, not a safety standard. It deliberately does not prescribe:
- Specific coverage criteria (no "you must achieve MC/DC")
- Specific test derivation methods (no "you must use BVA")
- Specific tools or frameworks

The assessor evaluates whether the *process* is defined, followed, and produces adequate evidence — not which specific methods are used. However, the organization's own verification strategy (BP.1) must define these choices, and the assessor will evaluate whether those choices are appropriate for the project's context and risk level.

### 2.5 Traceability Granularity

ASPICE assessors expect traceability at the **design element level**, not at the file or module level. Specifically:
- Each function/method in the detailed design should trace to test cases that verify it
- Each test case should trace back to the design element(s) it verifies
- Coverage matrices or traceability matrices are the standard evidence format

**Sources:**
- Automotive SPICE SWE.4 Guide (UL/SIS): https://www.ul.com/sis/resources/process-swe-4
- ASPICE SWE.4 Shortened Reference: https://www.flecsim.de/images/download/AutomotiveSpiceShortened/Automotive%20Spice%203.1/SWE.4.html
- Synopsys — Preparing for ASPICE Assessment: https://www.synopsys.com/blogs/chip-design/preparing-for-automotive-spice-assessment.html
- Polarion Blog — SWE.4: https://polarion.code.blog/2023/01/18/swe-4-software-unit-verification/
- Kugler Maag CIE SWE.4 Whitepaper: https://www.kuglermaagcie.cn/fileadmin/whitepapers/ASPICE/whitepaper_automotive-spice_en_swe4_software-unit-verification.pdf

---

## 3. ISO 26262 — Part 6: Software Unit Testing

### 3.1 Context Within the Standard

ISO 26262 Part 6 (Product Development at the Software Level) addresses software unit testing in two key sections:
- **Section 9:** Software unit design and implementation (left side of V)
- **Section 10:** Software unit testing (right side of V)

Requirements scale with ASIL (Automotive Safety Integrity Level): ASIL A (lowest) through ASIL D (highest).

### 3.2 Test Derivation Methods (Part 6, Table 10)

ISO 26262 Part 6, Table 10 specifies methods for software unit testing with explicit ASIL-scaled recommendations. The notation: "++" = highly recommended (interpreted as required in practice), "+" = recommended, "o" = no recommendation for or against.

| Method | ASIL A | ASIL B | ASIL C | ASIL D |
|--------|--------|--------|--------|--------|
| Requirements-based testing | ++ | ++ | ++ | ++ |
| Interface testing | ++ | ++ | ++ | ++ |
| Fault injection testing | + | + | ++ | ++ |
| Resource usage evaluation | + | + | ++ | ++ |
| Back-to-back comparison test | o | + | + | ++ |

### 3.3 Test Case Derivation Methods (Part 6, Table 11)

Table 11 specifies methods for deriving test cases:

| Method | ASIL A | ASIL B | ASIL C | ASIL D |
|--------|--------|--------|--------|--------|
| Analysis of requirements | ++ | ++ | ++ | ++ |
| Generation and analysis of equivalence classes | + | ++ | ++ | ++ |
| Analysis of boundary values | + | ++ | ++ | ++ |
| Error guessing | + | + | + | + |

Key observations:
- **Equivalence partitioning** is highly recommended for ASIL B and above — this is one of the few standards that explicitly names this technique
- **Boundary value analysis** is highly recommended for ASIL B and above
- **Error guessing** is recommended (but not highly recommended) across all levels — it supplements systematic methods
- **Requirements analysis** is the universal baseline at all ASIL levels

### 3.4 Structural Coverage Criteria (Part 6, Table 12)

Table 12 specifies structural coverage metrics for unit testing:

| Coverage Metric | ASIL A | ASIL B | ASIL C | ASIL D |
|-----------------|--------|--------|--------|--------|
| Statement coverage | ++ | ++ | + | + |
| Branch coverage | + | ++ | ++ | ++ |
| MC/DC | o | + | + | ++ |

Key observations:
- **Statement coverage** is the baseline for all ASIL levels (highly recommended at A and B)
- **Branch coverage** is the primary metric from ASIL B upward
- **MC/DC** is only highly recommended at ASIL D (contrast with DO-178C where MC/DC is required at DAL A)
- The progression is less aggressive than DO-178C — ISO 26262 does not require MC/DC until the highest safety level

### 3.5 Robustness / Fault Injection

ISO 26262 explicitly requires fault injection testing at ASIL C and D (highly recommended). This includes:
- Injecting invalid inputs to verify error handling
- Testing resource exhaustion scenarios
- Verifying that safety mechanisms detect and handle faults

This is more explicit than DO-178C's robustness testing, which focuses on abnormal input ranges rather than deliberate fault injection.

### 3.6 Traceability

ISO 26262 Part 8, Section 6 requires bidirectional traceability:
- Software unit design to software unit test cases
- Software unit test cases to software unit test results
- Test coverage must be demonstrated through traceability matrices

### 3.7 Independence

ISO 26262 Part 6 specifies independence recommendations for verification:
- ASIL A/B: Person different from the developer is recommended
- ASIL C/D: Person different from the developer is highly recommended

Unlike DO-178C, ISO 26262 does not mandate independence; it recommends it with increasing strength at higher ASIL levels.

**Sources:**
- ISO 26262-6:2018 Standard (iTeh preview): https://cdn.standards.iteh.ai/samples/68388/34205953cd2c4c5f947890009caa464e/ISO-26262-6-2018.pdf
- Embitel — ISO 26262 Compliant Unit Testing: https://www.embitel.com/blog/embedded-blog/how-iso-26262-compliant-unit-testing-strategies-manifest-in-automotive-software-development
- Parasoft — ISO 26262 Unit Testing: https://www.parasoft.com/learning-center/iso-26262/unit-testing/
- Parasoft — ISO 26262 Code Coverage: https://www.parasoft.com/learning-center/iso-26262/code-coverage/
- Lorit Consultancy — ISO 26262 Verification Methods: https://lorit-consultancy.com/en/2024/06/iso-26262-verification-methods-boundary-values-and-error-guessing/
- Heicon Ulm — Fault Injection in ISO 26262: https://heicon-ulm.de/en/iso26262-fault-injection-test-do-you-really-need-it/
- Verifysoft — ISO 26262 Coverage: https://www.verifysoft.com/en_ISO_26262_Road_Vehicles_Functional_Safety.html

---

## 4. IEC 62304 — Software Unit Verification for Medical Devices

### 4.1 Safety Classification

IEC 62304 classifies medical device software into three safety classes:
- **Class A:** No injury or damage to health possible
- **Class B:** Non-serious injury possible
- **Class C:** Death or serious injury possible

### 4.2 Section 5.5 — Software Unit Verification

The applicability of unit verification requirements depends on safety class:

| Requirement | Section | Class A | Class B | Class C |
|-------------|---------|---------|---------|---------|
| Establish verification process | 5.5.1 | — | Yes | Yes |
| Define acceptance criteria | 5.5.2 | — | Yes | Yes |
| Verify software units meet acceptance criteria | 5.5.3 | — | Yes | Yes |
| Additional acceptance criteria (performance, error handling, memory) | 5.5.4 | — | — | Yes |
| Document verification results | 5.5.5 | — | Yes | Yes |

Key observations:
- **Class A requires no unit verification at all.** Only software requirements (5.2) and release (5.8) documentation are required.
- **Class B requires unit verification**, but the acceptance criteria can be satisfied through code review, static analysis, or inspection alone. Dynamic testing (actual unit test execution) is not mandatory.
- **Class C requires dynamic testing.** Acceptance criteria must include performance aspects, error handling, memory utilization, and other non-functional properties. Code review alone is insufficient.

### 4.3 Verification Methods

IEC 62304 is deliberately flexible about methods. It does not prescribe specific test derivation techniques. However, it provides examples of acceptable approaches:
- Code review / walkthrough
- Static code analysis
- Dynamic testing (unit tests)
- Formal verification

The manufacturer must define and justify their verification approach in the software development plan. The choice of methods should be commensurate with the safety classification.

### 4.4 What IEC 62304 Does NOT Say

Notably absent from IEC 62304:
- No specific coverage criteria (no statement/branch/MC/DC requirements)
- No named test derivation methods (no equivalence partitioning, BVA)
- No explicit structural coverage requirements
- No independence requirements for unit testing

This makes IEC 62304 the least prescriptive of the four standards examined. It is a process standard that says "verify your units" but leaves the how almost entirely to the manufacturer.

### 4.5 Traceability

IEC 62304 requires traceability between:
- Software requirements and software items (units)
- Software items and verification activities
- Verification results and requirements

The granularity is less detailed than ASPICE or ISO 26262, and traceability matrices are not explicitly required (though they are standard practice).

**Sources:**
- Johner Institute — Unit Testing and IEC 62304: https://blog.johner-institute.com/iec-62304-medical-software/unit-testing-iec-62304/
- Johner Institute — Safety Classes: https://blog.johner-institute.com/iec-62304-medical-software/safety-class-iec-62304/
- OpenRegulatory — Software Verification for IEC 62304: https://openregulatory.com/software-verification-medical-software-iec-62304/
- QA Systems — IEC 62304 Compliance: https://www.qa-systems.com/solutions/iec-62304
- Wikipedia — IEC 62304: https://en.wikipedia.org/wiki/IEC_62304

---

## 5. Cross-Standard Comparison

### 5.1 Test Derivation Strategies

| Strategy | DO-178C | ISO 26262 | ASPICE | IEC 62304 |
|----------|---------|-----------|--------|-----------|
| Requirements-based testing | Required (Section 6.4.2) | ++ all ASIL (Table 10) | Required (BP.4) | Expected but unspecified |
| Equivalence partitioning | Implied by normal range testing | ++ ASIL B-D (Table 11) | Not specified | Not specified |
| Boundary value analysis | Implied by robustness testing | ++ ASIL B-D (Table 11) | Not specified | Not specified |
| Error guessing | Not mentioned | + all ASIL (Table 11) | Not specified | Not specified |
| Robustness / abnormal inputs | Required DAL C+ (6.4.2.2) | Fault injection ++ ASIL C-D | Not specified | Class C expects error handling |
| Normal range testing | Required (6.4.2.1) | Covered by requirements-based | Covered by BP.4 | Covered by acceptance criteria |

**Key finding:** ISO 26262 is the only standard that explicitly names equivalence partitioning, boundary value analysis, and error guessing as test derivation methods. DO-178C requires the same practices in substance (normal range + robustness testing) but does not use these specific terms. ASPICE and IEC 62304 leave method selection to the project.

### 5.2 Structural Coverage by Assurance Level

| Level | DO-178C | ISO 26262 |
|-------|---------|-----------|
| Highest (DAL A / ASIL D) | MC/DC | MC/DC (++) |
| High (DAL B / ASIL C) | Decision Coverage | Branch Coverage (++) |
| Medium (DAL C / ASIL B) | Statement Coverage | Branch Coverage (++), Statement (++) |
| Low (DAL D / ASIL A) | None required | Statement Coverage (++) |
| Lowest (DAL E / QM) | None | None |

ASPICE and IEC 62304 do not specify structural coverage criteria. The project must define them in the verification strategy.

### 5.3 Error Handling / Robustness Testing

| Standard | Requirement |
|----------|-------------|
| DO-178C | Robustness test cases required at DAL C and above (Section 6.4.2.2). Must test boundary values, invalid inputs, error paths, timing. |
| ISO 26262 | Fault injection testing ++ at ASIL C/D, + at ASIL A/B. Resource usage evaluation ++ at ASIL C/D. Back-to-back testing ++ at ASIL D. |
| ASPICE | Not explicitly required, but verification criteria (BP.2) should cover non-functional requirements including error handling. |
| IEC 62304 | Class C requires acceptance criteria for error handling, memory utilization, and performance (Section 5.5.4). |

### 5.4 Independence Requirements

| Standard | Unit Testing Independence |
|----------|--------------------------|
| DO-178C | Required at DAL A for many objectives. Some objectives require independence at DAL B. Not required at DAL C/D. |
| ISO 26262 | ++ at ASIL C/D (person different from developer). + at ASIL A/B. |
| ASPICE | Not specified as a process attribute. Organization decides. |
| IEC 62304 | Not specified. |

### 5.5 Traceability Requirements

All four standards require traceability, but at different granularity:

| Standard | Required Traceability Links |
|----------|----------------------------|
| DO-178C | LLR <--> Test Cases <--> Test Results. Coverage analysis must identify untested requirements and unreachable code. Dead code must be justified or removed. |
| ISO 26262 | Unit design <--> Test cases <--> Test results. Traceability matrix expected. |
| ASPICE | Detailed design elements <--> Test specifications <--> Test results (BP.5, BP.6). Bidirectional. Assessor will verify linkage. |
| IEC 62304 | Requirements <--> Software items <--> Verification results. Less granular than others. |

**Common requirement across all standards:** Every design element / low-level requirement must have at least one test case, and every test case must trace back to at least one design element / requirement. Orphan tests (tests with no requirement link) and untested requirements are findings in all frameworks.

### 5.6 Test Documentation Requirements

| Artifact | DO-178C | ISO 26262 | ASPICE | IEC 62304 |
|----------|---------|-----------|--------|-----------|
| Test strategy / plan | SVP (Section 4) | Part 8 | BP.1 output | Software dev plan |
| Test specification (cases + procedures) | SVCP (Section 11) | Part 6 Section 10 | 08-50 work product | Acceptance criteria |
| Test results | SVR (Section 11) | Part 6 Section 10 | 13-50 work product | Section 5.5.5 |
| Coverage analysis | Required (6.4.4) | Required (Table 12) | Strategy-dependent | Not specified |
| Traceability matrix | Required (6.3) | Required (Part 8) | Required (BP.5) | Expected |

---

## 6. Relationship Between Detailed Design and Tests

### 6.1 How Tests Should Trace to Design

Across all standards, the fundamental principle is:

**Tests verify the design, not the code.**

- In DO-178C, tests are derived from Low-Level Requirements, not from reading source code. Code coverage is a completeness check, not a test design input.
- In ISO 26262, tests are derived from the software unit design specification. Table 11 methods (equivalence classes, boundary values) are applied to the design, not to the implementation.
- In ASPICE, SWE.4 explicitly verifies "compliance of the software units with the software detailed design" (SWE.3 output).
- In IEC 62304, acceptance criteria are defined before or alongside implementation, then verified.

### 6.2 Expected Granularity of Traceability

| Standard | Expected Granularity |
|----------|---------------------|
| DO-178C | Individual LLR to individual test case. Each LLR has unique ID. Each test case references the LLR(s) it verifies. |
| ISO 26262 | Software unit design element to test case. Typically function-level or behavior-level. |
| ASPICE | Design element (from SWE.3 detailed design) to test case. Assessors expect to be able to pick any design element and find its test. |
| IEC 62304 | Software requirement to verification activity. Coarser granularity is acceptable. |

### 6.3 Are Coverage Matrices Required?

- **DO-178C:** Yes. A requirements-to-test-cases traceability matrix is a required lifecycle data item. Structural coverage analysis results are also required.
- **ISO 26262:** Yes. Traceability is mandated in Part 8, and structural coverage metrics (Table 12) must be reported.
- **ASPICE:** Yes, effectively. BP.5 requires bidirectional traceability. A matrix is the standard way to demonstrate this in an assessment.
- **IEC 62304:** Not explicitly required, but assessors and notified bodies expect it. In practice, a traceability matrix is considered standard evidence.

---

## 7. Implications for Our Test Derivation Skill

Based on this research, a test derivation skill that satisfies the superset of these standards should:

1. **Always start from design/requirements, never from code.** This is the universal principle across all standards.

2. **Apply these test derivation methods in order:**
   - Requirements-based test cases (normal range) — universal baseline
   - Equivalence class partitioning — explicitly required by ISO 26262 Table 11 for ASIL B+
   - Boundary value analysis — explicitly required by ISO 26262 Table 11 for ASIL B+, implied by DO-178C robustness testing
   - Robustness / error handling test cases — required by DO-178C DAL C+, ISO 26262 ASIL C+ (fault injection)
   - Error guessing — recommended by ISO 26262 at all levels as a supplement

3. **Produce traceable artifacts:** Every test case must link to a specific design element or requirement. The skill should output a traceability matrix as a first-class artifact.

4. **Support coverage analysis:** The skill should indicate which design elements are covered and flag any gaps. Structural coverage is a separate analysis step (tool concern), but the skill should ensure requirements coverage is complete.

5. **Separate normal-range and robustness test categories:** DO-178C makes this distinction explicit, and it maps naturally to the valid/invalid partition split in equivalence partitioning.

6. **Document the test derivation rationale:** Standards expect evidence of systematic test case selection, not just a list of tests. The skill should explain why each test case exists (which requirement, which equivalence class, which boundary).
