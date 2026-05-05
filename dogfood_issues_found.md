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

### Issue 10 - Too much readback during elicitation.
- As a user, it felt a bit redundant durinng the elicitation flow. There was first an capture of all potential open threads - good. Then for each thread we discussed and came to a conclusion - good. But after that there was the write to the document + readback and approval. That readback felt very forced. We had already agreed during the discussion. I would like to leave that out and instead have a final readback at the end. 


### Issue 11 — ADR and architecture author skills materialise new requirements without invoking the requirements-author skill's discipline

**Where surfaced.** `vmodel-skill-author-adr` pilot runs for ADR-001 and ADR-002 (2026-05-03). Both ADRs' Propagation blocks committed to "new requirement at this scope" routes for several consequences: ADR-001 → REQ-029 (stable emission order); ADR-002 → REQ-030 (schema-version pinning, originally compound), REQ-031 (no-external-schema-access), REQ-032 (queryability — created retroactively after the REQ-030 split). Step 8 of `vmodel-skill-author-adr/SKILL.md` instructs the author to choose a propagation route per consequence and, for the *new requirement at scope* route, to record *"Materialised as: REQ-... — '<requirement statement>'"* — meaning the ADR author writes the requirement statement inline. In the dogfooding session, the author also appended the materialised YAML requirement block to `specs/requirements.md`. None of this invoked `vmodel-skill-author-requirements`.

**Resolution improvised this session.** I drafted the requirement YAML blocks against my own approximation of the requirements skill's discipline. The downstream `vmodel-skill-review-requirements` adversarial review then caught:

- **REQ-029** hard_reject (`anti-pattern.implementation-prescription`) — statement said *"the system shall apply a stable ordering across the output"*, smuggling sorting / ordered traversal as the mandated mechanism. The observable invariant is byte-identical-output-on-byte-identical-input; the statement should have stopped there. Fixed in the second pass.
- **REQ-030** soft_reject (`anti-pattern.compound`) — two `shall`s in one statement (pinning + queryability). Fixed by splitting into REQ-030 (pinning) and REQ-032 (queryability).
- **REQ-030** soft_reject (`check.ears.invalid-pattern`) — statement opened with a noun-phrase subject, not a valid EARS keyword. Resolved by the split into Ubiquitous + Event-driven shapes.

All three are author-side gates that `vmodel-skill-author-requirements` would have prevented at draft time, before the requirements landed in the file. Catching them at review time worked but is the wrong gate — rework cost is higher when issues surface only after the artifact has been written and the parent ADR accepted.

**The gap.**
1. **ADR-author skill writes requirement-shaped content without invoking the requirements-author skill's gates.** Step 8 of `vmodel-skill-author-adr/SKILL.md` makes the ADR responsible for *Materialised-as* content but does not require the requirement statement to pass the requirements-author skill's atomicity / EARS / no-implementation-prescription / no-fabrication checks. The ADR-author skill's discipline catalog is decision-shaped, not requirement-shaped.
2. **The architecture-author skill carries the same shape of risk.** `vmodel-skill-author-architecture` Step 1 (Decomposition) allocates parent requirements to children; Step 2 (Interfaces) writes Design-by-Contract clauses with preconditions / postconditions / invariants — all requirement-shaped content. The architecture-author skill's anti-pattern catalog mentions some of the requirements-shaping concerns but is not a peer of the requirements-author skill's catalog. This session did not exercise the architecture-author skill, but the structural risk is the same and should be flagged before that session runs.
3. **The framework already has the right gate; it just is not invoked.** `vmodel-skill-author-requirements` exists with the correct atomicity / EARS / no-implementation-prescription gates. The ADR-author and architecture-author skills produce requirement-shaped content but treat the shaping as a sub-task of their own discipline rather than a delegation to the requirements skill. The author then either approximates the requirements discipline (and gets caught at review) or invokes the requirements skill manually as a separate session step (no automation, no documentation).
4. **Defect rate at the propagation interface.** Three reviewer-caught requirement-shape issues across two ADRs that produced four new requirements is a 75% per-requirement defect rate — not in the propagation logic, but in the requirement-shaping that piggybacks on it. Strong empirical evidence that the gate is missing.

**Suggested resolution.**
- **Option A — explicit cross-skill invocation.** Update `vmodel-skill-author-adr` Step 8 (Propagation) and `vmodel-skill-author-architecture` Step 1 (Decomposition) / Step 2 (Interfaces) to explicitly require invoking `vmodel-skill-author-requirements` for any new-requirement-at-scope content before the parent skill's draft is finalised. Cleanest "right gate at draft time" but introduces a recursive skill-invocation pattern the framework does not currently have.
- **Option B — checklist import.** Cross-link the requirements-author skill's atomicity / EARS / no-implementation-prescription / no-fabrication checklist into the ADR and architecture author skills' Propagation / Decomposition / Interfaces references. Author runs the checklist inline rather than recursively invoking the skill. Lower-cost but easier to skip silently.
- **Option C — reviewer-side catch as the explicit gate.** Acknowledge that ADR and architecture authoring will produce rough requirement-shaped content; require that `vmodel-skill-review-requirements` be invoked on the requirements doc immediately after every ADR or architecture session that materialises new requirements. Extends the framework's existing "review after author" cadence to cover propagated content.
- **My lean.** Option B with Option C as fallback. Option A's recursive invocation is cleaner but the framework's per-skill autonomy makes it cumbersome. Option B keeps the discipline visible without coupling skills. Option C catches what B misses.

