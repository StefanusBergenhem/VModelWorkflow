# Supporting questions — usage notes

Six questions for surfacing blind spots. Apply selectively, not mechanically. One or two well-chosen questions per product type is the right density. Read the question, the relevance signal, and the deferral note before deciding whether to ask.

---

## Q1 — Discoverability

**Question:** "How do users find this thing?"

**When to ask:** Consumer apps, developer tools distributed through marketplaces or package registries, products where user acquisition is part of the product's success. Skip for internal tools with a known, captive user base.

**What to listen for:** If the user hasn't thought about this, it often signals the product's boundary is under-specified (is distribution in-scope or out?). Discoverability often determines which onboarding flows are in-scope for the first slice.

**Deferral note:** If the user says "we'll figure that out later," capture as an open question: *"How users find and access the product is not yet decided."* Do not push.

---

## Q2 — Failure modes

**Question:** "What's the failure mode that matters most? Does graceful degradation matter?"

**When to ask:** Any product with uptime expectations, data integrity requirements, or users who depend on it for a workflow. Essential for infrastructure tools, APIs consumed by other systems, and any product where failure has downstream cost. Skip for pure offline tools or low-stakes utilities.

**What to listen for:** "It can't go down" without specifics is a signal to probe: *"What does a user experience look like when it does go down — do they lose work, hit an error, or see stale data?"* That probe surfaces whether the failure mode is primarily availability, consistency, or data-loss oriented — important framing for Requirements.

**Deferral note:** One-line note in Open questions (e.g., *"Failure mode and degradation strategy not yet decided"*). Redirect detailed treatment to Requirements.

---

## Q3 — Revenue / cost model

**Question:** "Who pays for this? Is there a business model, or is this cost-center infrastructure?"

**When to ask:** Commercial products, products with a pricing layer, products where monetization decisions affect feature scope (e.g., free tier vs paid features). Skip for internal tools, open-source utilities, or when the user confirms business model is out of scope.

**What to listen for:** Pricing model often constrains which users and which features are in-scope for the first slice. A freemium product and a direct-sale product have different scope boundaries.

**Deferral note:** One-line note in Open questions if not decided. Do not build a business-model section — one sentence under Open questions is the ceiling.

---

## Q4 — Success in 6 months

**Question:** "What does success look like in 6 months? What's the signal that this worked?"

**When to ask:** Any product where the user hasn't articulated a measurable outcome. Especially useful when the user's product description is abstract or aspirational. Skip if the user has already named concrete success signals during the base-question phase.

**What to listen for:** Vague answers ("people use it", "it helps the team") are a signal that the product's value hypothesis is fuzzy. That fuzziness is a legitimate open question — capture it rather than resolving it. Concrete answers (retention metric, specific task completion, cost reduction) are useful framing for downstream Requirements.

**Deferral note:** *"Success metric not yet defined"* — one line in Open questions.

---

## Q5 — Competition / replacement

**Question:** "Is there an existing thing this competes with or replaces?"

**When to ask:** When you don't know whether the product is net-new or a replacement for something already in use. Especially useful for internal tools (replacing a spreadsheet or a manual process) or products entering an established category.

**What to listen for:** Replacement products have an out-of-scope section that almost writes itself (the old workflow becomes explicitly out of scope). Competing products clarify the differentiation scope.

**Deferral note:** *"Competitive positioning not yet decided"* — one line in Open questions. Do not build a competitive-analysis section.

---

## Q6 — Riskiest assumption

**Question:** "What's the riskiest assumption about whether this works?"

**When to ask:** Any product where the core value proposition has not been validated. Particularly useful for new products, products in new markets, or products depending on a technical approach that hasn't been proven.

**What to listen for:** If the user can't name a risky assumption, they may not have thought about validation. That is worth noting as an open question — not as a criticism, but as a genuine gap. If they name one, it often surfaces the most important out-of-scope constraint (the assumption test is out of scope) or the most important first-slice driver (the assumption must be tested by the first slice).

**Deferral note:** *"Core validation assumptions not yet articulated"* — one line in Open questions.

---

## Application guidance

Choose questions based on product type:

| Product type | High-priority questions |
|---|---|
| Consumer app | Q1 (discoverability), Q4 (success signal), Q6 (riskiest assumption) |
| Developer tool / API | Q2 (failure modes), Q5 (competition), Q6 (riskiest assumption) |
| Internal / enterprise tool | Q3 (cost model), Q5 (replacement), Q2 (failure modes) |
| Infrastructure / platform | Q2 (failure modes), Q4 (success signal), Q3 (cost model) |
| Greenfield B2B SaaS | Q3 (revenue), Q5 (competition), Q4 (success signal) |

These are starting heuristics, not rules. Override if the user's context makes a different question clearly more relevant. Asking one highly relevant question is better than asking all six.
