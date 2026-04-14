# Research 6a: AI for Requirements Engineering at the System Level

Research for AI-at-system-level documentation. Covers what AI/LLMs can realistically
do for requirements quality checking, validation, traceability, and completeness at
the system and SW requirements level — and what they demonstrably cannot do.

This is "lighter" research: it synthesizes the current state of empirical evidence
rather than producing deep craft guidance. The honest finding is that empirical
evidence is thin for safety-critical domains specifically, with most studies targeting
general software. The field is moving fast (136% publication increase in 2024 vs 2023
for LLM4RE), but the evidentiary base does not yet support strong claims about
AI reliability at the system level for certified systems.

**Relationship to existing research:**
- Lower V AI research exists in `research/detailed-design/ai-assisted-detailed-design.md`
  and `research/implementation/unit-test-ai-generation-quality.md`. This document covers
  the system level — different problems, different evidence base.
- Codex page `concept-ai-assisted-design` covers design-level AI. This document is upstream.
- Inputs accumulated from Research 1-4 (backlog) are addressed section by section.

**Sources used:**
- [src-gruber-llm-qa] Gruber et al. — "LLM-based requirements quality assessment." arXiv:2408.10886, 2024. https://arxiv.org/html/2408.10886v1
- [src-nlp4re-2022] Ferreting et al. — NLP Tools Comparison Study, NLP4RE 2022 / Alstom dataset. CEUR-WS Vol-3122. https://ceur-ws.org/Vol-3122/NLP4RE-paper-3.pdf
- [src-rubric-2015] Arora/Sabetzadeh — "Automated Checking of Conformance to Requirements Templates." IEEE TSE, 2015. https://www.semanticscholar.org/paper/cc448189d55612eb4215190d4b91de0be61f55be
- [src-tvr-2025] "Automotive System Requirements Traceability Validation and Recovery Through RAG." arXiv:2504.15427, 2025. https://arxiv.org/html/2504.15427v1
- [src-kit-refsq-2025] KIT — "Requirements Traceability Link Recovery via RAG." REFSQ 2025. https://publikationen.bibliothek.kit.edu/1000178589/156854596
- [src-bonner-incose-2024] Bonner et al. — "LLM-based approach to establish traceability between Requirements and MBSE." INCOSE Symposium 2024. https://incose.onlinelibrary.wiley.com/doi/abs/10.1002/iis2.13285
- [src-nasa-ai-trace-2025] NASA NTRS — "AI-Enhanced Requirements Traceability Using MBSE and LLMs for Complex Systems." 2025. https://ntrs.nasa.gov/citations/20250008721
- [src-intelligentse-2025] "AI for Requirements Engineering: Industry Adoption and Practitioner Perspectives." arXiv:2511.01324, IntelligentSE 2025. https://arxiv.org/html/2511.01324v3
- [src-norheim-2024] Norheim et al. — "Challenges in applying large language models to requirements engineering tasks." Design Science, Cambridge, 2024. https://www.cambridge.org/core/journals/design-science/article/1FC7666F0A0B4E7091D2D4B2D46321B5
- [src-llm4re-slr-2025] "LLMs for RE: A Systematic Literature Review." arXiv:2509.11446, 2025. https://arxiv.org/html/2509.11446v1
- [src-frontiers-re-2025] "Research directions for using LLM in software requirement engineering." Frontiers in Computer Science, 2025. https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1519437/full
- [src-hallucinations-hazards-2025] "From Hallucinations to Hazards: Benchmarking LLMs for Hazard Analysis." ScienceDirect, 2025. https://www.sciencedirect.com/science/article/pii/S0925753525002814
- [src-llm-revision-2026] "LLM Requirements Revision / Stakeholder Support." arXiv:2601.16699, 2026. https://arxiv.org/html/2601.16699v1
- [src-llmrei-2025] "LLMREI — automated requirements elicitation interview system." arXiv:2507.02564, 2025.
- [src-aerospace-llm-2025] "LLM Aerospace Manufacturing Expertise Evaluation." arXiv:2501.17183, 2025. https://arxiv.org/html/2501.17183v2
- [src-qvscribe] QRA Corp — QVscribe 2.10: Automated EARS Templating + INCOSE Compliance. https://qracorp.com/news/introducing-qvscribe-2-10-automated-ears-requirements-templating-incose-compliance/
- [src-icsme-ambiguity-2025] "Requirements Ambiguity Detection and Explanation with LLMs: An Industrial Study." ICSME 2025 Industry Track. https://conf.researchr.org/details/icsme-2025/icsme-2025-industry-track/8/
- [src-surgical-ambiguity-2025] LLM ambiguity detection in surgical instructions. arXiv:2507.11525, 2025. https://arxiv.org/html/2507.11525v1

