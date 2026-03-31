# HumanLayer Repo — .claude/ Workflow Analysis

Source: https://github.com/humanlayer/humanlayer/tree/main/.claude (fetched via gh API 2026-03-31)

---

## Directory Structure

```
.claude/
├── commands/          # 26 command files
├── agents/            # 6 specialized agent files
└── settings.json      # Settings
```

---

## Commands (26 total)

Full list:
- `ci_commit.md`, `ci_describe_pr.md`
- `commit.md`, `describe_pr.md`, `describe_pr_nt.md`
- `create_plan.md`, `create_plan_generic.md`, `create_plan_nt.md`
- `implement_plan.md`, `iterate_plan.md`, `iterate_plan_nt.md`
- `validate_plan.md`
- `create_worktree.md`
- `create_handoff.md`, `resume_handoff.md`
- `debug.md`
- `founder_mode.md`
- `linear.md`
- `local_review.md`
- `oneshot.md`, `oneshot_plan.md`
- `ralph_impl.md`, `ralph_plan.md`, `ralph_research.md`
- `research_codebase.md`, `research_codebase_generic.md`, `research_codebase_nt.md`

---

## Agents (6 total)

All defined as `.claude/agents/*.md`:
- `codebase-analyzer.md` — Analyzes HOW code works (Read, Grep, Glob, LS / sonnet)
- `codebase-locator.md` — Finds WHERE code lives (Grep, Glob, LS / sonnet)
- `codebase-pattern-finder.md` — Finds similar patterns/examples
- `thoughts-analyzer.md` — Analyzes research/planning documents
- `thoughts-locator.md` — Finds relevant documents
- `web-search-researcher.md` — Web research (WebSearch tools)

Each agent has:
- `name`, `description` frontmatter
- Explicit `tools` restriction (read-only for most)
- `model: sonnet`
- Clear single-responsibility prompt

---

## Key Command Deep-Dives

### `/create_plan` — The Core Planning Workflow

This is HumanLayer's most sophisticated command. Key patterns:

**Phase 1: Read Everything First**
```
- Read all mentioned files IMMEDIATELY and FULLY (no limit/offset)
- CRITICAL: DO NOT spawn sub-tasks before reading files in main context
- NEVER read files partially
```

**Phase 2: Spawn Parallel Research Agents**
```
- codebase-locator: find all relevant files
- codebase-analyzer: understand current implementation
- thoughts-locator: find existing research/plans
- Wait for ALL tasks to complete before proceeding
```

**Phase 3: Present Understanding + Ask Only What Code Can't Answer**
```
"Based on the ticket and my research, I understand we need X.
Questions that my research couldn't answer: [specific gaps]"
```

**Phase 4: Interactive Plan Structure Development**
```
Present outline → Get approval → Write details → Get review → Sync
```

**Output Format:**
```
thoughts/shared/plans/YYYY-MM-DD-ENG-XXXX-description.md
```

**Plan template includes:**
- Overview
- Current State Analysis
- Desired End State
- What We're NOT Doing (explicit scope exclusion)
- Implementation Approach
- Phases with both **Automated Verification** and **Manual Verification** criteria
- "Pause here for manual confirmation from the human before proceeding"

---

### `/implement_plan` — Disciplined Execution

Key patterns:
- Read plan completely, check for existing checkmarks (- [x])
- Update checkboxes in the plan as sections complete
- After automated verification → **PAUSE for human manual testing**:
  ```
  Phase [N] Complete - Ready for Manual Verification

  Automated verification passed: [list]
  Please perform manual verification: [list from plan]
  Let me know when testing is complete before I proceed to Phase [N+1].
  ```
- Do NOT check off manual items until human confirms
- If plan doesn't match reality → STOP and present the mismatch

---

### `/validate_plan` — Post-Implementation Verification

- Gathers evidence from git log, diff
- Validates against plan's success criteria
- Distinguishes automated vs. manual criteria

---

### `/create_handoff` — Cross-Session Continuity

Creates compact handoff document for agent → agent (or session → session) transfer:
```
thoughts/shared/handoffs/ENG-XXXX/YYYY-MM-DD_HH-MM-SS_description.md
```
Goal: compact and summarize without losing key context.

