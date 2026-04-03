---
name: develop-code
description: >
  Implement code from a design with V-model quality: design-before-code discipline, quantified
  complexity limits, strict error handling, and clean architecture boundaries. Use this skill when
  the user asks to implement a feature, write production code, implement a design, build a module,
  or code a component. Also use when the user says "implement this", "write the code for this
  design", "build this module", or mentions implementation, coding, or development of a unit or
  component. Do NOT use for test code — use derive-test-cases instead.
user-invocable: true
---

# Develop Code

Implement production code from a design document. The code must be correct, maintainable, and
production-quality.

## Input

A **design document** describing what to implement. Can be any format. Look for:

- **Purpose** — what the unit does and why it exists
- **Interfaces** — inputs, outputs, types, constraints
- **Behavior** — rules, conditions, expected results
- **Error handling** — what happens on invalid input or failures
- **Configuration** — tuneable parameters with defaults
- **Constraints** — performance, threading, memory, real-time requirements

If the design is too vague to implement unambiguously, HALT and ask.

Also check for **existing code context**: if implementing into an existing codebase, read nearby
files first and match their conventions (naming, structure, patterns, error handling style).

## Rules

These are the specific practices that matter — the things that change code quality when followed
and cause defects when ignored.

### 1. Implement the design, not more

Write exactly what the design specifies. No extra features, no "while I'm here" improvements,
no speculative abstractions. Every line of code must trace to a design element.

Untested code that nobody asked for is a liability, not a feature.

### 2. Complexity limits

| Metric | Limit | Why |
|--------|-------|-----|
| Function length | 20 lines target, 50 hard max | Beyond 50, too many paths to hold in your head |
| Cyclomatic complexity | 10 per function | Each branch is a test case you need and a path where bugs hide |
| Nesting depth | 3 levels max | Deep nesting = extract a function |
| Parameters | 3 target, 5 max | More = introduce a parameter object |
| File length | 300 lines target | One concept per file |

If you can't meet these limits, the design probably needs decomposition — that's a HALT condition,
not something to push through.

### 3. Error handling — the non-negotiable rules

These rules exist because error handling is where the most production bugs hide, especially in
AI-generated code:

- **Never return null.** Use Optional, empty collections, or Null Object pattern. Every null
  return is a crash waiting to happen downstream.
- **Never swallow exceptions.** An empty catch block hides bugs. At minimum: log and re-throw.
- **Fail fast at boundaries.** Validate inputs at the public API surface. Don't let invalid data
  propagate through multiple layers.
- **Error messages include context.** What operation, what input, what was expected. Not just
  "Error" or "Invalid input".
- **Resource cleanup is mandatory.** Use try-with-resources, defer, RAII — whatever the language
  provides. No leaked handles, connections, or streams.

### 4. Architecture boundaries

Business logic must not depend on infrastructure. This is the single most important architectural
rule — it enables testing, enables change, and maps cleanly to V-model traceability.

- Domain/business logic: zero imports of database, HTTP, filesystem, framework packages
- Infrastructure implements interfaces defined by the domain, not the other way around
- Each layer calls only the layer below/inside it
- No circular dependencies between packages

If the design doesn't specify architecture layers, apply this default:
- **Domain** — entities, value objects, business rules (pure, no I/O)
- **Application** — use cases, orchestration (calls domain, uses interfaces for I/O)
- **Infrastructure** — adapters that implement interfaces (DB, HTTP, files)

### 5. Naming

Names are the primary way both humans and AI agents understand code. Bad names cause
misunderstanding, which causes bugs.

- Names reveal intent: `calculateMonthlyFuelConsumption()`, not `calc()`
- One word per concept across the codebase — don't mix `get`/`fetch`/`retrieve`
- Use domain vocabulary — the code should read like the domain, not like CS jargon
- Classes are nouns, methods are verbs

### 6. No dead code

Every function, every branch, every variable must be reachable and used. Delete unused code —
version control remembers.

Don't comment out code. Don't keep "just in case" functions. Don't leave TODO stubs for features
the design doesn't specify.

## Self-check before delivering

For each function you wrote:

1. **Trace check:** Does it map to a specific design element?
2. **Delete test:** Would removing this function break something the design requires?
3. **Complexity check:** Under 50 lines? Cyclomatic complexity under 10? Nesting under 4?
4. **Error check:** Are all error paths handled? Any null returns? Any empty catches?
5. **Boundary check:** Does domain code import infrastructure? Does it depend on a framework?
6. **Name check:** Would someone unfamiliar with the code understand each name?

Read `references/code-quality-checks.md` for the detailed review checklist.

## Output

1. **Source code file(s)** — production-quality, compilable code

## HALT conditions

Stop and ask the user if:
- The design is too vague to implement unambiguously
- Meeting complexity limits requires decomposing the design differently
- You need to touch files or modules outside the design's scope
- The design has contradictions or impossible constraints
- You're unsure about language, framework, or project conventions
