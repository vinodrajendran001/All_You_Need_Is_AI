---
type: concept
created: 2026-06-22
updated: 2026-10-23
tags:
  - concept
  - recursive-self-improvement
  - automated-research
  - ai-agents
source_ids:
  - src-2026-06-18-alyona-vert-recursive-self-improvement
  - src-2026-06-02-dwarkesh-eric-jang-alphago
  - src-2026-06-10-itsreallyvivek-frontier-ai-labs
  - src-2026-07-06-alphasignal-self-improving-harnesses
  - src-2026-08-07-mahesh-sathiamoorthy-rl-environments-agents
  - src-2026-08-23-wafer-ai-performance-engineering-resources
  - src-2026-07-24-ren-et-al-self-improvements-agentic-systems-survey
  - src-2026-07-16-lilian-weng-harness-engineering
  - src-2026-08-28-philipp-schmid-recursive-self-improvement
  - src-2026-08-29-baseten-agentic-kernels-production
  - src-2026-09-02-meta-organizational-second-brain
  - src-2026-09-09-zafstojano-recursive-synthetic-improvement
  - src-2026-09-15-turing-post-recursive-self-improvement
  - src-2026-10-09-dickson-agent-stack-optimization
  - src-2026-10-19-naam-million-agents-superintelligence
  - src-2026-10-14-maevyn-decoherence-trap
status: active
---

# Recursive Self-Improvement

## Definition

Recursive self-improvement (RSI) is the idea that AI systems can help improve the systems and processes that create future AI systems. In its strong form, an AI researcher would design, test, and build an improved AI researcher, which would then repeat the process with decreasing human involvement.

## Why it matters

RSI matters because it is the feedback-loop version of AI progress. If AI can automate more of the research loop - coding, experiment design, evaluation, data generation, training infrastructure, post-training, and deployment - then progress may accelerate even before systems become fully autonomous scientists.

## Current synthesis

[[Alyona Vert - AI 101 - What is Recursive Self-Improvement]] gives the clearest distinction for this vault: **self-improving agents are not the same as recursive self-improvement**.

| Pattern | What improves | Current status |
| --- | --- | --- |
| Self-improving agent | Prompts, tools, memory, code, skills, task execution | Already visible in workflow-level systems |
| Weak / early RSI | Parts of the AI research loop: coding, experiments, evaluation, post-training workflows | Emerging, still human-directed |
| Strong RSI | The model-building process that creates a better AI researcher or successor model | Mostly aspirational |

This connects directly to [[Automated AI Research]]. The Eric Jang source frames research automation as an autoresearch loop where models can implement experiments, run them, and tune hyperparameters. The Turing Post source places that inside a broader RSI spectrum: current agents can automate pieces of the loop, but the harder question is whether they can choose the next valuable research direction and improve the model-building process itself.

The current vault synthesis is conservative:

- AI can already compress execution-heavy research work.
- AI can increasingly optimize local workflow artifacts such as prompts, tools, and [[Agent Skill|skills]].
- AI is not yet reliably automating the full closed loop of proposing, validating, and building stronger successor AI systems.
- Human judgment remains central for goal-setting, result validation, safety boundaries, and deciding which branches of research deserve more compute.

The source also helps disambiguate RSI from [[Recursive Architectures]]. Recursive architectures reuse computation over internal state to improve reasoning depth. Recursive self-improvement is a socio-technical research loop where AI systems improve future AI systems. They share a word, not a mechanism.

[[Alpha Signal - Why self-improving harnesses are the next frontier]] describes workflow-level
**Self-Harness** and **HarnessX** runs: failure traces inform harness edits, with regression
gates and, for HarnessX, AEGIS search over modules. Its account concerns the operating scaffold,
not a demonstrated model-weight update. The October 9 evidence below adds co-evolution and makes
that qualification variant-specific rather than a permanent property of the named systems.
Their asserted guards against reward hacking and forgetting remain controls to evaluate, not
proof that either risk is settled.

