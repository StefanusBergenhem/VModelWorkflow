# Archived pre-pivot skills

These skills were operational pre-pivot (2026-04-18) and during early Phase 6. They are superseded by the V-model build-flow skills under `.claude/skills/vmodel-skill-{plan-build,orchestrate-build,render-tests,implement-leaf,review-execution,retrospect-build}/`.

| Pre-pivot skill | Replaced by |
|---|---|
| `derive-test-cases` | `vmodel-skill-render-tests` (TDD red-phase rendering) + `vmodel-skill-author-testspec` (case derivation) |
| `develop-code` | `vmodel-skill-implement-leaf` |
| `vmodel-skill-review-code` | `vmodel-skill-review-execution` (leaf layer) |
| `*-workspace` (`develop-code-workspace`, `derive-test-cases-workspace`, `vmodel-skill-review-code-workspace`) | n/a — workspace-orchestration patterns subsumed by `vmodel-skill-orchestrate-build` |
| `combined-workspace` | n/a — superseded by orchestration state machine |

Date archived: 2026-05-09. Preserved for reference only — do not invoke.