**Pairs with.** Issue 6 (skill template field-name divergence from schema) and Issue 9 (no protocol for missing canonical upstream) — all three suggest the same underlying pattern: per-skill autonomy without explicit cross-skill discipline produces silent-divergence failures that adversarial review catches but author-time gates would prevent.

### Issue 12 — No clean list of "which artifacts are left to derive"

**Where surfaced.** Architecture authoring session (2026-05-03). After authoring `specs/architecture.md` with 8 `[NEEDS-DD: ...]` markers and 1 `[NEEDS-ADR: ...]` marker, there was no canonical, structured place where these open items were aggregated for downstream consumption. The markers lived inline at the spot of deferral and were re-mentioned in prose form in the artifact's *Notes / Self-attestation* section. This made it hard for:

1. **Downstream DD authors** — to know which DDs are pending and at which scope.
2. **An orchestrator skill** — to compute "what's left to do" in the spec tree.
3. **Status reporting** — to derive a "% complete" or "next-steps" view without re-parsing every artifact's prose.

The session's mitigation was to add a structured *Open follow-ups* section to `specs/architecture.md` (per stakeholder request), modelled on the *Open gaps and follow-ups* section in `specs/requirements.md`. That mitigation works for one artifact at a time but does not generalise to the framework.

**The gap.**

1. The author skills' templates (`vmodel-skill-author-architecture`, `vmodel-skill-author-detailed-design`, `vmodel-skill-author-testspec`, `vmodel-skill-author-adr`) do not mandate or even suggest an *Open follow-ups* section. `vmodel-skill-author-requirements` has it organically; the others do not.
2. There is no canonical machine-readable index across the spec tree that aggregates `[NEEDS-DD: ...]` and `[NEEDS-ADR: ...]` markers from every artifact. Each artifact's deferrals live in its own prose; building a tree-level index requires regex over all `.md` files plus trust that markers were spelled consistently.
3. vmodel-core (the tool product being built in this pilot) does not yet have a "list-pending" capability in its v1 functional scope. The four reporting outputs (coverage / completeness / inventory / impact-analysis per REQ-018..021) do not include "open follow-ups" as a category.

**Suggested resolution.**

- **Author-skill templates.** Add an *Open follow-ups* section to every author-skill's artifact template (architecture, DD, TestSpec, ADR). Make it structurally identical to the requirements artefact's existing one: bullet list with title, owner, action, citation locations.
- **Marker syntax canonicalisation.** Standardise the inline marker syntax to one form (e.g., `[NEEDS-DD: <scope> — <description>]`) across all author skills, so a tree-level grep produces clean results.
- **vmodel-core capability (v1.x candidate).** Consider adding a fifth reporting output type — *open-follow-ups report* — that aggregates pending items across the spec tree by scope, type, and owner. Would require lifting the marker syntax into a parsable form (or extracting from per-artifact *Open follow-ups* sections directly).
- **Until the canonical index exists**, the per-artifact *Open follow-ups* section is the workaround. Apply it consistently across every artifact authored.

**Pairs with.** Issue 11 (per-skill discipline gaps caught at review only); both surface the same shape of "the framework has the right gate — it just isn't invoked / present uniformly across skills".

---

### Issue 13 — Handover between author and review skills should be file-based, not direct chat

**Where surfaced.** Architecture review (2026-05-03). The session ran `vmodel-skill-author-architecture` to produce `specs/architecture.md`, then dispatched a sub-agent with `vmodel-skill-review-architecture` to produce a verdict. The review's findings (verdict + 6 specific findings with severity, location, evidence, recommended action) returned via the sub-agent's natural-language summary to the parent session. The findings were ephemeral — neither the parent session nor any downstream consumer could re-read them later without re-running the review or scrolling back through the conversation log.

This pattern repeated across every author-review cycle this session (architecture authored / reviewed; previously, requirements authored / reviewed twice; ADRs authored / reviewed).

**The gap.**

1. **Findings are not durable.** A review's verdict + findings exist only in the conversation transcript that produced them. If a stakeholder wants to revisit the review days or weeks later, the only durable record is the after-the-fact CLAUDE.md status summary or commit message — both prose, both lossy.
2. **Findings are not consumable by tooling.** A future orchestrator skill (or vmodel-core itself) cannot read review findings programmatically — there is no canonical YAML / JSON shape on disk for review output.
3. **The framework already has the file-based handover idiom for build-side workflow** (per global `~/.claude/CLAUDE.md` *Workflow Rules* — `.workflow/current_task.yaml`, `review_ready.yaml`, `feedback.yaml`). The spec-side workflow does not yet use this idiom.
4. **Review-side authoring discipline is silent on output durability.** The review skills (`vmodel-skill-review-*`) emit verdicts and findings via the conversation channel only. None of them write to a canonical file path.

**Suggested resolution.**

