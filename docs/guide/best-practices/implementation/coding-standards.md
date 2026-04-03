# Coding Standards: What They Are and Why You Need One

## Why Every Safety Standard Requires a Coding Standard

Every V-model safety standard — DO-178C, ISO 26262, ASPICE, IEC 62304 — requires (or strongly recommends) that a coding standard be defined and applied. Not a specific one, but *one that exists, is documented, and is verifiable*.

Why? Because programming languages allow you to write code that is technically valid but practically dangerous. A coding standard constrains the language to a safe, predictable subset.

| Standard | Requirement | Reference |
|----------|-------------|-----------|
| DO-178C | "Programming language with unambiguous syntax and clear control of data with definite naming conventions and constraints on complexity" | Section 11.8 |
| ISO 26262 | Language subsets ++ (highly recommended) at ALL ASIL levels | Part 6, Table 1, item 1b |
| ASPICE | Coding standards compliance verified under SWE.4 | SWE.4 BP.3 |
| IEC 62304 | "Coding standards should be used to specify a preferred coding style" | Section 5.5 |

The pattern is universal: **define what is allowed, what is prohibited, and verify compliance.**

---

## Components of a Coding Standard

A complete coding standard addresses six areas. The first three are about *what* the code looks like; the last three are about *what the code does*.

### 1. Naming Conventions

Consistent, unambiguous naming is required by every standard. This is not cosmetic — it's a safety concern. Misleading names cause misunderstanding, which causes bugs.

**Rules that matter:**

- **Names reveal intent.** `remainingFuelMass_kg` tells the reader everything. `rfm` tells them nothing. If a name requires a comment, it doesn't reveal its intent.
- **One word per concept.** If you call it `get` in one class, don't call it `fetch` in another and `retrieve` in a third — unless they mean genuinely different things.
- **Classes are nouns, methods are verbs.** `FuelCalculator.calculateConsumption()`, not `FuelCalc.doIt()`.
- **No encodings or prefixes.** Hungarian notation (`strName`, `iCount`) was useful when IDEs couldn't show types. That era is over.
- **Use domain vocabulary.** In aviation: `waypoint`, `flightLeg`, `barometricAltitude`. In automotive: `actuator`, `sensorFusion`, `diagnosticTroubleCode`. The code should read like the domain, not like computer science.
- **Searchable names.** Single-letter variables (`e`, `t`, `d`) are unsearchable. Acceptable only in tiny scopes (loop counters, lambdas).

**Example — before and after:**

```java
// Bad: what is d? what does 7 mean?
double d = t * 7;

// Good: intent is clear, constant is named
double weeklyDistanceKm = dailyDistanceKm * DAYS_PER_WEEK;
```

### 2. Code Structure and Style

Style rules make code visually consistent, reducing cognitive load during reviews.

**Rules that matter:**

- **Consistent indentation and formatting.** Use an automated formatter (Checkstyle, clang-format, Black, Prettier). Never debate formatting manually.
- **One concept per file.** One public class per file (Java convention). One module per file. Don't pack unrelated things together.
- **Consistent file organization.** Within a class: constants, fields, constructors, public methods, private methods. Always the same order.
- **Braces on control structures — always.** Even for one-liners. `if (x) return;` becomes `if (x) { return; }`. This prevents a class of bugs where someone adds a second line thinking it's inside the block.
- **Line length limits.** 100-120 characters. Long lines hide complexity and cause horizontal scrolling in reviews.

### 3. Complexity Constraints

Complexity limits are required by DO-178C (via coding standard) and highly recommended at all ASIL levels by ISO 26262 (Table 1, item 1a).

**What to limit:**

| Metric | Recommended Limit | Why |
|--------|-------------------|-----|
| Cyclomatic complexity | 10 per function | Above 10, the function has too many paths to test exhaustively |
| Nesting depth | 3-4 levels | Deep nesting is hard to read and easy to get wrong |
| Function length | 20 lines (target), 50 lines (hard max) | Long functions do too many things |
| File length | 200-300 lines (target), 500 lines (hard max) | Long files indicate mixed responsibilities |
| Parameter count | 3 (target), 5 (hard max) | Many parameters = the function needs too much context |

**Cyclomatic complexity explained:**

