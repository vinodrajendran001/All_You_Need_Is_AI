---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-10-nizzyabi-instinct-teardown
source_title: "I reverse-engineered Instinct. Here's the whole machine"
source_author: "@nizzyabi"
source_url: "https://x.com/nizzyabi/status/2120194267066863738"
tags:
  - source/summary
  - ai-agents
  - personal-assistant
  - agent-memory
  - conversational-ux
source_ids:
  - src-2026-11-10-nizzyabi-instinct-teardown
status: active
---

# I Reverse-Engineered Instinct - Here's the Whole Machine

## Summary

An X long-form post by @nizzyabi measures the behavior of [[Instinct]], a personal AI assistant
used over text messages, from the author's own iMessage database, and combines that with other
people's teardowns of its internals. Its thesis is that Instinct is "several ordinary systems connected
well enough to feel like one person": a channel layer that reads every message within about a second
and reacts with tapbacks, a burst-coalescing step in front of the model, a chat agent that stays
reachable while separate task agents work, a Markdown-and-git memory, a disposable cloud sandbox, and
a proactive layer that texts first. The most transferable finding concerns self-knowledge: the
assistant once claimed a voice memo was sent when none arrived, because it knows what it asked the
channel to do but not what the channel did. This is a **third-party teardown, not first-party
documentation**: "one account and one thread on one Mac", with internals relayed from others and
"Instinct hasn't confirmed most of it". The author also has a commercial interest, since the post ends
by promoting Keiki, his team's competing agent platform.

## Key claims

### Work is bracketed by approval and verification

Buying dental insurance took **22** minutes, nine user messages, and two secure forms. Instinct
corrected the author's mistaken premise **43** seconds in, promised "Before anything gets submitted or
paid, I'll bring you the plan and price to approve", restated tier, price, and start date before
acting, and sent sensitive fields by link: "SSN and card go through a secure link, never in chat."
Across other tasks every email, form, and purchase reached the user first as a draft or price. It then
checked afterwards: **25** minutes after sending eight emails it reported a bounce under "Quick
correction". A hat listed at **$44** was **$64** in the cart, so it stopped at checkout ("my bad, all
10 hats I sent carried that gap"). It twice said it cannot place phone calls, although calling appears
in public product descriptions, so this "may differ by account or by date".

### The texting behavior is measured, not anecdotal

