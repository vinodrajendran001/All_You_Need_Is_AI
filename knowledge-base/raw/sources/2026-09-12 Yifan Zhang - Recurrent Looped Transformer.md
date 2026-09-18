---
type: raw-source
source_id: src-2026-09-12-zhang-recurrent-looped-transformer
title: "Recurrent Looped Transformer"
author: Yifan Zhang
url: "https://yifanzhang-pro.github.io/recurrent-looped-tranformer/"
published: 2026-09-12
captured: 2026-09-15
created: 2026-09-15
updated: 2026-09-18
tags:
  - source/raw
  - recurrent-transformers
  - latent-reasoning
  - reinforcement-learning
status: active
---
## Abstract

**Recurrent Looped Transformer (RLT)** combines a causal encoder with a recurrent decoder that carries its final hidden state and layerwise sliding-window attention (SWA) cache across every prompt and response token. The encoder constructs global key–value memory; the decoder extends a continuous latent computation as the sequence grows.

The design brings together **latent reasoning with unbounded temporal depth**, **model–hardware co-design**, and **model–RL algorithm co-design**. Parallel encoder work, sequence batching, memory reuse, and checkpointing surround a recurrent core. Pretraining, SFT, sampling, and current-policy replay share the same complete-state transition.

Infinite depth refers to an extensible temporal path, not infinite work within a token. Realized reasoning gains, hardware efficiency, and RL scaling remain to be established.

## Three design principles

01 / REASONING

### Depth that grows with the sequence.

Each token extends the recurrent path through the full decoder. After $t$ tokens, that path traverses $t L_{D}$ decoder blocks while the per-token block count stays fixed.

02 / HARDWARE

### Parallel work around a recurrent core.

Batch known-token encoder work and independent decoder updates. Reuse weights and memory, and checkpoint activations while preserving the reference computation.

03 / RL

### One transition from sampling to replay.

Rebuild the full history under current parameters, including prompt states and decoder SWA KV. Keep recorded behavior probabilities tied to the actual sampler.

### The complete state matters.

**Causal encoder** Known-token parallelism · global KV memory

**Recurrent decoder** Encoder cross-attention · local decoder SWA

**Carry forward: recurrent output + decoder SWA KV**

The previous output enters the next merge. Each SWA layer reads its own recent keys and values.

Prompt and response share one state transition. Encoder memory is prefix-restricted; decoder attention respects its local window. Neither decoder state component resets at the serving boundary.

$$
H_{t} = \left(s_{t} , C_{t}^{D}\right) , H_{0} = \left(s_{\star} , \emptyset\right) .
$$
 
$$
\left(s_{t} , C_{t}^{D}\right) = D_{\phi} \left(Merge \left(e_{t} , s_{t - 1}\right) ; M_{\leq t} , C_{t - 1}^{D} , t\right) .
$$
 
$$
p_{\Theta} \left(x_{t + 1} \mid x_{1 : t}\right) = softmax \left(W_{o} RMSNorm_{o} \left(s_{t}\right)\right)_{x_{t + 1}} .
$$

Here $M_{\leq t}$ is global encoder memory, $s_{t}$ is the recurrent output, and $C_{t}^{D}$ contains layerwise decoder KV. A SWA window of $W$ includes the current token and retains at most $W - 1$ historical entries for the next update.

The concrete configuration uses **48 encoder layers and 48 decoder layers**, with compatible attention and FFN weights shared across stages. The temporal path traverses $48 t$ decoder blocks after $t$ tokens. Each token executes 96 logical blocks; decoder cross-attention means these blocks do not all have equal FLOPs.

## One execution across training and inference

Known tokens can be encoded in a causal batch. Decoder updates still proceed in token order, constructing both recurrent outputs and decoder SWA caches.

| Mode | Encoder | Decoder |
| --- | --- | --- |
| Prompt prefill | Causal batch | Update complete state through every prompt token. |
| Generation | Incremental | Sample from the preceding state, then consume each token exactly once. |
| Pretraining | Causal batch | Full BPTT over all valid next-token targets. |
| SFT | Causal batch | Assistant-target loss; all context tokens update differentiable state. |
| RL replay | Rebuild with current weights | Replay the complete history and SWA caches; score each action before consuming it. |

**Forward consistency and complete gradients are separate requirements.** Full BPTT includes paths through recurrent outputs, decoder KV, and encoder memory. Detaching any of these changes the gradient. Parameter updates invalidate old caches for exact current-policy replay.

Behavior log-probabilities must describe the actual sampling distribution. Exact importance sampling additionally requires support coverage. Shared transitions remove structural prompt-boundary mismatch; numerical kernel parity and off-policy estimation remain separate concerns.

For the execution-level distinction, see the [prefill–decode kernel mismatch note](https://github.com/yifanzhang-pro/Pretraining-RL-Science/blob/master/Prefill_Decode_Kernel_Mismatch.pdf).

[Read the full report ↗](https://yifanzhang-pro.github.io/recurrent-looped-tranformer/Recurrent_Looped_Transformer.pdf)

## Citation

If you find this work useful, please cite:

```
@techreport{zhang2026recurrentlooped,
  title  = {Recurrent Looped Transformer},
  author = {Zhang, Yifan},
  year   = {2026},
  month  = sep,
  url    = {https://github.com/yifanzhang-pro/recurrent-looped-tranformer}
}
```