- **Define a canonical review-output file format.** YAML at a known path under `specs/` (or a new `specs/.reviews/` directory): one file per review run, named `<artifact-id>-review-<date>.yaml`, carrying verdict (APPROVED / REJECTED / DESIGN_ISSUE), findings (id, location, check_failed, severity, evidence, recommended_action), reviewer skill name + version, parent artifact id + version.
- **Update every `vmodel-skill-review-*`** to write its verdict + findings to the canonical path before emitting the conversation summary. The conversation summary becomes a human-friendly rendering of the file; the file is the source of truth.
- **Update every `vmodel-skill-author-*`** to read any prior review file for the artifact under authoring, so revision passes can address prior findings explicitly rather than re-eliciting them through conversation.
- **Align with the framework's `.workflow/` state directory pattern** for build workflow. Spec-side may not need every file the build pattern uses, but `review_ready.yaml` / `feedback.yaml` map cleanly to "review request" / "review verdict" for the spec workflow.

**Pairs with.** Issue 12 (no canonical machine-readable index of pending items); both move the framework toward file-based, tooling-consumable state rather than per-session natural-language artefacts.

---

### Issue 14 — No specs-global "definitions" / glossary document

The DDD definitions are saved in the root-level `requirements.md`. But that is a somewhat hidden place, and those definitions should be "specs-global" and enforced in all artifacts.

**Where surfaced.** Architecture authoring session (2026-05-03). The architecture introduced multiple typed concepts in interface contracts — `ArtifactSet`, `TraceabilityGraph`, `ArtifactTarget`, `ValidationMode`, `OutputFormat`, `Verdict`, `Finding`, `RuleCatalog`, `Schema`, `QBChecklist`, `VersionManifest`, `HTMLDocument`, `ReportRequest` — but none of these were added to a glossary. Some are defined inline in the interface entry's `operation` or `preconditions` fields; others (e.g., `ArtifactSet`) are used without explicit definition, relying on the reader's intuition.

The DDD-style glossary committed earlier in the session lives inside `specs/requirements.md` as a *Glossary* section. Terms there are scoped to that artifact's own usage. As the spec tree grows beyond requirements (architecture authored this session; DDs and TestSpecs to come), every artifact may use these terms and may need new ones, but:

1. The glossary is not "specs-global" — it is owned by `requirements.md` and any other artifact that wants to reference it must do so by ID lookup into a sibling file.
2. New typed concepts introduced in `architecture.md` (the architecture-introduced types listed above) have no canonical definition home. They live in interface contract prose.
3. There is no enforcement that a term used in a child artifact resolves to a definition somewhere upstream. vmodel-core's rule catalog (per REQ-010..014) does not include a "term-resolves" rule.

The risk this session: future DD authors may redefine `ArtifactSet` (or a similarly-loaded term) inconsistently from the architecture's intent, and there is no mechanical check to catch the divergence.

**The gap.**

1. **Glossary placement.** `TARGET_ARCHITECTURE §5` directory layout does not name a canonical location for a tree-wide glossary. Putting it in requirements.md makes it look root-scoped to that artifact rather than tree-global.
2. **Author-skill templates.** None of the author-skill templates (`-architecture`, `-detailed-design`, `-testspec`) instruct the author to register new terms in a tree-global glossary. The architecture-author skill in particular allows interfaces to introduce typed concepts without traceback.
3. **Validation-rule catalog.** The framework's traceability rule catalog (`references/schemas/traceability/validation-rules.catalog.json`) has no rule for term consistency. A "term defined in N artifacts with N distinct definitions" is not currently a finding.
4. **Phase-5 review-skill scope.** Per-artifact review skills check craft and structural rigor but do not cross-reference term usage against a global definition source.

**Suggested resolution.**

- **Tree-global glossary file.** Define a canonical `specs/glossary.md` (or a per-scope variant under each non-leaf scope) carrying authoritative term definitions. Add to `TARGET_ARCHITECTURE §5` as a first-class artifact location.
- **Author-skill discipline.** Update author-skill templates to instruct: when introducing a new typed concept (in an interface signature, a data structure, or a test fixture name), register it in the tree-global glossary or add to the local artifact's glossary section with explicit "promote to global if reused" criteria.
- **Validation rule (vmodel-core capability).** Consider adding a `terminology` rule class to the framework's canonical rule catalog: term resolution (every used term resolves to a glossary entry), consistency (one definition per term across the tree), drift detection (term redefined in a child artifact differently from the parent).
- **Until the canonical glossary exists**, every author skill should reference the existing `requirements.md` *Glossary* section by ID and surface "this term lacks a definition" as a `[NEEDS-GLOSSARY: <term>]` marker (analogous to `[NEEDS-DD: ...]`). Adopters can then resolve markers explicitly.

**Pairs with.** Issue 12 (no canonical index of pending items) — both stem from the framework not having tree-global indexable artefacts.

---

### Issue 15 — Author-architecture skill's Mermaid diagram templates are silent on parser-breaking characters

**Where surfaced.** Architecture rendering verification (2026-05-03). After authoring `specs/architecture.md` and having the matched review skill return APPROVED-after-fix on the architectural craft, the stakeholder attempted to render the document and reported that both Mermaid sequence diagrams failed to parse with errors:

- *"Parse error on line 24: ...embed.FS; REQ-030 + REQ-031) Val-> ... Expecting NEWLINE / AS / ... got '+'"*
- *"Parse error on line 12: ...read artifact 1 bytes FS-->>Load: byt ... Expecting SOLID_OPEN_ARROW / ... got NEWLINE"*

Three classes of breakage were diagnosed in the session's draft:

