---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-yc-qm-agent-harness-source-read
title: 'YC QM Agent Harness: A Source-Code Read'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/yc-qm-agent-harness-source-read
published: '2026-08-03'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# YC QM Agent Harness: A Source-Code Read

**Y Combinator open-sourced the agent harness it runs its own company on, and the interesting part is not the agent.**

QM landed on July 31 and did the numbers you would expect: 2.3M views on the announcement, 7,000+ GitHub stars in the first three days. The coverage since has mostly restated the thread. MIT license, Slack and web, YC uses it for accounting and legal and events, you can swap Pi or OpenCode or Codex or Claude Code underneath it.

All true, and none of it tells you whether to deploy the thing.

So we read the source at commit `7f2c916`. Here is the finding that reframed it for us, and it is countable rather than a matter of taste.

`src/` holds 342 TypeScript files across 50 modules. **Thirteen of them implement the harness - the part that actually talks to a model. Twenty-six implement access control, identity, auth, audit, policy, credentials, and security.** Twice as much code governs *who may see what* as drives the model.

That ratio is the product. QM is not a better agent. It is an answer to the question that stops every company-wide agent rollout: how do you give one agent to everybody without it becoming the fastest data-leak in the building?

If you are building agents for more than yourself, the six decisions below are worth your time whether or not you ever run QM.

## 1. The harness is a config field, not an architecture

The vendor-neutrality claim is real, and it is smaller than it sounds, which is a compliment.

All four runtimes ship as ordinary dependencies in `package.json`: `@anthropic-ai/claude-agent-sdk`, `@openai/codex`, `@opencode-ai/sdk`, and `@earendil-works/pi-coding-agent`. Each gets one adapter in `src/harness/` behind a shared `Harness` interface. Swapping runtime is a config write, not a migration.

What makes it usable at company scale is `resolveRuntimeChoice` in `src/harness/harness-router.ts`. Runtime selection resolves through three levels:

| Level | Who sets it | Effect |
| --- | --- | --- |
| Approved list | Org admin | The allowlist of harnesses and models that exist at all |
| Org default | Org admin | What everyone gets unless they change it |
| Scope override | A person or a room | Their own choice, inherited from org if unset |

Every level is validated back against the approved list, and an unsupported combination falls back rather than failing. The consequence worth stealing: **an admin can allow Claude Code and Codex and forbid everything else, and no individual can escape that by editing their own settings.** Most harnesses treat model choice as a user preference. Treating it as an org policy with per-scope inheritance is what makes it deployable somewhere with a compliance team.

The lesson generalizes past QM. If you are building a harness that more than one person uses, the model selector belongs in your policy layer, not your settings page. See our [six components of a production agent harness](/blog/harness-six-components) for where this sits in the wider picture.

## 2. Memory is a markdown notebook, not a vector store

The most-liked technical question under YC's announcement was whether long-term memory is "md+sqlite". Close. It is Postgres for persistence, and the memory itself is **a markdown notebook of atomic bullet facts, each stamped with a capture date** (`src/memory/notebook.ts`, `src/memory/postgres-memory-service.ts`).

There is no embedding index anywhere in the memory path.

Three strategies ship, selectable per deployment (`src/memory/strategy.ts`):

| Strategy | Behavior |
| --- | --- |
| `per-turn` (default) | Extracts facts as turns complete |
| `scratch-promote` | Buffers to a scratch area, promotes what survives |
| `agent-only` | The agent writes its own memory, no automatic extraction |

The part worth copying is consolidation. After a default of 10 new bullets accumulate below a marker, a model pass runs over the numbered notebook and returns **actions, not prose**: `UPDATE <n>`, `DELETE <n>`, `ADD:`, or exactly `NONE`. The prompt instructs it to prefer UPDATE over DELETE-plus-ADD when a fact evolved, keep every fact atomic and standalone, and delete what is stale or contradicted.

