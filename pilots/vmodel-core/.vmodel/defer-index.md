specs_root: pilots/vmodel-core/specs
summary:
  artifacts_with_pending_items: 4
  total_defer_markers: 19
  total_open_follow_ups: 0
items:
- scope: ''
  artifact_id: ARCH-IF-IReportCLI
  path: architecture/interfaces/IReportCLI.md
  defer_markers:
  - type: DEFER-DD
    line: 21
    description: cli-adapter — output destination handling
  - type: DEFER-ADR
    line: 49
    description: CLI deprecation notice period
  open_follow_ups: []
- scope: ''
  artifact_id: ARCH-IF-IValidationCLI
  path: architecture/interfaces/IValidationCLI.md
  defer_markers:
  - type: DEFER-ADR
    line: 52
    description: CLI deprecation notice period
  open_follow_ups: []
- scope: ''
  artifact_id: ARCH
  path: architecture.md
  defer_markers:
  - type: DEFER-DD
    line: 82
    description: cli-adapter — subcommand and flag structure
  - type: DEFER-ADR
    line: 111
    description: validation-engine internal split (one engine vs three sibling components)
  - type: DEFER-DD
    line: 111
    description: validation-engine — JSON Schema 2020-12 validator library selection
  - type: DEFER-DD
    line: 120
    description: reporter — HTML report template structure
  - type: DEFER-DD
    line: 159
    description: cli-adapter — subcommand and flag structure
  - type: DEFER-DD
    line: 170
    description: cli-adapter — subcommand and flag structure
  - type: DEFER-ADR
    line: 224
    description: reporter entrypoint shape (one entrypoint vs per-type)
  - type: DEFER-ADR
    line: 351
    description: build-pipeline release surface
  - type: DEFER-ADR
    line: 351
    description: build-pipeline binary signing
  - type: DEFER-ADR
    line: 367
    description: release surface
  - type: DEFER-DD
    line: 403
    description: validation-engine — per-rule-class scaling characteristics
  - type: DEFER-DD
    line: 425
    description: cli-adapter — subcommand and flag structure
  - type: DEFER-ADR
    line: 430
    description: build-pipeline binary signing
  open_follow_ups: []
- scope: ''
  artifact_id: TS
  path: testspec.md
  defer_markers:
  - type: DEFER-DD
    line: 56
    description: cli-adapter — subcommand and flag structure
  - type: DEFER-DD
    line: 589
    description: cli-adapter — version-query subcommand surface
  - type: DEFER-DD
    line: 730
    description: cli-adapter — version-query subcommand surface
  open_follow_ups: []

