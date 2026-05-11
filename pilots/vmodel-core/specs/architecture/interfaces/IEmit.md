---
id: ARCH-IF-IEmit
title: "vmodel-core — IEmit interface detail"
artifact_type: architecture-interface-detail
belongs_to: ARCH
kind: architecture-interface-detail
subject: IEmit
scope: ""
status: draft
date: "2026-05-12"
version: 4
---

# IEmit — interface detail

```yaml
preconditions:
  - "EmitValidation: findings channel will be closed by producer when done; verdict is one of {pass, fail, system-error} (REQ-027)."
  - "EmitReport: doc is the HTML document produced by reporter."
  - "sink is a writable byte sink (typically stdout)."

postconditions:
  on_success:
    - "Emitted bytes are determined solely by (input arguments, output format) — REQ-029."
    - "EmitValidation: exactly one verdict-record (REQ-001) plus zero-or-more finding-records (REQ-026), in JSON or text per REQ-024."
    - "EmitReport: emitted bytes are the HTML document unchanged."
    - "Findings emitted in stable order keyed by (artifact path, location-within-artifact, rule identifier) per REQ-029 + ADR-001 Negative #3."
  on_precondition_failure:
    - "Returns typed error before writing any bytes (ErrInvalidVerdict, ErrUnsupportedFormat)."
  on_downstream_failure:
    - "Returns typed error if sink fails during write (ErrSinkWrite); run becomes system-error per REQ-004."

invariants:
  - "Sole producer of bytes on the validation track."
  - "No collection traversal that depends on Go map iteration order leaks into emit output (REQ-029 / ADR-001 mitigation)."

errors:
  - { code: "ErrInvalidVerdict",    meaning: "Verdict value not in {pass, fail, system-error}." }
  - { code: "ErrUnsupportedFormat", meaning: "OutputFormat not in {JSON, text} for EmitValidation, or not HTML for EmitReport." }
  - { code: "ErrSinkWrite",         meaning: "Underlying sink returned a write error; system-error path." }

quality_attributes:
  determinism: "load-bearing — REQ-029."
  latency: "O(findings + verdict bytes); minor relative to validation cost."

authentication: "n/a — in-process call."
authorisation: "n/a — in-process call."

version: "internal — same scheme."
deprecation_policy: "Internal — same scheme."
```
