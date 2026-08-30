---
type: raw-source
source_id: src-2026-08-28-google-cloud-agent-delegation
title: "How agents can delegate better | Google Cloud Blog"
source: "https://cloud.google.com/blog/products/ai-machine-learning/how-agents-can-delegate-better"
author:
  - "[[Nenad Tomasev]]"
  - "[[Reshu Yadav]]"
published: 2026-08-21
created: 2026-08-28
description: "New research shows how delegation involves intelligence: adaptive negotiations, aligning on strict rules, contracts, and security guardrails. We’ll share four principles that emerged from our work, and how you might apply them to your own workflows."
tags:
  - "source/raw"
  - "clippings"
---
##### Nenad Tomasev

Research Scientist, Google DeepMind

##### Reshu Yadav

Applied AI Blackbelt, Google Cloud

##### Try Gemini Enterprise today

The front door to AI in the workplace

[Try now](https://business.gemini.google/?utm_source=cloud.google.com/blog&utm_medium=et&utm_campaign=FY26-Q2-GLOBAL-GLO27877-physicalevent-er-next26-mc-105752)

In any organizational behavior class, students will learn that effective delegation is among the most important skills for a seasoned leader. Getting meaningful work done involves careful coordination, starting with a subdivision of projects into manageable tasks, mapped onto the skills of the team, and assigned to the right people.

At Google Cloud, we’re learning a similar lesson when it comes to building and deploying AI agents in enterprise workflows. These workflows are best approached by multi-agent systems that can break apart and execute complex tasks. To do so, AI agents need to become good delegators.

To learn how, we turned to research from Google DeepMind. In their recent study titled [Intelligent AI Delegation](https://arxiv.org/abs/2602.11865), they prove how delegation itself involves intelligence: adaptive negotiations, aligning on formal contracts, and security guardrails.

This work opens up new opportunities for customers building AI agents that can communicate, share tasks, and coordinate towards set objectives. Today, we’ll share four principles that emerged from that work, and how you might apply them to your own workflows.

### Principle 1: Verify delegated work

If we are to permit AI to delegate tasks, we want it to do more than arbitrarily assign work. Agents should intelligently break down work into tasks that can be reliably verified. In our research, we call this "contract-first decomposition."

Like human delegation, this takes thoughtful deliberation. With people, this might mean a leader understanding their team’s strengths, and perhaps checking their work before it’s completed. For AI, there’s a similar learning curve. The orchestrating AI (the manager that sits atop a multi-agentic system) may consider multiple plans for how best to decompose and assign work, and keep decomposing sub-goals into smaller and smaller chunks until they become sufficiently simple to monitor and verify. Ideally, this should result in a plan where everything can be reliably graded. In reality, however, this may not always be possible to achieve.

Sometimes, it may be necessary to involve subjective assessment of whether work has been completed successfully, in line with expectations. Rather than being a problem, identifying such components helps us determine where human time is best spent, and how best to involve human expert judgement in oversight of agentic systems.

### Principle 2: Be smart about cost

The research framework helps us answer a question that keeps coming up with customers: Can this particular task be handled by a smaller, cheaper model? Enterprises are increasingly attentive to cost, and rightly so.

Finding the right balance between performance and budget is tricky. Taking a complex problem, like payroll, and handing it off to a lightweight model, might not be powerful enough for the results you want. On the other hand, it’s unnecessary to route simple tasks, like reformatting a spreadsheet, to a strong reasoning model.

According to the research, an agent that is intelligent about delegation would learn to recognize these scenarios, and match each task to the right tool or endpoint, to achieve the desired result and maximum reliability at a minimum cost. Use of model routing capabilities within API gateways is becoming a popular choice among customers, in addition to the alternative for using client-side proxies (such as LiteLLM).

You can learn more about model routing [here](https://docs.cloud.google.com/api-gateway/docs/model-routing-overview).

### Principle #3: Respect sensitive data

Many workflows handle private, sensitive data, and AI agents need to respect those boundaries and permissions. For example, if you’re deploying your orchestrator agent for payroll data, you know that agent should never pass along its full set of information to a sub-agent. This not only compromises security, but also bloats the context window for agents and degrades performance. An agent should grant the absolute minimum permissions required to complete that specific assignment, and nothing more.

The challenging part arises when needing to demonstrate, according to our first principle, that work has been reliably completed, without revealing private information. According to the research, advanced cryptography can help address this, via techniques such as zero-knowledge proofs. Zero-knowledge proofs enable one AI agent to prove to the other AI agent that a planned computation was performed correctly, without revealing the data itself. For example, an agent tasked with analyzing a sensitive dataset can generate a succinct non-interactive argument of knowledge that proves a specific property of the result. This enables the delegator to instantly verify the validity of the proof.

### Principles #4: Beware the zone of indifference

The zone of indifference is a term coined by Chester Barnard, an American business executive, in his 1938 book called The Function of the Executive. The zone is the space in which an employee will accept a task without questioning it. The task usually falls within their scope, so they unconsciously accept it. For example, if you’re a sales rep and your manager asks you to attend an upcoming pitch with a valued client, you probably wouldn’t push back or think too deeply about it.

As expressed in the research, current AI systems are defined by post-training safety filters and system instructions. As long as a request does not trigger a hard violation, the model complies. But when considering the emerging agentic web, this compliance might actually create a systemic risk. As mentioned in the research, “As delegation chains lengthen (? →? →?), a broad zone of indifference allows subtle intent mismatches or context-dependent harms to propagate rapidly downstream, with each agent acting as an unthinking router rather than a responsible actor.”

This has serious implications, because it means intelligent delegation requires “dynamic cognitive friction.” This means validating the information provided to agents to ensure that they are accurate, relevant, controlled and efficient.

This way, an agent can recognize when a request is ambiguous enough to warrant stepping outside their zone of indifference to challenge the delegator, or request human verification. Human participation and oversight similarly presume a degree of cognitive friction and active engagement, though this must be carefully managed, so as not to over-burden the users of the system. Human time is valuable and should only be invoked when necessary.

### Looking ahead

At Google Cloud, our long-term goal is to integrate agents naturally and efficiently into organizations, which will mean delegating to and from human experts and respecting boundaries. Together, we believe this will deliver business value beyond what individual agents can handle.

Ready to navigate the agentic web? Read Google DeepMind’s report paper, [Intelligent AI Delegation](https://arxiv.org/abs/2602.11865), on arXiv.

---

<sub>Note: A special thanks to Matija Franklin, Simon Osindero from Google DeepMind, and Vishal Agarwal, Andrea Morange from Google Cloud, for their contributions.</sub>

Posted in