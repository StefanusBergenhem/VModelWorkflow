---
id: DD-app-checkout-discount
artifact_type: detailed-design
title: "Walker Fixture — Discount Calc Detailed Design"
scope: "app/checkout"
parent_scope: "app"
parent_architecture: ARCH-app
status: active
date: "2026-05-10"
version: 1
governing_adrs:
  - ADR-001-use-redis
---

## Public Interface

```yaml
name: calculate_discount
signature: "calculate_discount(cart: Cart, code: str) -> Discount"
preconditions: ["cart is non-empty"]
postconditions: ["returns valid Discount"]
```
