---
type: concept
created: 2026-09-30
updated: 2026-09-30
tags:
  - ai-agents
  - security
  - system-design
  - governance
source_ids:
  - src-2026-09-28-bytebytego-agents-can-pay
status: active
---

# Agent Payment Protocols

## Definition

Agent payment protocols let an autonomous program pay for a resource inline with the request that
needs it, without a human checkout step and without an account held in the buyer's name. Payment
becomes a property of the request rather than of a prior relationship.

## Why it matters

Tool access in this vault has so far been governed by permission: an agent may or may not call an
endpoint. Payment introduces a second axis that permission does not cover. A spending cap bounds how
much an agent can lose but not what it buys, and money that moves without an identity behind it
cannot be reversed by the mechanisms ordinary commerce relies on. The economics are also unusual:
the transactions are individually worth less than a conventional payment fee, so the protocol has to
make settlement cheaper rather than merely make payment possible.

## Current synthesis

[[ByteByteGo - AI Agents Can Think, Now They Can Pay]] describes Machine Payments Protocol, launched
18th March 2026 and co-authored by Stripe and Tempo, as the worked example. The flow reuses HTTP 402
Payment Required as a live negotiation step rather than an error: an unpaid request returns a
challenge carrying an ID, amount, currency, recipient, payment method, and validity window; the agent
authorizes and retries with a credential; the server returns the resource plus a receipt. Failed
verification returns another 402 with a fresh challenge and a structured reason, not a 401, which
keeps the failure inside the payment conversation instead of escalating it to authentication.

Everything here is as described by a **secondary explainer**, not a protocol audit or production
measurement. The article reports as specification properties that unpaid requests must not cause side
effects, so a request that fails to pay cannot have already changed state, and that **a credential
sent a second time is rejected**. Credentials remain **bearer instruments authorizing real money**,
which is why the specification tells servers and intermediaries never to log them or echo them into
error messages.

The cost structure forces a second design. In the article's hypothetical, a web search worth a cent
**can** cost more than that to settle, because per-transaction fees do not shrink with the payment -
**below a threshold**, settlement costs more than the payment, so charge-per-request does not survive
its own overhead. Session intents let the agent reserve funds and then sign an IOU per request - the
cited example is a tenth of a cent - which the server verifies in the few milliseconds a signature
check takes, settling the accumulated IOUs in one transaction. Verification is made cheap enough to
run every time while settlement is batched. This is the same amortization the vault records in
[[KV Cache]] reuse and in batched inference, applied to trust rather than to computation.

Delegation is expressed through signing keys rather than through accounts. A key can carry a spending
cap per period, an expiry, a list of permitted recipients, a scope, one key per deployment, and
individual revocation, which maps onto the bounded-authority patterns in [[Agent Delegation]]. The
limits are real but partial: a cap prevents overspending and does not prevent valid spending on the
wrong service.

What the protocol deliberately excludes is as important as what it defines. Payment proves control of
a key, not the identity of a customer, so reputation, abuse prevention, refunds, and disputes are
left to other layers. MPP defines **no refund flow at all**. Unclaimed session reserve returns by
itself, which covers money never spent but not money already claimed; refunding a one-off charge means
the seller sending funds back to the paying key, and whether that works depends on the card network or
blockchain provider.

Adoption is small: the source reports MPP in production since March 2026 with **about 30,000 MPP
transactions as of August 2026**, a volume it itself calls "relatively small" while comparing the
trajectory to the early App Store.

## Open questions

- Without customer identity, what supplies the reputation and abuse signals that card networks
  currently derive from accounts and chargebacks?
- Are per-request spending caps the right control surface, or does bounding *what* an agent may buy
  require an allowlist of recipients that scales poorly?
- How does a refundless one-off charge interact with agents that buy on a principal's behalf and are
  wrong?
- Does the demand actually exist? The cited Cloudflare figure of around 57.5% of HTTP requests to web
  content covers all automated systems, not AI agents specifically.

## Tensions and limits

- The sole source is a **secondary explainer**, not a protocol audit or an independent measurement, so
  every mechanism on this page is reported specification rather than observed behaviour.
- Adoption is small: **about 30,000 MPP transactions as of August 2026**, against a launch in March
  2026.
- MPP defines **no refund flow at all** - unclaimed session reserve returns by itself, but money
  already claimed, and any one-off charge, has no defined path back.
- Payment proves **control of a key, not customer identity**, so reputation, abuse prevention, and
  disputes are out of scope by construction rather than by omission.

## Related pages

- [[Agent Security and Governance]]
- [[Agent Delegation]]
- [[AI Agents in Production]]
- [[Tool Use and Function Calling]]
- [[Tool Roster Economics]]
- [[Model Context Protocol]]
- [[Agentic Loop]]