Cyclomatic complexity counts the number of independent paths through a function. Each `if`, `for`, `while`, `case`, `&&`, `||` adds one to the count.

```java
// Complexity = 1 (straight-line code)
double calculateArea(double radius) {
    return Math.PI * radius * radius;
}

// Complexity = 4 (3 branches + entry)
String classify(int score) {
    if (score >= 90) return "A";      // +1
    else if (score >= 70) return "B";  // +1
    else if (score >= 50) return "C";  // +1
    else return "F";
}
```

A function with complexity 15 has 15 paths. Testing all of them is expensive. More importantly, a developer reading the function must hold all 15 paths in their head simultaneously. This is where bugs hide.

**Enforcement:** Use static analysis tools — SonarQube, PMD, Checkstyle (Java), cppcheck/clang-tidy (C++), pylint (Python). These tools should run in CI, not just locally. A complexity violation should fail the build.

### 4. Language Subset (Prohibited and Restricted Features)

A language subset defines which language features are safe to use and which are prohibited or restricted.

**Why this matters:** Programming languages are designed for expressiveness, not safety. Features like pointer arithmetic, implicit type conversions, and dynamic memory allocation are powerful but error-prone. Safety standards require restricting the language to a subset where behavior is predictable.

**Common language subset standards:**

| Standard | Language | Domain | Key Characteristics |
|----------|----------|--------|-------------------|
| MISRA C:2023 | C | Cross-domain safety | 175 rules (mandatory + required + advisory) |
| MISRA C++:2023 | C++ | Cross-domain safety | Updated for C++17 |
| AUTOSAR C++14 | C++ | Automotive | Extended MISRA C++ for AUTOSAR |
| JSF++ AV | C++ | Aviation/defense | Created for F-35, very strict |
| CERT C/C++ | C/C++ | Security-focused | Secure coding recommendations |

**For languages without a formal safety subset** (Java, Python, Go, TypeScript), the equivalent is:
- A static analysis tool with a configured ruleset (SonarQube, SpotBugs, PMD, ESLint, golangci-lint)
- Explicit documentation of prohibited patterns
- Automated enforcement in CI

**Commonly prohibited patterns (language-general):**

| Pattern | Why Prohibited | Alternative |
|---------|----------------|-------------|
| Unrestricted pointer arithmetic | Buffer overflows, undefined behavior | Bounds-checked access, iterators |
| `goto` | Unstructured control flow, unmaintainable | Structured loops, early returns |
| Recursion without depth limits | Stack overflow risk | Iterative algorithms, explicit stack |
| Dynamic memory allocation after init | Fragmentation, allocation failures at runtime | Pre-allocated pools, stack allocation |
| Implicit type conversions | Silent data loss, precision errors | Explicit casts with range checks |
| Global mutable state | Hidden coupling, race conditions, test pollution | Dependency injection, immutable state |

**Commonly restricted patterns** (allowed with justification):

| Pattern | Restriction | When Allowed |
|---------|-------------|--------------|
| Reflection / dynamic dispatch | Performance unpredictable, bypasses type safety | Framework integration points only |
| Multi-threading / shared mutable state | Race conditions, deadlocks | With documented synchronization strategy |
| Exceptions across module boundaries | Exception safety is hard to verify | With documented exception contracts |
| Compiler-specific extensions | Non-portable | When target platform is fixed and documented |

### 5. Error Handling

Every standard expects consistent, documented error handling. DO-178C includes it in coding standard requirements (Section 11.8). IEC 62304 Class C explicitly requires fault handling verification (Section 5.5.4).

**Principles:**

- **Use exceptions, not error codes.** Error codes force callers into nested `if` checking. Exceptions separate the happy path from the error path.
- **Never return null.** Every null return is a `NullPointerException` waiting to happen. Return `Optional`, empty collections, or use the Null Object pattern.
- **Never pass null.** Functions should not accept null parameters. If absence is meaningful, use `Optional` as the parameter type.
- **Create informative error messages.** Include: what operation was attempted, what input caused the error, what the expected state was. `"Failed to parse configuration file '/etc/app.yaml': expected integer for 'port', got 'abc'"` — not `"Parse error"`.
- **Error handling functions do nothing else.** A function that handles errors should not also perform business logic. Separate them.
- **Fail fast.** Validate inputs at the boundary. Don't let invalid data propagate through multiple layers before failing.
- **Don't swallow exceptions.** An empty catch block (`catch (Exception e) { }`) is a bug in disguise. At minimum, log the exception and re-throw.

