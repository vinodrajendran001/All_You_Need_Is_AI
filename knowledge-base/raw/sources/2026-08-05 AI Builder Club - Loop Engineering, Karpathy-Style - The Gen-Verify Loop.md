---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-loop-engineering-karpathy
title: 'Loop Engineering, Karpathy-Style: The Gen-Verify Loop'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/loop-engineering-karpathy
published: '2026-07-09'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Loop Engineering, Karpathy-Style: The Gen-Verify Loop

The phrase **"loop engineering"** is about a year old. Builders converged on it in mid-2026 to describe a shift: stop hand-writing prompts for agents, and start designing the loops that prompt them for you. But the *mechanic* underneath the phrase, the thing loop engineering actually asks you to build, is older. Andrej Karpathy has been describing it, in almost the same words, since he coined "vibe coding."

If you search for **"loop engineering karpathy"**, you're likely connecting two things you already half-connected in your head: the new loop-engineering vocabulary, and Karpathy's long-running advice about how to actually work with AI. They're the same idea. This post traces the through-line: what Karpathy actually said, why it *is* loop engineering, and how to apply "the Karpathy loop" in your own agent workflow.

For the full discipline, our [loop engineering guide](/blog/loop-engineering-guide-2026) is the pillar. This piece is the Karpathy-shaped door into it.

## What Karpathy Actually Said

Three of Karpathy's positions map directly onto loop engineering. All three are on the record.

