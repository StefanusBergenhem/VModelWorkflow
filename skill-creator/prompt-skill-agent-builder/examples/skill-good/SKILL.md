---
name: commit-message-writer
description: Writes conventional-commit-style git commit messages from a staged diff. Use when the user asks to write, generate, draft, or improve a git commit message, or says "commit this" after staging changes. Reads the staged diff, produces a subject line (≤72 chars, imperative mood, conventional-commit type prefix) and an optional body explaining the *why*. Flags diffs that span unrelated concerns and recommends splitting the commit.
---

# commit-message-writer

Produce a conventional-commit message for the currently staged changes.

## Flow

1. Read staged diff via `git diff --cached`.
2. Classify: single concern or multiple? If multiple, recommend `git reset` + per-concern staging before proceeding.
3. Infer type prefix: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`.
4. Draft subject: `<type>: <imperative summary>` ≤72 chars.
5. Draft body only if the *why* is non-obvious from the diff. Skip otherwise.
6. Emit to chat. User copies or runs `git commit -m`.

## Rules

- When the diff spans >1 concern, do not write a message — recommend splitting.
- When the diff is pure formatting, use `chore:` and a one-line subject, no body.
- When the diff touches tests only, use `test:`.
- When the *why* is obvious from the subject, omit the body.

## HALT conditions

1. No staged changes — report and exit.
2. Diff >1000 lines — recommend split or ask user to confirm before proceeding.