**Example — before and after:**

```java
// Bad: swallowed exception, null return, no context
public Config loadConfig(String path) {
    try {
        return parser.parse(readFile(path));
    } catch (Exception e) {
        return null;
    }
}

// Good: informative error, no null, specific exception
public Config loadConfig(String path) {
    String content = readFile(path);
    try {
        return parser.parse(content);
    } catch (ParseException e) {
        throw new ConfigurationException(
            "Failed to parse configuration file '%s': %s".formatted(path, e.getMessage()), e);
    }
}
```

### 6. Comments and Documentation

**When to comment (the "why", never the "what"):**

- Business rule context: `// Per DO-178C 6.4.2.2, robustness tests must cover out-of-range inputs`
- Warnings: `// Do not remove — hardware needs 50ms settle time after reset`
- Workarounds with references: `// Workaround for JDK-12345678, fixed in Java 19`
- TODO with ticket: `// TODO(JIRA-456): Replace with batch API when available`
- Public API contracts (Javadoc/docstrings) for libraries

**When NOT to comment:**

- Restating the code: `i++; // increment i` — noise
- Explaining bad naming — rename instead
- Commented-out code — delete it, version control remembers
- Change logs in code — that's what `git log` is for

**The rot problem:** Comments don't compile. When code is refactored, comments are often left behind, becoming actively misleading. Self-documenting code (meaningful names, small functions, clear structure) is the first priority. Comments supplement what code cannot express.

---

## Defining a Coding Standard for Your Project

A coding standard is a project artifact, not an afterthought. It should be:

1. **Documented** — in a versioned file, not tribal knowledge
2. **Approved** — before coding begins (this is an explicit requirement in DO-178C Section 5.3 and an ASPICE assessor expectation)
3. **Enforceable** — by automated tools where possible, by checklists where not
4. **Verifiable** — static analysis reports and code review records provide evidence
5. **Maintained** — updated when the team encounters patterns not covered by the original standard

**Minimum contents:**

```yaml
coding_standard:
  language: Java 17
  naming:
    conventions: Google Java Style Guide
    domain_glossary: docs/glossary.yaml
  formatting:
    tool: google-java-format
    enforced_in_ci: true
  complexity:
    max_cyclomatic: 10
    max_nesting: 4
    max_function_lines: 50
    max_file_lines: 500
    max_parameters: 5
  language_subset:
    static_analysis_tool: SonarQube
    ruleset: Sonar way (Java)
    additional_rules: docs/prohibited-patterns.md
    deviations_process: documented in code review record
  error_handling:
    strategy: exceptions (not error codes)
    null_policy: use Optional, never return null
    logging: SLF4J, structured format
  documentation:
    public_api: Javadoc required for all public methods
    comments: "why" only, no restating code
```

---

## Scaling by Assurance Level

Not every project needs the same rigor. The standards scale requirements by criticality:

| Aspect | Low Criticality (DAL D / ASIL A / Class A) | Medium (DAL C / ASIL B / Class B) | High (DAL A-B / ASIL C-D / Class C) |
|--------|---------------------------------------------|-------------------------------------|---------------------------------------|
| Coding standard | Required (can be lightweight) | Required (must be comprehensive) | Required (comprehensive + language subset) |
| Static analysis | Recommended | Required | Required (full ruleset, CI-enforced) |
| Complexity limits | Recommended | Required | Required (strictly enforced) |
| Code reviews | Self-review acceptable | Peer review required | Independent review required |
| Language subset | Recommended | Required | Required (formal: MISRA, CERT, etc.) |
| Deviations | Documented | Documented + justified | Documented + justified + approved |

---

## Sources

- RTCA DO-178C, Sections 5.3, 6.3.4, 11.8, Table A-5
- ISO 26262:2018, Part 6, Tables 1, 6, 9
- Automotive SPICE PAM 3.1/4.0, SWE.3, SWE.4
- IEC 62304:2006+AMD1:2015, Section 5.5
- Robert C. Martin, *Clean Code* (2008)
- Google Java Style Guide, MISRA C:2023, CERT C