---

## 1. The Reframe: Augmenting Scarce Engineering Judgment

The central question for AI at the system level is not "can AI write requirements?" but "can AI augment the scarce engineering judgment that safety standards depend on but don't supply?"

This reframe comes from a concrete observation: ARP 4754A, ISO 26262, and ASPICE all assume the availability of experienced engineers who can make judgment calls about completeness, allocation trade-offs, and safety implications. Peterson/NASA 2015 documented that this expertise has roughly a 25% training rate — three-quarters of the engineering workforce lacks the depth of experience these standards presume [unverified — Peterson 2015 primary source not located in this search; claim carried from Research 2 backlog notes].

The practitioner survey data supports this framing. A 2025 survey of 55 practitioners found that Human-AI Collaboration (HAIC) accounts for 54.4% of all AI-in-RE techniques, while full AI automation accounts for only 5.4% [src-intelligentse-2025]. The industry has already converged on "AI augments humans" rather than "AI replaces humans" — the question is *what specific augmentation tasks* have empirical support.

A 2026 user study found that participants rated LLM-revised requirements significantly higher than their own originals on alignment, readability, reasoning, and unambiguity. Critically, LLM revisions "often surfaced tacit details stakeholders considered important and helped them better understand their own requirements" [src-llm-revision-2026]. This is the most direct evidence that AI can function as a scaffolding tool for engineers who haven't internalized domain knowledge — exactly the engineering judgment augmentation the reframe calls for.

**What this means for our framework:** AI skills at the system level should be designed as *judgment amplifiers*, not *judgment replacements*. The human provides domain context, intent, and trade-off decisions. The AI provides systematic coverage checking, pattern validation, and consistency enforcement that humans do inconsistently under time pressure.

---

## 2. Requirements Quality Checking

### 2.1 The Pre-LLM Baseline

Before assessing LLM capability, we need the baseline. A 2022 NLP4RE workshop study evaluated four NLP tools (ARM, QuARS, RETA, RCM) on 180 industrial railway requirements from Alstom [src-nlp4re-2022]:

- **High recall, low precision** is the characteristic failure mode
- RETA achieved recall 0.98 but precision 0.41
- ARM and QuARS achieved precision 0.43
- These tools flag almost everything as ambiguous — practitioners drown in false positives

This is the pattern to beat: catching nearly every real issue, but burying it in noise.

### 2.2 LLM-Era Quality Checking

LLMs reproduce the same high-recall/low-precision pattern but add two capabilities classical NLP tools lack: **rationale generation** (explaining *why* something is flagged) and **improvement suggestions** (proposing a fix).

Gruber et al. (2024) tested Llama 2 (70B) on requirement quality assessment against ISO 29148 characteristics. Binary evaluation per quality characteristic plus rationale generation. Finding: "initial LLM precision may be low, recall is very high" — the same trade-off as pre-LLM tools [src-gruber-llm-qa]. A user study with SE participants found LLM rationales were rated helpful for trust.

An ICSME 2025 industry track paper on requirements ambiguity detection found LLMs demonstrate "proficiency in identifying linguistic and procedural ambiguities" using in-context learning on real industrial requirements [src-icsme-ambiguity-2025]. Precision/recall numbers not publicly available.

In an adjacent domain (surgical robot instructions), Llama 3.2 11B achieved procedural ambiguity recall of 0.80, with linguistic/critical type recall around 0.60 [src-surgical-ambiguity-2025]. Different domain, but the clearest published precision/recall data point found.

### 2.3 What This Means Practically

