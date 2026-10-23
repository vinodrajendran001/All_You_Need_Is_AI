---
type: concept
created: 2026-06-02
updated: 2026-10-23
tags:
  - concept
  - ai-agents
  - research
  - automation
source_ids:
  - src-2026-06-02-dwarkesh-eric-jang-alphago
  - src-2026-06-10-itsreallyvivek-frontier-ai-labs
  - src-2026-06-17-nathan-lambert-frontier-post-training-recipe-review
  - src-2026-06-18-alyona-vert-recursive-self-improvement
  - src-2026-06-30-alisa-liu-ai-research-job-search
  - src-2026-07-30-teaching-open-model-science
  - src-2026-07-16-lilian-weng-harness-engineering
  - src-2026-08-28-philipp-schmid-recursive-self-improvement
  - src-2026-09-09-zafstojano-recursive-synthetic-improvement
  - src-2026-09-15-turing-post-recursive-self-improvement
  - src-2026-10-19-cammarata-networks-already-clean
  - src-2026-10-19-naam-million-agents-superintelligence
status: active
---

# Automated AI Research

## Definition

Automated AI research is the use of LLM- or agent-driven systems to help formulate, implement, run, evaluate, and iterate on AI experiments and research artifacts.

## Why it matters

This is one of the clearest real-world paths by which AI capability could recursively accelerate further AI progress. It matters not because models suddenly become autonomous scientists overnight, but because they can begin to compress parts of the research loop before they can replace the whole thing.

## Current synthesis

- The Eric Jang interview frames research automation as an **autoresearch loop** rather than a one-shot assistant feature. The interesting question is not only whether a model can answer research questions, but whether it can keep iterating through experiments.
- The current sweet spot appears to be **execution-heavy tasks**: implementing experiments, running them, and optimizing hyperparameters.
- The harder bottlenecks remain **research taste and navigation**: deciding the next question worth asking, recognizing when a line of inquiry is a dead end, and changing course intelligently.
- The flashcard-generation workflow described in the same source is a smaller but concrete example of this pattern: a durable agent can read a transcript, incorporate blackboard screenshots, generate visuals, and pass outputs through a critic more effectively than a loose chain of calls.
- This concept fits naturally alongside the [[Agentic Loop]]: the loop is the general control pattern, while automated research is one high-value application domain with unusually strong feedback loops and unusually costly mistakes.
- [[itsreallyvivek - some notes on getting into frontier ai labs]] sharpens the bottleneck language. It argues that frontier research and trench engineering are both really about building useful abstractions when no complete map exists. The scarce resource is not information but **judgment**: picking which anomaly, bottleneck, or question actually deserves attention.
- That framing improves the page's distinction between what agents are already good at and what still resists automation:
  - **Execution** can often be automated or compressed.
  - **Abstraction-building and question selection** remain much harder.
- A durable summary is: automated research becomes more valuable as systems get better at generating possibilities, but that also makes **taste** more important, because the main problem shifts from "can we run this?" to "is this the right thing to run?"
- [[Nathan Lambert - Frontier post-training recipe review with Finbarr Timbers]] adds the organizational version of the same bottleneck. Frontier post-training recipes now require many specialist teachers, data mixtures, RL runs, distillation stages, and integration steps. That makes research automation less like "one agent finds the answer" and more like **coordination across many experimental subprograms**. The hard part is not only running experiments, but maintaining the recipe graph and deciding which specialist branch deserves more compute.
- [[Alyona Vert - AI 101 - What is Recursive Self-Improvement]] adds the recursive-improvement spectrum. Today's systems mostly automate coding, experiments, evaluation, post-training work, and workflow artifacts; stronger [[Recursive Self-Improvement]] would improve the model-building process itself, including data, architectures, training methods, evaluations, and future AI researchers.
- This distinction keeps the page conservative: self-improving agents can optimize prompts, tools, memory, code, or skills without yet reaching true RSI. The hard jump is from improving a workflow to improving the system that creates better AI systems.
- The same "judgment over execution" thesis shows up in hiring. [[ML Research Interview Preparation]] (from [[Alisa Liu - The AI Research Job Search]]) notes that interview *loops* heavily reward technical breadth and coding, but — echoing [[itsreallyvivek - some notes on getting into frontier ai labs]] — the durable ability labs ultimately select for is the research judgment and abstraction-building this page describes. The practical reconciliation: study to pass the loop, but the long-run edge is the same taste/anomaly-selection skill that makes automated research hard.
- [[Bojan Jakimovski - Teaching an Open Model to Do Science]] supplies a concrete workflow-level example. Loka's 21-run program trained a compact open MoE with GRPO and LoRA across biomedical tool investigation and Gene Ontology annotation, then promoted a checkpoint only after held-out scores, trace/verifier review, and application testing agreed. The research loop is therefore not just experiment execution: it is the design of verifiable environments, failure-sensitive rewards, and evidence-backed promotion criteria.

