---
type: index
created: 2026-05-08
updated: 2026-06-23
tags:
  - index
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
  - src-2026-05-08-murphy-reinforcement-learning-overview
  - src-2026-05-04-bytebytego-llm-tool-use-mcp
  - src-2026-04-22-perplexity-search-augmented-lm
  - src-2026-05-18-alphasignal-return-of-recursion
  - src-2026-05-18-pocketflow-tutorial-docs
  - src-2026-05-18-hanfang-pytorch-practice
  - src-2026-05-18-rag-architecture-comparison
  - src-2026-05-21-leetcode-templates
  - src-2026-05-21-bytebytego-batch
  - src-2026-05-28-bytebytego-airtable-search
  - src-2026-05-28-doordash-llm-judge
  - src-2026-06-02-ycombinator-yc-paper-club-inference-diffusion-world-models
  - src-2026-06-02-dwarkesh-eric-jang-alphago
  - src-2026-06-02-dwarkesh-eric-jang-flashcards
  - src-2026-06-02-dwarkesh-reiner-pope-chip-design
  - src-2026-06-02-dwarkesh-reiner-pope-flashcards
  - src-2026-06-02-alphasignal-look-past-rag-pipeline
  - src-2026-06-02-bytebytego-doordash-testing-system
  - src-2026-05-29-braintrust-multi-turn-scoring
  - src-2026-06-03-fareed-khan-train-llm-from-scratch
  - src-2026-06-03-liquid-ai-lfm2-5-8b-a1b
  - src-2026-06-03-nvidia-locateanything
  - src-2026-06-04-efficient-reasoning-edge
  - src-2026-06-04-progressive-thought-encoding
  - src-2026-06-04-pace-efficient-reasoning
  - src-2026-06-04-extreme-ratio-cot-compression
  - src-2026-06-04-reasoncache
  - src-2026-06-04-difficulty-aware-entropy-regularization
  - src-2026-06-04-conpress
  - src-2026-06-04-dss-grpo-cot-compression
  - src-2026-06-05-pguso-agents-from-scratch
  - src-2026-06-05-fei-fei-li-taxonomy-world-models
  - src-2026-06-05-dharma-ai-dpo-beyond-chatbots
  - src-2026-06-05-systemdesign42-system-design-academy
  - src-2026-06-10-0xkato-how-llms-actually-work
  - src-2026-06-10-bytebytego-token-spend-routing
  - src-2026-06-10-itsreallyvivek-frontier-ai-labs
  - src-2026-06-17-nathan-lambert-frontier-post-training-recipe-review
  - src-2026-06-17-prateek-singh-kv-cache-turboquant
  - src-2026-06-18-alyona-vert-recursive-self-improvement
  - src-2026-06-22-cameron-wolfe-agentic-rl-frameworks
  - src-2026-06-22-djfarrelly-agent-loop-architecture
  - src-2026-06-22-alphasignal-agent-skill-optimization
  - src-2026-06-23-mayank-pratap-singh-diffusion-visual-breakdown
status: active
---

# Knowledge Base Index

Start here. This file is the content-oriented routing layer for the wiki.

## Overviews

- [[AI Knowledge Base Overview]] - Workspace-specific orientation page for this persistent AI knowledge base.

## Concepts