The evidence supports AI as a **first-pass quality filter** for requirements — catching issues that human reviewers miss under time pressure. The high-recall/low-precision trade-off is acceptable in safety-critical contexts where missing a real defect is worse than a false alarm. But the interface design must handle false positive fatigue: if every third flag is noise, reviewers will start ignoring flags.

The LLM advantage over classical NLP tools is the rationale: instead of "this requirement is ambiguous," the LLM says "this requirement uses 'appropriate' without defining the standard — consider specifying the ISO reference." That's actionable. Classical tools can only point; LLMs can explain.

**Gap:** No published study evaluates LLM quality checking on requirements written for DO-178C, ISO 26262, or ASPICE compliance specifically. All evidence is from general software engineering or industrial requirements without safety certification context.

---

## 3. EARS Pattern Validation and Conditional Completeness

(Addresses Research 3 backlog input: "EARS pattern validation and conditional completeness checking are rule-based tasks AI can augment.")

### 3.1 The Grammar-Based Approach (Solved Without AI)

EARS syntactic conformance checking was solved in 2015 without LLMs. Arora and Sabetzadeh built RUBRIC, a grammar-based BNF approach using JAPE pattern matching and the GATE NLP framework [src-rubric-2015]. It checks whether requirements conform to EARS templates (ubiquitous, event-driven, unwanted behavior, state-driven, optional feature). This is a solved problem for syntactic conformance — LLMs add nothing here.

### 3.2 Where LLMs Could Add Value

LLMs potentially add value for **semantic EARS quality** — questions that grammar checking cannot answer:

- Is the trigger event in an event-driven requirement actually a detectable system event, or is it vague? ("When the system detects an error" — what error? detected how?)
- Is the system response in a ubiquitous requirement testable? ("The system shall provide adequate performance" — against what measure?)
- In a state-driven requirement, is the state well-defined and reachable?
- For conditional completeness: given a set of state-driven requirements, are all states covered? Are there unreachable or contradictory state combinations?

These are semantic reasoning tasks that grammar checking cannot reach. LLMs with domain context (e.g., a ConOps document or state model) could potentially flag gaps. **No peer-reviewed study validates this capability.** Commercial tools like QVscribe 2.10 claim automated EARS templating with "AI-powered rewriting" [src-qvscribe], but without independent empirical evaluation.

### 3.3 Honest Assessment

EARS syntactic validation → use grammar-based tools, not LLMs. EARS semantic validation → plausible AI opportunity, empirically unvalidated. The conditional completeness checking from Research 3's backlog input is tractable in principle (enumerate states × events, check for coverage) but no one has built and tested it.

---

## 4. Requirements Validation Assistance

(Addresses Research 1 backlog input: "The validation gap is the most interesting AI opportunity.")

### 4.1 Can LLMs Simulate Perspective-Based Reading?

Perspective-Based Reading (PBR) uses three perspectives — designer, tester, customer — to review requirements. Each perspective surfaces different defect types. Shull/Rus/Basili 2000 reported PBR detects significantly more defects than ad-hoc review (the oft-cited ~35% figure comes from the companion Basili et al. 1996 paper).

**No published study tests whether LLMs can replicate PBR's multi-perspective approach.** This is a gap in the literature, not a negative finding — nobody has tried it. The conceptual argument is plausible: prompt an LLM to review a requirement as if it were a designer (can I build this?), tester (can I test this?), and customer (is this what I need?). Each pass would produce different concerns.

This is an **unstudied research gap and a potential differentiator** for our framework. If we build a skill that implements multi-perspective review and instrument its defect detection rate, we would be producing novel empirical data.

### 4.2 Scenario-Based Validation

An alternative validation approach: given a requirement and a ConOps or operational scenario set, can AI check whether the requirement is consistent with all scenarios? This is closer to what LLMs can do — cross-referencing text against text — but no validated study was found for safety-critical requirements.

The LLMREI system for automated requirements elicitation interviews achieved up to 73.7% of requirements elicited through AI-driven interviews [src-llmrei-2025]. The flip side: roughly 1 in 4 requirements are structurally unavailable to AI without human facilitation. Validation (checking existing requirements) is likely more tractable than elicitation (discovering new ones), but no direct measurement exists.

