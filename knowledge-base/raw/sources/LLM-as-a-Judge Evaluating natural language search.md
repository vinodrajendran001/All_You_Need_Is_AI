---
title: "LLM-as-a-Judge: Evaluating natural language search"
source: "https://careersatdoordash.com/blog/doordash-llm-as-a-judge-evaluating-natural-language-search/"
author:
  - "[[Xiaochang Miao]]"
  - "[[Heather Song]]"
published: 2026-05-15
created: 2026-05-28
description: "How DoorDash uses LLM-as-a-judge to evaluate natural language search, replacing noisy human labels with scalable, facet-based AI evaluation."
tags:
  - "clippings"
---
Traditional food delivery search matches keywords such as "pizza," "sushi," or restaurant name. This works well when users know exactly what they want. However, a meaningful share of search sessions encode intent that cannot be captured by tokens alone:

- *Vibe/mood:* "Cozy date night dinner," "something light and refreshing"
- *Contextual situations:* "Quick lunch near the office under $15," "food for a sick friend"
- *Discovery:* "Surprise me," "Something I haven't tried"
- *Multi-constraint:* "Gluten-free fast spicy affordable"
- *Multi-constraints with dish names*: “Pizza under $20,” “top-rated beef noodle bowl in 30 min.”

These queries describe a situation or a product with multiple requirements. The user isn't naming a cuisine or a store; they're expressing an intent that requires the search engine to understand meaning, not match tokens.

DoorDash's natural language search (NLS) closes this gap. It’s an LLM-powered pipeline that rewrites vague intent into structured retrieval queries, retrieves candidates via semantic embeddings, and ranks results by relevance.

Building such a system, however, created a harder problem: How do you evaluate whether "cozy date night dinner" returns the correct results? There's no click-through ground truth for a query that never existed in your logs. Traditional search metrics such as click-through rate and null rate, are lagging and noisy. Human annotation is the obvious answer until it isn't.

NLS became the catalyst for rethinking evaluation end-to-end. Our solution: Replace periodic human annotation cycles with a calibrated LLM judge that runs continuously. Here we describe how we built that system and what we learned about measuring search quality at scale.

## Motivation: When manual labeling becomes the bottleneck

Evaluation speed acts as a gate to NLS iteration speed. Every change to query rewriting, retrieval, or ranking needs a quality signal before shipping. We needed to evaluate query-store relevance across structured queries ("spicy cheap tacos"), fuzzy queries ("comfort food for a rainy day"), and compositional queries (“vegan under $20”) that blend multiple constraints.

We initially relied on human annotation, but that was too slow. Each evaluation cycle required anywhere from two to five days for turnaround, and training contractors to apply a multi-constraint rubric consistently took weeks of calibration and guideline revision. Relevance for natural-language intent is contextual, which increases inter-annotator disagreement and introduces label inconsistency.

To quantify the impact, we followed the standard playbook: Train a supervised relevance model on the human-labeled data. We fine-tuned a Qwen3-based reranker and observed an area under the curve (AUC) of 0.56 on a held-out set — a stat that ranks barely above random. The model architecture wasn't the problem; the labels were. This motivated a systematic audit of the human labels.

## Diagnosis: Label noise and rubric–intent mismatch

To understand whether this model underperformance was driven by architecture or supervision quality, we ran a parallel evaluation: The same query–store pairs were graded by both human annotators and an LLM judge, in this case OpenAI’s o3-mini. We intentionally avoided heavily engineered rubrics at this stage and used only the base evaluation criteria to measure how the two “default” interpretations diverged.

The initial audit immediately suggested a label-quality issue. Among 35 manually reviewed cases, human ratings were incorrect in 19 after cross-functional adjudication. This was not an isolated pattern. As shown in Table 1, we saw misalignment rate across 6,824 total query-store judgments.

