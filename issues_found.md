---
purpose: Pilot findings from vmodel-core that should feed back into the VModelWorkflow framework repo.
audience: framework maintainer
status: living
---

# Issues found — vmodel-core pilot

Findings discovered while dogfooding the framework's per-artifact authoring + review skills inside `vmodel-core`. Each entry is self-contained so it can be lifted into the framework repo as-is (issue, suggested fix, where it surfaced).

---

## 2026-05-01

### Issue 1 — `needs.md` placement is under-specified by `vmodel-skill-elicit-needs`

**Where surfaced.** First real-use elicit-needs session on `vmodel-core` (PD seed input). User asked where `needs.md` should be written; the skill does not give a deterministic answer.

**What the skill says (`vmodel-skill-elicit-needs`).**
- `SKILL.md:60` — *"Default output filename: `needs.md`. If the user has a scope-tree convention (e.g. `/specs/needs.md`), follow it."* — names a filename only, treats `/specs/` as a passing example.
- `SKILL.md:144` — file layout shown as `{output-path}/needs.md`. The `{output-path}` placeholder is never resolved anywhere in the skill.
- `SKILL.md:140` — *"The skill does not create directories, schemas, validators, or sibling artifacts."* — explicitly refuses to create the directory the file would land in.

**What the framework says.**
- `TARGET_ARCHITECTURE §5` (Directory layout, lines 259–278) defines the canonical scope-tree layout: `/specs/` is a configurable root, root-scope artifacts live directly at `/specs/`. The example tree lists `product_brief.md`, `requirements.md`, `architecture.md`, `testspec.md` at root. **`needs.md` is not in the example.**
- `BACKLOG §148` — `needs.md` *"carries the root-scope upstream role for now"* in lieu of `vmodel-skill-author-product-brief` (deferred indefinitely).
- `BACKLOG §145` — elicit-needs lives at `.claude/skills/vmodel-skill-elicit-needs/`; pilot eval input named as `docs/plan/phase4-tool-briefs/core/product_description.md`. No mention of where `needs.md` *output* lives.

**The gap (three sub-issues).**
1. **Framework / skill disagreement on whether `needs.md` is in the scope tree.** `BACKLOG §148` makes it the de-facto root-upstream artifact; `TARGET_ARCHITECTURE §5` does not list it in the canonical layout. The two documents need to agree.
2. **Skill never resolves `{output-path}`.** Two plausible defaults are not distinguished:
   - `/specs/needs.md` — consistent with framework scope-tree convention for root-scope artifacts.
   - `needs.md` at project root — consistent with the skill's own "does not create directories" stance, leaving placement to the caller.
3. **No behaviour specified when the parent directory does not exist.** Skill refuses to `mkdir`. Skill does not say whether to HALT-and-ask, write at project root as a fallback, or expect the caller to create the directory. Currently the gap is closed by ad-hoc stakeholder negotiation — fine in interactive mode, broken in any non-interactive or batch use.

**Suggested resolution.**
- Update `TARGET_ARCHITECTURE §5` Directory layout to either:
  - **(a)** Include `needs.md` at the root level of the example tree (with a note that it is the elicit-needs output and may be transient pending decision γ), or
  - **(b)** Explicitly state `needs.md` is transient elicitation output that lives outside the scope tree (and pick a canonical location, e.g. `/specs/.elicitation/needs.md` or repo root).
