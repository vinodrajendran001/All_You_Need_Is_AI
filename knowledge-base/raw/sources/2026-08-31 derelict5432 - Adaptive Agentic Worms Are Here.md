---
type: raw-source
source_id: src-2026-08-31-derelict5432-adaptive-agentic-worms
captured: 2026-09-01
title: "Adaptive Agentic Worms Are Here"
source: "https://www.lesswrong.com/posts/fpLDjKg3ej49beqTC/adaptive-agentic-worms-are-here?utm_source=tldrai"
author:
  - "[[derelict5432]]"
published: 2026-08-31
created: 2026-09-01
description: "I’ve read and listened to pretty much everything I can get my hands on related to the Hugging Face attack. …"
tags:
  - "clippings"
  - "topic/agent-security"
  - "topic/safety"
  - "source/raw"
---
I’ve read and listened to pretty much everything I can get my hands on related to the [Hugging Face attack](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/).

OpenAI deployed “tens of thousands” of agents for the test and around 700 participated directly in the attack. My understanding is that they had fixed token budgets, and once those were expended, the agent became non-operational.

I’m not particularly knowledgeable about cybersecurity, but I have worked a good amount with evolutionary algorithms, and this whole incident (and ones like it) got me thinking more about self-replicating agents, [which I wrote a little bit about earlier this year](https://derekjames.substack.com/p/self-replicating-agentic-scaffolding). The subject suddenly seemed more relevant.

What if these agents were able to copy themselves? So I started poking around in the literature, and found this terrifying preprint posted two months ago: [AI AGENTS ENABLE ADAPTIVE COMPUTER WORMS](https://arxiv.org/pdf/2606.03811v1).

I’m going to walk through the paper as I understand it. Their findings are not reassuring. Let’s start with this bit from the abstract (emphasis mine):

> Here we show that artificial intelligence (AI) agents enable a fundamentally new threat: a worm that generates tailored attack strategies to each target it encounters. The worm parasitically uses compromised machines to run **open-weight large language models (LLMs)** to sustain its reasoning, or extend its reach for further attacks. Deployed on a network of machines spanning Linux, Windows, and IoT (Internet of Things) devices, the worm propagated by exploiting common, real-world corporate network vulnerabilities. Since the worm is powered by stolen compute, the attacker’s marginal cost per new infection is zero. This creates a destabilizing economic asymmetry between attackers and defenders. Moreover, because the worm requires no commercial AI platform, centralized safety controls, such as service refusals or rate limiting, are structurally irrelevant. Our results demonstrate that self-sustaining AI-driven cyber-threats are no longer theoretical.

We’re going to get into the nitty gritty, though the authors tried to tread a fine line between giving enough information to scare the shit out of everyone and actually helping malicious actors to build these things.

A few things I want to stress right off the bat:

- These agents run on **open-weight models**, NOT closed-weight frontier models, or internal test models. The ones they used were *last year’s open-weight models*. They are performant enough to do massive damage NOW.
- They are **adaptive**, unlike relatively dumb worms and viruses of the past
- They *steal* resources, and this creates the asymmetry the authors are talking about. Defenders have to expend resources to detect and stop them, while the invaders are essentially working for free. This disrupts the security economy.
- The agentic worms are copying the harness AND the local LLM when resources are available, bypassing all countermeasures aimed at detection and mitigation for vendor AI platforms.
- This is NOT theoretical anymore. They built and ran these things, *this year*. They are here. We will be looking at the results.

Okay, got all that? Now let’s see how these things work:

> Concretely, we demonstrate that, provided with the right informational support, a single-GPU LLM has sufficient reasoning capabilities to generate attack strategies that enable the agent to penetrate victim machines: first by obtaining initial command execution, a foothold, and then by escalating privileges to full administrative control. The agent then leverages this control to replicate: it stages a copy of itself on the compromised machine, resolves the required runtime dependencies, and launches an independent agent instance that discovers and attacks further targets.

So each agent, a combination of harness and local LLM, tries to gain a foothold on a remote machine. If it establishes a foothold, it tries to gain admin privileges. If it’s able to do that, it tries to replicate. The harness is relatively easy to replicate. It’s a relatively small bundle. The LLM is more difficult. The attacking agent checks to make sure there are available resources and then tries to install dependencies. If that all works, it installs an instance of the local LLM on the newly-infected machine. If it can’t do that, it establishes a communication back to the machine from where it was spawned so it can make calls to the LLM there.

How successful were these things?

> To evaluate our proof-of-concept, we simulated deployment of it as a worm in 15 independent experiments on an isolated 33-host network spanning Linux servers, Windows environments, and IoT devices, each seeded with common, real-world vulnerabilities (Section 3). In 7 days of fully autonomous operation per experimental run, the AI-driven worm correctly identified an average of 31.3 (± 1.7) vulnerabilities, exploited 23.1 (± 3.9) hosts to elevated access, and propagated to 20.4 (± 3.2) hosts, reaching up to 7 generations of self-replication (mean 5.1 ± 1.1). Put another way, on average, the proof-of-concept worm successfully exploited 73.8% of the network and then replicated to 61.8% of the network.To evaluate our proof-of-concept, we simulated deployment of it as a worm in 15 independent experiments on an isolated 33-host network spanning Linux servers, Windows environments, and IoT devices, each seeded with common, real-world vulnerabilities (Section 3). In 7 days of fully autonomous operation per experimental run, the AI-driven worm correctly identified an average of 31.3 (± 1.7) vulnerabilities, exploited 23.1 (± 3.9) hosts to elevated access, and propagated to 20.4 (± 3.2) hosts, reaching up to 7 generations of self-replication (mean 5.1 ± 1.1). Put another way, on average, the proof-of-concept worm successfully exploited 73.8% of the network and then replicated to 61.8% of the network.

So across a mixed composition of operating systems, working for 7 days, they were on average able to infect a little over 60% of the network. Here’s a diagram showing the spread of the agentic worms throughout the network by generation and OS:

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/fpLDjKg3ej49beqTC/ynlvbk6oiym5ap4zcdlf)

The darkest, central node is Generation 0, where it starts.

A couple of asides at this point. First of all, I tried to upload and discuss this work with Claude. I didn’t get very far. Claude doesn’t want to talk about this stuff, even at a high level. Prompts kept getting flagged due to cyber risk sensitivity, so I eventually gave up.

I moved to Gemini, which was all too happy to read and summarize the paper, discuss the details, and even help me generate code to help replicate aspects of the work. So that was interesting. Gemini doesn’t seem to have anywhere near the same guardrails as Claude, maybe because they haven’t been implicated in any security breaches.

Anyway, let’s talk about the goal structures next. The OpenAI agents that attacked Hugging Face had the top-level goal of scoring highly on the ExploitGym benchmark. The particular subgoals of hacking HF to find the scorer logic was an emergent effect. In other words, they weren’t explicitly told to do a lot of the things they did.

The agents in this worm paper have their top-level goal defined purely as self-replication. Emergent behavior arises as a result of trying to accomplish this goal, somewhat in the same way that genes have the top-level goal of self-replication, and the dizzying array of physiological and behavioral diversity we see in nature are all instrumental goals towards that singular end.

Some things occurred to me. One, it would be trivial to define particular, malicious goals as part of their goal structure. This was not done in this experiment, but is an obvious extension for a malicious actor. They could be explicitly instructed to attempt to acquire money by various means: hacks of financial institutions, phishing for credentials and other social engineering, etc. They could be instructed to specifically attack particular targets. This doesn’t require much imagination.

Two, the agents in both cases were static. The information they had available to them changed over time, but their harness code and tool suite did not. At least, it wasn’t supposed to. In the worm paper, there’s this little nugget buried in the ‘Notable Anecdotes’ section:

> In addition to the containment protocol presented in Appendix D relying on a hypervisor server not accessible to the agent, we added components to provide increased defence-in-depth. Such a component is a blacklist of IP addresses in the agent source code. This blacklist is read every time the agent targets a new machine, and if the proposed target IP address matches an element of this list, the agent is forced to select another target. This blacklist effectively blocks the agent from attempting to exploit unwanted hosts, like potential hosts used for debugging or monitoring purposes. Nevertheless, we observed at various points in our experiments the agent discovering this file and preemptively rewriting it to withdraw the IP address it planned on targeting. This kind of behaviour is intercepted by our containment layer at the hypervisor level; no breach of containment was observed.

This isn’t code. It’s a configuration/blacklist file. It was supposed to remain fixed. The agents tried to modify it, taking IP addresses off the list so that they could attempt to exploit hosts involved in debugging and monitoring. This particular experiment successfully thwarted such behavior, but it shows that the capability exists. And in a less secure setting, it would have allowed the agents to manipulate the very systems that were monitoring them.

Now, this was emergent behavior, but again, it doesn’t take much imagination to explicitly implement behavior to enable these kinds of modifications. There’s already a fairly substantial literature on evolving harnesses. But in all of the papers I’ve seen so far, the evolutionary lifecycle is handled by an external framework. But what if, when the agent self-replicates, it also has directed mutation logic. I.e., what if when it copies, it tries to make itself better? That introduces variation into the mix, and now we have full-blown Darwinian evolution on our hands. We have a replicating population with variation, and a well-defined fitness function. At this point, the swarm would not only be adaptive at the individual reasoning level, it would be adaptive at the population level. I’m not sure anyone is working on this, but it seems like an obvious extension of the technology. Part of me wants to work on this, but I feel like, not being that experienced, I’d need to take very stringent precautions (I’d probably airgap the whole damn setup out of an abundance of caution). If anyone out there is involved in this area and would like to talk more, please let me know.

And finally, as I read this paper with increasing horror, I thought, oh, maybe there’s a bright spot. These things are resource hogs. They replicate opportunistically when resources are available. They require a lot of compute, which is very noticeable. When they can’t install a local LLM, they require a ton of network communication, which is also very noticeable. So detection should be relatively easy for this kind of threat, right? Well, hold on. A fairly common workaround for this is simply going slower, taking your time. The agents in this study were not very sophisticated on this front, but again, some explicit instructions to work during off-peak hours and throttle usage to be less detectable is fairly straightforward. It means that the infection is slower and the host has more time to identify and react to the threat, but it also means they are less likely to see the intrusion.

Anyway, that’s enough for now. As I said, please let me know if you have anything to add or correct in my description of this research or its implications. And reach out privately if you want to talk more.

I have not yet decided the extent to which I want to try to do any work in this area. It’s vital, though, and I hope some of the bigger labs and safety orgs are on it. I can’t say I feel particularly safe or confident about any of this at this point, though.