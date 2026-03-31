# Agents vs Skills vs Commands in Claude Code

Source: https://code.claude.com/docs/en/skills and https://code.claude.com/docs/en/sub-agents (fetched 2026-03-31)

---

## Summary

There are three distinct extensibility mechanisms in Claude Code:
1. **Skills** (the successor to commands) — prompt-based workflows invoked via `/skill-name`
2. **Subagents** — specialized AI assistants that run in isolated context windows
3. **Built-in commands** — hardcoded CLI operations (`/help`, `/compact`, `/clear`, etc.)

Skills and commands have been **merged**: a file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way. Skills are the recommended going-forward approach because they support more features.

---

## 1. Skills (formerly Commands)

### What they are
Skills are Markdown files with YAML frontmatter that give Claude a playbook to follow. They create `/slash-command` interfaces and can also be invoked automatically by Claude when the description matches.

### Structure
```
~/.claude/skills/my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Optional template
├── examples/          # Optional example outputs
└── scripts/           # Optional scripts Claude can run
```

### Key frontmatter fields
| Field | Purpose |
|-------|---------|
| `name` | Becomes the `/slash-command` name |
| `description` | How Claude decides when to auto-invoke |
| `disable-model-invocation: true` | Only user can invoke (not auto) |
| `user-invocable: false` | Only Claude can invoke (background knowledge) |
| `context: fork` | Runs in isolated subagent context |
| `agent` | Which subagent type to use when `context: fork` |
| `allowed-tools` | Restricts which tools work in this skill |
| `model` | Override model for this skill |
| `effort` | low/medium/high/max |
| `paths` | Glob patterns for auto-activation scope |
| `hooks` | Lifecycle hooks scoped to this skill |

### Where skills live
| Location | Scope |
|----------|-------|
| `~/.claude/skills/<name>/SKILL.md` | All your projects (personal) |
| `.claude/skills/<name>/SKILL.md` | This project only |
| Plugin `skills/<name>/SKILL.md` | Where plugin is enabled |
| Enterprise managed settings | All org users |

### Invocation control
- Default: both user and Claude can invoke
- `disable-model-invocation: true` → only user (via `/name`)
- `user-invocable: false` → only Claude (background knowledge, no menu entry)

### Dynamic context injection
```yaml
!`gh pr diff`   # Shell command runs before Claude sees prompt; output replaces placeholder
```

### Two types of skill content
1. **Reference content** — knowledge/conventions Claude applies to current work (inline)
2. **Task content** — step-by-step instructions for a specific action (often `disable-model-invocation: true`)

### Running a skill in a subagent
```yaml
context: fork
agent: Explore  # or Plan, general-purpose, or any custom agent name
```

---

## 2. Subagents (Agents)

### What they are
Subagents are specialized AI assistants that run in their **own isolated context window** with a custom system prompt, specific tool access, and independent permissions. They handle tasks and return a summary to the main conversation.

Key properties:
- Each subagent runs in its own context window (preserves main conversation context)
- Can be constrained to specific tools
- Can use a different/cheaper model (e.g., Haiku)
- Cannot spawn other subagents (no nesting)
- Can be run in background (non-blocking)
- Can persist memory across sessions

### Structure
Subagent files are Markdown with YAML frontmatter. The body becomes the system prompt.

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
memory: project
---

You are a senior code reviewer...
```

### Where agents live
| Location | Scope | Priority |
|----------|-------|----------|
| `--agents` CLI flag | Current session | 1 (highest) |
| `.claude/agents/` | Current project | 2 |
| `~/.claude/agents/` | All projects | 3 |
| Plugin's `agents/` | Where plugin enabled | 4 |

### Built-in subagents
| Name | Model | Tools | Purpose |
|------|-------|-------|---------|
| Explore | Haiku | Read-only | Fast codebase search/analysis |
| Plan | Inherits | Read-only | Planning mode research |
| General-purpose | Inherits | All | Complex multi-step tasks |
| Bash | Inherits | Bash | Terminal commands in separate context |

### Key frontmatter fields
| Field | Purpose |
|-------|---------|
| `name` | Unique identifier |
| `description` | When Claude should delegate here |
| `tools` | Allowlist of tools (inherits all if omitted) |
| `disallowedTools` | Denylist of tools |
| `model` | sonnet/opus/haiku/inherit |
| `permissionMode` | default/acceptEdits/dontAsk/bypassPermissions/plan |
| `maxTurns` | Max turns before agent stops |
| `skills` | Skills to inject at startup (full content, not just available) |
| `mcpServers` | MCP servers for this agent only |
| `hooks` | Lifecycle hooks |
| `memory` | user/project/local — cross-session learning |
| `background` | Always run as background task |
| `effort` | low/medium/high/max |
| `isolation` | `worktree` — run in isolated git worktree |
| `initialPrompt` | Auto-submitted first user turn |

### Persistent memory
When `memory` is set, agent gets a persistent directory. `MEMORY.md` (first 200 lines) is injected at startup. Agent can read/write files in memory dir.

### Skills in agents (preloading)
```yaml
skills:
  - api-conventions
  - error-handling-patterns
```
Full skill content is injected at startup. Subagents don't inherit parent's skills — must list explicitly.

---

## 3. Built-in Commands

Fixed-logic operations hardcoded into the Claude Code CLI:
- `/help`, `/clear`, `/compact`, `/model`, `/cost`, `/debug`, `/agents`, `/permissions`
- Not extensible, not available through the Skill tool
- Bundled skills (`/batch`, `/simplify`, `/loop`) ARE prompt-based but ship with Claude Code

---

## 4. When to Use What

| Use case | Mechanism |
|----------|-----------|
| Reusable workflow you invoke manually | Skill with `disable-model-invocation: true` |
| Background knowledge Claude applies automatically | Skill with `user-invocable: false` |
| Complex task that should run in isolation | Skill with `context: fork` |
| Specialized AI role with own model/tools/memory | Subagent |
| Parallel independent research | Multiple subagents |
| Context isolation (high-volume output) | Subagent |
| Domain knowledge reference | Skill (inline reference type) |
| Cross-session institutional knowledge | Subagent with `memory:` field |

---

## 5. How Skills and Agents Compose

Two directions:

**Skill → Agent**: A skill with `context: fork` runs its content as the task prompt in the specified agent type.

**Agent → Skills**: An agent's frontmatter can preload skills via `skills:` field. Full content injected at startup.

Skills and agents are orthogonal dimensions:
- Skill = the task/knowledge definition
- Agent = the execution environment (model, tools, permissions, memory)

---

## 6. The Agent Skills Open Standard

Claude Code skills follow the [Agent Skills open standard (agentskills.io)](https://agentskills.io), which works across multiple AI tools. Claude Code extends it with invocation control, subagent execution, and dynamic context injection.

---

## 7. Scope Resolution Order

When same name exists at multiple levels:
**Enterprise > Personal (~/.claude) > Project (.claude) > Plugin**

Plugin skills use `plugin-name:skill-name` namespace to avoid conflicts.
