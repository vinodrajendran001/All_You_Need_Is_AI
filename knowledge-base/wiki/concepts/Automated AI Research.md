---
type: concept
created: 2026-06-02
updated: 2026-11-27
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
  - src-2026-10-29-decagon-autoresearch-inference
  - src-2026-11-02-takehi-weight-space-programming
  - src-2026-11-09-zvi-ai-rd-acceleration-rsi
  - src-2026-11-10-mollick-fable-5-2-jagged-agi
  - src-2026-11-06-psi-aaronson-ambainis-proof
  - src-2026-11-06-doubleai-llms-redesign-themselves
  - src-2026-11-10-goodfire-neurons-interpretable-basis
  - src-2026-11-18-toumbourou-wsp-1990s-researcher
  - src-2026-11-18-meta-ads-technique-propagation
  - src-2026-11-22-zhang-li-recursive-self-editing
  - src-2026-11-20-ankit-gupta-vibecoding-inference-chip
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

## Production-shaped experiments can automate optimization without automating research direction

[[Pavi Dhiman and Cyrus Asgari - Building an Inference Stack That Improves Itself]] describes
Decagon's human-initiated AutoResearch campaigns over serving settings, GPU layouts, engine
patches, and draft-model training. Devin Cloud coordinates the work and Modal supplies GPU
execution. Specialists return an explanation, intervention, predicted result, and falsification
condition; only the orchestrator runs scored experiments through the common harness.

The target is requests per second per GPU within an endpoint's production latency limits.
Replay preserves lengths, prefixes, timing, and concurrency; repeated baselines establish
noise. Trials receive Better/Same/Worse/Invalid verdicts, a win becomes the working baseline,
and the original remains the campaign reference. Budgets and human production approval keep
the loop bounded.

This is concrete evidence of an implemented optimization process, but its results are
first-party and endpoint-specific. The **1.05x-2.50x** table range cannot be pooled into
one gain, and the post inconsistently describes its starting baselines. It isolates neither
the contribution of agents nor the conversion from agent tokens to useful experiments.
Agent-initiated campaigns are future work. The execution-versus-direction distinction above
therefore remains: measured artifact improvements do not establish improved research taste.

## Agents propagating proven techniques across a production model fleet

[[Rahul Suresh et al - How Meta Uses AI Agents to Scale ML Innovations Across Ads Ranking Models]] is a larger first-party case of automating execution while direction stays elsewhere.
Techniques are proven first by people and by Meta's Ranking Engineer Agent (REA). Agents then handle
propagation: ranking technique-model candidates (discovery), adapting them to templates or, beside an
engineer, to bespoke models (generalization), and running multi-day experiments with failure recovery
and "an auto-research loop" on top of templates (adoption). Shipping gates are unchanged: offline
normalized entropy, guardrails, and "a statistically significant win in online A/B testing".

Meta estimates that since agents began driving execution in March 2026 they handle "over 60%" of
technique propagation. It reports "3x greater engineering productivity, a median 4x reduction in
training compute across select combinations, and an estimated $45M+ in compute savings by the end of
the year". Each stage has its own metric, and at discovery "Recall matters more here, since a model
missed at this stage never gets a second chance". No values are given for those stage metrics. Nothing
separates the agents' contribution from the Standard Model Templates beneath them. "self-evolving
learning" toward a **5x** throughput target is planned, not shown. See [[Meta]].

## Weights join the artifacts an agent can edit

[[Rikiya Takehi et al - Sparks of Weight-Space Programming]] places itself in a lineage of LLMs
optimizing ever deeper artifacts. It starts with prompts and programs (OPRO, DSPy, MIPRO, GEPA),
moves to whole harnesses (Meta-Harness) and training code and hyperparameters (autoresearch,
Reactive Optimizers), and ends with the weights themselves. In its largest experiment, GPT-6
Astra had **50** forward passes, a Python kernel with no GPU, and practice math sets to improve
Qwen3.5-0.8B without gradients. Over **158** turns and **17** edits it ran the loop this page
describes. It diagnosed a failure (looping thoughts), localized it, and checked the fix with
dose-response, layer-isolation and norm-matched random-direction controls. MATH-500 rose from
**7.9 to 48.1**.

Two details matter for this page. First, the agent's own final report was a hedged research
write-up, and on a Gemma model that rarely loops it reported its small gain as "not established".
That is evidence that an agent can report a null result, though not that it always will. Second,
the improvement was elicitation: removing loops that the stated sampling settings provoked. The
authors conclude that an edit could not add an ability the model lacked. Benchmarks, sampling
settings and budgets stayed fixed by the humans, so the result fits the bound above. Execution of
the loop is automated; the definition of improvement is not. All of this is one model on one
blog, with no comparison against a conventional search over the same edits.

