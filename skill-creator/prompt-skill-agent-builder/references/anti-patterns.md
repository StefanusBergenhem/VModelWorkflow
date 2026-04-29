# Anti-patterns (self-review checklist)

Run this checklist against any generated artifact. Report findings in chat with file:line references. Do not auto-fix.

## Universal (all three types)

- [ ] Vague adjectives without numeric bounds ("brief," "detailed," "thorough").
- [ ] Negative-only rules ("don't X") not paired with "do Y instead."
- [ ] Time-sensitive phrasing ("currently," "as of 2025," "the new API").
- [ ] Multiple responsibilities bundled (look for "and" in the scope statement).
- [ ] Re-explaining fundamentals the target model already knows (violates prime-don't-teach).
- [ ] Alternatives dumps — >1 option offered where a default + one escape hatch would do.
- [ ] Prescriptive chain-of-thought scaffold on a 4.6/4.7 target (overthinking risk).
- [ ] Prefill usage on Anthropic 4.6+ (deprecated; use Structured Outputs).
- [ ] Missing eval scenarios / no claim of measurable uplift on Haiku.
- [ ] Implementation intentions missing — rules stated as general maxims rather than "When X, do Y."

## Prompt-specific

- [ ] No target model stated.
- [ ] No explicit output format.
- [ ] No length bound.
- [ ] >3 examples (over-mimicking risk).
- [ ] Examples contradict stated format.
- [ ] Context dumped inline when it should be slotted.

## Skill-specific

- [ ] Frontmatter: name >64 chars, contains "anthropic"/"claude", not lowercase-hyphenated.
- [ ] Frontmatter: description >1024 chars, missing *what* or *when*, not third-person.
- [ ] SKILL.md >500 lines.
- [ ] References nested >1 level deep from SKILL.md.
- [ ] Reference file >100 lines without table of contents.
- [ ] Description lacks trigger keywords users would actually say.
- [ ] No HALT conditions.
- [ ] Scripts present for tasks prose could handle (punt → solve check).

## Agent-specific

- [ ] Tool allowlist uses wildcards without justification.
- [ ] No max-attempts bound on loops.
- [ ] No typed handover artifact.
- [ ] No retry-discipline rule (each retry must differ).
- [ ] No root-cause-tracing trigger after N failures.
- [ ] Destructive actions not gated by confirmation.
- [ ] Done-signal is vague (prose, not a typed/measurable condition).
- [ ] Compaction defaulted for long runs instead of fresh-context strategy.

## How to report

For each box checked, emit one line:
```
[anti-pattern name] — <file>:<line or section> — <one-line observation>
```

End with a single summary line:
```
Self-review: <N> findings. Address before shipping.
```

If zero findings:
```
Self-review: clean.
```
