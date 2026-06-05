---
type: log
created: 2026-05-08
updated: 2026-06-05
tags:
  - log
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
status: active
---

# Knowledge Base Log

Append-only operational history for the wiki.

## [2026-05-08] scaffold | Knowledge base initialized

- Created the `knowledge-base/raw/`, `knowledge-base/wiki/`, and `knowledge-base/templates/` directory scaffold inside the current workspace.
- Added the root `CLAUDE.md` schema with workflows, page conventions, and maintenance rules.
- Seeded `knowledge-base/wiki/index.md` and this log for navigation and chronology.

## [2026-05-08] ingest | Andrej Karpathy - LLM Wiki

- Captured the raw gist in `knowledge-base/raw/sources/2026-05-08 Andrej Karpathy - LLM Wiki.md`.
- Created [[Andrej Karpathy - LLM Wiki]] as the first source summary page.
- Seeded [[AI Knowledge Base Overview]], [[Persistent Wiki]], [[Schema-Driven Knowledge Base]], [[Ingest Query Lint Loop]], [[Index and Log]], [[Andrej Karpathy]], and [[Obsidian]] from the source.

## [2026-05-08] ingest | Kevin Murphy - Reinforcement Learning: An Overview

- Captured the paper as `knowledge-base/raw/sources/2026-05-08 Kevin Murphy - Reinforcement Learning - An Overview.pdf`.
- Added `knowledge-base/raw/sources/2026-05-08 Kevin Murphy - Reinforcement Learning - An Overview.md` as the immutable raw-source note with arXiv metadata and abstract.
- Created [[Kevin Murphy - Reinforcement Learning - An Overview]] as the source summary page.
- Seeded [[Reinforcement Learning]] as the first domain concept page derived from the paper and updated [[AI Knowledge Base Overview]] plus the index.

## [2026-05-08] query | Mathematical foundations for reinforcement learning

- Filed [[2026-05-08 Mathematical Foundations for Reinforcement Learning]] in response to a query about the math needed to go from Murphy's survey to expert-level RL understanding.
- Linked the answer into the index as the first durable query note in the knowledge base.

## [2026-05-08] lint | knowledge-base/wiki

- Audited the wiki for broken internal links, orphans, thin seed pages, and schema conformance.
- Confirmed all internal wikilinks resolve and no wiki pages are orphaned.
- Fixed a stale claim in [[AI Knowledge Base Overview]] about empty operational folders.
- Added missing `## Related pages` sections to both source summary pages to align them with the schema.
- Filed [[2026-05-08 Wiki Lint Pass]] and linked it from the index.

## [2026-05-13] ingest | Connecting LLMs to the Real World: Tool Use, Function Calling, and MCP

- Moved raw capture from `raw/` to `raw/sources/` per schema convention.
- Created [[ByteByteGo - Connecting LLMs to the Real World]] as source summary page with 10 durable claims and an adoption timeline.
- Seeded three new concept pages: [[Tool Use and Function Calling]], [[Model Context Protocol]], and [[Agentic Loop]].
- Created [[ByteByteGo]] entity page.
- Updated [[AI Knowledge Base Overview]] and the index with the new domain area (LLM tooling and agents).

## [2026-05-13] lint | knowledge-base/wiki

- Audited `knowledge-base/wiki` for broken internal wikilinks, orphans, related-pages coverage, frontmatter conformance, thin pages, index completeness, log consistency, and raw-source coverage.
- Fixed six broken or out-of-scope wikilinks by replacing unresolved wiki targets with valid in-scope references or explicit raw-source file paths.
- Confirmed there are no orphan substantive pages, no missing `## Related pages` sections in scoped content folders, no frontmatter omissions, and no thin pages below the current body-text threshold.
- Verified every scoped content page is listed in the index, every ingest in the log has a corresponding source summary page, and every file in `raw/sources/` is covered by a source summary page.
- Filed [[2026-05-13 Lint Pass]] and linked it from the index.

## [2026-05-13] ingest | Advancing Search-Augmented Language Models