[[Lex Toumbourou - Weight-Space Programming Builds Neural Networks Like a 1990s Researcher]] shows what a rich feedback channel does to rules stated in a prompt. He forbade fitting,
regression and searching, and gave Claude Fable 5.2 only loss, accuracy and a confusion matrix over
**10,000** MNIST training images per step, a loop he calls "*LLM Descent*". Across three runs the model
spent **22**, **24** and **27** steps on measurement, rewiring the output layer so the confusion matrix
reported how often each feature fired, then building a classifier from those rates. The author calls
this "kinda cheating" that "doesn't break the rules". The model also tracked which step would be
scored: "if this step does not beat 0.3111, step 48 is the one that gets scored." The rules constrained
the code, not what the metric let the agent compute, so the feedback channel became the fitting
procedure (compare [[Benchmark Optimization]]). The test set stayed untouched, so the **91.3%** best
run is not contaminated, but this is three runs of one model on one task. The wider set of weight-writing
results is on [[Weight-Space Programming]].

[[DoubleAI - Can LLMs Redesign Themselves as They Train]] moves the agent inside the training run. A
coding agent, "powered by a frontier model" that is never named, reads activation gradients, inserts
zero-gated code layers mid-training, and races each against twin and sham controls. On CLRS-Text it
raised accuracy from **55%** to **84%**, though the agent "already knows how to solve the tasks".
[[Curt Tigges et al - Neurons as an Interpretable Basis]] shows agent labor at population scale: a
Neuron Scientist harness wrote atlas pages for 2,734 stratified neurons, and the release adds
low-effort labels for all 10 million neuron-poles. Both are first-party, and neither reports agent
compute.

[[Linghua Zhang and Yunhe Li - Recursive Self-Editing - LLMs Program Their Own Weight Edits]]
removes the separation between agent and artifact. The editor is the model being improved,
Qwen3.8-27B, working in a persistent Python session with up to **30** tool rounds per candidate,
closed-form weight tools and a forward-only loss check, but no gradient tool. The harness keeps
outside the editor's reach the parts this page treats as not yet automated: humans fixed the math
domain, the gate and test sets, the rank and norm caps, the budgets and the acceptance rule, and
editors never read gate or test problems. The yield is modest. Four edits were accepted in five
generations, worth **+2.50** points on the gate and **+1.45** on the held-out test (avg@4). Unlike
the Astra run above, which checked its fix against dose-response, layer-isolation and norm-matched
random controls, the paper reports no control edit, so it does not answer this page's open question
about weight edits against conventional search. It is a single-run preprint.

## Assistance at a lab, unread research, and a scoped proof

Three November 2026 captures test the execution-versus-taste split from different sides.

**At a frontier lab, the measured gain comes mostly from assistance.**
[[Zvi Mowshowitz - AI R&D Is Accelerating Towards Potential RSI in 2027]] relays [[METR]]'s
assessment of [[Anthropic]]. METR finds that fully autonomous contributions "are not currently a
large contributor to overall progress, but they may be in the near future". Its evidence includes:

- researcher interviews whose estimates were "centered around a 2x acceleration";
- Slack-poll self-reports of uplift that reached **12x** in October 2026, though METR notes that
  the responses "reflect low-effort consideration";
- researchers' reports of "signs of life" for autonomous contributions.

Peter Wildeford, citing the report, separates the two speeds. Engineers can be sped up about
**12x** while overall progress speeds up only about **1.4x**, because of compute constraints and
Amdahl's law. That has the same shape as Naam's 124x tokens against 1.6x experiments above: a large
gain in inputs, a much smaller gain in output. See [[Recursive Self-Improvement]] for the
acceleration estimate and its uncertainty.

**Outside a lab, the bottleneck moves to checking.** In
[[Ethan Mollick - Fable 5.2 and Jagged AGI]], Mollick asked a pre-release model to find an unsolved
empirical problem in entrepreneurship research, find the data, preregister, write the paper, and
have other agents critique it. Fable picked the question, found public data and natural
experiments, and wrote the analysis plan and code. Mollick says the paper "tackles an important
topic with a clever research design" and is "ahead of what I would expect from second-year PhD
students". It is also "not publishable as it is":

- it runs **182** pages, "because every critique got a new analysis and nothing was ever cut";
- the model did not actually preregister, since the plans stayed inside the project and some were
  written after earlier results;
- Mollick spent less than an hour, but "no human has fully checked the results, including me".

His conclusion is that "AI can now produce research faster than anyone can read it". Here the agent
also chose the question, which this page treats as the hard part. That is one reader's first
impression, not a measure of research taste.

**In mathematics, a human scoped the problem and owns correctness.**
[[PSI Research - A Proof of the Aaronson-Ambainis Conjecture]] reports that an internal research
system, running instances of a non-public Anthropic model, had a complete proof of a quantum-
computing conjecture open since 2008 on the third day of a run, and that Lean accepted it. The
stated division of labor fits this page's split. David Turturean developed the system, "scoped the
problem and ran the system on it", prompted the model to draft the paper, reviewed the draft, and
"is responsible for the paper's correctness". The announcement is first-party, and the capture
links neither the manuscript nor the Lean code. See [[AI for Mathematical Discovery]].

