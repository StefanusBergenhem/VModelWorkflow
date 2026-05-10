---
id: src-zakariasson-clis-for-agents-2026
title: "CLI design patterns for AI agents (Zakariasson tweet/thread)"
type: source
source_type: article
authors: ["Zakariasson, Eric"]
year: 2026
publisher: "X (formerly Twitter), @ericzakariasson"
url: https://x.com/ericzakariasson/status/2036762680401223946
raw_path: raw/articles/zakariasson-clis-for-agents-2026.md
peer_reviewed: false
primary: true
confidence: low
depth: shallow
source_class: primary
status: draft
last_updated: 2026-04-25
sources: []
provenance_note: "User-supplied text. Direct WebFetch returned 402; nitter mirrors failed. Verbatim verification against the live X post is not possible. Treat any direct quotes from this source as user-attested rather than fetch-verified."
---

# CLI design patterns for AI agents (Zakariasson tweet/thread)

> **Summary.** A practitioner micro-thread arguing that most existing CLIs assume a human at the keyboard, and that AI agents fail on them in predictable ways: interactive prompts, missing flag forms, prose-heavy help, positional-arg gymnastics, hanging on missing inputs, non-idempotent operations. The post lists ten design patterns to make CLIs agent-friendly: non-interactive flag-driven invocation, lazy/discoverable help, example-rich `--help`, flags-and-stdin everywhere, fail-fast actionable errors, idempotency, `--dry-run`, `--yes`/`--force`, predictable resource+verb command structure, and structured machine-readable output. The framing claim is that this is mostly making explicit "what humans figured out implicitly." Single-author opinion piece; no citations, no measurements, no comparisons.

## Key claims

1. **Most CLIs were designed assuming a human at the keyboard.** Agents fail on these CLIs in characteristic ways: stuck on interactive prompts, parsing prose-only help. The framing is that the CLI-vs-agent ergonomic gap is real and widespread. [tweet ¶1]

2. **Make it non-interactive: every input passable as a flag.** Mid-execution prompts ("Which environment? (use arrow keys)") block agents. Interactive mode should be a fallback when flags are absent, not the primary path. Worked example: `mycli deploy` → blocks; `mycli deploy --env staging` → works. [tweet ¶2]

3. **Don't dump all docs upfront — let agents discover incrementally.** An agent runs `mycli`, sees subcommands, picks one, runs `mycli deploy --help`, gets what it needs. The reasoning is explicit: "No wasted context on commands it won't use." This is a context-window-economics argument made by a CLI builder. [tweet ¶3]

4. **`--help` should include examples; examples do the work.** Every subcommand gets `--help`; every `--help` includes example invocations. The author's claim: "An agent pattern-matches off `mycli deploy --env staging --tag v1.2.3` faster than it reads a description." Example beats prose for agent consumption. [tweet ¶4]

5. **Accept flags AND stdin for everything.** Agents think in pipelines and want to chain commands (`cat config.json | mycli config import --stdin`; `mycli deploy --env staging --tag $(mycli build --output tag-only)`). No "weird positional argument orders," no interactive fallbacks for missing values. [tweet ¶5]

6. **Fail fast with actionable errors — not interactive hangs.** A missing required flag should error immediately with the correct invocation embedded in the message, not drop into a prompt. "Agents are good at self-correcting when you give them something to work with." [tweet ¶6]

7. **Make commands idempotent.** "Agents retry constantly. Network timeouts, context getting lost mid-task. Running the same deploy twice should return 'already deployed, no-op', not create a duplicate." Idempotency is presented as a property required by agent retry behaviour, not just a general best practice. [tweet ¶7]

8. **`--dry-run` for destructive actions.** Agents should be able to preview destructive commands before committing. "Let them validate the plan, then run it for real." Worked example shows enumerated effects ("Stop 3 running instances / Pull image / Start 3 new instances") in the dry-run output. [tweet ¶8]

