---
title: "How to Steal an AI Model’s Private Thoughts"
source: "https://blog.bytebytego.com/p/how-to-steal-an-ai-models-private?utm_source=post-email-title&publication_id=817132&post_id=210942397&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-08-25
created: 2026-08-26
description: "In August 2026, a team at MATS Research, the ELLIS Institute Tübingen, and the Max Planck Institute for Intelligent Systems wanted to test whether the encrypted reasoning blocks that Anthropic, OpenAI, and Google hand back to clients actually keep that reasoning private."
type: raw-source
source_id: src-2026-08-25-bytebytego-stealing-reasoning-traces
captured: 2026-08-26
tags:
  - source/raw
  - reasoning-traces
  - ai-security
  - model-distillation
  - prompt-injection
  - privacy
---
## Secure AI and MCP with protocol-level access control (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!tQj0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2671a1da-90b1-485d-93df-351978e2a5cf_512x269.png)

Securing AI usually requires hardcoding permissions into application code for every MCP server, or using static API tokens for all-or-nothing access (and hoping your LLM doesn’t drift from intended actions).

Teleport eliminates these problems with zero-code MCP integration that applies the same zero trust security principles you use for human engineers:

- Least privilege access control that denies new tools by default
- Just-in-time (JIT) access requests for high-risk tools
- Logs for every action – with full audit and identity context
- Zero trust agent access to MCP servers, databases, and Kubernetes clusters

No need to write authorization code, rewrite MCP servers, or limit agent work.

---

When an AI model handles a difficult question, it produces three separate pieces of text:

- The first is the answer displayed on screen.
- The second is a shorter block, usually labeled thinking or reasoning, that appears while the answer is being assembled.
- The third is the model’s full reasoning process, which is never displayed.

The second piece of text is a summary of the third. It is generated separately and shown in place of the original reasoning process. The full reasoning runs longer. It also contains material that the summary leaves out. Most major providers withhold it. However, in place of the complete process, an encrypted version is shared with the client during the conversation.

In August 2026, a team at MATS Research, the ELLIS Institute Tübingen, and the Max Planck Institute for Intelligent Systems wanted to test whether the encrypted reasoning blocks that Anthropic, OpenAI, and Google hand back to clients actually keep that reasoning private. They showed that the blocks can be replayed into a cheaper model in the same family, which will then print the hidden reasoning in plaintext. In other words, the AI model’s thoughts are stolen, exposing information that should ideally be hidden.

In this article, we will cover what the researchers found out:

- Reasoning traces, and how they differ from answers and summaries
- Why providers withhold reasoning
- The storage problem that creates, and the two ways to solve it
- What the encrypted block contains, and what it authenticates
- The three forms of compatibility that follow
- The extraction method and its verification
- The four attack vectors
- Findings from a scan of published session logs
- The proposed fixes, and the limit that remains

