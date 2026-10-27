---
type: concept
created: 2026-05-29
updated: 2026-10-27
tags:
  - concept
  - llm-evaluation
  - search
  - quality-assurance
source_ids:
  - src-2026-05-28-doordash-llm-judge
  - src-2026-06-02-bytebytego-doordash-testing-system
  - src-2026-05-29-braintrust-multi-turn-scoring
  - src-2026-07-02-arora-llm-reasoning-advances
  - src-2026-07-06-sarthak-rastogi-production-agent
  - src-2026-07-29-giles-thomas-gpt2-weights-part-1
  - src-2026-07-31-giles-thomas-gpt2-weights-part-3-overtraining
  - src-2026-09-02-meta-organizational-second-brain
  - src-2026-09-06-rastogi-agent-observability
  - src-2026-09-09-zafstojano-recursive-synthetic-improvement
  - src-2026-09-14-bytebytego-llm-judge-health
  - src-2026-09-17-almeida-system-one-jev
  - src-2026-09-18-nandakishor-nonautoregressive-decisions
  - src-2026-09-23-kwok-contrastive-language-models
  - src-2026-09-28-martin-automating-eval-design-hillclimbing
  - src-2026-09-29-bytebytego-why-do-llms-lie
  - src-2026-10-06-bytebytego-sycophancy
  - src-2026-10-10-jaloza-microsoft-decision-1
  - src-2026-08-02-arise-llm-as-judge
  - src-2026-10-20-husain-decision-model-evals
  - src-2026-10-16-west-eval-engineering-lessons
  - src-2026-10-17-redwood-screwtape
status: active
---

# LLM-as-a-Judge

LLM-as-a-Judge is the pattern of using a language model to evaluate outputs such as search results, recommendations, summaries, generated answers, or full conversation traces against an explicit rubric. It does not eliminate human judgment; instead, it packages human intent into a calibrated evaluator that can run far more consistently and far more often than manual review alone.

## Why it works

The main advantage is consistency. A calibrated model can apply the same rubric across thousands of examples without the fatigue, shortcutting, and boundary drift that often appear in contractor or expert labeling pipelines. It can also catch synonym equivalence and latent semantic matches that are easy for rushed human raters to miss.

The second advantage is operational scale. Once a judge is reliable enough, teams can use it for daily monitoring, offline benchmarks, experiment comparisons, and pull-request guardrails instead of waiting for periodic annotation cycles.

In this vault, the pattern is especially relevant where retrieval and generation meet: [[Search-Augmented Language Models]], [[Retrieval-Augmented Generation]], and broader [[ML Systems at Scale]] pipelines all depend on evaluation loops that can keep up with production change.

## Key design principles

1. **Decompose relevance into facets.** Complex judgments are more reliable when split into narrow checks such as dish match, modifier match, or constraint satisfaction.
2. **Prefer binary checks to fuzzy multi-grade scales.** Binary decisions are easier to calibrate, easier to audit, and less vulnerable to disagreements around ambiguous middle buckets.
3. **Calibrate against a golden set.** The judge should be measured against adjudicated examples, not blindly trusted because it sounds plausible.
4. **Use structured criteria.** The G-EVAL result generalizes: explicit, step-by-step judging criteria tend to produce more reliable evaluations than unconstrained scoring prompts.
5. **Version the rubric.** Evaluation changes over time, so rubric updates and re-baselining need to be treated as part of the system, not as ad hoc prompt edits.
6. **Exploit the generator-verifier gap.** Open-ended generation is often harder than narrow verification. DoorDash's chatbot-testing system is a good example: binary policy checks over a full transcript are easier to calibrate than the original support-generation task.
7. **Score the right unit of work.** Braintrust's multi-turn scoring pattern shows that some systems need both turn-level and trace-level judges because local response quality and full-conversation success are different things.

## Production case studies

[[DoorDash - LLM-as-a-Judge for Search Evaluation]] is a strong production example. DoorDash found that natural-language search queries such as "cozy date night dinner" encode multiple interacting constraints that human annotators applied inconsistently. Their solution was a three-phase workflow: define facet-based rubrics, calibrate an LLM judge against a golden set, then automate evaluation for daily monitoring and PR-level regression checks.

