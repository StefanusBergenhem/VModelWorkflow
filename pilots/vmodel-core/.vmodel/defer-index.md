specs_root: pilots/vmodel-core/specs
summary:
  artifacts_with_pending_items: 5
  total_defer_markers: 19
  total_open_follow_ups: 24
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
  artifact_id: REQS
  path: requirements.md
  defer_markers: []
  open_follow_ups:
  - line: 1145
    text: '**`derived_from` placeholder `NEEDS-vmodel-core` is not in the canonical'
  - line: 1147
    text: '*Owner*: framework author.'
  - line: 1148
    text: '*Action*: resolve as part of elicit-needs decision γ (`dogfood_findings.md`'
  - line: 1156
    text: '**No parent-scope (VModelWorkflow-level) Requirements artifact exists.**'
  - line: 1157
    text: '*Owner*: framework author.'
  - line: 1158
    text: '*Action*: per `dogfood_findings.md` Issue 2, framework-level needs should
      be'
  - line: 1163
    text: '**NFR target slots (`fail`/`goal`/`stretch`/`wish`) are pending pilot'
  - line: 1165
    text: '*Owner*: framework author (in dogfooding pilot role).'
  - line: 1166
    text: '*Action*: set the four target slots per NFR from pilot calibration; revise'
  - line: 1169
    text: '**CLI ergonomic shape beyond exit codes and output formats is deferred.**'
  - line: 1170
    text: '*Owner*: framework author.'
  - line: 1171
    text: '*Action*: revisit once pilot evidence and the engineering-codex'
  - line: 1180
    text: '**Reporting output formats beyond HTML are deferred.**'
  - line: 1181
    text: '*Owner*: framework author.'
  - line: 1182
    text: '*Action*: decide whether the four reporting outputs also need JSON'
  - line: 1186
    text: '**Open-source licence is not yet selected.**'
  - line: 1187
    text: '*Owner*: framework author.'
  - line: 1188
    text: '*Action*: author a product-scope ADR selecting a specific licence (per'
  - line: 1191
    text: '**CLI deprecation notice period is not yet committed.**'
  - line: 1192
    text: '*Owner*: framework author.'
  - line: 1193
    text: '*Action*: author a product-scope ADR setting the minimum deprecation'
  - line: 1199
    text: '**Success metrics are deliberately unset at v1.**'
  - line: 1200
    text: '*Owner*: framework author.'
  - line: 1201
    text: '*Action*: per needs.md (turn 11), specific metrics for vmodel-core''s'
- scope: ''
  artifact_id: TS
  path: testspec.md
  defer_markers:
  - type: DEFER-DD
    line: 56
    description: cli-adapter — subcommand and flag structure
  - type: DEFER-DD
    line: 584
    description: cli-adapter — version-query subcommand surface
  - type: DEFER-DD
    line: 721
    description: cli-adapter — version-query subcommand surface
  open_follow_ups: []

