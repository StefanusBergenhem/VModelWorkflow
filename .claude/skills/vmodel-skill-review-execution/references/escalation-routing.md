# Escalation Routing

Full `target_layer` × `issue_type` routing table. Used by review-execution when writing `ESC-NNN.yaml` and mirrored in orchestrate-build's escalation-routing.md (orchestrate-build reads this table to decide how to route the file it receives).

---

## §1 Routing Table

| Pipeline position | Failure type | `target_layer` | `issue_type` | Who acts on the escalation |
|:-----------------|:-------------|:--------------|:------------|:--------------------------|
| Leaf review | Test assertion contradicts DD contract | `testspec` | `wrong-assertion` | TestSpec author (revision to testspec) |
| Leaf review | DD ambiguous — multiple valid impls disagree on observable behaviour | `detailed-design` | `ambiguity` | DD author (sharpen postcondition or add constraint) |
| Leaf review | DD contradictory — no impl can satisfy all postconditions | `detailed-design` | `contradiction` | DD author (resolve contradiction) |
| Leaf review | DD correct but contradicts a governing ADR | `adr` | `new-decision-needed` | ADR author or human principal (new or revised ADR; DD then follows) |
| Leaf review | DD requires a decision not yet captured in any spec layer | `adr` | `new-decision-needed` | ADR author or human principal |
| Branch review | ARCH interface contract inconsistent or missing | `architecture` | `contract-violation` | Architecture author (revise Composition/Interface section) |
| Branch review | ARCH correct; specific child DD inconsistent with interface it must implement | `detailed-design` | `contradiction` | DD author of the named child scope |
| Branch review | Branch TestSpec case asserts wrong interface behaviour | `testspec` | `wrong-assertion` | TestSpec author (branch scope) |
| Branch review | Integration failure traces to undocumented cross-cutting decision | `adr` | `new-decision-needed` | ADR author or human principal |
| Branch review | Ambiguous — unclear if ARCH or impl is the source | `architecture` | `ambiguity` | Human (orchestrator surfaces; do not auto-route) |
| Root review | Root requirement outcome unachievable or internally contradictory | `requirements` | `contradiction` | Requirements author |
| Root review | Root requirement outcome not covered by any system test | `testspec` | `gap` | Root TestSpec author |
| Root review | Root product need (PB/needs/PD) not translated into any requirement | `product` | `gap` | Product author or human principal |
| Root review | Failure traces to a cross-cutting architectural pattern, not a missing requirement | `architecture` | `new-decision-needed` | Architecture author or human principal |
| Root review | Root TestSpec case asserts an outcome contradicting a root requirement | `testspec` | `wrong-assertion` | Root TestSpec author |
| Any layer | Irresolvable ambiguity after applying decision tree | nearest in-lane target | `ambiguity` | Human (always surface with `confidence: low`) |

---

## §2 `target_layer` Enum

Valid values (schema-enforced in `ESC-NNN.yaml`):

```
detailed-design
testspec
architecture
adr
requirements
product
```

---

## §3 `issue_type` Enum

Valid values:

```
ambiguity          — spec is under-specified; multiple valid interpretations exist
gap                — something that should be present is absent
contradiction      — two spec elements are mutually exclusive
new-decision-needed — a decision is needed that no existing ADR captures
contract-violation  — a contract is stated but the impl or a downstream spec violates it
wrong-assertion    — a test assertion is incorrect relative to the governing spec
```

---

## §4 `target_artifact` Resolution

When `target_layer` identifies a specific artifact, set `target_artifact` to the artifact's id from its YAML front-matter.

| `target_layer` | `target_artifact` source |
|:--------------|:------------------------|
| `detailed-design` | `id` from the DD's front-matter (e.g., `DD-auth-token-validator`) |
| `testspec` | `id` from the TestSpec front-matter (e.g., `TS-auth-leaf`) |
| `architecture` | `id` from the ARCH front-matter (e.g., `ARCH-auth-service`) |
| `adr` | `id` from the ADR front-matter, or `"new"` if a new ADR is needed |
| `requirements` | `id` from the requirements front-matter |
| `product` | `id` from the product artifact front-matter |

If the artifact's id is not known (e.g., a new ADR is needed), use `"new"` as the value and describe the needed artifact in `required_action`.

---

## §5 Orchestrator Consumption

The orchestrator reads `target_layer` from `ESC-NNN.yaml` to:

1. Mark the affected task as `escalated`.
2. Propagate `blocked` to dependent tasks (per dep strength).
3. Surface to human if `confidence: low` or `medium` (unless `build.auto_route_medium: true`).
4. Auto-route `confidence: high` escalations: present the ESC file path + `required_action` to the relevant author skill (review-execution does not dispatch the author skill; orchestrate-build does this on resume after human confirmation or autonomously if policy allows).

---

## §6 ESC Sequence Numbering

ESC files live in `.vmodel/.build/escalations/`. The sequence number `NNN` is zero-padded to 3 digits.

To pick the next number:
1. List `.vmodel/.build/escalations/ESC-*.yaml`.
2. Parse all `NNN` values.
3. `next_NNN = max(NNN) + 1`, or `001` if the directory is empty.

If two concurrent tasks attempt to write the same NNN, HALT for the second task and report the collision to the orchestrator. The orchestrator retries with the next available sequence.
