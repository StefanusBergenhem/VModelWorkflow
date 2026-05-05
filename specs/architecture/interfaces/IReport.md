---
id: ARCH-IF-IReport
belongs_to: ARCH
kind: architecture-interface-detail
subject: IReport
scope: ""
status: draft
date: "2026-05-04"
version: 3
---

# IReport — interface detail

```yaml
preconditions:
  - "ArtifactSet and TraceabilityGraph are well-formed."
  - "request identifies a v1 report type (REQ-018..REQ-021) with appropriate parameters."
  - "embedded-resources reachable (criterion catalog needed for REQ-019 completeness)."

postconditions:
  on_success:
    - "Returns one self-contained HTML document (REQ-018..REQ-021)."
    - "Byte-identical for byte-identical inputs (REQ-029)."
  on_precondition_failure:
    - "Returns typed error (ErrUnknownReportType, ErrInvalidParameters); no HTML emitted."
  on_downstream_failure:
    - "n/a — no remote dependencies."

invariants:
  - "Read-only over inputs."
  - "Self-contained HTML per REQ-025 (no external asset references in v1)."

errors:
  - { code: "ErrUnknownReportType", meaning: "Requested report type is not in the v1 set." }
  - { code: "ErrInvalidParameters", meaning: "Parameters do not satisfy the report type's contract." }

quality_attributes:
  determinism: "REQ-029."
  latency: "dominated by graph traversal cost for impact-analysis (REQ-021); shape per REQ-022/REQ-023."

authentication: "n/a — in-process call."
authorisation: "n/a — in-process call."

version: "internal — same scheme."
deprecation_policy: "Internal — same scheme."
```
