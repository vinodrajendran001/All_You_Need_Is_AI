---
type: source-summary
created: 2026-11-06
updated: 2026-11-06
source_id: src-2026-11-04-axjns-agents-share-work
source_title: Agents Need Somewhere to Share Their Work
source_author: Unattributed in capture
source_url: https://axjns.dev/blog/synthetic-membrane
tags:
  - source/summary
  - multi-agent
  - coordination
  - shared-state
source_ids:
  - src-2026-11-04-axjns-agents-share-work
status: active
---

# Agents Need Somewhere to Share Their Work

## Summary

This blog post introduces the **synthetic membrane**, a proposed coordination layer for agent teams.
The paper version is [[axjns.dev - The Synthetic Membrane - A Coordination Layer for Multi-Agent AI Systems]].
The post starts from a gap: there is a difference between a collection of capable agents and a team
that can build on its own work. It proposes an explicit, policy-controlled boundary around shared work.
That boundary governs what an agent can publish, what another agent should receive, and what either
may do with it. The post says the implementation is "familiar infrastructure: records, queries,
subscriptions, policy checks, and task ownership". It treats the biological metaphor only as a name
for a design intention.

The post also includes a five-agent simulation and a modelled cost table. Both are presented
carefully. The author states that the numbers come from a stipulated exchange model, not measured
LLM behaviour. The post also says that "both estimates are quadratic". In other words, the shared
store changes the overhead terms, not the growth class.

## Key claims

### More agents do not make a team

- The post cites the Superminds Test of MoltBook, a platform hosting **more than two million
  agents**. That study found weak joint reasoning, limited synthesis and shallow interaction.
- The post immediately narrows the result. It concerns one agent society and its tests. It "does
  not mean two million agents were assembled into one controlled team, or that all multi-agent
  systems fail".
- The open problem is what infrastructure helps capable individuals become collectively capable.

### Three central responsibilities

- **Selective exchange.** Findings are published under a visibility policy. Peers discover them or
  subscribe within their permissions. Access control decides what a peer may receive. Relevance and
  context budgets decide what is useful to deliver now. "A model's confidence in a peer cannot
  override those permissions."
- **Persistent shared state.** Evidence, interpretations and actions have stable identities.
  - A summary points back to its source.
  - A retracted claim stays identifiable as retracted.
  - A replacement agent reads the current view and recent changes, not the whole conversation.
- **Explicit coordination.** Agents discover work, claim tasks, propose actions and transfer
  responsibility. An exclusive claim needs enforcement at execution time. "Shared memory on its own
  does not provide that guarantee."
- The full proposal has **six** conceptual responsibilities, with observability throughout:
  - governance;
  - discovery;
  - access;
  - shared state;
  - coordination;
  - cross-cutting defence.

  The post says these "need not become six services".

### The blackboard precedent should be allowed to win

- The closest relative is the blackboard architecture, studied for LLMs by Han and Zhang and by
  Salemi and colleagues. Those results "make shared work worth testing, without establishing that my
  particular combination is better".
- The proposed value lies in connecting a shared workspace to permissions, provenance and action
  ownership across runtimes. "None of those ideas is individually new." If an existing blackboard or
  persistent workflow can do the same more simply, it "should win the comparison".
- The membrane is meant to compose with protocols: MCP can expose its tools and resources, and A2A
  can carry task interactions. What changes is that the state of the work stays addressable after a
  message has been delivered.

### Reading still costs quadratically

- If N agents each contribute F facts and every agent reads every fact, total delivered information
  grows as **O(N²F)**. A shared store can remove repeated publication, but it cannot make reading free.
- The table follows a baseline of **1,240N(N−1)** token-equivalents and a membrane estimate of
  **300N² + 540N**, both for five facts per agent. The stipulated costs are **90** tokens per
  envelope, **60** per fact and **8** per acknowledgement.
- In the three-agent case, messages fall from **60 to 18 (70.0%)**. Token-equivalents fall from
  **7,440 to 4,320 (41.9%)**, and consensus steps from **6 to 2 (66.7%)**.
