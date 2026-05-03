---
id: ADR-001-implement-vmodel-core-in-go
artifact_type: adr
title: "Implement vmodel-core in Go"
status: accepted
date: "2026-05-03"
scope_tags: ["vmodel-core"]
---

# ADR-001: Implement vmodel-core in Go

**Y-statement.** In the context of vmodel-core's implementation language (foundation for the next architecture session), facing the need for a single-binary deterministic CLI on Linux/macOS/Windows that is mainly developed by AI coding agents, we decided for **Go**, to achieve high AI-codegen accuracy, a mature YAML 1.2 parser ecosystem, and stdlib HTML templating, accepting the loss of Rust's compile-time exhaustive-match for the system-error / rule-violation discrimination (REQ-005) — mitigated by separate types with separate emit functions.

## Context

vmodel-core is the daily-driver tool of the V-model framework's three-tool product set (`references/framework/TARGET_ARCHITECTURE.md §10`). Its requirements (`specs/requirements.md`) are at root scope, status `draft`, with 28 atomic requirements and 12 inherited constraints. Architecture authoring is the next planned session and is gated on a small number of load-bearing decisions; implementation language is the foundational one because it bounds every component's interface choice (error model, library availability, build pipeline shape, distribution mechanism). The decision must be made before architecture authoring proceeds. The framework author works solo in dogfooding-pilot mode, with primary code-production by AI coding agents.

The candidate language space considered for this decision spans five languages — **Go**, **Rust**, **Zig**, **C++**, and **Java / .NET with AOT** — each plausibly brought to the table by vmodel-core's hard constraints (single static binary across Linux/macOS/Windows; no separate runtime install; no LLM at runtime; mature parsing/schema/HTML library availability). All five are presented in the Alternatives section below with their context-specific rejection reasons; **Go** is the chosen option.

### Drivers

- **IC-004 — single-binary distribution.** Adopter must download one artefact and run it on Linux, macOS, or Windows with no separate runtime install.
- **IC-001 — determinism / no LLM at runtime.** Same input must produce identical output across runs.
- **IC-012 — commodity CI runner.** Worst-case target hardware constrains memory baseline and startup time.
- **IC-002 — stateless cold-start.** Each invocation is independent; cold-start is the only state.
- **REQ-022 — AI-caller author retry-loop latency.** The most latency-sensitive workflow is subprocess cold-start + parse + validate + verdict-emit, repeated multiple times per artifact during AI-agent retry.
- **AI-coding-agent productivity.** vmodel-core is mainly developed by AI coding agents. Open-web idiomatic-code corpus density affects AI-agent output quality; languages with denser idiomatic corpora produce more reliable agent output.
- **Framework-author maintainability.** Single-person dogfooding pilot; long-term maintenance falls on one person currently. Author has roughly equal basic fluency in Go and Rust at this date and is equally happy learning either further.
- **Library availability for the parse/validate/render pipeline.** Production-grade libraries needed for: YAML 1.2 parsing, JSON-Schema (draft 2020-12) validation, Markdown front-matter parsing, HTML templating, JSON serialisation.
- **Error-handling discriminator clarity (REQ-005).** Verdict-record must distinguish `system-error` from rule-violation findings; this is a discriminated-union shape at the type level.

### Assumptions (revisit triggers)

- IC-004's single-binary constraint holds. If the framework relaxes runtime-install policy, runtime-bearing languages (Python, Node, JVM) reopen the option space.
- AI-coding-agent corpus-density advantage for Go over Rust holds at this date and is expected to persist through v1. If Rust adoption surges or AI training corpora rebalance, this driver weakens.
- Rust's YAML 1.2 ecosystem remains in transition (`serde_yaml` unmaintained as of 2024; `yaml-rust2` and `saphyr` are live forks not yet at parity with `goccy/go-yaml`). If a Rust YAML 1.2 parser stabilises at production maturity comparable to `goccy/go-yaml`, this driver weakens.
- vmodel-core remains a sequential CLI with no concurrent engine and no async-runtime needs. If performance demands push toward heavy concurrency or a long-running process, Rust's no-GC model gains weight against Go's GC.
- Framework-author fluency in Go and Rust remains roughly equal. If the author's investment shifts deep into one language, that becomes a stronger driver and may re-tip the call.

## Decision

We will implement vmodel-core in **Go**.

## Alternatives considered