### 4.3 What AI Cannot Validate

The 2024 Norheim et al. study (MIT/RWTH Aachen, peer-reviewed) identifies shared challenge clusters for LLMs in RE, including that "NLP technology has long been seen as promising to increase RE productivity but has yet to demonstrate substantive benefits" [src-norheim-2024]. The study identifies that LLMs may produce different responses to the same requirements question when re-queried — non-determinism in a domain where reproducibility is a certification requirement.

---

## 5. Consistency and Traceability Checking

(Addresses Research 3 backlog input: "MOE/MOP/TPM consistency checking is a structured task well-suited to AI.")

### 5.1 Traceability Link Recovery — The Strongest Area

Requirements traceability is the most empirically mature AI application in requirements engineering. Multiple independent studies converge:

**TVR (2025):** RAG-based approach on real automotive requirements. Validation accuracy: 98.87%. Recovery correctness: 85.50%. Best model: Claude 3.5 Sonnet, Macro-F1 58.75% (lower than accuracy due to class imbalance). Baseline: LiSSA achieves Macro-F1 53.81% [src-tvr-2025]. This is the strongest published result.

**KIT/REFSQ 2025:** RAG approach with chain-of-thought prompting. Open-source models "comparable to proprietary" [src-kit-refsq-2025]. Peer-reviewed at the primary requirements engineering venue.

**INCOSE Symposium 2024:** Semi-automatic requirements-to-MBSE model link generation using embedding similarity plus LLM classification [src-bonner-incose-2024].

**NASA NTRS 2025:** AI-enhanced requirements traceability using MBSE and LLMs for complex systems [src-nasa-ai-trace-2025]. Signals NASA is actively evaluating this approach.

### 5.2 What These Numbers Mean

The distinction between validation (98.87%) and recovery (85.50% / Macro-F1 58.75%) is critical:

- **Validation** = "Is this existing trace link correct?" — a classification task. 98.87% is very strong.
- **Recovery** = "What should be linked to what?" — a search/matching task. 85.50% correctness means roughly 1 in 7 suggested links is wrong. Macro-F1 of 58.75% is more sobering — it means performance varies significantly across requirement types.

For legacy retrofit (our primary use case), recovery matters more than validation. A Macro-F1 of ~59% is useful as a starting point for human review — not as a final answer.

### 5.3 MOE/MOP/TPM Consistency

The NASA MOE/MOP/TPM triad (Measures of Effectiveness → Measures of Performance → Technical Performance Measures) creates a traceable chain from stakeholder value to verification. Checking consistency across this chain is a structured cross-referencing task: does every TPM trace to an MOP? Does every MOP trace to a MOE? Are the quantitative ranges compatible?

No published study addresses AI for this specific task. However, the traceability recovery evidence suggests this is tractable — it's a specialized form of hierarchical trace link validation. The structured, quantitative nature of TPMs (numbers with units) should make consistency checking easier than free-text traceability.

### 5.4 Important Degradation Finding

Research found that "ambiguity, inconsistency, and other requirement smells degrade LLM binary classification accuracy of trace links by up to 0.01 per 10% increase in smelly requirements, with semantic smells causing the largest decline." LLM traceability tools are only as good as the upstream requirements quality. Garbage in, garbage out — and this has been quantified.

---

## 6. Safety Requirements Completeness Checking

(Addresses Research 4 backlog input: "AI can cross-check system requirements against hazard analysis outputs to detect safety requirements that were never incorporated.")

### 6.1 The Opportunity

Safety analysis (FHA, HARA, STPA) produces safety requirements. These must be incorporated into the system requirements specification. In practice, this incorporation is often incomplete — the derived requirements feedback loop is "practically the most often skipped" step (Research 3 findings). AI could cross-check:

- Hazard analysis outputs → system requirements: for every identified hazard, is there a corresponding safety requirement?
- STPA controller constraints → requirements: for every constraint, is there a traceable requirement?
- ASIL/DAL assignments → requirement attributes: does every safety requirement carry the correct integrity level?

These are structured cross-referencing tasks, similar to traceability recovery. The TVR results [src-tvr-2025] suggest this is tractable.

