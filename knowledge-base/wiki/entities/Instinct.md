---
type: entity
created: 2026-11-13
updated: 2026-11-13
entity_kind: product
tags:
  - entity
  - product
  - personal-assistant
  - ai-agents
source_ids:
  - src-2026-11-10-nizzyabi-instinct-teardown
status: active
---

# Instinct

## What it is

A personal AI assistant that users reach by text message (the vault's account is iMessage), founded by
Noah Shinn and available by invite. It runs errands such as buying insurance, drafting and sending
email, booking, and shopping, and it texts users first with follow-ups and release notes. Everything
the vault knows about it comes from a third-party teardown,
[[@nizzyabi - I Reverse-Engineered Instinct - Here's the Whole Machine]], which measures one user's
thread and relays other people's inspections; Instinct "hasn't confirmed most of it".

## Why it matters here

Instinct is the vault's clearest example of an agent whose product quality is mostly **channel and
interaction engineering** around a model. The teardown measures behaviors that most agent write-ups
leave implicit: a read receipt at a median 1.1 seconds, tapbacks as a small status vocabulary,
short threaded replies, coalescing of messages that arrive together, and a chat agent that answers a
quick question while a separate task agent keeps working. Those observations feed [[Agentic Loop]].

It also shows two product rules that recur in [[AI Agents in Production]]: anything that spends money
or speaks for the user is shown as a draft or price before acting, and checkout is treated as one more
thing to verify, with sent emails checked afterwards. Its memory, as relayed, is Markdown files in a
git repository linked with wiki-links rather than a vector store — a consumer-scale relative of the
[[Persistent Wiki]] pattern recorded in [[Agent Memory]].

Its failures are as instructive. A voice memo it reported as sent never arrived, because it knew what
it asked the messaging channel to do but not what the channel did; a request not to keep a project in
memory was not honored as deletion. Both bear on [[Tool Use and Function Calling]] and on whether an
assistant's own action record can be trusted.

## Notes

- Internals relayed in the teardown: memory in Markdown and git with an approximately 13k-token
  per-turn profile (Dhravya Shah), and an [[E2B]] sandbox on Firecracker that is regularly discarded
  (Rohan Adwankar).
- The proactive layer reportedly costs far more tokens than chat, by Shinn's account as relayed.
- The teardown's author builds a competing platform (Keiki), so the account is both independent of
  Instinct and commercially interested.

## Related pages

- [[@nizzyabi - I Reverse-Engineered Instinct - Here's the Whole Machine]]
- [[Agentic Loop]]
- [[Agent Memory]]
- [[AI Agents in Production]]
- [[Tool Use and Function Calling]]
- [[Persistent Wiki]]
- [[E2B]]
- [[Agent Observability]]
- [[Computer Use Agents]]
