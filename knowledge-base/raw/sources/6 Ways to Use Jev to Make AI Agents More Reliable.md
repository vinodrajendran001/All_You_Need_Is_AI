---
title: "6 Ways to Use Jev to Make AI Agents More Reliable"
source: "https://sarthakai.substack.com/p/6-ways-to-use-jev-to-make-ai-agents?utm_source=post-email-title&publication_id=1338283&post_id=217209579&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[Sarthak Rastogi]]"
published: 2026-09-25
created: 2026-09-28
description: "Jev is exactly the cheap & fast decision layer agents need"
tags:
  - "clippings"
---
Open the trace of your AI agent and count the steps that **write something.** Then count the steps that **decide something.**

- Is this message a refund request or a bug report?
- Should the agent call the search tool?
- Is `rm -rf build/` safe to run right now?
- Is this reply good enough to send, or should a human look at it?

The agent makes these decisions by calling a frontier LLM — which works, but is slow, expensive, and a bit absurd.

![](https://substackcdn.com/image/fetch/$s_!eBmT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5bb562ca-a972-4a7d-b1f9-c9e0b1d08141_631x464.png)

A model called **Jev** launched on September 15, 2026 and it does this classification. It answers typed questions in about 100 milliseconds for $0.042 per million input tokens, with output tokens free. This article covers what it is, where it fits in your AI agent, and how other teams are already wiring it in.

---

## What Jev is

- Jev is a “System One” model from TypeSafe AI. You **send it some state** and typed questions, and it **returns typed answers with probabilities**. It generates no text.
- It fits at the **decision points** of an agent loop: intent routing, model routing, input screening, tool-call gating, output verification, and picking the next UI action.
- Typesafe says it’s 40x to 200x faster and up to 400x cheaper than frontier LLMs on decision-shaped work.

#### How it differs from an LLM:

![](https://substackcdn.com/image/fetch/$s_!kfAc!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e3b97ba-7305-4c76-8757-df538f4388ef_1384x1104.png)

While an LLM responds token by token with free form text that may turn out to be valid JSON, Jev responds with typed values only, with a confidence score for each value. See the diagram:

![](https://substackcdn.com/image/fetch/$s_!Iz82!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02f90072-a403-431f-b50d-165adf314975_2885x1701.jpeg)

### The three question types

Everything you ask Jev is one of three primitives:

![](https://substackcdn.com/image/fetch/$s_!cIkS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5b10e231-a653-44c9-92db-970820a00294_1430x542.png)

The table comes from the LangChain integration docs.

A `Noul` of 0.5 means “the model can’t tell”. It does not mean “medium”. For a spectrum, use a `Score`.

---

## How to use Jev in an agent loop

Agents run a loop:

1. the LLM decides,
2. a tool runs,
3. something evaluates the result,
4. repeat.

Thing is, a loop stays slow and costly because every decision needs another model call. Jev goes at the decision points and leaves the reasoning and writing to the LLM. See this example of where Jev fits in the agent loop. The pink steps are Jev decisions. Everything else is code or an LLM.

![](https://substackcdn.com/image/fetch/$s_!kMbu!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6d1274e-b277-4281-9b97-4d48f625e0fa_2854x3305.jpeg)

That’s what we’re about to do! Here are the usecases that the rest of the article covers:

![](https://substackcdn.com/image/fetch/$s_!Xipn!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fef95fd8c-16bc-4e06-a995-5ebc80164ac6_1438x828.png)

If agent loops and graphs are an unfamiliar concept to you, you can learn all about them here:

---

## Usecases

## Use case 1: intent classification and routing

### The problem

- Requests may need to go to different handlers: a database lookup, an LLM with product docs, a human. Eg, a user asks “I was billed incorrectly last month” and your agent needs to figure out the process to follow to respond to it.
- The classic version is a small LLM prompt that classifies among a set of intents like \[billing, orders, returns, products\] and then returns a label. That adds a call, adds latency, and gives you no calibrated confidence.

### The solution

Use ==Jev== to predict, for each request, the user’s intent. **This example LangGraph workflow** asks Jev for a typed `Choice` and routes each inbound email to the matching handler:

![](https://substackcdn.com/image/fetch/$s_!SDoT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1db777aa-996f-434d-a739-60f6749e8949_3680x7076.png)

![](https://substackcdn.com/image/fetch/$s_!f5zd!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe99b0b98-2144-4fc7-b055-66d9a15d5be7_585x376.png)

- For example, the order-status branch never goes to an LLM. That is where the savings live.
- Anything under 0.6 confidence goes to a person. Pick your own threshold after you measure!

---

## Use case 2: model routing

A simple lookup does not need the same model as a complicated task. Routing each request to the cheapest model that can do it is one of the best-documented ways to cut agent cost. ==Eg, (and this is before Jev) LiteLLM reported 43% savings and RouteLLM says it can save 85% by model routing.==

Suppose you get 100 user requests — here’s how that’ll pan out:

![](https://substackcdn.com/image/fetch/$s_!KBGw!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff66b35f2-fd20-4cc3-a30d-59e0e47c54bd_2999x1131.jpeg)

The catch is that the router itself has to be cheap and fast, or it eats the savings. An LLM-as-judge router can add 1 to 5 seconds per request, which can double the latency of short requests and cancel some of the savings!!

Let’s do it with Jev:

![](https://substackcdn.com/image/fetch/$s_!Ic7V!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7519ae91-a404-4be3-9367-5ac789a77516_3680x3208.png)

---

## Use case 3: catching malicious intent

This is a usecase personally very important to me. Users often try jailbreaks and prompt injection (eg, telling the agent to ignore its instructions and write a recipe for a bomb because of a dying grandma somewhere).

If you’ve been reading my work for while, you’ll know that I built a [set of open source classification models that can detect harmful user queries quite well. You can try this via my Python library rival-ai:](https://github.com/sarthakrastogi/rival/tree/main)

![](https://substackcdn.com/image/fetch/$s_!l3RN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ebc793d-77b4-43f5-8fb6-d144128d0a61_661x319.png)

Tool outputs and retrieved pages can also carry hidden instructions which can screw up your agent and produce an unsafe output.

> A system prompt isn’t the best place for any rules to prevent this, since a jailbreak is exactly an attempt to talk its way past it. A second LLM in front doubles latency and can be talked around as well.

The workable design is a fast Jev based classifier on both sides of the model: screen the input, screen the output.

**In [TypeSafe’s guardrails cookbook](https://docs.typesafe.ai/cookbooks/llm_guardrails.md), o** ne request per message runs a battery of `Noul` questions (jailbreak, harmful request, medical advice, self-harm) plus a `Score` for how much harm complying would do. Your code applies thresholds. Results from [the cookbook](https://docs.typesafe.ai/cookbooks/llm_guardrails.md), run on `jev-1.12`, show that it worked pretty well.

Here’s how to build your own:

![](https://substackcdn.com/image/fetch/$s_!_9eo!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6bb51dc0-7c7f-453f-9d54-9533ad61364a_3680x6628.png)

### Caution:

- **Jev does not treat its input as hostile.** TypeSafe’s own jaggedness notes say adversarial content in the state can move the answer. A dedicated injection question helps, but treat the screen as a filter and not as a security boundary. Keep least-privilege tool access underneath it.
- **False positives are a cost too.** Anthropic’s first classifier generation paid for its robustness in refusals of harmless queries. Track how many real messages your screen blocks.

---

## Use case 4: gating tool calls

- Agents fail hardest when they act. A bad reply is embarrassing but if it deletes your DB that’s a different level of catastrophe.
- The same command can be right or wrong depending on the task. `npm run db:reset` is correct if the user asked for a reset and a disaster if they asked to add a column.
- A second LLM on every call adds seconds. Users end up turning it off, or approving everything by reflex.

![](https://substackcdn.com/image/fetch/$s_!SHR6!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F432f2277-eb63-4958-b94e-6e7f07715f2f_622x405.jpeg)

A conventional response to Claude Code deleting your prod DB and responding with “You’re right to push back”.

**Think about Claude Code’s auto mode.** A classifier reviews each tool call before it runs. Safe ones proceed, risky ones get blocked with a reason so the agent can try something else, and repeated blocks fall back to a permission prompt. Anthropic’s [announcement](https://claude.com/blog/auto-mode) says the classifier can still miss risky actions when intent is ambiguous, and can block harmless ones.

And users approve about 93% of permission prompts anyway, per [Shipyard](https://shipyard.build/blog/claude-code-auto-mode/). That is the friction auto mode exists to remove. Let’s try and create a classifier with Jev instead:

![](https://substackcdn.com/image/fetch/$s_!WyA9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F81e57e4b-68fe-4f11-a094-a91931f817aa_3680x5276.png)

Notice that the gate only sees the task and the pending action, and never the tool outputs. That’s similar to the reasoning-blind design in Claude Code’s classifier.

---

## Use case 5: confidence-gated escalation

A wrong answer with no uncertainty attached is dangerous. The value of a calibrated model is that you can route the uncertain slice somewhere safer, like so:

![](https://substackcdn.com/image/fetch/$s_!N5N0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff98fef43-ecaf-4861-8d03-8ea526c606e6_3116x1408.png)

Escalate any low-confidence responses, and let the agent execute on high confidence ones. If there’s medium confidence, well, let the agent gather more context and try again (with a finite retry loop).

![](https://substackcdn.com/image/fetch/$s_!q_q0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F487efc36-c457-4a0b-a8b6-1bc5debd771a_2828x683.jpeg)

Then measure whether your thresholds mean what you think they mean:

![](https://substackcdn.com/image/fetch/$s_!4gHp!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff5a2e9ff-984d-4e68-8e46-c675e2258cba_3680x2128.png)

---

## Prompting Jev Well

The model hasn’t been out for very long, so from limited experience here’s what I’ve found so far:

- **One judgment per question.** If your question hides three factors, split it into three and combine the answers in code.
- **Write the exact condition.** Jev reads literally. Scoping words, negations and implied conditions are taken at face value.
- **Describe situations in criteria, not degrees.** “Broken feature, workaround exists” is better described than “moderate”.
- **Give it an exit.** Add an `other` option on every `Choice`, since the model has to pick something.
- **Keep math, dates and counting in code.** TypeSafe’s [jaggedness notes](https://docs.typesafe.ai/model-jaggedness/jev-1.13) list arithmetic and date comparison as weak spots. To count things that match a semantic condition, ask one `Noul` per item and sum in code.
- **Send only the state each question needs.** Accuracy falls as unrelated content piles up, so do some context engineering.

---

## How to roll out Jev in your agents without breaking prod

- **Week 0: pick one simple decision** your agent makes and make Jev do it.
- **Week 1: shadow mode.**
	- Run Jev beside the current behavior. Log the full answer, confidence and model version, and pin the versioned model ID once you tune thresholds.
		- Maybe trace it in [LangSmith](https://docs.langchain.com/oss/python/integrations/providers/typesafe), which logs classifier calls with token usage.
- **Week 2: label and measure.**
	- Label 100 to 200 cases. Compare against your current approach on accuracy, latency and cost per solved task.
- **Week 3: automate.**
	- Let Jev take over paths that it handles accurately. Act on high confidence for reversible actions. Send everything else to a human or a stronger model.

### What you gotta keep out of Jev

- Anything that must generate text.
- Arithmetic, counting, date logic.
- Images, audio and video. It reads text only.
- Any decision where a wrong answer is expensive and volume is low. Use a reasoning model and a person.

### Open source alternatives to Jev

The open-source community reacted fast to Jev’s release. Within a week there were clones such as [Kev](https://github.com/jaredpalmer/kev) (built on Qwen3.5, following Hume’s architecture), [openjev](https://github.com/TheoLeeCJ/openjev), NanoJev and Laya. None of them match TypeSafe’s training or calibration, and the founder says calibration data is the moat.

Calibration means that when Jev says 0.9, it should be right about 90% of the time. This is a generalised eval from Typesafe, so measure it yourself on your data too:)

---

## Conclusion

AI agents got their fluency from big generative models, and that fluency comes with latency and a bill on every decision. Jev is an early, credible attempt at making the decision cheap, and I like that.

I think the useful question for the next few weeks is which of your agent’s calls are simple checkboxes which can be delegated to Jev.

*If you try any of this, I’d like to hear what you measured:)*

---

If you have any questions, you can DM me here:

If you need help with adopting this to your own AI agent/app, you can ask me here:

Thanks for reading AI Agent Engineering! This post is public so feel free to share it.

If you’re building AI agents, you might enjoy reading these tutorials about making them more reliable: