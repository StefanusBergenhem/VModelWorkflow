# Scenarios — prompt-skill-agent-builder

## Scenario 1: Type-mismatch detection

**User prompt:** "Create a skill that runs autonomously, calls tools in a loop, and hands back a final report when done."

**Success criteria:**
- Model raises type mismatch, names the contradicting signals (loop, tool use, handover artifact).
- Recommends agent instead of skill.
- Asks user to confirm or override before proceeding.

**Would fail without skill because:** base model takes the user's "skill" label at face value and produces a malformed skill with agent semantics.

---

## Scenario 2: Interview dependency order

**User prompt:** "Create a skill for summarizing PRs."

**Success criteria:**
- Model opens with single-responsibility boundary question, not the name or description.
- Every question carries a recommended answer with one-line reasoning.
- Name and description questions come after the boundary is fixed (dependency order).
- Does not ask open-ended questions without a default.

**Would fail without skill because:** base model typically asks "what should we call it?" first, producing a name that doesn't match the eventual scope.

---

## Scenario 3: Self-review catches anti-patterns

**User prompt:** "Generate from this spec: name = claude-git-helper, description = 'helps with git stuff', covers commits and branching and merges."

**Success criteria:**
- Model generates the artifact (honoring the skip-interview shortcut) but self-review flags: name contains "claude"; description vague and missing *when*; multiple responsibilities.
- Findings reported with file:line references.
- Does not silently fix — surfaces findings to user.

**Would fail without skill because:** base model either refuses to generate from a weak spec, or generates and declares done without flagging the anti-patterns.
