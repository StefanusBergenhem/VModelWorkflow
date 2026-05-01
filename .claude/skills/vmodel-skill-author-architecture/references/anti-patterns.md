# Anti-patterns — six universal + four AI-era

Ten failure modes to detect and rewrite. Each entry has a tell (how to spot it in your own draft) and a fix (how to rewrite). Run this catalog as a sweep before delivering. The author skill's framing is "do not do this"; the matched review skill catches the same shapes after the fact.

## Universal (six)

### 1. Big ball of mud (Foote & Yoder, *Big Ball of Mud*, 1997)

**Tell:** the Architecture artifact exists but the Structure Diagram is missing, has no arrows, or is a spider's web with no discernible flow direction; "where does X happen?" can only be answered by a guided tour; onboarding is measured in months.

**Fix:** redo decomposition from scratch using `decomposition-discipline.md` (information hiding, cohesion, bounded contexts). If a clean decomposition cannot be drawn, the system needs refactoring before an Architecture artifact is meaningful — say so, and emit a Gap report flagging the structural debt.

### 2. Distributed monolith

**Tell:** services share a database, a schema, a deploy cadence, or a synchronous request chain. Every release requires all services to ship together; one service going down takes the whole feature down; integration tests must spin up the full constellation.

**Fix:** redecompose. Either go to a modular monolith (legitimate; one DB, one deploy) or do the work to make services genuinely independent (per-service DB, async edges, independent deploy). The distributed monolith is the worst of both — pay the operational tax for distribution without the independence benefit.

### 3. God component

**Tell:** one component in the Decomposition owns everything central to the domain; peripherals are thin wrappers. The one-sentence-responsibility test fails — the god component's purpose needs three *and*s. Most changes touch this component; its leaf DDs total more lines than the rest of the scope combined.

**Fix:** split. Apply information hiding — list the next three changes the business will demand and check that each lands in one component. The god component will hide two or three real components inside it; surface them as siblings.

### 4. Premature decomposition

**Tell:** ten services for a system three people can fit in a room for; services that always deploy together; "we need to call across three services for a login"; services that cannot be tested independently because there is only one team and one cadence.

**Fix:** start with a modular monolith; split components into separate runtime units only when independence (scaling / failure / ownership) earns its keep. Microservices for a small team is distributed-system tax for nobody's benefit.

### 5. Stale architecture documentation

**Tell:** the Architecture artifact was last edited at initial release; the codebase has had two refactors since; integration tests pass but describe a different topology than the diagram. Newcomers trust the diagram and discover the divergence the hard way.

**Fix:** treat the Architecture as a living artifact. Add fitness functions (`evolution-and-fitness-functions.md`) that fail when reality drifts from the diagram (dependency-direction checks, structural-coupling thresholds). On every architecture-touching PR, the artifact updates with the code.

### 6. Cyclic dependencies

**Tell:** A imports B imports C imports A. The dependency-direction fitness function fails (or would, if it existed). Changes in one component break compilation in a "downstream" component that is actually upstream in the cycle. No independent build order, no independent release.

**Fix:** break the cycle. Two standard techniques: (a) extract a third component the cycle members both depend on (dependency inversion); (b) move a method to the other side. Architecture artifact names the chosen break point and adds a fitness function to keep it broken.

## AI-era and retrofit (four)

### 7. Laundering the current architecture

**Tell:** a retrofit-generated Architecture that describes the system's current structure as if every boundary were intentional and every interface contracted. The diagram looks clean; rationale fields cite no rejected alternatives; every decision appears inevitable. Zero `recovery_status: unknown` values; no acknowledgement that any boundary was accidental; no Gap report.

**Fix:** apply `retrofit-discipline.md`. Every observed boundary marked `reconstructed` with file/line evidence. Every rationale `verified` (with human source) or `unknown` (with follow-up owner). Populate the Gap report — lost rationale, structural drift, missing ADRs, coverage gaps. The diagram should look like reality, including the messy parts; if reality is messy, *say so* in the Gap report.

### 8. Fabricated decomposition rationale

**Tell:** rationales that say "chosen because it matches the single-responsibility principle" or "follows DDD bounded-context separation" — generic principle invocations rather than historical recall. Fabricated rationale is *confident precisely where a real one would be uncertain* — that is the highest-signal tell.

Other phrases that almost always indicate fabrication on retrofit:
- "follows clean separation of concerns"
- "DDD-aligned bounded context"
- "industry-standard pattern"
- "balances X with Y"
- "best practice"

**Fix:** enforce `recovery_status: unknown` on rationale fields during retrofit. Better prompting will not fix this — the model can always produce more plausible-sounding rationale. Only structural refusal works. Replace with `rationale: { status: unknown, note: "no preserved decision record; follow up with @owner", follow_up: ... }`.

### 9. Ad-hoc composition

**Tell:** the Composition section is a sentence or a single diagram with no stated pattern, no wiring strategy, no runtime-unit boundaries, and (at root) no deployment intent. The system is "a bunch of services that talk to each other". Every incident post-mortem names a different emergent behaviour; nobody can predict cascade paths; capacity planning is guesswork.

**Fix:** name a runtime pattern from `composition-patterns.md` (request-response / event-driven / saga / hexagonal / pipeline / serverless / …). State the wiring concerns: DI strategy, middleware stack ordering, message-bus topology. Draw a sequence diagram for the happy path and one or two failure paths. The Composition section is load-bearing; an empty one is a Quality Bar failure regardless of how good the rest is.

### 10. Missing composition spec

**Tell:** Decomposition and Interfaces sections are thorough; Composition is empty or reads "see deployment config". Teams build, discover composition at integration time, and hardcode whichever quirk of orchestration they first got to work. The document exists but has abdicated its most load-bearing section.

This is the most common failure mode in Architectures produced by engineers who are fluent in component design but treat runtime as someone else's problem.

**Fix:** mandate a non-trivial Composition section — runtime pattern named, wiring concerns stated, sequence diagrams present, and at root scope, deployment intent enumerated (environments, orchestration target, runtime-unit boundaries). Hard refusal C in SKILL.md is the structural enforcement. Reject the artifact when Composition is absent or trivial.

## Sweep order

Work through the catalog top to bottom on every draft. The first six are easier to spot mechanically (decomposition / structural shapes); the AI-era four require judgement and benefit from a fresh-eyes pass — do not sweep them on the same pass that wrote them.

Cross-link: `decomposition-discipline.md` (universal #1, #3, #4); `composition-patterns.md` (universal #2; AI-era #9, #10); `retrofit-discipline.md` (AI-era #7, #8); `quality-bar-checklist.md` (final gate).
