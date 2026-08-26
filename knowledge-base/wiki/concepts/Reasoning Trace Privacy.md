---
type: concept
created: 2026-08-26
updated: 2026-08-26
tags:
  - concept
  - security
  - reasoning-traces
  - privacy
  - model-distillation
source_ids:
  - src-2026-08-25-bytebytego-stealing-reasoning-traces
status: active
---

# Reasoning Trace Privacy

## Definition

**Reasoning trace privacy** is the question of who can read a model's hidden chain of thought. Frontier providers withhold the full trace and return, in its place, an **encrypted reasoning block** the client stores and resends on the next turn. This page records what those blocks do and do not protect.

## Why it matters

A trace is more revealing than the answer it produces. It holds abandoned hypotheses, raw tool output, and any secret that passed through the session — and it is the *methodology* rather than the endpoint, which is what makes it valuable to a competitor. The canonical example from [[ByteByteGo - How to Steal an AI Model's Private Thoughts]] is exact: an agent asked to remove hardcoded credentials from a repository must read those credentials, so they enter the trace before any answer exists.

Two motives drive concealment. **Commercial:** traces are superior distillation material. **Safety:** the filter that turns a completed trace into a safe visible answer runs *after* the trace exists, so exposing the trace bypasses the filter.

## Why the encryption does not deliver privacy

The block is an AEAD envelope — base64 over header, nonce, authentication tag, and ciphertext — called `signature` at Anthropic, `encrypted_content` at OpenAI, and `thinkingSignature` at Google. The cryptography works. **The failure is in what got authenticated.**

The header covers the model name and version. It does **not** cover the account that produced the block or the conversation it belonged to. Evidence points to a single global key per ecosystem. Because origin is unauthenticated, a valid block is valid everywhere, in three widening senses:

| Compatibility | The block is accepted... | The legitimate feature it enables |
| --- | --- | --- |
| Cross-session | out of order, and in new sessions | editing history, compacting long sessions |
| Cross-user | from a different account | none |
| Cross-model | by a different model | mid-conversation switching, rerouting |

This is why the vulnerability is awkward to fix. Cross-user portability serves no product purpose and can simply be closed. Cross-session portability is load-bearing for features users rely on.

## The attack: a family is only as secure as its weakest member

Cross-model compatibility meets an asymmetry in training. Flagships receive anti-distillation training and verbatim-match filters; cost-optimized siblings in the same family receive far less. So:

1. Ask the strong model an ordinary question. Keep the encrypted block, discard the answer.
2. Open a fresh conversation with the cheap sibling.
3. Attach the block as prior context and ask for the attached reasoning to be transcribed.
4. The cheap model prints the strong model's reasoning in plaintext.

**The strong model's refusals never engage, because it was never asked to disclose anything.** Its output filter saw only a benign answer. The weak model is a *fuzzy decoder* — it approximates rather than decrypts.

The generalizable lesson is a systems claim, not a model claim: **anti-distillation training on a flagship buys little while a cheaper sibling accepts the same trust artifact.** Any tiered deployment where a strong and a weak component share a credential, cache, or envelope inherits this shape.

## Verification by billing

Reconstruction raises an evaluation problem — without the original, how do you know the recovered text is faithful rather than plausible invention? The researchers used **billing records**: APIs report exact reasoning-token counts because charges depend on them, so re-encoding the recovered text should reproduce that count. Across 120 programming problems the counts tracked closely, roughly 1:1 for Claude.

This is worth remembering as a technique in its own right. When a system's output is hidden but its *cost* is metered precisely, the meter is a side channel that can validate a reconstruction.

## Four consequences

Two use blocks the attacker generated: **distillation** (traces supply decomposition and intermediate steps, not just endpoints) and **jailbreaking** (models are largely not trained to avoid *reasoning* about harmful topics, because constraining trace content is believed to degrade traces for safety monitoring — so the trace can carry specifics the visible answer withheld).

Two use other people's blocks, and these are the ones that make this an operational concern rather than a research curiosity:

- **Leaked secrets in published traces.** Developers publish agent trajectories for reproducibility. They sanitise the visible text; they cannot sanitise blocks they cannot read. A scan of 6,708 public trajectories recovered API keys, passwords, access tokens, private keys, and personal email addresses from genuine sessions. **Perfect scrubbing of plaintext would have removed none of them.** Blocks must be *removed*, not cleaned.
- **Prompt injection via a planted block.** Long agentic runs are expensive to repeat, so resuming a published run is attractive. A block carrying an instruction, processed as prior context on resume, executes. This extends the injection surface described in [[Agent Security and Governance]] to an artifact that is opaque by design — the defender cannot inspect the payload either.

## The summary is not the trace

A separate finding, with implications beyond security: the visible "thinking" block is a *different artifact* generated separately, and the two can diverge. On an AIME problem the summary described methodical geometric work, while the recovered trace stated the answer from memory and reverse-engineered a justification through several wrong guesses.

This matters to [[LLM Reasoning]] and to anyone treating displayed reasoning as evidence of process. It is the same caution [[Latent-Space Reasoning]] raises from the other direction: what is shown is not necessarily what happened. Recovered traces were also often telegraphic and ungrammatical rather than fluent English — which undercuts trace-based safety monitoring, since that depends on traces being legible.

## Open questions

- The scheme was **inferred from behaviour**, not documented. No provider has published its envelope design, so "a single global key per ecosystem" is a well-evidenced inference rather than a confirmed fact.
- Cross-session binding via hash chains and Merkle roots is proposed but costs the fork/compact/downgrade features. Which does a provider give up?
- Already-published blocks were signed under a key encoding neither user nor session. Key rotation is the only retroactive remedy, and it invalidates legitimate continuations.
- If constraining trace content degrades traces for safety monitoring, and unconstrained traces are extractable, is there a stable position at all — or is the choice simply between two exposures?
- Should agent teams treat published traces as secrets by default, the way they treat `.env` files?

## Related pages

- [[ByteByteGo - How to Steal an AI Model's Private Thoughts]]
- [[Agent Security and Governance]]
- [[LLM Reasoning]]
- [[Knowledge Distillation]]
- [[Latent-Space Reasoning]]
- [[Context Engineering]]
- [[AI Agents in Production]]
- [[Defensive Deception for Open Models]]
- [[Anthropic]]
- [[OpenAI]]
