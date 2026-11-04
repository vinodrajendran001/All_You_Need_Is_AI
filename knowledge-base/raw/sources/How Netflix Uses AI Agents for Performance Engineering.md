---
title: "How Netflix Uses AI Agents for Performance Engineering"
source: "https://blog.bytebytego.com/p/how-netflix-uses-ai-agents-for-performance?utm_source=post-email-title&publication_id=817132&post_id=222755655&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-11-04
created: 2026-11-04
description: "The Netflix engineering team has developed an autonomous performance agent system. In this article, we’ll be learning more about it."
tags:
  - "clippings"
---
## The real benefits of end-to-end observability (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!AhGz!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4ff6acab-5dfa-413b-b839-cf5b13501afc_1200x628.png)

How does full-stack observability impact engineering speed, incident response, and cost control?

In this eBook from Datadog, you’ll learn how real teams across industries are using observability to:

- Reduce mean time to resolution (MTTR)
- Cut tooling costs and improve team efficiency
- Align business and engineering KPIs

See how unifying your stack leads to faster troubleshooting and long-term operational gains.

---

Performance engineering is the discipline in which you design, analyze, and optimize software systems so that they run quickly. Also, they should use resources efficiently. In distributed architectures, the focus of any performance engineering activity is on shaving milliseconds off response times. Or locating execution bottlenecks in CPU or memory. Or making sure infrastructure costs are kept under control.

Historically, performance engineering work has been slow. And manual. You often depend on a small group of really skilled developers. However, with the rise of AI-assisted software development, there’s a contradiction. Developers can write and ship code faster than ever. No matter what their skill level may be. But that code often introduces subtle performance problems.

To solve this problem, the Netflix engineering team has developed an autonomous performance agent system. In this article, we’ll be learning more about it. Here’s what we will cover:

- Bottlenecks for traditional performance work
- The problem with AI-Generated code
- Can LLMs handle profile data
- The agentic profiling pipeline
- The problems Netflix found in production
- Safety, verification, and trust architecture
- Shifting left

*Disclaimer: This post is based on publicly shared details from various sources. References at the end. Please comment if you notice any inaccuracies.*

## Bottlenecks For Traditional Performance Work

Traditional performance engineering work at Netflix was built on a highly iterative loop that is pretty much manual in nature.

