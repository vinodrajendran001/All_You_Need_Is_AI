---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-karpathy-software-3-0
title: 'Karpathy''s Software 3.0: The Context Window Is Code'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/karpathy-software-3-0
published: '2026-05-27'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Karpathy's Software 3.0: The Context Window Is Code

Andrej Karpathy has a framework for what is happening to software right now — and it reframes every decision you make as an AI builder.

At Sequoia Ascent 2026, he called it **Software 3.0**. Here is what it means, why it matters, and what it changes for anyone building AI products.

---

## The three eras of software

**Software 1.0** is traditional programming. You write explicit code. Deterministic, precise, brittle to edge cases. The program is the code.

**Software 2.0** is machine learning. You create datasets and objectives; neural networks learn the program into weights. The weights are the program. Karpathy introduced this framing years ago at Tesla.

**Software 3.0** is the current moment. You program LLMs through prompts, context, tools, examples, memory, and instructions. **The context window is the program.** The LLM is the interpreter.

Karpathy's phrasing:

> "What is in the context window is your lever over the interpreter, and the interpreter is the LLM. It interprets your context and performs computation in digital information space."

The scarce resource shifted from lines of code to context design.

---

## Why this is not just "faster coding"

The most important part of the Sequoia talk is what Karpathy says Software 3.0 is **not**.

It is not a speedup of what already exists. It is a category of things that were **not possible before**.

His MenuGen example makes this concrete. He built a traditional web app: take a menu photo, OCR the dishes, generate images, render them in a UI. Vercel, auth, payments, APIs — the full stack.

Then someone showed him the Software 3.0 version: take the photo, give it to a multimodal model, ask it to overlay dish images directly onto the menu photo. One prompt. One output. **The entire app architecture disappears.**

> "All of MenuGen is spurious in that framing. It is working in the old paradigm. That app shouldn't exist."

This is the founder question Software 3.0 forces: not just "what can we do faster?" but **"what software should stop existing as software?"**

---

## The installation example that reframes everything

Karpathy gave another example: the OpenClaw installation.

Normally, installing a complex tool across many environments requires a shell script. Those scripts balloon into hundreds of conditional lines. They break on edge cases.

The Software 3.0 version: a block of text you copy-paste into your agent. The agent reads your environment, performs intelligent actions, debugs errors in the loop, adapts to your machine, and completes the setup.

> "What is the piece of text to copy-paste into your agent? That is now part of the programming paradigm."

For AI builders: your product's onboarding flow, your setup docs, your deployment process — all of these exist in the Software 1.0 world. What does the Software 3.0 version look like?

---

## What is actually new: information transformations that were impossible before

Karpathy's LLM Wiki project is the clearest example of what Software 3.0 actually enables.

Instead of using RAG to answer questions from raw documents, an agent incrementally compiles raw sources into a persistent markdown wiki: summaries, entity pages, concept pages, contradictions, cross-links, evolving synthesis.

> "No classical program could robustly maintain that kind of knowledge base across messy human documents. But an LLM can."

This is not a faster search. It is a transformation that had no prior implementation path. The information work that Software 1.0 could not do is now natural.

For builders: before you optimize existing workflows, ask what workflows become possible for the first time.

---

## Verifiability: why AI moves faster in some domains

Karpathy has a framework for understanding where AI improves fastest: **verifiability**.

Traditional software automates what you can specify. LLMs and reinforcement learning automate what you can **verify**.

If a task has an automatic success signal — tests pass or fail, programs run or crash, diffs can be inspected — models can practice it. This is why coding agents feel dramatically better than most chatbot experiences. Code gives the model feedback.

The practical implication: if you are building a product, find where your domain has verifiable structure. What can be tested, measured, scored? The AI will improve fastest there.

**Karpathy's formula:** capability spike = verifiability × training attention × data coverage × economic value.

