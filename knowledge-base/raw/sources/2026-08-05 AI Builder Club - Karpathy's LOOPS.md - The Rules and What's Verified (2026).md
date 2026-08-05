---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-loops-md-karpathy
title: 'Karpathy''s LOOPS.md: The Rules and What''s Verified (2026)'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/loops-md-karpathy
published: '2026-07-17'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Karpathy's LOOPS.md: The Rules and What's Verified (2026)

If you searched **"loops.md karpathy,"** you probably saw a screenshot of a file called *LOOPS.md: Field Notes on Agents That Run for Days* and wanted the real thing to drop into your setup. Here's the honest situation, up front: **the advice in that file is genuinely good, but its attribution to Andrej Karpathy is, as of this writing, unverified.** Those are two separate facts, and this page keeps them separate. First what the file says and why it's worth your time, then exactly what we could and couldn't confirm about who wrote it.

## What the LOOPS.md file says

The document circulating as LOOPS.md is short: about nine rules, usually grouped into four moves, all pointed at one problem: **an agent that has to run for hours or days without a human in the chair.** Its thesis is that most agent systems die from a weak *harness*, not a weak model. The model can generate; what it can't reliably do on its own is decide when to stop, when to restart, and where to put its results. That work belongs to the loop around it.

Here are the rules, as they're consistently rendered across the copies sharing them:

![The nine rules of the circulating LOOPS.md file, grouped into four moves. Split the roles (write a loop not a prompt, separate planner/generator/evaluator, negotiate the contract first),, keep state outside the model (write to disk not context, let the loop restart), quality as a contract (grade the subjective, read the trace), and shrink the harness (delete the harness, the bottleneck always moves). A note adds that every rule is textbook loop engineering](/images/blog/loops-md-rules-diagram.png "The nine rules of the circulating LOOPS.md file, grouped into four moves. Split the roles (write a loop not a prompt, separate planner/generator/evaluator, negotiate the contract first),, keep state outside the model (write to disk not context, let the loop restart), quality as a contract (grade the subjective, read the trace), and shrink the harness (delete the harness, the bottleneck always moves). A note adds that every rule is textbook loop engineering")

Read them and you'll notice something: none of this is exotic. It's the same discipline serious builders have been converging on all year. Which is exactly why it's worth keeping, and also why the byline matters less than it looks.

## Why the rules are good: they're just loop engineering

Strip the file's framing and what's left is a clean statement of [loop engineering](/blog/loop-engineering-guide-2026), the shift from writing prompts to designing the loop the model runs inside. Every rule maps onto a principle the discipline already names:

- **"Write a loop, not a prompt"** and **"negotiate the contract first"** are the whole premise of loop engineering: the unit of work is the loop, and the loop closes on a *contract*, a checkable definition of done. That contract is the verifier, and in loop engineering [the verifier is the bottleneck](/blog/loop-engineering-guide-2026). The file is restating the core move.
- **"Separate the roles"**: planner, generator, evaluator as distinct contexts, is the [generator-verifier pattern](/blog/loop-engineering-karpathy): the thing that produces work can't be the thing that grades it, or the loop has no honest stop condition. It's also why a goal-based loop uses a *fresh* model to check completion, not the one doing the work, as we cover in [the four types of agentic loops](/blog/types-of-agentic-loops).
- **"Write to disk, not to context"** and **"let the loop restart"** are harness rules. State that has to survive a long run belongs in durable files, not a degrading context window. That is the artifact-and-log architecture from [harness engineering](/blog/harness-six-components). A loop that can rebuild cleanly from disk is one you can actually leave alone.
- **"Grade the subjective"** and **"read the trace"** are [how you evaluate an agent](/blog/how-to-evaluate-ai-agents): turn taste into an explicit rubric, and debug from the raw transcript instead of a summary. No rubric, no trace, no trustworthy verifier, and no closed loop.
- **"Delete the harness"** and **"the bottleneck always moves"** are the maintenance posture: as models get stronger, scaffolding that was load-bearing becomes dead weight, and the constraint you just fixed is replaced by the next one. Loop engineering is a moving target on purpose.

That's the useful takeaway, and it stands on its own: **the LOOPS.md rules are a good field guide because they describe real loop engineering, not because of whose name is on them.** Which brings us to the name.

