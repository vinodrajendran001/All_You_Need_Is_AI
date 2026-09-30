---
type: entity
created: 2026-08-25
updated: 2026-09-30
entity_kind: organization
tags:
  - entity
  - organization
  - ai-lab
  - claude
  - coding-agents
source_ids:
  - src-2026-08-21-anthropic-ai-native-sdlc
  - src-2026-08-25-bytebytego-stealing-reasoning-traces
  - src-2026-08-28-anthropic-chive-counterfactual-explanations
  - src-2026-09-28-martin-automating-eval-design-hillclimbing
status: active
---

# Anthropic

## What it is

AI research company, developer of the Claude model family and of Claude Code, the coding agent harness that appears across much of this vault's agent material.

## Why it matters here

Anthropic has been an ambient presence in this knowledge base for a long time — Claude Code is one of the reference harnesses in [[Coding Agent Harness]], `CLAUDE.md` is the canonical example of versioned institutional knowledge, and Claude skills recur throughout [[Agent Skill]]. This page exists so that presence has a home.

Its first directly ingested source, [[Anthropic - The AI-Native SDLC Playbook]], is also the vault's anchor for [[AI-Native Software Development Lifecycle]]. What makes it distinctive is scope: rather than describing how to make one agent work well, it describes what happens to an organisation's approval, review, and audit machinery when agents write most of the diff — and proposes rebuilding the lifecycle as a loop of committed artifacts with governance enforced as the agent acts.

Anthropic also appears indirectly on the hardware side. [[Jacob Peake - AI Chip Architectures]] records it as the anchor tenant validating AWS Trainium at frontier scale (over a million Trainium2 chips) and as a Google TPU customer contracted for up to a million chips — one of the clearest examples in the vault of a frontier lab deliberately spreading across non-NVIDIA silicon.

## Notes

- Vault sources are vendor material and should be read as such: the SDLC playbook consolidates the Applied AI team's consulting practice, with no baselines or measured outcomes.
- The playbook credits Jim Blackhurst, Will Steuk, and Jamal Arif for prior work it builds on.

## Reasoning-block exposure

[[ByteByteGo - How to Steal an AI Model's Private Thoughts]] reports that Anthropic returns encrypted reasoning state to clients in a field named `signature`, and that in July 2026 testing **Claude accepted almost every source/target block combination** — the exception being Fable 5, whose blocks only Fable 5 accepted. Claude was also the easiest family to extract from: a single fixed prompt sufficed, where GPT required up to 50 candidate extractions per block.

The mechanism is not a Claude-specific weakness so much as a design shared across providers — the envelope authenticates the model but not the account or conversation. It does, however, mean that anti-distillation training on Claude Opus 4.8 is undercut by Claude Haiku 4.5 accepting the same blocks and transcribing them. See [[Reasoning Trace Privacy]].

## Publishing a negative result on its own tools

[[Anthropic - Would This Change Your Answer (CHIVE)]] is an Anthropic Fellows paper (Adam Karvonen,
Euan Ong, Subhash Kantamneni, Samuel Marks) reporting that **activation-reading interpretability tools
give no uplift over a transcript-only baseline** at predicting counterfactual model behaviour — a
finding that undercuts a research direction the lab itself is prominently associated with.

The methodological contribution matters more than the headline: the **transcript-only baseline** is a
reference condition most published interpretability work has not run. See
[[Interpretability Evaluation]].

Anthropic appears in this vault on the other side of this argument too. Its finding that human raters
and reward models usually prefer confident agreeable answers over correct ones anchors the sycophancy
material in [[Reward Design for RL]], and its removal of **more than 80% of Claude Code's system
prompt with no measurable eval loss** is the strongest single data point in
[[Context Engineering]]'s case against instruction bloat.

## The evaluation method is published; the evaluation data is not

[[Lance Martin - Automating Eval Design and Hillclimbing with Claude]] extends Anthropic's presence in
this vault from harnesses and skills into evaluation methodology. The artifacts are skill commands: one
builds an evaluation for an application, the other improves the application against it one attributable
change at a time. The durable part is the set of controls — a held-out split, one patch per round, a
revert when only the training split improves, a noise floor measured by running the grader twice on the
same output, and a ceiling at roughly **95%** above which quality hillclimbing is abandoned in favour of
cost or latency. Those controls are legible enough to reuse without Anthropic's tooling; see
[[Benchmark Optimization]] and [[Harness Optimization]].

The results are a different matter, and they need reading with the conditions attached. On an internal
benchmark of **44 tickets** (**30** for search, **14** held out), the baseline Opus 4.8 at high effort
scored **74.4% decision accuracy at 4.6 cents per ticket**; Opus 5.5 at low effort **87.8% at 1.9
cents**; Sonnet 5 at low effort **88.9% at 1 cent**; prompt work took Sonnet 5 to **98.9%** at about the
same cost, and the held-out split moved from **78.6%** to **90.5%** at roughly **one fifth of the cost**.
Every figure is Anthropic-reported, on an Anthropic workflow, evaluating Anthropic models, with no
independent reproduction and no released evaluation data. The cost claim in particular is not a clean
measurement of the method, because the before-and-after bundles a model change, an effort change, a
prompt change, **and a pricing change** — Opus 5.5 is stated to price input and output **20% less** than
Opus 4.8 and cache reads **60% less**. Part of the reported saving is the vendor's own price list.

This complicates rather than contradicts the pattern recorded above, where Anthropic has published
findings that cut against its own positions — CHIVE's negative result on interpretability tooling, and
the removal of more than 80% of Claude Code's system prompt with no measurable eval loss. Martin's piece
does concede against interest: evaluation leakage and overfitting persist, **including harness additions
that solve benchmark quirks rather than production problems**, and a misconfigured judge still requires a
human to read scored transcripts. But a concession stated inside results nobody outside can check is a
weaker instrument than a published negative result on a released benchmark. Both belong on this page, and
they should not be collapsed into a single claim about the lab's transparency.

## Related pages

- [[Anthropic - The AI-Native SDLC Playbook]]
- [[AI-Native Software Development Lifecycle]]
- [[Coding Agent Harness]]
- [[Agent Skill]]
- [[Agent Security and Governance]]
- [[AI Accelerator Architecture]]
- [[AI Knowledge Base Overview]]
- [[ByteByteGo - How to Steal an AI Model's Private Thoughts]]
- [[Reasoning Trace Privacy]]
- [[Interpretability Evaluation]]
- [[Reward Design for RL]]
- [[Context Engineering]]
- [[Anthropic - Would This Change Your Answer (CHIVE)]]
- [[Lance Martin - Automating Eval Design and Hillclimbing with Claude]]
- [[Benchmark Optimization]]
- [[Harness Optimization]]
- [[Multi-Turn Evaluation]]
- [[Agentic Testing]]
- [[LLM-as-a-Judge]]