- **Rust.** Rejected on a combination of three context-specific drivers: (1) **AI-coding-agent corpus density** — open-web idiomatic Rust is sparser than idiomatic Go, and the project is mainly AI-developed; (2) **YAML 1.2 ecosystem state** — `serde_yaml` is unmaintained as of 2024, and the active replacements (`yaml-rust2`, `saphyr`) are not at parity with `goccy/go-yaml`, which matters for IC-001 (deterministic, predictable parser behaviour); (3) **HTML templating for REQ-025 reporting** — Rust requires an external crate (`askama` / `tera`), where Go's `html/template` is in stdlib. Rust's compile-time exhaustive-match (a real advantage for REQ-005's system-error-vs-finding split) and ownership-checked memory safety (modest marginal value for a sequential CLI) were not enough to outweigh the three drivers above at this project's size and AI-developed posture.

- **Zig.** Rejected on **library availability** grounds: production-grade libraries for YAML 1.2, JSON-Schema (draft 2020-12), Markdown front-matter, and HTML templating are nascent or absent in Zig at this date; vmodel-core would need to self-implement substantial parsing and validation infrastructure that is available mature off-the-shelf in both Go and Rust. The implementation cost falls outside dogfooding-pilot scope and offers no compensating advantage on any other named driver (IC-004 fit and binary size are comparable to Go and Rust, but the parser-implementation cost is the disqualifier).

- **C++.** Rejected on **framework-author maintainability** and **AI-coding-agent productivity** grounds: build pipeline complexity (no single canonical package manager standard across Linux / macOS / Windows), header / linkage ergonomics, and materially lower AI-codegen accuracy on idiomatic C++ than on Go. The pilot's solo, mainly-AI-developed posture cannot absorb these costs against the load-bearing drivers, and C++ offers no compensating advantage over Go or Rust on any named driver (IC-004 fit is comparable; library availability is comparable; correctness guarantees are weaker than Rust and not better than Go for vmodel-core's sequential workload).

- **Java with GraalVM AOT / .NET with NativeAOT.** Rejected on **IC-004** and **REQ-022** grounds: while NativeAOT toolchains can produce statically-linked binaries that satisfy IC-004 in principle, cross-compilation across Linux / macOS / Windows is materially more setup-heavy than Go's `CGO_ENABLED=0 go build` (a slight IC-004 cost), and runtime cold-start latency is higher than both Go and Rust on the AI-caller subprocess retry pattern (a REQ-022 cost — cold-start is the only state per IC-002, so steady-state JIT amortisation does not apply). The JVM and .NET ecosystems' framework richness is irrelevant to vmodel-core's narrow tool scope and offers no compensating advantage on any named driver.

## Rationale

Three drivers carried the call:

1. **AI-coding-agent productivity.** vmodel-core is mainly developed by AI coding agents, and idiomatic-Go corpus density on the open web is materially higher than idiomatic-Rust. Agent output accuracy on Go is correspondingly higher today, accelerating the dogfooding pilot and reducing the rate at which AI-generated code requires human correction.
2. **Library availability — YAML 1.2 specifically.** `goccy/go-yaml` is mature, maintained, and conformant; the Rust YAML ecosystem is in transition (`serde_yaml` unmaintained; replacements not yet at parity). For a tool whose entire input is YAML-bearing Markdown artefacts, parser maturity is load-bearing. Determinism (IC-001) compounds the cost of a parser that may shift behaviour during the transition.
3. **Library availability — HTML templating.** REQ-025 commits HTML reporting; Go's `html/template` is in stdlib with safe-by-default escape, while Rust requires an external crate. At this project's scale and single-author maintenance posture, "one fewer external dependency in the contextually-escape-sensitive output path" is a real driver, not a cosmetic one.

The framework-author maintainability driver did **not** carry the call: author fluency is roughly equal in Go and Rust at this date, so it does not tip in either direction; recording it explicitly prevents a future reader from inferring it was decisive. Build/cross-compile simplicity and IC-004 fit are slight Go advantages but not load-bearing on their own. IC-001, IC-012, IC-002, REQ-022, and the AI-caller subprocess pattern are wash drivers between the two candidates and do not pick. Rust's compile-time exhaustive-match for REQ-005's discrimination is a real advantage, but it is mitigable in Go by explicit separate types and tested emit functions; the cost of mitigation is bounded and lower than the cost of the corpus-density and YAML-ecosystem disadvantages.

## Consequences

**Positive**