![](https://substackcdn.com/image/fetch/$s_!Omyy!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c0596d3-72d6-49f2-8789-12bd919cadbe_2734x1512.png)

*Disclaimer: This post is based on publicly shared details from various sources. References at the end. Please comment if you notice any inaccuracies.*

## Reasoning Traces

Modern frontier models first generate an extended internal sequence of text before producing a visible answer. For example, if we ask a model to solve a hard mathematics question, the model may generate two thousand words of exploration, dead ends, and corrections, which ultimately helps it write a clean two hundred-word answer. This longer sequence of exploration is the reasoning trace, which is also known as the chain of thought.

The trace holds intermediate hypotheses that the model may have tried and abandoned. It contains the raw output of any tools that were called, the user’s data as the model processed it, and whatever contextual secrets were present in the session. Unsurprisingly, this trace is much denser and more revealing than the final polished output.

For example, if we ask a coding agent to remove hardcoded credentials from a code repository, the agent has to read those credentials to do the work. In other words, the credentials pass through the reasoning trace before any answer is produced.

## Concealment Rationale

Why do the model providers hide these reasoning traces?

There are two separate motivations:

- The first is commercial. A competitor can collect a large number of traces from a strong model to create training material for building a cheaper imitation of the strong model. This is because the final answer just provides the endpoint of a computation, whereas a trace provides the methodology behind the answer.
- The second is safety-related. A model sometimes has to generate reasoning about a harmful topic to refuse. The filtering that turns a completed trace into a safe visible answer runs after the trace already exists. Publishing the trace skips that filter and lets that information be seen by the user.

## State Management

Withholding a trace from reaching the user does not mean that the trace is not needed. In a multi-turn conversation, the reasoning from an earlier turn has to be available on the next turn. For example, a request to a model API carries no memory of what came before. The continuity we see in a chat window is reconstructed by the client resending the full history with every message. However, the server is stateless, which means it stores nothing between requests.

This leaves us with two options:

- The first option keeps the state on the server. The provider stores the trace in its own database, returns a meaningless identifier to the client, and looks it up when the next message arrives. This is straightforward but expensive because it means storing state for every conversation from every user of a global service.
- The second option encrypts the trace and returns it to the client, which stores the block and sends it back with each subsequent request. In this case, the provider stores nothing.

![](https://substackcdn.com/image/fetch/$s_!yjO5!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c0e1b7b-291f-4147-851f-d1a12364def7_2898x1560.png)

Providers like OpenAI, Anthropic, and Google chose the second option. Confidentiality keeps competitors from reading the trace, integrity prevents an altered trace from being fed back, and statelessness removes the storage cost. As you can see, two of those are security goals, and the third is a cost goal.

## Envelope Structure

So what is actually inside the block that gets sent back to the client?

It consists of a long string of base64 text, which is a way of writing binary data using ordinary letters and digits so that it survives inside JSON. Once decoded, it is an AEAD envelope. AEAD stands for Authenticated Encryption with Associated Data, and it accomplishes two tasks at once: hiding the content and proving that the content was not altered. The associated data portion holds extra fields that stay readable while remaining tamper-protected.

The envelope carries a header. Depending on the provider, it can include the model name, block type, version, and key identifier. Alongside that is a nonce, which is a random value used once per encryption so that identical content produces different-looking output each time, an authentication tag, and the ciphertext. The field carrying all of this is called signature at Anthropic, encrypted\_content at OpenAI, and thinkingSignature at Google.

Authentication here proves that the contents came from the provider and were not modified afterward. The model name and version are covered by that proof. However, the account that generated the block and the conversation it belonged to are absent from the authenticated fields entirely. To make this clear, since no provider has published a description of the scheme, the researchers inferred this mainly from observable behaviour. The evidence points toward a single global key used across an entire ecosystem.

![](https://substackcdn.com/image/fetch/$s_!Q_3_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F14b5c7a8-5c4b-4e94-9995-b550e3fca742_3022x1884.png)

## Trace Compatibility

If the authenticated fields provide no information about the origin, a valid block stays valid everywhere. The researchers have described three forms of this, each more permissive than the last:

- Cross-session compatibility means a block can be replayed out of order, and blocks from earlier sessions work in new ones. This supports editing conversation history and trimming long sessions to fit a context window.
- Cross-user compatibility means a block produced in one account is accepted when submitted from another.
- Cross-model compatibility means a block from one model is accepted by a different one, which supports switching models mid-conversation and automatic rerouting.

The researchers tested every source and target combination available in July 2026. Some of the findings were as follows:

- Claude accepted almost every combination, the exception being Fable 5, whose blocks were accepted only by Fable 5.
- GPT was organised by generation. The GPT-5.6 series accepted blocks from all earlier generations, while older models accepted only their own.
- Gemini accepted every combination across every generation.

## Extraction Method

Cross-model compatibility carries a lot of importance because protection inside a model family is uneven.

Flagship models such as Claude Opus 4.8 and GPT-5.6 Sol receive anti-distillation training aimed at preventing disclosure of their own reasoning. It is present behind input and output filters that check for verbatim matches. However, smaller models in the same family, such as Claude Haiku 4.5 and GPT-5.6 Luna, are optimised for cost and speed. As a result, they receive far less of that training. In other words, cross-model compatibility means the smaller model accepts blocks produced by the larger one.

The information extraction method is a direct result of this gap in training. Here’s what can happen:

- A question is asked of the strong model, and the response returns a visible answer and an encrypted reasoning block.
- The answer is discarded, and the block is kept.
- Next, a fresh conversation is opened with a weaker model in the same family.
- The reasoning block is placed into it as prior context, and the request asks for the attached reasoning to be transcribed.
- The weaker model outputs the stronger model’s reasoning in plaintext.

In other words, the strong model was queried once, with an ordinary question, and was never asked to disclose anything. Therefore, its refusal training was never engaged, and its output filter received only a benign answer.

![](https://substackcdn.com/image/fetch/$s_!FPAa!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F39d4d9dc-671b-4bc3-93b1-a7fe45ff185c_2860x1798.png)

The researchers describe the weaker model as a fuzzy decoder, since it generates an approximation rather than performing exact decryption.

This results in a verification problem. Without access to the original trace, how do you establish that a reconstruction is faithful rather than a plausible invention? The researchers used billing records. API responses report the number of reasoning tokens consumed, and that figure is exact because the charge depends on it. Re-encoding the recovered text and counting its tokens produces a number that should match. Across 120 programming problems, the two counts tracked closely. It was roughly one to one for Claude.

The difficulty of this approach varied by provider. A single fixed prompt worked for Claude, while GPT required up to 50 candidate extractions per block and output chunked below roughly 50 tokens to avoid a rejection triggered by verbatim reproduction.

## Attack Vectors

The research paper talks about four consequences of this gap. These are split based on who produced the original block.

Two of them use blocks the attacker generated:

- **Distillation:** It involves training a copycat model on a target’s visible answers. Traces make it stronger, because a trace supplies the problem decomposition and the intermediate steps. For reference, earlier work using approximate traces raised the MATH500 accuracy of a fine-tuned model from 68.4 percent to 76.0 percent over answer-only training. Decoding 10,000 traces at Claude Haiku 4.5 pricing costs roughly $720, and where blocks come from public datasets, the frontier model is never queried.
- **Jailbreaking:** Models are trained to withhold harmful content from visible output. However, they are largely not trained to avoid generating reasoning about harmful topics, since constraining trace content is believed to degrade the usefulness of traces for safety monitoring. In one demonstration, a prompt drew out extended reasoning about vehicle theft while the visible answer stayed within a responsible write-up aimed at manufacturers. The recovered trace contained specific vulnerable makes and model years.

The other two vectors use blocks produced by other people.

Developers publish agent session logs routinely, for reproducibility or by committing them accidentally, and they sanitise the visible text before publishing. However, they cannot sanitise the encrypted blocks, because they cannot read them either.

The researchers collected 6,708 public agent trajectories from GitHub and Hugging Face and decoded 315,320 reasoning blocks, filtering the results through an automated pipeline to remove placeholders and benchmark fixtures. Here are some findings:

- From genuine user sessions, 62 API keys, 33 passwords, 24 access tokens, 7 private keys, and 30 personal email addresses
- Across all sources, 1,028 blocks holding at least one confirmed leak
- 328 of the 6,708 sessions leaking at least one item

Sanitisation operates on plaintext only, so even if every user in that sample had scrubbed their visible text perfectly, all 62 API keys would have remained in the reasoning blocks. This was a non-exhaustive scan of public traces, and logs held locally or produced by live services are likely to contain more.

![](https://substackcdn.com/image/fetch/$s_!Qz_w!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd93b34a9-6f49-4259-938e-853e41ef73b6_3014x1734.png)

The fourth vector is prompt injection. Long agentic runs are expensive to repeat. Therefore, it makes sense to resume a published run. Encrypted blocks make that possible.

A block containing an instruction can be planted in a shared trace. When the session resumes, that block is processed as prior context. In one demonstration, a block carrying an instruction to upload PowerPoint files to an external address was ported into a conversation with GPT-5.6 Sol and paired with an unrelated slide-editing request. The resulting script added the requested slide and uploaded the presentation.

## Field Observations

Recovering traces at this scale brought out findings unrelated to the vulnerability itself.

Summaries and traces sometimes diverge. On an AIME 2025 mathematics problem, the summary returned by the API described methodical work through the geometry using the law of cosines. The recovered trace opened by stating the answer from memory and then working backward toward a justification, with several wrong guesses along the way. The researchers did not measure how often this occurs. However, they note that a smaller model summarising a larger one will compress the original.

Recovered GPT traces are frequently not fluent English. They are made up of compressed telegraphic notes with articles dropped and grammar abandoned. This carries a direct consequence for oversight, because trace monitoring depends on traces being legible.

## Proposed Mitigations

The research paper ultimately makes one strong point, which is the cause of the overall problem. The envelope we talked about earlier authenticates the content of a reasoning block, but it does not authenticate the context in which that block was produced or replayed.

The cheapest fix for this problem should address cross-user replay. This involves embedding an account identifier inside the authenticated data at issuance, allowing the API to compare it against the authenticated caller and reject any mismatch. This closes the attack vector entirely without the need for server-side storage.

Cross-session binding is harder, because some genuine features depend on the same portability. Users can fork conversations, compact old turns out of long sessions, and downgrade models mid-conversation. Binding each block to the complete transcript would break all three. The proposal is a hash chain tying each block to its session and to the fingerprint of its predecessor, combined with a Merkle tree that retains only root fingerprints once older blocks are pruned. This approach preserves ordering cheaply while still allowing integrity checks over any surviving stretch.

Blocks already published present a separate problem, since they were signed under a key encoding neither user nor session. The only retroactive remedy is to rotate those keys and refuse to decode anything signed under a retired key identifier. This also invalidates legitimate continuations of old sessions.

Other measures include moving to server-side storage entirely, configuring API gateways to reject envelopes from a different model version than the one queried, and training models to decline transcription requests regardless of framing.

## Conclusion

We’ve now understood the key points in the research paper. Here are some of the main takeaways:

- This wasn’t a failure of cryptographic techniques. The guarantee made by the envelope remained throughout the flow. The missing piece was a binding between a block and the context that produced it, which is a decision about which fields go into the authenticated portion.
- The summary displayed alongside an answer is a separate artifact from the trace it describes, and the two can diverge.
- Sanitising a session log reaches the plaintext only. Encrypted blocks have to be removed rather than cleaned, since the person publishing them cannot inspect what they contain.
- The security of a model family depends on its least protected member. Anti-distillation training on a flagship model provides limited benefits while a cheaper sibling model accepts the same blocks.

**References:**

- [Stealing Reasoning Traces from Proprietary LLM APIs](https://arxiv.org/abs/2608.09867)
- [Let’s talk about encrypted reasoning](https://blog.cryptographyengineering.com/2026/05/29/fooling-around-with-encrypted-reasoning-blobs/)
- [How to Steal Reasoning Without Reasoning Traces](https://arxiv.org/abs/2603.07267)
- [Leaky Thoughts: Large Reasoning Models Are Not Private Thinkers](https://arxiv.org/abs/2506.15674)

---

∙