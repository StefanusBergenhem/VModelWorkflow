# Research 6b: AI for Architecture Analysis and Safety Analysis

Research for AI-at-system-level documentation. Covers what AI/LLMs can realistically
do for architecture analysis, STPA assistance, FTA/FMEA support, derived requirements
detection, and the regulatory landscape for AI as a development tool in safety-critical
domains.

This is "lighter" research synthesizing the current state of empirical evidence. The
honest finding: FMEA brainstorming is the most validated AI capability in safety
analysis; STPA assistance is promising but empirically thin; FTA is early-stage;
and the regulatory landscape has a glaring gap — no authority has published guidance
on AI as a development tool (as opposed to AI as a product component).

**Relationship to existing research:**
- 06a covers AI for requirements engineering (upstream)
- `ai-assisted-detailed-design.md` covers AI at the detailed design level (downstream)
- `concept-ai-assisted-design` in the codex covers design-level AI
- Research 4 (safety analysis methods) provides the safety domain context
- Research 5 (architecture) provides the architecture domain context

**Sources used:**
- [src-warwick-stpa-2025] "Safety Analysis in the Era of LLMs: STPA using ChatGPT." Machine Learning with Applications Vol. 19, 2025. https://www.sciencedirect.com/science/article/pii/S2666827025000052
- [src-stpa-chatgpt4-2024] "Hazard analysis in the era of AI: ChatGPT4 in STPA." Safety Science, 2024. https://www.sciencedirect.com/science/article/abs/pii/S092575352400198X
- [src-toronto-stpa-2025] "An LLM-Integrated Framework for STPA." arXiv:2503.12043, 2025. https://arxiv.org/html/2503.12043v1
- [src-safecomp-fta-2025] Shentu/Trapp — "Facilitating Fault Tree Analysis with Generative AI." SAFECOMP 2025 Workshops. https://link.springer.com/chapter/10.1007/978-3-032-02018-5_38
- [src-torc-fta-2024] "FTA generation using GenAI with an Autonomy sensor Usecase." arXiv:2411.15007, 2024. https://arxiv.org/html/2411.15007v1
- [src-lund-fmea-2025] "AI-driven FMEA: integration of LLMs." Design Science, Cambridge, 2025. https://www.cambridge.org/core/journals/design-science/article/22F110A2BF0DB4D01A69472CF17A0B43
- [src-dbw-fmea-2024] "Integrating LLMs for improved FMEA: drive-by-wire case study." Proceedings of the Design Society, 2024. https://www.cambridge.org/core/journals/proceedings-of-the-design-society/article/486CCE3DD5C2127697AAB864C6C89372
- [src-collier-risk-2025] Collier et al. — "How good are LLMs at product risk assessment?" Risk Analysis (Wiley), 2025. https://onlinelibrary.wiley.com/doi/10.1111/risa.14351
- [src-fmea-rag-2026] "A framework for automating FMEA using LLMs and RAG." Int. J. System Assurance, Springer, 2026. https://link.springer.com/article/10.1007/s13198-026-03171-6
- [src-icsa-trace-2025] "Enabling Architecture Traceability by LLM — Architecture Component Name Extraction." ICSA 2025. https://fuchss.org/assets/pdf/2025/icsa-25.pdf
- [src-archagent-2025] "ArchAgent: Scalable Legacy Software Architecture Recovery with LLMs." arXiv:2601.13007. https://arxiv.org/html/2601.13007
- [src-faa-roadmap-2024] FAA — "Roadmap for Artificial Intelligence Safety Assurance Version I." July 2024. https://www.faa.gov/aircraft/air_cert/step/roadmap_for_AI_safety_assurance
- [src-easa-npa-2025] EASA NPA 2025-07: AI Trustworthiness Detailed Specifications. https://www.easa.europa.eu/en/document-library/notices-of-proposed-amendment/npa-2025-07
- [src-easa-concept-2024] EASA AI Concept Paper Issue 2, March 2024. https://www.easa.europa.eu/en/document-library/general-publications/easa-artificial-intelligence-concept-paper-issue-2
- [src-iso-tr5469-2024] ISO/IEC TR 5469:2024 — "Functional safety and AI systems." https://www.iso.org/standard/81283.html
- [src-iso-pas8800-2024] ISO/PAS 8800:2024 — "Road Vehicles — Safety and Artificial Intelligence." https://www.iso.org/standard/83303.html
- [src-loonwerks-2025] Loonwerks — "Qualification Considerations of ML-Based Tools for Avionics." DASC 2025. https://loonwerks.com/publications/pdf/liu2025dasc.pdf
- [src-swedish-stpa-2025] "Improving System Safety in Aviation: Supporting STPA with AI Models." Swedish Aerospace Conference FT2025. https://ecp.ep.liu.se/index.php/ft/article/view/1178
- [src-hrc-stpa-2025] "Proactive safety reasoning in human-robot collaboration through LLM-augmented STPA and FMEA." Computers in Industry, 2025. https://www.sciencedirect.com/science/article/pii/S0736584525002169
- [src-faa-notice-2025] FAA Notice 1370.52 — Generative AI Tools and Services (internal staff policy). March 2025. https://www.faa.gov/documentLibrary/media/Notice/N_1370.52_Generative_AI_Tools_and_Services.pdf

