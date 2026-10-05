---
title: "JEV : What a Model Built for Decisions Rather Than Text Would Have to Look Like"
source: "https://vizuara.substack.com/p/jev-what-a-model-built-for-decisions?utm_source=post-email-title&publication_id=3466476&post_id=218752133&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[Siddhant Rai]]"
published: 2026-10-05
created: 2026-10-05
description: "Most of what we use AI for in production is a judgment/decision, not a sentence. Jev is a model built on that assumption trying to optimize prediction calibration, speed while reducing the compute."
tags:
  - "clippings"
---
## Table of contents

1. *Introduction*
2. *The semantics of language generation*
3. *The two systems, and a third*
4. *A generalized, constrained decision model*
5. *The Ideal Case*
6. *What is Jev?*
7. *Methodology*
	1. *A problem, and an open-source solution to it*
		2. *Architecture: the encoder was always the right tool*
		3. *Data: outcomes, not labels*
		4. *Training: what the objective actually asks for*
		5. *This is a calibration metric used as a loss*
		6. *RLCD: Reinforcement Learning for Calibrated Decisions*
		7. *RLCD against RLHF and RLVR*
8. *Hands-on Jev*
9. *Results*
10. *Thoughts*
11. *Conclusion*

## 1\. Introduction

Using a modern LLM to do a predictive task is harder than it should be, and the difficulty is structural rather than incidental. You want a label, a score, or a decision your code can branch on, and what you have is a system engineered to produce text for a human to read, so you coerce it; you ask for JSON in the prompt, constrain the decoding grammar, parse the result, and add a retry for when it comes back malformed anyway.

