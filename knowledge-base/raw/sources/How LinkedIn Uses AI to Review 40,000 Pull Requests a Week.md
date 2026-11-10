---
title: "How LinkedIn Uses AI to Review 40,000 Pull Requests a Week"
source: "https://blog.bytebytego.com/p/how-linkedin-uses-ai-to-review-40000?utm_source=post-email-title&publication_id=817132&post_id=223813863&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-11-10
created: 2026-11-10
description: "Most of its reviews are posted before the first human reviewer even opens the PR"
tags:
  - "clippings"
---
## 4 Key Insights for Scaling LLM Applications (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!-g6Z!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f66d37b-9c93-4b16-81bd-15a36324a8c4_1920x1080.png)

The challenge of running LLM applications in production is that failures are silent, costs are unpredictable, and security vulnerabilities are hard to detect until it’s too late.

Download this Datadog eBook for practical strategies to monitor, debug, and secure your LLM application workflows end-to-end. You’ll get 4 key insights into how to overcome the challenges of deploying LLMs at scale — from tracing multi-step chain executions and detecting prompt injection attacks to tracking token costs and evaluating output quality in real time.

---

LinkedIn has more than **10,000 active code repositories**, with tens of thousands of pull requests (PRs) being opened each week \[1\]. As coding agents write more of that code, the slow part of shipping software has moved from writing code to reviewing it.

To overcome the code review bottleneck, LinkedIn built its own AI reviewer. In a typical week, this in-house reviewer covers more than **40,000 PRs**, and most of its reviews are posted before the first human reviewer even opens the PR \[1\].