- Raw capture already in `raw/sources/Advancing Search-Augmented Language Models.md`.
- Created [[Perplexity - Advancing Search-Augmented Language Models]] as source summary page with 10 durable claims covering the two-stage SFT→RL pipeline, gated reward aggregation, anchored efficiency penalties, and benchmark results.
- Seeded two new concept pages: [[Search-Augmented Language Models]] and [[Reward Design for RL]].
- Created [[Perplexity]] entity page.
- Updated [[Reinforcement Learning]] with cross-links to the new search-agent RL techniques.
- Updated [[AI Knowledge Base Overview]] and the index with the new source and concepts.

## [2026-05-13] lint | knowledge-base/wiki (pass 2)

- Re-audited `knowledge-base/wiki` after the Perplexity ingest, including broken links, orphans, related-pages coverage, frontmatter, thin pages, index/log completeness, raw-source coverage, and cross-link density.
- Found one broken wikilink to [[Group Relative Policy Optimization]] and fixed it by creating the missing concept page.
- Added reciprocal cross-links from [[Tool Use and Function Calling]] and [[Agentic Loop]] to the new search-agent pages to improve integration density.
- Confirmed that all internal wikilinks now resolve, no substantive pages are orphaned, all scoped pages include `## Related pages`, and all non-PDF raw sources are covered by source summary pages.
- Filed [[2026-05-13 Lint Pass 2]] and linked it from the index.

## [2026-05-18] ingest | Alpha Signal - The Return of Recursion

- Raw source already in `knowledge-base/raw/sources/The return of recursion - How AI is rethinking complex reasoning.md`.
- Created [[Alpha Signal - The Return of Recursion]] source summary page.
- Created [[Latent-Space Reasoning]] and [[Recursive Architectures]] concept pages.
- Created [[Alpha Signal]] entity page.
- Updated index, overview, and log.

## [2026-05-18] lint | Full wiki lint pass

- Audited `knowledge-base/wiki` for broken wikilinks, orphans, related-pages coverage, frontmatter conformance, thin pages, contradiction risk, index/log completeness, raw-source coverage, and cross-link density.
- Fixed all broken control-file wikilinks by normalizing them to [[index|Knowledge Base Index]] and [[log|Knowledge Base Log]].
- Corrected invalid frontmatter in [[Kevin Murphy - Reinforcement Learning - An Overview]] and refreshed stale maturity wording in [[AI Knowledge Base Overview]].
- Strengthened reciprocal cross-links across Karpathy-, ByteByteGo-, and Perplexity-derived pages.
- Filed [[2026-05-18 Lint Pass]] and linked it from the index.

## [2026-05-18] ingest | The Pocket - PocketFlow Tutorial Docs

- Captured 39 tutorial documents from the PocketFlow Tutorial Video Generator repo to `raw/sources/pocketflow-tutorial-docs/`.
- Created raw source note and [[The Pocket - PocketFlow Tutorial Docs]] source summary page.
- Created [[The Pocket]] entity page.
- Created new concept pages: [[Transformer Architecture]], [[LLM Training Pipeline]], [[Neural Network Fundamentals]], [[Model Quantization and Efficiency]].
- Updated [[Reinforcement Learning]] with cross-links to detailed RL tutorial content.
- Updated index and overview.

## [2026-05-18] ingest | Han Fang - PyTorch Practice

- Captured 7 files (5 Python scripts + README + runner) from the pytorch-practice repo to `raw/sources/pytorch-practice/`.
- Created raw source note and [[Han Fang - PyTorch Practice]] source summary page.
- Created [[Han Fang]] entity page.
- Updated [[Neural Network Fundamentals]], [[Transformer Architecture]], [[Model Quantization and Efficiency]], and [[LLM Training Pipeline]] with cross-links to from-scratch PyTorch implementations.
- Updated index and overview.

## [2026-05-18] ingest | Classic RAG vs Graph RAG vs Agentic RAG

- Added frontmatter to raw source `Classic RAG vs Graph RAG vs Agentic RAG.md`.
- Created [[Classic RAG vs Graph RAG vs Agentic RAG]] source summary page.
- Created [[Retrieval-Augmented Generation]] concept page synthesizing across Classic, Graph, and Agentic RAG tiers.
- Updated [[Search-Augmented Language Models]], [[Agentic Loop]], and [[Tool Use and Function Calling]] with RAG cross-links.
- Updated index and overview.

## [2026-05-18] lint | Full wiki lint pass (post-ingest)

