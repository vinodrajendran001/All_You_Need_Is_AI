---
type: raw-source
title: "How Local LLMs Run: Memory and Hardware"
source: "https://silicontales.com/local-llm-complete-guide/?trk=feed_main-feed-card_feed-article-content"
author:
  - "[[Onur Sirin]]"
published: 2026-06-30
created: 2026-07-04
description: "Running LLMs locally, explained simply: a prompt through eight stages, how much memory a model needs, and what fits on which machine, from 5090 to GB300."
tags:
  - "clippings"
  - "source/raw"

---
## Running an LLM locally: how it works, how much room it needs, and which machine it fits

This guide answers two big questions end to end. **Part one** follows a prompt through the silicon: what you type travels from disk to memory to the compute cores, eight stages laid out one by one, with the job each component does at every step and which machine has the edge. **Part two** is the memory maths: how much room a model really takes, what every term actually means (FP16, Q4, HBM, all in plain language), and what fits on which machine.

Worked examples: RTX 5090 and Mac Studio M3 Ultra carry the pipeline; the full comparison adds the M5 Ultra and the Asus ET900N G3 (GB300)

8

pipeline stages

4

machines compared

32 to 748 GB

fast-memory span

≤1T

params that fit (Q4)

1

Part one

## The pipeline: how a prompt actually runs

## One job, four very different machines

