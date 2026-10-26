AI agents might carry out sessions or conversations that last for a long time. For example, a customer-support agent might interact with a client for six months.

When asked about an earlier purchase or promise, should it search the original conversations or rely on a structured memory system that extracts important details? The answer affects the agent's accuracy, inference costs and maintenance.

[MemoryTax](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=b29e226b9b63ceed&lid=OKuaNJ00kAKqVVA6&mid=78bc441f-4142-4f0e-9983-3611b600e38b "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=b29e226b9b63ceed&lid=OKuaNJ00kAKqVVA6&mid=78bc441f-4142-4f0e-9983-3611b600e38b"), a new study by Shanghai Jiao Tong University, tests seven ways agents can access past conversations. The findings suggest that weaker models can benefit from structured memory but stronger models often do better when given the raw information.

For developers, the question is when building a separate memory layer earns back its cost.

**What MemoryTax tested**

The study used one conversation from [LoCoMo](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=b29e226b9b63ceed&lid=wzxCs6vE4wcP7Mhv&mid=78bc441f-4142-4f0e-9983-3611b600e38b "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=b29e226b9b63ceed&lid=wzxCs6vE4wcP7Mhv&mid=78bc441f-4142-4f0e-9983-3611b600e38b"), a benchmark for long-term conversations  with hundreds of turns. The experiment tests the agent’s ability for factual recall, connections across messages, and the sequence of events.

![alpha_signal_image_1](https://alphasignal.ai/image/1792938942235-7hm7f5.png)

They tested seven different memory approaches paired with three models: GPT-4o-mini, GPT-6 Luna, and Claude Opus 5.5.

The seven approaches fall into several groups:

- **Full context:** The entire conversation is inserted in the model's prompt. This avoids building a separate memory store but repeatedly processes the same history.
- **Retrieved memory:** The system uses an algorithm like BM25 to search the raw history and retrieve the parts that are relevant to the question.
- **Precomputed memory:** These are memory consolidation techniques like [Mem0](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=b29e226b9b63ceed&lid=Y79JvByEEEusIbZT&mid=78bc441f-4142-4f0e-9983-3611b600e38b "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=b29e226b9b63ceed&lid=Y79JvByEEEusIbZT&mid=78bc441f-4142-4f0e-9983-3611b600e38b"), which uses a model to extract and update useful facts, then retrieves them later. Another is [Zep](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=b29e226b9b63ceed&lid=D6peQ6royabkl4dH&mid=78bc441f-4142-4f0e-9983-3611b600e38b "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=b29e226b9b63ceed&lid=D6peQ6royabkl4dH&mid=78bc441f-4142-4f0e-9983-3611b600e38b"), which builds a knowledge graph that links different elements in the conversation history.
- **Agent-directed search:** A harness like Pi, Codex, or Claude Code receive the original conversation as a JSON file. The model could choose which parts to inspect using its tools.

The researchers used GPT-4o-mini to judge correctness of answers.

**What they found**

**1. Stronger models change memory economics**

With GPT-4o-mini, Mem0 achieved the highest accuracy among all methods. With GPT-6 Luna, full context had the best outcome. Claude Opus 5.5 reached 95% with either method. Memory extraction helped the weakest model in this test, but offered no accuracy advantage with the stronger ones.

![alpha_signal_image_2](https://alphasignal.ai/image/1792938903578-nqk5wj.png)

One more thing to consider is the upfront cost of each method. For example, with GPT-4o mini, answering all 152 questions with full context cost $0.43 while building Mem0's store alone cost $0.56. However, once built, Mem0 answered questions more cheaply. With the same history, Mem0 would break even with full context after 372–596 questions, depending on the model.

For example, A customer-service system making repeated queries about a stable account might recover the memory-building costs. An agent that reads a conversation once probably would not.

**2. Memory is limited by what gets preserved**

To isolate memory quality, the researchers let different models read stores built by other models. The key finding is that the model that writes the memory dictates the final quality of the answer.

When GPT-4o-mini built a Zep graph, it scored 43% reading that graph. With the same memory graph, Claude Opus 5.5 reached only 45%. But when Opus built and read the graph, accuracy rose to 87%. Mem0 showed a similar pattern.

![alpha_signal_image_3](https://alphasignal.ai/image/1792938821737-hwpise.png)

How can this happen? Imagine a support agent extracting a summary of a complaint but omitting the purchase date. A later warranty question requires that date. A stronger answering model cannot reconstruct it from the summary.

The practical safeguard is to keep original records available, even when extracted facts or graphs make common queries faster.

**3. Model-directed search can lower costs**

Claude Opus 5.5 with the minimalist Pi harness answered 99% of questions for $6.95, versus 95% for full context at $17.84. Instead of rereading everything, Pi used tools to locate relevant passages. As a result, it processed about 10,000 input tokens per question as opposed to 28,900 with full context.

![alpha_signal_image_4](https://alphasignal.ai/image/1792938874361-283h45.png)

One caveat to consider is that coding agents could read photo captions unavailable to the other methods. On 88 questions whose evidence did not involve photos, Pi scored 100% and full context 99%.

The choice of agent also mattered. On the same Opus model, Codex cost $25.41 and Claude Code $28.41, with 98% and 97% accuracy. This echoes [the HarnessTax](https://alphasignal.ai/news/understanding-the-harness-tax-behind-coding-agents "https://alphasignal.ai/news/understanding-the-harness-tax-behind-coding-agents") study that we covered recently, which found up to fivefold cost differences between coding-agent harnesses using the same model without comparable gains in success.

**How developers should choose agent memory**

It is worth noting that the study is not very comprehensive. The results come from one LoCoMo conversation, one run per configuration and a GPT-4o-mini judge. Also, the entire conversation history fitted within the models' context windows. So consider the study as a testing framework.

Developers can turn its findings into four practical checks:

- **Start with full context.** If the history fits in the model’s context and costs are acceptable, measure accuracy and spending before adding more engineering layers.
- **Add retrieval when context becomes unwieldy.** A coding agent searching the full history can fetch relevant passages instead of loading everything into each prompt. Test lexical search and model-directed file search first.
- **Precompute memory where reuse warrants it.** A CRM agent that repeatedly checks account ownership and past commitments might benefit from extracted facts or a memory graph.
- **Benchmark the complete stack.** Compare model-and-harness combinations on real tasks. Record accuracy, latency, tokens, cost per task and total cost over multiple tasks reusing the same history. Include memory construction and updates.

As models get better at finding information, you can spend less effort deciding in advance what the agent should remember and instead give it reliable access to original records. Then, design the memory layer that improves performance or reduces the cost of real work.