- [[Persistent Wiki]] - The wiki as a durable knowledge layer that compounds over time.
- [[Schema-Driven Knowledge Base]] - Why a schema file turns a generic model into a disciplined maintainer.
- [[Ingest Query Lint Loop]] - The three recurring operations that keep the wiki alive.
- [[Index and Log]] - Why the catalog and ledger are first-class control surfaces.
- [[Reinforcement Learning]] - Hub page for sequential decision making and RL method families.
- [[Agentic Reinforcement Learning]] - RL training for multi-turn tool-using LLM agents in stateful environments.
- [[Transformer Architecture]] - Decoder-only Transformer synthesis spanning attention, RoPE, and KV-cache inference.
- [[Diffusion Models]] - Generative models that learn to reverse noising processes for images and other data.
- [[LLM Training Pipeline]] - Pretraining, SFT, RLHF, DPO, and LoRA as one post-training map.
- [[Neural Network Fundamentals]] - Gradient descent, backpropagation, PyTorch, and Adam as the substrate of modern models.
- [[Algorithm Templates for Interviews]] - Template-based approach to DSA and ML engineering interviews.
- [[Model Quantization and Efficiency]] - Quantization, KV cache, LoRA, and sparse activation as core efficiency levers.
- [[KV Cache]] - Runtime attention-state cache that speeds autoregressive decoding but dominates long-context memory.
- [[On-Device Reasoning]] - Local reasoning under phone/laptop-class memory, latency, and power limits.
- [[Reasoning Compression]] - Shortening or replacing explicit reasoning traces without losing answer quality.
- [[Tool Use and Function Calling]] - How LLMs request actions from external systems via structured function calls.
- [[Model Context Protocol]] - Open standard (Anthropic) that solves the N×M tool-integration problem.
- [[Agentic Loop]] - The iterative plan-act-observe cycle that enables multi-step LLM tool use.
- [[Agent Planning]] - Planning as data structures, atomic actions, and AoT dependency graphs for safe multi-step execution.
- [[Agent Skill]] - Reusable agent capability artifacts spanning markdown procedures, durable workflows, and optimization loops.
- [[Agent Memory]] - Short-term context vs long-term persistent storage; explicit fact management for agents.
- [[AI Agents in Production]] - Real-world deployment of AI agents for team productivity and design workflows.
- [[Search-Augmented Language Models]] - LLMs that use web search as part of generation, with RL-trained tool-use policies.
- [[ML Systems at Scale]] - Production ML serving patterns from Netflix, Snapchat, Amazon, Instacart, and Airtable.
- [[Retrieval-Augmented Generation]] - Hub page for Classic, Graph, and Agentic RAG architectures.
- [[Direct Corpus Interaction]] - Raw-file retrieval via terminal tools as a precision layer for agentic search.
- [[LLM-as-a-Judge]] - Using calibrated LLMs to evaluate search relevance and generation quality at scale.
- [[Multi-Turn Evaluation]] - Turn-level plus conversation-level scoring for simulated and live multi-turn systems.
- [[Mixture of Experts]] - Sparse architectures that activate only part of the network per token.
- [[Reward Design for RL]] - Constructing composite reward signals for multi-objective LLM training.
- [[Group Relative Policy Optimization]] - Relative-policy optimisation method used in the search-agent RL pipeline.
- [[Latent-Space Reasoning]]
- [[Recursive Architectures]]
- [[World Models]] - Learned predictive models for planning, control, and embodied intelligence; now includes Fei-Fei Li's Renderer/Simulator/Planner taxonomy and POMDP framing.
- [[Context Engineering]] - Managing the full LLM context window at inference time: system prompt, history, retrieval, tool results, token budget. Distinct from prompt engineering.
- [[Model Routing]] - Choosing among model/provider tiers per request or step to satisfy quality thresholds under cost and latency constraints.
- [[Multi-Teacher On-Policy Distillation]] - 2026 frontier post-training pattern for consolidating domain-specialist teachers into one student.
- [[Direct Preference Optimization]] - Completion-level preference learning for chat alignment and structured output reliability; includes self-rejection pair methodology.
- [[Vision-Language Grounding]] - Text-conditioned spatial localization for objects, GUIs, documents, and scenes.
- [[Monte Carlo Tree Search]] - Search-time planning procedure that guides AlphaGo-style RL and clarifies dense supervision.
- [[Automated AI Research]] - Agentic research loops that automate experiments more readily than question selection.
- [[Recursive Self-Improvement]] - AI systems improving parts of the process that creates future AI systems.
- [[AI Accelerator Architecture]] - Hardware-level and cluster-level design tradeoffs behind AI compute.

## Entities