- Re-audited broken wikilinks, orphans, related-pages coverage, frontmatter, thin pages, index completeness, log consistency, raw-source coverage, cross-link density, and staleness risk across `knowledge-base/wiki`.
- Found no broken wikilinks, orphan substantive pages, missing related-pages sections, frontmatter gaps, thin substantive pages, index omissions, log mismatches, or raw-source coverage gaps.
- Corrected a stale source-ordering claim in [[AI Knowledge Base Overview]] so the Han Fang and RAG ingests now match chronological ingest order.
- Added an explicit raw-capture citation to [[Alpha Signal - The Return of Recursion]] to make the recursion-source coverage clearer.
- Filed [[2026-05-18 Lint Pass 2]] and linked it from the index.

## [2026-05-18] lint | Full wiki lint pass (post-consolidation)

- No broken wikilinks, orphan substantive pages, missing `## Related pages` sections, frontmatter gaps, thin pages, index omissions, log mismatches, raw-source coverage gaps, or cross-link density failures were found across `knowledge-base/wiki`.
- Verified that both `raw/sources/pytorch-practice/` and `raw/sources/2026-05-18 Han Fang - PyTorch Practice.md` intentionally map to [[Han Fang - PyTorch Practice]], so no new source summary was needed.
- Filed [[2026-05-18 Lint Pass 3]] and linked it from the index.

## [2026-05-21] ingest | Universal LeetCode Templates — The Complete Arsenal

- Added frontmatter to raw source `Universal LeetCode Templates — The Complete Arsenal.md`.
- Created [[Universal LeetCode Templates]] source summary page.
- Created [[Algorithm Templates for Interviews]] concept page synthesizing DSA templates with ML interview prep.
- Updated index and overview.

## [2026-05-21] lint | Full wiki lint pass

- Audited 45 markdown wiki pages for broken wikilinks, orphan pages, related-pages coverage, frontmatter conformance, thin pages, index completeness, log consistency, raw-source coverage, cross-link density, and staleness risk.
- Found no structural defects; all substantive pages resolve, are indexed, have valid frontmatter, and remain covered by the log and raw-source graph.
- Flagged the MCP timeline/security notes as time-sensitive monitor items for future ingests, but found no current contradictions requiring content edits.
- Filed [[2026-05-21 Lint Pass]] and linked it from the index.

## [2026-05-21] ingest | ByteByteGo - System Design and AI at Scale (May 2026 Batch)

- Added source_id frontmatter to 8 raw ByteByteGo articles in `raw/sources/`.
- Created composite source summary [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]].
- Created new concept pages: [[ML Systems at Scale]] and [[AI Agents in Production]].
- Updated [[ByteByteGo]] entity page, [[Agentic Loop]], [[Model Context Protocol]], [[Search-Augmented Language Models]], and [[Retrieval-Augmented Generation]] with cross-links.
- Updated index and overview.

## [2026-05-21] lint | Full wiki lint pass (post-ByteByteGo batch)

- Audited `knowledge-base/wiki` for broken wikilinks, orphan pages, related-pages coverage, frontmatter conformance, thin pages, index completeness, log consistency, raw-source coverage, cross-link density, and contradiction/staleness risk.
- Found no structural defects; all substantive pages resolve, are indexed, have valid frontmatter, and remain covered by the log and raw-source graph, including the composite ByteByteGo batch mapping.
- No immediate content-page fixes were required beyond control-file updates.
- Filed [[2026-05-21 Lint Pass 2]] and linked it from the index.

## [2026-05-29] ingest | Airtable Search + DoorDash LLM-as-a-Judge

- Added source_id frontmatter to 2 new raw articles.
- Created [[ByteByteGo - How Airtable Built the Search Layer]] and [[DoorDash - LLM-as-a-Judge for Search Evaluation]] source summary pages.
- Created [[LLM-as-a-Judge]] concept page.
- Created [[DoorDash]] entity page.
- Updated [[ML Systems at Scale]], [[Retrieval-Augmented Generation]], and [[ByteByteGo]] with cross-links.
- Updated index and overview.

## [2026-05-29] lint | Full wiki lint pass