---

## 1. AI-Assisted STPA

(Addresses Research 4 backlog input: "STPA has a highly structured process — can AI assist with generating control structures, enumerating UCAs, or checking constraint coverage?")

### 1.1 The Most Significant Empirical Study

The University of Warwick study (2025, peer-reviewed in *Machine Learning with Applications*) applied ChatGPT to two real systems — Automatic Emergency Brake (AEB) and Demand Side Management (DSM) — with human-expert baselines [src-warwick-stpa-2025].

**What AI was good at:**
- Loss scenario generation (brainstorming potential failure scenarios)
- Helping analysts understand the system
- Generating safety specifications from identified hazards

**What AI was bad at:**
- UCA generation — the core structured enumeration task. AI was *more conservative and less comprehensive* than human experts.
- Being used as a verification tool of human STPA results
- Applying causal STAMP reasoning without explicit guidance

**Key finding:** "Using ChatGPT without human intervention may be inadequate due to reliability issues." STPA-specific prompt engineering produced statistically more pertinent results than generic prompts, but prompting did not close the gap with human experts.

### 1.2 The UCA Enumeration Problem

STPA's UCA step is theoretically AI-tractable: for each control action, enumerate four types (provided causes hazard, not provided causes hazard, provided too early/late/wrong order, stopped too soon/applied too long). This is a structured, checklistable task.

The evidence says AI can enumerate candidates but:

1. **Misses context-dependent UCAs** that require understanding the actual control structure topology, not just the control action list
2. **Produces generic, over-broad UCAs** that don't map to real control structure constraints
3. **Cannot determine whether a UCA actually leads to a hazard** without deep system knowledge

A second study (Safety Science, 2024) compared ChatGPT-4 and Gemini on STPA: both demonstrated "weaknesses in systems thinking when used standalone" [src-stpa-chatgpt4-2024]. Neither applied causal STAMP reasoning without explicit guidance.

### 1.3 The Toronto Framework

An LLM-integrated framework from the University of Toronto (arXiv, March 2025) uses fine-tuned Llama 3.1-8B to extract losses/hazards/constraints from ConOps documents, with a verification/correction pipeline called BEDS [src-toronto-stpa-2025]. Open-source at github.com/blueskysolarracing/stpa. Claims "high degree of accuracy" but no specific precision/recall numbers were recoverable. Preprint, not peer-reviewed.

### 1.4 Honest Assessment

The 4-type UCA enumeration is AI-tractable as a **first-pass brainstorming tool** — generating candidates for human expert review. It is not validated as a standalone completeness check. No paper reports a verified miss rate (how many UCAs did AI miss vs. expert?).

STPA assistance is at **research prototype maturity**. The active work comes from Warwick, TUM, and Toronto — not MIT/Leveson's group directly, though MIT's STAMP Publications page lists the field's bibliography.

**For our framework:** An STPA assistance skill should generate candidate UCAs and loss scenarios for human review, not claim STPA completeness. The prompt engineering finding is important — STPA-specific prompts significantly outperform generic prompts, which means the skill's prompt design is load-bearing.

---

## 2. AI-Assisted FTA

### 2.1 The Co-Pilot Approach

