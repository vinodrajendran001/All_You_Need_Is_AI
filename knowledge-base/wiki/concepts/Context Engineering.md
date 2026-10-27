---
type: concept
created: 2026-06-05
updated: 2026-10-27
tags:
  - concept
  - context-engineering
  - prompt-engineering
  - ai-agents
  - production-ai
source_ids:
  - src-2026-06-05-systemdesign42-system-design-academy
  - src-2026-06-10-bytebytego-token-spend-routing
  - src-2026-06-22-cameron-wolfe-agentic-rl-frameworks
  - src-2026-06-22-alphasignal-agent-skill-optimization
  - src-2026-08-05-aibuilderclub-context-engineering-guide
  - src-2026-08-05-aibuilderclub-rag-vs-long-context-vs-fine-tuning
  - src-2026-08-05-aibuilderclub-prompt-context-harness-evolution
  - src-2026-08-07-avi-chawla-claude-code-cost
  - src-2026-08-26-alex-zhang-speculative-programmatic-tool-calling
  - src-2026-08-25-bytebytego-stealing-reasoning-traces
  - src-2026-07-16-lilian-weng-harness-engineering
  - src-2026-08-30-addy-osmani-audit-agent-files
  - src-2026-08-31-bytebytego-chatbot-request-lifecycle
  - src-2026-09-02-can-boluk-harness-playbook
  - src-2026-09-03-github-ai-coding-cost-efficient
  - src-2026-09-02-meta-organizational-second-brain
  - src-2026-09-01-iusztin-scoped-subagents
  - src-2026-09-15-bytebytego-llm-memory-goldfish
  - src-2026-09-14-li-long-context-latency
  - src-2026-09-29-yoon-multiplayer-ai
  - src-2026-10-05-bytebytego-lost-middle
  - src-2026-10-08-bytebytego-netflix-genrec
  - src-2026-10-12-rastogi-agent-engineer
  - src-2026-10-17-bytebytego-chunking-strategies
  - src-2026-10-19-rath-thin-orchestrator
  - src-2026-10-21-databricks-memcurrent
  - src-2026-10-26-bytebytego-salesforce-agent-stack
status: active
---

# Context Engineering

## Definition

Context engineering is the discipline of managing what goes into an LLM's context window at inference time. It is distinct from prompt engineering: prompt engineering is about crafting individual instruction phrasings to elicit desired output styles; context engineering is about the information architecture of the complete input — deciding *what* to include, *how much*, in *what order*, and what to leave out.

## Why it matters

LLM performance at inference time is determined by the content of the context window far more than by per-call prompt crafting. The context window contains system prompts, conversation history, retrieved documents, tool results, memory promotions, and any compressed summaries of prior state. Managing that window poorly — overloading it, leaving irrelevant content, failing to retrieve the right documents — is a primary source of production failures in deployed AI systems. As context windows grow longer (100K–1M tokens), the problem does not go away: longer windows increase cost, introduce lost-in-the-middle failures, and make token budget management more consequential.

## Current synthesis

### Context engineering vs. prompt engineering

| | Prompt engineering | Context engineering |
|-|-------------------|-------------------|
| **Focus** | How you phrase one instruction | What information populates the whole input |
| **Scope** | Single turn, one message | Full context window across turns |
| **Key skill** | Wording, instruction format | Information selection, compression, budget allocation |
| **Failure mode** | Wrong output format or style | Missing context, overloaded context, wrong retrieval |
| **When it matters most** | Few-shot examples, chain-of-thought elicitation | Long conversations, agentic systems, RAG pipelines |

Prompt engineering is a subset of context engineering — once you have the right context architecture, prompt phrasing matters less than what information is present.

### Skill files as optimizable context artifacts

[[Alpha Signal - How your agents can write and optimize their own skills]] adds a concrete artifact type to this page: the [[Agent Skill|skill file]]. A skill file is a standalone markdown operating procedure that enters the agent's context and tells it how to perform a task family, use tools, format outputs, and recover from failures.

The source's important shift is from one-off prompt tweaking to **text-space optimization**. SkillOpt, GEPA, and EvoSkill treat these text artifacts as external state that can be improved through rollouts, verifiers, reflection over trajectories, bounded edits, held-out validation, and rejected-edit buffers. This is context engineering becoming an optimization loop rather than a manual writing exercise.

