# ADR-propagation landing rules

When a governing ADR's `propagation.bindings:` block names a specific library, protocol, or framework bound to this scope, the binding lands in the matching Decomposition entry's `rationale` field, citing the ADR by id. It does NOT land in `purpose`, in `responsibilities`, in any interface `operation` signature, or in any other field that names what the component owns architecturally.

This file is a one-page rule. The landing rule is mechanical; the rest of architecture authoring is judgement.

## The headline rule

ADR-bound mechanism choices land in `rationale` only.

| Field | Carries | What MUST NOT appear |
|---|---|---|
| `purpose` | One sentence — what cross-component effect this child has | The library / protocol / framework name that realises that effect |
| `responsibilities` | At most three architectural-level effects | The mechanism realising any of them |
| `interface.operation` (signature) | Operation name, parameters, return type | Library types or framework primitives below the architectural level |
| `rationale` | One line per driver, OR one line per ADR-bound binding citing the ADR by id | — |

## Why the boundary matters

Architecture states **what a component owns** ("renders HTML reports", "accepts artifact-loader requests"). The ADR-cited rationale states **which mechanism satisfies the ownership** ("per ADR-001 — `html/template` chosen for stdlib-only deployability"). The two are different artifacts of thought. Naming the mechanism in responsibility smuggles implementation prescription into a layer that is supposed to be implementation-free at the boundary.

Two consequences flow from the rule:

1. A reader of `responsibilities` can swap the mechanism without rewriting the architecture — the responsibility is unchanged.
2. The ADR retains exclusive ownership of the binding. When the binding changes, one ADR is superseded; no architecture text edits are required beyond updating the rationale citation.

## Two-row example

The example uses ADR-001 binding `html/template` to the `reporter` Decomposition child.

### Positive — binding lands in `rationale`

```yaml
- id: reporter
  purpose: "Render review findings as a static HTML report a reviewer opens locally."
  responsibilities:
    - "Materialise traceability views from artifact-loader output."
    - "Emit a single self-contained HTML file under reports/."
  rationale:
    - "per ADR-001 — html/template chosen for stdlib-only deployability."
```

The mechanism appears once, in `rationale`, citing ADR-001 by id. `purpose` and `responsibilities` describe what the component owns, agnostic of mechanism.

### Negative — binding leaks into `responsibilities`

```yaml
- id: reporter
  purpose: "Render review findings as a static HTML report a reviewer opens locally."
  responsibilities:
    - "Render HTML using html/template per ADR-001."         # <-- leak
    - "Emit a single self-contained HTML file under reports/."
```

Fires `arch.adr-bound-mechanism-leaked` from `scripts/check-adr-landing.py`. The mechanism appears in `responsibilities`, conflating *what is owned* with *how it is realised*. Even though the ADR is cited, the citation is in the wrong field — a downstream reader treats the mechanism as architecturally load-bearing rather than rationale-load-bearing.

## Mechanical detection

`scripts/check-adr-landing.py` reads the governing ADR's `propagation.bindings:` block, walks each binding's `name`, and flags any matching name that appears outside `rationale` in the architecture artifact bound by `governing_adrs`. The check runs at Step 13 (Pre-publish mechanical self-check) of architecture authoring.

The script does not enforce that bindings ARE cited in `rationale` — that is a coverage check belonging to the matched review skill. It only flags placement defects: bindings appearing in the wrong field.

## Cross-link

`decomposition-discipline.md` (one-sentence-purpose, banned-fields rule) · `interface-contracts.md` (operation signature shape) · `adr-extraction-cues.md` (when to extract a decision to ADR) · `templates/decomposition-entry.yaml.tmpl` (slot for `rationale` with the binding-landing comment)