The case study matters because it frames judge quality as a measurement-design problem rather than a model-magic problem. The LLM becomes useful when the rubric is explicit, the context is complete enough, and disagreements trigger rubric or prompt refinement instead of blind trust.

[[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]] extends the pattern from search relevance into support-chatbot development. There the judge is not only monitoring a live system; it is part of an offline simulation flywheel that evaluates full multi-turn conversations and acts as a release gate for prompt and architecture changes.

[[Braintrust - How to evaluate multi-turn conversations]] adds the instrumentation and operations side: group turns into traces, score both individual responses and whole conversations, run scorers asynchronously in production, and use traffic-level clustering to find recurring failure modes.

## Judges as reasoning verifiers

Beyond product evaluation, the same "calibrated LLM evaluator" idea is the **verifier** that powers reasoning. [[Akhil Arora et al - Current Advances in LLM Reasoning]] frames it as: *verifiers separate generation from evaluation*, and they come in two flavours — **outcome** judges and **process reward models (PRMs)** that score the reasoning steps themselves. Generative reward models (GenRM) and **self-rewarding** setups (a model judging its own outputs via LLM-as-Judge, then improving through iterative DPO) extend the pattern into training. This makes LLM-as-a-Judge a shared substrate across three areas: product QA (this page's case studies), verifier-based [[Test-Time Scaling]] (rank/steer candidate solutions at inference), and [[Reward Design for RL]] (supply the reward signal during RL). The load-bearing caveat is the same everywhere — **a flawed judge/verifier can rank wrong answers higher**, so reward-model reliability and verifier robustness are open problems, not solved infrastructure.

## Judges as an inline production gate

[[Sarthak Rastogi - Making an AI Agent Production-Ready]] moves the judge from an offline scorer into the request path itself. Its output-validation node runs two LLM-judged checks **in parallel** before a response is returned: **faithfulness** (is the answer grounded in the retrieved context, i.e. hallucination detection, Ragas-style) and **completeness** (were all parts of a multi-part question answered?). Running the judge inline is the same measurement-design discipline as the case studies above — explicit, narrow, calibratable checks — applied as a live guardrail rather than a monitoring dashboard, and it is a core node of the [[AI Agents in Production|production agent architecture]].

## Limitations

LLM judges still need human calibration, especially on edge cases where domain experts may reasonably disagree. They can inherit rubric mistakes, miss missing-context problems, and drift away from product reality if the evaluation prompt does not reflect what users actually see. In practice, the safest pattern is human-designed criteria, human adjudication on a golden set, and continuous re-calibration rather than fully autonomous judging.

## Judge variability limits what a small comparison establishes

[[Giles Thomas - Why GPT-2 Weights Beat Mine Part 3 - Overtraining|Giles Thomas - Why GPT-2 Weights Beat Mine? Part 3: Overtraining]] shows a failure mode that
belongs on this page as much as on any training page. The experiment deliberately overtrains
GPT-2-scale models, lowers next-token test loss, and observes small instruction-judge gains.
The two new models switch order in a second judging.

The source uses a **one-to-two-point heuristic**, not a characterized noise floor or formal power
analysis. Its first score gains are **1.22 and 0.92 points out of 100** after separate instruction
fine-tuning; these are not accuracy percentages. The author explicitly leaves the overtraining
hypothesis unresolved.

This makes judge variability a **design parameter rather than a reporting detail**. Repeated,
paired grading and order checks can support uncertainty estimates; more observations may improve
precision, so single-run variability is not an absolute limit on detectable effect size. In this
small comparison, "no established material gain" is justified; "no gain exists" is not.
[[Giles Thomas - Why GPT-2 Weights Beat Mine Part 1]] records the two-stage evaluation protocol.
See [[Benchmark Optimization]] for the distinction between an improved proxy and an established
downstream effect.

## Blind on both sides, and a second judge that argues against

[[Meta - An Organizational Second Brain]] contributes two protocol details that sharpen how a judge is deployed
inside a maintenance loop, rather than how a judge is built.

**Targeted replay is blind on both sides.** When a knowledge change is validated, the agent under test does not
know it is being tested, and the judge does not know what changed. Both halves are load-bearing. An agent aware
of evaluation is a different agent; a judge told what changed will look for its effect and find it. This is a
stricter protocol than the production judging arrangements already on this page, most of which score outputs
whose provenance the judge can see.

**A second agent judges the diff adversarially.** Independent review is performed by an agent given **only the
diffs and no knowledge of the rationale**, with the explicit task of arguing against the change. Withholding the
motivating story is the design: a reviewer who knows why a change was made tends to reconstruct its
justification. This is a judge used as an opponent rather than as a scorer, and it is a role this page has not
previously recorded.

Sitting underneath both is a division of labour worth preserving: the **deterministic linter runs first** —
dangling cross-references, file-size budgets, identifier collisions, dependency cycles, *"not probabilistic, it
passes or fails"* — and only what it cannot decide reaches a model judge. Given this page's finding that a
judge's noise floor bounds what an experiment can detect, moving every mechanically checkable property out of the
judge's remit is the cheapest available precision gain.

## An online evaluator is triage; a synchronous gate is a different component

[[Sarthak Rastogi - Making AI Agents Observable, Monitorable, and Production-Ready]] draws a line that production teams routinely blur. Langfuse-style production
evaluators run LLM-as-judge asynchronously against a sample of live observations — "after the response has
already gone out... They are not, by themselves, a synchronous safety gate." They are monitoring and
triage.

A gate is a separate component with a different budget: a fast cheap judge sitting in the response path.
Singapore's GovTech published this pattern for public-service chatbots, using **lightweight
general-purpose models as low-latency security judges** that caught jailbreaks and prompt injection "with
F1 scores competitive with much heavier specialized safety models" — evidence that the gate does not have
to be a specialised safety model to be useful.

The sampling design that feeds the offline judge also has to change for LLM traffic. Random sampling works
for a payment API because "two requests that look similar probably behave similarly"; for an LLM call,
"two requests with near-identical inputs can produce wildly different outputs — one correct, one
hallucinated, one a policy refusal." A 1% random sample gives "1% of the picture with no way to know
what's in the missing 99%." The replacement is **tail-based, outcome-aware sampling**: always capture
errors, high latency, low grounding scores and guardrail flags, and sample routine successes at
**5–20%**.

The unresolved cost is that a 5–20% sample of routine successes is exactly the population where a slow
quality regression would first appear. See [[Agent Observability]].

## The judge crossed the inter-human agreement threshold in 2023, and then moved inside the model

[[@zafstojano - Recursive Synthetic Improvement]] supplies the result that made automated judging the default. Zheng et al. (2023)
measured **GPT-4 agreeing with human raters at roughly 80%, about equal to inter-human agreement** — past
which paying for human preference labels became optional for most purposes.

The lineage runs InstructGPT's three phases → Constitutional AI and RLAIF → LLM-as-a-judge, and the
current move is inward: **Kimi K2 folded the judge back into the policy** as its own rubric-guided critic
rather than maintaining a separate reward model.

The residual human-preference layer became a business rather than disappearing: Chatbot Arena's commercial
arm reached **$100M ARR eight months after commercial launch, on a $150M Series A**.

Two limits worth recording alongside. A learned router or policy inherits its judge's bias — "if the
evaluation method rewards fluent answers rather than correct ones, the router can learn the wrong lesson."
And a judge with highly correlated criteria is a reward-hacking target: in *Training to Paint with Code*
an elaborate multi-criterion reward collapsed to a single degenerate output because the criteria moved
together and the length term saturated.

See [[Synthetic Data Flywheel]] for the judge's place in the wider automation of the training stack.

## A layered evaluation stack, and a false shortcut

[[ByteByteGo - LLMs as a Judge - How to Know if Your LLM Is Healthy]] places judges after
deterministic checks and holdout cases, and before human calibration and production monitoring.
Pairwise order reversal tests position bias; failures discovered in production become new regression
cases. Its 1-5 rubric and 100-answer calibration are examples, not measured prescriptions.

[[Diogo Almeida - Introducing System One Models and Jev]] illustrates the shortcut to avoid. TypeSafe
compares Jev against averages from large models rather than independent ground truth, while the same
team authors the workflows and product. A teacher-model consensus can be a reference, but it cannot
establish calibration or correctness by itself.

## Calibration enables abstention, not ground truth

[[Nandakishor M - Non-Autoregressive Decision Models and Laya]] reports expected calibration error
and selective accuracy for a typed decision model, including an explicit Act/Escalate threshold.
Those metrics are useful only against trustworthy labels. A calibrated classifier can route uncertain
cases without becoming an independent judge of semantic quality.

## A verifier that ranks instead of writing, scored on 38 and 30 tasks

[[Jacky Kwok et al - Contrastive Language Models]] supplies the extreme case of this page's
generator-verifier gap. Its reward model produces no critique and no score text at all: the verdict
is a cosine similarity between a state embedding and an action embedding, over a **predeclared
candidate set**, with only a **20M-parameter projection head** trained on top of frozen LLM
backbones. That is cheap enough to belong in the response path rather than in an offline sweep,
which is the synchronous **gate** component distinguished above from asynchronous triage — and it
forfeits, by construction, any ability to say something the candidate set does not already contain.

The reported numbers are **81.6% on DeepSWE** and **87.6% on Terminal-Bench 2.1**, selecting from
candidate solutions sampled with **Opus 5** and **Fable 5** respectively, and the denominators
matter more than the percentages: **38** and **30 held-out tasks**, latency on an **H100 GPU**. On
38 tasks one task is worth about 2.6 points, which is this
page's own noise-floor argument pointed at a reward model rather than at a judge. A percentage
computed over a few dozen tasks cannot resolve differences smaller than a couple of tasks, so it
supports a claim of rough parity and not a ranking. The CLM latency advantages are likewise
condition-specific and must not be collapsed into a single figure: **up to 9x lower latency**
overall, **4-6x faster inference than Jev** in the benchmark section, and **13x** at roughly **1k
candidates**.

The provenance caveats are stronger here than for the production case studies above. Every figure is
first-party, "SOTA" is the authors' own characterization, the venue is a Notion page rather than a
peer-reviewed paper, and the capture arrived with no author in its frontmatter — the seven-author
list was recovered from the body and its BibTeX entry at ingest. The verifier's supervision also
comes from **~1M
ADP agent trajectories**, which is agent behaviour rather than adjudicated ground truth, so the
warning recorded above against [[Diogo Almeida - Introducing System One Models and Jev]] transfers
with the sign changed: teacher-model consensus and successful-trajectory mining are both references,
not independent truth. The source concedes the load-bearing point itself — improvements in
contrastive test loss do not by themselves establish verification reliability.

## Run the grader twice before trusting it, then ask it for claims rather than a score

[[Lance Martin - Automating Eval Design and Hillclimbing with Claude]] turns this page's noise-floor
argument into a procedure: the baseline diagnostic **runs the grader twice on the same output** to expose
grader noise, and results carry a confidence interval and one full transcript per case. It also names the
opposite boundary, which this page has not recorded — the procedure **warns when the baseline is about
95% or higher**, at which point quality hillclimbing is uninformative and cost or latency should become
the objective. A judge can fail by being noisier than the effect being sought, and it can fail by having
nothing left to resolve. Every figure here is Anthropic-reported on an Anthropic workflow, with no
independent reproduction and no released evaluation data.

On what to ask the judge, both new sources point the same way. Martin's rule is that judges should
**check specific claims rather than emit a 1-to-5 scale**, which agrees with this page's preference for
binary checks and sits against the 1-5 rubric recorded above from
[[ByteByteGo - LLMs as a Judge - How to Know if Your LLM Is Healthy]] — a rubric that source itself
offered as an example rather than a prescription. [[ByteByteGo - Why Do LLMs Lie]] supplies the
mechanics: verification belongs in a **separate stage from drafting**, where the answer is decomposed
into individual claims, each claim is checked against applicable evidence, and citations are validated
for **existence, applicability, and support**.

Its measurement proposal is the more durable contribution. Scoring should cover **correctness, support,
appropriate abstention, and unnecessary refusal**, because right-or-wrong scoring cannot distinguish a
system that has learned to say "I don't know" from one that has learned to refuse — a distinction the
calibration material above needs and cannot get from accuracy alone. The **factuality-versus-faithfulness**
split cuts the same way: a judge grading faithfulness to a stale document will pass an answer that is
wrong about the current policy, so a grounding judge certifies agreement with the evidence it was handed
and says nothing about whether that evidence is current.

Neither source claims the judge is thereby fixed. **A verifier is itself a model and can be wrong**, so
claim checking reduces rather than removes error, and the ByteByteGo piece is a secondary explainer with
no hallucination rates, controlled comparisons, or ablations to size the reduction. Martin concedes the
human stays in the loop for a different reason: **a misconfigured judge still requires a human to read
scored transcripts**. His own worked example shows why — grader and task inconsistencies were among the
defects fixed while the Claude API skill rose from **66%** toward about **88%** (the figure caption
reports **66.1%** baseline and **87.9% at round 24**), so the automated loop surfaced its own measurement
bugs only because someone was reading transcripts, and those numbers are Anthropic-reported too.

## A second opinion can share the first model's agreement bias

[[ByteByteGo - Why LLMs Agree With You Even When You Are Wrong]] adds [[Sycophancy]] as a judge
failure distinct from missing knowledge. A judge may reward an answer for matching the user's
stated belief or the first model's framing rather than for following the evidence.

Blind review can reduce anchoring but does not establish independent errors when judges share
training, prompts, or assumptions. A paired evaluation should change the user's asserted belief
while keeping evidence fixed, then separately test a valid correction. A judge that always resists
the user is not more truthful. Emotional acknowledgment should also be scored separately from
factual endorsement.

The explainer's probe-based intervention changes reward-model candidate scoring in a reported
experiment; it is not a universal deployable truth detector. Agreement between two LLMs remains
an observation, not an independent verifier.

## A bounded scoring interface does not validate a judge's thresholds

[[Lisa Brown Jaloza - Microsoft-Decision-1]] describes rubric-based scoring of answers and
proposed actions through fixed options and returned probabilities. This can avoid generating
a long judge rationale, but the capture's calibration claim has no numerical table or curve
from which to justify an act/defer/review threshold.

The reported **1.3% average decision flips** over eight perturbation types measures one
robustness axis, not correctness or calibration. Microsoft's 36-benchmark accuracy suite and
its separate internal product anecdotes also have different denominators. A practical judge
still needs task-specific labeled cases, error analysis, and deterministic checks wherever
the condition is mechanically verifiable. Fast structured scoring is not an authority grant
or evidence that a proposed action is safe to execute.

**Qualified 2026-10-23.** The artifact this section says is missing — reliability numbers from which an
act/defer/review threshold could be justified — now exists in this vault, for a different set of systems
on a different task; see the threshold and calibration material below. It does not supply
Microsoft-Decision-1's, which remain unpublished here.

## A validated baseline decides whether the judge measures anything

[[Sri Polkampally et al - LLM-as-Judge When It Works and When It Misleads]] argues, for clinical
post-deployment monitoring, that what separates a useful judge from a harmful one is "not the model,
the prompt, or the rubric" but a clearly validated, ideally human-expert baseline. That sharpens this
page's golden-set principle in three ways. **Order:** build the human gold-standard set first and
compare the judge against it, rather than grading LLM outputs and adding human review afterwards;
only the first leaves an artifact that can validate future graders. **Gate:** the judge goes to
scale only after its agreement with human graders clears a pre-specified threshold, and spot-checked
review continues. **Scope:** the tasks that fit are semantic equivalence to a reference and
standardized reasoning against agreed criteria. The post names no threshold value or agreement
statistic, and its cited validations appear without figures, so this is a protocol shape rather than
a sized result.

The source also fixes the judge's **unit of inference**: a "population-level instrument." A pattern
across thousands of notes is actionable; a verdict about one patient is not. That is a boundary the
inline-gate material above must respect. A per-response gate makes case-level decisions, so it needs
per-item error rates, especially misses, which population-level agreement does not supply. The
authors exclude rare or idiosyncratic presentations, contested rubrics ("A definable standard is a
precondition, not an output"), and any use as ground truth.

This sits in tension with the 2023 parity result recorded above, which [[@zafstojano - Recursive Synthetic Improvement]]
presents as making human preference labels optional for most purposes. Here human grading never
becomes optional: the seed set remains the standing benchmark, and ongoing spot-checking "is not
optional." The two are compatible only if broad preference agreement is not read as validation for a
specific task. Where experts themselves disagree, parity with inter-human agreement is a weak bar, and
the authors deny that a judge can resolve the disagreement.

Two further failure modes are named. A **slop cycle** occurs when the grader shares the generator's
blind spots, so errors are scored as correct. This is the same independence failure the
[[Sycophancy]] section above records for judges with shared training, prompts, or assumptions.
**Deprecation** can strand a validated grader and the benchmarks built on it when a closed API
retires its model. The authors recommend an open-source autograder where possible; see
[[Open Model Ecosystems]] and [[Benchmark Optimization]]. Their closing line connects to
[[Embedded Evaluation]]'s point about empty alert logs: "A bad judge is worse than none because it
hides the absence of evaluation behind the appearance of it."

## Discrimination, a cutoff, and calibration are three different properties

[[Hamel Husain - How To Use Decision Models for Evals]] is the first source here that uses **decision
models** as judges and then does the work the category usually skips. It scores **98** production traces
from an apartment-leasing agent — **61** known failures and **37** with no labeled failure, after
excluding **2** internal QA examples — with the judges receiving **masked traces** containing no labels
and no reviewer notes. The 61 failures are **39** from original human review plus **22** manually
validated discoveries from Braintrust and Arize, which is this page's golden-set discipline applied to
the eval set rather than to the system under test.

The practical finding is that the **0.50 threshold is an inherited default, not an optimum**. The
author's illustration makes the point without claiming to measure it: a model scoring failures **0.40**
and passes **0.10** would classify perfectly at a threshold of **0.30** and catch nothing at **0.50**.
Tuning used stratified **five-fold** cross-validation, choosing thresholds on training folds and
measuring on held-out folds, and it runs on **saved scores with no new model calls** — the cheapest
precision gain recorded on this page since moving mechanically checkable properties out of the judge's
remit.

The cutoff has to come from somewhere. Husain uses an **80% precision / 80% recall** requirement, stated
explicitly as an example business rule rather than a standard, and records how often it was infeasible:
the constrained procedure fell back to unconstrained F1 in **36 of 100** training splits for Perplexity
and **29 of 100** for Liquid d1-ultra, against **0 of 100** for OpenAI Decisions. Those are
training-split feasibility counts, not held-out guarantees.

Calibration is then shown to be separate from both. One Cloudflare Clef Flash score group averaged a
predicted failure probability of about **8%** while **60%** of those traces contained failures — a
judge whose scores may still order traces usefully can be read literally only at the cost of being wrong
about rates. Brier scores on saved out-of-fold probabilities, **before → after Platt scaling**: Jev
**0.187 → 0.188**, Liquid d1-ultra **0.173 → 0.172**, OpenAI **0.159 → 0.164**, with an exploratory
direct-probability refit giving OpenAI **0.154**. **Platt scaling made OpenAI's main-fit Brier score
worse.** Brier mixes discrimination with calibration, so these do not isolate calibration quality, and
nothing here establishes which calibration method generalizes.

The cost column is the figure most likely to be quoted out of scope, so it travels with its unit:
Perplexity was the cheapest remaining candidate at **0.82 cents per 100 eval runs** with **F1 0.79**,
while OpenAI Decisions reached **F1 0.87** at **3.72 cents per 100 eval runs**, about **4.5 times** the
cost — one eval run per trace, at those providers' prices and token lengths, with no batching. All of it
is one 98-trace private dataset in one domain, with the original conversations withheld, so it is not
independently reproducible, and the author says performance varies substantially across tasks and tells
readers to measure on their own data. He also notes the deliberately broad "any failure" task may
**exaggerate** the gaps and recommends separate judges per failure mode — this page's
facet-decomposition principle arriving as a caveat on his own comparison.

## A judge that reads the closing message grades the report, not the work

[[Casey West - Four Evaluation Engineering Lessons from Building Agent Plugins]] adds a failure that sits
upstream of every calibration step on this page: the judge was handed the wrong artifact. Google's team
first had an LLM judge score the agent's final text reply against a checklist, but "the grader only sees
what the agent wrote, not what it actually did." On the initial 11-prompt suite for the Google Cloud
Developer plugin, the judge failed three prompts that the raw tool-call logs showed the plugin had
passed. In a Cloud Run cleanup whose rubric required checking command syntax before running anything,
the agent's first step was `gcloud help run services list`, but its final message warned about permanent
data loss rather than reporting the check. "The grader penalized the agent for doing the right thing
simply because it didn’t brag about it in the summary."

This sharpens principle 7, *score the right unit of work*. The split that
[[Braintrust - How to evaluate multi-turn conversations]] supplies there is about granularity, turn
versus whole conversation; this case is about evidence, because a closing message is the agent's own
account of what it did. When a rubric line asks whether the agent ran something, a judge "is guessing
unless you evaluate the actual tool-call trajectory". It is the agent-side form of the faithfulness point
from [[ByteByteGo - Why Do LLMs Lie]]: a judge certifies only the evidence it was handed. It also
confirms [[Lance Martin - Automating Eval Design and Hillclimbing with Claude]] on reading transcripts,
since the misgrades surfaced when the team opened the raw logs.

The fourth lesson meets the golden-set principle as sharpened by
[[Sri Polkampally et al - LLM-as-Judge When It Works and When It Misleads]]: each run is scored against
"golden sets curated by real human experts who know what the ideal path looks like", a human-expert
reference defined over trajectories rather than answers. The post does not say who or what scores runs
against it.

The evidence is one 11-prompt suite for Google's own plugin, published on Google's blog. No judge model,
full rubric, or agreement rate is given, and no trajectory-reading judge is evaluated, so the post shows
a summary-reading judge failing, not a trajectory judge succeeding. How an alternative but acceptable
path earns credit against a golden set is also left open.

## Under optimization pressure, a judge's errors collect among the survivors

[[Redwood Research - Screwtape - Adversarial Transcript Editing for Monitor Red-Teaming]] runs LLM judges
inside an attack-optimization loop. The monitors under attack are judges whose score is compared with a
threshold "set to a fixed false positive rate on honest transcripts"; the verifier that decides whether
each edited attack is valid and severe is a second judge. An attacker iterates against both, receiving
the reasoning behind every failed check, which makes both judges optimization targets in the sense of
the reward-hacking warning recorded above from [[@zafstojano - Recursive Synthetic Improvement]].

The verifier's history qualifies principle 2 without contradicting it. "At first, we asked the verifier
for a simple yes/no verdict." Runs then stopped early on trivial successes, and the verifier accepted
many attacks that human experts did not find valid. The working verifier still accepts or rejects, but
only after assessing the attack along rubric dimensions inspired by NIST SP 800-160v1r1 and the STPA
Handbook and reasoning explicitly about consequences, with example questions such as what harm the attack
can cause, whether that harm has happened or is only prepared, and whether the user authorized the
actions. What failed under optimization was one holistic
verdict, not binary output; the fix is principle 1's facet decomposition, close to the claims-not-scores
rule from [[Lance Martin - Automating Eval Design and Hillclimbing with Claude]]. On average, the
verifier rejects 60–70% of candidate edits within a run.

Even so, "Verifier mistakes concentrate towards the end of the funnel", and final review confirmed 6 of
the 17 attacks that evaded the held-out monitor. The post does not test why. One plausible reading is
that iteration selects for whatever passes the verifier, so errors gather where the search has pushed
hardest. That sits against the population-level framing in
[[Sri Polkampally et al - LLM-as-Judge When It Works and When It Misleads]]: an agreement rate measured
on unselected items need not hold for the items an optimizer selects. Severity was also hard to label
"even for human experts", so Redwood set conservative thresholds.

For judging monitors, the source offers counterexamples without rates: "we can’t get any quantitative
safety estimates from the pipeline". Golden-set agreement gives rates on natural data but no adversarial
search, so neither replaces the other. These are Redwood's observations on its own withheld pipeline;
the false-positive rate, the verifier's agreement with experts, and a reconciliation of the post's
attack counts are not reported.

## Open questions

- Threshold tuning needs labeled data. For a judge deployed where no labeled failures exist yet, what
  sets the first cutoff, and how wrong can the inherited 0.50 be before anyone notices?
- Precision is measured against *known* failures. The scored set contains **37** traces with no labeled
  failure, which is not the same as 37 traces without one, and the source does not estimate how many
  failures its label set misses.
- A threshold tuned at one prevalence is not shown to transfer to another. The source reports no
  prevalence correction and explicitly declines to claim transfer.
- Brier score mixes discrimination and calibration, so none of the before/after comparisons isolates
  calibration quality. What would a calibration-only comparison show, and does the
  8%-predicted/60%-actual group survive recalibration?
- Nothing in that comparison establishes anything about judges on other domains, longer traces, batched
  workloads, or the narrower per-failure-mode rubrics the author himself recommends.
- Reading the tool-call trajectory is the remedy West proposes, but the post evaluates no
  trajectory-reading judge against human labels. How much of a trajectory must a judge see before its
  verdicts on rubric lines that ask whether the agent ran a command can be trusted?
- Adversarial search such as Screwtape yields counterexamples without rates; golden-set agreement yields
  rates on unselected data without adversarial search. How should the two be combined before a judge or
  monitor is trusted as a gate?

## Related pages

- [[Casey West - Four Evaluation Engineering Lessons from Building Agent Plugins]]
- [[Google Cloud]]

- [[Redwood Research - Screwtape - Adversarial Transcript Editing for Monitor Red-Teaming]]
- [[Redwood Research]]
- [[Chain-of-Thought Monitoring]]

- [[Hamel Husain - How To Use Decision Models for Evals]]
- [[Hamel Husain]]
- [[Liquid AI]]
- [[Perplexity]]

- [[Sri Polkampally et al - LLM-as-Judge When It Works and When It Misleads]]
- [[Embedded Evaluation]]
- [[Open Model Ecosystems]]

- [[Lisa Brown Jaloza - Microsoft-Decision-1]]
- [[Microsoft-Decision-1]]

- [[ByteByteGo - Why LLMs Agree With You Even When You Are Wrong]]
- [[Sycophancy]]

- [[Giles Thomas - Why GPT-2 Weights Beat Mine Part 3 - Overtraining|Giles Thomas - Why GPT-2 Weights Beat Mine? Part 3: Overtraining]]
- [[DoorDash - LLM-as-a-Judge for Search Evaluation]]
- [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]]
- [[Braintrust - How to evaluate multi-turn conversations]]
- [[DoorDash]]
- [[Braintrust]]
- [[Multi-Turn Evaluation]]
- [[Search-Augmented Language Models]]
- [[ML Systems at Scale]]
- [[Retrieval-Augmented Generation]]
- [[LLM Reasoning]]
- [[Test-Time Scaling]]
- [[Reward Design for RL]]
- [[Akhil Arora et al - Current Advances in LLM Reasoning]]
- [[Sarthak Rastogi - Making an AI Agent Production-Ready]]
- [[AI Knowledge Base Overview]]
- [[Institutional Knowledge Agents]]
- [[Meta - An Organizational Second Brain]]
- [[Meta]]
- [[Recursive Self-Improvement]]
- [[Agentic Testing]]
- [[Sarthak Rastogi - Making AI Agents Observable, Monitorable, and Production-Ready]]
- [[Agent Observability]]
- [[Sarthak Rastogi]]
- [[@zafstojano - Recursive Synthetic Improvement]]
- [[Synthetic Data Flywheel]]
- [[@zafstojano]]
- [[Jacky Kwok et al - Contrastive Language Models]]
- [[Typed Probabilistic Decision Models]]
- [[Benchmark Optimization]]
- [[NVIDIA]]
- [[Lance Martin - Automating Eval Design and Hillclimbing with Claude]]
- [[ByteByteGo - Why Do LLMs Lie]]
- [[Anthropic]]
- [[LLM Application Resilience]]
