# State and concurrency checks

Mirrors `state-and-concurrency.md` on the author side. Apply only when the State section has substantive content (i.e., the leaf is stateful).

## Contents

- `check.state.absence-not-asserted` (stateless leaves) and `check.state.transition-table-missing` (stateful)
- `check.state.invariant-per-state-missing`, `undefined-event-handling-unstated`, `terminal-states-unstated`
- `anti-pattern.state-explosion`, `anti-pattern.missing-cancellation`
- `check.thread-safety.*` (leaf category, shared field contract); `check.timing.unmeasurable`

## check.state.absence-not-asserted (soft)

**Check that** stateless leaves explicitly assert absence in one line.

**Reject when** the State section is empty OR missing entirely on a stateless leaf.

**Approve when** a stateless leaf has a one-line assertion ("Stateless between calls; all state lives in <where>.").

**recommended_action:** *"Add a one-line assertion of statelessness. Explicit absence is content; missing absence is a defect."*

## check.state.transition-table-missing (soft)

**Check that** every stateful leaf has a transition table with five columns: source, event, guard, action, target.

**Reject when** transitions are described in flat prose without the five-column structure, OR the table is partial (missing guards or actions).

**Approve when** the transition table is structured and complete.

**recommended_action:** *"Render transitions as a table with source / event / guard / action / target columns."*

## check.state.invariant-per-state-missing (soft)

**Check that** every named state has an invariant (what is true while the leaf is in that state).

**Reject when** states are named without invariants — names alone are not state semantics.

**Approve when** every state names an invariant.

**recommended_action:** *"Add a per-state invariant. A state without an invariant is just a name on a node."*

## check.state.undefined-event-handling-unstated (soft)

**Check that** the State section names what happens when an event arrives in a state where it is not in the transition table.

**Reject when** undefined-event handling is unstated.

**Approve when** the choice is named: ignore / log / fault / raise (or one explicit policy applied per state).

**recommended_action:** *"Name the undefined-event handling. Silence is dangerous — implementers will pick differently."*

## check.state.terminal-states-unstated (soft)

**Check that** the State section names initial and terminal states.

**Reject when** initial state is unstated, OR terminal states (if any) are unstated.

**Approve when** both are named.

**recommended_action:** *"Name initial and terminal states. The reader cannot trace lifecycle without these."*

## anti-pattern.state-explosion (soft)

**Check that** the state machine fits on a page or two; reviewers can reason about reachability.

**Reject when** the machine has dozens of states or hundreds of transitions; the diagram cannot be read.

**Approve when** the machine is decomposed into hierarchical states, OR split into sibling leaves.

**recommended_action:** *"Decompose the state machine. Use hierarchical states with substates, OR split the leaf so each sub-leaf carries a smaller machine."*

## check.thread-safety.leaf-category-unstated (soft)

**Check that** the leaf names a thread-safety category (Goetz taxonomy) when used across threads.

**Reject when** the leaf is multi-threaded but no category is named.

**Approve when** the category is one of: immutable / thread-safe / conditionally-thread-safe / thread-compatible / thread-hostile.

**recommended_action:** *"Name the thread-safety category. Silent assumptions become production defects."*

## check.thread-safety.shared-field-without-contract (soft)

**Check that** every shared mutable field names lock + happens-before + reader/writer.

**Reject when** a shared field has no synchronisation contract.

**Approve when** all three are named per shared field.

**recommended_action:** *"State the synchronisation contract per shared field. Cross-link to `data-and-invariant-checks.md`."*

## anti-pattern.missing-cancellation (soft)

**Check that** long-running operations have a cancellation contract.

**Reject when** an operation may run longer than the caller's patience and the contract specifies start and completion but not "can be asked to stop".

**Approve when** signal / cooperative-or-abrupt / state-after-cancel / what-caller-observes are all named.

**recommended_action:** *"Add a cancellation contract: signal, cooperative-or-abrupt, state-after-cancel, what caller observes."*

## check.timing.unmeasurable (soft)

**Check that** timing constraints state all five elements: type / numeric bound + unit / conditions / upstream requirement / verification mechanism.

**Reject when** a timing constraint is qualitative ("shall execute quickly") OR missing one of the five elements.

**Approve when** all five elements are present.

**recommended_action:** *"State the timing constraint with type, bound + unit, conditions, upstream requirement, and verification. Qualitative speed is not a constraint."*

## Cross-link

`anti-patterns-catalog.md` · `quality-bar-gate.md` (State card) · `templates/state-machine.mmd.tmpl`