---

### `/resume_handoff` — Pick Up Where Left Off

- Reads handoff document FULLY
- Reads all linked research/plan documents
- Begins from documented next steps

---

### `/local_review` — Peer Code Review

- Parses `username:branchname` format
- Creates git worktree for isolation
- Copies Claude settings into worktree
- Runs setup
- **Isolation pattern**: reviewer works on isolated worktree, not main repo

---

### `/oneshot` — Autonomous Long-Running Task

```
1. Call /ralph_research with ticket number
2. Launch NEW session: humanlayer launch --model opus --dangerously-skip-permissions --title "plan ENG-XXXX" "/oneshot_plan ENG-XXXX"
```
**Key insight**: Uses `humanlayer launch` to spawn a completely new Claude Code session for long-running autonomous work.

---

### `/founder_mode` — Retroactive Ticketing

For experimental features implemented without proper process:
1. Get commit SHA
2. Read Linear command
3. Create Linear ticket retroactively
4. Create branch, cherry-pick commit, push
5. Create PR

---

## Specialized Agents Deep-Dive

### `codebase-analyzer`
```yaml
tools: Read, Grep, Glob, LS
model: sonnet
```
Role: "YOUR ONLY JOB IS TO DOCUMENT AND EXPLAIN THE CODEBASE AS IT EXISTS TODAY. DO NOT suggest improvements."
Returns: file:line references, data flow explanations.

### `codebase-locator`
```yaml
tools: Grep, Glob, LS  # No Read — only finding, not reading
model: sonnet
```
Role: Find WHERE code lives. Returns organized file lists by purpose.
Called with: "Super Grep/Glob/LS tool — use when you'd otherwise run these more than once."

### `web-search-researcher`
For information not in training data / modern/evolving topics.
Can be re-run with altered prompt if first result is unsatisfactory.

---

## Key Patterns Worth Adopting

### 1. Plan → Implement → Validate Separation
Three separate commands with clear interfaces between them. No single "do everything" command.

### 2. Automated vs Manual Verification Distinction
Every phase has TWO checklists:
- Automated: `make test`, `go test ./...`, etc. — agent can run these
- Manual: UI/UX, performance under load, edge cases — human must do these
- Agent pauses after automated and explicitly hands off to human

### 3. Parallel Research Agents with Role Specialization
- `locator` agent: ONLY finds files (no reading)
- `analyzer` agent: ONLY explains how code works (no finding)
- `thoughts-locator/analyzer`: separate agents for documentation research
- All read-only with minimal tool sets

### 4. Handoff Documents for Cross-Session Continuity
Structured format for state persistence. Compact but complete.

### 5. Sub-task Spawning Discipline
Rules from `create_plan`:
- Spawn multiple tasks in parallel for efficiency
- Each task focused on ONE specific area
- Provide detailed instructions including exact directories
- Be EXTREMELY specific about directories (not "UI" but "humanlayer-wui/")
- Wait for ALL tasks before synthesizing
- Verify sub-task results — if unexpected, spawn follow-ups

### 6. "What We're NOT Doing" Section
Explicit scope exclusion in every plan. Prevents scope creep.

### 7. Interactive, Iterative Planning
Never write the full plan in one shot. Get buy-in at each step.
```
Present understanding → Confirm → Present options → Choose → Present outline → Approve → Write details → Review → Finalize
```

### 8. Model Selection Per Command
Planning = Opus (maximum reasoning)
Research agents = Sonnet (balanced)
Locator agents = Sonnet with minimal tools (fast, cheap)

### 9. Worktrees for Isolation
Code review happens in isolated worktrees. No risk of contaminating main state.

---

## What HumanLayer Does (the Product)

HumanLayer is an SDK that intercepts AI agent tool calls and routes them to human approval channels (Slack, email, web UI) before the tool executes. Their `.claude/` setup is their internal development workflow, separate from their product.

Their development workflow is a sophisticated "plan → implement → validate" cycle with strong human gates, parallel research agents, and cross-session handoff mechanisms.
