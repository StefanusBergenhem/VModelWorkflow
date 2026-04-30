# Evolution and fitness-function checks

Mirrors the author-side `evolution-and-fitness-functions.md`. Architecture is a hypothesis; fitness functions verify it stays honest. One stand-alone check id; the rest land at the Quality Bar gate.

## check.fitness-function.not-named-for-load-bearing-property (soft)

**Check that** load-bearing architectural properties have named fitness functions — automated checks that a stated property still holds.

**Reject when** the document names a load-bearing property (a budget like "p95 ≤ 1200 ms", a dependency-direction rule like "domain must not import infrastructure", a posture like "no plaintext secret in config", a coupling threshold) but does not name a fitness function (CI rule, synthetic probe, SAST rule, static-analysis threshold) that would catch deviation.

**Approve when** every named load-bearing property has at least one fitness function from the four standard categories: dependency direction, latency budget, module size + coupling, security posture.

**Evidence pattern:** name the load-bearing property and state which fitness-function category covers it (or doesn't).

**recommended_action:** *"Add a fitness function for the load-bearing property. Architectural properties without automated checks erode silently — no functional test catches the slow drift toward god-component or dependency-cycle."*

## Soft observations (Quality Bar items, no stand-alone catalog id)

### Architecture-as-hypothesis statement

**Check that** the Overview names the architecture-as-hypothesis bet — one sentence per bet, no more than two or three bets per scope.

**Reject when** the Overview has no hypothesis statement and the document is non-trivial. (Trivial scopes can omit; the absence becomes telling at root.)

**Approve when** the bet is named with sufficient specificity that a future team would recognise when it broke.

**recommended_action:** *"Add the hypothesis as one sentence in Overview. Naming the bet converts an implicit assumption into a testable one — and gives future teams a place to record when it broke."*

### Strangler-fig completeness (where applicable)

**Check that** when a strangler-fig migration is in play, the Architecture entry names the routing mechanism, the retirement criteria, and the rollback point.

**Reject when** strangler-fig is named but any of the three is missing — leaving the migration as aspiration rather than plan.

**Approve when** all three are stated concretely (routing mechanism: reverse-proxy / feature flag / conditional dispatch; retirement criteria: traffic %, error parity, latency parity; rollback point: flag flip + retention window).

**Conditional gating:** applies only when the document mentions strangler-fig, legacy-replacement, or a routing-based migration.

**recommended_action:** *"Add routing mechanism, retirement criteria, and rollback point to the strangler-fig section. Migrations without all three become permanent dual-stack."*

### Test-seam shape per Decomposition entry

**Check that** every Decomposition entry names the test-seam shape (driving ports, driven ports, fake strategy).

**Reject when** the test-seam shape is absent and the component has business logic. A leaf where every test must spin up the database is one whose Architecture neglected testability.

**Approve when** driving and driven ports are listed and the fake strategy is named (in-memory adapter / recorded interactions / pure component).

**recommended_action:** *"Name the test-seam shape per Decomposition entry. Testability is a property of the architecture, not of the test suite — components without seams mandate heavyweight integration tests for every unit test."*

## Sweep order

Walk top to bottom. The stand-alone check (fitness-function naming) is mechanical. The Quality Bar items require reading the Overview and per-Decomposition entries with judgment about what is "load-bearing" at this scope.

Cross-link: `quality-bar-gate.md` (Rationale and traceability card — fitness-functions sub-item); `decomposition-checks.md` (test-seam shape lives in the Decomposition entry); `composition-patterns-checks.md` (latency budget is a load-bearing property).