9. **`--yes` / `--force` to bypass confirmations.** "Make the safe path the default but allow bypassing." Humans get "are you sure?"; agents pass `--yes`. [tweet ¶9]

10. **Predictable resource+verb command structure.** "If an agent learns `mycli service list`, it should be able to guess `mycli deploy list` and `mycli config list`." Pick one pattern and apply it everywhere — this is a generalization story specifically tied to how agents extrapolate from observed examples. [tweet ¶10]

11. **Return structured data on success; emojis are unnecessary.** Worked example shows key-value lines: `deployed v1.2.3 to staging / url: ... / deploy_id: dep_abc123 / duration: 34s`. The implicit claim is that machine-parseable output beats decorative output. [tweet ¶11]

12. **Framing claim: this is mostly making explicit what humans figured out implicitly.** The closing line of the post — agent-friendly CLI design is about codifying human-tacit conventions into explicit affordances rather than inventing new patterns. [tweet ¶12]

## References cited by this source

None. The post makes no citations to research, blog posts, vendor documentation, or other practitioner sources. All claims are the author's own assertions presented as personal observation.

## What this source is silent on

- **Empirical backing.** No measurements, A/B comparisons, success-rate data, or even named anecdotes. Every claim is asserted.
- **Which agent platforms were tested.** "Agents" is used generically — no statement on whether the observed failure modes were measured on Claude, GPT, Cursor, Aider, custom harnesses, or anything else.
- **Whether the failure modes are model-tier specific.** Smaller models presumably handle interactive prompts even worse than larger ones, but the post does not address this.
- **Any treatment of MCP, function-calling, or structured tool interfaces** as alternatives to CLI ergonomics. The whole framing is "fix the CLI" — it does not engage with the question of whether CLIs are even the right interface for agents in the first place.
- **How agent-friendly CLI design interacts with traditional Unix CLI conventions** (e.g., POSIX flag parsing, the do-one-thing principle, exit codes). Most of these recommendations are consistent with classical Unix style — the post does not name this lineage.
- **Cost/effort of retrofit.** No guidance on how to migrate an existing interactive-first CLI to flag-first.
- **What "predictable resource+verb" should be when conventions clash** (e.g., kubectl-style `<verb> <resource>` vs. AWS-CLI-style `<service> <verb>`). The post asserts "pick a pattern" without engaging with the pre-existing ecosystem patterns.
- **Authority/identity of the author beyond the handle.** No biographical claim is made in the post itself; the codex does not assert what organization Zakariasson is affiliated with.

## Confidence assessment

Practitioner micro-thread on X by a single author, no peer review, no citations, no measurements, ~600 words. The claims are coherent and consistent with broader practitioner literature on context-window economics, progressive disclosure, and LLM tool-use ergonomics, but no individual claim is independently validated within this source. The piece is useful as a **named, articulated checklist** of CLI affordances that agents need — particularly the tying of idempotency-to-retry-behaviour and example-rich-help-to-pattern-matching, which are mechanism-level claims rather than just style advice. Confidence: **low**. Claims from this source should be cited as practitioner observation, not as established fact, and should be marked `[unverified]` or paired with a corroborating source for any load-bearing use.

**Provenance caveat:** The raw text was pasted into the conversation by the human user on 2026-04-25 because direct fetch of the X.com post returned HTTP 402 (X authentication wall) and Nitter mirrors failed. Verbatim verification against the live X post is not possible from within the codex's verification protocol. The raw file's frontmatter records this honestly. Treat any direct quotes from this source as user-attested rather than fetch-verified.

## See also

- [Context Window Management](../concepts/concept-context-management.md) · [[concept-context-management|Context Window Management]] — progressive-disclosure / on-demand-context theme
- [Model Context Protocol (MCP)](../tools/tool-mcp.md) · [[tool-mcp|Model Context Protocol]] — agent-native alternative to retrofitted CLIs
- [Agent-ergonomic tool design (open question)](../questions/q-agent-ergonomic-tool-design.md) · [[q-agent-ergonomic-tool-design|Agent-ergonomic tool design]]