[[Mahesh Sathiamoorthy - RL Environments Are All You Need]] identifies scored environments as shared infrastructure for this progression. The same held-out tasks can optimize weights, prompts, or harness code. This supports workflow-level self-improvement, but does not remove the stronger RSI bottlenecks: choosing valuable objectives, preventing reward hacking, and generalizing beyond the curated environments.

## The domain with the cleanest reward signal

GPU kernel generation is the closest thing to a laboratory for this page's claims: correctness is checkable by execution and improvement is measurable in wall-clock time, so the verifier problem that blocks self-improvement elsewhere looks solved by construction. [[AI-Generated Kernels]] records what happened when the loop was actually run — the benchmark had to be hardened twice, first for correctness and then for baseline realism, because models found the gaps in the evaluator before they found the gaps in the kernels.

The lesson is not that self-improvement fails here, but that **an easy verifier is not the same as a sound one**. A loop optimizes against the measurement it is given, so the measurement has to be hardened at the same rate the optimizer improves. See [[Benchmark Optimization]].

## Parameters and scaffold are two separate update surfaces

[[Zhe Ren et al - Self-Improvements in Modern Agentic Systems]] supplies a decomposition this page
benefits from. It defines a foundation-model agent as **model parameters plus a scaffold** — prompts,
memory, tools, and control logic — and defines self-improvement as a **durable, execution-derived
update to either component**.

Two boundaries in that definition do real work.

**Durable excludes the transient.** Anything living only in the context window or the KV cache is not
self-improvement, however adaptive it looks within a session. This draws a clean line between an
agent that behaves well because of what is in its prompt right now and one that has actually changed.
It also means the interesting engineering question is what gets *written back* and where.

**Two surfaces, very different economics.** Parameter updates can come from intrinsic generative
demonstrations, intrinsic evaluative feedback, or extrinsic exploratory experience. The survey gathers
that experience either in grounded task environments or in simulated proxy environments built on
learned world models. This is the [[Agentic Reinforcement Learning]] path: expensive and centralized. Scaffold updates modify prompts, memory, tools, workflows, and control logic, and
are cheap, fast, and available to anyone deploying an agent without training access. Most systems
described in this vault improve themselves through the scaffold; the survey's contribution is naming
that as a legitimate self-improvement mechanism rather than mere configuration.

The survey's formalism keeps a version history of scaffold states, which it says "inherently
supports validation and rollback against harmful modifications across all components", and it calls
scaffold updates "typically faster, more reversible" than parameter updates. Treating that as a
governance requirement is the vault's reading rather than the survey's prescription: because scaffold
updates are cheap and largely unconstrained, they should be **versioned, validated, and reversible**.
That is the same reversibility requirement [[Agent Security and Governance]] applies to agent
actions, turned on the agent's own definition.

**Caveat:** the captured text ends partway through section 6.2.1, so it does not support claims about
the survey's later evaluation and safety material.

## Three loops, separated by what persists

[[Philipp Schmid - Recursive Self-Improvement]] supplies the operational test this page needed. His
definition: *a loop in which a system makes a persistent change that improves its future performance
**and its ability to produce subsequent improvements***. The taxonomy that follows separates loops by
**which layer survives the run** — and above all by whether the verifier moves.

| Loop | Output | System | Verifier |
| --- | --- | --- | --- |
| **Iteration** — edit code, rerun the test | changes | fixed | fixed |
| **Self-improvement** — add a tool, record a skill | changes | changes | fixed |
| **Recursive self-improvement** — raise the bar itself | changes | changes | **rises** |

Everything shipping today is the middle row. This sharpens the distinction already drawn above between
self-improving agents and RSI: a rising task score proves self-improvement, while **recursion is a
claim about a second curve — did the next round face a harder bar the system still could not cheat?**
Nobody is measuring that curve.

Schmid also removes a common assumption: **RSI does not require a better model.** A frozen model with
an honest verifier and a writable environment can climb on its own. The easiest target is the harness,
which is why [[Harness Optimization]] is the mechanical core of this page.

### What the bounded loop has actually delivered

- Karpathy's **autoresearch** ran ~700 experiments on a single GPU against nanochat, kept ~20 changes
  that transferred, and cut time-to-GPT-2-quality from **2.02 to 1.80 hours**. Prime Intellect scaled
  the same keep-or-revert loop to ~10,000 trials and beat the human baseline.
