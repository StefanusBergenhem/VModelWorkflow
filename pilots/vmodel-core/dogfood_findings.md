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

### Issue 24 — `check-typed-error-coverage` script doesn't know about the leaf-testspec deferral pattern

**Where surfaced.** Running `scripts/check-typed-error-coverage.py` against the pilot's root spec tree on 2026-05-10 produced 12 findings (typed errors declared in interface specs but no testspec case verifies them). Investigation: 9 of those 12 errors are internal-component errors (`IArtifactLoad.ErrIOFailure`, `IEmit.ErrInvalidVerdict`/`ErrSinkWrite`/`ErrUnsupportedFormat`, `IFrameworkResources.ErrUnknownArtifactType`, `IGraphBuild.ErrMalformedFrontMatter`, `IReport.ErrInvalidParameters`/`ErrUnknownReportType`, `IValidate.ErrPreconditionFailed`) that the root testspec explicitly defers to per-component leaf testspecs (testspec.md "Inherited upstream gaps" section, architectural choice documented at draft time). 3 of 12 mapped cleanly to existing root cases (TC-004, TC-005, TC-025) and were added in 2026-05-10 fixup; 1 remaining (`IReportCLI.errors.system-error`) is a real root-layer gap.

**The gap.**

The script treats the spec tree as a single layer and complains about every typed error not verified at the root, even when the architectural choice explicitly defers internal-interface error coverage to leaf testspecs (which don't yet exist because leaf DDs haven't been authored). This produces high noise once non-leaf-coverable errors are excluded.

**Suggested resolution.**

1. **Script side.** Extend `check-typed-error-coverage.py` to accept a per-interface coverage-layer declaration (e.g., `coverage_layer: leaf` in the interface YAML), and skip findings for errors whose interface is declared leaf-covered when only the root testspec exists.
2. **Spec-author side.** When the root testspec defers component errors to leaf testspecs, declare it explicitly in the interface YAML so the check script can honour the deferral.
3. **Real-gap action.** `IReportCLI.errors.system-error` should be covered by a new root-layer case (TC-027: "Reporting invocation against an unreadable input produces verdict=system-error with exit code 2") modelled on TC-005. Track as a follow-up; do not fabricate the case at this migration pass.

**Pairs with.** Issue 17 (ID encoding), Issue 20 (typed-error case coverage discipline) — both surface from mechanical-check scripts whose assumptions don't perfectly match the spec-tree state.

## 2026-05-11

### Issue 25 — REQ-016 names six canonical artifact types but the framework publishes a seventh schema (`architecture-interface-detail`)

**Where surfaced.** Authoring `DD-embedded-resources` (the leaf DD that owns typed accessors over `embed.FS` for the rule catalog, schema set, and Quality Bar checklist set). Defining the `ArtifactType` closed enum required reconciling two upstream sources:

- **`specs/requirements.md` REQ-016 + Glossary.** The *Framework canonical schema set* glossary entry names exactly **six** per-artifact schemas: `product-brief, requirements, architecture, adr, detailed-design, test-spec`. REQ-016 obliges vmodel-core to validate each artifact against the per-artifact schema corresponding to its `artifact_type`.
- **Framework `schemas/artifacts/`.** Publishes **seven** per-artifact schema files. The seventh — `architecture-interface-detail.schema.json` — has its own `artifact_type` const value (`architecture-interface-detail`) and is the canonical shape for the Rule-8 architecture bundle's per-interface detail files (`<scope>/architecture/interfaces/<NAME>.md`).

**The gap.** The seventh schema exists structurally (Rule 8 architecture bundle files in the pilot tree right now would be subject to it, e.g. `IFrameworkResources.md`), but is not enumerated in REQ-016's contract or the Glossary. Two clean outcomes; one wrong one:

