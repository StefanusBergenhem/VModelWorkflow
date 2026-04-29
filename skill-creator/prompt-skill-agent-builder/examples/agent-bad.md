---
name: super-helper
---

# super-helper

This agent helps with all your dev tasks. It can review code, fix bugs, write tests, refactor, deploy, and more. Just tell it what you need.

Think step by step about the problem. Be thorough. Don't make mistakes. Try your best.

Keep working on the problem until it's solved. If something doesn't work, try again.

Tools: all of them.

## What's wrong

- **No model or effort setting.**
- **Multiple responsibilities** — review, fix, test, refactor, deploy. Split into focused agents.
- **"Helps with all your dev tasks"** — no single-responsibility boundary.
- **Prescriptive CoT** — "think step by step" on a modern model.
- **Vague adjectives** — "thorough," "best."
- **Negative-only** — "don't make mistakes" with no positive counterpart.
- **"Keep working until solved"** — no max-attempts, infinite loop risk.
- **"Try again"** — no retry discipline, no variation requirement.
- **No HALT conditions.**
- **No handover artifacts** — entry and exit are unstructured.
- **"Tools: all of them"** — wildcard allowlist, no justification, massive blast radius.
- **No autonomy scope** — destructive actions not gated.
- **No context discipline** — will fill the window and fail.
- **No done-signal** — cannot distinguish "succeeded" from "ran out of tries."
