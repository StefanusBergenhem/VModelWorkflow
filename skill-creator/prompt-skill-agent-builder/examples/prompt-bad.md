# Bad prompt example

Same task (extract from customer email), written poorly.

```
Hey, can you take a look at this email and pull out the important stuff? Be thorough and don't miss anything. Don't hallucinate. Think step by step about what's relevant. Give me a good summary.

Email: {{EMAIL_TEXT}}
```

## What's wrong

- **No target model stated** — can't calibrate CoT or length.
- **"Important stuff"** — vague, no schema, no field list.
- **"Be thorough," "good summary"** — vague adjectives, no numeric bounds.
- **"Don't hallucinate"** — negative-only, no positive counterpart. Model has no handle.
- **"Think step by step"** — prescriptive CoT; on 4.6/4.7 causes overthinking; Haiku extraction doesn't need it.
- **Email context at the bottom** — Anthropic guidance: long context at top, query at bottom. Here the context is short, but the query is under-specified.
- **No output format** — model will produce prose; downstream can't parse.
- **"Pull out" and "summary" contradict** — extraction vs. summarization are different tasks. Decompose.