1. **Amend REQ-016 + Glossary to seven types.** Treat `architecture-interface-detail` as a first-class artifact type subject to vmodel-core schema validation. The cost is small (one Glossary entry, one phrase in REQ-016, an enum member to add in `DD-embedded-resources`). This is most likely the right outcome — interface detail files are real artifacts in the spec tree and there is a real schema for them.
2. **Mark `architecture-interface-detail` as a non-validated sub-shape of `architecture`.** Treat the interface detail files as fragments of the parent architecture artifact for validation purposes; do not publish them as a distinct `artifact_type` to vmodel-core. Requires retracting the `artifact_type: architecture-interface-detail` const from `architecture-interface-detail.schema.json` (or making it internal-only).
3. **(Wrong.)** Quietly grow the `DD-embedded-resources` ArtifactType enum to seven without amending REQ-016. This is DD inventing past its upstream and would silently fail the requirements / DD trace test.

**Pilot decision for this session.** `DD-embedded-resources` pins the ArtifactType enum at six per REQ-016 (no DD invention). The seventh schema's runtime addressability through `IFrameworkResources` is blocked on the requirements amendment.

**Suggested resolution.** Pick outcome (1) or (2) at framework scope, then propagate:

- **If (1):** amend `requirements.md` REQ-016, REQ-017, and the *Framework canonical schema set* / *Framework canonical Quality Bar checklist set* Glossary entries to name seven types. Amend `DD-embedded-resources` ArtifactType enum and bundle layout to include `architecture-interface-detail.schema.json`. (There is no `architecture-interface-detail.quality-bar.json` today — decide whether QB applies to detail files too.)
- **If (2):** retract or internalise the `artifact_type` const in `architecture-interface-detail.schema.json`; document the interface-detail files as validation-scope-internal sub-shapes of `architecture` in the schema reference.

**Pairs with.** Issue 16 (architecture skill: where do ADR-bound library / protocol bindings land) — both concern the gap between what the schemas publish as first-class artifact types and what the requirements layer enumerates.

### Issue 26 — DEFER markers bleed across scopes when cited in prose

**Where surfaced.** Authoring `DD-embedded-resources` on 2026-05-11. The DD's Overview originally cited the parent ARCH's existing `[DEFER-DD: validation-engine — JSON Schema 2020-12 validator library selection]` in prose to explain why this leaf returns raw JSON bytes (not pre-parsed Schema objects). `scripts/index-deferred-items.py` picked up the prose citation as a new DEFER-DD marker anchored at `DD-embedded-resources`. The deferral genuinely lives at `validation-engine` scope; the DD merely references it. The fix in this session was to drop the bracket form and paraphrase in prose — i.e., the author skill silently rewards rewording around the script rather than supporting honest cross-reference.

