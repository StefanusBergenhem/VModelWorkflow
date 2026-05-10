---
id: ARCH-app
artifact_type: architecture
title: "Walker Fixture — App Architecture"
scope: "app"
parent_scope: ""
status: active
date: "2026-05-10"
version: 1
derived_from:
  - REQS-app
---

## Decomposition

```yaml
id: discount-calc
purpose: "Computes discount for a cart"
responsibilities:
  - "Apply discount rules"
allocates:
  - REQ-app-001
```
