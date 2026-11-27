---
type: concept
created: 2026-08-24
updated: 2026-11-27
tags: [concept, ai-agents, plugins, interoperability]
source_ids:
  - src-2026-08-17-google-cloud-agent-plugins
  - src-2026-08-20-jeremy-morrell-extensible-software
  - src-2026-08-28-philipp-schmid-recursive-self-improvement
  - src-2026-09-02-can-boluk-harness-playbook
  - src-2026-10-12-rastogi-agent-engineer
  - src-2026-11-23-bas-nijholt-orchestrating-orchestrators
  - src-2026-11-25-frank-rousseau-agentic-coding-open-source
  - src-2026-11-24-uber-agent-skill-evals
status: active
---

# Agent Plugin Architecture

## Definition

Agent plugin architecture is a packaging and isolation pattern for distributing agent instructions, executable tools, assets, and client configuration as one installable unit while retaining explicit component boundaries.

## Current synthesis

[[Google Cloud - Agent Plugins Are the Future of Agent Skills]] proposes a portable directory containing:

- a manifest for identity, discovery, and compatibility;
- one or more [[Agent Skill|skills]] expressed as `SKILL.md` procedures;
- [[Model Context Protocol|MCP]] server definitions for executable tools;
- read-only packaged assets and client-managed persistent data;
- optional configuration for hosts that have not standardized their extension points.

This resolves a layer mismatch: skills describe how to work, while MCP exposes what can be executed. A plugin transports both. Robust implementations should validate the manifest strictly but isolate failures so one invalid server does not erase valid skills.

[[Jeremy Morrell - Extensible Software in the Age of LLMs]] generalizes the same idea to generated application extensions. A trusted host owns identity, storage, routing, and privileged capabilities; generated workers run behind a narrow RPC boundary. The common principle is capability-oriented composition under zero trust.

## Limits

Portability remains partial. Authentication, browser extensions, hooks, commands, and permission semantics still vary by client. A common folder layout does not prove behavioral compatibility or security.

## How far the plugin boundary can move

[[Philipp Schmid - Recursive Self-Improvement]] ranks three harness postures by how much of the system
is expressed as a plugin, and the ranking is effectively a spectrum from "extension points" to "there
is no core."

- **Fixed core with extension points** — Claude Code, Codex, Cursor. Skills, hooks, and plugins extend
  a core the agent cannot reach.
- **Minimal core** — Pi ships four built-in tools (`read`, `write`, `edit`, `bash`) and a system
  prompt under 1,000 tokens. Everything else is a TypeScript extension auto-discovered from
  `.pi/extensions/`, which **an agent can write, reload, and continue with mid-session**. Amp takes a
  related path by storing project plugins with the codebase.
- **Plugin kernel** — DeepSeek Harness, built on the Cordis kernel, treats models, tools, sessions,
  sandboxes, and **the control loop itself** as replaceable. Its key engineering property is that
  **plugin side effects unwind on unload**, so the runtime can swap parts of itself without dying.

That unload-safety property is what makes the extreme position viable at all: hot-swapping the control
loop is only survivable if partially-applied changes can be reversed cleanly.

The cost is symmetric with the benefit. An agent that can author its own extensions can build
capabilities its developers did not predict — and can break compatibility or weaken a permission
boundary, with effects that persist past the session that introduced them. This is the same tension
[[Harness Optimization]] records between search-space size and safety.

## The state contract is where extension APIs fail

[[Can Bölük - The Harness Playbook]] provides the sharpest available evidence that extension APIs fail at the
**state contract** rather than at the capability surface. An audit of **78 official Pi extension examples** found
60 stateless, and among the 17 that carried state, **only two were correct**. These are maintainer-written
reference examples — the material other authors copy.

The failures are all one failure: state stored where the harness's durable operations cannot see it. A git
checkpoint in a transient map, cleared before `/fork` can use it. A turn counter in a closure that reports 4
after rewinding to turn 1 and 0 after resume. A dynamically registered tool that survives rewind but disappears
after resume. A "last message" bookmark that means last *in file order*, so it can point at an abandoned branch.

The conclusion drawn is that this distribution of bugs is not a documentation problem:
*"documentation would not repair this distribution of bugs. The engine needs one place where state can exist."*
That is the argument of [[Harness State Authority]], and the property it buys extension authors is precise —
**adding a stateful feature never adds a call site to rewind, fork, resume, or replication.**