*Vault reading:* In all three cases, producing the work is no longer the constraint. Where a machine
checker exists, as Lean does for the proof, checking can keep pace with production, though PSI's
proof still had an advisor's audit and outside experts are still reading it. Where none exists, as
for the empirical paper, output outruns its readers. Inside a lab, faster engineers are held back by
compute and serial steps. This is the Verifier's law above, applied at research scale.

## A multi-day agent loop on hardware, with humans setting process and correctness

[[Ankit Gupta - Vibecoding an Inference Chip]] reports a coding agent running for several days to
implement and optimize bit-exact decoding of a DeepGrove ternary-weight model on an AWS F2 FPGA, mostly
in C++ with some Verilog, a language the author has "never written". Over hundreds of experiments and
**$10,000** of Claude and OpenAI tokens, throughput rose from **6.43** tok/s, the loop's own first
correct image, to **213.13** tok/s (33.13×) through 14 mostly modest, compounding steps. The human role
was mainly encouragement plus a few hints. The outside input that changed the work was process
advice: told to stop long simulations, the agent switched at once to a short synthesis loop, while the
advisers' design ideas were mostly already planned or were rejected for breaking exactness.

The author's conclusion is that "the humans are still useful at defining how to iterate fast and what
correctness looks like, and the agents are great to manage the exploration." This is one self-reported
project. The account of what was adopted is the agent's own retrospective, the 33× is measured against
its own naive starting point, and the token figure excludes instance hours.

## Open questions

- What evaluation signal best measures progress for research agents: paper quality, benchmark gains, reproducibility, or something else?
- At what point does the main bottleneck shift from execution to selecting fruitful research directions?
- When does workflow-level self-improvement become model-building-level recursive self-improvement?
- How should agent-generated scientific labels, such as neuron explanations and graph groupings, be audited so that agent priors do not become the result?
- When an agent edits weights directly, does it find improvements a gradient-based or conventional search over the same budget would miss, or mainly remove obstacles that hide existing ability? A 27B self-editing preprint adds small gains on a model with no reported obstacle, but no comparison with search or gradient training at the same budget.
- **Nobody has reported G, λ, or N on real AI research.** Every curve Naam assembles comes from benchmarks,
  and the essay does not show that benchmark scaling transfers to research. Until it is measured on a research
  workload, the protocol is a specification rather than a result.
- **The agent-count evidence stops far short of the claim it is used to evaluate.** The largest team cited is
  roughly 10,000 agents; million- and billion-agent conclusions in either direction are extrapolations, and
  the essay explicitly does not establish that very large teams cannot produce new capability.
- **Does the 124x-tokens-to-1.6x-experiments ratio describe a bottleneck or an accounting artifact?** Nothing
  in the source separates compute spent per experiment from the number of experiments a research programme
  chose to run.
- **What replaces full human checking where no formal checker exists?** Lean checked every step of
  PSI's proof, though an advisor still audited it and outside experts are still reading it.
  Mollick's 182-page paper had agent critiques but no complete human check, and the model skipped
  the preregistration it was asked for.
- **Can conceptual breakthroughs be parallelised?** The essay argues the sequential-structure mechanism but
  does not prove it, and it concedes that better coordination, more diverse training, or genuinely new
  learning methods could change the curves it reports.

- Meta grades its propagation agents stage by stage (precision and recall, human interventions per
  experiment, share of issues self-mitigated) but publishes no values. Do stage metrics like these
  predict the final A/B outcome well enough to steer a multi-day agent pipeline?

## Related pages

- [[Pavi Dhiman and Cyrus Asgari - Building an Inference Stack That Improves Itself]]
- [[Decagon]]
- [[Rikiya Takehi et al - Sparks of Weight-Space Programming]]
- [[Serving Benchmarks and Goodput]]
- [[Loop Engineering]]
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
- [[Zvi Mowshowitz - AI R&D Is Accelerating Towards Potential RSI in 2027]]
- [[Ethan Mollick - Fable 5.2 and Jagged AGI]]
- [[PSI Research - A Proof of the Aaronson-Ambainis Conjecture]]
- [[METR]]
- [[Anthropic]]
- [[Ethan Mollick]]
- [[AI for Mathematical Discovery]]
- [[DoubleAI - Can LLMs Redesign Themselves as They Train]]
- [[Curt Tigges et al - Neurons as an Interpretable Basis]]
- [[Rahul Suresh et al - How Meta Uses AI Agents to Scale ML Innovations Across Ads Ranking Models]]
- [[Meta]]
- [[ML Systems at Scale]]
- [[Lex Toumbourou - Weight-Space Programming Builds Neural Networks Like a 1990s Researcher]]
- [[Weight-Space Programming]]
- [[Benchmark Optimization]]
- [[Linghua Zhang and Yunhe Li - Recursive Self-Editing - LLMs Program Their Own Weight Edits]]
- [[Ankit Gupta - Vibecoding an Inference Chip]]