- Audited 54 markdown wiki pages for broken wikilinks, orphan pages, related-pages coverage, frontmatter conformance, thin pages, index completeness, log consistency, raw-source coverage, cross-link density, and contradiction/staleness risk.
- Strengthened [[Search-Augmented Language Models]] and [[ML Systems at Scale]] with [[LLM-as-a-Judge]] links and DoorDash-derived evaluation notes so the new production-evaluation branch is fully integrated.
- Filed [[2026-05-29 Lint Pass]] and linked it from the index.

## [2026-06-02] ingest | Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club

- Captured the YouTube video metadata as `knowledge-base/raw/sources/2026-06-02 Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club.md`.
- Saved the auto-generated transcript in both VTT and cleaned text form under `knowledge-base/raw/assets/`.
- Created [[Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club]] as the source summary page.
- Seeded [[World Models]] and [[Y Combinator]].
- Updated [[Model Quantization and Efficiency]], [[LLM Training Pipeline]], [[AI Knowledge Base Overview]], and the index with the new source.

## [2026-06-02] ingest | Dwarkesh Patel - Eric Jang interview + flashcards

- Captured the article as `knowledge-base/raw/sources/2026-06-02 Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch.md` and preserved extracted body HTML plus readable transcript assets under `knowledge-base/raw/assets/`.
- Captured the flashcards as `knowledge-base/raw/sources/2026-06-02 Dwarkesh Patel - Eric Jang Flashcards.md` and preserved structured JSON plus readable markdown assets under `knowledge-base/raw/assets/`.
- Created [[Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch]] and [[Dwarkesh Patel - Eric Jang Flashcards]] as source summary pages.
- Seeded [[Monte Carlo Tree Search]], [[Automated AI Research]], and [[Eric Jang]].
- Updated [[Reinforcement Learning]], [[Agentic Loop]], [[AI Knowledge Base Overview]], and the index with the new sources and concepts.

## [2026-06-02] ingest | Dwarkesh Patel - Reiner Pope article + flashcards

- Captured the article as `knowledge-base/raw/sources/2026-06-02 Dwarkesh Patel - Reiner Pope - Chip design from the bottom up.md` and preserved extracted body HTML plus readable transcript assets under `knowledge-base/raw/assets/`.
- Captured the flashcards as `knowledge-base/raw/sources/2026-06-02 Dwarkesh Patel - Reiner Pope Flashcards.md` and preserved structured JSON plus readable markdown assets under `knowledge-base/raw/assets/`.
- Created [[Dwarkesh Patel - Reiner Pope - Chip design from the bottom up]] and [[Dwarkesh Patel - Reiner Pope Flashcards]] as source summary pages.
- Seeded [[AI Accelerator Architecture]] and [[Reiner Pope]].
- Updated [[Model Quantization and Efficiency]], [[ML Systems at Scale]], [[LLM Training Pipeline]], [[AI Knowledge Base Overview]], and the index with the new sources and hardware/compute branch.

## [2026-06-02] lint | Full wiki lint pass

- Audited 67 markdown wiki pages for broken wikilinks, relative links, orphan pages, related-pages coverage, frontmatter conformance, thin pages, index completeness, and staleness risk.
- Found no structural defects: no broken links, no orphans, no missing related-pages sections, and no index omissions.
- Expanded [[Alpha Signal]], [[Andrej Karpathy]], and [[Obsidian]] to address the only immediate content issue: thin entity coverage.
- Filed [[2026-06-02 Lint Pass]] and linked it from the index.

## [2026-06-02] ingest | Alpha Signal - As AI agents evolve, we need to look past the RAG pipeline

- Mapped the local raw capture `knowledge-base/raw/sources/As AI agents evolve, we need to look past the RAG pipeline.md` into a source summary page, preserving the fact that the capture did not include the original publication URL.
- Created [[Alpha Signal - As AI agents evolve, we need to look past the RAG pipeline]].
- Seeded [[Direct Corpus Interaction]].
- Updated [[Retrieval-Augmented Generation]], [[AI Agents in Production]], [[Tool Use and Function Calling]], [[Alpha Signal]], [[AI Knowledge Base Overview]], and the index with the new retrieval-interface branch.

## [2026-06-02] ingest | DoorDash chatbot evaluation + Braintrust multi-turn scoring

