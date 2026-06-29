---
type: overview
created: 2026-05-08
updated: 2026-06-29
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
  - src-2026-06-24-bytebytego-llm-vs-slm
  - src-2026-06-26-nithin-llm-inference
  - src-2026-06-28-mayank-pratap-singh-timesformer
  - src-2026-06-29-maarten-grootendorst-visual-guide-quantization
  - src-2026-06-29-siddhant-rai-turboquant
  - src-2026-06-29-siddhant-rai-nested-learning
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

The first source in the system is [[Andrej Karpathy - LLM Wiki]], which establishes the baseline operating model for future ingests. The second source, [[Kevin Murphy - Reinforcement Learning - An Overview]], seeds the first domain-specific branch of the wiki around [[Reinforcement Learning]]. The third source, [[ByteByteGo - Connecting LLMs to the Real World]], opens the **LLM tooling and agents** branch covering [[Tool Use and Function Calling]], [[Model Context Protocol]], and the [[Agentic Loop]]. The fourth source, [[Perplexity - Advancing Search-Augmented Language Models]], deepens the RL and agents area with a concrete production pipeline for [[Search-Augmented Language Models]] and introduces [[Reward Design for RL]] as a cross-cutting concept. The fifth source, [[Alpha Signal - The Return of Recursion]], adds a new branch around [[Latent-Space Reasoning]] and [[Recursive Architectures]], framing recursive computation as a complementary path to faster, lower-cost reasoning systems. The sixth source, [[The Pocket - PocketFlow Tutorial Docs]], adds a major tutorial library covering LLM internals, LLM training pipelines, reinforcement-learning methods, and mathematical foundations, and it seeds [[Transformer Architecture]], [[LLM Training Pipeline]], [[Neural Network Fundamentals]], and [[Model Quantization and Efficiency]]. The seventh source, [[Han Fang - PyTorch Practice]], reinforces that practical deep-learning branch with a compact interview-oriented PyTorch repo full of runnable from-scratch implementations for optimization, normalization, attention, training-loop mechanics, and model-efficiency techniques. The eighth source, [[Classic RAG vs Graph RAG vs Agentic RAG]], adds a retrieval-architecture taxonomy that unifies Classic, Graph, and Agentic RAG under the new hub page [[Retrieval-Augmented Generation]]. The ninth source, [[Universal LeetCode Templates]], expands the interview-preparation branch beyond ML implementation drills into reusable DSA problem-solving patterns, and it seeds [[Algorithm Templates for Interviews]] as a bridge between LeetCode-style template selection and [[Han Fang - PyTorch Practice]]. The tenth source, [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]], broadens the vault into production system design and ML-at-scale, seeding [[ML Systems at Scale]] and [[AI Agents in Production]] while connecting AI concepts to real architectures at Netflix, Snap, Amazon, Instacart, Grab, Figma, and DoorDash. The eleventh source, [[ByteByteGo - How Airtable Built the Search Layer]], deepens the retrieval branch with a concrete vector-search infrastructure case study around Milvus partitioning, HNSW latency/recall tradeoffs, and hot/cold memory tiering for Airtable's AI features. The twelfth source, [[DoorDash - LLM-as-a-Judge for Search Evaluation]], opens a new evaluation branch around [[LLM-as-a-Judge]], showing how facet-based rubrics, calibration, and continuous automated judging can replace noisy periodic annotation for natural-language search. The thirteenth source, [[Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club]], adds a frontier-research conversation artifact that strengthens the vault's inference-efficiency and pretraining branches while seeding [[World Models]] as a new planning-and-prediction concept. The fourteenth and fifteenth sources, [[Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch]] and [[Dwarkesh Patel - Eric Jang Flashcards]], deepen the RL branch with a worked AlphaGo example, seed [[Monte Carlo Tree Search]], and add [[Automated AI Research]] as a realistic agentic-research concept. The sixteenth and seventeenth sources, [[Dwarkesh Patel - Reiner Pope - Chip design from the bottom up]] and [[Dwarkesh Patel - Reiner Pope Flashcards]], open a new hardware-and-compute branch around [[AI Accelerator Architecture]] and strengthen the vault's understanding of throughput, memory bandwidth, cluster topology, and AI-chip design tradeoffs. The eighteenth source, [[Alpha Signal - As AI agents evolve, we need to look past the RAG pipeline]], deepens the retrieval-and-agents branch by seeding [[Direct Corpus Interaction]] and reframing coding-agent retrieval as an interface-design problem rather than only an embeddings problem. The nineteenth and twentieth sources, [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]] and [[Braintrust - How to evaluate multi-turn conversations]], deepen the evaluation branch by seeding [[Multi-Turn Evaluation]] and extending [[LLM-as-a-Judge]] from search relevance into full conversation scoring, simulation, and release-gated iteration. The twenty-first source, [[Fareed Khan - Train LLM From Scratch]], reinforces the code-first LLM branch by turning Pile-based pretraining, decoder-only Transformer construction, and single-GPU-oriented experimentation into one runnable repository. The twenty-second and twenty-third sources, [[Liquid AI - LFM2.5-8B-A1B]] and [[NVIDIA - LocateAnything]], extend the vault into sparse on-device assistants and vision-language grounding, seeding [[Mixture of Experts]] and [[Vision-Language Grounding]] as new concept branches. The twenty-fourth source, [[Efficient Reasoning on the Edge]], deepens the local/private deployment branch by seeding [[On-Device Reasoning]] and tying together LoRA reasoning adapters, budget forcing, switcher routing, verifier-guided inference scaling, and 4-bit quantized mobile deployment. The thirty-second source, [[pguso - Agents From Scratch]], deepens the agents branch by providing the most explicit ground-up treatment of the [[Agentic Loop]] in this vault — building a single evolving agent across 12 lessons from raw LLM call to observable, testable, production-ready agent. It seeds [[Agent Planning]] (planning as data, atomic actions, AoT dependency graphs) and [[Agent Memory]] (short-term vs long-term, explicit storage), and adds evals and telemetry to [[AI Agents in Production]]. The thirty-third source, [[Fei-Fei Li - A Functional Taxonomy of World Models]], substantially deepens the [[World Models]] concept with the first clear functional taxonomy in the vault: Renderers (visual plausibility), Simulators (physics and geometry), and Planners (action) as three projections of the POMDP loop. The essay argues that simulation is the linchpin capability and that all three categories are converging toward a unified foundation model. It introduces [[Fei-Fei Li]] and [[World Labs]] as new entities. The thirty-fourth source, [[Dharma-AI - Direct Preference Optimization Beyond Chatbots]], generalises DPO beyond chat alignment into structured output reliability: using the model's own degenerate outputs (repetition loops in OCR) as self-generated rejection pairs, achieving 59.4% average text-degeneration reduction across five model families with no human annotation. This seeds a new [[Direct Preference Optimization]] concept page that mechanistically distinguishes SFT (closes task-domain distance) from DPO (moves distribution away from failure attractors) and introduces the three conditions for self-rejection DPO to work. The thirty-fifth source, [[systemdesign42 - System Design Academy]], adds the most comprehensive system design case study index in the vault — 60+ real company architectures (Netflix, Amazon, Stripe, Shopify, Uber, etc.) and 60+ technology concept articles (Kafka, Redis, consistent hashing, API patterns, distributed systems). Its AI Engineering section introduces [[Context Engineering]] as a new concept: the discipline of managing the full LLM context window (system prompt, history, retrieval, tool results, token budget) as distinct from crafting individual prompts. It also documents named agentic design patterns (ReAct, Plan-and-Execute, Reflection, routing) and multi-agent architectures (Orchestrator–Worker, Peer-to-peer, Hierarchical), deepening [[AI Agents in Production]] and [[ML Systems at Scale]]. The thirty-sixth source, [[0xkato - How LLMs Actually Work]], deepens the vault's LLM-internals branch with a highly legible end-to-end transformer walkthrough covering tokenization, embeddings, RoPE, attention, GQA, residual streams, RMSNorm, MoE, and speculative decoding. It materially strengthens [[Transformer Architecture]] by tying those mechanisms into one coherent picture and clarifying the difference between shared architecture, trained weights, and post-training. The thirty-seventh source, [[ByteByteGo - Token Spend Out of Control - The Case for Smarter Routing]], extends the agents branch into explicit inference economics. It seeds [[Model Routing]] as a new concept and shows that long-loop agents need routing infrastructure — unified gateways, known-signal mode routing, model tiers, and budget-aware spend governance — not just smaller prompts. The thirty-eighth source, [[itsreallyvivek - some notes on getting into frontier ai labs]], deepens [[Automated AI Research]] by reframing frontier research and trench engineering as the same underlying skill: building useful abstractions and making good judgments when no complete map exists.

