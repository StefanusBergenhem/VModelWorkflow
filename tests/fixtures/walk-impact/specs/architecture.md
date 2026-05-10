---
id: ARCH
artifact_type: architecture
title: "Walker Fixture — Root Architecture"
scope: ""
parent_scope: null
status: active
date: "2026-05-10"
version: 1
derived_from:
  - PB
  - REQS
governing_adrs:
  - ADR-001-use-redis
---

## Decomposition

```yaml
id: walker-engine
purpose: "BFS over reverse-link graph"
responsibilities:
  - "Walks reverse edges"
allocates:
  - REQ-001
  - REQ-002
```