1. **Semicolons in message text.** Mermaid sequence diagrams treat `;` as a statement terminator inside message bodies, splitting the line. The parser then sees the orphan tail as a new statement and fails on the next token. Five occurrences in the draft (e.g., `Res-->>Val: bundled content (per ADR-002 embed.FS; REQ-030 + REQ-031)`).
2. **Angle brackets in message text.** Some Mermaid renderers interpret `<...>` as HTML and either escape the content or break parsing. Two patterns in the draft (`<path>` and `<root>` used as argument placeholders, four occurrences total).
3. **Forward slashes in unquoted participant aliases.** `participant Caller as AI-caller / CI / human` failed in some renderers; quoting the alias (`as "AI caller, CI, or human"`) fixed it.

All three were fixed in the session by simple substitutions (`;` → `—`, `<X>` → literal placeholder, unquoted alias → quoted). None changed the architectural content.

**The gap.**

1. **Skill template silence.** `vmodel-skill-author-architecture/templates/sequence-diagram.mmd.tmpl` and `templates/structure-diagram.mmd.tmpl` provide diagram skeletons but do not list known parser-breaking characters in message text or aliases. The author skill emitted multiple syntax errors that were only discoverable at render time, not at author time.
2. **Skill review silence.** `vmodel-skill-review-architecture` evaluates Quality Bar items, anti-patterns, and traceability — it does not invoke a Mermaid parser to verify diagram syntax. Diagrams that fail to render can pass review.
3. **Cross-skill recurrence likely.** Every author skill that emits Mermaid (`-architecture`, plus `-detailed-design` for state diagrams) has the same template-silence risk.

**Suggested resolution.**

- Add a script for checking format. 
- **Author-skill template.** Add a comment block to `templates/sequence-diagram.mmd.tmpl` (and `templates/structure-diagram.mmd.tmpl`, and any state-diagram template in `vmodel-skill-author-detailed-design`) listing parser-breaking characters and their canonical replacements:
  - `;` in message text → use `—` (em-dash) or `,`.
  - `<...>` in message text → use a literal placeholder (e.g., `PATH` not `<path>`) or square brackets `[...]`.
  - Special characters in unquoted aliases (`/`, `:`, `,`, etc.) → quote the alias with double quotes.
- **Review-skill check.** Add a `check.mermaid.parser-breaking-chars` to `vmodel-skill-review-architecture` (and the DD review) that flags the three classes mechanically. This is purely structural — no Mermaid parser invocation required; regex-detect the patterns.
- **Optional v1.x: canonical render verification.** Candidate for vmodel-core: add a Mermaid parse step to validation, producing a structural finding when a diagram fails. Lifts the gap from "stakeholder discovers at render time" to "validation catches before commit". Parser availability in Go is the gating concern.

**Pairs with.** Issue 11 / Issue 16 (per-skill discipline catches certain shapes only at review or render time); same pattern of "the failure mode is mechanically detectable but no skill-side gate currently invokes the detection".

---

### Issue 16 — Architecture skill: where do ADR-bound library / protocol bindings land in the architecture artifact?

**Where surfaced.** Architecture review (2026-05-03). `vmodel-skill-review-architecture` returned **REJECTED** on first pass with two hard-reject findings (F-001 and F-002, both same root cause):

> Decomposition entry `reporter`, responsibility 2: *"Render the aggregate to a self-contained HTML document **using Go's stdlib html/template per ADR-001**."* — fires `check.responsibility.implementation-prescription` and `anti-pattern.dd-content-in-architecture`.

The author had named the specific library `html/template` inside a Decomposition responsibility statement. The library choice was correctly mandated by ADR-001's *Propagation* section ("HTML reporting uses Go's `html/template` stdlib package"), so the author placed the library name in the responsibility because that is where the consequence visibly applies. The review correctly rejected: library names belong in the rationale field (which already carried the ADR citation).

The fix was a single-edit removal (delete "using Go's stdlib html/template" from the responsibility line; the library name remains correctly in `rationale` and in the ADR). But the failure mode is structural, not local.

**The gap.**

1. **The author-architecture skill's discipline is silent on landing rules for ADR-bound consequences.** When ADR-001's *Propagation* section says "HTML reporting uses Go's `html/template`" and "YAML 1.2 parsing uses `goccy/go-yaml`" with the route "governing_adrs from child architecture", the architecture author needs to know **where in the child entry** the library binding lands. Three plausible locations, only one of which is correct:
   - `purpose` — a one-sentence statement; library would smuggle implementation prescription. **Wrong.**
   - `responsibilities` — what the component does; library binding is *mechanism*, not architectural responsibility. **Wrong** (review rejects).
   - `rationale` — why the component is shaped this way and which constraints bind; library binding cited from the governing ADR is correct. **Right.**

   The skill's `references/decomposition-discipline.md` and `references/interface-contracts.md` do not state this landing rule explicitly. The author defaulted to responsibility because that is where the library is "used", not where its choice is justified.

2. **The author-architecture skill's anti-pattern catalog (`anti-patterns.md` #10 DD-content-in-architecture) catches the failure but doesn't redirect the author.** The catalog's "Fix" guidance says to name the runtime pattern from `composition-patterns.md` — that is the right fix for a missing-pattern case, not for a library-in-responsibility case. The author needs a different redirect: "library bindings from ADR Propagation land in `rationale`, not in `responsibilities`, `purpose`, or interface signatures".

3. **The review-architecture skill caught it correctly at review time, but the author-time gate was missing.** Same shape as Issue 11 / Issue 15 — discipline that exists at review level but not at author template level.