The thread holds **185** messages from the author and **375** messages plus **88** tapbacks from
Instinct; the source list describes the thread as **648** rows from August 18 to November 9, 2026,
plus five texts on November 10.
Messages were marked read at a median **1.1 s**; delivery took about **0.2 s**, and **90%** were read
within **2.0 s**, with one **26.6 s** outlier that looked like a cold start. Of **171** exchanges,
**76** opened with a tapback (the post's **44%**), about seven seconds after the user's message; 22
tapbacks were the entire answer, and all 85 traceable tapbacks were on the user's messages. Instinct's
median message is **131** characters against the author's **58**; of **173** replies, **79** were one
message and **48** were two, split about **2.1 s** apart; **328** of 375 were threaded to the
message they answered. The author infers a written-down set of texting rules rather than model
judgment.

### Bursts are coalesced before the model sees them

Two unrelated messages sent together got two threaded answers about 30 seconds later. A **$600**
budget followed by **$900** produced one reply using $900 and noting the replacement; three messages,
the first saying to wait for the others, produced one answer at **45** seconds. An instruction to stop
using tapbacks held until the test ended. The author concludes that "something sits in front of the
model and collects messages that arrive close together".

### A chat agent stays available while task agents work

Across **149** requests, the median time to the last message was **26** seconds and **90%** finished
within **140** seconds; **26** took over 90 seconds, four over five minutes, and one **100** minutes.
During a long research task, "40.8" (17% of 240) came back in **19** seconds while the research
continued. The author infers that the chat agent and task agents are separate, consistent with guesses
by Yash and Aaron Pitt. The same prompt took seven and a half minutes on October 13 and **50**
seconds on October 25: "a text thread doesn't have a version number."

### Memory: relayed internals, observed edge cases

Relaying Dhravya Shah's teardown: no vector database; Markdown files in a git repository with folders
for people, facts, preferences, timelines, and workstreams, linked to each other with wiki-style
double-bracket links, searched by keyword, and tidied by a roughly daily background job; each turn
starts with a profile, a one-page summary, open to-dos, and a recap, about **13k** tokens together in
his snapshot. Rohan Adwankar found the repository at `/memory` and the lasting copy stored as a git
bundle. The author's tests: a fictional budget changed from **$480** to **$620** was recalled four
weeks later with its edit history in **16** seconds; a project described only as "named after a plant
and a small bird" was retrieved as "Moss Finch" in nine seconds, which plain keyword search should not
manage; and a project the author had asked it not to keep in long-term memory was still known sixteen
days later, though still labeled fictional.

### Sandbox, proactive messages, and network effects

Adwankar's inspection, relayed, found an [[E2B]] sandbox on Firecracker with Ubuntu 22.04, **2**
vCPUs, about **1.9 GB** RAM, and about **30** minutes of uptime, so the computer is disposable and the
memory repository persists. A calculator arrived as working HTML in **54** seconds with a screenshot and
a note that it had been run against the author's numbers. Instinct texted first **17** times in twelve
weeks (six follow-ups, nine first-person release notes, one waitlist notice, one holiday greeting),
all between 8:57 am and 7:20 pm. Founder Noah Shinn has said this proactive layer "costs far more in
tokens than chat does" (paraphrased by the author). Over **300k** assistant-to-assistant coordinations
are "reported" and were not tested.

### "Sent" is not "delivered"

Instinct mostly declined to bluff: it reported an unreachable URL, a missing attachment, kept 40.8
when told 48, and treated a pasted note as data. But on October 27 it said it had sent a voice memo
that never arrived. A retry produced a **14 KB** audio message and the note: "The voice memo is marked
'sent', but I don't have a 'delivered' confirmation." The agent "knows what it asked the messaging
channel to do, and it has no way of knowing what the channel actually did". Shinn describes a watchdog
over every action and reasoning trace, but one that reads the agent's own record "would miss this too";
Instinct's terms say action records "may not always be accurate". The proposed fix is channel-side
delivery receipts the agent can read.

## Why it matters

The post is the vault's most detailed behavioral measurement of a consumer agent. It gives
[[Agentic Loop]] a split between an always-available chat loop and background task agents, plus
input coalescing; [[Agent Memory]] a relayed file-and-git design with observed retention failures;
[[Tool Use and Function Calling]] a precise case of a tool result that reports the request, not the
outcome; and [[AI Agents in Production]] product rules about approval, verification, and invisible
versioning. The receipt problem is proposed for [[Agent Observability]].

## Tensions / open questions

- **Third-party inference.** One account, one Mac, typing indicators unmeasured; internals come from
  other teardowns and interviews, and Instinct has not confirmed most of them.
- **Conflict of interest.** The author's team built Orchid and started Keiki; the post closes with a
  Keiki SDK example (`policy: { approval: 'ask' }`, a two-second steering debounce window). Its
  framing that the plumbing, not the model, is the hard part supports that pitch.
- The "Moss Finch" result contradicts the relayed keyword-search account; the author offers two
  untested explanations.
- A "don't save" request was not honored as deletion, and GPCA's write-up reports that an early user
  found Gmail records he could not delete (and that a deletion tool was later added). Retention
  controls are unverified.
- Some tables and timelines are images, so not every figure is checkable; source links in the capture
  are mangled with an `x.com/nizzyabi/status/` prefix.
- Venture-investor (677 messages), press, and testimonial claims are anecdotes, not measurements.

## Affected pages

- [[Instinct]]
- [[Agentic Loop]]
- [[Agent Memory]]
- [[Tool Use and Function Calling]]
- [[AI Agents in Production]]
- [[Agent Observability]]

## Raw capture

- [[knowledge-base/raw/sources/I reverse-engineered Instinct. Here's the whole machine]]

## Citations

- Canonical URL: <https://x.com/nizzyabi/status/2120194267066863738>
- By @nizzyabi on X, published November 10, 2026; captured November 12, 2026 via a newsletter link
  (tracking parameters removed). The post describes itself as independent commentary not endorsed by
  Instinct.

## Related pages

- [[Instinct]]
- [[Agentic Loop]]
- [[Agent Memory]]
- [[Tool Use and Function Calling]]
- [[AI Agents in Production]]
- [[Agent Observability]]
- [[Persistent Wiki]]
- [[E2B]]
- [[Computer Use Agents]]
- [[Agent Security and Governance]]
