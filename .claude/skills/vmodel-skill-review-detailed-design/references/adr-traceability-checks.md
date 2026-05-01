# ADR traceability checks

Mirrors `adr-extraction-cues.md` on the author side.

## check.adr.governing-not-resolved (HARD ★ broken-reference)

**Check that** every entry in `governing_adrs:` resolves to an actual ADR document.

**Reject when** a listed ADR id cannot be located.

**Approve when** all entries resolve.

**Evidence pattern:** quote the unresolvable entry; note the absence at the expected path.

**recommended_action:** *"Resolve the unresolvable id, OR remove it from `governing_adrs:` if it was a stale reference. A broken reference is a document-integrity failure."*

## check.adr.governing-not-cited-in-body (soft)

**Check that** every ADR listed in `governing_adrs:` appears at least once at a body-citation point.

**Reject when** an ADR is listed in front-matter but never cited at the spot in the body where its decision applies.

**Approve when** every listed ADR has at least one body citation.

**Evidence pattern:** name the ADR id; note the absence of body citation.

**recommended_action:** *"Cite the ADR at the body decision-application point. A `governing_adrs:` list with no body citations is decoration."*

## check.adr.body-citation-unresolved (soft)

**Check that** every body citation of the form `(per ADR-NNN)` corresponds to an entry in `governing_adrs:`.

**Reject when** the body cites an ADR id that does not appear in front-matter.

**Approve when** every body citation has a front-matter entry.

**recommended_action:** *"Add the cited ADR to `governing_adrs:` OR remove the body citation if the ADR is not actually governing this DD."*

## check.adr.needs-adr-stub-not-resolved (soft)

**Check that** no `[NEEDS-ADR: ...]` stubs remain in a finalised artifact.

**Reject when** the artifact is marked `status: active` (or otherwise finalised) and still contains `[NEEDS-ADR: ...]` markers.

**Approve when** the artifact is `draft` (stubs allowed) OR every stub has been resolved by ADR authoring + body-citation replacement.

**Evidence pattern:** quote the remaining stub.

**recommended_action:** *"Resolve every `[NEEDS-ADR: ...]` stub before finalising: author the ADR, add the id to `governing_adrs:`, replace the stub with a body citation."*

## check.adr.inline-decision-should-be-extracted (soft)

**Check that** rationale obviously meeting the three ADR criteria (load-bearing AND cross-cutting AND hard-to-reverse) is extracted to an ADR rather than inlined.

**Reject when** inline rationale describes a decision that affects multiple scopes, is hard to reverse, and is load-bearing — but no ADR is referenced.

**Approve when** such decisions are extracted (or stubbed `[NEEDS-ADR: ...]`).

**Evidence pattern:** quote the inline rationale; identify the three criteria it satisfies.

**recommended_action:** *"Extract the decision to an ADR. Inline a `[NEEDS-ADR: <decision> — extract before finalising]` stub in draft mode if no ADR exists yet."*

## Cross-link

`anti-patterns-catalog.md` · `quality-bar-gate.md` (Rationale and traceability card) · `templates/governing-adr-reference.yaml.tmpl` (author side)
