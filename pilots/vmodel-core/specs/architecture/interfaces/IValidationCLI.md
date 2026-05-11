---
id: ARCH-IF-IValidationCLI
title: "vmodel-core — IValidationCLI interface detail"
artifact_type: architecture-interface-detail
belongs_to: ARCH
kind: architecture-interface-detail
subject: IValidationCLI
scope: ""
status: draft
date: "2026-05-12"
version: 4
---

# IValidationCLI — interface detail

```yaml
preconditions:
  - "Supplied input identifies a readable artifact, scope path, or spec-tree root accessible to the invoking process (REQ-024 precondition #1)."
  - "vmodel-core binary is executable on the invoking host (IC-004)."

postconditions:
  on_success:
    - "Exactly one verdict-record on stdout (REQ-001)."
    - "Each rule violation reported as exactly one finding-record (REQ-006, shape per REQ-026)."
    - "Process exit code 0 on pass / 1 on fail (REQ-028)."
    - "No mutation of adopter spec tree (IC-003)."
    - "Byte-identical output for byte-identical input (REQ-029)."
  on_precondition_failure:
    - "Diagnostic on stderr; exit code 2 (system-error per REQ-024 error_handling)."
    - "No mutation of adopter spec tree (IC-003)."
  on_downstream_failure:
    - "n/a — no remote downstream dependencies (REQ-031)."

invariants:
  - "Read-only on adopter spec tree (IC-003)."
  - "Stateless between invocations (IC-002)."
  - "No filesystem read outside the binary for framework canonical inputs (REQ-031)."
  - "No network access (REQ-031)."

errors:
  - { code: "system-error", exit_code: 2, meaning: "Non-recoverable system-level failure during the run; verdict-record value is 'system-error' per REQ-005." }
  # Note: 'pass' (exit 0) and 'fail' (exit 1) are verdict outcomes per REQ-027, not error conditions.

quality_attributes:
  determinism: "REQ-029."
  latency: "REQ-022 (targets pending pilot calibration); composition-level budget breakdown in *Quality attributes (allocated)*."
  scale: "REQ-023 (targets pending pilot calibration)."
  cold_start: "the only state — IC-002."

authentication: "n/a at application layer — OS-level identity only."
authorisation: "n/a at application layer — OS file permissions only."

version: "v1 — additive-only-within-major (REQ-024 versioning)."
deprecation_policy: "Pending product-scope ADR per REQ-024 follow-up: `[DEFER-ADR: CLI deprecation notice period]`. Until accepted, no v1 surface element may be deprecated."
```
