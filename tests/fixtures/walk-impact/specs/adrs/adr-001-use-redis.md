---
id: ADR-001-use-redis
artifact_type: adr
title: "Use Redis for the walker cache (fixture)"
status: accepted
date: "2026-05-10"
version: 1
scope_tags:
  - ""
---

## Context

Fixture ADR for the walker test. Multiple downstream artifacts cite it via
governing_adrs.

## Decision

Use Redis.

## Alternatives Considered

- PostgreSQL — slower for this workload.
- In-memory dict — no persistence.

## Consequences

- Operational complexity rises slightly.
- Reversibility: yes — swap to a different KV store with a one-day migration.