### 6.2 The Evidence Gap

No published study directly evaluates AI cross-checking hazard analysis against requirements. The closest evidence is the general traceability recovery work applied to the specific artifact pair (hazard analysis ↔ requirements specification). This should work — it's the same underlying task — but it hasn't been validated.

### 6.3 What AI Cannot Do for Safety Completeness

AI cannot certify that the hazard analysis itself is complete. If the hazard analysis missed a hazard, the cross-check will pass — there's nothing to flag. Completeness of safety analysis requires domain expertise, operational experience, and accident/incident history that LLMs do not have reliable access to.

The "From Hallucinations to Hazards" benchmark (2025, peer-reviewed) tested 8 proprietary LLMs, 7 open-weight LLMs, and 4 VLMs on hazard identification: **no model scored above 70% on the Hazards Identification Test** [src-hallucinations-hazards-2025]. This is a load-bearing finding: LLMs cannot reliably identify hazards, so they cannot be trusted to verify hazard analysis completeness.

---

## 7. The Derived Requirements Feedback Loop

(Addresses Research 3 and Research 4 backlog inputs on derived requirements.)

Research 4 found that the derived requirements feedback loop is broken partly because it requires human judgment to classify derived requirements as safety-relevant or not. The backlog question: can AI pre-screen derived requirements for potential safety impact?

### 7.1 What Pre-Screening Would Look Like

When architecture or design creates a new requirement not traceable to a parent requirement, a pre-screening tool would:
1. Detect that the requirement is derived (no parent trace link)
2. Analyze whether it relates to a safety function, safety mechanism, or safety-relevant interface
3. Flag it for safety team review if yes

Step 1 is a traceability gap detection task — well within demonstrated AI capability. Step 2 is a classification task — requires understanding what "safety-relevant" means in the specific system context. Step 3 is trivial.

### 7.2 Evidence

No published study directly addresses AI for derived requirements screening. The general classification evidence suggests Step 2 is feasible at the "high recall, low precision" level — AI would flag many derived requirements for safety review, with some false positives. In a safety context, over-flagging is acceptable; under-flagging is not.

---

## 8. What AI Demonstrably Cannot Do at the Requirements Level

This section collects the negative findings — what has been tested and failed, or what is structurally impossible with current technology.

### 8.1 Capturing Stakeholder Intent (Tacit Knowledge)

Confirmed across multiple studies. LLMs cannot elicit what a stakeholder has not articulated. The LLMREI automated interview system elicited up to 73.7% of requirements — meaning roughly 1 in 4 requirements are structurally unavailable without human facilitation [src-llmrei-2025]. The missing 26% includes exactly the requirements that matter most: implicit assumptions, domain constraints, unstated safety expectations.

The practitioner survey finding reinforces this: "AI cannot effectively weigh political considerations, business implications, or resource constraints, leading to suggestions of technically optimal solutions that are politically unfeasible" [src-intelligentse-2025].

### 8.2 Domain-Specific Safety Judgment

The "From Hallucinations to Hazards" benchmark is definitive: no model scored above 70% on the Hazards Identification Test [src-hallucinations-hazards-2025]. The paper identifies that existing benchmarks have "inadequate coverage of safety-specific knowledge" and "limited evaluation of causal reasoning in technical contexts." LLMs cannot make safety judgment calls that require understanding failure physics, operational context, and regulatory implications.

In the aerospace domain specifically: when queried about titanium fastener surface treatment for Boeing 787, a leading LLM recommended "electroless nickel plating with 15-20µm thickness — violating three aerospace standards simultaneously" [src-aerospace-llm-2025]. Domain-specific hallucinations are not just wrong — they are wrong in ways that a non-expert reviewer cannot detect.

### 8.3 Making Allocation Trade-offs

Requirements allocation to SW, HW, and operational domains requires trade-off reasoning: cost, weight, power, timing, reliability, certifiability, maintenance. These trade-offs are multi-dimensional, stakeholder-dependent, and require understanding physical constraints. No AI system has demonstrated reliable allocation reasoning. The practitioner survey confirms: AI suggestions are "generic rather than product-specific" due to generalized training data [src-intelligentse-2025].

