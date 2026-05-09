# Language detection — vmodel-init

## Detection table

Scan the project root for the following marker files in order. First match wins.
For Java/Kotlin, check for both `pom.xml` and `build.gradle` / `build.gradle.kts`.

| Marker file(s)                                  | Detected language     |
|-------------------------------------------------|-----------------------|
| `package.json`                                  | typescript (default; check `main`/`types` fields; if absent assume ts) |
| `go.mod`                                        | go                    |
| `Cargo.toml`                                    | rust                  |
| `pyproject.toml` / `requirements.txt` / `setup.py` | python             |
| `pom.xml`                                       | java                  |
| `build.gradle` / `build.gradle.kts`             | java (or kotlin if `.kts` or `kotlin` in build file) |
| `*.csproj` / `*.sln`                            | csharp                |

**Multiple markers present:** report all detected and ask at Checkpoint 1
which is the primary language. Note secondary languages — they may warrant
`components` overrides in config (see schema `components` section).

**No marker found:** set language to `"other"` and leave all command fields
as `""`. Do not guess.

---

## Default command suggestions per language

Use these values as suggestions at Checkpoint 4. Show evidence alongside
each suggestion (the marker file that drove the detection).

### go

| Field              | Suggested value                                 |
|--------------------|-------------------------------------------------|
| `test_unit`        | `go test ./...`                                 |
| `test_integration` | `go test -tags=integration ./...`               |
| `test_system`      | `""` (not standard — leave empty)               |
| `lint`             | `golangci-lint run`                             |
| `build`            | `go build ./...`                                |
| `coverage`         | `go test ./... -coverprofile=coverage.out`      |

### python

| Field              | Suggested value                                 |
|--------------------|-------------------------------------------------|
| `test_unit`        | `pytest`                                        |
| `test_integration` | `pytest -m integration`                         |
| `test_system`      | `""` (not standard — leave empty)               |
| `lint`             | `ruff check .`                                  |
| `build`            | `""` (most Python projects don't have a build step) |
| `coverage`         | `pytest --cov`                                  |

Note: if `requirements.txt` only (no `pyproject.toml`), prefer `pytest` for
test and check for `flake8`/`pylint` in requirements before suggesting `ruff`.

### java

| Field              | Suggested value                                 |
|--------------------|-------------------------------------------------|
| `test_unit`        | `mvn test` (or `./gradlew test` if Gradle)      |
| `test_integration` | `mvn verify -P integration` (or `./gradlew integrationTest`) |
| `test_system`      | `""` (not standard — leave empty)               |
| `lint`             | `""` (suggest checkstyle/pmd if detected in build descriptor) |
| `build`            | `mvn package` (or `./gradlew build`)            |
| `coverage`         | `""` (suggest jacoco if detected in build descriptor) |

Gradle detection: if `build.gradle.kts` exists, prefer `./gradlew` prefix.
Maven detection: if `pom.xml` exists and no `build.gradle`, use `mvn`.

### kotlin

Same as java, substituting `./gradlew` as primary and noting `.kts` files.

| Field              | Suggested value                                 |
|--------------------|-------------------------------------------------|
| `test_unit`        | `./gradlew test`                                |
| `test_integration` | `./gradlew integrationTest`                     |
| `test_system`      | `""`                                            |
| `lint`             | `./gradlew ktlintCheck`                         |
| `build`            | `./gradlew build`                               |
| `coverage`         | `""`                                            |

### typescript / javascript

| Field              | Suggested value                                 |
|--------------------|-------------------------------------------------|
| `test_unit`        | `npx vitest run` (if `vitest` in devDeps); else `npm test` |
| `test_integration` | `""` (not standard — leave empty unless detected) |
| `test_system`      | `npx playwright test` (if `playwright` in devDeps); else `""` |
| `lint`             | `npx eslint .`                                  |
| `build`            | `npm run build`                                 |
| `coverage`         | `npx vitest run --coverage` (if vitest); else `npx jest --coverage` (if jest); else `""` |

Additional sniff: read `package.json` `devDependencies` for `vitest`, `jest`,
`playwright`, `cypress`, `eslint`. Adjust suggestions accordingly.

### rust

| Field              | Suggested value                                 |
|--------------------|-------------------------------------------------|
| `test_unit`        | `cargo test`                                    |
| `test_integration` | `cargo test --test '*'`                         |
| `test_system`      | `""`                                            |
| `lint`             | `cargo clippy`                                  |
| `build`            | `cargo build`                                   |
| `coverage`         | `""` (tarpaulin or llvm-cov not always present — leave empty) |

### csharp

| Field              | Suggested value                                 |
|--------------------|-------------------------------------------------|
| `test_unit`        | `dotnet test`                                   |
| `test_integration` | `dotnet test --filter Category=Integration`     |
| `test_system`      | `""`                                            |
| `lint`             | `dotnet format --verify-no-changes`             |
| `build`            | `dotnet build`                                  |
| `coverage`         | `dotnet test --collect:"XPlat Code Coverage"`   |

### other (unknown language)

All command fields: `""`. Do not guess. Inform the user at Checkpoint 4:
"Language not auto-detected — command fields left empty. Fill in manually."