The caveat is that this only works when the task has a verifiable feedback signal. For subjective or poorly specified work, automated skill-file optimization can overfit to weak evals or introduce hidden regressions.

### Context rules during agentic RL

[[Cameron R. Wolfe - Agentic RL Frameworks and Best Practices]] adds a training-time version of context engineering. In [[Agentic Reinforcement Learning]], the full rollout may contain many steps of generated text, tool calls, observations, rewards, and environment state. But the model-visible context at the next step does not have to be a naive append-only transcript.

Agent-R1-style frameworks store the full step-level trajectory, then apply an environment-specific context rule that can preserve, summarize, remove, or transform past steps before the next action. This matters because append-only context can create **context rot**: verbose tool outputs or irrelevant reasoning history crowd out useful state. The source reports that sliding-window context can outperform append-only and summarization strategies in some environments, reinforcing that "more context" is not always better.

### What context engineering manages

1. **System prompt** — role definition, capability boundaries, output format rules, tool schemas. Should be stable and concise, with use of important instructions tested across context positions rather than assumed from placement.
2. **Conversation history** — which prior turns to include. Naive approaches include all history; engineering approaches apply sliding windows, summarization of older turns, or importance-weighted retention.
3. **Retrieved content (RAG)** — what documents to include and how many. The quality of retrieval is a context engineering problem, not just a retrieval problem: wrong documents in the window cost tokens and actively mislead the model.
4. **Tool and function call results** — output from tool executions can be large. Truncating, summarizing, or filtering tool results before including them in the context is context engineering.
5. **Memory promotions** — facts promoted from long-term storage ([[Agent Memory]]) into the active context must be selected for relevance to the current query, not included wholesale.
6. **Token budget allocation** — on constrained systems ([[On-Device Reasoning]]), token budgets must be explicitly partitioned across system prompt, history, retrieval, and output reservation.

### Context window as information architecture

One useful analogy is a **bounded working store**: schema design becomes prompt structure, query
selection becomes retrieval, and cache management becomes history retention. It is not a reliable
database read: evidence present in the window can still go unused, and fewer tokens do not by
themselves establish lower end-to-end latency or better answers.

### Relationship to agent memory

[[Agent Memory]] distinguishes short-term context (the window) from long-term persistent storage. Context engineering operates at the boundary: deciding what to promote from long-term storage into the short-term window, how to represent it compactly, and when to evict. This makes context engineering the operational layer of memory management for agents.

### Relationship to on-device reasoning

[[On-Device Reasoning]] operates under hard token budget constraints on mobile-class hardware. Every byte of context competes with reasoning trace length and output. The Qualcomm paper's budget-forcing mechanism is a form of context engineering applied to the *reasoning* portion of the context specifically.

### Routing is the economic complement to context engineering

[[ByteByteGo - Token Spend Out of Control - The Case for Smarter Routing]] adds an important systems correction: even when you compress history, trim tool results, and retrieve more selectively, long-loop agents still have to resend large contexts many times. Context engineering controls **how many tokens** get sent; [[Model Routing]] controls **which model pays for them**.

The practical synthesis is:

1. **Reduce the context where you can** — summarize, filter, stage retrieval, reserve generation headroom.
2. **Measure token spend by feature/task** — context cost is often dominated by a few heavy workflows rather than by the highest request count.
3. **Route on the strongest trustworthy signal you already have** — if the system already knows the task mode (planning vs editing vs background chore), do not infer difficulty from scratch.

Kilo's production numbers are useful here because they show the limit of "just cache more." Even with high cache reuse, spend stayed high because request volume and uncached context were still large. That makes routing and context engineering complementary infrastructure layers rather than competing techniques.

### Production failure modes that context engineering addresses

- **Lost-in-the-middle**: a model can use middle-position evidence less reliably. Mitigation to test: move or compact critical evidence without losing exceptions; start/end placement is not a guarantee.
- **Context overload**: additional retrieved documents can degrade generation. Mitigation to test: rank and select while retaining needed coverage.
- **History drift**: older context can conflict with current state. Mitigation to test: summarize with provenance and explicit supersession rather than silently erasing constraints.
- **Tool result bloat**: verbose outputs consume space with low-density material. Mitigation to test: structured extraction that preserves evidence and error states.
- **Token exhaustion**: input can leave insufficient generation room. Reserve and enforce an explicit token budget; that prevents a size failure, not a reasoning failure.

