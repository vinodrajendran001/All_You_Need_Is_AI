---
title: "AI 101: What is Recursive Self-Improvement?"
source: "https://www.turingpost.com/p/what-is-recursive-self-improvement"
author:
  - "[[Alyona Vert.]]"
published: 2026-06-18
created: 2026-06-18
description: "Recursive self-improvement is the idea of AI improving the systems that create future AI. Here’s what RSI means today and why it matters."
tags:
  - "clippings"
---
[AI 101](https://www.turingpost.com/t/ai-101)

![](https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,quality=80,format=auto,width=720,onerror=redirect/uploads/asset/file/60d1206c-8787-4919-b46e-caa442e8a3c6/RSI.png)

How AI systems are beginning to automate coding, experiments, evaluation, and research workflows ‒ and why Anthropic, Recursive, and Sakana AI show the first real steps toward AI that improves AI

## What is Recursive Self-Improvement?

Recursive self-improvement or RSI, is the idea of an AI system improving the process that creates future AI systems. This guide explains what RSI means today, how it differs from self-improving agents, and why Anthropic, Recursive, and Sakana AI are early signals of this shift.

**TL;DR:** Recursive self-improvement is when AI systems help improve the next generation of AI systems. Today’s RSI is mostly about automating coding, experiments, evaluation, and research workflows – not fully autonomous AI building stronger foundation models without humans.

When we started seeing **Recursive Self-Improvement (RSI)** show up more often, it felt familiar: like the early days of [reasoning models](https://www.turingpost.com/p/reasoningmodels), [test-time scaling](https://www.turingpost.com/p/testtimecompute), and the [reinforcement learning](https://www.turingpost.com/p/rlguide) wave, when an old idea suddenly became the next research frontier.

This time, the direction is **AI that builds AI.**

So what is Recursive Self-Improvement?

At its core, it is the idea that AI can participate in its own development. Instead of only helping researchers write code or analyze results, the system becomes part of the research loop itself: proposing ideas, running experiments, evaluating outcomes, generating training data, improving components, and helping design the next iteration.

This does not make researchers irrelevant. If anything, it changes their role. As AI takes over more of the research loop, humans increasingly focus on setting goals, validating results, and governing the self-improvement process. Instead of spending time on every experiment and implementation detail, researchers can spend more time deciding which directions are worth pursuing and which results can be trusted.

But let’s ask more realistic questions: How much of the AI development loop can AI eventually handle on its own, and which parts should stay under human control?

Today we are at the very early stage of RSI. And the most outstanding steps just came from Anthropic, Recursive, and long-lasting Sakana AI’s idea to create better loops instead of wasting more compute.

Let’s discuss what they have brought and what AI can actually automate today.

**In today’s episode**:

- *The echo of Von Neumann*
- *So what is recursive self-improvement, and how does it work?*
- *The difference between self-improving agents and RSI*
- *Sakana AI and the foundation for RSI*
- *Anthropic’s achievements in coding automation*
- *Recursive’s automated AI research system*
- *Conclusion: Where the first steps in RSI lead us*
- *Sources and further reading*

## The echo of I.J. Good and Von Neumann

As we often do, let's look backward to see where the idea is heading. Recursive self-improvement is not an invention of modern AI labs, and its clearest ancestor is not the one usually named.

The instinct is to reach for John von Neumann, who in the 1940s sketched a theory of [self-reproducing automata](https://cba.mit.edu/events/03.11.ASE/docs/VonNeumann.pdf?utm_campaign=ai-101-what-is-recursive-self-improvement&utm_medium=referral&utm_source=www.turingpost.com): machines that could construct copies of themselves. His real contribution was subtler than replication. He identified a threshold of complexity below which a machine's offspring must come out simpler than its parent, and above which a machine could, in principle, build something at least as complex as itself. That threshold is the substrate the entire conversation still rests on. But Von Neumann was asking whether a machine could reproduce, not whether it could improve.

The improvement question belongs to Irving John Good. In 1965, in [Speculations Concerning the First Ultraintelligent Machine,](http://incompleteideas.net/papers/Good65ultraintelligent.pdf?utm_campaign=ai-101-what-is-recursive-self-improvement&utm_medium=referral&utm_source=www.turingpost.com) Good defined an ultraintelligent machine as one that could surpass every intellectual activity of any person – including the activity of designing machines. From there the conclusion is almost mechanical: such a machine could design a better machine, which could design a better one still, the runaway he named the intelligence explosion. Good called the first such machine the last invention humanity would ever need to make, on the condition that it stayed under our control.

RSI brings this old idea into today’s AI development loop. A model writes code that improves training infrastructure. An agent proposes experiments that improve post-training. A research system tests model changes, remembers what worked, and chooses the next branch. We are not (yet!) watching AI independently design a stronger successor from scratch. But we are already seeing the first pieces of the improvement loop move from human hands into machine hands.

## So what is recursive self-improvement, and how does it work?

Before AI became part of everyday work for developers, researchers, and business teams, building software systems mostly meant writing the code, documentation, tests, and infrastructure by hand. Then AI tools became useful enough to help with small parts of these workflows, especially coding. By the end of 2025, agent capabilities had moved further: agents could edit files, work through larger tasks, use tools, and handle more steps without constant human instruction.

Today, agents can plan and execute longer tasks, improve their own outputs, and in some cases delegate work to other agents. Systems such as OpenClaw and Hermes point in this direction. But the broader ambition is bigger than workflow automation. **The industry is moving toward AI systems that can help build and train future AI systems**

And that seems almost impossible without, that’s right, **recursive self-improvement**: an AI system capable of designing and developing its own successor. Or, in the phrase that may scare a layperson: **AI that builds AI.**

But lay aside the doomism. RSI opens the door to a new phase of AI-powered research, one that could fundamentally accelerate progress in science and technology.

**Research is a loop: propose an idea → implement it → run the experiment → validate the result → learn from it → and choose what to try next.**

![](https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,quality=80,format=auto,width=720,onerror=redirect/uploads/asset/file/a6058add-3505-4c55-89e1-434359eb7eee/Research_is_a_loop.jpg)

Then repeat, repeat and repeat. Through numerous attempts only a couple or just one variant would really work. Or none. RSI system’s task is to automate these stages.

In an ideal version, RSI systems would operate as automated research assistants inside a closed-loop experimentation pipeline. But realistically, this is still an early-stage direction. **RSI is only beginning to enter different parts of the AI development loop, and most of what exists today is post-training or workflow-level rather than foundation-model-level.** The term can suggest AI systems inventing entirely new neural network architectures on their own, but current work is usually closer to automated ML engineering and automated AI research.

And there is one more clarification to make…

## The difference between self-Improving agents and RSI

Before RSI became the focus of attention, researchers spent years building and exploring self-improving agents. Are these two concepts the same, since they both revolve around "self-improvement"? Actually, no.

The key technical distinction is that today’s “self-improving” agents mostly improve their workflows– prompts, tools, memory, code, and task execution– while **true recursive self-improvement would improve the model-building process itself:** data, architectures, training methods, evaluation, and deployment of a stronger successor.

The recursive aspect appears when the outputs of one generation of AI systems are used to create the next generation with less and less human involvement. There is the degree of recursion:

- Current systems are usually: Human → AI research assistant
- A stronger RSI system becomes: Human → AI researcher → improved AI researcher
- And the strongest form would be: AI researcher → improved AI researcher → even better AI researcher

From this perspective we can see that RSI is not a binary capability but a spectrum, and today's systems are only automating parts of the loop rather than the entire loop.

![](https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,quality=80,format=auto,width=720,onerror=redirect/uploads/asset/file/ff748b38-d261-445d-83e1-e6aced77f5fe/ChatGPT_Image_Jun_17__2026__04_54_19_PM.png)

Now we’ll walk you through several most outstanding RSI variants. Read along, because you want to know about them and be ahead. From now on, RSI is on an acceleration path.

If you prefer videos, we also talk about RSI in this episode of Attention Span

![](https://www.youtube.com/watch?v=RB8vjn1QPeM)

**FAQ**

**What is recursive self-improvement in AI?**

Recursive self-improvement, or RSI, is the idea that an AI system can help improve the systems that create future AI. In its strongest form, one AI researcher would design, test, and build a better AI researcher with less and less human involvement.

**Is recursive self-improvement already happening?**

Only in early and limited forms. Today’s systems can automate parts of coding, experimentation, benchmark optimization, and research workflows, but they are not yet fully designing and training stronger foundation models on their own.

**What is the difference between self-improving agents and recursive self-improvement?**

Self-improving agents usually improve their own workflows, prompts, tools, memory, or code. Recursive self-improvement goes deeper: it improves the model-building loop itself, including data, training methods, architectures, evaluation, and future AI systems.

**Why does recursive self-improvement matter?**

RSI matters because it could accelerate AI research by automating more of the research loop: proposing ideas, implementing experiments, testing results, and selecting the next direction. The promise is faster progress; the risk is losing human oversight over increasingly automated improvement loops.

**What are the risks of recursive self-improvement?**

The main risks are unreliable evaluation, reward hacking, benchmark overfitting, unsafe autonomy, and weak human supervision. If AI systems optimize for measurable progress without understanding broader consequences, they may pass tests while failing in real-world deployment.

![](https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,quality=80,format=auto,width=720,onerror=redirect/uploads/asset/file/b8079204-0aa8-4e27-aee7-6268ebd4dcd4/TP-footer-1200x300.png)