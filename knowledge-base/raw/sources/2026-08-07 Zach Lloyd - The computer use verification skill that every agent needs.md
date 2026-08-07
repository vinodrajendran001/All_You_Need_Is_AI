---
type: raw-source
source_id: src-2026-08-07-zach-lloyd-computer-use-verification
title: The computer use verification skill that every agent needs
author: Zach Lloyd
url: https://x.com/zachlloydtweets/status/2084411777354277027
published: 2026-08-04
captured: 2026-08-07
status: immutable
tags:
  - source/raw
  - agents
  - computer-use
  - evaluation
---

> Preserve the source body below this line as the canonical capture.

![Image](https://pbs.twimg.com/media/HO1QQj-XsAANl4f?format=jpg&name=large)

In this post I’ll describe how to add computer and browser use to your agents to reproduce issues and verify fixes and new features.

Prior posts in this series:

1. [Build an issue triage agent and implementor agent](https://www.warp.dev/blog/how-to-build-a-cloud-software-factory-the-automatic-triage-skill)
2. [Add spec driven development via a spec agent](https://www.warp.dev/blog/how-to-build-a-cloud-software-factory-add-spec-driven-development-skills)
3. [Add a self-improving code review agent](https://www.warp.dev/blog/how-to-build-a-cloud-software-factory-self-improving-code-review)

For folks unfamiliar with [computer and browser use](https://www.warp.dev/blog/computer-use-cloud-agents), it’s a tool that allows agents to control a running application directly with mouse clicks and keyboard presses. Most of the major model providers have models that support this, and they are increasingly available in different harnesses, including Warp.

> Aug 2
> 
> Already shipped: prompt queueing. While an agent works, Ctrl/⌘+Shift+J auto-queues your next prompts, or /queue a follow-up. Queued rows can be reordered, edited, or sent early. https://docs.warp.dev/agent-platform/local-agents/interacting-with-agents/prompt-queueing/…

We’ve brought computer use to all parts of our agentic stack, [including feature requests on Twitter](https://x.com/ozdotdev/status/2083740540500152411)

The value of computer use in your cloud software factory is less as a standalone agent, and more as a capability to provide to other agents in the factory flow. Specifically, computer use is valuable:

1. During the [triage phase](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/triage/SKILL.md) to reproduce bugs before trying to fix them
2. During [implementation](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/implementation/SKILL.md) to verify fixes and verify that new features match specs
3. During [review](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/review-pr/SKILL.md) to prove to a human reviewer that code actually matches expected behavior

The verification is particularly valuable as a way of lessening code review burden. If you can see a video of a feature working, you are more likely to trust the underlying code (although you’ll still want to review the code to make sure the architecture is good, code is clean and secure, etc). Especially for pure UI changes that are low risk, having “proof” that a feature works from the user perspective is valuable and saves time.

Another less obvious benefit of computer use is that it lets an agent create a loop where it can debug changes on its own. This works especially well with [spec-driven development](https://www.warp.dev/blog/how-to-build-a-cloud-software-factory-add-spec-driven-development-skills) when you have a detailed [PRODUCT.md](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/spec/SKILL.md) that the agent is trying to implement. At every implementation pass, it can run computer use to see how close the implementation is to spec, and continue until it’s good. You’ll want to monitor costs here as it can be expensive, but it increases the likelihood of success.

As with prior posts, you can use the implementation on your own repos by following the [open-source demo](https://github.com/warpdotdev-demos/cloud-factory-demo). There’s a [skill you can install](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/oz-cloud-factory-demo/SKILL.md) and then invoke from your favorite coding agent to directly set up everything on your own repo:

npx skills add warpdotdev-demos/cloud-factory-demo --skill oz-cloud-factory-demo

## Add computer use verification to your agents

Diving into computer-use, we create a new skill called [verify-behavior](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/verify-behavior/SKILL.md) that defines how to use computer and browser use.

![Image](https://pbs.twimg.com/media/HO1PclBWsAA_c2E?format=jpg&name=large)

The [verify behavior skill](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/verify-behavior/SKILL.md)

The key aspects of the skill are:

- When to use computer use (desktop and mobile-native) vs. browser use (webapps)
- What to capture: video preferably, but screenshots are fine
- The two modes to use it in:
- **reproduce:** try to confirm that a reported bug occurs
- **verify:** verify a new behavior

In order for this skill to work, it needs to be run through a harness that supports computer and browser use. Since we are building a cloud software factory, this should be a harness that supports cloud agents. As with prior posts, we use [Warp’s cloud agent platform](https://www.warp.dev/oz), but there are others that support it as well.

At this point, you can run the [verify-behavior](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/verify-behavior/SKILL.md) skill directly, but it’s actually more useful to hook it into the other agents in your factory as a capability they can take advantage of. To do this, we will update the existing [Triage](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/triage/SKILL.md), [Review](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/review-pr/SKILL.md) and [Implementation](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/implementation/SKILL.md) skills to encourage them to use the verify-behavior skill when it will help them do their jobs.

For instance, we can update the [Triage skill](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/triage/SKILL.md) to try to reproduce bugs:

![Image](https://pbs.twimg.com/media/HO1PqlbWIAAvFeI?format=jpg&name=large)

And update the [Implementation skill](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/implementation/SKILL.md) to verify new features:

![Image](https://pbs.twimg.com/media/HO1PgZqWgAAeeUV?format=jpg&name=large)

Note that the verify-behavior skill uses cloud subagents. You can also do computer use locally, but it tends to be a worse experience unless the platform you’re using can test in the background (otherwise it steals focus and prevents you from doing anything while it runs). Warp and Codex do support this, but it still tends to be best in my experience to do computer use on a cloud machine where there’s no chance of the agent doing anything weird with the apps running on your machine.

For complex or new behaviors, we ask our orchestrator to fan-out to verify all of the user stories independently and in-parallel (your harness needs to support multi-agent orchestration for this to work). Computer use is typically single-threaded, so if you want better throughput, it’s best to fanout cloud agents across machines. This can get expensive, but it’s very cool, and reduces latency a ton.\\

## Computer use in action

I have a [demo repo](http://warpdotdev-demos/nano-banana-editor/) that I’ve used in a few of these posts that implements a simple agentic image editor using Nano Banana.

As a first user story, I’m going to show how you can use computer use to verify an issue. In this case, there’s a bug in the demo app: when an image is uploaded, its preview renders at thumbnail size rather than gallery size. The GitHub issue where this was reported is [here](https://github.com/warpdotdev-demos/nano-banana-editor/issues/46).

The agent here was able to run and produce screenshots of the broken behavior:

![Image](https://pbs.twimg.com/media/HO1PiXaXMAApVZJ?format=jpg&name=large)

The zero state for reproducing the issue

![Image](https://pbs.twimg.com/media/HO1P3gtXcAAebXu?format=jpg&name=large)

A screenshot showing the incorrect thumbnail

This is a trivial example, but for folks dealing with bug reports, having images automatically generated to verify the reproduction is a big unlock. You can see the raw cloud agent run that generated these images [here if you’re curious what the agent trace](https://app.warp.dev/session/cb8401f0-05c4-4418-a923-3fb016a1fd8d) looks like.

Moving on to a second use case, I asked an agent to implement a new feature in this repo end-to-end and verify it using computer use. The feature is described in this [issue](https://github.com/warpdotdev-demos/nano-banana-editor/issues/42) and is a relatively straightforward UI change, adding “clear” and “replace” controls to the image editor. There are clear acceptance criteria in the issue for the verifier to check against:

![Image](https://pbs.twimg.com/media/HO1P7CgXcAEMjfy?format=jpg&name=large)

Acceptance criteria for [verify-behavior](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/verify-behavior/SKILL.md) to check

The [PR](https://github.com/warpdotdev-demos/nano-banana-editor/pull/43) itself has screenshots showing the controls, and a link to a video proving they work.

![Image](https://pbs.twimg.com/media/HO1QFB0WAAAJ03G?format=jpg&name=large)

Here’s a [video](https://app.warp.dev/api/v1/agent/artifacts/019fb961-7a29-79bb-9e0d-b08e160077cd/download) the agent produced showing the feature in action end-to-end:

![Image](https://pbs.twimg.com/media/HO1QHpjXQAAHKTn?format=jpg&name=large)

It really is that simple – once you have the scaffolding set up you can use computer use to help lift the burden on PR review. In fact, for low-risk UI changes, you might decide that watching these videos is enough and you don’t need to look at the code at all.

To recap, we have created agents that:

1. [Triage new issues](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/triage/SKILL.md), optionally sending them to be implemented or spec’d
2. [Spec issues](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/spec/SKILL.md) from a product and technical perspective
3. [Implement the actual code](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/implementation/SKILL.md)
4. [Review the code](https://github.com/warpdotdev-demos/cloud-factory-demo/blob/main/.agents/skills/review-pr/SKILL.md) and improve review over time [with an observer loop](https://www.warp.dev/blog/self-improvement-loop-for-skills)

And now we’ve added a verification capability that all of the other agents can use to make sure the implementation is correct and allow a human reviewer to see a record of how the feature works.

These posts show how, with a simple set of primitives, you can start to build your own factory and truly automate more of your mundane work. The primitives are just:

- A cloud agent platform like [Warp](http://www.warp.dev/oz) that supports computer-use
- A workflow tool like GitHub Actions
- A set of agent skills that you and an agent can tune

My next post in this series will show how you can expand this factory with agents that monitor features and fixes after they are released and feed that monitoring back into the Triage phase, completing a basic factory loop.