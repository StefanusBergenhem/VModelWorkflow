# Iteration 1 Grading Summary

## Test Setup

- **Model:** Haiku (claude-haiku-4-5)
- **Skills:** develop-code + derive-test-cases (combined)
- **3 eval cases**, each with skill vs baseline (6 total runs)

| # | Design | Format | Language |
|---|--------|--------|----------|
| 1 | FuelRateLimiter | Layer 2 (structured, IDs) | Java 17 / JUnit 5 |
| 2 | TemperatureController | Plain markdown (no IDs) | Python / pytest |
| 3 | SessionManager | Layer 1 only (component level) | Go / testing |

---

## Assertion Results

### A1: Coverage matrix produced (derive-test-cases value-add)

The model wouldn't produce a design-to-test traceability matrix without being told to.

| Run | With Skill | Baseline |
|-----|-----------|----------|
| FuelRateLimiter | **PASS** — proper coverage matrix with design IDs mapped to tests | **FAIL** — produced a "build guide" not a coverage matrix |
| TempController | **PASS** — coverage matrix with all 4 strategies labeled | **FAIL** — no coverage matrix at all |
| SessionManager | **PASS** — coverage matrix mapping component elements to tests | **PARTIAL** — "test coverage analysis" exists but is a prose summary, not a traceability matrix |

**Score: With skill 3/3, Baseline 0/3**

### A2: Implementation notes produced (develop-code value-add)

Design decisions and traceability notes that explain *why* the implementation is the way it is.

| Run | With Skill | Baseline |
|-----|-----------|----------|
| FuelRateLimiter | **PASS** | **FAIL** — README exists but no implementation notes |
| TempController | **PASS** | **FAIL** — no notes |
| SessionManager | **PASS** | **PASS** — baseline also produced implementation notes |

**Score: With skill 3/3, Baseline 1/3**

### A3: No code beyond design scope (develop-code rule #1)

Extra methods, build files, or features not specified in the design.

| Run | With Skill | Baseline |
|-----|-----------|----------|
| FuelRateLimiter | **PASS** — no extra methods | **FAIL** — added `getPreviousRate()`, `reset()`, `pom.xml`, `build.gradle` |
| TempController | **PASS** | **PASS** |
| SessionManager | **PASS** | **PASS** |

**Score: With skill 3/3, Baseline 2/3**

### A4: Immutable result objects (develop-code error handling)

Return types should be immutable to prevent downstream mutation bugs.

| Run | With Skill | Baseline |
|-----|-----------|----------|
| FuelRateLimiter | **PASS** — immutable FuelRateResult (final fields) | **PASS** — also immutable |
| TempController | **PASS** — `@dataclass(frozen=True)` | **FAIL** — plain `@dataclass` (mutable) |
| SessionManager | **PASS** — Go structs returned by value | **PASS** — same |

**Score: With skill 3/3, Baseline 2/3**

### A5: Tests organized by derivation strategy (derive-test-cases structure)

Tests explicitly grouped by requirement-based, equivalence class, boundary value, error handling.

| Run | With Skill | Baseline |
|-----|-----------|----------|
| FuelRateLimiter | **PASS** — test classes by strategy | **FAIL** — organized by behavior, not strategy |
| TempController | **PASS** — 10 test classes by strategy | **FAIL** — organized by state (init, idle, heating, cooling) |
| SessionManager | **PASS** — organized by strategy | **FAIL** — organized by component |

**Score: With skill 3/3, Baseline 0/3**

### A6: Boundary value tests present (derive-test-cases strategy #3)

Explicit tests at min, max, just-below, just-above for constrained inputs.

| Run | With Skill | Baseline |
|-----|-----------|----------|
| FuelRateLimiter | **PASS** — 8 boundary tests named explicitly | **PARTIAL** — some boundary cases but not systematic |
| TempController | **PASS** — 24 boundary-related test references | **PARTIAL** — 5 boundary references |
| SessionManager | **PASS** — boundary tests for capacity, TTL | **PARTIAL** — some boundary coverage |

**Score: With skill 3/3, Baseline 0/3 (all partial)**

### A7: Complexity within limits (develop-code rule #2)

Functions under 50 lines, cyclomatic complexity under 10.

| Run | With Skill | Baseline |
|-----|-----------|----------|
| FuelRateLimiter | **PASS** — longest function ~30 lines, decomposed into mode handlers | **FAIL** — single `applyLimit()` method is ~95 lines with nested switch/if |
| TempController | **PASS** — all functions under 20 lines | **PASS** — also well-decomposed |
| SessionManager | **PASS** | **PASS** |

**Score: With skill 3/3, Baseline 2/3**

---

## Summary

| Assertion | With Skill | Baseline | Delta |
|-----------|-----------|----------|-------|
| A1: Coverage matrix | 3/3 (100%) | 0/3 (0%) | **+100%** |
| A2: Implementation notes | 3/3 (100%) | 1/3 (33%) | **+67%** |
| A3: No scope creep | 3/3 (100%) | 2/3 (67%) | **+33%** |
| A4: Immutable results | 3/3 (100%) | 2/3 (67%) | **+33%** |
| A5: Strategy-organized tests | 3/3 (100%) | 0/3 (0%) | **+100%** |
| A6: Systematic boundary tests | 3/3 (100%) | 0/3 (0%) | **+100%** |
| A7: Complexity limits | 3/3 (100%) | 2/3 (67%) | **+33%** |
| **TOTAL** | **21/21 (100%)** | **7/21 (33%)** | **+67%** |

## Key Observations

1. **The skills' strongest impact is on artifacts the model wouldn't produce unprompted:** coverage matrices (A1), strategy-organized tests (A5), and systematic boundary testing (A6) all show +100% delta. These are the V-model value-adds.

2. **Code quality is more subtle:** Both with-skill and baseline produce functional code. The differences are in discipline — immutability (A4), scope control (A3), complexity limits (A7). The baseline is "good enough" code; the skill produces "auditable" code.

3. **The baseline FuelRateLimiter is the most telling example:** It added `getPreviousRate()`, `reset()`, `pom.xml`, and `build.gradle` — none of which were in the design. The with-skill version contained exactly what was specified and nothing more. This is the "implement the design, not more" rule in action.

4. **Format independence works:** The skills performed equally well on Layer 2 structured designs (eval1), plain markdown (eval2), and Layer 1 component-level designs (eval3). No format-specific instructions were needed.

5. **Layer 1 handling:** Both skill and baseline handled the sparse Layer 1 design reasonably — they filled in reasonable assumptions. The skill version was more explicit about documenting those assumptions in implementation notes.
