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
