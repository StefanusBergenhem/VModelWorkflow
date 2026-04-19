# Pre-Pivot Archive (2026-04-18)

This directory preserves artifacts from the original safety-focused V-model design:
- HW/SW split borrowed from aviation / automotive standards
- Safety assurance levels (DAL A–E, ASIL A–D, IEC 62304 class, SIL) as primary rigor axis
- Tier-based scaling of rigor proportional to consequence severity
- Stakeholder Needs, Concept of Operations, and Completeness Analysis as separate top-level artifacts

The pivot (2026-04-18) removed safety as the primary concern and replaced tier-based rigor with uniform high rigor enforced via per-artifact Quality Bar checklists. Stakeholder Needs, ConOps, and Completeness Analysis are folded into a new root-level **Product Brief** artifact.

Files in this archive are preserved for:
- Historical reference — why earlier decisions were made.
- Reuse if safety or tiered rigor is reintroduced later.
- Craft-knowledge extraction — reusable content is re-homed in the new artifact docs; these originals are superseded.

For the full pivot summary, see `status.md` in this directory.

## Concept mapping (old → new)

| Old concept | New location |
|---|---|
| Stakeholder Needs (separate artifact) | Product Brief §3 (Stakeholders, Problem, Outcomes) |
| Concept of Operations (separate artifact) | Product Brief §4 (Operational Concept) |
| Completeness Analysis (separate artifact) | Product Brief preamble + discipline folded into Quality Bar |
| Assurance levels (DAL / ASIL / SIL / IEC 62304 class) | Removed; uniform high rigor via Quality Bar |
| HW/SW split | Removed; generic software |
| Tier-based rigor scaling | Removed; Quality Bar applies uniformly |
| System Requirements / SW Requirements (separate layers) | Requirements at each non-leaf scope in the scope tree |
| System Architecture / SW Architecture | Architecture at each non-leaf scope |
| SW Detailed Design | Detailed Design (at leaf scopes only) |
| — | **New: Product Brief** (root only) |
| — | **New: TestSpec** (every scope — unit / integration / system by layer) |
| — | **New: ADR** (cross-cutting) |
