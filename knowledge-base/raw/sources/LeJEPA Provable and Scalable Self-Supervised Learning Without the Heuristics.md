---
title: "LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics"
source: "https://vizuara.substack.com/p/lejepa-provable-and-scalable-self?utm_source=post-email-title&publication_id=3466476&post_id=214459483&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[Siddhant Rai]]"
published: 2026-09-07
created: 2026-09-07
description: "Every anti-collapse trick in SSL was found, not derived. LeJEPA asks what distribution embeddings should follow, proves there is exactly one answer, and skips the rest of the machinery."
tags:
  - "clippings"
---
## Table of contents

1. *Introduction*
2. *What a JEPA actually is*
	1. *What is a world model?*
		2. *Why predict in representation space?*
3. *Connecting probability with optimization*
4. *The heuristics zoo, and what “under-specified” really means*
5. *The Ideal Case*
6. *Methodology*
	1. *Finding Q: why the isotropic Gaussian?*
		2. *Finding D: measuring the distance to a Gaussian*
7. *SIGReg in code*
8. *Results & Outcomes*
9. *Thoughts*
10. *Conclusion*

---

## Introduction

I have been a fan of self-supervised learning for a very long time, and at this point I don’t think that qualifies as a niche taste anymore. If you look underneath almost anything that has worked in deep learning recently, you will find some version of SSL doing the actual work, and it tends to fall into one of two camps. Next-token prediction in LLMs and most of what we do with time series are learning a *temporal* world; what follows what, and how state evolves along an axis we cannot run backwards. The DINO family, masked image modelling, contrastive image-text pairs are learning a *spatial* world; what belongs with what, and how structure holds together across a scene that is all present at once. The supervision never really went away in either case, it just stopped coming from a human and started coming from the structure of the data itself. We had been writing multiple articles on SSL and respective methodologies; in case if you want to brush up some more details:

The interesting question then is no longer whether SSL works, we have more than enough evidence for that. It is what exactly we are asking a model to do when we train it this way, and among all the SSL families, JEPA has committed to the sharpest answer by deriving the model from the combination of spatial and temporal which is a video. A video is temporal structure laid over spatial structure, and if your input space is video, then the thing you are actually trying to learn is neither the layout of a frame nor the ordering of frames, but the *dynamics* that carry one into the next. The way JEPA goes after this is by predicting in **representation space** rather than in pixel space, which frees the model to discard whatever it cannot predict instead of wasting capacity reconstructing it. That single shift does most of the heavy lifting here, and it is worth unpacking properly, which we will do in the next section.