Shentu and Trapp (SAFECOMP 2025 Workshops, TU Munich) explicitly chose **not** to generate complete fault trees from scratch [src-safecomp-fta-2025]. Instead, their tool acts as a co-pilot suggesting new sub-causes for existing partial trees. Applied to a Lane Keeping Assist System (LKAS). Specific accuracy numbers not publicly available, but the design choice itself is significant: the authors concluded that generating complete trees was unreliable and chose the more conservative architecture.

### 2.2 Generation from Scratch

Torc Robotics (2024) used open-source LLMs with prompt engineering to generate fault trees as PlantUML code for Lidar sensor failure scenarios, targeting ISO 26262 / PAS 21448 [src-torc-fta-2024]. Reports "promising results" for initial tests. No precision/recall numbers — the "promising" framing without specific metrics is a weakness.

### 2.3 The Software Blind Spot

(Addresses Research 4 backlog input: "The software blind spot in FTA/FMEA is exactly where AI could help.")

Traditional FTA models software failure as "undeveloped events" — black boxes at the bottom of the tree. This is the software blind spot that Research 4 documented. LLMs operating on code or requirements could theoretically expand those leaves:

- Analyzing source code for error paths that could produce the failure condition
- Cross-referencing requirements to find uncovered states
- Identifying common-cause software failures across redundant channels

**No published study addresses this undeveloped-event expansion problem.** This is an open research gap. It's conceptually the intersection of code analysis and safety analysis — two things LLMs can each do partially, but nobody has combined them for this purpose.

### 2.4 Honest Assessment

AI-assisted FTA is at **early research prototype stage**. The only validated use cases are: (a) generating initial tree structure from text, (b) suggesting sub-cause candidates for human review. Automated FTA that would serve as certification evidence has not been demonstrated.

---

## 3. AI-Assisted FMEA

FMEA is the most empirically rich area for AI in safety analysis.

### 3.1 The Core Finding: Brainstorming Works, Scoring Doesn't

Collier et al. (Risk Analysis, Wiley, 2025, peer-reviewed) evaluated ChatGPT across product risk assessment tasks including FMEA table construction: **LLMs performed better at divergent tasks (brainstorming failure modes, generating mitigations) than at convergent structured assessment tasks** (severity/occurrence/detectability scoring) [src-collier-risk-2025].

This pattern is consistent across studies:

- **Lund University (Design Science, 2025):** GPT-3.5/4/4o and Gemini on automotive vehicle failure modes (validated on ~18,000 reviews). "Significant improvements in speed, accuracy, and reliability" for failure mode identification [src-lund-fmea-2025]. But validation dataset is customer reviews, not engineering FMEA worksheets.

- **Drive-by-wire case study (2024):** LLMs assisted in exploring failure modes and recommending mitigations for a safety-critical automotive system [src-dbw-fmea-2024].

- **RAG-enhanced FMEA (2026):** Open-source LLMs with retrieval augmentation for "promising levels of automation and contextual accuracy" [src-fmea-rag-2026].

### 3.2 Why Brainstorming Works but Scoring Doesn't

Failure mode brainstorming is a **divergent enumeration task**: "what could go wrong?" LLMs excel at this because it maps to their strength — generating diverse, plausible completions from a prompt. The domain knowledge required is broad (many things can fail) rather than deep (how specifically does this thing fail in this context).

Severity/occurrence/detectability scoring is a **convergent judgment task**: "how bad is this specific failure in this specific system?" It requires:
- Quantitative understanding of failure rates (occurrence)
- System-specific consequence analysis (severity)
- Knowledge of the actual detection mechanisms in place (detectability)

These require deep, specific, quantitative knowledge that LLMs do not reliably have.

### 3.3 Honest Assessment

FMEA failure mode brainstorming is at **research prototype to early commercial** maturity (Fabasoft Approve markets AI-supported FMEA commercially). All studies require SME validation. No study reports that AI-only FMEA output would be acceptable as certification evidence.

**For our framework:** An FMEA assistance skill should focus on candidate failure mode generation and mitigation brainstorming, explicitly leaving scoring to human experts. The RAG approach (grounding in historical FMEA data from similar systems) appears to improve quality.

---

## 4. AI for Architecture Analysis