![](https://careersatdoordash.com/wp-content/uploads/2026/04/image-23-1024x532.png)

Figure 1: Human evaluation label vs. misalignment rate between human raters and adjudicated relevance. The chart shows that disagreement is relatively low for clearly relevant results, but rises sharply for boundary cases such as mostly relevant, partially relevant, and irrelevant. The key takeaway is that label noise is concentrated near ambiguous decision boundaries, which makes supervised relevance training unstable

The key signal is where the noise concentrates: Disagreement exceeds 30% for “mostly relevant,” “partially relevant,” and “irrelevant” judgments, which are exactly the boundary cases that carry the greatest learning signal for ranking models. Label noise near the decision boundary is precisely what causes supervised relevance training to collapse into contradictions rather than stable patterns.

- *Modifier equivalence blindness:*For "baked wings," human raters scored a pizza chain at 0.5 (partially relevant). The menu lists oven-roasted chicken wings, functionally an equivalent to “baked.” The LLM caught that equivalence; the human didn't. PM adjudication: 1.0 (fully relevant). Similarly, for "baked mac n cheese," a comfort food chain that offers an entire “mac & cheese” menu section was rated 0.5 by humans. PM adjudication: 1.0.
- *Undefined subjective terms:* For "healthy vegan," raters marked a vegan burger-and-fries restaurant as fully relevant — defaulting to "vegan = healthy." The LLM flagged that fried items don't align with a health-oriented query. For "fast healthy wings," a human rated a Hawaiian bowl restaurant at 1.0, but the store only carries cauliflower wings — not what most consumers mean by "wings." PM adjudication: 0.0 (irrelevant). The S&O team noted: "Cauliflower wing is not a common reference for wings."
- *Inconsistent threshold and menu-depth application:* For "best quick spicy burger," a human rated a San Francisco-based low-carb-gluten-free restaurant at 1.0 despite a 4.69 rating (below the 4.7 "best" threshold in the rubric) and a menu that's primarily bowls, not burgers. The LLM flagged both issues. For "vanilla coffee," a human rated a neighborhood cafe at 1.0, but when we scrolled the full menu, there was no vanilla coffee or vanilla syrup option, only a "vanilla milk." The LLM correctly rated it irrelevant.

| **Query** | **Store** | **Human** | **LLM** | **Adjudicated** | **What happened** |
| --- | --- | --- | --- | --- | --- |
| baked wings | Pizza store | 0.5 | Relevant | 1.0 | Oven-roasted = baked; human missed equivalence |
| healthy cheap tacos | Taco store | 0 | Relevant | 1.0 | Multiple affordable veggie tacos; human scored irrelevant |
| fast healthy wings | A healthy salad bowl store | 1.0 | Not relevant | 0.0 | Only cauliflower wings — not real wings; human over-rated |
| baked salmon | Bento store | 1.0 | Not relevant | 0.8 | Has salmon but not baked; human missed preparation method |
| keto noodles | Hot pot store | 0 | Relevant | — | Menu has shirataki noodles (keto-friendly); human missed it |
| vanilla coffee | A cafe | 1.0 | Not relevant | 1.0 | Menu has “vanilla milk,” not vanilla coffee — edge case where PM and LLM disagreed |

*Table 2: Representative examples of disagreement between human annotators and the LLM judge, with adjudicated outcomes. These cases illustrate the main failure modes in manual labeling, including missed synonym equivalence, subjective modifier interpretation, inconsistent thresholding, and incomplete menu inspection. The table shows that many disagreements were driven by rubric ambiguity or missing evidence, not simply by judge error.*

## Root cause: Random error and rubric–intent mismatch

The audit surfaced two interacting causes of label noise: Human error/inconsistency and a rubric that underspecified how to judge compositional natural-language intent. At scale, annotators experience occasional misses, such as in menu depth or synonyms, but the larger issue is inconsistency — implicit heuristics for subjective modifiers such as “healthy” or “fast” and variable strictness on constraints like time, price, or rating.

This is amplified in NLS because queries are rarely simple dish keywords. Instead, they encode multiple constraints and modifier semantics. Relevance therefore behaves like a joint satisfaction problem across facets, and when the rubric does not make those facets explicit, raters are forced to improvise, which makes disagreement systematic rather than exceptional.

The core issue is supervision quality — specifically a rubric that forced both humans and LLMs to improvise on boundary cases. When the rubric doesn't specify how to weigh "healthy" against "fast" against "affordable," disagreement isn't annotator error; it's a measurement gap. The cleanest signal comes from making evaluation criteria explicit enough that any competent rater — human or LLM — would converge.

This aligns with the LLM’s G-EVAL finding: Evaluation reliability improves when criteria are explicit and the judge follows structured steps rather than producing unconstrained scores. The insight is not that LLMs are better judges. It's that decomposing intent into concrete, evidence-based checks reduces variance for any evaluator.

## Identifying binary facets key to design

The audit showed the bottleneck wasn’t “humans vs. LLM,” but the measurement interface. A multi-grade relevance scale (e.g., 0/0.5/0.8/1.0) looks nuanced, but the intermediate buckets are hard to reproduce. The boundary between “partially” and “mostly” relevant is rarely anchored to objective evidence, so minor interpretational differences shift scores without a clear notion of error. This instability affects both humans and LLM judges.

To reduce degrees of freedom and make disagreements diagnosable, we reframed relevance as multiple discrete checks over intent facets, then aggregated those outcomes into an overall judgment. This aligns with a broader evaluation pattern: LLM-as-a-judge becomes more reliable when criteria are explicit, structured, and “form-fillable,” and when complex judgments are decomposed into simpler sub-decisions rather than collapsed into a single opaque score.

### Defining facets

Facet design matters as much as judge selection. The facet set should reflect what actually drives user-perceived search quality, while continuing to remain stable and measurable:

- *User-grounded*: Facets represent distinct aspects of the consumer experience such as “core match” vs. “modifier/constraint satisfaction,” not internal implementation details.
- *Independent and minimally overlapping*: Each facet tests one capability so failures are attributable; overlap double-counts evidence and blurs diagnosis (see Pydantic’s post [LLM-as-a-Judge: A Practical Guide with Pydantic Evals](https://pydantic.dev/articles/llm-as-a-judge) for more details).
- *Evidence-based*: Each check should be answerable from query + observable store/menu signals, not inferred preferences or “vibes.”
- *Right level of specificity*: Avoid both brittle hard-coded exception lists and overly general “is this a good match?” prompts. Structured rubric guidance improves repeatability.

With facet-based rubrics, we can calibrate the judge against adjudicated consensus, tune prompts at the facet level, and operationalize evaluation as a continuous signal – offline benchmarks + regression guardrails – rather than a periodic, subjective labeling exercise, as shown in Figure 3.

![](https://careersatdoordash.com/wp-content/uploads/2026/04/image-26.png)

Figure 3: Shift from a single multi-grade relevance score to binary facet-based evaluation. The left side shows the old setup, where a query-store pair received one ambiguous overall score; the right side shows the new setup, where relevance is decomposed into independent checks such as dish match, modifier match, and constraint satisfaction before being aggregated. The reader should take away that binary facet evaluation reduces ambiguity, lowers variance, and makes failures easier to debug and optimize.

## Architecture in three phases

We built a three-phase system that starts with human judgment, calibrates an LLM judge against it, then automates execution, as shown in Figure 4.

![](https://careersatdoordash.com/wp-content/uploads/2026/04/image-24-1024x683.png)

Figure 4: Three-phase LLM-as-a-judge evaluation workflow: foundation, calibration, and execution. The diagram shows how the system begins with sampling and rubric definition, creates an adjudicated golden set, tunes the LLM judge to match that standard, and then operationalizes the judge through daily monitoring and pull-request guardrails. The key message is that reliable LLM evaluation requires not just a judge model, but an end-to-end workflow for calibration, monitoring, and re-calibration over time.

### Phase 1: Define rubrics

The initial rubric asked annotators subjective, open-ended questions – "How relevant is this store to the query?" – on a four-graded relevance level without defining what "relevant" means. For a query such as "healthy cheap tacos," raters had to simultaneously judge dietary alignment, price, and cuisine match, with no guidance on how to weigh each factor or what threshold counts as "cheap." Different raters applied different implicit heuristics, producing the noise we measured in the diagnosis.

Product managers, the strategy and operations team, and engineers collaboratively redesigned the rubric by decomposing single vague questions into independent binary checks, each targeting one constraint, answerable from observable menu and store data

Before: "Rate the relevance of this store to the query 'healthy cheap tacos' on a scale of 0 to 1."

After:

- "Does this store serve tacos or a close equivalent?" (Yes/No)
- "Does this store offer items under $12?" (Yes/No)
- "Does this store offer health-conscious options — salads, grilled items, low-calorie choices?" (Yes/No)

For a fuzzy query like "cozy date night dinner," the decomposition makes implicit expectations explicit:

- "Does this store's cuisine type fit a date-night setting?" (Yes/No)
- "Does this store have dinner-appropriate items (not just coffee or snacks)?" (Yes/No)
- "Is the store's average rating above 4.5?" (Yes/No)

Each binary question leaves little room for interpretation. After switching to decomposed rubrics, variance between LLM judges and human annotators dropped significantly; the decomposition removed the ambiguity that was driving most of the disagreement.

Human annotators grade a representative set of query-store pairs using these binary questions, producing a golden dataset that serves as the calibration target.

### Phase 2: Calibrate the loop

The LLM judge grades the same golden set. We measure alignment against adjudicated human consensus, not individual rater labels, which we've established are noisy. When the judge diverges, we iterate by adjusting the prompt, enriching the context (menu metadata, store attributes), or refining the rubric itself.

Calibration often reveals rubric flaws, not just judge flaws. When the judge consistently disagrees with humans on a specific pattern – for example, modifier equivalence – we investigate whether the rubric needs to be updated rather than assuming the judge is wrong.

### Phase 3: Automate execution

Once calibrated, the judge runs in two parallel tracks:

- *Production monitoring:* Live search traces flow through daily LLM judge grading. Results populate a quality dashboard with standardized metrics such as NDCG@5 or per-facet precision to give the team a daily read on search quality without waiting for human evaluation cycles.
- *Pull-request-level guardrails:* When an engineer opens a pull request that touches the search pipeline, the system deploys the change to a sandbox, replays a standard query set, and runs side-by-side comparison between control and treatment. The LLM judge provides comparison reasoning and a pass/fail signal — a quality gate that catches regressions before they ship.

When evaluation criteria change – such as a new facet, updated threshold, or refined weighting – we version the rubric and re-run calibration against the golden set. Historical metrics remain comparable because each data point is tagged with its rubric version.

A key benefit of this architecture is that the judge returns not just a score but a rationale. When a metric drops, the trace-level reasoning points directly to why — whether the regression is in core match, modifier interpretation, or constraint satisfaction. This makes failures actionable in a way that aggregate metrics never could.

## When the evaluation broke

While the architecture diagram suggests a clean pipeline, there were three distinct evaluation failures — each a different category of error — that forced fundamental changes to the rubric, the judge, and the product itself.

- *Compounded metrics hid real failures*: Our initial evaluation used an overall normalized discounted cumulative gain (NDCG) score per query. For multi-faceted queries, this blended performance across all facets into a single number. An example: Our results for the query "gluten free fast spicy affordable" showed stores that perfectly matched the dietary and price requirements but uniformly failed on speed. Because we aggregated NDCG across all queries tagged "dietary," the speed failure dragged down the dietary score. As a result, we were debugging a dietary problem that didn't exist.The solution was to evaluate each facet independently. Per-facet NDCG revealed the real performance landscape, as shown in Figure 5.
![](https://careersatdoordash.com/wp-content/uploads/2026/04/image-27-1024x502.png)

Figure 5: Per-facet search quality measured by NDCG@5 across relevance dimensions. The chart shows that cuisine, price, flavor, and dietary understanding were relatively strong, while location and especially speed lagged far behind. The main takeaway is that per-facet evaluation exposes specific product and system gaps that would be hidden by an aggregate relevance metric.

The cuisine and price segments were strong. Speed and location were broken; the per-facet breakdown made the root causes immediately actionable. Location failed because the pipeline lacked real-time geolocation. For example, a query like "McDonald's on Market Street" sent from Richmond, Virginia, would use the consumer's home address instead of resolving the mentioned street to the user’s current coordinates. Speed failed because the system didn't incorporate real-time ETA estimates. Neither gap was visible in the aggregate score. Per-facet evaluation became the default, not just as a diagnostic tool, but as a way to surface clear engineering priorities.

- Fuzzy queries exposed missing dimensions: Structured queries such as "spicy cheap tacos" have relatively clear relevance criteria. Fuzzy queries, such as "cozy date night dinner" or "something new and exciting," forced the rubric to handle dimensions it never anticipated.Discovery/indecision queries scored lowest across all query types (NDCG@5 = 0.743 vs. 0.844 for vibe/mood queries). As we dug in, we found that on average 40% of store results were duplicates across different queries for the same consumer. The query rewrite module was collapsing diverse intents into similar retrieval queries but gave the rubric no mechanism to penalize this. The rubric was missing two dimensions:
	- *Novelty/familiarity:* For a query like "surprise me with something new," returning the consumer's frequently ordered stores is a failure, but the rubric scored it as relevant because the cuisine matched their profile. We introduced dynamic weighting that penalizes profile-matching stores on exploration queries (weight = -1) while rewarding them on repurchase queries (weight = +1).
		- *Price and rating alignment:* Fuzzy queries don't specify price or quality, but consumers have implicit expectations. We incorporated the consumer's historical price range and a store rating floor (>= 4.5) as evaluation facets, even when the query didn't mention them.
- *The judge revealed its own blind spots*: Calibration isn't one-directional. Each round of judge output surfaced gaps in the judge's own reasoning:
	- *Price thresholds:* For "tacos under $20," the judge evaluated store-level relevance but didn't filter by individual item prices. A store with one $12 taco and twenty $25 entrees was marked relevant.
		- *Menu customization:* For "spicy ramen," the judge missed that spice level is a customizable option at many restaurants; the base menu item says "ramen," not "spicy ramen."
		- *Display logic mismatch:* For "top rated" queries, the judge disqualified stores rated 4.69 because the rubric threshold was 4.7 — but the app UI rounds to 4.7. The evaluation didn't match the user's reality.
- As shown in Figure 6, each improvement required enriching the judge's context with things like item-level pricing metadata, customization option flags, and display-rounded ratings. The pattern repeats: Product change → evaluation gap → rubric update → judge re-calibrated → next product change.
![](https://careersatdoordash.com/wp-content/uploads/2026/04/image-25-1024x683.png)

Figure 6: Iterative improvement loop for LLM-as-a-judge, showing how new evaluation failures surface over time. The figure traces three rounds of learning: first, overall NDCG was too coarse to localize failures; second, fuzzy queries exposed missing rubric dimensions such as novelty; and third, calibration revealed blind spots in the judge itself due to missing item-level context. The reader should discern that evaluation quality improves through repeated cycles of rubric refinement, context enrichment, and judge recalibration.

## Practical advice for adopting LLM-as-a-judge

*Start with binary relevance:* Multi-grade scales inflate inter-annotator disagreement. Binary aligns with AUC, simplifies golden-set construction, and is easier for both humans and LLMs to apply consistently.

- *Decompose intent into independent checks:* Keep questions minimally overlapping, anchor them in observable evidence, and avoid both extremes – hard-coded exception lists and vague "is this a good match?" prompts.
- *Human labels are not ground truth:* Audit early by running an LLM judge over the same examples before investing in model training. The most valuable disagreements reveal rubric ambiguity, not annotator incompetence.
- *Use chain-of-thought prompting:* Evaluating each facet sequentially, rather than packing everything into a single system prompt, reduces variance and forces the judge to reason about each binary question independently.
- *Evaluate per facet from Day One:*A combined metric won't tell you, for example, whether the failure is dietary understanding, constraint enforcement, or retrieval coverage.
- *Treat the rubric as a product artifact:*Every evaluation cycle surfaces edge cases the rubric doesn't cover. Plan for rubric updates as a first-class part of the engineering loop.
- *Automate the execution loop early:* Daily monitoring catches regressions that weekly reviews miss. PR-level guardrails prevent them from shipping.

## What we would do differently

Operationalizing LLM-as-a-judge delivered leverage, but also taught us where the approach breaks.

1. *Start with the simplest facet set that captures user experience:* Our first design encoded too many special cases, which increased maintenance without improving accuracy.
2. *Prefer simple facet definitions over long exception lists:* When rubric text becomes "if A then B unless C," both humans and LLMs become brittle.
3. *Evaluation quality is bounded by context quality:* Many "judge failures" were actually missing signals, such as item-level pricing, menu customization flags, or display logic that differed from raw metadata.

If starting again, we would invest earlier in context completeness for known hard dimensions, set explicit processes for rubric changes, including review, versioning, and re-baselining, and treat rubric iteration as ongoing operational work rather than a one-off setup.

## Looking forward

Our current calibration loop — collect golden labels, manually tune the judge, and re-baseline — works, but doesn't scale. Recent work across the industry points toward three new directions:

1. *From matching to reasoning:* Alibaba's [TaoSR1](https://arxiv.org/abs/2508.12365) \[4\] and [LORE](https://arxiv.org/abs/2512.03025) \[5\] reframe relevance as multi-step reasoning with explicit chain-of-thought, decomposing it into orthogonal capabilities. LORE reports a 27% improvement in cumulative online quality over more than three years. Judges that reason through facets outperform holistic scoring, which is consistent with our finding.
2. *Hybrid evaluation and policy-as-code:* [Amazon's PRECISE](https://arxiv.org/abs/2601.18777) \[11\] combines roughly 100 human annotations with thousands of LLM judgments via prediction-powered inference. [LinkedIn's SAGE](https://arxiv.org/abs/2602.07840) \[8\] formalizes evaluation as versioned policy + curated precedent + distilled surrogate judges at 92x lower cost. Both show principled human-LLM combination outperforms either alone.
3. *Automated rubric evolution*. [RocketEval](https://arxiv.org/abs/2503.05142) \[9\] achieves frontier-model agreement with a 2B model via instance-specific checklists. [GEPA](https://arxiv.org/abs/2507.19457) \[10\] optimizes evaluation prompts through reflective evolutionary search. [Google DeepMind](https://arxiv.org/abs/2503.19092) \[7\] warns that LLM judges exhibit significant bias toward LLM-generated rankings — a calibration risk requiring continuous monitoring.

For DoorDash, the near-term priorities are hybrid evaluation routing, rubric versioning as code, and GEPA-style automated prompt refinement. NLS is the proving ground, but the methodology — decompose, calibrate, and automate — generalizes to any evaluation task where human labels are expensive and intent is compositional.

## Acknowledgements

We are deeply grateful to our collaborators across the core consumer organization and cross-functional partners, including:

- Engineering team members Sangmin, and Eric Gu for enabling production deployment.
- Product and S&O partners Alex Levy, Christian Lai, Raghu Sreepada, and Mauricio Barrera Acuna.

At DoorDash, we're tackling some of the most interesting open problems in applied AI/ML. The LLM-as-a-judge work in this post is just one thread in a much larger story. **If you are interested, come join us to build the next generation of AI-powered discovery and search experiences for millions of consumers.**

---

## References

\[1\] Liu, Y. et al. "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment." [arXiv:2303.16634](https://arxiv.org/abs/2303.16634), 2023.

\[2\] Zheng, L. et al. "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." NeurIPS 2023.

\[3\] Wang, H. et al. "LLM-based Relevance Assessment for Web-Scale Search Evaluation at Pinterest." EARL Workshop at RecSys 2025. [arXiv:2509.03764](https://arxiv.org/abs/2509.03764).

\[4\] Dong, C. et al. "TaoSR1: The Thinking Model for E-commerce Relevance Search." Taobao & Tmall Group, Alibaba. [arXiv:2508.12365](https://arxiv.org/abs/2508.12365), 2025.

\[5\] Lu, C. et al. "LORE: A Large Generative Model for Search Relevance." Alibaba Group. [arXiv:2512.03025](https://arxiv.org/abs/2512.03025), 2025.

\[6\] Su, Y. et al. "Modernizing Facebook Scoped Search: Keyword and Embedding Hybrid Retrieval with LLM Evaluation." Meta. [arXiv:2509.13603](https://arxiv.org/abs/2509.13603), 2025.

\[7\] Balog, K., Metzler, D., and Qin, Z. "Rankers, Judges, and Assistants: Towards Understanding the Interplay of LLMs in Information Retrieval Evaluation." Google DeepMind. [arXiv:2503.19092](https://arxiv.org/abs/2503.19092), 2025.

\[8\] Le, B. et al. "SAGE: Scalable AI Governance & Evaluation." LinkedIn. [arXiv:2602.07840](https://arxiv.org/abs/2602.07840), 2026.

\[9\] Wei, T. et al. "RocketEval: Efficient Automated LLM Evaluation via Grading Checklist." ICLR 2025. [arXiv:2503.05142](https://arxiv.org/abs/2503.05142).

\[10\] Agrawal, L. et al. "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning." ICLR 2026 Oral. [arXiv:2507.19457](https://arxiv.org/abs/2507.19457).

\[11\] "PRECISE: Reducing the Bias of LLM Evaluations Using Prediction-Powered Ranking Estimation." Amazon. AAAI 2026. [arXiv:2601.18777](https://arxiv.org/abs/2601.18777).

\[12\] Takehi, R. et al. "LLM-Assisted Relevance Assessments: When Should We Ask LLMs for Help?" SIGIR 2025. [arXiv:2411.06877](https://arxiv.org/abs/2411.06877).

\[13\] Calderon, N., Reichart, R., and Dror, R. "The Alternative Annotator Test for LLM-as-a-Judge." ACL 2025. [arXiv:2501.10970](https://arxiv.org/abs/2501.10970).

\[14\] Fabbri, F. et al. "Evaluating Podcast Recommendations with Profile-Aware LLM-as-a-Judge." Spotify Research. RecSys 2025. [arXiv:2508.08777](https://arxiv.org/abs/2508.08777).