## Did Karpathy actually write it? What we checked

The file spread with a specific hook: that Andrej Karpathy, who *did* [join Anthropic in May 2026](https://techcrunch.com/2026/05/19/openai-co-founder-andrej-karpathy-joins-anthropics-pre-training-team/), keeps this as his personal playbook for long-running agents. That real, verifiable career move is what makes the story feel plausible. So we went looking for the file at a primary source. Here is what we searched, on 2026-07-17, and what we found:

![A provenance check for LOOPS.md, as of July 17 2026. karpathy.ai has no such file, no github.com/karpathy repository contains a LOOPS.md, his public gists don't either, secondary blogs and gists cite it with no link to a primary source, the claim originates in a secondhand post saying a friend on his team shared the file, and Karpathy himself has never posted about or confirmed it; verdict: unverified, not disproven, and the page will be updated if he publishes or confirms one](/images/blog/loops-md-attribution-diagram.png "A provenance check for LOOPS.md, as of July 17 2026. karpathy.ai has no such file, no github.com/karpathy repository contains a LOOPS.md, his public gists don't either, secondary blogs and gists cite it with no link to a primary source, the claim originates in a secondhand post saying a friend on his team shared the file, and Karpathy himself has never posted about or confirmed it; verdict: unverified, not disproven, and the page will be updated if he publishes or confirms one")

Every place a genuine Karpathy artifact would live, meaning his site, his repositories and his gists, has no LOOPS.md. Every secondary copy that shares the rules cites them without a link back to him; the most formal one lists it in a reference section as *"Karpathy, A. (2026). LOOPS.md…"* with no URL at all. And the origin of the whole thing is a secondhand post of a familiar shape: *a friend on his team showed me the file he actually uses.* That construction is unverifiable by design. There's no artifact to check, only a claim about a private one.

A few things this page is deliberately **not** saying. It's not claiming the file was invented, and it's not a knock on Karpathy. He's the person being *misattributed to* here, not the subject of a complaint. He may well keep a working file like this; plenty of good engineers do. The point is narrower and it's about sourcing: **an unverifiable private file can't be cited as a public source.** Until there's a primary link, the rules are good advice with an uncertain byline, so we publish them as good advice, not as his.

And we'll keep this honest going forward: **if Karpathy publishes a LOOPS.md or confirms one, we'll update this page and say so.** That's the line that makes this a note you can trust rather than a take.

## What to actually do with LOOPS.md

Use the rules, just use them on their merits. The reason this matters practically: builders keep waiting for the *canonical* file from the *famous* engineer, as if the authority is the value. It isn't. The value is the discipline, and the discipline is checkable against your own runs. Take any long-running agent you have and ask the LOOPS.md questions directly:

1. **Is there a contract?** Can you state, in one line a fresh model could check, what "done" means for this loop? If not, that's your first rule to apply, before any of the others.
2. **Are the roles separate?** Is anything grading its own output? If the generator is also the judge, your stop condition is a vibe, not a verifier.
3. **Does state live on disk?** If a run dies at hour six, can the loop resume from files, or does it lose everything in the context window?
4. **Can you read the trace?** When it goes wrong, do you debug from the raw transcript, or guess and re-run?

If you get stuck on the first two, meaning you know a loop needs a contract and a stop condition but you can't actually write them down, our free [AI Agent Loop Builder](/tools/agent-loop-builder) takes your task type and generates a verifier checklist, a concrete stop condition, and round and budget caps to start from. That's how the answer to question two stops being a vibe and starts being a verifier.

Those four questions are the file's real content, and they don't need a byline to be worth answering.

## FAQ

**Did Andrej Karpathy write LOOPS.md?**
As of July 17, 2026, there's no primary source for it. We found no LOOPS.md at karpathy.ai, in any github.com/karpathy repository, or in his public gists, and he hasn't posted about or confirmed one. Every secondary copy cites it without a link, and the claim traces to a secondhand post. The honest status is *unverified*, not disproven. He may keep a private file like this; an unverifiable private file just can't be treated as a public source.

**What is LOOPS.md?**
A document circulating as *"LOOPS.md: Field Notes on Agents That Run for Days (v060726),"* attributed to Karpathy. It's about nine rules for building agents that run unattended for hours or days, arguing that most agent systems fail on a weak harness, not a weak model, so the discipline belongs in the loop around the model, not in one clever prompt.

**What are the nine rules in LOOPS.md?**
Write a loop, not a prompt; separate the planner, generator, and evaluator roles; negotiate the contract for "done" first; write state to disk, not to context; let the loop restart cleanly; grade subjective quality with an explicit rubric; debug by reading the raw trace; delete harness scaffolding as models improve; and remember the bottleneck always moves. It's textbook [loop engineering](/blog/loop-engineering-guide-2026).

**Is LOOPS.md real, and should I use its rules?**
The advice is real and worth using. It restates durable loop-engineering practice that predates the file. What's unverified is the byline. Use the rules on their merits, not because a famous name is attached.

## Related Content

- **[Loop Engineering: Stop Writing Prompts, Start Writing Verifiers](/blog/loop-engineering-guide-2026)**: The pillar the LOOPS.md rules describe: the loop as the unit of work, the verifier as the bottleneck, and the starting checklist.
- **[Loop Engineering, Karpathy-Style](/blog/loop-engineering-karpathy)**: The generation-verification loop and the autonomy slider, the discipline the file's "separate the roles" rule points at.
- **[The 4 Types of Agentic Loops](/blog/types-of-agentic-loops)**: Turn, goal, time, and proactive: the loop patterns you'd build to actually run an agent for days.
- **[How to Evaluate AI Agents](/blog/how-to-evaluate-ai-agents)**: Building the rubric and the trace the "grade the subjective" and "read the trace" rules depend on.
- **[Andrej Karpathy's AI Engineering Playbook](/blog/karpathy-ai-engineering-playbook)**: His frameworks that *are* verifiably his, in one place. The counterpart to this page.

---

## Start Here

Pick the one long-running agent you least trust to run without you, and put it through the four questions above: contract, separated roles, state on disk, a readable trace. The gap you find is the rule to apply first. If you want the whole discipline built end to end rather than reverse-engineered from a screenshot, the [**Loop Engineering course**](/courses/loop-engineering) walks you through it: the contract that defines done, the verifier that earns the right to walk away, the on-disk state and logs, and the scheduled loop that ships while you're away. That's what LOOPS.md is gesturing at, engineered into a system you can actually run, with a byline you don't have to take on faith.

As of July 17, 2026, there is no primary source for it. We could not find a LOOPS.md at karpathy.ai, in any github.com/karpathy repository, or in his public gists, and Karpathy has not posted about or confirmed one. Every secondary copy cites it without a link, and the claim traces to a secondhand social post. So the honest status is unverified - not disproven. He may keep a private file like this; an unverifiable private file simply can't be treated as a public source.

It's a document circulating online as 'LOOPS.md: Field Notes on Agents That Run for Days (v060726),' attributed to Andrej Karpathy. It's a short set of about nine rules for building agents that run for hours or days unattended - the core argument being that most agent systems fail because of a weak harness, not a weak model, so the discipline belongs in the loop around the model rather than in one clever prompt.

As rendered across the copies sharing it: (1) write a loop, not a prompt; (2) separate the planner, generator, and evaluator roles; (3) negotiate the contract - what 'done' means - first; (4) write state to disk, not to the context window; (5) let the loop restart cleanly instead of patching forward; (6) grade subjective quality with an explicit rubric; (7) debug by reading the raw trace; (8) delete harness scaffolding as models improve; (9) the bottleneck always moves, so find the next one. Whatever its origin, this is textbook loop engineering.

The advice is real and worth using - it restates durable loop-engineering practice that predates the file. What's unverified is the byline. Use the rules on their merits, not because a famous name is attached; the discipline is the same whether Karpathy wrote them or not.

This page does two things. First, it reports what the document circulating as 'LOOPS.md: Field Notes on Agents That Run for Days (v060726)' actually claims - the nine rules, as rendered consistently across the secondary copies sharing them. Second, it reports a provenance check performed on 2026-07-17: we searched karpathy.ai, github.com/karpathy repositories, and his public gists for a LOOPS.md and found none, and traced the claim's origin to a secondhand social post rather than a primary source. We do not assert the file is invented - only that its attribution to Andrej Karpathy is, as of that date, unverified. The mapping of the rules onto loop-engineering discipline is our synthesis, grounded in our own loop-engineering guide. See our [editorial standards](/about).
