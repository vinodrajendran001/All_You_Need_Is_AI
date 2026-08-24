---
type: raw-source
source_id: src-2026-08-24-bytebytego-ollama-vllm-sglang
title: Ollama vs vLLM vs SGLang
author: ByteByteGo
url: https://blog.bytebytego.com/p/ep223-ollama-vs-vllm-vs-sglang
published: 2026-08-22
captured: 2026-08-24
status: immutable
tags:
  - source/raw
  - inference
  - serving
  - agents
---

> Preserve the source body below this line as the canonical capture.
## Over 80% of container spend is wasted. Here’s how to fix it. (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!5rl9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c17fb96-10a5-4e04-8254-0a65b64d027b_2020x1200.png)

Many teams over-provision containers, underuse spot instances, and have no visibility into which pods are burning budget. Get the eBook from Datadog, which covers five practical optimizations for Kubernetes and ECS environments with specific techniques your team can apply today.

You’ll learn how to:

- Pinpoint idle containers, over-provisioned pods, and unused clusters draining your cloud budget.
- Right-size CPU and memory with resource requests, limits, and automated cost recommendations.
- Cut costs up to 90% with spot instances and savings plans and know exactly when to use each

---

This week’s system design refresher:

- Ollama vs vLLM vs SGLang
- How does Claude’s text watermark work?
- Top 12 Agent Skills You Should Know
- Git Workflow: Essential Commands
- Apache Kafka vs. RabbitMQ

---

## Ollama vs vLLM vs SGLang

To use open-weight models on your machine, you have three main options: Ollama, vLLM, and SGLang. But each engine handles requests differently. The diagram below shows the differences and the main techniques behind each engine.

![Image](https://substackcdn.com/image/fetch/$s_!kbZ3!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3efa7ef0-fa76-4e8c-9d50-540d1c42e7d3_2484x3002.png)

Ollama: A local user calls the OpenAI-compatible API, and requests line up in a FIFO queue. Then Ollama runs a pre-quantized GGUF model, a compressed format it pulls, and the response comes back to the user.

Ollama is best for local dev, prototyping, and laptop-scale hardware.

vLLM: Many users hit the server at once, and continuous batching slots new requests into the running batch instead of making them wait for it to finish. PagedAttention stores the KV cache, the memory a model keeps for tokens it has already processed.

vLLM is best for high-traffic serving, max GPU utilization, and thousands of concurrent requests.

SGLang: Agents and multi-turn chats send requests whose prompts overlap heavily. A prefix-aware scheduler routes them through the RadixAttention cache, a radix tree that reuses every shared prefix instead of recomputing it.

SGLang is best for AI agents and tool loops, multi-turn chats, and JSON/regex outputs.

---

## How does Claude's text watermark work?

Anthropic recently shared their intent to watermark text so they can identify AI-generated text. This post is based on my understanding of how it works.

![diagram](https://substackcdn.com/image/fetch/$s_!QmFs!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d8301f9-1ad3-44c7-9134-69e30888049c_1280x1546.jpeg)

LLMs produce text word by word. At each step, they generate probabilities for the next likely word. Instead of sampling randomly from those words, the watermarking trick changes which words are allowed to be picked.

How to watermark a response?

Step 1: The model produces probabilities for the next word.

Step 2: Normally a random number generator picks one of the good candidates. With watermarking, a keyed function takes a secret key plus the previous few words and decides which candidates are valid to pick from.

Step 3: This repeats for the whole response. Places where there are multiple plausible choices carry the watermark signal.

How to detect a watermarked text?

Step 1: For any candidate word in the text, we check whether it is a valid choice based on the secret key and the few preceding words. If the word is valid, that is counted as a match.

Step 2: Run this across the entire text. Watermarked text matches far more often. The overall match rate can be treated as an AI-generated score.

I’m personally getting quite annoyed by the false negatives from all these AI text detection techniques, especially for technical writing.

What's your thoughts on AI text detection? Do you think AI text detection is useful, or will it create more problems?

---

## Top 12 Agent Skills You Should Know

Agent skills are instructions and scripts that teach your LLM agent a new skill. The diagram below shows the 12 most-starred skill repos on GitHub as of August 2026.

![Image](https://substackcdn.com/image/fetch/$s_!6j7M!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d0d1c6c-a864-4b20-b1fc-2d86c8ad2fab_2484x3002.png)

1. Superpowers (obra/superpowers): This skill makes your agent plan before it writes code.
2. skills (mattpocock/skills): Matt Pocock's personal skill set makes your agent challenge your plan first. This is useful as agents can sometimes be too soft.
3. andrej-karpathy-skills: Multica AI distilled Karpathy's advice on AI coding pitfalls into one skill.
4. everything-claude-code: Skills that help you set up your coding agent. This is useful when you are starting Claude Code from scratch.
5. skills (anthropics/skills): This is Anthropic's official skills. It makes your agent capable of creating outputs like Word or PDF files.
6. ui-ux-pro-max-skill: This has instructions that teach your agent how to prevent AI-like designs.
7. caveman: Julius Brussee's skill makes your agent reply in short caveman speak.
8. ponytail: Dietrich Gebert's skill teaches your agent how to write code that is simple and clean.
9. agent-skills: Google's Addy Osmani included production-grade engineering practices in a skill
10. graphify (safishamsi/graphify): This skill converts a codebase into a knowledge graph, so an agent can navigate easier.
11. Understand-Anything: Egonex AI converts a codebase into visual maps to explore.
12. impeccable (pbakaus/impeccable): This skill makes an agent better at UI polish.

Over to you: Which skill would you add to this list?

---

## Git Workflow: Essential Commands

Git has a lot of commands. Most workflows use a fraction of them. The part that causes problems isn’t the commands themselves, it’s not knowing where your code sits after running one.

![Image](https://substackcdn.com/image/fetch/$s_!Fevp!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb1ae3fa-80a7-464d-97a2-869170caaa2f_2360x2960.png)

Working directory, staging area, local repo, remote repo. Each command moves code between these. Here’s what each one does.

- Saving Your Work: “git add” moves files from your working directory to the staging area. “git commit” saves those staged files to your local repository. “git push” uploads your commits to the remote repository
- Getting a Project: “git clone” pulls down the entire remote repository to your machine. “git checkout” switches you to a specific branch.
- Syncing Changes: “git fetch” downloads updates from remote but doesn’t change your files. “git merge” integrates those changes. “git pull” does both at once.
- The Safety Net: “git stash” is your undo button. It temporarily saves your uncommitted changes so you can switch contexts without losing work. “git stash apply” brings them back. “git stash pop” brings them back and deletes the stash.

---

## Apache Kafka vs. RabbitMQ

Kafka and RabbitMQ both handle messages, but they solve fundamentally different problems. Understanding the difference matters when designing distributed systems.

![Image](https://substackcdn.com/image/fetch/$s_!_5Is!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ebf5287-65fa-4db7-8490-54792fd1886c_2360x2920.png)

Kafka is a distributed log. Producers append messages to partitions. Those messages stick around based on retention policy, not because someone consumed them. Consumers pull messages at their own pace using offsets. You can rewind, replay, reprocess everything. It is designed for high throughput event streaming where multiple consumers need the same data independently.

RabbitMQ is a message broker. Producers publish messages to exchanges. Those exchanges route to queues based on binding keys and patterns (direct, topic, fanout). Messages get pushed to consumers and then deleted once acknowledged. It is built for task distribution and traditional messaging workflows.

The common mistake is using Kafka like a queue or RabbitMQ like an event log. They’re different tools built for different use cases.

Over to you: If you had to explain when NOT to use Kafka, what would you say?