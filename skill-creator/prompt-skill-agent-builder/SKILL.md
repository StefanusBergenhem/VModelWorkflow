---
name: prompt-skill-agent-builder
description: Creates prompts, Claude Code skills, and agents following Anthropic's skill authoring guidelines and prompt engineering best practices. Use when the user wants to build, write, design, or scaffold a new prompt, skill, subagent, or system instruction. Detects type mismatches (e.g., a "skill" that is really an agent) and raises them once before proceeding. Produces the final artifact with frontmatter, progressive-disclosure structure, bundled templates and examples, and eval scenarios for Haiku-floor testing. Applies shared authoring discipline (single responsibility, degree-of-freedom calibration, anti-patterns, HALT conditions) plus type-specific guidance loaded on demand.
---

# prompt-skill-agent-builder

Create or edit one AI-instruction artifact: a prompt, a skill, or an agent.

## Flow

1. **Parse intent** → tentative type (prompt/skill/agent) + mode (create/edit).
   - Edit mode inferred if the user references an existing file or path. Confirm in one line: "editing existing <type> at <path>, not creating new — ok?"
   - Create mode needs no confirmation beyond the output-path step (§6).
2. **Type-mismatch check** → load the signal table in `references/<type>.md`. If ≥2 signals point to a different type, raise once: name the signals, state the recommended type, accept the user's call. Do not re-raise.
3. **Load type reference** → `references/prompt.md`, `references/skill.md`, or `references/agent.md`. Do not load the others.
4. **Interview** → open with this exact phrasing, verbatim:

   > Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

   Then walk the **Mandatory decisions** list in the active type reference in dependency order. One decision per turn (unless trivially coupled). Every question carries a recommended answer + one-line reasoning; user accepts or overrides. No open-ended questions without a default. Edit mode: parse the existing artifact first and interview only on gaps or weak answers.
5. **Termination** → interview ends when (a) every mandatory decision has an answer AND (b) 2 consecutive turns yield no new material information. User may shortcut with "skip interview, generate from spec" — proceed with defaults for anything unresolved and flag them in the self-review.
6. **Output path** → default by type:
   - prompt → emit to chat; optional save if user names a path.
   - skill → `~/.claude/skills/<name>/`.
   - agent → `./.claude/agents/<name>.md` (project-local).
   Confirm path in one line. Halt (§HALT) if path exists with substantive content and overwrite not confirmed.
7. **Self-review** → always. Run `references/anti-patterns.md` checklist against the generated artifact. Report findings in chat. Do not auto-fix; surface and ask.
8. **Eval scaffold** → ask: "generate 3 Haiku eval scenarios now?" If yes, write to the artifact's `evals/scenarios.md` (or append for prompts). If no, skip.

## HALT conditions

Report to chat (no file). Summarize decisions-so-far, unresolved questions, suggested next steps.

1. Stated intent contains contradictions unresolved after 2 turns.
2. Output path occupied, overwrite not confirmed.
3. Scope creep request (e.g., "also deploy," "also write the downstream consumer").
4. 3 consecutive interview turns with no new material information.

## Binding authoring rules

Applied to every artifact produced:

- **Prime, don't teach.** State numeric contracts and decisions. Do not re-explain prompt engineering fundamentals to the model.
- **Single responsibility.** One artifact, one job. If scope splits, produce two artifacts or HALT.
- **Degrees of freedom match task fragility.** Heuristic tasks → principles. Fragile/destructive tasks → exact scripts or templates.
- **Positive instructions.** "Do X" over "don't do Y." Negative rules only for absolute prohibitions, always paired with "do Y instead."
- **Implementation intentions.** "When X, do Y" — not general rules.
- **Deterministic enforcement where possible.** Concrete checks (regex, schema, numeric contracts) beat vague prose.
- **Measurable uplift on Haiku.** Every skill/agent ships with ≥3 eval scenarios that would fail without the artifact.

## Repository layout (this skill)

- `SKILL.md` — this file.
- `references/{prompt,skill,agent,anti-patterns}.md` — loaded on demand per §3.
- `templates/{prompt.md, skill/, agent/}` — scaffolds to fill in.
- `examples/` — paired good+bad for each type.
- `evals/` — scenarios the user runs against produced artifacts.

## Pointer rules

- Do not load `references/*.md` for types other than the active one.
- Do not read `examples/*-bad*` unless generating the self-review or the user asks.
- Templates are copied and filled, not read wholesale into context.
