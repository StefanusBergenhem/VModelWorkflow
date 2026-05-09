# `verifies` traceability

The `verifies:` field is the load-bearing traceability link from a TestSpec to the upstream world. Two scopes: the artifact-level `verifies:` (a union over upstream IDs covered by this TestSpec) and the per-case `verifies:` (one or more upstream IDs the case is asserting against). Both are mandatory non-empty (refusal B).

## The hard rule (refusal B)

Refuse to emit:
1. Artifact-level `verifies: []`.
2. A case missing the `verifies:` field, or `verifies: []`.
3. A `verifies:` element that does not resolve to a live ID in the upstream artifacts.

Tells: empty list at artifact level; case missing the field; `verifies` value resolves to nothing in any upstream artifact; `verifies` references look like file paths (`src/auth/token.py:42`) instead of artifact IDs (`DD-auth-session-validator.public_interface.validate.postconditions.on_success`).

## Granularity per layer

Granularity follows layer. Pointing a leaf case at a root requirement is a granularity mismatch (soft-reject); the leaf case verifies a DD field, not a root requirement.

| Layer | `verifies:` element points at | Form |
|---|---|---|
| **Leaf** | A DD field or sub-field | `DD-<scope>.public_interface.<name>.<clause>` or `DD-<scope>.data_structures.<name>.<invariant>` |
| **Branch** | An Architecture interface or composition invariant | `ARCH-<scope>.interfaces.<name>` or `ARCH-<scope>.composition.<invariant_id>` |
| **Root** | A requirement or a PB outcome | `REQ-<id>` or `PB-outcome-<id>` |

Field-level qualification is permitted and encouraged at leaf — `DD-x.behavior.earliest_of_idle_and_absolute` is more precise than `DD-x` and lets the reviewer tell which clause is being verified.

## Slot-fill

```yaml
# Artifact-level (front-matter)
verifies:
  - "<upstream-ID-1>"
  - "<upstream-ID-2>"

# Per-case
- id: TC-<scope>-001
  verifies:
    - "<upstream-ID-1>"
    - "<upstream-ID-2>"      # multiple permitted when one case asserts a property over multiple upstream elements
```

## Empty-scope worked example

Per the empty-scope ID rule (TARGET_ARCHITECTURE §5.4), at root scope (`scope: ""`) the scope segment is omitted from derived identifiers — so `verifies:` entries pointing at root-scope artifacts use the bare prefix. Never emit `DD-.field`, `ARCH-.interfaces.X`, or `TC--001`.

```yaml
# Root scope (scope: "") — verifies entries against root-scope artifacts.
# Bare `DD`, `ARCH` prefixes; `REQ-NNN` and `PB-outcome-X` carry no scope at any layer.

# Artifact-level (front-matter)
verifies:
  - "REQ-007"
  - "PB-outcome-collaboration-onboarding"
  - "ARCH.interfaces.OrderPlacement"

# Per-case
- id: TC-001
  verifies:
    - "REQ-007"
- id: TC-002
  verifies:
    - "DD.public_interface.sort.postconditions.on_success"
```

```yaml
# Branch / leaf scope (scope: "cart-service" or "session-store/expiry-calculator") — suffix appears.

# Artifact-level (front-matter)
verifies:
  - "ARCH-cart-service.interfaces.OrderPlacement"

# Per-case
- id: TC-cart-service-001
  verifies:
    - "ARCH-cart-service.interfaces.OrderPlacement.postconditions.on_accept"
- id: TC-session-store-expiry-calculator-001
  verifies:
    - "DD-session-store-expiry-calculator.public_interface.sort.postconditions.on_success"
```

## Resolution check

When authoring → for each `verifies:` element, confirm the ID exists in the upstream spec being read (DD / Architecture / Requirements / PB). When the ID does not exist:

| Cause | Action |
|---|---|
| Typo | Fix to the canonical ID |
| Upstream spec is missing the element this case implies | HALT — the gap is in the upstream spec, not the TestSpec; surface as a question to the human |
| The element exists under a different name | Rename to the canonical ID; do not silently rewrite |
| The element should exist but does not (retrofit) | Mark `recovery_status: unknown` on the case; the link is reconstructed without confirmation |

## When one case verifies many upstream elements

A property case may assert an invariant that spans multiple postconditions or interfaces — the `verifies:` list carries one entry per upstream element the property covers. Do not collapse to a single ID when the property genuinely covers multiple.

When the count grows beyond ~4 upstream elements per case → the case is doing too much; split into multiple cases or escalate the property to an artifact-level invariant covered by a dedicated property test on a higher-level abstraction.

## Anti-patterns this rule prevents

- **Orphan tests** — cases with no upstream link cannot be verified for coverage; deletion has no effect on derivation traceability.
- **Granularity-mismatched cases** — a leaf case pointing at `REQ-001` reveals that the leaf author skipped the DD layer's contract.
- **`verifies` as path or filename** — paths point at code/test files; the TestSpec verifies *spec elements*, not files.

## Implicit-verifies rule

When a case's `preconditions:` or `expected:` text mentions a specific upstream identifier (`REQ-\d+`, `IC-\d+`, `ADR-\d+`, `ARCH\.\w+`), that identifier MUST appear in the case's `verifies:` list. The text reference is the case's commitment to verifying that upstream content; omitting it from `verifies:` produces a silent traceability gap. Pre-publish self-check: `scripts/check-implicit-verifies.py` greps each case for upstream-id patterns and cross-references against `verifies:`.

Granularity convention: a parent ID in `verifies:` covers any sub-path mentioned in prose (`ARCH.interfaces.IValidate` covers `ARCH.interfaces.IValidate.errors.ErrInvalidVerdict`). A specific sub-path in `verifies:` covers itself only.

## Cross-link

`testspec-purpose-and-shape.md` (the layer→parent-spec mapping) · `dd-traceability-cues.md` / `architecture-traceability-cues.md` / `requirements-traceability-cues.md` (per-layer seam files showing which IDs to point at) · `retrofit-discipline.md` (`recovery_status: unknown` for reconstructed `verifies`) · `anti-patterns.md` (`anti-pattern.orphan-tests`)
