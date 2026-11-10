AI agents (particularly coding agents) accumulate millions of tokens of context as they work with large code repositories and document libraries. At that scale, handling the attention values of the underlying model becomes tedious and expensive.

To address this bottleneck, researchers at Prefrontal AI and ETH Zurich have developed [Latent Sparse Attention](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=9cbcf695eecafe5a&lid=TRF9ADUsJcqzfxxV&mid=f4e5fa0f-601b-455c-a2a8-9f189464234b "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=9cbcf695eecafe5a&lid=TRF9ADUsJcqzfxxV&mid=f4e5fa0f-601b-455c-a2a8-9f189464234b") (LSA), a new technique that cuts the compute costs of processing long contexts in LLMs.

LSA is among a growing range of techniques for optimizing the attention mechanism in LLMs. However, it addresses a bottleneck in other sparse attention methods, which limits how many previous tokens a model examines.

LSA organizes attention values into clusters and groups to make it easier to search through them when mapping new queries. For example, in experiments on 10-million-token tasks, it reduced time to first token by more than 9 times a full-attention model and 2.2 times against a model using a popular sparse attention mechanism.

For developers building long-running agents and LLM applications that process large contexts, LSA offers a way to reduce inference latency.

**Why sparse attention still becomes expensive**

In a transformer, attention determines which parts of the context matter when processing a token. Each token has a query (what is it looking for), a key (what information is relevant), and a value (the information to obtain the answer). In full attention, every new query examines all preceding keys.

The full attention mechanism becomes very expensive as the model’s context grows. Doubling the context roughly quadruples full-attention computation.

This is particularly evident in the “prefill” stage, where the model must process the attention values of the entire input, which can become quite long for tasks involving large documents and codebases.

When generating new tokens, the “decode” stage, the model must also consult the entire context for each new token, which also becomes slow and expensive as the context grows.

![alpha_signal_image_1](https://alphasignal.ai/image/1794150107624-ixyttl.png)

Sparse attention solves the compute bottleneck by selecting a limited set of keys for each query. Methods such as DeepSeek Sparse Attention (DSA) use a smaller, cheaper indexer to score candidates. Other approaches group neighboring keys into blocks and score the blocks instead.

But if the indexer still examines every previous key or block, its prefill work continues to grow quadratically. For example, in a 10-million-token experiment with GLM-5.3-Flash, which uses a variant of DSA, selecting relevant tokens consumed 98% of an attention layer's prefill time.

**How latent sparse attention works**

LSA organizes attention values like a library. Rather than checking a description of every book, a query first examines groups of books, then retrieves books from the most promising groups. LSA creates these groups in a learned “latent space,” where compact numerical representations help identify similar keys.

The process has four main stages:

- **Represent:** Create compact representations of keys for selection.
- **Organize:** Organize keys into clusters based on their similarities, and store a representative vector, called a “centroid,” for each cluster.
- **Search:** Compare each query with cluster centroids and select the groups most likely to contain relevant information.
- **Attend:** Retrieve the original keys from those groups and perform conventional attention over them, alongside a recent-token window and a few initial tokens that remain accessible.

![alpha_signal_image_2](https://alphasignal.ai/image/1794150168874-zwbo0b.png)

The researchers propose two ways to search the clusters. “Flat search” compares a query with every cluster centroid. This is simple but the search tax grows with the number of clusters. “Tree search” optimizes search by organizing clusters into hierarchies and following promising branches.

There are also two ways to integrate LSA into models. Distilled LSA (D-LSA) adds a trained indexer to an existing model. The indexer learns to reproduce the model's attention preferences while the original model remains frozen.

![alpha_signal_image_3](https://alphasignal.ai/image/1794150073368-t5ymhv.png)

Native LSA (N-LSA) incorporates clustering during training, learning through the usual next-token prediction task without a separate teacher or index projections.

**What the experiments show**

The researchers evaluated D-LSA on Qwen-3.8-27B, which uses full attention, and GLM-5.3-Flash, which already uses sparse attention.

At 10 million tokens on an NVIDIA H200, D-LSA accelerated one GLM attention layer's prefill by 22.7 times and decoding by 4.6 times against the baseline sparse attention. For Qwen, prefill was 72.4 times faster than full attention.

In end-to-end serving across eight H200 GPUs, GLM's time to first token improved by 2.2 times, and its time per output token by 2.1 times. Qwen's time to first token improved by 9.2 times.

![alpha_signal_image_4](https://alphasignal.ai/image/1794150140170-kcl70k.png)

On RULER, a benchmark for long-context retrieval and reasoning, Qwen improved by scoring 63.9 at 10 million tokens against 59.9 for full attention. GLM, however, lost up to eight points at contexts of two to five million tokens relative to its sparse-attention baseline.

They tested N-LSA by training a 500-million-parameter hybrid model at up to 128,000 tokens. It matched full attention's validation loss and trained 1.6 times faster per attention layer and 1.24 times faster end to end. It also retained more long-context accuracy than other baseline attention methods such as sliding-window attention (SWA).

**What developers can do with LSA**

Prefrontal AI has published [the code](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=9cbcf695eecafe5a&lid=fQvILvtAbuk2iXlA&mid=f4e5fa0f-601b-455c-a2a8-9f189464234b "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=9cbcf695eecafe5a&lid=fQvILvtAbuk2iXlA&mid=f4e5fa0f-601b-455c-a2a8-9f189464234b") under the Apache 2.0 license, along with distilled indexer weights for Qwen and GLM, native-training checkpoints, evaluation tools, and an SGLang integration.

The first candidates are applications that repeatedly process very large contexts: coding agents with extensive histories, research assistants searching document collections, and systems that must connect facts across many files.

Compare LSA against existing attention methods using representative input lengths, first-token latency, output-token latency, and retrieval accuracy. Note that the reported gains become much smaller in shorter context tasks.

AI models and agents are becoming increasingly better at long horizon tasks. Accordingly, the underlying attention mechanisms must catch up to make sure the AI systems don’t grind to a halt. LSA is one of the techniques that can enable this future where agents work for hours and days at a time.