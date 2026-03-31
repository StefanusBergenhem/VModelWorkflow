# Meta-Skills: Skills for Creating Skills, Agents, and Commands

Sources: Web search, GitHub (fetched 2026-03-31), Claude Code docs, awesome-claude-code repo

---

## What Are Meta-Skills?

Meta-skills are skills/agents/commands that help you:
1. **Create** new skills, agents, commands
2. **Validate** existing skill files
3. **Test** skill quality and reliability
4. **Organize** and manage skill libraries
5. **Bootstrap** agent workflows from scratch

---

## Meta-Skills Available in Claude Code (Built-in)

### `skill-creator` (Already installed)
Purpose: Create new skills, modify and improve existing skills, measure skill performance.
Capabilities:
- Create skill from scratch
- Update or optimize existing skill
- Run evals to test a skill
- Benchmark skill performance with variance analysis

### `find-skills` (Already installed)
Purpose: Helps discover and install agent skills.
Use when: Looking for a skill that can do X, asking "how do I do X".

### `/agents` command (Built-in)
Interactive interface for managing subagents:
- View all subagents (built-in, user, project, plugin)
- Create new subagents (guided or Claude-generated)
- Edit existing subagent configuration
- Delete custom subagents

---

## Community Meta-Skills

### `agnix` (agent-sh)
Source: https://github.com/hesreallyhim/awesome-claude-code → agent-sh
Purpose: Comprehensive linter for Claude Code agent files.
Validates: CLAUDE.md, AGENTS.md, SKILL.md, hooks, MCP configuration, and more.
**High value for us**: Can validate our Pillar 3 skill files during development.

### `ContextKit` (FlineDev/NeoLabHQ)
Source: Context Engineering Kit in awesome-claude-code
Purpose: Transform Claude Code into a proactive development partner via structured methodology.
Covers: Advanced context engineering techniques, minimizing token footprint.
**Relevant**: For designing skills that work efficiently with smaller LLMs.

### `TÂCHES Claude Code Resources` (glittercowboy)
Includes: Meta-skills/agents like `skill-auditor` for workflow adaptation.
**Relevant**: Skill auditing pattern — validates that skills are well-formed and effective.

---

## Meta-Agents in HumanLayer Repo

HumanLayer uses specialized read-only agents as meta-infrastructure:

### `codebase-locator`
The "Super Grep/Glob/LS" — for efficiently finding files during skill development.
Pattern: When building a skill for a codebase, first run locator to understand the file structure.

### `web-search-researcher`
For looking up modern information during skill design.
Pattern: When skill needs to reference external standards (DO-178C, EARS), use researcher to get current details before embedding in skill.

---

## Meta-Agent Patterns

### Pattern 1: Agent-Creates-Agent
Some orchestration frameworks use an agent to generate skill files. Risks:
- Generated prompts may be vague
- No validation of generated skill quality
- Can create circular dependencies

**Recommendation**: Use `skill-creator` for initial generation, but always review the output. Don't auto-deploy generated skills.

### Pattern 2: Skill Linter (agnix pattern)
Run a validation agent over skill files to check:
- Frontmatter completeness (name, description required)
- Description quality (specific enough for auto-invocation decisions)
- Tool access appropriate for skill purpose
- SKILL.md length (<500 lines recommended)
- Supporting files referenced correctly

### Pattern 3: Skill Testing
HumanLayer's approach: Create a test scenario → Run skill → Validate output schema → Compare to expected.
Claude Code docs note: "Description not specific enough" is the most common skill failure.

---

## Recommended Skills to Install

Based on research, here are skills to evaluate for installation:

### High Priority

| Skill | Reason | Source |
|-------|--------|--------|
| `agnix` | Validate our Pillar 3 skill files | awesome-claude-code → agent-sh |
| `tdd` (already installed) | Our skills must be TDD-aligned | Built-in |
| `skill-creator` (already installed) | Scaffold new skills | Built-in |
| `wf-skill-build/review` (already installed) | Pipeline pattern reference | Built-in |

### Medium Priority (Evaluate)

| Skill | Reason | Source |
|-------|--------|--------|
| Trail of Bits Security Skills | Pattern for adversarial review craft | VoltAgent/awesome-agent-skills |
| AB Method | Spec-driven workflow pattern (similar to DRTDD) | awesome-claude-code |
| RIPER Workflow | Research-Plan-Execute-Review phase structure | awesome-claude-code |
| Context Engineering Kit | LLM-tier efficiency techniques | awesome-claude-code |

### Low Priority (Reference Only)

| Skill | Reason | Source |
|-------|--------|--------|
| Agentic Workflow Patterns | Mermaid diagrams, orchestration patterns | awesome-claude-code |
| Superpowers | Planning/reviewing/testing bundle | awesome-claude-code |

---

## Our Own Meta-Infrastructure Needs

For building Pillar 3, we should create:

### 1. `validate-skill` (internal meta-skill)
Check that a Pillar 3 skill file is well-formed:
- Frontmatter complete
- Description specific enough
- Output format explicitly defined
- Example output included
- Schema version referenced
- Within 500-line limit

### 2. `test-skill` (internal meta-skill)
Run a skill against a test scenario and validate:
- Output matches expected schema
- Required fields present
- Enum values valid
- No fabricated content in structured fields

### 3. Skill development process (not a skill, a CLAUDE.md rule)
When creating a new Pillar 3 skill:
1. Define what artifact it produces (Pillar 1 schema)
2. Write `validate-skill` test first (red)
3. Write skill body (green)
4. Validate with `agnix` equivalent
5. Test against pilot codebase scenario

---

## Bootstrapping Strategy for Pillar 3

The chicken-and-egg problem: we need skills to build skills.

**Resolution**: Use `skill-creator` (built-in) to scaffold each craft skill, then:
1. Review and refine the generated SKILL.md
2. Add Pillar 1 schema reference (what artifact does this produce)
3. Add example output section
4. Validate with agnix
5. Test against a pilot scenario

This is DRTDD applied to skill development:
```
REQUIRE (what artifact schema does this produce?)
DESIGN  (what craft knowledge goes into this skill?)
TEST    (what does a good vs bad output look like?)
IMPLEMENT (write the SKILL.md)
REFACTOR (crisp, unambiguous, model-tier compatible)
VERIFY  (does it pass agnix? does it produce valid artifacts?)
```
