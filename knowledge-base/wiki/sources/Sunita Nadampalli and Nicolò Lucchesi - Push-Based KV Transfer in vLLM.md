---
type: source-summary
created: 2026-10-19
updated: 2026-10-19
source_id: src-2026-10-14-vllm-nixl-push-connector
source_title: "Push-Based KV Transfer to Improve TTFT and TPOT for Disaggregated Inference in vLLM"
source_author: Sunita Nadampalli (AWS) and Nicolò Lucchesi (Mistral)
source_url: https://vllm.ai/blog/2026-10-14-nixl-push-connector
tags: [source/summary, inference, serving, kv-cache, disaggregation, benchmarks]
source_ids: [src-2026-10-14-vllm-nixl-push-connector]
status: active
---

# Sunita Nadampalli and Nicolò Lucchesi - Push-Based KV Transfer in vLLM

## Summary

A vLLM project blog post introducing `NixlPushConnector`, a push-mode alternative to the default
pull-mode NIXL connector for [[Prefill-Decode Disaggregation|disaggregated prefill/decode]]
serving. NIXL is the NVIDIA Inference Xfer Library; here it moves KV blocks over AWS Elastic
Fabric Adapter (EFA) RDMA directly between device memories.

In pull mode, coordination starts only after prefill finishes: the router relays the prefill
instance's block metadata, the decode instance allocates destination blocks and prepares the
transfer, then issues a NIXL READ. Push mode moves decode-side allocation and registration to the
start of the request, overlapping prefill, and the prefill side issues a NIXL WRITE straight into
decode memory from a background thread once both the prompt KV and the destination registration
exist.

The authors, from AWS and Mistral, built and validated the feature on AWS Trainium clusters with
EFA and contributed it upstream as an accelerator-agnostic feature. The published measurements come
from a GPU cluster. This is a project/co-developer benchmark of one topology, not an independent
comparison.

## Key claims

### Mechanism

- **Pull path (default `NixlConnector`).** Router relay of source metadata, including prefill block
  IDs, then decode-side allocation and NIXL transfer preparation, then NIXL READ. All three run
  serially on the time-to-first-token (TTFT) critical path.
- **Push path (`NixlPushConnector`)** has three logical steps:
  1. **Registration (decode side).** When the decode worker allocates local blocks for a request
     needing remote prefill, it sends, within the same engine step, a NIXL notification naming its
     identity and the reserved block locations. Destination blocks are known before prefill ends.
  2. **Rendezvous (prefill side).** Registration and prefill completion may arrive in either order;
     whichever happens second triggers the transfer. Matching is by request identifier and accounts
     for reissued requests, so preempted or retried requests are associated correctly.
  3. **Transfer (prefill side).** The producer opens or reuses a connection and issues a NIXL WRITE
     into the decoder's registered memory, addressing each destination tensor-parallel rank. Each
     side maps block locations to its own physical layout, so the two sides may use different block
     sizes. The decoder treats KV as received only after one completion notification has arrived
     from **every producer rank** that writes into it.
- **Threading.** A dedicated background transfer thread on each prefill worker establishes or reuses
  the NIXL connection, maps KV block IDs to memory descriptors, merges contiguous blocks into larger
  transfer regions, and submits the WRITE. The prefill main loop hands off and returns to model
  execution.
- **Routing trade-off.** Pull lets the router select a decode instance after prefill, preserving
  load-aware routing and quality-of-service flexibility. Push must select it earlier so destination
  setup can overlap prefill; in return, under comparable load, the prefill instance can release its
  KV blocks sooner. The authors recommend pull for workloads needing **bidirectional KV transfer** or
  **deferred decode-instance selection**.
- In push mode the proxy must also be given the prefill instance's NIXL coordinates so it can tell
  the decode node where to register. Both servers must run the matching connector; the
  troubleshooting notes report a server crash after the first request when mode and connector
  disagree.

### Reported measurements

| Condition | Pull | Push |
| --- | --- | --- |
| TTFT, low load and short prompts | "almost identical" | "almost identical" |
| TTFT, 8 QPS, 16k input | about **1,744 ms** | roughly **540 ms** |
| Time per output token (TPOT), light load | around **5.6–5.8 ms** | around **5.6–5.8 ms** |
| TPOT, 4–8 QPS, 16k input | about **10.4 ms** | near **7 ms** |