- The modelled reduction grows with team size:

  | Agents | Reduction |
  | --- | --- |
  | 5 | **58.9%** |
  | 8 | **66.1%** |
  | 12 | **69.6%** |
  | 20 | **72.2%** |

- The post says these figures are "not measurements of an LLM team's accuracy, latency, or API
  bill". Real savings would have to come from three places:
  - delivering fewer irrelevant facts;
  - reusing useful work;
  - avoiding retries.

  Those savings must be net of indexing, summarisation, gating and any missed evidence.

### A recorded demonstration of mechanics

- The five-agent run (orchestrator, researcher, writer, editor, reviewer) exercises several
  mechanics:
  - registration;
  - private versus public exposure;
  - trust-gated reads;
  - retraction of a superseded draft;
  - a "swarm" that activates at a threshold of **2** members;
  - a broadcast.
- The run reports **32 events** in **22ms wall-clock**, **8** entries, **7** trust edges and **4**
  subscriptions. The post calls its trust thresholds "simplified rules, not a validated model of
  identity or permission".
- The intended integration setting is Sympozium. The next step is a comparison with a single agent,
  a persistent orchestrator and a conventional blackboard under matched budgets.

## Why it matters

- [[Multi-Agent Coordination]] gains a position that locates team failure in missing shared work
  products, not in too few agents. That complements the vault's evidence that teams mostly route
  through a lead.
- [[Agent Memory]] and [[Persistent Wiki]] get a shared-memory version of rules the vault already
  follows: summaries point back to sources, and retractions stay visible.
- [[Agent Delegation]] gets a precise warning: shared memory does not enforce exclusive ownership of
  an action.
- [[Model Context Protocol]] is cast as an interface onto the coordination state, not a replacement
  for it.

## Tensions / open questions

- This is a first-party design proposal with no measured task outcomes. The author says, "I do not
  yet have evidence that it delivers all three" of its operational goals.
- The cost model is stipulated, so the headline reductions follow from its assumptions. Because both
  curves are quadratic, a larger N widens the modelled gap without demonstrating any real saving.
- The demo gates reads on trust scores. Reviewer access, for example, is denied at
  "trust=0.00 < 0.50". The post and the paper both say model confidence or trust cannot grant
  permissions, and the demo's rule is labelled simplified. The prototype's access mechanism is
  therefore not the one the proposal argues for.
- The demo output has small unexplained discrepancies:
  - six `set_trust` calls appear, but the final state reports **7** trust edges;
  - four subscriptions are counted, but no subscription call is shown;
  - the final store lists no `drafts.*` keys, although only `drafts.intro` was retracted.
- The Superminds Test result is summarized from a linked paper that was not captured here.

## Affected pages

- [[Multi-Agent Coordination]]
- [[Agent Memory]]
- [[Persistent Wiki]]
- [[Agent Delegation]]
- [[Model Context Protocol]]

## Raw capture

- [[knowledge-base/raw/sources/Agents Need Somewhere to Share Their Work]]

## Citations

- Canonical URL: https://axjns.dev/blog/synthetic-membrane
- Site: axjns.dev. The capture names no author and gives no publication date. The page links the
  GitHub repositories `sympozium-ai/sympozium` and `AlexsJones/research`. The linked paper credits
  Alex Jones, but this post carries no byline, so none is assigned here.
- Captured: 2026-11-04.

## Related pages

- [[axjns.dev - The Synthetic Membrane - A Coordination Layer for Multi-Agent AI Systems]]
- [[axjns.dev - The Sticky-Note Problem]]
- [[axjns.dev - The Agent Environment Should Be a Lease]]
- [[axjns.dev - Testing Celln's Boundary]]
- [[axjns.dev - Post-Kubernetes Infrastructure for GenAI Workloads]]
- [[Multi-Agent Coordination]]
- [[Agent Memory]]
- [[Persistent Wiki]]
- [[Agent Delegation]]
- [[Model Context Protocol]]
- [[Harness State Authority]]
- [[Celln]]
- [[Cohere - Scaling Agent Teams - Reach the Frontier at 30% of the Cost]]