The June 17 ingest adds two dense infrastructure/post-training sources. [[Nathan Lambert - Frontier post-training recipe review with Finbarr Timbers]] seeds [[Multi-Teacher On-Policy Distillation]], updating the post-training branch from SFT/DPO/RLVR-era recipes toward 2026 specialist-teacher consolidation, where many domain experts are trained separately and merged through on-policy student rollouts. [[Prateek Singh - KV Cache and TurboQuant]] seeds [[KV Cache]] as a standalone inference-efficiency page and clarifies why long-context AI is often memory-bound: KV cache solves repeated attention compute but becomes the dominant GPU-memory object, motivating PagedAttention, GQA/MQA/MLA, eviction/skipping methods, and TurboQuant-style 3-4 bit cache compression.

The June 22 ingest adds agent-infrastructure and research-automation sources. [[djfarrelly - The Agent Loop Architecture]] reframes production agents as **loops + skills + orchestration**, where durable execution, step checkpoints, retries, concurrency, and run history are what make long-running loops safe. [[Alpha Signal - How your agents can write and optimize their own skills]] adds the text-artifact side of the same branch, treating markdown skill files as optimizable external state through SkillOpt, GEPA, EvoSkill, verifiers, held-out evals, and bounded edits. Together they seed [[Agent Skill]] and add [[Inngest]] as the concrete orchestration platform example. [[Alyona Vert - AI 101 - What is Recursive Self-Improvement]] seeds [[Recursive Self-Improvement]], separating workflow-level self-improving agents from stronger model-building-level RSI.