This is also a startup wedge. Frontier labs focus on coding and math because they are verifiable and economically valuable. Many other domains have latent verifiable structure that nobody has exploited yet.

---

## Agent-native infrastructure: build for the agent, not just the human

This is the part most builders miss.

Most software is still built for humans clicking through screens. Docs say "go to this URL, click this button, open this panel." But increasingly the user is not the human directly — it is the human's agent.

Karpathy's taxonomy: **sensors and actuators**. Sensors turn world state into digital information. Actuators let agents change something. The future stack is agents using sensors and actuators on behalf of people.

**What agent-native products look like:**

- Markdown docs instead of click-through UI flows
- CLIs and APIs instead of dashboards
- MCP servers for structured data access
- Copy-pasteable agent instructions for setup
- Machine-readable schemas and structured logs
- Safe permissioning and auditable actions

For builders: every product decision has two versions — the human version and the agent version. Start asking which one you are building.

---

## The practical implication for what you build next

Karpathy's questions for founders at the end of the Sequoia talk:

1. What becomes possible when the primary user is an agent acting for a human?
2. What workflows can be rebuilt around sensors, actuators, and verifiable loops?
3. What software should disappear into direct model transformations?
4. What domains are valuable and verifiable but not yet heavily trained by frontier labs?
5. What human judgment must remain in the loop to preserve quality?

These are not rhetorical. They are a practical filter for what to build in 2026.

---

Software 3.0 is not the endpoint. Karpathy ended with an extrapolation: neural nets running virtualized on computers today; someday the neural net becomes the host process and CPUs become coprocessors. The application layer as we know it starts to dissolve.

But that is years out. Right now, the shift is real and actionable: **the context window is your program. Design it accordingly.**

Want to go deeper on building in the Software 3.0 era? [Join AI Builder Club](https://www.aibuilderclub.com/pricing?utm_source=blog&utm_medium=article&utm_campaign=software-3-0) — weekly workshops on real agentic workflows, what works, what breaks, and how to build things that last.

Software 3.0 is Karpathy's framework for the current programming paradigm where you program LLMs through prompts, context, tools, examples, memory, and instructions. The context window is the program, and the LLM is the interpreter. Unlike Software 1.0 (explicit code) or Software 2.0 (learned neural network weights), Software 3.0 uses natural language and structured context as the programming medium. He introduced this at Sequoia Ascent 2026.

Software 1.0 is traditional programming — you write explicit, deterministic code. The program is the code. Software 2.0 is machine learning — you create datasets and objectives, neural networks learn the program into weights. The weights are the program. Software 3.0 is the current moment — you program LLMs through prompts, context, and tools. The context window is the program. Each paradigm shifts what the 'program' actually is and how you create it.

Just as a traditional programmer writes code that a CPU interprets, a Software 3.0 builder designs context that an LLM interprets. Everything in the context window — prompts, instructions, examples, tool definitions, memory, retrieved documents — constitutes the program. The LLM reads this context and performs computation in digital information space. Your leverage over the output comes from what you put into that window.

Verifiability is Karpathy's framework for understanding where AI improves fastest. Traditional software automates what you can specify; LLMs automate what you can verify. If a task has an automatic success signal — tests pass/fail, code compiles, metrics improve — models can practice and improve at it. This is why coding agents feel dramatically better than other AI applications. For builders: find where your domain has verifiable structure and build there first. Karpathy's formula: capability spike = verifiability × training attention × data coverage × economic value.

Agent-native products are built for AI agents as the primary user, not just humans clicking through screens. Characteristics: markdown docs instead of click-through UI flows, CLIs and APIs instead of dashboards, MCP servers for structured data access, copy-pasteable agent instructions for setup, machine-readable schemas, structured logs, and safe permissioning with auditable actions. Every product decision now has two versions — the human version and the agent version.

This guide is written from hands-on testing, then cross-checked against primary sources - official documentation and first-party announcements. Field results and opinions are labeled as such. See our [editorial standards](/about).