![](https://substackcdn.com/image/fetch/$s_!7uC5!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0bf6359-ff2d-4ed1-b2bf-37a0bb81d5c4_500x500.png)

There is a framing of all this that I keep coming back to, and it comes from Yann’s [lecture at NYU](https://youtu.be/8u2s64ZtmiA). SSL, in his telling, is not really a learning trick at all; it is an optimization problem with constraints, and the constraints are where the entire inductive bias of the method lives. The prediction task on its own is trivially solvable, because a model that maps every input to the same constant vector predicts perfectly and learns absolutely nothing in the process. Hence the constraint is not some detail bolted onto the objective for stability, it is closer to being the objective itself, and everything we discuss in this article follows from taking that seriously.

Which is exactly where things get uncomfortable. If the constraint is carrying all of the inductive bias, then we should have some principled theory of which constraint to use, and we simply don’t. What we have instead is an accumulated pile of mechanisms that were found empirically and kept because they happened to work; negative samples (SimCLR, MoCo), teacher–student networks with hand-tuned EMA schedules (BYOL, DINO), stop-gradients (SimSiam), feature whitening (Barlow Twins, W-MSE), and explicit variance-covariance penalties (VICReg). Every one of these prevents the model from cheating, and not one of them was derived from a statement about what the embeddings ought to look like, largely because no such statement existed to derive from.

LeJEPA is an attempt to finally write that statement down. Balestriero and LeCun ask which distribution the embeddings *should* follow in order to be useful for downstream tasks that nobody has seen yet, prove that there is exactly one such distribution, construct a penalty term that enforces it, and then delete the rest of the machinery; no stop-gradient, no teacher–student, no schedulers, one hyperparameter. The route they take to get there is genuinely lovely, involving an isotropy argument that falls straight out of plain bias-variance, a theorem that lets you read a high-dimensional distribution entirely off its one-dimensional shadows, and a statistical hypothesis test repurposed as a loss function.

As always, we will build this from the *why* forward, so that by the end the objective stops looking like a proposal someone made and starts looking like the only thing that could have been written.

*(Usual caveat: the information in this article is upper bounded by my own grasp of the topic, my patience for typing for hours, and a writing medium that still refuses to support inline LaTeX. Please re-visit everything you read here, and go read the paper.)*

---

## 2\. What a JEPA actually is?

*Let us start by understanding the claim which JEPA starts with, i.e. it being a world model.*

### 2.1 What is a world model?

The phrase gets used loosely enough to have lost most of its meaning, so let me pin down the version that matters here.

A world model is an internal representation of how things work that is good enough to run forward. Not a recording of what happened, a mechanism for anticipating what happens next. You have one. It is why you flinch before the ball hits you, why a wobbling glass makes you reach out, and why you can read half a sentence and know roughly where it is going. None of that involves retrieving a stored instance; it involves running a model of the situation slightly ahead of the situation itself.

Three properties matter, and each one turns out to be a design constraint.

1. **It predicts, so it must be usable in the forward direction.** A representation that describes the present beautifully but supports no inference about the next moment is a description, not a model. The test is always whether you can push it forward and get something useful.
2. **It is abstract, so it discards.** The version of the falling cup that lets you predict the outcome contains gravity, brittleness and height. It does not contain the reflection on the ceramic. Detail that does not affect what happens next is not merely unnecessary, it is actively in the way; a model cluttered with it is harder to run and easier to confuse.
3. **It is reusable, so it is not built per task.** The same intuitions about objects and support and momentum serve you when catching a ball, stacking dishes and judging whether a shelf will hold. You did not learn a separate model for each. That reuse is exactly what “foundation model” is meant to name; one representation, many tasks, none of them known when the representation was learned.

It is worth seeing where this sits in the larger picture, because LeCun’s proposal for autonomous machine intelligence is considerably bigger than a world model alone.

![](https://substackcdn.com/image/fetch/$s_!dsde!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcfbe933b-102e-4eba-aa94-9d79af40f6da_1200x675.png)

*LeCun’s proposed architecture for autonomous machine intelligence. The world model is one module among several.*

Reading the diagram: **perception** turns percepts into a representation of the current state. The **world model** takes that state, plus an imagined action, and predicts the state that would follow, which is what lets the system evaluate a plan without executing it. The **actor** proposes actions, the **cost** and **critic** modules score the predicted outcomes, **short-term memory** holds the trajectory being considered, and the **configurator** adjusts the other modules for whatever task is at hand.

The point I want to draw from this is a limiting one. JEPA is a proposal for how to train the green box, and nothing else. There is no actor here, no cost module, no planning loop; the architecture around it is a research programme rather than something anyone has built. So when we talk about world models in this article we mean the representation-learning half specifically, and questions about what you would do with one, planning, control, action-conditioning, are outside what LeJEPA addresses.

Which is why the paper’s framing matters. If the world model is the piece everything else depends on, then getting its representation right is not one optimization problem among many, it is the one that determines whether the rest of the architecture has anything to work with.

![](https://substackcdn.com/image/fetch/$s_!7J2t!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec237317-b1de-4e31-86ef-21b50a6d532f_1664x741.png)

*The same scene under three objectives. Only the third keeps what determines the outcome and lets the rest go.*

**Why prediction is the natural way to learn one**

Here is the part that makes this more than philosophy. If you want a model with those properties and you have no labels, prediction is the only training signal available that produces them for free.

To predict what comes next you must represent what determines what comes next. There is no shortcut; a model that ignores the causal structure cannot anticipate it. So the prediction task does not merely test the world model, it *forces* one into existence, and the pressure to be abstract comes along automatically, because carrying unpredictable detail costs capacity and buys nothing.

This is the argument for self-supervision at its strongest, and it explains why the field keeps returning to it across modalities that otherwise share nothing. Next-token prediction, next-frame prediction and masked-patch prediction are the same bet: that predicting is how you are forced to understand.

**Where JEPA fits**

JEPA is a specific and, I think, correct answer to the question of where the prediction should happen.

Everything above says predict. Nothing above says predict in pixel space, and that turns out to be the crucial degree of freedom. Reconstruct the next frame and you are graded on the reflection on the ceramic, which forces exactly the detail-hoarding that the second property said to avoid. Predict in representation space and the model is free to discard whatever it cannot anticipate, which is what the same property demanded.

So JEPA’s claim is narrow but load-bearing: **predict, but predict abstractly, and let the abstraction be learned rather than specified.** The rest of this section is what that looks like when written down.

### 2.2 The setup

The architecture itself is deliberately plain, and it helps to see it as four steps before we complicate it:

1. Take **two views** of the same underlying thing.
2. Push both through an **encoder** Enc(·), which lands them in some embedding space R^K.
3. Ask a small **predictor** Pred(·) to produce one of those embeddings from the other, where one is used at all.
4. Measure how far it missed, and backpropagate.

![JEPA: Joint Embedding Predictive Architecture Explained](https://substackcdn.com/image/fetch/$s_!Dyur!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5867b5bb-cf5c-4dfe-81f0-10fcba8aae58_1200x637.jpeg)

JEPA: Joint Embedding Predictive Architecture Explained

Everything interesting is hiding in that first step, because what counts as “two views of the same thing” is entirely up to you. If your data is video then time gives you views for free, and view one is frame *t* while view two is frame *t+1*, which means you are effectively asking the model where the world is going next. If your data is images then you have to manufacture views instead of finding them, so you take two random crops of the same photo, or a masked patch and the context around it, or the same image under two different colour jitters, and you ask the model what belongs with what. The machinery downstream is completely identical in both cases and only the view-generator changes, which is why I will mostly just say “two views” from here on and stay agnostic about where they came from.

### 2.3 Why predict in representation space?

We asserted this in 2.1 and it is worth earning properly, because the cleanest way to see it is to write the two objectives next to each other.

Reconstruction, which is what autoencoders and masked image models do, predicts back into the input space:

*L\_recon(θ) = E \[ ‖ Dec(Enc(x̃)) − x ‖² \], x ∈ R^D*

whereas JEPA predicts into the embedding space instead:

*L\_pred(θ) = E \[ ‖ Pred(Enc(x\_v)) − Enc(x\_v′) ‖² \], Enc(x) ∈ R^K*

![](https://substackcdn.com/image/fetch/$s_!lwLU!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8318feea-6584-4f7a-938a-f72bfeb4f57b_1883x1238.png)

*The same two encoders, two different places to put the target. Moving it from pixel space to representation space is the entire architectural claim.*

The difference between these two lines looks almost cosmetic, and it is anything but, because it changes three things at once.

The first is that **unpredictable detail becomes free to throw away**, which is the world-model property from 2.1 arriving as a loss function. Under reconstruction every pixel of the missing patch contributes to your loss, so the model is actively penalized for failing to predict things that are not predictable in principle; the position of each leaf on a tree, the grain of the sensor noise, the exact texture of gravel. A real fraction of model capacity ends up going into hallucinating plausible detail, which is a genuine skill but not the one you were trying to teach.

Suppose I nudge a cup off the edge of a table and ask what happens next; you will say without hesitation that it falls, hits the floor and probably breaks. What you will not do is give me the coordinates of each ceramic shard, and if I insisted you would rightly say the question is unreasonable, not because your understanding is poor but because that information does not yet exist in any form your prediction could access. Your grasp of the dynamics is excellent and your ability to reproduce the pixels is nil. Reconstruction grades you on the second; JEPA grades you on the first.

The second consequence is subtler and matters more than it first appears: **the target is no longer fixed**. In reconstruction, x is handed to you by the dataset and cannot move no matter what the optimizer does, whereas in JEPA the target Enc(x\_v′) is itself a function of θ, so both sides of the loss shift every time you take a step.

Which leads directly to the third, namely that **this is exactly where the trouble begins**. A fixed target makes collapse structurally impossible, because there is no way to cheat your way into reproducing a photograph you have never seen. A learnable target makes collapse the single easiest thing the optimizer can do, and it will find that shortcut unless you stop it. Hence JEPA needs anti-collapse machinery for a structural reason that autoencoders never had, and that is not a flaw so much as the price of the freedom we bought in the first consequence.

One aside about the predictor network, since it will come back later. Its stated job is to absorb whatever systematic difference exists between the two views before the comparison, and that is well-motivated when the views really are asymmetric in information content, for instance when you condition the prediction on an observed robot action so that there is an actual transformation to be learnt. It stands on much shakier ground when the views are symmetric, in which case it looks less like a modelling choice and more like a device for breaking an inconvenient symmetry. Hold that thought; it turns out LeJEPA does not need one at all.

### 2.4 The definition, and the crack running through it

The paper states the JEPA criterion compactly, and the shape of the statement matters as much as its content:

**Enc(x\_{t+1}) is predictable from Enc(x\_t), for all n and t, and Enc(·) is not degenerate.**

It is worth reading twice, because it is two clauses joined by an “and”, and those clauses are not remotely the same kind of object.

The first is a loss function, specifically the L\_pred we wrote above; you can put it on paper, differentiate it, and hand it to an optimizer with no ambiguity about what you are asking for. The second is an English sentence. “Not degenerate” is a property everyone agrees they want and nobody has specified, which means it has no gradient, no closed form, and nothing you can minimize, so in practice it gets silently translated into whichever mechanism happened to fix the last failure someone observed. That crack between a clause you can compute and a clause you can only gesture at is, in a very real sense, the entire subject of this article.

### 2.5 Writing the whole thing as one objective

Let us now push both clauses into a single equation, because doing that makes the missing piece impossible to ignore.

The general form of constrained optimization is something we built up from scratch in the [regularization article](https://vizuara.substack.com/p/regularization-what-why-and-how-part), and the shape of it is that you want to minimize an objective while respecting a constraint,

*min\_θ f(θ) subject to g(θ) ≤ 0*

which you then fold into a single expression by attaching the constraint to the objective through a multiplier:

*L(θ) = f(θ) + α · g(θ)*

*\[EMBED: Regularization: What? Why? and How? (Part -1)\]*

Mapping JEPA onto that gives us the skeleton that the rest of this article exists to fill in, with the predictive term playing the role of the objective and the anti-degeneracy requirement playing the role of the constraint:

*L\_JEPA(θ; X) = L\_pred(θ; X) + α · L\_constraint(θ)*

*where L\_pred is f(θ), i.e. clause one, and L\_constraint is g(θ), i.e. clause two.*

Three things fall out of this, and together they set up everything that follows.

The first is that **f is settled while g is not**, since every JEPA variant in the literature agrees almost exactly on the predictive term, and every disagreement between them, without exception, turns out to be a disagreement about g. The second is that **every existing method is really an unwritten g in disguise**, because stop-gradients, EMA teachers, whitening layers, negative samples and VICReg’s variance-covariance penalties are all mechanisms that behave like constraints without ever having been stated as one, and several of them are not even in the loss at all but are instead surgery performed directly on the gradient flow. The third is that **α cannot exist until g does**, which is worth noticing because a single principled trade-off parameter is only available to you once the thing being traded off has an actual form; if your constraint is a collection of architectural interventions then there is nothing to put a coefficient on, and you are left tuning schedules instead.

All of which lets us state the paper’s contribution in one line, before we have looked at a single piece of its machinery: **LeJEPA is a specific, derived choice of g**, and everything from Section 6 onwards is the derivation of it.

### 2.6 What “degenerate” actually looks like

Since g exists to prevent degeneracy, we should be concrete about what it is preventing, and there are two versions of the failure with the second being considerably more dangerous than the first.

**Complete collapse** is the blunt version, where the encoder simply maps every input to the same constant vector:

*Enc(x) = c ∀x ⟹ L\_pred(θ) = 0*

Both embeddings are then identical, the predictor happily learns the identity function, the loss drops to zero, and the model has learnt precisely nothing. This is the failure mode we flagged in the introduction and it is the easy one to deal with, because it is loud in the loss curve and obvious the moment you look at the embeddings.

**Dimensional collapse** is the version that actually ruins your week. Here the encoder does not push everything to a single point, but it does confine everything to a low-dimensional subspace of the embedding space, so that if we write Σ = Cov(Enc(x)) with eigenvalues λ₁ ≥ … ≥ λ\_K, what we observe is

*λ\_k ≈ 0 for all k > r, where r ≪ K*

meaning your representation is nominally 1024-dimensional while the model is genuinely using perhaps thirty of those directions and the remaining several hundred carry essentially no variance at all. What makes this so much worse than complete collapse is that nothing in your training run will tell you it is happening; the prediction loss looks entirely healthy, distinct views really are being mapped to distinguishable embeddings, the model genuinely is solving the task you set it, and you typically discover the problem much later when a linear probe underperforms for reasons you cannot localize to anything in particular.

It is also worth noticing that this is not a binary condition in the way complete collapse is. Dimensional collapse is a spectrum, every trained model sits somewhere along it, and the honest question is never whether your model has collapsed but rather how much of the embedding space you paid for is doing real work. Which hands us a considerably sharper question than the vague one we started this section with, because if what we actually care about is how variance gets distributed across the directions of the embedding space, then the thing we should be asking is: **what is the right distribution of variance across those directions?**

Hold onto that, because it turns out to have a precise answer, and pinning that answer down is the whole of Section 6.

---

## 3\. Connecting probability with optimization

We closed the last section with an objective of the form f(θ) + α·g(θ), and I asked you to take on trust that this is the natural shape for a JEPA to take. That was slightly unfair, because written that way the constraint term looks like something we bolted on because we needed it. So before we go hunting for the right g, it is worth showing that this shape is not a convenience at all; it drops out of probability theory on its own, and once you see where it comes from, the presence of a constraint term stops being a design decision and becomes something you could not avoid even if you wanted to.

### 3.1 Starting from Bayes

Start from the most familiar statement in probability:

*P(A | B) = P(B | A) · P(A) / P(B)*

Nothing controversial here, it is a rearrangement of the definition of conditional probability, and A and B are just labels. That last part matters more than it usually gets credit for, because it means we get to decide what goes in those slots depending on what we are actually trying to learn.

In our setting there are two objects in play; the data X that we observed, and the parameters θ of the model we are fitting. Putting those in gives us

*P(θ | X) = P(X | θ) · P(θ) / P(X)*

and each piece here has a job. P(θ|X) is the posterior, the thing we are trying to maximize, and it asks how plausible a particular set of parameters is given the data we have. P(X|θ) is the likelihood, which asks how probable our observed data would be under a given setting of the parameters. P(θ) is the prior over parameters, what we believed about reasonable models before seeing anything. And P(X) is the evidence, which is a normalization term.

We can drop the evidence immediately, and it is worth being precise about why. P(X) does not contain θ anywhere, so its gradient with respect to θ is exactly zero, which means it shifts the value of the objective without ever changing where the optimum sits. It is not being neglected as small, it genuinely has no say in the answer.

### 3.2 Taking logs

The remaining expression is a product, which is awkward to optimize; gradients through products get messy and probabilities underflow the moment you multiply enough of them together. Since log is monotonic, whatever maximizes a quantity also maximizes its log, so we lose nothing by taking logs and gain a sum:

*log P(θ | X) = log P(X | θ) + log P(θ)*

And there it is. The objective we want, on the left, is the sum of a fit term and a prior term, and nobody put that second term there deliberately; it fell out of Bayes and there is no version of this equation that does not contain it.

That second term is one you have used your whole career, usually without calling it a prior. Put a Gaussian prior on the weights and −log P(θ) becomes a squared penalty on their magnitude, which is weight decay. Put a Laplace prior on them and you get L1. The entire discussion we had in the [regularization article](https://vizuara.substack.com/p/regularization-what-why-and-how-part) about penalizing large weights and constraining model complexity was, underneath the geometry, an argument about how to choose P(θ).

### 3.3 Where LeCun’s framing changes the picture

So far this is standard, and it gets us a constraint on the *parameters*. But the thing we care about in self-supervised learning is not really the weights, it is the representation, and this is where LeCun’s way of setting the problem up becomes useful.

The move is to stop treating the representation as an intermediate quantity that happens to appear inside the network, and start treating it as part of what we are inferring. Instead of asking about θ alone, we ask about the pair:

*P(\[θ, Z\] | X) = P(X | \[θ, Z\]) · P(\[θ, Z\]) / P(X)*

Same equation, same evidence term dropping out for the same reason, same logs:

*log P(\[θ, Z\] | X) = log P(X | \[θ, Z\]) + log P(\[θ, Z\])*

I should be upfront that there is a modelling stance hidden in this substitution rather than a derivation. In a JEPA the encoder is deterministic, so Z = Enc(X; θ) is fully determined once you fix θ and X, and treating Z as something to be inferred alongside θ is a choice we are making rather than something the mathematics forces on us. But it is the right choice, and it is more or less the whole of LeCun’s position; the representation is the object of interest and the weights are merely how we happen to parameterize it. If that is what you believe, then the representation belongs in the objective, and Bayes has no objection to putting it there.

Now flip the sign, so that we are minimizing a loss like everywhere else in this article rather than maximizing a probability. Negating the log posterior gives us

*−log P(\[θ, Z\] | X) = −log P(X | \[θ, Z\]) − log P(\[θ, Z\]) + log P(X)*

and since log P(X) contains neither θ nor Z, it shifts the value without moving the optimum, so it survives in the equation but disappears from the minimization:

*argmin over (θ, Z) of \[ −log P(\[θ, Z\] | X) \] = argmin over (θ, Z) of \[ −log P(X | \[θ, Z\]) − log P(\[θ, Z\]) \]*

*where the first term is f(·), the fit, and the second is g(·), the prior.*

Finally we attach a coefficient, because in practice we do not want the fit and the prior weighted equally. This last step deserves an honest label, since the moment α appears we are no longer computing a posterior and the equality would be a lie; what we are doing is *defining* a training objective that is inspired by one:

*L(θ, Z; X) ≜ −log P(X | \[θ, Z\]) + α · ( −log P(\[θ, Z\]) )*

*with the semicolon separating what we optimize over, θ and Z, from what the loss is conditioned on, X.*

*min over (θ, Z) of L(θ, Z; X)*

which is exactly the f + αg we wrote down at the end of Section 2, now arrived at rather than asserted. Setting α to one recovers exact Bayesian inference; anything else is a deliberate statement about how seriously we take the prior relative to the data, and that knob is the same Lagrange multiplier that appeared in the regularization article when a hard threshold got softened into a penalty.

### 3.4 What lives inside the joint prior

The interesting term is P(\[θ, Z\]), and the reason it is interesting is that it is a joint prior over both objects at once. It is not a prior on weights with a representation term stapled on; it is a single statement of belief about what a good (parameters, representation) pair looks like, and that gives us more room than we are used to having.

There are three kinds of belief you can express in there.

![](https://substackcdn.com/image/fetch/$s_!w79z!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F35c86bac-43c2-4052-ac7e-de4d295584ee_1678x606.png)

*The joint prior gives three distinct places to put a belief. Almost all classical work sits in the leftmost panel; every SSL constraint we are about to look at sits in the middle one.*

You can place belief **on θ alone**, which is classical regularization and is what almost all of the literature has historically done. Weight decay, L1, spectral norms, anything that says a good model has small or well-behaved parameters. This constrains the machine.

You can place belief **on Z alone**, which is far less explored and is where this entire article is heading. Statements like “the representation should not collapse”, “the representation should use its dimensions evenly”, “the representation should follow some particular distribution”. This constrains what the machine produces, which is a genuinely different thing to constrain.

Or you can place belief **on the coupling between them**, which is the part that only exists because we kept the prior joint. Anything that says a certain kind of representation should only arise from a certain kind of parameterization lives here, and it is largely unexplored territory.

One detail about the Z part is worth pausing on, because it explains something that confuses people the first time they implement any of this. A belief about the representation is almost never a belief about an individual embedding vector; it is a belief about the *distribution* of embeddings that the encoder induces across the data. Collapse is not a property any single vector can have. A lone embedding sitting at the origin is unremarkable, and it is only when every embedding sits at the origin that anything has gone wrong. Hence any term in this slot has to be computed over a population rather than per-sample, which is precisely why every anti-collapse mechanism in the literature operates on a batch and why none of them can be written as a per-example loss.

![](https://substackcdn.com/image/fetch/$s_!nS1A!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F896b7dba-ee0b-4df2-9502-c7a534dd2b58_1664x586.png)

*The orange point is the same embedding in all three panels. Nothing about it tells you whether the representation has collapsed; only the cloud around it does.*

### 3.5 Why the constraint carries the inductive bias

Now Yann’s framing from the introduction stops being a slogan and becomes something you can point at in the equation.

Recall from Section 2 that the fit term is trivially satisfiable. A constant encoder drives the predictive loss to zero and learns nothing, which in the language we have just built means f(·) does not determine the solution; there is an enormous family of (θ, Z) that optimize it perfectly and they differ wildly in how useful they are. The fit term tells you which solutions are *admissible*. It says nothing about which one you should end up at.

The prior term is what chooses. Which means whatever you put in that slot is not a safety mechanism protecting your training run, it is the thing that decides what your model actually learns. Two JEPAs with identical predictive losses and different priors are not two implementations of one idea with different stability characteristics; they are different learning algorithms that will converge to genuinely different representations.

That is an uncomfortable thought when you set it next to the list from the introduction, because none of those methods wrote their prior down. Stop-gradients, EMA teachers, whitening layers, negative samples, variance-covariance penalties; every one of them is an attempt to express a belief about Z without ever stating what that belief is, and several of them are not even in the loss but are instead surgery performed directly on the gradient flow. We have been choosing the most important part of the objective by trial and error, and then describing the result as a stability trick.

That is the gap LeJEPA walks into. Its claim is that the Z part of this prior has a correct form, that the form can be derived rather than guessed, and that once written down properly it makes every mechanism that was approximating it unnecessary. The next two sections look at what those mechanisms actually are and where each one falls short, and then we can go looking for the answer.

---

## 4\. The heuristics zoo, and what “under-specified” really means

We now have a slot in the objective that needs filling, and we have the observation that every existing method is filling it without saying so. It is worth going through those methods properly, not to catalogue them but to ask the same question of each one; what belief about Z is this mechanism trying to express, and where does the expression fall short? Because the pattern that emerges is remarkably consistent, and it is what tells us what we should be asking for in the first place.

Most of these mechanisms we have met before, since I went through the contrastive, clustering and distillation families in some detail in the [SSL primer](https://vizuara.substack.com/p/a-primer-on-self-supervised-learning); what I want to do here is different, which is to re-read each of them through the lens we just built and ask what belief each one is really trying to express.

It helps to keep the base form from the last section in view while we do this, because every method below is an answer to the question of what g should be, and a few of the answers turn out to be that there isn’t one:

*L(θ, Z; X) = f(θ, Z; X) + α · g(θ, Z), where g(θ, Z) = −log P(\[θ, Z\])*

### 4.1 Two perspective of SSL tasks

Before going mechanism by mechanism, it is worth borrowing the taxonomy LeCun uses in the same lecture series, because it explains why the zoo has the shape it does rather than being an arbitrary collection of tricks.

The framing is energy-based. Define some scalar E(x) that is low for configurations the model considers plausible and high for the ones it does not; for our purposes E measures how compatible two views are under the current encoder, so low energy means “these belong together”. Training then has exactly one job, which is to push energy down on the data.

And here is the difficulty that generates everything else. Pushing energy down on the data is trivially easy. A model that assigns low energy to *everything* achieves it perfectly, and that is the same statement as collapse written in a different notation; a flat energy surface and a constant encoder are the same failure. So the entire problem of self-supervised learning is not making energy low where it should be, it is making energy **high everywhere else**.

There are exactly two ways to do that, and every method we are about to look at is one or the other.

![](https://substackcdn.com/image/fetch/$s_!6UB9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc64aa0c1-9317-4dbd-ad11-bc6536c6981f_1766x761.png)

*Orange points are the data. Both families end up with energy that is high away from the data; they differ entirely in how they get there.*

**Contrastive methods push the energy up explicitly.** You pick some points, you increase their energy, and the surface acquires shape because you carved it. The variants differ only in how the points get chosen; you can push up *everywhere* at once, which is maximum likelihood and which needs either a tractable partition function or a variational approximation because “everywhere” is an integral over the whole space. You can push up at *chosen locations*, which covers most of what we actually use, including metric learning and siamese networks, noise contrastive estimation, contrastive divergence, and, viewed from the right angle, the discriminator in a GAN. Or you can train a function that *maps off-manifold points back onto the manifold*, which is what denoising autoencoders do and what masked models like BERT do, where the corrupted input is the high-energy point and the reconstruction is the push back down.

**Regularized and architectural methods limit the volume of low-energy space instead.** Nobody is pushed up anywhere. Instead you arrange matters so that there is only so much low energy to go around, and the model is forced to spend it where the data actually is. These come in variants too. You can build the machine so the low-energy region is *bounded by construction*; PCA has a fixed number of components, K-means a fixed number of centroids, a normalizing flow is volume-preserving by design, and in none of these is there a term in the loss doing the work, since the architecture simply makes the failure unreachable. You can add a *regularization term that measures the volume of low-energy space* and penalizes it, which is sparse coding, sparse autoencoders, VAEs with their KL term, and VQ-VAE with its finite codebook. You can make the output as *insensitive as possible* to the latent, which is what contracting and saturating autoencoders do by penalizing the Jacobian. Or you can shape the surface *locally*, minimizing the gradient and maximizing the curvature around data points, which is score matching.

**Mapping this back onto our equation**

Now read both families through the objective from Section 3, because the taxonomy predicts exactly what we are about to find.

Contrastive methods put the push-up directly into g, and we will see this concretely in a moment when InfoNCE splits apart; the denominator is a sum over chosen points whose energy is being raised, and it is a real term with a real value. The trouble is that the sum has to run over the points you chose, so the cost scales with how many you need, and in high dimension the number needed to meaningfully shape a surface grows uncomfortably. That is not an implementation detail you can optimize away, it is intrinsic to the decision to push up pointwise in a large space.

Architectural methods have no g at all, which is precisely the g ≡ 0 we are going to keep running into. The constraint has been moved out of the objective and into the shape of the model or the behaviour of the optimizer, where it cannot be inspected, weighted, or ported to a new setting.

Regularization-term methods are the interesting branch, because they keep the constraint in the loss without paying the pointwise cost. Rather than raising energy at specific locations, they make a statement about the *distribution* of low energy as a whole, which is a global claim rather than a pointwise one, and that is why it can be cheap. It is also exactly the slot we identified at the end of Section 3.

Which tells us where this article is going. **LeJEPA lives in the regularization branch**, and it inherits the obvious question that the branch has never answered properly; if your term is supposed to measure something about the distribution of the representation, what exactly should it measure? Sparse coding says the representation should be sparse. VAEs say it should look like a chosen prior, which is closer to the mark than anything else on this list and we will come back to it. VICReg says its covariance should be the identity. All three are guesses.

The rest of this section walks through the guesses and where each one falls short, and then we go looking for a derivation instead.

### 4.2 Negative samples

The oldest answer, and in some ways still the most honest, is to simply tell the model that different things should not land in the same place. Contrastive methods like SimCLR and MoCo pull the two views of an image together while explicitly pushing every other image in the batch away, which turns the anti-collapse requirement into something you can write down; a collapsed encoder maps everything to one point, so if you penalize proximity between unrelated samples then collapse is directly and heavily punished.

![](https://substackcdn.com/image/fetch/$s_!QW-G!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0917cbfa-658d-4e79-930d-fe5a6229d8fe_1054x637.png)

*The positive pair is pulled together while every other sample in the batch is pushed away, which is where the quadratic cost comes from.*

Contrastive learning does something rather elegant on our equation, in that f and g are both hiding inside a single expression. Expand the InfoNCE loss and they separate cleanly:

*L\_InfoNCE = −log \[ exp(sim(z, z⁺)/τ) / Σ\_j exp(sim(z, z\_j)/τ) \]*

*\= − sim(z, z⁺)/τ + log Σ\_j exp( sim(z, z\_j)/τ )*

*where the first term is f(·), the fit, and the second is g(·), the constraint.*

The numerator pulls the positive pair together and is the fit term; the denominator sums over every other sample in the batch and is the constraint. So contrastive methods do have a real g, they simply never separated it out and named it. The cost is visible right there in the sum, which runs over the whole batch for every sample and gives us O(B²K).

The belief being expressed here is that the representation should spread its mass out rather than concentrate it, and as beliefs go that is entirely reasonable. The trouble is what it costs to say it this way. Every sample has to be compared against every other sample in the batch, which is a quadratic operation, and worse, the quality of the signal depends on how many negatives you have available; too few and the constraint barely bites, so you end up needing enormous batches or an auxiliary memory bank of stored embeddings to make it work at all. You are also, in a subtle way, lying to the model, since two different photographs of the same breed of dog are treated as things that must be pushed apart when they arguably should not be. The constraint is real and statable, it is just expensive and slightly wrong.

### 4.3 Teacher–student networks with EMA

BYOL and DINO take an entirely different route, and this is the one I find hardest to justify from first principles. You keep two copies of the network, a student that receives gradients normally and a teacher whose weights are an exponential moving average of the student’s, and the student is trained to predict the teacher’s output. The teacher never receives gradients at all; it simply trails behind.

![](https://substackcdn.com/image/fetch/$s_!c-V-!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F33c9c9fe-a0c9-41ff-b235-936c3f0340e6_2046x1176.png)

*Two ways of avoiding collapse without writing anything into the objective. In both cases the constraint lives in the gradient flow rather than in the loss.*

Written against our base form, the objective here is only the fit term, with the target produced by a second, slower parameter set:

*L\_BYOL = ‖ Pred(Enc\_θ(x\_v)) − Enc\_ξ(x\_v′) ‖², ξ\_t = τ ξ\_{t−1} + (1−τ) θ\_t*

*g(·) ≡ 0*

There is nothing at all in the constraint slot. The entire anti-collapse behaviour lives in that second expression, which is an update rule rather than a term in the objective, and τ is a schedule rather than a trade-off.

What belief about Z does this express? I genuinely struggle to answer that, and I do not think the answer exists in a clean form. The mechanism is temporal rather than distributional; because the teacher lags, the target the student chases is always slightly stale, so the collapsed solution is a fixed point the optimizer cannot walk into quickly enough to reach before other structure has formed. Collapse is avoided by making the descent path awkward rather than by making collapse expensive.

And it works, extremely well, which is exactly what makes it such a clean illustration of the argument from the previous section. Here is a mechanism carrying an enormous amount of the inductive bias in some of the best vision models we have, and if you ask what property of the representation it guarantees, nobody can tell you. There is no theorem. There is an EMA decay rate that needs to be scheduled by hand, and if you get the schedule wrong the whole thing falls over.

### 4.4 Stop-gradients

SimSiam pushed this further and showed, somewhat startlingly, that you can drop the EMA teacher entirely and keep the collapse-avoidance, provided you place a stop-gradient on one branch so that gradients only flow through the other.

The same situation, made starker:

*g(·) ≡ 0, ∇̃\_θ L ≠ ∇\_θ L*

The constraint is not so much absent from the objective as the objective is absent from the optimization; we descend a modified gradient for which no corresponding loss exists.

I want to flag what has happened here, because it is easy to skate past. A stop-gradient is not a term in the loss. It does not appear in the objective, it has no value, it cannot be traded off against anything. It is an instruction to the autograd engine to discard part of the true gradient, which means the quantity actually being descended is not the gradient of the loss you wrote down. Whatever implicit objective SimSiam is optimizing, it is not L\_pred, and there is no expression for it anywhere.

In the framing from Section 3 this is not a badly-specified prior; it is not a prior at all. There is nothing in the P(\[θ, Z\]) slot, and the constraint has instead been smuggled into the optimizer.

### 4.5 Whitening

Barlow Twins and W-MSE take the most transparent approach of the lot. If dimensional collapse means the embedding dimensions are redundant and confined to a subspace, then simply require them not to be redundant; drive the cross-correlation matrix between the two views’ embeddings towards the identity, so that each dimension carries its own information and none duplicates another.

![](https://substackcdn.com/image/fetch/$s_!2F8r!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71d63b3a-1a64-4504-86b1-245b351f84c6_1375x773.png)

*Barlow Twins drives the cross-correlation matrix towards the identity. The object being optimized is K × K, which is the entire cost problem in one picture.*

This is the first method that puts something explicit into the slot:

*g\_BT(Z) = Σ\_i (1 − C\_ii)² + λ Σ\_{i≠j} C\_ij²*

*where C = cross-corr( Zᵛ, Zᵛ′ ) is a K × K matrix.*

A genuine, differentiable, statable term at last. The K × K sitting in the shape of C is exactly the cost problem.

This is a real belief about Z, stated in the loss, differentiable, and defensible. The problem is what it costs and how it behaves. Building a correlation matrix over a K-dimensional embedding is a K×K operation, so both memory and compute grow quadratically in the embedding dimension, which is precisely the direction you want to scale. Several variants additionally need matrix inverses or square roots to perform the whitening, and those are numerically delicate in a way that shows up as instability at exactly the moment your model gets large enough to be interesting.

### 4.6 VICReg, and the thing that is actually wrong

VICReg deserves the most attention here, both because it is the most explicit of the lot and because it will reappear later as a special case of what LeJEPA does.

Its loss has three named terms; an invariance term that pulls the two views together, a variance term that forces each embedding dimension to maintain a minimum standard deviation across the batch, and a covariance term that pushes off-diagonal covariances towards zero. Put together, the second and third are a direct instruction about the shape of the embedding distribution; every dimension should carry variance, and no two dimensions should be correlated. Written in the language of Section 3, VICReg says the representation should have roughly identity covariance.

That is a genuine, written-down belief about Z, which already puts it ahead of everything above. And it still is not enough, for a reason that has nothing to do with cost.

In our notation its constraint term is the most explicit of the lot:

*g\_VIC(Z) = Σ\_k max( 0, γ − σ\_k(Z) ) + Σ\_{i≠j} \[ Cov(Z) \]²\_ij*

*the first sum being the variance term and the second the covariance term.*

***Identity covariance constrains the first two moments of a distribution and says absolutely nothing about the rest of it.***

And now the failure can be stated precisely rather than merely argued, because both terms depend on Z only through Cov(Z), which means:

*Cov(P) = Cov(Q) ⟹ g\_VIC(P) = g\_VIC(Q)*

That single line is the whole problem. Any two distributions sharing a covariance matrix are completely indistinguishable to this penalty, no matter how different they are in every other respect.

This is what “under-specified” means, and it is worth being concrete, because the phrase gets used loosely. A criterion is under-specified when a solution can satisfy it completely while remaining degenerate in a way the criterion cannot see. And there are many distributions with mean zero and identity covariance:

1. A standard Gaussian has identity covariance.
2. So does a distribution concentrated on the corners of a hypercube; all mass sitting at ±1 in each coordinate, nothing anywhere in between.
3. So does a heavy-tailed distribution where most embeddings sit near the origin and a handful sit very far away, arranged so the second moments work out.
1. So does a mixture of a few tight, widely separated clusters.

Every one of those passes VICReg’s check with a perfect score. Several of them are terrible representations. A distribution living on hypercube corners has a discrete, spiky structure that any downstream linear probe will struggle with; a heavy-tailed one has most of its samples crowded into a region where they cannot be told apart while its variance budget is spent on outliers. The covariance matrix cannot distinguish any of these from a Gaussian, because covariance is blind to everything above the second moment.

So the criterion is satisfied and the model is still bad, and crucially, nothing in your loss curve will indicate this. You have not been told you are wrong, honestly you have been told nothing at all about the thing you failed to constrain.

![](https://substackcdn.com/image/fetch/$s_!beTV!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9a9f4e9-cd14-4028-ba2b-16231fa9d75a_1526x1676.png)

*Four distributions with identical mean and covariance, computed rather than asserted. Three of them are poor representations, and no covariance-based penalty can tell any of them apart from the first.*

### 4.7 The pattern

Setting all five side by side, and specifically setting their g terms side by side, the failures sort themselves into three kinds, and most methods manage to exhibit more than one. Two of the g terms are identically zero, one is O(B²) in the batch, one is O(K²) in the embedding dimension, and the only cheap and well-specified-looking one turns out to be blind to everything above the second moment.

![](https://substackcdn.com/image/fetch/$s_!ChrH!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d1397b3-1f5a-45d4-83f6-41dd109bce4a_1664x1053.png)

*The five mechanisms, their constraint terms, and the three ways of falling short.*

The three failure kinds are worth naming, because they are exactly what we will demand the fix avoid:

1. **Quadratic in something you want to scale.** Batch size for contrastive methods, embedding dimension for whitening. Both are dimensions you would like to grow, and both are where the cost lands.
2. **Under-specified.** The criterion can be fully satisfied by a degenerate solution, which is VICReg’s problem and, in a looser sense, everybody’s.
2. **Not in the loss.** Stop-gradients and EMA schedules are interventions in the training procedure rather than statements in the objective, which means they cannot be reasoned about, traded off, or ported to a new setting without re-tuning from scratch.

Notice that none of these is a complaint about performance. All of these methods work; several of them produce state-of-the-art representations, and I have written admiringly about models built on them. The complaint is that we cannot say what any of them guarantees, which means we cannot improve them except by trying things, and we cannot know whether we are near the best available answer or nowhere close.

Which finally lets us ask the right question. Rather than continuing to patch, what would we actually want from a term in that slot if we could specify it freely? That is the next section.

---

## 5\. The Ideal Case

We have spent three sections building a frame and then finding that nothing quite fits in it. Section 3 gave us a slot in the objective and told us what kind of object belongs there; Section 4 went through everything currently occupying that slot and found each occupant wanting. Which puts us in the position I always find most useful at this point in a paper, namely to stop reading it entirely and ask what we would want if we could simply specify it.

The nice thing is that Section 4 has already done most of the work, because each failure inverts directly into a requirement. So let us collect those first, then add the one requirement that the failures cannot possibly tell us about, which turns out to matter more than the rest combined.

### 5.1 What the failures demand

***One. The constraint must actually exist*****.** It sounds absurd to have to say this, and yet two of the five mechanisms we looked at had g ≡ 0. Whatever we end up with has to be a term in the loss with a value you can print, a gradient you can inspect, and a coefficient you can turn. Not a schedule, not a second network, not an instruction to the autograd engine.

***Two. It must be fully specified.*** This is the VICReg lesson and the most important of the lot. We saw the failure stated exactly; Cov(P) = Cov(Q) implies g(P) = g(Q), which means any two distributions agreeing on their second moments are invisible to each other under the penalty. What we want is the opposite property, that g(P) = g(Q) should force P and Q to genuinely be the same distribution rather than merely agreeing on a couple of summary statistics. Anything constraining finitely many moments fails this by construction.

***Three. It must be linear in both batch size and embedding dimension*****.** Contrastive methods are O(B²K) and whitening is O(BK²), and those are quadratic in precisely the two directions you would like to grow. Any constraint requiring all pairs of samples, or a matrix over all pairs of dimensions, hits a wall exactly when the model becomes interesting.

***Four. One knob*****.** This follows from requirement one rather than standing alone; once the constraint has a form, a single coefficient in front of it is available, and the trade-off becomes a number instead of a tuning ritual. The difference between one hyperparameter and six is not really about convenience, it is about whether you can move the method to a new domain without redoing the search from scratch.

***Five. Bounded, well-behaved gradients.*** Stability should come from the shape of the objective rather than from discovering the schedule that avoids the instability. A constraint whose gradients blow up when embeddings wander somewhere unusual will accumulate warmups and clipping and decay curves until you are back where you started.

### 5.2 A requirement the failures cannot give us

Those five are all defensive. Every one is derived from something that went wrong, which means collectively they describe what a constraint must avoid rather than what it should be. Satisfy only those and you get a cheap, stable, fully-specified penalty that pins the representation to some particular shape, with nothing whatsoever telling you *which* shape.

Recall too where the energy framing left us at the end of 4.1. Both families exist to make energy high away from the data, and we concluded that LeJEPA belongs in the regularization branch, which limits the volume of low-energy space rather than pushing up pointwise. But “limit the volume” is a statement about how much, not about where or in what shape, and sparse coding, VAEs and VICReg are three different guesses at the missing part. None of the five requirements above can adjudicate between them, because all three are perfectly capable of being cheap, stable and in the loss.

So here is the sixth requirement, and it is the one that actually generates an answer rather than filtering candidates:

***Six. The representation should be optimal for downstream tasks we have not seen yet.***

This is easy to nod at and harder to take seriously. The entire premise of self-supervised pretraining is that you do not know what the model will be used for. You train on unlabelled data, freeze the encoder, and later somebody attaches a linear probe for a classification problem you never anticipated, or runs k-NN over the embeddings, or fine-tunes on a small labelled set from a domain you have never seen. At the moment of pretraining the downstream label y does not exist. It is not merely unknown to us, it has not been chosen by anyone.

Which makes the question we are really asking a slightly strange one, worth stating carefully:

*which distribution should Z follow to minimize expected risk,*

*when the task is drawn from a family we cannot observe?*

Notice what has happened over the course of three sections. We started with a defensive question, how do we stop the model from cheating, and by taking the requirements seriously we have arrived at an entirely different one, which is what shape a representation ought to be. The first question has many acceptable answers, which is precisely why the literature contains so many mechanisms. The second question, remarkably, has exactly one.

### 5.3 What we are really asking for

Putting all six together, the thing we want in that slot is not a penalty at all. It is a **target distribution**.

That reframing is what the whole article has been building towards, so let me state it plainly. If the constraint must fully specify the distribution rather than a handful of its moments, then it cannot be a list of desirable properties like “high variance” or “low correlation”. It has to name a distribution Q and measure how far the induced representation distribution p\_z sits from it:

*g(θ, Z) = D( p\_z ‖ Q )*

for some target Q and some notion of distance D. Requirement six then tells us how to choose Q, since it should be whichever distribution minimizes expected risk over unseen tasks. Everything else on the list becomes a constraint on D; it must be linear in K and B, differentiable with bounded gradients, and it has to genuinely distinguish distributions rather than just their moments.

Which splits the problem cleanly in two, and that split is the structure of the rest of this article:

1. **Which Q?** A question about statistics and downstream risk, and the answer is provable rather than chosen. This is Section 6.
2. **Which D?** A question about how you compare distributions in high dimension without the cost exploding or the gradients misbehaving. This is Section 7.

It is worth flagging how unusual this separation is. In most papers the objective and its implementation are tangled together and you cannot discuss one without the other. Here the target and the divergence are genuinely independent design decisions; you could keep LeJEPA’s Q and swap its D, or the reverse, and both halves would still make sense. That separability is usually a sign the framing is correct.

It also explains why VAEs came closest of anything in Section 4. A VAE with a KL term to a Gaussian prior has exactly this shape, a target distribution and a divergence to it. What it lacks is any argument that its particular Q is the right one, since the Gaussian there is chosen for the reparameterization trick and analytic convenience rather than derived from downstream risk, and its D is a KL that needs the latent to be sampled rather than deterministic. The form was right. The justification was missing.

### 5.4 A note on what we are giving up

Before we go looking for Q, it is worth being honest that requirement six carries a real cost, and the paper is upfront about it.

Optimizing for an unknown task means optimizing for the *worst case* over a family of tasks, and a worst-case optimum is by construction not the best answer to any particular one. If you happen to know your downstream application is medical imaging, or document retrieval, or one specific classification problem, then a representation shaped for that task will beat a task-agnostic one. We are deliberately choosing not to bet, and the price of never betting is that you never win big on any single hand.

Whether that trade is worthwhile depends entirely on what you are building. For a foundation model, whose whole premise is serving tasks that do not exist yet, it is obviously right. For a system with one known downstream use it may not be, and I will come back to this in the Thoughts section, because I do not think it is as settled as the paper implies.

With that noted, let us go and find Q.

---

## 6\. Methodolgy: Finding Q (why the isotropic Gaussian?)

This is the section the whole article has been walking towards, so we are going to take it slowly and derive rather than assert. The claim we are chasing is that there is exactly one distribution the embeddings should follow, and it turns out to fall out of two separate arguments that answer two genuinely different questions. People conflate them constantly, so it is worth naming them up front.

The first argument asks about the **shape of the covariance** and answers *isotropic*. The second asks about **everything above the second moment** and answers *Gaussian*. Neither one gets you there alone, and the gap between them is precisely where VICReg lives.

### 6.1 Setting up a question that can actually be answered

We cannot minimize risk on a task we have not seen. That is not a technical obstacle, it is a logical one; there is no y, so there is no risk to minimize. What we can do is minimize risk over a whole family of possible tasks, and specifically over the worst member of that family, which is what requirement six was really asking for.

Before we can compare candidate distributions we need to fix what is held constant, otherwise the question is ill-posed. Consider what happens if we do not: take any embedding distribution and multiply every vector by a thousand. Every downstream probe becomes trivially better conditioned, the effective noise shrinks relative to the signal, and we have learnt nothing except that bigger numbers are easier to fit. So we constrain the total variance,

*tr( Cov(Z) ) = Σ\_k λ\_k = κ*

and hold κ fixed throughout. Now the question becomes sharp and non-trivial. We have a fixed budget of variance, and the only question is **how to distribute it**. Every candidate distribution below has the same total energy; they differ only in geometry.

Notice this is already an interesting reframing. We are not asking how much information the representation should carry, we are asking how it should be arranged.

### 6.2 Linear probing gives us isotropy

Start with the most common way anybody evaluates a frozen encoder, which is to fit a linear probe on top of it. The probe solves ridge regression:

*β̂ = argmin over β of ‖ y − Zβ ‖² + λ ‖β‖²*

I want to pause on this equation for a second, because we have met it before. This is exactly the objective we built from scratch in the [regularization article](https://vizuara.substack.com/p/regularization-what-why-and-how-part), fit term plus L2 penalty, with λ the Lagrange multiplier that emerged when a hard constraint on the weights got softened into a penalty. That article was about what regularization does to a model. This section is about what it does to your *evaluation*, and the two turn out to be the same mathematics pointed in different directions.

*\[EMBED: Regularization: What? Why? and How? (Part -1)\]*

The solution is standard:

*β̂ = ( ZᵀZ + λI )⁻¹ Zᵀ y*

Now, why are we looking at this at all? Because β̂ is an estimator, and estimators have bias and variance, and both of those turn out to depend on the geometry of Z in a way we can compute. If we can show that anisotropy hurts both, we are done with the first half of the argument.

**Step 1: what the bias looks like**

Assume the task is genuinely linear in the embedding, so y = Zβ\* + ε with E\[ε\] = 0 and β\* the true parameters, and take Z to be mean-centred. Then

*E\[β̂\] = ( ZᵀZ + λI )⁻¹ ZᵀZ β\**

and the bias is the difference between that and the truth:

*Bias = \[ ( ZᵀZ + λI )⁻¹ ZᵀZ − I \] β\**

This is opaque as written, so let us do the thing that always helps with expressions full of matrix inverses, which is to move into the eigenbasis. Write the empirical second moment as ZᵀZ ≈ N·Σ where Σ = Cov(Z), and eigendecompose Σ = UΛUᵀ with eigenvalues λ₁ … λ\_K. In that basis everything becomes diagonal and the whole expression collapses to a per-coordinate statement:

*Bias\_k = \[ Nλ\_k / (Nλ\_k + λ) − 1 \] β\*\_k = − s\_k · β\*\_k, s\_k = λ / (Nλ\_k + λ)*

**This is the whole thing, so let us read it carefully.** Each coordinate of the estimate is shrunk towards zero by a factor s\_k that depends only on that coordinate’s eigenvalue. When λ\_k is large the denominator is large, s\_k ≈ 0, and that coordinate is recovered faithfully. When λ\_k is small s\_k ≈ 1, and that coordinate is shrunk almost to nothing regardless of what the true β\*\_k was.

![](https://substackcdn.com/image/fetch/$s_!M7dm!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5e6b1b8-ed3b-4d5b-8c2d-485bcef7bc5d_1296x815.png)

*The shrinkage factor as a function of a direction’s eigenvalue. Directions carrying little variance are erased from the estimate entirely, whatever the task needed from them.*

So the ridge penalty is not shrinking your estimate uniformly. It shrinks hardest along the directions where your representation has the least variance, which is a completely reasonable thing for it to do, since those are the directions where the data tells you least, and it is catastrophic if the task happens to depend on one of them.

**Step 2: taking the worst case**

Squaring and summing gives the total squared bias:

*‖Bias‖² = Σ\_k ( λ / (Nλ\_k + λ) )² · β\*²\_k*

Now we invoke requirement six. We do not know β\*, and we are not allowed to assume anything about it, so we ask what the worst task of a given size looks like. Fix ‖β\*‖ and let an adversary point it wherever it does most damage; obviously it points along the coordinate with the largest shrinkage, which is the one with the **smallest** eigenvalue:

*max over ‖β\*‖ = c of ‖Bias‖² = ( λ / (Nλ\_min + λ) )² · c²*

And now the optimization writes itself. Minimizing the worst-case bias means maximizing λ\_min, subject to the eigenvalues summing to κ. There is no cleverness required here; if you have a fixed total to distribute and you want to make the smallest share as large as possible, you split it evenly:

*max λ\_min subject to Σ λ\_k = κ ⟹ λ₁ = λ₂ = … = λ\_K = κ/K*

**Which is isotropy.** Not chosen, not preferred; forced, by the combination of a fixed variance budget and a refusal to assume anything about the downstream task.

**Step 3: the variance says the same thing**

Bias was one half of it. For the variance, set λ = 0 so the algebra stays clean, and use the standard result for OLS:

*Var(β̂) = σ² ( ZᵀZ )⁻¹ = (σ²/N) Σ⁻¹*

Total estimator variance is the trace, which in the eigenbasis is just a sum of reciprocals:

*tr( Var(β̂) ) = (σ²/N) · Σ\_k 1/λ\_k*

Minimize that subject to Σλ\_k = κ. Lagrange gives

*∂/∂λ\_k \[ Σ\_j 1/λ\_j + μ Σ\_j λ\_j \] = − 1/λ\_k² + μ = 0 ⟹ λ\_k = 1/√μ for every k*

which is the same value for every k, so once again all eigenvalues equal and once again **isotropy**.

![](https://substackcdn.com/image/fetch/$s_!cXme!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff7546f1e-0b4e-43b9-8c14-ed3db59e6630_1728x1376.png)

Each line is a linear probe fitted to a different resample of the same distribution. The anisotropic embedding has the same total variance and a far less stable estimator.

There is something worth staring at in that sum of reciprocals, though, because it is doing more than delivering the same answer twice. As any λ\_k → 0, the sum diverges. Not degrades, *diverges*. And a λ\_k heading towards zero is precisely the dimensional collapse we defined back in Section 2. So this expression is telling us that dimensional collapse does not merely waste capacity, it sends the variance of every downstream estimator to infinity. The failure mode we started the article worrying about and the geometry we are now deriving are the same phenomenon seen from two angles.

### 6.3 Why isotropy is not enough

We now have a result, and it is a real one; the covariance should be a scaled identity. It is also, unfortunately, exactly the result VICReg already had.

Look back at the four distributions from Section 4.6. All four have identity covariance, so all four are perfectly isotropic, so all four are equally optimal by everything we have derived so far. Three of them are terrible representations.

The reason our argument cannot see the difference is structural rather than accidental. A linear probe interacts with the embedding only through ZᵀZ, which is to say only through the second moment. Anything the second moment cannot see, a linear probe cannot see either, and so no amount of care in the linear analysis will ever tell us about the shape of the distribution beyond its covariance.

Hence if we want to constrain the rest of the distribution, we need a probe that actually depends on the rest of the distribution. Which is not a contrivance, incidentally; k-NN and kernel probes are standard ways to evaluate frozen encoders, arguably more common than linear probes in retrieval settings. So let us redo the analysis with one of those and see what falls out.

### 6.4 Nonlinear probing gives us Gaussian

Take a radius-based k-NN probe, which predicts by averaging the labels of everything inside a ball:

*ŷ(q) = ( 1 / |N\_r₀(q)| ) · Σ\_{n ∈ N\_r₀(q)} y\_n, N\_r₀(q) = { n: ‖z\_n − q‖ ≤ r₀ }*

The key difference from before: this estimator depends on which points happen to be nearby, and that is a statement about the local density of the embedding distribution rather than about its global second moment. That is exactly the sensitivity we were missing.

**Step 1: where the bias comes from**

Let g(z) = E\[y | z\] be the true regression function. The bias of the probe at a query point q is

*Bias(q) = E\[ g(z) | z ∈ N\_r₀(q) \] − g(q)*

that is, the difference between the average of g over the neighbourhood and its value at the centre. Taylor expand g about q:

*g(z) = g(q) + ∇g(q)ᵀ (z−q) + ½ (z−q)ᵀ H (z−q) + …*

Now here is the crucial observation, and it is worth thinking about before we compute anything. **If the points in the neighbourhood were distributed symmetrically about q, the linear term would average to exactly zero.** For every point displaced in one direction there would be a matching point displaced the other way, and ∇g would contribute nothing to the bias. The neighbourhood average would be unbiased to first order and only the curvature term would survive.

So the linear term only survives when the neighbourhood is **lopsided**, that is, when there are systematically more points on one side of q than the other. And a systematic imbalance of points across a small ball is exactly what it means for the density to have a gradient there.

![](https://substackcdn.com/image/fetch/$s_!_0Qz!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F738b7fda-c5cb-4481-80cf-7b60c9c7af22_1375x918.png)

*Left, a flat density: the neighbours sit symmetrically about the query and their displacements cancel. Right, a density gradient: the ball fills unevenly and the average is pulled towards the dense side.*

**Step 2: making that precise**

Expand the density around q in the same way, using ∇p = p · ∇log p:

*p(z) ≈ p(q) · ( 1 + ∇log p(q)ᵀ (z−q) + … )*

Taking the density-weighted expectation of the displacement over the ball, and using the standard fact that for a uniform ball of radius r₀ in R^K we have E\[(z−q)(z−q)ᵀ\] = r₀²/(K+2) · I:

*E\[ (z−q) | z ∈ N\_r₀(q) \] ≈ ( r₀² / (K+2) ) · ∇log p(q)*

So the displacement does not average away. It averages to something proportional to the log-density gradient, and the bias picks up a term

*Bias(q) ≈ ( r₀² / (K+2) ) · ∇log p(q)ᵀ ∇g(q) + ( a second O(r₀²) term from the curvature H )*

Read that plainly: **the probe is biased in proportion to how fast the density is changing.** In a region where embeddings pile up on one side, the neighbourhood average is pulled towards that side, and the prediction inherits the pull.

**Step 3: integrating over all query points and all tasks**

Square the bias and integrate over the distribution of query points. The ∇g factor depends on the task, which we do not know, so we treat it as an unknown of bounded size and absorb it into a constant τ\_g. What is left is:

*ISB ∝ ( r₀⁴ / (K+2)² ) · τ\_g² · J(p), J(p) = ∫ ‖∇log p(z)‖² p(z) dz*

That integral has a name. J(p) is the **Fisher information** of the distribution with respect to location, and it measures how sharply the density varies relative to its own magnitude. A density with steep gradients, spikes, sharp edges or isolated clusters has large J(p). A smooth, gently-varying density has small J(p).

Everything else in that expression is fixed by the setup; the radius, the dimension, the unknown task. **The only thing we control is J(p), and it is the only thing left to minimize.**

**Step 4: which distribution minimizes Fisher information?**

We now have a clean, self-contained mathematical question with nothing to do with machine learning:

*min over p of J(p) subject to Cov(p) = Σ*

And it has a classical answer. For any distribution with covariance Σ,

*J(p) ≥ tr( Σ⁻¹ ), with equality if and only if p = N(0, Σ)*

**The Gaussian is the unique minimizer.** Not the best among the ones we tried, not optimal under extra assumptions; unique, given the covariance constraint.

![](https://substackcdn.com/image/fetch/$s_!4WPp!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d828ec7-f1e0-4702-8978-6d6694ac09f3_1398x849.png)

*The four distributions from Section 4.6, evaluated by numerical integration. Covariance could not tell them apart at all; Fisher information separates them by nearly three orders of magnitude, and only the Gaussian attains the bound.*

Combine that with 6.2, which told us Σ must be a scaled identity, and the answer is fully pinned down:

*Q = N( 0, σ² I\_K )*

Every degree of freedom in the choice of target distribution has now been used up. The shape of the covariance came from the linear probe, and everything above the second moment came from the nonlinear one.

### 6.5 Why this is the right answer from two directions

I find a result more convincing when a second, unrelated argument arrives at the same place, and here one does.

Ask a different question: given a fixed variance budget, which distribution assumes the *least* about anything? That is the maximum entropy question, and its answer under a covariance constraint is famously the Gaussian. So the distribution that minimizes Fisher information and the distribution that maximizes entropy, under the same constraint, are the same distribution.

That coincidence is not a coincidence, and it has a clean interpretation. Both quantities are measuring structure. Entropy asks how much structure the distribution has, Fisher information asks how sharply that structure varies, and under a variance budget the flattest, least committed, most spread-out option optimizes both.

Which finally gives us the intuition to carry away from this whole section. **You are building a searchlight before you know where you will need to look.** Any asymmetry in the beam is a bet about where the target will be. Isotropy is the decision not to bet on direction; Gaussianity is the decision not to bet on location within a direction, by refusing to concentrate mass anywhere in particular. The two theorems in this section are the two halves of declining to gamble, and requirement six was the statement that we are not in a position to gamble at all.

![](https://substackcdn.com/image/fetch/$s_!63yD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9e59bca-f7bb-400e-afca-a8164ad35ec7_2004x727.png)

*Three ways to spend a fixed illumination budget. The first two are excellent if the tasks land where you guessed and useless otherwise; only the third makes no assumption at all.*

It also retroactively explains the four distributions from Section 4.6. The hypercube corners and the cluster mixture both make an enormous bet, namely that the downstream task cares about exactly those four regions and nothing in between; if it does they are excellent, and if it does not they are useless. The heavy-tailed distribution bets everything on the centre. Only the Gaussian bets nothing, and that is precisely why it wins the worst case.

### 6.6 Where this leaves the objective

We came into this section with a target-shaped hole:

*g(θ, Z) = D( p\_z ‖ Q )*

and we can now fill in half of it:

*g(θ, Z) = D( p\_z ‖ N(0, σ² I) )*

which, plugged back into the objective from Section 3, gives us the shape of LeJEPA:

*L(θ, Z; X) = L\_pred(θ; X) + α · D( p\_z ‖ N(0, σ² I) )*

One thing remains, and it is not a small thing. We have to actually compute D, which means measuring the distance between an empirical distribution of a few hundred embedding vectors and a Gaussian, in a space of a thousand dimensions, differentiably, cheaply, and with bounded gradients. That is a genuinely hard problem and it is where most of the paper’s engineering lives.

That is Section 7.

---

## 7\. Methodology: Finding D (measuring the distance to a Gaussian)

We know what we want the embedding distribution to be. Now we have to write down something differentiable that says how far we are from it, and this turns out to be considerably harder than it sounds.

Here is the problem in its concrete form. Your batch gives you maybe 256 embedding vectors sitting in 1024 dimensions. From that you have to produce a single scalar saying how un-Gaussian this cloud of points is, differentiate it, and do so cheaply enough to run on every step of training. Anyone who has tried to estimate a density in a thousand dimensions from a few hundred samples will already be uncomfortable, and they should be; that problem is genuinely hopeless. So the interesting question is how the paper avoids having to solve it.

### 7.1 Distribution matching as a hypothesis test

The usual instinct here is to reach for a divergence. KL, Wasserstein, MMD, pick one, minimize it. The paper does something different, and the reframing is the first good idea in this section.

Rather than asking how far apart two distributions are, ask a statistician’s question:

*H₀: p\_z = Q versus H₁: p\_z ≠ Q*

This is a hypothesis test. You compute a test statistic T from your samples, which is a single number summarizing how much evidence the data provides against the null, and if it exceeds a critical value you reject. Statisticians have been designing these for a century and they come with properties that divergence estimators generally do not; known null distributions, provable consistency, and a clear notion of what the statistic is measuring.

Then comes the move that makes it useful to us. **The test statistic is already a scalar function of the embeddings, so just use it as the loss.**

*g(θ, Z) = T( { f\_θ(x\_n) } )*

Minimizing T is minimizing the evidence against the null, which is to say training the encoder until a statistician could no longer distinguish its embeddings from Gaussian samples. That is a much more precise statement of intent than “penalize the covariance”, and it is exactly the “fully specified” requirement from Section 5 restated in a form you can compute.

It also gives us something no other method in Section 4 could offer, which is a scale for the number. A test statistic can be compared against a critical value, so you can ask whether your representation is *acceptably* Gaussian at some significance level rather than just noting the penalty went down.

### 7.2 The obstacle: high dimension

Unfortunately, multivariate normality tests are not cheap. Mardia’s test needs third and fourth moment tensors, Henze–Zirkler needs all pairwise distances, and essentially every classical option is at least quadratic in sample count and often far worse in dimension. Worse than the cost is the sample complexity; to say anything reliable about the shape of a density in K dimensions you need a number of samples that grows exponentially in K. With 256 samples in 1024 dimensions, the empirical distribution is not an approximation to p\_z, it is 256 isolated points in a space so large that they are all effectively equidistant from one another.

![](https://substackcdn.com/image/fetch/$s_!btpf!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a474e6e-e03f-4304-83a8-aececa2db419_1201x790.png)

*Estimating a density directly needs sample counts that grow exponentially with dimension; a univariate test on each slice needs a fixed number regardless of K.*

So a direct test is not merely expensive, it is statistically meaningless at the batch sizes we can afford. We need a way of not looking at the high-dimensional density at all.

### 7.3 Sketching: reading a distribution off its shadows

The escape is a theorem from 1936, and it is the most elegant thing in the paper.

**Cramér–Wold.** For two random vectors X, Y in R^K:

*⟨a, X⟩ ≜ᵈ ⟨a, Y⟩ for every unit vector a ⟺ X ≜ᵈ Y*

In words: if every one-dimensional projection of two distributions matches, the distributions themselves match. Nothing is lost by only ever looking at shadows, provided you look from every angle. The paper proves a hyperspherical variant of this (Lemma 3) restricted to unit-norm directions, which is what we actually sample.

Take a moment with how strong that is. A distribution over a thousand dimensions is an enormously complicated object, and this says it is completely determined by a family of one-dimensional distributions, each of which is a thing you can plot on a line and reason about with century-old statistics.

![](https://substackcdn.com/image/fetch/$s_!W-wd!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8c287f98-d424-4959-aeae-a1be49c26c49_2674x1164.png)

The procedure follows immediately. Sample M unit directions, project the batch onto each, run a cheap univariate normality test per direction, and aggregate. Theorem 2 in the paper establishes that taking the worst direction gives a valid test, with the right level under the null and power tending to one under the alternative:

*T\_A(Z) = max over a ∈ A of T( { aᵀ z\_n } )*

And then the paper immediately does something else. The actual SIGReg definition averages over directions rather than maximizing:

*SIGReg(A, Z) = (1 / |A|) · Σ\_{a ∈ A} T( { aᵀ z\_n } )*

The stated reason is worth dwelling on, because it is a good illustration of the difference between a statistic and a loss. The maximum is the correct *test*, since you reject the null if any direction provides evidence against it. But as an objective it produces a sparse gradient; only the single worst direction receives any signal on each step, and the other M−1 projections contribute nothing. Averaging spreads the gradient across every direction at once, and since we are optimizing rather than deciding, that is the behaviour we want. The theory justifies the max; the implementation uses the mean.

**Why this beats the curse of dimensionality**

This deserves care, because the argument is not the naive one. You might hope that since each univariate test needs a sample size independent of K, everything is fine. But the real question is different: if we only constrain M directions, what happens along all the directions we did not sample?

The paper answers with smoothness. If the embedding density lies in a Sobolev space H^α, then satisfying the test exactly on M directions bounds the expected discrepancy over *all* directions:

*E\_a ∫ | φ\_a(t) − φ\_N(t) |² dt ≤ C(K, α) · |A|^(−2α / (K−1)) · (‖ · ‖\_{H^α})*

The exponent is what matters. The bound decays as |A| grows, and it decays **faster when α is larger**, meaning smoother embedding densities are constrained more effectively by the same number of directions. The paper’s conclusion is that |A| = O(K) directions suffice for an ε-approximation when α is large, and it argues that deep networks produce naturally smooth densities, both from the architecture and from the implicit and explicit regularizers already in play. Since the target itself is a smooth isotropic Gaussian, α grows quickly during training, which makes the bound tighten as you converge.

![](https://substackcdn.com/image/fetch/$s_!YdZX!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbee6f05b-fa9c-4887-94f1-eb63dcc1e96d_1648x1336.png)

There is a second argument, and it is the one I find more persuasive because it is almost free. SGD resamples the directions at every step. So while any single minibatch constrains only M directions, the cumulative number of directions applied over training grows linearly with the number of steps. The paper reports that |A| as small as 16, resampled every step, comfortably outperforms a fixed set of thousands held constant throughout training.

![](https://substackcdn.com/image/fetch/$s_!q34H!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe13fe2a2-97d6-4818-b5cc-78a55559519f_1396x1260.png)

So the curse is beaten twice over; once by smoothness, which says a modest M constrains the whole sphere, and once by resampling, which says the effective M is the number you draw times the number of steps you take.

**A fortunate interaction with Section 6**

Something quietly convenient happens here. Slicing requires knowing the projected target distribution for each direction a. For a general target that is its own computation, potentially different for every direction. But our target is the isotropic Gaussian, and for z ~ N(0, σ²I) with ‖a‖ = 1:

*aᵀ z ~ N(0, σ²) for every a*

**Every projection of an isotropic Gaussian is the same univariate Gaussian.**

So there is nothing to compute per direction; the target is one fixed 1-D distribution and every one of the M tests compares against it. Back in Section 5 I claimed Q and D were independent design decisions. They are, in the sense that you could swap either, but they are not indifferent to each other, and the Q that the risk argument forced on us happens to be the one that makes slicing essentially free.

### 7.4 Choosing the univariate test

We have reduced everything to: given N real numbers, how Gaussian are they? The paper works through three families and rules out two of them.

**Option one: moments**

Take the Jarque–Bera test, which compares skewness and kurtosis, and extend it with the first two moments to get a standard-Gaussian test rather than a Gaussian-of-any-mean-and-variance test. This is moment matching over the first four moments, and moment matching is a respectable tool.

Two problems, and the paper formalizes both. The first is identifiability. Theorem 3 states that minimizing a weighted sum of squared differences over any *finite* number of moments does not imply the distributions are equal:

*Σ\_{k=1..K} c\_k ( m\_k(P) − m\_k(Q) )² = 0 does not imply P = Q*

Which is precisely VICReg’s failure from Section 4, generalized. The obvious response is to use more moments. Which runs into the second problem: gradient norms scale as O(k) and the variance of Monte Carlo gradient estimates grows as O(k² m\_{2(k−1)}) for the k-th moment, because moments are polynomial in the data and raising values to a power of k explodes quickly. The paper’s phrasing is that stability and identifiability cannot be achieved simultaneously with moments, and that is the whole objection.

**Option two: the empirical CDF**

Cramér–von Mises, Anderson–Darling, Watson. These compare the empirical CDF against the target and are properly consistent, so unlike moments they are not under-specified. The problem is mechanical. All of them require sorting, and sorting breaks the embarrassingly parallel nature of SGD, particularly across multiple GPUs where synchronization is needed. Sorting and order statistics are also non-differentiable, so gradient-based optimization needs a relaxation, and every available relaxation introduces its own hyper-parameters, which defeats the entire motivation. The paper also excludes Kolmogorov–Smirnov specifically because its ℓ∞ norm produces sparse gradients, and reports Shapiro–Wilk as unstable in practice.

**Option three: characteristic functions**

The empirical characteristic function is the Fourier transform of the density, estimated as a simple average:

*φ̂\_X(t) = (1/n) Σ\_j e^{i t X\_j}*

Three properties make this the right choice. It is **identifiable**, since the map from distribution to characteristic function is a bijection, so a test built on φ encodes the whole distribution rather than a summary. It is **differentiable**, with no sorting anywhere. And it is **distributed-friendly**, because an average over samples composes across devices via a single all-reduce.

The Epps–Pulley test compares the two in weighted ℓ² norm:

*EP = N ∫ | φ̂\_X(t) − φ(t) |² w(t) dt*

with the weight function typically Gaussian, w(t) = e^{−t²/σ²}, and σ commonly set to 1.

The boundedness is where this becomes decisive, and the paper proves it as Theorem 4:

*| ∂EP / ∂z\_i | ≤ 4σ² / N, | ∂²EP / ∂z\_i² | ≤ C √π σ³ / (2N)*

Both the gradient and the curvature are bounded by constants depending only on the batch size and the weight bandwidth σ, and on nothing about the data. Compare that to moments, where the gradient of the k-th moment grows like |x|^{k−1} and a single drifting embedding can dominate everything. Chain rule then gives a stable bound on the gradient with respect to θ. **Stability here is a property of the function rather than something tuned in**, which is requirement five from Section 5 met by construction.

![](https://substackcdn.com/image/fetch/$s_!COZ5!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6163feba-96e8-4bdd-9b3c-8693812288d4_2036x644.png)

One honest detail the paper is upfront about. Using minibatches introduces a bias in the estimator, quantified in Theorem 6:

*E\[ L̂\_n(θ) \] = L(θ) + (1/N) ∫ w\_s(t) ( 1 − |φ\_P(t)|² ) dt*

So both the loss and its gradient carry an explicit O(1/N) bias. The authors report this as minimal in practice even at batch sizes as small as 16, and note that U-statistic debiasing or sample splitting would remove it, neither of which they pursue.

### 7.5 Putting SIGReg together

Assembling everything, SIGReg draws M unit directions, projects the batch onto each, computes the Epps–Pulley statistic of each projection against N(0, 1), and averages:

*SIGReg(A, Z) = (1 / |A|) Σ\_{a ∈ A} EP( { aᵀ z\_n } )*

The integral inside EP is estimated by quadrature. The paper finds the simple trapezoidal rule sufficient with as few as 17 knots, and exploits the symmetry of the integrand to double the effective number of knots for free.

![](https://substackcdn.com/image/fetch/$s_!idfe!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22ae67e2-757e-4a0e-898b-b6ac0a9a5d6f_2036x644.png)

Check it against the Section 5 requirements. It is a term in the loss with a value and a gradient, so requirement one holds. It is built on characteristic functions, which are identifiable, so requirement two holds. Its cost is linear in minibatch size, so requirement three holds. It sits behind a single coefficient, so requirement four holds. Its gradients and curvature are bounded by Theorem 4, so requirement five holds. And its target came from the risk argument in Section 6, so requirement six holds.

Six for six, which is the first time anything in this article has managed that.

**Why it distributes so well**

The only quantity crossing between devices is the empirical characteristic function, which is an average over samples. Averages compose; each device computes its partial mean and one all-reduce combines them. Nothing depends on gathering the embeddings themselves. Contrastive methods, by contrast, need negatives from across the batch and therefore must move embeddings between devices, which is a far larger and more awkward transfer.

**VICReg falls out as a special case**

A satisfying way to close, and the mechanism is simpler than I expected. It is not an approximation or a limit of the Epps–Pulley statistic; it is a different choice of T. Substitute

*T( { x\_n } ) = mean( { x\_n } )² + ( std( { x\_n } ) − 1 )²*

into SIGReg, keep everything else, and in the limit of many slices you recover VICReg. The paper proves in Appendix B.14 that this enforces exactly E\[Z\] = 0 and Cov(Z) = I; the argument is a neat one, showing that if every unit direction has zero mean and unit variance in projection then the mean vector must vanish and the covariance must be the identity, by testing the standard basis vectors and then their pairwise sums.

So VICReg is LeJEPA with a degenerate statistical test, and by Theorem 3 that test is exactly the kind that admits shortcut solutions. The paper is blunt about it, advocating strongly against the setting for that reason.

![](https://substackcdn.com/image/fetch/$s_!fZfr!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9115c329-3e48-46c3-b27b-dd6b2640c0eb_2016x838.png)

### 7.6 What actually gets trained

Before moving on, it is worth saying plainly that **the objective is the paper**. Everything we have built over the last four sections, the joint prior, the isotropic Gaussian target, the sliced characteristic-function test, is the contribution. What follows is scaffolding, and the paper treats it that way too; there is no clever architecture here, no novel augmentation scheme, no training trick. That is rather the point. If the objective is right, the rest should be boring.

#### The encoder is arbitrary.

f\_θ appears nowhere in the derivation except as the thing producing Z, so LeJEPA imposes no architectural requirement whatsoever. The paper pretrains roughly 50 architectures from 8 families, taking every model in timm under 20M parameters, and all of them learn useful representations. A method carrying architectural anti-collapse machinery inherits assumptions about the architecture; a constraint stated purely on the output distribution does not care what produced it.

#### No predictor.

This is stronger than “optional”. Prior work established that predictors in image JEPAs, absent genuinely asymmetric views, exist primarily to prevent collapse, and removing them collapses the encoder to chance level. With SIGReg in place the paper removes both the predictor and the teacher–student architecture without collapse, and recommends training without a predictor. A teacher–student setup still gives ViTs a small boost, but as stochastic weight averaging rather than as a collapse guard.

#### No register tokens.

Recent vision models need register tokens to avoid training instabilities. The paper’s position is that those instabilities come from poorly conditioned objectives, and LeJEPA is stable with or without them.

#### Views follow the DINO setup.

Eight views total, two global at 224×224 and six local at 96×96. Nothing exotic, and the configuration common in prior work transfers directly.

#### Training data.

ImageNet-10, ImageNet-100 and ImageNet-1k for the main runs, and the in-domain experiments pretrain directly on the target corpus, including Galaxy10 (11,000 samples, 10 classes), Food101, Flowers102, CIFAR-10 and CIFAR-100. Worth noticing what is absent: no curated billion-image collection and no data-filtering pipeline, which is a meaningful contrast given that recent progress in this area has come substantially from data curation rather than from objectives.

#### The recommended settings.

Unusually for this kind of article, I can just list them, because there are so few: λ = 0.05, two global and six local views, batch size at least 128, 1024 slices, 17 quadrature knots over an integration domain of \[−5, 5\], AdamW with standard linear warmup and cosine annealing on the learning rate and no scheduler on weight decay. The ablations show none of these choices is delicate; the paper’s own summary is that while some settings slightly improve performance, none of them leads to catastrophic collapse.

![](https://substackcdn.com/image/fetch/$s_!4fbc!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F987a3bda-5a7f-4838-bfb2-de3c57a80f29_7536x4508.png)

### 7.7 The complete objective

Two pieces remain to be written down properly, and the first is more interesting than it looks.

**The prediction loss.**

The natural way to write “all views should agree” is as an average over all pairs of views:

*L\_pred = (1/V\_g) Σ\_{v=1..V\_g} (1/V) Σ\_{v′=1..V} ‖ z\_{n,v} − z\_{n,v′} ‖²*

which looks like it costs V\_g × V comparisons. It does not. The paper shows (Appendix B.6) that this collapses exactly into a distance-to-the-mean:

*L\_pred = (1/V) Σ\_{v′=1..V} ‖ μ\_n − z\_{n,v′} ‖², μ\_n = (1/V\_g) Σ\_{v=1..V\_g} z\_{n,v}*

The algebra is a pleasant little identity; expanding the squared norms, the cross terms reorganize into the mean and the pairwise structure disappears. So every view predicts the average of the global views, and the cost is linear in the number of views rather than quadratic. There is no predictor network anywhere in this expression.

**The total loss.**

The two terms combine as a convex combination rather than an unbounded penalty:

*L\_LeJEPA = λ · (1/V) Σ\_v SIGReg( { z\_{n,v} } ) + (1 − λ) · (1/B) Σ\_n L\_pred( { z\_{n,v} } )*

*with λ = 0.05 recommended as a robust default.*

Note that SIGReg is applied per view and then averaged, rather than to all views pooled together. And note the shape of the combination: λ sits in \[0, 1\] and trades the two terms against each other directly, which is a slightly different object from the Lagrange multiplier we derived in Section 3. The Bayesian derivation still tells you why there are exactly two terms and what each one is; the convex form is the practical parameterization, and it has the pleasant property that λ is bounded and interpretable rather than needing a scale search.

That is the whole method. One predictive term, one constraint term, one hyperparameter. No teacher, no stop-gradient, no predictor, no schedule, no whitening, no negatives, no register tokens.

![](https://substackcdn.com/image/fetch/$s_!JFKS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F390123e6-c2a5-4d08-a00e-fcb893a50b93_1898x1360.png)

It is worth pausing on how much of that objective we derived rather than read. The form came from Bayes in Section 3, the target came from downstream risk in Section 6, and the divergence came from the requirements list in Section 5 plus a theorem from 1936. The only genuinely free choices left are λ, the number of slices, and the quadrature grid, and of those only λ meaningfully changes what the model learns.

Next, what this looks like as code.

---

## 8\. SIGReg in code

The paper gives its implementation in full, and it is short enough to walk through line by line. What follows is Algorithm 1 from the paper, split into pieces, with Algorithm 2 for the full loss at the end.

### 8.1 The signature

```markup
def SIGReg(x, global_step, num_slices=256):
    # x is an (N, K) tensor of embeddings
    dev = dict(device=x.device)
```

Everything the constraint needs is in that first argument plus a step counter. No teacher weights, no momentum buffer, no queue of past embeddings, no temperature schedule. The global\_step is not used for annealing anything; it is a random seed, and the next fragment explains why.

### 8.2 Directions

```markup
g = torch.Generator(**dev)
g.manual_seed(global_step)
proj_shape = (x.size(1), num_slices)
A = torch.randn(proj_shape, generator=g, **dev)
A /= A.norm(p=2, dim=0)
```

Gaussian samples, normalized to the unit sphere. That is the standard way to draw uniformly from a sphere, and it is genuinely just randn; the paper discusses low-discrepancy sequences in its appendix but notes they do not change the asymptotic bounds, and the shipped implementation does not use them.

The seeding is the detail worth noticing. Every device seeds its generator with the same global\_step, so every device draws the *same* directions on the same step without any communication. And because the seed advances every step, the directions are resampled continuously, which is exactly the compounding-coverage effect from 7.3. One line buys both distributed consistency and the escape from the curse of dimensionality.

### 8.3 Projection

```markup
x_t = (x @ A).unsqueeze(2) * t              # (N, M, T)
```

The projection itself is x @ A, taking an (N, K) batch to (N, M). **After this, K never appears again.** Everything downstream is one-dimensional statistics on M columns. The unsqueeze and multiply broadcast each projected scalar against the integration grid, giving an (N, M, T) tensor which is the largest thing this function allocates, and which is linear in all three of its dimensions.

### 8.4 The integration grid

```markup
t = torch.linspace(-5, 5, 17, **dev)
exp_f = torch.exp(-0.5 * t**2)
```

Seventeen points spanning \[−5, 5\]. The exp\_f term does double duty; it is both the characteristic function of the standard Gaussian, e^{−t²/2}, which is our target, and the Gaussian window used to weight the integrand. That the two coincide is a convenience of targeting a Gaussian.

Seventeen knots sounds coarse for a numerical integral. The ablation shows the choice barely matters, and the reason is instructive: the characteristic function is accurate near zero, so the moments of the distribution are well characterized even over a modest integration range.

### 8.5 The empirical characteristic function

```markup
ecf = (1j * x_t).exp().mean(0)
ecf = all_reduce(ecf, op=”AVG”)
```

The first line is the empirical characteristic function, computed as a complex exponential averaged over the batch, collapsing (N, M, T) to (M, T). Using complex tensors directly keeps the real and imaginary parts together, and both carry information; the real part sees deviations that are symmetric about the mean, the imaginary part sees asymmetric ones.

The second line is the entire distributed story. An empirical characteristic function is a mean over samples, and means compose across shards, so one all-reduce of an (M, T) array, a few thousand complex numbers, gives exactly the result you would have obtained on a single device. Nothing depends on N, K, or the device count. This is why the paper can claim fifty lines.

### 8.6 Comparing to the target

```markup
err = (ecf - exp_f).abs().square().mul(exp_f)
N = x.size(0) * world_size
T = torch.trapz(err, t, dim=1) * N
return T
```

The weighted squared discrepancy, integrated over frequency by the trapezoidal rule and scaled by the global batch size. Note that N is the *total* across devices, not the local batch, which matters because the Epps–Pulley statistic is defined with that scaling.

This is also where boundedness becomes visible as code. ecf is an average of complex exponentials, so its magnitude is at most one no matter what the embeddings do; an embedding sitting at 10⁶ contributes a point on the unit circle, exactly like every other embedding. Put a kurtosis penalty in the same position and that embedding contributes 10²⁴. **No single input can dominate this statistic**, which is Theorem 4 arriving as an operational fact.

One thing this function does not do is take a maximum. The return value is a per-direction vector, and the averaging happens in the caller. As we saw in 7.3, that is deliberate.

### 8.7 The full loss

```markup
def LeJEPA(global_views, all_views, lambd):
    g_emb = forward(torch.cat(global_views))
    a_emb = forward(torch.cat(all_views))
    centers = g_emb.view(-1, bs, K).mean(0)
    a_emb = a_emb.view(-1, bs, K)
    sim = (centers - a_emb).square().mean()
    sigreg = mean(SIGReg(emb, global_step) for emb in a_emb)

    return (1 - lambd) * sim + lambd * sigreg
```

Eight lines. The centers variable is μ from 7.7, the mean of the global-view embeddings, and sim is every view’s squared distance to it, which is the collapsed all-pairs loss. There is no predictor and no second network; forward is called twice on the same encoder. For non-ViT architectures the paper simply sets global\_views = all\_views and the local-view machinery disappears.

![](https://substackcdn.com/image/fetch/$s_!6FHD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a2e3988-b23d-4ed4-ab29-15e17cd70080_1004x1060.png)

SIGReg is applied per view and averaged, and the two terms combine convexly through λ. That is the entire training step, minus the optimizer.

### 8.8 Complexity, totalled

The paper states the implementation is O(N) in both time and memory with respect to the minibatch size, and reports wall-clock timings. Reading the operations directly: the projection is O(NKM), the characteristic function is O(NMT), and the reduction is O(MT), giving

*O( N. M ( K + T ) )*

linear in batch size, linear in embedding dimension, linear in slices. To put numbers on it, at N = 512, M = 512 and 16 integration points the forward-backward pass costs about 0.47 ms on a V100, and holding N fixed while raising M from 512 to 8192 takes it only to about 0.67 ms. Against an encoder forward pass, this is a rounding error.

![](https://substackcdn.com/image/fetch/$s_!0IQ1!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff71f0a78-18d7-4726-9cc7-ae78ce13eeb0_2788x920.png)

---

## 9\. Results & Outcomes

A derivation can be elegant and still lose to a pile of heuristics that somebody tuned for two years, so what follows is the empirical case. The paper’s validation spans more than ten datasets and over sixty architectures at scales approaching two billion parameters. I have grouped the findings into five, roughly in order of how much each one surprised me.

### 9.1 Stability across hyper-parameters and architectures

LeJEPA trains stably across every hyper-parameter the authors varied and across roughly 50 architectures from 8 families, using a single value of λ.

The architecture sweep is the cleanest demonstration. The authors took every model in the timm library under 20M parameters, 50 of them spanning ConvNeXt, EfficientNet, Inception, LeViT, MaxViT, MaxxViT, ResNet and ViT, pretrained each on ImageNet-10 with the same recipe, and evaluated with a frozen backbone. All 50 land between **91.5% and 95% top-1**, which is a remarkably narrow band for a set of models that different. The paper’s practical note is that architectures which do well under supervision also do well here, so ResNets and ViTs are the sensible starting point over specialized designs like EfficientNet.

![](https://substackcdn.com/image/fetch/$s_!vUvE!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9776e93d-b86a-4b26-9514-00c8d596ffe3_2778x1248.png)

On hyper-parameters, the headline is that nothing is delicate. Varying λ across two orders of magnitude on ImageNet-100 with a ResNet-50 leaves performance stable, with the optimum drifting slightly upward as the number of views increases. On ImageNet-1k with a ViT-Large/14, the ablations cover the Epps–Pulley integration domain, the number of quadrature points, the number of slices, batch size, projector dimension and register tokens. The paper’s own summary is the right one to quote in spirit: while some settings slightly improve performance, **none of the choices leads to a catastrophic collapse**.

![](https://substackcdn.com/image/fetch/$s_!ibHD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbda096bc-0f50-4b5f-a5e9-7e1f1a37be09_1186x1104.png)

Two details worth pulling out. Competitive performance holds at batch sizes as small as 128 on ImageNet-1k, which suggests noticeably lower memory requirements than methods needing large batches for negatives. And the number of slices has only a modest effect, with 512 already competitive and 1024 recommended.

The removal results are the ones that most directly vindicate the theory. Prior work established that predictors in image JEPAs and teacher–student architectures exist primarily to prevent collapse, and that removing them yields encoders at chance level. With SIGReg in place the paper removes both and trains fine. A teacher–student setup still helps ViTs slightly, but as stochastic weight averaging rather than as a collapse guard. Register tokens, introduced elsewhere to stabilize vision transformers, turn out to be unnecessary too, and the paper’s read is that those instabilities were symptoms of poorly conditioned objectives rather than facts about the architecture.

![](https://substackcdn.com/image/fetch/$s_!SJe4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e1d076d-8048-45a9-b0ae-fe7ededf865c_2310x526.png)

### 9.2 The training loss predicts downstream accuracy

LeJEPA’s training loss correlates with downstream linear-probe accuracy at roughly **85% Spearman** out of the box, rising to nearly **99%** under a simple rescaling, which makes it usable for label-free model selection.

This is the result I did not expect, and the most practically useful one in the paper. Ordinarily an SSL pretraining loss tells you almost nothing about representation quality; a contrastive loss can fall steadily while the representation quietly loses rank, which is exactly the dimensional collapse from Section 2 and is invisible in the curve. The paper notes that in recent JEPA models the training loss may not even decrease monotonically. So the standard workflow is to checkpoint, freeze, fit a probe on labelled data and read the accuracy, meaning every model-selection decision inside a supposedly unsupervised procedure secretly requires labels.

The rescaling is worth stating because it is so simple. Correlate the loss divided by a power of the trade-off parameter:

*C(α) = ρ\_s ( train\_loss / λ^α, test\_accuracy )*

At α = 0 you recover the plain training loss, already strongly correlated. At α ≈ 0.4 the correlation reaches nearly 99% across multiple datasets and architectures, with the individual curves running from 0.60 to 0.95 on ResNet-18 with Flowers102, and 0.90 to 0.98 on ViT-S/8 with ImageNet-10. The entire set of points is collected across variation in learning rate, weight decay, epoch count and λ, so this is not a within-run artifact.

![](https://substackcdn.com/image/fetch/$s_!kGQC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F08e794bd-c3fd-4101-afa4-c8a9bf881d6b_2382x844.png)

![](https://substackcdn.com/image/fetch/$s_!7fKD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb14357bc-1c05-4fd0-a5aa-07f4e9a8b6e0_1114x844.png)

Why does LeJEPA behave differently? The answer follows from Section 6, and it is worth stating because the paper reports the observation more than it explains it. The SIGReg term is not a proxy for downstream performance, it is a direct estimate of the quantity the theory says *governs* downstream performance. If the isotropic Gaussian argument is correct, the loss ought to predict the probe. That it empirically does, at 99% correlation, is the strongest available evidence that the argument describes something real rather than merely being internally consistent.

![](https://substackcdn.com/image/fetch/$s_!gF9G!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2701b745-5a27-47e1-b8d7-e206946001b4_2338x1196.png)

There is a nice secondary observation in the loss plane. Different values of λ trace out trade-off fronts between the two terms that produce similar downstream accuracy, and those fronts are linear and point towards the lower-left corner. Which is to say the two terms are not fighting each other in any complicated way; you want both small, and λ decides how you get there.

### 9.3 In-domain pretraining outperforms frontier transfer

On Galaxy10, LeJEPA pretrained directly on the target data with a small backbone outperforms DINOv2 and DINOv3 transferred from natural images, across every data regime from one sample per class to the full set, under both frozen-backbone linear probing and full finetuning.

The setup deserves stating because it is deliberately unflattering to LeJEPA. Galaxy10 is a galaxy-morphology task with **11,000 training samples across 10 classes**, visually and statistically remote from natural images. The paper pretrains a variety of backbones on it for 400 epochs using default hyper-parameters, no tuning, and compares against DINOv2 (trained on LVD-142M) and DINOv3 (trained on LVD-1.7B).

![](https://substackcdn.com/image/fetch/$s_!gVE4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F69156f35-633a-4847-a384-bcf55925f732_2380x1046.png)

Reading the frozen-backbone column, which is where representation quality shows most directly: LeJEPA ResNet-34 reaches 78.17 against DINOv3’s 71.38 and DINOv2’s 67.62 on the full set, and the gap holds at every sample count down to one per class. Under full finetuning the same ResNet-34 reaches 83.28 against 81.60 and 78.34. A 21M-parameter model trained from scratch on eleven thousand images beats a model pretrained on 1.7 billion.

![](https://substackcdn.com/image/fetch/$s_!DM_v!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a98e19b-d2c8-4300-8c84-ca8cdb81a61a_1558x938.png)

The effect is not confined to astronomy. Across six datasets the paper shows in-domain LeJEPA competitive or better, including Flowers102 with only **1,020 training samples**, where a ResNeXt-26 reaches 82.19 from scratch. The one place frontier transfer still wins comfortably is where you would expect it to, on natural-image datasets like CIFAR and ImageNet-10 where I-JEPA pretrained on ImageNet-22k has an enormous head start.

![](https://substackcdn.com/image/fetch/$s_!D2XN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3cfdbf7c-20b1-42a9-9ead-98e0d382f291_1866x536.png)

Why this matters beyond the leaderboard: the received wisdom is that in-domain SSL on a small dataset is not worth attempting, because you cannot out-train a foundation model pretrained on a billion curated images, so you transfer and finetune instead. That wisdom formed when SSL required careful per-dataset tuning and collapsed if you got it wrong, which made in-domain pretraining an expensive gamble on a dataset too small to justify it. Take away the tuning and the gamble disappears, which suggests the received wisdom was partly an artifact of the methods rather than a fact about the data.

### 9.4 Scaling across data and models

On ImageNet-1k, LeJEPA reaches **77.1% online linear probe with a ViT-Large (0.3B)** and **78.5% with a ConvNeXtV2-Huge (0.6B)**, and transfers better than I-JEPA while using a smaller model and a third of the training schedule.

The transfer comparison is the more informative one. Against I-JEPA with a ViT-Huge (0.6B), across eight datasets spanning textures, objects and fine-grained categories, LeJEPA ViT-L (0.3B) averages 79.48 to I-JEPA’s 78.50 in the all-shot setting, while training for **100 epochs against I-JEPA’s 300**. That is roughly a threefold reduction in training cost with a model half the size, and the margins are widest exactly where you would hope, on fine-grained tasks; DTD 78.30 against 73.32, Food101 82.05 against 81.02, Flowers102 91.21 against 86.47.

![](https://substackcdn.com/image/fetch/$s_!mWhP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3836282a-9707-4abe-a581-d86e0b375ebd_2426x1314.png)

On the largest run, a ViT-gigantic at 1.8B parameters trains with a smooth, stable loss curve and no special handling, which the authors attribute directly to the bounded-gradient guarantee from Theorem 4.

![](https://substackcdn.com/image/fetch/$s_!hFAe!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6df71721-487d-47d1-8661-500ecda90ae5_2262x768.png)

Worth framing carefully, because this is easy to over- or under-sell. These are not state-of-the-art numbers in absolute terms; heavily tuned DINOv2 and DINOv3 systems reach higher on ImageNet. What they are is competitive numbers produced by an objective with one hyper-parameter and no heuristics, at a fraction of the training budget. The useful comparison is not whether 78.5% wins the benchmark, but how much was given up by deleting the teacher, the predictor, the stop-gradient, the schedulers, the whitening and the register tokens, and the answer appears to be less than one would expect.

### 9.5 Emergent semantic structure

PCA of last-layer features from an ImageNet-1k pretrained LeJEPA ViT-Large shows clear object–background separation, and thresholding the attention maps yields object segmentation and tracking across video frames without any segmentation supervision.

Projecting the first three principal components to RGB gives images in which warm colours consistently pick out foreground objects and cool colours pick out background and foliage. This is the DINO-style qualitative check, and LeJEPA passes it.

![](https://substackcdn.com/image/fetch/$s_!y4bK!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c20c1fe-5cbe-47bd-b8b1-4d0714f97b25_1176x1168.png)

The video result goes further than I expected. Thresholding the self-attention of the \[CLS\] token produces binary masks that track salient objects across frames with reasonable temporal coherence, again with no segmentation labels anywhere in training.

![](https://substackcdn.com/image/fetch/$s_!TO-2!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31c9b7cc-ac20-4d55-8243-39d06db3c1ff_2440x528.png)

This is soft evidence and I would not lean on it hard, but it is a good consistency check. Nothing in SIGReg mentions semantics; the constraint only says the embedding cloud should be an isotropic Gaussian. Semantic organization appearing along the principal directions anyway is what you would hope for if the predictive term is doing its job and the constraint is genuinely neutral about *what* gets represented, caring only about how the mass is arranged. The authors’ framing is that a stability-focused objective does not sacrifice semantic richness, and on this evidence that holds.

### 9.6 Limitations of the evidence

Three things the results do not establish, which are worth stating plainly.

1. **Vision only.** Every experiment is on images. The Section 6 theory makes no reference to modality, since the risk argument concerns probes and distributions rather than pixels, so there is no principled barrier to audio, text or time series. Nobody has demonstrated it, and “should transfer” has a poor track record here.
2. **No matched-compute comparison against the strongest baselines.** The I-JEPA comparison is careful and favourable, but DINOv2 and DINOv3 are compared only in the in-domain setting where they are transferring rather than training in-domain. The experiment that would settle the general question is DINOv3’s exact data, architecture and compute with only the objective swapped, and nobody has run it.
3. **“One hyper-parameter” is generous.** True of the objective, and it excludes learning rate, weight decay, batch size, augmentation policy and architecture, all of which still require choosing; the paper cross-validates learning rate and weight decay in its architecture sweep. The accurate claim is that LeJEPA eliminates the hyper-parameters specific to preventing collapse, which is a real reduction but not a single knob in total.

What I will like to point out is that the limitation I expected to find is not there as I assumed the number of slices would be an underexamined knob hiding a lot of sensitivity, since it controls how well the Cramér–Wold approximation holds. The paper ablates it directly, bounds it theoretically, and shows that resampling makes small values work.

---

## 10\. Thoughts

**1\. The heuristics were never wrong, they were unnamed.**

Every mechanism from Section 4 was groping towards a constraint on the embedding distribution without stating what it was. VICReg got the second moments, whitening got the correlation structure, negatives got the spread. All three are shadows of “be isotropic Gaussian” seen from different angles. The field was doing empirical science on an objective nobody had written down, and each heuristic was a partial measurement of the same object.

**2\. The loss does not predict performance, it measures it.**

The 99% correlation is under-sold in the paper. Operationally it means architecture search, hyper-parameter selection and early stopping without touching a label, which removes the most annoying dependency in the pretraining workflow. But the reason matters more: SIGReg estimates the quantity that provably bounds downstream risk. If that framing is right, any objective built on a proven risk bound should behave this way, and the loss-tells-you-nothing era was a symptom of under-specified objectives rather than a fact about self-supervision.

**3\. Gaussianize once, or Gaussianize always?**

In [TurboQuant](https://vizuara.substack.com/p/turboquant-online-vector-quantization) the central move was a Hadamard rotation applied to KV-cache vectors so that, by CLT, their coordinates become approximately Gaussian, because a known distribution lets you precompute an optimal Lloyd-Max codebook. The whole method manufactures Gaussianity at inference because the model did not provide it.

LeJEPA trains the representation to be Gaussian in the first place. So: **if you train with SIGReg, do you still need the rotation?** A model whose hidden states are natively isotropic Gaussian is already in the distribution Lloyd-Max wants; skip the Hadamard, skip the online scale estimation, quantize directly.

Both papers want the same target for the same reason and arrive from opposite ends, one post-hoc because it cannot change the model, one during training because it can. Both lean on random one-dimensional projections to make a high-dimensional problem tractable; TurboQuant to preserve inner products under sign quantization, LeJEPA to test distributional fit. The same tool pointed in opposite directions.

**4\. Isotropic is right only if you are genuinely not betting.**

The isotropic Gaussian is optimal for *worst-case* risk over an unknown task family, which is exactly right for a foundation model and not obviously right when you know a lot about your downstream use. There, worst-case optimality means declining to use information you have. SIGReg does not care what Q is; the machinery works for any target whose one-dimensional projections you can write down. A task-informed, deliberately anisotropic Q is the most immediately actionable gap I can see.

**5\. What happens in language?**

Every experiment is vision and the theory is modality-agnostic, so text is the obvious move. I suspect it is harder than it looks: LLM embeddings are famously anisotropic, the cone effect, and there is an argument that the anisotropy encodes real structure about token frequency rather than being pathology. Forcing isotropy might destroy something the model was using. Or the cone is dimensional collapse we have been rationalizing for years because we had no principled reason to object. Section 6 gives us that reason now.

**6\. The contribution is the question.**

The contribution is not SIGReg, and not the isotropic Gaussian result either. It is asking *what distribution should the embeddings follow*, which nobody had posed in that form. Once asked, the answer is a fairly standard exercise in bias-variance and Fisher information, and the implementation is a statistical test from 1983 wrapped in a theorem from 1936. None of the pieces is new; the framing is. Worth remembering when reading papers for techniques to borrow, since the technique here is a fifty-line function, but the thing worth stealing is the habit of asking what the correct answer would look like before going to find one.

---

## 11\. Conclusion

We talked about self-supervised learning, and specifically about the part of it nobody could justify. Stop-gradients, EMA teachers, whitening, negatives, register tokens; all found by trial and error, all kept because they prevented collapse.

The route out was taking Yann’s framing seriously. If SSL is constrained optimization, the constraint is not a safety mechanism, it is the thing that decides what the model learns. Bayes made that precise in Section 3, giving a joint prior with two slots — one for parameters, which is classical regularization, and one for the representation, where every anti-collapse mechanism had been operating without saying so.

That turned the question from *how do we stop the model cheating* into *what shape should a representation be*, and the second has exactly one answer. A linear probe forces isotropy, since a variance budget spread unevenly always leaves some task badly served. A nonlinear probe forces Gaussianity, since neighbourhood-averaging probes are biased in proportion to Fisher information, which the Gaussian uniquely minimizes. Isotropy declines to bet on direction, Gaussianity declines to bet on location.

Enforcing it was harder. Density estimation in a thousand dimensions from a few hundred samples is hopeless, and the escape was Cramér–Wold: a distribution is determined by its one-dimensional shadows. Project onto random directions, run a characteristic-function test on each, average. The result is fully specified, bounded in gradient by construction, linear in everything you want to scale, and about twenty lines of PyTorch. Then delete the machinery, because none of it does anything the constraint does not.

The empirical case holds. Fifty architectures on one hyper-parameter. A loss predicting downstream accuracy at 99%, so model selection without labels. Eleven thousand galaxy images beating a model pretrained on 1.7 billion.

What strikes me most is how little here is new. Epps–Pulley is from 1983, Cramér–Wold from 1936, Fisher information older still. The contribution is a question nobody had asked in that form, and everything else follows from asking it properly.

Whether SIGReg becomes standard I have no idea. The durable part is the move underneath it: when something in your pipeline works and you cannot say what it guarantees, that is not a trick you have found, it is a specification you have not written.

**References:**  
LeJEPA paper: [https://arxiv.org/pdf/2511.08544](https://arxiv.org/pdf/2511.08544)  
Code: [https://github.com/rbalestr-lab/lejepa](https://github.com/rbalestr-lab/lejepa)  
Yann's NYU lecture:

![](https://www.youtube.com/watch?v=8u2s64ZtmiA)

That's all for today.  
Follow me on [LinkedIn](https://www.linkedin.com/in/siddhant-rai/) and Substack for more such posts and recommendations, till then happy Learning. Bye👋