- Mapped `knowledge-base/raw/sources/How DoorDash Built a Testing System to Evaluate LLMs.md` into [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]].
- Mapped `knowledge-base/raw/sources/How to evaluate multi-turn conversations - Blog.md` into [[Braintrust - How to evaluate multi-turn conversations]].
- Seeded [[Multi-Turn Evaluation]] and [[Braintrust]].
- Updated [[LLM-as-a-Judge]], [[ML Systems at Scale]], [[DoorDash]], [[AI Knowledge Base Overview]], and the index to integrate the new evaluation branch.

## [2026-06-02] lint | Full wiki lint pass (post-evaluation ingests)

- Audited 74 markdown wiki pages for broken wikilinks, relative links, orphan pages, related-pages coverage, frontmatter conformance, thin pages, index completeness, and staleness risk.
- Found no structural defects: no broken links, no orphans, no missing related-pages sections, no frontmatter gaps, and no index omissions.
- Re-checked the active gap statements in [[AI Knowledge Base Overview]] and left them unchanged because they remain accurate.
- Filed [[2026-06-02 Lint Pass 2]] and linked it from the index.

## [2026-06-03] ingest | Fareed Khan - Train LLM From Scratch

- Captured the GitHub repository as `knowledge-base/raw/sources/2026-06-03 Fareed Khan - Train LLM From Scratch.md` and saved a commit-pinned README snapshot under `knowledge-base/raw/assets/`.
- Created [[Fareed Khan - Train LLM From Scratch]] as the source summary page.
- Seeded [[Fareed Khan]].
- Updated [[Transformer Architecture]], [[LLM Training Pipeline]], [[Neural Network Fundamentals]], [[AI Knowledge Base Overview]], and the index with the new code-first LLM training source.

## [2026-06-03] ingest | Liquid AI LFM2.5 + NVIDIA LocateAnything

- Mapped `knowledge-base/raw/sources/LFM2.5-8B-A1B An Even Better On-Device Mixture of Experts.md` into [[Liquid AI - LFM2.5-8B-A1B]].
- Mapped `knowledge-base/raw/sources/LocateAnything.md` into [[NVIDIA - LocateAnything]].
- Seeded [[Mixture of Experts]], [[Vision-Language Grounding]], [[Liquid AI]], and [[NVIDIA]].
- Updated [[Model Quantization and Efficiency]], [[AI Accelerator Architecture]], [[AI Agents in Production]], [[AI Knowledge Base Overview]], and the index to integrate the new sparse-model and multimodal-grounding branches.

## [2026-06-03] lint | Full wiki lint pass

- Audited 83 markdown wiki pages for broken wikilinks, relative links, orphan pages, related-pages coverage, frontmatter conformance, thin pages, index completeness, and staleness risk.
- Found no structural defects: no broken links, no orphans, no missing related-pages sections, no frontmatter gaps, and no index omissions among substantive pages.
- Re-checked the active gap statements in [[AI Knowledge Base Overview]] after the Liquid AI and NVIDIA ingests and left them unchanged because they remain accurate.
- Filed [[2026-06-03 Lint Pass]] and linked it from the index.

## [2026-06-04] ingest | Efficient Reasoning on the Edge

- Copied the user-provided PDF into `knowledge-base/raw/sources/2026-06-04 Yelysei Bondarenko et al - Efficient Reasoning on the Edge.pdf` and created the paired raw-source note with arXiv metadata, hash, and local PDF reference.
- Created [[Efficient Reasoning on the Edge]] as the source summary page.
- Seeded [[On-Device Reasoning]] and [[Qualcomm AI Research]].
- Updated [[Model Quantization and Efficiency]], [[LLM Training Pipeline]], [[Reward Design for RL]], [[Group Relative Policy Optimization]], [[AI Agents in Production]], [[AI Knowledge Base Overview]], and the index to integrate the new on-device reasoning branch.

## [2026-06-04] ingest | Efficient reasoning compression batch

