---
type: source-summary
created: 2026-10-19
updated: 2026-10-19
source_id: src-2026-10-17-bytebytego-chunking-strategies
source_title: "EP229: 8 Chunking strategies for RAG-based agents"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/ep229-8-chunking-strategies-for-rag
tags: [source/summary, rag, chunking, embeddings, agent-skills]
source_ids: [src-2026-10-17-bytebytego-chunking-strategies]
status: active
---

# ByteByteGo - EP229 Chunking Strategies for RAG-Based Agents

## Summary

A weekly ByteByteGo "system design refresher" issue (EP229, published October 17, 2026) that
bundles five items: an embedded video on testing AI-written code, a list of eight chunking
strategies for retrieval, a simplified illustration of neural machine translation, an Agent Skills
workflow, and a PostgreSQL-versus-MySQL architecture comparison. A sponsored Railway section opens
the issue and is not part of the evidence here; the video's content was not captured.

Every item is a definition-level explainer. The issue reports no retrieval metrics, costs,
latencies, or comparisons, so it contributes vocabulary and a decision space, not evidence about
which strategy works.

## Key claims

### Eight chunking strategies

| Strategy | What decides the boundary, as described |
| --- | --- |
| Fixed-size | A fixed number of tokens, with a small overlap |
| Recursive | Paragraphs first, falling back to lines, then words and characters only when a piece is still too big |
| Document-based | Breaks the document already marks — headings, chapters, HTML tags — so a markdown file becomes one chunk per section |
| Semantic | Each sentence is embedded; a new chunk starts when similarity to the previous sentence drops |
| LLM-based | An LLM rewrites the text as standalone propositions, one idea per line, each becoming a chunk |
| Agentic | An agent reads each document, decides what it is (code, contract, table), and picks the method for that file |
| Late chunking | The full document runs through an embedding model first; normal split boundaries are then applied and embeddings are mean-pooled within each boundary |
| Hierarchical | Layers: sections, paragraphs, then sentences |

- Semantic chunking is said to find "real topic shifts instead of guessing by length." Nothing in
  the issue tests that claim.
- LLM-based chunking is "high quality but expensive across a large corpus." Neither quality nor
  cost is quantified.
- The section closes by asking which strategy readers run in production. It offers no selection
  rule.

### Agent Skills workflow

- Motivation: "Long prompts hurt agent performance." The claim is not quantified.
- The workflow has five steps: a user query arrives; the runtime combines it with a **skills
  index**, a lightweight list of available skills and short descriptions; the LLM reasons and
  selects a skill; the runtime loads `SKILL.md` into the active context; the LLM follows it, runs
  scripts, and produces the output.
- Claimed benefit: loading skills only when needed keeps "context small and the LLM's behavior
  consistent." The consistency claim is asserted, not measured.

### Translation illustration, explicitly not Google's current system

- The item is labeled "A simplified illustration of common techniques. Not an exact map of Google
  Translate's current system."
- Steps: a small classifier detects the source language; a BPE tokenizer splits text into subword
  tokens; a special token such as `<2es>` steers the output language; a Transformer encoder emits
  one vector per input token; the decoder predicts next-token distributions conditioned on those
  vectors; beam search keeps several candidate translations and returns the one with the highest
  probability.

### Out-of-scope database comparison

- PostgreSQL is described as process-based: each connection gets its own process sharing a common
  memory pool, with background workers for writing, vacuuming, and logging. MySQL is thread-based,
  with pluggable storage engines such as InnoDB and MyISAM. This is recorded for completeness and
  sits outside the vault's AI scope.

## Why it matters

The chunking list makes visible what the boundary decision is delegated to. Fixed-size,
recursive, and document-based chunking defer to length or to the author's structure; semantic and
late chunking defer to an embedding model; LLM-based and agentic chunking defer to a generating
model. That grouping is the vault's reading rather than the issue's framing. It connects chunking
to failure layers already recorded on [[Retrieval-Augmented Generation]] and
[[Embedding Model Selection]]: a boundary placed by embedding similarity inherits what the
embedding space does and does not encode, and a proposition written by a model is a paraphrase
whose support still has to be traced to the original passage.

The Agent Skills item restates the progressive-disclosure pattern [[Agent Skill]] already carries
from practitioner sources. It adds no measurement to set against the vault's null and mixed
evidence on context files.

## Tensions / open questions

- None of the eight descriptions addresses the split-conditions failure recorded from
  [[ByteByteGo - Why Do LLMs Lie]], where a rule and its exception land in different chunks.
  Rewriting text as one proposition per line could make that failure more likely unless each
  proposition carries its conditions; the issue does not say.
- Late chunking requires the whole document to pass through the embedding model. Long documents
  then depend on the model's maximum input length, and an edit anywhere in a document plausibly
  changes every chunk vector derived from that pass. Both are inferences from the described
  mechanism, not claims in the capture.
- Agentic per-document method choice turns chunking into a model decision whose errors are
  invisible at query time unless the method used is recorded for each document.
- Skill selection depends on the model reading short descriptions. The issue does not discuss
  mis-selection, overlapping skills, or what a loaded skill's scripts are permitted to do.
- The translation sketch is a teaching diagram. It is not evidence about any production
  translation system's architecture.

## Affected pages

- [[Retrieval-Augmented Generation]]
- [[Embedding Model Selection]]
- [[Agent Skill]]
- [[Context Engineering]]
- [[ByteByteGo]]

## Raw capture

- [[EP229 8 Chunking strategies for RAG-based agents]]

## Citations

- Canonical article: <https://blog.bytebytego.com/p/ep229-8-chunking-strategies-for-rag>
- Published October 17, 2026; captured October 19, 2026. The clipped URL's email-tracking
  parameters were removed above.
- The embedded testing video and the sponsored section were not used as evidence.

## Related pages

- [[Retrieval-Augmented Generation]]
- [[Embedding Model Selection]]
- [[Agent Skill]]
- [[Context Engineering]]
- [[ByteByteGo - Why Do LLMs Lie]]
- [[ByteByteGo - Why Your RAG System Is Only as Good as Its Translator Model]]
- [[Transformer Architecture]]
- [[Test-Time Scaling]]
- [[ByteByteGo]]