![](https://substackcdn.com/image/fetch/$s_!GBi3!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb2808b1-cf03-4196-ada2-51fa90c2b3ec_500x727.png)

Three problems follow:

- The estimates are uncertain in a way you cannot inspect, because a confidence number produced by a text generator was never trained to correspond to how often the model is actually right.
- Hallucination in a decision setting means a label outside your schema or a confident answer the context does not support.
- And cost is architectural, since autoregressive models emit one token at a time, each conditioned on the last, so a decision that is logically a single choice gets paid for as a sequence and the latency cannot be bought away with more hardware.

![](https://substackcdn.com/image/fetch/$s_!ZuR8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F60f05d61-6176-4d06-9a6b-9ab4b3031d62_1664x822.png)

What makes this worth dwelling on is that predictive tasks are not a niche corner of what we do. Routing a ticket, scoring a lead, flagging a transaction, judging whether a tool call is safe to run; the overwhelming majority of AI inside real software is making a judgment rather than writing something, and in almost every case we are using generation as a proxy for prediction. It works, which is why nobody has pushed on it, but proxies have a way of becoming invisible until somebody removes one.

That is what TypeSafe did in September with **Jev**, a model that does not generate text at all; you hand it context and typed questions defined in your code, and it returns choices, scores and calibrated probabilities directly, with nothing to parse. They call it the first **System One model**, after Kahneman’s fast intuitive mode of thought as against the slow deliberate System Two that chat models are built for. One caveat before we start, because it shapes what this article can be: there is no paper. TypeSafe spent two years in stealth and announced a new architecture, a new sampler and a new training algorithm while publishing essentially none of it, so instead of deriving somebody’s method from their description, we will ask what a model of this kind would have to look like built from first principles, and then hold that against what has actually been published.

*(Usual caveat: the information in this article is upper bounded by my own grasp of the topic, my patience for typing for hours, and a writing medium that still refuses to support inline LaTeX. Please re-visit everything you read here, and since there is no paper to point you to this time, go read the docs and form your own view.)*

---

## 2\. The semantics of language generation

Before we can say what a decision model should look like, we need to be precise about what we are asking a language model to do when we use one for prediction, and the cleanest way in is through an analogy most readers will already have strong feelings about.

### 2.1 Strongly typed, loosely typed

In a strongly typed language, you declare what a function returns and the compiler checks it before anything runs; a mismatch is caught at build time, and by the time the program executes, an entire class of error has been eliminated. In a loosely typed one, the same mismatch is discovered at runtime, which is to say in production, by a user. The argument for the former has never really been about aesthetics, it is that the contract is verified before the cost of being wrong is incurred.

Now look at how we currently get structured output from an LLM. You describe the shape you want in a prompt, the model generates a string, you parse it, and you discover whether the contract held. That is runtime checking in the worst sense, because the thing being checked is not even deterministic; the same prompt can honour the schema on one call and invent a category on the next. Structured output and constrained decoding tighten this considerably, but they tighten it by validating the string as it is produced rather than by removing the string from the problem.

![](https://substackcdn.com/image/fetch/$s_!Enb8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a824257-20e0-4c4a-9cd2-3520e7f7c0f4_1758x753.png)

*The same three-way choice, declared two ways. In the top row the contract is a sentence and the check happens after the fact; in the bottom row the contract is a type and the invalid answer has nowhere to come from.*

The thing worth noticing is that a typed question defined in your code is checkable in a way a prompt never is. If the answer space is an enum with three members, the return type is one of three members, and that is true before the model runs, not after it has spoken. That is the actual difference between the two paradigms, and the rest of this section is about why it costs so much to get there through generation.

### 2.2 How much of a sentence is actually information?

Take a sentence that encodes a decision, something like “Based on the transaction history, this appears to be a duplicate charge, and therefore the refund policy supports approving it.” How much of that is the decision?

The decision is roughly two bits. Duplicate or not, approve or not. Everything else is scaffolding; *based on, appears to be, and therefore, supports*. Those words are doing real grammatical work, they make the sentence a sentence, but they carry almost no information about the answer, and crucially they are highly predictable given what came before. Once a model has committed to “and there-”, the continuation “-fore” is nearly certain.

![](https://substackcdn.com/image/fetch/$s_!cTWv!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89250eca-7d3f-4655-8513-c4c594254cae_1768x837.png)

*Illustrative per-token surprisal for the sentence above. The information is concentrated in two positions; every other forward pass is spent emitting grammar.*

We have met this idea before, in the [Byte Latent Transformers article](https://vizuara.substack.com/p/byte-latent-transformers-patches), where the whole patching mechanism was built on exactly this observation; sequences of low-entropy bytes get grouped together because they are cheap and predictable, while high-entropy points are where the model should spend its attention. BLT used entropy to allocate compute within the input. The same lens applied to the output says something uncomfortable.

If we write the information content of a generated sequence as the sum of per-token surprisals,

$$
H \left(y\right) = - \Sigma_{i = 1. . \left|\right. y \left|\right.} l o g P \left(y_{i} \left|\right. y_{< i} , x\right)
$$

then for a decision expressed in prose, the overwhelming majority of that sum comes from a handful of positions and the rest contributes almost nothing. But an autoregressive model does not know that in advance, and more importantly it cannot act on it even if it did, because every token requires a forward pass regardless of how predictable it was. **You pay uniformly for a signal that is distributed extremely unevenly.** A decision worth two bits costs you forty forward passes, thirty-eight of which are spent emitting grammar.

And those passes are sequential, which is the part that no amount of hardware fixes. Each token is conditioned on the last, so the latency floor is the length of the output, not the size of your cluster.

### 2.3 Generation as constrained optimization

Let us make this precise, because the optimization framing is where the difference becomes structural rather than merely wasteful.

Unconstrained generation searches over all sequences the vocabulary can produce:

$$
y * = a r g m a x y \in V * o f P \left(y \left|\right. x\right)
$$

where V\* is every finite string over the vocabulary, an unimaginably large space of which the overwhelming majority is nonsense. The model’s job is to concentrate probability mass on the thin sliver that is fluent and relevant, and it does this remarkably well, which is the entire achievement of language modelling.

Structured output narrows the feasible set to the strings that satisfy a grammar:

$$
y * = a r g m a x y \in L o f P \left(y \left|\right. x\right) , L \subset V *
$$

This is a genuine improvement and it is why constrained decoding works. But read the mechanism carefully; at each step you compute a distribution over the full vocabulary and then mask out the tokens that would violate the grammar. The search space has been restricted, the *computation* has not. You are still taking |y| sequential passes, still evaluating all of V at each one, and still doing it to arrive at an answer that was, all along, one of three options.

Now write what we actually wanted:

$$
a * = a r g m a x o v e r a \in A o f P \left(a \left|\right. x\right) , \left|\right. A \left|\right. s m a l l a n d k n o w n
$$

![](https://substackcdn.com/image/fetch/$s_!WHkG!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ca807d9-a2c6-404c-a4c2-1485171bd3a0_1311x729.png)

*Three nested feasible sets. Constrained decoding moves you from the outer box to the middle one; a decision model operates natively in the inner one.*

The feasible set is no longer a subset of string space, it is a finite answer set defined in your code; A might have two members or two hundred, and Jev caps it at 255. And this changes the problem qualitatively rather than quantitatively, because when the answer set is small and enumerable you do not need to search it one token at a time. You can evaluate the whole distribution over A in a single pass, which is precisely what removes both the sequential latency and the uniform cost on uninformative tokens.

That is the gap this article is about. Constrained decoding projects a generation problem onto the feasible set after the fact. What we are describing optimizes over the feasible set natively, and a model built that way is a different object from a language model wearing a grammar.

But having established the shape of the difference, we are left with two questions that the mathematics does not answer. The first is practical: *which* real problems actually have this shape, because |A| being small and known is a property of the task rather than something you can impose on an arbitrary one, and it would be useful to have a way of recognizing those tasks on sight. The second is about trust: if the model returns a distribution over A rather than a sentence, we are going to make decisions based on those numbers, and we need to know what the numbers mean before we build anything on top of them. The next section gives us vocabulary for both.

---

## 3\. The two systems, and a third

Two things need naming before we can look at the model itself, and they answer the two questions we just left open. The first is a frame for recognizing which problems belong in this category at all, borrowed from psychology and used here somewhat loosely. The second is the property that decides whether the output can be trusted, which is considerably more technical and which I think is the single most important idea in this article.

### 3.1 System One and System Two

The name comes from Kahneman, who split human cognition into two modes in *Thinking, Fast and Slow*.

![Thinking, Fast and Slow : Kahneman, Daniel: Amazon.in: Books](https://substackcdn.com/image/fetch/$s_!RsJI!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad2523c7-1dc6-4f8e-be2f-71781d5a115a_650x1000.jpeg)

Thinking, Fast and Slow: Kahneman, Daniel: Amazon.in: Books

System 1 is fast, automatic and effortless; it is what recognizes a face, reads a word without deciding to, senses that a room feels tense, or knows a sentence is ungrammatical before you could say why. System 2 is slow, deliberate and expensive; it is what multiplies seventeen by twenty-four, compares two mortgage offers, or follows an argument through four steps to check whether it holds.

The useful part of the distinction is not speed, though, it is **structure**, and this is where the section connects back to what we built in Section 2. System 1 is not a faster System 2 working on the same problem; it is a different operation on a differently shaped problem, a match against an answer space that is already known rather than a search through a space that has to be constructed. Which is exactly the distinction we drew in optimization terms, because searching over V\* for a fluent sequence and selecting from a known A are not the same problem at different speeds, they are different problems. **A System 1 task is one whose feasible set is small, enumerable and fixed in advance.** That is the whole of it, and it is why the two framings are really one framing; Kahneman’s vocabulary describes in cognitive terms what the nested-sets diagram describes in mathematical ones.

![](https://substackcdn.com/image/fetch/$s_!Oecz!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59ea8aa8-fecf-4d43-8e4c-96fbe2098118_1407x729.png)

*The same distinction twice. Kahneman’s vocabulary describes in cognitive terms what the nested-sets diagram describes in mathematical ones.*

Today’s chat models are System 2 machines by design and correctly so. They are built to work through novel problems, construct chains of reasoning, and produce answers nobody enumerated beforehand, with a human reading the output. That is a genuine achievement and the right tool for an enormous number of tasks.

But it is the wrong tool for ticket routing, and now we can say why precisely rather than observing that it feels slow. **Ticket routing is a System 1 problem being solved by a System 2 machine.** The answer space is three teams, known in advance, enumerable; there is nothing to search and nothing to construct, and what is needed is a match against candidates we already hold. Instead we deploy a machine that builds a sentence one token at a time in order to tell us which of the three it picked.

I should flag that the metaphor is marketing as much as it is science. Kahneman’s dual-process account is a description of human cognition still under dispute among psychologists rather than an architectural specification, and nothing about Jev literally implements System 1. What the name usefully captures is the shape of the problem being targeted; bounded, enumerable, pattern-matched, answers known ahead of time. Read as a claim about the task rather than the mechanism, it holds up well.

### 3.2 A hypothesis: System Three

Here is where I want to speculate slightly, because the two-system framing has an obvious hole once you start building with it.

If some of your decisions are System 1 and some are System 2, something has to decide which is which. That dispatcher is not doing either kind of work; it is not pattern-matching an answer and it is not reasoning through a novel problem, it is deciding what kind of problem it is looking at and routing accordingly. Call it **System Three**, and note that this is not quite as invented as it sounds, since Stanovich’s tripartite model of cognition already splits Kahneman’s System 2 into an algorithmic mind that executes and a reflective mind that decides what is worth executing.

![](https://substackcdn.com/image/fetch/$s_!PMJd!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbebeaf16-61fb-496d-825b-c2203ce3f633_1535x822.png)

*The dispatcher nobody names. It is not doing either kind of work; it is deciding which kind of work the request needs, and that judgment is itself bounded and enumerable.*

The reason this matters practically is that every agent harness already has a System Three and nobody calls it that. Something decides whether a user request needs the fast model or the expensive one. Something decides whether a tool call is risky enough to interrupt and ask about. Something decides whether the current answer is good enough to return or needs another loop. Those are all metacognitive decisions, made constantly, and until recently they were made either by hand-written heuristics or by burning a full reasoning-model call to ask.

And the interesting thing, which we will see concretely in the hands-on section, is that a System One model turns out to be a very good System Three. Deciding which model should handle this request is itself a bounded, enumerable, pattern-matched judgment; the answer space is your list of models, the state is the request, and the decision wants to be fast because it sits on the critical path of every single call. So you end up with a System One model whose job is to decide when System Two is needed, which is a slightly recursive arrangement but a sensible one.

I offer this as a frame rather than a claim. TypeSafe does not use the term and nothing in their material depends on it. But I find it clarifies why this category of model is interesting beyond cost; it is not only that some decisions get cheaper, it is that the orchestration of expensive reasoning becomes something you can afford to do well.

### 3.3 Calibration, which is the load-bearing word

Now the property everything rests on, and the one most likely to be skimmed because it sounds like a technicality.

Any classifier can emit a number between zero and one; a softmax guarantees they sum to one and tells you nothing whatsoever about whether they mean anything. **Calibration** is the much stronger property that the numbers correspond to observed frequencies, so that among all the cases where the model says 0.8 it is right about 80% of the time. If it is right 95% of the time the model is underconfident, and if it is right 60% of the time it is overconfident, and in both cases the number is lying to you even though the ranking may be perfectly good.

We went through this properly in the [uncertainty and calibration primer](https://vizuara.substack.com/p/a-primer-on-uncertainty-and-calibration), including why modern networks tend to be badly overconfident and what a reliability diagram actually shows, so I will not rebuild the machinery here.

What I want to add is why it matters *more* in this setting than in the ones we discussed there. In a conventional classifier the probability is usually decoration; you take the argmax and move on, and whether 0.8 really meant 80% rarely changes what the system does. In a decision model the probability is the **control surface**. You are going to write code that acts automatically above 0.9, escalates to a human below 0.6, and calls a reasoning model in between, and every one of those thresholds is meaningless unless the number means what it says. An uncalibrated model with excellent accuracy will route confidently wrong cases straight past your human review, because it was confidently wrong about precisely the cases the threshold existed to catch.

![](https://substackcdn.com/image/fetch/$s_!j-Uh!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8dd0754b-dbc4-4a08-87cd-2e2b9d0f2c2e_1245x878.png)

*A reliability diagram. The shaded area is the distance between what the model claims and what it delivers, and the threshold is where your code stops asking anyone.*

This is also why TypeSafe’s training algorithm is called Reinforcement Learning for *Calibrated* Decisions rather than something about accuracy. The claim is not merely that the answers are good, it is that the uncertainty attached to them is honest, and those are separate properties that can be optimized separately.

One caveat the docs are admirably direct about, and which is easy to misread. Calibration is measured **across groups of predictions**, never within one. A well-calibrated 0.8 tells you that cases like this one are right about eighty percent of the time; it does not tell you that this particular answer is eighty percent correct, because this particular answer is either right or wrong and there is no eighty about it. The distinction sounds pedantic until somebody builds a system that treats a single confidence score as a per-case guarantee, which is exactly the mistake the property invites.

So we now have both pieces. A **System One task** is one whose answer space is small, enumerable and fixed in advance, which is Section 2’s feasible set stated in cognitive rather than mathematical terms. And **calibration** is what makes the returned distribution usable as a control surface rather than decoration, which is what we need if code is going to act on it without a human reading the output first.

Which raises the obvious question, and it is the one the next section is about. If a model is going to serve *every* task of this shape rather than being trained for one of them, what exactly is that model? It cannot be a classifier in the usual sense, because a classifier’s labels are baked in at training time and we have just said the answer space arrives at call time. So what is it?

---

## 4\. A generalized, constrained decision model

### 4.1 The generalized classifier

The answer begins with an observation that is obvious in hindsight and that I had never quite put together until I started reading about this.

Imagine you have trained three models; one that detects spam, one that flags fraudulent transactions, and one that tags named entities in text. These are different tasks in different domains with different label sets, and in the normal course of things they are three codebases, three training runs, three deployments and three sets of eval infrastructure.

Now ask what they actually have in common, because the answer is not what you might first assume. It is not the architecture; one might be a fine-tuned BERT, another gradient-boosted trees over engineered features, another a sequence tagger with a CRF on top. It is not the data either, in the sense of subject matter, since an email and a card transaction and a sentence of news copy share nothing at all.

What they share is the **shape** of the problem. Each takes some context and returns a member of a known, finite set. Spam or not. Fraudulent or not. Person, organization, location, or none of them. The domains differ wildly and the structure is identical, and the thing we have been doing for fifteen years is building a new model for each domain while rebuilding that identical structure every time.

![](https://substackcdn.com/image/fetch/$s_!nw9U!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffce0af1-63b4-4ab8-84ed-56079cabc765_1664x822.png)

*Three unrelated domains, three unrelated architectures, and an identical problem shape underneath all of them.*

Which suggests an inversion. If the structure is what is constant, then instead of fixing the data and varying the model, **fix the model and vary the structure**. One model that understands natural language well enough to make a judgment about anything, into which you inject the answer space at call time rather than at training time. The spam classifier becomes a question with two options, the fraud detector becomes a question with two options and some transaction records as context, the entity tagger becomes a question with four options asked once per span.

![](https://substackcdn.com/image/fetch/$s_!LdLS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F176266d3-945f-49fd-8a53-e622adbe426c_1503x637.png)

*The inversion. Rather than training a model per label set, the label set arrives with the request.*

That is what Jev is, and it is worth saying plainly before we complicate it: **a generalized classifier whose label set you supply at inference time.** Everything else in this section is about why that is harder than it sounds and what you get when it works.

### 4.2 Why not just use an LLM for this?

The obvious objection is that we already have models which understand language well enough to make these judgments, and we have been using them for exactly this. So what is actually wrong?

It helps to think about it in terms of entropy, since that is the language we used in Section 2 and it makes the mismatch precise.

An autoregressive language model places a distribution over sequences, and the entropy of that distribution is enormous. At each step it is choosing among a vocabulary of perhaps a hundred thousand tokens, and over a sequence of length n the space has size |V|ⁿ. The model’s entire job is to concentrate probability onto the vanishingly small fraction of that space which is fluent and relevant, and it is extraordinarily good at this, which is the whole achievement of language modelling.

A decision has an entropy of at most log|A|. For a three-way routing choice that is about 1.6 bits. For a yes-or-no question it is one bit.

*H(decision) ≤ log₂ |A| versus H(sequence) ~ n · log₂ |V|*

So when we use an LLM for a decision, we take a machine built to navigate an astronomically large space and point it at a problem whose answer space has three members. The model does not know the space is small. It is still computing a full distribution over its vocabulary at every step, still spending its capacity on the question of what word plausibly comes next, and the fact that only 1.6 bits of the output actually matter is information available to us and not to it.

There is a second mismatch that is subtler and, I think, more damaging. **The probability of a token is not the probability of a decision.** When a model emits the token “billing” with probability 0.87, that number is the likelihood of that token appearing at that position in text, conditioned on everything before it. It is not the model’s belief that billing is the right team. Those two quantities are correlated, often quite strongly, and they are not the same thing, and nothing in next-token-prediction training ever asks them to be. This is why extracting confidence from an LLM’s logits gives you something that behaves roughly like confidence while failing exactly the calibration test from Section 3.

So the answer to “why not just use an LLM” is that you can, and people do, and it works adequately. But you are paying for an enormous search you do not need, and the uncertainty you get back is a byproduct of a different objective rather than an estimate of what you actually asked.

### 4.3 Where the tokens go

The cost consequence is worth seeing laid out, because it is not uniform across the three parts of an LLM call.

A chat-model request has an input, possibly some reasoning, and an output. The input is usually the largest in raw token count, but it is also the cheapest per token, it is processed in parallel rather than sequentially, and it is frequently cached. Reasoning tokens and output tokens are where the cost and latency actually live, and they are priced accordingly; on current frontier models output tokens cost several times what input tokens do, precisely because each one requires its own forward pass that cannot be batched with the others.

Now look at what happens to that profile when the output is a choice rather than a sentence.

![](https://substackcdn.com/image/fetch/$s_!-BD8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F14c6663f-a4d6-42ba-86a0-fc2166187f0f_1961x1062.png)

*Illustrative rather than measured. The input does not shrink and should not, since the context is what grounds the decision; what collapses is the expensive end.*

The input does not shrink, and should not, because the context is what grounds the decision and you want to give it everything relevant. Reasoning may or may not be present depending on whether the task needs it. But the output collapses from a sentence to a value, and since the output is the expensive end, the economics change shape rather than merely scaling down.

I want to be careful here, because there is a sloppy version of this claim going around that says output cost goes to zero. It does not. A choice still has to be produced, there is still computation behind it, and TypeSafe still charges for tokens. What is true is that the output becomes **insignificant relative to the input**, which is a different and more defensible statement. We will return to this in the Thoughts, because the gap between “free” and “negligible” matters more than it sounds.

### 4.4 What this unlocks, practically

Abstractly, cheap calibrated decisions sound like an infrastructure improvement. Concretely they change what is worth building, and the clearest examples are in the places where volume has always been the obstacle.

Take customer interaction at scale. A sales team with fifty thousand inbound leads cannot afford to have a frontier model read each one and judge intent, fit and urgency, so they use keyword rules and a scoring heuristic that everybody knows is crude and nobody can justify improving because the model calls would cost more than the leads are worth. Drop the per-decision cost by two orders of magnitude and the calculation inverts; now you can ask six questions of every lead, and more importantly you can ask them *again* whenever the context changes rather than scoring once at capture.

The same pattern appears anywhere a judgment currently happens either rarely or crudely because it was too expensive to do properly. Content moderation on every message rather than on a sample. Support ticket triage on arrival rather than after a queue delay. Marketing segmentation recomputed per interaction rather than nightly. Routing every agent request to an appropriately sized model rather than sending everything to the largest one.

![](https://substackcdn.com/image/fetch/$s_!dXC3!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffa3d7271-ba2b-4328-bce4-2f49c8d9f96b_1503x891.png)

*The band in the middle is the article’s practical claim: a set of judgments that were always desirable and never affordable.*

And this is where the naming becomes relevant, because Jev is named after William Stanley Jevons, who observed that making a resource cheaper to use does not reduce consumption of it but increases it. If TypeSafe is right about the cost curve, the interesting consequence is not that your existing classification bill falls by 99%. It is that decisions become cheap enough to put in a hundred places where nobody would currently consider putting one, and the aggregate load goes *up*. That is a claim about the shape of what gets built, not about anyone’s invoice, and I will come back to it at the end.

---

## 5\. The Ideal Case

That said and given our understanding of pre-requisits; imagine if we could specify the model we want, here is what we would ask for.

1. **It reads like a language model.** Messy human text, a ticket with typos, a log excerpt, three transaction records and a paragraph of policy, understood the way a competent colleague would understand it on first reading.
2. **It answers like a function.** I declare the answer space in my own code, and that declaration is a contract; if I say the answer is one of three things, a fourth has nowhere to come from. No parsing, no validation, no retry.
3. **The probability means something.** Not a softmax, not a confidence the model generated because I asked for one. A number I can threshold; when it says 0.9 across a thousand cases, roughly nine hundred are right.
4. **Many questions, one price.** Real decisions decompose into several independent judgments about the same context. Asking five should cost about what asking one costs, because nothing about the second depends on the first.
5. **Latency set by the model, not the answer.** An autoregressive model’s floor is how long the output is. A model evaluating a known set in one pass has a floor set by its own size. The second is low enough to sit inside a request a user is waiting on.
6. **Pay for reading, not for replying.** Charge me properly for the context, which is the whole point, and nominally for an answer carrying two bits. Otherwise the economics steer me towards asking fewer questions than I should.
7. **Grounded in what I gave it.** If the context does not support a conclusion, that should show up in the number rather than being filled in from training. A judgment drawing on knowledge I cannot see is one I cannot audit.

### The tension

Read that list back and there is a contradiction sitting in it.

![](https://substackcdn.com/image/fetch/$s_!2nPY!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F13076344-e419-4376-8483-9c4e64446510_1503x729.png)

*One requirement and six, pulling against each other. Everything in Sections 6 and 7 is about how that gets resolved.*

Point 1 wants deep language understanding, and we know exactly one way to get that: pretrain something enormous on text. Points 2 through 7 want behaviour that pretraining does not give you and in places works against. The thing that understands language is an autoregressive generator, and an autoregressive generator is slow, untyped, and produces token probabilities rather than decision probabilities.

So the specification is for something that is **a language model on the way in and a classifier on the way out**. Not an LLM with a grammar bolted on, which keeps all the sequential cost. Not a classifier with better features, which has its labels welded in and no real understanding of what it reads.

### What we are giving up

**No explanation.** A model returning a value has nowhere to put a reason. When an answer looks wrong you have the context, the question and the number, and nothing else.

**No surprises.** The answer space is fixed before the model runs. If the right answer is not in the set, you get the nearest one with whatever confidence it has, not a warning that the set was wrong.

Neither is fixed by a better model. They are the price of the shape, and the shape is what we came for.

---

## 6\. What is Jev?

### 6.1 The answer to the tension

Section 5 ended on a contradiction: the specification needs a language model on the way in and a classifier on the way out, and those are two different machines.

Jev’s answer, as far as anyone outside TypeSafe can tell, is to keep the first and discard the second half of what usually comes with it. It understands language the way a pretrained model does and it does not generate. You send it a **state**, the context the judgment is about, together with one or more **questions** defined in your code, and it returns typed values with probabilities. No prose, no code, no rationale, nothing to parse.

![](https://substackcdn.com/image/fetch/$s_!uMF-!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F16b73218-26fe-4a7b-954c-b50ee2dbb5dd_1546x683.png)

*Two inputs, one pass, a typed answer. Nothing in the path emits a token.*

The crucial word is **non-autoregressive**. Jev does not emit tokens one at a time conditioned on the last, which is what collapses the latency floor from the length of the answer to the size of the model. That single architectural fact is doing most of the work behind points 2, 5 and 6 on our list.

TypeSafe calls this a System One model and Jev is the first public one. How it is built, they have not said.

### 6.2 Three primitives

The answer space is declared through one of three question types.

![](https://substackcdn.com/image/fetch/$s_!MomH!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdadb9d38-9fbb-4760-b8fb-bf1a14e9e37f_1849x797.png)

*Choice returns a distribution over your options; Score returns a continuous value between ordered levels; Noul returns the probability that a statement is true.*

**Choice** selects one option from a set, returning a probability for every option plus a confidence. Up to 255 members.

**Score** rates the state against ordered levels, and because the levels have a direction the model returns a continuous value between them; 1.4 on a zero-to-two frustration scale rather than a forced bucket.

**Noul** answers yes or no and returns the probability that the statement is true. TypeSafe’s own coinage, and the one you reach for most.

The design philosophy is **decomposition**. Rather than one large question requiring the model to weigh several things at once, you ask several small ones and combine them in code: *was a refund requested*, *does the evidence suggest a duplicate charge*, *does the policy permit it*. Judgment in the model, policy in your repository.

![](https://substackcdn.com/image/fetch/$s_!pfvn!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb50cfd95-774b-49f1-9f3e-09ab9025a52c_1503x682.png)

*The model is asked what it can judge; the rules about what to do with those judgments stay in code you can read and change.*

And because the questions are independent they are evaluated **in parallel in a single pass**, so a fourth question barely moves the latency. That is point 4 satisfied directly.

### 6.3 Where it meets the spec, and where it does not

![](https://substackcdn.com/image/fetch/$s_!pZrF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd3d56664-59ef-408d-a0c8-aa20a8c83af0_1129x666.png)

Three of the seven are vendor claims rather than verified properties, and the third is the one I would most want independent evidence for, since calibration is what the whole control-surface argument rests on.

### 6.4 The numbers, and how to read them

TypeSafe reports 70–500 ms end to end, 40–200× faster than frontier models on this class of query, and headline figures of 193.6× faster and 444.6× cheaper. Context is 64k tokens per request, with state plus the longest question fitting inside 32k.

Treat these as vendor claims. They are comparisons the vendor chose against baselines the vendor selected, on a task shape the vendor defined. That does not make them wrong; it makes them unverified. The independent evaluations in Section 8 are more useful precisely because nobody involved had a stake in the result.

### 6.5 What it is not

**It does not write.** No prose, no code, no explanations. A complement to a generative model, not a replacement.

**It is not a drop-in LLM replacement.** It handles the classification work we currently route to chat models, and nothing else.

**It is hosted and proprietary.** Not fine-tuned on your data, not self-hostable, reachable through one endpoint. A different kind of dependency from a classifier you trained yourself, and worth noticing before cheap decisions make it tempting to put one in a hundred places.

**And the method is undisclosed.** Two years in stealth produced a new architecture, a new sampler and a new training algorithm, none of which has been published. The next section is about what can be inferred anyway.

---

## 7\. Methodology

### 7.1 A problem, and an open-source solution to it

Everything so far has described what Jev does. This section is about how, and it runs into the wall I flagged in the introduction: TypeSafe has published nothing. Two years in stealth, a new architecture, a new sampler and a new training algorithm, all undisclosed.

Fortunately the category did not stay closed for long. **Laya**, from Convai Innovations, is an open-weight System One model released under Apache 2.0 with the same three primitives, the same single-pass evaluation, and the same training approach. It is 421M parameters, runs locally in about a gigabyte, and the weights, export scripts and training configuration are all public.

So for the rest of this section I will describe Laya and treat it as evidence about the category. The two models are not the same and I will be clear about which claims come from where, but the architectural questions, how do you get a language model to answer like a classifier and how do you train a probability to be honest, have public answers now, and those answers are almost certainly close to what TypeSafe is doing.

### 7.2 Architecture: the encoder was always the right tool

The answer to Section 5’s tension turns out to be slightly embarrassing in hindsight, which is that we already had the architecture and stopped using it.

Laya is a **bidirectional encoder** with a decision head on top. The English checkpoint is ModernBERT-large; the multilingual one is mmBERT-based, covering 100+ languages. That is the BERT lineage, not the GPT lineage, and the distinction is exactly what matters here.

An autoregressive decoder reads left to right because it has to; it is predicting the next token and must not see the future. An encoder has no such constraint. Every token attends to every other token in both directions, the whole input is processed at once, and what comes out is a representation of the entire state rather than a prediction about what follows it. For understanding a thing, that is strictly better. For generating text, it is useless.

![](https://substackcdn.com/image/fetch/$s_!-l-2!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbcf70aeb-05a0-411d-bb7d-23a4623e1e96_1545x887.png)

*The same sentence under two attention patterns. The triangle is why generation is sequential; the full square is why a decision is not.*

And it is not only Laya. GLiNER2.5-Decide, an open 340M model from Fastino, uses **DeBERTa-v3-large** as its encoder and exposes the same call-time label sets in a single forward pass. Two independent teams reaching independently for the same architecture family is stronger evidence for the argument above than either one alone. The encoder was the right tool, and the only reason it stopped being obvious is that the field spent five years optimizing for generation.

Which is why the field moved on. Once generation became the goal the decoder won, and encoders became what you reached for when you had a specific classification task and some labelled data.

**But we are not generating.** We want a representation of the state good enough to answer questions about it, and a bidirectional encoder is the right machine for that and always was. The novelty is not the encoder; it is what sits on top.

The decision head takes the encoder’s representation together with the question’s answer space and produces a distribution over the options. One forward pass, no decode loop, and because the questions are independent given the representation, all of them are answered from the same pass. That is where the latency goes: Laya reports 32.8 ms p50 for a routed question against Jev’s 236–276 ms, and both are a different order of magnitude from a chat model’s one to three seconds.

### 7.3 Data: outcomes, not labels

Before the training objective, a word about what it needs to consume, because this is the part nobody discusses and it is harder than it looks.

The encoder pretraining is unremarkable and public. ModernBERT and mmBERT are trained the way encoders have always been trained, on large text corpora with masked-language-modelling objectives, and Laya inherits that lineage rather than inventing anything.

The decision stage is where it gets interesting. **A proper scoring rule needs outcomes, not labels**, and those are different objects.

A labelled dataset says *this ticket belongs to billing*. An outcome dataset says *this ticket was routed to billing, and that turned out to be correct*. The first is an annotator’s judgment; the second is what happened. For training a classifier the distinction barely matters, but for training a calibrated classifier it is the whole thing, because calibration is a claim about frequencies in the world and you can only learn it from the world’s frequencies.

Which creates a sourcing problem. Annotated corpora are abundant and outcome-resolved decision logs are not; they live inside companies, they are domain-specific, and they are rarely collected with this use in mind. How either lab assembled enough of them is unstated. Laya ships three checkpoints, English, multilingual, and one tuned for enterprise decisions like customer-service routing, which at least tells you the shape of what they targeted, and Convai’s evaluation uses a 2,000-decision benchmark of their own construction.

For Jev we know nothing at all. No data description, no mixture, no scale, and no indication of whether the outcomes were collected, simulated, or derived from labels by some procedure they have not described.

I flag this not as a complaint but because it bears on the zero-shot question in 7.8. If calibration is learned from outcome distributions, then how well it transfers to your distribution depends on how much your decisions resemble the ones it was trained on, and neither lab has given you the information to judge that.

### 7.4 Training: what the objective actually asks for

**Start with what ordinary supervised learning asks for.**

Train a classifier the standard way and your objective is cross-entropy against a hard label; the target is 1 for the correct class and 0 for everything else. Read that literally and notice what it is telling the model: *you should have said one hundred percent*. Every training example, without exception, pushes towards maximal certainty, and the only thing restraining it is that it cannot be certain about everything at once.

So the model learns to be right, and it learns that confidence is rewarded. What it never learns is when to be unsure, because nothing in the objective ever asks. There is no example whose label says “this one is genuinely a coin flip, please output 0.5”. The gradient points at 1.0 every time.

That is the root of the overconfidence we documented in the [calibration primer](https://vizuara.substack.com/p/a-primer-on-uncertainty-and-calibration), and it is why the usual remedy is post-hoc, temperature scaling, fitting one parameter on a validation set to squash the probabilities after training is already done. A patch applied to a model optimized for the wrong thing.

**Now the alternative.** A **scoring rule** assigns a reward to a predicted probability given the outcome that occurred. It is **proper** if the model maximizes expected reward by reporting its true belief, and **strictly proper** if that is the unique maximum:

*Brier = (p − y)² Log-loss = − \[ y log p + (1−y) log(1−p) \]*

The difference from cross-entropy is not the formula, log-loss is cross-entropy, it is what you evaluate it against. Supervised training scores you against a hard label on one example. A scoring-rule objective scores you against **observed outcomes across many predictions**, which is the setting where honesty becomes optimal.

**A worked example.** Suppose the model genuinely believes an event has probability 0.7 and is deciding what to report. Over a hundred such cases the event happens about seventy times. Reporting 0.9 costs an expected 0.250, reporting 0.5 also costs 0.250, and reporting the honest 0.7 costs 0.210.

![](https://substackcdn.com/image/fetch/$s_!uPeJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F87fba0e6-21e9-4048-898e-6eec21f03e99_1240x938.png)

*Overclaiming and hedging are both punished. The minimum sits exactly at the model’s true belief and nowhere else.*

In general, the expected penalty for reporting q when the truth is p works out to

*E\[Brier\] = p(1−p) + (p − q)²*

*the first term is irreducible, the second is the penalty for lying*

a parabola in q with its floor at q = p. The first term is the world’s own uncertainty, which no report can remove; the second is what you pay for misrepresenting your belief, in either direction.

So the objective **rewards honesty rather than confidence**. The model cannot improve its score by sounding more certain, which is precisely the lever cross-entropy hands it.

### 7.5 This is a calibration metric used as a loss

Worth naming plainly, because if you have read anything on forecast evaluation you will already have recognized it.

A strictly proper scoring rule is the classical tool for **measuring** calibration, not a new invention. The Brier score has a well-known decomposition:

*Brier = reliability − resolution + uncertainty*

Reliability is exactly the gap in the reliability diagram from 3.3, the distance between what you claimed and what happened. Resolution is how much your predictions vary from the base rate, which is to say whether you are telling anyone anything. Uncertainty is a property of the data you cannot touch.

So the objective is not a novel mechanism. It takes a metric meteorologists have used for sixty years and moves it from the evaluation step to the training step, which is a real contribution but a different kind from the one the name implies.

And the decomposition surfaces a failure mode that matters. **Optimizing calibration alone admits a degenerate solution**: a model that ignores the input entirely and reports the base rate on every example is perfectly calibrated. If 12% of tickets are urgent, answer 0.12 always, and your reliability is flawless. It is also useless, because the resolution term is zero and you have learned nothing about any particular ticket.

A strictly proper rule does punish this, since the resolution term enters with a negative sign and the degenerate model forfeits all of it. But it means calibration and accuracy are both being optimized and they are in tension, and a model can trade some of one for the other. Which is the honest reason requirement three in the 6.3 table reads “claimed” rather than “met”.

### 7.6 RLCD: Reinforcement Learning for Calibrated Decisions

We now have both halves of the idea, so let us put the name to them.

**Reinforcement Learning for Calibrated Decisions** is TypeSafe’s training algorithm and, as far as the open-source work indicates, the same approach Laya uses. Neither lab has published the method, so what follows is the shape of it rather than the details, assembled from what both say about it and from what the mathematics requires.

**The loop.** Write the model as a policy π\_θ that takes a state x and a question with answer space A, and emits a distribution over the options:

*π\_θ( · | x, A ) = ( p₁, p₂, …, p\_|A| ), Σ\_k p\_k = 1*

The world then resolves the question, giving an outcome y ∈ A. A strictly proper scoring rule S turns that resolution into a reward, and the objective is the expectation of it:

*J(θ) = E over (x, A, y) of S( π\_θ( · | x, A ), y )*

![](https://substackcdn.com/image/fetch/$s_!D0zx!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e717fd5-7565-4ab3-99cc-4fb8458ced1d_1584x729.png)

*A policy, an environment, a reward and an update. What is unusual is that the action is a probability and the reward is a scoring rule.*

That is reinforcement learning in a fairly literal sense; a policy produces an output, the environment returns a reward, parameters move to increase it. What is unusual is that the action is a probability rather than a token or a move, and the reward is a scoring rule rather than a preference or a check.

**Why it has to be RL rather than supervised fitting.**

This is the part worth slowing down on, because at first glance you could imagine skipping the machinery; just collect outcomes, turn them into soft labels, and do ordinary supervised learning. It does not work, and the reason is instructive.

*Imagine you are training a weather forecaster.* On Tuesday she says there is a 70% chance of rain. It rains. Was she right?

You cannot answer that. Not “you do not have enough information yet”, the question genuinely has no answer from one day. A 70% forecast is not falsified by rain and not confirmed by it either, because the forecast was never a claim about Tuesday. It was a claim about *the class of days that look like Tuesday*, and the only way to check it is to collect every day she said 70% and count how many were wet.

So there is no per-example target. The supervised framing wants to write a loss against some target t(x), and the target does not exist. All you observe is y ∈ {0, 1}, and regressing probabilities onto hard outcomes is exactly the cross-entropy setup from 7.4 that drives everything towards 1.0.

The property we actually want is a statement about a group:

*E\[ y | p\_θ(x) = q \] = q for every q in \[0, 1\]*

Read it carefully: among all the inputs on which the model says q, the outcome rate should be q. That is a constraint on the distribution of predictions the model produces, not on any individual prediction, and **it depends on the policy’s own behaviour**. Change the model and you change which inputs land in the q bucket, which changes what the constraint is evaluated over.

There is a Bayesian way to see the same thing, and it makes the “one example tells you nothing” point concrete. Suppose you want to check whether the forecaster’s 70% claim is honest. Put a prior on the true rain-rate among 70%-days, say a Beta, and update it with each resolved day:

*θ ~ Beta(α, β), θ | data ~ Beta( α + r, β + (n − r) )*

where r is how many of those n days were wet. The posterior mean is (α + r) / (α + β + n), and the spread shrinks like 1/√n.

![](https://substackcdn.com/image/fetch/$s_!UiOV!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F419f95e3-daa2-401f-85a1-f41f905a334b_1114x836.png)

*After one day the posterior is still almost the prior. The evidence about a probability accumulates across cases and cannot be extracted from one.*

After one rainy day the posterior has barely moved; it is consistent with the true rate being anywhere from 0.3 to 0.95. After a few hundred days it has collapsed onto a narrow interval, and now you can say whether 0.7 was honest. And notice that this is what the model is implicitly being asked to do. A calibrated predictor is one whose outputs would survive exactly this test, bucket by bucket, which is why the training signal has to be evaluated over a population of its own predictions rather than per example.

That is precisely the structure reinforcement learning exists to handle: an objective defined over the distribution your policy induces rather than over fixed targets per input. You cannot get here by relabelling your training set, because the thing you would need to label is a property the model has not yet exhibited.

*Another way to see it.* Supervised learning asks “what is the answer to this?” and marks you against a key. RLCD asks “how often are you right when you talk like that?” and marks you against your own track record. The second question is incoherent for one example and perfectly well-posed for ten thousand.

**What the three letters are doing.** Reinforcement, because the signal comes from consequences rather than a supplied answer. Calibrated, because the reward is chosen to make honesty optimal rather than accuracy. Decisions, because the action is a typed choice over a known answer space rather than free-form output.

**And the thing to keep hold of.** Everything in 7.4 and 7.5 was reward design, not algorithm. RLCD’s contribution is the choice of what to reward, and that choice is a scoring rule from the 1950s. The RL wrapper is how you optimize something defined over a distribution of predictions; the proper scoring rule is why what you converge to is honest. Two separable ideas, and the second is doing the work.

### 7.7 RLCD against RLHF and RLVR

With RLCD described, it is worth placing it against the two reinforcement-learning approaches you will already know. All three are distinguished by where the reward comes from.

**RLHF** gets its signal from human preference. A person compares two outputs, a reward model learns to imitate that judgment, and the policy optimizes against the reward model. It works for things only a human can assess, tone, helpfulness, whether an answer is actually useful, and it inherits the annotators’ biases plus the reward model’s willingness to be gamed.

**RLVR** gets its signal from verification. The answer is checked mechanically; the test passes, the proof checks, the arithmetic is right. Far more reliable than a reward model, and confined to domains where correctness is machine-checkable. We looked at this family in [SRL](https://vizuara.substack.com/p/srl-supervised-reinforcement-learning) and at reward during pretraining in [RPT](https://vizuara.substack.com/p/rpt-reinforcement-learning-during).

**RLCD** gets its signal from outcomes, scored by a proper rule. Not whether a human liked the answer or whether a checker accepted it, but how well the stated probability matched what actually happened, across many predictions.

![](https://substackcdn.com/image/fetch/$s_!2sQU!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec36a2ae-26ea-44d2-bc44-53b64f5f31a2_1784x753.png)

*What each family can be asked to optimize, and what it costs you to ask.*

The clarifying question is what each can ask for. RLHF can optimize for qualities nobody can define formally. RLVR can optimize for correctness where correctness is decidable. **RLCD can optimize for honest uncertainty**, which neither of the others can express, because neither has a notion of a well-calibrated answer, only of a good one and a right one.

---

## 8\. Hands-on with first-order system

Which is where the theory runs out. We have the architecture, the objective, and the training loop. What none of it tells you is whether the thing is pleasant to use, and a decision model is not something you chat with and evaluate by reading; it is something your code calls a hundred times a second.

A note on how this section changed while I was writing it. I started out writing against Jev’s SDK and found myself guessing at method names, because the hosted client is thinly documented and I could not run the thing I was describing. Then, looking for something I could actually execute, I found **GLiNER2.5-Decide**, a 340M open model from Fastino, Apache 2.0, that does the same job locally. It also, on its own benchmark, beats both of the models this article has been about.

### 8.1 State, and how little of it there is

Let us see what state is in the open models variant (it is simpler than Jev’s version): just the text.

```markup
text = “”“From: compliance@group.example
Subject: Protocol update — action required today
Please confirm the new retention rule is applied before Friday’s audit.”“”
```

Jev additionally accepts JSON objects and arrays, which genuinely matters when your decision depends on structured records alongside prose; the crash-narrative study and the refund example both need that. GLiNER2.5-Decide takes a string, so structure has to be serialized by you. A real difference, and a point in the hosted model’s favour.

The questions are where both converge.

### 8.2 The smallest possible call

```markup
# pip install gliner2
from gliner2 import AutoExtractor

model = AutoExtractor.from_pretrained("fastino/GLiNER2.5-Decide")

model.classify_text(
    “Your mailbox is almost full. Click here in the next hour “
    “or we will delete every message.”,
    {”label”: [”spam”, “ham”]},
)
{”label”: “spam”}
```

Four lines, no API key, no network call after the weights are cached, and roughly a gigabyte of model sitting in memory. Three things worth noticing.

**The label set is the second argument.** Not a prompt, not a schema file, not a fine-tuning run; a Python dict, at call time. That is Section 4’s inversion in its most literal form, since the same loaded model answers a spam question now and a routing question on the next line.

**There is no prompt anywhere.** No instructions, no template, no “you are a helpful classifier”. The model was trained to take a label set directly, so the only English in the call is the labels themselves.

**The output is the decision.** A dict your code reads. No parsing, no retry, no JSON mode.

### 8.3 Several decisions at once

The decomposition argument from 6.2, made concrete. One text, three heads, one forward pass:

```markup
model.classify_text(
    text,
    {
        “intent”:  [”fyi”, “request”, “approval”, “complaint”,
                    “newsletter”, “security_alert”],
        “urgency”: [”low”, “normal”, “high”, “critical”],
        “route”:   [”support”, “billing”, “legal”, “security”,
                    “finance”, “archive”],
    },
)
{”intent”: “request”, “urgency”: “high”, “route”: “legal”}
```

Three questions, one pass over the encoder. This is the parallel-evaluation property from 6.2 arriving as something you can time yourself; add a fourth head and the latency barely moves, because the expensive part was reading the text and that happened once.

And it is the same design discipline. Three small factual judgments, combined by your code, rather than one large question that buries the policy inside the model.

### 8.4 Confidence, which you have to ask for

Here is the parameter the model card does not mention and which the whole of 3.3 depends on:

```markup
model.classify_text(
    text,
    {”route”: [”support”, “billing”, “legal”, “security”, “finance”, “archive”]},
    include_confidence=True,
)
```

It defaults to False, so by default you get a bare label and no probability, which is exactly the thing Section 5’s requirement three said not to accept. Turn it on and you have a number to threshold:

```markup
r = model.classify_text(text, {”route”: [...]}, include_confidence=True)
if r[”route”][”confidence”] > 0.90:
    assign(r[”route”][”label”])               # act alone
elif r[”route”][”confidence”] > 0.60:
    assign(r[”route”][”label”], review=True)  # act, but watch
else:
    escalate_to_reasoning_model()             # ask something expensive
```

![](https://substackcdn.com/image/fetch/$s_!NkIr!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5fa29680-215d-4e3a-ac43-bb1963de4583_1198x729.png)

*The three-tier pattern from 3.3, now with a parameter that actually returns the number it depends on.*

I should flag that I verified include\_confidence in the package source but could not run the model to see the exact response shape, so treat the accessor above as the shape to check rather than the shape to trust. The parameter is real; the key names may differ.

And the Section 9 caveat applies with full force here. A confidence you have not validated on your own data is a number, not a threshold; measure the reliability before you branch on it.

### 8.5 Multi-label, thresholds, and ordinal scales

Three variations that cover most of what you will actually need.

**Multi-label**, when several answers apply at once:

```markup
model.classify_text(
    “Battery dies before lunch, but the keyboard and the screen “
    “are the best I have used.”,
    {”aspects”: {
        “labels”: [”battery”, “keyboard”, “screen”, “camera”, “price”, “support”],
        “multi_label”: True,
        “cls_threshold”: 0.4,
    }},
)
# {”aspects”: [”battery”, “keyboard”, “screen”]}
```

**Ordinal scales**, which are Jev’s Score primitive done the cheap way; pass the levels as ordinary strings:

```markup
model.classify_text(
    “Payroll file has to be corrected before the 5pm cutoff “
    “or the whole company is paid late.”,
    {”urgency”: [”0”, “1”, “2”, “3”, “4”, “5”]},
)

# {”urgency”: “5”}
```

Worth being precise about the difference. Jev’s Score understands the levels as ordered and returns a continuous value between them, 1.4 on a zero-to-two scale. This returns the nearest level as a string. For most SLA systems that is fine; if you need the interpolation, it is a real gap.

**Labels with descriptions**, for when the name alone is ambiguous:

```markup
model.classify_text(
    “Please reset the card PIN. The new one never arrived “
    “and the old one is locked.”,
    {”intent”: {”labels”: {
        “card_pin_change”: “The customer wants a new PIN or the current PIN replaced”,
        “card_lost”:       “The physical card is missing”,
        “balance_inquiry”: “The customer wants the current balance”,
    }}},
)
```

This is where the prompt quietly comes back. A description is a short instruction, and writing good ones is the same skill as writing good instruction strings for a Noul. The typed interface removes the parsing problem completely; it does not remove the specification problem.

### 8.6 A yes/no question over a passage

The closest thing to Jev’s Noul, and the primitive you reach for most:

```markup
model.classify_text(
    “The treaty was signed in Paris in 1992. It entered into force “
    “the following year, after the last signatory ratified it.”,
    {”answer”: {
        “labels”: [”yes”, “no”],
        “prompt”: “Did the treaty enter into force in 1992?”,
    }},
)
# {”answer”: “no”}
```

The text is the state, the prompt is the question, and the answer is one bit. No chain of thought, no extracted sentence, no explanation. This is the grounding-check shape, is this claim supported by this passage, which is one of the most common things people currently burn a chat-model call on.

### 8.7 All together

The refund case from 6.2, end to end, running locally (no API key required).

```markup
# pip install gliner2

from gliner2 import AutoExtractor

model = AutoExtractor.from_pretrained("fastino/GLiNER2.5-Decide")

def handle_ticket(message: str, transactions: list, policy: str) -> str: 

    # ---- 1. the state is a string, so serialize the structure yourself ----
    lines = [f"- {t['id']}: {t['amount']} on {t['ts']}" for t in transactions]
    state = (
        f"{message}\n\n"
        f"Recent transactions:\n" + "\n".join(lines) + "\n\n"
        f"Policy: {policy}"
    )

    # ---- 2. several independent judgments in one forward pass ------------
    r = model.classify_text(
        state,
        {
            "intent":      ["refund_request", "order_status", "cancel_subscription",
                            "login_problem", "bug_report", "speak_to_human", "other"],
            "duplicate":   ["yes", "no"],
            "urgency":     ["0", "1", "2", "3", "4", "5"],
            "needs_human": ["yes", "no"],
            "queue":       ["billing", "technical", "account"],
        },
        include_confidence=True,
    )

    # ---- 3. every business rule lives here, none of it in the model ------
    asked     = r["intent"]["label"] == "refund_request"
    duplicate = r["duplicate"]["label"] == "yes"
    urgency   = int(r["urgency"]["label"])
    queue     = r["queue"]

    if asked and duplicate and queue["confidence"] > 0.80:
      return {"action": "approve_refund"}
    elif urgency >= 4 or r["needs_human"]["label"] == "yes":
      return {"action": "escalate", "priority": "high"}
    else:
      return {"action": "queue_for_review", "suggested": queue["label"]}

    # ---- 4. log probabilities so you can audit calibration later ---------
    log_decision(outcome=outcome, raw=r)
    return outcome

if __name__ == "__main__":
    result = handle_ticket(
        message="I was charged twice for the same order and nobody has replied "
                "in three days. Please refund the duplicate.",
        transactions=[
            {"id": "tx_8821", "amount": "49.00", "ts": "2026-09-14T10:02Z"},
            {"id": "tx_8822", "amount": "49.00", "ts": "2026-09-14T10:03Z"},
        ],
        policy="Duplicate charges within 24h are refundable without review.",
    )
    print(result)
    # output : {'action': 'queue_for_review', 'suggested': 'billing'}
```

Four things this file demonstrates, and they are the same four regardless of which model sits behind it.

**Step one is where the open model costs you something.** The transactions have to be flattened into prose because the state is a string, and that flattening is a parsing problem you created. Jev’s JSON state avoids it. This is the clearest practical argument for the hosted model.

**Step two is one forward pass.** Five heads, one read of the text. Writing it as five calls would be five times slower for nothing.

**Step three contains every business rule in the system**, and none of them are in the model. Thresholds, the precedence of escalation over approval, the decision to treat low routing confidence as grounds for review; all readable, testable, and changeable by someone who has never heard of GLiNER.

**Step four is the one people skip.** Logging the probabilities alongside what actually happened is what lets you build the reliability diagram from 3.3 three months from now, and Section 9 will show that you will need it.

### 8.8 What using it actually feels like

Three observations from writing the above.

**Running locally changes the calculus more than I expected.** No API key, no rate limit, no per-call cost, no network hop. The Section 4 argument about cheap decisions unlocking new volume is one thing when a decision costs $0.000004 and another thing entirely when it costs nothing and runs on the machine already doing the work.

**The decomposition discipline is the hard part**, and it is a skill rather than a syntax. The temptation is to ask one big question, something like a single “decision” head with approve, deny and escalate as its labels, and the interface will happily let you. That puts the policy back inside the model and you lose the thing you came for.

**And the label names are doing more work than they look like they are.** refund\_request versus wants\_money\_back is a prompt-engineering decision wearing a very small hat. The model reads those strings. You are still choosing words carefully, just fewer of them.

---

## 9\. Results

### 9.1 Independent evaluation exists, which is unusual this fast

Two months after release there are at least six third-party evaluations of Jev on arXiv, which is more scrutiny than most closed models get in a year. Since the vendor’s figures are unverifiable, these are what this section rests on.

The broadest is a benchmark study from Bonn covering **37 datasets and 346,009 requests**, run zero-shot on full evaluation splits with one frozen template per dataset, for **under US$10** in total, which is itself a data point about the cost claim.

**Where it is strong.** Binary sentiment at 96.5% on IMDB and 96.4% on SST-2, language identification at 99.6%, commonsense at 95.5% on HellaSwag, science questions at 98.8% on ARC, and 86.7% on Belebele across 122 languages. Intent routing reaches 89.5% on CLINC150 with 151 options in a single Choice.

**Against open-weight models** scored on identical requests through their exact option probabilities, Jev beats Qwen3.8-27B on 27 of 37 datasets and Gemma-4-E4B on all 37. Worth noting what that comparison is: a hosted commercial model against a 27.8B and an 8B open model, and the margins are real but not enormous.

There is a third data point, and it is awkward for both models this article has been about. **GLiNER2.5-Decide**, an open 340M encoder, reports **60.2%** exact-match accuracy on Fastino’s fast-decisions benchmark, 17 domains with 300 held-out examples each and the same text and candidate labels for every model, against **57.6% for JevK5** and 46.6% for Laya Router. A 340M model beating a hosted commercial one on a public benchmark is a real result, with the usual caveat that the benchmark belongs to the people who won it. Still, the direction is consistent with the Bonn study’s finding that Jev’s advantage over well-used open models is in interface and consistency rather than raw accuracy.

**Where it fails.** Emotion at 58.5% on noisy hashtag-derived labels, SST-5 five-way sentiment at 57.9%, GoEmotions macro-F₁ of 0.243, and worst of all AGB-DE at F₁ 0.204, deciding whether a German consumer-terms clause is void under German law, which the authors rightly describe as requiring domain knowledge rather than a snap judgment. Prompt-injection detection has perfect precision and 50% recall.

![](https://substackcdn.com/image/fetch/$s_!-fSu!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa1ecd75-f492-4e55-8e3a-a812a0281e98_1784x1030.png)

*Thirty-one of the 37 datasets, sorted. The right-hand tail is where a snap judgment is the wrong tool.*

### 9.2 The calibration picture is more complicated than the marketing

Here is the finding that matters most, and it cuts both ways.

**Pooled, the calibration is genuinely good.** Across 22 Choice datasets and 279,925 answers, expected calibration error is 0.028. Averaged per dataset, Jev’s ECE of 0.074 is level with Qwen’s 0.075 and far better than Gemma’s 0.184.

**Per dataset, it ranges by two orders of magnitude.** From 0.003 on Language ID and 0.005 on ARC, up to 0.279 on Emotion, 0.264 on AGB-DE and 0.236 on Prompt Injections. The aggregate number is an average over a spread that wide, and your task sits somewhere in it without you knowing where.

![](https://substackcdn.com/image/fetch/$s_!DrEE!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe6ee7ec-101d-43aa-bfeb-517e2f0f763d_1632x1002.png)

*Every bar is the same model under the same evaluation harness. The dashed line is the number that gets quoted.*

**And Noul is weaker than Choice.** Binary probabilities rank well but sit badly relative to a fixed 0.5 threshold; tuning the threshold on training data raises micro-F₁ on UNFAIR-ToS from 0.50 to 0.75. The same pattern appears in moderation: AUROC 0.989 on ToxicChat toxicity and 0.982 on prompt injection, with mediocre decisions at 0.5. The model knows which cases are more likely true; it does not know where to put the line.

### 9.3 Three domain studies agree

**Crash narratives.** A 27-question schema over 499,500 Texas police narratives, 195,857 coded by jev-1.13.0 at 3,673 mean input tokens and 0.20 s median latency. Against 2,416 blinded human judgments: F₁ 0.908, with precision 0.902 and recall 0.915. One frontier model gains 0.059; the other is statistically indistinguishable. Raw probabilities overstate prevalence; recalibrated on those judgments, out-of-fold calibration error falls to 0.0069 with slope 0.97. The authors’ conclusion is that calibration varies by model rather than by paradigm, so each model must be audited.

**Radiology.** Jev judging factual agreement between generated and physician-written reports. Raw ECE 0.1235, Brier 0.1269, AUROC 0.8858. After isotonic calibration on a held-out half, ECE falls to 0.0077, a sixteen-fold improvement. On controlled errors it reaches AUROC 0.977 for detecting a reversed finding. The recommendation is explicit: recalibrate per task before thresholding.

**Medicine.** The least flattering, and preliminary. ECE from 0.063 on MetaMedQA to 0.141 on PubMedQA. At a 0.9 threshold, accuracy is 75.9% at 17.3% coverage, meaning roughly one in four of its most confident answers was wrong.

A human-activity-recognition study adds the blunt version: fast and inexpensive to query, but its probabilities are not reliably calibrated for recognition.

### 9.4 The pattern

Six studies, one consistent finding. **Calibration out of the box is decent on average and unreliable per task, and post-hoc recalibration fixes it dramatically.** Every study that tried it reports a large gain from modest labelled data.

![](https://substackcdn.com/image/fetch/$s_!rizC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdb3d2e61-467f-4c2f-ae9e-e1193b1701ee_1138x799.png)

*A few thousand resolved outcomes from your own distribution, and an isotonic fit, closes most of the gap.*

Practitioners report the same from the other direction; [this walkthrough](https://www.youtube.com/watch?v=_yD790y_gq4) makes the point that the outputs are not always calibrated and a confidently wrong answer is entirely possible. The marketing line that the model “never hallucinates” is true only in the narrow sense that it cannot emit a category you did not define. A wrong answer at 0.95 confidence is the same problem wearing a type signature.

Which lands awkwardly against Section 7. The argument for RLCD was that calibration should be trained in rather than patched on, that temperature scaling is a remedy for a model optimized for the wrong objective. The empirical finding is that you should fit an isotonic map on your own data before trusting a threshold. That does not make RLCD pointless, since starting at 0.1235 beats starting at 0.4, but it qualifies the claim considerably. **Calibration is a property of a model on a distribution, and you are not running it on the distribution it was trained for.**

### 9.5 The caveat the benchmarks hide

Now the thing most coverage skipped, and the most important practical fact here.

Laya’s shipped checkpoints work zero-shot, and on Convai’s own 2,000-decision benchmark they score **0.362**. Fine-tuned on the target domain, the same model scores **0.766**. Roughly double.

Read that against Section 4’s framing. The promise was one model serving every label set without retraining; the measurement says that out of the box, on a broad benchmark, the open model is mediocre, and most of its headline accuracy comes from domain adaptation. Which is a classifier with extra steps.

Two things soften it. The number is Laya’s, not Jev’s, and Jev is considerably larger and hosted, so its zero-shot gap may be much smaller, though TypeSafe explicitly does not fine-tune on customer data, which means whatever zero-shot performance you get is what you have, permanently. And a single aggregate over 2,000 heterogeneous decisions says little about any particular task; a three-way routing problem with well-separated options is not a fine-grained multilingual rubric.

It also connects straight back to 7.3 in the methodology. If calibration is learned from outcome distributions, zero-shot transfer is a question about how much your decisions resemble the training ones, and nobody has published enough for you to answer that in advance.

The honest summary: **the category’s zero-shot generality is the least-evidenced of its claims**, and it is the first thing I would test on my own data rather than take on trust.

### 9.6 What we still do not know about Jev

Laya tells us what the category looks like. It does not tell us what TypeSafe built.

Unknown: the architecture beyond non-autoregressive, the model size, the training data, the sampler they describe as novel, the specifics of their RLCD implementation, and any reliability data for the calibration claim. The 193.6× and 444.6× figures are vendor comparisons against vendor-chosen baselines.

What we can say is that an open 421M encoder reaches roughly 33 ms with competitive calibration using published techniques, which makes TypeSafe’s claims plausible in kind if not in magnitude. That is weaker than reading their paper, and considerably better than what we had two months ago.

---

## 10\. Thoughts

**1\. Jevons was the right name, and more right than intended.**

Jevons observed that making a resource cheaper increases total consumption. If a decision costs 400× less, the consequence is not that your bill falls 99.75%, it is that you start making decisions where nobody currently makes one. The benchmark study is the proof: 346,009 decisions for under ten dollars.

Which is fine until the second-order version. A system making a million calibrated judgments a minute is one whose behaviour is set by a million small thresholds that nobody reviewed individually. The cost curve is the easy part; the governance of a hundred thousand confidence thresholds is the part nobody has thought about.

**2\. The speedup numbers are measured against the most expensive possible baseline.**

“40–200× faster” and “193.6× faster” are comparisons against frontier models, the Opus 5.5 and GPT-5.6 class, large models with reasoning paths behind a hosted API. Of course a 400 ms typed decision beats a multi-second reasoning call by two orders of magnitude; that baseline was never the right tool.

![](https://substackcdn.com/image/fetch/$s_!hd1o!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff76a69dd-d5a3-4541-9eef-4915d3a0aa75_1687x835.png)

*Approximate, and the point is the ratio rather than any one number. Against the right baseline the gap is real but ordinary.*

Compare against what a sensible engineer would actually reach for, GPT-OSS, or Qwen or Gemma at a few billion parameters doing constrained decoding on a short classification, and the gap compresses to roughly 2–3×. The Bonn study is instructive here: it scores Qwen3.8-27B and Gemma-4-E4B on identical requests via a single forward pass over option tokens, which is the right way to use an LLM for this, and Jev’s advantage is in accuracy and interface rather than orders of magnitude of latency.

The sharpest version comes from the open side. Laya is a 421M encoder running locally at 32.8 ms, against Jev’s 236–276 ms. **The open model is 7.8× faster than the thing whose headline figure is 193.6×**, which tells you most of that number was about the baseline rather than the method.

The architecture argument still holds; non-autoregressive single-pass evaluation genuinely removes the sequential floor. It is the magnitude that is a marketing artifact.

**3\. Output tokens are priced at zero, which is not the same as costing nothing.**

TypeSafe charges US$0.042 per million input tokens and nothing for output. So in billing terms the output genuinely is free.

But that is a pricing decision rather than a statement about physics. Producing the answer still costs compute; it is bundled into the input price, which TypeSafe can afford to do precisely because the output is two bits rather than a paragraph. And if reasoning is involved it is charged normally, so “free output” describes the choice, not the deliberation that might precede it.

The interesting consequence is the incentive it creates. With input dominant and output free, the economics push you to send **more context**, which is the opposite of the instinct everyone developed optimizing chat prompts. The crash-narrative study runs 3,673 input tokens per decision without comment.

**4\. Grounding reduces hallucination and relocates the failure.**

The model cannot invent a category outside your answer space, which removes a whole class of failure. That is real.

But it does not remove being wrong, it concentrates it. One in four of the medicine benchmark’s most confident answers was incorrect; the model was not hallucinating, it was selecting the wrong option from a valid set with high confidence. And a bare value with no rationale leaves nothing to inspect. A chat model that reasons its way to a wrong answer at least leaves a trail.

So the choice becomes a **single point of failure** in a way prose is not. The mitigation is the decomposition discipline from 8.6, several small questions whose answers can disagree, rather than one large one that cannot.

**5\. Is this a step toward AGI?**

No, and the framing is wrong in an interesting way. This is not a weaker general intelligence, it is a parallel branch on a simpler assumption: that most decisions do not require general intelligence. Routing a ticket needs no world model.

Where it touches the deeper argument is on representations. LeCun’s position, which we went through in the [LeJEPA article](https://vizuara.substack.com/p/lejepa-provable-and-scalable-self), is that intelligence is largely about representations good enough to support prediction, and a System One model is precisely a bet that a good representation plus a bounded answer space is all most tasks need.

**6\. The thing I would actually watch.**

Not speed, which will be matched. Not cost, which will fall. Whether **calibrated uncertainty becomes a standard thing to expect from a model**.

We have spent three years building on outputs whose confidence means nothing, compensating with evals and guardrails and human review. If the number becomes trustworthy enough to branch on, that changes what software can safely delegate far more than another order of magnitude on latency would.

The evidence says we are partway: calibrated on average, unreliable per task, fixable with modest labelled data. A real capability with a real caveat.

---

## 11\. Conclusion

We talked about Jev, and specifically about the gap it is trying to close; most of what we use AI for in production is a judgment rather than a piece of writing, and we have been making those judgments with a text generator because that is what was available.

The route out was noticing that this is not a rough edge but a category error. A sentence encoding a decision is mostly grammar, so you pay forty sequential forward passes for two bits; constrained decoding narrows the search space without touching the computation; and the probability you get back is the likelihood of a token appearing at a position, which is not the model’s belief about the answer and was never trained to be.

That turned the question from how do we parse the output into what shape should a decision model be, and the answer has a contradiction in it. It has to read like a language model and answer like a function, and the thing that reads like a language model is an autoregressive generator, which is slow, untyped, and gives you token probabilities. The resolution is slightly embarrassing in hindsight: we already had the architecture. A bidirectional encoder was always the right machine for understanding a fixed input, and we stopped reaching for it when generation became the goal.

Calibration was the harder half. Cross-entropy against hard labels tells a model it should have said one hundred percent, every time, which is why modern networks are confidently wrong. A strictly proper scoring rule asks a different question, how often are you right when you talk like that, and has a unique optimum at the model’s honest belief. That is a metric from the 1950s moved from the evaluation step to the training step, wrapped in reinforcement learning because calibration is a property of a distribution of predictions rather than of any single one.

The empirical case is more mixed than the marketing. Thirty-seven datasets, 346,009 decisions for under ten dollars, beating a 27B open model on most of them. Speed real but smaller than advertised, since 193.6× was measured against a frontier model and an open 421M encoder runs 7.8× faster than Jev itself. And calibration pooled at 0.028 while ranging from 0.003 to 0.279 across tasks, which is decent on average and unreliable where it matters.

What strikes me most is how little here is new. The encoder is BERT’s architecture, the Brier score is from 1950, proper scoring rules have been the standard tool for evaluating forecasts for sixty years. The contribution is noticing that a decision is not a short piece of text, and everything else follows from taking that seriously.

Whether Jev specifically becomes standard I have no idea. The durable part is the claim underneath it: that a model can tell you how much to trust it, in a number you can act on. We have spent three years building on outputs whose confidence means nothing, and if that changes, it changes what software can safely delegate more than any amount of latency ever would.

This marks the end of our walk through System One models, and with this we conclude.

**References:**

TypeSafe docs: https://docs.typesafe.ai

Laya, open weights: [https://huggingface.co/convaiinnovations/laya](https://huggingface.co/convaiinnovations/laya)

Benchmark study: [https://arxiv.org/abs/2609.37647](https://arxiv.org/abs/2609.37647)

Crash narratives at scale: [https://arxiv.org/abs/2609.24052](https://arxiv.org/abs/2609.24052)

Radiology factuality: [https://arxiv.org/abs/2609.27607](https://arxiv.org/abs/2609.27607)

That’s all for today. Follow me on LinkedIn and Substack for more such posts, till then happy Learning. Bye 👋