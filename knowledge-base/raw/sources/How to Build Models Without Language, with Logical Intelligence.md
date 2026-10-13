---
title: "How to Build Models Without Language, with Logical Intelligence"
source: "https://blog.bytebytego.com/p/how-to-build-models-without-language?utm_source=post-email-title&publication_id=817132&post_id=219325762&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-10-12
created: 2026-10-13
description: "Something unusual happened in a public Sudoku experiment early this year."
tags:
  - "clippings"
---
## More AI code. More CI. Bigger CI bills. (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!Kxz4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48982efa-a7e5-4b78-abcb-bf96432d926b_1600x840.png)

AI agents write more code. More code means more commits, more CI runs and bigger CI bills. For many teams, GitHub Actions is now the bottleneck.

WarpBuild fixes that. Teams at Braintrust, Raycast, OpenRouter, Comcast and Jane Street run their CI on it.

- Twice as fast at half the cost
- One line change to runs-on, nothing else to migrate
- Linux, macOS and Windows on x86-64 and ARM64
- Unlimited macOS concurrency

Use code START50 for $50 in free credits.

---

Something unusual happened in a public Sudoku experiment early this year. According to Logical Intelligence, a panel of frontier large language models (LLMs), including OpenAI’s GPT-5.2, Claude Opus 4.5 and Sonnet 4.5, Gemini 3 Pro, and DeepSeek V3.2, collectively **only solved 2% of the puzzles and burned around $11,000 in API calls**. Interestingly, a model named Kona, about a thousand times smaller, **solved 96.2% for only $4 in GPU time** \[1\].

At first glance, the result of the demo may seem strange or unexpected, because Sudoku is not a particularly hard game to play. A ten-year-old can learn the rules and solve a puzzle after some practice. The rules are well-defined, and there is little ambiguity. It is the kind of problem that LLMs should handle easily.

