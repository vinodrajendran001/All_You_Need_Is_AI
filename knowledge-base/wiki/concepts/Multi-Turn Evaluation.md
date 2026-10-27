---
type: concept
created: 2026-06-02
updated: 2026-10-27
tags:
  - concept
  - llm-evaluation
  - conversations
  - simulation
  - traces
source_ids:
  - src-2026-06-02-bytebytego-doordash-testing-system
  - src-2026-05-29-braintrust-multi-turn-scoring
  - src-2026-07-06-sarthak-rastogi-production-agent
  - src-2026-08-05-aibuilderclub-how-to-evaluate-ai-agents
  - src-2026-08-05-aibuilderclub-loop-engineering-guide-2026
  - src-2026-08-05-aibuilderclub-reviewing-ai-generated-pull-requests
  - src-2026-08-07-zach-lloyd-computer-use-verification
  - src-2026-08-07-mahesh-sathiamoorthy-rl-environments-agents
  - src-2026-08-12-yoko-li-loop-convergence
  - src-2026-08-21-hume-ai-asr-benchmark-optimization
  - src-2026-09-02-paolo-perrone-agentic-testing
  - src-2026-08-31-bytebytego-chatbot-request-lifecycle
  - src-2026-09-06-rastogi-agent-observability
  - src-2026-09-28-martin-automating-eval-design-hillclimbing
  - src-2026-10-05-bytebytego-lost-middle
  - src-2026-10-06-bytebytego-sycophancy
  - src-2026-10-06-arush-self-modeling-emergent-misalignment
  - src-2026-10-20-husain-decision-model-evals
  - src-2026-10-16-west-eval-engineering-lessons
  - src-2026-10-06-iusztin-rag-evals
status: active
---

# Multi-Turn Evaluation

## Definition

Multi-turn evaluation is the practice of measuring an AI system over an entire conversation or interaction trace, not just over isolated single responses. It usually combines turn-level checks with conversation-level outcome metrics such as resolution, consistency, policy compliance, or progress.

## Why it matters

Many conversational failures only emerge across turns: repeated questions, contradictions, circular dialogue, missed escalations, or a polite conversation that never actually solves the user's problem. If evaluation only scores individual responses, those failures remain invisible.

## Current synthesis

- The Braintrust article makes the base point explicit: turn-level and conversation-level scores answer different questions, and both are necessary.
- Turn-scoped metrics catch local issues such as tone, helpfulness, or policy alignment. Trace-scoped metrics catch global issues such as resolution, consistency, and whether the conversation made meaningful progress.
- Structured traces are a prerequisite. If turns are not grouped into a single conversation object, multi-turn evaluation becomes impossible or unreliable.
- [[LLM-as-a-Judge]] becomes especially useful here when the judging task is narrow and explicit: binary policy checks, resolution checks, or constrained rubric facets tend to be more calibratable than fuzzy holistic scoring.
- The DoorDash flywheel extends the pattern from passive scoring into active development. Human reviewers identify a failure mode, engineers write an evaluation, a simulator generates realistic multi-turn chats from historical scenarios, the system runs the assistant against those scenarios, and the resulting pass rate becomes a release gate.
- Simulation matters because production conversations are too expensive and risky to use as the only testing environment. Synthetic but transcript-grounded multi-turn chats let teams iterate on prompts, context shaping, and backend behavior offline.
- Aggregation closes the loop. Once turn and trace scores exist at volume, clustering and topic analysis can surface recurring failure modes instead of forcing humans to read every conversation manually.
- [[Sarthak Rastogi - Making an AI Agent Production-Ready]] pushes the same loop into the *release process*: a regression suite re-scores a fixed set of queries on **faithfulness + completeness** against a baseline on every prompt or model change, because a model upgrade that raises average quality can silently regress a specific query category. Paired with A/B model routing (send N% of traffic, compare scores before cutover), evaluation becomes a deployment gate, not just a monitoring surface.

### Operate the artifact

[[AI Builder Club - How to Evaluate AI Agents - What Works in 2026]] adds a strong acceptance rule: evaluate the artifact through its real interface rather than only reading the agent's report. Run tests, exercise the UI, inspect generated files, and preserve the full trace so failures can become regression cases. A fresh-context evaluator reduces shared-reasoning bias but does not remove model-family blind spots, so deterministic and behavioral gates remain preferable where possible.

[[Zach Lloyd - The computer use verification skill that every agent needs]] provides the UI-specific implementation: reproduce and verify modes operate the application and attach screenshots or video to the trace. [[Mahesh Sathiamoorthy - RL Environments Are All You Need]] generalizes the same idea into reusable scored environments that can evaluate model, prompt, skill, or harness changes against held-out tasks.