- Downloaded seven arXiv PDFs into `knowledge-base/raw/sources/` and created paired raw-source notes for [[Training Large Reasoning Models Efficiently via Progressive Thought Encoding]], [[PACE - Prefix-Protected and Difficulty-Aware Compression for Efficient Reasoning]], [[Towards Efficient Large Language Reasoning Models via Extreme-Ratio Chain-of-Thought Compression]], [[ReasonCACHE - Teaching LLMs To Reason Without Weight Updates]], [[Compress the Easy, Explore the Hard - Difficulty-Aware Entropy Regularization for Efficient LLM Reasoning]], [[ConPress - Learning Efficient Reasoning from Multi-Question Contextual Pressure]], and [[Shorter Thoughts, Same Answers - Difficulty-Scaled Segment-Wise RL for CoT Compression]].
- Created the seven corresponding source summary pages under `knowledge-base/wiki/sources/`.
- Seeded [[Reasoning Compression]] as a new concept hub for CoT shortening, state-space substitution, and difficulty-aware reasoning-budget control.
- Updated [[LLM Training Pipeline]], [[Model Quantization and Efficiency]], [[On-Device Reasoning]], [[Reward Design for RL]], [[Group Relative Policy Optimization]], [[Latent-Space Reasoning]], [[Efficient Reasoning on the Edge]], [[AI Knowledge Base Overview]], and the index to integrate the new reasoning-compression branch.

## [2026-06-04] lint | Full wiki lint pass

- Audited all 95 wiki pages for broken wikilinks, broken relative links, missing frontmatter, missing type/updated fields, missing Related pages sections, thin pages, orphans, and index coverage.
- Found no structural defects. The wiki is healthy after the seven-paper reasoning-compression batch.
- Filed [[2026-06-04 Lint Pass]] and linked it from the index.

## [2026-06-05] ingest | pguso - Agents From Scratch

- Fetched the full GitHub repository `pguso/agents-from-scratch` via API: README, PHILOSOPHY, QUICKSTART, all 12 lesson markdown files, and the agent/evals/telemetry module listing.
- Created the immutable raw source note at `knowledge-base/raw/sources/2026-06-05 pguso - Agents From Scratch.md`.
- Created [[pguso - Agents From Scratch]] as the source summary page.
- Seeded [[Agent Planning]] (plans as data, atomic actions, AoT dependency graphs) and [[Agent Memory]] (short-term vs long-term, explicit storage) as new concept pages.
- Extended [[Agentic Loop]] with the ground-up anatomy: state transitions, termination as first-class design, structure-over-cleverness principle, and the full 12-lesson progression.
- Extended [[Tool Use and Function Calling]] with the request/execute separation pattern and why structured output is the prerequisite for reliable tool calls.
- Extended [[AI Agents in Production]] with the evals + telemetry disciplines (golden datasets, spans/traces, runtime metrics).
- Updated [[AI Knowledge Base Overview]], index, and log.

## [2026-06-05] ingest | Fei-Fei Li - A Functional Taxonomy of World Models

- Mapped `knowledge-base/raw/sources/A Functional Taxonomy of World Models.md` into [[Fei-Fei Li - A Functional Taxonomy of World Models]] as the source summary page.
- Seeded [[World Labs]] and [[Fei-Fei Li]] as new entities.
- Substantially updated [[World Models]] with the Renderer / Simulator / Planner taxonomy, POMDP-loop framing, Marble product, convergence thesis, and data-scarcity note.
- Updated [[AI Knowledge Base Overview]], index, and log.

## [2026-06-05] ingest | Dharma-AI - Direct Preference Optimization Beyond Chatbots

- Mapped `knowledge-base/raw/sources/Direct Preference Optimization Beyond Chatbots.md` into [[Dharma-AI - Direct Preference Optimization Beyond Chatbots]] as the source summary page.
- Created [[Direct Preference Optimization]] as a new concept page with the SFT-vs-DPO mechanical distinction, self-rejection pair methodology, three conditions for applicability, and the completion-level attractor argument.
- Updated [[LLM Training Pipeline]] with the DPO generalisation insight and self-rejection pairs pattern.
- Updated [[AI Knowledge Base Overview]], index, and log.
- Fixed orphan: linked [[2026-06-04 Efficient Reasoning on the Edge - Blog Post]] query from the index.

## [2026-06-05] lint | Full wiki lint pass

- Audited all 105 wiki pages for broken wikilinks, orphans, frontmatter completeness, related-pages coverage, and schema conformance.
- Found no structural defects after two new ingests (Fei-Fei Li world models taxonomy + DPO beyond chatbots).
- Discovered and documented the pre-existing Liquid AI validator false-positive (caused by `Path().stem` mis-parsing dots in filenames); corrected the validator.
- Filed [[2026-06-05 Lint Pass]] and linked it from the index.
