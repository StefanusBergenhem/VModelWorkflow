# Requirement type classification — checks

Every requirement is filed under exactly one of five types. Misclassification silently weakens the document because each type has different rigor rules and different downstream consumers (allocation, test derivation, audit, contract).

## The five types

| Type | What it states | Sentence shape |
|---|---|---|
| **Functional** | What the system does in response to stimuli or in a given state | EARS event-driven, state-driven, ubiquitous |
| **Quality attribute (NFR)** | A measurable non-functional characteristic under specified load and environment | Five-element rule; Planguage for tiered targets |
| **Interface** | A contract with an external caller, dependency, or protocol peer | Five dimensions + DbC + versioning |
| **Data** | Format, retention, privacy class, integrity invariants | EARS for behavioural data rules; declarative invariants for structural ones |
| **Inherited constraint** | Bounds imposed from above or outside (parent decisions, regulations, organisational, financial, temporal) | Source citation + cost-of-relaxing + (often) derived requirements |

## Classification check — decision table

For every requirement, walk this table top to bottom; the first Yes determines the correct type. If the requirement is filed under a different type, emit a misclassification finding.

| # | Question | If Yes |
|---|---|---|
| 1 | Is the statement imposed from outside this scope (parent decision, regulation, contractual obligation, or organisational policy)? | **Inherited constraint** |
| 2 | Does the statement primarily specify a contract with an external caller, dependency, or protocol peer? | **Interface** |
| 3 | Does the statement primarily specify the format, retention, privacy, or integrity of data? | **Data** |
| 4 | Does the statement specify a measurable non-functional characteristic with a target and a condition? | **Quality attribute (NFR)** |
| 5 | Does the statement specify behaviour the system performs (in response to a trigger, in a state, as an invariant)? | **Functional** |

If none of 1–5 apply, the statement is misclassified or under-specified.

- **check_failed**: `check.type.misclassified`
- **severity**: `soft_reject`
- **evidence shape**: quote the statement, name the section it was filed under, name the section the decision table places it in
- **recommended_action**: *"Re-file under the correct type section. Re-check NFR / interface / constraint completeness rules for the new type."*

## Two recurring level-confusion errors

Both are common in AI-authored or LLM-translated requirements drafts.

### Error pattern 1 — NFR written as functional

Tells:
- Statement is filed in the Functional section but contains *fast, slow, scalable, available, secure, robust, performant, efficient* without a measurable target.
- Statement reads as "shall be \<adjective>".

```
"The system shall be fast."
"The session service shall be highly available."
"The application shall be secure."
```

- **check_failed**: `check.type.nfr-as-functional`
- **severity**: `soft_reject`
- **recommended_action**: *"Move to the Quality Attributes section. Apply the five-element rule from `nfr-five-elements-checks.md`."*

### Error pattern 2 — Design smuggled as functional

Tells:
- Statement is filed in the Functional section but names a specific technology, framework, library, data structure, or algorithm (outside externally imposed protocols).
- Reads as "shall use \<named tech>".

```
"The system shall use a distributed cache to store session tokens."
"The service shall use Redis with a 5-second TTL."
"The system shall persist sessions in a relational database."
```

This is a **hard-reject trigger** — it's also `anti-pattern.implementation-prescription` / `anti-pattern.requirements-smuggling-design` (see `anti-patterns-catalog.md`).

- **check_failed**: `anti-pattern.implementation-prescription`
- **severity**: `hard_reject`
- **recommended_action**: *"Move the design choice to an architectural decision (ADR). Replace here with the behavioural requirement the design choice was meant to ensure."*

## Same-scope discipline — level-confusion check

Every requirement in a document must apply to **this scope** (the document's frontmatter `scope` value). Parent-scope concerns belong as upstream `derived_from` references; child-scope concerns belong in child documents.

### Tells of level confusion

- Statement uses a term that is more granular than this scope (e.g., a session-service requirements document containing a statement about a specific module's internal queue).
- Statement uses a term broader than this scope (e.g., a session-service document containing a statement about platform-wide audit policy).
- Mixed-scope statements within the same section ("the platform shall …" alongside "the session service shall …" in a session-service document).

- **check_failed**: `check.type.level-confusion`
- **severity**: `soft_reject`
- **evidence shape**: quote the offending statement; name the scope it actually applies to
- **recommended_action**: *"Move the statement to the correct scope's document. If the parent-scope concern is upstream context, capture it as `derived_from` rather than as a requirement here."*

## Section-presence checks

A complete requirements document has all five typed sections, even if some are empty:

- Functional Requirements
- Quality Attributes (NFRs)
- Interface Requirements
- Data Requirements
- Inherited Constraints

An empty section is acceptable (with a one-line note explaining why no requirements of that type exist for this scope) — but a *missing* section may indicate the author skipped a type that should be present.

- **check_failed**: `check.type.section-missing`
- **severity**: `info`
- **recommended_action**: *"Add the missing section header, or note explicitly why this scope has no requirements of that type."*
