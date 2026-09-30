---
type: raw-source
source_id: src-2026-09-29-bytebytego-why-do-llms-lie
title: "Why Do LLMs Lie?"
author: ByteByteGo
url: https://blog.bytebytego.com/p/why-do-llms-lie
published: 2026-09-29
captured: 2026-09-30
created: 2026-09-30
updated: 2026-09-30
tags:
  - source/raw
  - quality
  - rag
  - evaluation
  - tool-use
  - reasoning
  - production
status: active
---
## Debugging Agents in Different Environments - Live Workshop (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!ngw_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9b8e98ac-3d80-4acc-b777-111e867d8ccd_1200x1200.png)

Your agent returns something odd. Was it the prompt, a tool call that timed out, or a response your code could not parse? Without traces, you are guessing.

In this hands-on workshop, Serge from Sentry instruments three agents with Sentry Agent Tracing: a chatbot in an ecommerce store, a custom Slack agent, and a GitHub Action that reviews PRs. You’ll see how to catch bad tool calls and unexpected output, plus how to track token spend and performance across every agent you run.

---

A customer asks a company’s new AI-based support assistant whether a subscription purchased 15 days ago qualifies for a refund. Let’s assume that the assistant responds immediately by explaining that the company offers a 30-day refund window, describes the cancellation process, and promises that the money will arrive within five working days. All of it sounds quite helpful, confident, and complete.

But there is just one problem.

In reality, the company only allows refunds within 14 days. Also, there is no promise about the 5-day processing time. The assistant has actually taken bits of a plausible policy and invented a fake commitment out of thin air. In other words, it has lied. The customer now expects something that the company never offered.

Though this example might sound fictitious, it shows one of the most important problems in applications built with LLMs. While LLMs can produce excellent language, they can get the underlying information totally wrong.

In this article, we will look at why this problem of hallucinations happens with LLMs and the techniques that can help make LLMs more dependable for answering. Here’s what we will cover:

- What hallucination actually means in an LLM
- Three ways an answer can go wrong
- How predicting text produces invented facts
- Why models struggle to admit uncertainty
- Giving the model evidence with RAG
- Looking up missing facts with tools
- Writing useful answers
- Why an explanation is not proof
- Checking the answer before it reaches the user

## What Hallucination Actually Means

Hallucination in the context of LLMs is generated information that is factually incorrect, invented, or inconsistent with the material the model is supposed to use. Here’s how a hallucination is happens:

