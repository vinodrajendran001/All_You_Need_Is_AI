---
type: concept
created: 2026-06-22
updated: 2026-09-04
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

[[Alpha Signal - Why self-improving harnesses are the next frontier]] supplies concrete 2026 examples that sit firmly on the *workflow* end of this spectrum: **Self-Harness** and **HarnessX** let an agent rewrite its own [[Coding Agent Harness|harness]] — mining failure traces, proposing edits, and gating them behind regression tests (HarnessX even frames the search as RL via its AEGIS engine). Crucially, they improve the *operating environment*, not the base model, so their gains are bounded by the model's latent capability — the exact distinction between self-improving agents and stronger model-building RSI. They also inherit the risks named here (reward hacking, catastrophic forgetting), which they claim to guard against but do not prove settled.

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

**Two surfaces, very different economics.** Parameter updates can come from generated demonstrations,
intrinsic evaluation, or grounded experience — the [[Agentic Reinforcement Learning]] path, expensive
and centralized. Scaffold updates modify prompts, memory, tools, workflows, and control logic, and
are cheap, fast, and available to anyone deploying an agent without training access. Most systems
described in this vault improve themselves through the scaffold; the survey's contribution is naming
that as a legitimate self-improvement mechanism rather than mere configuration.

The survey's own governance recommendation follows directly: because scaffold updates are cheap and
unconstrained, they should be **versioned, validated, and reversible**. That is the same reversibility
requirement [[Agent Security and Governance]] applies to agent actions, turned on the agent's own
definition.

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

## Related pages

- [[Zhe Ren et al - Self-Improvements in Modern Agentic Systems]]
- [[Automated AI Research]]
- [[Alyona Vert - AI 101 - What is Recursive Self-Improvement]]
- [[Agentic Loop]]
- [[Agent Skill]]
- [[AI Agents in Production]]
- [[Recursive Architectures]]
- [[Agent Skill]]
- [[Coding Agent Harness]]
- [[Alpha Signal - Why self-improving harnesses are the next frontier]]
- [[Reinforcement Learning]]
- [[Mahesh Sathiamoorthy - RL Environments Are All You Need]]
- [[Continual Learning for Agents]]
- AI-Generated Kernels
- Wafer - AI Performance Engineering Resources
- Benchmark Optimization
- [[Harness Optimization]]
- [[Philipp Schmid]]
- [[Lilian Weng]]
- [[Lilian Weng - Harness Engineering for Self-Improvement]]
- [[Philipp Schmid - Recursive Self-Improvement]]
- [[Baseten - Agentic Kernels in Production]]
- [[AI-Generated Kernels]]
- [[Inference Efficiency Frontier]]
- [[Institutional Knowledge Agents]]
- [[Meta - An Organizational Second Brain]]
- [[Meta]]
- [[LLM-as-a-Judge]]
