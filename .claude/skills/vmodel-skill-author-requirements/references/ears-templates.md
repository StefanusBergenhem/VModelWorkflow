# EARS templates

EARS = Easy Approach to Requirements Syntax. Five sentence templates that cut most of the ambiguity out of natural-language requirements by forcing the author to classify the requirement before writing it.

Use EARS as the default sentence shape for every functional requirement and every unwanted-behaviour requirement. NFRs use the five-element rule (see `nfr-five-elements.md`); interface requirements use the five dimensions (see `interface-five-dimensions.md`).

## The five patterns

### 1. Ubiquitous (always-on invariant)

Template:

```
The <system> shall <response>.
```

When to use: behaviour that is true without a trigger or state condition. Used for system-wide invariants.

Example:

```
REQ-001: The session service shall use a cryptographically secure pseudo-random
         number generator for all session token generation.
```

### 2. Event-driven (When)

Template:

```
When <trigger>, the <system> shall <response>.
```

When to use: stimulus-response. The trigger is a discrete event; the response fires once per trigger.

Example:

```
REQ-002: When a user submits a valid credential pair, the session service shall
         create a new session, persist it in the ACTIVE state, and return the
         session token and its absolute-timeout expiry timestamp.
```

### 3. State-driven (While)

Template:

```
While <state>, the <system> shall <response>.
```

When to use: behaviour that persists for the duration of a named mode or condition.

Example:

```
REQ-003: While a session is in the IDLE state, the session service shall reject
         validation requests for that session with status 401 and reason
         'idle-timeout'.
```

**State-driven complementary pair rule.** Every While-statement implicitly raises the question: what does the system do *outside* that state? Either author the complementary pair, or explicitly mark out-of-state as out of scope. → See `statement-quality.md`.

### 4. Optional-feature (Where)

Template:

```
Where <feature>, the <system> shall <response>.
```

When to use: behaviour conditional on a configuration or deployment variant.

Example:

```
REQ-004: Where the tenant has enabled multi-factor authentication, the session
         service shall require step-up authentication before promoting a session
         to the ELEVATED state.
```

### 5. Unwanted-behaviour (If/then)

Template:

```
If <condition>, then the <system> shall <response>.
```

When to use: error paths, fault responses, security violations. Every "shall not" candidate should be rephrased as a positive "shall" under an unwanted condition.

Example:

```
REQ-005: If three consecutive credential-validation attempts for the same user
         account fail within 10 minutes, then the session service shall lock
         the account for 15 minutes and shall emit a 'credential-lockout' audit
         event.
```

## Compound templates

Keywords combine in canonical order:

```
Where → While → When → If/then → shall
```

**Compound limit: at most two keywords per statement.** Three or more keywords means the statement is carrying multiple requirements that need to be split.

Example (Where + When, two keywords):

```
REQ-006: Where the tenant plan is Enterprise, when an elevated session requests
         a bulk export larger than 10 MB, the session service shall enqueue the
         export to the long-running-job queue and shall return a job token with
         status 202.
```

When you find yourself writing a three-keyword compound, stop and split. The result is two or three atomic statements, each easier to test and trace.

## EARS cargo-culting — the trap to avoid

EARS grammar without underlying discipline produces statements that *look* rigorous and *are* vacuous. Reject these and require revision:

```
BAD:  "When the system experiences load, the system shall respond appropriately."
      Structurally event-driven, semantically empty. "Load" is undefined,
      "appropriately" is unmeasurable.

GOOD: "When the session-validation endpoint receives more than 5,000 concurrent
       requests, the session service shall queue requests beyond that ceiling
       and shall return them in FIFO order within the request's timeout window."
```

The remedy is not "write better EARS" but "force the author to pass the box test" — see `statement-quality.md`. EARS is a framing for thinking, not a shield against it.

## When EARS is not the right fit

EARS handles functional and unwanted-behaviour requirements well. It is less natural for:

- **NFRs with multi-level targets** — use the five-element rule (`nfr-five-elements.md`) and Planguage's tiered form
- **Multi-step scenarios with pre- and post-conditions** — Given-When-Then (GWT) is more natural; GWT maps cleanly to EARS (Given ↔ While, When ↔ When, Then ↔ shall)
- **Temporal/duration expressions beyond simple triggers** — EARS does not forbid "within 5 seconds of …" but their detection and enforcement is author discipline

The default is EARS for the requirement statement; GWT may appear in the optional `acceptance` block when the statement alone leaves conditions ambiguous; Planguage appears inside NFR target specifications. Do not mix two structured forms inside one statement.