- **Single-binary cross-compile is trivial.** `CGO_ENABLED=0 go build` with `GOOS` / `GOARCH` produces a statically-linked binary for Linux, macOS, and Windows from any host, with no per-target tooling beyond the Go toolchain itself. Direct fit for IC-004.
- **HTML templating is in stdlib.** REQ-025's HTML reporting needs no third-party templating dependency; `html/template`'s context-aware escape provides safe output by default.
- **Mature YAML 1.2 parser available** (`goccy/go-yaml`). Predictable, maintained parser behaviour supports IC-001 directly.
- **AI coding agents produce more idiomatic, more reliable code on Go than on Rust at this date.** Pilot velocity benefits; AI-agent retry loop on vmodel-core's own implementation converges faster.
- **Build time fast** (typically seconds for vmodel-core's expected scale). Keeps the dev loop snappy during pilot iteration.

**Negative**

- **Lose compile-time exhaustive-match for system-error-vs-rule-violation discrimination (REQ-005).** Mitigation: `SystemError` and `Finding` are distinct Go types with separate emit paths on the verdict-aggregator; behaviour test enforces that an emit-stream contains either zero `SystemError`s plus zero-or-more `Finding`s, or exactly one `SystemError` plus zero-or-more pre-halt `Finding`s. Mitigation cost is one additional emit-path test per consuming surface. Bounded.
- **Lose Rust's compile-time memory-safety guarantees.** For a sequential CLI processing structured input, the marginal risk is small; mitigated by standard Go testing practice (race detector under `-race` for any goroutine usage; bounds-checked stdlib slice operations).
- **Go map iteration is randomised by design.** To preserve IC-001 determinism across runs, finding-records and report contents that traverse map data must be sorted before emit. This is a one-line discipline at each emit boundary; cost is bounded but real (every emit path must be reviewed for stable ordering).
- **AI-codegen density advantage is on a moving signal.** If Rust adoption surges or training corpora rebalance, the chief driver weakens. The decision is partly bet on a current-state assumption; revisit triggers are listed in the Assumptions section above.

**Reversibility.** *(Verbatim prompt: "Is this decision reversible? If yes: state the rollback path. If no: state the recovery plan and name who must sign off before implementation.")*

**Reversible.** Rollback path: port the codebase to the alternative language (Rust), re-run the full test suite, and rebuild distribution. The CLI surface contract (REQ-024 / REQ-025) is language-agnostic — adopters consuming vmodel-core as a subprocess (per IC-006) are not affected by a language switch. Cost estimate is roughly proportional to LOC and test surface: at the start of v1 (current state), days of work; after v1 ships, several engineer-weeks; after v1.x with non-trivial accreted code, weeks-to-months. Revisit triggers (Assumptions section) should be checked before the rewrite cost grows beyond what we are willing to pay — practically, before each major version cut. No external sign-off required.

## Propagation

- **Consequence:** *"Single-binary cross-compile via `CGO_ENABLED=0 go build` with `GOOS` / `GOARCH` is the distribution mechanism."*
  Route: governing_adrs from child architecture.
  Bound by: forthcoming vmodel-core root architecture (will carry `governing_adrs: [ADR-001-implement-vmodel-core-in-go]` and specify the build / deploy pipeline citing this ADR in its Composition / Deployment-intent section).

- **Consequence:** *"HTML reporting uses Go's `html/template` stdlib package."*
  Route: governing_adrs from child architecture.
  Bound by: forthcoming root architecture's reporting component decomposition (carries `governing_adrs: [ADR-001-implement-vmodel-core-in-go]`).

- **Consequence:** *"YAML 1.2 parsing uses `goccy/go-yaml`."*
  Route: governing_adrs from child architecture.
  Bound by: forthcoming root architecture's parser component decomposition (carries `governing_adrs: [ADR-001-implement-vmodel-core-in-go]`).

- **Consequence:** *"System-error and rule-violation findings are discriminated by separate types with separate emit functions, enforced by test."*
  Route: governing_adrs from child architecture (and downstream Detailed Design).
  Bound by: forthcoming root architecture's verdict-aggregator and rule-engine components (carry `governing_adrs: [ADR-001-implement-vmodel-core-in-go]`).

- **Consequence:** *"Findings and report contents must be emitted in a stable order independent of internal map iteration."*
  Route: new requirement at this scope.
  Materialised as: **REQ-029** — *"When emitting one or more finding-records during a validation run, the system shall emit them in a stable order determined solely by the emitting artifact's path and the location within that artifact, such that two runs against identical input produce byte-identical finding-record streams."* Testable at vmodel-core's stdout boundary by running the same input twice and comparing emitted streams byte-for-byte. (Pending edit to `specs/requirements.md` — see session note.)

- **Consequence:** *"AI-codegen density advantage is a current-state signal; revisit if it shifts."*
  Route: revisit-trigger only — listed in Context Assumptions; no co-located requirement (this is a monitoring concern, not a contract).

- **Consequence:** *"Build-time speed advantage."*
  Route: revisit-trigger only — no co-located requirement (this is a developer-experience property, not a testable contract).
