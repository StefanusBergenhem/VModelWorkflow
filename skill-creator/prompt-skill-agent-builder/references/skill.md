# Skill reference

A skill is a directory with `SKILL.md` + frontmatter + optional references/templates/scripts. Discovered by description-matching. Loaded on demand.

## Signal table (type mismatch check)

User said "skill." Check for ≥2 contradicting signals:

| Signal present | Points to |
|---|---|
| One-shot text, never reused | prompt |
| No discovery trigger — always explicitly invoked, single-session | prompt |
| Autonomous loop / multi-step self-directed execution | agent |
| Central use of tools with explicit allowlist | agent |
| Has a termination/handover contract | agent |
| Runs without user in the loop for >1 turn | agent |

If ≥2 present, raise: "you described <signals> — that's a <type>, not a skill. Proceed as <type> or override?"

## Mandatory decisions (dependency order)

1. **Single-responsibility boundary.** What is the one job? State it in one sentence. If two jobs emerge, split into two skills. *Default: have user state it; challenge if it contains "and."*
2. **Name.** ≤64 chars, lowercase + hyphens, no "anthropic"/"claude". Keyword-rich, gerund form preferred (`processing-pdfs` not `pdf-processor`). *Default: generate 3 candidates from the boundary statement; user picks.*
3. **Description.** ≤1024 chars, third-person, covers *what* + *when*, dense with trigger keywords users will actually say. *Default: draft from boundary + name; user accepts/overrides.*
4. **Discovery triggers.** List the user phrasings that should match this skill. Inform description wording. *Default: enumerate with user; require ≥3 distinct phrasings.*
5. **Degrees of freedom.** For each sub-task the skill handles: heuristic (principles) or fragile (exact script/template)? *Default: heuristic unless the task is destructive, ordering-dependent, or requires external-system correctness.*
6. **Reference structure.** Which content stays in SKILL.md, which moves to `references/*.md`? *Default: SKILL.md ≤500 lines; move anything type-specific, domain-specific, or >100 lines of detail.*
7. **Templates and examples bundled?** *Default: templates yes if the skill produces a structured artifact; paired good+bad examples yes if the skill teaches a style.*
8. **Scripts.** Does the skill need executable logic? *Default: no. Only add if the task is genuinely deterministic computation (lint, schema validation) that prose cannot enforce.*
9. **HALT conditions.** What makes this skill stop and hand back? *Default: require the user to name at least 2 conditions; propose irresolvable-contradiction and scope-creep as starters.*
10. **Eval scenarios.** 3+ scenarios where the skill should produce measurably better output than no-skill baseline on Haiku. *Default: draft 3 with user; scenarios must fail without the skill.*

## Creating

1. Fill `templates/skill/SKILL.md.tmpl` using interview answers.
2. Create `references/` only if decision 6 said so; populate from interview.
3. Bundle templates and examples per decision 7.
4. Create `evals/scenarios.md` from decision 10 if user accepted eval scaffold.
5. Run self-review.

## Editing

1. Parse existing `SKILL.md` + frontmatter + reference tree.
2. Map against the 10 mandatory decisions. Flag gaps.
3. Specifically check: description triggers, single-responsibility creep (has the skill accrued a second job?), reference files that are now >500 lines, time-sensitive phrasing, deprecated patterns (prefill, prescriptive CoT).
4. Interview only on flagged items.
5. Output as a diff tree (files changed, lines added/removed).

## Skill-specific anti-patterns

- Vague description ("helps with documents").
- Name includes "anthropic" or "claude".
- SKILL.md >500 lines (progressive disclosure failure).
- References nested >1 level deep (head-read risk).
- References >100 lines with no table of contents.
- Description missing either *what* or *when*.
- Multiple responsibilities ("and" in the boundary statement).
- Time-sensitive content ("as of 2025," "currently," "the new API") — move to an "old patterns" section or delete.
- Alternatives dumps ("you could also try X, Y, Z") — pick a default, offer one escape hatch.
- No eval scenarios / no measurable uplift claim.