### 4.1 Architecture Traceability — The Strongest Area

Architecture traceability link recovery is the best-evidenced AI capability in this domain:

**ExArch / ArTEMiS (ICSA 2025):** Extracts architecture component names from Software Architecture Documents for traceability link recovery between architecture documentation and code [src-icsa-trace-2025]. Removes need for manual Software Architecture Mappings. The study found LLMs can identify component names and structural relationships with useful precision but "struggle with complex abstractions such as class relationships and fine-grained design patterns."

**ArchAgent (2025):** Combines static analysis, adaptive code segmentation, and LLM synthesis to reconstruct multi-view architectures from cross-repository codebases [src-archagent-2025]. Reports "significant improvements over existing benchmarks" with ablation study confirming cross-repository dependency context improves accuracy. The benchmark is other automated tools, not human-authored ground truth.

### 4.2 Anti-Pattern and Conformance Detection

Code smell detection at method/class level has moderate empirical support (iSMELL at ASE 2024 showed LLMs increase true positive rates vs. static analysis alone). Architecture-level anti-pattern detection (circular dependencies, god components, layering violations) has **vendor claims but no independent empirical evaluation** from tools like NDepend and Augment Code.

No peer-reviewed study from 2023-2026 evaluates LLM ability to detect architecture anti-patterns in safety-critical systems.

### 4.3 What AI Cannot Do at the Architecture Level

**Allocation trade-offs:** Determining whether a function belongs in SW, HW, or operational procedures requires multi-dimensional reasoning (cost, weight, power, timing, certifiability, maintenance) that is domain-specific and stakeholder-dependent. Not demonstrated by any AI system.

**Quality attribute analysis:** Architecture evaluation methods like ATAM and SAAM require stakeholder scenario walkthroughs and trade-off analysis. LLMs can structure scenarios but cannot make the trade-off judgments.

**Interface consistency at the safety level:** Verifying that interfaces between components correctly handle all failure modes, maintain required independence, and satisfy timing constraints requires quantitative analysis, not text generation.

---

## 5. Derived Requirements Detection

(Addresses Research 3 and 4 backlog inputs on the broken derived requirements feedback loop.)

### 5.1 The Open Gap

**No dedicated empirical study was found on AI detecting derived requirements created by design decisions.** This is the weakest area in the literature.

The LLM4RE systematic literature review (74 studies, 2023-2024) covers classification, completion, traceability, and specification generation — but not derived requirement identification [src-llm4re-slr referenced in 06a].

### 5.2 What It Would Take

Detecting derived requirements requires:
1. Understanding what the parent requirements specify (text comprehension — tractable)
2. Understanding what the design decided (text comprehension — tractable)
3. Identifying where the design introduces constraints, behaviors, or interfaces not traceable to any parent requirement (gap analysis — potentially tractable but untested)

The gap analysis step is structurally similar to "negative traceability" — finding things that *should* have a trace link but don't. The positive traceability evidence (Macro-F1 ~59% for recovery) suggests this is feasible at the "flag candidates for review" level.

### 5.3 Safety Impact Pre-Screening

The backlog question: can AI pre-screen derived requirements for safety relevance? This is a classification task: given a requirement with no parent trace link, does it relate to a safety function or mechanism?

No validated study exists. The general text classification evidence suggests this is feasible with high recall / low precision — AI would over-flag, which is acceptable in a safety context. The key risk is under-flagging (missing a safety-relevant derived requirement), which would be catastrophic.

---

## 6. The Regulatory Landscape: AI as Development Tool

### 6.1 The Core Gap

The entire regulatory landscape has a glaring blind spot: **no authority has published binding guidance on AI tools used during the development process** for safety-critical systems. All published guidance addresses AI as a product component (AI in aircraft, AI in vehicles), not AI as an engineering tool (LLM used to write requirements or generate test cases).

This is not a case of "the guidance exists but is incomplete." The guidance does not exist.

### 6.2 FAA Position

The FAA published the "Roadmap for Artificial Intelligence Safety Assurance Version I" in July 2024 [src-faa-roadmap-2024]. This is a **non-binding advisory** document — a strategic planning document, not a regulatory instrument.

