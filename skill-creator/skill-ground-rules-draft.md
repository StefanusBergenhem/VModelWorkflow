 HALT schema (v1)

  # .workflow/halts/<ISO-timestamp>_<halt_id>.yaml
  # Pointer to most recent: .workflow/halt.yaml (symlink or copy)

  schema_version: 1

  halt_id: halt-2026-04-16-001
  timestamp: 2026-04-16T14:32:11Z

  # Who halted
  agent: vmodel-agent-tdd-developer           # agent that halted
  skill: vmodel-skill-develop-code             # skill active at halt (optional)
  task_contract: .workflow/current_task.yaml   # pointer, not inline

  # Why
  category: uncertain | missing-input | off-track | conflict | out-of-scope | design-issue | retry-exhausted
  trigger: "one-line description of what triggered the halt"
  context_summary: |
    2-5 lines: what the agent was doing, how far it got, what state
    it's leaving behind.

  # What was tried (for retry-exhausted or off-track)
  what_was_tried:
    - attempt: 1
      approach: "brief description"
      outcome: "what happened"
    # ...

  # What the agent needs from human
  specific_question: "single crisp question, or null if category is design-issue/retry-exhausted"
  options:                                     # null if open-ended
    - name: "option-a-slug"
      summary: "1-2 lines"
      consequence: "1-2 lines on downstream impact"
    - name: "option-b-slug"
      summary: "..."
      consequence: "..."

  # Enables clean resume
  work_in_progress:
    files_touched: ["src/foo.py", "tests/test_foo.py"]    # for rollback/commit decisions
    uncommitted: true
    references: [".workflow/current_task.yaml", "design/foo-dd.md"]

  resume_instructions: |
    Human provides: answer to specific_question (or selected option).
    Resuming agent loads: task_contract, halt.yaml, files_touched.
    Recommended: restart in fresh context per GR-13 if category is
    off-track or retry-exhausted.

  Rules of use:
  - Every agent entry reads (and references) a contract; every agent exit — success, failure, or HALT — writes a
  handover artifact.
  - schema_version: 1 — bump on any field rename or semantic change. Agents must refuse to parse a HALT with unknown
  schema_version.
  - Stored under .workflow/halts/ with full history; .workflow/halt.yaml always points to the latest.

  Any field you want to add or cut before we lock?

  ---
  Deterministic enforcement catalog (saved — goes into skills architecture)

  ┌─────┬───────────────────────┬──────────────────────────────┬────────────────────────────────────────────────────┐
  │  #  │      Enforcement      │            Scope             │                       Notes                        │
  ├─────┼───────────────────────┼──────────────────────────────┼────────────────────────────────────────────────────┤
  │ 1   │ YAML/JSON schema      │ All artifacts, contracts,    │ Via schemas/                                       │
  │     │ validation            │ trace files, HALT files      │                                                    │
  ├─────┼───────────────────────┼──────────────────────────────┼────────────────────────────────────────────────────┤
  │ 2   │ Language linter       │ Source code                  │ Per-language, no suppression directives allowed    │
  │     │                       │                              │ (CLAUDE.md rule)                                   │
  ├─────┼───────────────────────┼──────────────────────────────┼────────────────────────────────────────────────────┤
  │ 3   │ Type checker          │ Source code (where language  │ Same no-suppression rule                           │
  │     │                       │ supports it)                 │                                                    │
  ├─────┼───────────────────────┼──────────────────────────────┼────────────────────────────────────────────────────┤
  │ 4   │ Test runner + exit    │ Unit tests, integration      │ Pipe to /tmp to protect context (CLAUDE.md rule)   │
  │     │ code                  │ tests                        │                                                    │
  ├─────┼───────────────────────┼──────────────────────────────┼────────────────────────────────────────────────────┤
  │ 5   │ Coverage check        │ Line / branch / (optional)   │ Coverage matrix cross-check                        │
  │     │                       │ mutation                     │                                                    │
  ├─────┼───────────────────────┼──────────────────────────────┼────────────────────────────────────────────────────┤
  │ 6   │ Trace link validator  │ Trace files                  │ Checks (a) target exists, (b) content-hash not     │
  │     │                       │                              │ stale                                              │
  ├─────┼───────────────────────┼──────────────────────────────┼────────────────────────────────────────────────────┤
  │ 7   │ Content-hash          │ All traced artifacts         │ Deterministic, no LLM needed                       │
  │     │ staleness             │                              │                                                    │
  ├─────┼───────────────────────┼──────────────────────────────┼────────────────────────────────────────────────────┤
  │ 8   │ File boundary guard   │ Every agent task             │ Only files_to_touch editable (CLAUDE.md rule)      │
  ├─────┼───────────────────────┼──────────────────────────────┼────────────────────────────────────────────────────┤
  │ 9   │ Structured-output     │ All agent output claiming    │ Reject on parse failure                            │
  │     │ parser                │ YAML/JSON                    │                                                    │
  ├─────┼───────────────────────┼──────────────────────────────┼────────────────────────────────────────────────────┤
  │     │ Requirement regex     │                              │ EARS patterns, subset of INCOSE 42 rules (e.g.,    │
  │ 10  │ checks                │ Requirement artifacts        │ absolute quantifiers, passive voice, vague         │
  │     │                       │                              │ adjectives)                                        │
  ├─────┼───────────────────────┼──────────────────────────────┼────────────────────────────────────────────────────┤
  │ 11  │ Secret/credential     │ Pre-commit                   │ Standard tool                                      │
  │     │ detector              │                              │                                                    │
  ├─────┼───────────────────────┼──────────────────────────────┼────────────────────────────────────────────────────┤
  │ 12  │ Schema-version guard  │ All handover/HALT files      │ Refuse unknown schema_version                      │
  └─────┴───────────────────────┴──────────────────────────────┴────────────────────────────────────────────────────┘

  Known to NOT be automatable (ADR these in the architecture doc when we get there):
  - Requirement semantic correctness ("does this actually capture what the stakeholder meant")
  - Design judgment / trade-off reasoning
  - Review judgment on "is this well-written / clear"
  - Safety analysis completeness certification (AI empirically <70%, humans required)
  - Stakeholder interpretation / concurrence

  Reminder to self: every time we draft a skill, check this catalog first. If the rule is in the catalog, the skill
  delegates to the tool and doesn't re-enforce in prose.

  ---
  Locked ground rules (GR-1 through GR-14)

  GR-1   Prime, don't teach. Reference known concepts by name; add reasoning
         only where the model doesn't default to it.

  GR-2   Total instruction budget: 120 per composed agent at run-time
         (system prompt + CLAUDE.md + tool defs + skills + agent body).
         No per-skill sub-budget. [exact number: revisit empirically]

  GR-3   One instruction = one enforceable directive.
         Count: MUST / MUST NOT / NEVER / ALWAYS / SHOULD, or one checklist
         item. Compound sentences split per obligation.
         Don't count: definitions, rationale, examples, references.

  GR-4   Minimalism everywhere. Thin CLAUDE.md. MCP only when strictly
         needed. Controlled skill count. No deeply nested references
         (one level deep from SKILL.md, per vendor).

  GR-5   Match persuasion profile to skill role.
           Lower-V / discipline: Authority + Commitment + Social Proof
           Upper-V / advisory:   Unity + Commitment, moderate Authority
           Framework / template: Clarity only
         NEVER use Liking or Reciprocity.

  GR-6   HALT option on every skill. Every HALT produces a versioned
         halt.yaml (schema v1 above). Every agent entry and exit is a
         handover artifact.

  GR-7   Implementation intentions over general instructions.
         "When X, do Y" beats "generally do Y".

  GR-8   Strict typed handover artifacts at every agent entry/exit,
         with schema_version. No untyped in-memory state across agents.

  GR-9   Progressive disclosure via staggered loading within a single
         skill. SKILL.md is thin; references load when the agent reaches
         the phase that needs them. Target: stay in very-smart zone,
         degrade only to normal-smart, never enter dumb zone.

  GR-10  Deterministic enforcement by default. Anything checkable by
         schema, lint, regex, or AST MUST NOT be in the prompt — push it
         to a tool. Catalog above. ADR what we can't mechanize.

  GR-11  Evaluation baseline for every craft skill. Must show measurable
         uplift over a no-skill baseline on Tier 3 (Haiku). No skill
         ships without this.

  GR-12  Separation of concerns. No "do everything" skills; each skill
         owns one role. Tight coupling between orchestrator and craft
         skill internals is banned.

  GR-13  Restart over repeated correction. Fresh context when agent is
  ---
  Codex filing

  Proposal: file back as concept-vmodel-skill-authoring-principles (project-specific synthesis) in
  engineering-codex/wiki/concepts/. Sources cited: src-seed-anthropic-best-practices, pat-skill-persuasion,
  concept-context-management, concept-skill-composition, pat-handoff-documents, src-horthy-rpi-retro-2026,
  src-12-factor-agents-2025, pat-model-tier-aware-skills.

  It's a cross-repo write, so confirming before I touch anything: approve the codex write now, or wait until we've put
  the rules through at least one skill and know they hold up in practice? My lean: wait one cycle — file after we've
  built the first skill (or revised an existing one) using these 14 rules and confirmed they're not theoretical. That
  keeps the codex's "no fabrication" discipline tight.

  ---
  Next move once you confirm HALT schema and codex timing: update docs/guide/skills-architecture.html with these ground
  rules + the deterministic enforcement catalog + HALT pattern. That's step A from the earlier plan (now with real
  content). OK to proceed?