**Empirical signal.** This session, two ADR-propagated library bindings (`goccy/go-yaml` for parsing, `html/template` for templating) needed to land in two child entries (`artifact-loader`, `reporter`). The author got `goccy/go-yaml` correct (it landed in `artifact-loader.rationale`) and got `html/template` wrong (it landed in `reporter.responsibilities`). One out of two is a 50% defect rate at the propagation interface — not a fluke, especially given that ADR-001 used near-identical Propagation language for both bindings.

**Suggested resolution.**

- **Add a landing-rules reference to `vmodel-skill-author-architecture`.** Either a new file (`references/adr-propagation-landing-rules.md`) or an additional section in `references/decomposition-discipline.md` and `references/interface-contracts.md`:
  > *When a governing ADR's Propagation section binds a specific library, protocol, or framework to a child or interface in this scope, the binding lands in the **rationale** field of the relevant Decomposition entry / Interface entry, citing the ADR by id. The binding does NOT land in `purpose`, `responsibilities`, the interface `operation` signature, or any other field that names the component's architectural ownership. Architecture states what the component owns (renders HTML); the ADR-cited rationale states which mechanism satisfies that ownership.*
- **Update the architecture template's decomposition entry stub** (`templates/decomposition-entry.yaml.tmpl`) with a comment near the `rationale` field: `# ADR-bound library / protocol / framework choices land here, not in purpose/responsibilities`.
- **Add a review-side check** `check.responsibility.adr-bound-mechanism-leaked` that fires when a responsibility or purpose names content that the artifact's `governing_adrs` Propagation section binds. Pairs with the existing `check.responsibility.implementation-prescription`.

**Pairs with.** Issue 11 (per-skill discipline gaps caught at review only) and Issue 15 (Mermaid syntax pitfalls); all three are the same shape — a mechanically-detectable failure mode that the review skill catches but the author skill emits without a gate.

---

## 2026-05-04

### Issue 17 — Empty-scope ID encoding is undefined for `id:`, `verifies:`, and dotted-path references

**Where surfaced.** `vmodel-skill-author-testspec` pilot run on `specs/testspec.md` (2026-05-03) and adversarial review by `vmodel-skill-review-testspec` (2026-05-04). vmodel-core operates at root scope (`scope: ""`). Three encoding decisions had to be improvised because the skill's templates and references degenerate ungracefully when the scope segment is the empty string:

1. **TestSpec front-matter `id:`.** Template `vmodel-skill-author-testspec/templates/test-spec.md.tmpl` line 1 says `id: TS-<<scope-flattened>>`. With `scope: ""`, this resolves to `TS-` (trailing-hyphen) or `TS` (suffix dropped). The author improvised `id: TS` (no suffix) by analogy with the architecture artifact's `id: ARCH` and requirements artifact's `id: REQS`. No skill rule sanctions this.

2. **Per-case `id:`.** Template `case-branch.yaml.tmpl` and `case-leaf.yaml.tmpl` say `id: TC-<<scope>>-NNN`. With empty scope this gives `TC--NNN` (double-hyphen) or `TC-NNN` (segment dropped). Author improvised `TC-NNN`. No skill rule sanctions this either.

