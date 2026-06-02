---
type: concept
created: 2026-05-13
updated: 2026-06-02
tags: [tool-use, function-calling, llm, agents]
source_ids:
  - src-2026-05-04-bytebytego-llm-tool-use-mcp
  - src-2026-05-18-rag-architecture-comparison
  - src-2026-06-02-alphasignal-look-past-rag-pipeline
status: active
---

# Tool Use and Function Calling

The mechanism by which LLMs request actions from external systems without executing those actions directly.

## Core idea

LLMs are text-prediction engines with no built-in ability to interact with the outside world. **Tool use** is the pattern where the application layer surrounding the model provides a menu of available functions, and the model can respond with structured requests (typically JSON) instead of final answers. The application validates and executes the request, then feeds results back to the model.

**Function calling** is the formalised version of this pattern, introduced by OpenAI in mid-2023 as a first-class API feature. Each function is described with a name, purpose, and parameter schema. The model generates calls against these definitions; it never executes them.

## Key properties

- **Separation of reasoning and execution** — the model decides *what* should happen; the application layer decides *whether and how* it happens. This boundary is where security and control are enforced.
- **Structured output** — function calls are JSON, making them machine-parseable and validatable before execution.
- **Multi-step chaining** — the model can call several tools in sequence within a single user request, forming an [[Agentic Loop]].
- **Provider fragmentation** — before [[Model Context Protocol|MCP]], each provider (OpenAI, Anthropic, Google) had its own schema format, creating an N×M integration problem.
- **Search as tool use** — web search agents are a concrete instance of this pattern; see [[Search-Augmented Language Models]] for the RL-trained version.
- **Retrieval as tool use** — vector search, graph traversal, SQL lookup, and browser/search calls are common retrieval tools inside [[Retrieval-Augmented Generation]] systems, especially in the agentic variant.
- **Terminal access can be tool use too** — some agent tasks work better with low-level corpus interfaces such as `grep`, `find`, `cat`, `sed`, and shell pipelines than with vector search alone. This is the intuition behind [[Direct Corpus Interaction]].

The important nuance is that raw power still has to be wrapped in a model-legible interface. Terminal-style tools can expose precise evidence that a vector retriever would miss, but without good constraints they can also overwhelm the model with noise or create unsafe execution surfaces.

## Historical context

- **ChatGPT Plugins** (early 2023) — an earlier attempt at third-party tool integration. Deprecated by April 2024 due to discoverability issues, inconsistent quality, and security concerns.
- **Function calling API** (mid-2023) — OpenAI's controlled replacement. Developers explicitly define which tools the model can access.
- **MCP** (late 2024) — Anthropic's open standard that decouples tool definitions from provider-specific formats, solving the N×M problem.

## Related pages

- [[Model Context Protocol]]
- [[Agentic Loop]]
- [[Search-Augmented Language Models]]
- [[Retrieval-Augmented Generation]]
- [[Direct Corpus Interaction]]
- [[ByteByteGo - Connecting LLMs to the Real World]]