**1. "Keep the AI on a leash."** When Karpathy popularized vibe coding, he was careful to warn against the failure mode it invites: letting the model run unchecked. His guidance, [widely reported in 2025](https://visualstudiomagazine.com/articles/2025/04/25/vibe-coding-pioneer-advises-tight-leash-to-rein-in-ai-bs.aspx), was to keep AI-generated code on a *tight leash*, making small, verifiable changes and confirming each one rather than accepting a giant diff on faith. The leash isn't distrust of the model; it's the recognition that **the human is the accountable verifier**.

**2. "Maximize the speed of the Generation-Verification loop."** In his [Software 3.0 keynote](https://www.latent.space/p/s3) at the Y Combinator AI Startup School, Karpathy named the actual unit of AI-assisted work: a loop where the AI *generates* and the human *verifies*, over and over. His prescription was blunt. The way you get faster isn't a bigger model or a cleverer prompt, it's **shrinking the time it takes to verify**. GUIs, visual diffs, fast tests, small steps: anything that lets you audit output at a glance and get back to generating.

**3. The autonomy slider.** In the same talk, Karpathy described AI tools as having an *autonomy slider*, from "suggest a completion" to "do the whole task unsupervised." His point was that you don't pin it to the right. You slide it up only as far as your ability to verify allows, and you keep the human in the loop until that changes.

Read those three back to back and the pattern is unmistakable: **a loop, a verifier, and a dial for how much you trust it to run alone.** That's the whole of loop engineering, described before the word existed.

![The Karpathy loop: a generation-verification cycle of Generate, Verify, Correct, with the note that the verifier is the leash and loop speed is the lever you control](/images/blog/karpathy-loop-diagram.png "The Karpathy loop: a generation-verification cycle of Generate, Verify, Correct, with the note that the verifier is the leash and loop speed is the lever you control")

## Why This *Is* Loop Engineering

Loop engineering takes Karpathy's intuitions and turns them into design objects you can actually build. Here's the translation, term by term.

**The leash is the verifier.** Karpathy's "keep it on a leash" is loop engineering's central claim in different words: the generator is cheap and runs endlessly, so [the verifier is the bottleneck](/blog/loop-engineering-guide-2026) that decides whether all that generation produces value. "Keeping the AI on a leash" *is* writing a verifier. You're just doing it with your eyes instead of with code. Loop engineering's move is to promote that verifier from your attention (which doesn't scale) into something explicit: a test, a schema check, an LLM-as-judge, a diff review gate. Once the check lives outside your head, the loop can run when you're not watching.

**"Speed up the loop" is the whole optimization target.** Karpathy said your throughput is set by verification speed. Loop engineering says the same thing and then asks the operational question: *what is your verifier, how long does it take, and how do you make it cheaper?* If verification is a human reading a 400-line diff, your loop is slow and you are its rate limiter. If verification is `npm test && the-typecheck-passes`, the loop can spin without you. Every technique in the discipline, from bounded retries to artifact contracts to [eval sets](/blog/how-to-evaluate-ai-agents), is in service of running the generation-verification cycle faster and more times.

**The autonomy slider is the open-loop-to-closed-loop spectrum.** This is the cleanest mapping of all. Karpathy's slider from "suggest" to "autonomous" is exactly what loop engineering calls the move from an **open loop** (a human closes every cycle) to a **closed loop** (an automated check closes it). And both frameworks agree on the safety rule: *you earn the right to slide right by strengthening the verifier first.* Push autonomy past your verifier and you don't get productivity. You get an agent that [burns budget producing confident garbage](/blog/ai-agent-reliability-cost-control).

![The autonomy slider from Suggest to Supervised to Unattended, each stage labeled with the verifier that unlocks it, mapping open loop to closed loop](/images/blog/karpathy-autonomy-slider-diagram.png "The autonomy slider from Suggest to Supervised to Unattended, each stage labeled with the verifier that unlocks it, mapping open loop to closed loop")

## How to Apply the Karpathy Loop

If Karpathy's advice is the *why*, here's the *how*: four moves that take you from "prompting an AI" to running a loop, using nothing but tools you already have.

**1. Make verification cheaper before you make prompts longer.** The instinct when an agent gets something wrong is to add three more sentences to the prompt. Karpathy's instinct is the opposite: shorten the loop. Before touching the prompt, ask what would let you *verify* the next output in seconds instead of minutes. A failing test that pins the requirement, a smaller task boundary, a visual diff. A tight verifier fixes more failures than a longer prompt, because it catches the model *every* cycle instead of hoping the wording holds.

**2. Put a testable target in front of the model.** Karpathy's leash tightens when the "done" condition is concrete. "Make the auth flow better" has no verifier; "the login test passes and no existing test breaks" does. A testable target is what lets the loop close without you. It's the difference between an agent you supervise and an agent that supervises itself. This is the single highest-leverage habit, and it's the spine of our [loop engineering guide](/blog/loop-engineering-guide-2026).

**3. Set the autonomy slider deliberately, per task.** Don't run everything at the same autonomy level. A refactor with full test coverage can run near-unattended; a schema migration against production data stays on "supervised." Decide the slider position *before* you start, based on how good your verifier is for *this* task, not on how much you trust the model in general.

**4. Keep yourself in the loop until the verifier earns its removal.** The graduation from open to closed loop is a promotion the verifier has to earn. Run the loop supervised until you've watched the automated check catch the failures *you* would have caught. When it's caught them a dozen times without a miss, slide the human out. That's not a leap of faith; it's the leash getting longer because you measured that it holds.

## Karpathy's Loop, In Context

Karpathy's generation-verification loop isn't a standalone idea. It sits inside the larger body of his engineering thinking, most of which is about **making the loop legible and repeatable**. His [CLAUDE.md rules](/blog/karpathy-claude-md-rules) are, functionally, a way to make the *generate* half of the loop more predictable so the *verify* half has less to catch. His [Software 3.0 framing](/blog/karpathy-software-3-0), English as the new programming language with the human as reviewer, is the same loop viewed from altitude. We collect the full set in the [Karpathy AI engineering playbook](/blog/karpathy-ai-engineering-playbook).

It also sets the ceiling on what one loop can do. Karpathy's own framing of adding more agents to the mix is where the single generation-verification cycle stops being the unit and a set of connected ones takes over, which is what [graph engineering](/blog/graph-engineering-guide-2026) names: specialized nodes, edges that route between them, and state that survives the handoff. The verifier discipline doesn't change, it just gets applied per node.

The reason the loop-engineering vocabulary caught on where Karpathy's phrasings didn't quite is that it's *operational*. "Keep the AI on a leash" is a great instinct but not a spec. "Write a verifier, bound the retries, put it on a trigger, and slide autonomy up as the verifier proves out" is something you can build on a Tuesday. Loop engineering is Karpathy's advice with the checklist attached.

## FAQ

**Did Andrej Karpathy invent loop engineering?**
No. Karpathy never used the phrase; the term was coined by the builder community in mid-2026. But the mechanic it describes, keeping AI on a leash and maximizing the speed of the generation-verification loop, is one Karpathy has advocated for years. Loop engineering gave his instinct a name, a vocabulary, and a build order.

**What is Karpathy's generation-verification loop?**
The cycle where the AI generates work and a human or automated check verifies it before the next step: prompt, it writes, you check, you re-prompt. His core claim is that throughput is set by how fast you can run that loop, so the leverage is in speeding up verification, not lengthening prompts.

**What is the autonomy slider?**
Karpathy's metaphor for how much independence you give the AI, from "suggest only" to "fully autonomous." In loop-engineering terms it's the open-loop-to-closed-loop spectrum: you earn the right to slide toward autonomy by making your verifier cheap, fast, and trustworthy first.

## Related Content

- **[Loop Engineering: Stop Writing Prompts, Start Writing Verifiers](/blog/loop-engineering-guide-2026)**: The full discipline: the verifier as bottleneck, open vs closed loops, and the starting checklist.
- **[Loop Engineering vs Harness Engineering](/blog/loop-engineering-vs-harness-engineering)**: The loop is the choreography; the harness is the stage. Which to build first.
- **[Karpathy's AI Engineering Playbook](/blog/karpathy-ai-engineering-playbook)**: Every Karpathy framework in one place, from CLAUDE.md to Software 3.0.
- **[Graph Engineering: The 2026 Guide](/blog/graph-engineering-guide-2026)** - What happens to the loop when one agent isn't the unit any more: nodes, edges, and shared state.
- **[How to Evaluate AI Agents](/blog/how-to-evaluate-ai-agents)**: Turning "keep it on a leash" into real verifiers: generator-evaluator, eval sets, LLM-as-judge.
- **[AI Agent Reliability and Cost Control](/blog/ai-agent-reliability-cost-control)**: What happens when you push the autonomy slider past your verifier, and the levers that fix it.

---

## Start Here

Take the last thing you vibe-coded and ask Karpathy's question: *how would I verify that without reading every line?* Write that check, whether a test, a schema, or a diff gate, and run the task again behind it. That single check is your first verifier, and it's the beginning of a loop.

Want to build the whole thing end to end? The [**Loop Engineering course**](/courses/loop-engineering) walks you through it layer by layer: feedback gates, a sandbox that bounds the blast radius, the unattended loop that runs while you're away, and a scheduled automation ladder. By the end you have a loop that ships a PR behind quality gates without you watching. It's Karpathy's generation-verification loop, engineered to close by itself.

No. Karpathy never used the phrase 'loop engineering'; that term was coined by the builder community in mid-2026. But the mechanic the term describes is one Karpathy has advocated for years: keep AI on a tight leash and maximize the speed of the human-AI generation-verification loop. Loop engineering is the discipline that gave his advice a name and a checklist.

It's the cycle where the AI generates work and a human (or an automated check) verifies it before the next step: prompt, it writes, you check, you re-prompt. Karpathy's core claim is that your throughput is set by how fast you can run that loop, so the highest-leverage work is speeding up verification, not writing longer prompts.

Karpathy's metaphor for how much independence you give the AI, from 'suggest only' to 'fully autonomous'. In loop-engineering terms it's the open-loop-to-closed-loop spectrum: you only earn the right to slide toward autonomy by making your verifier cheap, fast, and trustworthy enough to run without you.

The Karpathy positions quoted here are drawn from primary talks and reporting: his 'Software Is Changing (Again)' / Software 3.0 keynote at the Y Combinator AI Startup School (June 2025, writeup linked below), and contemporaneous reporting of his 'keep AI on a leash' vibe-coding guidance. The mapping from those positions to the loop-engineering vocabulary (verifier, open vs closed loop, bounded retry) is our synthesis, cross-checked against our own loop-engineering guide. The application steps are one builder's workflow from running agent loops in Claude Code in mid-2026, not benchmarks. See our [editorial standards](/about).
