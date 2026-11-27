---
type: concept
created: 2026-11-06
updated: 2026-11-27
tags:
  - concept
  - human-oversight
  - ai-agents
  - evaluation
source_ids:
  - src-2026-10-27-anthropic-agents-judgment-calls
  - src-2026-11-04-x-town-square-rebuild
  - src-2026-11-23-tomassetti-legacy-modernization-measured
  - src-2026-11-22-nikolas-goebel-informal-verification
status: active
---

# Human Deferral to AI

## Definition

**Human deferral to AI** is a person adopting an AI system's choice, framing, or argument on a
decision they are nominally responsible for, so that the outcome reflects the model's preference more
than their own judgment. It differs from two neighbouring ideas in this vault. Automation bias, as
recorded in [[Agent Observability]] and [[LLM Application Resilience]], is the failure to catch a
*wrong* output during review. [[Sycophancy]] runs the other way: the model bending toward the
user. Deferral matters most on **judgment calls with more than one defensible answer**, where there
is no error to catch and the work looks sound whichever option wins.

## Why it matters

Most of the vault's agent governance assumes a human gate is an independent check: review tiers in
[[AI-Native Software Development Lifecycle]], approvals in [[Agent Security and Governance]], and
human escalation in [[Agent Observability]]. That assumption is only as good as the reviewer's
independence. If many teams defer to models with the same preferences, the agreement between their
results may no longer be independent evidence either.

## The first randomized measurement