[[Yoko Li - Knowing When to Stop - The Art of Making a Loop Converge]] adds evaluator failure as a trace-level outcome: a loop may diagnose that a target is unreachable while an external evaluator keeps sending it back. Evaluation must therefore distinguish task failure, verifier mismatch, impossibility, and diminishing returns rather than treating every non-pass as another retry.

### Test the test set

Everything above assumes the evaluation set measures what it claims to. [[Hume AI - Measuring Benchmark Optimization in Speech Recognition]] supplies the vault's first rigorous demonstration that this assumption can fail systematically, and its probe design is domain-independent: **construct inputs where the benchmark's answer and the correct answer disagree, then see which one the model produces.** Three transferable instruments — reproduce the benchmark's known reference *errors*, delete the required information from the input and see if it reappears, and offer a choice the input cannot decide — separate recall of the test from capability at the task.

The finding that should change reading habits: on two widely used ASR benchmarks the models with the **lowest** error rate were the most likely to reproduce erroneous references, so leaderboard rank order was partly anti-correlated with the capability being measured. This is the evaluation-side twin of the reward hacking discussed in [[Reward Design for RL]], and it strengthens this page's core argument — a static, public, i.i.d. test set is exactly the artifact an optimiser learns to recognise. The recommended remedies are structural: fully held-out sets, and temporal, speaker, or metadata-based splits rather than random ones. See [[Benchmark Optimization]].

## pass@k measures the wrong thing

[[Paolo Perrone - What is Agentic Testing]] draws a distinction that applies to most capability numbers this
vault holds. **pass@k** asks whether a system succeeded **at least once** in k attempts; **pass^k** asks
whether it succeeded **every** time. The worked example — five checks over three runs — gives **pass@3 = 0.6**
against **pass^3 = 0.4**. The instruction is unhedged: *"Report pass^k."*

For multi-turn work the gap is wider than that example suggests, because a multi-turn task compounds
per-turn reliability: an agent that clears each of ten turns 90% of the time completes the whole conversation
about a third of the time. pass@k hides exactly this, and it is the failure users experience.

**A second variance source sits below the model.**
[[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]] reports that temperature 0
does **not** produce deterministic output, because numerics depend on batch composition — **1,000 identical
prompts yielded roughly 80 distinct completions**. So a single-run score is partly a measurement of the
serving stack, and re-running an eval on a differently loaded cluster is not a re-run of the same experiment.

Together these argue that any evaluation reported as a single number, from a single run, at temperature 0,
is under-specified. The minimum honest report is k runs and a pass^k. Note the ~80-completions figure is given
without attribution in an explainer and should be treated as indicative.

## Evaluation presupposes a reconstructable run, and the hardest failures are found by humans

[[Sarthak Rastogi - Making AI Agents Observable, Monitorable, and Production-Ready]] places observability logically prior to evaluation: evals "tell you whether that
chain was *good*", but only once the chain can be reconstructed. Without a causal trace there is nothing
for a multi-turn evaluation to attach its judgement to.

The finding that should temper confidence in test suites: in an eight-week study of 22 fully-traced
production incidents, **roughly 70% of "fail-plausible" incidents were discovered by a human noticing
something was off, and close to 0% were caught by unit tests** — "because the output isn't malformed, it's
just wrong." The canonical case is a warranty tool that rate-limits during a deploy spike and returns null
with no error field; the model, "seeing nothing that looks like a hard failure", tells the customer their
device is covered.

Two detectors partially close that gap, and neither is a test: mark degraded tool results with an explicit
`input.anomalous=true` attribute on the span feeding the next model call, and track
`fallback_response_rate` — where a near-zero value indicates the agent has never declined to answer rather
than that it is performing well.

**Retrieval can also succeed and still fail through context position bias**, where "a critical policy
clause buried in the middle of five retrieved documents can be ignored even though retrieval technically
'worked.'" The detector is a rank comparison: track the rank of the passage the model actually cites
against the rank at which it was retrieved.

Multi-agent evaluation needs trace context propagated across handoffs, so a receiving agent creates a
child span under the same trace ID rather than an orphaned trace — formalised by the A2A Traceability
Extension with parent/child step IDs and per-step cost accounting.

## Build the eval from real traffic first, and synthesize only when nothing real is left

