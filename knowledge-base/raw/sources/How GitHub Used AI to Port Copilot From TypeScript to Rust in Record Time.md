---
title: "How GitHub Used AI to Port Copilot From TypeScript to Rust in Record Time"
source: "https://blog.bytebytego.com/p/how-github-used-ai-to-port-copilot?utm_source=post-email-title&publication_id=817132&post_id=223839962&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-11-11
created: 2026-11-11
description: "In this article, we’ll look at how this porting was done and the learnings along the way."
tags:
  - "clippings"
---
## NYSE President Lynn Martin discusses AI (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!lwOL!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d5d673d-38f3-47e7-8a75-b00db4d680ad_1200x1200.jpeg)

AI is moving fast, from experiments to agents that act on their own. Few people have a better view of what that shift means for business than Lynn Martin, President of NYSE Group. At the Agentic Data Summit on December 9, Lynn joins Redpanda Founder & CEO Alex Gallego for a conversation on what it takes to adopt AI where reliability is everything, how AI is showing up in the companies coming to market, and why timely, trustworthy data matters more than ever as agents start acting in real time. Tune in at 9:19 AM PT. The summit is free and virtual and runs 8:30 AM–2:00 PM PT.

---

GitHub recently rewrote the software engine behind multiple Copilot products. They ported the codebase from TypeScript to Rust. Almost 800K lines of code. And the great part was that all of this was done using the GitHub Copilot app itself.

This porting exercise was triggered because the existing design was eating up a lot of resources. It was also becoming difficult to embed Copilot in other applications.

However, a project of this size would have required a big team of developers and a couple of years to get done. But by using the GitHub Copilot app, Copilot CLI, and AI agents, a single developer was able to finish the whole thing in a few months. In this article, we’ll look at how this porting was done and the learnings along the way. Here’s what we will cover:

- The need for porting the Copilot runtime
- The porting strategy
- How the porting work started
- The role of agent fleets
- How the new code was reviewed
- What were the issues
- The performance impact
- Cost of porting and learnings

*Disclaimer: This post is based on publicly shared details from various sources. References at the end. Please comment if you notice any inaccuracies.*

## The Need for Porting the Copilot Runtime

You can think of GitHub’s Copilot runtime as the shared software engine that takes care of AI agent behavior across multiple products. Due to this runtime, all these products can reuse the same capabilities instead of needing to maintain their own implementation.