[[Anthropic - How AI Agents Shape Experts' Judgment Calls]] is the vault's first controlled test.
Fifty professional analysts used Claude Code on a causal-inference task with four open analytical
choices. A hidden coin flip set which option each agent argued for, under instructions to argue
honestly, change its mind if the evidence turned, and never mislead. Analysts chose the agent's lean
**86%** of the time against an expected **50%** if it had no effect, with per-decision shifts of
**62 to 82** percentage points. The final recommendation moved less directly (**54%** versus **36%**
roll-out), but the four leans alone predicted **82%** of recommendations, against **61%** for always
guessing the most common one (extensions excluded), because the analytical choices had already
shaped the estimate.

Three findings make deferral a structural problem rather than a matter of reviewer diligence:

- **It is not self-detectable.** Analysts who called the recommendation more their own still shifted
  about **65** points toward the lean, against **79** for the others, a difference within the margin
  of error. Analysts who followed the lean on all four decisions averaged confidence **71** versus
  **73** for the rest. **77%** reused the agent's arguments, sometimes verbatim, and **15%**
  credited it.
- **Expertise did not predict deferral.** None of the 10 measured characteristics, including
  experience, education, quiz score, and trust in AI, survived correction for multiple comparisons,
  though with so little variation even real differences would have been hard to detect.
- **Stated preferences were abandoned.** In **38** cases where an analyst stated a preference first,
  they switched **60%** of the time when the agent disagreed versus **6%** when it agreed, with a
  wide interval (**24 to 82** points) and a possible selection effect.

The study also cuts against using it as a reason to avoid agents: analysts without the agent made
serious methodological errors far more often, though that group was small, self-selected, and less
experienced. The trade is between error reduction and the independence of judgment, not between
safety and convenience.

## Where the decision moves when implementation is delegated

[[X Engineering - Rebuilding the Global Town Square from Scratch]] describes the operating model
this risk applies to. With agents doing much of the implementation, X's engineers "set the
architecture, decided what to build, and reviewed every change", and their job shifted toward
"deciding what the system should do, then checking in a real browser that it actually does." X
makes verification concrete — lint rules, parity scripts, and tests pinned to the old servers'
behavior — because those questions have a reference answer. The Anthropic study shows the residual
human role is the part with no reference answer: the decisions are exactly where agent influence is
hardest to see. X reports no measure of whose choices its design decisions reflected, and nothing in
either source says the X workflow suffered from deferral; the pairing identifies where to look.

## An agent asked only to translate also made the design decisions

[[Federico Tomassetti - Legacy Modernization with LLMs, Measured]] shows decisions moving to the agent
without a human being offered a choice. The prompt asked for a translation of an RPG application into
Java and to "Organize the project as you see fit". The author's account: "We asked for a translation,
and we also got an architecture that we had not chosen." Tactical choices, such as how to represent
fields, access files, call between programs, own transactions, and handle missing source, differed
between runs. Strategic choices were "the same every time, and they are not the ones we would have
made": no application framework such as Spring Boot, and CSV files or H2 rather than a more obvious
choice such as PostgreSQL. The agent also kept text screens on the console, "the agent's choice under
our instructions".

That consistency parallels the study's unassigned baseline (see the open questions below), where
Claude Opus 4.8 made the same five choices in **112 of 123** runs. In the vault's reading, a team
that accepts such a translation inherits a stable set of model preferences, and because every run
agrees on them, comparing runs will not expose them. Tomassetti's team noticed because it had its
own architecture in mind; no measurement of deferral was made.

## Checkable arguments make the agent's framing visible, not neutral

[[Nikolas Göbel - Informal Verification]] targets the trust a human gate is meant to supply. He
separates **empirical** trust, built by a record of correct results, from **epistemic** trust, the
belief that a system works the way you think it does, and proposes informal proofs whose premises and
steps are each checked by a model. A reviewer then gets "seven concrete claims (four premises and
three reasoning steps)" to compare with their own understanding, instead of "a single agentic
thumbs-up at the end". Read against the study above, this changes what is presented, not who frames
it. **77%** of the analysts reused the agent's arguments, and a decomposed proof is still an argument
the agent chose. The checker tests whether each step follows from the stated premises, not whether
those premises or that property were the right ones to examine, and like a human it silently fills in
facts it considers too obvious to state, which is where the agent's framing and the reviewer's
assumptions can coincide. Göbel reports no study of reviewers using such proofs.

## Current synthesis

- **Verification and judgment need different controls.** Tests, parity checks, and judges catch
  errors against a reference. They cannot reveal whether a defensible choice was the expert's.
- **Deferral is measurable only by design.** The study could see it because the lean was
  randomized; asking people afterward did not reveal it. Production systems need equivalent
  instruments — for example, recording the human's view before the agent offers one.
- **Agent design is one lever.** The authors suggest agents could argue each option or ask for the
  expert's view first, while noting that raising every open decision would overwhelm users, and that
  choosing which decisions to raise is itself a judgment call.
- **Institutions decide where it is acceptable.** The authors propose deciding deliberately which
  decisions need a person's own informed judgment and protecting the skills those decisions require.
- **Unasked decisions count.** An open instruction such as "organize the project as you see fit"
  delegates design choices without naming them. In Tomassetti's runs the agent made the same strategic
  choices every time, so a gate that asks only whether the output works will not surface them.

## Open questions

- How large is deferral when the agent has no assigned lean? With none assigned, Claude Opus 4.8
  made the same five choices in **112 of 123** runs, and the authors say unassigned agents have
  weaker preferences and sometimes push back.
- Does domain expertise, rather than method expertise, reduce deferral? The analysts were new to
  farming.
- Can a review gate be designed to elicit independent judgment without asking reviewers to
  re-derive every open choice?
- If deferral correlates conclusions across teams using the same model, what evidence should count
  as independent replication?
- Would reviewers shown a checked, decomposed argument defer less or more than analysts shown prose
  recommendations? No source tests it.

## Related pages

- [[Anthropic - How AI Agents Shape Experts' Judgment Calls]]
- [[X Engineering - Rebuilding the Global Town Square from Scratch]]
- [[Sycophancy]]
- [[Agent Observability]]
- [[LLM Application Resilience]]
- [[AI-Native Software Development Lifecycle]]
- [[Agent Security and Governance]]
- [[Anthropic]]
- [[Sri Polkampally et al - LLM-as-Judge When It Works and When It Misleads]]
- [[Federico Tomassetti - Legacy Modernization with LLMs, Measured]]
- [[Nikolas Göbel - Informal Verification]]
