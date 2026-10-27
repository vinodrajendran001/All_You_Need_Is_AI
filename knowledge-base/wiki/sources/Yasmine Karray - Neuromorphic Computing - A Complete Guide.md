---
type: source-summary
created: 2026-10-27
updated: 2026-10-27
source_id: src-2026-04-19-karray-neuromorphic-guide
source_title: "Neuromorphic Computing : A Complete Guide"
source_author: Yasmine Karray
source_url: https://medium.com/@ykarray29/neuromorphic-computing-a-complete-guide-33ed404e60dd
tags: [source/summary, ai-hardware, neuromorphic, spiking-neural-networks, edge-ai]
source_ids:
  - src-2026-04-19-karray-neuromorphic-guide
status: active
---

# Yasmine Karray - Neuromorphic Computing - A Complete Guide

## Summary

A Medium explainer by Yasmine Karray, published 19 April 2026. It introduces neuromorphic computing:
hardware that imitates the brain's asynchronous, event-driven, sparse computation, with memory and compute
in the same place. It covers biological neurons, the von Neumann bottleneck, spiking neural networks
(SNNs), the leaky integrate-and-fire (LIF) neuron model, four arguments for efficiency, applications, and
a software migration path.

It is useful orientation, but nearly every quantitative claim is uncited: the 99% energy saving, the 100×
to 1000× efficiency factors, and the robot results. Treat those figures as the author's claims, not as
evidence.

## Key claims

**The target is the von Neumann bottleneck.** In a classical processor, "the limiting factor is generally
not the speed of computation — it is the time spent transferring data between memory and the processor."
The article says a data-center GPU can draw 300 to 700 watts, "of which only a fraction is spent on actual
computation".

**Spikes instead of dense activations.** SNN neurons communicate with binary spikes, and information is
carried by spike rate, precise timing, and which neurons fire together. "If there is no spike, there is no
computation." An LIF neuron accumulates input while its potential leaks back toward rest, fires when the
potential reaches a threshold, and then resets.

**Four claimed sources of efficiency, none cited.**

1. Weights are "stored locally", next to the units that compute, removing the memory round trip.
2. Sparsity: "typically 1–5% of neurons are active at any moment", which the article says "largely
   explains the 100× to 1000× efficiency factors observed experimentally".
3. No global clock. On a GPU, clock distribution "can consume up to 30–40% of the chip’s total energy".
4. No batching, which suits real-time inputs at the edge.

**Applications are reported without setups.** Event-based vision for automotive braking is said to reach
"sub-millisecond reaction times". With Intel's Loihi 2 research chip, the ETH Zurich ANYmal quadruped
robot's "AI computation part consumes up to 100× less energy" than an Nvidia Jetson, and walking-control
tests cut overall processor consumption by 90%. No configuration, workload, or citation is given.

**Training needs surrogate gradients.** A spike is a step function whose derivative is zero, which blocks
backpropagation. With surrogate gradients, the backward pass replaces the step with a continuous curve, so
standard optimizers still work. SpikingJelly and Norse run on PyTorch; their neurons carry state that must
be reset between batches, data gain a time dimension, and training also aims to maximize sparsity.

**A division of labor, not a replacement.** "Neuromorphic computing is not destined to replace the GPU for
training large models." In the article's picture, GPUs train models in data centers, and the trained
models are converted to run on neuromorphic chips in edge devices. It presents this split as the state of
the field in 2026 but names no deployed conversion.

## Why it matters

[[AI Accelerator Architecture]] has covered GPUs, systolic arrays, wafer-scale engines, and dataflow
designs. This adds the event-driven branch, whose efficiency case rests on sparsity and memory placed with
compute rather than on faster matrix multiplication.

It also sharpens a disagreement on deployment. [[Jacob Peake - AI Chip Architectures]] lists neuromorphic
designs among the architectures "in serious development" and leaves them out of those that "have won real
deployment". This guide describes the GPU-plus-neuromorphic split as the current arrangement.

## Tensions / open questions

- **Uncited numbers.** The 99%, 100× to 1000×, 100×, and 90% figures have no baseline, workload, hardware
  configuration, or source.
- **The article's own arithmetic does not reach its range.** If only 1–5% of neurons are active,
  proportional savings top out at about a hundredfold, so sparsity alone cannot "largely" explain the
  upper end of 100× to 1000×.
- **No matched comparison.** SNNs and conventional networks are never compared at equal accuracy,
  latency, or energy.
- **Silent costs are not discussed.** The claim that an idle chip "consumes almost nothing" leaves out
  leakage, memory retention, and sensor power.
- **Byline.** The clipping records the author in lowercase ("yasmine karray"); this page uses title case.

## Affected pages

- [[AI Accelerator Architecture]]

## Raw capture

- [[Neuromorphic Computing  A Complete Guide]]

## Citations

- Canonical URL: https://medium.com/@ykarray29/neuromorphic-computing-a-complete-guide-33ed404e60dd
- Published 19 April 2026 and captured 26 October. The raw file name contains a double space where the
  title has a colon.

## Related pages

- [[AI Accelerator Architecture]]
- [[Jacob Peake - AI Chip Architectures]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[GPU Execution Model]]
- [[Neural Network Fundamentals]]
- [[On-Device Reasoning]]
- [[AI Knowledge Base Overview]]