Running an LLM locally is one job approached four ways, and none of them wins at everything. The corners of the triangle are different: fast-pool capacity, bandwidth, and shape (a single flat pool, or a tiered one). Two of these, the [RTX 5090](https://silicontales.com/rtx-5090-review/) and the Mac M3 Ultra, carry the pipeline walkthrough below because they are the most opposite designs. Part two scales the lesson out to all four.

Discrete GPU

### RTX 5090 Desktop

Model: Qwen 3.6 27B · Q4\_K\_M · ~17 GB · **dense**

GPU memory

**32 GB** GDDR7

Mem bandwidth

**~1.79 TB/s**

CPU

Ryzen 9 7900X3D

System RAM

32 GB DDR5-6400

Disk

T705 PCIe 5.0

Compute

Tensor + CUDA cores

Unified memory

### Mac Studio M3 Ultra

Model: gpt-oss 120B · MXFP4 (~Q4) · ~63 GB · **MoE, ~5B active**

Unified memory

**96 GB** (only option\*)

Mem bandwidth

**819 GB/s**

GPU

80-core

VRAM

none (one pool)

PCIe hop

none (CPU = GPU)

Neural Engine

mostly idle

\* Apple dropped the 512 GB option in March 2026 and the 256 GB option in May 2026 (DRAM shortage). The M3 Ultra now ships only as 96 GB.

Unified · rumoured

### Mac Studio M5 Ultra

Model: frontier-class MoE up to ~768 GB · **unconfirmed**

Unified memory

**~768 GB** \*

Mem bandwidth

**~1.1 TB/s** (rumour)

Structure

flat (uniform)

VRAM

none (one pool)

Status

~Q4 2026 (rumour)

Price

$10,000+ (estimate)

\* Every M5 Ultra figure here is rumour or leak, not official. Apple is said to have tested a 768 GB option but may not ship at that capacity given the memory shortage.

Coherent · GB300

### Asus ET900N G3

Model: frontier and ~1T-param models · **tiered HBM + LPDDR**

Coherent memory

**748 GB**

HBM3e (fast)

**252 GB** @ 7.1 TB/s

LPDDR5X (large)

496 GB @ 396 GB/s

Link

NVLink-C2C

Structure

tiered

Price

enterprise

## The eight-stage pipeline

Say you have caught the local-LLM bug: you want to generate text or write code on your own machine, and you have started wondering what actually happens the instant you hit a key and send a prompt. Where does it go, and what does the work? Here is the whole journey at a glance, the eight stages a prompt passes through, from the disk in your machine to the words landing on your screen. The colours mark what each stage is limited by (its bottleneck), and you can tap any stage to jump to the full detail.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 662" role="img" style="width:100%;height:auto;min-width:940px;display:block" aria-labelledby="dgT dgD"><title id="dgT">LLM inference pipeline architecture</title> <desc id="dgD">A prompt is loaded, tokenized and prefilled once, then a per-token decode loop reads weights and the KV cache from memory to emit tokens that are detokenized and streamed.</desc> <defs><marker id="ah" markerWidth="9" markerHeight="9" refX="7.2" refY="3" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L8,3 L0,6 Z" fill="#5b6a7d"></path></marker><marker id="ahs" markerWidth="9" markerHeight="9" refX="0.8" refY="3" orient="auto" markerUnits="userSpaceOnUse"><path d="M8,0 L0,3 L8,6 Z" fill="#5b6a7d"></path></marker><marker id="ahf" markerWidth="8" markerHeight="8" refX="6.4" refY="2.6" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L7,2.6 L0,5.2 Z" fill="#3a4656"></path></marker></defs><rect x="8" y="8" width="1184" height="646" rx="20" fill="#0e131a" stroke="#1b212b" stroke-width="1.5"></rect><text x="30" y="42" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="12.5" font-weight="600" fill="#ffb866" text-anchor="start" letter-spacing=".14em">INFERENCE PIPELINE</text> <text x="30" y="60" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="12" font-weight="400" fill="#c2cad5" text-anchor="start" letter-spacing="0">how one prompt becomes a stream of tokens</text> <circle cx="702" cy="40" r="5.5" fill="#8f86ff"></circle><text x="714" y="44" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="12" font-weight="500" fill="#d7dce4" text-anchor="start" letter-spacing="0">I/O</text> <circle cx="757.6" cy="40" r="5.5" fill="#f2c14e"></circle><text x="769.6" y="44" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="12" font-weight="500" fill="#d7dce4" text-anchor="start" letter-spacing="0">Compute</text> <circle cx="842.0" cy="40" r="5.5" fill="#43c6b7"></circle><text x="854.0" y="44" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="12" font-weight="500" fill="#d7dce4" text-anchor="start" letter-spacing="0">Bandwidth</text> <circle cx="940.8" cy="40" r="5.5" fill="#c2cad5"></circle><text x="952.8" y="44" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="12" font-weight="500" fill="#d7dce4" text-anchor="start" letter-spacing="0">Trivial</text> <rect x="128" y="96" width="438" height="180" rx="18" fill="none" stroke="#3a4656" stroke-width="1.4" stroke-dasharray="2 7"></rect><rect x="596" y="96" width="492" height="180" rx="18" fill="none" stroke="#3a4656" stroke-width="1.4" stroke-dasharray="2 7"></rect><text x="144" y="86" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="11.3" font-weight="600" fill="#c2cad5" text-anchor="start" letter-spacing=".05em">ONE-TIME · LOADS &amp; UNDERSTANDS THE PROMPT</text> <text x="612" y="86" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="11.3" font-weight="600" fill="#ffb866" text-anchor="start" letter-spacing=".05em">PER-TOKEN LOOP · ≈ 99% OF WALL-CLOCK</text> <rect x="22" y="184" width="88" height="48" rx="24.0" fill="#1b2330" stroke="#3a4656" stroke-width="1.5"></rect><text x="66.0" y="206.0" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="12.5" font-weight="600" fill="#f4f2ec" text-anchor="middle" letter-spacing="0">Prompt</text> <text x="66.0" y="222.0" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="10" font-weight="400" fill="#c2cad5" text-anchor="middle" letter-spacing="0">your text</text> <rect x="1096" y="184" width="84" height="48" rx="24.0" fill="#1b2330" stroke="#5fd08a" stroke-width="1.5"></rect><text x="1138.0" y="206.0" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="12.5" font-weight="600" fill="#f4f2ec" text-anchor="middle" letter-spacing="0">Output</text> <text x="1138.0" y="222.0" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="10" font-weight="400" fill="#c2cad5" text-anchor="middle" letter-spacing="0">stream</text> <a href="#s1" aria-label="Stage 01: Cold load"><g><rect x="138" y="158" width="118" height="92" rx="14" fill="#161c25" stroke="#28303b" stroke-width="1.5"></rect><rect x="138" y="158" width="118" height="5" rx="2" fill="#8f86ff" stroke="none" stroke-width="0" opacity="0.92"></rect><circle cx="161" cy="185" r="12.5" fill="#8f86ff" opacity="0.15"></circle><circle cx="161" cy="185" r="12.5" fill="none" stroke="#8f86ff" stroke-width="1.3"></circle><text x="161" y="189" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="11.5" font-weight="700" fill="#8f86ff" text-anchor="middle" letter-spacing="0">01</text> <text x="243" y="189" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="9.3" font-weight="600" fill="#8f86ff" text-anchor="end" letter-spacing=".04em">I/O</text> <text x="154" y="213" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="14" font-weight="600" fill="#f4f2ec" text-anchor="start" letter-spacing="0">Cold load</text> <text x="154" y="232" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="10.8" font-weight="400" fill="#d7dce4" text-anchor="start" letter-spacing="0">model into memory</text> </g></a><a href="#s2" aria-label="Stage 02: Tokenize"><g><rect x="290" y="158" width="118" height="92" rx="14" fill="#161c25" stroke="#28303b" stroke-width="1.5"></rect><rect x="290" y="158" width="118" height="5" rx="2" fill="#c2cad5" stroke="none" stroke-width="0" opacity="0.92"></rect><circle cx="313" cy="185" r="12.5" fill="#c2cad5" opacity="0.15"></circle><circle cx="313" cy="185" r="12.5" fill="none" stroke="#c2cad5" stroke-width="1.3"></circle><text x="313" y="189" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="11.5" font-weight="700" fill="#c2cad5" text-anchor="middle" letter-spacing="0">02</text> <text x="395" y="189" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="9.3" font-weight="600" fill="#c2cad5" text-anchor="end" letter-spacing=".04em">TRIVIAL</text> <text x="306" y="213" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="14" font-weight="600" fill="#f4f2ec" text-anchor="start" letter-spacing="0">Tokenize</text> <text x="306" y="232" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="10.8" font-weight="400" fill="#d7dce4" text-anchor="start" letter-spacing="0">text to token IDs</text> </g></a><a href="#s3" aria-label="Stage 03: Prefill"><g><rect x="442" y="158" width="118" height="92" rx="14" fill="#161c25" stroke="#28303b" stroke-width="1.5"></rect><rect x="442" y="158" width="118" height="5" rx="2" fill="#f2c14e" stroke="none" stroke-width="0" opacity="0.92"></rect><circle cx="465" cy="185" r="12.5" fill="#f2c14e" opacity="0.15"></circle><circle cx="465" cy="185" r="12.5" fill="none" stroke="#f2c14e" stroke-width="1.3"></circle><text x="465" y="189" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="11.5" font-weight="700" fill="#f2c14e" text-anchor="middle" letter-spacing="0">03</text> <text x="547" y="189" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="9.3" font-weight="600" fill="#f2c14e" text-anchor="end" letter-spacing=".04em">COMPUTE</text> <text x="458" y="213" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="14" font-weight="600" fill="#f4f2ec" text-anchor="start" letter-spacing="0">Prefill</text> <text x="458" y="232" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="10.8" font-weight="400" fill="#d7dce4" text-anchor="start" letter-spacing="0">read whole prompt</text> </g></a><a href="#s5" aria-label="Stage 05: Decode"><g><rect x="620" y="158" width="118" height="92" rx="14" fill="#161c25" stroke="#28303b" stroke-width="1.5"></rect><rect x="620" y="158" width="118" height="5" rx="2" fill="#43c6b7" stroke="none" stroke-width="0" opacity="0.92"></rect><circle cx="643" cy="185" r="12.5" fill="#43c6b7" opacity="0.15"></circle><circle cx="643" cy="185" r="12.5" fill="none" stroke="#43c6b7" stroke-width="1.3"></circle><text x="643" y="189" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="11.5" font-weight="700" fill="#43c6b7" text-anchor="middle" letter-spacing="0">05</text> <text x="725" y="189" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="9.3" font-weight="600" fill="#43c6b7" text-anchor="end" letter-spacing=".04em">BANDWIDTH</text> <text x="636" y="213" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="14" font-weight="600" fill="#f4f2ec" text-anchor="start" letter-spacing="0">Decode</text> <text x="636" y="232" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="10.8" font-weight="400" fill="#d7dce4" text-anchor="start" letter-spacing="0">next token</text> </g></a><a href="#s6" aria-label="Stage 06: Sample"><g><rect x="772" y="158" width="118" height="92" rx="14" fill="#161c25" stroke="#28303b" stroke-width="1.5"></rect><rect x="772" y="158" width="118" height="5" rx="2" fill="#c2cad5" stroke="none" stroke-width="0" opacity="0.92"></rect><circle cx="795" cy="185" r="12.5" fill="#c2cad5" opacity="0.15"></circle><circle cx="795" cy="185" r="12.5" fill="none" stroke="#c2cad5" stroke-width="1.3"></circle><text x="795" y="189" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="11.5" font-weight="700" fill="#c2cad5" text-anchor="middle" letter-spacing="0">06</text> <text x="877" y="189" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="9.3" font-weight="600" fill="#c2cad5" text-anchor="end" letter-spacing=".04em">TRIVIAL</text> <text x="788" y="213" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="14" font-weight="600" fill="#f4f2ec" text-anchor="start" letter-spacing="0">Sample</text> <text x="788" y="232" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="10.8" font-weight="400" fill="#d7dce4" text-anchor="start" letter-spacing="0">pick the token</text> </g></a><a href="#s8" aria-label="Stage 08: Detokenize"><g><rect x="954" y="158" width="118" height="92" rx="14" fill="#161c25" stroke="#28303b" stroke-width="1.5"></rect><rect x="954" y="158" width="118" height="5" rx="2" fill="#c2cad5" stroke="none" stroke-width="0" opacity="0.92"></rect><circle cx="977" cy="185" r="12.5" fill="#c2cad5" opacity="0.15"></circle><circle cx="977" cy="185" r="12.5" fill="none" stroke="#c2cad5" stroke-width="1.3"></circle><text x="977" y="189" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="11.5" font-weight="700" fill="#c2cad5" text-anchor="middle" letter-spacing="0">08</text> <text x="1059" y="189" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="9.3" font-weight="600" fill="#c2cad5" text-anchor="end" letter-spacing=".04em">TRIVIAL</text> <text x="970" y="213" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="14" font-weight="600" fill="#f4f2ec" text-anchor="start" letter-spacing="0">Detokenize</text> <text x="970" y="232" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="10.8" font-weight="400" fill="#d7dce4" text-anchor="start" letter-spacing="0">tokens to text</text> </g></a><path d="M110,204.0 H138" fill="none" stroke="#5b6a7d" stroke-width="2" marker-end="url(#ah)"></path><path d="M110,204.0 H138" fill="none" stroke="#ffb866" stroke-width="2" opacity="0.8"></path><path d="M256,204.0 H290" fill="none" stroke="#5b6a7d" stroke-width="2" marker-end="url(#ah)"></path><path d="M256,204.0 H290" fill="none" stroke="#ffb866" stroke-width="2" opacity="0.8"></path><path d="M408,204.0 H442" fill="none" stroke="#5b6a7d" stroke-width="2" marker-end="url(#ah)"></path><path d="M408,204.0 H442" fill="none" stroke="#ffb866" stroke-width="2" opacity="0.8"></path><path d="M560,204.0 H620" fill="none" stroke="#5b6a7d" stroke-width="2" marker-end="url(#ah)"></path><path d="M560,204.0 H620" fill="none" stroke="#ffb866" stroke-width="2" opacity="0.8"></path><path d="M738,204.0 H772" fill="none" stroke="#5b6a7d" stroke-width="2" marker-end="url(#ah)"></path><path d="M738,204.0 H772" fill="none" stroke="#ffb866" stroke-width="2" opacity="0.8"></path><path d="M890,204.0 H954" fill="none" stroke="#5b6a7d" stroke-width="2" marker-end="url(#ah)"></path><path d="M890,204.0 H954" fill="none" stroke="#ffb866" stroke-width="2" opacity="0.8"></path><path d="M1072,204.0 H1096" fill="none" stroke="#5b6a7d" stroke-width="2" marker-end="url(#ah)"></path><path d="M1072,204.0 H1096" fill="none" stroke="#ffb866" stroke-width="2" opacity="0.8"></path><rect x="545.0" y="195.0" width="90.0" height="18" rx="5" fill="#0e131a" stroke="none" stroke-width="0" opacity="0.92"></rect><text x="590" y="207.5" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="10.3" font-weight="500" fill="#d7dce4" text-anchor="middle" letter-spacing="0">context ready</text> <rect x="895.0" y="195.0" width="54.0" height="18" rx="5" fill="#0e131a" stroke="none" stroke-width="0" opacity="0.92"></rect><text x="922" y="207.5" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="10.3" font-weight="500" fill="#d7dce4" text-anchor="middle" letter-spacing="0">1 token</text> <path d="M831,158 C831,116 679,116 679,158" fill="none" stroke="#43c6b7" stroke-width="2" marker-end="url(#ah)"></path><path d="M831,158 C831,116 679,116 679,158" fill="none" stroke="#43c6b7" stroke-width="2.4" opacity="0.9"></path><a href="#s7" aria-label="Stage 07: decode loop"><rect x="671.0" y="103" width="168" height="21" rx="10.5" fill="#0e131a" stroke="#43c6b7" stroke-width="1.2"></rect><text x="755.0" y="117" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="10.3" font-weight="600" fill="#43c6b7" text-anchor="middle" letter-spacing="0">07 · DECODE LOOP ×N</text> </a><a href="#s4" aria-label="Stage 04: KV cache"><path d="M485.0,326 V390 a105.0,14 0 0 0 210,0 V326" fill="#152031" stroke="#43c6b7" stroke-width="1.5"></path><ellipse cx="590.0" cy="326" rx="105.0" ry="14" fill="#1b2330" stroke="#43c6b7" stroke-width="1.5"></ellipse><ellipse cx="590.0" cy="326" rx="105.0" ry="14" fill="#43c6b7"></ellipse><text x="590.0" y="358" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="13.5" font-weight="600" fill="#f4f2ec" text-anchor="middle" letter-spacing="0">04 · KV cache</text> <text x="590.0" y="378" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="10.6" font-weight="400" fill="#d7dce4" text-anchor="middle" letter-spacing="0">grows by one entry every token</text> </a><path d="M501,250 C501,300 531.0,302 531.0,322" fill="none" stroke="#5b6a7d" stroke-width="2" marker-end="url(#ah)"></path><rect x="478.0" y="291" width="60.0" height="18" rx="5" fill="#0e131a" stroke="none" stroke-width="0" opacity="0.92"></rect><text x="508" y="303.5" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="10.3" font-weight="500" fill="#d7dce4" text-anchor="middle" letter-spacing="0">write KV</text> <path d="M679,250 C679,300 649.0,302 649.0,322" fill="none" stroke="#5b6a7d" stroke-width="2" marker-end="url(#ah)" marker-start="url(#ahs)"></path><rect x="645.0" y="291" width="90.0" height="18" rx="5" fill="#0e131a" stroke="none" stroke-width="0" opacity="0.92"></rect><text x="690" y="303.5" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="10.3" font-weight="500" fill="#d7dce4" text-anchor="middle" letter-spacing="0">read + append</text> <text x="140" y="448" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="11.3" font-weight="600" fill="#c2cad5" text-anchor="start" letter-spacing=".06em">WHERE IT PHYSICALLY RUNS</text> <rect x="140" y="470" width="176" height="90" rx="13" fill="#161c25" stroke="#28303b" stroke-width="1.5"></rect><text x="158" y="500" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="13.5" font-weight="600" fill="#f4f2ec" text-anchor="start" letter-spacing="0">Storage</text> <text x="158" y="521" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="10.8" font-weight="400" fill="#d7dce4" text-anchor="start" letter-spacing="0">NVMe SSD</text> <text x="158" y="542" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="10.3" font-weight="500" fill="#8f86ff" text-anchor="start" letter-spacing="0">.gguf · 17 GB</text> <rect x="380" y="470" width="360" height="90" rx="13" fill="#161c25" stroke="#43c6b7" stroke-width="1.5"></rect><text x="398" y="500" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="13.5" font-weight="600" fill="#f4f2ec" text-anchor="start" letter-spacing="0">Memory</text> <text x="398" y="521" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="10.8" font-weight="400" fill="#d7dce4" text-anchor="start" letter-spacing="0">VRAM (GDDR) or unified pool</text> <text x="398" y="542" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="10.3" font-weight="400" fill="#c2cad5" text-anchor="start" letter-spacing="0">holds the weights and the KV cache</text> <rect x="596" y="490" width="128" height="48" rx="9" fill="#10211f" stroke="#43c6b7" stroke-width="1.2"></rect><text x="660" y="509" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="9.8" font-weight="600" fill="#43c6b7" text-anchor="middle" letter-spacing="0">bandwidth =</text> <text x="660" y="525" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="9.8" font-weight="600" fill="#43c6b7" text-anchor="middle" letter-spacing="0">decode bottleneck</text> <rect x="800" y="470" width="288" height="90" rx="13" fill="#161c25" stroke="#f2c14e" stroke-width="1.5"></rect><text x="818" y="500" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="13.5" font-weight="600" fill="#f4f2ec" text-anchor="start" letter-spacing="0">Compute</text> <text x="818" y="521" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="10.8" font-weight="400" fill="#d7dce4" text-anchor="start" letter-spacing="0">Tensor / CUDA / GPU cores</text> <text x="818" y="542" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="10.3" font-weight="500" fill="#f2c14e" text-anchor="start" letter-spacing="0">matrix multiply lives here</text> <path d="M316,515 H380" fill="none" stroke="#5b6a7d" stroke-width="2" marker-end="url(#ah)"></path><path d="M316,515 H380" fill="none" stroke="#ffb866" stroke-width="2" opacity="0.8"></path><rect x="330.0" y="491" width="36.0" height="18" rx="5" fill="#0e131a" stroke="none" stroke-width="0" opacity="0.92"></rect><text x="348" y="503.5" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="10.3" font-weight="500" fill="#d7dce4" text-anchor="middle" letter-spacing="0">load</text> <path d="M740,515 H800" fill="none" stroke="#5b6a7d" stroke-width="2" marker-end="url(#ah)" marker-start="url(#ahs)"></path><path d="M740,515 H800" fill="none" stroke="#ffb866" stroke-width="2" opacity="0.8"></path><rect x="725.0" y="491" width="90.0" height="18" rx="5" fill="#0e131a" stroke="none" stroke-width="0" opacity="0.92"></rect><text x="770" y="503.5" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="10.3" font-weight="500" fill="#d7dce4" text-anchor="middle" letter-spacing="0">weights/token</text> <path d="M197,250 V470" stroke="#3a4656" stroke-width="1.4" stroke-dasharray="2 6" fill="none" marker-end="url(#ahf)"></path><rect x="153" y="351.0" width="88" height="18" rx="5" fill="#0e131a" stroke="none" stroke-width="0" opacity="0.9"></rect><text x="197" y="363.5" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="9.8" font-weight="400" fill="#c2cad5" text-anchor="middle" letter-spacing="0">reads.gguf</text> <path d="M590.0,404 V470" stroke="#3a4656" stroke-width="1.4" stroke-dasharray="2 6" fill="none" marker-end="url(#ahf)"></path><rect x="558" y="428.0" width="64" height="18" rx="5" fill="#0e131a" stroke="none" stroke-width="0" opacity="0.9"></rect><text x="590" y="440.5" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="9.8" font-weight="400" fill="#c2cad5" text-anchor="middle" letter-spacing="0">lives in</text> <circle cx="372" cy="630" r="4" fill="#ffb866"></circle><text x="388" y="634" font-family="'Switzer',system-ui,-apple-system,sans-serif" font-size="12" font-weight="500" fill="#d7dce4" text-anchor="start" letter-spacing="0">The loop (decode then sample) repeats for every token, and its speed is set by memory bandwidth, not raw compute power.</text></svg>

## The pipeline's eight stages

For each stage: what happens (simply), what each component does on each machine, who has the advantage and why, and a weak spot.

### Read this first: this is not a race

Below you will see times like two seconds on the 5090 and far longer on the big machines. **Do not read that as a ranking.** Each machine runs a completely different model, sized to the memory it has, so they are never doing the same job.

**RTX 5090 · 32 GB** Runs a small, fast model (gpt-oss 20B). Brilliant for quick code edits, autocomplete and simple chat, but limited in what it can hold.

**Mac M3 Ultra · 96 GB** Runs a large MoE (gpt-oss 120B) that the 5090 cannot fit into its VRAM at all.

**M5 Ultra · rumoured** Expected to hold a larger model again, 200B and up, in the same unified-memory style.

**Asus GB300 · 748 GB** Runs a frontier 671B and up model, a different category of capability entirely.

It is faster because its model is tiny. The big machines spend more time per step because they run models that are vastly more capable. This guide is about what each tier lets you **do**, and how the work flows through it, not about who wins a benchmark, because no benchmark here would be fair.

01

### Loading the model into memory

Cold load, once, before inference starts

I/O-bound

The model file on disk is moved into the memory where the GPU will do its maths. Think of the **"Loading..."** screen when a game opens: it happens once at the very start and then never repeats. The bigger the file and the slower the disk, the longer it takes.

#### RTX 5090

**Runs** gpt-oss 20B · ~17 GB

- **Disk (T705):** reads the 17 GB.gguf file
- **CPU:** mmaps the file, manages the load
- **PCIe 5.0:** copies the weights from RAM to VRAM
- **VRAM:** the final stop, 17 of the 32 GB fill

Time~2-5 s

#### Mac M3 Ultra

**Runs** gpt-oss 120B · ~63 GB

- **SSD:** reads the 63 GB file (~4x larger)
- **CPU:** mmaps it, manages the load
- **Unified memory:** the weights land directly, **no PCIe copy**
- 63 of the 96 GB fill

Time~10-15 s

#### M5 Ultra

**Runs** a 200B+ MoE · rumoured

- Unified memory, the M3 path: weights land directly, no PCIe copy
- a larger pool holds a bigger model than the M3 fits
- the file is larger again, so the read is longer

Time~15-30 s (est.)

#### Asus GB300

**Runs** a 671B+ frontier model

- NVMe into the 748 GB coherent pool (HBM3e + LPDDR5X) over NVLink-C2C
- a frontier model is hundreds of GB, so this is the longest cold load
- done once, then it never repeats

Time~30-90 s (est.)

What this meansCold load rewards small files and fast disks, so the lighter the model, the quicker the start. Read that as convenience, not capability. The machines that take longer are loading far larger, far more capable models, and a two second start on a 17 GB model is simply not the same job as a one minute start on a 671 GB one.

02

### Turning text into tokens

Tokenize, text to numbers

Trivial

Your prompt and code are split into small pieces called tokens and turned into numbers. The model sees numbers, not letters: **"Hello world" becomes \[15043, 8222\]**, roughly. Pure bookkeeping, done in under a millisecond.

#### RTX 5090

- **CPU:** runs the tokenizer (BPE), produces the token-ID list
- **GPU:** sits idle

#### Mac M3 Ultra

- **CPU (P-cores):** does the same
- **GPU:** sits idle

What this meansTokenizing is a sub-millisecond job on the CPU. It is identical on all four machines and is never the bottleneck.

03

### Processing the prompt

Prefill, reading and understanding the context

Compute-bound

Every prompt token passes through every layer of the model at once, in parallel. This is where the model **reads and understands** the context you gave it. Feed in a big codebase and this is exactly why the first reply is delayed (TTFT). The stage is dominated by matrix multiply, so it is **compute-bound**: the limit is raw processing power.

#### RTX 5090

**Runs** gpt-oss 20B · ~17 GB

- **Tensor cores:** do the heavy GEMMs (attention + FFN), very high throughput, the real power sits here
- **CUDA cores:** activations, softmax, RoPE, layernorm
- **VRAM:** feeds the weights to the cores, holds the activations

ResultFast TTFT

#### Mac M3 Ultra

**Runs** gpt-oss 120B · ~63 GB

- **GPU cores:** do the same multiplies, but without tensor-core density, so lower raw FLOPS
- **Unified memory:** feeds the weights
- **MoE:** across many tokens, many experts get touched

ResultSlow TTFT

#### M5 Ultra

**Runs** a 200B+ MoE · rumoured

- Apple GPU cores, expected denser than the M3, still not discrete tensor-core class
- a larger, smarter model means more work to digest
- unified memory feeds the weights

Resultmoderate (est.)

#### Asus GB300

**Runs** a 671B+ frontier model

- Blackwell Ultra GPU with tensor cores, the 5090's class but far more of it
- up to 20 PFLOPS FP4 of raw throughput on tap
- the model and context are frontier-scale, so there is vastly more to chew

Resultfast for its size (est.)

What this meansRaw compute decides how quickly a prompt is digested, and the discrete tensor cores in the 5090 and the Asus lead here. But each machine is digesting a different prompt into a different model, so this measures how each tier copes with its own work, not a shared race.

04

### Holding the context in memory

KV cache, so the past is not recomputed

Capacity + bandwidth

For every token, attention's Key and Value values are stored so later tokens do not recompute the whole history. As the context grows, this cache **grows** with it, like a long notebook: the more you write, the more room it takes. The problem is capacity, because this cache shares memory with the model weights.

#### RTX 5090

**Runs** gpt-oss 20B · ~17 GB

- **VRAM:** the KV cache lives here, sharing the same 32 GB as the 17 GB of weights, so about ~15 GB is free
- A very long context can still pressure it, but the headroom is now roughly double that of a 24 GB card

#### Mac M3 Ultra

**Runs** gpt-oss 120B · ~63 GB

- **Unified memory:** the KV cache is here too, in the 96 GB pool
- With the model taking ~63 GB, around 25 to 30 GB is left for context, far more than the 5090, though not the old 512 GB luxury

#### M5 Ultra

**Runs** a 200B+ MoE · rumoured

- a larger unified pool again (expected), so even more context headroom
- the M3 idea with more of it, long histories stay comfortable

What this meansThis is the stage where memory size becomes capability. More memory does not make a machine faster, it makes a bigger model and a longer context possible at all. The 5090 is quick but cramped, while the big-memory machines trade a little speed for room a desktop card simply does not have.

05

### Producing one token

Decode (1 token), the stage that actually decides

Bandwidth-bound

Once the prompt is processed, the next token is produced. For a single token, one pass through all the layers happens, and the weights it needs must be **read** from memory. The compute is tiny (one token), so the limit is **how fast you can read memory**. That is why it is bandwidth-bound, and why this is the stage that sets tokens per second.

#### RTX 5090

**Runs** gpt-oss 20B · ~17 GB

- **VRAM bandwidth (~1.79 TB/s):** for this one token it reads the ~17 GB of weights, that is the per-token cost
- **Tensor cores:** a width-one multiply, barely used, they **wait on memory**
- **CUDA cores:** prepare the sampling

Speed~70-90 tok/s

#### Mac M3 Ultra

**Runs** gpt-oss 120B · ~63 GB

- **Unified memory bw (819 GB/s):** reads only the **active experts** (~5B, roughly 3 GB), not all 63 GB, the MoE trick
- **GPU cores:** a width-one multiply, memory-bound
- ~5B active params means very little to read, so decode is surprisingly quick

Speed~50-70 tok/s

#### M5 Ultra

**Runs** a 200B+ MoE · rumoured

- Unified-memory bandwidth, expected above the M3's 819 GB/s
- an MoE reads only its active experts per token, so decode stays quick
- the bigger model is smarter, not heavier per token

Speedbrisk (est.)

#### Asus GB300

**Runs** a 671B+ frontier model

- Tiered memory: hot weights and KV in HBM3e at 7.1 TB/s, the rest in LPDDR5X at 396 GB/s
- a frontier MoE streams its active experts from the fast tier
- raw bandwidth dwarfs a desktop card, but the model is far larger

Speedfast at 671B (est.)

What this meansDecode speed depends on the model and the memory feeding it, so these numbers do not compare across machines. A 17 GB model on a desktop card and a 671 GB model on a coherent pool are different workloads, and being fast on a tiny model is not the same as being capable on a huge one.

06

### Choosing the next token

Sampling, picking from the logits

Trivial

The model produces probabilities (logits) across the whole vocabulary, and one is chosen, with settings like **temperature** and **top-p** steering the pick. The "roll the dice for the next word" stage, done in under a millisecond.

#### RTX 5090

- **CUDA cores:** compute softmax over the logits
- **CPU/GPU:** apply the sampling strategy

#### Mac M3 Ultra

- **GPU cores / CPU:** do the same

What this meansSampling is sub-millisecond on every machine. No tier has an edge here, and it never moves the total time.

07

### The generation loop

Decode loop, 99 percent of the time

Bandwidth (continuous)

Steps 5 and 6 repeat for every output token: a new token is added, fed back, the next is produced, and the KV cache grows by one each step. **Almost all** of the total wait happens here. The longer the answer, the more the loop turns.

#### RTX 5090

**Runs** gpt-oss 20B · ~17 GB

- Each token is the same **VRAM read**; steady speed until the KV cache fills the VRAM
- An 800-token code reply

≈ Time~9-12 s

#### Mac M3 Ultra

**Runs** gpt-oss 120B · ~63 GB

- Each token is the same **unified-memory read**; steady speed
- 800 tokens, and it is running a 120B model the 5090 **cannot fit** in VRAM at all

≈ Time~12-16 s

#### M5 Ultra

**Runs** a 200B+ MoE · rumoured

- each token is the same unified-memory read, steady
- it sustains a 200B+ model the 5090 cannot load at all

Timesteady (est.)

#### Asus GB300

**Runs** a 671B+ frontier model

- each token streams active experts from HBM3e, steady at frontier scale
- it runs a 671B model end to end, a different category of work

Timesteady at 671B (est.)

What this meansThe loop is where almost all of the waiting lives, and every machine runs it on its own model. The question is not whose loop is quicker, it is that more memory is what lets a bigger, more capable model run the loop at all.

08

### Turning tokens back into text and streaming

Detokenize + stream, numbers to screen

Trivial

Each token ID produced is turned back into text and streamed to your editor or screen as it is generated. **The words appearing one by one in ChatGPT** is the visible form of this step. The CPU handles it in parallel while the GPU keeps producing in the background.

#### RTX 5090

- **CPU:** turns IDs into text, streams to screen while the GPU produces

#### Mac M3 Ultra

- **CPU:** does the same

What this meansTurning tokens back into text and streaming them is a light CPU job, identical on every machine. It is the visible part of generation, never the slow part.

## Glossary, the ideas in the pipeline

Every term used in the stages above, in plain words. (Memory types and precision, HBM, FP16, Q4, get their own deeper treatment in part two.)

### Memory & storage

VRAM (GDDR7)

The GPU's own ultra-fast memory. While the model runs, the weights must sit here. On the 5090 that is **32 GB** and very fast (~1.79 TB/s), but small. This ceiling is where the whole bottleneck comes from.

discrete GPU only, a separate pool

System RAM (DDR5)

The computer's main memory, what the CPU uses. Far slower than VRAM (dual-channel, ~100 GB/s). If the model does not fit in VRAM, the excess spills here (offloading) and speed collapses.

32 GB in this build, the CPU's memory

Unified memory

Apple's single memory pool. CPU, GPU and Neural Engine reach the same memory at the **same speed**. It plays the role of System RAM and VRAM at once, no split, no copy.

Apple Silicon only, M3 Ultra is now 96 GB (once up to 512)

Memory bandwidth

How many GB per second can be **read** from memory. In an LLM the weights are read for every token produced, so this sets the generation speed directly. Think of it as how wide the memory's hose is.

the single number that sets tok/s

KV cache

Attention's Key and Value values for each token. Stored so later tokens do not recompute the whole history. It grows as the context grows, taking room like a long notebook.

shares VRAM and memory with the weights

Context (length)

How many tokens the model can hold "in mind" at once, prompt plus generated answer. A bigger context means more KV cache, which means more memory. Expressed as 32K, 128K and so on.

feeding a whole repo is about this

OOM (Out of Memory)

Memory filling up and overflowing. On the 5090 it happens when weights plus KV cache exceed 32 GB; the model crashes or will not run. Avoided by trimming the context or choosing a smaller model.

the classic penalty of tight VRAM

mmap

A technique for mapping the model file into memory. Instead of copying the whole file at once, parts are pulled in as needed. The CPU manages the loading.

the plumbing under the load stage

### Compute units

CPU

A general-purpose processor. In an LLM it does not do the heavy maths; it handles the coordination work: tokenizing, sampling, orchestration and memory management. The real load is on the GPU.

Ryzen 9 7900X3D in this build

GPU

A processor that runs the same operation in parallel across thousands of small cores. The heart of LLM inference: model weights are read from its memory, matrix multiplies turn over on its cores.

the real workhorse

CUDA cores

The general parallel cores in an NVIDIA GPU. They do everything outside matrix multiply: activations (SiLU), softmax, normalization, RoPE, sampling prep.

the helper maths

Tensor cores

Special units in an NVIDIA GPU that do **only matrix multiply**. A transformer's heaviest maths, attention and FFN, runs on these. The real engine behind a fast prefill.

the 5090's secret weapon

GPU cores (Apple)

The cores in an Apple GPU. They handle both matrix multiply and the helper maths, doing the job of Tensor and CUDA cores on their own, but without that dedicated matmul muscle. Raw FLOPS are lower.

80-core on the M3 Ultra

Neural Engine (ANE)

Apple's AI accelerator. Against intuition, LLM engines like llama.cpp and MLX **do not use it**; the GPU does the work. A common misconception, and the ANE mostly sits idle.

not in play for LLMs

GEMM / matrix multiply

"General Matrix Multiply", the basic operation a transformer performs. In every layer, huge matrices are multiplied. A model "thinking" is, in practice, billions of matrix multiplies.

the Tensor cores' job

FLOPS

Floating-point operations per second, a measure of raw compute power. In compute-bound stages like prefill, high FLOPS sets the speed. The 5090's FLOPS are clearly higher than the M3 Ultra's.

the unit of compute power

### Pipeline stages & concepts

Token

The smallest piece of text the model sees, a word, syllable or letter group. The model processes the numbers (IDs) that map to tokens, not letters.

the currency of everything

Prefill

The stage where all prompt tokens pass through the model at once, in parallel. Where the model reads and understands the context. The reason behind first-reply delay (TTFT).

compute-bound

Decode

The stage that produces the answer token by token. Each time, a single token is produced and the weights must be read from memory. The real cost of generation is here.

bandwidth-bound, 99 percent of the time

Sampling / logits

The model produces a probability (logits) for every token in the vocabulary. Sampling picks the next one; temperature and top-p steer it.

"pick the next word"

TTFT

"Time To First Token", the time from sending the request to the first word arriving. The faster the prefill, the shorter the TTFT.

the output of prefill

tok/s

"Tokens per second", the count of tokens produced each second. The practical measure of generation speed; in decode, memory bandwidth sets it.

the unit of generation speed

Compute-bound

Speed limited by **processing power** (FLOPS). Prefill is like this, so Tensor cores shine and the 5090 pulls ahead.

set by FLOPS

Bandwidth-bound

Speed limited by **memory read speed**. Decode is like this, so memory bandwidth sets it.

set by bandwidth

2

Part two

## Memory and hardware: what fits, and how fast

## How much room does a model take?

We walked the pipeline above with the RTX 5090 and the M3 Ultra. The hardware comparison here widens the lens to the full current landscape. The mechanism is the same; what changes is capacity and bandwidth. First, the core sum:

parameter count × bytes per parameter = weight size

example: 70B model × 0.5 byte (Q4) ≈ 35 GB · 70B × 2 byte (FP16) = 140 GB

**Parameter (weight):** a single number the model learned during training. When people say "7B", "70B" or "671B", they mean the count of these numbers inside the model (B = billion). More parameters, a "smarter" but bigger model.

One question is left: how many bytes does each parameter take? That is set by **precision**, the next section.

## Precision & quantization (FP16, Q4, Q8...)

These terms answer one question: how precisely do we store each number? It is the single biggest thing that affects a model's size.

**First, what a bit is:** the smallest unit of information in a computer, just a 0 or a 1. The more bits you use to store a number, the more precise (detailed) you keep it, but the more room it takes. 8 bits = 1 byte.

**An analogy:** think of pi. Do you write it as "3.14159265358..." (very precise, lots of room), or as "3.14" (rough but enough, little room)? Precision is how "long" we write each parameter of the model. **Floating point (FP)** is the technical name for that long form:

**FP32** 32-bit, "full precision"

4 byte/param, most precise, fattest

**FP16 / BF16** 16-bit, "half precision"

2 byte/param, half the room

**FP8 / INT8 (Q8)** 8-bit

1 byte/param

**INT4 / NVFP4 (Q4)** 4-bit

~0.5 byte

**Quantization:** shrinking the model by **rounding** each parameter to fewer bits. "Q8" is about 8-bit (1 byte), "Q4" is about 4-bit (~half a byte). Q4 shrinks the model about 4x versus FP16, in exchange for a very small and usually unnoticeable quality loss.

**An analogy:** like compressing a high-resolution photo to JPEG. The file shrinks a lot, and to the eye it looks almost the same. Names like "Q4\_K\_M" are one of the different recipes for this compression (K\_M is a balanced variant). **NVFP4** is NVIDIA's own 4-bit format; the same idea, optimised for the hardware.

A practical shortcut (in GB)

**FP16 ≈ params × 2 · Q8 ≈ params × 1 · Q4 ≈ params × 0.55**

Most people run **Q4** locally: that is the sweet spot, small enough to fit in memory, good enough to keep the quality.

## The four things that fill memory

When a model loads, it is not one thing but four taking up room. The total need is their sum:

weights + KV cache + activations + overhead

Roughly, in proportion (at a medium-length context):

weights ~78%

KV ~14%

act.

oh.

### Weights

biggest piece, fixed

All the knowledge the model learned in training, billions of parameters. This is the model's "brain". Loaded once, unchanged from start to finish. Its size is the earlier sum (parameters times precision).

Analogy: every book in the library, permanent, always there.

### KV cache

grows with context

The model's short-term memory of the current conversation. It grows with each new token, so the model does not recompute the past. The longer the context (prompt plus answer), the more room it takes.

Analogy: the notebook where you jot what has been said in a meeting; it fills as it runs long.

### Activations

temporary, small

The temporary intermediate values used while a single token is computed. Wiped as soon as the maths is done, recreated for the next token. Usually a small footprint.

Analogy: the scrap paper you use for a calculation, then throw away.

### Overhead

fixed, small

The fixed cost of the software running it (the inference framework, the CUDA or Metal driver). The base space taken when the program opens. Independent of the model, small, and roughly constant.

Analogy: the RAM an app takes the moment you open it, before doing anything.

Shortcut: total ≈ weights × ~1.2

At a medium-length context, KV plus activations plus overhead add roughly 20 percent on top of the weights. At a very long context (say 128K tokens) the KV cache swells and that share grows, and then you need to count KV separately.

## Memory types: HBM, GDDR, LPDDR...

These memory types keep coming up in the comparison table. Let me explain each in everyday language so they stick.

GDDR7

The fast memory used in gaming and consumer graphics cards (like the RTX 5090). Fast and relatively affordable. It is the technology that makes up VRAM.

**Speed class:** very fast (~1.79 TB/s on the 5090).

HBM (HBM3e)

**"High Bandwidth Memory"**, premium memory where the memory chips are stacked on top of each other and placed right next to the GPU. It gives extraordinary width but costs a lot; it is data-centre class.

**Analogy:** if GDDR is a one or two-lane fast road, HBM is a 16-lane motorway. ~7+ TB/s.

LPDDR5X

**"Low Power DDR"**, the efficient memory type used in phones and laptops. High capacity and energy-friendly, but not as fast as HBM. NVIDIA's Grace CPU uses it as a large pool.

**Speed class:** medium (~396 GB/s), even lower than the Mac's bandwidth.

VRAM

The memory attached to the graphics card (GPU) itself. While the model runs, the weights sit here. It is fast but limited in capacity (for example 32 GB on the RTX 5090).

**Analogy:** the GPU's desk, only what it is working on right now fits on top.

Unified memory

The CPU and GPU sharing a single memory pool (as on Apple Silicon). No separate VRAM, no data copying. The whole pool runs at **one speed**.

**Analogy:** everyone sharing the same desk, nobody passing anything to anybody.

Coherent memory

Two **separate** memory pools (for example the CPU's LPDDR plus the GPU's HBM) behaving as one, where both processors can reach all of it. On the NVIDIA GB300, NVLink-C2C provides this.

**The difference:** unified means physically one pool; coherent means two pools managed as one.

Memory bandwidth

How many GB per second can be **read** from memory (GB/s, TB/s). It sets the LLM's speed (tok/s) directly, the most important idea in this section.

**Analogy:** the width of the tap; a wider hose moves more water in the same time.

MoE / active parameters

The **whole** model stays in memory, but for each token only a small subset of "experts" runs. Capacity is set by the whole model, speed only by the active part.

**Critical:** MoE does not save room, it saves **speed**. 671B still wants 671B of room.

## What fits in ~750 GB?

We know the sum now. Here are a few current frontier models, their sizes, and whether they fit in a large memory (748 to 768 GB). We leave ~50 to 80 GB for KV plus overhead.

| Model | ~Params (type) | Q4 (~0.55) | Q8 (~1.05) | Fits in ~750 GB? |
| --- | --- | --- | --- | --- |
| Llama 70B | 70B dense | ~38 GB | ~73 GB | ✓ easily (even FP16) |
| Qwen 3.5 | ~397B MoE | ~218 GB | ~417 GB | ✓ comfortably |
| DeepSeek V4 | ~671B MoE | ~370 GB | ~705 GB | Q4 ✓ / Q8 very tight |
| GLM 5.2 | ~744B MoE | ~410 GB | ~780 GB | Q4 ✓ / Q8 × |
| Kimi K2.6 | ~1T MoE | ~560 GB | ~1.05 TB | Q4 ✓ / Q8 × |

So at Q4, models up to a trillion parameters can fit. But "fitting" is half the story; the other half is the next section.

## The crucial point: "fitting" is not "running at full speed"

This is what really separates the hardware. A model can fit in memory, but how fast it runs depends on **which part of the memory** it sits in.

The reason is the bandwidth from stage 05: tok/s = (bytes read per token) ÷ (the bandwidth of that memory). So whether the memory is **flat (uniform) or tiered** changes everything:

### Flat / uniform

Mac (M3/M5 Ultra). One pool, one speed. Wherever it sits, it is read at the same speed.

768 GB · ~1 TB/s all one speed

### Tiered

Asus GB300. A small very-fast region plus a large medium-speed region. Speed depends on where the model lands.

252 GB HBM 7.1 TB/s

496 GB LPDDR 396 GB/s

### Tiny but very fast

RTX 5090. Small but blazing VRAM; if it overflows, it drops to slow RAM over PCIe.

32 GB 1.79 TB/s

system RAM ~100 GB/s, behind PCIe, very slow

Example: how does DeepSeek 671B Q4 (~370 GB) run on the Asus?

The model is 370 GB. The first **252 GB fits in HBM and flies at 7.1 TB/s**, while the remaining ~118 GB spills to LPDDR and is read **slowly at 396 GB/s**. So "748 GB, it fits" does not mean "all of it runs at full speed". MoE is the saviour here: if the active experts can mostly be kept in HBM, the practical speed stays high.

An important distinction: the Asus's slow tier (LPDDR, 396 GB/s, over NVLink-C2C) is **far better** than a PC spilling to system RAM over PCIe (~100 GB/s). Even the GB300's second tier is many times faster than the 5090's overflow scenario. The same Grace Blackwell idea scaled up to a full rack lives in [NVIDIA's rack-scale AI systems](https://silicontales.com/nvidia-vera-rubin-nvl72/).

## Four machines, side by side

One job (a local LLM), four hardware philosophies. None of them wins at everything: the corners of the triangle are different, fast-pool capacity, bandwidth, and shape (flat or tiered).

### RTX 5090 PC

tiny-but-fastest · available

Fast pool32 GB GDDR7

Bandwidth~1.79 TB/s

Shapesingle fast pool  
\+ slow RAM

Price~$2,000 (card)

### Mac Studio M3 Ultra

balanced · available (96 GB)

Pool96 GB unified

Bandwidth819 GB/s

Shapeflat (uniform)

Price~$5,300

### Mac Studio M5 Ultra

big + fast · soon (rumour)

Pool~768 GB unified\*

Bandwidth~1.1 TB/s (rumour)

Shapeflat (uniform)

Price$10,000+ (estimate)

### Asus ET900N G3

frontier · enterprise · available

Pool748 GB coherent

Bandwidth7.1 TB/s (HBM)  
396 GB/s (LPDDR)

Shapetiered

Priceenterprise (tens of thousands)

|  | RTX 5090 PC | Mac M3 Ultra 96GB | Mac M5 Ultra (soon) | Asus ET900N G3 (GB300) |
| --- | --- | --- | --- | --- |
| Fast pool | 32 GB GDDR7 | 96 GB unified | ~768 GB unified\* | 252 GB HBM3e |
| Fast-pool bandwidth | ~1.79 TB/s | 819 GB/s | ~1.1 TB/s (rumour) | 7.1 TB/s |
| Second / slow pool | system DDR5 (~100 GB/s, PCIe) | one pool only | one pool only | 496 GB LPDDR5X (396 GB/s) |
| Total usable | 32 GB fast | 96 GB | ~768 GB | 748 GB |
| Shape | tiny-but-very-fast | flat (uniform) | flat (uniform) | tiered |
| Fits at full speed | ≤~28 GB (≤~50B Q4) | ≤~85 GB (≤~150B Q4) | ≤~700 GB (frontier included) | ≤252 GB in HBM (≤~450B Q4) |
| Fits at all (incl. slowly) | spill to RAM, very slow | 96 GB ceiling | up to ~768 GB | up to 748 GB (~1T params) |
| Status | available | available | ~Q4 2026 (rumour) | available |
| Best at | highest tok/s on ≤32 GB models | balanced, quiet, affordable | big + fast (future promise) | frontier models + enterprise AI |

\* The M5 Ultra's 768 GB option was tested by Apple but may not ship at that capacity given the memory shortage. All M5 Ultra figures here are rumour or leak, not official.

## Summary, a mind map

Both parts come down to the same handful of ideas.

PIPELINE · 01

### Two regimes: prefill vs decode

**Prefill is compute-bound**, so the 5090's Tensor cores win and digest prompt and context fast. **Decode is bandwidth-bound**, so speed depends on memory read speed. First-token latency and generation speed lean on completely different components.

MEMORY · 02

### Capacity = parameters × precision

This multiplication decides whether a model **fits**. At Q4, about half a GB per billion parameters. Total need = weights + KV cache + activations + overhead (≈ weights × 1.2).

MEMORY · 03

### Speed = the bandwidth of the memory it sits in

tok/s = (bytes read per token) ÷ bandwidth. This is where MoE helps: few active params means little reading means fast decode (even on a 4x bigger model). But MoE saves speed, not capacity.

HARDWARE · 04

### "Fitting" is not "at full speed"

A flat pool (Mac) reads everywhere at the same speed. A tiered pool (Asus) fits a big model, but speed depends on how much lands in the fast HBM. The 5090 is light-speed yet small; let it overflow and it collapses behind PCIe.

HARDWARE · 05

### The crossover narrowed

For **anything that fits in ≤32 GB**, the consumer GPU (5090) is fastest. Mac and workstation only win for bigger models. Apple's 96 GB cap narrowed that range; the M5 Ultra (768 GB) and the Asus GB300 (748 GB) reopen it, but one is a rumour and the other is enterprise-priced.

FOR YOU · 06

### You already have a 5090

On ≤32 GB models the 5090 is fast and enough; System RAM and PCIe only come into play if the model overflows (and then speed collapses). For bigger models the real question is not technical but strategic: do you **need** to run the frontier **locally** (privacy, zero API cost), or is the API enough? We weighed exactly that in [local model versus cloud](https://silicontales.com/local-llm-vs-cloud/).

## Frequently asked questions

The short answers, each one drawn straight from the guide above.

### What decides whether an LLM fits on my machine?

Capacity equals parameter count times bytes per parameter. At Q4 a model needs roughly half a gigabyte per billion parameters, plus about 20 percent more for KV cache, activations and overhead, so total memory is roughly weights times 1.2.

### What sets the generation speed (tokens per second)?

Decode is bandwidth bound. Tokens per second is roughly the bytes read per token divided by the bandwidth of the memory the model sits in. The faster that memory, the faster the output.

### Why can a Mac keep pace with a discrete GPU despite slower memory?

Mixture of experts. A MoE model keeps all of its weights in memory but reads only a small active subset for each token, so a much larger model still reads little and decodes quickly. MoE saves speed, not capacity.

### Does fitting in memory mean running at full speed?

No. On tiered memory such as the GB300, a model fits across a fast HBM tier and a slower LPDDR tier, and speed depends on how much sits in the fast tier. A uniform pool like a Mac reads everywhere at one speed.

### Is an RTX 5090 enough for local LLMs?

For anything that fits inside its 32 GB it is the fastest option here. Larger models need a big unified pool like a Mac or a workstation like the GB300. Spilling a 5090 to system RAM over PCIe collapses the speed.

### What is quantization, and what do Q4 and Q8 mean?

Quantization rounds each parameter to fewer bits to shrink the model. Q8 is about one byte per parameter and Q4 is about half a byte, roughly four times smaller than FP16, with a small and usually unnoticeable quality cost.