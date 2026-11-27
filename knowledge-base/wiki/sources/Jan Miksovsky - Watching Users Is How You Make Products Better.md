---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-23-jan-miksovsky-watching-users
source_title: "Watching users is how you make products better"
source_author: Jan Miksovsky
source_url: https://jan.miksovsky.com/posts/2026/11-23-observing-users.html
tags:
  - source/summary
  - usability
  - product-design
  - testing
  - opinion
source_ids:
  - src-2026-11-23-jan-miksovsky-watching-users
status: active
---

# Watching Users Is How You Make Products Better

## Summary

A short opinion post. Jan Miksovsky argues that "the single most useful exercise" in his career in
software design and engineering "has always been just watching people use whatever product or feature
I'm working on", that hardly anyone does it any more, and that a small team can start this week. He gives a
16-point list for low-budget observation sessions. AI appears only as a jab: while executives "pursue
their dreams of AI riches", he doubts they will check "their vibecoded apps meet real needs". The post is
in the vault as a human-in-the-loop counterweight to automated testing. It is experience and argument, not
a study.

## Key claims

### Observation is rare, and that shows

He calls the advice "a fairly safe claim to make, because very few companies have ever invested enough in
observing users", and concludes from how rarely anyone mentions a lesson learned this way that "people
hardly do it anymore". Video game companies are his "notable exception". He says many sites and apps have
problems so "glaring" that their creators "must take great care to avoid ever watching real users", which
is rhetoric rather than evidence.

### One session can redesign a product

He watched a user struggle through a Web Origami tutorial and say, "There are no words you could have
written here that would have gotten me to understand this." That uncomfortable session "led me to explore
alternative ideas that resulted in a complete redesign of the language". It is a single anecdote about
his own project.

### Being in the room beats a report or a recording

People at companies that already observe users should join a session, because "reading a report or
watching a video clip is nothing like being there live."

### A budget method

The list says to:

- go to the person and observe them wherever they would normally use the product (at Cozi he observed
  families in their kitchens), on their own device unless the device is under test;
- say up front that "you're not testing them", you are testing the product;
- collect only a *tiny* amount of background, ask them to think aloud, and give a short script of basic
  tasks, or the feature under development for experienced users;
- say little, and when asked a question, ask what they would do if you were not there;
- help when they are clearly "off the rails", because then "you're not going to learn anything more, and
  letting them suffer is cruel";
- ask for their thoughts before time runs out, end on time, and pay them;
- repeat: "If multiple people get stuck in the same place, you've found a real problem", and the fix can
  be checked by watching again. "You don't need big numbers of people to identify important issues."

### Why people avoid it

Observation is "humbling and often excruciating". He recalls Microsoft engineers in the 1990s, at their
first usability lab test, asking "Where did you find such stupid users?" They took a long time to see the
design problems and longer to see that "they themselves hadn't spotted the problem" until the user hit it.
He calls avoiding that discomfort "childish" and "a recipe for bad products".

## Why it matters

[[Agentic Testing]] records ever more automated oracles, such as test suites, recorded browser videos,
model judges, and fault injection. Miksovsky's claim is that the most useful test of a product is one
nobody scripts: a real person trying to do a real task, with the builder in the room. It also cautions
against treating per-test recordings as a substitute for watching people.

## Tensions / open questions

- **Opinion and anecdote.** No study, sample size, or defect count supports "the single most useful
  exercise" or "you don't need big numbers"; the post points readers to a search for "budget usability
  testing" instead of citing research.
- **No AI method.** Whether agent-run usability tests or synthetic users could substitute for observation
  is not discussed; the post's only AI reference is the vibecoding remark.
- **Recordings versus presence.** His dismissal of video clips is a claim about what the builder learns,
  not about whether a recording is useful evidence of a defect; [[Paul Irish - chrome-capture]], the vault's
  per-test video source, makes the second claim, not the first.

## Affected pages

- [[Agentic Testing]]

## Raw capture

- [[knowledge-base/raw/sources/Watching users is how you make products better]]

## Citations

- Canonical URL: <https://jan.miksovsky.com/posts/2026/11-23-observing-users.html> (the captured link
  carried a `utm_source=tldrnewsletter` parameter, removed here).
- The capture's `author` field is empty and the body has no byline. The author, Jan Miksovsky, was
  recovered outside the capture from the live page and site at jan.miksovsky.com. The capture gives the
  2026-11-23 publication date. Captured 2026-11-25.
- The capture spells "extremly" in its last sentence; not quoted here.

## Related pages

- [[Agentic Testing]]
- [[Paul Irish - chrome-capture]]
- [[Federico Tomassetti - Legacy Modernization with LLMs, Measured]]