- The headline is "up to 3x better TTFT and up to 30% better time-per-output-token (TPOT)". Both are
  the sweep's largest gaps, not typical improvements; the post adds that results depend on workload
  and configuration.
- Setup: Qwen3-32B in BF16 on a **1P1D** pair (one prefill node, one decode node), each a
  `p5en.48xlarge` with 8x NVIDIA H200 and 16 EFA interfaces at 200 Gb/s each; tensor parallelism 8,
  `--max-model-len 32768`, `--max-num-seqs 8`; input lengths 1k–16k and request rates 1–8 QPS;
  **128 output tokens**; prefix caching disabled on the decode node so every request transfers its
  full KV. vLLM 0.29.0 and NIXL 1.4.1 with the LIBFABRIC backend; a third, smaller node runs the
  proxy and benchmark client. Both GPU nodes sat in one availability zone without a cluster placement
  group.
- The post attributes pull's degradation to descriptor posting "inline on the decode worker,
  synchronously within its engine loop", which stalls token generation; push moves descriptor
  preparation and transfer submission to a background thread on the prefill side.
- By default NIXL registers each GPU's KV cache only on the two EFA rails that share that GPU's PCIe
  switch, so transfers stay PCIe-local; no device overrides were set.

## Why it matters

[[Prefill-Decode Disaggregation]] treats KV transfer as the cost that replaces interference. This
source shows that the transfer's *coordination* — metadata relay, allocation, descriptor posting,
and which loop performs them — can matter as much as interconnect bandwidth: both modes use the same
NIXL and EFA/RDMA data path, yet the high-load gap is large. It also adds a routing-commitment cost to
the design space: overlapping setup with prefill requires choosing the decode instance before prefill
finishes.

## Tensions / open questions

- **Protocol versus thread placement.** The post attributes the divergence mainly to synchronous
  descriptor posting inside the decode engine loop, and an open pull request (#45211) explores moving
  pull-mode NIXL setup to a background thread. The vault's reading is that part of the measured gap
  may come from where setup work runs rather than from push semantics alone; the benchmark does not
  separate the two.
- **"Stays flat" versus the reported numbers.** The post says push keeps per-token latency flat at
  high concurrency and long contexts. Its own figures show push TPOT rising from around 5.6–5.8 ms to
  near 7 ms: push degrades less, not zero.
- **One operating surface.** One model, one 1P1D pair, one availability zone, 128-token outputs, and
  decode prefix caching disabled by design. The isolation is right for attributing a transfer
  mechanism, but with prefix caching on, overlapping prompts could reuse the decode node's local
  cache and skip the transfer. Other xPyD ratios, models, and output lengths are untested here.
- **Queueing regime.** Each server is launched with `--max-num-seqs 8`, so the high-QPS, long-input
  cells also measure queueing, where a per-request stall in the decode loop compounds. This is the
  vault's reading of the published configuration, not a claim the post makes.
- **No dispersion or service objective.** The reproduction writes per-iteration result files, but
  the post reports no variance, confidence interval, or iteration count, no goodput at a stated
  latency objective, and no correctness check such as token equivalence between connectors.
- **Trainium versus GPU.** The feature was built and validated on Trainium, but the capture contains
  only GPU results.

## Affected pages

- [[Prefill-Decode Disaggregation]]
- [[KV Cache]]
- [[Inference Serving Engines]]
- [[Serving Benchmarks and Goodput]]
- [[AI Accelerator Architecture]]
- [[NVIDIA]]

## Raw capture

- [[Push-Based KV Transfer to Improve TTFT and TPOT for Disaggregated Inference in vLLM]]

## Citations

- Canonical article: <https://vllm.ai/blog/2026-10-14-nixl-push-connector>
- Published October 14; captured October 19, 2026.
- Linked material not separately read: the push-connector design note
  <https://docs.vllm.ai/en/latest/design/nixl_kv_push_connector/>, benchmark-script PR #57567, and
  pull-mode threading PR #45211. The appendix's installation and reproduction commands were not run.

## Related pages

- [[Prefill-Decode Disaggregation]]
- [[KV Cache]]
- [[Inference Serving Engines]]
- [[Serving Benchmarks and Goodput]]
- [[AI Accelerator Architecture]]
- [[LLM Inference]]
- [[NVIDIA]]
- [[Qwen]]
- [[Tanya Lenz - EPD Disaggregation for Multimodal Model Serving]]
- [[Wafer - AI Performance Engineering Resources]]
- [[Netflix - Reliable GPU Compute for Training and Inference]]
