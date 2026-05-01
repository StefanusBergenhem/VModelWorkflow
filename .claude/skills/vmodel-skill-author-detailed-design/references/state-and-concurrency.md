# State and concurrency

When the leaf is stateless → State section is one line: *"Stateless between calls; all state lives in <where>."* Explicit absence is content; missing absence is a defect.

## Contents

- [Required parts when stateful](#required-parts-when-stateful) — inventory, transitions, undefined-event, entry/exit
- [State inventory — invariant per state](#state-inventory--invariant-per-state)
- [Transition table — five columns](#transition-table--five-columns)
- [Undefined-event handling — pick one per (state, event)](#undefined-event-handling--pick-one-per-state-event)
- [Hierarchy — when to decompose](#hierarchy--when-to-decompose)
- [Thread-safety per leaf — Goetz category](#thread-safety-per-leaf--goetz-category)
- [Cancellation contract — when long-running](#cancellation-contract--when-long-running)
- [Timing constraints — testable](#timing-constraints--testable)

## Required parts when stateful

| Part | Required when |
|---|---|
| **State inventory** with per-state invariants | Always (when stateful) |
| **Transition table** (source / event / guard / action / target) | Always |
| **Initial and terminal states** | Always |
| **Undefined-event handling** | Always — silence is dangerous |
| **Entry / exit actions** | When entering or leaving requires an action |

Slot-fill: `templates/state-machine.mmd.tmpl` (Mermaid skeleton).

## State inventory — invariant per state

A state without an invariant is just a name on a node. Every state names what is true while the leaf is in it.

```text
State PRICED
  invariant: cart.signed_quote IS NOT NULL
             AND cart.signed_quote.expires_at > now()
             AND cart.total = sum(line.line_total)

State COMPLETED
  invariant: cart.order_id IS NOT NULL
             AND no further mutation of cart fields permitted
```

## Transition table — five columns

| Source | Event | Guard | Action | Target |
|---|---|---|---|---|
| ACTIVE | finalise(idem_key) | cart non-empty AND quote valid | reserve; authorise | AUTHORISED |
| AUTHORISED | commit() | reservation valid | write order; emit; release | COMPLETED |
| AUTHORISED | timeout(60s) | — | release; void PSP | ACTIVE |

Every guard is a precondition for the transition. Every action is the side-effect commitment. Every target is unambiguous.

## Undefined-event handling — pick one per (state, event)

For every (state × event) NOT in the transition table, the DD names what happens:

| Choice | When appropriate |
|---|---|
| **Ignore** | Spurious / duplicate events; idempotent acceptance |
| **Log** | Should not happen but does not damage state |
| **Fault** | Transition to a fault state; reject further events until reset |
| **Raise** | Function raises typed `InvalidStateTransition`; caller decides |

A blanket *"undefined events are ignored"* is legitimate; leaving it unsaid is not — implementers will pick differently.

## Hierarchy — when to decompose

When the state machine exceeds ~10 states or does not fit on a page → decompose: hierarchical states with substates, or split into sibling leaves. Anti-pattern: state-explosion.

## Thread-safety per leaf — Goetz category

State the leaf's thread-safety category:

| Category | Contract |
|---|---|
| Immutable | State cannot change after construction |
| Thread-safe | All public ops safe for concurrent calls |
| Conditionally thread-safe | Some ops safe; others require external sync per a documented protocol |
| Thread-compatible | Caller must serialise |
| Thread-hostile | Cannot be made safe externally; single-threaded only |

Per shared field, name: which lock guards it, what happens-before relation is established, who reads / who writes. See `data-structures-by-invariant.md`.

Undocumented shared mutable field → finding `anti-pattern.designing-for-races`.

## Cancellation contract — when long-running

When the operation may run longer than the caller's patience → state:

| Element | Slot-fill |
|---|---|
| Signal | Cancellation token / context, sentinel input, none |
| Cooperative or abrupt | Polled at safe checkpoints, OR interrupted at any point |
| State after cancellation | No mutation, bounded mutation, compensated, undefined |
| What caller observes | Typed `Cancelled`, sentinel return, fire-and-forget ack |

No cancellation contract on a long-running op → finding `anti-pattern.missing-cancellation`.

## Timing constraints — testable

Every timing constraint states five things:

| Element | Example |
|---|---|
| Type | deadline / period / response time / jitter bound |
| Bound + unit | "p95 ≤ 200 ms"; "period 100 ms ± 5 ms" |
| Conditions | "under nominal load (≤ 50 req/s); not under saturation" |
| Upstream requirement | "REQ-052 — checkout latency budget" |
| Verification | "production metric `claim_latency_ms_p95`; alert on rolling 7-day regression" |

*"Shall execute quickly"* → finding `check.timing.unmeasurable`.

## Mermaid diagram — when

When the state count is small enough to fit on one page (≤ ~10 states) → use `templates/state-machine.mmd.tmpl`. The diagram complements the transition table; the table is the source of truth.

## Cross-link

`data-structures-by-invariant.md` (shared mutable state) · `function-contracts.md` (per-function thread-safety) · `error-handling.md` (undefined events as error class) · `anti-patterns.md`
