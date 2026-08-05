---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-graph-engineering-peter-steinberger
title: Peter Steinberger's Loops or Graphs Tweet (2026)
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/graph-engineering-peter-steinberger
published: '2026-07-28'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Peter Steinberger's Loops or Graphs Tweet (2026)

**On July 18, 2026, Peter Steinberger posted one question to X: *"Are we still talking loops or did we shift to graphs yet?"* The post did not coin "graph engineering." The phrase appears in a 2024 post and again in a July 11, 2026 post. What Steinberger's question did was amplify it to a much larger audience. During the first four days after the post, the phrase spread through replies and X Articles. LangChain also published an official response.**

If you searched the exact sentence, the short answer is that the post is real and the wording above is exact. This page tracks the July 2026 wave around it, not the origin of graph-shaped orchestration or the phrase itself.

---

## What Did Peter Steinberger Actually Say?

The whole post is twelve words:

> Are we still talking loops or did we shift to graphs yet?

Steinberger posted it at [00:34:54 UTC on July 18, 2026](https://x.com/steipete/status/2078277297791189132). The post contains neither the phrase "graph engineering" nor a claim about a new technique.

It reads as a joke about vocabulary churn. That is an interpretation of the wording, especially the word "yet," rather than a statement of Steinberger's intent. The source does not say what he expected the audience to do with it.

## The Phrase Existed Before the Tweet

The clearest earlier use in the sources is from [Itamar Friedman on February 29, 2024](https://x.com/itamar_mar/status/1763168555539812407), in a reply to LangChain:

> When building real world AI empowered systems, we see a shift from prompt engineering to flow (/graph) engineering.

One week before Steinberger's post, [Mike (@michaelmasson55) posted this ladder](https://x.com/michaelmasson55/status/2075913998449701170):

> prompt engineering
>
> context engineering
>
> harness engineering
>
> loop engineering
>
> next is: graph engineering

Those posts rule out an origin story centered on July 18. LangChain's own retrospective makes the narrower claim: the July discussion was [kicked off by Steinberger's tweet](https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph). That describes the start of a viral wave around an existing phrase.

The same distinction matters for "loop engineering." [Franziska Hinkelmann used and defined "Loop Engineering" on March 8, 2026](https://x.com/fhinkel/status/2030606162719109491). Addy Osmani later wrote the widely shared June article that organized the practice into a system and parts list. His article helped popularize and structure the term, but the term did not come from that article.

## Who Posted It?

On his own About page, Steinberger says he [made OpenClaw, joined OpenAI in February 2026, and previously bootstrapped PSPDFKit](https://steipete.me/about). Those facts establish who posted the question. They do not establish why it spread, what he intended, or which tools his audience had installed.

The evidence for the wave is in the dated responses themselves.

## What Happened in the First Four Days After

### Before July 18

Friedman's February 2024 post and Mike's July 11, 2026 post show that "graph engineering" was already in use. They belong at the start of this timeline because they separate earlier usage from Steinberger's later amplification.

### Day 0, July 18

Steinberger posted at 00:34:54 UTC.

[Shubham Saboo](https://x.com/Saboo_Shubham_/status/2078301249376825397) followed at 02:10:05 UTC with this quote-post:

> Loops made Agent behavior programmable. Graphs make agent orgs programmable.

[Hamel Husain](https://x.com/HamelHusain/status/2078346425621237935) published the X Article *"Loop Engineering Is Dead. Enter Graph Engineering"* at 05:09:36 UTC.

Ten minutes later, [Yohei Nakajima](https://x.com/yoheinakajima/status/2078348875656790230) quote-posted:

> loops go oops
>
> use graphs to laugh

[Carlos E. Perez's](https://x.com/IntuitMachine/status/2078419526354378975) *"From Loop Engineering to Graph Engineering?"* arrived at 10:00:04 UTC. It was a same-day long-form response, nearly five hours after Husain's article.

### Day 1, July 19

[Dale Everett](https://x.com/daleverett/article/2078969402046009374) published *"Loops are just shitty graphs."* at 22:25:05 UTC. His argument was that a loop is already a simple graph, which placed the July debate over old architectural ground.

### Day 2, July 20

[Harrison Chase](https://x.com/hwchase17/status/2079219804951683380), a LangChain cofounder from the team behind LangGraph, wrote at 15:00:06 UTC:

> So i didn’t really know what graph engineering is, and i still don’t really… but it’s basically just langgraph?

The team-level attribution matters. [LangChain's official About page](https://www.langchain.com/about) says the company launched LangGraph; it does not credit Chase as its sole creator.

### Day 3, July 21

[Codila published a freely readable X Article](https://x.com/0xCodila/status/2079597821511020996) at 16:02:12 UTC with "full 5-step course" in its title. The source supports one course-styled article. It does not support the earlier claim that multiple paid courses had appeared.

### Day 4, July 22

[Shann Holmberg published "graph engineering explained (marketing edition)"](https://x.com/shannholmberg/status/2079896903186260259) at 11:50:38 UTC.

Across the first four days, the record shows a fast sequence of posts around Steinberger's question. It does not show that the question originated the phrase.

## Did Anything About Building Agents Change?

None of the cited July posts announced a new graph-orchestration capability. LangGraph, AutoGen GraphFlow, and Google ADK already supported graph-shaped orchestration. LangChain's retrospective says it had been building agents as graphs for years.

What changed in July was the phrase's reach. More people used "graph engineering" to discuss explicit nodes, routes, shared state, and control flow around agents. That wider circulation can make an existing design pattern easier to discuss without turning the phrase into a new capability.

The practical decision still depends on the work. Use a loop when one agent can pursue one objective and check its own progress against a clear verifier. Consider a graph when the job needs explicit branching, state shared between specialized steps, or controlled handoffs. The detailed mechanics belong in the [graph engineering guide](/blog/graph-engineering-guide-2026), not in an origin story about one tweet.

## What Should You Do About the July Wave?

1. **Do not restructure a working system because the vocabulary moved.** A new burst of discussion does not make a graph necessary.
2. **Learn the architecture before you need it.** The [graph engineering guide](/blog/graph-engineering-guide-2026) covers nodes, edges, and shared state.
3. **Use a concrete trigger.** Move beyond one loop when the work needs branching or a handoff that must preserve state.
4. **Start with the smallest implementation.** [Graph Engineering with Claude Code](/blog/graph-engineering-with-claude-code) shows how subagents can act as nodes without adding a new framework.

---

## Related Content

- **[Graph Engineering: What Happens When Your Agent Outgrows the Loop](/blog/graph-engineering-guide-2026)** - the pillar guide to nodes, edges, shared state, and frameworks.
- **[Graph Engineering vs Loop Engineering](/blog/graph-engineering-vs-loop-engineering)** - the architectural differences behind the July vocabulary.
- **[Is Graph Engineering Just LangGraph?](/blog/is-graph-engineering-just-langgraph)** - a framework-by-framework answer to Harrison Chase's question.
- **[Graph or Loop: When to Use Which](/blog/agent-graph-vs-loop-when-to-use)** - a decision guide for choosing the smaller shape that fits.
- **[Loop Engineering Guide](/blog/loop-engineering-guide-2026)** - how to build and verify a single agent loop.

## Start Here

If you came for the July 18 post, the historical answer is now clear: Steinberger amplified "graph engineering"; he did not originate it.

Read the [graph engineering guide](/blog/graph-engineering-guide-2026) for the mechanics, or [join AI Builder Club](/pricing) to build one with other practitioners.

Jason settled the practical question in our August 2 workshop by checking one of Steinberger's more recent posts: what he was showing is a control graph for shipping an engineering task. [Watch the session](/courses/live-ai-workshops?utm_source=blog&utm_medium=article&utm_campaign=graph-engineering-peter-steinberger).

On July 18, 2026, he posted one question to X: 'Are we still talking loops or did we shift to graphs yet?' That is the entire post. It did not include the phrase 'graph engineering,' a framework, or an announcement.

No, and he did not claim to. Itamar Friedman used 'flow (/graph) engineering' in February 2024, and Mike (@michaelmasson55) posted a ladder ending in 'graph engineering' on July 11, 2026. Steinberger's July 18 question amplified the phrase and kicked off that weekend's wave.

Steinberger says he made OpenClaw, joined OpenAI in February 2026, and previously bootstrapped PSPDFKit. Those facts come from his own About page. This article does not infer that his biography caused the post to spread.

None of the cited posts announced a new graph-orchestration capability. LangGraph, AutoGen GraphFlow, and Google ADK already supported graph-shaped orchestration. The July discussion gave an existing phrase wider circulation.

Harrison Chase, a LangChain cofounder from the team behind LangGraph, wrote: 'So i didn’t really know what graph engineering is, and i still don’t really… but it’s basically just langgraph?' LangGraph is one established implementation of the pattern, not proof that the phrase began in July 2026.

This is a sourcing piece about Peter Steinberger's July 2026 post and the wave it amplified. Every quoted post is tied to a dated primary source. Earlier uses from 2024 and July 11, 2026 are included to separate the phrase's history from the July wave. The timeline covers the first four days after Steinberger's July 18 post. Engagement is described qualitatively because X counts move after capture. See our [editorial standards](/about).