Key points:
- Focuses primarily on AI *as airborne software*, not AI *as development tool*
- Acknowledges DO-178C/DO-330 "may support securing AI/ML software on the aircraft but will be insufficient for complete protection"
- The "Use of AI for Safety" area mentions leveraging AI to improve safety lifecycle processes — the closest the roadmap gets to development tools, but stops short of guidance
- A policy memo on "considerations for AI/ML used in development of airborne systems" was targeted for Q4 2024; as of April 2026, search results do not confirm it was published

FAA Notice 1370.52 (March 2025) governs FAA staff use of generative AI [src-faa-notice-2025]: all generative AI output used by FAA staff "must undergo human review for validity, accuracy, and completeness." This is operationally relevant (FAA reviewers might use AI to process certification data) but does not constitute guidance for industry.

### 6.3 EASA Position

EASA has been more prolific but equally focused on AI-as-product:

**Concept Paper Issue 2 (March 2024):** Extends the V-model to a "W-shape" for AI applications — adding an AI learning assurance arm alongside the development arm [src-easa-concept-2024]. Covers Level 1 (AI-assisted) and Level 2 (human-AI teaming). This is about AI *in the aircraft*.

**NPA 2025-07:** First formal regulatory proposal on AI trustworthiness, implementing EU AI Act requirements [src-easa-npa-2025]. Covers high-risk AI systems in aviation. Comment period closes June 2026. Again: about AI *as product*, not AI *as development tool*.

Neither document addresses AI-generated lifecycle data or tool qualification for LLM-based development tools.

### 6.4 ISO/IEC TR 5469:2024 — The Only Relevant Document

ISO/IEC TR 5469:2024 is the **only document found that explicitly scopes AI-as-development-tool** [src-iso-tr5469-2024]. Its scope includes: "use of AI systems to design and develop safety-related functions."

However, it is a **Technical Report (TR)** — informative, not normative. It describes what is known, not what is required. It maps the AI lifecycle (ISO/IEC 5338) to the functional safety lifecycle (IEC 61508) and identifies compliance gaps for probabilistic, non-deterministic AI tools. It does not resolve those gaps — it flags them.

### 6.5 ISO/PAS 8800:2024

ISO/PAS 8800 addresses AI in road vehicles, bridging ISO 26262 and AI-specific properties [src-iso-pas8800-2024]. It explicitly "does not provide specific guidelines for software tools that use AI methods." AI-as-development-tool is out of scope.

### 6.6 ARP6983/ED-324 (In Development)

SAE/EUROCAE Working Group WG-114/G-34 is producing ARP6983/ED-324 — "Process Standard for Development and Certification Approval of Aeronautical Products Implementing AI." Draft 5B consolidated. First approvals of Level 1 AI/ML systems expected by end of 2025. But this is about **AI in the product**, not AI tools used during development.

### 6.7 The Practical Implication

An LLM used to generate requirements, design, or test cases for a certified system would likely need tool qualification:
- Under **DO-330** for aviation (Criterion 1, 2, or 3 depending on how the tool output is used)
- Under **ISO 26262 Part 8, Clause 11** for automotive (Tool Confidence Level assessment)

No industry guidance exists on how to qualify non-deterministic AI tools for this purpose.

The only practically defensible path identified in the literature is **qualification by verification**: independently verify every AI output, reducing the tool to DO-330 Criterion 3 (output is independently verified → no qualification required). This is the pattern described in the codex as `pat-qualification-by-verification`. It is structurally sound but not authority-endorsed.

### 6.8 The Loonwerks Methodology

The closest published work to a formal qualification methodology for ML-based development tools is the Loonwerks 2025 DASC paper, which proposes qualifying low-criticality ML tools under DO-330 TQL-5 [src-loonwerks-2025]. It treats the ML tool as a black box. This targets DAL D/E equivalent — low criticality only. It has not been reviewed by a certification authority.

---

## 7. DO-178C Independence and AI Authorship

This is the most structurally consequential open question for our framework.

### 7.1 The Ambiguity

DO-178C requires that for DAL A and B software, the person verifying an artifact may not be the person who authored it. The standard's definition of "development" does not contemplate non-human authorship.

Three competing interpretations exist:

1. **AI is a tool, human is the author.** The human who prompts, reviews, and accepts the AI output is the author. A different human reviews. Independence satisfied. (Most common practitioner position.)

