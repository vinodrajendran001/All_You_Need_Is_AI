Consider a coding agent that has spent an hour exploring a repository, running tests and tracing a difficult bug. Now it must either switch to a stronger model to solve the problem or delegate part of the investigation to a specialist model working in parallel.

Both options introduce severe compute overhead. Researchers are exploring transfers through key-value (KV) caches, representations models build when reading input.

Nvidia has developed a way to reuse a cache across models, speeding up the handoff by up to 25 times. A separate technique, Cache-to-Cache (C2C), lets models share information without generating text tokens, reporting an average 2.5x speedup.

For developers building longer-running agents, these techniques address the growing cost of moving work between models.

**Why AI model handoffs become expensive**

There are two common reasons to hand off work in a multi-model system:

- **Model switching**: An existing session is transferred to a more capable model for difficult reasoning, or to a smaller model to cut costs on easier tasks.
- **Task delegation:** A subtask is given to a specialist model, such as reviewing a component or writing tests.

The handoff tax is different between different modes. In model switching, the new model needs to reprocess the accumulated source code, test results, conversation and earlier decisions. In delegation, the main tax becomes expensive when specialists exchange long reports or overlapping contexts.

The costs arise from how language models process input. During **prefill**, a model reads the prompt and computes the keys and values used by its attention mechanism. It stores these representations in a KV cache. During **decode**, it generates the answer token by token, consulting the cache instead of processing the entire preceding sequence from scratch.

As the agent reads more files, calls tools and receives new instructions, the tokens in its context expand and the KV cache grows. Switching models require repeating the prefill phase because the KV cache is model-specific and the new model can’t reuse the older model’s cache.

**Transfer the cache instead of rebuilding it**

Suppose our coding agent has built its context with Qwen3 14B and now needs Qwen3 32B to resolve a complex bug. Nvidia's [cross-model KV cache transfer technique](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=0848f5de78330a79&lid=EF7ohxAmGCDgFBOU&mid=e430119e-6f6e-40a0-bf29-57e5b96d1b47 "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=0848f5de78330a79&lid=EF7ohxAmGCDgFBOU&mid=e430119e-6f6e-40a0-bf29-57e5b96d1b47") maps the smaller model's KV cache into a form the larger model can continue from. The larger model can start generating its answer without recomputing the accumulated context again.

![alpha_signal_image_1](https://alphasignal.ai/image/1791722934224-pdz4ot.png)

The mapping reconstructs the receiving model's internal representations from the source model's through three components:

- **Layer selection:** Pick the source model's layers that best predict each layer in the receiving model.
- **Position handling:** Remove the position-dependent rotation applied to key representations, known as Rotary Position Embedding (RoPE), before translating them. This allows mapping longer contexts than those used in calibration.
- **Linear regression:** Fit the conversion using ridge regression, a statistical method that can be calibrated without costly neural-network training through backpropagation.

The team evaluated six smaller-to-larger model pairs from Qwen3, Llama 3.1 and Ministral 3 families, and calibrated the mapping layer with 500 sequences of 1,024 tokens.

![alpha_signal_image_2](https://alphasignal.ai/image/1791723023255-w5drpp.png)

In transferring a 32,768-token sequence from Qwen3 14B to 32B transfer, the KV cache transfer took 278 milliseconds against the near-7 seconds it took to compute the cache from scratch, a 25-fold speedup.

Using this method comes with an accuracy tradeoff that depends on the task, the models, and the number of mapping layers. The researchers propose a trained neural mapper that improves accuracy but adds complexity to the calibration stage.

**Cache-2-Cache transfer**

Now imagine a different handoff for our coding agent. It asks a code-analysis specialist to examine a failure while a code-writing model prepares a fix. The analyst must generate a report in text. The writer uses the report to process the analyst's findings.

Text handoffs introduce several costs. The analyst must produce its message one token at a time. The writer must then process that additional text. And a concise explanation may lose details that were represented internally, or describe them ambiguously.

![alpha_signal_image_3](https://alphasignal.ai/image/1791722998616-i17ors.png)

With [Cache-2-Cache (C2C)](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=0848f5de78330a79&lid=1vUdWVzHwwNd0SrUC&mid=e430119e-6f6e-40a0-bf29-57e5b96d1b47 "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=0848f5de78330a79&lid=1vUdWVzHwwNd0SrUC&mid=e430119e-6f6e-40a0-bf29-57e5b96d1b47") transfer, both models first process the same relevant context and construct their own KV caches. A **cache fuser** projects the first model's representations into a form the second can use and injects them into the second model's cache.

C2C still requires the receiver's initial prefill over the shared input. Its savings come from avoiding the sender's intermediate text generation and the receiver's processing of that message. It aims to transfer useful information about a context.

![alpha_signal_image_4](https://alphasignal.ai/image/1791722968054-sejew3.png)

C2C can also bridge models with different sizes, tokenizers and architectures. The team evaluated models from Qwen, Llama and Gemma families, including models specialized for code and mathematics. During training, both models remain frozen and only the fuser learns to combine their representations.

In reasoning and knowledge benchmarks, C2C improved accuracy by approximately 3.1–5.4 percentage points over text-based communication and reported an average latency speedup of about 2.5 times.

In one measured handoff, generating an 80-token message took 1,312 milliseconds while the cache-fusion step took roughly 90 milliseconds. Full latency also includes input processing and answer generation.

It is worth noting that C2C requires a trained fuser and direct access to internal caches. A poorly matched or weaker source model can feed the receiver misleading information.

In an exploratory two-agent math workflow, a hybrid approach that combined a textual interpretation with cache fusion scored higher than either alone. This suggests direct cache communication may complement text rather than replace it.

**What this means for agent developers**

For our coding agent, the appropriate optimization depends on the handoff. A long session moving between compatible models may benefit from cache conversion. Specialist agents exchanging detailed findings may benefit from cache-based communication. For narrow tasks, short text handoffs may suffice.

These techniques apply to teams that have access to model weights and internal caches. Developers working through closed-model APIs cannot insert these transformations. The work also fits into a broader effort to shrink and manage the KV cache through compression, selective eviction and more efficient attention.

As coding agents take on longer tasks, the cost of remembering what they have done and passing that information along will become harder to ignore. Better orchestration will increasingly depend on avoiding unnecessary computation and communication between model calls.