![](https://substackcdn.com/image/fetch/$s_!8-Vx!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feee9aeb7-69b1-46e1-806b-739be8a49644_3952x1674.png)

The entire response may not be wrong. In fact, an otherwise useful explanation can contain a single fabricated date, an unsupported promise, or a reference to a document that doesn’t exist. That small detail may be the part the reader relies upon.

We can’t outright call this behavior lying, but it comes pretty close to a lie. The answer resembles a confident falsehood. However, lying usually implies an intention to deceive. A hallucination doesn’t establish that intention. The model can produce an incorrect answer through its normal generation process. In the support example from earlier, the immediate problem is that the application presents an incorrect generated policy as established company information.

The context matters a lot here. Inventing a refund policy for a fictional company is appropriate when the task asks for one. However, presenting that same invention as the policy of an actual business is a factual failure. Ultimately, the difference is more about what the answer claims to represent.

## Three Ways an Answer Can Go Wrong

The AI support assistant’s errors become easier to reason about when divided into three useful categories:

- A factual hallucination contradicts reality. For example, saying that the company’s refund window is 30 days, when it is actually 14, belongs here. The company exists and has a real policy, but the assistant describes it incorrectly.
- A faithfulness hallucination concerns the relationship between the answer and its supplied evidence. For example, if the application provides a policy requiring an unused account, but the assistant says usage does not matter, it has contradicted its source.
- Fabrication involves inventing something such as a policy section, a confirmation number, or a research paper.

These three categories overlap.

![](https://substackcdn.com/image/fetch/$s_!2jOz!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0f09d0f-daa0-4eb4-856b-001cd563bf8e_4222x2028.png)

A fabricated policy section can be both factually false and unsupported by the supplied documents. We can also treat factuality and faithfulness as the two broader categories, with fabrication falling under factuality failures. The main distinction to be made is between checking agreement with reality and checking agreement with the provided evidence.

This distinction throws light on an interesting situation. An AI assistant can faithfully summarize an outdated document and still give an incorrect answer about the current policy. To fix the response, we need to pay attention to both the model and the information acting as the source.

---

## Build and scale a winning AI agent strategy (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!oQc_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbf87ce3e-cae2-4ccd-ad93-8301cf3f1b18_1080x1080.png)

Shipping agents to production is the easy part. Keeping them reliable, governable, and improving over time is where most enterprise AI programs stall.

How do top teams do it? They use an Agentic Operating Model (AOM), a step-by-step framework for aligning people, process, and technology so enterprise agents improve as they scale.

In LangChain’s latest guide, you’ll learn:

- Why AI agents don’t break like traditional software
- The engineering stack that covers the entire agent lifecycle
- Shifting from “build and deploy” to “operate and continuously improve”

---

## How Predicting Text Produces Hallucinations

To understand the mechanism clearly, let us look at how an LLM builds a particular response.

As you may be aware, LLMs process text in small units called tokens. A token can be a word, part of a word, or punctuation. For a given input and the response generated so far, the model calculates probabilities for the possible next tokens. A generation method selects one, adds it to the response, and repeats the whole process once again. Depending on the settings, selection may choose the most likely token or sample among possible continuations.

A likely continuation is not the same thing as a verified statement. The probability used to select the next token concerns text generation. It doesn’t certify the entire answer. Likewise, words such as “certainly” and “definitely” are generated language. Their presence cannot establish that the model has checked the policy or possesses reliable evidence.

The model learns these patterns during training.

In the initial stage, called pretraining, it works through large amounts of text and learns to predict continuations. Its internal numerical settings, known as parameters or weights, gradually capture patterns involving grammar, concepts, relationships, and facts. This produces useful knowledge and the ability to handle many different language tasks.

However, familiarity with a subject cannot establish every specific fact about it. A model may encounter 1000s of refund policies mentioning 14 days, 30 days, unused accounts, and processing delays. Those examples help it discuss refunds in an appropriate way. But they don’t tell anything about which conditions apply to this particular customer at this particular company.

Something similar happens with fabricated citations. The model learns what a research reference looks like, including author names, publication years, and technical titles. It can reproduce that structure without having a real reference to back things up.

## Why Models Struggle to Admit Uncertainty

LLMs are mainly optimized for plausible text. They receive additional training to improve accuracy, helpfulness, and responses to uncertainty. Still, a fluent continuation doesn’t prove that every statement made by the LLM is true.

Some training incentives can also encourage guessing. For example, consider an evaluation approach that awards a point for a correct answer but gives the same score to a wrong answer and an admission of uncertainty. In this way, guessing offers some chance of receiving a point. Abstaining from guessing means zero points. This incentive trains the model to guess, resulting in hallucinations.

However, it isn’t totally correct to say that hallucinations are unavoidable because they are built into the architecture. Models can recognize some uncertainty and detect some mistakes. Models have useful self-evaluation abilities under particular conditions, together with limitations when those abilities must generalize to unfamiliar tasks. However, there is no dependable internal guarantee that separates every correct answer from every guess.

Asking the model for a confidence percentage also cannot automatically solve this problem. For example, a response claiming 95% confidence needs evidence that such scores are meaningful for the task. Calibration measures whether confidence estimates match observed accuracy across many cases. Without that evaluation, an impressive percentage can add another vague detail to an already uncertain answer.

## Giving the Model Evidence with RAG

The first major defense addresses missing information directly.

Retrieval-augmented generation (RAG) finds relevant material and adds it to the model’s input before generation. Retrieval finds the information, augmentation supplies it, and generation produces the answer.

![](https://substackcdn.com/image/fetch/$s_!FxOF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc4b709c8-d91c-4806-a639-7adb27133990_4404x2024.png)

In our example support application, a refund question triggers a search through approved company documents. The application retrieves passages describing the applicable policy and adds them alongside the question. The assistant now has the company’s actual conditions available while writing its response.

This changes what a useful and valid answer looks like. For example, the retrieved policy makes it clear that the purchase must fall within 14 days and that the account must be unused for the refund to be valid. The customer’s query establishes only the purchase timing. The assistant should recognize that one condition remains unresolved.

RAG still has failure points. A search can return a retired policy, choose the wrong product’s policy, or miss an exception. The model can also misread a correct passage or add an unsupported promise.

For this application, documents need clear product names, effective dates, and approval status. Conflicting policies need explicit handling so that the model can know which one is applicable.

Document preparation also includes keeping related conditions together. Suppose the refund period appears at the end of one passage while the unused-account requirement begins the next. Retrieving only the first passage can leave the assistant with an incomplete rule. Regularly checking what the model actually receives helps distinguish a retrieval problem from a failure to interpret complete evidence.

## Looking Up the Missing Facts with Tools

Documents explain general rules, but the LLM-based assistant also needs facts about the individual customer. This is where tool use becomes very important.

A tool lets the application obtain information or perform a defined operation outside the model’s scope. Examples include searching the web, retrieving an account record, and running a calculation. Interaction with external information sources can reduce errors on evaluated tasks.

![](https://substackcdn.com/image/fetch/$s_!AvNT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2851a160-5e17-4ae2-a96c-e0915bce733a_4222x2484.png)

An API provides a defined way for one program to request information or actions from another. The support application might offer an account-lookup API that returns the purchase date and whether the subscription has been used. The model requests the lookup, the application executes it, and the returned result becomes available for generating a proper answer.

RAG and tool use can overlap because document retrieval can itself be exposed as a tool. In this example, they supply complementary evidence. The policy states the conditions, while the account lookup supplies the customer facts needed to apply them.

The important thing is that the lookup must actually happen. A generated sentence saying that the account was checked doesn’t prove anything. If the tool fails, that failure must remain visible to the application. Assuming that the account is unused would simply introduce a hallucination at a different point.

Eligibility and payment are separate facts as well. Even after confirming that a customer qualifies, the assistant cannot truthfully say that a refund has been issued until the payment system reports success. Generating a made-up confirmation number doesn’t create a transaction. The application needs the actual operation and its outcome before describing that action as completed.

## Writing Useful Answers

Another defense to hallucinations is to make insufficient evidence a valid outcome.

Explicit instructions can tell the assistant to identify missing information and avoid unsupported conclusions. We can disallow uncertainty by restricting answers to supplied material when appropriate, and grounding claims in supporting passages. These measures can reduce hallucinations, but they don’t eliminate them.

Either way, doing so is more helpful than a bare admission of ignorance. In our example, the assistant can explain that the purchase falls within the 14-day window while account usage still needs checking. This preserves the information already established and identifies the exact obstacle to a complete answer.

![](https://substackcdn.com/image/fetch/$s_!_BVU!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff6ba78d-6f3e-4998-88e4-e83bdd19d15d_3526x2104.png)

The software also needs a way to represent that outcome. Requiring every response to contain either “eligible” or “ineligible” leaves no room for missing evidence. A third state, such as “needs review,” allows uncertainty to influence the application’s next action.

## Why an Explanation Is Not Proof

Another proposed defense is chain-of-thought prompting, which asks a model to work through a problem in intermediate steps.

Breaking a task into smaller parts can improve some answers and make mistakes easier to notice. However, a generated explanation may contain false premises or fail to faithfully describe what influenced the result.

For example, suppose the assistant explains that the customer purchased 15 days ago, the refund window is 30 days, and the customer therefore qualifies. The argument is easy to follow, but it depends on the wrong policy. More explanation doesn’t supply the missing fact.

A useful application instead requests a concise justification connected to checkable evidence. The assistant identifies the policy clause, the relevant account information, and how the conditions apply. This gives a reviewer concrete claims to inspect without treating the explanation itself as proof.

## Checking the Answer Before It Reaches the Customer

Verification makes inspection a separate part of the workflow. This is because drafting an answer, generating verification questions, and answering those questions independently reduced hallucinations on the evaluated tasks. This supports structured checking, while leaving open the possibility that the checker also makes mistakes.

For the support assistant example, the sentence “The customer qualifies for a refund that will arrive within five days” contains separate claims. Eligibility requires the policy and account facts. Processing time needs its own supporting evidence. If nothing establishes the five-day promise, that promise should be removed.

Citations make these checks easier, provided the citations are checked too. A document must exist, apply to the question, and support the particular statement attached to it. The application can construct links from retrieved document identifiers and check whether quoted passages occur in those documents. Just placing a real link beside an unsupported claim remains an unreliable answer.

Some simpler techniques are also present, but they have narrower benefits.

Lowering temperature generally concentrates token sampling more strongly on likely continuations, but it doesn’t establish factual accuracy. The assistant may become more consistent while repeating the same wrong policy. Requiring a particular output format also helps software process a response without proving that its contents are correct.

For unambiguous rules, ordinary application code can perform part of the decision. If the policy has clearly defined conditions, code can compare the verified purchase date and usage status against those conditions. The model can then explain the result. However, exceptions and ambiguous policy language still require explicit handling.

## Conclusion

The improved support workflow with fewer hallucinations can be thought of as having a clear sequence.

It retrieves the applicable policy, obtains the necessary account facts, checks the conditions, and prepares an explanation. It then checks the explanation’s factual claims and citations. If some information is missing, it generates a specific unresolved status. Lastly, cases requiring judgment are routed for further review.

The reliability of such a setup must be measured on realistic examples. Test cases should include eligible purchases, used accounts, missing records, outdated policies, and questions containing false assumptions. A customer asking how to claim a “guaranteed 30-day refund” should not cause the assistant to accept that guarantee without checking.

Evaluation also needs to consider usefulness. An assistant that always answers may make unsupported claims, while one that always declines provides little value. We should measure whether delivered answers are correct and supported, whether unanswerable cases are handled appropriately, and whether answerable questions are declined unnecessarily.

Returning to the original customer, the LLM-based assistant can now explain which conditions are satisfied, which remain unresolved, and what evidence supports its response. The wording may be less confident when information is missing, but the answer becomes more useful. A developer’s responsibility is to build a process in which the evidence determines what the application can claim in a responsible manner.

---

∙