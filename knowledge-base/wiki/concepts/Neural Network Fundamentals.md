---
type: concept
created: 2026-05-18
updated: 2026-06-23
tags:
  - concept
  - neural-networks
  - pytorch
  - optimization
  - backpropagation
source_ids:
  - src-2026-05-18-pocketflow-tutorial-docs
  - src-2026-05-18-hanfang-pytorch-practice
  - src-2026-05-21-leetcode-templates
  - src-2026-06-03-fareed-khan-train-llm-from-scratch
  - src-2026-06-23-mayank-pratap-singh-diffusion-visual-breakdown
status: active
---

# Neural Network Fundamentals

## Definition

Neural network fundamentals are the small set of ideas that make modern deep learning work: tensors, linear layers, forward passes, loss functions, gradients, backpropagation, and iterative parameter updates through optimizers.

## Why it matters

This vault has several higher-level pages about LLMs and RL, but those topics depend on a compact substrate of optimization and implementation knowledge. The PocketFlow tutorials make that substrate explicit and teach it from first principles.

## Current synthesis

- The `nn` tutorial reduces learning to a simple loop: define an error surface, compute gradients, and repeatedly step downhill. It connects gradient descent, partial derivatives, and the chain rule into one story about assigning credit through layered computation.
- A durable takeaway from that lesson is that backpropagation is not a separate magical algorithm; it is just the **chain rule applied systematically through a computation graph**.
- The `pytorch` tutorial translates that math into the five-step training loop used everywhere: **prediction → loss calculation → backward pass → parameter update → gradient reset**. That loop scales from toy regression models to LLM training.
- PyTorch's `requires_grad`, computation graphs, and `loss.backward()` are valuable because they automate differentiation without changing the underlying math. The abstraction is ergonomic, not conceptual.
- The collection also keeps returning to the `nn.Linear` layer as the workhorse primitive. Much of modern deep learning, including the inside of a Transformer block, is still repeated affine transformation plus nonlinearity.
- The `adam` tutorial gives the optimizer layer of the story: Adam combines
  - **momentum / first-moment tracking** for directional stability,
  - **second-moment tracking** for adaptive per-parameter step sizes, and
  - **bias correction** to avoid tiny early updates.
- That makes Adam a practical answer to two weaknesses of vanilla gradient descent: memoryless updates and one-size-fits-all learning rates.
- Taken together, these tutorials imply a strong vault-level pattern: before treating Transformers and RLHF as special, first recognize that they are compositions of the same core objects—tensors, matrix multiplies, gradients, losses, and optimizers.
- [[Han Fang - PyTorch Practice]] complements that conceptual story with runnable interview-style implementations of stable softmax, custom BatchNorm, a hand-built SGD-with-momentum optimizer, and masked attention, making the page's abstractions feel like ordinary PyTorch building blocks rather than separate theory.
- [[Fareed Khan - Train LLM From Scratch]] reinforces the same point at the LLM scale: a language model still reduces to familiar PyTorch pieces such as embeddings, MLPs, attention modules, batch iterators, AdamW updates, and cross-entropy loss. The repo is a useful reminder that "LLM training" is mostly these standard components composed at larger scale.
- [[Mayank Pratap Singh - Diffusion Model Visual Breakdown]] adds a complementary generative-model example. A diffusion model still fits the same neural-network training loop — prediction, loss, backward pass, optimizer step — but the target is known Gaussian noise added by the training code, not the next token. This makes [[Diffusion Models]] a clean contrast case for how changing the supervised target changes the whole generative behavior.
- For the complementary DSA side of interview preparation, [[Algorithm Templates for Interviews]] covers the reusable array, graph, DP, and data-structure patterns that often appear alongside ML-specific coding rounds.

## Open questions

- Which additional fundamentals deserve their own pages next: initialization, normalization, regularization, or batching/data pipelines?
- How much of modern model behavior is still well explained by these fundamentals versus by scale-specific phenomena?

## Related pages

- [[The Pocket - PocketFlow Tutorial Docs]]
- [[The Pocket]]
- [[Han Fang - PyTorch Practice]]
- [[Fareed Khan - Train LLM From Scratch]]
- [[Transformer Architecture]]
- [[Diffusion Models]]
- [[Mayank Pratap Singh - Diffusion Model Visual Breakdown]]
- [[LLM Training Pipeline]]
- [[Model Quantization and Efficiency]]
- [[AI Knowledge Base Overview]]
- [[Algorithm Templates for Interviews]]
