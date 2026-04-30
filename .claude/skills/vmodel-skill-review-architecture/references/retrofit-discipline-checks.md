# Retrofit discipline checks

Mirrors the author-side `retrofit-discipline.md`. **All checks in this file apply only when `recovery_status:` is declared in front-matter.** Greenfield documents skip this entire file.

Two of the five checks are HARD (refusal A class). The honesty test is whether human-only content (rationale, rejected alternatives, original intent) is allowed to be `unknown` rather than fabricated.

## check.retrofit.observed-not-marked-with-evidence (soft)

**Check that** every observed structural claim (Decomposition entry, Interface entry, observed wiring) marked `recovery_status: reconstructed` cites at least one evidence reference: file path + line range, commit hash, schema artifact, or operational log reference.

**Reject when** a `reconstructed` field has no citation, OR cites only "the codebase" without specific file/commit/schema reference.

**Approve when** every `reconstructed` claim cites at least one concrete evidence type. (Multiple sources are encouraged but not required.)

**Evidence pattern:** quote the field with `recovery_status: reconstructed` and note the absence of a citation.

**recommended_action:** *"Add an evidence citation to the reconstructed field — file:line range, commit hash, schema artifact, or operational log. Reconstruction without citation is fabrication with extra steps."*

## check.retrofit.human-only-content-marked-reconstructed (HARD — refusal A)

**Check that** human-only fields — rationale, rejected_alternatives, original_intent, decision_record — are NEVER marked `recovery_status: reconstructed`. Allowed values are `verified` (with human source cited) or `unknown` (with follow-up owner) only.

**Reject when** any human-only field carries `recovery_status: reconstructed`. This is the most consequential single rule violation in retrofit; one occurrence rejects the document.

**Approve when** every human-only field is `verified` or `unknown` only.

**Evidence pattern:** quote the field name and the illegal `reconstructed` value.

**recommended_action:** *"Change to `verified` (with human source cited) or `unknown` (with follow-up owner queued). Reconstructing rationale from observable code is fabrication — the value cannot be derived from artifacts the rationale field is meant to carry."*

## check.retrofit.unknown-without-followup-owner (soft)

**Check that** every `recovery_status: unknown` field is paired with a follow-up owner and an action.

**Reject when** an `unknown` field has no `follow_up:` block, OR the follow-up names no owner / no action / both.

**Approve when** every `unknown` is paired with: an owner (`@person` or role), a concrete action (verify, propose redecomposition, supply rationale), and ideally a deadline.

**recommended_action:** *"Pair every `unknown` with a follow-up owner and action. `unknown` without follow-up is a fact resigned-to, not a finding; follow-ups make the gap actionable."*

## check.retrofit.gap-report-missing (soft)

**Check that** the retrofit document carries a Gap report populating four buckets: lost rationale, structural drift, missing ADRs, coverage gaps.

**Reject when** retrofit-mode and no Gap report section exists, OR the section exists but one or more buckets is empty AND the document has any `unknown` fields, observed cycles, or unallocated parent requirements (which are exactly what should populate the buckets).

**Approve when** the Gap report exists and each bucket either has entries OR explicitly states "no items" with a brief justification.

**recommended_action:** *"Populate the Gap report — lost rationale (where rationale is unknown), structural drift (where the diagram differs from runtime), missing ADRs (load-bearing decisions with no preserved record), coverage gaps (parent requirements with no observable allocation). A retrofit artifact without a Gap report is laundered by omission."*

## check.retrofit.laundering-detected (HARD — refusal A)

**Check that** the retrofit document does not present a clean, polished story that contradicts observable runtime mess.

**Reject when** the document has zero `unknown` markings, zero items in the Gap report's structural-drift or lost-rationale buckets, every rationale generic ("follows DDD", "single-responsibility"), AND the diagram looks too clean for a system that was retrofitted.

**Approve when** the document acknowledges accidental boundaries, structural drift, lost rationale, and missing ADRs honestly. The diagram should look like reality, including the messy parts.

**Evidence pattern:** name the absence pattern (zero unknowns + zero gap-report items + generic rationales + clean diagram). The combination is the laundering tell.

**recommended_action:** *"Stop laundering. Mark fields `unknown` where rationale is genuinely lost; populate the Gap report's structural-drift bucket where reality diverges from the diagram; replace generic-principle rationale with `unknown` + follow-up. Better prompting will not fix this — only structural refusal works."*

## Conditional gating

All checks above apply ONLY when `recovery_status:` is declared in front-matter. Three retrofit-related anti-pattern ids — `anti-pattern.fabricated-decomposition-rationale`, `anti-pattern.laundered-architecture` — are also conditional on retrofit mode (see `anti-patterns-catalog.md`).

In greenfield mode, retrofit checks do not fire. The `recovery_status:` field is absent and these checks are skipped.

Cross-link: `anti-patterns-catalog.md` (anti-pattern.fabricated-decomposition-rationale, anti-pattern.laundered-architecture); `quality-bar-gate.md` (Retrofit honesty card); SKILL.md hard refusal A (umbrella class).