The June 23 ingest adds [[Cameron R. Wolfe - Agentic RL Frameworks and Best Practices]], which seeds [[Agentic Reinforcement Learning]]. This extends the RL branch from single-turn LLM post-training into multi-turn interactive trajectories with tools, environment state, isolated rollouts, asynchronous training infrastructure, action masks, context rules, outcome/process rewards, and stability failures such as echo traps and template collapse.

The later June 23 ingest adds [[Mayank Pratap Singh - Diffusion Model Visual Breakdown]], seeding [[Diffusion Models]] as the vault's first dedicated diffusion page. It separates diffusion from the LLM training branch by explaining forward noising, denoising targets, timestep embeddings, U-Net denoisers, latent diffusion, conditioning, classifier-free guidance, diffusion transformers, and the speed-quality tradeoff in iterative sampling.

The June 26 ingest adds [[ByteByteGo - Large Language Models vs Small Language Models]], seeding [[Small Language Models]]. It deepens the efficiency and production-inference branches by showing how deployment target, inference economics, and training budget drive small-model architecture, training, quantization, KV-cache design, hardware mapping, and hybrid compositions with larger models.

The June 26-29 ingest adds five sources spanning quantization, inference, memory, and video. [[Nithin - What Actually Happens During LLM Inference]] seeds [[LLM Inference]] with the **prefill (compute-bound) vs decode (memory-bound)** split that underlies most efficiency work, plus serving-engine patterns (PagedAttention, continuous batching). [[Maarten Grootendorst - A Visual Guide to Quantization]] gives the vault its most thorough treatment of quantization mechanics (affine map, symmetric/asymmetric, PTQ vs QAT, GPTQ vs GGUF, BitNet), deepening [[Model Quantization and Efficiency]]. [[Siddhant Rai - TurboQuant - Online Vector Quantization]] supplies the math behind online KV-cache quantization (rate-distortion, rotation + Lloyd-Max codebook + 1-bit QJL residual), deepening [[KV Cache]]. [[Siddhant Rai - Nested Learning]] seeds [[Nested Learning]], a memory-as-structure / continuous inference-time-learning frame (Titans → Continuum Memory System → Hope) that sharpens [[Agent Memory]], [[Retrieval-Augmented Generation]], and [[Recursive Architectures]]. [[Mayank Pratap Singh - Transformers for Video - TimeSformer]] seeds [[Video Transformers]], extending [[Transformer Architecture]] into spatiotemporal divided space-time attention. These ingests also introduce [[Maarten Grootendorst]], [[Vizuara]], and [[Siddhant Rai]] as entities.

## Key pages