Two reasons that design is better than it looks. An action list is **reviewable and diffable** in a way a rewritten memory file is not, so you can see what your agent decided to forget. And the `<!-- consolidated: DATE -->` marker means consolidation is incremental rather than a full rewrite every time.

This is the same shape as the memory-consolidation ideas circulating from the labs, shipped in a form you can read. If memory design is your current problem, our [agent memory systems guide](/blog/agent-memory-systems-guide) covers the alternatives QM chose against.

## 3. Multiplayer means redacting the transcript, not just the room

This is the function we would point at if we could only show you one.

In a shared room, several people and one agent read the same session. Their permissions differ. So `filterTapeForAudience` in `src/harness/tape-fold.ts` filters the session tape **per audience**, checking every record against every viewer's scope entitlement.

The detail that shows someone hit this problem in production: when a viewer is not entitled to a message, a tool *result* is not simply dropped. It is substituted, so the transcript stays structurally valid, because a conversation missing the result of a tool call it can still see is a broken conversation, not a redacted one.

Anyone can put an agent in a channel. Getting the transcript to say different things to different readers, without corrupting it, is the actual engineering. If you are building anything multiplayer, read that file before you design your own.

## 4. The sandbox's real job is egress

`src/egress-authz-main.ts` is a standalone authorizing proxy, and its defenses name specific attacks.

- Requests carry **signed capability tokens**, verified per request, rather than ambient network trust. The signing path uses JWS compact serialization via `jose` alongside an HMAC-SHA256 route with constant-time comparison (`src/auth/signed-token.ts`).
- Link-local ranges are blocked: `169.254.0.0/16`, `fe80::/10`, and `fd00:ec2::254`.
- Cloud metadata hosts are blocked by name: `metadata.google.internal`, `metadata.goog`.
- Hostnames are **resolved and the resulting IP re-checked**, which is what closes DNS rebinding.
- Every decision goes to an audit sink, with a Postgres implementation included.

That metadata-endpoint block is the tell. `169.254.169.254` is how an agent that can fetch a URL turns into an agent holding your cloud credentials. It is one of the first things a security reviewer asks about and one of the last things a hobby agent project implements.

**If you run agents in a sandbox today, this is the highest-value thing on this page to copy.** Container isolation without egress control means your agent cannot write to the host but can still exfiltrate to anywhere on the internet. Related reading: [agent sandboxes and OS-level security](/blog/agent-sandbox-os-level-security).

## 5. The unit is the scope, not the user

Personal assistants scope everything to a person. QM scopes to a **scope**, which is a person *or* a room, and the same set of things hangs off both: memory, files, keychain view, permissions, crons, web apps, and a durable sandbox.

That is why `src/` has a `resolution/` module. Configuration, credentials, and context all resolve through a scope chain rather than a user lookup. Skills are scope-owned and shared by explicit grant, with admin-gated promotion to the whole org (`src/skills/`, `src/acl/`).

The practical difference: when a colleague picks up a thread in a shared room, they are talking to the same agent with the same accumulated context, not their own instance that has to be re-briefed. Sharing is the default state of a room rather than a feature bolted onto a personal assistant.

## 6. The limits are in SECURITY.md, and they are unusually honest

Most launch coverage skipped this file. It contains the two facts most likely to decide whether you can deploy QM at all.

**An org admin is a privileged content reader.** In QM's own words, an admin is "a privileged content reader, not only a policy administrator," and admin content reads are scope-authorized and audited but "require no additional user approval." Your admin can read your agent conversations. That is a defensible design for a startup and a blocker in plenty of regulated environments, and you should learn it before rollout rather than after.

**It is not a multi-tenant boundary.** The document states plainly that QM "is not a hardened public or multi-tenant service boundary" and assumes one organization of authenticated internal users. Published web apps are the one deliberate exception: a capability link authorizes reach to that app only, and does not create a principal or grant agent access.

