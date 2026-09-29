---
title: "AI Agents Can Think. Now They Can Pay."
source: "https://blog.bytebytego.com/p/ai-agents-can-think-now-they-can?utm_source=post-email-title&publication_id=817132&post_id=217161816&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-09-28
created: 2026-09-29
description: "I attended a MPP event at Stripe HQ, where I spoke with Emily Sands and Matt Schulman from Stripe, along with Brendan Ryan from Tempo."
tags:
  - "clippings"
---
## AI SREs are here. Here's how to prepare your stack. (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!QYQo!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feaad3f59-e4e7-4ca4-8d09-4e473baa7065_1080x1080.png)

AI SREs are here. If your telemetry, alerts, and access controls aren’t ready, expect missed incidents, alert fatigue, and AI-driven investigations that go nowhere. This Datadog eBook covers how to prepare your stack for the AI SRE future, including a practical self-assessment checklist and real examples from Datadog’s own implementation.

You’ll learn how to:

- Assess whether your telemetry coverage gives an AI SRE enough signal to investigate effectively
- Design alerts and monitors that an AI agent can act on, not just surface to humans
- Set up the access controls and data quality foundations that make AI-driven investigations trustworthy

---

For 30 years, every online business has been built with a simple assumption that your customers are human. Humans browse the website. Humans enter credit card numbers. Humans click buy.  
  
AI Agents are starting to change this assumption. If ChatGPT is going to be your customer, the internet may need a new protocol.

