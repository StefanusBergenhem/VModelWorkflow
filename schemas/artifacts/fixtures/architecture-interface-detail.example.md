---
id: ARCH-IF-ShortenRequest
title: "URL Shortener — ShortenRequest interface detail"
artifact_type: architecture-interface-detail
belongs_to: ARCH
kind: architecture-interface-detail
subject: ShortenRequest
scope: ""
status: active
date: "2026-05-12"
version: 1
---

# ShortenRequest — interface detail

```yaml
preconditions:
  - "Request body contains a non-empty 'url' string."
  - "Request 'url' parses as a syntactically valid HTTP or HTTPS URL per RFC 3986."

postconditions:
  on_success:
    - "Response is HTTP 201 with JSON body containing 'code' (≤10 chars, alphanumeric) and 'url' (the original URL)."
    - "The pair (code, url) is persisted in redis-store with SET NX semantics; readers see the pair within the consistency model of redis-store."
  on_precondition_failure:
    - "Response is HTTP 422 with body containing 'error: invalid-url'."
    - "No state change in redis-store."
  on_downstream_failure:
    - "Response is HTTP 503 with body containing 'error: storage-unavailable' when redis-store is unreachable."
    - "No partial pair is left in redis-store."

invariants:
  - "Same input URL produces the same response code value across retries within one binary lifetime (idempotency on the SET NX branch)."
  - "Response time stays within the latency budget regardless of the URL's path length."

errors:
  - { code: invalid-url, http: 422, meaning: "The supplied URL is not a valid HTTP or HTTPS URL." }
  - { code: storage-unavailable, http: 503, meaning: "redis-store is unreachable; caller may retry." }

quality_attributes:
  latency: "p99 ≤ 200 ms under 500 concurrent requests"
  availability: "Inherits root composition's redundancy posture; no per-interface SLO overrides."

authentication: "Bearer token (issued by upstream auth gateway); validated by the API gateway before this handler runs."
authorisation: "Any authenticated caller may shorten any URL. Per-caller rate limiting at gateway (REQ-rate-limit), not enforced here."

version: "v1 — additive-only within major. New optional fields in request and response are permitted; new exit codes for new failure modes are permitted; removal is breaking."
deprecation_policy: "Minimum 90 days notice before any v1 surface element is deprecated; documented in API change log."
```
