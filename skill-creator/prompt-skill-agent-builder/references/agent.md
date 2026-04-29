# Agent reference

An agent is a system prompt + tool allowlist + often a loop/orchestration contract. Explicitly invoked (not discovered). Operates autonomously across multiple turns, often with handover artifacts between phases.

## Signal table (type mismatch check)

User said "agent." Check for ≥2 contradicting signals:

| Signal present | Points to |
|---|---|
| Single-turn, user reads output and acts | prompt |
| No tools, no loop | prompt or skill |
| Reused across sessions, triggered by user phrasing | skill (or skill that invokes the agent) |
| Purely advisory — no autonomous action | skill |
| One-shot paste-into-chat usage | prompt |

If ≥2 present, raise: "you described <signals> — that's a <type>, not an agent. Proceed as <type> or override?"

## Mandatory decisions (dependency order)

1. **Single responsibility.** What one job does this agent do autonomously? *Default: user states; challenge "and."*
2. **Name.** Follows skill naming rules (≤64, lowercase-hyphens). *Default: 3 candidates, user picks.*
3. **Autonomy scope.** What may it do without user confirmation? What must it confirm? *Default: destructive/irreversible actions always confirm; reversible local actions proceed.*
4. **Tool allowlist.** Exact list. No wildcards unless justified. *Default: start from read-only tools; add write/execute tools one by one with justification.*
5. **Effort / model.** Which model, what effort setting? *Default: Sonnet 4.6 at medium effort; bump to Opus 4.7 high only if reasoning is the bottleneck.*
6. **Loop / termination contract.** What does one iteration produce? What signals done? What bounds attempts? *Default: require explicit max-attempts; require explicit done-signal (typed artifact, user confirmation, or measurable condition).*
7. **Handover artifacts.** Typed outputs at entry and exit. Schema for each. *Default: require YAML/JSON with schema; free-form prose only for user-facing summary.*
8. **HALT conditions.** When does it stop and escalate rather than retry? *Default: 3 consecutive failures on the same approach → HALT; any unrecognized error type → HALT.*
9. **Failure retry discipline.** Each retry must differ from the previous. On 2nd consecutive failure apply root-cause tracing. *Default: enforce via prompt; no exceptions.*
10. **Context budget.** How does the agent handle context-window pressure? Fresh context vs. compaction? State persistence files? *Default: pipe verbose output to `/tmp/*.log`, read log back; persist state in typed files, prefer fresh context over compaction for long runs.*
11. **Eval scenarios.** 3+ scenarios where agent produces measurably better outcome than base model on the same task. *Default: draft 3 with user; must be end-to-end, not unit-scale.*

## Creating

1. Fill `templates/agent/agent.md.tmpl` (system prompt) using interview answers.
2. Fill `templates/agent/tools.yaml.tmpl` with the allowlist from decision 4.
3. Write to `./.claude/agents/<name>.md` (project-local).
4. Bundle eval scenarios if user accepted.
5. Run self-review.

## Editing

1. Parse existing agent file + any co-located tools.yaml or config.
2. Map against 11 mandatory decisions.
3. Specifically check: tool allowlist creep, missing HALT conditions, missing retry discipline, vague done-signal, unbounded loops.
4. Interview only on flagged items.
5. Diff output.

## Agent-specific anti-patterns

- Wildcard tool allowlist without justification.
- No max-attempts bound (infinite loop risk).
- No typed handover artifact — agent hands back free-form prose only.
- Retry without varying approach ("try again" → same failure).
- Compaction as default strategy for long runs (prefer fresh context).
- Destructive action without user confirmation.
- Prescriptive CoT in system prompt on 4.6/4.7 (use effort setting instead).
- No root-cause-tracing trigger after repeated failure.
- Agent claims completion without fresh evidence (stale test output, unreread file).
- Scope creep into adjacent responsibilities.