To better understand the landscape of AI reviewers and how LinkedIn built theirs, we interviewed [Min Chen](https://www.linkedin.com/in/minchen07/), a Principal Staff Engineer at LinkedIn, and [Balaji Srinivasan](https://www.linkedin.com/in/thebalaji/), Senior Director of Engineering at LinkedIn. Thanks to both of them for their time and for being open about what did not work.

![](https://substackcdn.com/image/fetch/$s_!JDQw!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F35a42d09-7b73-4378-83ed-a907f990eaef_2882x3010.png)

LinkedIn’s AI reviewer system (High-Level)

In this article, you’ll learn:

- What an AI code reviewer is, and why review is the bottleneck these days
- Three main directions for teams and companies to handle the code review bottleneck
- How to build a multi-agent AI reviewing system that works in production
- What evaluation looks like for AI reviewers
- What’s ahead and where the new bottlenecks move

## What Is an AI Code Reviewer?

Software development has two main steps. An engineer writes a change, and other engineers review it before it merges into the main codebase.

![](https://substackcdn.com/image/fetch/$s_!mHmN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe7e46450-0dc0-4fd2-afb3-aa40d0ba575a_2652x706.png)

Software development’s two main steps

When an engineer writes the code, the change becomes a PR. Then reviewers read its diff, that is, the lines it adds, removes, or changes. Here are the typical steps from when a writer opens a PR to when the PR is merged back into the codebase:

1. The author opens a PR from a branch that has the change.
2. The code host, such as GitHub, notifies the reviewers and starts continuous integration (CI), which runs tests and linters (to flag style problems and simple errors).
3. A reviewer reads the PR and comments on specific lines.
4. The author pushes fixes. Then the reviewer looks again.
5. The reviewer approves, and the PR merges.

![](https://substackcdn.com/image/fetch/$s_!4ygB!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2c5301d2-9020-4476-8dd8-4f11eeb1e6b8_3168x1332.png)

The typical path of a PR, from opening to merging.

AI is changing this development process, because it can now help with some of these steps. Engineers hand those steps to AI agents and spend more of their time focusing on intent and judgement. That is AI-native development.

Specifically for the writing step, frontier coding agents have shown promise lately. Given a task, an agent implements the feature, writes the tests, then runs those tests, and iterates until they pass. Finally, it opens a PR for review.

![](https://substackcdn.com/image/fetch/$s_!fexj!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10557b0c-b291-4842-82d3-b8daeb2664f6_3968x1334.png)

Coding agents automate writing, but PRs still waits for review.

With coding agents, writing (the first step) can now be largely automated and done much faster. Instead of an engineer spending hours or days writing a change, the agent spends minutes writing it. But if real humans still have to review the proposed changes, the process will still be slow, because engineers’ hours are still fixed and limited.

![](https://substackcdn.com/image/fetch/$s_!QHv6!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ab657d5-ba75-4b13-b127-08b813b79003_3366x1006.png)

Writing got faster, so review became the bottleneck.

The fix is a system that can reliably review code, ideally before humans do. That system is called an AI reviewer. It reads a PR the way a human reviewer would and comments on the lines that need attention. Once the automated code review is complete, the author, in this case the coding agent, addresses them so human reviewers spend their limited time on judging the fixes.

Since models are also getting better at reading code, more teams are automating reviews this way \[2\]. They mostly differ in the extent to which they aim to automate the reviewing process. Full automation would let AI approve changes on its own. This is difficult, and most labs are not there yet.

Partial automation keeps human approval on changes and gives AI the first pass. This makes the process faster but keeps real humans in the loop to reduce the risk of merging buggy or insecure code. Partial automation is more feasible these days, and companies that have an AI reviewer in place, like LinkedIn, usually use partial automation. In the rest of this article, we focus on partial automation.

![](https://substackcdn.com/image/fetch/$s_!I-_H!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46143547-41f7-4c96-8c0c-30f17fb6d757_2804x1494.png)

Full vs partial automation

But why is building an AI reviewer challenging? For an AI reviewer to be reliable, it has to have four properties:

- Grounded: it flags real problems in the changed lines.
- High-signal: the issues it produces are real bugs and high-risk lines (not just minor style nits a linter would catch).
- Codebase-aware: it follows the codebase’s own conventions.
- Timely: it comments while the author can still act on it.

![](https://substackcdn.com/image/fetch/$s_!GcsX!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe859b357-f37a-418b-93a1-8b792ea8a060_3136x1942.png)

The four properties an AI review comment needs

Getting all four at once is the hard part. LinkedIn built its own system over several iterations to get there. Let’s see how they built it.

---

## Stop reinstalling your toolchain on every CI run (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!cxFV!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc050743f-6377-4e5e-b752-43b299c8b439_1600x840.png)

AI agents open more pull requests, and each one reinstalls the same dependencies from scratch. That is wasted CI time and money.

WarpBuild keeps that work:

- Snapshot runners boot from a saved machine image, with your toolchain already on disk
- Each job still gets a fresh, ephemeral runner
- The WarpBuild cache restores dependencies between jobs
- Twice as fast at half the cost of default runners

Trusted by teams at Braintrust, Raycast, OpenRouter, Comcast and Jane Street.

Use code START50 for $50 in free credits.

---

## How to Build an AI Code Reviewer

Remember from earlier that the goal is partial automation. PRs still get a human review, but the AI review comes first. As a company, you have different options to have an AI reviewer in place. Some options are easier to set up but less flexible, while others take more work to build but give you more control over the quality of the comments.

Three common directions are:

- Use a vendor’s reviewer
- Use an off-the-shelf model with your rules
- Build a custom multi-agent review system

![](https://substackcdn.com/image/fetch/$s_!TQnI!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05fa3d3b-c715-4796-ac24-5ab8d088c48e_3188x2082.png)

Three ways to get an AI reviewer

### Direction 1: Use a vendor’s reviewer

A fast way to have an AI reviewer in place is to simply buy a hosted system from a vendor. The reviewer connects to the code host and comments on each new PR moving forward. So you don’t have to build the system internally.

This direction is simple to set up, does not need any particular expertise, and is probably the fastest option. But it has two major limits. First, it is generic. You can add a rule file, but the vendor controls the prompts and the harness, so many comments are generic and could apply to any project.

The second limit is control. The vendor owns the system, so it decides when the model or the instructions change. You cannot test an update before engineers see it or gradually roll out a change.

![](https://substackcdn.com/image/fetch/$s_!whTq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F901db15f-6fdc-4e3a-af5a-ff695aef0de9_2804x1670.png)

A vendor’s reviewer meets your codebase only through a rules file.

LinkedIn tried this option first. During an AI-native pilot, teams were asked to opt in to a vendor’s hosted reviewer. But the team observed that the comments were noisy and generic. They did not fit LinkedIn’s codebase and each repository’s rules. When the comments are noisy, engineers lose trust.

Soon, engineers asked to opt out, which meant the full manual review was back again. The team also had no control over the vendor’s changes. Min put it this way: “You don’t own anything. They do something, they change something, you just react to it.”

### Direction 2: Use an off-the-shelf model with your rules

Since a hosted reviewer is too generic, a natural next step is to use an off-the-shelf model, but build your own harness around it. That way, you can choose your own prompts and write the codebase’s own rules into its instructions. With those instructions and more control over the harness, the comments will be more specific to your conventions.

This direction sounds promising: the comments would be specific to the codebase and would likely arrive quickly, before human review. But it has two main problems.

The first problem is hallucination. Because the system relies on a single model and there is no verification in place, if the model hallucinates, nothing will catch it. The author will end up with a comment about a problem that does not exist, or a real problem attached to the wrong line.

![](https://substackcdn.com/image/fetch/$s_!iZX3!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e89b7c8-8912-4116-862b-1e48b0e53a69_2992x2026.png)

Grounded vs. hallucinated comment

The second problem is knowledge gaps. A model learns what good and bad code look like from its training data. With a single model, it will work well on areas that overlap with its training data, but will fail on out-of-distribution inputs or inputs that were less frequent in the training data. That means a single reviewer model misses the same classes of issues repeatedly and may over-flag the same low-value issues.

![](https://substackcdn.com/image/fetch/$s_!NgcF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F426010b4-8260-435f-abd9-705ae4be5581_3366x2092.png)

A single model works well on what looks like its training data.

LinkedIn also observed the same issues when the team built the review system with their repository-specific rules. The model gave good results but produced many hallucinations, and some of its comments did not even match the line numbers in the diff. Using a different model for review than for writing code did not fix the hallucination issue. But that idea led the team to ask whether a second model could check and verify the first model, the idea behind the multi-agent design.

### Direction 3: Build a custom multi-agent review system

This direction relies on multiple agents to produce grounded reviews. There are different design patterns for multi-agent systems, but a popular one is the orchestrator-subagent pattern \[3\], where one agent hands work to several subagents and combines their results. For code review, the subagents independently review the same PR, often each with a different model, and return their findings with line numbers. The orchestrator then merges overlapping findings, ranks them by confidence, and posts only reliable reviews.

![](https://substackcdn.com/image/fetch/$s_!Unbj!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff24c9eb1-d57b-447e-b7b9-70028c3c15b8_3366x1334.png)

The orchestrator-subagent pattern

This design can mitigate most of the limitations of the previous directions because you own the whole system, different models cover each other’s knowledge gaps, and findings by different agents must be verified by others to survive and be posted.

To add your rules and codebase conventions, there are two ways. One is context injection, which means adding a rule file to the repository that the AI reviewer reads on every PR. This can work in simple codebases, but is not a flexible approach because some rules apply to every repository, some to one repository, and some to one kind of change. A single file being injected as context cannot contain all three or combine the right ones for each PR.

The other approach, which LinkedIn used, is a layered design. You design several tiers, and each has its own scope, owner, and rules. Then a dedicated subagent uses those rules to perform an independent review. LinkedIn used the following three tiers:

- **Company-wide rules** apply to every repository. These can be YAML files clarifying what the model should check.
- **Repository rules** cover one codebase. This can be a markdown file containing the team’s conventions like coding standards and review criteria.
- **Pull request rules** apply only to one kind of change.

![](https://substackcdn.com/image/fetch/$s_!Koqu!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ba30a54-30d3-48bd-9591-1b3816def004_3474x1490.png)

Layered rules to get a right mix of company, team, and change-specific checks.

To better understand how this system reviews a PR, let’s go over a concrete example and see how each step handles it. Imagine an author opens a PR that has a new python file named cache.py, implementing an in-memory cache for a Python service. But the code has two problems. It has a race condition and a bare except.

![](https://substackcdn.com/image/fetch/$s_!Pa4m!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6958e80-026b-4468-8944-f9e7d810a36d_3254x1572.png)

The AI reviewer handles the example PR in three steps: review, merge, and verify.

The author, who may be a coding agent, writes the change and opens a PR. The PR is then handed to the AI reviewer, which reviews it in the following three steps.

**Step 1: Running parallel independent reviews**

The orchestrator fetches the diff and codebase context, then dispatches them to several subagents at once. A subagent builds its own prompt, reviews the full diff in the context of the codebase and its recent changes, and then returns its structured findings.

Notice that the subagents never see each other’s findings while they review. If Subagent A could read Subagent B’s findings first, it would tend to agree, but because the subagents work independently, their agreement counts as evidence.

![](https://substackcdn.com/image/fetch/$s_!gAR-!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3f51393a-e92d-4790-b94e-6a3821231cdb_3896x2396.png)

Independent subagent reviews

**Step 2: Merging reviews**

The independent subagents from the previous step produce findings. Many of those findings may overlap, pointing to the same issue(s). For example, if three subagents find the same five issues, the author gets fifteen comments for five problems. So the orchestrator has to merge duplicates.

This can be done in two phases. First, a deterministic check marks findings with overlapping line ranges as candidates, a cheap step that limits the search to the same code. Second, an LLM decides whether each candidate pair describes the same problem. This second phase is necessary to find overlaps semantically because two models usually do not phrase an issue the same way.

The overlaps also indicate review confidence. If multiple findings merge into a single comment, the engineer is more likely to accept it, so the code reviewer can rank it higher.

![](https://substackcdn.com/image/fetch/$s_!J_dU!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1bc54187-ce25-4d40-836f-9267f9d2f32a_3214x2124.png)

Findings merge in two passes

The outcome of this step is a shorter list of findings, with overlapping ones merged into single high-confidence comments. However, we still need to check the findings that only one subagent raised, which is the focus of the last step.

**Step 3: Verifying reviews**

A finding from only one subagent is harder to judge. It might be a real issue the other model missed, but it might also be a hallucination. To find out, the orchestrator sends those to another model to verify against the code. According to LinkedIn’s post, this often saves real issues \[1\]. A model that missed an issue, when asked to verify another model’s finding, confirms the issue is real. Verified findings are then rated for importance.

When the verifying model contradicts the finding, its confidence score drops. Then, low-scoring findings become candidates for filtering. In addition, findings that are cosmetic, already fixed in a later commit, or against the repository’s established patterns are suppressed before posting.

![](https://substackcdn.com/image/fetch/$s_!aPpZ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96237ea4-23f4-4fd3-92a0-be2e0145c5bf_3858x1332.png)

Confirmed findings pass a final filter

With multiple agents, layered rules, and a three-step workflow, the system has all the properties we described earlier. It merges several independent reviews into one, verifies the findings, and posts the review.

## How to Evaluate an AI Code Reviewer

Labs and teams owning an AI reviewer system constantly change it. They may swap models, edit prompts, or add something in the harness. To tell whether a change will make the AI reviewer better, you must run evaluations, or evals, which are repeatable tests of an AI reviewer’s quality.

In this section, we cover the two phases of running evals for an AI reviewer: before a change is released, and in production after the code merges.

![](https://substackcdn.com/image/fetch/$s_!hyeK!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96506a0b-af97-4d61-8979-af807b48b470_3328x1474.png)

Evals run in two phases: before a release and in production.

### Eval before a release

Before a change ships, you need to know whether the change will improve things or not. A typical process is to run the production version and the candidate on the same PRs and compare their reviews, either with an LLM judge or against a golden dataset built from human labels.

With an LLM judge, a separate model takes both reviews of the same PR as inputs, and scores them. This is cheap to run and does not need human labels. You mostly need to have a fixed rubric so the LLM follows a more predictable and reliable path to score the reviews. LinkedIn has a rubric with six weighted yes-or-no criteria, and runs every prompt, model, and harness change through this before they ship.

![](https://substackcdn.com/image/fetch/$s_!nJxM!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9818de4-c396-4a5e-a64c-d7d685bc435b_2964x1136.png)

An LLM judge scores the production and candidate reviews against the same rubric.

LLM-as-a-judge works well for comparisons \[4\], but it cannot reliably decide which comments are actually right. A golden dataset fills that gap with known right answers.

A typical process is to collect real PRs at the point a bug was found, and humans mark which review comments are correct. This becomes our golden dataset. We can score candidates against these labels and measure traditional metrics like precision and recall. LinkedIn has built such a dataset and is now building the eval on top of it, as a complement to its LLM-as-a-judge.

### Eval in production

Pre-release evals run on a sample of PRs or a fixed dataset, so they cannot show how the reviewer performs on thousands of real PRs, or whether engineers find its comments useful. Those kinds of measurements can be obtained only from production. Evaluating an AI reviewer in production relies on two things: the right metrics and a feedback loop.

The right metrics determine how well your system is doing in production. There are often so many different metrics to track, such as time to first review, cost per review, and how engineers react to comments. But some are more insightful than others. Emoji reactions, for example, are noisy because they say little about whether a comment helped. On the other hand, acceptance rate is a good metric because it checks whether the code changed because of a comment. Balaji explained what counts as acceptance at LinkedIn: “Not someone giving thumbs up or thumbs down, but the code actually changed.”

![](https://substackcdn.com/image/fetch/$s_!518K!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ab50597-7aa0-4495-8329-bc053bcf03c1_2924x1136.png)

Acceptance counts code that changed.

LinkedIn evaluated their system in production and measured acceptance on thousands of AI comments. As the next figure shows, engineers accepted 63.9% of them \[1\]. These numbers show that engineers act on most of the AI reviewer’s comments, with the highest rates on concurrency bugs and dead code (100%) and logic errors (80%).

![](https://substackcdn.com/image/fetch/$s_!-7nB!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff84b8f8c-973b-43b7-8d1d-ff64ead3bedd_3188x1808.png)

Acceptance by category

We talked about metrics, but the more important part of evaluation in production is to have a feedback loop: a mechanism that turns those measurements into actual fixes.

As you measure your system with different metrics, you learn where the gaps are. If you run and measure your system every day, you can close those gaps. For example, LinkedIn now runs its acceptance check daily and produces a trend report of which rules and prompts are gaining or losing acceptance. The team uses it to decide which rules to disable and which prompts to change.

![](https://substackcdn.com/image/fetch/$s_!Vd8H!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F923795e6-22eb-43e7-b429-3e682dc4c432_2644x2080.png)

A daily loop turns acceptance trends into rule and prompt changes.

That is evaluation. Pre-release evals check whether a change is safe to ship, and the daily loop measures the system in production and improves it over time.

## What’s Next

In Balaji’s view, the next bottleneck after review is confidence in the quality of the software as a whole, which takes more than reviewing each PR. He does not expect review to stop being a bottleneck until automated validation is in place. Deploying, monitoring, and handling incidents also take more effort than development, so LinkedIn is aiming AI tools there too. As he put it, “the faster we are pushing out code, the faster we are potentially breaking production.”

![](https://substackcdn.com/image/fetch/$s_!WsAT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F14872cec-f635-4402-9380-87225b3edb0a_3214x1402.png)

Next bottleneck

LinkedIn’s next step for its AI reviewer is a risk heat map: an optional feature that will score each region of a PR’s diff by predicted risk so that engineers review the riskiest parts first.

![](https://substackcdn.com/image/fetch/$s_!PT00!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d3f9e86-dd0f-42de-b752-64bc4860312e_3214x1568.png)

Risk heat map

### References

\[1\] High-Signal AI Code Review That Adapts to Your Codebase at Scale: [https://www.linkedin.com/blog/engineering/ai/high-signal-ai-code-review-that-adapts-to-your-codebase-at-scale](https://www.linkedin.com/blog/engineering/ai/high-signal-ai-code-review-that-adapts-to-your-codebase-at-scale)

\[2\] 60 million Copilot code reviews and counting: [https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/](https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/)

\[3\] How we built our multi-agent research system: [https://www.anthropic.com/engineering/multi-agent-research-system](https://www.anthropic.com/engineering/multi-agent-research-system)

\[4\] Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena: [https://arxiv.org/abs/2306.05685](https://arxiv.org/abs/2306.05685)

---

∙