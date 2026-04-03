# AI-Assisted Development: Practices for Agents and Humans Working Together

This document covers what works and what doesn't when AI agents write code. It's relevant both for humans supervising AI agents and for the agents themselves.

---

## The Reality of AI-Generated Code (2025-2026 Data)

The data is substantial and sobering:

- **AI-created PRs have 75% more logic and correctness errors** than human-written ones (Stack Overflow, 2026)
- **AI generates 1.7x as many bugs as humans** across 470 studied GitHub repositories (Stack Overflow, 2026)
- **Google's DORA Report (2025):** 90% increase in AI adoption correlated with 9% increase in bug rates, 91% increase in code review time, 154% increase in PR size
- **Developer trust:** Only 3% of developers report high trust in AI output accuracy (Stack Overflow Developer Survey, 2025)
- **Security:** AI-generated code includes vulnerabilities at 1.5-2x the rate of human code

**The pattern:** AI agents are fast but careless. They produce plausible-looking code that passes cursory review but harbors subtle logic errors, security vulnerabilities, and architectural problems. This makes **rigorous review and testing non-negotiable** — not optional, not reduced because "the AI is good."

---

## Common Mistakes AI Agents Make

### Logic and Correctness

| Mistake | Description | Example |
|---------|-------------|---------|
| **Plausible but wrong** | Code looks correct but has subtle logic errors | Off-by-one in range check, wrong comparison operator (`<` vs `<=`) |
| **Untested edge cases** | Happy path works, boundaries don't | Null inputs, empty collections, integer overflow, concurrent access |
| **Hallucinated APIs** | Invents methods or config options that don't exist | `list.removeLast()` on a Java version that doesn't have it |
| **Stale knowledge** | Uses deprecated APIs or removed features | Deprecated framework methods from training data |

### Architectural Problems

| Mistake | Description | Impact |
|---------|-------------|--------|
| **No architectural awareness** | Defaults to common patterns regardless of project context | Spring Boot patterns in a plain Java project |
| **Copy-paste patterns** | Repeats training data patterns even when they don't fit | Over-engineered microservice patterns in a monolith |
| **Inconsistent style** | Internally consistent but clashes with existing codebase | Different naming, different error handling, different layering |
| **Over-abstraction** | Deeply nested abstractions for simple tasks | Interface + abstract class + concrete class for a function that's called once |

### Testing Failures

| Mistake | Description | Why It's Dangerous |
|---------|-------------|-------------------|
| **Tautological tests** | Tests verify the implementation does what it does | Tests pass but prove nothing about correctness |
| **Missing edge cases** | Only happy-path tests | The bugs that reach production are in the edge cases |
| **Brittle tests** | Tests internal details instead of behavior | Break on every refactoring, providing no safety net |
| **Over-mocking** | Mocks everything, tests mock wiring | Verifies the test setup, not the business logic |

### Security

| Mistake | Risk |
|---------|------|
| Hardcoded secrets | API keys, passwords in source code |
| Insecure defaults | Missing input validation, weak encryption |
| Dependency confusion | Wrong package names, outdated vulnerable versions |
| Missing error handling | Happy path only, exceptions swallowed |

---

## Best Practices for AI-Assisted Development

### 1. Specification First

**Write a clear spec before asking the agent to code.** Include:
- Goals and acceptance criteria
- Technical constraints (language, framework, dependencies)
- Interface contracts (function signatures, input/output types)
- Non-functional requirements (performance, concurrency, error handling)

**Define the interface contract first.** Give the agent the signatures, types, and expected behavior. Then let it implement. This is how V-model development works: design before code.

**Test-first (TDD/DRTDD):** Have the agent generate tests from acceptance criteria BEFORE implementation. Then implement until tests pass. This inversion works remarkably well with agents — it gives them a clear success criterion.

### 2. Review Every Line

**Never merge AI-generated code without reviewing it.** Treat every AI output like a PR from a talented but careless junior developer.

**Review focus areas:**

