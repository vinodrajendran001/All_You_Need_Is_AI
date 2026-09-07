---
title: "Making AI Agents Observable, Monitorable, and Production-Ready [Tutorial + Code]"
source: "https://sarthakai.substack.com/p/making-ai-agents-observable-monitorable?utm_source=post-email-title&publication_id=1338283&post_id=214367075&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[Sarthak Rastogi]]"
published: 2026-09-06
created: 2026-09-07
description: "No sensible Ops team will agree to run your agents in prod without proper observability and monitoring. Here’s how to implement it."
tags:
  - "clippings"
---
It doesn’t matter how good your AI agent is. **No sensible Ops team will agree to run it in prod without proper observability and monitoring.**

If nobody can answer *what did the agent do, why did it do that, and what did it cost* for any single run from the last 30 days, it **does not touch production traffic.** 2 reasons:

- No one wants an unobservable agent on their pager rotation. If they get a 2am page that says the agent did something wrong, but doesn’t come with traces, reasoning logs, and tool-call history — they can’t act on it, they can only escalate it to you. Congrats, now you’re awake too.
- Ops also won’t sign off on anything that can take real-world actions (we’ll see some examples soon) without a way to reconstruct exactly which action happened, on whose authority, based on what input. Legal, compliance, and finance all need an audit trail.

