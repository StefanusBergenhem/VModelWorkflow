# Code Review Checklist

A structured checklist for reviewing code against V-model standards, clean code principles, and AI-specific concerns. Usable by human reviewers and AI review agents.

---

## How to Use This Checklist

This is organized by concern area. Not every item applies to every review — use the **applicability** column to filter. Items marked "ALL" apply always. Items marked by assurance level apply when the project has that classification.

**Verdict criteria:**
- All "ALL" items must pass
- Items at the project's assurance level must pass
- Remaining items are recommendations

---

## 1. Design Compliance

Does the code implement the design — and only the design?

| # | Check | Applicability | Notes |
|---|-------|---------------|-------|
| 1.1 | Every code unit traces to a design element | ALL | No orphan code |
| 1.2 | Code follows the data flow defined in the design | ALL | Compare against design's data flow diagram |
| 1.3 | Code follows the control flow defined in the design | ALL | Sequence of operations matches design |
| 1.4 | No functionality beyond what the design specifies | ALL | Extra features = scope creep = untraceable code |
| 1.5 | Algorithms match the design specification | ALL | If design says "linear search", code does linear search |
| 1.6 | Interface signatures match the design | ALL | Parameter types, return types, exceptions |
| 1.7 | Error handling follows the design's error strategy | ALL | Consistent with design's error handling section |

**V-model reference:** DO-178C Table A-5 objectives 1, 2, 5; ASPICE SWE.3 BP.5, BP.6; ISO 26262 Part 6 Clause 8

---

## 2. Coding Standard Compliance

Does the code follow the project's coding standard?

| # | Check | Applicability | Notes |
|---|-------|---------------|-------|
| 2.1 | Naming conventions followed | ALL | Consistent with project glossary and style guide |
| 2.2 | Code formatting consistent | ALL | Automated formatter output, no manual formatting |
| 2.3 | Cyclomatic complexity within limits | ALL | Default: max 10 per function |
| 2.4 | Nesting depth within limits | ALL | Default: max 3-4 levels |
| 2.5 | Function length within limits | ALL | Default: max 50 lines, target under 20 |
| 2.6 | File length within limits | ALL | Default: max 500 lines, target under 300 |
| 2.7 | Parameter count within limits | ALL | Default: max 5, target 3 or fewer |
| 2.8 | No prohibited language features used | Medium+ | Per project language subset |
| 2.9 | Restricted features have documented justification | Medium+ | Per project language subset |
| 2.10 | Static analysis clean (no new violations) | ALL | Tool output attached to review |

**V-model reference:** DO-178C Section 11.8, Table A-5 objective 4; ISO 26262 Part 6 Table 1; IEC 62304 Section 5.5.3

---

## 3. Clean Code Principles

Is the code maintainable and understandable?

| # | Check | Applicability | Notes |
|---|-------|---------------|-------|
| 3.1 | Names reveal intent | ALL | No abbreviations unless universal (id, url, http) |
| 3.2 | Functions do one thing | ALL | Describable without "and" |
| 3.3 | One level of abstraction per function | ALL | No mixing of high-level and low-level operations |
| 3.4 | No boolean flag arguments | ALL | Split into separate functions |
| 3.5 | No side effects in query functions | ALL | Command-Query Separation |
| 3.6 | No dead code | ALL | Unreachable branches, unused methods, commented-out code |
| 3.7 | No magic numbers / strings | ALL | Named constants for all non-obvious literals |
| 3.8 | Classes have single responsibility | ALL | One reason to change |
| 3.9 | High cohesion within classes | ALL | All methods use most fields |
| 3.10 | Low coupling between classes | ALL | Communication through interfaces, simple parameters |
| 3.11 | Composition preferred over inheritance | ALL | Inheritance only for genuine "is-a" |
| 3.12 | Abstractions only at boundaries | ALL | No premature interfaces (YAGNI) |

---

## 4. Error Handling

Is error handling complete, consistent, and correct?

| # | Check | Applicability | Notes |
|---|-------|---------------|-------|
| 4.1 | All error paths are handled | ALL | No unhandled exceptions in public API |
| 4.2 | No swallowed exceptions | ALL | Empty catch blocks are bugs |
| 4.3 | Error messages include context | ALL | Operation, input, expected state |
| 4.4 | No null returns from methods | ALL | Use Optional, empty collections, Null Object |
| 4.5 | No null parameters | ALL | Validate at boundary, not everywhere |
| 4.6 | Fail-fast at boundaries | ALL | Validate inputs at system boundary, not deep inside |
| 4.7 | Error handling separate from business logic | ALL | Error handling functions do nothing else |
| 4.8 | Resource cleanup in finally/try-with-resources | ALL | No leaked connections, handles, streams |
| 4.9 | Boundary checking present | High | Explicit for all array/buffer/range operations |
| 4.10 | Memory management verified | High | No leaks, no overflow, initialization verified |

**V-model reference:** DO-178C Section 11.8 (error handling in coding standard); IEC 62304 Section 5.5.4 (Class C: fault handling, memory management); ISO 26262 Table 1, item 1d (defensive implementation)

---

## 5. Architecture Compliance

Does the code respect architectural boundaries?

| # | Check | Applicability | Notes |
|---|-------|---------------|-------|
| 5.1 | Business logic has no infrastructure imports | ALL | No database, HTTP, filesystem imports in domain code |
| 5.2 | Dependencies point inward only | ALL | Domain doesn't depend on adapters |
| 5.3 | Interfaces defined from consumer perspective | ALL | Ports defined by core, not by infrastructure |
| 5.4 | Layer boundaries respected | ALL | Each layer calls only the layer below/inside |
| 5.5 | No circular dependencies between packages | ALL | Verified by static analysis or build tool |
| 5.6 | External dependencies accessed through interfaces | ALL | No direct coupling to third-party APIs in business logic |
| 5.7 | New code follows existing patterns | ALL | Don't introduce a new pattern when one exists |

---

## 6. AI-Specific Checks

Additional checks when code was generated by an AI agent:

| # | Check | Applicability | Notes |
|---|-------|---------------|-------|
| 6.1 | APIs actually exist | ALL | Verify methods, params, return types against actual library docs |
| 6.2 | Dependencies are correct version | ALL | Package names, versions match project's dependency management |
| 6.3 | No hallucinated configuration | ALL | Config keys, environment variables actually exist |
| 6.4 | Logic verified with specific inputs | ALL | Mentally trace through with concrete values |
| 6.5 | Edge cases tested | ALL | null, empty, boundary, overflow, concurrent |
| 6.6 | Tests are not tautological | ALL | Tests should fail if implementation is wrong, not just different |
| 6.7 | No excessive abstraction | ALL | Interfaces, factories, indirection justified by actual need |
| 6.8 | Style matches existing codebase | ALL | Not just internally consistent — matches project conventions |
| 6.9 | No tutorial code patterns | ALL | Unnecessary CORS setup, demo logging, example comments |
| 6.10 | No hardcoded secrets or credentials | ALL | No API keys, passwords, tokens in source |

---

## 7. Traceability

Can every piece of code be traced through the V-model?

| # | Check | Applicability | Notes |
|---|-------|---------------|-------|
| 7.1 | Every code unit traces to a design element | ALL | Bidirectional: design -> code and code -> design |
| 7.2 | Every public interface traces to a requirement | Medium+ | Via design element |
| 7.3 | No orphan code | ALL | All code traceable to a requirement |
| 7.4 | No dead code | ALL | No unreachable code paths |
| 7.5 | Deactivated code is documented | High | DO-178C specific: even disabled code must be verified |

**V-model reference:** DO-178C Table A-5 objective 5; ASPICE SWE.3 BP.5; ISO 26262 Part 8 Section 6

---

## Review Record

When used formally, document the review as:

```yaml
review_record:
  reviewer: [name]
  date: [date]
  code_under_review: [module/file/PR reference]
  design_reference: [design document ID]
  coding_standard_reference: [coding standard ID and version]
  static_analysis_report: [attached/referenced]
  checklist_version: "1.0"
  findings:
    - id: F-001
      checklist_item: 4.2
      severity: major
      description: "Exception swallowed in ConfigLoader.load() catch block"
      resolution: required
  verdict: [approved / approved_with_conditions / rejected]
```

---

## Sources

- RTCA DO-178C, Table A-5, Section 6.3.4
- ISO 26262:2018, Part 6, Tables 1, 6, 9
- Automotive SPICE PAM, SWE.3, SWE.4
- IEC 62304:2006+AMD1:2015, Section 5.5
- Robert C. Martin, *Clean Code* (2008)
- Stack Overflow Blog, AI agent studies (2026)
