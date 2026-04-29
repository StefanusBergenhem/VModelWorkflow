# Evals for prompt-skill-agent-builder itself

These scenarios test the meta-skill's own behavior: does it produce better artifacts than a model without the skill loaded?

## How to run

1. Load the skill.
2. Run each scenario from `scenarios.md` twice: once with the skill active, once without.
3. Score against the scenario's success criteria.
4. Pass bar: ≥2 of 3 scenarios show measurable uplift on Haiku 4.5.

## Success definition

Uplift = with-skill output meets criteria AND without-skill output fails them.
