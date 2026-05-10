---
id: TS
artifact_type: test-spec
title: "Walker Fixture — Root TestSpec"
scope: ""
parent_scope: null
level: system
status: active
date: "2026-05-10"
version: 1
verifies:
  - REQ-001
---

## Test Cases

```yaml
id: TC-001
title: "Discovery finds all artifacts"
type: functional
verifies:
  - REQ-001
inputs: {}
expected: ["all artifact ids present in graph"]
```
