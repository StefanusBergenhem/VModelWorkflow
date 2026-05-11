---
id: ARCH-IF-IFrameworkResources
title: "vmodel-core — IFrameworkResources interface detail"
artifact_type: architecture-interface-detail
belongs_to: ARCH
kind: architecture-interface-detail
subject: IFrameworkResources
scope: ""
status: draft
date: "2026-05-12"
version: 4
---

# IFrameworkResources — interface detail

```yaml
preconditions:
  - "artifactType (where applicable) is one of the seven framework-canonical types."

postconditions:
  on_success:
    - "Returns the bound content as compiled into the binary at build time (REQ-030)."
    - "Versions() returns build-time VersionManifest (REQ-032)."
    - "Multiple calls return content byte-identical to itself across binary lifetime (immutable post-build)."
  on_precondition_failure:
    - "Returns typed error (ErrUnknownArtifactType) for Schema / QualityBarChecklist on unknown artifactType."
  on_downstream_failure:
    - "n/a — bundle is in-binary; absence is a build-time failure."

invariants:
  - "No filesystem read outside the binary's compiled-in embed.FS (REQ-031)."
  - "No network access (REQ-031)."
  - "Returned content is read-only; mutating it is undefined behaviour."

errors:
  - { code: "ErrUnknownArtifactType", meaning: "artifactType is not one of the seven framework-canonical types." }

quality_attributes:
  determinism: "content bound at build time; runtime accessor is a pure function over (binary bytes)."
  latency: "decode is sub-millisecond at expected scale (sub-megabyte JSON inputs per ADR-002 Assumption #5)."

authentication: "n/a — in-process call."
authorisation: "n/a — in-process call."

version: "internal — same scheme."
deprecation_policy: "Internal — same scheme."
```