### 8.4 Consistency Under Re-Query

LLMs may produce different responses to the same requirements question when re-queried [src-norheim-2024]. In safety-critical domains where reproducibility is a certification requirement (DO-178C requires that verification results be reproducible), this non-determinism is a structural problem, not a tuning problem.

### 8.5 Distinguishing Requirements Levels

LLMs tend to mix stakeholder need, system requirement, and software requirement in the same output — not respecting the V-model hierarchy. This is a persistent finding across multiple studies but lacks clean quantification. For our framework, where level discipline is fundamental, this means AI-generated requirements always need human classification.

---

## 9. Summary: What's Empirically Established vs. Speculative

| Capability | Evidence | Best number | Honest assessment |
|---|---|---|---|
| Quality checking (syntax) | Pre-LLM NLP: industrial | Recall 0.98 / Precision 0.41 | Solved without AI |
| Quality checking (LLM, ISO 29148) | Preprint + user study | High recall / low precision | Adds rationale; same trade-off |
| EARS syntactic conformance | Peer-reviewed 2015 | "Robust and accurate" | Solved without AI (grammar) |
| EARS semantic quality | No study | — | Plausible, unvalidated |
| PBR multi-perspective review | **Not studied** | — | Open research gap |
| Traceability validation | Preprint, automotive | 98.87% accuracy | Strong for existing links |
| Traceability recovery | Preprint, automotive | Macro-F1 ~59% | Useful as starting point |
| Safety completeness cross-check | No direct study | — | Tractable (like traceability) |
| Hazard identification | Peer-reviewed benchmark | No model >70% | Not viable standalone |
| Engineering judgment augmentation | Preprint user study | Significant improvement | Real but limited |
| Tacit stakeholder knowledge | Multiple studies | ~27% not AI-elicitable | Hard limit |
| Allocation trade-offs | Practitioner surveys | — | Not viable |
| Full automation of RE | Practitioner survey | 5.4% of techniques | Industry consensus: no |

---

## 10. Implications for Our Framework

### Design principles for system-level AI skills

1. **AI as quality checker, not author.** The evidence supports AI reviewing human-written requirements, not generating them. Quality checking with rationale is the sweet spot.

2. **High recall is acceptable; low precision requires UX design.** False positives are manageable in safety-critical contexts (better safe than sorry), but the review interface must not cause alert fatigue.

3. **Traceability is the killer app.** RAG-based traceability recovery is the most mature capability. A skill that suggests trace links between requirements levels, flags orphans, and detects gaps would be immediately useful in legacy retrofit.

4. **PBR simulation is an unstudied differentiator.** Nobody has published controlled experiments on multi-perspective AI review. Building and instrumenting this would produce novel data.

5. **Safety completeness cross-checking is the logical next step.** Cross-referencing hazard analysis against requirements is structurally identical to traceability recovery. The evidence base for traceability makes this credible even without direct validation.

6. **Never claim completeness.** AI can find issues; it cannot certify their absence. Every AI-assisted quality check must be framed as "here's what I found" not "this is complete."

7. **Human gates are non-negotiable.** The hazard identification benchmark (<70% for all models) and the domain hallucination examples (aerospace standards violations) make unreviewed AI output indefensible for safety-critical requirements.

---

## Gaps and Honest Uncertainties

- **Peterson/NASA 2015 "25% training rate" claim:** Carried from Research 2 backlog. Primary source not located in this search. Should be verified before citing in documentation.
- **PBR defect detection improvement:** The "35% more defects" figure is attributed to Basili et al. 1996. The primary paper is not in the codex and was not found in this search. The number should be treated as approximate.
- **No safety-domain-specific quality checking study exists.** All LLM quality checking evidence is from general software or industrial (non-safety) requirements. The gap between "industrial requirements" and "DO-178C-compliant requirements" is unknown.
- **Traceability numbers are from automotive.** Aviation requirements may have different characteristics (longer, more formal, more safety content). Transfer of results is plausible but unvalidated.
- **EARS semantic validation is an educated guess.** The argument that LLMs can check semantic EARS quality is logical but entirely untested. It may turn out that LLMs cannot reliably distinguish between a vague trigger event and a precise one.
