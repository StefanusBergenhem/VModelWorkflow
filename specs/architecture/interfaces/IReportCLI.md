---
id: ARCH-IF-IReportCLI
belongs_to: ARCH
kind: architecture-interface-detail
subject: IReportCLI
scope: ""
status: draft
date: "2026-05-04"
version: 3
---

# IReportCLI — interface detail

```yaml
preconditions:
  - "Parameters identify a v1 report type (REQ-018..REQ-021) and a readable target scope (REQ-025 precondition)."
  - "vmodel-core binary is executable (IC-004)."

postconditions:
  on_success:
    - "Exactly one self-contained HTML document on stdout (or caller-supplied output path per [DEFER-DD: cli-adapter — output destination handling])."
    - "Process exit code 0."
    - "No mutation of adopter spec tree (IC-003)."
    - "Byte-identical output for byte-identical input (REQ-029)."
  on_precondition_failure:
    - "Diagnostic on stderr; exit code 2 (REQ-025 error_handling — shares mapping with REQ-028)."
    - "No mutation of adopter spec tree (IC-003)."
  on_downstream_failure:
    - "n/a (REQ-031)."

invariants:
  - "Read-only on adopter spec tree (IC-003)."
  - "Stateless between invocations (IC-002)."
  - "No filesystem read outside the binary (REQ-031)."
  - "No network access (REQ-031)."

errors:
  - { code: "system-error", exit_code: 2, meaning: "Non-recoverable system-level failure during report production." }

quality_attributes:
  determinism: "REQ-029."
  latency: "REQ-022 shape applies (targets pending pilot calibration)."
  cold_start: "the only state (IC-002)."

authentication: "n/a at application layer (same as IValidationCLI)."
authorisation: "n/a at application layer (same as IValidationCLI)."

version: "v1 — additive-only-within-major (REQ-025 versioning)."
deprecation_policy: "Shared with IValidationCLI per REQ-025; pending `[DEFER-ADR: CLI deprecation notice period]`."
```
