---
type: source-summary
created: 2026-09-11
updated: 2026-09-11
source_id: src-2026-09-01-iusztin-scoped-subagents
source_title: "From 1 Bloated Context Window to 6 Scoped Subagents"
source_author: Paul Iusztin
source_url: https://www.decodingai.com/p/subagents-are-context-engineering
tags:
  - source/summary
  - topic/agents
  - topic/context-engineering
source_ids:
  - src-2026-09-01-iusztin-scoped-subagents
status: active
---

# Paul Iusztin - From 1 Bloated Context Window to 6 Scoped Subagents

## Summary

Lesson 5 of an open-source course that builds a coding agent (**Decode**) from scratch in Python. The
thesis is compressed into the subtitle: **"Subagents are context engineering."** A subagent is not a
multi-agent architecture, it is a mechanism for keeping search noise out of the parent's context
window. Iusztin motivates it from his own failure case — a deep-research setup that passed "up to 200
notes, transcripts, and PDFs to a single Claude Code session", read them "1 by 1, taking minutes and
draining my weekly subscription" — and replaces it with "6 researcher subagents per query, running in
parallel, each dropping its internal state and returning only the final results to the orchestrator".

The valuable part is that the piece treats the two ways of spawning a child as a genuine design choice
rather than a preference, and states the trade-off in a way that survives the specific codebase: the
in-harness tool is a **context primitive**, `tmux` process spawning is a **process primitive**.

## Key claims

**A subagent exists to trade tokens for a compressed report.** Citing Anthropic's context-engineering
guide, "a subagent can burn tens of thousands of tokens reading code and hand back only a distilled
1,000- to 2,000-token summary". That asymmetry is the whole justification; if the child's work would
fit comfortably in the parent's window, the machinery buys nothing.

**The child's prompt is the only dynamic input; everything else is static configuration.** In Decode
the tool signature is `agent(prompts: list[str]) -> str`. The child's system prompt and permissions
come from a persona file, not from the caller. This is what makes the fan-out auditable — the parent
cannot widen the child's authority by phrasing the prompt differently.

**Budget enforcement belongs in the tool, not in the orchestration script.** Decode caps the fan-out at
`MAX_FANOUT_PROMPTS` = 6 per call, bounds concurrency with `asyncio.Semaphore(subagent_max_parallel)`
= 4, caps each child at `UsageLimits(request_limit=25)`, and divides a shared 16,000-byte result budget
as `child_max_bytes = 16_000 // len(prompts)`. Guards that fail return a `ModelRetry` — "the tool's way
of sending the model a correction instead of a result" — so the model is corrected rather than crashed.

**The report contract is enforced with one retry, then a warning.** A child must make at least one tool
call or return a non-empty result; on the first failure the harness retries with a nudge, and on the
second it substitutes a "no usable report" note rather than failing the whole fan-out.

**Two spawn mechanisms, two different things bought.** Keeping the subagent in the harness gives "the
cheapest subagent — a loop re-entry, not a process: no cold start, no serialization", a context window
that "stays clean by construction", and "the budget in 1 place". Claude Code goes further: "because the
parent and child run the same loop, the summary fork reuses the parent's prompt cache." Spawning the
CLI under `tmux` instead gives "a real boundary. An OS process, not an allowlist", live observability,
and "children that outlive the parent" as resumable on-disk sessions with state in plain Markdown.
Mario Zechner's objection to the built-in tool is quoted directly: it is *"a black box within a black
box"*.

**The persona catalog is a tools allowlist plus a permission mode, and the two are not the same knob.**
"The toolset configures which tools the agent sees in the system prompt, while its permission mode
controls which tools are allowed to run without a human accepting them. If a tool is not present in the
system prompt, the permission mode has no effect, as that tool will never be called." Decode's `build`
persona carries all 15 tools at `mode: default`; `plan` drops `write`, `edit`, `bash`; `code-reviewer`
drops `write` and `edit` but keeps `bash` with `allow: ["bash(git *)"]`.

**The subagent persona is deliberately crippled, and each removal has a stated reason.** `explore` is
marked `subagent: true`, so "the only way it runs is as a child of the `agent` tool". Its allowlist is
exactly `read`, `glob`, `grep`, `lsp` — no `bash`, no `web_fetch`, no `ask_user` "(which would deadlock
the fan-out)", and no `agent` "(to avoid recursion)".

**Fan-out is a harness guarantee, not a model behaviour.** It is "parallelism the harness guarantees,
not a courtesy the model may or may not extend by emitting N tool calls." The same argument recurs from
an unrelated pipeline: a 100-document serial loop rewritten under `asyncio.gather()` with a
`Semaphore(5)` turned an hours-long run into a bounded one.

**The semaphore exists because of the provider, not the model.** "When you own your infra... the
bottleneck is your infra, but when using an LLM API such as OpenRouter, OpenAI, or Gemini, you have
strict limits on how many requests you can make per minute." Owning the endpoint "skips that
negotiation entirely, and bursty fan-outs are the exact workload serverless GPU pricing was designed
for."

## Why it matters

This vault already holds the claim that the harness, not the model, decides coding-agent quality — and
Iusztin opens with the same evidence, that in LangChain's Terminal-Bench experiment "changing only the
harness (with the same model) moved a coding agent from ~30th place into the top 5". What is new here is
a concrete, inspectable answer to *where the budget lives*. [[Tool Roster Economics]] established that
tool rosters have a measurable cost; this source shows the complementary move, which is bounding the
cost of *delegation* rather than of the tool list.

The in-harness-versus-process distinction is the durable contribution. It reframes a question usually
argued as taste ("are subagents worth it?") into two questions with different answers: do you need the
parent's context protected, or do you need a real security boundary and live observability? Those are
independent, and the source says so.

The persona catalog also sharpens [[Agent Skill]] and [[Agent Plugin Architecture]]: a persona is a
Markdown file with YAML front matter carrying name, description, tools allowlist, default mode,
optional allow/deny rules, and a subagent flag, with the system prompt in the body. That is the same
shape the vault has recorded for skills, applied to the agent's own identity rather than to a capability.

## Tensions / open questions

- Decode has no in-flight queue letting the parent talk to a running subagent; Iusztin names this as
  unbuilt. Without it, a fan-out is fire-and-forget, and a child that misreads its prompt burns its full
  25-request budget before anyone finds out.
- Truncating every report to `16_000 // N` bytes means a wider fan-out gives each child *less* room to
  report. Six children get ~2.7 KB each. Nothing in the source establishes that a useful report fits.
- The author's own practice diverges from his artifact: for fan-outs beyond 10 agents he uses Claude
  Code's dynamic workflows rather than either mechanism described here, and says "I rarely reach for
  `tmux`". The tmux case is argued more than it is used.
- No measurement. The numbers here are budgets and limits, not results. There is no before/after on
  token spend, latency, or answer quality for the six-subagent research setup that motivates the piece.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Agent Delegation]]
- [[Context Engineering]]
- [[Coding Agent Harness]]
- [[Agent Skill]]
- [[Harness Optimization]]
- [[Paul Iusztin]]

## Related pages

- [[Agentic Loop]]
- [[Agent Frameworks]]
- [[Harness State Authority]]
- [[Agent Plugin Architecture]]
- [[Tool Roster Economics]]
- [[Can Bölük - The Harness Playbook]]

## Citations

- Raw capture: [[2026-09-01 Paul Iusztin - From 1 Bloated Context Window to 6 Scoped Subagents]]
- Source: <https://www.decodingai.com/p/subagents-are-context-engineering>