- Update `vmodel-skill-elicit-needs/SKILL.md` to:
  - Name a deterministic default path resolution rule (e.g. *"write to `<scope-tree-root>/needs.md` if a project config exists; otherwise `specs/needs.md`; otherwise HALT and ask"*).
  - Specify behaviour when the parent directory does not exist (HALT-and-ask vs create vs follow caller's project config).
  - Either drop the throwaway `{output-path}` placeholder in `SKILL.md:144` or define it explicitly.
- Decide in the pass that resolves elicit-needs **decision γ** (promote / merge / stay-transient) — placement should follow from artifact status. If `needs.md` becomes a tracked framework artifact, it earns a place in `TARGET_ARCHITECTURE §5`. If it stays transient, it earns explicit "where transient artifacts live" guidance.

**Pilot decision for this session.** Per stakeholder call (2026-05-01): write to `specs/needs.md`, consistent with the TARGET_ARCHITECTURE scope-tree convention for root-scope artifacts. Caller (this Claude Code session) creates the `specs/` directory because the skill refuses to.

---

### Issue 2 — Needs elicitation should run at the parent scope first, not per-product

**Where surfaced.** End of first real-use elicit-needs session on vmodel-core. After completing `specs/needs.md`, stakeholder realised vmodel-core is *not* the top of any tree — it's a derivative tool product within VModelWorkflow's three-product structure (`TARGET_ARCHITECTURE §10`). Needs should have been elicited at framework level first, then cascaded down to per-product needs.

**The gap.**
1. **Cascade not articulated.** `vmodel-skill-elicit-needs/SKILL.md` treats each invocation as scope-already-correct. There's no upfront check "have parent-scope needs been elicited?" — so the skill silently allows derivative-scope elicitation without parent-scope grounding.
2. **Affects all three sibling tool products.** `vmodel-author` and `vmodel-retrofit` will hit the same trap if elicit-needs is run on each of them independently. Per-tool needs.md inventing framework-level stakeholder context that should be inherited.
3. **Compounds Issue 1's placement gap.** Issue 1 surfaced that needs.md placement is unspecified per scope; Issue 2 adds that the *order* of needs elicitation across scopes is also unspecified.

**Suggested resolution.**
- Add to `vmodel-skill-elicit-needs/SKILL.md` a pre-check: *"Before eliciting needs for a derivative or sub-scope, confirm parent-scope needs have been elicited (or explicitly waived). If not, recommend halting and eliciting upstream first."*
- Document the needs cascade in `TARGET_ARCHITECTURE` (probably §5 scope tree or §10 three-product structure): framework-level needs → per-product needs → per-component needs. Each level inherits scope-narrowing from its parent.
- **Decision γ data point.** In this pilot, `specs/needs.md` surfaced ~30% net-new framing (mostly the (b)-reframings of design-smuggled constraints) and ~70% restatement of PD. A meaningful chunk of that 70% would have been pre-cascaded if framework-level needs.md existed first; the per-product session would have focused on genuinely product-specific deltas.

---

### Issue 3 — Readback discipline silent on flagged-but-unaddressed extrapolations

**Where surfaced.** Session readback turn 4. I had flagged an extrapolation in turn 4's readback ("CI/human consume the same five dimensions"); the user replied "almost — change X" addressing other items but not that one. I interpreted silence as "still unresolved" and dropped the extrapolation in the revision. User corrected: *"I didn't address it because I agreed and didn't have any comments."*

**The gap.**
- `references/anti-assumption.md` enforces "every detected ambiguity surfaces as a structured question — never silently fill the gap." Strong on flagging.
- `references/readback-protocol.md` (and `references/state-machine.md` CONFIRM logic) silent on what to do when an extrapolation IS flagged and the user doesn't address it on the next turn.
- The default behaviour I improvised (drop on silence) was wrong. The user's expectation: flag = surface-it discipline; once surfaced, silence is informed agreement.

**Suggested resolution.** Add to `readback-protocol.md` (or `anti-assumption.md`): *"When an extrapolation is flagged in a readback and the user responds without addressing it, treat as tacit acceptance. Do not drop the extrapolated content; do not re-flag in the next round. Flagging is the discipline; user silence after a flag is informed silence."*

---

### Issue 4 — No-design-language discipline silent on premature numerical commitments

**Where surfaced.** Session turn 8 (Quality needs probe on performance + scale). PD §3 carried specific numbers (p95 < 1s, ~1,000 artifacts, "developer-grade hardware"). When asked, stakeholder explicitly resisted committing any of them: *"I don't have strict latency budgets yet, so I don't want to create a fake number that narrows the technology selection possibilities unnecessarily."*

**The gap.** The skill's "no design language" discipline (Hard Refusal #3, `anti-assumption.md`) focuses on *vocabulary* — implementation choices, framework names, technology references. It's silent on *numerical* premature-commitment that pre-narrows the solution space without justification. A stakeholder might intuitively avoid saying "Go binary" but accept "p95 < 1s" because numbers feel neutral. They aren't.

**Suggested resolution.** Extend `anti-assumption.md` (or add a small companion ref `premature-numbers.md`) calling out numerical commitment as a category of design-smuggling. When a seed PD or candidate stakeholder answer suggests a specific number but the underlying need is shape-only ("fast enough not to block workflow"), preserve shape and explicitly defer the number — recording in session notes which numbers were deferred and why. Numbers belong in pilot calibration, Architecture, or downstream design — not in needs.md when no real anchor exists yet.

---

## 2026-05-03

### Issue 5 — Skill silent on input precedence between upstream needs.md and framework references

**Where surfaced.** `vmodel-skill-author-requirements` pilot run (specs/requirements.md, 2026-05-03). needs.md (Open gaps) defers most CLI ergonomic patterns to pilot evidence. TARGET §10 has "applies to every tool" CLI patterns including the same patterns needs.md defers. The skill's "Inputs" section names both as legitimate upstream — *"a product brief or scope statement", "a parent-scope requirements document", "user stories or stakeholder needs", "governing architectural decisions (ADRs)", "inherited constraints"* — but does not articulate which wins when both speak to the same topic. Stakeholder ruled mid-session: *"in cases where there is conflicts between needs.md and the TARGET_ARCHITECTURE or BACKLOG, then the needs document supersedes."* That ruling came from the human in the loop; an autonomous run would have to choose silently or guess.

**The gap.**
- `vmodel-skill-author-requirements/SKILL.md` `## Inputs` lists upstream input classes but specifies no ordering between them.
- The hard-refusal section bans fabrication and design-smuggling but is silent on the mirror failure — silent override of stakeholder-confirmed deferrals by framework-level "applies to every tool" content.
- Without a precedence rule, a skill run in non-interactive mode against a needs.md that defers a topic and a TARGET that commits the same topic has no protocol for which wins.

**Suggested resolution.** Add to `vmodel-skill-author-requirements/SKILL.md` a *Precedence rule* subsection: *"When two or more upstream sources speak to the same topic, the most recent stakeholder-confirmed source wins, unless the framework reference is itself an inherited constraint named in the upstream source. In practice: needs.md > parent requirements > framework TARGET / BACKLOG / docs > schema-implied conventions. Where conflict exists, capture the precedence reasoning in the affected requirement's rationale rather than applying the override silently."* Generalise to all per-artifact authoring skills.

---

### Issue 6 — Skill template `governing_decisions` does not match schema field `governing_adrs`

**Where surfaced.** `vmodel-skill-author-requirements/templates/requirements.md.tmpl` (2026-05-03). Line 7 of the template uses front-matter property `governing_decisions:`. The framework requirements schema (`schemas/artifacts/requirements.schema.json`) defines the property as `governing_adrs`. Authoring directly against the template would produce front-matter that fails schema validation; vmodel-core (when it runs against this artifact) would emit a structural finding for an unknown property.

**The gap.**
- Concrete bug in the skill bundle. Self-containment test fails: the skill, taken on its own, produces output that fails the framework schema.
- Likely an artefact of a rename in the schema that did not propagate to the skill template.

**Suggested resolution.**
- Rename `governing_decisions` to `governing_adrs` in `vmodel-skill-author-requirements/templates/requirements.md.tmpl`.
- Audit other author-skill templates (`vmodel-skill-author-architecture`, `vmodel-skill-author-detailed-design`, `vmodel-skill-author-testspec`, `vmodel-skill-author-adr`) for the same divergence.
- Add to skill QA: when releasing a new version of any author skill, every template field name must be diff'd against the matching schema. Mechanise if cheap.

---

### Issue 7 — NFR five-element rule has no protocol for explicitly deferred numerical targets

**Where surfaced.** `vmodel-skill-author-requirements` pilot run (REQ-022 performance, REQ-023 scale, 2026-05-03). needs.md (turn 8, 2026-05-01) explicitly defers specific latency and scale numbers to pilot evidence to avoid prematurely narrowing technology selection. The NFR five-element rule (`references/nfr-five-elements.md`) requires every NFR to commit metric+unit+target+condition. With numerical targets explicitly deferred, no NFR can be authored that satisfies the rule as written.

**Resolution improvised this session.** Planguage form with `scale` and `meter` filled (shape only, no numbers) and `fail`/`goal`/`stretch`/`wish` slots set to `pending — pilot calibration`, plus `follow_up` blocks owning the calibration. Documented in *Open gaps*. The review skill accepted this resolution and the *Spec Ambiguity Test* passed (downstream readers can see the deferral and know which questions to wait on).

**The gap.** The resolution is doctrine-shaped but not articulated anywhere in the skill. A future user without the precedent might fabricate numbers (violating the no-fabrication rule extended to numbers per Issue 4 above) or HALT for stakeholder input that doesn't exist yet (the calibration evidence is *future* pilot data, not a current human gap). Pairs with Issue 4: both surface that numerical commitments need their own discipline distinct from vocabulary-level design-smuggling.

**Suggested resolution.** Extend `references/nfr-five-elements.md` (or add a companion `references/deferred-numbers.md` co-located with the resolution to Issue 4): *"When upstream input explicitly defers numerical targets to pilot evidence or downstream calibration, use Planguage with `scale` and `meter` filled (shape) and `fail`/`goal`/`stretch`/`wish` set to `pending — <named calibration source>`. Author a `follow_up` block owning the calibration with a named owner and action. Document the deferral in the artifact's *Open gaps* section. Do not fabricate numbers; do not HALT — the document is honestly partial, not invalid. The Quality Bar items demanding target+statistical-level are then evaluated against the Planguage `scale`+`meter` rather than the empty target slots; a missing `scale` or `meter` remains a defect."*

---

### Issue 8 — Interface-versioning check forces premature commitment when upstream is silent on versioning

**Where surfaced.** `vmodel-skill-review-requirements` first-pass review of `specs/requirements.md` (2026-05-03). The author's first draft of REQ-024 / REQ-025 marked all three versioning sub-elements (label, compatibility regime, deprecation policy) as `pending — to be set by ADR before v1 release` because needs.md is silent on versioning. The review skill flagged both as soft_reject (`check.interface.missing-versioning`). Author resolved by committing version label (v1) and compatibility regime (additive-only-within-major) at requirements scope, with rationale citing *"the standard-engineering interpretation of IC-006's stable-contract constraint"*; deprecation notice period remained the only pending element.

**The gap.**
- The additive-within-major commitment is borderline fabrication: it derives from "standard-engineering interpretation" rather than from any explicit stakeholder decision or framework reference.
- The review skill forced a commitment; the author resolved by importing engineering-convention defaults. The resolution is plausibly correct (the convention is well-established) but the no-fabrication discipline (`references/rationale-and-traceability.md`) does not have a clear rule on when standard-convention imports are acceptable rationale vs. when they cross into fabrication.
- Conversely: a strict reading of the no-fabrication rule would have forced HALT on every interface contract whose upstream is silent on versioning — almost every greenfield interface, especially at first-draft.

**Suggested resolution.** Extend `references/rationale-and-traceability.md` no-fabrication discipline with a *Standard-engineering-convention imports* clause: *"Standard-engineering-convention imports (industry convention is well-established and the upstream constraint clearly implies the convention as a single natural read) are permissible rationale, provided the rationale explicitly identifies (a) the convention being imported, (b) the upstream constraint that implies it, and (c) why the convention is the natural read of that constraint rather than one of several reasonable reads. If multiple reasonable reads exist, HALT and ask."* Optionally also relax `check.interface.missing-versioning` from soft_reject to info when versioning sub-elements are explicitly `pending — <named ADR>` AND a `follow_up` is queued AND the document is in `status: draft`.

---

### Issue 9 — Author skills provide no protocol for downstream artifacts with no canonical upstream

**Where surfaced.** `vmodel-skill-author-requirements` pilot run, front-matter `derived_from` (2026-05-03). vmodel-core has no Product Brief; needs.md is not in the canonical artifact set per TARGET §5. The schema requires non-empty `derived_from` with resolvable `artifact_id_ref`. Three coherent paths existed at session start: (a) HALT and ask the stakeholder to author the upstream first; (b) use a placeholder upstream id and document the gap; (c) cite a framework reference (e.g. TARGET §10) as upstream.

**Resolution improvised this session.** Stakeholder selected (b) — placeholder `NEEDS-vmodel-core` documented in *Open gaps* with a two-path resolution (author PB or promote needs.md). The consequent `TRV-REF-001` finding when vmodel-core eventually validates this artifact is treated as a deliberate pilot data point.

**The gap.**
- `vmodel-skill-author-requirements/SKILL.md` `## Inputs` lists upstream input classes but does not address *"what if no canonical upstream artifact exists yet"*.
- HALT condition #1 (*"upstream allocation is itself ambiguous"*) is close but does not match this case — the upstream is clear (needs.md), it is just not in the canonical artifact set.
- The same gap exists in every per-artifact authoring skill, not only requirements: a leaf DD authored before its parent Architecture exists, an Architecture authored before its parent Requirements exists, etc.
- Compounds Issues 1, 2, 6 from 2026-05-01: those flagged that needs.md placement, cascade, and template/schema mismatches are unresolved; Issue 9 generalises to *"how does any author skill handle a missing canonical upstream"*.

**Suggested resolution.** Add an explicit pre-check to every author skill (template subsection, then make concrete in each skill's SKILL.md): *"Before authoring, check that the canonical upstream artifact exists and has a resolvable `artifact_id`. If it does not, three paths are acceptable — choose explicitly: (a) HALT and ask the stakeholder to author the upstream artifact first (default for greenfield once the framework is mature); (b) use a placeholder upstream id and document the gap in *Open gaps* with a `follow_up` owning the resolution (acceptable when stakeholder explicitly accepts the orphan for a documented pilot reason); (c) cite a framework reference as upstream only if that reference is itself a canonical artifact in the framework's own scope tree (this is currently rare — most framework references are documentation, not artifacts). Do not silently invent an upstream id; do not bypass the schema's non-empty-`derived_from` requirement."* Cross-link from each per-artifact author skill to the new shared protocol.

---
