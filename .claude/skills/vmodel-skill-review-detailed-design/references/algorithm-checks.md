# Algorithm checks

Mirrors `algorithms.md` on the author side. The hard-reject triggers (refusal C) are flagged ★.

## anti-pattern.code-paraphrase (HARD ★ refusal C)

**Check that** the Algorithms section does not walk through the implementation step-by-step.

**Reject when** every clause is derivable from reading the implementation (the DD is the code in another notation), OR pseudocode tracks variable names and loop control flow with no abstraction lift.

**Approve when** the section either states result properties (when the algorithm is implementer's choice) OR names a contractual algorithm with a stated reason (determinism / worst-case / operational / wire-compatibility).

**Evidence pattern:** quote the paraphrasing clause; note the absence of any element the code would not show.

**recommended_action:** *"Replace pseudocode-paraphrase with result-property statements (refusal C). The DD specifies what must be true; the code specifies which implementation was chosen."*

## check.algorithm.contractual-without-reason (soft)

**Check that** when the algorithm is named (rather than left to the implementer), the reason is stated.

**Reject when** the DD names a specific algorithm without naming why ("Use mergesort" without rationale).

**Approve when** the reason is named: determinism / worst-case bound / operational constraint / wire compatibility, with a citation where applicable.

**recommended_action:** *"Either name the reason the algorithm is contractual (with citation) OR state the result property and leave the algorithm to the implementer."*

## check.algorithm.too-vague (soft)

**Check that** algorithm specifications are specific enough that a test engineer can derive tests.

**Reject when** the section reads "the function processes the data" or "computes the result" without a property specification.

**Approve when** the result property is stated; tests are derivable.

**recommended_action:** *"State the result property concretely (Rule 2 — specificity). Vagueness breaks test-derivability."*

## check.algorithm.pattern-mismatch (soft)

**Check that** the specification pattern fits the behaviour shape.

**Reject when** rule-based logic is described in flat prose (decision table would be appropriate); mode-dependent behaviour is described without state machine; multi-step protocol is described without numbered sequence.

**Approve when** the form fits the shape.

**recommended_action:** *"Use the form that makes the behaviour reviewable: decision table for rule-based; state machine for mode-dependent; numbered sequence for protocols."*

## check.algorithm.decision-table-incomplete (soft)

**Check that** decision tables partition the input space (the rule masks union to exhaust 2^N or product space; no overlapping rules).

**Reject when** the table has gaps in coverage OR overlapping rules without conflict resolution.

**Approve when** the table is complete and unambiguous.

**recommended_action:** *"Complete the table by adding rules covering the missing input combinations, OR reduce overlapping rules."*

## check.algorithm.sequence-without-invariants (soft)

**Check that** numbered-sequence specifications carry per-step invariants (what holds between steps).

**Reject when** the sequence is just a list of actions with no invariant statements.

**Approve when** each step has an invariant naming what is true after that step.

**recommended_action:** *"Add per-step invariants. Reviewers must be able to walk 'what state is the leaf in if step N fails'."*

## Cross-link

`anti-patterns-catalog.md` (#5 algorithmic-postcondition is in function-contract-checks; #13 code-paraphrase is here) · `quality-bar-gate.md` (Algorithms card) · refusal C in `SKILL.md`
