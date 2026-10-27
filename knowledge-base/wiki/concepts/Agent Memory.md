---
type: concept
created: 2026-06-05
updated: 2026-10-27
tags:
  - concept
  - ai-agents
  - memory
  - state
source_ids:
  - src-2026-06-05-pguso-agents-from-scratch
  - src-2026-05-21-bytebytego-batch
  - src-2026-06-29-siddhant-rai-nested-learning
  - src-2026-07-02-alyona-vert-ai-concepts-2026
  - src-2026-08-05-aibuilderclub-ai-agents-101-part-3
  - src-2026-08-05-aibuilderclub-agent-memory-systems-guide
  - src-2026-08-05-aibuilderclub-ai-coding-agent-memory-agentmemory
  - src-2026-08-05-aibuilderclub-codebase-memory-mcp-guide
  - src-2026-07-24-ren-et-al-self-improvements-agentic-systems-survey
  - src-2026-09-02-meta-organizational-second-brain
  - src-2026-09-12-cheruku-patel-multitenant-agentic-ai
  - src-2026-09-05-lenz-nemoclaw-memory-agent
  - src-2026-09-15-bytebytego-llm-memory-goldfish
  - src-2026-09-29-yoon-multiplayer-ai
  - src-2026-10-05-bytebytego-lost-middle
  - src-2026-10-21-databricks-memcurrent
  - src-2026-10-23-image-aware-agent-memory
  - src-2026-10-26-alphasignal-memory-tax
status: active
---

# Agent Memory

## Definition

Agent memory is the set of mechanisms by which an agent retains information beyond the immediate prompt context. This vault's sources distinguish three layers: **in-context state** (what the model can see right now), **short-term session memory** (facts stored within one interaction sequence), and **long-term persistent storage** (data that survives across separate sessions).

## Why it matters

Persistent memory lets agents accumulate context across sessions, maintain user preferences,
and build on earlier work. External stores can make retained evidence and retrieval decisions
inspectable; this is an architectural choice, not a property of every kind of memory.
The structural-memory approaches discussed below retain information inside model computation.

## Current synthesis

### The context/memory distinction

[[pguso - Agents From Scratch]] makes the clearest definition in this vault:
- **Context** = everything currently in the prompt. Temporary. Gone when the interaction ends.
- **Memory** = persistent storage that outlives the prompt. Loaded into context on demand.

In this external-store design, the model sees the memory that the application retrieves into
its context. Explicit storage and retrieval make inspection and access control possible;
they do not establish that either control is implemented correctly.

### Explicit over implicit

The pguso repo stores memory as a simple list of strings and gives the model explicit control over what gets saved:

```python
# Agent returns structured output including what to remember
{"reply": "Nice to meet you, Alice!", "save_to_memory": "User's name is Alice"}
```

The application layer writes this to the memory store. On the next interaction, it prepends all stored facts to the prompt:

```
You remember the following:
- User's name is Alice
```

This pattern exposes the saved facts, not everything the model knows from its weights.
There is no opaque embedding lookup in this example; the stored facts are plain text.

### Short-term vs long-term

| Layer | Lifetime | Storage | Use case |
|-------|----------|---------|----------|
| In-context state | One loop iteration | `AgentState` object (steps, done, current_plan) | Loop control, step counting |
| Session memory | One multi-turn session | In-memory list or Redis | User name, task progress, partial results |
| Long-term memory | Across sessions | PostgreSQL, files, vector DB | User preferences, historical summaries, project facts |

The Grab production case from [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]] uses Redis for fast session needs and PostgreSQL for conversation history — a direct instance of this tiered pattern.

### Memory as a reliability lever

The pguso example loads all saved facts, without a matching or ranking step. This is a
simple baseline for a small store, not exact-match search or a demonstrated best choice
for every application. Semantic retrieval is a separate scaling decision.

