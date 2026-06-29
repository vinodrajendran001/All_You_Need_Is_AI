---
title: "Nested Learning: The Illusion of Deep Learning Architecture"
source: "https://vizuara.substack.com/p/nested-learning-the-illusion-of-deep?publication_id=3466476&post_id=202300851&isFreemail=true&r=6dm571&triedRedirect=true"
author:
  - "[[Siddhant Rai]]"
published: 2026-06-29
created: 2026-06-29
description: "Rethinking how Memory and architeucture are constructed and coupled together for inference-time learning"
tags:
  - "clippings"
---
## Table of contents

1. *[Introduction](https://vizuara.substack.com/p/23c397ae-b774-4c2e-b0ef-a280e030d5c9?updated=2026-06-27T12%3A24%3A02.359Z&postPreview=free&sub=free&device=desktop&audience=everyone&free_preview=false&freemail=true#%C2%A71-introduction)*
2. *[How Do Models Learn Beyond Training?](https://vizuara.substack.com/p/23c397ae-b774-4c2e-b0ef-a280e030d5c9?updated=2026-06-27T12%3A24%3A02.359Z&postPreview=free&sub=free&device=desktop&audience=everyone&free_preview=false&freemail=true#%C2%A72-how-do-models-learn-beyond-training)*
3. *[Why RAG Isn’t Enough](https://vizuara.substack.com/p/23c397ae-b774-4c2e-b0ef-a280e030d5c9?updated=2026-06-27T12%3A24%3A02.359Z&postPreview=free&sub=free&device=desktop&audience=everyone&free_preview=false&freemail=true#%C2%A73-why-rag-isnt-enough)*
4. *[Why Memory is Hard](https://vizuara.substack.com/p/23c397ae-b774-4c2e-b0ef-a280e030d5c9?updated=2026-06-27T12%3A24%3A02.359Z&postPreview=free&sub=free&device=desktop&audience=everyone&free_preview=false&freemail=true#%C2%A74-why-memory-is-hard)*
5. *T [he Ideal Case](https://vizuara.substack.com/p/23c397ae-b774-4c2e-b0ef-a280e030d5c9?updated=2026-06-27T12%3A24%3A02.359Z&postPreview=free&sub=free&device=desktop&audience=everyone&free_preview=false&freemail=true#%C2%A75-the-ideal-case)*
6. *[Quick Recap of Titans Architecture](https://vizuara.substack.com/p/23c397ae-b774-4c2e-b0ef-a280e030d5c9?updated=2026-06-27T12%3A24%3A02.359Z&postPreview=free&sub=free&device=desktop&audience=everyone&free_preview=false&freemail=true#%C2%A76-quick-recap-of-titans-architecture)*
7. *[Methodolog](https://vizuara.substack.com/p/23c397ae-b774-4c2e-b0ef-a280e030d5c9?updated=2026-06-27T12%3A24%3A02.359Z&postPreview=free&sub=free&device=desktop&audience=everyone&free_preview=false&freemail=true#%C2%A77-methodology) y*
	1. *[The Neural Learning Module and the Nested Learning Paradigm](https://vizuara.substack.com/p/23c397ae-b774-4c2e-b0ef-a280e030d5c9?updated=2026-06-27T12%3A24%3A02.359Z&postPreview=free&sub=free&device=desktop&audience=everyone&free_preview=false&freemail=true#%C2%A771-the-neural-learning-module-and-the-nested-learning-paradigm)*
		2. *[Continuum Memory System (CMS)](https://vizuara.substack.com/p/23c397ae-b774-4c2e-b0ef-a280e030d5c9?updated=2026-06-27T12%3A24%3A02.359Z&postPreview=free&sub=free&device=desktop&audience=everyone&free_preview=false&freemail=true#%C2%A772-continuum-memory-system-cms)*
		3. *[Self-Modifying Titans and the Hope Architecture](https://vizuara.substack.com/p/23c397ae-b774-4c2e-b0ef-a280e030d5c9?updated=2026-06-27T12%3A24%3A02.359Z&postPreview=free&sub=free&device=desktop&audience=everyone&free_preview=false&freemail=true#%C2%A773-self-modifying-titans-and-the-hope-architecture)*
		4. *[Training Pipeline](https://vizuara.substack.com/p/23c397ae-b774-4c2e-b0ef-a280e030d5c9?updated=2026-06-27T12%3A24%3A02.359Z&postPreview=free&sub=free&device=desktop&audience=everyone&free_preview=false&freemail=true#%C2%A774-training-pipeline)*
		5. *[Inference-Time Optimization](https://vizuara.substack.com/p/23c397ae-b774-4c2e-b0ef-a280e030d5c9?updated=2026-06-27T12%3A24%3A02.359Z&postPreview=free&sub=free&device=desktop&audience=everyone&free_preview=false&freemail=true#%C2%A775-inference-time-optimization)*
		6. *[Muon and the Multi-Scale Momentum Optimizer (M3)](https://vizuara.substack.com/p/23c397ae-b774-4c2e-b0ef-a280e030d5c9?updated=2026-06-27T12%3A24%3A02.359Z&postPreview=free&sub=free&device=desktop&audience=everyone&free_preview=false&freemail=true#%C2%A776-muon-and-the-multi-scale-momentum-optimizer-m3)*
8. *[Results and Outcomes](https://vizuara.substack.com/p/23c397ae-b774-4c2e-b0ef-a280e030d5c9?updated=2026-06-27T12%3A24%3A02.359Z&postPreview=free&sub=free&device=desktop&audience=everyone&free_preview=false&freemail=true#%C2%A78-results-and-outcomes)*
9. *[Thoughts](https://vizuara.substack.com/p/23c397ae-b774-4c2e-b0ef-a280e030d5c9?updated=2026-06-27T12%3A24%3A02.359Z&postPreview=free&sub=free&device=desktop&audience=everyone&free_preview=false&freemail=true#%C2%A79-thoughts)*
10. *[Conclusion](https://vizuara.substack.com/p/23c397ae-b774-4c2e-b0ef-a280e030d5c9?updated=2026-06-27T12%3A24%3A02.359Z&postPreview=free&sub=free&device=desktop&audience=everyone&free_preview=false&freemail=true#%C2%A710-conclusion)*

---

## 1\. Introduction

A while back, I wrote about Titans which is Google’s proposal for a model that could update its own memory during inference, without waiting for a retraining cycle. If you haven’t read that piece, I’d strongly recommend starting [there](https://vizuara.substack.com/p/titans-learning-to-memorize-at-test), as what follows builds directly on it.

Titans was a significant result. It demonstrated that the rigid boundary between training and inference; something the field had treated as structurally fixed but it doesn’t have to be that way. By treating the hidden state of a neural module as a learnable projector rather than a static representation, Titans showed that a model could genuinely update what it knows at test time, not just retrieve from what it was trained on. The three-memory architecture: short-term attention, long-term updatable state, persistent fixed memory was a clean solution to a problem that RNNs, SSMs, and standard transformers had each failed to solve completely.

But there was a question the original Titans paper left open.

Titans showed you *could* learn at test time. What it didn’t fully answer was how to do this *continuously* across an ongoing stream of new information, over long horizons, without the memory degrading, overwriting itself, or losing coherence with what came before. A model that updates once at test time is impressive. A model that keeps updating, correctly and efficiently, across thousands of interactions is a much different and harder problem entirely.

![](https://substackcdn.com/image/fetch/$s_!Os_a!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff69598c4-bbf2-4785-9831-308688e74674_500x616.png)

The [paper we are discussing today](https://arxiv.org/pdf/2512.24695) (also from Google) is the answer to that question. It introduces a framework for continuous inference-time learning a system where the model doesn’t just adapt to a single query, but genuinely accumulates knowledge across time, deciding what to remember, what to overwrite, and how to integrate new information into reasoning without destroying what already exists. This is done by combining self-modifying sequence model with the continuum memory system for a learning module, called Hope, showing promising results in language modeling, knowledge incorporation and reasoning.

A lot of jargons? Dont worry; That is what we are unpacking today.

---

## 2\. How Do Models Learn Beyond Training?

Before we get into the architecture, we need to build a precise understanding of what it even means for a model to learn and how much of that learning can happen after the training run ends. This is not a philosophical question. It has direct architectural consequences.

#### 2.1 The Spectrum

Most discussions treat model learning as a binary, i.e. either the model is training, or it is not; this framing is too coarse/sparse. The more useful way to think about it is as a spectrum, defined by a single axis: **how much is the model allowed to change in response to new information?**

At one extreme, you have a fully frozen model with weights fixed, no updates of any kind, every query answered from a static snapshot of what was learned during pretraining. At the other extreme, you have a fully dynamic model; one that continuously updates its own parameters in real time, integrating every new piece of information as it arrives.

In between these two poles live three distinct learning regimes, each with a different answer to how much change is permitted and where that change is allowed to happen.

![](https://substackcdn.com/image/fetch/$s_!uOTP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e43b484-bda2-4d94-8c33-99e82faea674_2486x1359.png)

HOPE operates on Inference-time learning block (green)

#### 2.2 In-Context Learning (Change Without Weight Updates)

The softest form of post-training adaptation is in-context learning. The model weights never change. Instead, the model conditions its behaviour on examples, instructions, or information provided directly in the context window; hence, effectively using the attention mechanism as a temporary, ephemeral form of memory.

Formally, given a context C=(c1,c2,…,ck) of examples and a query q, in-context learning computes:

$$
P \left(y \mid q , C\right) = P \left(y \mid q , c_{1} , c_{2} , \ldots , c_{k}\right)
$$

The model hasn’t learned anything in the weight-update sense. It has simply conditioned on more information. The moment the context window is cleared, everything is gone and the model returns to its prior state as if nothing happened.

![All You Need to Know about In-Context Learning | Towards Data Science](https://substackcdn.com/image/fetch/$s_!Ptm3!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa3f6f19-2afd-46a6-9b77-ec1b6a66f33b_483x360.png)

All You Need to Know about In-Context Learning | Towards Data Science

This is powerful as Transformers are remarkably good at in-context learning, and it requires zero infrastructure beyond the model itself. But it has a hard ceiling: the context window. Once k exceeds the maximum sequence length, you cannot fit more information in. The model’s ability to adapt is bounded by how much it can see at once, not by how much it has experienced over time.

In-context learning is adaptation without memory. It is stateless across queries and boundless in its forgetting.

#### 2.3 Continual Learning (Change Across Time, Without Forgetting)

Continual learning asks for something harder. The model should be able to learn from a sequential stream of tasks or data over time hence accumulating knowledge rather than replacing it. Each new piece of information should be integrated without destroying what came before.

The core challenge is **catastrophic forgetting**; which happens when a neural network is updated on new data via gradient descent, the weight updates that improve performance on the new task systematically degrade performance on old tasks. The gradients don’t know what the old weights were protecting. They just follow the loss surface of the current objective, overwriting whatever was previously encoded.

Formally, suppose a model with parameters θ is trained sequentially on tasks T1,T2,…,Tn. After training on Ti, the parameters shift from θi−1 to θi. The catastrophic forgetting problem is:

$$
m a t h c a l L_{\mathcal{T}_{j}} \left(\theta_{i}\right) \gg \mathcal{L}_{\mathcal{T}_{j}} \left(\theta_{j}\right) \text{for } j < i
$$

Performance on old tasks Tj degrades severely after training on new ones. The model is plastic as it learns new things; but it is not stable as it cannot retain old things simultaneously/to a large extent.

This is the **plasticity-stability tradeoff**, and it is the central unsolved tension in continual learning. A model that updates too readily is plastic but unstable as it learns fast and forgets fast. A model that updates too conservatively is stable but rigid as it retains old knowledge but resists integrating new information. These two requirements pull in opposite directions, and there is no free solution that achieves both simultaneously.

#### 2.4 Inference-Time Learning (Change During the Forward Pass)

Inference-time learning is the most architecturally radical of the three. The model updates its own parameters *during* inference, not before, not after, but as part of the forward pass itself. Each query doesn’t just consume the model’s knowledge; it potentially modifies it.

This sounds paradoxical as inference is supposed to be a read operation as you can pass an input forward through fixed weights and get an output. Making it also a write operation where the forward pass updates the very weights it is passing through requires rethinking what a forward pass even means.

Architecturally, this requires two things. First, a subset of the model’s parameters must be designated as updatable at inference time (not the full model), which would be prohibitively expensive, but a structured, bounded module whose updates are fast and local. Second, an update rule must be defined that operates at inference speed; not full backpropagation through the entire model, but a lightweight approximation that captures the signal of new information without the cost of a full training step.

The Titans architecture from the previous article was an early answer to both requirements. The neural memory module which is a small MLP whose weights serve as the memory state can be updated during inference via a self-supervised objective. The update is local, fast, and bounded. It doesn’t touch the full model. But as noted in the introduction, it handles a single update at test time. What happens when updates need to keep coming?

#### 2.5 Three Points on the Same Spectrum

These three regimes are not competing paradigms. They are different answers to the same question: how much should a model be allowed to change in response to new information? when placed at different points on a single spectrum; it looks something like this:

![](https://substackcdn.com/image/fetch/$s_!xYEE!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23b4f8fa-bc38-40de-babc-7e4179158b8c_2082x254.png)

The paper this article covers lives at the inference-time learning end of this spectrum; but it extends it further than Titans did, toward something closer to true continual learning. The model doesn’t just update once at test time. It keeps updating, across a stream of information, with an explicit mechanism for deciding what to retain and what to overwrite.

That is the regime the next sections build toward.

---

## 3\. Why RAG Isn’t Enough

If the spectrum in the previous section is about how much a model is allowed to change, RAG occupies a curious position as it looks like it solves the memory problem, without actually touching the model at all.

#### 3.1 What RAG Actually Does

Retrieval-Augmented Generation works by treating an external corpus as a lookup table. Given a query q, a retriever selects the top-k most relevant documents D=(d1,d2,…,dk) from a large external store, and these are concatenated into the model’s context:

$$
P \left(y \mid q\right) \approx P \left(y \mid q , d_{1} , d_{2} , \ldots , d_{k}\right)
$$

This should look familiar as it is structurally identical to the in-context learning formulation from the previous section. RAG is not a new point on the spectrum. It is in-context learning with an automated retrieval step bolted on front. The model weights never change. The retrieved documents are not learned because they are simply read, once, for this query, and discarded the moment the next query begins.

This is why RAG feels like memory; but isn’t. It gives the appearance of a model that “knows” things beyond its training data, but the knowing is entirely externally held in a vector database, not in the model itself.

#### 3.2 The Structural Limitations

Four limitations follow directly from this design.

**Context window bounds.** Retrieved documents still have to fit inside the model’s context window, alongside the query and the conversation history. As the corpus grows, the retriever has to be more selective; because the value of k stays roughly fixed even as the available information grows without bound.

**Retrieval quality ceiling.** The entire system is bottlenecked by the retriever’s ability to find the right k documents. If the retriever misses the relevant document because of an imperfect embedding, an ambiguous query, or information that wasn’t indexed well; then the model never sees it, no matter how capable the model itself is. The generator cannot compensate for what the retriever failed to surface.

**No true integration.** This is the subtlest limitation. Even when retrieval succeeds and the right document is in context, the model is not integrating that information into its world model. It is conditioning on it, for this one forward pass, the way it would condition on any other text in the prompt. The next query starts from zero again; hence, nothing about how the model reasons has changed, only what it was shown changed (abstract context).

**Stateless across queries.** Every query is an independent retrieval-and-generate event. There is no accumulation. If a user mentions an important fact in turn one, and the conversation moves past it in the context window by turn fifty, that fact has to be re-retrieved or it is gone as the model never actually held it in the first place. (arguably memory could be maintained; but it is just another layer of retrieval).

#### 3.3 The Deeper Problem: Memory as Storage vs. Memory as Structure

These four limitations all trace back to a single design choice: RAG treats memory as something external to the model like a filing cabinet you consult, rather than something that shapes how you think.

This is worth sitting with, because it is easy to conflate “has access to information” with “remembers” and they are not the same thing. A filing cabinet gives you access to information. It does not change how you reason about the world. You can look something up, use it for the task at hand, and put it back, completely unchanged by having read it.

![](https://www.youtube.com/watch?v=Rvmvt7gscIM)

Human memory does not work this way, because when you learn something like a fact, a skill, a person’s name then it does not sit in a separate compartment that you consult on demand. It becomes part of the substrate you think with; hence it changes which associations come to mind, which patterns you notice, which conclusions feel obvious versus surprising.

#### 3.4 The Question This Sets Up

This reframes the problem we actually need to solve. The question is not *“how do we give a model access to more information than fits in its context window”*; as that is the question RAG answers, reasonably well.

The question is: what would it mean for a model to actually remember something; basically not retrieve it from an external store and condition on it for one forward pass, but have it genuinely reshape how the model processes every subsequent query, the way a fact you learned last year quietly shapes a judgment you make today, without you consciously retrieving it at all? That is a question about architecture, not retrieval infrastructure.

---

## 4\. Why Memory is Hard

We have established what memory should look like in principle: structure that shapes reasoning, not storage you consult on demand. Now we need to confront why building this is genuinely difficult, not just an engineering inconvenience waiting to be solved with more compute.

#### 4.1 The Plasticity-Stability Tradeoff

Any system that learns continuously faces a tension between two properties it needs simultaneously.

**==Plasticity==** ==is the ability to change in response to new information. A model needs this, or it can never learn anything beyond what it saw during pretraining.==

**==Stability==** ==is the ability to retain what was already learned. A model needs this too, or every new piece of information would simply erase the last one (remember catastrophic forgetting).==

The problem is that these two properties pull directly against each other. Consider a model with parameters θ, currently encoding some knowledge K <sub>old</sub>, that receives a new piece of information requiring an update Δθ:

$$
\theta_{\text{new}} = \theta_{\text{old}} + \Delta \theta
$$

If Δθ is large enough to fully encode the new information, it is also large enough to overwrite whatever values in θ <sub>old</sub> were responsible for K <sub>old</sub>. There is no inherent mechanism in this update rule that protects old knowledge while incorporating new knowledge. The same parameters that hold K <sub>old</sub> are the parameters being modified to hold the new information.

You can dampen Δθ to reduce the risk of overwriting. But a smaller Δθ also means less of the new information actually gets encoded. You have not solved the tradeoff. You have just chosen a different point on it. Push toward plasticity and you risk forgetting. Push toward stability and you risk never learning. There is no parameter setting that gives you both for free.

#### 4.2 Catastrophic Forgetting

The plasticity-stability tradeoff is the abstract version of the problem. Catastrophic forgetting is what it looks like concretely, in a trained neural network, when gradient descent is the update mechanism.

![](https://substackcdn.com/image/fetch/$s_!84xD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4858b94e-a14d-4d70-bd84-6afc2196a3dd_2254x1542.png)

caption...

Suppose a model has been trained on task T <sub>1</sub> and has converged to a region of parameter space θ <sub>1</sub> that performs well on it. Now it receives new data from task T <sub>2</sub> and is updated via gradient descent:

$$
\theta_{2} = \theta_{1} - \eta \nabla_{\theta} \mathcal{L}_{\mathcal{T}_{2}} \left(\theta_{1}\right)
$$

This update is computed entirely with respect to T <sub>1</sub>. The gradient ∇ <sub>θ</sub> L <sub>T2</sub> has no term, no penalty, no awareness whatsoever of L <sub>T1</sub>. It simply descends the loss surface of the current task. If the region of parameter space that minimizes L <sub>T2</sub> is far from the region that minimized L <sub>T1</sub>, the update walks the model directly away from where it needs to be for the old task.

The result is not gentle decay. It is sudden and severe. Performance on T <sub>1</sub> can collapse after just a few gradient steps on T <sub>2</sub>, even though nothing in the training procedure explicitly tried to destroy that knowledge. It is simply a side effect of optimizing for the wrong objective using parameters that were doing double duty.

This is the mechanism, not just the symptom. Any system that wants to learn continuously without forgetting needs to either protect specific parameters from being overwritten, route new information to a region of parameter space that doesn’t interfere with old knowledge, or find some other structural way to prevent the gradient from old and new objectives from cancelling each other out.

#### 4.3 The Write Problem

Even if you solve the forgetting problem, you are left with a second, equally hard question: what is actually worth remembering?

Not all information that arrives during inference deserves to be written into memory. Some of it is noise. Some of it is redundant with what is already known. Some of it is relevant only to the current query and has no business influencing future reasoning. A memory system that writes everything indiscriminately will fill up fast, with most of its capacity spent on information that didn’t need to be retained in the first place.

This is a selection problem, and it is genuinely hard for a structural reason: deciding whether something is worth remembering often requires knowing whether it will be useful in the future, which you cannot know at the moment you encounter it. A fact that seems irrelevant today might be exactly what a future query needs. A fact that seems important today might never come up again.

A good memory system needs some signal, some proxy, for deciding what to write. This could be based on how surprising the new information is relative to what the model already expects, how often similar information has proven useful in the past, or how confidently the information can be verified. Whatever the signal, the system needs one, because the alternative, writing everything, is not actually a memory system. It is just an ever-growing, ever more diluted version of the context window problem RAG already has.

#### 4.4 Where This Leaves Us

Put these three problems together and the difficulty of the task comes into focus. You need a system that is plastic enough to integrate genuinely new information, stable enough not to destroy what it already knows, and selective enough not to drown itself in irrelevant updates. None of these three requirements can be solved in isolation. A solution to plasticity that ignores stability gives you catastrophic forgetting. A solution to stability that ignores plasticity gives you a frozen model. A solution to both that ignores selectivity gives you a memory system that degrades under its own weight.

This is the real shape of the problem the next section’s ideal case has to grapple with. Not “can a model update at test time”, which Titans already showed was possible, but “can a model update continuously, indefinitely, while staying coherent.” That is a substantially harder bar to clear.

---

## 5\. The Ideal Case

Let’s start with an unconstrained dream, the similar way we did for Fast BLT (our previous article).

The perfect continuously-learning memory system would do four things at once. It would update instantly the moment new information arrives, with no separate training step and no delay. It would never forget anything it had previously learned, no matter how much new information arrived afterward. It would know, automatically, what was worth remembering and what wasn’t, writing only the information that would matter later. And it would integrate everything it learned into how it reasons, not store it as a separate fact to be consulted, but let it quietly reshape every subsequent inference.

This is the ideal. Instant plasticity, perfect stability, perfect selectivity, full integration. And it is unachievable, for reasons that go deeper than current engineering limitations.

---

#### 5.1 Why the Ideal Breaks Down

The reason traces directly back to section 4.1. Plasticity and stability are not two independent dials you can both turn to maximum. They are coupled through the same mechanism, the same set of parameters, the same update rule.

Recall the update equation:

$$
\theta_{\text{new}} = \theta_{\text{old}} + \Delta \theta
$$

For the system to be instantly and fully plastic, Δθ must be large enough to fully encode any new piece of information, regardless of how it relates to what is already stored. For the system to be perfectly stable, Δθ must never perturb the components of θ <sub>old</sub> that encode previously learned knowledge. These two requirements can only both hold if every new piece of information happens to map onto a completely disjoint region of parameter space from everything learned before it, indefinitely, forever. There is no mechanism that guarantees this. Parameter space is finite. Information is not.

This is structurally the same kind of impossibility we encountered with the autoregressive dependency chain in the Fast BLT article. There, the constraint was that you cannot compute x <sub>t</sub> before x <sub>t−1</sub> exists, because the dependency is a logical fact about the factorization of the joint distribution, not an engineering limitation. Here, the constraint is that you cannot guarantee perfect plasticity and perfect stability simultaneously, because the parameters doing the remembering are the same parameters being asked to change. It is not a question of better hardware or more compute. It is a property of what it means to update a finite system indefinitely.

The selectivity requirement compounds this. Even if you could solve plasticity and stability, deciding what is worth remembering requires information about the future that is not available at write time, as we discussed in section 4.3. A perfect selector would need to know, in advance, which pieces of information will matter for queries that haven’t been asked yet. This is not a hard engineering problem. It is asking for foresight the system structurally cannot have.

#### 5.2 The Real Question

Given that the ideal is unreachable, the question that matters is not “how do we build the perfect memory system.” It is: how close can we get, and what are we willing to give up to get there?

This reframes the entire design space. Just as Fast BLT was not trying to reach the impossible single-pass generation ideal but instead tracing a speed-quality frontier as close to it as possible, a continuous learning system is not trying to reach perfect plasticity and perfect stability simultaneously. It is trying to trace a frontier between them, recovering as much of both as the architecture allows.

We can write this formally as a constrained optimization, mirroring the structure from our Fast BLT article. Let P denote plasticity, how readily the system integrates new information, and let S denote stability, how well it retains old information. The achievable frontier is:

$$
S^{*} \left(P\right) = \underset{\text{architecture}}{max} S \text{subject to} \text{plasticity} = P
$$

Every architectural choice, how memory is represented, how updates are computed, what gets written and what gets protected, places the system at some point on or below this frontier. The goal of any concrete design is to push as close to the frontier as possible, knowing the frontier itself never touches the ideal corner of perfect P and perfect S simultaneously.

#### 5.3 What Determines How Close You Can Get

Two things determine where on this frontier a real system can land.

**How the architecture separates what changes from what stays fixed.** If updates are forced to touch the same parameters that encode everything else, plasticity and stability fight directly, as in section 4.1’s basic update equation. If the architecture instead routes new information into a structurally separate component, one that can change freely without disturbing a more protected store of existing knowledge, the conflict softens considerably. This is the architectural lever.

**How selective the write mechanism is.** A system that filters aggressively, writing only information that clears some bar of novelty or usefulness, makes far better use of its limited capacity for change than one that writes indiscriminately. This does not solve the foresight problem from section 4.3, but a good proxy signal, something correlated with future usefulness even if not a perfect predictor of it, can meaningfully improve where the system sits on the frontier.

These two levers, architectural separation of memory components, and selective writing, are exactly what the methodology section is going to dig into. The paper’s answer to “how close can we get to the ideal” lives in how it structures the neural language module, how the continuous memory system is organized, and how the self-modifying mechanism decides what to write and what to protect.

That is where we are headed next.

---

## 6\. Quick Recap of Titans Architecture

If you’ve read the [original Titans article](https://vizuara.substack.com/p/titans-learning-to-memorize-at-test), this section will feel familiar.

If you haven’t, here is quick summary you need to follow the rest of this piece.

#### 6.1 The Core Idea: Memory as a Neural Module

Titans starts from a simple but consequential reframing: instead of treating memory as a fixed-size vector or buffer, treat it as the weights of a small neural network. The hidden state isn’t a static representation that gets overwritten and decayed the way an RNN’s hidden state does. It is a projector, a learnable function, with the capacity to encode high-resolution information precisely because it has parameters that can be optimized.

This single design choice resolves a tension we touched on in section 2. RNNs and SSMs achieve constant space complexity but suffer from lossy compression, since their fixed-size hidden state has to discard information to make room for new input. Transformers achieve high-quality representation through attention but pay for it with quadratic complexity, since every token attends to every other token. Titans’ neural memory module gets the constant space of an RNN while approximating the representational capacity of a much larger system, because the module’s weights, not just its activations, are doing the work of encoding information.

![](https://substackcdn.com/image/fetch/$s_!OLWQ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f7ae6ad-7007-4d17-9d92-6bc2b06a7c08_2714x860.png)

#### 6.2 Three Memories, Three Roles

Titans separates memory into three distinct components, each with a different update rule:

**Short-term memory** is standard attention, operating over a limited window of recent tokens. It is precise and high-quality, but quadratic in cost, so it is kept short by design.

**Long-term memory** is the neural module described above. Its weights are updated during inference, via a self-supervised objective, allowing the model to incorporate information from far outside the attention window without paying attention’s quadratic cost.

**Persistent memory** is also neural, also low-dimensional, but never updated at inference time. It encodes stable, task-general knowledge that should not drift, regardless of what happens during a particular inference session.

The separation between in-context and in-weights memory follows directly from this structure. In-context memory lives in the attention window, the same mechanism behind standard in-context learning from section 2.2, bounded and ephemeral. In-weights memory lives in the long-term module’s parameters, persisting across the session and shaped by an actual update rule rather than just conditioning.

#### 6.3 The Test-Time Update Mechanism

The mechanism that makes long-term memory updatable at inference time is a gradient step, computed on the fly, using a self-supervised objective often referred to as a surprise signal. When the model encounters information that its current memory module predicts poorly, the resulting error drives an update to the memory module’s weights:

$$
\theta_{\text{mem}} \leftarrow \theta_{\text{mem}} - \eta \nabla_{\theta_{\text{mem}}} \mathcal{L}_{\text{surprise}}
$$

This is, structurally, the same update equation we wrote in section 4.1 and 5.1, applied specifically to the long-term memory parameters rather than the full model. The persistent memory and the bulk of the model’s other weights are left untouched. Only the long-term memory module is plastic at inference time, which is exactly the kind of architectural separation we flagged in section 5.3 as a lever for softening the plasticity-stability tradeoff.

#### 6.4 Where Titans Leaves Off?

Titans demonstrated something genuinely new: a model can update its own weights mid-inference, using a fast, local, self-supervised signal, without touching the bulk of the network. That is inference-time learning, concretely realized, for the first time at this level of architectural cleanliness.

But the original paper was largely concerned with a single inference session. It showed the update mechanism works, that it improves long-range understanding, that it can be parallelized for training. What it did not fully address was what happens when the updates don’t stop. What happens after the hundredth update to the same memory module, the thousandth, across sessions, across days, across a genuinely continuous stream of new information. Does the surprise-driven update rule remain well-behaved indefinitely, or does it start to drift, saturate, or interfere with itself the way the gradient updates in section 4.2 interfered across tasks?

Titans showed you could learn at test time, but the question this new paper takes on is how to do that continuously, and how to do it efficiently enough that it remains practical at scale. That is exactly where the methodology section picks up.

---

## 7\. Methodology

Now that we have revised Titan and under the capabilites and advancements we need on top of it to realize the idea of a strong continuual learning paradigm; let’s start with the methdology proposed in paper.

### 7.1 The Neural Learning Module and the Nested Learning Paradigm

Before this paper, the natural way to think about a deep network was as a stack of layers, each layer a fixed computational block, with a separate optimizer sitting outside the architecture, adjusting weights via backpropagation. Nested Learning (NL) asks you to discard that picture entirely.

![](https://substackcdn.com/image/fetch/$s_!lTzA!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff82fb003-0058-48b4-be37-386a9e7435dd_1506x830.png)

##### The Reframe: Optimizers Are Memory Modules

The paper’s starting observation is unusual: a gradient-based optimizer, the thing that updates a model’s weights, is itself a kind of memory module. Consider standard SGD with momentum. At every step, it takes the current gradient, combines it with a running average of past gradients, and uses that combination to update the weights:

$$
m_{t} = \beta m_{t - 1} + \left(1 - \beta\right) \nabla_{\theta} \mathcal{L} \left(\theta_{t - 1}\right)
$$

$$
\theta_{t} = \theta_{t - 1} - \eta m_{t}
$$

Look closely at the first equation. It is an associative memory update. The momentum term m <sub>t</sub> is compressing a stream of gradients, the “context flow” of the optimization process, into a fixed-size representation, the same way the long-term memory module in Titans compresses a stream of tokens into its weights. Adam does the same thing with two separate compression terms, one for the gradient mean and one for its variance.

This is the central reframe of Nested Learning: training a neural network and updating a memory module are not two different things happening at different stages. They are the same operation, an associative memory compressing a context flow, applied at different places in the system and at different speeds.

![](https://substackcdn.com/image/fetch/$s_!P81l!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ec19449-88e7-4fd5-b618-ba7d7437bde6_2556x1164.png)

##### Multi-Level Optimization

Once you accept that framing, a deep learning model stops looking like a flat stack of layers with one optimizer outside it, and starts looking like a set of nested optimization problems, each with its own context flow, each updating at its own frequency.

Formally, NL represents a model as a collection of levels ℓ=1,2,…,L, where each level has its own parameters θ(ℓ), its own local objective L(ℓ), and its own update frequency f(ℓ), the rate at which that level’s parameters are allowed to change:

$$
\theta_{t + 1}^{\left(ℓ\right)} = \theta_{t}^{\left(ℓ\right)} - \eta^{\left(ℓ\right)} \nabla_{\theta^{\left(ℓ\right)}} \mathcal{L}^{\left(ℓ\right)} \left(\right. \theta_{t}^{\left(ℓ\right)} , C_{t}^{\left(ℓ\right)} \left.\right)
$$

where Ct(ℓ) is the context flow that level ℓ sees at time t, the stream of information it is being asked to compress. Crucially, an outer level’s parameters can themselves be the thing that defines an inner level’s context flow or objective, which is why these problems are described as nested rather than merely parallel. The outer loop shapes the conditions under which the inner loop operates; the inner loop’s behaviour, in turn, contributes to the signal the outer loop optimizes against.

This single formalism is expressive enough to describe a standard transformer. In a transformer, the attention block has, in this framing, an effectively infinite update frequency, f→∞, since it recomputes its in-context behaviour fresh on every forward pass with no persistence across calls. The MLP blocks, by contrast, have update frequency f→0, since their weights are frozen entirely after pretraining and never change again at inference time. The paper’s striking observation is that the entire spectrum we mapped out in section 2, from in-context learning to continual learning, is really just a description of where on this frequency axis different components of a model happen to sit.

##### Why Nesting? (Navigating Plasticity and Stability Through Frequency)

This is where the nested structure earns its purpose. Recall the plasticity-stability tradeoff from section 4.1: a single set of parameters cannot be simultaneously maximally plastic and maximally stable, because the same update that integrates new information is the update that risks overwriting old information.

Nested Learning’s answer is not to find a clever update rule that magically achieves both. It is to refuse the premise that there has to be a single set of parameters and a single update rate at all. Instead, the system is decomposed into multiple levels, each with its own frequency, and the tradeoff is resolved not within any single level but across the hierarchy of levels.

![](https://substackcdn.com/image/fetch/$s_!XueS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd532e916-e813-467c-8901-9f3101a7b3e8_2870x1164.png)

A fast inner loop, updating frequently, gives you inference-time adaptability. It can absorb new information immediately, the way the attention mechanism absorbs the current context, or the way Titans’ long-term memory module absorbs a surprising new fact mid-session. Because it updates fast, it is plastic.

A slow outer loop, updating only during training, gives you stable long-term structure. It changes rarely, and when it does change, it does so based on aggregated signal across enormous amounts of data, not any single new fact. Because it updates slowly, it is stable.

Neither loop, on its own, solves the tradeoff. But together, they don’t have to. The fast loop is allowed to be unstable because the slow loop isn’t relying on it to hold permanent knowledge. The slow loop is allowed to be rigid because the fast loop is handling everything that needs immediate adaptation. The tradeoff from section 4.1 is not eliminated. It is distributed across timescales, with each level responsible only for the part of the tradeoff it is suited to handle.

This is the structural lever we flagged in section 5.3 as the key to pushing closer to the frontier, separating what changes from what stays fixed. Nested Learning generalizes that separation from Titans’ three discrete memory tiers into a full spectrum of update frequencies, and it is this generalization that the rest of the methodology, the Continuum Memory System and the self-modifying Hope architecture, builds directly on top of.

### 7.2 Continuum Memory System (CMS)

The traditional view of memory in a transformer is binary: there is short-term memory, the attention mechanism operating over recent tokens, and long-term memory, the MLP’s frozen weights encoding everything learned during pretraining. This binary framing maps cleanly onto the two extreme frequencies from section 7.1; which is attention at f→∞, MLPs at f→0; hence nothing in between.

The Continuum Memory System (CMS) discards this binary entirely as Memory is not two discrete tiers. It is a spectrum of frequencies, each responsible for a different timescale of knowledge, each updating at a rate appropriate to what it is storing; hence we want to operate in a continuous space.

#### 7.2.1 Memory as a Chain of Frequencies

Formally, CMS replaces the single MLP block in a transformer with a chain of kk k MLP blocks:

$$
\text{MLP}^{\left(f_{1}\right)} \left(\cdot\right) , \text{MLP}^{\left(f_{2}\right)} \left(\cdot\right) , \ldots , \text{MLP}^{\left(f_{k}\right)} \left(\cdot\right)
$$

where f1>f2>⋯>fk and each block updates at a strictly lower frequency than the one before it. Given input x={x1,…,xT}, the output of the chain is computed sequentially:

$$
y_{t} = \text{MLP}^{\left(f_{k}\right)} \left(\right. \text{MLP}^{\left(f_{k - 1}\right)} \left(\right. \hdots \text{MLP}^{\left(f_{1}\right)} \left(x_{t}\right) \left.\right) \left.\right)
$$

Each block ℓ has its own parameters θ <sup>(fℓ)</sup>, updated every C <sup>(ℓ)</sup> steps (its chunk size), the number of tokens it processes before incorporating what it has seen into its weights:

![](https://substackcdn.com/image/fetch/$s_!uTP3!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e03fdb7-99d0-430c-94c1-3ff593127eb9_2878x354.png)

The block updates in a batch; accumulating gradients over its chunk window and then applying them all at once. Between updates, its parameters are frozen, acting as a static memory for that timescale.

The standard transformer MLP is a degenerate case of this formulation: k=1, frequency of update zero, chunk size effectively infinite. CMS generalises this into a full spectrum by stacking blocks at different C <sup>(ℓ)</sup> values — with the smallest chunk size at the fastest block and the largest at the slowest.

#### 7.2.2 What Each Frequency Level Stores

This is the key intuition behind CMS: the chunk size C <sup>(ℓ)</sup> determines the scope of what a block can know about.

A block with C <sup>(ℓ)</sup> =1 updates on every single token. It is highly plastic as it responds immediately to every new piece of information; but its parameters reflect only the most recent token’s context. It is volatile by design. This is the fast, adaptive end of the spectrum.

A block with C <sup>(ℓ)</sup> =T represents the entire sequence length and updates only once after processing everything. Its parameters compress the entire context into a single set of weights. It is stable and slow to change, but what it stores is a global summary of everything seen so far. This is the persistent end of the spectrum.

Between these extremes, blocks at intermediate chunk sizes store knowledge at intermediate timescales. A block with C <sup>(ℓ)</sup> =128 has seen and integrated 128 tokens’ worth of context before updating its knowledge is local enough to be responsive, global enough to be coherent across a short segment.

![](https://substackcdn.com/image/fetch/$s_!Qx5o!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F51ed48b4-1e68-4c10-8f65-0d6c20dbc081_2622x1578.png)

Formally, each block’s parameters θ <sup>(fℓ)</sup> are a compressed representation of their context window:

$$
\theta^{\left(f_{ℓ}\right)} \approx arg \underset{\theta}{min} \mathcal{L} \left(\right. \theta ; \left\{\right. x_{t} \left.\right\}_{t = i - C^{\left(ℓ\right)}}^{i} \left.\right)
$$

This gives CMS a property the binary long-term/short-term model structurally cannot have: **multi-timescale knowledge recovery**. If a fast block forgets something because its chunk window has moved on, the information may still be encoded in a slower block whose window hasn’t expired yet. Knowledge can be partially recovered from a lower-frequency layer even after the fast layers have moved past it; which is something that is impossible in a system where the only options are ephemeral attention or frozen weights.

#### 7.2.3 The Write Mechanism

Writing into a CMS block is gradient-based memory update, applied locally within each block’s chunk window. For a block at frequency f <sup>ℓ</sup> processing chunk i, the write step is:

$$
\theta_{i + 1}^{\left(f_{ℓ}\right)} = \theta_{i}^{\left(f_{ℓ}\right)} - \sum_{t = i - C^{\left(ℓ\right)}}^{i} \eta_{t}^{\left(ℓ\right)} \nabla_{\theta} \mathcal{L} \left(\theta_{t}^{\left(f_{ℓ}\right)} ; x_{t}\right)
$$

The gradient here is computed with respect to the block’s own local objective in language modeling, this is the next-token prediction loss evaluated on the chunk. Each block is, in the Nested Learning framing from section 7.1, an associative memory compressing its own context flow into its parameters. The surprise signal is how much the block’s current parameters fail to predict the incoming token which drives the update.

Crucially, this write is **bounded in scope**. The gradient only flows through the current block’s parameters, not the full model. The plasticity is local. The slower blocks below it are not touched. This is the architectural separation we identified in section 5.3 as the key lever for navigating the plasticity-stability tradeoff as fast blocks are free to be plastic because slow blocks are structurally isolated from their updates.

#### 7.2.4 The Read Mechanism

Reading from CMS is simply the forward pass through the chain where input flows through MLP(f <sub>1</sub>) first, then MLP(f <sub>2</sub>), and so on. Each block transforms the representation based on its current parameter state, which encodes whatever it has learned from its chunk history.

This is fundamentally different from attention-based retrieval. In attention, reading involves computing similarity scores between a query and every key in the context, then retrieving a weighted combination of values. The retrieved content is always a direct function of the current query and the stored keys and values.

In CMS, reading is a deterministic forward pass through a learned function. There are no explicit keys, no similarity scores, no direct addressing. The block’s parameters have already compressed the relevant patterns from its context window as the read operation simply evaluates that compression on the current input. It is implicit retrieval rather than explicit lookup.

The tradeoff is expressivity versus efficiency. Attention retrieval is content-addressable which you can retrieve exactly what you ask for, from anywhere in the context. CMS retrieval is structural as whatever you get is shaped by what the block has learned to encode, which is a compressed summary of the context, not a direct lookup into it. For long-range information that matters across many tokens, CMS’s compression is more efficient. For precise retrieval of specific earlier tokens, attention remains sharper.

#### 7.2.5 Variants: How Levels Connect?

CMS is not a single architecture but a family, distinguished by how knowledge flows between frequency levels.

**Nested CMS** is the initial state of block ℓ+1 is meta-learned from block ℓ. Each block initializes from a stable learned prior rather than from zero:

$$
\theta_{0}^{\left(f_{ℓ + 1}\right)} = arg \underset{\Phi}{min} \mathbb{E}_{\mathcal{T} \sim \mathcal{C}^{\left(ℓ\right)}} \left[\right. \mathcal{L} \left(\Theta , \mathcal{T} ; \Phi\right) \left]\right.
$$

After each chunk is processed and the block resets, it reinitializes to this meta-learned starting point rather than cold-starting. This gives higher-frequency blocks a stable prior that reflects everything the lower-frequency levels have consolidated into an approximation of how the human brain’s offline consolidation during sleep replays (in hippocampus) and reorganizes recent memories into longer-term cortical storage.

**Sequential CMS** are blocks that are chained but independent/isolated during initialization. The output of one block feeds into the next, but there is no meta-learning of initial states across levels. This is simpler to implement, but at the cost of the inter-level knowledge transfer that nested CMS provides.

Both variants contrast sharply with the binary long-term/short-term memory model. There is no hard boundary between ephemeral and persistent memory as only a gradient of update frequencies, each responsible for its own timescale, collectively providing the multi-scale memory management that the plasticity-stability tradeoff requires.

### 7.3 Self-Modifying Titans and the Hope Architecture

The Continuum Memory System from section 7.2 solved the representation problem: how to store knowledge across multiple timescales without forcing everything into a binary long-term/short-term split. But it left a second problem untouched: what drives the updates? Every CMS block updates via gradient descent on the next-token prediction loss, which is a fixed, hand-designed update rule. The model learns what to store, but the mechanism by which it stores things is prescribed externally, the same gradient descent formula applied uniformly across every block, at every frequency level.

The Self-Modifying Learning Module asks a more radical question: what if the model learned its own update rule, rather than having one imposed on it?

#### 7.3.1 The Core Idea: Learning to Update

Recall from section 7.1 that NL frames a gradient-based optimizer as an associative memory module, something that compresses a context flow (the gradient history) into a fixed representation (the momentum terms or second moments) via gradient descent on a local objective. The update rule itself is therefore just another learned compression, operating at a higher level than the network weights it is updating.

This observation opens a design space that standard deep learning leaves completely unexplored: if the update rule is a compression, and if more expressive compressions are better, then the update rule itself can be parameterized and learned, in the same way we learn the network weights it applies to.

The Self-Modifying Learning Module (SMLM) operationalizes this. It is a sequence model that maintains two sets of parameters:

- **Outer parameters** (Θ), updated only during training via standard backpropagation on the task loss. These are slow, stable, and encode the model’s long-run structural knowledge.
- **Inner parameters** (ϕ), updated during inference according to a rule that is itself parameterized by Θ. These are fast, plastic, and encode the model’s short-run adaptation to the current context.

![](https://substackcdn.com/image/fetch/$s_!-Yt9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4eb23dc0-835f-47d1-86c9-ca6c154f99b9_2352x1511.png)

The key property is that the inner update rule is not fixed. It is a function gΘ learned by the outer loop:

$$
\phi_{t + 1} = \phi_{t} + g_{\Theta} \left(\phi_{t} , x_{t} , \nabla_{\phi} \mathcal{L} \left(\phi_{t} ; x_{t}\right)\right)
$$

where gΘ is a learned function parameterized by the outer weights Θ, taking the current inner parameters, the current input, and the current gradient as inputs, and outputting a parameter update. The outer loop trains Θ such that the resulting gΘ produces good inner updates across a distribution of tasks and contexts. The inner loop applies gΘ at inference time to actually adapt ϕ.

This is what “learning to modify itself” means concretely. The model is not just updating its weights at inference time. It is doing so according to an update rule that was itself optimized, end to end, to be a good update rule for this class of problems.

#### 7.3.2 How a Self-Modifying Layer Works

To make this concrete, consider how a single SMLM layer processes an input sequence x1,x2,…,xT.

At each step tt t, the layer maintains its current inner parameters ϕt. The forward pass has two components that happen simultaneously.

**The output computation** applies ϕt to the current input:

$$
y_{t} = f_{\phi_{t}} \left(x_{t}\right)
$$

This produces the layer’s output for this token, using whatever the inner parameters currently encode.

**The parameter update** applies the learned update rule to generate new inner parameters for the next step:

$$
\phi_{t + 1} = \phi_{t} + g_{\Theta} \left(\right. \phi_{t} , x_{t} , \nabla_{\phi} \mathcal{L} \left(f_{\phi_{t}} \left(x_{t}\right) , x_{t}\right) \left.\right)
$$

The gradient ∇ϕL here is computed with respect to a local self-supervised objective, something like predicting the current token given recent context, the same surprise signal from Titans’ memory update in section 6.3. The output y <sub>t</sub> and the updated parameters ϕt+1 are both produced in the same forward step. The layer has processed the input and updated itself simultaneously.

#### 7.3.3 Why This Is Different from Fine-Tuning

The comparison to fine-tuning is natural but misleading. Fine-tuning updates a model’s weights on new data using backpropagation through the full network on a labeled objective, with an externally chosen optimizer running for multiple gradient steps over the full parameter space. It is a process that happens offline, between deployments, not during inference.

The SMLM update differs on every one of these dimensions.

**Scope.** The inner update touches only ϕ, the inner parameters of this specific layer. The outer parameters Θ are completely frozen during inference. The rest of the model is not involved. There is no risk of one layer’s adaptation cascading into unintended changes elsewhere in the network.

**Speed.** The update gΘ(⋅) is a single forward pass through a learned function, not iterative gradient descent over multiple steps. It happens in the same computational budget as the forward pass itself.

**The update rule itself.** In fine-tuning, the optimizer is SGD or Adam, chosen by the engineer, fixed, the same for every problem. In the SMLM, the optimizer is gΘ, learned end to end to be a good update rule for this specific class of tasks. This is the deeper difference: the model is not just updating its weights with an external tool. It has internalized the update process as part of its own learned behavior.

#### 7.3.4 Gradient Flow Through a Self-Modifying Layer

This section requires careful treatment because the gradient flow is non-trivial in a way that matters for how the system is trained.

In a standard layer, the gradient of the loss with respect to the layer’s input flows through the layer’s fixed parameters. One backward pass, one gradient, one update.

In an SMLM layer, there are two pathways through which gradients flow:

**Pathway 1: Through the output.** The standard path. Given output yt=fϕt(xt), the outer training loss L <sub>outer</sub> backpropagates through y <sub>t</sub> to reach ϕ <sub>t</sub> and Θ:

$$
\frac{\partial \mathcal{L}_{\text{outer}}}{\partial \Theta} \left|\right._{\text{path 1}} = \frac{\partial \mathcal{L}_{\text{outer}}}{\partial y_{t}} \cdot \frac{\partial y_{t}}{\partial \phi_{t}} \cdot \frac{\partial \phi_{t}}{\partial \Theta}
$$

**Pathway 2: Through the update rule.** The less obvious path. Because ϕt+1 depends on Θ through the learned update rule gΘ, and because y <sub>t+1</sub> depends on ϕ <sub>t+1</sub>, the outer loss at step t+1 also flows back through the update rule itself to reach Θ:

$$
\frac{\partial \mathcal{L}_{\text{outer}}}{\partial \Theta} \left|\right._{\text{path 2}} = \frac{\partial \mathcal{L}_{\text{outer}}}{\partial y_{t + 1}} \cdot \frac{\partial y_{t + 1}}{\partial \phi_{t + 1}} \cdot \frac{\partial \phi_{t + 1}}{\partial \Theta}
$$

where ∂Θ∂ϕt+1 requires differentiating through gΘ, which itself is a neural network with parameters Θ. The total gradient on Θ is the sum across both pathways, and across all timesteps:

$$
\frac{\partial \mathcal{L}_{\text{outer}}}{\partial \Theta} = \sum_{t = 1}^{T} \left(\frac{\partial \mathcal{L}_{\text{outer}}}{\partial \Theta} \left|\right._{\text{path 1}} + \frac{\partial \mathcal{L}_{\text{outer}}}{\partial \Theta} \left|\right._{\text{path 2}}\right)
$$

This is what makes the outer loop training expensive and why it requires careful implementation. Computing path 2 requires differentiating through the update rule gΘ, which means keeping the computation graph of the inner loop alive during the outer loop backward pass, a memory cost analogous to unrolling an RNN through time.

In practice, the paper truncates this to avoid the full unrolling cost, computing only a fixed number of inner steps before detaching the gradient, the same truncated backpropagation through time trick used in training recurrent networks. The truncation introduces bias into the outer gradient estimate but keeps the training computationally tractable.

#### 7.3.5 Hope: Putting It Together

Hope (Higher-Order Parameter Evolution) is the concrete architecture that combines the Self-Modifying Learning Module with the Continuum Memory System into a single, unified sequence model.

![](https://substackcdn.com/image/fetch/$s_!m4Jk!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5fbafec1-f4b9-4dd6-8f00-3e1627854e7e_2037x1718.png)

The architecture replaces the standard transformer block with a Hope block, which consists of:

- A standard attention layer handling short-term in-context memory, unchanged from the transformer
- A CMS chain handling multi-timescale in-weights memory, updating at decreasing frequencies
- An SMLM layer whose inner update rule is learned rather than fixed, operating on top of the CMS chain’s output

Each component maps onto a different level of the nested learning hierarchy from section 7.1. Attention operates at infinite frequency, reading the current context with full precision and no persistence. The CMS chain operates at intermediate frequencies, encoding knowledge across windows of increasing length. The SMLM layer operates with a learned update rule that itself evolves during outer loop training, making the entire adaptation mechanism a product of optimization rather than engineering.

The result is a model where different parts of the parameter space change at different rates, for different reasons, according to rules that were themselves learned. Attention adapts every token, the CMS chain adapts every chunk, and the SMLM layer adapts according to a policy that the outer loop trained specifically to be useful for this task distribution. Each level handles the part of the plasticity-stability tradeoff it is best suited for, and no single level is asked to handle all of it alone.

### 7.4 Training Pipeline

Training a model that modifies itself at inference time is not straightforwardly reducible to standard supervised learning. The usual setup is based on fixed parameters, one forward pass, one backward pass, one gradient update and assumes the model being evaluated is the same model (static weight structure) throughout. Hope violates this assumption. The model at step t+1 has different inner parameters than the model at step t, because the forward pass at step t already updated them. Training a system like this requires a careful decomposition of what is being optimized, at what speed, and against what objective.

#### 7.4.1 The Two-Loop Training Structure

Training Hope decomposes into two nested optimization loops, operating at different timescales and against different objectives. This maps directly onto the NL formalism from section 7.1, but now applied to the training procedure itself rather than just the inference procedure.

The **inner loop** runs at inference time. Given a sequence of inputs x1,x2,…,xT, the inner loop applies the learned update rule gΘ to update the inner parameters ϕ at each step:

$$
\phi_{t + 1} = \phi_{t} + g_{\Theta} \left(\phi_{t} , x_{t} , \nabla_{\phi} \mathcal{L}_{\text{inner}} \left(\phi_{t} ; x_{t}\right)\right)
$$

The inner loop objective L <sub>inner</sub> is a self-supervised signal, typically next-token prediction on the current chunk, the same surprise-based signal from Titans. This objective is local and computed on the fly. Neither labels are needed nor external supervision is required as the inner loop is entirely self-contained.

The **outer loop** runs during training. It optimizes the outer parameters Θ (which include the weights of the learned update rule gΘ and the slow CMS blocks) against a task-level objective L <sub>outer</sub> computed after the inner loop has already run:

$$
\Theta_{k + 1} = \Theta_{k} - \eta_{\text{outer}} \nabla_{\Theta} \mathcal{L}_{\text{outer}} \left(\right. \phi_{T} \left(\Theta_{k}\right) , \Theta_{k} ; \mathcal{D} \left.\right)
$$

where ϕT(Θk) denotes the inner parameters after T steps of inner loop adaptation starting from Θk. The outer gradient therefore has to propagate back through the inner loop updates, which is what creates the two-pathway gradient structure we described in section 7.3.4.

![](https://substackcdn.com/image/fetch/$s_!eWYf!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd73ba695-b33b-488f-8c59-3e69494e8948_2509x1924.png)

The key asymmetry is that the outer loop is training Θ to produce a gΘ that makes the inner loop useful, not just to minimize the loss on the current batch. The outer loop is optimizing for a property of the inner loop’s behavior, not just for a direct prediction objective.

#### 7.4.2 The Outer Loop Objective

The outer loop objective has to capture what it means for the inner loop to have been useful. A naive choice would be to evaluate the task loss at the very end of the sequence, after all inner loop updates have been applied:

$$
\mathcal{L}_{\text{outer}} \left(\Theta\right) = \mathbb{E}_{x \sim \mathcal{D}} \left[\mathcal{L}_{\text{task}} \left(f_{\phi_{T}} \left(x_{T}\right)\right)\right]
$$

This is valid but myopic as it rewards gΘ only for what the inner loop managed to produce by the final token, giving no signal about the quality of intermediate adaptations. A better objective aggregates the task loss across all timesteps after the first inner update:

$$
\mathcal{L}_{\text{outer}} \left(\Theta\right) = \mathbb{E}_{x \sim \mathcal{D}} \left[\sum_{t = 1}^{T} \mathcal{L}_{\text{task}} \left(f_{\phi_{t}} \left(x_{t}\right)\right)\right]
$$

This rewards the learned update rule for producing good predictions at every step, not just at the end. It means the outer loop is training gΘ to be a good optimizer throughout the sequence, producing useful parameter updates early and consistently, rather than one that only converges to something useful after many steps.

The outer loop loss is evaluated against the standard language modeling objective on a held-out task distribution, something rich and diverse enough that the learned update rule gΘ has to generalize across contexts rather than overfit to a narrow task.

#### 7.4.3 Keeping the Inner Loop Stable

The most practically delicate part of training Hope is ensuring the inner loop updates don’t destabilize during training. Because gΘ is itself being learned, there is no guarantee early in training that the update rule it produces is well-behaved. A poorly initialized gΘ can produce inner updates that send ϕ into a bad region of parameter space, which then produces a garbage outer gradient, which then produces a worse gΘ, which produces even worse inner updates. The training dynamics can spiral.

Three mechanisms stabilize this.

**Initialization.** The inner parameters ϕ are initialized from the outer parameters Θ at the start of each sequence. This means the inner loop starts from a known good point, the outer loop’s current best estimate of a good parameter configuration, rather than from a random initialization. Even if the first few inner updates are poor, the starting point is already reasonable.

**Update magnitude clipping.** The learned update rule gΘ is regularized to produce updates bounded in norm:

$$
\parallel \Theta \left(\phi_{t} , x_{t} , \nabla_{\phi} \mathcal{L}\right) \parallel_{2} \leq \delta
$$

for a small threshold δ. This prevents catastrophically large inner updates, regardless of what the raw output of gΘ would otherwise be. It is a hard constraint, not a soft penalty, so the inner loop cannot escape its stability envelope no matter how badly gΘ misfires early in training.

**Truncated inner unrolling.** As discussed in section 7.3.4, the outer loop gradient propagates back through the inner loop updates. If this unrolling runs for all T inner steps, the computation graph becomes enormous and the gradients become numerically unstable, exploding or vanishing through the long chain of inner updates. The paper truncates the unrolling to a fixed window K≪T, computing outer gradients only through the last K inner steps and treating earlier ones as detached constants. This introduces bias into the outer gradient estimate but keeps the training numerically stable and computationally tractable.

#### 7.4.4 Data Ordering and Curriculum

In a standard transformer, training data order matters primarily for optimization efficiency. Curriculum learning, where easier examples come earlier, can speed up convergence, but the model’s final capabilities are largely order-agnostic because every forward pass sees the same fixed weights.

Hope breaks this. Because the inner loop updates ϕ as it processes a sequence, the order of tokens within a training sequence now affects the state of ϕ at every subsequent position. A sequence where easier, more predictable tokens come first produces a better-initialized ϕ by the time harder tokens arrive. A sequence where difficult tokens come first may send ϕ off in a bad direction before the inner loop has had time to stabilize. This has two practical consequences:

**Within-sequence ordering matters.** Training sequences should be constructed so that each sequence has some internal coherence, so that the inner loop is adapting to a consistent local context rather than a random splice of unrelated documents. Random shuffling of tokens within sequences, standard in many language model training pipelines for deduplication purposes, is harmful here because it destroys the local context structure that the inner loop is trying to adapt to.

![](https://substackcdn.com/image/fetch/$s_!CReF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7f4e7995-c80b-484e-b71f-8052cc7773f7_2720x1293.png)

**Cross-sequence curriculum is beneficial.** At the sequence level, there is evidence that presenting simpler, more internally coherent sequences early in training helps gΘ learn a stable update rule before being asked to handle difficult, rapidly-shifting contexts. Once gΘ has learned the basic mechanics of a useful update rule on easier material, it generalizes more reliably to harder sequences where the inner loop has to navigate more complex adaptation trajectories.

![](https://substackcdn.com/image/fetch/$s_!eKoD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a3f7321-7424-4ffe-bb62-52faf63bdc37_2720x1000.png)

The interaction between data ordering and inner loop behavior is one of the less well-understood aspects of this training paradigm, and it represents one of the open engineering questions that differentiates training Hope from training a standard transformer at scale.

### 7.5 Inference-Time Optimization

The self-modifying mechanism described in 7.3 is theoretically clean, but it carries a practical cost that has to be confronted directly: running a gradient update inside every forward pass is expensive, and if that cost is not managed carefully, the latency overhead makes Hope undeployable regardless of how good its memory system is.

This section is about how the paper brings that cost down to a level that is practical at inference time, what approximations are made to get there, and what the residual overhead looks like relative to a standard transformer.

#### 7.5.1 The Raw Cost of an Inner Update

Before discussing approximations, it is worth being precise about what the inner loop update actually costs in its full, unapproximated form.

At each token xt, the full inner update requires three things: a forward pass through the inner parameters ϕt to compute f <sub>ϕt</sub> (xt), a backward pass through ϕt to compute the gradient ∇ϕ <sub>L</sub> inner(ϕt;xt), and a forward pass through the learned update rule gΘ to compute the parameter update Δϕt.

For a standard transformer forward pass with L layers and hidden dimension dd d, the cost is O(Ld <sup>2</sup>) per token. The full inner update, because it requires an additional backward pass through ϕ and a forward pass through gΘ, adds a constant multiple of this cost per token, so the total per-token cost is O(cLd <sup>2</sup>) for some c>1 that depends on the size of gΘ.

For large d and deep gΘ, this multiplier becomes prohibitive. A model that is 3 times more expensive per token than a standard transformer is not a practical inference system, regardless of its quality. The inference-time optimizations are therefore not optional refinements but necessary conditions for Hope to be deployable at all.

#### 7.5.2 Approximating the Gradient

The most expensive component of the inner update is the backward pass to compute ∇ϕL <sub>inner</sub>. Full backpropagation through ϕ costs roughly twice the forward pass through ϕ in FLOPs and requires storing all intermediate activations, which adds memory pressure proportional to the depth of ϕ.

The paper replaces the full gradient with a lightweight approximation computed directly from the forward pass activations, without a separate backward pass. The key observation is that for the local self-supervised objective used in the inner loop, the gradient signal is dominated by the prediction error at the output layer, and the deeper gradient terms are relatively small in magnitude for well-initialized ϕ.

![](https://substackcdn.com/image/fetch/$s_!5bkl!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc75a80fe-3176-4877-8b26-f1dc1ee86069_2720x1478.png)

Formally, the full gradient is:

$$
\nabla_{\phi} \mathcal{L}_{\text{inner}} = \sum_{ℓ = 1}^{L_{\phi}} \frac{\partial \mathcal{L}_{\text{inner}}}{\partial \phi^{\left(ℓ\right)}}
$$

where the sum runs over all layers ℓ of the inner parameter network ϕ. The approximation retains only the last-layer gradient term and discards the deeper terms:

$$
\nabla_{\phi} \mathcal{L}_{\text{inner}} \approx \frac{\partial \mathcal{L}_{\text{inner}}}{\partial \phi^{\left(L_{\phi}\right)}}
$$

This is computable directly from the output activation and the prediction error, without any backward pass through the earlier layers of ϕ. The approximation loses the signal from how the prediction error propagates back through the intermediate representations, and this is the primary quality cost of the inference-time optimization. For inner parameters that have already adapted to a reasonable local context, this approximation is tight, because the early-layer gradients are small relative to the output-layer gradient. For inner parameters that are far from a good local solution, early in a new context window for example, the approximation is looser, and the inner loop converges more slowly than it would under the full gradient.

#### 7.5.3 Chunked Updates and Amortization

Even with the gradient approximation, computing an inner update at every single token is wasteful because adjacent tokens within a chunk are highly correlated. The update that ϕ would make on token t is almost identical to the update it would make on token t+1 if the two tokens carry similar information, so computing both updates independently squanders compute on a negligible difference.

Hope addresses this through chunked updates, which directly mirrors the CMS chunk structure from section 7.2. Rather than updating ϕ on every token, the inner loop accumulates a gradient estimate across a chunk of C tokens and applies a single update at the chunk boundary:

$$
\phi_{i + 1} = \phi_{i} - g_{\Theta} \left(\phi_{i} , \frac{1}{C} \sum_{t = i C}^{\left(i + 1\right) C} \nabla_{\phi} \mathcal{L}_{\text{inner}} \left(\phi_{i} ; x_{t}\right)\right)
$$

The gradient is averaged over the chunk, which has two benefits beyond compute savings. The averaged gradient is a lower-variance estimate of the true local gradient than any single token’s gradient, so the update is more stable. Additionally, averaging across a chunk means the update reflects the aggregate local context rather than any single token’s idiosyncratic signal, which makes ϕ more robust to individual noisy or uninformative tokens.

The amortized cost per token of the inner update is now 1/C of the per-token cost, since one update is shared across C tokens. For a chunk size of C=64, the overhead of the inner loop drops to less than 2% of the total forward pass cost per token, which is negligible in practice.

#### 7.5.4 KV Cache Compatibility

A practical concern that is easy to overlook is how inner loop updates interact with the KV cache, the mechanism that makes autoregressive generation efficient by storing past keys and values to avoid recomputing attention over the full context at every step.

In a standard transformer, the KV cache is valid indefinitely because the attention weights are frozen. In Hope, the inner parameters ϕ change at each chunk boundary, so any KV cache entries computed under the old ϕ are no longer exactly valid under the new ϕ.

The paper handles this with a partial cache invalidation strategy. At each chunk boundary, only the KV entries corresponding to the most recent chunk are recomputed under the updated ϕ. Older KV entries, from chunks far back in the context, are retained without recomputation. The justification is that the inner update at chunk ii i represents a small perturbation to ϕ, so the keys and values computed under ϕ <sub>i−1</sub> are close to what ϕ <sub>i</sub> would compute for the same tokens, and the approximation error is bounded by the magnitude of the inner update, which is already constrained by the clipping from section 7.4.3.

![](https://substackcdn.com/image/fetch/$s_!FVRl!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e79e267-bbb9-40f5-9d04-a750e9a4d998_2720x1248.png)

This selective cache invalidation means the KV cache overhead of Hope is slightly larger than that of a standard transformer (because recent entries are periodically recomputed) but not dramatically so, since the cost is amortized across the chunk size C and the recomputed entries are only the most recent C tokens.

#### 7.5.5 Net Overhead Relative to a Standard Transformer

With all three optimizations in place (gradient approximation, chunked updates, and selective cache invalidation), the per-token inference cost of Hope relative to a standard transformer at equivalent parameter count can be summarized as follows:

![](https://substackcdn.com/image/fetch/$s_!ABwY!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdeae5c48-d3b9-48a6-9cf3-c3a85c73542b_2178x544.png)

The 10-15% overhead figure assumes a moderately sized gΘ and a chunk size of 64. Larger chunk sizes reduce the overhead further at the cost of slower inner loop adaptation. Smaller chunk sizes increase the overhead but make ϕ more responsive to rapid context shifts.

The memory overhead is more significant than the compute overhead. Storing ϕ separately from Θ doubles the parameter count of the self-modifying module, and keeping the chunk gradient accumulation buffer in VRAM adds memory proportional to the chunk size and the inner parameter dimension. In practice, the total memory footprint of Hope is roughly 20-25% larger than a standard transformer at the same layer count and hidden dimension, with most of the excess coming from the dual parameter representation rather than the gradient buffers.

### 7.6 Muon and the Multi-Scale Momentum Optimizer (M3)

The methodology sections so far have focused on what the model learns and how it stores that learning like the CMS, the SMLM, the nested update structure; but, there is a fourth piece that sits underneath all of this and is easy to overlook: what optimizer is actually running the outer loop? The paper argues that the standard answer: Adam is not just suboptimal but structurally mismatched with the Nested Learning paradigm. This is where ***Muon*** enters.

#### 7.6.1 What is Muon?

Muon stands for [Momentum Orthogonalized by Newton-Schulz](https://arxiv.org/abs/2601.19156). It is an optimizer designed specifically for the 2D weight matrices of neural network hidden layers, and its core idea is deceptively simple: take the momentum gradient update that SGD-momentum would normally apply, and replace it with the nearest semi-orthogonal matrix to that update before applying it to the weights.

Formally, given a weight matrix gradient G∈R <sub>n×m</sub> with singular value decomposition G=USV <sup>⊤</sup>, the Muon update replaces G with:

$$
\text{Ortho} \left(G\right) = U V^{\top}
$$

The singular values in S which encode the magnitude of the gradient in each direction are discarded entirely. What remains is only the directional information: which directions in weight space the gradient is pointing, stripped of any scale differences between them.

This is computed not via full SVD, which is prohibitively slow, but via a Newton-Schulz matrix iteration that converges to UV <sup>⊤</sup> in just 5 steps and can be run stably in bfloat16:

$$
G^{'} = a G + b \left(G G^{\top}\right) G + c \left(\right. G G^{\top} \left.\right)^{2} G
$$

where the coefficients (a,b,c)=(3.4445,−4.7750,2.0315) are tuned to maximize convergence speed. Each application of this quintic polynomial pushes the singular values of G′ closer to 1, and after 5 iterations the result is within a small tolerance of true orthogonalization. The FLOP overhead relative to standard training is at most Tm/B where T=5 is the number of Newton-Schulz steps, m is the model dimension, and B is the batch size in tokens in practice under 1% for typical LLM training scenarios.

#### 7.6.2 Why Standard Optimizers Fall Short

To understand why Muon matters for Nested Learning specifically, you need to understand what the paper argues is wrong with Adam as a gradient compressor.

Recall from section 7.1 that NL frames gradient-based optimizers as associative memory modules, compressing a context flow (the gradient history) into a fixed representation (the optimizer state). Adam does this compression through two running statistics: the first moment mtm\_t mt (a weighted average of past gradients) and the second moment v <sub>t</sub> (a weighted average of past squared gradients):

$$
m_{t} = \beta_{1} m_{t - 1} + \left(1 - \beta_{1}\right) g_{t} v_{t} = \beta_{2} v_{t - 1} + \left(1 - \beta_{2}\right) g_{t}^{2}
$$

$$
\theta_{t + 1} = \theta_{t} - \eta \frac{m_{t}}{\sqrt{v_{t}} + \epsilon}
$$

The second moment term v <sub>t</sub> acts as a per-coordinate scaling as it divides each gradient component by an estimate of its typical magnitude. This is beneficial when gradient components have very different scales, which is common in embedding layers and output heads. However, for the hidden 2D weight matrices of a transformer, the paper argues this coordinate-wise scaling is actively harmful. The gradient matrices for these layers typically have very high condition number as they are nearly low-rank, with most of the gradient signal dominated by a small number of directions. Adam’s coordinate-wise scaling does nothing to address this structural problem. It scales each entry independently, without any awareness of the matrix structure of the parameter it is updating.

The result is that the effective update applied by Adam to a 2D weight matrix is dominated by the same few high-singular-value directions in every step, with the rare but important directions; as the ones corresponding to small singular values consistently underweighted (mostly). The model learns the dominant directions fast and the rare directions slowly, regardless of how important those rare directions might be.

Orthogonalization fixes this by definition. By replacing G with UV <sup>⊤</sup>, Muon equalizes all singular values to 1; hence every direction in weight space receives an update of equal magnitude, regardless of how large or small the corresponding gradient component was. Rare directions are no longer suppressed by the dominance of the common ones.

#### 7.6.3 How Muon Connects to the NL Paradigm

The connection to Nested Learning is direct. In the NL framing, every optimizer is a memory module compressing gradient context into a parameter update. The question is which compression is optimal for which context flow.

The paper makes a specific argument: for the 2D hidden weight matrices, the relevant context flow is a sequence of gradient matrices with high condition number and near-low-rank structure. The optimal compression of this context flow, under a spectral norm objective rather than the element-wise L2 objective that motivates Adam, is precisely the orthogonalized gradient. Adam is the optimal associative memory for element-wise L2 regression on gradient vectors. Muon is the better-suited memory for the matrix-structured gradient context of hidden layers.

This is not just a philosophical point. It means that different components of the network should be optimized by different optimizers, chosen based on the structure of their gradient context flows like the corresponding embedding layers and output heads, whose gradients don’t have the same near-low-rank matrix structure, continue to use Adam. Only the hidden 2D weight matrices switch to Muon. The optimizer is no longer a single global choice but a per-component decision made on the basis of what each component’s gradient context looks like.

#### 7.6.4 M3: Multi-Scale Momentum Muon

The paper’s own contribution on top of Muon is the Multi-Scale Momentum Muon optimizer, abbreviated as M3. The motivation follows directly from the CMS design in section 7.2. If CMS showed that memory systems benefit from operating at multiple timescales simultaneously, the same logic applies to the gradient compressor which is the optimizer.

Standard Muon maintains a single momentum term at a single timescale:

$$
m_{t} = \beta m_{t - 1} + \left(1 - \beta\right) g_{t} \theta_{t + 1} = \theta_{t} - \eta \cdot \text{Ortho} \left(m_{t}\right)
$$

M3 replaces this with a chain of momentum terms at different decay rates, mirroring the CMS chain structure:

$$
m_{t}^{\left(k\right)} = \beta_{k} m_{t - 1}^{\left(k\right)} + \left(1 - \beta_{k}\right) g_{t} k = 1 , 2 , \ldots , K
$$

$$
\theta_{t + 1} = \theta_{t} - \eta \cdot \text{Ortho} \left(\sum_{k = 1}^{K} \alpha_{k} m_{t}^{\left(k\right)}\right)
$$

where each momentum term (β1>β2>⋯>βK) has a different decay rate, compressing gradient history over a different timescale. The fast momentum terms (βk close to 0) respond quickly to recent gradients. The slow momentum terms (βk close to 1) compress a long history of gradient information, encoding stable long-run directional structure. The final update is a weighted combination of all timescales, orthogonalized before being applied.

![](https://substackcdn.com/image/fetch/$s_!yro6!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c987331-91dc-4311-8b15-83ac973cbd37_606x616.png)

The intuition is the same as CMS: no single timescale captures everything. A single β=0.9 momentum term compresses roughly the last 10 gradient steps. It loses information from step 100 and ignores information from step 2. M3 runs multiple compressors simultaneously and combines them, letting the optimizer retain signal from multiple depths of gradient history without having to choose a single window.

#### 7.6.5 Where M3 Sits in the Full Hope Architecture

In the complete Hope architecture, the three optimization components map onto three distinct levels of the NL hierarchy:

- The **inner loop** (the SMLM update rule gΘ) handles inference-time adaptation, running at the fastest timescale and updating on every chunk.
- The **CMS chain** handles multi-timescale memory storage, updating at intermediate frequencies across the sequence.
- **M3** handles outer loop training, running at the slowest timescale and compressing gradient history across the full training run into stable weight updates

![](https://substackcdn.com/image/fetch/$s_!jZ1p!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F00f12766-fed7-4a83-aa29-4c239213450b_2720x1760.png)

Each level compresses its own context flow at its own frequency. M3 is the outermost and slowest level (as we saw abaove) the one responsible for the kind of long-run structural learning that persists across training. Its multi-momentum design ensures that this compression is as expressive as possible, retaining signal from multiple depths of gradient history rather than collapsing everything into a single exponential moving average.

---

## 8\. Results and Outcomes

The paper evaluates Hope across four task categories: language modeling, common-sense reasoning, long-context reasoning, and formal language recognition.

![](https://substackcdn.com/image/fetch/$s_!PG2u!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F82a2bb7e-bf87-47e1-87b1-594d5a75650f_1647x487.png)

Baselines include Transformer++, RetNet, DeltaNet, Samba, Mamba2, TTT, and the original Titans, evaluated at 340M, 760M, and 1.3B parameter scales, all trained on 30B to 100B tokens from The Pile.

#### 8.1 Language Modeling and Common-Sense Reasoning

At the 1.3B parameter scale, Hope achieves the highest average accuracy of 57.23% on reasoning tasks and the lowest perplexity of 15.11 on the Wiki benchmark, outperforming Transformer++, RetNet, DeltaNet, and the original Titans.

![](https://substackcdn.com/image/fetch/$s_!mCgY!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7f093a57-8043-47e2-9904-8a4c26cd91ec_972x432.png)

Across language modeling and common-sense reasoning tasks, Hope demonstrates lower perplexity and higher accuracy compared to modern recurrent models and standard transformers. The margin over Titans is meaningful because Titans already represented the state of the art among memory-augmented sequence models, so Hope’s improvement is not against a weak baseline.

![](https://substackcdn.com/image/fetch/$s_!-J2o!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9910ab2e-7729-4fc8-91a4-f1df00415f7b_970x287.png)

The gain comes specifically from two places: the self-modifying update rule adapts the inner parameters to the local context more expressively than Titans’ fixed surprise signal, and the CMS chain provides multi-timescale memory that recovers information at longer ranges than Titans’ single long-term memory module.

#### 8.2 Long-Context Reasoning

Hope showcases superior memory management in long-context Needle-In-Haystack (NIAH) downstream tasks, proving that the CMS offers a more efficient and effective way to handle extended sequences of information, outperforming Titans, TTT, and Mamba2.

![](https://substackcdn.com/image/fetch/$s_!xavp!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffcf9eb36-95d7-41e2-b1c6-c4adb27465d9_749x653.png)

NIAH is a particularly diagnostic benchmark for a continuously-learning memory system because it requires retrieving a specific piece of information planted early in a very long context, after processing a large amount of intervening noise. Standard transformers fail here because the relevant token falls outside the attention window.

![](https://substackcdn.com/image/fetch/$s_!NdsJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc5cbb94b-52eb-4679-9d4f-bb567e30f90d_436x397.png)

RAG-based systems can fail when the retriever doesn’t surface the right document. Hope’s CMS chain handles it by encoding the planted fact into a slow-frequency block whose chunk window is large enough to span the distance between the fact and the query.

#### 8.3 Formal Language Recognition

Hope achieves perfect accuracy on formal language recognition tasks where standard transformers fail, leveraging non-parallelizable computation enabled by its nested recurrent structure.

![](https://substackcdn.com/image/fetch/$s_!b6Qm!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F77e395a8-ca92-42ea-904f-3c9967801d79_1251x395.png)

Formal language recognition is a stress test for computational depth rather than memory capacity. Certain formal languages, particularly those requiring counting or stack-based operations, cannot be recognized by a standard transformer because the attention mechanism’s parallelism prevents the kind of sequential state accumulation these tasks need. Hope’s nested recurrent structure, where the inner loop updates ϕ sequentially across each chunk, provides exactly the kind of iterative computation that transformers structurally cannot perform.

#### 8.4 Muon and M3: Optimizer Benchmarks

The paper evaluates M3 against AdamW and Muon on two axes: quality and training cost.

M3 consistently occupies the bottom-left quadrant; i.e. lower train loss and lower test loss simultaneously across multiple hyperparameter configurations. AdamW clusters further right and higher, indicating both worse generalization and worse training fit. Standard Muon sits between the two, better than AdamW but consistently outperformed by M3. The shaded pink region marks the Pareto-optimal zone; M3 configurations dominate it almost entirely across both the smaller and larger model scales shown.

![](https://substackcdn.com/image/fetch/$s_!gZM8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcda3679d-1f58-4cd7-8cea-1c4840ec3a73_1031x499.png)

When evaluating at scale; for 140M parameters M3 takes roughly 43 hours versus 38 hours for Muon and 41 hours for AdaMuon. At 1.3B parameters, M3 takes roughly 79 hours versus 70 hours for Muon and 75 hours for AdaMuon. The overhead is real but modest as it is approximately 10 to 15% above standard Muon and consistent with the theoretical estimate from section 7.5 that the multi-momentum bookkeeping adds bounded cost proportional to the number of momentum terms K.

![](https://substackcdn.com/image/fetch/$s_!Crtv!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e96202d-165b-41aa-9d9c-7f6d603d7243_549x499.png)

The quality gain from Figure 11 outweighs the cost overhead from Figure 12 by a meaningful margin, which is the paper’s central argument for M3 as the right outer loop optimizer for Hope.

---

## 9\. Thoughts

The Nested Learning paradigm is genuinely ambitious, and Hope validates it as a proof of concept. But several questions sit underneath the benchmark numbers that deserve honest examination.

- **No comparison against a strong RAG baseline:** Hope was not evaluated head-to-head against a strong RAG baseline on knowledge incorporation tasks. NIAH is a synthetic retrieval benchmark where the needle is planted deliberately. A real-world retrieval task with a well-tuned RAG system could tell a very different story, and the absence of that comparison leaves the paper’s central motivation empirically unresolved.
- **The data ordering tax is a hidden deployment cost:** Standard LLM training pipelines shuffle aggressively, deduplicate across document boundaries, and mix domains without regard for within-sequence coherence. Hope’s inner loop depends on that coherence to produce useful chunk-level updates. This is not a minor engineering note. It means adopting Hope at scale requires rethinking the data pipeline from the ground up, an invisible cost the benchmark numbers do not reflect.
- **The chunk size selection problem has no principled answer right now:** The CMS design shows that more frequency levels help, but the paper does not give a method for choosing the chunk size schedule. At 1.3B parameters with a small fixed set of chunk sizes, this is manageable. At 10B or 70B, with longer contexts and more diverse data distributions, the wrong frequency schedule could waste most of the multi-timescale benefit. This feels like the kind of hyperparameter that will require its own line of research before CMS is reliably deployable.
- **M3 is the most immediately usable contribution:** Unlike Hope, which requires rearchitecting the full model and training pipeline, M3 can be dropped into any existing training setup as a replacement for Adam on hidden layer parameters. The overhead is bounded and predictable, the quality gains are consistent across scales, and it requires no changes to inference. The community will likely adopt M3 independently of whether Hope itself gains traction, and the paper somewhat undersells this.
- **The inner loop overhead scaling is uncharacterized beyond 1.3B.** The 10 to 15% per-token overhead estimate from section 7.5 holds under specific assumptions about chunk size and model dimension. At larger scales, the interaction between growing model dimension, longer contexts, and the chunked update approximations introduces compounding factors that have not been studied. It is plausible that the overhead remains bounded, but it is equally plausible that it grows in ways the current analysis does not capture.
- **The most profound implication is what NL says about the design space.** If optimizers, architectures, and learning algorithms are all instances of the same underlying operation, then the field has been exploring a very small corner of what is possible. We have been treating the model and the thing that trains the model as categorically separate objects. Nested Learning dissolves that boundary. Hope is a first-order approximation of what emerges when you take that dissolution seriously. The more interesting architectures are the ones that come after it.

---

## 10\. Conclusion

Nested Learning reframes the entire machinery of deep learning, not as a stack of layers trained by an external optimizer, but as a coherent system of nested optimization problems, each compressing its own context flow at its own frequency. Through this lens, the boundary between architecture and optimizer dissolves, the boundary between training and inference softens, and the design space for future models expands in a dimension the field has barely begun to explore.

In this article, we started by establishing why current models are structurally amnesiac as their knowledge is confined to either the immediate context window or the frozen weights of pretraining, and every mechanism built to work around this, from RAG to fine-tuning to in-context learning, is a patch on top of a system that was never designed to keep learning. We grounded the difficulty of the problem in the plasticity-stability tradeoff and the catastrophic forgetting problem, showing why continuous learning is not just an engineering challenge but a structural one.

We then built up the Nested Learning paradigm from first principles, revisiting the Titans architecture that first showed inference-time learning was possible, and tracing how Hope extends that foundation into a full multi-timescale system. We explored the Continuum Memory System, which replaces the binary long/short-term memory split with a spectrum of frequency levels each responsible for its own timescale of knowledge. We examined the Self-Modifying Titans module, whose inner loop learns not just what to update but how to update, making the adaptation mechanism itself a product of optimization. We introduced M3, which brings the same multi-timescale philosophy to the optimizer, replacing Adam’s single exponential average with a chain of momentum terms that compress gradient history at multiple depths simultaneously.

The key takeaway is that the static nature of current language models is not a fundamental constraint of the architecture class. It is a consequence of treating the model and its training procedure as two separate objects, one that learns and one that is learned. When you recognize them as the same kind of thing operating at different frequencies, a new design axis opens up. Hope is the first architecture to seriously inhabit that axis.

We are not yet at a model that learns the way a person does, continuously, selectively, without forgetting, weaving new knowledge into the substrate of old reasoning rather than retrieving it from an external store. But Nested Learning tells us what the path toward that model looks like. The question is no longer whether inference-time learning is possible. The question is how deep the nesting can go; this changes the entire framework and space on which we optimnize.

Paper: [https://arxiv.org/pdf/2512.24695](https://arxiv.org/pdf/2512.24695)

That’s all for today.  
  
Follow me on [LinkedIn](https://www.linkedin.com/in/siddhant-rai/) and Substack for more such posts and recommendations, till then happy Learning. Bye👋