This page has argued for simulation without ranking it against the alternatives.
[[Lance Martin - Automating Eval Design and Hillclimbing with Claude]] supplies the ordering. Cases are
sampled in a **fixed order of preference**: production transcripts first, then bug reports and support
tickets, then **five to ten cases written by hand**, then cases synthesized from the codebase. Synthesis
is the last resort rather than a parallel option, which sharpens the DoorDash flywheel already recorded
here — that simulator is transcript-grounded, and the ordering explains why that grounding is the load-
bearing part rather than a convenience.

The four properties Martin requires of a usable evaluation include **low run-to-run variance**, which is
this page's pass^k concern restated as a construction requirement: a suite with high variance cannot
support the multi-run reporting this page demands, because the variance being reported is partly the
suite's own. The diagnostic operationalizes it — run **the grader twice on the same output** to separate
grader noise from system noise, check for timeouts, API errors, and truncated responses, and report a
confidence interval with one full transcript per case. The other three properties are a production-like
task distribution, scores that rise with stronger models and more effort, and frontier performance with
**headroom below 100%**, with a warning fired when the baseline is about **95% or higher**.

Grader choice follows output shape: programmatic checks for constrained outputs, LLM-as-a-judge for
open-ended ones, and judges that **check specific claims rather than emit a 1-to-5 scale**. That agrees
with this page's existing position that narrow, explicit judging calibrates better than holistic scoring,
and it comes with the concession that keeps it honest — a misconfigured judge still requires a human to
read scored transcripts, which is why one full transcript per case is an output of every run rather than
an optional artifact. See [[LLM-as-a-Judge]].

What the source does not contribute is anything about the turn-versus-trace distinction this page is
built on. Its worked examples score a single per-ticket decision on a **44-case** internal benchmark
(**30** for search, **14** held out), which is outcome scoring on isolated cases, not conversation-level
measurement. So it strengthens the construction and noise-control side of this page while leaving the
aggregation side untouched, and every figure in it is Anthropic-reported on an Anthropic workflow with no
independent reproduction and no released evaluation data; see [[Anthropic]].

## Position, pressure, and behavioral generalization need different controls

[[ByteByteGo - The LLM Blindspot - Lost in the Middle]] strengthens the earlier retrieval warning:
test the same question and evidence at different prompt positions, with length and distractors
controlled. Missing or truncated evidence is a different failure from available-but-unused
evidence. A RULER length curve is not itself a position-controlled result, and citation rank is a
diagnostic rather than proof of the cause.

[[ByteByteGo - Why LLMs Agree With You Even When You Are Wrong]] adds a conversation-level pair:
does an answer change under unsupported user pressure, and does it change appropriately when a
valid correction arrives? Score factual commitment separately from emotional acknowledgment.
Neither rigid disagreement nor a second model's agreement establishes truth.

[[Arush et al - Self-Modeling Interventions Modulate Emergent Misalignment]] adds a useful warning
about outcome labels. Its "agentic" evaluations are **single-turn scenarios with no tools**, not
executed trajectories; TruthfulQA **error is one minus accuracy**, separate from its other
misalignment metrics. Standard EM recovery can coexist with residual TruthfulQA errors, and
prevention is weaker than reversal. The findings motivate broader regression coverage but do not
demonstrate multi-turn agent safety.

## A trace-level grader that returns one number still needs a cutoff

This page scores conversations with judges that write.
[[Hamel Husain - How To Use Decision Models for Evals]] scores them with judges that do not. Each system
under test receives a whole **masked trace** — conversation plus actions, with labels and reviewer notes
removed — and returns a single **failure probability from 0 to 1** for that trace. This is trace-level
evaluation in its most compressed form: one scalar per conversation, no per-turn attribution, no
rationale text for a human to read.

The compression moves the design problem onto the **threshold**. Scores at or above **0.50** are flagged
by default in the tested APIs, and the author's position is that this default is inherited rather than
optimal: a model scoring failures **0.40** and passes **0.10** would classify his illustration perfectly
at **0.30** and catch nothing at **0.50**. Tuning used stratified **five-fold** cross-validation over
**98** traces — **61** known failures, **37** with no labeled failure — choosing thresholds on training
folds and measuring on held-out folds. The detail that matters for suite builders is that this runs on
**saved scores and requires no new model calls**, so the cutoff can be re-derived whenever the label set
grows, which is not true of re-running a generative judge.

Two cautions attach to this page's existing concerns. **Feasibility is not guaranteed:** a constrained
rule requiring at least **80% precision and 80% recall** on training data — the author's example of a
business rule, not a standard — fell back to unconstrained F1 in **36 of 100** training splits for
Perplexity and **29 of 100** for Liquid d1-ultra, against **0 of 100** for OpenAI Decisions. And **the
task was deliberately broad**: one "does this trace contain a failure" question, chosen to make model
differences visible, which Husain says may exaggerate the gaps and which he would replace in production
with separate judges per failure mode. That is the opposite move from this page's turn-versus-trace
split — it collapses the trace rather than decomposing it — and the author recommends against it for
real use.