- [[Andrej Karpathy]] - Author of the pattern that seeded this implementation.
- [[ByteByteGo]] - Engineering newsletter; source for the tool-use and MCP article.
- [[Braintrust]] - Evaluation platform whose material in this vault focuses on multi-turn traces and online scoring.
- [[DoorDash]] - Delivery platform; source for LLM-as-a-Judge search evaluation and country-launch architecture.
- [[Fareed Khan]] - Repository author whose code-first LLM project ties Pile preprocessing, Transformer implementation, and training into one workflow.
- [[Han Fang]] - Author of the PyTorch Practice interview tutorial.
- [[Liquid AI]] - Model company focused here on sparse on-device assistants and local tool calling.
- [[NVIDIA]] - Research organization whose current source opens the multimodal grounding branch.
- [[Obsidian]] - The note environment that acts as IDE, browser, and graph surface for the wiki.
- [[Qualcomm AI Research]] - Mobile/edge deployment group focused here on efficient on-device reasoning.
- [[Perplexity]] - AI search company; source for the search-augmented LM training pipeline.
- [[Alpha Signal]]
- [[Inngest]] - Durable workflow/orchestration platform used as the concrete example in the agent loop architecture source.
- [[The Pocket]] - Organization behind PocketFlow and its tutorial-documentation curriculum.
- [[Y Combinator]] - Startup accelerator and publisher of YC Paper Club frontier-research sessions.
- [[Eric Jang]] - Researcher whose AlphaGo reconstruction ties together MCTS, RL, and autoresearch.
- [[Reiner Pope]] - Hardware researcher whose material ties chip design to LLM throughput and serving math.
- [[Nathan Lambert]] - Interconnects author focused here on RLHF, post-training, and open/frontier recipe comparisons.
- [[Finbarr Timbers]] - Post-training researcher whose interview contributions sharpen the MOPD and frontier recipe discussion.

- [[Fei-Fei Li]] - Co-founder of World Labs; author of the functional world-model taxonomy using the POMDP loop.
- [[World Labs]] - AI company focused on spatial intelligence, world models, and unified Renderer/Simulator/Planner foundation models.

## Sources

