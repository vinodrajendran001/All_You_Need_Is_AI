---
type: overview
created: 2026-05-08
updated: 2026-06-04
tags:
  - overview
  - ai
  - knowledge-base
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
  - src-2026-06-02-dwarkesh-eric-jang-alphago
  - src-2026-06-02-dwarkesh-eric-jang-flashcards
  - src-2026-06-02-ycombinator-yc-paper-club-inference-diffusion-world-models
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
status: active
---

# AI Knowledge Base Overview

## Scope

This wiki is the persistent knowledge layer for the `All_You_Need_Is_AI` vault. It is meant to accumulate sources, syntheses, and durable answers about AI instead of rediscovering them from scratch on every query.

## Current picture

The workspace now implements Karpathy's three-layer pattern:

- Raw sources live under `knowledge-base/raw/`.
- Curated wiki pages live under `knowledge-base/wiki/`.
- The operating schema lives in the root `CLAUDE.md` note.

The first source in the system is [[Andrej Karpathy - LLM Wiki]], which establishes the baseline operating model for future ingests. The second source, [[Kevin Murphy - Reinforcement Learning - An Overview]], seeds the first domain-specific branch of the wiki around [[Reinforcement Learning]]. The third source, [[ByteByteGo - Connecting LLMs to the Real World]], opens the **LLM tooling and agents** branch covering [[Tool Use and Function Calling]], [[Model Context Protocol]], and the [[Agentic Loop]]. The fourth source, [[Perplexity - Advancing Search-Augmented Language Models]], deepens the RL and agents area with a concrete production pipeline for [[Search-Augmented Language Models]] and introduces [[Reward Design for RL]] as a cross-cutting concept. The fifth source, [[Alpha Signal - The Return of Recursion]], adds a new branch around [[Latent-Space Reasoning]] and [[Recursive Architectures]], framing recursive computation as a complementary path to faster, lower-cost reasoning systems. The sixth source, [[The Pocket - PocketFlow Tutorial Docs]], adds a major tutorial library covering LLM internals, LLM training pipelines, reinforcement-learning methods, and mathematical foundations, and it seeds [[Transformer Architecture]], [[LLM Training Pipeline]], [[Neural Network Fundamentals]], and [[Model Quantization and Efficiency]]. The seventh source, [[Han Fang - PyTorch Practice]], reinforces that practical deep-learning branch with a compact interview-oriented PyTorch repo full of runnable from-scratch implementations for optimization, normalization, attention, training-loop mechanics, and model-efficiency techniques. The eighth source, [[Classic RAG vs Graph RAG vs Agentic RAG]], adds a retrieval-architecture taxonomy that unifies Classic, Graph, and Agentic RAG under the new hub page [[Retrieval-Augmented Generation]]. The ninth source, [[Universal LeetCode Templates]], expands the interview-preparation branch beyond ML implementation drills into reusable DSA problem-solving patterns, and it seeds [[Algorithm Templates for Interviews]] as a bridge between LeetCode-style template selection and [[Han Fang - PyTorch Practice]]. The tenth source, [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]], broadens the vault into production system design and ML-at-scale, seeding [[ML Systems at Scale]] and [[AI Agents in Production]] while connecting AI concepts to real architectures at Netflix, Snap, Amazon, Instacart, Grab, Figma, and DoorDash. The eleventh source, [[ByteByteGo - How Airtable Built the Search Layer]], deepens the retrieval branch with a concrete vector-search infrastructure case study around Milvus partitioning, HNSW latency/recall tradeoffs, and hot/cold memory tiering for Airtable's AI features. The twelfth source, [[DoorDash - LLM-as-a-Judge for Search Evaluation]], opens a new evaluation branch around [[LLM-as-a-Judge]], showing how facet-based rubrics, calibration, and continuous automated judging can replace noisy periodic annotation for natural-language search. The thirteenth source, [[Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club]], adds a frontier-research conversation artifact that strengthens the vault's inference-efficiency and pretraining branches while seeding [[World Models]] as a new planning-and-prediction concept. The fourteenth and fifteenth sources, [[Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch]] and [[Dwarkesh Patel - Eric Jang Flashcards]], deepen the RL branch with a worked AlphaGo example, seed [[Monte Carlo Tree Search]], and add [[Automated AI Research]] as a realistic agentic-research concept. The sixteenth and seventeenth sources, [[Dwarkesh Patel - Reiner Pope - Chip design from the bottom up]] and [[Dwarkesh Patel - Reiner Pope Flashcards]], open a new hardware-and-compute branch around [[AI Accelerator Architecture]] and strengthen the vault's understanding of throughput, memory bandwidth, cluster topology, and AI-chip design tradeoffs. The eighteenth source, [[Alpha Signal - As AI agents evolve, we need to look past the RAG pipeline]], deepens the retrieval-and-agents branch by seeding [[Direct Corpus Interaction]] and reframing coding-agent retrieval as an interface-design problem rather than only an embeddings problem. The nineteenth and twentieth sources, [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]] and [[Braintrust - How to evaluate multi-turn conversations]], deepen the evaluation branch by seeding [[Multi-Turn Evaluation]] and extending [[LLM-as-a-Judge]] from search relevance into full conversation scoring, simulation, and release-gated iteration. The twenty-first source, [[Fareed Khan - Train LLM From Scratch]], reinforces the code-first LLM branch by turning Pile-based pretraining, decoder-only Transformer construction, and single-GPU-oriented experimentation into one runnable repository. The twenty-second and twenty-third sources, [[Liquid AI - LFM2.5-8B-A1B]] and [[NVIDIA - LocateAnything]], extend the vault into sparse on-device assistants and vision-language grounding, seeding [[Mixture of Experts]] and [[Vision-Language Grounding]] as new concept branches. The twenty-fourth source, [[Efficient Reasoning on the Edge]], deepens the local/private deployment branch by seeding [[On-Device Reasoning]] and tying together LoRA reasoning adapters, budget forcing, switcher routing, verifier-guided inference scaling, and 4-bit quantized mobile deployment. The twenty-fifth through thirty-first sources form a new **reasoning compression** branch around [[Reasoning Compression]], covering progressive vector encoding, prefix-protected and difficulty-aware compression, extreme-ratio CoT compression, fixed KV-cache reasoning without weight updates, entropy-regularized RL compression, contextual self-compression, and segment-wise GRPO for think/answer separation.