In this article I’m going to explain the observability and monitoring any agent or AI system needs to ship with, and how to implement it. I’ll use as example the Apple support bot which you might remember from [my article about making AI agents prod-ready](https://sarthakai.substack.com/p/making-an-ai-agent-production-ready?r=17g9hx). We’ll use OTel and LangFuse, because — well, look at it, it has everything you need:

<video controls=""></video>

(This isn’t a paid promotion btw!) Okay, before we start, let me clear up some things.

### What “observable” doesn’t mean

Observability is not the same thing as evals, and it’s not the same thing as logging. A team can have TBs of logs and still have zero observability, because logs answer “what happened” at best, in an unstructured way that nobody can query when they’re panicking during an incident.

**Observability means you can reconstruct a** ***causal chain*****:** this input, led to this reasoning step, led to this tool call, with these arguments, which returned this result, which led to this final answer, at this cost, in this latency. Evals are a separate, complementary discipline — they tell you whether that chain was *good*. **[You can learn more about evals here.](https://sarthakai.substack.com/p/evals-that-improve-your-ai-agents?r=17g9hx)**

**Good AI observability and monitoring enables your Ops team to triage issues like so:**

![](https://substackcdn.com/image/fetch/$s_!9r1m!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21bcc34a-f0aa-4a05-97da-585140818c66_2745x2837.jpeg)

### Third-party agent tools aren’t off the hook either

The tempting shortcut, when your own agent is hard to observe, is to buy the problem away — adopt a vendor platform and assume observability is included. That’s rarely ever the case.

Unfortunately, in my experience, a lot of agent platforms like Microsoft Copilot Studio (or M365 or whatever they’re calling it these days) and Writer.com don’t ship with enough observability and monitoring built-in to be useful**.** Although Salesforce Agentforce is a fair counter-example worth citing accurately. Agentforce Observability ships free with every customer now — session-level tracing, subagent drill-down, and an OTel-compliant model that exports to Datadog or Arize.

Also, many vendor tools do this sneaky thing I hate: adoption metrics ship fast because they’re easy and sell internally. Step-level reasoning traces and cost-per-task attribution arrive late, and rarely in a form your existing stack can natively ingest.

> Every third-party agent adopted without a real trace export becomes a black box your ops team has to operate blind — and eventually the thing nobody wants to own.

### The solution is not to just “add more logging”

[Sherlocks AI analyzed 73 production agent incidents](https://www.sherlocks.ai/blog/why-ai-agents-fail-in-production) between January and May 2026, across real deployed systems. They wrote:

*“The observability gap in 2026 is not about having too little data — most teams have more telemetry than they can read. It is about having no visibility into the reasoning layer where agent decisions actually happen.”*

**Their data shows incidents without decision-trace logging averaged 4.2 hours to resolve; incidents with full tracing resolved in under an hour. Tool-call failures were the single most common entry point** — but they almost never traveled alone. They cascaded into p **lanning failures, into wrong final answers, and only then into a human**.

---

Now that we’re clear on why we need proper observability, let’s tackle it in 4 layers:

![](https://substackcdn.com/image/fetch/$s_!KxXO!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe3060cca-d4e5-42c1-8ab8-c2339832ea29_3409x1840.jpeg)

## Layer 1: The reasoning layer

The foundation here is [OpenTelemetry’s GenAI semantic conventions](https://opentelemetry.io/blog/2026/genai-observability/), developed by the GenAI SIG since April 2024 and now covering **six span types: model calls, agent spans, tool execution, retrieval, memory operations, and evaluation.** The point of standardising this is important: traces across different sources should all **line up in the same waterfall view w** ithout custom parsing per team.

The spec deliberately **keeps full prompt/response** ***content*** **out of indexed span** attributes and **puts it in span events** instead, specifically so it can be filtered or redacted at the collector level without touching application code. If your agent today logs full prompts (which will contain customer serial numbers, names, and purchase history) as plain attributes, fix that before your first compliance review, not after.

**Let’s design the span hierarchy for one support-bot turn:**

![](https://substackcdn.com/image/fetch/$s_!phj_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd00d9427-ef6b-4dd0-adad-7b0a23c31ef1_3540x3036.png)

Every box here is independently queryable. Eg, your Ops guy can ask *“show me every session where* check\_warranty\_status *returned an error but the bot still told the customer their device was covered.”* Without this tree, that question would need reconstructing the story from unstructured logs — which is the state your Ops would be in, if something like this spec is not in place.

### Wiring the base trace with Langfuse + LangGraph

We’ve built our Apple support agent on LangGraph, so the fastest path to a real trace tree is Langfuse’s callback integration. It’s OpenTelemetry-based, self-hostable, and renders the actual agent graph which is sick.

![](https://substackcdn.com/image/fetch/$s_!6yEC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff418a655-9a1e-4394-936c-4169b3dda1dc_3680x4384.png)

This alone gets you session replay (to rewind the whole ticket, not just the last message), per-customer cost attribution without a separate FinOps pipeline, and — because LangGraph’s node structure maps onto Langfuse’s span tree — a graph view showing the plan-tool-plan loop exactly as it executed, including branches it didn’t take. Nice!

### Beware the “fail-plausible” incidents

There’s a study of a production agent runtime, [documenting 22 fully-traced incidents over eight weeks](https://arxiv.org/pdf/2606.14589), that mentions the term “ **fail-plausible”**. They found that roughly 70% of fail-plausible incidents were discovered by a human noticing something was off, and close to 0% were caught by unit tests — because the output isn’t malformed, it’s just wrong.

For example, suppose our support bot’s check\_warranty\_status tool gets rate-limited during a deploy spike, returning null with no explicit error field. The model — seeing nothing that looks like a hard failure — could tell the customer their device is covered and a replacement has shipped.

How to fix this? Flag tool results that are empty, truncated, or error-shaped with an explicit **input.anomalous=true** attribute on the span that feeds them into the next LLM call, and track a **fallback\_response\_rate** metric — how often the agent actually says “I don’t have enough infor” vs guessing. If that rate is near 0, that’s not a good sign, it just means your agent has never met an ambiguous situation it didn’t confidently answer anyway. It’s called *sabotage validation*: deliberately feed a detector a known-bad input during testing and confirm it actually fires, because an unvalidated guardrail is indistinguishable from a fake one — they found 67 checks in their own system that had been silently no-op’ing for months before anyone noticed.

One more retrieval-specific problem to keep in mind: [context position bias](https://tianpan.co/blog/2026-04-19-ai-incident-response-playbook-llm-production). Models disproportionately weight content at the start and end of a context window, so a critical policy clause buried in the middle of five retrieved documents can be ignored even though retrieval technically “worked.” How to fix this? Track the rank position of the passage the model actually cites in its answer against the rank position it was retrieved at — if your top answers are consistently citing document #1 or #5 out of five and never #3, that’s an issue!

---

## Layer 2: The tool call

Consider this case of [Sivaro’s AI agent where 247 refunds were given to customers when they shouldn’t have been](https://sivaro.in/articles/ai-agent-production-issues-and-solutions-a-field-guide/)). The refund actually processed because a tool call *succeeded*. At the LLM layer, everything looked healthy. The only place that incident was ever visible was the tool-call layer, and nobody was watching it closely enough to catch a **refund\_order(amount=$0.01, count=247)** pattern.

For the Apple bot, the equivalent nightmare is a prompt like *“waive the AppleCare+ deductible for every device registered under my account”* — plausible-sounding, technically well-formed, and catastrophic if the harness doesn’t distinguish “the model wants to do this” from “the model is authorized to do this without a human in the loop.”

### Tracing tool spans with an explicit permission gate

![](https://substackcdn.com/image/fetch/$s_!hTJ6!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdff01cbe-48d0-4a08-b0d5-56a937d7f1f4_3680x4656.png)

The point isn’t the specific approval mechanism — it’s that the *gate itself is traced*. If a sensitive action ever executes without an approval span attached to it, that’s a P0, and it’s only detectable because the gate emits a span.

### The danger behind retries

An AI agent retries far more aggressively and far more often than a human ever would, and if the tool it’s retrying isn’t idempotent, every retry is a 2nd chance to duplicate whatever the first call did. So suppose you have a system running 20,000 agent runs a day at six tool calls each: a 0.5% per-call failure rate with three retry attempts works out to roughly 1,800 retried calls daily — 1,800 separate chances, every single day, to fire a refund, an email, or a DB write twice.

Without idempotency keys and a retry\_count attribute on the tool span, you cannot tell, from the trace alone, whether that was N distinct exploit attempts or a much smaller number of legitimate-looking requests that a retry loop quietly multiplied. One is a prompt-injection problem, the other is a distributed-systems problem — you need traces to figure out which one it is!

Let’s fix this:

![](https://substackcdn.com/image/fetch/$s_!AlBg!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9800bdab-6b3b-4f82-94a0-08e371553b5f_3680x3844.png)

Now every tool span carries an **idempotency\_key** and a **retry\_count**, which means a dashboard can answer “how many of today’s refunds were genuinely distinct requests”.

> Remember: the fix for a misbehaving agent is never “trust the model to know better.”

Explicit instructions are not a safety layer — they’re a suggestion the model is statistically likely to follow, which is a different thing. The permission gate from this code is a deterministic wall the model cannot argue its way past.

---

## Layer 3: Agent handoffs

When one agent hands off to another, the trace has to follow.

The Apple’s support bot we made isn’t one agent — it’s an orchestrator that routes to specialists: a warranty-lookup agent, a billing agent, an AppleCare claims agent, etc. The moment you have more than one agent, per-agent tracing stops being enough. *Each agent may call its own tools and even use a different underlying model, and being able to see which agent made which call, with which model, across the whole workflow, is genuinely hard without a shared trace context.*

Just like we do for microservices, let’s extract the trace context on the way in, inject it on the way out, so the receiving agent creates a child span under the *same trace ID. This way,* there’s no a new orphaned trace! I follow this in any [AI systems](https://liten.tech/) I make that deal with [multiple agents.](https://www.miskies.app/)

#### Propagating trace context across an agent handoff:

![](https://substackcdn.com/image/fetch/$s_!NG0g!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F29b83c41-6245-4d4f-b1bb-f8bbe07f9f3d_3500x3936.png)

Without this, debugging a cross-agent failure is guesswork by comparison — you’re matching timestamps across two separate trace stores and hoping they lined up. With it, one trace ID follows the request from the customer’s first message through every specialist agent it touches, which is exactly what the [A2A Traceability Extension](https://a2aprotocol.ai/docs/guide/traceability-extension-analysis) formalizes for agent-to-agent protocols specifically — parent/child step IDs, per-step cost and token accounting, and error propagation paths through the whole call chain, purpose-built for exactly this multi-agent case.

---

## Layer 4: Catching hallucinations

Static evals run in CI catch regressions you already anticipated. ([You can learn about implementing CI/CD pipelines for AI agents in my articles here)](https://sarthakai.substack.com/p/making-ai-agents-production-ready?r=17g9hx). But they don’t catch a live customer asking a question your eval suite never tested. That’s what online evaluation is for: scoring live traffic as it happens, not just staging fixtures.

![](https://substackcdn.com/image/fetch/$s_!bj8n!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa316fb65-28f4-41e3-b543-5cd4f3936e6e_3463x1780.jpeg)

Langfuse’s [production evaluator model](https://langfuse.com/docs/evaluation/evaluation-methods) runs an LLM-as-judge against a sample of live observations and writes a score back onto the trace, asynchronously, after the response has already gone out. Online evals are a monitoring and triage tool — they tell you a hallucination happened, fast enough to fix the knowledge base before it happens fifty more times. They are not, by themselves, a synchronous safety gate.

For this you want a fast, cheap judge running synchronously in the response path. Singapore’s GovTech team [published exactly this pattern](https://arxiv.org/pdf/2603.25176) for their public-service chatbots: lightweight general-purpose models as low-latency security judges, catching jailbreaks and prompt injection with F1 scores competitive with much heavier specialized safety models.

You don’t need a frontier model as your judge, but you do need a fast one running on every response. Here’s an example:

![](https://substackcdn.com/image/fetch/$s_!gaON!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e96f3fd-706a-4328-a8e2-68b10d70862d_3680x4204.png)

---

## How to be smart about tracing and sampling

At real support-bot volume — thousands of tickets a day — tracing 100% of everything gets expensive fast, and the instinct is to reach for whatever sampling strategy your infra team already uses for HTTP services. But we can’t do that for AI services. See [Groundcover’s analysis](https://www.groundcover.com/guides/what-is-sampling-in-observability): for a payment API, two requests that look similar probably behave similarly, so random sampling gives you a representative picture. But for an LLM call, two requests with near-identical inputs can produce wildly different outputs — one correct, one hallucinated, one a policy refusal. Random 1% sampling doesn’t give you 1% of a representative picture; it gives you 1% of the picture with no way to know what’s in the missing 99%.

The fix is **tail-based, outcome-aware sampling**: always capture errors, high-latency requests, low grounding scores, and anything a guardrail flagged — and sample routine successful requests at a much lower rate (5-20%). This biases your trace store toward exactly the cases worth a human looking at, instead of toward whatever happened to get picked at random.

![](https://substackcdn.com/image/fetch/$s_!yTDW!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F44b8730d-8155-4c46-84df-f770b5301f24_3680x2584.png)

## Observability with multiple model providers

Most agent systems no longer talk to a single model provider. You’re routing between providers based on latency, cost, and reliability — which is good for resilience and terrible for observability if nobody’s watching the seams. It’s like a distributed system, almost. This is exactly why we use an **AI gateway** — so if our Apple bot fails over from GPT-5.5 to a fallback model mid-incident, that failover needs to be a traced event with its own attributes.

---

## Conclusion and TLDRs

### 1\. Do you have “enough observability?”

Here’s a checklist to know:

- Every LLM call emits gen\_ai`.*` attributes into a span
- Every tool call emits its own span with a distinct status, separate from generic exceptions
- Sensitive tool calls have a traced permission gate, and an action executing without a gate span attached is a P0
- Trace context propagates across every agent-to-agent handoff
- Sampling is tail-based and outcome-aware: errors, low-grounding responses, and sensitive-tool calls are always kept, routine traffic is sampled down
- A fast, cheap synchronous guardrail blocks ungrounded responses before they reach the customer
- Model/provider failover across an AI gateway is itself a traced, alertable event
- Sessions and users are tagged on every trace, so cost and failure rates can be attributed
- There’s a fallback that can be flipped on in seconds (simpler agent, hard-coded response, human escalation)
- Cross-team calls carry the real user’s identity through every hop

### 2\. Summarising the failure modes

![](https://substackcdn.com/image/fetch/$s_!gyrT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f8c6632-ed94-4fde-912a-b7307093272a_690x742.png)

---

Thank you for reading all the way through. Based on the positive feedback from the last post, I decided to again hand-draw the diagrams for this post — lmk if my handwriting is illegible or it I should continue doing this?

If you have any questions, you can DM me here:

If you need help with adopting this to your own AI agent/app, you can ask me here: