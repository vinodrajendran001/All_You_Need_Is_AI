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

Two invariants do the safety work. Unpaid requests must not cause side effects, so a request that
fails to pay cannot have already changed state. Payment proofs are single-use, so a captured
credential cannot be replayed.

The cost structure forces a second design. A single web search may be worth a cent while
per-transaction fees exceed that, so charge-per-request does not survive its own overhead. Session
intents let the agent reserve funds and then sign an IOU per request - the cited example is a tenth
of a cent - which the server verifies in the few milliseconds a signature check takes, settling the
accumulated IOUs in one transaction. Verification is made cheap enough to run every time while
settlement is batched. This is the same amortization the vault records in [[KV Cache]] reuse and in
batched inference, applied to trust rather than to computation.

Delegation is expressed through signing keys rather than through accounts. A key can carry a spending
cap per period, an expiry, a list of permitted recipients, a scope, one key per deployment, and
individual revocation, which maps onto the bounded-authority patterns in [[Agent Delegation]]. The
limits are real but partial: a cap prevents overspending and does not prevent valid spending on the
wrong service.

What the protocol deliberately excludes is as important as what it defines. Payment proves control of
a key, not the identity of a customer, so reputation, abuse prevention, refunds, and disputes are
left to other layers. MPP reportedly has no defined refund flow for one-off charges; unclaimed session
funds return automatically, but one-off reversals depend on the underlying payment rail.

## Open questions

- Without customer identity, what supplies the reputation and abuse signals that card networks
  currently derive from accounts and chargebacks?
- Are per-request spending caps the right control surface, or does bounding *what* an agent may buy
  require an allowlist of recipients that scales poorly?
- How does a refundless one-off charge interact with agents that buy on a principal's behalf and are
  wrong?
- Does the demand actually exist? The cited Cloudflare figure of around 57.5% of HTTP requests to web
  content covers all automated systems, not AI agents specifically.

## Related pages

- [[Agent Security and Governance]]
- [[Agent Delegation]]
- [[AI Agents in Production]]
- [[Tool Use and Function Calling]]
- [[Tool Roster Economics]]
- [[Model Context Protocol]]
- [[Agentic Loop]]
