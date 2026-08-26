---
type: source-summary
created: 2026-07-03
updated: 2026-08-26
source_id: src-2026-07-02-arora-llm-reasoning-advances
source_title: "Current Advances in LLM Reasoning"
source_author: Akhil Arora, Vishrav Chaudhary, Julia Kreutzer, Nearchos Potamitis, Lars Klein, Nouha Dziri, Niket Tandon
source_url: https://docs.google.com/presentation/d/1GoSHhf6BwHwXA6vF_zhSxgsl8ty-8Zav9dGbP6qZsMg/edit?usp=sharing
tags:
  - source/summary
  - reasoning
  - test-time-scaling
  - reinforcement-learning
  - evaluation
  - tutorial
source_ids:
  - src-2026-07-02-arora-llm-reasoning-advances
status: active
---

# Akhil Arora et al - Current Advances in LLM Reasoning

## Summary

This is a full-length tutorial deck (llmreasoning.github.io, presented 2 July 2026) that surveys the entire LLM-reasoning field across three parts: **how well can models reason**, **how do we make them reason better**, and **what are the next frontiers**. It is unusually citation-dense (hundreds of 2024–2026 papers) and is the vault's most comprehensive single reasoning source. Its organizing thesis is the **frozen-θ view**: a trained model already contains latent CoT paths, self-verification, backtracking, and subgoal decomposition; performance gains come from better **search/exploration** (internal) plus **verification/retrieval/tools** (external), which post-training *unlocks* — not from adding new knowledge.

Part 1 defines reasoning (deduction/abduction/induction), shows LLMs are primarily *inductive* pattern-completers, and then systematically documents how **fragile and unfaithful** current reasoning is under perturbation, and how it fails in high-stakes (medical) settings. Part 2 covers the two levers for improvement: **inference-time / test-time scaling** (verifier-free search vs verifier-based selection) and **post-training / RL** (SFT, DPO, RLVR, PPO→GRPO, distillation). Part 3 lays out open frontiers as pillars — retrieval-vs-memory, verification, test-time scaling, multi-agent systems, continual learning, and systems — each with 2025–2026 evidence that they are unsolved.

## Key claims

### What reasoning is and how well models do it
- **Three reasoning types:** deduction (apply a rule → certainty), abduction (guess the best cause → plausible), induction (learn the rule → probability). LLMs are **primarily inductive**: they "reason" at inference by pattern completion; "thinking models" bake these inference-time patterns into weights. CoT emulates *deductive* chains; *abductive* reasoning needs divergent hypothesis generation + convergent selection, which a single linear pass can't do — motivating Tree-of-Thoughts, MCTS, and multi-agent methods.
- **Reasoning traces are tokens, not thoughts.** Traces do not have to be faithful; biased context flips answers while the CoT rationalizes post-hoc ("reasoning models don't always say what they think"). Longer traces are not always better — a model can get lost in a wrong path, or find the right answer then "correct" itself into a wrong one.
- **Reasoning is not robust.** Four fragility axes, each backed by multiple studies: input perturbations (rename/renumber → 10–65% drop, GSM-Symbolic); cultural/context (adding an irrelevant cultural rule = −24.5 pp on NormAd); prompt sensitivity (fidelity-preserving prompt polish raises plain IO from 3.0 → 31.3, +28 pp); and faithfulness. Single-run evaluation hides this instability — repeated runs and error bars are required (ReasonBench, arXiv:2512.07795).
- **English dominates reasoning.** Models mostly train on English traces, so traces stay English even for non-English prompts; answer accuracy ≠ reasoning-language accuracy, and multilinguality often trades off against accuracy.
- **High-stakes (medical) reasoning largely fails the classic Ledley (1959) diagnostic loop.** Models manage clinical facts (✅ MedQA passed since GPT-3.5) but are weak at generating alternative hypotheses (❌), estimating their probabilities (❌), and selecting actions (💀 — a ChatGPT-Health triage test undertriaged 52% of gold-standard emergencies, "would have killed the patient"). This motivates interactive **simulators** (MediQ, PatientSim, AgentClinic) over static QA.

### How to make models reason better
- **Inference-time scaling splits into verifier-free vs verifier-based.** Verifier-free explores the internal space (self-consistency/majority voting, Tree-of-Thoughts, MCTS, beam search, Fleet of Agents); verifier-based anchors to ground truth (process reward models, GenRM, code execution, retrieval). "Verifiers separate generation from evaluation."
- **Search & sieve:** without a pruning/verification function, purely sequential generation suffers exponentially compounding errors from autoregressive drift — the mathematical reason inference pipelines split into verifier-free (VF) and verifier-based (VB) regimes.
- **Inference compute is a first-class scaling axis** (longer traces, more samples, more search budget, budget forcing) — but "just thinking more is not enough": more tokens can cause *overthinking*, so scaling needs a **controller** that decides whether to answer, think longer, branch, retrieve, verify, or call tools. The frontier "is no longer a better prompt; it's a controller."
- **Post-training has three objectives** — follow instructions, be helpful, think logically — and is the comparatively cheap stage that turns a next-word predictor into a useful model. **SFT enables skills** by composing a data mix (Tulu 3 buckets: instruction/reasoning/math/coding/safety/multilingual/chat); **quality > quantity** (s1: 1,000 curated traces beat o1-preview).
- **DPO** skips the reward model: the policy *is* the reward model (log-ratio to a reference is an implicit reward), so you optimize preference pairs directly. **RLVR (RL with Verifiable Rewards)** drops the neural reward model entirely — math checked by calculator, code by test suite, format by tags — and works as well as or better than learned rewards, creating a contrastive correct-vs-incorrect signal that transfers to unseen problems.
- **PPO → GRPO** is what made large-scale reasoning RL practical: PPO needs four models (policy, reward model, critic baseline, KL reference); GRPO drops the critic and uses the **group mean/std** as the baseline, roughly halving memory, with a KL penalty keeping the policy near the base model.
- **SFT reproduces, RL discovers.** SFT faithfully reproduces the training distribution and fails out-of-distribution; RL discovers novel strategies (Logic-RL trained on 5K puzzles generalizes to math). Open debate: does RL *create* reasoning or *amplify* latent capability (Dr. GRPO shows base Qwen already reasons)?
- **Distillation is now standard and merging with RL.** DeepSeek-R1 distillation transfers ~85–90% of capability into 1.5–70B students with pure SFT; s1 and Qwen3 strong-to-weak confirm efficiency. The 2026 frontier unifies KD + RL in one stage (KDRL, RL-aware KD that up-weights critical reasoning tokens), ~40% faster than sequential SFT→RL. Production pipelines are multi-stage (QwQ-32B 2-stage, Qwen3 5-stage, GLM-5 4-stage "slime").

### Frontiers (each an open pillar with 2025–2026 evidence it's unsolved)
- **Retrieval vs memory** (Search-R1, MCTS-RAG, Sleep-time Compute, Mem0; tool-induced hallucination; high-stakes retrieval calibration MedReason/CARE).
- **Verification** (calibrated uncertainty BIRD; process reward without human labels ThinkPRM/GenRM-CoT; verifier robustness Absolute Zero/VeriFree; formal bridges AlphaGeometry2/RAP).
- **Test-time scaling** (sufficiency detection CALM; efficient early exit DeepConf/DEER; test-time RL, TTRL).
- **Multi-agent systems** — the "Illusion of MAS advantage": does multi-agent actually help vs hurt under *token-matched* controls? Communication overhead and a coordination-failure taxonomy are undertheorized (MAS-Orchestra, Skill-MAS).
- **Continual learning** (distribution drift, catastrophic forgetting, model collapse, "peak data," reward hacking).
- **Systems** (parallel decoding, speculative decoding, batched-inference determinism, CacheSaver from the authors' group).
- **Abductive failure modes:** Evidence Fabrication, Context Drift, Early Stopping (Pan 2026).

## Why it matters

This deck is the natural **hub** for the vault's scattered reasoning material and seeds the new [[LLM Reasoning]] concept, which ties together [[Reasoning Compression]], [[Latent-Space Reasoning]], [[Recursive Architectures]], and [[Monte Carlo Tree Search]] under one map. It also seeds [[Test-Time Scaling]] (verifier-free vs verifier-based inference-time compute), the missing counterpart to [[Reasoning Compression]] (spend *more* compute to reason better vs. spend *less* without losing accuracy) and to [[LLM Inference]] (serving mechanics). Its post-training material sharpens [[Reinforcement Learning]], [[Group Relative Policy Optimization]] (the crisp PPO-vs-GRPO memory argument), [[Direct Preference Optimization]] (policy-as-reward-model), [[Reward Design for RL]] (RLVR), [[LLM-as-a-Judge]] (PRM/GenRM/self-rewarding verifiers), [[LLM Training Pipeline]], and [[Multi-Teacher On-Policy Distillation]] (KD+RL merging). The robustness/faithfulness findings give the vault its clearest evidence base for "reasoning is brittle."

## Tensions / open questions

- The source is a **slide deck captured via plain-text export**, so speaker-note prose is interleaved with fragmentary slide text and some layout/OCR noise; exact figures live in the cited papers, not the capture.
- The central **create-vs-amplify** debate (does RL produce new reasoning or surface latent capability?) is explicitly left open and shapes how one reads every RL result here.
- **Faithfulness** undercuts the whole enterprise: if traces don't reflect computation, trace-based supervision and trace-based evaluation are both suspect — mechanistic interpretability is proposed as a better lens.
- Many "frontier" claims are pointers to very recent (2026) preprints presented without independent replication; treat them as signals to track.

## Affected pages

- [[LLM Reasoning]]
- [[Test-Time Scaling]]
- [[Reasoning Compression]]
- [[Reinforcement Learning]]
- [[Group Relative Policy Optimization]]
- [[Direct Preference Optimization]]
- [[Reward Design for RL]]
- [[LLM-as-a-Judge]]
- [[Monte Carlo Tree Search]]
- [[LLM Training Pipeline]]
- [[Multi-Teacher On-Policy Distillation]]
- [[LLM Inference]]
- [[Latent-Space Reasoning]]
- [[Recursive Architectures]]
- [[Retrieval-Augmented Generation]]
- [[Agentic Reinforcement Learning]]
- [[Nested Learning]]
- [[AI Knowledge Base Overview]]

## Citations
- Source URL: [Google Slides](https://docs.google.com/presentation/d/1GoSHhf6BwHwXA6vF_zhSxgsl8ty-8Zav9dGbP6qZsMg/edit?usp=sharing)
- Tutorial site: [https://llmreasoning.github.io/](https://llmreasoning.github.io/)
- Key framing sources cited in the deck: ReasonBench (arXiv:2512.07795), GSM-Symbolic (arXiv:2410.05229), DeepSeek-R1 Thoughtology (Marjanović 2025), "Reasoning Models Don't Always Say What They Think" (Chen 2025, arXiv:2505.05410).

## Raw capture

- [[2026-07-02 Akhil Arora et al - Current Advances in LLM Reasoning]]

## Related pages

- [[LLM Reasoning]]
- [[Test-Time Scaling]]
- [[Reasoning Compression]]
- [[Reinforcement Learning]]
- [[Group Relative Policy Optimization]]
- [[Direct Preference Optimization]]
- [[Reward Design for RL]]
- [[LLM-as-a-Judge]]
- [[Monte Carlo Tree Search]]
- [[LLM Training Pipeline]]
- [[Multi-Teacher On-Policy Distillation]]
- [[LLM Inference]]
- [[AI Knowledge Base Overview]]