## Key pages

- [[index|Knowledge Base Index]] - main entry point into the wiki
- [[Persistent Wiki]] - the central idea behind the whole system
- [[Schema-Driven Knowledge Base]] - how the schema keeps maintenance disciplined
- [[Ingest Query Lint Loop]] - the repeating maintenance cycle
- [[Index and Log]] - control files that help the LLM navigate the vault
- [[Reinforcement Learning]] - first domain hub page seeded from an ingested paper
- [[Transformer Architecture]] - decoder-only Transformer blueprint plus attention, RoPE, and KV-cache synthesis
- [[LLM Training Pipeline]] - pretraining, SFT, RLHF, DPO, and LoRA as one connected map
- [[Neural Network Fundamentals]] - gradient descent, backpropagation, PyTorch, and Adam as the substrate under higher-level model pages
- [[Algorithm Templates for Interviews]] - template-selection map connecting classic DSA interview patterns with ML engineering preparation
- [[Model Quantization and Efficiency]] - quantization, KV cache, LoRA, and sparse activation as deployment/adaptation efficiency levers
- [[On-Device Reasoning]] - local reasoning under mobile constraints, where memory, latency, and power shape the whole stack
- [[Reasoning Compression]] - shortening, replacing, or budgeting explicit reasoning traces to reduce cost without losing accuracy
- [[Mixture of Experts]] - sparse architectures that trade total capacity against lower active compute per token
- [[AI Accelerator Architecture]] - logic gates, systolic arrays, memory hierarchy, and cluster-scale compute/communication tradeoffs
- [[World Models]] - learned predictive models for planning, control, and embodied intelligence
- [[Vision-Language Grounding]] - text-conditioned spatial localization across objects, GUIs, documents, and scenes
- [[Monte Carlo Tree Search]] - search-time planning plus dense policy targets from AlphaGo-style supervision
- [[Automated AI Research]] - autoresearch loops, experiment execution, and the remaining bottlenecks in research agents
- [[Tool Use and Function Calling]] - how LLMs request real-world actions
- [[Model Context Protocol]] - open standard for universal tool integration
- [[Agentic Loop]] - the iterative cycle powering multi-step tool use
- [[Search-Augmented Language Models]] - LLMs with RL-trained search tool policies
- [[Retrieval-Augmented Generation]] - Classic, Graph, and Agentic RAG as a single retrieval-architecture map
- [[Direct Corpus Interaction]] - terminal-mediated corpus search as a precision layer for agentic retrieval
- [[Reward Design for RL]] - composite reward signals for multi-objective LLM training
- [[Group Relative Policy Optimization]] - relative-policy optimisation method used in the Perplexity RL stage
- [[Multi-Turn Evaluation]] - turn-level plus conversation-level scoring for simulated and live multi-turn systems
- [[Latent-Space Reasoning]] - reasoning through internal latent states instead of explicit token traces
- [[Recursive Architectures]] - modern recursive reasoning systems such as HRM, TRM, and RecursiveMAS
- [[ML Systems at Scale]] - production ML serving patterns spanning multimodal search, recommendation, hybrid retrieval, and vector-search infrastructure.
- [[LLM-as-a-Judge]] - calibrated LLM evaluators for search relevance, quality assurance, and continuous regression monitoring.
- [[AI Agents in Production]] - operational patterns for deploying agents with tool boundaries, MCP, guardrails, and human review.