**What the script does.** Matches `[DEFER-(DD|ADR): ...]` anywhere in any artifact body, regardless of whether the bracket form is an *owning* marker (this artifact owns the deferred decision) or a *citing* reference (this artifact references another artifact's deferred decision).

**What `authoring-discipline.md` Rule 6 says.** A `[DEFER-<TARGET>: <topic>]` marker names a deferred decision and the artifact at which it will be answered. Implicit semantics: the marker should appear *exactly once* in the spec tree — at the artifact where it will be answered.

**The gap.** There is no canonical syntax to *cite* a DEFER marker by reference. Two side effects:

1. The author skill rewards paraphrasing-around-the-script over honest cross-reference; an author who cites the marker verbatim is "punished" by the index counting it twice (and by `index-deferred-items.py` inflating the apparent surface area of unresolved gaps).
2. The defer-index conflates "this artifact owns this deferral" with "this artifact is aware of it" — different things; a human reading the index cannot tell which is which.

**Suggested resolution.**

1. **Script side.** Make `index-deferred-items.py` distinguish *owning* marker from *citing* prose. Two options: (a) introduce a bracket-syntax distinction (e.g., `[DEFER-DD: ...]` for owners; `[cite-DEFER-DD: <owner-artifact-id>]` or `«DEFER-DD: <owner-id>»` for citations); (b) deduplicate by topic-string equality — if the same bracket text appears in multiple artifacts, attribute the marker to the artifact whose scope matches the marker's `<scope>` segment or whose `parent_architecture` chain identifies it as the owner.
2. **Rule 6 side.** Extend `authoring-discipline.md` Rule 6 to specify how to cite a DEFER marker from a downstream artifact without re-emitting it, or to explicitly forbid prose citation of bracket markers (forcing prose-only descriptions of upstream deferrals).
3. **Author-skill side.** Add explicit guidance to author skills: when referencing another artifact's deferred decision, do not use the `[DEFER-XX: ...]` bracket form; describe the deferral in prose with an artifact-id citation to the owner.

**Pairs with.** Issue 6 (skill template / schema mismatch — adjacent failure mode where stale skill conventions create phantom artifacts in the index).

### Issue 27 — Authoring a "simple" leaf DD consumes 178k tokens of session context

**Where surfaced.** Authoring `DD-embedded-resources` on 2026-05-11. The leaf is one of the simplest in the architecture: stateless, one error code, six accessors with shared shape, sub-megabyte data, every load-bearing decision inherited from ADR-002 / `IFrameworkResources`. Total message-channel context after authoring + mechanical-check sweep + dogfood-finding logging: 178k tokens (per `/context` 21% of a 1M-token window).

**Approximate breakdown.**

- ~30k loading the skill SKILL.md + references (`dd-purpose-and-shape`, `function-contracts`, `data-structures-by-invariant`, `error-handling`, `algorithms`, `state-and-concurrency`, `anti-patterns`, `quality-bar-checklist`) + template + worked example.
- ~25k loading the pilot's parent ARCH, ADR-002, REQ-016 / REQ-030..032, `IFrameworkResources` detail, `partial-parent-protocol`, `authoring-discipline`.
- ~15k schema-validation snippets (jsonschema + referencing install, registry build, validator runs — see Issue 28).
- ~12k pre-existing `dogfood_findings.md` context (read for Issue 25 append).
- ~80k authoring + iterative refinement + dogfood-finding drafts.

**The gap.** Even on the cheapest valid leaf in the product, a single authoring session consumes ~17% of a 1M-token window on a top-tier model. Mid-tier models (Sonnet, Haiku) with smaller working windows would have to either skip references (degrading craft floor) or split authoring across multiple sessions (degrading coherence). Issue 22 captured the same shape for `architecture.md` *file* size; this issue names the *session* cost for the simplest DD. The framework's Haiku-floor eval discipline (memory: `feedback_eval_model.md`) is at risk: if the cheapest leaf overflows mid-tier context budgets, every leaf will.

**Suggested resolution.** This is the dogfooding finding the framework was built to surface. Directions worth stakeholder triage:

- **Reference compression.** Per-skill, can the bundled references compress to ≤10k tokens without losing craft floor? `dd-purpose-and-shape` + `function-contracts` + `data-structures-by-invariant` + `error-handling` are the load-bearing four; `algorithms` + `state-and-concurrency` + `anti-patterns` + `quality-bar-checklist` add craft pedagogy that may overlap with content already in those four.
- **Selective reference loading.** Split SKILL.md into a thin shell that names references and a flag-set indicating which apply for this artifact's shape (stateless / stateful, greenfield / retrofit, single-state-machine / multi). For `DD-embedded-resources`: `state-and-concurrency` was mostly N/A, `retrofit-discipline` fully N/A. Both loaded anyway.
- **Pilot upstream caching.** The pilot's ARCH + ADRs + REQ slices needed for any DD in this product are stable across DD authoring sessions. A pilot-level "what every DD in this product must know" summary (under `pilots/vmodel-core/`) would replace re-reading 5 upstream files per session.
- **Mechanical-check tooling.** Inline schema-validation snippets (Issue 28) cost ~15k of this session's budget; a pre-built script would amortise that to a few hundred tokens per run.

**Pairs with.** Issue 22 (architecture.md file size — same shape, different surface), Issue 28 (mechanical-check tooling missing → inline snippets), feedback memory `feedback_eval_model.md` (Haiku-floor evals).

### Issue 28 — Schema validation is invented per-session instead of being a pre-built script

**Where surfaced.** Authoring `DD-embedded-resources` on 2026-05-11. The DD author skill's Step 13 (Pre-publish mechanical self-check) lists `scripts/check-mermaid.py` and `scripts/check-id-encoding.py` as the canonical scripts but **does not** include a JSON Schema validation step. To validate front-matter against `detailed-design.schema.json` and embedded YAML blocks against the per-block `$defs`, the author session wrote two ad-hoc inline Python snippets via bash heredoc:

1. Parse front-matter, build a `referencing.Registry` from every schema under `schemas/`, run a `Draft202012Validator` against `detailed-design.schema.json`.
2. Extract every `\`\`\`yaml\` block from the body, identify which `$defs` member each should validate against (`public_interface_entry`, `data_structure_entry`, `error_matrix_row`), validate each entry.

**Real defects caught only because the snippets were written.** The first run reported one front-matter error: `title: 'title' is a required property`. The `title` field had been omitted; **none of the scripts listed in Step 13 detect this**. The artifact would have shipped schema-invalid had the snippets not been written. Two of the existing scripts (`check-id-encoding.py`, `check-template-schema-fields.py`) target adjacent concerns but neither validates against the JSON Schema.

**Cost side.** Writing, debugging (`jsonschema` not installed in the project venv → `pip install jsonschema referencing` → re-run), and re-running the snippets consumed ~15k of the session's token budget (Issue 27). This work is identical at every author session — every author skill across every artifact type — and so is pure waste against the schema-validation goal.

**The gap.** Schema validation is the single most foundational mechanical check (it is, after all, what `vmodel-core` itself will do as a CLI per REQ-015 / REQ-016). Author skills should not invent it per session. The current Step 13 script list lets schema-invalid artifacts ship if no author thinks to add the check.

**Suggested resolution.**

1. **Until `vmodel-core` ships — add `scripts/check-schema-validation.py`.** Generic validator that:
   - Reads any artifact path.
   - Reads `artifact_type` from front-matter.
   - Locates the corresponding `schemas/artifacts/<type>.schema.json`.
   - Validates front-matter against the per-artifact schema (which composes the envelope).
   - Extracts embedded YAML blocks from the body, identifies the `$defs` member by section context (`Public Interface` → `public_interface_entry`, `Data Structures` → `data_structure_entry`, error-matrix table → `error_matrix_row`).
   - Validates each entry; emits `<file>:<line>:<rule-id>:<message>` per finding; exit 0 / 1 / 2 per the existing script convention.

2. **Add the script to every author skill's Step 13 (Pre-publish mechanical self-check),** since the check is uniform across all six artifact types.

3. **After `vmodel-core` ships** — retire `scripts/check-schema-validation.py`; replace the Step 13 entry with `vmodel-core validate <artifact-path>`. The script is interim scaffolding for the period before the canonical validator is available.

**Pairs with.** Issue 24 (`check-typed-error-coverage` — another mechanical script whose assumptions don't perfectly match the spec-tree state), Issue 27 (session token cost — schema-validation snippets are a large slice of the waste).

### Issue 29 — Mechanical-check script paths in SKILL.md are ambiguous (bundled vs repo-root)

**Where surfaced.** Authoring TestSpec for `embedded-resources` on 2026-05-11. `vmodel-skill-author-testspec` SKILL.md Step 11 lists:

> Scripts for this skill:
> - `scripts/check-implicit-verifies.py <specs-root>` — ...
> - `scripts/check-typed-error-coverage.py <specs-root>` — ...
> - `scripts/check-id-encoding.py <specs-root>` — ...

The literal `scripts/...` path is ambiguous between the skill's bundled `scripts/` subdir (analogous to the bundled `references/` and `templates/`) and the repo-root `scripts/`. I first invoked them as `python3 .claude/skills/vmodel-skill-author-testspec/scripts/check-implicit-verifies.py ...` and got `No such file or directory`. The scripts actually live at `/scripts/check-*.py` at the framework repo root.

**The gap.** The path notation does not unambiguously name the directory. The skill bundles `references/` and `templates/` in-tree, so "scripts/" reads naturally as another bundled subdir — but it isn't. Every author skill that lists Step-11 scripts has this same ambiguity. Authors and downstream agents will hit the same misread; the bash failure mode is non-catastrophic (the agent retries with a different path) but the misread costs tokens and session time.

**Suggested resolution.**

- Resolve via `.vmodel/config.yaml` — add `paths.scripts` (matching the existing `paths.references` pattern). Skills then refer to `${paths.scripts}/check-implicit-verifies.py`. Framework default `paths.scripts: scripts/` resolves at the repo root; projects can relocate.
- Apply across every author skill's Step 11 / Pre-publish self-check sections in one sweep.

**Pairs with.** Issue 28 (`check-schema-validation.py` missing — sibling script-discoverability gap), Phase 6 central-config pattern (the `paths.*` family).

### Issue 30 — Leaf TestSpec closing an ARCH-level typed-error must dual-cite, and the rule is buried mid-sentence

**Where surfaced.** Authoring TestSpec for `embedded-resources` on 2026-05-11. The leaf TestSpec naturally cited `DD-embedded-resources.public_interface.Schema.errors.ErrUnknownArtifactType` for TC-007 / TC-008 — the layer-correct granularity per `per-layer-weight.md` (leaf → DD field). `check-typed-error-coverage.py` then reported `ARCH.interfaces.IFrameworkResources.errors.ErrUnknownArtifactType` as uncovered because it looks for the ARCH-level path literally and does not traverse the DD's `parent_architecture` / `derived_from` link back to the ARCH interface.

Step 6 of `vmodel-skill-author-testspec` says:

> "Typed-error enum coverage: every entry in a parent interface's `errors:` enum requires at least one case under the `error` or `fault-injection` strategy. Roll-up cases (one case covering multiple errors via shared halt-and-report path) are permissible when the parent contract treats them uniformly, but each rolled-up code MUST be cited in the case's `verifies:` list. Mechanically detected by `scripts/check-typed-error-coverage.py` at Step 11."

The "each rolled-up code MUST be cited" half is buried mid-sentence and reads at first scan as covering only the roll-up case. The cross-layer dual-citation pattern (leaf closes ARCH-level typed-error by citing BOTH the DD-level error path AND the ARCH-level error path in the same case's `verifies:`) is not stated explicitly anywhere — neither in Step 6, `verifies-traceability.md`, nor `dd-traceability-cues.md`.

**The gap.** A layer-correct authoring pass (leaf cites DD only) silently fails the mechanical check. The author must either: (a) add the ARCH-level citation manually after the check fails; (b) read `check-typed-error-coverage.py` source to understand what it looks for. I did (a) after the check fired. A first-time author would probably do (b), expanding token cost.

**Suggested resolution.**

- **Author-side fix** (cheapest). Promote the dual-citation rule to its own bullet in Step 6 with a worked example: a leaf case whose `verifies:` carries both `DD-<scope>.public_interface.<fn>.errors.<code>` and `ARCH.interfaces.<iface>.errors.<code>`. Cross-link from `verifies-traceability.md` and `dd-traceability-cues.md`.
- **Script-side fix** (more involved, correct). Teach `check-typed-error-coverage.py` to traverse a DD's `parent_architecture` and `derived_from: [..ARCH-IF-X..]` links and infer that DD-level coverage closes the ARCH-level row. Mirrors what a human reviewer does mentally.

Author-side fix is fast and visible; script-side fix is the long-term correct answer. Both warranted.

**Pairs with.** Issue 24 (`check-typed-error-coverage` deferral-pattern blind spot — same script, sibling concern).

### Issue 31 — QB "error/happy ratio ≥ 1:2" lacks an escape valve for leaves with small genuine error surface

**Where surfaced.** Authoring TestSpec for `embedded-resources` on 2026-05-11. The DD's error matrix has exactly one row (`ErrUnknownArtifactType`) across two callsites, exhaustively covered by TC-007 / TC-008. The success/invariant surface needs 12 cases (six contract + five byte-stability + one thread-safety). Result: error/happy ratio is 2:6 = 1:3, below QB Group 2's heuristic of ≥ 1:2.

`quality-bar-checklist.md` Group 2 reads:

> "Error / happy ratio is at least 1:2."

And the checklist's preamble says:

> "When any 'Yes' cannot be honestly answered, do not ship — surface the gap."

For leaves whose DD genuinely has one or two error-matrix rows (and where bundle absence / decode failure / sandbox violation are *explicitly* out of scope at the leaf — system-level or build-time, with documented rationale), no amount of honest authoring can lift the ratio without fabricating error surface. The honest move is to write an inline Overview paragraph naming the non-fit and the reason. I did this; the reviewer judged the framing legitimate.

**The gap.** No documented escape pattern. Authors either: (a) silently pass — close cousin of `anti-pattern.coverage-as-quality-metric` (ratio rhetoric without surface); (b) fabricate "robustness" cases for non-existent failure modes — direct anti-pattern; (c) write inline justification each time — what I did, fine but un-documented and varies by author. Reviewers must re-judge each instance.

**Suggested resolution.**

- Soften the bar in `quality-bar-checklist.md` Group 2 to a conditional phrasing: *"Error / happy ratio is at least 1:2 when the parent spec's error surface supports it; otherwise the author names the non-fit and the reason in the Overview, citing which DD error-matrix rows are covered and which failure modes are out-of-scope-with-rationale."*
- Cross-reference from `anti-patterns.md` so the legitimate-non-fit pattern is documented adjacent to the fabrication anti-pattern it's the opposite of.

**Pairs with.** Refusal C (no weak assertions) and the broader honest-authoring discipline — the legitimate-non-fit is the *opposite* of the fabricated-intent refusal: the author refusing to fabricate and naming the gap instead.

### Issue 32 — Review-file path convention is split between author-skill SKILL.md and pilot CLAUDE.md

**Where surfaced.** Authoring TestSpec for `embedded-resources` on 2026-05-11, dispatching the review subagent. Step 0 of `vmodel-skill-author-testspec` reads:

> "If `specs/.reviews/<artifact-id>-*.yaml` contains review files for this artifact: ..."

Per TARGET_ARCHITECTURE §5.6 review output convention.

The pilot's CLAUDE.md says:

> ```
> .vmodel/
>   .reviews/             — Spec-side review verdict files (checked in)
> ```

So the canonical path is split: framework author-skill says `specs/.reviews/`, pilot says `.vmodel/.reviews/`. The reviewing subagent had to pick one; it picked the pilot convention. Step 0 of the *next* author-skill revision pass will look at `specs/.reviews/` (per SKILL.md) and find no review files, silently treating the artifact as never-reviewed.

**The gap.** Two canonical paths. Authors and review subagents drift apart. Revision-pass Step 0 (which reads the latest review) silently loses review state if the path used at write-time differs from the path used at read-time. The drift is not detected by any mechanical check — `index-deferred-items.py` doesn't traverse review state.

**Suggested resolution.**

- Resolve via `.vmodel/config.yaml` `paths.reviews` (matching the existing `paths.references` pattern). Framework chooses a default; projects may override.
- Pick the default: `.vmodel/.reviews/` matches the rest of the central-config pattern from Phase 6 Cluster 5 (config, references, build outputs all under `.vmodel/`); `specs/.reviews/` keeps reviews next to the artifacts but inverts the central-config convention. Recommend `.vmodel/.reviews/`.
- Update every author-skill Step 0 reference and every review-skill output path to read `paths.reviews` instead of literal `specs/.reviews/`. Update TARGET §5.6 to name the central-config indirection.

**Pairs with.** The `.vmodel/config.yaml` `paths.*` family introduced in Phase 6 Cluster 5. TARGET §5.6 (review output convention — currently the authoritative source for `specs/.reviews/`).

### Issue 33 — Review subagent for one leaf TestSpec consumed ~100k tokens

**Where surfaced.** Dispatching the review of `TS-embedded-resources` on 2026-05-11 via the general-purpose Agent (subagent_type: general-purpose, no project-bundled review-execution agent because this is a *spec-side* review, not a build-side review). The subagent reported `total_tokens: 102634, tool_uses: 24, duration_ms: 123267`.

**Approximate breakdown.**

- ~25k loading the review skill SKILL.md + references (review skill bundles its own checklist + anti-pattern catalog + per-layer-shape reference).
- ~30k loading the artifact under review + parent DD + governing ADR + the `IFrameworkResources` interface detail + the referenced REQs.
- ~15k iterative re-reads while applying QB checklist + anti-pattern sweep.
- ~30k synthesis, finding-drafting, YAML emission, writing the review file.

**The gap.** A *review* should be cheaper than authoring. The author session for the same artifact (~80k tokens just for authoring + iteration after the 60k of skill/upstream loading — see Issue 27's breakdown shape applied to this TestSpec) reflects the cost of *producing* the artifact. The review only *consumes* the artifact and applies checks. ~100k tokens for one leaf-TestSpec review producing one YAML with one info finding is a ~58% cost ratio of authoring — but the artifact-production / verdict-emission asymmetry is much larger than 58%.

Multiply across the pilot's expected build flow: 7 leaves × 1–2 review iterations on the TestSpec + 1–2 review iterations on the DD + branch + root reviews → ~30–40 spec-side review passes per pilot, at ~100k each → ~3–4M tokens just on spec-side reviews before code-side review begins. At Sonnet/Haiku context budgets, the review *cannot run* in a single subagent session if the cost stays at 100k.

**Suggested resolution.**

- **Review-skill reference compression.** The review skill duplicates large portions of the author skill's references (anti-pattern catalog, per-layer-shape, oracle-quality). Carry a *checklist-only* slice (no pedagogy, no examples) under 5k tokens on the review side; reviewers do not need to re-learn craft, they need the gates to apply.
- **Layer-conditional reference loading.** A leaf-TestSpec review does not need branch and root reference content; SKILL.md should branch on `level:` and load only the layer-relevant slice.
- **Author/review handoff via structured manifest.** The author session emits (or the author skill emits) a manifest naming `(artifact_path, derived_from, governing_adrs, mechanical_check_results, author_flagged_non_fits)`. The review subagent reads the manifest and the artifact only — does not re-discover the spec tree by chasing links. Cuts the ~30k spec-tree-loading slice substantially.
- **Pre-computed mechanical-check results consumed, not re-derived.** The review subagent in this rep was told the author had already run the mechanical checks; verify whether it re-ran them and trim if so.

**Pairs with.** Issue 27 (session token cost — author side, same shape), Issue 13 (handover between author/review should be file-based — sibling concern, surfaced earlier), feedback memory `feedback_eval_model.md` (Haiku-floor eval discipline — a Haiku-budget review session at ~200k working window cannot afford 100k just to verdict one artifact).

### Issue 34 — Complete leaf V-pair-completion session (TestSpec authoring + review + 5 dogfood findings) consumed ~150k parent-context tokens

**Where surfaced.** TestSpec-authoring session on 2026-05-11 ending with the commit that lands `TS-embedded-resources`. `/context` reported `148.9k / 1m tokens (15%)` on Opus 4.7 (1M context). The session covered: invoking `vmodel-skill-author-testspec`, reading parent DD + ARCH interface detail + ADR-002 + REQ-030/031/032, walking skill references (per-layer-weight, dd-traceability-cues, coverage-mutation-bar, quality-bar-checklist, template), authoring the 14-case TestSpec, running three mechanical-check scripts, dispatching the review subagent (which itself consumed ~100k in its isolated context — see Issue 33), applying TC-001 tightening per F-001, drafting five new dogfood findings (Issues 29–33).

**Approximate parent-context breakdown (~150k total).**

- ~12k initial context (framework CLAUDE.md, pilot CLAUDE.md, memory, system prompt).
- ~10k skill loading (`vmodel-skill-author-testspec` SKILL.md + references).
- ~25k reading parent DD + `IFrameworkResources` interface + ADR-002 + the three REQs.
- ~10k skill reference walks (per-layer-weight, dd-traceability-cues, coverage-mutation-bar, quality-bar-checklist, leaf-case template).
- ~15k authoring the TestSpec + iterating + TC-001 tighten.
- ~3k mechanical check runs + result reads.
- ~5k review-subagent dispatch (prompt out + summary in — the subagent's internal 100k stays in its own window).
- ~15k drafting and writing five new dogfood findings (interactive selection + ~5500 words of issue content).
- ~10k misc tool overhead + file-context syncing.

**Comparator with Issue 27.** DD authoring for the same leaf was 178k. TestSpec authoring + review + 5 findings was 150k. So a full leaf V-pair (DD + TestSpec + review + findings) costs ~328k parent-context tokens on Opus 4.7 (1M). The review subagent additionally consumes ~100k in its isolated window (Issue 33). The TestSpec session was *not* cheaper than DD authoring per artifact, despite Issue 27's prediction — the savings on upstream loading were eaten by review dispatch + finding drafting.

**The gap.** On a Sonnet (200k) working window, a full V-pair-completion session would consume 75%+ of context just to land one leaf, leaving no room for downstream work in the same session. On Haiku (200k) the same shape applies. The framework's Haiku-floor eval discipline is at risk: even running a single complete leaf V-pair in a Haiku session is structurally tight.

**The 60/40 split that matters.** Of ~150k, only ~75k was *load-bearing for the artifact*: skill loading, upstream reading, authoring, reviews. The other ~75k was *meta-overhead*: drafting dogfood findings (~15k), context syncing (~10k), iterative tool calls (~15k), interactive question flow (~15k), and the review-subagent handshake (~5k of parent tokens, with the bulk in the subagent). Reducing meta-overhead is the highest-leverage cost cut.

**Suggested resolution.**

- **Dogfood-findings batching.** Writing 5 findings inline cost ~15k. Defer finding-drafting to a dedicated session (or capture as one-liner stubs during authoring + flesh out in a batch). Trades immediate documentation for amortised token cost.
- **Tool-output trimming.** Several Reads loaded full files (testspec template, quality-bar-checklist) when only a section was needed. The author skill could pre-name section anchors so partial Reads are the default.
- **Review-result reconstitution.** The review-subagent's YAML output is the canonical record; the parent doesn't need to re-narrate it. A short tool-result summary suffices.
- **Pre-built session brief.** The pilot's `pilots/vmodel-core/CLAUDE.md` already pre-loads ~10k of context. Extending it with "what every leaf TestSpec session needs to know" (per-pilot skill-reference pre-loads, common upstream anchors) would offset some skill-reference re-loading.

**Pairs with.** Issue 27 (DD authoring session cost — 178k), Issue 33 (review subagent isolated cost — 100k), feedback memory `feedback_eval_model.md` (Haiku-floor eval discipline). The session-cost pattern is the dogfooding signal the framework was built to expose; Issues 27 + 33 + 34 collectively define the cost envelope of one leaf V-pair.

