---
type: source-summary
source_id: src-2026-08-25-bytebytego-stealing-reasoning-traces
source_title: "How to Steal an AI Model's Private Thoughts"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-to-steal-an-ai-models-private
created: 2026-08-26
updated: 2026-08-26
tags:
  - source/summary
  - reasoning-traces
  - ai-security
  - model-distillation
  - prompt-injection
  - privacy
status: active
---

# ByteByteGo - How to Steal an AI Model's Private Thoughts

## Summary

A walkthrough of an August 2026 paper from MATS Research, the ELLIS Institute Tübingen, and the Max Planck Institute for Intelligent Systems showing that the **encrypted reasoning blocks** Anthropic, OpenAI, and Google return to API clients do not keep the reasoning private. A block obtained from a flagship model can be replayed into a cheaper model in the same family, which will transcribe the hidden reasoning in plaintext.

The failure is not cryptographic. The envelope's guarantees hold throughout. What is missing is a **binding between a block and the context that produced it** — a decision about which fields go into the authenticated portion.

## Key claims

- **A reasoning model produces three artifacts, not two:** the visible answer, a short summary labelled "thinking," and the full trace that is never shown. The summary is generated separately and can diverge from what it summarizes.
- **The trace is denser and more revealing than the answer.** It holds abandoned hypotheses, raw tool output, and whatever secrets were in session. The article's example is exact: an agent asked to remove hardcoded credentials must read those credentials, so they pass through the trace before any answer exists.
- **Two motives for hiding traces.** Commercial — a trace supplies methodology, not just an endpoint, and is therefore better distillation material. Safety — the filter that turns a trace into a safe answer runs *after* the trace exists, so publishing the trace skips the filter.
- **Statelessness forces a choice.** Either the provider stores traces server-side (simple, expensive at global scale) or it encrypts them and hands them back to the client to resend (free storage). All three providers chose the second.
- **The envelope is an AEAD structure** — base64 over a header (model name, block type, version, key id), nonce, auth tag, and ciphertext. It is called `signature` at Anthropic, `encrypted_content` at OpenAI, `thinkingSignature` at Google.
- **The account and the conversation are absent from the authenticated fields.** Evidence points toward a single global key across an entire ecosystem. No provider has published the scheme; the researchers inferred it from observable behaviour.
- **Three widening compatibilities follow:** cross-session (replay out of order, blocks from old sessions work in new ones — this is what makes history editing and context trimming work), cross-user (a block from one account is accepted from another), and cross-model (a block from one model is accepted by another — this is what makes mid-conversation model switching and rerouting work).
- **Tested across every source/target pair available in July 2026:** Claude accepted almost every combination except Fable 5, whose blocks only Fable 5 accepted; GPT was generation-scoped, with the GPT-5.6 series accepting all earlier generations and older models accepting only their own; Gemini accepted every combination across every generation.
- **The extraction exploits uneven protection inside a family.** Flagships such as Claude Opus 4.8 and GPT-5.6 Sol get anti-distillation training and verbatim-match filters; cost-optimized siblings such as Claude Haiku 4.5 and GPT-5.6 Luna get far less. Ask the strong model an ordinary question, discard the answer, keep the block, open a fresh conversation with the weak sibling, attach the block, ask for transcription. **The strong model's refusal training is never engaged, because it was never asked to disclose anything.**
- **The weak model is a "fuzzy decoder"** — it approximates rather than decrypts, which creates a verification problem the researchers solved with **billing records**. APIs report exact reasoning-token counts because charges depend on them; re-encoding the recovered text should reproduce that count. Across 120 programming problems the counts tracked closely — roughly 1:1 for Claude.
- **Difficulty varied by provider.** One fixed prompt sufficed for Claude; GPT needed up to 50 candidate extractions per block and output chunked below ~50 tokens to dodge a verbatim-reproduction rejection.
- **Four attack vectors.** Two use blocks the attacker generated — *distillation* (earlier work with approximate traces lifted a fine-tuned model's MATH500 accuracy from 68.4% to 76.0% over answer-only training; decoding 10,000 traces at Haiku 4.5 pricing costs about $720, and where blocks come from public datasets the frontier model is never queried) and *jailbreaking* (models are largely not trained to avoid *reasoning* about harmful topics, since constraining trace content is thought to degrade traces for safety monitoring; a demonstration drew extended reasoning about vehicle theft while the visible answer stayed responsible).
- **Two use other people's blocks.** A scan of 6,708 public agent trajectories from GitHub and Hugging Face decoded 315,320 blocks and found, from genuine user sessions, **62 API keys, 33 passwords, 24 access tokens, 7 private keys, and 30 personal email addresses**; 1,028 blocks held at least one confirmed leak across 328 of the 6,708 sessions. The fourth vector is prompt injection: plant an instruction inside a block in a shared trace, and it executes when someone resumes that expensive run. A demonstration ported a block instructing PowerPoint upload to an external address into GPT-5.6 Sol alongside an unrelated slide-editing request; the script added the slide and uploaded the deck.
- **Sanitisation reaches plaintext only.** Publishers cannot scrub blocks because they cannot read them. Every one of those 62 API keys would have survived perfect scrubbing of visible text.
- **Two incidental findings.** Summaries and traces diverge — on an AIME 2025 problem the summary described methodical work through the geometry using the law of cosines, while the recovered trace stated the answer from memory and worked backward with several wrong guesses. And recovered GPT traces are frequently not fluent English but compressed telegraphic notes, which matters because trace monitoring depends on traces being legible.
- **Mitigations, in ascending cost.** Cheapest: embed an account identifier in the authenticated data and reject mismatches — this closes cross-user replay entirely with no server storage. Harder: cross-session binding, because forking, compaction, and mid-conversation downgrades all depend on the same portability; the proposal is a hash chain tying each block to its predecessor's fingerprint plus a Merkle tree keeping only roots once old blocks are pruned. For already-published blocks the only retroactive remedy is key rotation, which also invalidates legitimate continuations.

## Why it matters

The vault had **no coverage of encrypted reasoning blocks, anti-distillation training, or trace-level leakage**. This source supplies all three, and it lands squarely on an argument already running through [[Agent Security and Governance]]: the boundary that matters is not the one you drew, it is the one an attacker can reach around.

The single most transferable claim is the last takeaway: **the security of a model family is the security of its least protected member.** Anti-distillation training on a flagship buys little while a cheap sibling accepts the same blocks. That is a systems property, not a model property, and it generalizes to any tiered deployment where a strong and a weak component share a trust artifact.

The public-trace scan also converts an abstract risk into an operational one for anyone in this vault's audience who publishes agent traces for reproducibility — which [[AI Agents in Production]] and [[Multi-Turn Evaluation]] both encourage.

## Tensions and open questions

- **This is a secondary explainer of a primary paper.** ByteByteGo carries its own disclaimer that the post is based on publicly shared details and invites correction. Specific numbers should be cited to arXiv:2608.09867 rather than to this summary.
- **The scheme was inferred, not documented.** No provider has published its envelope design, so "a single global key across an ecosystem" is an inference from behaviour. It is a well-evidenced inference, but the vault should hold it as such.
- The 1:1 token-count verification is strong evidence of faithful reconstruction but is not proof; a fuzzy decoder could in principle produce a plausible trace of the right length.
- Cross-session portability is not a bug that can simply be removed — history editing, context compaction, and model downgrade are real features built on it. The mitigation section is honest that the fix has a product cost.
- The jailbreak vector rests on a deliberate safety trade-off: traces are left unconstrained *so that* they remain useful for monitoring. This source shows the cost of that choice without resolving it.
- If recovered GPT traces are telegraphic and non-fluent, what exactly is trace-based safety monitoring reading?
- The finding that summaries misrepresent traces has implications well beyond security — it undercuts the visible "thinking" block as evidence of how an answer was reached.

## Affected pages

- [[Reasoning Trace Privacy]] - new
- [[Agent Security and Governance]]
- [[Knowledge Distillation]]
- [[LLM Reasoning]]
- [[Context Engineering]]
- [[Anthropic]]
- [[OpenAI]]
- [[ByteByteGo]]
- [[AI Agents in Production]]

## Raw capture

- [[2026-08-25 ByteByteGo - How to Steal an AI Model's Private Thoughts]]

## Citations

- *Stealing Reasoning Traces from Proprietary LLM APIs*, arXiv:2608.09867 (MATS Research, ELLIS Institute Tübingen, Max Planck Institute for Intelligent Systems)
- *Let's talk about encrypted reasoning*, Cryptography Engineering blog, 2026-05-29
- *How to Steal Reasoning Without Reasoning Traces*, arXiv:2603.07267
- *Leaky Thoughts: Large Reasoning Models Are Not Private Thinkers*, arXiv:2506.15674

## Related pages

- [[Reasoning Trace Privacy]]
- [[Agent Security and Governance]]
- [[Knowledge Distillation]]
- [[LLM Reasoning]]
- [[Anthropic]]
- [[OpenAI]]
- [[ByteByteGo]]
- [[AI Knowledge Base Overview]]
