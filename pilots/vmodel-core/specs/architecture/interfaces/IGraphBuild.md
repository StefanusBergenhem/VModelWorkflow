---
id: ARCH-IF-IGraphBuild
belongs_to: ARCH
kind: architecture-interface-detail
subject: IGraphBuild
scope: ""
status: draft
date: "2026-05-04"
version: 3
---

# IGraphBuild — interface detail

```yaml
preconditions:
  - "ArtifactSet entries have well-formed front-matter."

postconditions:
  on_success:
    - "Returns TraceabilityGraph (artifacts as nodes; canonical link types as labelled directed edges)."
    - "Returns zero or more cycle findings (REQ-012) in REQ-026 shape."
    - "Enumeration order is stable per ArtifactSet (REQ-029)."
  on_precondition_failure:
    - "Returns typed error (ErrMalformedFrontMatter); cli-adapter treats as system-error per REQ-004."
  on_downstream_failure:
    - "n/a — pure in-memory."

invariants:
  - "Computed fresh per invocation — no caching (IC-002)."

errors:
  - { code: "ErrMalformedFrontMatter", meaning: "Front-matter is structurally malformed beyond what the loader caught; halt." }

quality_attributes:
  determinism: "graph topology and cycle-finding emission are pure functions of ArtifactSet content."
  latency: "O(N) over artifacts + edges; budgeted under REQ-022/023."

authentication: "n/a — in-process call."
authorisation: "n/a — in-process call."

version: "internal — same scheme as IArtifactLoad."
deprecation_policy: "Internal — same scheme as IArtifactLoad."
```