- **AlphaEvolve** found a 48-multiplication algorithm for 4x4 complex matrix multiplication (one fewer
  than Strassen's 49) and sped up a kernel used to train Gemini by 23%.
- **Cline** hill-climbed Opus 4.5 from 47% to 57% on Terminal Bench by hand, then had an agent run the
  same method for 17 hours and about $50 of compute, moving Kimi K3 from 69 to 79 of 89 tasks.

Every one of these is bounded: in each, the fitness function sat outside the editable region.

### The negative results are as informative as the wins

**HarnessOpt-Bench** separates the editing agent from the tester and scores candidate harnesses on
hidden tasks; across 111 runs, 5 optimizer models, and 4 tasks, results **varied sharply by model and
task**. **PAST-Bench** asks whether stored experience helps later episodes and finds that in many
scenarios turning memory on **does not help** — an uncomfortable result for the
file-system-as-memory pattern this vault otherwise endorses. A Princeton-led study found agents can
execute much of the *engineering* of AI research while still struggling to choose original and useful
directions.

### Model-harness co-evolution is the near-term shape

SIA updates both a task agent's harness and its weights; Recursive Harness Self-Improvement edits a
harness partly to produce **better traces for training future models**. This is the least speculative
description of where the field is going, and it is the one the evidence supports.

### Why the verifier has to stay out of reach

Schmid's formulation is blunt: **"If it can edit evaluation, it can jailbreak itself. Reward hacking
is the default behavior of a system asked to raise a number."** The agent may change prompts, skills,
tools, memory, and harness code; a separate entity must own the evaluation. That constraint is exactly
what keeps current systems at self-improvement rather than recursion — and it is why
[[Lilian Weng - Harness Engineering for Self-Improvement]] reports that the working rung-4 systems
(AHE, Self-Harness) make the verifier, tracer, runs directory, and model configuration **read-only**.

Schmid's closing point is the one that does not have an engineering fix: **taste lives outside the
loop.** Agents will raise any number they are given. Deciding what counts as a win — and that reward
hacking does not — is still a human job.

## Recursive structure is not itself the gain

Weng's survey supplies the cleanest refutation of the idea that recursion is doing the work. **STOP
improved when driven by GPT-4 but degraded with GPT-3.5 and Mixtral.** Applying a self-improvement
loop to a weak proposer makes it worse, because the loop amplifies whatever candidate quality the base
model can generate.

The scaling picture is stranger still. Weng cites Lin et al. finding that **harness-updating capability
is roughly flat** from ~9B parameters to frontier models — small models write skill files procedurally
similar to those from much larger ones — while **harness-benefit is non-monotonic**, peaking for
mid-tier models. Weak models cannot exploit a good scaffold; the strongest already know most of what
it would say. Self-improvement returns are therefore highest in the middle of the capability range,
not at the frontier.

## A shipped loop whose memory is the artifact

[[Baseten - Agentic Kernels in Production]] is a production instance of the loop this page separates out as
the one where **the scaffold's memory**, not the weights, is what persists.

Its optimization framework retains kernels that pass correctness and end-to-end checks as reusable candidates,
and — the part worth recording — adds lessons from **both successful and failed attempts** to an evolving
knowledge base, alongside workload constraints and integration findings. Successes are captured as reusable
patterns, **failures as caveats and root causes**, with dead ends explicitly recorded. Each iteration starts
from accumulated experience.

Two observations. **Recording failures is the substantive design choice.** A store of successful patches is a
cache; a store that also explains why a class of attempt does not work prunes the search space on every
subsequent run, which is what makes the loop converge rather than merely repeat. This is structurally the same
argument this vault makes for itself in [[Persistent Wiki]] — the durable asset is the record of what was
tried and what it cost.

**And the gains are bounded by the domain, not by the loop.** The same framework returns **42.3%** on
diffusion models but about **5.5%** on LLMs, because LLM kernels are already heavily human-optimized. Self
improvement converges on the headroom that exists; where prior effort has removed it, the loop has little to
find. This is a concrete case of the caution already on this page that recursive structure is not itself the
gain. See [[AI-Generated Kernels]].

## A self-improvement loop with the model held fixed

[[Meta - An Organizational Second Brain]] is a useful boundary case for this page: a genuine improvement loop in
which **the model never changes.** Over three two-week sprints, the only thing that improved was a body of 200+
text files, compiled from expert feedback under regression tests. It supports this page's existing position that
parameters and scaffold are separate update surfaces, by showing the scaffold surface moving alone.

What makes it more than an anecdote is that the loop is defended at every stage, and each defence targets a
failure mode this page has recorded elsewhere:

- **Against misattributed fixes:** diagnosis asks *"could the agent have reached the correct conclusion from its
  source materials?"* — separating a broken procedure from missing knowledge from an organisational position
  nobody has actually decided.
- **Against self-serving justification:** an **independent adversarial reviewer** sees only the diffs, with no
  knowledge of the rationale, and argues against them. Withholding the story is the mechanism.
- **Against silent capability trades:** every fix becomes a permanent regression test, and validation replay is
  **blind on both sides** — the agent does not know it is being tested, the judge does not know what changed.
- **Against unverifiable structure:** a deterministic linter that passes or fails on dangling references,
  file-size budgets, identifier collisions, and dependency cycles.

The honest reading of the results is that they do not yet demonstrate much. "Useful almost all the time," "days
to minutes," and **"zero regressions"** are qualitative, without baselines, task counts, or comparison against
fine-tuning on the same workload — and the zero-regression claim is measured by a suite the loop itself wrote. As
evidence of a *design* for constrained self-improvement it is valuable; as evidence of *effectiveness* it is not
yet decisive. See [[Institutional Knowledge Agents]].

## The recursion runs through artifacts, not weights

[[@zafstojano - Recursive Synthetic Improvement]] proposes a deflationary but far more checkable reading: RSI "might as well stand for
**Recursive Synthetic Improvement**." The loop is not a model rewriting itself; it is that "a
human-generated artifact gets replaced by a model-generated one, which trains better models, which then
generate better artifacts", with human effort redirected to whatever is not yet automated.

The value of the reframing is that it decomposes into **five stages that can each be audited separately**
for whether the human has actually been removed: the **Judge**, the **Corpus**, the **Teacher**, the
**Curriculum**, and the **Environment**. Each sits at a different point on that arc, and each has
published evidence and published limits — collected under [[Synthetic Data Flywheel]].

**The clearest single piece of evidence is accidental.** GLM-5.3 has the same base, the same architecture,
and the same total and activated parameters as GLM-5.2; the difference is **one month of scaling
long-horizon environments and RL**, and "the gains are not marginal." Jie Tang's gloss is that "the dials
do not have to be turned together" — against Noam Shazeer's earlier framing that "FLOPs were intelligence;
parameters were knowledge."

**Two caveats belong with the claim, and the first is the author's own.** The apparent exponential "is
mostly an artifact of just how little these labs disclose" — most of the timeline is assembled from
technical reports written by parties with an interest in the narrative. And the survey documents five
automated stages without ever establishing that the loop **compounds**: better judges improving corpora
improving teachers is asserted by arrangement, not measured.

The distillation dispute that usually accompanies RSI claims is left unresolved here too. Anthropic
accused Moonshot of exfiltrating **3.4 million exchanges**, and Panfilov et al. disclosed that encrypted
reasoning traces are interchangeable across sessions and models within a provider's ecosystem — but the
evidence that Kimi K3 was prefilled with decoded Opus 4.8 reasoning is explicitly **inconclusive**, and
the counter-evidence (RL's Razor, *Retaining by Doing*, *SFT Memorizes, RL Generalizes*) points the other
way. Nathan Lambert's formulation closes it: **"One does not simply 'distill' RL environments,
infrastructure to run them at scale, or algorithms to mix them together effectively."**

## Recursion begins when the improvement process enters the editable set

[[Turing Post - What Is Recursive About Recursive Self-Improvement]] supplies a boundary test for the
examples above. Repeated optimization with fixed objectives, compute, permissions, and evaluation is
AI-assisted improvement, not necessarily recursion. The recursive claim strengthens only when the
system can alter search strategy, experiment design, experience acquisition, environment adaptation,
or the process that produces the next improvement.

That boundary creates a governance regress. If the evaluator that certifies progress becomes editable,
some protected test, human judgment, formal check, or external measurement must remain outside the
loop. The source reports no self-sustaining capability growth; it is a taxonomy and control argument.

## Co-evolution and meta-agent editing are different claims

[[Ben Dickson - How AI Agents Are Learning to Optimize Their Own Stack]] reports HarnessX
reusing harness trajectories to train the backbone, then feeding new behavior into later
harness evolution. That is a coupled weights-and-scaffold update rather than the frozen-model
workflow in the earlier briefing. It does not alone establish improved ability to make the
next improvement or self-sustaining capability growth.

Hyperagents targets another axis: a task agent and its modifying meta-agent share an editable
program, so the modification process can change too. EnvHarness edits the training experience
without changing the stated core logic or verifier; Raven targets coordination. These examples
separate *what changes* from *what counts as progress* and do not form a mandatory hierarchy.

The source's practical rule is therefore narrower than "make everything self-improving":
locate the bottleneck, authorize the smallest relevant update, preserve the artifacts needed to
attribute it, and keep independent evaluation. The newsletter's reported task gains are not
measurements of an indefinitely compounding research loop.

## Two objections that do not depend on capability at all

Every argument above locates the limit inside the loop: the verifier can be captured, the proposer is too weak,
the harness benefit peaks mid-range, taste sits outside. Two October 2026 essays argue the limit is somewhere
else entirely — one in the **scaling exponent** of parallel research, one in the **substrate** the loop runs on.
Neither is an experiment. Both deserve to be kept as arguments, and they **disagree about where the ceiling
lives**, which is more useful than merging them.

### The exponent is too small

[[Ramez Naam - Can a Million AI Agents Create Superintelligence]] is a synthesis of roughly a dozen third-party
multi-agent scaling results, not a study. Its author's summary of his own epistemic position —
**"We're all operating on far too little real world data."** — should travel with every number below.

The argument is that adding agents buys **speed** far better than it buys **collective intelligence**, so a
takeoff model that assumes parallel research scales near-linearly is assuming something the measurements do not
show. The curves he assembles are collected on [[Test-Time Scaling]]; the ones that bear on recursion are the
saturating ones. On Anthropic's Opus 5.5 formal-math benchmark (49 weighted theorem statements, 24 hours per
team), going from **ten to one hundred agents added 27 score points and going further added two** — even though
the hundred-agent team organised itself into a hierarchy with 12 sub-leads and could spend roughly 10x the
aggregate runtime. On Lean formal math the local speed exponent **λ fell from about 0.75 to 0.33** across
10→30 and 30→100 agents.

**The spread between published models is the actual argument.** Fed the same input — Anthropic's reported
research-agent ratios of about **9 agent-hours per human work-hour by mid-July** and **19** by late August,
against a company-wide ratio near **6** — the scaling assumptions in circulation disagree by an order of
magnitude about how much faster research should now be: Chan et al. (2026)'s exponent implies roughly **25x**
April's pace by August, Davidson and Houlden's 0.6 parallel-research exponent about **2-4x**, plain logarithmic
scaling about **2x**, and the sub-logarithmic shapes Naam collects only **1.1-1.8x**. Those conversions assume
equal value per agent-hour and treat additional runtime as parallel labour; both are strong assumptions the
author flags.

This is the first thing on this page that attaches a **number** to the gap between workflow self-improvement
and strong RSI. The existing table calls strong RSI "mostly aspirational" on the grounds that nobody has
demonstrated it; Naam's contribution is a quantitative gap rather than a merely undemonstrated one. The
number itself comes from his **earlier** RSI post, where he calibrated the measured **software feedback
loop** — gains from smarter models — at roughly **five to ten times below self-sustaining strength**. The
parallel-scaling curves assembled in *this* essay are separate third-party evidence; Naam attaches no
comparable multiple to them, reporting instead that multi-agent intelligence gains look logarithmic or
sub-logarithmic and therefore "too weak to make RSI self-sustaining". His forecast — allowing a
**six-month** research-to-publication lag — is no
sustained acceleration in the Epoch Capabilities Index through the first half of 2027 (see [[Epoch AI]]), and
he states he expects data to correct him.

Crucially, the essay **does not falsify runaway RSI**. It argues the scaling assumptions inside those models
exceed current evidence, it measures nothing near a million agents, and it concedes that better coordination,
more diverse training, recombination, or new learning methods could change the curves.

### The substrate degrades as you scale on it

[[The Decoherence Trap]] is an **unattributed essay** — no author is named anywhere in the capture, which is
published at maevyn.codes — and it is an argument built on analogy and a self-declared toy simulation, not a
measurement. It should never be cited as evidence about how real systems behave.

Its objection is structurally different from Naam's. **Decoherence** is defined as the accumulation of locally
valid but mutually incompatible or redundant models in a system that keeps changing, distinguished from
infrastructure debt (wear) and technical-advancement debt (the need to upgrade). The cost is combinatorial:
with multiple coexisting paradigms, interactions multiply, so each later change requires more analysis and time
pressure produces further shortcuts. The claim that bears on this page is that **more agents help only while
complexity grows linearly** — if each rushed change raises the cost of the next one, parallel capacity cannot
indefinitely compensate, and the end state the essay names **Decoherence Collapse** is systems too complex for
humans to repair that agents cannot recohere either.

Extended to RSI, the argument is that an AI optimising inside a data-centre bubble can improve a program's
speed, size, and efficiency while having no way to verify that its changes remain **globally coherent or
useful**, because usefulness is defined outside the bubble. The essay ties this to Tom Reed's **Goodhart
Singularity** and to Goodhart's law, and supports it by analogy: Boole published Boolean algebra in **1847** and
Shannon connected it to relay circuits in **1937**, so a locally valid formal result can sit unimportant until a
real problem supplies the context. It cites a **September** declaration signed by Terence Tao and **24 other
Fields Medalists** arguing that solving problems is only a proxy for mathematical understanding.

**This is the same shape as the verifier argument this page already carries, pushed one level out.** Schmid's
constraint is that the agent must not be able to edit its evaluation. The decoherence argument is that even an
unreachable verifier is only a proxy if nothing outside the loop re-grounds it — so the governance regress
already recorded here does not terminate at "keep the verifier read-only"; it terminates, if at all, in contact
with reality.

The third-party studies it cites are the most concrete negative evidence the vault holds on agent-assisted
development, and they are about coding throughput rather than about RSI:

| Study, as cited | Scope | Reported result |
| --- | --- | --- |
| Chen and Stratton, Harvard working paper | 718 companies | coding agents increased code written by **30%** with no measurable increase in finished work; pull requests took **49% longer** to review and **nearly twice as many** were returned for changes |
| He et al., Carnegie Mellon | open-source projects adopting Cursor | large initial velocity increase that **did not last**; rising code complexity contributed to the later slowdown. **No effect size is quoted** |
| Liu et al. | over **300,000** AI-authored commits across more than **6,000** repositories | approximately **one in eleven** commits — up to **one in seven** depending on assistant — introduced at least one quality issue; **nearly a quarter** of those issues remained in the code |

The essay's own simulation should not be read as support for any of this. Coherence settings of **-0.2, +0.2,
+0.6, +0.8** produced displayed feature counts of **152, 247, 417, 376**, implying a mid-range "sweet spot" —
and the author states plainly that **"The simulation has arbitrary weights and does not definitively prove that
this is how complex systems will evolve."** Those are outputs of a toy model under chosen parameters, not
measurements of software.

### Why keeping both matters

Naam says the loop is too weak to run away; the decoherence essay says the ground under the loop erodes while it
runs. They are not the same claim and they imply different tests. Naam's resolves with a measurement — G, λ, and
N on real AI research. The decoherence claim resolves only with a fitted growth rate for complexity in
production codebases, which **nobody has produced**, including this essay.

## Open questions

- What evaluation signal is strong enough for automated research loops without causing reward hacking or benchmark overfitting?
- Which parts of the AI development loop should remain human-controlled even if automation becomes possible?
- How do teams measure whether an AI research agent is genuinely improving research direction rather than only increasing experiment volume?
- When does workflow-level self-improvement become model-building-level recursive self-improvement?
- How would a system strengthen its own verifier *without capturing it*, and how would that claim be
  checked without appealing to an outer verifier? Schmid's definition requires this step; nobody has
  demonstrated it, and the regress has no stated termination.
- If harness-benefit peaks for mid-tier models while harness-updating capability is flat, does
  self-improvement research have a shrinking window as base models improve?
- PAST-Bench finds stored experience often fails to help later episodes. Is that a failure of memory as
  a mechanism, or of retrieval policy? The vault's file-system-as-memory pattern assumes the latter.
- Plugin-kernel harnesses maximize the rewritable surface at exactly the moment the argument says the
  verifier must stay unreachable. Which of the two trends gives way?
- **Neither October objection is a result.** Naam measures no team near a million agents, proves nothing
  about whether conceptual breakthroughs can be parallelised, and does not show that benchmark scaling curves
  transfer to real research. The decoherence essay demonstrates no exponential complexity growth in any real
  system, shows no system that has reached Decoherence Collapse, and does not establish that agents cannot
  maintain or repair highly complex systems. Both are arguments that current takeoff models assume more than
  the evidence supports.
- **Is the measured parallel-scaling exponent a property of today's models or of multi-agent work as such?**
  The Opus 5.5 and Opus 5 comparison suggests coordination ability improves between model generations, which
  would move the curves this page just recorded.
- **Does decoherence apply to the loops this page actually describes?** The cited studies concern human teams
  adopting coding assistants in production repositories. Nothing links them to a bounded self-improvement run
  against a fixed verifier, where the editable region is small and the artifact is discarded if it fails.
- **Can a verifier be re-grounded without a human?** If an unreachable verifier is still only a proxy, the
  decoherence argument requires contact with reality to correct it — and no source here describes what that
  contact looks like mechanically, or how often it has to happen.
- **What would falsify either objection?** G, λ, and N measured on real AI research would resolve Naam's; a
  fitted complexity-growth rate on production codebases would resolve the other. Neither exists.

## Related pages

- [[Ramez Naam - Can a Million AI Agents Create Superintelligence]]
- [[The Decoherence Trap]]
- [[Ramez Naam]]
- [[Test-Time Scaling]]
- [[Agent Delegation]]
- [[Epoch AI]]
- [[Legacy Code Modernization with AI Agents]]
- [[AI-Native Software Development Lifecycle]]

- [[Ben Dickson - How AI Agents Are Learning to Optimize Their Own Stack]]
- [[Graph Engineering]]
- [[Zhe Ren et al - Self-Improvements in Modern Agentic Systems]]
- [[Automated AI Research]]
- [[Alyona Vert - AI 101 - What is Recursive Self-Improvement]]
- [[Agentic Loop]]
- [[Agent Skill]]
- [[AI Agents in Production]]
- [[Recursive Architectures]]
- [[Coding Agent Harness]]
- [[Alpha Signal - Why self-improving harnesses are the next frontier]]
- [[Reinforcement Learning]]
- [[Mahesh Sathiamoorthy - RL Environments Are All You Need]]
- [[Continual Learning for Agents]]
- [[AI-Generated Kernels]]
- [[Wafer - AI Performance Engineering Resources]]
- [[Benchmark Optimization]]
- [[Harness Optimization]]
- [[Philipp Schmid]]
- [[Lilian Weng]]
- [[Lilian Weng - Harness Engineering for Self-Improvement]]
- [[Philipp Schmid - Recursive Self-Improvement]]
- [[Baseten - Agentic Kernels in Production]]
- [[Inference Efficiency Frontier]]
- [[Institutional Knowledge Agents]]
- [[Meta - An Organizational Second Brain]]
- [[Meta]]
- [[LLM-as-a-Judge]]
- [[@zafstojano - Recursive Synthetic Improvement]]
- [[Synthetic Data Flywheel]]
- [[RL Environment Design]]
- [[@zafstojano]]
- [[Nathan Lambert]]
