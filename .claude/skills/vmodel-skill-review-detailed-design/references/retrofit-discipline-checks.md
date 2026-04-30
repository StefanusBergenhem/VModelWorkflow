# Retrofit discipline checks

Mirrors `retrofit-discipline.md` on the author side. All checks here apply ONLY when front-matter declares `recovery_status:`.

## check.recovery-status.overview-reconstructed (HARD ★ refusal A — schema-enforced)

**Check that** when `recovery_status` is in map form, the `overview` key is `verified` or `unknown` only.

**Reject when** `recovery_status: { overview: reconstructed }` — schema enum violation; Overview carries intent (human-only).

**Approve when** the Overview key is `verified` (with cited human source) OR `unknown`.

**Evidence pattern:** quote the front-matter `recovery_status` block.

**recommended_action:** *"Change `overview: reconstructed` to `overview: unknown` (with follow-up) or `overview: verified` (with cited human source). Refusal A; schema enforces."*

## check.retrofit.human-only-content-marked-reconstructed (HARD ★ refusal A)

**Check that** rationale fields, rejected-alternatives, and original-intent are marked `verified` or `unknown` only.

**Reject when** any of these fields is marked `reconstructed`.

**Approve when** human-only fields use the two-value vocabulary.

**recommended_action:** *"Human-only fields cannot be `reconstructed`. Mark `verified` (with cited source) or `unknown` (with follow-up)."*

## check.retrofit.observed-not-marked-with-evidence (soft)

**Check that** every `reconstructed` field cites at least one of: file/line, commit hash, schema artifact, operational log reference.

**Reject when** `reconstructed` is bare (no evidence cited).

**Approve when** evidence is cited concretely.

**recommended_action:** *"Cite file/line, commit, schema, or operational log evidence per `reconstructed` field. Bare claims are not honest retrofit."*

## check.retrofit.derived-from-vague (soft)

**Check that** retrofit `derived_from` cites observable evidence, not categories.

**Reject when** `derived_from: [auth, security]` (categories) instead of `derived_from: ["observed_behaviour: src/auth/token.py:14"]`.

**Approve when** every entry cites a specific code / config / schema / log artifact.

**recommended_action:** *"Replace category-style entries with observable-evidence citations (file/line/commit/schema/log)."*

## check.retrofit.unknown-without-followup (soft)

**Check that** every `unknown` field is paired with a follow-up owner and action.

**Reject when** `unknown` is bare.

**Approve when** owner + action are stated; deadline optional.

**recommended_action:** *"Pair `unknown` with `follow_up: { owner, action, deadline? }`. Unknowns without follow-ups are dropped data."*

## check.retrofit.gap-report-missing (soft)

**Check that** retrofit DDs include a populated Gap Report section with four buckets: lost rationale, behavioural drift, missing ADRs, coverage gaps.

**Reject when** the section is absent or empty.

**Approve when** at least the buckets that have items are populated; bucket absence is acceptable when there are no items in that bucket.

**recommended_action:** *"Add the Gap Report section. Retrofit without a Gap Report is laundering by omission."*

## anti-pattern.laundered-retrofit (HARD ★ refusal A)

**Check that** retrofit DDs do not present the system as inevitable, well-considered, and free of ambiguity.

**Reject when** all of: zero `unknown` markings + Gap Report empty/missing + every rationale generic + diagram cleaner than reality.

**Approve when** the artifact acknowledges what was not preserved (with `unknown`s and follow-ups), surfaces drift, names missing ADRs.

**Evidence pattern:** identify the absence pattern (zero `unknown`s + empty Gap Report + all rationales generic). The combination is the laundering tell.

**recommended_action:** *"Apply retrofit discipline. Mark observed structure with file/line evidence; mark rationale `verified` or `unknown`; populate the Gap Report. Honest retrofit makes uncertainty visible."*

## Cross-link

`anti-patterns-catalog.md` (#16 fabricated-rationale, laundered-retrofit) · `quality-bar-gate.md` (Retrofit card) · `rationale-checks.md` · refusal A in `SKILL.md`
