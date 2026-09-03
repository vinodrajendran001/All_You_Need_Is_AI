---
type: concept
created: 2026-06-02
updated: 2026-09-03
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

## Open questions

- Which conversation-level outcomes can be safely reduced to binary or rubric-based checks?
- How much simulation fidelity is enough before offline metrics become misleading?
- What is the right balance between always-on online scoring and cheaper sampled evaluation?
- Do agent and coding benchmarks carry a text-side analogue of the acoustic "which test am I taking" cue, and how would a team detect it in their own regression suite?

## Related pages

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