3. **`verifies:` dotted-path references to architecture interfaces.** `references/architecture-traceability-cues.md` shows the canonical form as `ARCH-<scope>.interfaces.<name>`. With empty scope this becomes `ARCH-.interfaces.<name>` — a syntactically odd string with a stranded hyphen before the dot. Author improvised `ARCH.interfaces.<name>` (the plain prefix, since the architecture's `id` is plain `ARCH`). The adversarial review on 2026-05-04 confirmed the improvised form resolves correctly against the architecture document and accepted it explicitly, but the framework convention is undocumented and a non-improvising author could:
   - Hard-fail on `ARCH-.interfaces.<name>` because the resolver does not strip the trailing-hyphen,
   - Silently drift to inconsistent forms across artifacts (`ARCH.interfaces.X` in one testspec, `ARCH-.interfaces.X` in another), or
   - HALT in confusion with no deterministic rule to apply.

**The gap.**

1. **Template silence on empty-scope degeneration.** The three templates (`test-spec.md.tmpl`, `case-branch.yaml.tmpl`, `case-leaf.yaml.tmpl`) use `<<scope>>` and `<<scope-flattened>>` placeholders without specifying behaviour when the placeholder is empty. The same gap likely exists in author-architecture, author-detailed-design, and author-adr templates.
2. **Reference-example silence.** `references/architecture-traceability-cues.md` shows worked examples at non-empty scopes only (e.g., `ARCH-cart-service.interfaces.OrderPlacement`). The empty-scope case never appears in any example across any reference file.
3. **No canonical resolver behaviour.** Whether a hyphen-suffix form (`ARCH-`) is equivalent to the plain form (`ARCH`) at empty scope is a resolver-implementation decision that vmodel-core itself will eventually face. The framework needs a single canonical rule.

**Suggested resolution.**

- **Pin the empty-scope rule explicitly.** Add to `references/scope-tree-conventions.md` (or wherever the framework's scope-naming convention lives): *"At root scope (`scope: ""`), the scope segment is omitted from all derived identifiers. The artifact id is the bare type prefix (`TS`, `ARCH`, `REQS`, `DD`, `PB`); per-case ids are `TC-NNN`; dotted-path references use the bare artifact id as prefix (`ARCH.interfaces.<name>`, not `ARCH-.interfaces.<name>`). Resolvers MUST treat the bare-prefix form as canonical at empty scope and SHOULD reject the trailing-hyphen form to prevent silent drift."*
- **Update template placeholders** in every author skill to use a conditional substitution rule (e.g., `<<scope-suffix?>>` that expands to `-<<scope>>` for non-empty scope and to empty string for root). Surface the rule in each template's leading comment block.
- **Add a worked empty-scope example** to `references/architecture-traceability-cues.md`, `references/dd-traceability-cues.md`, and `references/requirements-traceability-cues.md` so the convention is visible to authors.
- **Add a vmodel-core validation rule (v1.x candidate).** Once vmodel-core implements the resolver, add a `terminology` or `reference_integrity` rule that flags trailing-hyphen forms (`ARCH-.X`, `TC--NNN`, `TS-`) as malformed, surfacing silent drift mechanically.

**Pairs with.** Issue 6 (skill template field-name divergence from schema — same family of "template / framework convention not aligned") and Issue 12 (no canonical machine-readable index — both surface that the framework's identifier conventions need tighter machine-readability).

---

### Issue 18 — Author-testspec skill has no protocol when canonical root-layer parent is partially missing (Product Brief absent)

**Where surfaced.** `vmodel-skill-author-testspec` pilot run on `specs/testspec.md` (2026-05-03). The skill's `## Inputs` section names the parent spec for each layer:
- Leaf: parent Detailed Design.
- Branch: parent Architecture.
- Root: Requirements + Product Brief.

vmodel-core has Requirements (`specs/requirements.md`) but no Product Brief (the gap formalised in Issue 1 / decision γ). Three coherent paths were available at session start, none sanctioned by the skill:

- **(a)** HALT and demand the Product Brief be authored first. Defensible per HALT condition #1 ("missing parent spec"), but the upstream gap is structural (decision γ unresolved) and can't be closed at testspec authoring time.
- **(b)** Author a *branch-layer* TestSpec at root scope, deriving from Architecture only. Mismatches `references/per-layer-weight.md` which says root scope → `level: system`, not `level: integration`.
- **(c)** Author a hybrid: `level: system` (matches scope position) with branch-shape cases (because the only available parent is Architecture). Documented as deviation in Overview.

**Resolution improvised this session.** Path (c) — `level: system`, branch-shape cases, hybrid posture explicitly declared in Overview, with a "replacement on Product Brief authoring" follow-up. The matched review skill on 2026-05-04 accepted the hybrid as a documented deviation (not a refusal trip), with one specific point-finding (TC-024 named an internal Go interface method in `expected:`, fixed in revision).

**The gap.**

1. **SKILL.md HALT condition #1 is too coarse for partial-parent cases.** The skill says: *"missing parent spec — leaf without parent DD; branch without parent Architecture; root without Requirements + Product Brief"* → HALT. But the root case is more nuanced: Requirements exists, Product Brief does not. The skill doesn't distinguish "no parent at all" from "one of two canonical parents present, the other missing for a documented upstream-traceable reason".
2. **`references/per-layer-weight.md` table forces a level-vs-shape contradiction.** Root scope → `level: system`. But case shape comes from the parent spec type: Requirements + PB → root-shape (user-journey narrative); Architecture → branch-shape (fixtures-rich preconditions). With Product Brief absent, the level-vs-shape pairing breaks and the skill provides no fallback rule.
3. **Generalises across artifact-types.** The same shape applies elsewhere — leaf TestSpec without DD but with Architecture (the parent's parent); branch testspec without Architecture but with Requirements. The author-testspec skill needs a framework-level rule for "next-best parent" with explicit shape-vs-level acceptance criteria.

**Suggested resolution.**

- **Add a partial-parent fallback section** to `vmodel-skill-author-testspec/SKILL.md`: *"When the canonical parent for a layer is partially missing (one of multiple required parents absent for a documented upstream-traceable reason), three paths are acceptable — choose explicitly: (a) HALT and request the missing parent be authored first (default unless the upstream gap is structurally deferred); (b) author from the next-best available parent and document the deviation in Overview, surfacing the hybrid layer/level posture; (c) author against framework-reference content as upstream only when the framework reference is itself a canonical artifact in the framework scope tree. The hybrid (b) path requires: declared `level:` follows scope position; declared case shape follows the actual parent spec type; deviation explicitly documented in Overview with a 'replacement on canonical-parent authoring' follow-up."*
- **Add a row to `references/per-layer-weight.md`** for the hybrid case: *"Root scope, derived from Architecture only (Product Brief absent for documented reason): `level: system` + branch case shape; expected: in user-vocabulary-equivalent terms (verdict, findings, exit codes, HTML), not internal API names."*
- **Cross-link to Issue 9.** The same upstream-missing pattern affects every author skill; the testspec-specific instance should be unified with the generalised protocol from Issue 9.

**Pairs with.** Issue 9 (no protocol for downstream artifacts with no canonical upstream — same family, generalised) and Issue 1 (Product Brief absence is the specific upstream gap that triggered this session's hybrid).

---

### Issue 19 — Author-testspec refusal-C boundary is unclear for upstream-pending NFR thresholds

**Where surfaced.** `vmodel-skill-author-testspec` authoring of TC-023 (REQ-022 latency NFR) and review by `vmodel-skill-review-testspec` (2026-05-04). The case carried `expected.threshold: "TBD-by-REQ-022-pilot-calibration"` because REQ-022 in the parent requirements artifact carries an explicit follow-up to set fail/goal/stretch/wish from pilot calibration (the resolution Issue 7 documented).

The author self-flagged `[QB-FAIL: oracle-specificity]` in the case's notes. On adversarial review, the reviewer judged this NOT to be a refusal-C trip on the grounds that:

- Refusal-C tells (per `references/case-quality.md`) are qualitative phrases: "verifies behaviour", "works correctly", "does not throw" alone, "non-null" alone, "instance of X" alone.
- A structured placeholder string (`"TBD-by-REQ-022-pilot-calibration"`) with named upstream owner and resolution path is structurally different from a qualitative phrase.
- The skill's own template (`templates/coverage-mutation-bar.yaml.tmpl`) explicitly permits `"TBD-by-project-policy"` placeholders in coverage thresholds; same logic should apply to performance thresholds with documented upstream-pending resolution.

The reviewer captured the case as `info` (downstream-pending), not soft-reject.

**The gap.**

1. **Skill silence on the placeholder pattern.** `references/case-quality.md` enumerates refusal-C tells but does not address structured placeholders. An author following the rules strictly might either (a) refuse to author the case at all (HALT), or (b) hard-reject themselves at draft time (refusal-C self-trip) — both wrong outcomes when the upstream NFR is legitimately pending and the case shape is fully specified.
2. **Reviewer judgment is precedent, not rule.** The 2026-05-04 review's "info, not refusal-C" call was the reviewer's independent reasoning, not a written rule. A different reviewer (or autonomous review run) might trip refusal-C on the same case.
3. **Pattern applies beyond performance.** The same pattern surfaces wherever an oracle's literal value depends on a downstream-pending decision: TC-007's "or equivalent locale-stable phrasing decided by reporter DD" (HTML literal strings deferred to reporter DD), TC-022's abstract subcommand description (CLI surface deferred to cli-adapter DD).

**Suggested resolution.**

- **Add a placeholder-oracle subsection** to `references/case-quality.md`: *"A structured placeholder oracle is permissible when (a) the placeholder string is explicitly typed (e.g., `\"TBD-by-REQ-022-pilot-calibration\"`, not `\"TBD\"`), (b) the resolution path is named (a specific upstream artifact, requirement, or DD), (c) a named owner is identified for closing the gap, and (d) the case's surrounding oracle elements (metric, sample size, environment) are fully specified. Such cases are not refusal-C trips and are captured as `info` rather than soft-reject. They are NOT executable as CI gates until the placeholder resolves; the artifact's Open follow-ups section tracks the resolution. Distinct from qualitative phrases ('works correctly', 'does not throw' alone) which are refusal-C."*
- **Mirror the rule in review skills.** Update `vmodel-skill-review-testspec/references/case-quality-checks.md` to explicitly distinguish placeholder oracles from weak assertions, citing the four conditions above. Add a `check.oracle.deferred-placeholder` `info` finding for cases that meet the criteria; reserve `check.oracle.weak-assertion` for the genuinely qualitative cases.
- **Document the pattern at template level.** Add an example placeholder oracle to `templates/case-branch.yaml.tmpl` (and case-root.yaml.tmpl) showing the four-condition shape, distinguishing it from a weak assertion in a leading comment.

**Pairs with.** Issue 4 (no-design-language discipline silent on premature numerical commitments) and Issue 7 (NFR five-element rule has no protocol for explicitly deferred numerical targets) — all three concern the same gap: the framework's no-fabrication discipline is specified for vocabulary and numbers at *requirements* time, but its downstream consequences at *testspec* time are not articulated.

---

### Issue 20 — Author-testspec skill does not explicitly mandate per-typed-error case coverage

**Where surfaced.** `vmodel-skill-author-testspec` first-draft authoring of `specs/testspec.md` (2026-05-03). The architecture's IArtifactLoad interface declares four typed errors:

```yaml
errors:
  - { code: "ErrTargetUnreadable", meaning: "..." }
  - { code: "ErrTargetNotFound",   meaning: "..." }
  - { code: "ErrParseFailure",     meaning: "..." }
  - { code: "ErrIOFailure",        meaning: "..." }
```

The first draft covered three: ErrParseFailure (TC-004), ErrTargetUnreadable (TC-005). ErrTargetNotFound was missed; ErrIOFailure was rolled into ErrParseFailure's halt-and-report case (TC-004) without an isolating case. The 2026-05-04 review caught ErrTargetNotFound as F-002 (`check.derivation.error-path-uncovered`); ErrIOFailure remains unverified.

**The gap.**

1. **`references/architecture-traceability-cues.md` says only:** *"Interface entry — precondition → Error case forcing precondition violation across the boundary"*. That instructs on preconditions, not on the `errors:` enum's exhaustiveness. An author who derives cases from preconditions only (rather than from the typed-error enum) will miss errors that don't correspond to a precondition.
2. **`references/derivation-strategies.md` for the `error` strategy says:** *"One case per detection condition asserting typed error + state guarantee"*. This is closer but still ambiguous — "detection condition" can be read as "precondition violation", which is a subset of typed-error enum entries.
3. **Empirical signal.** This session, IArtifactLoad declared 4 typed errors; the first draft covered 2 of 4 (50% coverage at draft time). Pairs with Issue 11's empirical signal (75% defect rate at the propagation interface for ADR-author skill); both indicate that "the right discipline exists at review time but not at author time" pattern is a recurring framework gap.

**Suggested resolution.**

- **Add explicit typed-error-enum coverage rule** to `references/architecture-traceability-cues.md`:
  > *"Every entry in an interface's `errors:` enum requires at least one case under the `error` or `fault-injection` strategy. The case's `verifies:` resolves to `ARCH.interfaces.<name>.errors.<code>`. Roll-up cases (one case covering multiple errors via shared halt-and-report path) are permissible when the parent interface contract treats them uniformly, but each rolled-up error code MUST be cited explicitly in the case's `verifies:` list. Missing-error coverage is a soft-reject (`check.derivation.error-path-uncovered`), not refusal."*
- **Add a per-case `verifies:` granularity hint** to the slot-fill examples in `architecture-traceability-cues.md` showing typed-error-enum-level qualification (e.g., `ARCH.interfaces.IArtifactLoad.errors.ErrTargetNotFound`).
- **Mirror the rule in `vmodel-skill-review-testspec`** so the review skill enumerates the parent's typed-error enum and lists missing-coverage by code, rather than catching only the most visible omission.

**Pairs with.** Issue 11 (per-skill discipline gap) and Issue 16 (architecture-author skill landing rules) — same shape: mechanically-detectable failure mode where the review skill catches what the author skill emits without a gate.

---

### Issue 21 — Implicit-`verifies` pattern: REQs exercised by precondition or expected text but not listed in case-level `verifies:`

**Where surfaced.** `vmodel-skill-review-testspec` adversarial review of `specs/testspec.md` (2026-05-04), finding F-005. Multiple cases referenced specific REQ-NNN content in their `preconditions:` or `expected:` text without listing the REQ in their `verifies:` list:

- **TC-001** preconditions: `"Output format: JSON (the AI-caller default per REQ-024)"` — exercises REQ-024 (validation CLI surface), but `verifies:` did not include REQ-024.
- **TC-001 / TC-002 / TC-004** expected: assert verdict-record values from the closed set `{pass, fail, system-error}` (REQ-027's enum), but `verifies:` did not include REQ-027.
- **TC-006 / TC-007 / TC-008 / TC-009** all assert HTML output per REQ-025, but only one (TC-006 after revision) cites REQ-025.
- **TC-022** uses the version manifest mechanism per REQ-030 + REQ-032, but the first draft cited only REQ-032.

The review surfaced 4 unlinked REQs across 24 first-draft cases; revisions on 2026-05-04 added the citations. This is structurally similar to F-002 (typed-error enum coverage) but for requirement-level traceability rather than typed-error-level.

**The gap.**

1. **Skill silence on REQ-citation discipline.** `references/verifies-traceability.md` says *"every `verifies:` element must resolve to a live ID in the upstream artifacts"* and discusses granularity per layer, but does not say *"every REQ-NNN whose content the case references in `preconditions:` or `expected:` MUST be listed in `verifies:`"*. The author can implicitly exercise a REQ without citing it.
2. **Empirical signal.** First-draft testspec implicitly exercised at least 8 REQs (REQ-024, REQ-025, REQ-027, REQ-030 — plus probably others) without citation. Approximately 30% under-citation rate at draft time.
3. **Knock-on effect: requirement-unverified soft-rejects at review time.** F-005 was the dominant soft-reject in the 2026-05-04 review precisely because of this pattern. Five REQs reported as unverified, four of which were actually exercised but uncited.
4. **The author-time discipline is mechanically derivable.** A simple text-grep of each case's preconditions + expected for `REQ-NNN` strings, cross-referenced against the case's `verifies:` list, would mechanically catch the gap. Currently no such gate exists.

**Suggested resolution.**

- **Add an implicit-`verifies` rule** to `references/verifies-traceability.md`: *"When a case's `preconditions:` or `expected:` text mentions a specific upstream identifier (REQ-NNN, IC-NNN, ADR-NNN, ARCH.interfaces.X), that identifier MUST appear in the case's `verifies:` list. The text reference is the case's commitment to verifying that upstream content; omitting it from `verifies:` produces a silent traceability gap. Pre-publish self-check: grep each case's preconditions and expected text for upstream-id patterns; cross-reference against the verifies list."*
- **Add a self-check step** to `vmodel-skill-author-testspec/SKILL.md` Step 6 (Specify each case to the oracle bar): *"Before declaring the case complete, scan its preconditions and expected for any upstream-id pattern (`REQ-\d+`, `IC-\d+`, `ADR-\d+`, `ARCH\.\w+`) and confirm every match appears in the case's `verifies:` list."*
- **Add a review-side check** `check.verifies.implicit-reference-uncited` to `vmodel-skill-review-testspec`. Mechanically derivable; high signal-to-noise.

**Pairs with.** Issue 20 (typed-error enum coverage discipline), Issue 11 (per-skill discipline caught at review only), Issue 16 (architecture landing rules) — all four concern mechanically-detectable failure modes that should be author-time gates but currently surface only at review.

### Issue 22 - files are growing too large. 
Even for a project quite small like this one, the architecture.md is above 30k tokens. a session of just running a single author skill have been at around 250-300k tokens, and review at around 100k. This is too large for doing quality work in anything but the high-end models.

### Issue 23 - unclear what the testspec should verify. is it requirements? or is it architecture?

