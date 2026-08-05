---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-karpathy-agentic-engineering
title: 'Agentic Engineering: Karpathy''s New Framework'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/karpathy-agentic-engineering
published: '2026-05-27'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Agentic Engineering: Karpathy's New Framework

Andrej Karpathy just reframed the entire conversation about AI coding — and if you are building with Claude Code, Codex, or Cursor, it directly changes how you should think about your work.

At Sequoia Ascent 2026 (April 30), Karpathy drew a hard line between two things most people treat as the same:

**Vibe coding raises the floor. Agentic engineering raises the ceiling.**

Here is what that actually means — and why the distinction matters if you want to ship serious AI products.

---

## What is vibe coding (and why it is not enough)

Vibe coding is what most people think of when they hear "AI-assisted development." You describe what you want, the agent generates code, you accept it and move on. It is fast, accessible, and genuinely useful for prototypes.

Karpathy coined the term in early 2025. By Sequoia Ascent 2026, he was already moving past it.

The problem: vibe coding has no quality bar. You can ship fast but ship slop. The agent tries to match your Stripe email to your Google account email — two different emails, broken user credits — and you accept the diff without catching it. The code runs. The product is broken.

> "You are not allowed to introduce vulnerabilities because of vibe coding. You are still responsible for your software, just as before."

---

## What agentic engineering actually looks like

Agentic engineering is a professional discipline. You are not a passive recipient of generated code — you are an orchestrator of fallible, stochastic agents who are extremely powerful but still wrong in surprising ways.

**The skills that matter:**

- **Spec design:** writing a detailed spec before you prompt. Not plan mode — something deeper. The docs, the invariants, the security boundaries. You write them; agents fill in the implementation.
- **Diff review:** reading what the agent actually produced. Not accepting blindly. Understanding whether the abstraction makes sense, not just whether the tests pass.
- **Eval design:** building feedback loops. Does this work? How do you know? Tests pass or fail — that verifiable signal is what lets agents improve.
- **Security oversight:** the agent thinks email is a good cross-system identifier. It is not. You still have to know why.
- **Quality bar:** sometimes the generated code is bloated, copy-pasted, awkwardly abstracted. It works but it is gross. You need enough taste to insist on better.

This is what the ceiling looks like. And Karpathy thinks the ceiling is very high — much higher than the old "10x engineer" benchmark.

> "People who master agentic workflows may outperform others by far more than 10x."

---

## The December 2025 inflection point

Karpathy described a specific moment: December 2025. He was on break, had more time, and noticed something changed in the models.

> "The chunks just came out fine. Then I kept asking for more and they still came out fine. I couldn't remember the last time I corrected it."

The unit of programming shifted from writing lines of code to delegating macro actions:

- Implement this feature
- Refactor this subsystem
- Research this library
- Write tests, run them, fix failures
- Compare approaches and propose a plan

This is why agentic engineering matters now and did not matter as much a year ago. The agents got reliable enough to delegate to. Which means the constraint shifted to the orchestrator — to you.

---

## What human skills become more valuable

This is the most important part of the Sequoia talk for builders.

As agents do more, what becomes scarcer:

**Understanding** — you can outsource thinking, but not understanding. You still need to know what is worth building, what result is suspicious, what tradeoff is acceptable.

**Taste** — agents produce code that works but is sometimes gross. They can refactor a 100K-line codebase but cannot simplify it to the elegant core the way a senior engineer would.

**System design judgment** — the Stripe/Google email example. Agents make plausible-but-wrong architectural decisions. You catch them, or you ship a bug.

**Eval design** — knowing whether the agent is off the rails requires a feedback loop. Building that loop is a human skill.

Karpathy's summary: "The scarce thing is shifting. Less scarce: code generation, boilerplate, first drafts, setup. More scarce: understanding, taste, eval design, security, agent orchestration."

---

## How to hire for this (Karpathy's test)

Hiring for agentic engineering looks different. The old small puzzle interview is dead.

Karpathy's proposed test: give someone a substantial project, have them build and deploy it with agents, then send adversarial agents to try to break it.

Can the candidate decompose work for agents? Write useful specs? Preserve quality while moving fast? Review generated work? Secure and harden the system?

These are the skills to practice now. The developer who masters this workflow does not compete at 10x — they compete at a much higher multiple.

---

## What to do with this

If you are currently vibe coding your way through projects, here is the upgrade path:

**1. Slow down at the spec stage.** Write out what you are building before you prompt. Invariants, security boundaries, data model. 20 minutes here saves hours of bad diffs.

**2. Review every diff.** Not for syntax. For architecture. Does the abstraction make sense? Are there hidden cross-system assumptions?

**3. Build your feedback loop.** Tests, evals, benchmarks. The agent improves when it has a signal. Without it, you are just retrying prompts.

**4. Keep conceptual ownership.** Let the agent remember that PyTorch uses `dim` and numpy uses `axis`. You still need to know about memory, views, storage, copies — the fundamentals the agent gets wrong under pressure.

---

Vibe coding was a beginning. Agentic engineering is the profession.

AI Builder Club members are running weekly workshops on real agentic workflows — spec templates, diff review patterns, eval loops, and the mistakes nobody talks about. [Join us](https://www.aibuilderclub.com/pricing?utm_source=blog&utm_medium=article&utm_campaign=agentic-engineering) and work through these with people already in the field.

---

*Source: Karpathy's Sequoia Ascent 2026 talk (April 30, 2026).*

Agentic engineering is a professional discipline where you orchestrate fallible, stochastic AI agents rather than passively accepting generated code. Core skills include spec design (writing detailed requirements before prompting), diff review (reading generated code for architectural correctness), eval design (building feedback loops with verifiable signals), security oversight, and quality taste. Karpathy introduced the term at Sequoia Ascent 2026 to distinguish serious AI-assisted development from casual vibe coding.

Vibe coding raises the floor — anyone can describe what they want and get working code. It's fast and accessible but has no quality bar. Agentic engineering raises the ceiling — you maintain conceptual ownership, review every diff for architecture (not just syntax), build eval loops, and preserve security boundaries. Vibe coding ships fast but ships slop; agentic engineering ships fast *and* ships quality. Karpathy's framing: vibe coding is a beginning, agentic engineering is the profession.

Karpathy described a specific inflection point in December 2025 when he was on break and noticed that model outputs consistently came out correct — larger chunks, more complex tasks, fewer corrections needed. The unit of programming shifted from writing lines of code to delegating macro actions: implement this feature, refactor this subsystem, research this library, write and fix tests. This is when agentic engineering became viable as a daily workflow rather than an occasional experiment.

As agents handle more code generation, the scarce skills shift to: (1) Understanding — you can outsource thinking but not comprehension of what's worth building. (2) Taste — agents produce code that works but is sometimes bloated or awkwardly abstracted. (3) System design judgment — catching plausible-but-wrong architectural decisions like using email as a cross-system identifier. (4) Eval design — building feedback loops so you know when the agent is off the rails. (5) Agent orchestration — decomposing work, writing specs, managing multiple parallel agents.

Karpathy proposes replacing small puzzle interviews with a substantial project test: give the candidate a real project, have them build and deploy it using AI agents, then send adversarial agents to try to break it. This tests decomposition skill, spec writing quality, speed with quality preservation, diff review rigor, and security hardening — the actual skills that matter in an agentic engineering workflow.

This guide is written from hands-on testing, then cross-checked against primary sources - official documentation and first-party announcements. Field results and opinions are labeled as such. See our [editorial standards](/about).