- [[Andrej Karpathy - LLM Wiki]] - Summary of the original `LLM Wiki` gist and its implications for this vault.
- [[Kevin Murphy - Reinforcement Learning - An Overview]] - Survey source that seeds the vault's RL area.
- [[ByteByteGo - Connecting LLMs to the Real World]] - Tool use, function calling, and MCP evolution from isolated LLMs to real-world agents.
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]] - Eight articles on production ML systems, AI agents, and architecture patterns.
- [[ByteByteGo - How Airtable Built the Search Layer]] - Vector search architecture with HNSW, hot/cold tiering, and hierarchical partitioning.
- [[DoorDash - LLM-as-a-Judge for Search Evaluation]] - Facet-based LLM evaluation replacing noisy human annotation for NL search.
- [[Perplexity - Advancing Search-Augmented Language Models]] - Two-stage SFT→RL pipeline for training web search agents with gated rewards.
- [[Alpha Signal - The Return of Recursion]]
- [[Alpha Signal - As AI agents evolve, we need to look past the RAG pipeline]] - Argument that coding agents need higher-resolution corpus interfaces than vector-only RAG, motivating DCI and hybrid retrieval.
- [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]] - Support-chatbot simulation and evaluation flywheel with transcript-derived scenarios and LLM judges.
- [[Braintrust - How to evaluate multi-turn conversations]] - Operational recipe for turn-level and trace-level evaluation over grouped conversation traces.
- [[The Pocket - PocketFlow Tutorial Docs]] - Composite tutorial source spanning LLM internals, training pipelines, RL methods, and math foundations.
- [[Classic RAG vs Graph RAG vs Agentic RAG]] - Comparison of three RAG architecture tiers and their use cases.
- [[Han Fang - PyTorch Practice]] - Code-first PyTorch tutorial for ML engineer interview preparation.
- [[Universal LeetCode Templates]] - 20 battle-tested algorithm templates with pattern recognition and complexity analysis.
- [[Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club]] - Frontier-research discussion session spanning inference, diffusion control, world models, generalization, and pretraining scaling.
- [[Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch]] - Long-form interview connecting AlphaGo, MCTS, RL-for-LLMs, and autoresearch loops.
- [[Dwarkesh Patel - Eric Jang Flashcards]] - Retrieval-oriented companion distilling MCTS, self-play, and AlphaZero training into compact Q/A form.
- [[Dwarkesh Patel - Reiner Pope - Chip design from the bottom up]] - Blackboard lecture on AI chip design from logic gates to GPUs, TPUs, FPGAs, and memory hierarchy.
- [[Dwarkesh Patel - Reiner Pope Flashcards]] - Structured companion on LLM training/serving math, batching, memory bandwidth, MoE racks, and pipeline parallelism.
- [[Fareed Khan - Train LLM From Scratch]] - Code-first PyTorch repo for Pile preprocessing, decoder-only Transformer training, and text generation.
- [[Liquid AI - LFM2.5-8B-A1B]] - On-device MoE model emphasizing sparse inference, long context, multilingual tokenization, and local tool calling.
- [[NVIDIA - LocateAnything]] - Parallel Box Decoding framework for fast, high-quality visual grounding and detection.
- [[Efficient Reasoning on the Edge]] - End-to-end on-device reasoning pipeline with LoRA adapters, budget forcing, switcher routing, verifier-guided parallel decoding, and 4-bit deployment.
- [[Training Large Reasoning Models Efficiently via Progressive Thought Encoding]] - Progressive vector encoding for bounded-cache reasoning training and inference.
- [[PACE - Prefix-Protected and Difficulty-Aware Compression for Efficient Reasoning]] - Prefix-protected and difficulty-aware CoT compression.
- [[Towards Efficient Large Language Reasoning Models via Extreme-Ratio Chain-of-Thought Compression]] - Extreme-ratio CoT compression with mixed-ratio SFT and hierarchical optimisation.
- [[ReasonCACHE - Teaching LLMs To Reason Without Weight Updates]] - Prefix-tuned fixed KV caches that teach reasoning without conventional weight updates.
- [[Compress the Easy, Explore the Hard - Difficulty-Aware Entropy Regularization for Efficient LLM Reasoning]] - Difficulty-aware entropy regularisation for shorter but still exploratory reasoning.
- [[ConPress - Learning Efficient Reasoning from Multi-Question Contextual Pressure]] - Self-supervised reasoning compression learned from multi-question prompts.
- [[Shorter Thoughts, Same Answers - Difficulty-Scaled Segment-Wise RL for CoT Compression]] - Segment-wise GRPO that compresses thinking without damaging the final answer.
- [[pguso - Agents From Scratch]] - Local-first Python repo building one agent across 12 lessons: loop, tools, memory, planning, atomic actions, AoT, evals, and telemetry.
- [[Fei-Fei Li - A Functional Taxonomy of World Models]] - Renderer/Simulator/Planner taxonomy using the POMDP loop; argues simulation is the linchpin and introduces World Labs' Marble product.
- [[Dharma-AI - Direct Preference Optimization Beyond Chatbots]] - DPO applied to OCR text degeneration suppression using self-generated rejection pairs; 59.4% average degeneration reduction across five model families.
- [[systemdesign42 - System Design Academy]] - Curated A-Z index of 150+ system design articles across case studies, fundamentals, AI engineering, and interview prep.
- [[0xkato - How LLMs Actually Work]] - Clear end-to-end transformer walkthrough covering tokenization, RoPE, attention, GQA, residual streams, RMSNorm, MoE, and speculative decoding.
- [[ByteByteGo - Token Spend Out of Control - The Case for Smarter Routing]] - Production view of agent economics and model routing, with Kilo as a real routing-layer case study.
- [[itsreallyvivek - some notes on getting into frontier ai labs]] - Essay-thread on research taste, abstraction-building, and judgment under uncertainty in frontier AI work.
- [[Nathan Lambert - Frontier post-training recipe review with Finbarr Timbers]] - Historical and current map of post-training recipes from InstructGPT to MOPD-style 2026 frontier pipelines.
- [[Prateek Singh - KV Cache and TurboQuant]] - Interactive KV-cache memory explainer and TurboQuant breakdown for long-context inference compression.
- [[Alyona Vert - AI 101 - What is Recursive Self-Improvement]] - Turing Post AI 101 explainer distinguishing workflow-level self-improving agents from stronger model-building-level RSI.
- [[Cameron R. Wolfe - Agentic RL Frameworks and Best Practices]] - Survey of multi-turn, tool-using agent RL frameworks, rollout infrastructure, reward design, and stability failures.
- [[Mayank Pratap Singh - Diffusion Model Visual Breakdown]] - Visual explainer of DDPM noising/denoising, latent diffusion, conditioning, guidance, and diffusion transformers.
- [[djfarrelly - The Agent Loop Architecture]] - Durable agent loop architecture organized around loops, skills, orchestration, checkpoints, retries, and run history.
- [[Alpha Signal - How your agents can write and optimize their own skills]] - SkillOpt, GEPA, EvoSkill, and loop-engineered skill-file optimization for agents.

