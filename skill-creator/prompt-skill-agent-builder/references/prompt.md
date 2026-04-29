# Prompt reference

A prompt is a single block of instruction text. No frontmatter, no file structure, no discovery mechanism. One-shot or paste-into-chat usage.

## Signal table (type mismatch check)

User said "prompt." Check for ≥2 contradicting signals:

| Signal present | Points to |
|---|---|
| Reused across sessions by triggering on a description | skill |
| Requires discovery/auto-loading | skill |
| Central use of tools | agent |
| Autonomous loop / multi-step self-directed execution | agent |
| Termination or handover contract | agent |
| Bundled reference files or templates needed | skill |

If ≥2 of the above are present, raise: "you described <signals> — that's a <type>, not a prompt. Proceed as <type> or override?"

## Mandatory decisions (dependency order)

1. **Target model.** Which model will run this? (Opus/Sonnet/Haiku, which version.) *Default: ask; Haiku if unstated — forces the prompt to be clearer.*
2. **One-shot or templated?** Is this a fixed prompt, or a template with variable slots? *Default: one-shot; upgrade to template only if user names slots.*
3. **Role/persona.** Does the task need a persona? *Default: none, unless tone/expertise is load-bearing for output quality.*
4. **Context grounding.** What reference material does the model need inline, and where does it come from? *Default: inline only if small and static; otherwise describe the slot.*
5. **Task statement.** One sentence, verb-first, naming the exact deliverable. *Default: draft one; have user accept/override.*
6. **Output format.** Explicit structure: JSON schema, bullet shape, length, tone. *Default: specify; never leave implicit.*
7. **Examples (few-shot).** 0, 1, or 3? *Default: 0 unless the format is non-obvious; 3 if format is fragile; never >3.*
8. **Chain-of-thought.** Needed? *Default: no explicit CoT on Opus 4.6/4.7 (adaptive thinking handles it); add only if target is Haiku AND reasoning is the bottleneck.*
9. **Hallucination guards.** Is factual grounding required? *Default: allow "I don't know," require quote-before-answer only for long-document tasks.*
10. **Length target.** Token/word bound. *Default: specify a range (e.g., "3–5 sentences"); never "brief."*

## Creating

1. Fill `templates/prompt.md` using interview answers.
2. Run self-review (`references/anti-patterns.md`, prompt section).
3. Emit to chat. If user requested a save path, write the file.

## Editing

1. Read the existing prompt text the user supplies or points at.
2. Map current content against the 10 mandatory decisions. Flag missing, vague, or contradictory answers.
3. Interview only on flagged items.
4. Propose changes as a diff (old → new), not a full rewrite.

## Prompt-specific anti-patterns

- "Brief" / "detailed" / "good" without numeric bounds.
- Negative-only instructions ("don't hallucinate") without positive counterpart.
- Multiple tasks in one prompt (decompose).
- Examples contradicting the stated format.
- Explicit CoT scaffold on a 4.6/4.7 model (causes overthinking).
- Prefill patterns (deprecated on 4.6+; use Structured Outputs).