That’s the question behind **Machine Payments Protocol (MPP).** To better understand this shift, I attended a MPP event at Stripe HQ, where I spoke with [Emily Sands](https://www.linkedin.com/in/egsands/) and [Matt Schulman](https://www.linkedin.com/in/matt-schulman1/) from Stripe, along with [Brendan Ryan](https://www.linkedin.com/in/brendanjohnryan/) from Tempo.

In this deep dive, we’ll explore:

- The problem with today’s payment flow
- What is MPP
- How MPP works
- Two use cases of agentic payment
- Your Next Customer Might Be an Agent

## The Problem with Today’s Payment Flow

Right from its inception, the internet has run on the basic assumption that it will be used mostly by humans. However, this assumption is no longer valid.

![](https://substackcdn.com/image/fetch/$s_!pBqF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff591d17c-3c53-4832-b8f6-b594faa53e8f_2048x1026.png)

According to a recent report from Cloudflare, automated systems are now generating around 57.5% of HTTP requests to web content. AI tools are evolving from question-and-answer chatbots to autonomous agents that can make comprehensive plans, execute actions based on those plans, and evaluate the outcomes of those actions.

However, the internet’s payment model is still stuck in the human-centric era.

![](https://substackcdn.com/image/fetch/$s_!wmgK!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F80af75d2-3c28-4cd1-9372-0e932a1099e1_1589x2048.png)

This is where MPP (Machine Payments Protocol) comes into the picture. It is a protocol that removes the friction between the buyer and the seller. This friction exists at the interface, which has been built keeping in mind a user reading a web page to figure things out. MPP creates a similar interface for AI agents so that they can settle payments with a service on the internet, irrespective of the payment method.

In other words, the innovation that MPP brings to the table is not only about making payments. It is more about the disappearance of the human from this process.

---

## \[Webinar\] How to stop babysitting your agents (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!i7gR!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92cbecfb-dc4b-47cc-89ba-53f10dbe054d_1600x900.png)

Agents can generate code. Getting it right for your system, team conventions, and past decisions is the hard part. You end up wasting time and tokens in the correction loops.

More MCPs, rules, and bigger context windows give agents access to information, but not understanding. The teams pulling ahead have a context layer to give agents exactly what they need for the task at hand.

[Join us for a FREE webinar on Oct 7](https://go.bytebytego.com/Unblocked_092826) to see:

- Where teams get stuck on the AI maturity curve and why common fixes fall short
- How a context layer solves for quality, efficiency, and cost
- Live demo: the same coding task with and without a context layer

If you want to maximize the value you get from AI agents, this one is worth your time.

---

## What is MPP?

If we take the human out of the payment flow, something has to fill the gap. MPP, or Machine Payments Protocol, is the thing that fills this gap.

MPP was co-authored by Stripe and Tempo, and launched on 18th March, 2026. The core of the MPP specification has been published as the Payment HTTP Authentication Schema and has been submitted to the IETF standards track. This is the same body that also maintains HTTP.

What exactly does MPP do?

Before any money moves between two parties, they need to agree to a few things. For example, what is the cost of a service, what counts as payment, and what the proof of payment should look like.

As we discussed, humans make all these decisions just by looking. A user opens a page, finds the price, recognizes the checkout button, and knows what to do next.

Now, MPP manages each of these decisions. It also gives a specific name to each of them:

- The Challenge is what the server asks for (payment) when someone requests a service.
- The Credential is what the client sends back as proof.
- The Receipt is what the server returns along with the service delivery.

These three objects (Challenge, Credential, and Receipt) form the core of the protocol along with payment intents around charge, session, and subscription.

![](https://substackcdn.com/image/fetch/$s_!fDXQ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F305de768-290d-4eae-9efd-73bec7ad42a0_2048x1776.png)

However, every website on the internet has a slightly different way of presenting the payment details to the users. In the case of humans, it rarely matters, because people are good at figuring things out. Software cannot do that. It needs the terms in the same place and format every time so that it can parse the details efficiently.

Therefore, MPP places these details in HTTP headers.

The server sends its terms back in a WWW-Authenticate: Payment header. The client returns the proof in an Authorization: Payment header. The server finally confirms with a Payment-Receipt header. The Challenge contains details such as an ID, the amount, the currency, who to pay, which payment method, and the validity of the offer.

![](https://substackcdn.com/image/fetch/$s_!QHEh!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F97222458-8aa6-41e7-a989-24a6af6c1bf1_2048x1944.png)

The payment methods are governed separately. Each rail (card networks, blockchain, payment processor) can write and maintain its own specification for how it fits the core. This makes the protocol open enough so that it isn’t controlled by individual companies. The protocol itself is free, with no licensing fees for implementing it.

The ultimate goal of MPP is to become the language of internet payments. A service that understands MPP can sell to any agent. An agent that understands MPP can buy from any service. Neither one has to have heard of the other beforehand.

## How Does MPP Work?

When an agent requests your API or service, your service returns an HTTP 402 response with payment details. The agent authorizes the payment, retries the request, and gets access to the paid resource along with a receipt. The diagram below shows the overall process flow:

![](https://substackcdn.com/image/fetch/$s_!gNlQ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F38af2e84-a27a-4d0a-bab4-ed6729866015_2048x1681.png)

Here’s how the process works:

1. The agent asks for access to a service or an API.
2. The server provides a price when it receives an access request. It answers 402 Payment Required and places the terms in a WWW-Authenticate: Payment header. This header carries a Challenge, which contains a unique ID, the payment method, the intent, and an expiry. It also has an encoded payment request that holds the amount, the currency, and the recipient address.
3. The agent checks the details. There is no account creation, form filling, or buying an API key. The agent reads the terms provided by the server. It checks the various details such as the amount, the recipient, the currency, and the validity window from the signed payload.
4. Then it authorizes the payment based on a limit that was set earlier as part of the agent’s configuration. These limits are part of the signing key rather than in the agent’s reasoning. This is a delegated key with a spending cap per period, an expiry, a list of permitted recipients, and a scope. Often, there is one key per deployment. Each can be revoked individually so that a runaway agent cannot spend beyond the limit.
5. In the next step, the agent provides the proof of payment. It repeats the identical request for access using an Authorization: Payment header with a Credential. This includes the Challenge ID with a payment payload, which might be a signed transaction, a paid invoice, or a card token. Credentials are bearer instruments that authorize the spending of real money. Servers and intermediaries don’t log them or echo them into error messages for security purposes.
6. In the last step, the server provides the access. It verifies the proof against the rail and returns the search results. It also attaches a Payment-Receipt header confirming the settlement.

The overarching rule behind this entire exchange is that the server must not perform side effects (such as database writes or calls to other services) for a request that has not been paid for. The unpaid request that triggers the 402 changes nothing except recording the Challenge. Proofs are single-use, so a Credential sent a second time is rejected.

If verification fails for some reason, the server does not return 401. It returns another 402 with a fresh Challenge along with a structured problem document that provides details about the failure, such as payment-insufficient, payment-expired, verification-failed, and invalid-challenge. The 402 status code means the payment barrier is still present. But the AI agents get to learn about the failure and make corrections.

In the case of Stripe, this setup fits quite well. A successful payment creates a PaymentIntent. The money settles into the existing balance of the business in the default currency. The same tooling works to support other features such as tax, fraud, reporting, and refunds. No customer records are created. No need to deal with user accounts. There is only a receipt on the client side and the payment on the server side. The next time an agent needs something, it has to start from zero.

## Two use cases of agentic payment

Let us now look at some use cases of MPP.

### Use Case 1: How AI Agents Can Pay Pennies

As we saw in the previous section, every time an agent needs something, it starts from the beginning. While starting from zero every time sounds great, it also has a cost.

Let’s say the cost for a single web search request is just a cent. However, moving a cent across the banking system often costs more than a cent.

![](https://substackcdn.com/image/fetch/$s_!oc4i!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F275ac1e4-90ab-4035-aaa8-cec3b5a81614_1784x1138.png)

Cards charge a flat fee per transaction. Blockchains charge a network fee per transaction and also take time to confirm. These charges don’t shrink even when the payment amount gets smaller. In other words, below a specific threshold, the cost of settling a payment can turn out to be higher than the payment amount itself.

This is the reason why the internet has relied on subscriptions, credit packs, and monthly plans. Services get bundled up until the value goes above the threshold value. However, agents don’t buy in bundles. They might buy constantly. They could make a search request followed by a lookup. Then, they might ask for another page. This could happen thousands of times inside a single task. If we settle each separately, the processing fee makes things economically unviable. If we wait for each one to confirm, the entire time goes into waiting.

To get around this, MPP does not settle every single payment. It uses the concept of sessions.

In this approach, the agent can open a session by putting money aside at the beginning. This could be a deposit into a reserve. The point is that the deposit is committed, but not yet claimed by the seller. Then, every request is paid with a signed IOU. IOU stands for “I Owe You” and is an informal written record or digital acknowledgment that one party owes a certain amount of money to another party. The agent can sign a message saying another tenth of a cent is owed. It then sends it along with the request. The server checks the signature and serves. There is no immediate settlement.

See the diagram below that shows the session-based flow:

![](https://substackcdn.com/image/fetch/$s_!faaq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda176d46-db61-4f72-8171-762ccc4185b4_2048x1852.png)

These IOUs accumulate as requests pile up. When the session finally ends, the server claims the total amount in a single real transaction. This way, a single processing fee is divided across thousands of requests. The per-request cost falls to nearly nothing. The delay is just the few milliseconds it takes to perform a simple signature check. In other words, sessions make it possible for agents to pay pennies in an economically feasible manner.

### Use Case 2: Purchase ByteByteGo Newsletter Single Article

Making micropayments becomes extremely easy with MPP. This opens up some new possibilities.

For example, a reader can use MPP to purchase the latest article from publications like ByteByteGo. Michael Blau [demonstrated this using Drip](https://x.com/blauyourmind/status/2085581359217881510). In this setup, the agents pay per use from an attached Tempo wallet without the need to buy subscriptions. Writers get paid behind the scenes even if the amount is just a single cent. Moreover, the writer can receive the money within a few milliseconds.

![](https://substackcdn.com/image/fetch/$s_!z08f!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda7b97e9-6633-4c08-a403-02383146b0d8_2048x869.png)

As MPP matures, more such use cases are definitely going to appear. Some of the exciting possibilities are as follows:

- The internet gets a native payment layer. For years, the web was funded by advertising. However, machines that can pay per request make paid access a strong alternative to the typical advertising-driven internet economy.
- Agentic workflows can now transact with the world. This opens new possibilities where agents can buy services like compute, data, and so on. AI becomes more of an economic participant.
- It opens a new supply side where we now have a reason to build things specifically for machines being the consumers.
- Payments become interoperable at the protocol layer and not at the vendor layer.

## When Every Customer is a Stranger

Despite the many advantages of MPP, there are also some aspects of MPP that might impact the business in unexpected ways. As we discussed, if we take away the old signup flow, human involvement disappears. But there are also other things that vanish along with it.

Traditionally, the signup process helped the seller find out who was buying the service. The whole signup process created a record containing names, company details, and email addresses. It also helped maintain a history of what a particular customer has done before. Other important requirements, such as abuse control, depend on signups. When someone misuses a service, you could disable their account. Managing disputes and refunds also rely on signups for getting information about the user.

Once we remove the account, all of these things have to change.

![](https://substackcdn.com/image/fetch/$s_!08FP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3dd7dba9-4174-4e28-9468-01fddff31838_2048x1053.png)

With a protocol like MPP, the seller only gets a public key. The payment simply proves that whoever sent it controls the key. It doesn’t tell about which company might be behind the request, which end user the agent might be working for, and whether the same buyer has bought a service earlier with a different key. In other words, payment is no longer a form of identification.

The spending limits can help a little, but only with a specific type of problem. A capped key stops an agent from spending more than it should. It doesn’t stop an agent from spending correctly on the wrong things. The payment is valid, signed, and final. Even if the seller wants to offer a better service, there is nobody to contact after the transaction is done.

The commercial side of business will also see changes:

- The signup funnel is no longer present because a person won’t visit the landing page and register for the service.
- When a user availed the free tier, it gave an indication about a user who could be potentially converted into a paid customer down the line. That sort of data is difficult to obtain.
- The sales call provided details about someone the business could call.

This is why identity and disputes are being built as separate layers rather than being attached to the MPP payment flow.

For identity, there is a way for an agent to sign its requests so that a server can determine which automated client it’s dealing with. These use specifications backed by Visa and Cloudflare. The same key can be recognized across a complete workflow without paying again. This way, the seller can decide whether to trust a particular agent operator.

MPP, however, has not defined a refund flow at all. In a specific session, unclaimed money returns by itself. But in a one-off charge, refunds mean the seller has to send funds back to the key that was used to make the payment. A lot depends on the card network or blockchain provider on whether the refund works as expected.

MPP makes it quite clear what it can control. For example, TLS is mandatory. Challenges can expire. Proofs only work once. Servers should never log a Credential or put one in an error message.

There are also a few guardrails that are part of the MPP specification and should be followed:

- The first guardrail is to deal with a runaway agent that spends much more than intended. The solution is to have a delegated signing key with a spending cap per period, a fixed expiry, and a list of permitted recipients. Lastly, there should be a separate key for each deployment so that a particular key can be revoked.
- The second guardrail is for a dishonest seller who might quote different prices in the description and the signed payload. The MPP specification tells the clients to verify the amount, recipient, current, and expiry from the signed payload and ignore the friendly text description.
- The third guardrail is around discoverability. Directories that list available services and their costs are needed for agents to find sellers. However, according to the MPP specification, these directories and lists should only be treated as advisory when it comes to judging cost and quality.

## Your Next Customer Might Be an Agent

MPP has been in production since March 2026. The volume so far is relatively small. As of August 2026, about 30,000 transactions are MPP transactions. However, the pattern might be similar to the early days of the Apple App Store, where the first year’s revenue said very little about what the platform would eventually become. What matters more here is the new type of customer that just arrived.

**References:**

- [Introducing the Machine Payments Protocol](https://stripe.com/blog/machine-payments-protocol)
- [Machine Payments Protocol: Stripe Docs](https://docs.stripe.com/payments/machine/mpp)
- [Shared payment tokens: Stripe Docs](https://docs.stripe.com/agentic-commerce/concepts/shared-payment-tokens)
- [Cloudflare Radar: Bot vs. human traffic](https://radar.cloudflare.com/traffic)
- [Bots Now Outnumber Humans Online](https://www.forbes.com/sites/josipamajic/2026/06/04/bots-now-outnumber-humans-online-and-the-internet-was-never-built-for-this/)
- [Machine Payments Protocol: Overview](https://mpp.dev/overview)
- [Machine Payments Protocol: Protocol](https://mpp.dev/protocol)
- [Machine Payments Protocol: HTTP 402](https://mpp.dev/protocol/http-402)
- [Machine Payments Protocol: Sessions](https://mpp.dev/intents/session)

---

∙