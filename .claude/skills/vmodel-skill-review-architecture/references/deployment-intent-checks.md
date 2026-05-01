# Deployment intent checks (root scope only)

Mirrors the author-side `deployment-intent.md`. **All checks in this file apply only when `parent_scope: null` (root scope).** At branch scope, deployment intent inherits from root and these checks are skipped — flag any branch-scope deployment intent as informational rather than required.

The hard refusal C composition trigger `check.composition.deployment-intent-missing` (also documented in `composition-patterns-checks.md`) is the umbrella check. The soft items below catch the specific concerns when deployment intent is present-but-incomplete.

## check.composition.deployment-intent-missing (HARD — refusal C, root only)

(Cross-reference; full definition in `composition-patterns-checks.md`.)

**Check that** at root scope the Composition section enumerates environments, names an orchestration target, and maps Decomposition components to runtime units.

**Reject when** root scope and any of those three pillars is absent.

**Approve when** all three are stated.

## Soft checks — sub-completeness when deployment intent is present

(These are not assigned stand-alone catalog ids. They surface as part of the Quality Bar gate. The reviewer flags them under `check.composition.deployment-intent-missing` evidence when the umbrella check is in scope but partially populated; or as info-level observations when the deployment intent is otherwise complete.)

### Environment enumeration completeness

**Check that** every environment the system runs in (dev, staging, production, plus any per-region or per-tenant variants) is named with differences enumerated: scale, data set, external integrations, observability stack.

**Reject when** environments are listed without enumerating their differences. "We have dev, staging, prod" without naming what differs is environment naming, not enumeration.

**Approve when** each environment has a difference table (scale numbers, data set type, integration mode, telemetry destination).

**recommended_action:** *"Enumerate environment differences. Environments that exist but are not enumerated are environments that drift."*

### Orchestration-target rationale

**Check that** the orchestration target choice (Kubernetes / serverless / container orch / VM-based / bare-metal) names the rationale or `governing_adrs:` reference.

**Reject when** the target is named without rationale ("we use Kubernetes" period). "Default to whatever ops already runs" is a legitimate rationale; "default to Kubernetes because resume-driven" is not.

**Approve when** target rationale is concrete or reference-bound.

**recommended_action:** *"Add rationale for the orchestration target. The choice bounds operational primitives the rest of the architecture can reach for; defaulting on autopilot is how teams accidentally adopt service-mesh complexity they do not need."*

### Runtime-unit mapping completeness

**Check that** every component in the Decomposition is mapped to a runtime unit, and every runtime unit has lifecycle / observability surface / resource budget / failure story.

**Reject when** a component is unmapped, OR a runtime unit lacks any of the four populated fields.

**Approve when** every component lands in a unit and every unit's four fields are populated (even if the answer is "no autoscaling, fixed two-replica" — that is still a populated answer).

**recommended_action:** *"Map every component to a runtime unit. Co-location is a choice (shared fate); separation is a choice (network boundary). State the rationale per unit."*

### IaC-as-implementation discipline

**Check that** IaC paths are referenced, and capacity (pod counts, DB instance size, partition counts) is NOT re-specified in the Architecture artifact.

**Reject when** the artifact re-specifies capacity numbers that belong in IaC (counts, instance types, exact partition layout).

**Approve when** the artifact references the IaC repo and explicitly states "capacity lives in IaC".

**recommended_action:** *"Reference IaC for capacity; do not re-specify what IaC declares. Architecture states intent; IaC implements; specifying both is how they drift apart."*

### 12-factor stance and cost model

**Check that** the 12-factor stance is stated factor-by-factor where load-bearing, AND the cost model (envelope, cost-per-request, cost-of-a-9) is stated.

**Reject when** the document is silent on both, OR cites 12-factor without naming any departures explicitly.

**Approve when** applied/departed lists are explicit and the three cost numbers (or documented "out of scope at this iteration" decisions) are present.

**Note:** the cost-model sub-check has its own catalog id — `check.qa.cost-model-missing` (`data-and-persistence-checks.md`) — to be cited when cost numbers are absent.

**recommended_action:** *"State 12-factor stance where load-bearing and add the three cost numbers. A well-engineered architecture killed by the bill is a category of failure the artifact is meant to prevent."*

## Sweep order

Confirm `parent_scope: null` first. If branch scope, skip the entire file. If root, walk umbrella check first; if it passes, walk soft checks sequentially.

Cross-link: `composition-patterns-checks.md` (umbrella check); `data-and-persistence-checks.md` (`check.qa.cost-model-missing`); `quality-bar-gate.md` (Composition card, root-scope subsection).
