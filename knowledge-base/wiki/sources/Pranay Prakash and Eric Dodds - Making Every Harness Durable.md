---
type: source-summary
created: 2026-10-27
updated: 2026-10-27
source_id: src-2026-10-19-vercel-durable-harness
source_title: Making every harness durable
source_author: Pranay Prakash and Eric Dodds
source_url: https://vercel.com/blog/making-every-harness-durable
tags: [source/summary, ai-agents, agent-harness, durable-execution, reliability]
source_ids:
  - src-2026-10-19-vercel-durable-harness
status: active
---

# Pranay Prakash and Eric Dodds - Making Every Harness Durable

## Summary

A Vercel product announcement, published 19 October 2026, for `durable-harness`: open-source adapters
that make existing coding-agent harnesses (Pi, OpenCode, Codex, and Claude Code) survive crashes and
function timeouts **without changing the harness**. The design is a per-session durable log written
around every model and tool call, a queue message that hands an interrupted turn to a new function,
and a per-tool declaration of whether that tool may run again after a crash. Its durable contribution
to this vault is a concrete rule for the case resilience advice usually leaves open: what to do with a
tool call that was interrupted and may or may not have taken effect.

The article reports no measurements. It describes an interactive crash demo, which was not captured,
and the mechanism; recovery time, logging overhead, storage cost, and failure-injection results are
not given.

## Key claims

**The cloud breaks an assumption local harnesses rely on.** Harnesses were built for long-lived
processes holding the session in memory, and agent tasks commonly run for minutes or hours. Locally,
resuming interrupted work "only requires a simple prompt". A cloud VM with persistent storage does not
record "which model and tool calls completed or resume interrupted turns after a crash". In the
authors' words: "A failed turn or network error means lost work."

**Intent before, outcome after, and a queue as backstop.** Before a model or tool call runs,
`durable-harness` records an intent; when it finishes, it records the outcome. The turn is backstopped
by a queue message, so if its function dies, a new function reads the log and continues. After a crash
the log distinguishes what finished, what was running, and what never started:

| Call state after a crash | What happens |
| --- | --- |
| Completed (outcome recorded) | Never runs again; its result is read from the log |
| Interrupted tool marked `replay: 'safe'` | Runs again automatically |
| Any other interrupted tool | Returned to the model as **possibly run**; the model decides whether to check |

The vendor's stated consequence is that "you're never billed twice for a finished model call's
tokens", and that models "remember their previous calls rather than repeating them."

**Replay safety is declared per tool by the developer.** A lookup, a file read, or a CI status check is
`'safe'`. A refund or a PR comment is `'never'`: it "never runs twice: the model is told the call may
have happened, so it can check before it tries again." Tools the developer supplies run in the
developer's own function rather than in a sandbox, so database queries and API calls can run there and
"required credentials never have to enter the sandbox."

**The harness's own session files are mirrored, not replaced.** Claude Code's transcript, Codex's
rollout, and OpenCode's event store have every record mirrored into the log, so a new function or
sandbox rebuilds them from it. Vercel's own harnesses, eve and fx, are described as durable natively.

**Application state can live in the same log.** A *document* is typed JSON stored in the session's
log; tools edit it through `io.docs`, and "each edit commits to the log alongside the tool's result, so
the document's durable state stays consistent with the tool calls themselves". The `virtual()` workspace
is built the same way: its file tree is a document.

**Three workspace options, because a shared function host is not a safe place for a shell.** "Many
sessions can share the same function, and its filesystem isn't guaranteed to persist between
invocations." `virtual()` keeps files in the log with a bash-compatible shell that "can't reach your
function's files or the network"; `virtual({ durable: false })` is in-memory scratch cleared every turn;
`sandbox()` gives the session its own Vercel Sandbox with `/workspace` on a Drive that outlives every
sandbox and function. Claude Code and Codex always run in a sandbox, "since they expect a real shell and
filesystem, and aren't safe for multi-tenant use."

**One storage interface makes the agent portable.** The backend is the Workflow SDK's *World*, an
interface combining storage, a queue, and a stream — "the log, the backstop and the stream behind one
interface." Worlds exist for Vercel, local files, Postgres, MongoDB, Redis, and Turso; two environment
variables move an agent to Postgres. Resumed turns appear in the same trace in Vercel's Agent Runs view.

## Why it matters

[[LLM Application Resilience]] records an unreconciled tension: exponential backoff is the standard
response to a transient failure, yet a transient failure on a non-idempotent tool is exactly where a
retry is unsafe. This source supplies an explicit rule for the crash case — re-run only what the
developer declared safe, and hand everything else back to the model as uncertain — rather than leaving
the choice to a generic retry policy. It is a design, not an evaluation.

[[Harness State Authority]] argues that resume, rewind, and fork are only reliable when state derives
from one journal. `durable-harness` applies a journal from outside unmodified harnesses, and its
documents give application state the single-authority property the concept page asks for: the state
change and the tool result commit together.

[[Multi-Tenant Agent Architecture]] gains a runtime-residence case: on a shared function host, the
shell and filesystem move into a per-session virtual workspace or sandbox while credentials stay in the
developer's function.

## Tensions / open questions

- **No reported measurements.** There is no recovery-time figure, no overhead for logging every model
  and tool call, no storage cost, and no failure-injection result. The interactive demo is a product
  illustration; its trace labels survive only in the original clipping and are not evidence.
- **The `'never'` path moves the exactly-once problem to the model.** It works only if the model
  chooses to check and the tool's effect is checkable, for example a refund-status lookup. The article
  does not discuss idempotency keys, which the vault's other resilience sources recommend for the same
  problem.
- **The window between a call finishing and its outcome reaching the log is not discussed.** The
  no-double-billing statement is made for *completed* calls; what happens to a model call that finished
  at the provider but whose outcome was not yet recorded is not stated.
- **Outside-in durability recovers what the harness persists.** Session files are mirrored record by
  record; the article does not say what happens to harness state kept outside those files, such as
  extension state, which is the failure class [[Harness State Authority]] documents.
- **That Claude Code and Codex "aren't safe for multi-tenant use" is asserted, not explained.** The
  isolation described is per
  session; tenant identity and authorization are not discussed, and the linked security documentation
  was not captured.
- Vendor announcement for Vercel's own open-source package and platform. Not every code sample was in
  the server-rendered page: the sample for creating a World in code is missing, and the served page
  masks the example Postgres connection string.

## Affected pages

- [[Harness State Authority]]
- [[LLM Application Resilience]]
- [[Multi-Tenant Agent Architecture]]
- [[Vercel]]

## Raw capture

- [[2026-10-19 Pranay Prakash and Eric Dodds - Making every harness durable]]

## Citations

- Raw capture: [[2026-10-19 Pranay Prakash and Eric Dodds - Making every harness durable]], re-fetched
  from the public page on 2026-10-27 at the user's request.
- Original clipping, which preserved only the demo trace's timing labels: [[Making every harness durable]].
- Canonical URL: https://vercel.com/blog/making-every-harness-durable
- Repository named in the article: https://github.com/vercel-labs/durable-harness (not inspected).

## Related pages

- [[Harness State Authority]]
- [[LLM Application Resilience]]
- [[Multi-Tenant Agent Architecture]]
- [[Coding Agent Harness]]
- [[AI Agents in Production]]
- [[Agent Observability]]
- [[Speculative Tool Execution]]
- [[djfarrelly - The Agent Loop Architecture]]
- [[Can Bölük - The Harness Playbook]]
- [[Vercel]]
- [[Inngest]]