The scope is one private 98-trace dataset in one domain, with the original conversations withheld, so it
is not independently reproducible. Its class mixture, **61 to 37**, is also far more failure-heavy than
most production traffic; precision depends on prevalence, and the source states only that a tuned
threshold is not shown to transfer to another dataset. This page reads that as a reason to treat the
cutoff as local to this mixture rather than as a portable setting.

## Grade the trajectory, keep its turn boundaries, and run a credential-free condition beside the live one

[[Casey West - Four Evaluation Engineering Lessons from Building Agent Plugins]] reports the mirror
image of the fail-plausible incidents above: an agent that behaved correctly and was graded as
failing. On the initial 11-prompt suite for the newly released Google Cloud Developer plugin, an LLM
judge that read the final reply against a checklist failed three prompts that the raw tool-call logs
showed had passed. In a Cloud Run cleanup whose rubric required checking command syntax first, the
agent's first step was `gcloud help run services list`, but its closing message warned about
permanent data loss instead of mentioning the check: "The grader penalized the agent for doing the
right thing simply because it didn't brag about it in the summary." A judge asked whether something
ran "is guessing unless you evaluate the actual tool-call trajectory", which applies the acceptance
rule from [[AI Builder Club - How to Evaluate AI Agents - What Works in 2026]] (evaluate the artifact
through its real interface, not the agent's report) to the grader itself.

The second lesson refines the reconstructable-run prerequisite. The harness sent a skill-loading call
and two documentation searches in a single `tool_calls` payload. Because [[Agent Skill|skill]]
activation takes two steps, a short launch stub and then the full instructions on the next turn, the
guidance meant to govern the searches arrived after they had run. A telemetry extractor that flattens
calls into one timeline makes that look like an agent ignoring clear instructions, so a reconstructable
run has to keep its turn boundaries, not only its events. The cause sits in the harness, which never
gave the skill a dedicated turn; the post's remedy sits in telemetry.

The third lesson adds a second condition. Live runs use sandboxed credentials and test execution and
restraint before destructive actions, but they frequently abort on an unexpected permission error at
step two, before reaching the behavior under test. Plan-only runs strip the credentials and ask the
agent to explain what it would do. "Roughly half our most important findings came from the delta
between the two." In one onboarding prompt the live run was blocked at once on a project-list call,
while the plan-only run produced an 8,000-character plan that ignored organization policies, admin
approvals, and governance. In the vault's reading, plan-only changes the instruction as well as the
environment, so the delta mixes the two effects.

The fourth lesson, golden sets for the whole harness, model, and tools stack run as continuous
integration, turns the full trajectory into a standing baseline scored against "golden sets curated by
real human experts who know what the ideal path looks like". The limits are those of a
self-evaluation: single examples from Google's own build on Google's blog, a rough estimate for the
share of findings, no pass rates or later suite sizes, and no count of runs per prompt, so the pass^k
reporting this page asks for is not addressed.

## Before any trace exists, earlier human corrections can label the first eval set

[[Paul Iusztin - Stop Guessing - Evaluate Your RAG App]] partly answers the cold-start question that
the ordering from [[Lance Martin - Automating Eval Design and Hillclimbing with Claude]] leaves open
below. Alexey Grigorev shipped the DataTalks.Club FAQ automation without recording interactions: "My
goal was to just get this out and test how it works." With no transcripts, the first eval set came
from proxy labels. Each contributed GitHub issue supplied an input, and his review of the resulting
pull request supplied the verdict: accepted unchanged was a pass, altered was a fail with a
one-sentence critique. The general advice is to look for "any place a human already judged your
output" and to trace everything from then on.

The answer is partial. It turns *no traffic* into *untraced traffic*: the method needs a system that
already ran under human review, and Grigorev's own advice is to settle how the app should work and
what the UX is first, because evals built for the wrong UX get thrown away with it. Proxy labels also
exist only where a person looked. A false `DUPLICATE` or `WRONG_COURSE` closes the issue with no pull
request, "so I would never discover it", and the article calls that the dangerous error. It is the
labeling-side face of the finding above that people, not tests, catch the hardest failures: a label
set built from human review inherits whatever no person saw.

The case also shows a production eval used as a floor. Each failure is captured as a case first, the
prompt is changed until that case passes, and then the whole set is re-run: "It's kind of test-driven
development, but like eval-driven development." The generation set passes 42 of 61 cases on GPT-5.4
nano, and that score is a baseline that must not fall rather than a target; hard cases may stay
failing so that the prompt does not grow to cover every corner case. Like Martin's per-ticket
decisions, though, these cases are single structured decisions, an action and a section, not
conversations, so the turn-versus-trace distinction this page is built on is again untouched.

This is one community project with 61 generation cases and 25 retrieval cases, relayed in an article
sponsored by Opik, with no confidence intervals and a runner its owner calls "not very scientific"
yet. The proxy labels also inherit reviewer behavior: any edit to a pull request counts as a fail, so
a cosmetic change and a real error carry the same label, and nothing estimates the resulting noise.

## Open questions

- Which conversation-level outcomes can be safely reduced to binary or rubric-based checks?
- How much simulation fidelity is enough before offline metrics become misleading?
- What is the right balance between always-on online scoring and cheaper sampled evaluation?
- Do agent and coding benchmarks carry a text-side analogue of the acoustic "which test am I taking" cue, and how would a team detect it in their own regression suite?
- Production transcripts rank first as a source of cases, but a system with no production traffic can
  only reach the third rung — five to ten hand-written cases. What does the ordering say about the first
  evaluation a team builds, which is exactly the one that decides whether anything ships?
  [[Paul Iusztin - Stop Guessing - Evaluate Your RAG App]] answers part of this: a system that ran
  untraced under human review can label its first set from the reviewer's corrections, much as bug
  reports and support tickets serve the second rung. A system with no reviewed output is still left at
  the third.
- Low run-to-run variance is listed as a property of the evaluation, yet part of the variance lives in
  the serving stack rather than in the suite. Can a suite be constructed to a variance target it does not
  control?
- A single failure probability per trace says that a conversation failed, not where. That comparison
  reports no turn-level attribution and no test of one-scalar trace scoring against combined turn-plus-
  trace scoring, so it leaves this page's central distinction untouched.
- Thresholds there were tuned on a set that is **61** failures to **37** non-failures. Nothing in the
  source says how a cutoff should be re-derived as production prevalence drifts away from the labeled
  mixture.
- The comparison covers one domain and one deliberately broad failure question. Per-failure-mode judges,
  which its author recommends for production, were not measured, so the reported gaps between systems
  may not survive decomposition.
- Golden sets score a run against the path a human expert considers ideal. How should a different but
  valid trajectory get credit, and how much of a live-versus-plan-only difference comes from the
  changed instruction rather than the missing credentials?

## Related pages

- [[Casey West - Four Evaluation Engineering Lessons from Building Agent Plugins]]
- [[Paul Iusztin - Stop Guessing - Evaluate Your RAG App]]
- [[Google Cloud]]
- [[Paul Iusztin]]
- [[Agent Skill]]

- [[Hamel Husain - How To Use Decision Models for Evals]]
- [[Hamel Husain]]
- [[Typed Probabilistic Decision Models]]

- [[ByteByteGo - The LLM Blindspot - Lost in the Middle]]
- [[ByteByteGo - Why LLMs Agree With You Even When You Are Wrong]]
- [[Arush et al - Self-Modeling Interventions Modulate Emergent Misalignment]]
- [[Sycophancy]]
- [[Emergent Misalignment]]
- [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]]
- [[Braintrust - How to evaluate multi-turn conversations]]
- [[Hume AI - Measuring Benchmark Optimization in Speech Recognition]]
- [[Benchmark Optimization]]
- [[LLM-as-a-Judge]]
- [[ML Systems at Scale]]
- [[DoorDash]]
- [[Braintrust]]
- [[Sarthak Rastogi - Making an AI Agent Production-Ready]]
- [[AI Agents in Production]]
- [[AI Knowledge Base Overview]]
- [[Loop Engineering]]
- [[Graph Engineering]]
- [[Agent Security and Governance]]
- [[AI Builder Club - Build AI Agents]]
- [[Zach Lloyd - The computer use verification skill that every agent needs]]
- [[Mahesh Sathiamoorthy - RL Environments Are All You Need]]
- [[Yoko Li - Knowing When to Stop - The Art of Making a Loop Converge]]
- [[Agentic Testing]]
- [[Paolo Perrone - What is Agentic Testing]]
- [[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]]
- [[Sarthak Rastogi - Making AI Agents Observable, Monitorable, and Production-Ready]]
- [[Agent Observability]]
- [[Sarthak Rastogi]]
- [[Retrieval-Augmented Generation]]
- [[Lance Martin - Automating Eval Design and Hillclimbing with Claude]]
- [[Anthropic]]
- [[Harness Optimization]]
