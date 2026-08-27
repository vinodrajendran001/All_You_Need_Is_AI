---
type: concept
created: 2026-05-13
updated: 2026-08-27
tags: [concept, tool-use, function-calling, llm, ai-agents]
source_ids:
  - src-2026-05-04-bytebytego-llm-tool-use-mcp
  - src-2026-05-18-rag-architecture-comparison
  - src-2026-06-02-alphasignal-look-past-rag-pipeline
  - src-2026-06-05-pguso-agents-from-scratch
  - src-2026-08-26-alex-zhang-speculative-programmatic-tool-calling
  - src-2026-08-25-ibm-granite-4-2-how-they-are-built
status: active
---

# Tool Use and Function Calling

The mechanism by which LLMs request actions from external systems without executing those actions directly.

## Core idea

LLMs are text-prediction engines with no built-in ability to interact with the outside world. **Tool use** is the pattern where the application layer surrounding the model provides a menu of available functions, and the model can respond with structured requests (typically JSON) instead of final answers. The application validates and executes the request, then feeds results back to the model.

**Function calling** is the formalised version of this pattern, introduced by [[OpenAI]] in mid-2023 as a first-class API feature. Each function is described with a name, purpose, and parameter schema. The model generates calls against these definitions; it never executes them.

## Key properties

- **Separation of reasoning and execution** — the model decides *what* should happen; the application layer decides *whether and how* it happens. This boundary is where security and control are enforced.
- **Structured output** — function calls are JSON, making them machine-parseable and validatable before execution.
- **Multi-step chaining** — the model can call several tools in sequence within a single user request, forming an [[Agentic Loop]].
- **Provider fragmentation** — before [[Model Context Protocol|MCP]], each provider (OpenAI, Anthropic, Google) had its own schema format, creating an N×M integration problem.
- **Search as tool use** — web search agents are a concrete instance of this pattern; see [[Search-Augmented Language Models]] for the RL-trained version.
- **Retrieval as tool use** — vector search, graph traversal, SQL lookup, and browser/search calls are common retrieval tools inside [[Retrieval-Augmented Generation]] systems, especially in the agentic variant.
- **Terminal access can be tool use too** — some agent tasks work better with low-level corpus interfaces such as `grep`, `find`, `cat`, `sed`, and shell pipelines than with vector search alone. This is the intuition behind [[Direct Corpus Interaction]].

The important nuance is that raw power still has to be wrapped in a model-legible interface. Terminal-style tools can expose precise evidence that a vector retriever would miss, but without good constraints they can also overwhelm the model with noise or create unsafe execution surfaces.

## The request/execute separation (ground-up view)

[[pguso - Agents From Scratch]] adds the most explicit treatment of why this separation matters in practice:

> "The model **requests** tools. The system **executes** them. No autonomy yet."

The concrete implementation pattern:
1. Tool call is a structured JSON output: `{"tool": "calculator", "arguments": {"a": 42, "b": 7, "operation": "multiply"}}`
2. The application validates the tool name against the available registry
3. The application validates the arguments schema before running anything
4. Only then does execution happen

This separation provides:
- **Access control** — the registry defines what the model is allowed to call
- **Validation** — wrong argument types or missing fields are caught before any side effect
- **Human-in-the-loop** — the execution layer can pause for approval on high-stakes tools
- **Extensibility** — adding a new tool means registering a new function, not retraining the model

The repo makes one further observation: **structured output is the prerequisite for reliable tool use**. Free-text "I think I should call the calculator" is unparseable. A JSON schema with validation + retries turns probabilistic output into a reliable function-call contract.

## The alternative contract: code instead of schemas

Everything above describes a JSON-schema contract — one named tool, validated arguments, one result, back to the model. [[Programmatic Tool Calling]] ([[Alex L. Zhang - Speculative Programmatic Tool Calling]]) proposes the opposite: make executable code the action space and expose every tool as a function inside it. The strong form of the claim is that a code REPL is the only tool a system needs.

The trade is legible. Schemas buy **bounded, inspectable, approvable actions** — the properties this page's request/execute separation depends on. Code buys **composition, context economy, and an optimization surface**: control flow and fan-out happen in the interpreter instead of costing one model turn each, large intermediate results never traverse the context window, and the runtime can analyse a program in ways it can never analyse a JSON object — see [[Speculative Tool Execution]].

The two are not mutually exclusive, and the useful open question is where the line falls: irreversible or approval-gated actions arguably still want a schema, precisely because a program is an unbounded request.

## Historical context

- **ChatGPT Plugins** (early 2023) — an earlier attempt at third-party tool integration. Deprecated by April 2024 due to discoverability issues, inconsistent quality, and security concerns.
- **Function calling API** (mid-2023) — OpenAI's controlled replacement. Developers explicitly define which tools the model can access.
- **MCP** (late 2024) — [[Anthropic]]'s open standard that decouples tool definitions from provider-specific formats, solving the N×M problem.

## Related pages

- [[Model Context Protocol]]
- [[Agentic Loop]]
- [[Agent Planning]]
- [[Search-Augmented Language Models]]
- [[Retrieval-Augmented Generation]]
- [[Direct Corpus Interaction]]
- [[pguso - Agents From Scratch]]
- [[Coding Agent Harness]]
- [[Test-Time Scaling]]
- [[ByteByteGo - Connecting LLMs to the Real World]]
- [[Programmatic Tool Calling]]
- [[Speculative Tool Execution]]
- [[Alex L. Zhang - Speculative Programmatic Tool Calling]]
- [[Alex L. Zhang]]
