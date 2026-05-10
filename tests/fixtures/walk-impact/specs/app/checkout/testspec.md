---
id: TS-app-checkout
artifact_type: test-spec
title: "Walker Fixture — Checkout Leaf TestSpec"
scope: "app/checkout"
parent_scope: "app"
level: unit
status: active
date: "2026-05-10"
version: 1
verifies:
  - DD-app-checkout-discount
---

## Test Cases

```yaml
id: TC-checkout-001
title: "calculate_discount returns Discount for non-empty cart"
type: functional
verifies:
  - DD-app-checkout-discount
inputs:
  cart: {items: ["a"]}
  code: "SAVE10"
expected: ["returns Discount object"]
```
