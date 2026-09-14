DeepSeek released [V4.1-Flash](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=dbce367ad97e73c6&lid=1j5cVDqye4cQkzilB&mid=aed6268d-5c86-40e2-bb2f-c2bb6dd365d5 "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=dbce367ad97e73c6&lid=1j5cVDqye4cQkzilB&mid=aed6268d-5c86-40e2-bb2f-c2bb6dd365d5") on September 10 with an unusual combination of numbers. It is almost twice the size of V4-Flash but is 4x more efficient than its predecessor when it comes to KV cache storage.

The model is also competitive with leading proprietary models. At maximum reasoning effort, V4.1-Flash scores 40 on the [Artificial Analysis Intelligence Index](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=dbce367ad97e73c6&lid=PXFglVJRBNeCbxw5&mid=aed6268d-5c86-40e2-bb2f-c2bb6dd365d5 "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=dbce367ad97e73c6&lid=PXFglVJRBNeCbxw5&mid=aed6268d-5c86-40e2-bb2f-c2bb6dd365d5"), just behind Gemini 3.8 Flash High at 41, while having a quarter of the cost per task.

Sebastian Raschka called the release a “big overhaul” and argued that DeepSeek could have called it V5.

![alpha_signal_image_1](https://alphasignal.ai/image/1789312507559-swqmbb.png)

For engineers, the interesting part is how DeepSeek separated model capacity from the resources needed to serve it. Parameter count alone says less about production cost when architectures can change how much of the model runs on each token, how much context must stay in memory, and how much work is required to retrieve it. V4.1-Flash provides a useful case study in all three.

**A much bigger model**

DeepSeek-V4.1-Flash is a 552B Mixture-of-Experts (MoE) model (one shared, 384 routed with six shared experts per token) with a 40-layer Transformer backbone, divided into a 20-layer causal encoder and a 20-layer decoder (more on this in a bit). The model accepts text and images, generates text, and supports a context window of up to one million tokens.

(You might see other figures, such as 763B params. This is because V4.1-Flash has some other auxiliary components that are separate from the main backbone.)

**Prefill, decode and the KV cache**

When you send a prompt to an LLM, inference starts with “prefill.” The model processes all the input tokens and constructs the internal attention state it will need to produce an answer. Then comes “decode,” where the model generates new tokens sequentially while repeatedly referring back to the tokens it has already processed.

The KV cache connects these phases. Transformer attention creates key and value representations for previous tokens. Keeping those representations in memory saves the model from recomputing the entire history for every new output token.

KV cache efficiency matters for agents because their contexts accumulate. A coding agent might carry source files, conversation history, retrieved documentation and dozens of tool results. DeepSeek has steadily reduced the global KV footprint for these workloads, from around 48 KB per token in V3.2 to 3,514 bytes in V4-Flash and 890 bytes in V4.1-Flash.

![alpha_signal_image_2](https://alphasignal.ai/image/1789312382359-cppics.png)

**Causal Encoder-Decoder: make reading cheaper**

In a conventional decoder-only Transformer, every input token moves through the entire model during prefill. Each layer creates a new representation of the prompt and derives the keys and values that it will later need during generation. If the prompt contains hundreds of thousands of tokens, all of that work happens before the model produces its first output.

DeepSeek changes that with its Causal Encoder-Decoder (CED) architecture. The first 20 layers act as the encoder and process the prompt to create a contextual representation for each position. The second 20 layers are only used during the decode phase

As a result, DeepSeek-V4.1-Flash only uses 8B active parameters for each input token and 16B for each generated token. (V4-Flash activated around 13B for both.)

![alpha_signal_image_3](https://alphasignal.ai/image/1789312441190-e35f9e.png)

**SWA Bounded Replay: store less local context**

V4.1 also uses Sliding-Window Attention (SWA). Full attention lets each token look across the entire preceding context. SWA gives each layer a much smaller local view instead to reduce the costs of computing and storing KV cache.

SWA creates a problem when a cached agent session is restored and the local cache is missing. Reconstructing it exactly is expensive. Each layer depends on representations produced by the layer below, so the historical dependency expands as you move through the stack.

DeepSeek’s “Bounded Replay” limits that work. When reconstructing the KV cache, the serving system recomputes only the most recent tokens to rebuild the local window state instead of reproducing the full dependency chain.

Because SWA state can be reconstructed cheaply, DeepSeek does not need to persist that local KV state to SSD. Combined with the compression of the global cache, persistent KV-cache storage falls to roughly one-eighth of V4-Flash.

**CSA2: share the long-term memory**

SWA works for nearby tokens, but the model still needs access to older information. Full attention over a million-token is expensive because every new token needs to attend to all previous tokens.

“Sparse attention” reduces that work by finding a much smaller set of relevant historical tokens and running the expensive attention operation over that subset.

DeepSeek already used compressed sparse attention in V4. V4.1 introduces Compressed Sparse Attention 2 (CSA2), which addresses redundancy across layers. CSA2 allows layers to share both cache state and, in some cases, retrieval results.

It divides attention layers into three modes. A “Full” layer creates a fresh KV state and indexes relevant tokens. A “Reindex” layer shares the existing KV but performs its own search, allowing it to choose a different subset of the history. A “Reuse” layer shares both the KV and an earlier set of selected positions.

![alpha_signal_image_4](https://alphasignal.ai/image/1789312410183-j3jxj2.png)

Instead of every layer keeping a separate copy of the model’s history, multiple layers can treat compressed historical state as a shared memory resource. That removes one of the factors that makes KV cache grow so quickly in conventional architectures.

**Hierarchical indexing: make sparse attention cheap to search**

Before the sparse attention mechanism can attend to a few hundred useful positions, it has to find them. If every Reindex layer searched all one million tokens independently, the indexing stage itself could become the bottleneck.

DeepSeek solves this with a “Hierarchical Sparse Indexer.” The first Full decoder layer searches the wider history and creates a candidate pool of up to 2,048 blocks. Later Reindex layers search only inside this pool, and individual attention layers ultimately select up to 512 compressed positions.

![alpha_signal_image_5](https://alphasignal.ai/image/1789312338415-qfj5uw.png)

The important point is that the deeper search no longer grows directly with the full context. Once context windows reach hundreds of thousands of tokens, finding the relevant memory can become a substantial cost of its own. V4.1 bounds that cost as well as the size of the memory being searched.

Finally, DeepSeek-V4.1-Flash compresses the remaining main KV cache further by storing it in FP4 format (four-bit floating-point values), compared to FP8 for V4-Flash.

**What this means for inference costs**

At the full one-million-token context window, 890 bytes per token works out to roughly 890 MB of growing global KV state for one sequence. At V4-Flash’s 3,514 bytes per token, the equivalent is about 3.5 GB. The difference compounds quickly when a server is handling many long-running agent sessions.

DeepSeek summarizes the storage effect as about “one-quarter of V4-Flash’s HBM requirement and one-eighth of its SSD cache storage.” These differences matter most when applications maintain long prompts rather than starting every request from a short context.

The optimizations also show themselves in the cost structure. DeepSeek costs $0.30 per million input tokens and $1.20 per million output tokens. (Cache hits cost $0.006 per million tokens.)

V4.1-Flash shows why total parameter count is becoming a weaker way to estimate the economics of an LLM. For developers evaluating models for long-context and agentic applications, a more useful set of questions is emerging:

- How many parameters are active for input versus output?
- How many bytes of KV cache does each token add?
- What state must be persisted when a session pauses?
- Does attention and retrieval cost keep growing with context?

DeepSeek has attacked those problems at several levels in one model. The result suggests that there is still substantial performance to be found in the architecture between better GPUs and better application code.

If these techniques spread, the next generation of efficient models might not be defined by having fewer parameters. They might instead get better at deciding which parameters need to run, which memories need to survive, and which parts of a million-token history are worth looking at again.