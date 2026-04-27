---
id: REQS-session-service-RETROFIT
scope: session-service
parent_scope: ecommerce-platform
derived_from:
  - <observed_evidence>
status: draft
date: 2026-04-26
recovery_status:
  glossary: reconstructed
  requirements: reconstructed
  rationale: reconstructed   # ← VIOLATION — see annotation 1
---

# Retrofit Requirements — session-service

A team runs a retrofit agent against a four-year-old internal session service. The original designers have left; no decision records are preserved. The agent produced this document.

## Counter-example — what NOT to do

This example shows fabricated rationale, smuggled design, and laundered current state — three of the most common AI-era anti-patterns. Every numbered annotation marks a defect.

```yaml
- id: REQ-R-session-001
  statement: |
    The session service shall use a 30-minute idle timeout for all sessions.
  # ❌ ANNOTATION 2 — IMPLEMENTATION PRESCRIPTION DISGUISED AS REQUIREMENT
  # The "30 minutes" is a configuration value of the deployed system, not a
  # requirement. The requirement should describe the *behaviour* — that the
  # session transitions to IDLE after a period of inactivity — and leave the
  # specific timeout to per-tenant configuration policy (ADR territory).
  #
  # The fabricated form locks the configuration value into the requirements
  # document, where future per-tenant tuning becomes a "requirements change"
  # rather than a configuration change.

  rationale: |
    30 minutes balances security (limiting session hijack windows) with user
    experience (avoiding frequent re-authentication). This is an industry-
    standard timeout value chosen after consultation with the security team.
  # ❌ ANNOTATION 3 — FABRICATED RATIONALE
  # Three tells of fabrication, all present:
  #
  # (a) "industry-standard" — generic phrase, no specific source cited.
  # (b) "consultation with the security team" — no record of any consultation
  #     exists; the original team has left and no decision documents remain.
  # (c) "balances X with Y" — generic reasoning that could be applied to any
  #     timeout value (10, 30, 60, 120 minutes all "balance" the same things).
  #
  # The agent generated boilerplate that "sounds right". A future reviewer
  # reading this rationale will cite "the security team" as the source — for
  # a decision the security team never made.
  #
  # CORRECT FORM: rationale: unknown; rationale_recovery_status: unknown;
  #               follow_up: queue a security-team review.

  derived_from: [user-experience, security]
  # ❌ ANNOTATION 4 — VAGUE NON-ARTIFACT REFERENCES
  # "user-experience" and "security" are not artifact identifiers. They are
  # categories. Real `derived_from` links point to specific upstream
  # artifacts (parent requirements, decisions, user stories) or, in retrofit,
  # to observed evidence (file:line, commit, log entry).

  recovery_status: reconstructed
  # ❌ ANNOTATION 1 — ILLEGAL recovery_status FOR RATIONALE
  # The rationale field is human-only. Allowed states: `verified` or `unknown`.
  # `reconstructed` is forbidden because rationale cannot be reconstructed
  # from observable code — only the behaviour can. A retrofit agent that
  # emits `reconstructed` for a rationale field is fabricating the rationale.
```

## How to fix it — honest retrofit of the same requirement

```yaml
- id: REQ-R-session-001
  type: functional
  statement: |
    While a session has had no recorded authenticated activity for 30 minutes,
    the session service shall transition the session to the IDLE state and
    shall reject subsequent validation requests for that session with status
    401 and reason 'idle-timeout'.
  statement_recovery_status: reconstructed
  # ✅ Behaviour is observable from code: session_service.py:L245-L268 enforces
  # the 30-minute timeout against config value session.idle_timeout_seconds=1800.
  # `reconstructed` is the right state for the behaviour field.

  rationale: unknown
  rationale_recovery_status: unknown
  # ✅ No preserved record of why 30 minutes was chosen. Honest "unknown" is the
  # correct retrofit outcome — not a defect, not a partial result, not a gap
  # to paper over.

  follow_up:
    - owner: "@security-team"
      action: |
        Confirm whether 30-minute idle timeout is the intended policy for this
        service. If not, raise a change request with the proposed value and
        rationale.

  derived_from:
    - "observed_behaviour: session_service.py:L245-L268"
    - "observed_config: config/prod.yaml#session.idle_timeout_seconds = 1800"
  # ✅ derived_from points to specific observed evidence, not to abstract
  # categories. A future reader can verify the source.
```

## What this counter-example teaches

1. **Rationale is human-only in retrofit.** The behaviour can be reconstructed from code; the *why* cannot. An agent that emits `recovery_status: reconstructed` for a rationale field is signalling fabrication.

2. **Honest "unknown" beats fabricated "plausible".** The honest version tells a future reader exactly what is known (the behaviour) and what is not (the reason). A team reading the honest version can act on the gap. A team reading the fabricated version believes a story that was never true.

3. **Configuration values do not belong in requirement statements.** The "30 minutes" is a deployed configuration. The requirement is the *shape* of the behaviour, parameterised by configuration that lives elsewhere.

4. **`derived_from` links must be concrete.** "user-experience" and "security" are not artifacts. File-line citations, commit hashes, and configuration references are. In retrofit, every link must be verifiable.

5. **Generic rationale phrases are red flags.** "Industry-standard", "best practice", "balances X with Y", "after consultation with X" — when these appear without a specific source, treat them as fabricated until proven otherwise.
