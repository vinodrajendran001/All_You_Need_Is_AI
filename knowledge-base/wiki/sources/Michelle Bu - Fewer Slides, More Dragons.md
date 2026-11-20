---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-18-bu-fewer-slides-more-dragons
source_title: "Fewer slides, more dragons"
source_author: "Michelle Bu"
source_url: "https://www.breakingchange.blog/p/fewer-slides-more-dragons"
tags:
  - source/summary
  - coding-agents
  - collaboration
  - presentations
  - opinion
source_ids:
  - src-2026-11-18-bu-fewer-slides-more-dragons
status: active
---

# Michelle Bu - Fewer Slides, More Dragons

## Summary

Michelle Bu, who works at Stripe on a team called DEEP (Developer & End-user Experience Platform),
describes a personal experiment. She banned herself "from creating slides for *any* reason" and used a
coding agent to build interactive web pages for presentations and group activities instead. She calls
the experiment "*surprisingly* successful". The evidence is her own experience and colleagues' visible
engagement; nothing is counted or measured. The post is an **anecdotal first-person essay** with a
light how-to at the end. Its main interest for the vault is how agent-built, git-tracked artifacts
change **who contributes** to a shared document, and the role an AGENTS.md file plays in that.

## Key claims

### The problem with slides

Slides pull a presenter into "obsessive pixel-pushing", and multi-author decks clash in style. Her
example is a pasted slide whose "matched styles" theme turned a green "on track" status badge dull
yellow. She admits she may have said slides should be banned "in anger". She treats the ban as a
provocation that cheap AI alternatives now make practical: "Sometimes you have to take away the rotary
phones to get people to use new technology."

### What she built

- A Bauhaus-themed interactive strategy explainer, made "Without much effort (and in under 30
  minutes)".
- A planetary-system home page for her team's "executive briefing" meetings with stakeholder teams,
  customised to highlight each viewer's focus areas. Attendees can explore it afterwards via a link.
- A **tech-lead village** icebreaker for a cross-org onsite. Many people and their agents added to one
  page during the day. A Risk tech lead added a dungeon and a dragon "to represent the dragons the team
  slays for us". Others added a Live MaaS sign and the Pacifica Taco Bell for the MaaS (Money as a
  Service) team, and a DEEP lake. Someone added a way to explore inside each team's space. "An old,
  non-AI innovation called git kept everyone's contributions manageable."
- A storybook holiday book exchange that she "previously would have run in Figma". At Stripe,
  colleagues can point their agent at the linked AGENTS.md to build one for their team on internal
  infrastructure.

### Why collaboration changed (her account)

Slide collaboration is a burden: someone breaks the template, and section owners produce a "jarring"
or at best "mid" result. By contrast, "*everyone* has fun building low-stakes, vibe-coded webpages
together". She asks the agent to fix layout instead of moving things herself. After people see others
doing it, "they do it themselves because it saves time while allowing them to be *more* creative". The
village was "the first time I'd seen people engage with the creation of an icebreaker activity or
presentation *beyond* the bounds of the activity itself."

### The process

She says "simple prompts work best for divergent work like brainstorming, naming, or picking a visual
direction". Her five steps, which she had her agent write up:

1. Have an idea to present (a doc, bullets, or notes typed on a ferry).
2. Ask the coding agent for a few ways to explain it, with quick mocks, and repeat until a concept
   works.
3. Pick a concept and explore visual styles (for example pixel art, Bauhaus, a "Spiderverse" version).
4. Build and iterate on content, visuals, interactions and animations.
5. "Ask your agent to create an AGENTS.md explaining how the project works and how to contribute.
   Then your coworkers and their agents can take it from there."

She claims this "consistently takes less time than making slides", with the agent iterating in the
background. Run locally to present, deploy only if others need to explore, and ask the agent for a
presenter mode if needed.

## Why it matters

Two points connect to existing pages. First, step 5 uses AGENTS.md as a **contribution guide for
other people's agents**, not only as context for the author's own agent. That extends the
[[Context Engineering]] discussion of hand-written context files to multi-author projects. Second, the
village is a small, low-stakes case of shared human-and-agent creation, kept workable by git, not by
a shared agent workspace. [[Agent Workflow Maturity]] records PostHog's observation that collaboration
happened "more in GitHub than in the product's own UI" and that people prefer starting privately. Bu's
case agrees on git as the coordination layer. She reports people joining in once they saw others do
it, which was a social cue, not a default setting.

## Tensions / open questions

- "Consistently takes less time than making slides" and "making meetings much more fun and efficient"
  are self-reports with no timing or audience comparison. The 30-minute figure covers one artifact.
- The artifacts are low-stakes by design. The essay does not address accessibility, maintenance,
  accuracy review, or what happens when an executive briefing's content is wrong in an interactive page
  nobody re-reads.
- Screenshots are "heavily redacted", so the artifacts cannot be inspected.
- The AGENTS.md contributor guide is described but not shown. Whether it was hand-edited or left as
  the agent wrote it is unknown.

## Affected pages

- [[Context Engineering]]
- [[Agent Workflow Maturity]]

## Raw capture

- [[knowledge-base/raw/sources/Fewer slides, more dragons]]

## Citations

- Raw capture: Michelle Bu, "Fewer slides, more dragons" (subtitle: "What happened when I banned myself
  from making slides"), published 2026-11-18 on the Breaking Change blog (source ID date), captured
  2026-11-20. The canonical URL drops the newsletter `utm_source` parameter.
- Employer and team come from the text ("At Stripe", "my team (DEEP)"). No Stripe entity page exists
  in the vault.

## Related pages

- [[Context Engineering]]
- [[Agent Workflow Maturity]]
- [[Zach Wills - The Levels of Agentic Engineering]]
- [[Generative User Interface]]
- [[Agent Skill]]