![](https://substackcdn.com/image/fetch/$s_!Btiw!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92a20801-5be8-4b3b-9c11-e553abc4bba7_2048x991.png)

This gap is not really about puzzles like Sudoku. LLMs are the most capable AI models we’ve ever built around language, but many tasks require intelligence that goes beyond language. In fact, most of the tasks we face every day are not language problems. Some of them require spatial or dimensional reasoning. Others may depend on logic, planning, or just emotional awareness. And much of what we do cannot even be fully verbalized. The ability to extrapolate, to be creative, not repetitive, is what makes intelligence feel alive rather than mechanical \[2\].

Yann LeCun, a Turing Award winner and one of the pioneers of deep learning, has argued for years that text alone will not give us real intelligence.

![](https://substackcdn.com/image/fetch/$s_!XPey!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7fc5fd29-b2c2-4f2c-a6de-fee684b31032_1200x430.png)

![](https://substackcdn.com/image/fetch/$s_!BPF9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ad5e02e-d2bf-4866-9cfe-56dc5ced3d70_1198x446.png)

Yann LeCun’s X Post

We spoke with [Eve Bodnia](https://www.linkedin.com/in/eve-bodnia-351b41355/), founder and CEO of Logical Intelligence, to understand how the models her team builds, energy-based reasoning models (EBRMs) like Kona, can perform so well on constraint problems such as Sudoku, and to learn about her vision and the new paradigm of building truly intelligent systems. We thank Eve for taking the time to walk us through the work in detail.

In this article, you’ll learn:

- Where LLMs fail on constraint problems, and why.
- What energy-based latent reasoning means, and how it works.
- What EBRMs can and cannot do, and why a model like Kona works so well on certain tasks.
- Why latent reasoning with EBRMs is more reliable, and how verification and safety work differently in those systems.
- How the industry and the hardware that drives it are likely to develop.

## Language Models and Their Limitations

At its most basic, a large language model is a system designed to predict the next item in a sequence. It reads as input a sequence of previous tokens, then it selects as output the most plausible token to continue that sequence.

![](https://substackcdn.com/image/fetch/$s_!16sg!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c6dbe34-2f45-424f-b701-6512547c7ffe_2048x658.png)

The aim of this design is to achieve mastery of language. Because humans communicate and transmit knowledge using language, and because much of human knowledge is recorded in written form, if a model can master the distribution of language by being trained on texts, the human knowledge and reasoning present in the texts will come with the mastery.

![](https://substackcdn.com/image/fetch/$s_!a0ER!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8b651dd4-3b95-4c96-84d0-6f47f5f1d6d3_2048x1019.png)

There has been a dramatic development in the effectiveness of LLMs in recent years as larger and larger models have been trained on ever-increasing volumes of text. The output produced is far more useful than mere autocomplete. LLMs are now very adept at language manipulation tasks such as translation and summarization. And they can generate code.

But not all problems are primarily language-based. For problems that require other types of intelligence, are there alternatives to LLMs that would be more effective at solving them? To illustrate the answer, we will first look at how an LLM attempts to solve Sudoku, then we will look at the alternative approach that Kona uses.

The rules of the game are well defined and simple. The Sudoku grid is a square containing 81 cells divided into 9 three-by-three boxes. The player must fill all the cells with the digits 1 to 9 in such a way that the following three rules are all satisfied:

1. Each digit must appear only once in each row.
2. Each digit must appear only once in each column.
3. Each digit must appear only once in each three-by-three box.

![](https://substackcdn.com/image/fetch/$s_!rXvX!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc4b5c55-4a6b-44ea-9930-e648bf1fe922_1318x1072.png)

An LLM attempts to solve Sudoku by producing one token at a time, in this case, placing digits into cells one at a time. Before producing a token, the model reads the entire grid. Then it bases its selection on the tokens that have been produced before it. The LLM steps its way to the completed grid in this manner, token by token.

![](https://substackcdn.com/image/fetch/$s_!BV6U!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fe787f2-682d-4a29-ba95-4fc3ed8e7cc7_2048x631.png)

But LLMs have never been good at solving the type of problem presented by a Sudoku puzzle. The best LLM in the demo had a success rate of only 6.9%. It failed 93% of the time \[1\].

There are two primary reasons why an LLM finds it hard to play Sudoku. The first is because an LLM generates tokens from left to right. The order in which the digits are placed depends on the prompt. Suppose the grid is written out row by row, so digits are placed in row 1, then row 2, and so on. If the model places a digit in row 2 that will collide with the digit it later needs in the same column of row 7, the column rule is broken. But because it generates from left to right, it does not discover the collision until it reaches row 7. Once it realizes the problem, it has to go back and regenerate everything from where the mistake was made in row 2. Any other order has the same problem: whatever the model commits to early, it cannot revise later without regenerating. Thus, the way an LLM operates makes fixing earlier mistakes expensive.

![](https://substackcdn.com/image/fetch/$s_!aRIp!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff1884424-ce7d-45ce-b18a-342052dee357_2048x822.png)

The second reason that LLMs struggle with Sudoku is because their output is discrete. Tokens (e.g., the digits 1 to 9) are the smallest units that LLMs learn or produce. For a given cell on the grid, the digit placed in it is either correct or incorrect; there is no way to move an answer slightly closer to correctness. Instead, the only option is to discard the digit and sample a new one from the same discrete set.

Sudoku is merely one example of where these two challenges exist. Left-to-right generation and discrete output are, in fact, foundational limitations of LLMs \[3\], and they emerge as problems whenever a candidate answer has to satisfy multiple constraints simultaneously. Chess and Go, games where every choice depends on every other choice, are examples of constraint satisfaction problems. Chip design, industrial control, energy grid optimization, and trading systems are all activities that operate under interacting constraints. Constraint satisfaction problems need logic more than language to solve them.

![](https://substackcdn.com/image/fetch/$s_!5hoz!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7133f778-727a-43e1-88e3-1b9d8ca44a86_2048x1270.png)

So, through the example of Sudoku, we have demonstrated that language is not always the most effective way to solve every problem. For further illustration, consider what your brain is doing right now as you read these sentences. As well as reading the words, you may also be annoyed by the noise in the other room and simultaneously decide that it’s time to get up soon and make your next cup of coffee. None of those things need to be verbalized to be acted upon. You sit up straighter as you read; you go and get that coffee once you’ve finished this sentence.

Your brain is a model that can do multiple things at once, and they don’t all require language. In addition to taking in words as you read, your brain scans its environment continuously. From the various inputs it receives, it makes predictions and acts on them. No words necessary.

![](https://substackcdn.com/image/fetch/$s_!G360!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc5e6d7e6-828b-43fb-ab7d-81e2153583ec_2048x1016.png)

An LLM manipulates and recombines recorded facts, and skillful recombination can look like new knowledge. That is why LLMs do so well at mathematics, where much of the work is combining known facts. Language is indeed a powerful tool in the development of knowledge. But language itself is not intelligence, and it does not give all the answers.

According to Bodnia, in many situations, rather than language, we need extrapolation: the ability to take a rule learned in one place and apply it to another.

Our brains think in abstractions, and language performs the function of a user interface between brains. Thus, language is the interface to intelligence, not the intelligence itself.

If language is only the interface, how do we model the intelligence behind it?

## Latent reasoning with Energy-Based Models

Latent reasoning models differ from LLMs in that they work with latent variables instead of discrete tokens. Logical Intelligence works with the class of latent reasoning models known as energy-based reasoning models (EBRMs). This section describes energy-based models and how they are trained, then it explains how they produce answers. Then we will look at how the reasoning is developed in a latent space. (Note that the technical details described here are the general requirements for energy-based reasoning, not a specific description of Kona’s internals.)

### What is an energy-based model?

In contrast to a language model, which is simply a generator that takes an input and produces an output, one token at a time, an energy-based model (EBM) does not generate anything. Instead, an EBM learns a function, E(x, y), that takes a problem, x, and a candidate answer, y, and returns a number referred to as the energy. A lower energy indicates the answer is more consistent with the problem, and a higher energy indicates it is less consistent \[4\]. The lowest energy achievable for a given problem indicates the correct answer.

![](https://substackcdn.com/image/fetch/$s_!D7Q0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7171652e-c3e3-49c7-b2bf-67ab8efbeee1_2048x1329.png)

The neural network of an EBM defines a landscape over all possible answers, where the best answers are found in valleys and the worst answers are found on peaks, with a continuum of intermediate answers found on the slopes, moving toward correctness as they descend. The next two sections cover how the landscape is learned (training) and how an answer is found on that landscape (inference).

![](https://substackcdn.com/image/fetch/$s_!M3kw!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9157852c-c3b1-43f9-9c40-d8653bd02048_2048x1000.png)

### How an EBM is trained

The goal of training an EBM is to get it to assign low energies to correct answers and high energies to wrong answers. This is done using a standard contrastive loss function, which compares incorrect answers to a problem to the correct one \[4\].

Consider a problem, x, and its correct answer, y+. Pair it with a wrong answer, y-, for the same problem. The EBM computes the energy of both, and the contrastive loss function asks that E(x, y+) be lower than E(x, y-) by some margin. If the required margin already exists, nothing changes. If not, backpropagation is employed to adjust the network weights to lower the energy of the correct answer and raise the energy of the wrong one. The answers are not changed during training, only the weights.

![](https://substackcdn.com/image/fetch/$s_!WtbC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e4fc551-a231-4613-90a6-920d3da728a2_2048x1025.png)

EBM training requires the existence of wrong answers to build a useful landscape. Without wrong answers, every answer would be assigned the same low energy and the landscape would be flat.

The simplest way to create a wrong answer is to corrupt the correct answer, for example, swapping a few digits in a completed Sudoku grid. But the model itself can be used to provide wrong answers. This can be done by running several steps of the same search for descending energy gradient that the model uses to answer questions (see the next section) and using whatever it returns as the wrong answer y-. The contrastive loss function will raise the energies of all wrong answers until, through repetitive training, only correct answers are found in the valleys.

![](https://substackcdn.com/image/fetch/$s_!ERKa!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09fe404a-0c87-4570-877f-cecf48f3d6d4_2048x1174.png)

Naturally, Logical Intelligence did not give us specific details about how Kona was trained. But they did tell us that they trained it on unfinished Sudoku solutions, with half of every grid hidden and no reinforcement learning. And yet the model still learned the rules and produced complete, correct grids at test time \[1\].

Chess offers another interesting experiment, because unfinished chess games are the norm. Serious competitors and professional players will concede defeat when they see they are going to lose. As a result, most recorded games do not end with checkmate. Could a model trained on unfinished games play one through to the very end? According to Bodnia, yes, it could.

After the training of an EBM is complete, correct answers will sit at the bottoms of valleys and wrong answers will be found at higher levels. The resulting landscape will be continuous. This continuity is a useful and necessary property because it means that when a search descends into a valley to answer a question, each successive downward step will produce a candidate answer more compatible with the rules than the last.

![](https://substackcdn.com/image/fetch/$s_!jQrG!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9816200-f181-4614-9c66-573bc14eae8e_2048x1087.png)

### How inference works

An EBM model finds correct answers by assessing their energies. It keeps going until it has found the answer with the lowest energy. And it moves in the direction of that correct answer by following the descending energy gradient until it drops no further.

The first candidate answer to be assessed is random noise. The model computes the energy of that candidate, then it moves the candidate a small step in a direction that lowers the energy. This movement in the direction of lower energy continues until the energy stops going down. The candidate answer is then read out in the form required by the task. For a Sudoku puzzle, this means placing the correct digit into each cell.

![](https://substackcdn.com/image/fetch/$s_!S09T!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd542a276-3841-4f7f-9bc4-fb10db98c6d4_2048x1336.png)

Since the search continues until the energy no longer falls with subsequent movement, the number of steps required to find the answer is not fixed. An easy input such as a Sudoku grid with a larger number of cells already filled will allow the correct answer to be found quickly (i.e., in fewer steps), and a harder input will require more steps. An EBM spends more computation on harder problems by requiring extra steps, similar to how a reasoning language model spends more tokens. In practice, though, the search is quick compared to an LLM. In the Sudoku demo, Kona settled in 313 milliseconds on average. The LLMs took up to 90 seconds for a single puzzle.

![](https://substackcdn.com/image/fetch/$s_!QsVd!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05b5df27-efca-455f-89ef-382cca56a9be_2048x743.png)

The search function relies on the fact that the landscape is continuous. Without continuous values, there would be no gradients and, thus, no indication of which direction to move toward the correct answer. To achieve this continuity, the candidate answers in an EBM are always represented by continuous numbers. For Sudoku, each cell holds nine scores, one per digit. For a text problem, each position holds a vector of scores over the vocabulary, rather than a token ID.

![](https://substackcdn.com/image/fetch/$s_!fv6z!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2951c0aa-f229-4165-b1ce-8b30ed46738a_2048x1139.png)

### Reasoning in a latent space

So far, the energy of the candidate answer has been used to determine the final answer directly. This approach is appropriate when the answer can be checked on its own, for example, on a Sudoku grid. But many answers carry no trace of how they were reached. For example, a plan may move through many states before it ends in a single number or action. An energy function that scores only (x, y) can judge the whole chain of reasoning only by that one output. Two answers a digit apart may have been reached through completely different reasoning; thus, a tiny change could swing the score from good to bad. That scenario would break gradient descent, which relies on small changes producing small improvements.

The fix is to have the energy function evaluate the steps. Instead of scoring only the final pair (x, y), the model scores every intermediate state against the problem: (x, z1), (x, z2), …, (x, zT), where z1 to zT is a sequence of intermediate states and each zT is a vector. This sequence is the reasoning; thus, the energy function evaluates the reasoning when it evaluates each state in the sequence.

The intuition above is similar to how we work through problems. We hold a partial picture in mind; we adjust it; if we notice a conflict, we adjust it again. Only at the end do we put the result into words. The words are just the output format.

Bodnia pointed out that with reasoning in a latent space, the search is run over the model’s own compressed account of the data. In her words, “you’re navigating the understanding, rather than the data.”

![](https://substackcdn.com/image/fetch/$s_!jIob!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F141d1129-2d6d-41ab-b825-61bf8a42abc6_2048x1028.png)

Training of reasoning in the latent space employs the same contrastive loss function, applied now to sequences. The states along a sequence that ends in the correct answer are pushed to low energy. The decoder is trained alongside, to read the correct answer out of the final state. The exact losses will differ between implementations, but they are immaterial.

Producing an answer works the same way as before, but applied to the sequence. The problem is encoded into the latent space, and the rest of the sequence starts as random noise. The model then adjusts the whole sequence at once. Every step moves together until the energy settles. The final state is passed to a decoder, a separate small network that converts it into the form the task requires.

Inference on the sequence follows these 5 steps:

1. Encode the problem into the latent space.
2. Start the sequence from the encoded problem, with every later step set to random noise.
3. Score each state against the problem. A state that breaks the rules shows high energy.
4. Adjust the states to lower their energies.
5. Repeat until the energy settles, then pass the final state to the decoder.

![](https://substackcdn.com/image/fetch/$s_!HqgG!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee922adc-07eb-42af-b462-6242dd57a6d1_2048x953.png)

## Energy-based reasoning versus language models

Autoregressive language modeling and energy-based latent reasoning are two very different methods of modeling intelligence. Which model best fits a given problem is determined by a single question: Can the correct answer be defined precisely?

An EBRM learns from correct and wrong answers. Therefore, it is suited for tasks where correctness can be verified. For example, in Sudoku, a filled grid is either correct or incorrect. A simple program can check the correctness of a candidate grid. Thus, the energy function has something clear to learn. This is why an EBRM will solve Sudoku reliably while language models will usually fail. Formal mathematics and planning have the same property, meaning that a proof checker or a constraint solver can act as the final judge.

![](https://substackcdn.com/image/fetch/$s_!8Zm_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ecc65c7-f43d-4bb7-bf9e-7a697a627800_2048x1337.png)

When correctness is vague, the advantage flips to language models. Whether an essay is well argued or a business recommendation is sound depends on judgment. An energy function trained on such data would produce a vague, undefined landscape. Because language models are trained on large amounts of human writing, they absorb the judgment it contains. As Bodnia puts it, “EBRMs are not going to write poems for you.”

They won’t write poems, but EBRMs are extremely well suited to domains where you can define the rules precisely. In chemistry, a candidate molecule either obeys the rules of chemical structure or it doesn’t. Physics requires the conservation of things such as matter and energy. In finance, the invariants can be as simple as “money in equals money out.” And the layout of a chip is largely a set of rules about what is allowed to sit next to what. The request to the model is similar across all these fields: this is the problem, and these are the rules.

![](https://substackcdn.com/image/fetch/$s_!stF7!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ef8e5fe-4d3b-4010-bd11-164586973056_2048x911.png)

Cost is the other half of the story. A model that only scores answers does not have to be large. Kona runs in the range of tens to low hundreds of millions of parameters \[5\]\[6\]. Compare this to a frontier model, which runs in the hundreds of *billions*. Therefore, Kona can run on less expensive hardware. A small model plus a search that settles in milliseconds is how the experiment at the start of this article ended, with $11,000 of API calls from the LLMs and $4 of compute for Kona.

Consider this rough test for your own work: can you define your rules? If you can, consider using an EBRM. If not, a language model might be your better starting point.

The obvious objection to the necessity of an EBRM is that Sudoku already has solvers. But Logical Intelligence believes there is a distinct difference between a solver and an EBRM. A solver is a program hand-written for one problem. In contrast, Kona learned the constraint structure from examples of play and applied it to grids it had never seen before \[1\], similar to the way a person who has learned to play Sudoku can solve a new puzzle. And Kona can learn other things, no solvers required.

Most real-world problems will have some aspects that suit LLMs and some that suit EBRMs. The optimal arrangement is likely a division of labor. Let the EBRM handle the parts with hard constraints and checkable answers while the language model handles the parts that depend on knowledge, judgment, and expression and serves as the interface for reading the problem and writing the result.

Logical Intelligence has built toward this arrangement. EBRMs do the reasoning, and language models handle the interface \[3\]. Kona does the reasoning.

## Verification and safety

Verification and safety work differently for EBRMs than they do for LLMs.

For a language model producing text, there is no pass mark for the text. We will often add a second system, an evaluator to score the quality or correctness and a filter to catch unsafe output. Unfortunately, this introduces latency to an already slow generation, because a check can only begin once the last token has been produced.

The two stages of an EBRM provide different kinds of guarantees. The first stage is the search. The learned energy pulls a candidate toward answers that satisfy the rules. As a result, most wrong answers are rejected before anything is output. This stage is probabilistic. The search wanders, and where it lands depends on where it started. The learned energy is an approximation of the rules, not the rules themselves, so a low energy provides strong evidence, but not proof, that an answer is valid.

The second stage is the check. Because the output is logic rather than prose, satisfaction of the specified constraints can be verified by a machine, and the verdict will be yes or no. What does the checking depends on the task. For a Sudoku grid, a simple program can check the rules. For proving theorems, Logical Intelligence uses **Lean 4**, a proof assistant that checks formal statements by machine \[7\]\[8\]. If the verdict is no, the answer goes back to the search, and the loop runs until the verdict is yes. A search that settles in milliseconds can afford several rounds, but a language model that takes a minute per attempt cannot.

![](https://substackcdn.com/image/fetch/$s_!QjUo!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbae577ce-e843-4105-90a8-ed1dd5ddfb3b_2048x1067.png)

The pipeline is probabilistic in the middle and exact at the end. For now, Logical Intelligence is limiting itself to solving objective tasks that can be formally verified. The check guarantees that an answer satisfies the constraints. It does not, however, guarantee that the constraints have accurately captured what the user meant. Therefore, the writing of constraints remains a human job.

## What’s Next

Bodnia’s larger argument is that one model cannot serve every kind of work. Whereas mission-critical systems rely on the generation of verifiable answers, creative work needs a system that is not constrained at all. Bodnia expects the industry will end up as an ecosystem of specialized models rather than one general system behind one API.

From here, Bodnia expects two shifts in the industry. First, the hardware may move away from GPUs. Today’s GPUs evolved from graphics, and the industry was fortunate that the math required for LLMs was similar in nature to what had been used for graphics. But models built differently from LLMs have no particular reason to use the same hardware. Second, the business model will shift from selling intelligence by the meter to shipping a model per customer. Small models can be trained quickly enough to make that shift possible. Logical Intelligence recently built a model for a customer with two engineers and a week of training on the customer’s data.

The EBRM field is still young, and there remains much to be explored. The next few years promise to be exciting.

### References:

[\[1\] What Sudoku Reveals About AI Reasoning Architectures and the Future of Our Economy](https://logicalintelligence.com/blog/energy-based-model-sudoku-demo)

[\[2\] The Art of Knowing](https://logicalintelligence.com/blog/energy-based-ai-vision-the-art-of-knowing/)

[\[3\] Energy-Based Models for Reasoning, LLMs for the Interface: Scaling Reasoning with Agentic AI](https://logicalintelligence.com/blog/energy-based-models-for-reasoning)

[\[4\] A Tutorial on Energy-Based Learning](https://yann.lecun.com/exdb/publis/pdf/lecun-06.pdf)

[\[5\] WTF is a “Reasoning Energy-Based Model”?! w/ Eve Bodnia of Logical Intelligence](https://www.theneurondaily.com/p/watch-wtf-is-a-reasoning-energy-based-model-w-eve-bodnia-of-logical-intelligence)

[\[6\] Everyone Is Betting on Bigger LLMs. She’s Betting They’re Fundamentally Wrong](https://www.generalist.com/p/everyone-is-betting-on-bigger-llms)

[\[7\] Lean programming language and proof assistant](https://lean-lang.org/)

[\[8\] Aleph Prover Tops Leading Formal Reasoning Benchmarks and Signals What Comes Next for AI](https://logicalintelligence.com/blog/aleph-prover-tops-leading-benchmarks)

---

∙