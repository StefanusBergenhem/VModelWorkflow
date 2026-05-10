---
id: ARCH-IF-IArtifactLoad
belongs_to: ARCH
kind: architecture-interface-detail
subject: IArtifactLoad
scope: ""
status: draft
date: "2026-05-04"
version: 3
---

# IArtifactLoad — interface detail

```yaml
preconditions:
  - "target is well-formed and readable to the running process."
  - "filesystem reachable (IC-004)."

postconditions:
  on_success:
    - "Returns ArtifactSet — one entry per artifact in scope, each holding parsed front-matter, Markdown body, embedded YAML blocks, raw Mermaid blocks."
    - "Enumeration order is stable per (target, filesystem state) — supports REQ-029 emit-time keying."
  on_precondition_failure:
    - "Returns typed error (ErrTargetUnreadable, ErrTargetNotFound) and an empty ArtifactSet."
  on_downstream_failure:
    - "Returns typed error (ErrParseFailure, ErrIOFailure); halts the walk per REQ-004."
    - "May return zero or more partially-loaded artifacts; caller treats as system-error track per REQ-004."

invariants:
  - "Read-only on filesystem (IC-003)."
  - "No network access (REQ-031)."

errors:
  - { code: "ErrTargetUnreadable", meaning: "Supplied target path exists but is not readable." }
  - { code: "ErrTargetNotFound",   meaning: "Supplied target path does not exist." }
  - { code: "ErrParseFailure",     meaning: "YAML/Markdown structure could not be parsed; halt-and-report per REQ-004." }
  - { code: "ErrIOFailure",        meaning: "Filesystem IO error during the walk; halt-and-report per REQ-004." }

quality_attributes:
  determinism: "stable enumeration; per-artifact parse output is a function of file bytes only."
  latency: "single-artifact parse fits within REQ-022 budget allocation."

authentication: "n/a — in-process call."
authorisation: "n/a — in-process call."

version: "internal — versioned with vmodel-core MAJOR (ADR-001 / REQ-024)."
deprecation_policy: "Internal — vmodel-core MAJOR-version compatibility regime."
```