### AI Builder Club's four operating strategies

[[AI Builder Club - Context Engineering - The Complete Guide (2026)]] consolidates the operational playbook into four strategies: **offload** detailed artifacts to external storage, **retrieve** them just in time, **isolate** specialist work in separate contexts, and **compress** history while preserving future constraints. It also names poisoning, distraction, confusion, and clash as context failure modes.

The collection adds a cache-level implication: stable prefixes and append-only histories can preserve prefix reuse, while dynamic material placed early invalidates it. Context design therefore affects quality, latency, and cost together.

### Cost attribution confirms the replay tax

[[Avi Chawla - 86 Percent of Your Claude Code Bill Has Nothing to Do With Your Prompts]] reports a vendor-associated team analysis in which visible user prompts accounted for only 14% of input tokens. The larger categories were system and skill instructions, MCP schemas, tool results, and prior assistant context. The exact percentages need independent replication, but the mechanism is durable: caching discounts repeated prefixes without removing their volume, and every retained tool result raises the cost of later turns.

## Two additions: code as context economy, and traces as leaked context

[[Programmatic Tool Calling]] ([[Alex L. Zhang - Speculative Programmatic Tool Calling]]) offers a structural answer to a problem this page usually attacks with summarization and retrieval. When the agent's action is a program, a large intermediate result can be processed *in the interpreter* and only its conclusion returned. Under a JSON tool-call contract that result must pass through the context window to be acted on at all. Filtering, aggregation, and fan-out become interpreter work rather than context work.

