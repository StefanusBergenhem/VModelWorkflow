---
name: vmodel-skill-elicit-pd
description: Elicit a lightweight Product Description (PD) — the most lightweight of three root-of-tree product options (PB, needs, PD). Question-prompted blind-spot scanning produces a short PD doc with five mandatory sections (Product, Users, Smallest worthwhile slice, Out of scope, Open questions). No enforced stakeholder roster, no NFR matrix — push those concerns to Requirements or to the heavier PB. Use when starting a new project where discovery is not the bottleneck and a vision-level start is wanted. Triggers — write product description, draft product_description.md, lightweight vision, product overview, top-of-tree spec.
type: skill
---

# Elicit product description

This skill conducts a short, focused elicitation conversation and produces a single Markdown file: `product_description.md`. The document captures product shape — vision, users, minimum slice, scope boundary, and surfaced blind spots — in five mandatory sections. The output is intentionally lightweight: no stakeholder roster, no NFR matrix. Those concerns belong downstream in Requirements or in the heavier Product Brief if the project warrants it.

The skill is self-contained. The supporting-questions checklist and output template are bundled in `references/` and `templates/`. No external lookups are needed during a session.

## When to use

Activate this skill when the user asks to:

- Write or draft a `product_description.md` for a new project or scope root
- Create a lightweight vision-level start before diving into Requirements or Architecture
- Produce a product overview when discovery is not the bottleneck
- Capture what the product is and what it is not before specification work begins

## Do not activate this skill for

- Running a stakeholder discovery session — that is `vmodel-skill-elicit-needs`; use it when stakeholders, NFRs, and constraints need structured capture
- Authoring a full Product Brief — that is a heavier artifact with enforced stakeholder roster, NFR matrix, and formal structure
- Authoring Requirements, Architecture, or any downstream artifact
- Reviewing an existing product description — that is a separate review concern

## Inputs

Expected from the user (gather through the five base questions):

- A description of what the product is
- Who uses it
- The smallest version worth shipping
- What is explicitly out of scope
- Any blind spots the supporting-questions checklist surfaces

No upstream artifact is required — this is the root of the spec tree.

## Output

A single Markdown file using the structure in `templates/product_description.md.tmpl`. The file has YAML front-matter and five mandatory sections: Product, Users, Smallest worthwhile slice, Out of scope, Open questions.

**Default output path: `<scope-root>/product_description.md`** — the `<scope-root>` is the project's spec root directory (typically `specs/` or the path the user names). If unspecified, use `specs/product_description.md`. If the immediate parent directory does not exist, state the path and let the user confirm or correct it before writing.

## Authoring procedure

Run the five base questions in order, then apply the supporting-questions checklist selectively. Write the document only after gathering answers to the five base questions.

### Step 1 — What is this thing?

Ask: *"What is this product? Give me one paragraph — what it does and for whom."*

Capture as-is in stakeholder voice. Do not expand or restate. If the answer is too vague to be meaningful (e.g., "a platform for things"), probe once: *"What's the primary action a user takes?"* If still vague, flag as an open question and continue.

### Step 2 — Who uses it?

Ask: *"Who uses this? One or two sentences — no need for a full stakeholder roster."*

Accept persona names, role labels, or brief descriptions. Do not push for a formal stakeholder table. If the user starts expanding into stakeholder analysis, note that depth and redirect to `vmodel-skill-elicit-needs`.

### Step 3 — Smallest worthwhile slice

Ask: *"What's the smallest version of this that's worth shipping? Push for concrete and small — not a roadmap, not a vision. What does day-one look like?"*

If the answer is a list of features spanning multiple releases, probe: *"Which single capability would make that worth shipping to the first user?"* Capture the result verbatim; do not restructure into a feature list.

### Step 4 — Out of scope

Ask: *"What is this explicitly NOT? Anything the team might assume is included but isn't?"*

Accept brief bullets. If the user has nothing, leave the section as a placeholder — do not invent exclusions.

### Step 5 — Supporting-questions checklist

Apply selectively from `references/supporting-questions.md`. For each question in the checklist, judge whether it is relevant to this product type. If yes, ask it. Capture the answer in *Open questions* if the user defers or says they don't know yet; skip entirely if they confirm it doesn't apply.

Do not ask all six questions mechanically. One or two well-chosen questions per product type is the right density. A developer tool needs the failure-mode question; a consumer app needs the discoverability question; a B2B SaaS needs the revenue question.

### Step 6 — Write the document

Using `templates/product_description.md.tmpl`, compose the document from gathered answers. Populate:

- `# Product` from Step 1
- `# Users` from Step 2
- `# Smallest worthwhile slice` from Step 3
- `# Out of scope` from Step 4 (placeholder if nothing gathered)
- `# Open questions` from any deferred supporting-question answers, unanswered base questions, or blind spots the checklist raised but the user could not answer

Set `status: draft` and `date` to today's date.

### Step 7 — Self-check before delivering

Before presenting the document, verify:

1. The `# Product` section is one paragraph describing what the product does and for whom — not a feature list, not a roadmap
2. The `# Users` section is one or two sentences — not a stakeholder roster
3. The `# Smallest worthwhile slice` section is concrete and bounded — not "the full product" or a multi-phase roadmap
4. No NFR matrix entries are present — individual NFR mentions are acceptable as one-liners under Open questions if the user raised them; a matrix is not
5. No content was fabricated — if the user could not or would not answer a question, it is an open question or a placeholder, not an invented answer
6. Items that cannot be answered Yes are flagged inline in the output, not silently passed

## Hard refusals

**No stakeholder roster.** Refuse to build a formal stakeholder table or stakeholder-analysis grid. One or two sentences naming users is the ceiling. If the user wants more, redirect to `vmodel-skill-elicit-needs`.

**No NFR matrix.** Refuse to produce a non-functional requirements matrix. If the user raises specific NFRs (e.g., "must support 10k concurrent users"), capture them as one-line notes in Open questions and redirect detailed treatment to the Requirements layer. A list of one-line NFR mentions is acceptable; a structured matrix is not.

**No fabrication.** If the user cannot or will not answer a question, that answer is an open question — never invented. A `product_description.md` with open questions is a valid and complete output.

**No feature-list substitution.** The `# Product` section must describe product shape (what it is, for whom, why), not enumerate capabilities. If the user delivers a feature list, ask: *"What is this for? What problem does it solve for the user?"* and capture the answer to that probe, not the list.

## HALT conditions

Stop and hand back when:

1. **User requests stakeholder-analysis depth** — redirect to `vmodel-skill-elicit-needs` and stop.
2. **User cannot answer the first two base questions** — without a product and user description, there is no PD to write. Surface the gap and ask for a broader context conversation first.
3. **Scope creep beyond a single root artifact** — user asks to also produce Requirements, Architecture, or an ADR. Decline; name the right artifact for each expanded ask.

## File layout produced by this skill

```
<scope-root>/product_description.md
```

One file. The skill does not create directories, schemas, validators, or sibling artifacts.

## Pointers

- `references/supporting-questions.md` — the six supporting questions with usage notes (when to ask, what to listen for, how to handle deferred answers)
- `templates/product_description.md.tmpl` — the five-section output template