A second failure appears one level up. Two popular workflow extensions for the same harness collide with
"Another workflow is active" — despite the harness having **no workflow API**. Both ship a private mutex, and
both were written by the same author, so the coordination only holds inside one author's suite. The
generalisable point: **a missing abstraction becomes visible the moment independently written extensions meet**,
and until then each author reinvents it privately and incompatibly.

## Packaging procedures, workers, and hooks does not isolate their effects

[[Sarthak Rastogi - Make Your Coding Assistant a 10x AI Engineer]] describes
[[agent-engineer]] as **11 skills, four subagents, and five hooks**. Skills carry procedures,
workers isolate investigations, and hooks trigger guidance or checks. The creator-run six-task
comparison reports **53% versus 34% of requirements met**, with three runs per arm and a
blinded prewritten checklist.

This is evidence about the bundle under that setup, not an ablation proving which extension
surface helped, a 10x productivity result, or independent host-compatibility verification.
The evaluation gate blocks at most once per session and is disableable. One failed run
corrected its final reply but left a false accuracy claim in a report, exposing a boundary
between intercepting a response and governing all written artifacts.

Plugin design therefore needs separate contracts for activation, capability enforcement,
persistent state, and evaluation. Loading bodies on demand is useful context management,
not measured zero overhead or a non-bypassable security boundary.

## Building features as plugins tests the interface, and plugins move pressure onto the core

Two practitioner accounts describe plugin systems from the host's side. Both concern application
plugins for agent-era tools rather than the portable skill-and-MCP bundles defined above.

[[Bas Nijholt - I Used to Orchestrate Agents, Now I Orchestrate Orchestrators]] builds real features of
his chat client, including the pull-request panel and git worktree support, as plugins: "building real
features as plugins is how I know the plugin interface is strong enough". One plugin closes a
maintenance loop. An error notifier posts errors into a room, an agent triages each error on its own,
and a pull request is waiting when he checks in. Dogfooding tests whether the interface is expressive
enough, not whether it isolates a faulty plugin.

[[Frank Rousseau - Agentic Coding on an Open-Source Project]] reports the ecosystem effect. Kitsu's new
plugin system let studios build and share plugins, some of them built with LLMs. The drawback is that
contributors now propose changes to core components, and studios want more plugin customization, while
Kitsu's philosophy is a common interface so that users "find the same setup when moving from studio to
studio". "We haven't arbitrated on the topic yet." Cheaper extensions bring more requests to widen the
boundary, which is the question of how far the plugin boundary can move, above. Neither account
measures plugin failures or security.

## Layered plugin configuration that only adds

[[Uber Engineering - How Uber Evals 1 Million Agent Skill Invocations a Month]] describes a plugin
distributor at company scale. Uber's aifx CLI installs groups of skills as plugins into Claude Code,
Codex, OpenCode and Uber's hosted agents. It manages personas that set default skills and
configuration for engineers, data scientists and other roles. It merges configuration in six layers:
company defaults, team or program, repository, working directory, user, and a local override. "Later
layers add plugins and never remove them, so a repository can declare the plugins that everyone
working in it needs." Add-only merging makes required plugins hard to drop. It also means that a
later, more specific layer cannot remove a plugin that an earlier layer added, and the post does not
say how conflicting or unwanted plugins are handled. Uber also blocks `.mcp.json` files in skills
and plugins. See [[Agent Skill]] and [[Agent Security and Governance]].

## Related pages

- [[Sarthak Rastogi - Make Your Coding Assistant a 10x AI Engineer]]
- [[agent-engineer]]

- [[Agent Skill]]
- [[Model Context Protocol]]
- [[Tool Use and Function Calling]]
- [[Agent Security and Governance]]
- [[LLM-Native Extensible Software]]
- [[Harness Optimization]]
- [[Coding Agent Harness]]
- [[Philipp Schmid]]
- [[Philipp Schmid - Recursive Self-Improvement]]
- [[Harness State Authority]]
- [[Tool Roster Economics]]
- [[Can Bölük - The Harness Playbook]]
- [[Can Bölük]]
- [[Bas Nijholt - I Used to Orchestrate Agents, Now I Orchestrate Orchestrators]]
- [[Frank Rousseau - Agentic Coding on an Open-Source Project]]
- [[Uber Engineering - How Uber Evals 1 Million Agent Skill Invocations a Month]]
