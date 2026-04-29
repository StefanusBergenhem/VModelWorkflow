# Prompt template

Fill each slot. Delete slots not used. Emit the result verbatim as the final prompt.

```
<!-- Target model: {{MODEL}} ({{EFFORT}}) -->
<!-- Optional persona: -->
You are {{PERSONA}}.

<!-- Context (inline small/static; otherwise slot) -->
<context>
{{CONTEXT}}
</context>

<!-- Task: verb-first, one sentence, names the deliverable -->
{{TASK}}

<!-- Output format: explicit structure, length bound -->
Output format: {{FORMAT}}
Length: {{LENGTH}}

<!-- Examples: 0, 1, or 3. Skip if format is obvious. -->
<example>
Input: {{EX_IN}}
Output: {{EX_OUT}}
</example>

<!-- Hallucination guard: include only if factual grounding is required -->
If the answer is not supported by the context, say "I don't know." Quote supporting lines before answering.
```