2. **AI is the author, human is independent by definition.** Since AI and the reviewing human are clearly different entities, independence is trivially satisfied. (Logically consistent but untested with authorities.)

3. **Tool qualification preempts the independence question.** If the AI tool is not qualified under DO-330, then the independence question is moot — the tool usage itself is non-compliant unless every output is independently verified (Criterion 3). (Most conservative reading.)

### 7.2 The Practitioner Consensus

Industry sources (AdaCore, AFuzion, eplaneai) converge on interpretation #1: "AI generates draft, human takes authorship by reviewing and approving, accountability is entirely with human engineers." This is **industry consensus opinion, not regulatory guidance.** No DER formal position or ACO acceptance memo has been published.

### 7.3 What This Means for Our Framework

Our framework already mandates human gates on every artifact. This is not just good practice — it is the only defensible position given the regulatory vacuum. The "AI as analyst, not author" framing (Thoughtworks) aligns with both the evidence and the regulatory reality:

- AI accelerates comprehension (66% reverse-engineering time reduction per Thoughtworks case study)
- Human engineers take authorship responsibility
- Independent review by a different human satisfies DO-178C independence
- The AI tool falls under Criterion 3 (output independently verified)

This is a defensible architecture. It is not authority-endorsed, but it is structurally sound against the existing framework.

---

## 8. What AI Demonstrably Cannot Do at This Level

### 8.1 Systems Thinking in STPA

Multiple studies confirm LLMs do not apply STAMP's control-theoretic reasoning without explicit scaffolding [src-warwick-stpa-2025] [src-stpa-chatgpt4-2024]. They process text patterns, not causal system models. They miss UCAs that require understanding *why* a control action in a specific context causes a hazard at the system level.

### 8.2 Safety Argument Construction

No empirical study demonstrates AI constructing a valid safety case (e.g., GSN argument structure) for a novel system. A plausible but incorrect safety argument is worse than no argument — it provides false assurance. Enterprise LLM hallucination rates make unreviewed safety argument text indefensible.

### 8.3 FDAL/IDAL and ASIL Decomposition Reasoning

(Addresses Research 4 backlog input: "FDAL/IDAL reduction and ASIL decomposition require genuine architectural independence.")

FDAL/IDAL assignment requires reasoning about independence, common-cause failure exposure, dissimilarity, and probabilistic safety targets. Peterson found that functional independence was NOT demonstrated at the specification level for SAAB-EII 100, even where hardware independence existed — common specification paths create common mode exposure [from Research 4]. These are judgment calls requiring architecture topology knowledge, failure independence evidence, and domain expertise. No AI system has demonstrated reliable reasoning about architectural independence.

### 8.4 FTTI Budget Validation

(Addresses Research 1 and 4 backlog inputs on timing constraints.)

Whether an architecture satisfies Fault Tolerant Time Interval budgets (FDTI + FRTI < FTTI - margin) requires quantitative analysis of worst-case execution times, latency chains, and communication delays. This requires specialized timing analysis tools (MAST, SymTA/S, or similar). LLMs cannot compute or validate these numbers. AI might assist in *parsing* architecture documents to identify timing paths, but the validation is a tool problem, not a language problem.

### 8.5 Completeness of Hazard Coverage

AI can enumerate hazards it "knows about"; it cannot certify that all hazards have been found. The miss rate for AI-generated UCAs and hazards has not been rigorously measured against known-complete baselines. This is the core certification problem: completeness arguments require evidence of exhaustive analysis, and current AI cannot support that argument.

---

## 9. Summary: Maturity Assessment