For this text-memory pattern, retain inspectable facts rather than only an opaque retrieval
embedding. The broader external-memory requirement is **traceable evidence and controlled
retrieval**, not that every record be plain text. [[Image-Aware AI Agent Memory - Oracle 26.8]]
illustrates the distinction: a searchable caption can point to original image bytes that
remain available for authorized inspection. Its storage design does not by itself prove
correct retrieval or authorization.

### State vs memory

[[pguso - Agents From Scratch]] also distinguishes agent *state* from agent *memory*:
- **State** (`AgentState`) tracks loop mechanics: step count, done flag, current plan. It resets between runs.
- **Memory** stores facts the agent should know. It persists across runs.

Both are Python objects the developer can inspect at any time, which is what makes debugging possible.

### Episodic, semantic, and procedural memory

The AI Builder Club collection adds a functional taxonomy:

- **episodic memory** records events and prior runs;
- **semantic memory** stores durable facts and relationships;
- **procedural memory** stores reusable instructions, skills, and workflows.

This taxonomy cuts across storage technologies. Files, databases, vector indexes, and codebase maps are implementation choices; the harder questions are what gets written, how stale or conflicting items are handled, and what is promoted into active context. Automatic accumulation without provenance, expiry, or conflict policy creates memory poisoning rather than learning.

### A contrasting frame: memory as structure, not storage

The pguso design treats memory as **explicit stored text** loaded into context by the
application. [[Siddhant Rai - Nested Learning]] introduces a different view: memory as
**learnable structure inside the model's computation**, updated during inference rather
than retrieved into the prompt. See [[Nested Learning]].

- It places memory on a **learning spectrum** — in-context (attention as ephemeral memory, erased when context clears), continual (accumulate across tasks, threatened by catastrophic forgetting), and inference-time (weights update during the forward pass).
- Its **Continuum Memory System** organizes memory as a chain of modules updated at different frequencies (fast/volatile recent detail → slow/stable consolidated knowledge), a structural answer to the **plasticity-stability tradeoff**.
- The tension with the storage view is real and intentional: storage memory is auditable but external and inert; structural memory is integrated and adaptive but harder to inspect and carries stability/safety risk. This vault keeps both framings rather than collapsing them.
- [[Alyona Vert - AI Concepts and Techniques in 2026]] adds a third framing to track: **conditional (selective) memory**, illustrated by DeepSeek's Engram, where a model *retrieves* memory through sparse lookups instead of storing everything in parameters or an ever-growing context. Its "U-shaped allocation law" — the best systems balance memory capacity against computation rather than maximising either — is a frontier signal that memory is becoming something a model decides *what to keep and when to fetch*, sitting between the storage and structural poles above.

## Memory as one of several scaffold update surfaces

[[Zhe Ren et al - Self-Improvements in Modern Agentic Systems]] places memory inside a wider frame
that is useful for this page. It treats memory as one component of an agent's **scaffold** — alongside
prompts, tools, and control logic — and treats a write to any of them as the same kind of event: a
durable, execution-derived update.

The clarifying consequence is the survey's boundary between durable and transient. The transient
context of an ongoing interaction, including in-context examples held in the attention cache, is not
part of the agent's intrinsic configuration, no matter how much an agent appears to remember within a
session. The boundary is durability, not representation. The survey still counts implicit memory
objects, such as self-updatable latent memory pools and latent embeddings injected into the KV cache,
as memory scaffolding. Only what survives the interaction and is retrievable afterwards counts.
That gives this page a sharper test than "does the agent recall it" — namely, does anything get
written back, and can a later run retrieve it.

It also suggests, as the vault's reading of the survey's version-history formalism, that memory
should be governed like the other scaffold surfaces: **versioned, validated, and reversible**. Memory writes are usually treated as append-only bookkeeping, but under this framing
a bad memory write is the same class of event as a bad tool registration — a durable change to future
behavior that ought to be inspectable and undoable. See [[Recursive Self-Improvement]].

## Memory as a compiled, reviewable artifact