It also states that QM does not protect a deployment from a malicious or compromised operator.

We would rather read this than another launch post. A threat model that names its own gaps is a better signal about engineering culture than any benchmark, and it is the section to hand your security reviewer first.

## What to steal if you are not deploying it

The repo is more useful as a reference implementation than as a dependency for most teams:

1. **Model choice as org policy** with per-scope inheritance and validated fallback, not as a user setting.
2. **Consolidation that emits an action list** (`UPDATE` / `DELETE` / `ADD` / `NONE`) so memory edits stay reviewable.
3. **Audience-filtered transcripts** with structural substitution instead of deletion.
4. **An egress proxy that blocks metadata IPs** and re-checks resolved addresses.
5. **A threat model that names what it does not defend against.**

## Should you deploy it?

**Reasonable yes:** you are a startup on Slack, you want one agent across functions rather than per-team bots, you can run Postgres and either Fly or AWS, and you accept beta software where admins can read content.

**Reasonable no:** you need a multi-tenant or external-user boundary, you are in a regulated environment where unapproved admin content reads are disqualifying, or you want something stable. It is version 0.1.0 and YC calls it an experiment with bugs.

**The middle path most teams should take:** read the five patterns above, take the two that fix a hole you already have, and keep watching the repo.

## Frequently Asked Questions

**What is QM?**
QM is an open-source multiplayer agent harness that Y Combinator built and uses internally across accounting, legal, events, and engineering. It was released under MIT on July 31, 2026, runs in Slack and a web UI, and gives each person and each room its own scoped memory, files, credentials, permissions, crons, web apps, and sandbox.

**Is QM free and open source?**
Yes. MIT licensed at `github.com/yc-software/qm`, self-hostable on Fly or AWS. It is version 0.1.0 and YC describes it as an early experiment.

**How does QM store long-term memory?**
As a markdown notebook of atomic bullet facts with capture dates, persisted in Postgres. There is no vector index in the memory path. A consolidation pass runs after roughly 10 new facts and returns explicit UPDATE, DELETE, and ADD actions rather than rewriting the file.

**Can QM use Claude Code, Codex, or OpenCode?**
Yes, all four including Pi. Each ships as a dependency with an adapter behind one shared interface, and runtime is chosen by config. An org admin sets which harnesses and models are approved, and individual scopes can only pick from that list.

**Is QM secure enough for company data?**
It isolates data by scope and ships a real egress proxy that blocks cloud metadata endpoints and re-checks resolved IPs. But SECURITY.md is explicit that QM is not a hardened public or multi-tenant boundary, that org admins can read content without user approval, and that it does not protect against a compromised operator. Read SECURITY.md before deploying.

**How is QM different from Claude Tag?**
Both put a persistent agent where a team already works. Claude Tag is Anthropic's hosted product in Slack. QM is self-hosted, MIT licensed, and lets you choose the model and harness underneath. See our [Claude Tag guide](/blog/what-is-claude-tag) for the hosted comparison.

**How do you deploy QM?**
It is cloud-first and targets Fly or AWS. You customize and deploy from a private fork, running `qm init` to materialize an org deployment directory under `deploy/layers/<org>/`. The repo's own instruction is that core stays byte-identical to upstream and everything organization-specific is confined to that layer, which is what makes upgrades survivable.

## Start here

If QM's design is interesting but deploying it is not your next move, the transferable version of these ideas is in [the 6 components of a production agent harness](/blog/harness-six-components), and the patterns behind them in [harness engineering for production agents](/blog/harness-engineering-agent-production-guide).

The AI Builder Club [skills repo](https://github.com/AI-Builder-Club/skills) is where we ship the setup pieces as installable skills, including sandbox and verifier setup.

This guide is written from hands-on testing, then cross-checked against primary sources - official documentation and first-party announcements. Field results and opinions are labeled as such. See our [editorial standards](/about).
