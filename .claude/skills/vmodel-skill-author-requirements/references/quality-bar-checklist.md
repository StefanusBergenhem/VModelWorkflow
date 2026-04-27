# Quality Bar — self-check before delivering

Yes/No checklist, grouped by concern. The document passes when every applicable item is answered Yes. The Spec Ambiguity Test at the end is the meta-gate: a document that ticks every box but cannot let a junior engineer or mid-tier AI derive defensible architecture, design, and tests fails regardless.

## Vocabulary discipline

- [ ] Is a Glossary section present and non-empty for every non-trivial document?
- [ ] Is every domain term used in a requirement statement defined in the glossary?
- [ ] Is there one word per concept and one concept per word within this scope?
- [ ] Are generic placeholder terms (Manager, Service, Handler, Record, Processor) audited out except where they name actual domain concepts?

## Requirement type clarity

- [ ] Is every requirement filed under the correct type section (functional / quality-attribute / interface / data / inherited-constraint)?
- [ ] Are NFRs in NFR form (not functional statements with an adjective) and functional requirements in functional form (not NFRs with a behaviour smuggled in)?
- [ ] Has level confusion been audited — does every requirement's scope match this document's scope?

## Statement-level quality

- [ ] Is every statement atomic (one `shall`, one behaviour)?
- [ ] Does every statement pass the box test (a tester can write the test from the statement and the glossary alone)?
- [ ] Is every statement solution-free (no named technologies, frameworks, libraries, data structures, or algorithms — except externally imposed protocols in interface requirements)?
- [ ] Is every state-driven (`While …`) requirement paired with its complementary out-of-state behaviour, or is the out-of-state case explicitly out of scope?
- [ ] Is structured language (EARS primary; GWT in `acceptance` blocks where useful) used consistently rather than mixed within a statement?

## NFR measurability — five-element rule

- [ ] Does every NFR name the **system or subsystem** specifically?
- [ ] Does every NFR name the **response or behaviour** being measured?
- [ ] Does every NFR give a **metric with unit**?
- [ ] Does every NFR give a **target value** at the correct statistical level (percentile where applicable, not raw mean)?
- [ ] Does every NFR state the **condition** (load, environment, operating mode, measurement point)?
- [ ] For tiered NFRs, is the Planguage form (`scale`, `meter`, `fail`, `goal`, `stretch`, `wish`) used rather than a single flat target?

## Interface contract completeness

- [ ] Does every interface requirement specify **protocol**, **message structure**, **timing**, **error handling**, **startup/initial state**?
- [ ] Are pre/post-conditions and invariants stated for each externally callable operation?
- [ ] Is a versioning and deprecation policy stated for every versioned interface?
- [ ] Are externally imposed protocols cited by specification (RFC, OIDC version, protocol draft) rather than informal name?

## Constraints discipline

- [ ] Does every inherited constraint cite its source (decision, regulation, contract, policy)?
- [ ] Does every inherited constraint name the cost of relaxing it?
- [ ] Is every inherited constraint categorised (technical / regulatory / organisational / financial / temporal)?
- [ ] For constraints with behavioural consequences at this scope, are derived requirements authored and cross-linked?

## Rationale — no fabrication

- [ ] Does every requirement carry a `rationale` field with non-trivial content, or an explicit `pending`/`unknown` marker?
- [ ] Is rationale captured at decision time (or, for retrofits, explicitly marked `unknown` where the original reasoning is lost)?
- [ ] Is rationale in retrofit mode marked `verified` or `unknown` only — never `reconstructed`?
- [ ] Are rationales audited for circularity (not "because test T passes") and laundering (not "because the current design is right")?

## Traceability completeness

- [ ] Does every requirement have non-empty `derived_from`?
- [ ] Does every derived requirement (those flagged `derivation: derived`) cite the introducing decision?
- [ ] Are governing decisions referenced in the front-matter and reflected in at least one requirement or derived requirement in the body?

## Inspection discipline

- [ ] Has the document been read from at least the **designer** and **tester** perspectives before delivering?
- [ ] Where a stakeholder-facing outcome is at stake, has the **user/stakeholder** perspective also been read?

## Retrofit honesty (retrofit mode only)

- [ ] Are behaviour fields marked `verified` (human-confirmed) or `reconstructed` (derived from code/tests/schemas)?
- [ ] Are rationale, open-alternatives, and intent fields marked `verified` or `unknown` only?
- [ ] Does every `unknown` field have a follow-up owner and action queued?
- [ ] Are `derived_from` links pointing to *observed evidence* (file:line, commit, operational log), not fabricated artifact names?

## Spec Ambiguity Test — meta-gate

- [ ] Could a junior engineer or mid-tier AI, reading only this document (plus its Glossary and governing decisions), derive a defensible architecture allocation to children, a detailed design for each leaf, and a test specification whose cases verify every requirement — **without asking clarifying questions**?

If the answer is No, the document under-specifies its translation role. Revise before declaring complete. **This test overrides every box above**: a document that passes all the other checks but fails this one has not done the job a requirements document exists to do.
