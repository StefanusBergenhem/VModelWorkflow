# DD shape checks

Mirrors `dd-purpose-and-shape.md` on the author side. Walk every DD against these checks.

## check.shape.section-missing (soft)

**Check that** all seven sections are present with substantive content OR an explicit assertion of absence.

**Reject when** any section is missing entirely, OR a stateless leaf has no State section at all (rather than a one-line "stateless" assertion).

**Approve when** all seven sections are present; absence is asserted explicitly when applicable.

**recommended_action:** *"Add the missing section. If the section's content is genuinely absent (e.g., stateless leaf), assert the absence in one line; do not omit the section heading."*

## check.shape.metadata-missing (soft)

**Check that** front-matter includes `id`, `artifact_type: detailed-design`, `scope`, `parent_scope`, `parent_architecture`, `derived_from` (non-empty), and `governing_adrs` where applicable.

**Reject when** any required field is absent or empty (`derived_from` empty list).

**Approve when** all required fields are present with non-empty values.

**recommended_action:** *"Populate the missing front-matter field per the template `templates/detailed-design.md.tmpl`."*

## check.parent-architecture.missing (HARD ★ refusal B)

**Check that** `parent_architecture:` resolves to an actual Architecture artifact, and the leaf appears in that Architecture's Decomposition.

**Reject when** `parent_architecture:` is absent, OR the referenced Architecture cannot be located, OR the Architecture's Decomposition has no entry for this leaf.

**Approve when** the parent Architecture exists and its Decomposition allocates work to this leaf.

**Evidence pattern:** quote the front-matter value; cite the parent Architecture's Decomposition (or its absence).

**recommended_action:** *"DD authoring without a parent Architecture allocation is incomplete (refusal B). Provide the parent Architecture and re-author against its Decomposition entry for this leaf."*

## check.parent-architecture.allocation-mismatch (HARD ★ refusal B)

**Check that** the DD's responsibilities (Overview + Public Interface + Data Structures) match the parent Architecture's Decomposition entry for this leaf.

**Reject when** the DD claims responsibilities not allocated by the parent, OR omits responsibilities the parent allocated, OR specifies cross-component composition the parent already fixed.

**Approve when** the DD's surface aligns with the parent's allocation.

**Evidence pattern:** name the responsibility/responsibilities present in the DD that are absent from the parent, OR vice versa.

**recommended_action:** *"DD's surface diverges from the parent Architecture's allocation. Realign — either revise the DD to match the parent, or surface the divergence as DESIGN_ISSUE upstream."*

## check.dd.cross-component-content (HARD ★ refusal B)

**Check that** the DD does not specify content that belongs in the parent Architecture: cross-component composition, sibling-leaf interfaces beyond what this leaf consumes/produces, or runtime patterns spanning scopes.

**Reject when** the DD has Composition-section content (request-response / event-driven / saga); when it specifies sibling leaves' internals; when it draws structure diagrams of the parent scope.

**Approve when** the DD scope-discipline holds — leaf-internal contracts only.

**Evidence pattern:** quote the cross-component content; identify which parent-Architecture concern it belongs in.

**recommended_action:** *"Move the content to the parent Architecture (or surface as a parent-Architecture defect). The DD specifies one leaf only."*

## check.shape.overview-thin (soft)

**Check that** Overview names what slice of the parent Architecture this leaf realises, at one level of abstraction above the code (not pseudocode).

**Reject when** Overview is one sentence, OR pseudocodes the implementation, OR fails to name the leaf's posture relative to siblings.

**Approve when** Overview is two to three paragraphs naming intent, posture, and parent-Architecture alignment.

**recommended_action:** *"Expand Overview to name what this leaf is, what slice of its parent Architecture it realises, and the approach at one level above the code."*

## check.derived-from.empty (soft)

**Check that** `derived_from:` is non-empty.

**Reject when** the list is empty or absent — orphan design.

**Approve when** at least one upstream id is listed (REQ, ARCH interface, sibling DD, or ADR).

**recommended_action:** *"Add at least one upstream artifact id. An empty `derived_from` is an orphan design — the DD has no traceable upstream."*

## check.derived-from.unresolvable (HARD ★ broken-reference)

**Check that** every id in `derived_from` resolves to an actual upstream artifact.

**Reject when** any listed id does not resolve.

**Approve when** all ids resolve.

**recommended_action:** *"Resolve the unresolvable id, OR remove it from `derived_from` if it was a stale reference."*

## Cross-link

`templates/detailed-design.md.tmpl` (full scaffold) · `quality-bar-gate.md` (Structure card) · refusal B in `SKILL.md`