## Queries

- [[2026-06-19 Efficient Edge Reasoning and TurboQuant]] - Synthesis of how edge reasoning systems and TurboQuant-style KV-cache compression could combine.
- [[2026-06-04 Efficient Reasoning on the Edge - Blog Post]] - Beginner-friendly self-contained blog post on efficient reasoning for edge devices.
- [[2026-05-08 Mathematical Foundations for Reinforcement Learning]] - Structured answer on the math stack needed to move from Murphy's survey to RL expertise.

## Lint reports

- [[2026-05-08 Wiki Lint Pass]] - Structural lint pass covering link integrity, schema conformance, and current wiki gaps.
- [[2026-05-13 Lint Pass]] - Comprehensive lint pass covering structural integrity, coverage, and immediate fixes.
- [[2026-05-13 Lint Pass 2]] - Follow-up lint pass after the Perplexity ingest, covering new-page integration and residual structural issues.
- [[2026-05-18 Lint Pass]] - Full-vault lint pass covering broken links, schema conformance, coverage gaps, and cross-link fixes.
- [[2026-05-18 Lint Pass 2]] - Post-ingest full wiki lint covering structural checks, raw-source coverage, and one overview staleness fix.
- [[2026-05-18 Lint Pass 3]] - Post-consolidation full wiki lint verifying structural integrity and Han Fang raw-source coverage.
- [[2026-05-21 Lint Pass]] - Seventh comprehensive lint pass covering full-wiki structural integrity after the Universal LeetCode Templates ingest.
- [[2026-05-21 Lint Pass 2]] - Eighth comprehensive lint pass covering full-wiki structural integrity after the ByteByteGo system-design batch ingest.
- [[2026-05-29 Lint Pass]] - Ninth comprehensive lint pass covering the full wiki after the Airtable search and DoorDash LLM-as-a-Judge ingests.
- [[2026-06-02 Lint Pass]] - Tenth comprehensive lint pass covering the post-Reiner wiki and fixing three thin entity pages.
- [[2026-06-02 Lint Pass 2]] - Eleventh comprehensive lint pass covering the expanded evaluation branch and finding no new structural defects.
- [[2026-06-03 Lint Pass]] - Twelfth comprehensive lint pass covering the sparse-model and multimodal-grounding expansions and finding no structural defects.
- [[2026-06-04 Lint Pass]] - Thirteenth comprehensive lint pass (95 pages) covering the reasoning-compression batch and finding no structural defects.
- [[2026-06-05 Lint Pass]] - Fourteenth comprehensive lint pass (105 pages) after World Models taxonomy + DPO ingests; no defects; fixed Liquid AI validator bug and blog-post orphan.
- [[2026-06-05 Lint Pass 2]] - Fifteenth comprehensive lint pass (108 pages) after System Design Academy ingest; no defects.
- [[2026-06-17 Lint Pass]] - Sixteenth comprehensive lint pass (119 pages) after MOPD + KV Cache ingests; no defects.
- [[2026-06-22 Lint Pass]] - Seventeenth comprehensive lint pass (127 pages) after agent-skill and RSI ingests; fixed one unreferenced raw source and found no remaining defects.

## Control files

- [[log|Knowledge Base Log]] - Chronological record of scaffolding, ingests, queries, and lint passes.
