# Rationale capture

Capture rationale at decision time, at the site of the decision.

## Two forms — pick by load-bearing weight

| Form | When |
|---|---|
| **Inline rationale** (parenthetical, short note, sentence next to the clause) | Most decisions |
| **ADR** (linked via `governing_adrs:`, body-cited at application point) | Decision is **load-bearing AND cross-cutting AND hard-to-reverse** — see `adr-extraction-cues.md` |

Default to inline. Promote to ADR only when all three criteria hold.

## Inline-rationale slot-fills

```text
postcondition: "<property>"
rationale: "<one sentence naming the forcing constraint — REQ-NNN, ADR-NNN,
            or named trade-off>"
```

```text
algorithm: "<result property>"
rationale: "<why the algorithm choice is contractual or implementer's call>"
```

```text
recovery: <strategy>
rationale: "<the constraint that forces this strategy>"
```

Test for sufficient rationale: a future maintainer reads the rationale and can answer *"What would force me to revisit this?"*

## The four constraint kinds — name one

Every rationale states which kind of constraint is forcing the decision:

| Kind | Examples |
|---|---|
| **External** | Standard, platform limitation, certification, contractual SLA. *"AWS API Gateway 29s integration timeout"*; *"PCI-DSS 4.0 §3.2"* |
| **Architectural** | Choice made at a higher scope. *"Single-threaded event loop per ARCH-…"*; *"Idempotency required because parent saga retries on timeout"* |
| **Resource** | Timing, memory, capacity budget. *"Hot path; ≤ 2 ms"*; *"Streaming-read; cannot buffer"* |
| **Temporal** | Correct now; expected to lift. *"Preserves pre-v2 shape; relaxes when v1 clients retired"* |

Form: `[kind: external | architectural | resource | temporal]` followed by the constraint statement. Kind tells the future reader whether the constraint is permanent or expected to lift.

## What is NOT rationale

| Phrase | Why it fails |
|---|---|
| "Follows best practice" | Whose? In what circumstance? |
| "Clean separation of concerns" | Which concerns? Why drawn here? |
| "Industry-standard pattern" | Which industry? Cited where? |
| "Balances flexibility and performance" | What trade-off, in concrete terms? |
| "Single-responsibility / SOLID / DDD" | Name-drop without specific application |

These are **confident precisely where a real rationale would be specific**. On retrofit → finding `anti-pattern.fabricated-rationale` (refusal A, hard-reject). On greenfield → finding `check.rationale.generic-principle-invocation` (soft-reject).

## When the forcing constraint is an ADR — cite, don't paraphrase

```text
recovery: retry (max 2, exponential backoff with jitter)
rationale: "Per ADR-019 — DB write idempotency under at-least-once delivery"
```

Don't restate the ADR's contents; reference it. ADR rationale lives in the ADR.

## Where rationale lives in the artifact

| Decision lands at | Rationale lives at |
|---|---|
| Public Interface clause (postcondition / invariant / error) | Inline next to the clause OR per-entry `rationale:` |
| Data structure invariant | Per-field invariant text OR per-structure `rationale:` |
| Algorithm contractuality | Inline in Algorithms section |
| State transition guard | Inline next to the guard OR per-transition note |
| Error matrix row's recovery | Inline next to the strategy OR per-row note |
| Cross-cutting load-bearing | ADR (separate artifact); referenced via `governing_adrs:` |

## When rationale is unknown (retrofit)

Use `unknown` with a follow-up — never an invention.

```yaml
rationale:
  status: unknown
  note: |
    No design notes preserved. Observed in code (file:line) and config
    (path:key). Forces driving the choice not recoverable.
  follow_up:
    owner: "@team-lead"
    action: "Confirm under current threat model; supply rationale or propose revision."
```

`unknown` without follow-up → finding `check.retrofit.unknown-without-followup`.

## Cross-link

`adr-extraction-cues.md` · `retrofit-discipline.md` · `anti-patterns.md` · refusal A in `SKILL.md`