- [[index|Knowledge Base Index]] - main entry point into the wiki
- [[Persistent Wiki]] - the central idea behind the whole system
- [[Schema-Driven Knowledge Base]] - how the schema keeps maintenance disciplined
- [[Ingest Query Lint Loop]] - the repeating maintenance cycle
- [[Index and Log]] - control files that help the LLM navigate the vault
- [[Reinforcement Learning]] - first domain hub page seeded from an ingested paper
- [[Agentic Reinforcement Learning]] - RL training for multi-turn tool-using LLM agents in stateful environments
- [[Transformer Architecture]] - decoder-only Transformer blueprint plus attention, RoPE, and KV-cache synthesis
- [[Video Transformers]] - extending attention to video via divided space-time attention (TimeSformer)
- [[Diffusion Models]] - generative models that learn to reverse noising processes for images and other data
- [[LLM Training Pipeline]] - pretraining, SFT, RLHF, DPO, and LoRA as one connected map
- [[Neural Network Fundamentals]] - gradient descent, backpropagation, PyTorch, and Adam as the substrate under higher-level model pages
- [[Algorithm Templates for Interviews]] - template-selection map connecting classic DSA interview patterns with ML engineering preparation
- [[Model Quantization and Efficiency]] - quantization, KV cache, LoRA, and sparse activation as deployment/adaptation efficiency levers
- [[KV Cache]] - runtime attention-state storage and compression for long-context decoding
- [[LLM Inference]] - the prefill (compute-bound) vs decode (memory-bound) split and the serving stack built around it
- [[On-Device Reasoning]] - local reasoning under mobile constraints, where memory, latency, and power shape the whole stack
- [[Small Language Models]] - small/on-device/high-volume LLMs designed around deployment and inference constraints
- [[Reasoning Compression]] - shortening, replacing, or budgeting explicit reasoning traces to reduce cost without losing accuracy
- [[Mixture of Experts]] - sparse architectures that trade total capacity against lower active compute per token
- [[AI Accelerator Architecture]] - logic gates, systolic arrays, memory hierarchy, and cluster-scale compute/communication tradeoffs
- [[Context Engineering]] - managing the full context window at inference time as information architecture
- [[Model Routing]] - selecting model tiers/providers per request so long-loop agent workloads stay affordable
- [[Small Language Models]] - constrained model designs for local, cheap, or high-volume inference
- [[Multi-Teacher On-Policy Distillation]] - frontier post-training consolidation from domain-specialist teachers
- [[World Models]] - learned predictive models (Renderer / Simulator / Planner taxonomy) for planning, control, and embodied intelligence
- [[Direct Preference Optimization]] - completion-level preference learning; SFT vs DPO mechanical distinction; self-rejection pairs for structured outputs
- [[Vision-Language Grounding]] - text-conditioned spatial localization across objects, GUIs, documents, and scenes
- [[Monte Carlo Tree Search]] - search-time planning plus dense policy targets from AlphaGo-style supervision
- [[Automated AI Research]] - autoresearch loops, experiment execution, and the remaining bottlenecks in research agents
- [[Recursive Self-Improvement]] - AI systems improving parts of the process that creates future AI systems
- [[Tool Use and Function Calling]] - how LLMs request real-world actions
- [[Model Context Protocol]] - open standard for universal tool integration
- [[Agentic Loop]] - the iterative cycle powering multi-step tool use
- [[Agent Skill]] - reusable agent capability artifacts spanning markdown procedures, durable workflows, and optimization loops
- [[Search-Augmented Language Models]] - LLMs with RL-trained search tool policies
- [[Retrieval-Augmented Generation]] - Classic, Graph, and Agentic RAG as a single retrieval-architecture map
- [[Direct Corpus Interaction]] - terminal-mediated corpus search as a precision layer for agentic retrieval
- [[Reward Design for RL]] - composite reward signals for multi-objective LLM training
- [[Group Relative Policy Optimization]] - relative-policy optimisation method used in the Perplexity RL stage
- [[Agentic Reinforcement Learning]] - multi-turn RL training for tool-using agents
- [[Multi-Turn Evaluation]] - turn-level plus conversation-level scoring for simulated and live multi-turn systems
- [[Latent-Space Reasoning]] - reasoning through internal latent states instead of explicit token traces
- [[Recursive Architectures]] - modern recursive reasoning systems such as HRM, TRM, and RecursiveMAS
- [[Nested Learning]] - continuous inference-time learning and memory-as-structure (Titans, Continuum Memory System, Hope)
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
- [[Agentic Reinforcement Learning]]
- [[Cameron R. Wolfe - Agentic RL Frameworks and Best Practices]]
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
- [[Agent Skill]]
- [[djfarrelly - The Agent Loop Architecture]]
- [[Alpha Signal - How your agents can write and optimize their own skills]]
- [[Inngest]]
- [[Reward Design for RL]]
- [[Transformer Architecture]]
- [[Diffusion Models]]
- [[Mayank Pratap Singh - Diffusion Model Visual Breakdown]]
- [[LLM Training Pipeline]]
- [[Neural Network Fundamentals]]
- [[Model Quantization and Efficiency]]
- [[Small Language Models]]
- [[ByteByteGo - Large Language Models vs Small Language Models]]
- [[On-Device Reasoning]]
- [[Reasoning Compression]]
- [[Mixture of Experts]]
- [[AI Accelerator Architecture]]
- [[Vision-Language Grounding]]
- [[Monte Carlo Tree Search]]
- [[Automated AI Research]]
- [[Recursive Self-Improvement]]
- [[Alyona Vert - AI 101 - What is Recursive Self-Improvement]]
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
