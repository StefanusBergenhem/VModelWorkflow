# Implementation Best Practices (Human Reference)

This directory contains verbose, educational documentation on software implementation — targeting human developers and AI agents who need to understand what "good code" means in a V-model context.

These documents combine three perspectives:
1. **What safety standards require** — DO-178C, ISO 26262, ASPICE, IEC 62304
2. **What the industry considers best practice** — Clean Code, SOLID, design patterns
3. **What works specifically for AI-assisted development** — patterns that help agents write better code

## Contents

- **coding-standards.md** — What coding standards are, why every V-model standard requires them, and how to define one for your project. Covers language subsets, complexity limits, naming conventions, and style guides.
- **clean-code-principles.md** — Core principles for writing maintainable code: naming, functions, error handling, classes, SOLID, DRY/KISS/YAGNI. With examples and rationale.
- **architecture-and-design.md** — Code-level architecture: separation of concerns, hexagonal architecture, interface-driven design, testability as a design constraint, cohesion and coupling.
- **ai-assisted-development.md** — Specific practices for AI agents writing code: common mistakes, structuring code for AI maintainability, context window management, review practices.
- **code-review-checklist.md** — A structured checklist for reviewing code against V-model and clean code criteria. Usable by humans and AI reviewers.

## Relationship to Agentic Skills

These are the "source of knowledge" documents. The corresponding agentic skills in `.claude/skills/` are distilled extractions optimized for LLM consumption. When updating, update the human version here first, then distill into the agent version.

## Research Backing

All content is backed by research in `research/implementation/`:
- `v-model-standards-implementation.md` — Standards requirements analysis
- `v-model-standards-unit-testing.md` — Standards testing requirements analysis
- `clean-code-best-practices.md` — Industry best practices compilation
