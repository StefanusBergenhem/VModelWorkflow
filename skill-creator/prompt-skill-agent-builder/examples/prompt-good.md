# Good prompt example

Target: Haiku 4.5. Task: extract structured data from a customer email.

```
You are a data extraction assistant.

<email>
{{EMAIL_TEXT}}
</email>

Extract the following fields from the email above. If a field is not present, output null — do not infer.

Output as JSON with this shape:
{
  "customer_name": string | null,
  "order_id": string | null,
  "issue_category": "billing" | "shipping" | "product" | "other" | null,
  "urgency": "low" | "medium" | "high" | null
}

Output the JSON only. No prose, no code fence.
```

## Why this is good

- Target model stated.
- Role is load-bearing (sets extraction mindset).
- Context delimited with XML tag.
- Task verb-first and names the deliverable.
- Output format is explicit and machine-parseable (enum values, nullable fields).
- "If not present, output null — do not infer" is a positive instruction that prevents hallucination without saying "don't hallucinate."
- No examples needed — JSON schema is unambiguous.
- No CoT scaffolding (Haiku extraction doesn't benefit).