[[Meta - An Organizational Second Brain]] describes a memory system whose defining property is that **every
update is a text diff a domain expert can review in 30 seconds.** The agent's durable knowledge is 200+ structured
files — position files, taxonomies, routing indexes, gateway files — and improvement happens by compiling expert
feedback into those files rather than by writing embeddings, appending to a scratchpad, or retraining.

Two design rules distinguish it from the memory architectures already on this page.

**Memory is typed, and the types are enforced.** *Recipes* hold procedures and no domain facts; *knowledge files*
hold declarative positions and no procedures. The purpose is failure attribution: when the agent is wrong, the
type tells you whether the procedure or the knowledge is at fault. Undifferentiated memory stores cannot make
that distinction, which is why their failures are hard to fix rather than merely hard to detect.

**Memory declares its own dependency graph.** Each file names `depends_on` and `referenced_by` in frontmatter, so
the consequences of an edit are a lookup rather than an investigation — and so a deterministic linter can reject
dangling references and dependency cycles before anything is served.

The retrieval boundary is drawn by **information density and expected usage frequency**: dense, frequently needed
material is promoted into curated memory; the rest stays in a retrieval corpus. Loading that memory by
progressive disclosure rather than in full is reported to cut **tokens per turn by about 80%**.

The costs are the usual ones for curated memory, and the source does not hide them: the compile-validate-review
loop is ongoing human and machine expense, and the reported outcomes after three sprints are qualitative with no
denominators. See [[Institutional Knowledge Agents]].

## Memory is selected state, not replayed history

[[ByteByteGo - Do LLMs Have the Memory of a Goldfish]] reinforces the application boundary: model
weights hold trained knowledge, the context window holds temporary working state, and cross-session
memory is external data retrieved into a later prompt. Prompt caching reduces repeated computation
but does not enlarge context or decide what should be remembered.

[[Tanya Lenz - Building a Memory-Driven Agent with NVIDIA NemoClaw]] adds a governed self model:
human-readable Markdown for people, projects, priorities, and provenance; SQLite for obligations,
rankings, corrections, and audit events. On 186 author-reported questions it improves overall
accuracy from **82.8% to 90.9%**, but lowers corpus faithfulness and single-hop lookup. Memory is
therefore a selective trade, not a monotonic improvement.

For multi-tenant systems, [[Nithin Reddy Cheruku and Dhawal Patel - Multi-Tenant Agentic AI with Gemini Enterprise]]
makes scope part of correctness. A memory key that omits tenant identity can turn a good retriever
into a cross-account data leak; tenant, user, session, provenance, and deletion policy must travel
together.

## The weak point is the writer: 64 users started a context file and 14 edited it

Every curated-memory design on this page - explicit `save_to_memory` returns, typed knowledge files,
governed Markdown self-models - assumes a writer who keeps writing.
[[Jina Yoon - We're Building Multiplayer AI]] reports a count against that assumption: over
**90 days**, **64 users** started a shared `CONTEXT.md` and only **14** ever edited it. These are
internal product observations from PostHog rather than a study, with no denominator of eligible users,
no selection method, and no comparison group. Held loosely, it is still the only number this page has
about whether curated memory gets maintained, and it lands directly on the premise the Meta
second-brain material rests on and does not test.

PostHog's answer converts memory maintenance into a pipeline. A nightly **"dreaming" task** records
what happened that day into a version-controlled Markdown wiki, extracting from work objects such as
PRs, docs, and dashboards. The write criterion is what was **actually shipped, merged, or decided**,
excluding meeting notes and brainstorming documents so that a proposal never becomes a remembered
fact. Read against this page's taxonomy, that is an episodic-to-semantic consolidation rule with a
provenance test folded into it: the artifact carrying an organisational commitment is also the
evidence for the memory, so the store inherits an audit trail without anyone writing one.

The **artifact** mechanism adds a layer this page's three tiers do not cleanly hold. Artifacts are
portable session-state snapshots - a session produces one, and that artifact becomes context for the
next session. By the Ren et al. test this page adopts (does anything get written back, and can a later
run retrieve it) that is durable memory rather than transient context, yet it is scoped to a work
object rather than to a user, a session, or an agent. Memory keyed to *the thing being worked on* is a
fourth scoping dimension alongside the tenant, user, and session keys the multi-tenant material
requires.

What is not resolved is who may read any of it, and PostHog says so: it calls governance and
permissions **one of its biggest blind spots**, and says it is interviewing users to learn more.
Without a stated population, its early data says users **overwhelmingly preferred starting tasks
privately** despite the team expecting shared-Space defaults, and collaboration happened more in
GitHub than in the product; the **~200 employees** figure the post gives is scoped to three recurring
Space-**setup** patterns, not to these findings, and the 64/14 counts above are **user** counts that
are not a fraction of it. A memory layer whose inputs are shared work objects, serving users who
default to private work, has a key-design problem before it has a retrieval problem. And the layer
reports **no measured hallucination reduction, token savings, latency change, or task-quality lift**
after **a few weeks** of dogfooding, so it belongs on this page as a design with an argument, not as
evidence that derived memory works.

## Persisting and retrieving a fact does not ensure that the next answer uses it

[[ByteByteGo - The LLM Blindspot - Lost in the Middle]] adds a final stage to the memory lifecycle:
evidence use after promotion into context. Stored, retrieved, present, and actually used are four
different states. A durable memory can survive perfectly on disk and still fail its immediate task
when buried among distractors.

Test the promoted fact at different positions with the same question and controlled context, then
inspect the answer rather than treating retrieval or citation as completion. Compaction should keep
the original reference and material exceptions so relevance optimization does not become fact
rewriting. This strengthens the writer-maintenance argument above while rejecting an unlimited
context window as a substitute for maintenance.

## The first ablation this page has for *which kind* of persistence pays

[[Databricks AI Research - MemCurrent Persistent Memory for Production Agents]] is the first source
here that removes memory components one at a time and reports what each was worth. The architecture
splits **episodic memory** — append-only raw session traces — from **derived memory**, mutable
structured knowledge files holding distilled corrections, preferences, definitions, and workflows. An
automatically generated **`memory.md` index** describes the available files, and a session-start
plugin injects that index; both types live in a production database, with derived memory represented
as a mutable table simulating a hierarchical filesystem. Reads go through `search_memory` and
`fetch_memory`; writes through `add_memory`, `update_memory`, and `delete_memory`.

On their **Internal Memory Benchmark** — **114 test cases**, **29 users**, and **2,233 history
sessions** mined down from **12K+** Databricks Genie sessions, covering **5 memory types** and **11
scenarios**, scored by an adversarial judge against seven criteria with manual review applied to case
construction, run with Claude Opus 4.6 as agent model and GPT 5.6 sol as memory model over three
repeats — the two ablations are:

| Configuration | Pass rate |
| --- | --- |
| No memory | **22.3%** |
| Episodic traces alone | **35.8%** |
| Derived memory alone | **66.1%** |
| Both | **68.4%** |
| Gold-memory injection (ceiling) | **78.6%** |

| Access pattern | Pass rate |
| --- | --- |
| Offline consolidation alone | **63.5%** |
| Agent-invoked memory tools alone | **53.9%** |
| Both | **66.1%** |

The authors' summary is **"Derived memory does most of the work"**, and the shape of the numbers
supports it: distillation carried the system from the 22.3% floor to 66.1%, while raw traces alone
reached 35.8% and added **2.3 percentage points** on top of derived memory. The authors note episodic
memory is searched in only about **one-third** of internal test cases. That reframes this page's
central question. Most designs recorded above — explicit `save_to_memory` returns, tiered session and
long-term stores, governed Markdown self-models — are concerned with *storing and retrieving* the
right item. This result says the determining step is **consolidation**: what gets distilled out of
history, not what gets fetched back from it. Against this page's episodic/semantic/procedural
taxonomy, "derived memory" collapses the semantic and procedural layers into one mutable store and
treats the episodic layer as a fallback for detail that distillation dropped.

The second ablation is the more uncomfortable one. A **background process reviewing sessions
afterwards (63.5%)** beat **the agent deciding in-session what to remember (53.9%)**, which is
evidence against the explicit-control pattern this page opens with — the pguso design in which the
model names what to save. Explicit control remains the more *auditable* arrangement; it is not, on
this benchmark, the more *effective* one.

**Two naming hazards, stated plainly.** First, Databricks calls its offline consolidation pipeline
**"dreaming"**, and so does the nightly PostHog task recorded above from
[[Jina Yoon - We're Building Multiplayer AI]]. **These are unrelated systems from different companies
that happen to use the same word**, and nothing connects them. PostHog's writes what shipped, merged,
or was decided that day into a shared company wiki, drawing on work objects such as pull requests,
docs, and dashboards; Databricks' consolidates **one agent's own prior sessions** into its derived
memory files, extracting implicit learning, splitting oversized files, merging duplicates, and
resolving conflicts. PostHog reports no measured effect; Databricks reports the ablations above.

Second, the headline figures need their baseline attached. **"Triples pass rate", 31% fewer tokens,
and 26% faster are all measured against the no-memory baseline on Databricks' own internal
benchmark** — not against a competing memory system and not against full context. The absolute
internal numbers are **68.4%** pass rate at **252s** latency and **418K** tokens per task, reported as
**1.35x faster** and **1.44x cheaper** than no memory, closing **"over 80% of the gap"** to gold
injection. The one comparator shown there, Mem0, scored **43.9%** at higher latency and cost. The
frequently quotable workflow example — **11 tool calls, 8 subagents, and nearly six minutes** reduced
to **2 tool calls, 1 subagent, and 41 seconds** once a workflow was remembered — is an **anonymized
illustration, not a benchmark aggregate**, and demonstrates possibility rather than average
improvement.

Everything here is **first-party**: company-created, company-operated, partly LLM-judged, 114 cases,
and drawn from one product's sessions. The ablations cover memory type and access pattern only — not
indexing, retrieval, consolidation quality, conflict resolution, or memory-file structure — and the
results do not separate memory from model choice, prompting, harness, or Genie-specific
infrastructure. The authors' own caveats belong with the numbers: offline updates arrive with
**delay**, plugins add runtime cost and latency and are inflexible, tool quality depends on agent
capability, and **distillation can drop details** that episodic memory only partly recovers.

## Store the original evidence separately from its searchable description

[[Image-Aware AI Agent Memory - Oracle 26.8]] describes images persisted as DOCUMENT
records, retrieved through captions/descriptions, and returned without original bytes
unless `include_bytes=True` is requested. Ordered text/image message parts preserve the
relationship between a user's statement and attached evidence.

This separates three memory contracts: durability of the original, discoverability through
text, and selective loading into the application. It complements the consolidation tradeoff
above: a useful caption can omit the exact visual detail a later question needs. Keeping
the original permits later inspection, but does not guarantee retrieval of a record whose
caption never named that detail.

The unattributed tutorial describes a synthetic-image notebook, not a task benchmark or a
run reproduced here. Default byte omission reduces payload exposure but is not deletion or
authorization. Captions and metadata can also be sensitive; both search and original-byte
hydration need access checks, as [[Multi-Tenant Agent Architecture]] makes explicit.

## Against a full-context baseline, memory gave strong models no accuracy gain, and the writer set the ceiling

[[Alpha Signal - The Hidden Memory Tax in AI Agents]] asks a different question from the MemCurrent
ablation above: whether a memory layer beats giving the model the raw record, not whether it beats
having none. It relays MemoryTax, a Shanghai Jiao Tong University study that ran seven approaches
(full context, BM25-style retrieval, Mem0, a Zep graph, and the Pi, Codex, and Claude Code harnesses
searching the conversation as a JSON file) with GPT-4o-mini, GPT-6 Luna, and Claude Opus 5.5 on one
LoCoMo conversation. Mem0 was the most accurate method with GPT-4o-mini, but with GPT-6 Luna "full
context had the best outcome", and "Claude Opus 5.5 reached 95% with either method." A store also
costs something before it answers: with GPT-4o mini, building Mem0's store cost $0.56, more than the
$0.43 spent answering all 152 questions from full context, and it would break even only after
372–596 questions, depending on the model.

The second finding moves this page's *weak point is the writer* claim from people to models.
[[Jina Yoon - We're Building Multiplayer AI]] counts people who stop maintaining a context file;
MemoryTax finds the extracting model capping what any reader can recover. A Zep graph built by
GPT-4o-mini scored 43% when GPT-4o-mini read it and only 45% when Claude Opus 5.5 read it, while a
graph Opus built and read reached 87%, and Mem0 showed a similar pattern. "The key finding is that
the model that writes the memory dictates the final quality of the answer." That turns the MemCurrent
caveat that distillation can drop details, and the [[Image-Aware AI Agent Memory - Oracle 26.8]]
point that a caption can omit what a later question needs, into a ceiling the stronger reader barely
moved. The article's safeguard is the one the Oracle section argues, "keep original records
available", with that section's qualification that a kept original still has to be found.

The third finding applies [[Direct Corpus Interaction]] to conversational memory. Claude Opus 5.5 in
the minimalist Pi harness answered 99% of questions for $6.95 at about 10,000 input tokens per
question, against 95% for $17.84 and 28,900 tokens with full context. On the same model, Codex cost
$25.41 at 98% and Claude Code $28.41 at 97%, so the harness moved the bill far more than the accuracy,
which makes this as much a [[Harness Optimization]] result as a memory one. The comparison is not
quite like for like: the coding agents could read photo captions that the other methods could not,
and on the 88 questions whose evidence did not involve photos, Pi scored 100% and full context 99%.

The full-context findings do not contradict the MemCurrent ablation, because the baselines differ, as the
MemoryTax summary notes. The 66.1% for derived memory, 68.4% for both, and 43.9% for the Mem0 comparator
sit above a 22.3% no-memory floor on an internal benchmark whose histories were too long for full
context. Where [[Databricks AI Research - MemCurrent Persistent Memory for Production Agents]] does run a
full-context ceiling, on three open benchmarks that include LoCoMo, MemCurrent averaged 88.1% against
87.8% at 8.4K versus 103K input tokens per question, and its post claims a win over full context on the
two benchmarks with the longest histories, which by the session counts in its summary are not LoCoMo.
Read together, the two are compatible: MemCurrent matched full context on average and places its wins on
longer histories than LoCoMo's, while MemoryTax, on one LoCoMo conversation that fit every model's
window, found no accuracy gain for the stronger models. They part on cost. MemCurrent states its
open-benchmark saving in input tokens per question, and its summary gives no separate figure for building
the memory, while MemoryTax prices the build separately and suggests that only repeated queries over a
stable history would pay it back.

The access-method results pull in a different direction from MemCurrent's. With Claude Opus 5.5, Pi
searching the raw record scored 99%, while a Zep graph that Opus itself built scored 87%; the
photo-caption caveat above applies to the first figure. MemCurrent found retrieval over raw episodic
traces the weaker mechanism, and attributes that weak score to the agent searching its traces "in about a
third of test cases". Neither source tests search frequency, history length, or model directly, so the
distilled-over-raw reading holds for MemCurrent's long histories and is unsettled for histories that fit
the window.

The evidence is thin and secondhand. The article itself says "the study is not very comprehensive":
the results come from "one LoCoMo conversation, one run per configuration and a GPT-4o-mini judge",
so the weakest model graded the strongest, and the whole history fit within every model's context
window. The clipping has no byline, date, or canonical URL, and the paper is reachable only through
tracking redirects that were not followed, so no figure was checked against the study. GPT-6 Luna's
results are unquantified, and the costs and break-even range are local to this history, these model
prices, and these harnesses.

## Open questions

- At what memory store size does simple "get all" retrieval break down and semantic retrieval become necessary?
- How should conflicting facts be handled — does a newer memory overwrite an older one, or do both
  persist? MemCurrent now supplies a *mechanism* — an offline pipeline that splits oversized files,
  merges duplicates, and resolves conflicts — but no evaluation of whether its resolutions are correct,
  so the question is answered architecturally and not empirically.
- How should memory be scoped when multiple users share an agent system?
- When is **storage memory** (auditable, external) the right tool versus **structural/inference-time memory** (integrated, adaptive but opaque)? See [[Nested Learning]].
- If memory is derived only from artifacts that carry a commitment, what happens to knowledge that
  never becomes a PR, doc, or dashboard - and does the rule bias the store toward whatever a
  work-tracking system can see?
- When users work privately by default, whose memory does an automatic extractor write into, and what
  makes a later private session eligible to read it?
- Derived memory beat episodic traces **66.1% to 35.8%** on one 114-case company benchmark. Does the
  ordering hold where the valuable content is a specific prior transcript rather than a reusable
  correction, preference, definition, or workflow?
- Background consolidation outscored agent-invoked memory tools. If the agent is the weaker judge of
  what to remember, what remains of the auditability argument for explicit `save_to_memory` control?
- Distillation can drop details and episodic memory recovers only some of them. MemoryTax gives one
  single-pass data point: reading a Zep graph, Claude Opus 5.5 scored 45% when GPT-4o-mini built the
  graph and 87% when Opus built it, against 95% with full context, so what a single pass loses depends on
  the model that writes it. No source here measures whether loss compounds across passes.
- MemCurrent's results come from one product's sessions with an LLM judge. No independent party has
  reproduced them, and no cross-model or cross-agent portability experiment is reported.
- The MemoryTax history fit inside every model's context window. Does model-directed search over the
  raw record keep its accuracy and cost edge once a history outgrows the window, where MemCurrent's
  internal benchmark had to fall back to gold-memory injection as its ceiling?

## Related pages

- [[Alpha Signal - The Hidden Memory Tax in AI Agents]]
- [[Alpha Signal]]
- [[Direct Corpus Interaction]]
- [[Harness Optimization]]
- [[Coding Agent Harness]]
- [[Image-Aware AI Agent Memory - Oracle 26.8]]
- [[Databricks AI Research - MemCurrent Persistent Memory for Production Agents]]
- [[Databricks]]
- [[ByteByteGo - The LLM Blindspot - Lost in the Middle]]
- [[Multi-Turn Evaluation]]
- [[Zhe Ren et al - Self-Improvements in Modern Agentic Systems]]
- [[Agentic Loop]]
- [[Agent Planning]]
- [[AI Agents in Production]]
- [[Tool Use and Function Calling]]
- [[pguso - Agents From Scratch]]
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- [[Retrieval-Augmented Generation]]
- [[Nested Learning]]
- [[Siddhant Rai - Nested Learning]]
- [[Alyona Vert - AI Concepts and Techniques in 2026]]
- [[AI Knowledge Base Overview]]
- [[AI Builder Club - Build AI Agents]]
- [[Context Engineering]]
- [[Agent Security and Governance]]
- [[Institutional Knowledge Agents]]
- [[Meta - An Organizational Second Brain]]
- [[Meta]]
- [[Schema-Driven Knowledge Base]]
- [[ByteByteGo - Do LLMs Have the Memory of a Goldfish]]
- [[Tanya Lenz - Building a Memory-Driven Agent with NVIDIA NemoClaw]]
- [[Multi-Tenant Agent Architecture]]
- [[Jina Yoon - We're Building Multiplayer AI]]
- [[Agent Workflow Maturity]]
- [[Continual Learning for Agents]]