| Area | What to Check |
|------|--------------|
| Logic correctness | Walk through with specific inputs. Does it handle boundaries? |
| Error handling | Are all failure paths covered? Any swallowed exceptions? |
| API usage | Do the APIs, methods, and configs actually exist in project dependencies? |
| Security | Input validation? Authentication checks? Authorization boundaries? |
| Architecture compliance | Does it respect layer boundaries? No infrastructure in domain? |
| Naming and style | Consistent with existing codebase? |

### 3. Incremental Generation

**Small tasks, not big features.** Generate one function, one class, one test at a time. Verify each before proceeding.

**Build complexity incrementally.** Don't ask the agent to handle multiple abstraction layers simultaneously. Start with the domain model, verify it, then add the use case, verify it, then add the adapter.

**One concern per prompt.** Mixing implementation, testing, documentation, and refactoring in one prompt degrades quality on all of them.

### 4. Context Management

**Provide relevant context, not everything.** The agent needs:
- The interface it's implementing
- The types it's using
- The conventions it should follow
- Example code to match style

It does NOT need the entire codebase.

**Keep project conventions documented.** A CONVENTIONS.md or CLAUDE.md that describes naming, architecture, error handling patterns, and prohibited practices. The agent reads these to maintain consistency.

**Reference existing code as examples.** "Follow the pattern in UserService.java" is more effective than describing the pattern in prose.

---

## Structuring Code for AI Maintainability

Code that's good for humans is good for AI agents — but AI amplifies the consequences of both good and bad structure.

### File Organization

| Guideline | Target | Why |
|-----------|--------|-----|
| One concept per file | One class, one interface, one enum | AI accuracy degrades with mixed concerns |
| Small files | Under 200-300 lines | AI context windows are large but accuracy degrades with size |
| Flat-ish directories | 2-3 levels deep | Deep nesting obscures location |
| Colocate related files | Tests next to source | Reduces context the agent needs to load |

### Function Design for AI

| Guideline | Target | Why |
|-----------|--------|-----|
| Small functions | 5-20 lines | AI generates better modifications to small, focused functions |
| Explicit types | Full type signatures on all public methods | AI relies heavily on types to understand behavior |
| No hidden state | No global/static mutable state | Functions with hidden state are nearly impossible for AI to reason about |
| Low complexity | Cyclomatic complexity under 10 | Deeply nested control flow increases AI error rates significantly |

### Naming for AI Context

**Names are the primary context signal for AI.** The agent uses names to understand what code does before reading the body.

- `calculateMonthlySalesTax(order)` gives the agent everything. `calc(o)` gives it nothing.
- Consistent vocabulary: if you call it `User` in one place, don't call it `Account`, `Member`, and `Person` elsewhere.
- Method names describe behavior, not implementation: `persistUser()` not `writeToPostgres()`.

### Documentation for AI

| Document | Purpose | Keep Updated |
|----------|---------|-------------|
| README per module/package | AI loads these for context | Yes — stale READMEs mislead AI |
| Interface contracts (Javadoc on interfaces) | AI uses these to understand expected behavior | Yes |
| Architecture documentation | Shows layers and allowed dependencies | Yes |
| CONVENTIONS.md | Project-specific rules AI must follow | Yes |

---

## Anti-Patterns in AI-Generated Code

Watch for these during review — they appear frequently in AI output:

| Anti-Pattern | What It Looks Like | Fix |
|---|---|---|
| **Plausible Hallucination** | Uses APIs that don't exist in your dependency versions | Verify against actual docs |
| **Tautological Tests** | Tests verify what the implementation does, not what it should do | Derive tests from requirements, not implementation |
| **Over-Mocking** | Every dependency mocked, tests verify mock wiring | Use fakes for complex deps, real objects for simple ones |
| **Shotgun Abstraction** | Premature interfaces, factories for simple cases | YAGNI — abstract when a second consumer appears |
| **Style Inconsistency** | AI follows training patterns, not project conventions | Provide conventions, linter configs, example code |
| **Copy-Paste Scaling** | Duplicates code instead of extracting reusable components | Explicitly request refactoring after initial implementation |
| **Happy Path Only** | Error handling, edge cases are missing | Require explicit error handling in spec |
| **Excessive Comments** | Comments on every line (trained on tutorial code) | Strip "what" comments, keep only "why" |
| **God Method** | One long method instead of composed functions | Constrain function length in instructions |
| **Dependency Confusion** | Wrong package names, outdated versions | Verify every added dependency |