![](https://substackcdn.com/image/fetch/$s_!uk-_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa461266-54bb-4caa-87bd-44e62109da52_2432x2038.png)

First, you trigger profiling for an application. A developer tries to detect high latency or increased resource usage by triggering a profiler on a live production server.

In the second step, the profiler outputs raw trace data or flame graphs. The developer downloads these details to their local machine.

Third, the developer spends time looking at complex, color-coded flame graphs. They try to spot wide stack frames that might show signs of higher-than-normal CPU or memory consumption.

Next, the developer goes through the codebase looking for cryptic method names found in the flame graph. They try to make sense of the surrounding application logic to figure things out.

Fifth, the developer traces the execution path and identifies the inefficient operation. They write a proposed patch to fix the operation.

Moving further, the developers deploy the patch to an environment where any change in performance levels can be measured.

At the end, when new code paths are deployed in production, the developer starts the manual process once again.

As you may have noticed, this workflow doesn’t scale. Everything depends on a few domain experts who have a deep sense of understanding about low-level execution stacks. Since human attention is a scarce resource, you can investigate performance issues only for major incidents or obvious system slowdowns. Smaller but steady resource drains go unnoticed.

---

## Why Braintrust, Raycast and Jane Street use WarpBuild (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!XUMB!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe02e5fb7-c8c4-4a9b-bba1-0fd863850cbb_1600x840.png)

Fast-moving teams ship more code than ever, and AI tools add even more. Their CI has to keep up without the bill getting out of hand.

That is why teams at Braintrust, Raycast, OpenRouter, Comcast and Jane Street run GitHub Actions on WarpBuild:

- Twice as fast at half the cost
- Linux, macOS and Windows on x86-64 and ARM64
- Unlimited macOS concurrency
- One line change to runs-on

Use code START50 for $50 in free credits.

---

## The Problem with AI Code

The use of AI coding assistants has increased performance problems. There are two main reasons for this. The speed trap and the context gap.

Developers who are using AI tools can generate and ship code up to 10 times faster than before. No matter their skill level or knowledge of the system. But you cannot guarantee that code that is fast to generate also performs well. While your average developer might be able to write 10K lines of code in a few minutes, the team might have to spend years debugging regressions. Or dealing with code bloat. Or handling other architecture-related problems.

Also, if you’ve noticed, LLMs are great at syntax and local-level logic. If you ask an LLM to write a function or an API endpoint, it writes code that compiles successfully and runs without any obvious errors. It might also pass standard unit tests. However, the LLM has no idea about the host platform’s runtime environment.

For example, you can’t expect the LLM to know that a particular utility function being used in your code might run 10 million times per second on a critical request path. It cannot see the overall call stack. Neither can it understand memory allocation challenges that might exist inside a container running at peak load within your platform. Therefore, the code you write might appear good enough in isolation. But it can still waste a huge amount of resources when you run it at scale.

## Can LLMs Handle Profile Data

Netflix wanted to test whether automation could remove these issues. They set up an experiment to find out if an LLM can read and make sense of raw profiling data directly.

![](https://substackcdn.com/image/fetch/$s_!Jm17!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe791ea9f-247d-4cc5-bc29-5f800a035695_3292x2012.png)

Different languages have different profilers. But they use a shared language and store the same core information. For example, JVM’s async-profiler or Java Flight Recorder operates at 100 Hz sampling to capture execution traces, memory allocation rates, and thread lock contention. Python’s py-spy provides low-overhead, async stack sampling of live production processes. Go has pprof, which generates goroutine profiles, heap snapshots, and block contention data.

Each one of these profilers breaks down execution into call stacks. They track two main metrics. First, you have the inclusive time. This is the total time spent executing a function. It includes every child function and the subroutines called by this function. Second, you have the Self (CPU) Time. It’s the time spent running code purely inside the function itself. No external calls are involved.

With this exercise, the Netflix engineering team came to the conclusion that a single analytical pipeline could understand data from almost any programming runtime.

Another advantage of LLMs is that they don’t have to guess how an algorithm works from scratch. Since LLMs have been broadly trained on many software repositories, they are mostly familiar with classic programming anti-patterns. For example, they know that quadratic loops where a hot method is called again and again for each item in a collection aren’t a good idea. Also, loop invariants where you compute a calculation for every iteration of the loop instead of making the calculation once at the beginning. Other patterns include excessive object allocation on hot execution paths and “N+1” query patterns.

Due to this knowledge base of LLMs, you don’t need to ask an AI model to guess why an application might be performing poorly. You can build a workflow that asks the model to pattern-match known performance bugs against actual call stacks.

## The Agentic Profiling Pipeline

Netflix built an automated performance system that wraps the LLM inside a well-defined pipeline.

![](https://substackcdn.com/image/fetch/$s_!Fpfx!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F937b41ad-bfbf-411c-9061-fbd0fbfad501_3472x1934.png)

A key lesson Netflix engineers learnt during this implementation was about scoping. If you feed an LLM a complete, raw stack trace without boundaries, it can get distracted. Often, the model spends a lot of reasoning tokens analyzing internal JVM garbage collection pauses, low-level Linux kernel syscalls, or even 3rd party open-source framework overhead.

Application developers don’t have any control over such internal library concerns or OS routines. Therefore, you need to provide the agent with strict package prefix rules. This way, the model can ignore generic platform noise and focus on tracing only the specific application code.

## The Problems Netflix Found in Production

When the Netflix engineering team deployed the profiling pipeline against its production service, the agent found 4 major categories of performance bugs.

First was an algorithmic bottleneck that wasted 8.8% of CPU resources. The agent found an aggregation method using Java Streams where an immutable map was updated inside a reduction step.

```markup
// Anti-pattern: O(N^2) accumulation inside stream reduction
stream().reduce(ImmutableMap.of(), (acc, val) -> {
    return ImmutableMap.builder()
        .putAll(acc) // Copies every existing entry on every single step
        .put(val)
        .build();
});
```

Since putAll(acc) copies every existing key-value pair on every step, you need to copy elements again and again to build a map of size N. This results in quadratic complexity.

The agent modified the quadratic builder reduction with a linear collection approach.

```markup
// Optimized: O(N) single-pass collection
stream()
    .flatMap(e -> e.entrySet().stream())
    .collect(toMap(Entry::getKey, Entry::getValue));
```

The second category was about regular expressions on the hot path. In a service, the developer had to sanitize incoming request strings by modifying characters that weren’t allowed. The earlier implementation ran a raw regular expression substitution on every request.

```markup
// Anti-pattern: Dynamic regex evaluation per request
String sanitized = input.replaceAll(”[^a-zA-Z0-9.-]”, “_”);
```

As you might know, evaluating regular expressions involves parsing and state-machine transitions. This logic on high-volume traffic used 46% of the service’s CPU time.

The agent replaced the regex evaluation with a pre-computed lookup table that checked characters by index. The execution got 22 times faster.

The next category was related to unnecessary object allocation that caused OOM crashes. A service frequently checked whether incoming data payloads contained specific metadata fields. To perform the check, the code was creating a new, heavy HashSet on every incoming call.

However, the underlying data object already had an internal lookup method available. Also, instantiating millions of such objects consumed 47% of the service’s total heap collections.

The agent fixed this issue by removing the redundant object instantiations and modified the code to reuse the cached method.

The next category was around library misuse. For example, the discovery involved metric telemetry instrumentation. One of the services tracked operations by looking up a counter from a metric registry on every single call.

```markup
// Anti-pattern: Looking up metric instances on every function execution
Metrics.counter(”request.count”).increment();
```

When the query was sent to the registry, it needed dictionary lookups and internal synchronization locks. The profiler showed that the work consumed 66% of the CPU, whereas the actual business logic used only 0.3%.

The agent fixed it by caching the metric counter reference at the time of class initialization. Also, it found that the same issue was happening across three independent services.

## Safety, Verification, and Trust Architecture

If you have an AI agent that can optimize code, it’s quite dangerous if the changes are applied without automatic verification. If the agent makes a change that breaks business logic, it’s worse than inefficient code.

To prevent regressions, the agentic pipeline uses the standard SDLC.

In stage 1, you verify the logic. Before you move any code, the agent’s branch must pass all existing unit, integration, and contract tests. This is to make sure that the changes made by the change don’t alter basic inputs, outputs, or handling of edge cases.

In stage 2, you have the canary deployment. If the tests pass, the pipeline spins up a canary deployment in production. The canary instance gets a portion of the traffic. It runs side-by-side with an identical baseline instance that runs the original code.

Stage 3 is about generating the observability report. The platform collects hard telemetry metrics over a big enough window. Some metrics are relative CPU utilization, median latency, P99 latency, and memory allocation rates. They also don’t use any AI model to check the canary results.

In stage 4, you have the final engineering decision. When the canary version shows a good level of performance improvement with zero increase in error rates, the system opens a PR. This PR goes for human review. It includes the code change, the original flame graph, and the canary report. The final decision on deploying the change to production is taken by the human developer.

## Shifting Left

Automated production profiling is quite effective. But if you just rely on it, you end up exposing several limitations.

By the time an agent finds an anti-pattern in production, you’ve already paid for days or weeks of wasted compute capacity.

Second, developers are anyway cautious about changing a running service. If you have a service that handles production traffic without crashing, the developers hesitate to just make changes for the sake of optimization.

Lastly, multiple teams often make the exact same mistakes when it comes to patterns. If you run a super-expensive agent on 10 different services just to find the same problem, it’s not very efficient.

These limitations led to Netflix making the decision to shift performance checks left into the early development cycle. Also, they wanted the agents to share their findings across the entire engineering organization.

However, as you might know, language models are stateless. Every time you send a prompt to an LLM, it starts with a clean slate. It might no retain any memory of the bug it found some time back in another service. The Netflix engineering team built a Pattern Catalog to make the models achieve persistence. This was done by pairing a stateless LLM with a stateful catalog. Or a shared memory across the fleet.

The Pattern Catalog was built around 4 key principles.

- First, it has to be centralized and serve as the single source of truth for all engineering teams. This way, no two teams end up debugging the same issues.
- The second principle is that the same catalog entries should work across distinct environments. For example, offline profiling, CI/CD pull request checks, and local development tools.
- Third, you need to format entries so that an automation script can easily inject them into an LLM’s system prompt.
- Lastly, the contents of the catalog should be reviewable by human developers.

To implement the Pattern Catalog, the Netflix engineering team used a simple Git repository filled with plain Markdown files. They didn’t use vector databases or complex knowledge stores. The idea was borrowed from the “LLM-wiki” concept popularized by Andrej Karpathy.

By using a standard Git repository, the developers got several advantages. For one, developers can diff changes, open pull requests, and use git features to find out why an entry was created. It also scales well to 100s of detailed performance rules without the need for complex search infrastructure. Lastly, plain Markdown is easy for both humans and language models to read without translation layers.

## How Netflix Catches Problems Early

With the Pattern Catalog in place, Netflix can handle performance engineering via two paths. Reactive and Proactive.

![](https://substackcdn.com/image/fetch/$s_!zz8C!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b9b4997-595e-4a9f-9b67-fffaba0aca9c_3592x2272.png)

In the reactive path, your system profiles production services on a recurring schedule or on demand. When the agent finds a new bottleneck, it tests the fix on a canary instance. If everything goes fine, the patch is merged, and the agent documents the new finding in the Pattern Catalog.

In the proactive path, the process starts when a developer creates a new PR. CI tooling performs a fast regex or symbol match against the Pattern Catalog index. If the code in the PR matches known anti-patterns, the CI bot calls an LLM and provides it with the pull request diff. The LLM checks the context and leaves an inline comment that explains the inefficiency. It shows the resource impact and suggests a fix. All this happens before the code ever merges to the main branch.

## Conclusion

The key learning from the Netflix engineering experience is that automating performance engineering work is not an all-or-nothing game. You can have organizations adopt workflows along a four-level maturity spectrum.

Level 0 is the manual situation. This is the level where machine learning is not used. Human developers manually capture traces, interpret flame graphs, and trace code paths.

Level 1 is the assist approach. This is the entry point for AI adoption. The LLM acts as an analytical copilot. A developer initiates the profiling process. But they don’t spend time studying flame graphs. Instead, they feed the stack dump to the model. The model finds the hot execution path.

Level 2 is the orchestration level. This is the current state at Netflix. A lot of proactive scanning happens. Also, they use the Pattern Catalog.

Level 3 is the fully autonomous level. This is the long-term vision at Netflix for performance agents. At Level 3, the agents will create their own optimization strategies. They will explore multiple alternative implementations. Or run automated benchmarks.

**References:**

- [A Netflix Production Story - P99 Conference](https://p99conf.io/session/the-autonomous-performance-agent-a-netflix-production-story/)

---

∙