## What the automated loop reliably does, and what it does not

Two 2026 surveys let this page separate the settled part from the aspirational part.

**Execution is close to solved on verifiable targets.**
[[Philipp Schmid - Recursive Self-Improvement]] collects the evidence: Karpathy's autoresearch ran
~700 experiments on one GPU against nanochat, kept ~20 transferable changes, and cut
time-to-GPT-2-quality from 2.02 to 1.80 hours; Prime Intellect scaled the same keep-or-revert loop to
~10,000 trials and beat the human baseline; AlphaEvolve found a matrix-multiplication algorithm one
scalar multiplication better than Strassen's and sped up a Gemini training kernel by 23%. In every
case the loop was a propose-train-evaluate cycle scored by something the agent could not edit.

**Direction-setting is not.** A Princeton-led study cited by Schmid found agents can execute much of
the engineering of AI research while still struggling to choose original and useful directions. Or as
he puts it: "The loop is excellent at hill-climbing a verifiable metric. Taste is not a metric."

**The failure modes are now catalogued.**
[[Lilian Weng - Harness Engineering for Self-Improvement]] names six characteristic ways automated
research pipelines go wrong:

1. **Training-data defaults** — reverting to a familiar method instead of the specified one.
2. **Implementation drift** — the code stops matching the stated design.
3. **Memory degradation** over long runs.
4. **Over-optimism**, including "numerical duct tape" applied to make results look clean.
5. **Insufficient domain intelligence.**
6. **Weak scientific taste.**

Weng's benchmark appendix — PaperBench, CORE-Bench, ScienceAgentBench, RE-Bench — is the current
measurement surface, and all four score *execution*. None of them scores the choice of question,
which is precisely where the Princeton study locates the gap.

## Self-play works when it is anchored to something that cannot be argued with

[[@zafstojano - Recursive Synthetic Improvement]] traces the curriculum-generation lineage — Schmidhuber (2002) → AlphaGo and AlphaGo
Zero → GANs → **STaR** → **Self-Rewarding LMs** → **SPIN** → **Absolute Zero** — and the design pattern
that separates the working versions from the degenerate ones is the anchor.

**Absolute Zero** pairs a proposer with a solver in self-play, rewards the proposer for **learnability**
(neither trivial nor impossible), and covers abduction, deduction and induction — but crucially it is
**anchored in a code interpreter**, so the self-play cannot drift away from ground truth. **PopuLoRA**
takes a different route, evolving a population of student and teacher LoRAs paired by TrueSkill.

**The unanchored version fails in a documented way.** In *Training to Paint with Code*, an elaborate
multi-criterion reward collapsed to "the same flat clip-art flower with five rounded petals", because the
judge's criteria were highly correlated and the length term saturated. The shipped reward was much
simpler. See [[Reward Design for RL]].

**Jason Wei's Verifier's law** states the constraint generally: "The ease of training AI to solve a task
is proportional to how verifiable the task is." Automated research is therefore easiest exactly where an
oracle exists, and the frontier of automation tracks the frontier of verification rather than the frontier
of difficulty.

That framing also supplies the limiting problem: Florian Brand is quoted that "semi-private evals and
evals with a hold out set are basically dead." An automated research loop that cannot be independently
measured cannot be shown to be improving. See [[Synthetic Data Flywheel]].

## Automation is bounded by what it cannot edit

[[Turing Post - What Is Recursive About Recursive Self-Improvement]] uses AI4AI-Bench as a bounded
case: an agent receives several hours to modify a real training algorithm, which is then rerun from
scratch under fixed evaluation. The system automates experiment execution without owning the
definition of improvement.

This makes editable scope a more useful measure than how many research steps use AI. A fast loop can
remain non-recursive while objectives, budgets, permissions, and evaluation stay external.

## Interpretability as an agent-scaled science

[[Nick Cammarata - Neural Networks Are Already Clean]] applies the execution-versus-taste split to
interpretability. Agents do the high-volume parts of the conjecture-and-test loop:

- writing explanations of individual neurons, with a 1,000-neuron random gallery offered;
- writing blind-maximum and near-miss examples from an explanation alone;
- grouping neurons in attribution graphs and sorting all **10,240** experts of Qwen3.6;
- reviewing **100,000** attribution graphs, against the author's thousands by hand.

The author says the project began as a test of whether agents had research taste, with neurons
as a baseline; the neuron explanations kept holding up instead.

The page's existing boundary holds. The loop scales labeling and testing, but the essay locates
the scarce work in choosing questions and recognizing motifs: "interpretability is largely the
search for the right question." Its proposed future is a laboratory of automated scientists guided
by a "mechanistic constitution". That is a design sketch, not a demonstrated system.

The essay also reports something resembling the **training-data defaults** failure that Lilian
Weng catalogues for research agents. Agents brought their own default reading of
"superposition". The author attributes part of this to an informal 2023 note on composition and
superposition that opens with a large embedded base64 image. The agents' web readers hit their
length limit inside the image before the argument began. The
agent-written labels, controls, and groupings are therefore part of the measurement. Its
cleanliness figures are agent-assisted, threshold-dependent, and not independently reproduced.
See [[Mechanistic Interpretability]].

## Adding researchers buys throughput, and the page has never had a number for the conversion

[[Ramez Naam - Can a Million AI Agents Create Superintelligence]] attacks this page's execution-versus-taste
split from an unexpected direction: it asks what the *execution* half actually converts into. The essay is a
**survey and synthesis of other people's results**, not an experiment, and its author says so —
**"We're all operating on far too little real world data."** Read it as a well-sourced argument about where
the evidence currently sits, not as evidence in itself.

**The distinction it supplies is speed versus collective intelligence.** More agents reliably make a solvable
task finish sooner; what is unproven is that they let a team solve a *harder* problem or reach a new skill
level. Three mechanisms are offered for the gap — coordination cost, homogeneity producing shared blind spots,
and the sequential structure of hard problems: *"A million independent searches can run at once. A sequential
investigation can't."* and *"A thousand copies don't automatically supply the insight one copy is missing."*
That maps almost exactly onto the bottleneck this page already names. Execution parallelises; abstraction-
building and question selection are the sequential part.

**One figure reframes the automated-research pipeline directly.** Naam reports, from his own earlier post
summarising OpenAI, that the lab used **124 times as many tokens per researcher** while running only **1.6
times as many experiments per researcher**. If that holds, the conversion from compute spent to experiments
actually run is far lossier than "execution is close to solved" suggests — the loop above may be excellent at
hill-climbing and still be a poor converter of tokens into trials. The figure is third-party and
self-reported, with no stated accounting of what a "token per researcher" or an "experiment" includes.

**The modelling spread is the argument.** Taking Anthropic's reported agent-hour ratios as input — about
**9 agent-hours per human work-hour by mid-July**, **19** by late August, against a company-wide ratio near
**6** — the published scaling assumptions give wildly different answers for how much faster research should
now be going: Chan et al. (2026)'s exponent implies roughly **25x** April's pace by August, Davidson and
Houlden's parallel-research exponent of **0.6** implies about **2-4x**, plain logarithmic scaling about
**2x**, and the sub-logarithmic shapes Naam collects only about **1.1-1.8x**. Those conversions also assume
equal value per agent-hour and treat extra runtime as parallel labour, which the author flags.

**The proposed protocol is the part this page should adopt.** Naam asks for three quantities measured on real
AI research rather than on benchmarks: **G**, the verified task-performance gain per multiplication of agents;
**λ**, how speed scales with team size; and **N**, the team size at which gains weaken or saturate — reported
separately for **1→10, 10→100, and 100→1,000 agents**. The design choice that matters is **reporting gains per
multiplication rather than per total**, which is precisely what makes saturation visible and what a headline
"we ran 10,000 agents" conceals. This page's long-standing open question about what signal measures research-
agent progress has had no candidate answer until now; G/λ/N is one, and it is a proposal with no results
attached.

Naam's own forecast, allowing a **six-month** research-to-publication lag, is that no sustained acceleration
should appear in the Epoch Capabilities Index through the first half of 2027 (see [[Epoch AI]]). He states he
expects to be corrected by data.

## Open questions

- What evaluation signal best measures progress for research agents: paper quality, benchmark gains, reproducibility, or something else?
- At what point does the main bottleneck shift from execution to selecting fruitful research directions?
- When does workflow-level self-improvement become model-building-level recursive self-improvement?
- How should agent-generated scientific labels, such as neuron explanations and graph groupings, be audited so that agent priors do not become the result?
- **Nobody has reported G, λ, or N on real AI research.** Every curve Naam assembles comes from benchmarks,
  and the essay does not show that benchmark scaling transfers to research. Until it is measured on a research
  workload, the protocol is a specification rather than a result.
- **The agent-count evidence stops far short of the claim it is used to evaluate.** The largest team cited is
  roughly 10,000 agents; million- and billion-agent conclusions in either direction are extrapolations, and
  the essay explicitly does not establish that very large teams cannot produce new capability.
- **Does the 124x-tokens-to-1.6x-experiments ratio describe a bottleneck or an accounting artifact?** Nothing
  in the source separates compute spent per experiment from the number of experiments a research programme
  chose to run.
- **Can conceptual breakthroughs be parallelised?** The essay argues the sequential-structure mechanism but
  does not prove it, and it concedes that better coordination, more diverse training, or genuinely new
  learning methods could change the curves it reports.

## Related pages

- [[Ramez Naam - Can a Million AI Agents Create Superintelligence]]
- [[Ramez Naam]]
- [[Agent Delegation]]
- [[Test-Time Scaling]]
- [[Epoch AI]]

- [[Nick Cammarata - Neural Networks Are Already Clean]]
- [[Mechanistic Interpretability]]
- [[Goodfire]]

- [[Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch]]
- [[itsreallyvivek - some notes on getting into frontier ai labs]]
- [[Nathan Lambert - Frontier post-training recipe review with Finbarr Timbers]]
- [[Alyona Vert - AI 101 - What is Recursive Self-Improvement]]
- [[Recursive Self-Improvement]]
- [[Multi-Teacher On-Policy Distillation]]
- [[ML Research Interview Preparation]]
- [[Agentic Loop]]
- [[AI Agents in Production]]
- [[Eric Jang]]
- [[Bojan Jakimovski - Teaching an Open Model to Do Science]]
- [[Harness Optimization]]
- [[Lilian Weng]]
- [[Philipp Schmid]]
- [[Lilian Weng - Harness Engineering for Self-Improvement]]
- [[Philipp Schmid - Recursive Self-Improvement]]
- [[@zafstojano - Recursive Synthetic Improvement]]
- [[Synthetic Data Flywheel]]
- [[RL Environment Design]]
- [[@zafstojano]]