![](https://substackcdn.com/image/fetch/$s_!t5iH!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2e64b9e1-d8ca-427a-b096-38cffbb4851e_4024x1604.png)

Originally, the GitHub engineering team had built the runtime using TypeScript that ran on Node and the V8 JavaScript engine. While this supported rapid development, the runtime was tightly coupled to the command-line application’s user interface. When GitHub needed an SDK to let other applications talk to Copilot, it built that SDK on top of the existing command-line application. When you started the SDK client, you had to launch a separate background process that was made up of the command-line application and its runtime. Requests and responses moved between the consumer app and that process.

This setup became harder to justify when the runtime spread to applications that had stricter requirements for speed, memory usage, and scale. Even if you had an application written in Python, Java, or C#, it had to hold the additional Node and V8 machinery. When you started a client, you had to launch another process and prepare JavaScript for execution. Each client had to bear roughly 100 MB of memory overhead at a bare minimum. Also, processes talking to each other added a lot of overhead. Lastly, applications had to monitor two processes, and a crash in the Node process could take the session with it. These costs were a huge problem for services that hosted many clients.

Therefore, GitHub wanted a standalone runtime library that was clearly separate from the UI. Applications should be able to load that library directly into their own process.

Rust was an ideal choice for this type of requirement. It had low overhead and predictable resource usage. An early estimate showed that roughly 130K lines of production TypeScript had to be ported. But additional logic moved out of the interface layer into the runtime. Also, you had other developers adding new features. Ultimately, 430K lines of production TypeScript code moved through the migration.

![](https://substackcdn.com/image/fetch/$s_!NG8Z!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde2a2a2c-e3de-4a1b-8f24-b6f22af03b1b_1200x660.png)

Source: GitHub Engineering Blog

---

## How much of your week is spent answering questions? (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!w0ew!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca4a3bd9-29ce-405e-a38a-2677e0f7df28_1600x900.png)

New hires, support, PMs, and your coding agents all need to know how the product works and why it works that way. Today, you’re the one pointing them in the right direction.

Unblocked works out what’s current and relevant across your code, PRs, tickets, Slack, and production data, so:

- Everyone gets cited answers in Slack without pulling in an engineer
- When the answer turns into a fix, a cloud agent drafts the PR
- Your agents generate code that follows past decisions, no steering needed

---

## The Porting Strategy

GitHub used an incremental, in-place porting strategy.

In this strategy, you replace the runtime one piece at a time, even when the product is under active development. The development team could continue to add new features and release updates throughout the migration.

![](https://substackcdn.com/image/fetch/$s_!rc9H!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb758cd12-3a72-448c-b721-e9848564425b_3472x2534.png)

The GitHub engineering team didn’t go for a complete rewrite followed by one large switchover. This approach would have concentrated all the risk into a single release. The replacement would need to keep catching up with oncoming changes. With the smaller replacements, they were able to make each change easier to review, test, and investigate.

The process worked in a step-by-step manner. A component’s TypeScript implementation was replaced with Rust in a single pull request, which grouped the changes for review. Any TypeScript code that depended on that component called the new Rust implementation through a thin wrapper. You can think of this wrapper as a temporary bridge between two languages. The old implementation was deleted as part of the same change, so that the team had to maintain only one active version of the component. As more and more stuff moved to Rust, these temporary bridges were also removed.

![](https://substackcdn.com/image/fetch/$s_!VDUl!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7acdc28c-e1a7-4bbd-966a-f7ea4e1e569e_3388x1476.png)

As far as the tasks were concerned, the work began with small, independent helpers that already had strong test suites and didn’t manage shared state. These early changes also helped test the build setup, packaging, and communication between languages. Once they had made the approach concrete, the migration went to more interconnected parts of the system.

Throughout this process, the key aim was to maintain existing behavior and algorithms. Broader redesigns were pushed after migration. At each step, validation was performed. They had existing end-to-end tests that checked if complete workflows behaved properly as their implementation changed. If there was a test failure, the changes weren’t merged. Also, when it came to the users, the ported components reached users through incremental releases. They often appeared in a pre-release before going to a stable release.

## How the Porting Work Started

GitHub started with a few small, working examples to test the waters before dealing with larger components.

The first couple of pull requests took care of the basic Rust setup. Things like build tools, automated checks, and coding instructions. They also introduced the runtime library and mechanisms for TypeScript and Rust to talk to each other.

The first main porting change moved three independent helper functions through the complete process. You can think of these early efforts as checking whether the translated code worked well. The team also tested how Rust code would be organized, built, packaged, and integrated with existing code. This gave the team practical experience with the entire process.

The rest of the work was ordered according to dependencies. For example, you had small helpers and supporting utilities come first. It was followed by components that managed state, then tools, model clients, and other integrations.

Session orchestration, which is supposed to manage much of the runtime, was left for the end. This is because larger subsystems often needed several rounds of work.

## The Role of Agent Fleets

Agent fleets played a key role in dividing the migration work among multiple AI agents working at the same time. You could have a coordinating agent investigate a large component, break the work into smaller tasks, and create other agents to handle them. The Copilot app made it possible to check these sessions and switch between them. It also let them exchange messages as the work progressed.

The team got two different types of assistance from these agents. First, you had the subagents that worked within the parent session’s workspace and returned their findings to it. These subagents were good for investigating code and answering specific questions. Then, you had the child sessions that had their own Git branches and separate working copies of the repository. This lets them make changes independently. This separation helped multiple agents work on different areas of the implementation without any risk.

![](https://substackcdn.com/image/fetch/$s_!x-1i!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F54d2acdc-7172-41d9-b155-b0d2aa72b680_3386x1930.png)

One example was around the session\[dot\].ts file that was roughly 30K lines and connected to many parts of the runtime. The coordinating agent spent an hour reading and checking before creating anything. After analyzing, it divided the work among 15 child sessions. It made the choice of models for each task. The parent talked with these sessions and tracked their progress from beginning to end. Finally, it brought the completed changes into its own branch.

Despite the advantages, running so many agents also created some limitations. When all 15 sessions tried to build and test their code at the same time, they overwhelmed the developer’s laptop. The workflow was adjusted so that child agents avoided expensive builds and tests. All that work was left for the parent. A separate chat session took care of build access for each of the porting sessions. It only allowed one build at a time.

Much of the agent fleet’s activities involved reading code, checking for dependencies, testing, and reviewing results. Their role wasn’t limited to writing Rust code. They also helped understand the existing system and check whether the replacement kept the same behavior. During all of this, human oversight remained critical.

## How the New Code was Reviewed

Developers were constantly changing the repository, and hence, code review had to check both the translation and whether the port had the latest changes. The team used a reusable instruction called “rust-rebase-review” to handle this process.

![](https://substackcdn.com/image/fetch/$s_!rT_-!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7bd8220a-010c-46c4-b0cc-92af87fd3752_2888x2034.png)

First, the main agent pushed its work to the latest main branch and resolved any conflicts. After this, it checked that any newly incoming TypeScript changes had also been ported into Rust. Deleting the old TypeScript helped bring such changes to attention. If another developer modified a deleted file, Hit would flag a conflict that had to be handled.

Next, you had multiple review agents using different AI models compare the old TypeScript with the new Rust code line by line. Their main job was to identify changes in behavior or compatibility. They also checked whether the Rust implementation was efficient enough. Also, whether obsolete TypeScript and temporary wrappers had been removed. They also had to ensure that existing end-to-end tests remained unchanged because they were the only reference for expected behavior.

The code review was done in a repeated cycle. When agents found any issues, the coordinating agent checked the findings and fixed any valid problems. This continued until the reviews became clean. Every round of fixes could be committed and pushed so automated checks could be done along with further reviews. Copilot Code Review and additional review bots also checked every commit and left feedback on the pull request.

Human reviewers focused on architecture, interface contracts, and risk factors that might have been highlighted by agents or tests.

## What Were the Issues

The porting exercise caused some regressions as well. You can think of these regressions as behavior that had worked earlier but stopped working as expected after the rewrite. The team found and fixed a bunch of regressions.

A common problem was that translated code changed the existing behaviour in a subtle manner. For example, some whole-number values were changed to decimal numbers, causing issues with certain SDKs. Other differences were around empty strings, time zones, or replacement libraries that had a different way of handling errors. The code could compile successfully. But the results could not be handled by other parts of the system.

Another major group of issues was around state management and coordination of operations. For example, when an operation was cancelled, it didn’t always stop all the related work. Also, when resources were released too early, the session got stuck. There was also a loss of some features. And some of them were only partially migrated.

There were also general integration and performance problems. For example, the Rust code sometimes performed lengthy work on Node’s main thread. This froze the interface. On Windows, missing process-launch settings made unwanted console windows appear.

## The Performance Impact of Porting

The rewrite brought down the overhead of running Copilot’s agent runtime. Especially in terms of time and memory. With the use of Rust, there was no need to initialize Node and V8. Also, no need to load and prepare the JavaScript application. Applications could load the Rust runtime directly into their own process. This avoided the cost of talking with a separate runtime process.

![](https://substackcdn.com/image/fetch/$s_!sNPx!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff7e78740-b2f3-4129-b2bc-ab849ef8c8cb_1200x530.png)

Source: GitHub Engineering Blog

GitHub saw performance gains during their detailed testing. For example, in a particular trial, creating a client, completing a single turn, and cleaning up took 5.25 seconds before the porting and 292 milliseconds after porting. This was an improvement of almost 18 times.

They also had capacity gains. In a test where many sessions shared one client, throughput went up from 7.55 completed session lifecycles per second to 120. Memory consumption also went down. In a 10-client test, the peak increase in private memory went down from 1383 MB to 126 MB.

The rewrite largely preserved the original algorithms. More improvements could happen if parts of the runtime are redesigned around Rust’s approach to memory ownership and concurrency.

## Cost of Porting and Learnings

The entire porting work cost around $120K in AI token costs. They covered roughly 136 billion tokens. Most of this volume was made up of cached input, which brought down the cost of repeatedly processing existing context.

More than that, you also had developer time that was spent on this work. Apart from the main developer, other developers also made contributions to integrations, packaging, build improvements, and reviews.

There were a lot of learnings along the way.

For one, it was critical to give clear instructions to the AI tools. Some of the initial requests to port a component sometimes led agents to translate only the central logic. The surrounding work stayed in TypeScript. The instructions had to be made more effective to handle this.

Another learning was that to perform such a migration successfully, you need strong end-to-end tests. These tests should check if complete workflows retained their original behavior. The team improved its test coverage beforehand. But additional coverage could have prevented some more regressions.

The tests also needed protection. For example, you don’t want an agent changing an implementation to make the test weaker or alter an expected result. So, you need to have some sort of oversight.

One more learning was that for such migrations, you should try to translate things first without worrying about redesigning. It’s more important to keep existing behavior and algorithms intact. If you attempt to combine the porting with other improvements, it only increases issues, time, and token costs.

**References:**

- [Migrating the GitHub Copilot runtime to Rust, using Copilot](https://github.blog/ai-and-ml/generative-ai/migrating-the-github-copilot-runtime-to-rust-using-copilot)

---

∙