From the opposite direction, [[ByteByteGo - How to Steal an AI Model's Private Thoughts]] shows that context management has a disclosure surface. Encrypted reasoning blocks are context the client carries but cannot read — and because they cannot be read, they cannot be sanitised. A scan of 6,708 published agent trajectories recovered API keys, passwords, and private keys from blocks whose visible text had been scrubbed clean. See [[Reasoning Trace Privacy]]. The operational rule is that opaque context artifacts must be **removed** rather than cleaned, and that compaction, forking, and history editing all rest on the same portability that makes the leak possible.

## Context collapse, and why playbooks must be itemized

[[Lilian Weng - Harness Engineering for Self-Improvement]] names a failure mode that any
self-maintaining context file eventually hits. **Context collapse** occurs when a whole context
document is regenerated each round by a model with a brevity bias: accumulated detail erodes round
after round until the playbook is shorter and worse than where it started. The problem is not the
model's judgement about any single item — it is that wholesale rewriting gives every item a fresh
chance to be dropped.

ACE (Agentic Context Engineering) is the structural fix. It splits the work across a **generator**, a
**reflector**, and a **curator**, and stores the evolving playbook as **itemized bullets** added,
edited, or retired one at a time. Updates become local, attributable, and reversible. MCE extends this
to a bi-level loop — meta skill evolution above base context optimization — and Meta-Harness goes a
rung higher by optimizing the optimizer's own code. See [[Harness Optimization]] for the full ladder.

## The null result this page has to answer

[[Addy Osmani - Audit your Agent files]] supplies the sceptical case, with numbers larger than most of
the positive evidence in this area:

- **288 runs across 17 tasks**: the presence of `AGENTS.md` / `CLAUDE.md` made **no clear difference to
  correctness**. It did change behaviour — agents wrote more targeted tests — but the outcome measure
  did not move.
- Anthropic removed **more than 80%** of Claude Code's system prompt with **no measurable eval loss**.
- Across 100 repositories: **lint leakage 62%, context bloat 42%, skill leakage 35%**.
- **Personalized skills performed roughly on par with borrowed ones**, and a generic skill built from
  many developers' practice was **more useful** than a personalized one. (Caveat, flagged by Osmani
  himself: the study used an LLM-based developer simulator.)
- Agents answering behavioural questions from **prose summaries** scored **4/45**; from **source code**,
  **27/45**.

The last finding constrains how context should be written for agents: a summary of behaviour is a poor
substitute for a pointer to the code that implements it. The others invert the default — context
**must justify itself against an eval, and the default action for an unjustified rule is deletion**.
Osmani's mechanics are worth keeping straight: `/doctor` (in-session) audits active configuration
while `claude doctor` (CLI) only runs install diagnostics; `/memory` is a separate review pass; and
skill *listings* are budgeted at roughly **1% of the context window**, with only the invoked skill's
body loading — so a long skill body is cheap until called, but a proliferation of skill names is not
free.

## Context engineering as a serving fact

[[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]] restates this page's
subject from the infrastructure side: what reaches the model is an **assembled document** — system prompt,
tool definitions, memory, retrieved documents, conversation history, new message — which is why **two products
on the same model give different answers**.

Because the model is **stateless**, the whole document is re-sent every turn. The worked progression is
**1,100 → 1,300 → 1,500 tokens**, reaching roughly **4,900 by turn 20**, and input dominates the bill.

**The multiplier is in the tool loop.** Each tool result re-runs the entire pipeline. Twenty tool calls means
the earliest messages are paid for **twenty times**, and a **2,000-token instruction block across 200 calls
becomes 400,000 input tokens before any work is done**.

This changes what a bloated instruction block *is*. Once, it is negligible; two hundred times, it is the
dominant cost of the run. Instruction-block size is therefore an agent-architecture decision rather than a
prompt-writing one — and it gives the itemized-playbook argument above a second, purely economic
justification. Layout matters too: cached prefixes bill at roughly **1/10 of the input rate**, so stable
content belongs at the top and changing content at the bottom. See [[KV Cache]], [[Agentic Loop]] and
[[Inference Efficiency Frontier]].

A related constraint the vault had not recorded: token counts for the same meaning differ by **up to 15×**
across languages, so an identical context budget is not an identical amount of usable context.

## Three 2026 results: scheduling, measurement, and disclosure

Three sources ingested together sharpen this page in different directions.

**Compaction is a scheduling problem, not an exception handler.** [[Can Bölük - The Harness Playbook]] argues
that firing compaction when the context window fills guarantees it fires at the worst moment — mid-task, with the
user waiting. The alternative is to schedule it roughly 10% before the limit, branch the session, and splice the
compacted result in. Related designs he catalogues: **remote compaction**, where a provider compacts server-side
with access to decrypted thinking that the client can never see (and returns an opaque blob), and **handoff**,
where the summary is written for a fresh session rather than for continuation. The same source warns that
**truncation must be opt-out, not opt-in** — an opt-in flag guarantees uneven coverage, and he found truncation
layers stacking N+1 deep inside a single evaluation path.

**Token savings must be measured on the loop, not the component.** [[GitHub - How We Make AI Coding More Cost Efficient]] shipped an aggressive output compressor that reduced per-response tokens and raised total cost,
because agents re-read what had been removed. The compressor that shipped is deliberately conservative: preserve
source-like output (`cat`, `git diff`, `git show`), reorganise search results losslessly, and compress repetitive
build and install noise only when the savings are substantial. The framing is worth keeping: it is
*"conservative not because the goal was to build a conservative compressor, but because that is what the
evaluations supported."*

**Progressive disclosure has a reported magnitude.** [[Meta - An Organizational Second Brain]] reports roughly
**80% fewer tokens per turn** from routing an agent through gateway files and deterministic routing indexes
rather than loading a fixed context — the largest context reduction figure in this vault, though unattributed
across several simultaneous changes.

Together these push the page's centre of gravity from *what to put in the window* toward *when to change it, and
how to know the change helped*.

## Delegation is a context-engineering technique before it is an architecture

[[Paul Iusztin - From 1 Bloated Context Window to 6 Scoped Subagents]] argues the case in its subtitle — **"subagents are context engineering"** — and the
motivating failure is a context failure, not a capability one: a deep-research setup that passed "up to
200 notes, transcripts, and PDFs to a single Claude Code session", which read them "1 by 1, taking minutes
and draining my weekly subscription." The fix was six researcher subagents running in parallel, each
dropping its internal state and returning only final results.

That reframes the question. The value of a child process is the **asymmetry between what it reads and what
it returns** — tens of thousands of tokens consumed against a 1,000–2,000-token summary handed back. Where
that asymmetry is absent, delegation is overhead. Where it is large, it is the cheapest available form of
context compression, because the noise never enters the parent's window at all rather than being
summarised out of it afterwards.

The implementation detail that makes this a context decision rather than an architectural one: the result
budget is shared and divided, `child_max_bytes = 16_000 // len(prompts)`. A wider fan-out gives each child
*less* room to report. Context is the scarce resource being allocated, and the fan-out width is the knob.

See [[Agent Delegation]] for the in-harness versus process distinction, and [[Tool Roster Economics]] for
the complementary cost — the tool list itself.

## Long context is a provider-specific latency decision

[[ByteByteGo - Do LLMs Have the Memory of a Goldfish]] separates memory architecture from context
capacity: replaying ten rounds that each add about 1,000 tokens processes roughly **55K cumulative
input tokens**, even though the visible conversation ends near 10K. Caching can reduce repeated
compute, but cannot prevent context crowding or choose which history remains relevant.

[[Jason Li - Latency Scaling Differences for GPT and Claude Models]] shows why the retention policy
cannot be model-agnostic. Across API measurements up to roughly 900K tokens, GPT-5.6 Terra and Sol
show strong upward TTFT curvature while Claude Sonnet 5 is near-linear and Opus is noisy but
consistent with little curvature. The result is behavioral evidence, not proof of the underlying
attention architecture, because TTFT also includes network, routing, queueing, and cache effects.

## Hand-maintained context files lose to context extracted from work that shipped

Almost every context artifact on this page - `AGENTS.md`, skill files, itemized playbooks, curated
memory - assumes someone maintains it. [[Jina Yoon - We're Building Multiplayer AI]] puts a count
against that assumption: over **90 days**, **64 users** started a shared `CONTEXT.md` and only **14**
ever edited it. This is internal product observation from PostHog, not a study - there is no
denominator of eligible users, no selection method, and no comparison group - but it is a measurement
of a premise this page has largely taken on faith.

PostHog's replacement inverts who writes. The context layer starts nearly empty and a nightly
**"dreaming" task** records what happened that day into a version-controlled Markdown wiki, extracting
from work objects such as PRs, docs, and dashboards. The selection rule is the design: record what was
**actually shipped, merged, or decided in a day**, not meeting notes or brainstorming documents, so
the agent does not treat proposals as company state. That is a context-selection criterion this page
has not carried before. Relevance, recency, density, and token budget all ask *how much* to include;
this one asks whether anything in the organisation ever committed to the claim.

It sits beside Osmani's null result rather than overturning it. His **288 runs across 17 tasks** found
that the presence of `AGENTS.md` / `CLAUDE.md` made **no clear difference to correctness**, and his
rule is that context must justify itself against an eval, with deletion the default for anything that
cannot. Yoon's finding is upstream of that argument: for most teams the file was never written in the
first place. The two do not combine into a conclusion, because PostHog reports **no measured
hallucination reduction, token savings, latency change, or task-quality lift** from the derived layer,
and it had been dogfooded for only **a few weeks**. One source says curated context has not shown its
value; the other says curation does not happen by default. Neither licenses the other's remedy.

There is also an unresolved conflict with the context-collapse material above. A nightly writer that
re-reads the day and regenerates a wiki is structurally the wholesale-rewrite pattern ACE was built to
avoid, with a brevity-biased model given a fresh chance to drop items each round. Two things differ -
the source of truth is external work objects rather than the document's own prior text, and the store
is version-controlled so a drop is recoverable - but version control is the only defence stated, and
nothing reported measures whether detail survives across nights.

## Available context and usable context are different measurements

[[ByteByteGo - The LLM Blindspot - Lost in the Middle]] separates four failures: evidence never
supplied, evidence truncated, retrieval that misses it, and evidence present but not used. Only the
last can establish a position effect when the question, evidence, length, and distractors are
controlled.

The causal mask does not bar the answer from earlier middle tokens. Its permission is not a
guarantee of effective evidence use. Likewise, the explainer's RULER comparison across 17 models
measures length-dependent degradation, not a pure position experiment or a universal 20K-token
cliff.

The operating consequence is to test *effective* context on the task: move the same evidence,
retain qualifications and citations when compressing it, and measure the answer. Tags, repetition,
query-focused retrieval, and start/end placement are candidate mitigations, not universal fixes
or security boundaries.

## Context selection also matters when the model never writes an answer

[[ByteByteGo - How Netflix Taught an LLM to Recommend Movies]] supplies a non-agent example:
GenRec verbalizes viewing history and metadata for a catalog-scoring head. The input remains
text even though inference produces rankings rather than prose.

Its selection policy spends detail on stronger engagements and cold-start item metadata,
compresses repeated viewing, and drops weak events. Context-length experiments show diminishing
ranking returns from adding history. The account reports roughly **one third of the original
tokens** and a similar serving-cost reduction, with prompts also arranged for shared-prefix reuse.

This extends the page's information-allocation rule beyond chat history. What matters is useful
evidence per input budget, not preserving every event or making the model generate a shorter
answer. It does not reverse the earlier compression warning: the capture gives no matched
ablation, model/hardware configuration, or general guarantee that cutting tokens preserves quality
or cuts cost proportionally.

## Measured guidance bundles do not settle the prose-only question

[[Sarthak Rastogi - Make Your Coding Assistant a 10x AI Engineer]] supplies a small positive
comparison: **53% versus 34% of requirements met** across six tasks with three runs per arm,
graded blind against a prewritten checklist. The intervention adds skills, isolated workers,
and hooks together. Only two tasks are explicitly held out from experiment-driven changes.

That does not contradict Osmani's null result for instruction files: the interventions,
tasks, and outcome measures differ, and no component ablation identifies a prose-only effect.
The useful addition is to treat activation and persistence as evaluated choices. Optional
project records can retain design and experiments with user agreement, but a corrected final
message did not repair a false report in the source's own failure example.

On-demand loading limits when skill bodies enter context; it does not establish zero cost
for discovery metadata, hooks, or host integration. Context must still earn its place through
the complete workflow's measured results.

[[ByteByteGo - EP229 Chunking Strategies for RAG-Based Agents]] restates the on-demand pattern
as a five-step runtime sequence: keep a skills index in the prompt, let the model pick a skill,
then load only that `SKILL.md`. Its premise, "Long prompts hurt agent performance," and its
promise of more consistent behavior are unmeasured. It describes the mechanism this section
qualifies; it does not test it.

## Interference is an architectural failure, not a budget failure

Most of this page treats a crowded context as a **cost** problem with a quality tail. [[Plawan Rath et al - The Thin Orchestrator]]
reports it as a correctness problem severe enough to force a rebuild. A single Meta agent holding
schemas, code-generation rules, routing logic, validation requirements, and patterns for **more than
10 data sources** reportedly **cross-contaminated concepts between subsystems** and hallucinated in
production while working in demos. The authors' summary is the inversion this page's
"more context is not always better" material has lacked a blunt statement of: **"The agent had
everything it needed. That was the problem."**

Their response is context isolation as architecture rather than as compression. Domain knowledge lives
in **25+ files**, typically a few thousand tokens each, loaded **at runtime by the specialist that
needs them**; the coordinating router holds none of it. This is progressive disclosure applied at
*agent* granularity rather than at document granularity — the unit that never sees the irrelevant
material is a whole subagent, so **"No agent sees the full picture. That's the feature, not the
bug."** The nearest figure the page already holds is [[Meta - An Organizational Second Brain]]'s
roughly **80% fewer tokens per turn** from gateway files and routing indexes; this is the same
company's second application of the same instinct, with no token figure attached.

One measurement is worth recording precisely because of what it measures: a single-agent alternative
reached **70-80%** success **with manual prompt engineering per task** and **10-20%** without it. Read
as a context result, that is a statement about **how much hand-tuning a loaded context requires to
work at all** — not a benchmark, since workload and sample size are unstated and the comparison is
self-reported. The whole account is first-party with **no ablation** separating context isolation from
deterministic routing, workflow templates, and runtime loading, so "interference caused the failure"
remains the authors' diagnosis rather than a demonstrated cause.

## Distilled memory matched full context at roughly 12x fewer input tokens

[[Databricks AI Research - MemCurrent Persistent Memory for Production Agents]] supplies the efficiency
anchor this page has wanted for the "dumping history into the window is expensive rather than thorough"
claim. On three open benchmarks — LoCoMo (**19-32 sessions/sample**), LongMemEval (**38-62
sessions/sample**), and a ConvoMem subset of **500 samples** at **100 sessions/sample**, averaged over
the LangGraph and OpenAI Agents SDK harnesses and **three repeats**, with GPT 5.6 luna as both agent
and memory model — a memory system scored **88.1%** against **87.8%** for injecting full context, at
**8.4K versus 103K input tokens per question**. That is roughly **12x fewer** input tokens for
comparable accuracy on those benchmarks.

Two qualifications travel with it. The comparison is **first-party**, and the authors note that open
benchmarks use **synthetic conversations** that may not represent enterprise work. And matching
full-context accuracy at lower token use does not establish that a distilled context is *more*
accurate than full context in general — only that, here, the extra 95K tokens per question bought
nothing measurable.

The architectural finding is more transferable than the ratio. The system separates **episodic
memory** (append-only raw traces) from **derived memory** (mutable, distilled knowledge files), and on
their internal benchmark derived memory alone scored **66.1%** while episodic alone scored **35.8%**,
against a **22.3%** no-memory floor and **68.4%** for both. Stated in this page's terms: **what you
carry forward should be distilled, not replayed.** Retrieval over raw history is the weaker mechanism
even when the raw history is available. The access-pattern result points the same way — background
offline consolidation alone reached **63.5%** against **53.9%** for agent-invoked memory tools —
which says the agent deciding in-session what to keep is worse than a process that reviews sessions
afterwards. All of these are Databricks' own figures on a **114-test-case**, company-built,
partly LLM-judged benchmark drawn from Genie sessions, so they indicate a direction, not a
general law.

**A naming collision to keep straight.** Databricks calls its offline consolidation pipeline
**"dreaming"**, and so does the nightly context-extraction task described above from
[[Jina Yoon - We're Building Multiplayer AI]]. They are **unrelated systems from different companies**
that happen to share a word. PostHog's writes what shipped that day into a shared, version-controlled
company wiki; Databricks' consolidates one agent's own prior sessions into derived memory files,
splitting oversized files, merging duplicates, and resolving conflicts. Only the Databricks pipeline
has an ablation behind it.

## Some jobs should leave the context window entirely, not just be compressed inside it

[[ByteByteGo - A Deep Dive into Salesforce's Agent Tech Stack]] relays, from interviews with
[[Salesforce]] executives, a redesign that removes work from the window instead of shrinking it. The
first Agentforce prompt had to enforce the rules, find the customer, include the right data, and keep
the agent within its permissions. The team observed that this held "for up to eight instructions. But
beyond eight, the model would discard instructions." The article concludes that a prompt "cannot
enforce that behavior".

Each job now has its own system. Agent Script runs a `before_reasoning` block before the prompt is
built, so the appointment lookup that a naive prompt merely requests "always runs reliably". Data 360
resolves identity, Agent Identity holds permissions (see [[Agent Security and Governance]]), and the
Agent Context Engine selects data in six steps: resolve, plan, reconcile, govern (access, masking,
consent), compile, and learn. The rule of thumb, "use code for the parts we want predictable behavior,
such as conditions, and use natural language for the parts that need actual reasoning", extends the
code-as-context-economy point above from intermediate results to instructions. Unlike the
deterministic router in [[Plawan Rath et al - The Thin Orchestrator]], the model still picks the
subagent; code governs what runs before and after it.

The token comparison is weaker evidence than the Databricks result above. In one demo, "show me
details of my insurance plan" took 124,000 tokens without context management and 9,000 with the
engine. After a follow-up, the naive session had used about 300,000 tokens in two questions, and the
engine 65,000 after a third step that processed an enrollment. Step counts differ and answer quality
is not reported, so this is a spend claim, not the comparable-accuracy claim Databricks measured.

The learn step adds a persistence rule. A note that a customer may be moving is "a memory, not yet a
fact" until the enrollment, and "only approved facts like this are promoted into long-term memory".
That is the commitment test of PostHog's shipped, merged, or decided rule from
[[Jina Yoon - We're Building Multiplayer AI]], applied to one customer's record instead of a company
wiki. Despite the shared acronym, this ACE is unrelated to Agentic Context Engineering above, and the
account does not say whether its memory is edited item by item or regenerated.

The limits are those of a secondhand account of vendor interviews. The demo company and patient are
simulated, the eight-instruction observation names no method, sample, or model, and no before/after
rate of dropped rules is reported.

## Open questions

- What is the right abstraction layer for context engineering in multi-agent systems where multiple agents share or read each other's contexts?
- How do very long context windows (1M+ tokens) change the engineering priorities vs. practical retrieval-based approaches?
- Can context engineering be learned and automated (the model manages its own context), or does it require explicit engineering?
- Does deriving context from shipped work avoid context collapse or relocate it? A nightly
  regeneration has the same brevity-bias exposure ACE describes, with git history as the only stated
  recovery path.
- What eval would show that derived context beats no context? PostHog reports none, and Osmani's null
  result is the only controlled comparison this page has for context files at all.
- Databricks' 12x token reduction is measured against full-context injection on synthetic open
  benchmarks. What does the ratio look like on real enterprise sessions, where their own histories were
  too long to inject at all?
- Isolating a specialist's context prevents interference but also removes any chance of a cross-domain
  connection. Nothing in the Meta account measures what the isolated agents fail to notice.
- Distilled derived memory outperformed raw episodic traces by a wide margin, and the authors concede
  **distillation can drop details**. What detects a dropped detail before it costs a task?
- Salesforce's context-engine demo reports large token reductions with unequal step counts and no
  answer-quality comparison. What matched test would show that a governed selection pipeline keeps
  answers as good as full context, as Databricks showed for distilled memory?

## Related pages

- [[Plawan Rath et al - The Thin Orchestrator]]
- [[Databricks AI Research - MemCurrent Persistent Memory for Production Agents]]
- [[Databricks]]
- [[Meta]]
- [[Continual Learning for Agents]]
- [[ByteByteGo - EP229 Chunking Strategies for RAG-Based Agents]]
- [[Sarthak Rastogi - Make Your Coding Assistant a 10x AI Engineer]]
- [[agent-engineer]]
- [[ByteByteGo - How Netflix Taught an LLM to Recommend Movies]]
- [[Semantic Recommendation Systems]]
- [[Netflix]]
- [[ByteByteGo - The LLM Blindspot - Lost in the Middle]]
- [[Transformer Architecture]]
- [[Agent Memory]]
- [[Agent Skill]]
- [[Agentic Reinforcement Learning]]
- [[Retrieval-Augmented Generation]]
- [[On-Device Reasoning]]
- [[Model Routing]]
- [[Agentic Loop]]
- [[AI Agents in Production]]
- [[Direct Corpus Interaction]]
- [[Model Context Protocol]]
- [[LLM Training Pipeline]]
- [[ByteByteGo - Token Spend Out of Control - The Case for Smarter Routing]]
- [[Alpha Signal - How your agents can write and optimize their own skills]]
- [[Cameron R. Wolfe - Agentic RL Frameworks and Best Practices]]
- [[systemdesign42 - System Design Academy]]
- [[Coding Agent Harness]]
- [[Real-Time Voice AI]]
- [[Sarthak Rastogi - Making an AI Agent Production-Ready]]
- [[AI Knowledge Base Overview]]
- [[AI Builder Club - Build AI Agents]]
- [[Loop Engineering]]
- [[Avi Chawla - 86 Percent of Your Claude Code Bill Has Nothing to Do With Your Prompts]]
- [[Graph Engineering]]
- [[Agent Security and Governance]]
- [[Programmatic Tool Calling]]
- [[Reasoning Trace Privacy]]
- [[ByteByteGo - How to Steal an AI Model's Private Thoughts]]
- [[Alex L. Zhang - Speculative Programmatic Tool Calling]]
- [[Speculative Tool Execution]]
- [[Harness Optimization]]
- [[Lilian Weng]]
- [[Addy Osmani]]
- [[Lilian Weng - Harness Engineering for Self-Improvement]]
- [[Addy Osmani - Audit your Agent files]]
- [[Inference Efficiency Frontier]]
- [[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]]
- [[Tool Roster Economics]]
- [[Harness State Authority]]
- [[Institutional Knowledge Agents]]
- [[Can Bölük - The Harness Playbook]]
- [[GitHub - How We Make AI Coding More Cost Efficient]]
- [[Meta - An Organizational Second Brain]]
- [[Paul Iusztin - From 1 Bloated Context Window to 6 Scoped Subagents]]
- [[Paul Iusztin]]
- [[Agent Delegation]]
- [[Jina Yoon - We're Building Multiplayer AI]]
- [[Agent Workflow Maturity]]
- [[ByteByteGo - A Deep Dive into Salesforce's Agent Tech Stack]]
- [[Salesforce]]
