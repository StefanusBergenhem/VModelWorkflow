---
name: claude-git-helper
description: Helps with git stuff.
---

# claude-git-helper

This skill helps you with git. It can do commits, branches, merges, rebases, cherry-picks, resolving conflicts, and also helps write good commit messages. You should use it whenever you're working with git.

## How to write good commit messages

A good commit message should be clear and concise. Think step by step about what changed. Don't be vague. Don't hallucinate. Make sure to summarize the changes well.

As of early 2025, conventional commits are the standard. The new `git commit --ai` feature integrates with this skill.

You could use `feat:`, `fix:`, `refactor:`, or `chore:`. Or you could use the older Angular convention. Or you could write freeform — whatever the team prefers.

...

(500 more lines about branching strategies, merge conflict resolution, rebase workflows, etc.)
```

## What's wrong

- **Frontmatter name contains "claude"** — violates naming rules.
- **Description is vague** — "helps with git stuff." No trigger keywords.
- **Description missing *when*** — only states *what*.
- **Multiple responsibilities** — commits, branches, merges, rebases, cherry-picks, conflicts, messages. Should be split into single-responsibility skills.
- **"Helps with"** — vague verb.
- **Prescriptive CoT** ("think step by step") on a task that doesn't need it.
- **Negative-only rules** ("don't be vague," "don't hallucinate") with no positive counterpart.
- **Time-sensitive phrasing** ("as of early 2025," "the new `git commit --ai` feature").
- **Alternatives dump** (3 commit conventions offered, no default).
- **500+ lines in SKILL.md** — progressive disclosure failure; should move detail to references.
- **No HALT conditions.**
- **No eval scenarios / no measurable uplift claim.**
