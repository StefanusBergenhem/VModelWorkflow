---
id: ARCH-IF-IValidate
belongs_to: ARCH
kind: architecture-interface-detail
subject: IValidate
scope: ""
status: draft
date: "2026-05-04"
version: 3
---

# IValidate — interface detail

```yaml
preconditions:
  - "ArtifactSet and TraceabilityGraph are well-formed."
  - "embedded-resources is reachable (compile-time bundle intact per REQ-031)."

postconditions:
  on_success:
    - "Emits zero or more finding-records (REQ-006), each in REQ-026 five-field shape."
    - "All five rule classes evaluated (REQ-010..REQ-014); envelope + per-type schema (REQ-015/016); QB structural (REQ-017)."
    - "Channel closed when evaluation completes."
  on_precondition_failure:
    - "Closes channel without emission; returns typed error (ErrPreconditionFailed)."
  on_downstream_failure:
    - "Closes channel after emitting any pre-halt findings; returns typed error (ErrSystemError); signals system-error track per REQ-004."

invariants:
  - "Findings emitted in source-document iteration order on the channel; stable byte-order applied downstream by emitter (REQ-029)."
  - "Output is a function of (ArtifactSet, TraceabilityGraph, embedded-resources content) only (REQ-031)."

errors:
  - { code: "ErrPreconditionFailed", meaning: "Inputs malformed before validation could begin." }
  - { code: "ErrSystemError",        meaning: "Non-recoverable per REQ-004; halt." }

quality_attributes:
  determinism: "given identical inputs, the multiset of findings is identical run-to-run; ordering stabilised at emit time."
  latency: "dominates REQ-022 budget; breakdown in *Quality attributes (allocated)*."

authentication: "n/a — in-process call."
authorisation: "n/a — in-process call."

version: "internal — same scheme as IArtifactLoad."
deprecation_policy: "Internal — same scheme as IArtifactLoad."
```
