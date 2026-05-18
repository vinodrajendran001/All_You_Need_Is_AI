
As the AI industry shifts its focus toward handling advanced and complex reasoning tasks, the limits of classic large language models (LLMs) are becoming evident. To address the reasoning bottleneck, researchers are revisiting "recursion," an older architectural concept that circumvents the need to build larger models.

The core of this shift involves transitioning from token-space reasoning to latent-space reasoning. Instead of generating text to "think," recursive architectures loop through continuous internal memory states. This enables them to operate much faster and at a fraction of the cost when solving deterministic problems.

**Recursion vs autoregressive models**

Classic LLMs are based on autoregressive Transformer models, which means they read the entire input sequence and produce the next token in a single forward pass. The benefit of this architecture is that it can be scaled. Adding more layers and training data continues to improve the performance of the model.

However, it hits a limit when handling problems that require complex reasoning before producing the answer. A model with a fixed number of layers runs out of computation steps for incompressible tasks.

![alpha_signal_image_1](https://alphasignal.ai/image/1779006002324-2nhhjl.png)

To handle these problems, LLMs rely on chain-of-thought (CoT) prompting to simulate reasoning. CoT forces the model to externalize its intermediate "thoughts" token by token. Those thoughts are then fed back to the model to allow it to continue its reasoning until it reaches the answer.

The problem with this approach is that the model is reasoning one token at a time. It can't compress its thoughts into more abstract representations. And this approach becomes slow and memory-intensive as the CoT sequence grows longer.

[Recurrent neural networks](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=30b0b31dfa42ffb1&lid=pCPsxktUg2kPS926&mid=905704a5-b0da-460a-8546-80668bb92684 "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=30b0b31dfa42ffb1&lid=pCPsxktUg2kPS926&mid=905704a5-b0da-460a-8546-80668bb92684") (RNNs), the predecessor to LLMs, avoided this by continuously looping through an internal memory state. Recursive models keep a fixed memory footprint and, in theory, they can increase their reasoning capacity by increasing the number of processing loops.

However, RNNs were abandoned because compressing information across multiple loops was very difficult. The main challenge of RNNs (and their variants such as LSTM) happened during training, where unrolling memory loops during training caused gradients to vanish or explode.

**Hierarchical reasoning models**

A recent architecture called the [Hierarchical Reasoning Model](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=30b0b31dfa42ffb1&lid=pCPsxktUg2kPS926&mid=905704a5-b0da-460a-8546-80668bb92684 "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=30b0b31dfa42ffb1&lid=pCPsxktUg2kPS926&mid=905704a5-b0da-460a-8546-80668bb92684") (HRM) brings recursion back with inspiration from human cognition. HRM uses "latent reasoning," where instead of generating "thinking tokens," the model reasons in its internal, abstract representation of the problem.

HRM solves the problems of classic recurrent models with two coupled, recurrent modules: a high-level (H) module for slow, abstract planning, and a low-level (L) module for fast, detailed computations.

The L-module acts as a fast loop that addresses a subsection of the problem, running multiple steps until it reaches a stable, local solution. It then passes the result to the slower H-module, which updates its overall strategy, and gives the L-module a new, refined sub-problem to work on.

![alpha_signal_image_2](https://alphasignal.ai/image/1779006067864-mw0zj3.png)

This recursive approach enables HRM to simulate the reasoning depth of a much larger network. HRM's efficiency shows itself in the numbers. A 27-million-parameter HRM achieved state-of-the-art results on ARC-AGI puzzles using only 1,000 training examples.

Operating entirely in latent space gives HRM a speed advantage over token-generating models. It delivers up to a 100x speedup in reasoning for deterministic tasks while outperforming zero-shot reasoning on larger LLMs.

**Tiny recursive models**

Samsung researchers built on HRM to create the [Tiny Recursive Model](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=30b0b31dfa42ffb1&lid=pCPsxktUg2kPS926&mid=905704a5-b0da-460a-8546-80668bb92684 "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=30b0b31dfa42ffb1&lid=pCPsxktUg2kPS926&mid=905704a5-b0da-460a-8546-80668bb92684") (TRM), testing whether the recursive loop itself was the core driver of performance. They found that HRM's biological arguments and hierarchical nesting could be removed entirely.

TRM replaces the hierarchical structure of HRM with a single, weight-sharing network of two layers. This brings the total model size down to 5 to 7 million parameters.

The researchers optimized TRM by using a full recursive loop. They showed that increasing recursive steps, rather than adding layers, maximized the model's ability to generalize.

![alpha_signal_image_3](https://alphasignal.ai/image/1779006204681-onnih1.png)

TRM outperformed both HRM and frontier models on reasoning benchmarks:

- The 5M-parameter TRM hit 87.4% accuracy on the Sudoku-Extreme dataset. (HRM scored 55.0% on the same benchmark while models like DeepSeek-R1 scored 0.0%.)
- TRM reached 45% accuracy on ARC-AGI-1 and 85% on difficult maze navigation tasks.

**Practical application of recursive computation**

Models like TRM and HRM operate as specialized reasoning engines. A TRM trained to solve mazes cannot draft a document or orchestrate a web search. They lack the semantic world knowledge of LLMs and serve as targeted compute modules.

However, they can serve as complements. For language-based and creative tasks, LLMs continue to be superior. But for complex or deterministic tasks, an HRM-like architecture offers superior performance at a lower cost.

Given their efficiency, they are especially suitable for latency-sensitive fields like embodied AI and robotics, or data-scarce domains like scientific exploration.

Latent-space recursion is also finding new ways to solve emerging problems in advanced AI applications. One example is multi-agent systems.

![alpha_signal_image_4](https://alphasignal.ai/image/1779006258227-lruoz7.png)

Current multi-agent frameworks suffer from token-space limitations. Agents communicate between each other through text tokens, which slows them down and increases inference costs.

A framework called [RecursiveMAS](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=30b0b31dfa42ffb1&lid=pCPsxktUg2kPS926&mid=905704a5-b0da-460a-8546-80668bb92684 "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=30b0b31dfa42ffb1&lid=pCPsxktUg2kPS926&mid=905704a5-b0da-460a-8546-80668bb92684") applies recursive principles to agent orchestration. Instead of generating text, agents pass their continuous latent representations to each other, collaborating internally and outputting text only at the end.

This architecture enables the agents to recursively reason internally and between them in latent representations without generating any text. It is as if the agents communicate telepathically in their mathematical language and only generate text when they want to provide their final answer.

Bypassing the text generation step changes the economics of agent deployment:

- It achieves up to a 2.4x end-to-end speedup in inference.
- It reduces token usage by 75.6% by the third round of recursion.
- It yields an average accuracy improvement of 8.3% across code generation and medical reasoning benchmarks.

Latent-space recursion is proving to be a scalable approach for building faster, cost-effective autonomous systems.

We are still in the early innings of rediscovering recursion. From HRM to RecursiveMAS, the field has made a lot of progress. As the AI industry moves to remove new bottlenecks, we can expect what is old to become new again.