---

## Existing Codebases vs. Greenfield

### Greenfield Projects

- AI agents excel at scaffolding: project structure, boilerplate, initial patterns
- **Risk:** AI over-scaffolds. Adds every feature from tutorials (CORS, metrics, health checks) whether needed or not. YAGNI applies.
- **Best practice:** Define conventions BEFORE the agent starts. Once AI establishes a pattern, it propagates everywhere.
- Start minimal. Add infrastructure as requirements demand it.

### Existing Codebases

- AI agents struggle more — they must understand implicit context and conventions.
- **Read before write:** Always have the agent read relevant existing code before generating new code.
- **Provide architecture documentation:** Without it, AI introduces conflicting patterns.
- **Incremental changes:** Small, focused modifications are far more reliable than large refactoring.
- **Module-by-module:** Legacy codebases should be modernized one module at a time.
- **Run existing tests** after every AI change to catch regressions.

### The Rewrite Temptation

AI agents, when shown legacy code, often suggest or attempt a full rewrite. This is almost always wrong:
- Rewrites discard embedded domain knowledge
- Rewrites invalidate all existing tests
- Rewrites introduce new bugs while fixing old ones

**The right approach:** Incremental refactoring, guided by tests, one smell at a time.

---

## Context Window Management

The context window is the AI agent's working memory. Everything in it competes for attention.

### Practical Guidelines

| Aspect | Guideline | Rationale |
|--------|-----------|-----------|
| File size | Under 300 lines | Accuracy degrades with size |
| Function length | 5-20 lines (max 50) | Modification accuracy drops beyond 50 |
| Cyclomatic complexity | Under 10 | Nested control flow confuses AI |
| Type signatures | Explicit everywhere | Types reduce need to read function bodies |
| Self-documenting names | Always | Reduces context needed to understand intent |
| Interface size | 3-5 methods per interface | Easier to implement correctly |
| Coding guidelines | Constraints, not prose | Long instructions waste context |

### Reducing Context Needs

- **Strong typing reduces context.** The type signature tells the AI what a function does.
- **Self-documenting names reduce context.** The agent doesn't need to read the body to understand `calculateShippingCost(order, destination)`.
- **Small interfaces reduce context.** An interface with 3 methods is easier to implement correctly than one with 30.
- **Colocated tests reduce context.** The agent can read the test to understand expected behavior without loading distant files.

---

## The V-Model Connection

All of these practices aren't just "nice engineering" — they directly support V-model compliance:

| Practice | V-Model Benefit |
|----------|----------------|
| Specification first | Design-before-code ordering (ASPICE SWE.3 requirement) |
| Small, focused functions | Clean design-to-code traceability |
| Interface-driven design | Clear architectural boundaries for review |
| Incremental generation | Verifiable at each step |
| Review every line | Code review evidence (DO-178C Table A-5, ISO 26262 Table 9) |
| Test-first | Requirements-based testing (DO-178C 6.4.2) |
| Explicit error handling | Robustness verification (DO-178C 6.4.2.2, IEC 62304 5.5.4) |
| No dead code | DO-178C dead code requirement |

AI-assisted development done right produces *more* V-model evidence, not less — because the agent generates tests, traces, and verification artifacts as part of its normal workflow.

---

## Sources

- Stack Overflow Blog, "Are bugs and incidents inevitable with AI coding agents?" (2026)
- Stack Overflow Blog, "AI can 10x developers...in creating tech debt" (2026)
- Google DORA Report (2025)
- Anthropic, "Building Effective Agents" (2025)
- Anthropic, "Effective Harnesses for Long-Running Agents" (2025)
- Stack Overflow Blog, "Building Shared Coding Guidelines for AI (and People Too)" (2026)