## System design and ML-at-scale branch

- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]] adds a dedicated production-systems branch to the wiki.
- [[ByteByteGo - How Airtable Built the Search Layer]] adds a detailed vector-search infrastructure case study around Milvus partitioning, HNSW index selection, and hot/cold serving.
- [[ML Systems at Scale]] synthesizes shared serving patterns from Netflix, Snap, Amazon, Instacart, and now Airtable's semantic-search infrastructure.
- [[DoorDash - LLM-as-a-Judge for Search Evaluation]] adds a production evaluation case study for natural-language search.
- [[LLM-as-a-Judge]] captures the calibrated-LLM-evaluator pattern as a durable concept.
- [[AI Agents in Production]] captures how Grab and Figma operationalize agents for data engineering and design↔code workflows, and how newer sources extend that frame to local/private and perceptual agents.

## Gaps

- Existing notes elsewhere in the workspace have not yet been ingested into this structure.
- Reinforcement learning now has a denser hub page and stronger tutorial coverage, but its major subtopics are still not yet broken into dedicated notes.
- The `queries/` folder is active, `lint/` now has recurring reports, and `syntheses/` remains the least-developed content area.
- No search tooling has been added yet because the index is enough at the current scale.

## Related pages

- [[Andrej Karpathy - LLM Wiki]]
- [[Persistent Wiki]]
- [[Schema-Driven Knowledge Base]]
- [[Index and Log]]
- [[Obsidian]]
- [[Reinforcement Learning]]
- [[Tool Use and Function Calling]]
- [[Model Context Protocol]]
- [[Agentic Loop]]
- [[ByteByteGo - Connecting LLMs to the Real World]]
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- [[Perplexity - Advancing Search-Augmented Language Models]]
- [[Search-Augmented Language Models]]
- [[Retrieval-Augmented Generation]]
- [[Direct Corpus Interaction]]
- [[ML Systems at Scale]]
- [[LLM-as-a-Judge]]
- [[Multi-Turn Evaluation]]
- [[DoorDash - LLM-as-a-Judge for Search Evaluation]]
- [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]]
- [[ByteByteGo - How Airtable Built the Search Layer]]
- [[AI Agents in Production]]
- [[Reward Design for RL]]
- [[Transformer Architecture]]
- [[LLM Training Pipeline]]
- [[Neural Network Fundamentals]]
- [[Model Quantization and Efficiency]]
- [[On-Device Reasoning]]
- [[Reasoning Compression]]
- [[Mixture of Experts]]
- [[AI Accelerator Architecture]]
- [[Vision-Language Grounding]]
- [[Monte Carlo Tree Search]]
- [[Automated AI Research]]
- [[World Models]]
- [[The Pocket - PocketFlow Tutorial Docs]]
- [[The Pocket]]
- [[Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club]]
- [[Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch]]
- [[Dwarkesh Patel - Eric Jang Flashcards]]
- [[Dwarkesh Patel - Reiner Pope - Chip design from the bottom up]]
- [[Dwarkesh Patel - Reiner Pope Flashcards]]
- [[Alpha Signal - As AI agents evolve, we need to look past the RAG pipeline]]
- [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]]
- [[Braintrust - How to evaluate multi-turn conversations]]
- [[Liquid AI - LFM2.5-8B-A1B]]
- [[NVIDIA - LocateAnything]]
- [[Efficient Reasoning on the Edge]]
- [[Training Large Reasoning Models Efficiently via Progressive Thought Encoding]]
- [[PACE - Prefix-Protected and Difficulty-Aware Compression for Efficient Reasoning]]
- [[Towards Efficient Large Language Reasoning Models via Extreme-Ratio Chain-of-Thought Compression]]
- [[ReasonCACHE - Teaching LLMs To Reason Without Weight Updates]]
- [[Compress the Easy, Explore the Hard - Difficulty-Aware Entropy Regularization for Efficient LLM Reasoning]]
- [[ConPress - Learning Efficient Reasoning from Multi-Question Contextual Pressure]]
- [[Shorter Thoughts, Same Answers - Difficulty-Scaled Segment-Wise RL for CoT Compression]]
- [[Fareed Khan - Train LLM From Scratch]]
- [[Han Fang - PyTorch Practice]]
- [[Universal LeetCode Templates]]
- [[Algorithm Templates for Interviews]]
- [[Han Fang]]
- [[Fareed Khan]]
- [[Eric Jang]]
- [[Reiner Pope]]
- [[Liquid AI]]
- [[NVIDIA]]
- [[Qualcomm AI Research]]
- [[Latent-Space Reasoning]]
- [[Recursive Architectures]]
- [[Alpha Signal - The Return of Recursion]]
- [[Alpha Signal]]
- [[Perplexity]]
- [[Braintrust]]
- [[Y Combinator]]
