---
type: source-summary
created: 2026-07-03
updated: 2026-07-03
source_id: src-2026-07-03-bytebytego-openai-voice
source_title: "How OpenAI Delivers Low-Latency Voice AI for 900M Users"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-openai-delivers-low-latency-voice
tags:
  - source/summary
  - systems
  - voice-ai
  - webrtc
  - infrastructure
source_ids:
  - src-2026-07-03-bytebytego-openai-voice
status: active
---

# ByteByteGo - How OpenAI Delivers Low-Latency Voice AI

## Summary

This ByteByteGo teardown explains the WebRTC infrastructure OpenAI built to serve real-time voice to 900M weekly users. The core tension: **WebRTC assumes stable servers with fixed IPs/ports, while Kubernetes treats addresses as disposable.** OpenAI's original design was a single Pion-based Go service doing both signaling and media termination; at scale it hit **port exhaustion** (one UDP port per session → tens of thousands of public ports) and **state stickiness** (ICE/DTLS are stateful, so a session's packets must return to the process that started it).

The fix splits the stack into a **stateless relay** (a thin, geographically-distributed packet forwarder with a tiny public footprint) and a **stateful transceiver** (owns ICE, DTLS, SRTP, and the session lifecycle). The clever bit: the relay routes the first packet of a session by reading the **ICE ufrag** — a field WebRTC already exchanges during setup — into which OpenAI encodes routing metadata, avoiding a hot-path database lookup or an extra internal hop. They rejected the standard SFU model (built for multiparty; OpenAI's traffic is overwhelmingly 1:1) and TURN (adds setup round-trips).

## Key claims

- **Voice AI lives or dies on latency**, and audio must arrive as a continuous stream so the model can transcribe/reason/call tools while the user is still speaking; break the stream and the experience collapses to push-to-talk.
- **WebRTC** (ICE + DTLS + SRTP + RTCP) is the industry protocol for this; OpenAI employs original WebRTC architects (Justin Uberti) and the Pion maintainer (Sean DuBois), which shows in the design depth.
- **The Kubernetes mismatch** produces two failures: port exhaustion (cloud load balancers expect a few well-known ports) and state stickiness (stateful ICE/DTLS require session affinity).
- **Relay/transceiver split:** a stateless relay does protocol-aware packet routing at the edge and forwards encrypted payloads opaquely; a stateful transceiver behind it terminates the WebRTC session. Signaling goes straight to the transceiver; media enters via the relay.
- **First-packet routing via the ufrag:** OpenAI generates the server-side ICE username fragment during signaling and embeds a routing hint; the relay parses just the first STUN binding request to decode it, then every later packet uses the established source→transceiver map (cached in Redis for fast relay-restart recovery). Principle: *when you need data on the hot path, read what the protocol already exchanges.*
- **Global Relay + geo-steering:** identical relay ingress points are distributed worldwide; Cloudflare steers signaling to a nearby cluster, and the ufrag lets any relay route media to the right transceiver — shortening the first hop while the session stays anchored to one transceiver for its lifetime.
- **Deliberately simple implementation:** a userspace Go relay using `SO_REUSEPORT` (multiple workers share a UDP port), `runtime.LockOSThread` (pin flows to cores for cache locality), and pre-allocated buffers — they evaluated kernel-bypass and chose against it.
- **Explicit tradeoffs:** the whole design assumes 1:1 sessions (multiparty would need rework), carries a custom-infra maintenance burden, is "stateless" only in spirit (soft in-memory + Redis state), and depends on OpenAI controlling both ends of signaling.

## Why it matters

This is the vault's clearest **production real-time-systems** case study and the infrastructure half of the new [[Real-Time Voice AI]] concept — the transport layer that carries the audio the [[ByteByteGo - Inside Thinking Machines Interaction Models|interaction model]] would consume. It also extends [[ML Systems at Scale]]: the "bring data to the compute / read what the protocol already carries" and "place work near the user" patterns are the same locality laws seen across Netflix/Snap/Instacart, applied to media transport. First substantive [[OpenAI]] entity anchor in the vault.

## Tensions / open questions

- ByteByteGo's own disclaimer notes it is a third-party reconstruction of publicly shared details; exact latency numbers and failure rates are not given.
- The 1:1 assumption is load-bearing; how OpenAI would add multiparty (group calls, human handoff) without an SFU is unresolved.
- The relay's "stateless" framing is qualified by its Redis-backed soft state; the durability/consistency behaviour under relay churn is only sketched.

## Affected pages

- [[Real-Time Voice AI]]
- [[ML Systems at Scale]]
- [[OpenAI]]
- [[AI Knowledge Base Overview]]

## Citations

- Raw capture: `knowledge-base/raw/sources/How OpenAI Delivers Low-Latency Voice AI for 900M Users.md`
- Source URL: [https://blog.bytebytego.com/p/how-openai-delivers-low-latency-voice](https://blog.bytebytego.com/p/how-openai-delivers-low-latency-voice)

## Related pages

- [[Real-Time Voice AI]]
- [[ByteByteGo - Inside Thinking Machines Interaction Models]]
- [[ML Systems at Scale]]
- [[OpenAI]]
- [[ByteByteGo]]
- [[AI Knowledge Base Overview]]