| Task | AI capability | Evidence quality | Maturity |
|---|---|---|---|
| STPA loss/hazard enumeration | Moderate — good candidates | 2-3 peer-reviewed | Research prototype |
| UCA generation (4 types) | Weak standalone | 2 empirical studies | Research prototype |
| STPA scenario generation | Moderate | Multiple studies | Research prototype |
| FTA co-pilot (suggest sub-causes) | Plausible, unquantified | 1 peer-reviewed | Research prototype |
| FTA generation from scratch | Early, unvalidated | 1 arXiv paper | Research prototype |
| FMEA failure mode brainstorming | **Best-evidenced** | 4+ peer-reviewed | Prototype → early commercial |
| FMEA scoring (S/O/D) | Weak | Implicit in studies | Not viable |
| Architecture trace recovery | Strong | 3+ peer-reviewed | Approaching commercial |
| Code smell detection (class level) | Moderate | 2+ peer-reviewed | Research prototype |
| Architecture conformance | Vendor claims only | No evaluation | Commercial (unvalidated) |
| Derived requirements detection | No validated work | None | **Open gap** |
| Safety argument construction | Not validated | No positive evidence | Not viable |
| FDAL/IDAL reasoning | Not demonstrated | No evidence | Not viable |
| FTTI budget validation | Not applicable | N/A | Not viable (needs tools) |

---

## 10. The Regulatory Summary

| Topic | Binding guidance exists? | Status |
|---|---|---|
| FAA on AI dev tools | No | Q4 2024 policy memo unconfirmed as published |
| EASA on AI dev tools | No | NPA 2025-07 is about AI-as-product |
| ISO/PAS 8800 on dev tools | No | Explicitly out of scope |
| ISO/IEC TR 5469 on dev tools | Partially (informative TR) | Only doc that scopes AI-as-dev-tool |
| ARP6983/ED-324 | No | About AI-in-product |
| DO-330 AI tool qualification | No guidance | Loonwerks 2025 proposes TQL-5 path |
| Independence + AI authorship | No | Active ambiguity; practitioner consensus only |

**The core reality:** The regulatory gap will not be filled soon. FAA policy memos are still being drafted. EASA's second NPA targets 2026. ARP6983 first approvals are end-2025, and that standard doesn't cover development tools. The "qualification by verification" pattern (every AI output independently reviewed → Criterion 3) is the only defensible path.

---

## 11. Implications for Our Framework

### Design principles for architecture-level and safety AI skills

1. **FMEA brainstorming is the most viable safety analysis skill.** Divergent enumeration of failure modes and mitigations — AI's strength — maps directly to the early phases of FMEA. Leave scoring to humans.

2. **STPA skills must be prompt-engineered.** The Warwick study shows STPA-specific prompts significantly outperform generic prompts. Skill design must embed STPA structure (4 steps, 4 UCA types, defined scenario categories) into the prompt, not leave it to the user.

3. **FTA co-pilot, not FTA generator.** The SAFECOMP 2025 design choice is instructive: suggest sub-causes for existing partial trees, don't try to generate complete trees.

4. **Architecture traceability is ready for use.** Component name extraction and trace link suggestion are at sufficient maturity for legacy retrofit assistance.

5. **The software blind spot is an unexplored opportunity.** Combining code analysis with FTA to expand "undeveloped events" at the bottom of fault trees is conceptually compelling and empirically untested. This could be a differentiator.

6. **Qualification by verification is our regulatory architecture.** Every AI output is independently reviewed by a human. The AI tool is Criterion 3 under DO-330. This removes the tool qualification burden while maintaining defense-in-depth.

7. **Never construct safety arguments with AI.** Hallucination risk is disqualifying. AI can gather evidence for a safety case; it cannot construct the argument.

8. **Derived requirements detection is an open research opportunity.** Nobody has built this. "Negative traceability" — finding design decisions that create requirements without parent links — is a gap our framework could address.

---

## Gaps and Honest Uncertainties

- **Warwick STPA study used ChatGPT at one point in time.** Model capabilities evolve. The findings represent a snapshot, not a permanent ceiling.
- **FMEA evidence is concentrated in automotive and consumer products.** Transfer to aviation (DO-178C context) is plausible but unvalidated.
- **The "qualification by verification" pattern is practitioner-derived.** No DER or ACO has published acceptance of this approach. It is logically sound against the DO-330 framework but has not been tested in a real certification program.
- **EASA NPA 2025-07 comment period closes June 2026.** The final guidance may differ from the NPA. Monitor this.
- **Loonwerks TQL-5 methodology targets low criticality only.** Extending to higher TQLs (DAL A/B) would require different evidence and has not been proposed.
- **No study has measured transfer from automotive traceability results to aviation.** Aviation requirements are typically longer, more formal, and more heavily cross-referenced than automotive. Results may differ.
