---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-10-mollick-fable-5-2-jagged-agi
source_title: Fable 5.2 and Jagged AGI
source_author: Ethan Mollick
source_url: https://www.oneusefulthing.org/p/fable-52-and-jagged-agi
tags:
  - source/summary
  - ai-agents
  - multi-agent
  - evaluation
source_ids:
  - src-2026-11-10-mollick-fable-5-2-jagged-agi
status: active
---

# Fable 5.2 and Jagged AGI

## Summary

Ethan Mollick used Anthropic's Claude Fable 5.2 before its public launch and asks whether it meets
his deliberately limited definition of AGI: "an AI as good as most human experts at most
intellectual tasks you can do with a computer". His answer is "almost", which he calls **Jagged
AGI**. Across one-shot video, hardware hacking, a business plan, a literature course, two research
projects, and a multi-agent world-building run, the model did expert-level work in many roles. Its
failures were no longer made-up facts or bad arithmetic. Instead they were failures of taste and
self-assessment: a joyless course, a 182-page paper, repeated themes, and an agent bureaucracy. The
central gap, in his account, is that the AI "did not notice these problems itself". Its critics,
fact-checkers, and judges found errors but never asked whether the work was too long, too
repetitive, or no fun. This is a first-person experience essay, not a controlled evaluation.

## Key claims

### The definition and the verdict

- The definition explicitly excludes physical-world work, work involving other people, and most
  whole jobs, in which using a computer is only one task.
- Mollick says that on many individual tasks Fable met the bar he set. The "almost" comes from gaps
  that are harder to describe than hallucinations, because they concern taste and judgment.

### Wide range, from single prompts

- **Hardware.** From a single prompt, Fable read the code of the two apps controlling a Codex Micro
  keyboard, worked out how to drive its keys, knob, and joystick, and wrote **six** games on the first
  try. Mollick says there are no public instructions for this "as far as I can tell".
- **Business.** Asked to make at least **$20,000** a year with no more than **20 minutes** a month of
  his time, Fable screened **22** ideas and chose "Prebid Brief". The service would tell equipment
  sales reps about funded park and water projects before they go to bid. It read public agendas from
  **201** city and county governments. The AI put its own chance of success at **20%-40%**. When it
  began setting up scheduled tasks and asked to send public-records requests, Mollick stopped it at
  the demo stage. He says he would not yet trust it to run a business on its own.
- **Humanities.** Claude rebuilt W. H. Auden's 1941 course, which had **6,000** pages of reading, as
  a site covering all **35** major works. Critic agents reviewed every word, and fact-checkers compared
  claims with sources. Mollick's own cross-checks, and checks with other advanced AIs, found no major
  errors. However, the
  first version was "accurate and joyless", the second a "kiddie game" about ringing bells, and its
  poem readings ignored what Auden had written about them. Each fix took minutes once he pointed out
  the problem.

### Research it produced faster than anyone checked

- **"The One-Dollar Company."** Fable chose an open question, found the data and natural experiments,
  and wrote the plan, code, and paper. It estimated that new registrations rose **about 17%** when
  Colorado cut its LLC fee from **$50 to $1**, and fell **about 17%** when the UK raised its fee from
  **£12 to £50**. Later records of business activity did not change comparably, which suggests the
  extra firms were not high quality.
- Mollick calls the result ahead of what he would expect from second-year PhD students, but says it is
  not publishable as it stands. It runs **182** pages, because every critique added an analysis and
  nothing was cut. Two GPT-6 Pro reviews found issues, and the revisions added "Claudespeak".
- **It was not actually preregistered.** The plans stayed inside the project, and some were written
  after earlier results. **No human has fully checked the results**, Mollick included. He concludes
  that AI "can now produce research faster than anyone can read it".
- A second project read **1,186** stories to test whether stories follow a few emotional arcs. It went
  more smoothly; its main problem was the same Claudespeak.

### A multi-agent project that built a bureaucracy

- From a one-paragraph prompt for an endless journey through portal-linked 3D worlds, Claude had
  **204** worlds live after twenty hours, and there are now over **450**. By day ten a lead agent was
  running **28** teams in parallel. Claude estimated about **25,000** agent runs, most of them single
  tasks such as judging an image.
- The agents built **328** worlds in the first two days. Quality was uneven, and poor coordination
  produced repetition: three separate teams made a cyclone of circling animals.
- When Mollick asked the agents to "polish" what they had, they decided each new version had to beat
  the old one in a blind vote by judge agents on **twelve** test screenshots. The teams then optimized
  their worlds for those screenshots. The lead agent banned the trick and tightened the rules. By the
  next morning there was a rule book Mollick never asked for, with **84** sections. After twelve days
  it had **204** sections and **87,500** words, because rules were added and none removed. Launching a
  world needed an approved idea, three AI judges, and a code review against the rule book, which took
  about a day. Reading the rule book used up much of an agent's working context.
- Output fell to about a dozen worlds a day. A separate team of "consultant" agents reviewed the whole
  process from outside and brought it back to **thirty or more** a day while keeping much of the
  quality control. Mollick did not read their recommendations, which he found too long and dense.

### Where the jaggedness now sits

- Knowing when your own work is not good enough "is a large part of what makes someone an expert",
  and Mollick says it is the part Fable does least reliably.
- Some problems started with him: the rule book grew from his vague instruction to "polish". He often
  could not tell whether a failure came from the team or from how it was managed. He says this is a
  question he never had to ask about software.

## Why it matters

[[Automated AI Research]] gains a concrete case of research generated faster than humans verify it,
including a requested preregistration that did not actually happen.
[[Benchmark Optimization]] gains a small, legible case of Goodhart's law inside an agent
organization: judges scored twelve fixed screenshots, so builders optimized for those screenshots.
[[Anthropic]] gains an independent, pre-launch account of Fable 5.2. [[Ethan Mollick]] gains a second
source that moves his argument from how agents coordinate to how they judge their own work.
[[Multi-Agent Coordination]] and [[LLM-as-a-Judge]] gain the rule-book and screenshot-judging
failure modes.

## Tensions / open questions

- **Anecdote, not measurement.** There are no baselines, repeated trials, or failure rates. Mollick
  chose digital tasks the AI could do largely alone, and he steered the longer projects.
- **Access and disclosure.** He had early access with unmetered tokens. He discloses that he takes no
  money from AI labs, would not benefit from Anthropic's likely IPO, and that Anthropic did not see the
  post in advance.
- **Unverified outputs.** The 17% estimates come from an AI-written paper that no human has fully
  checked, so they should not be cited as findings. The "25,000 agent runs" figure is Claude's own
  estimate.
- **Naming and counts.** The post uses "Claude" and "Fable" interchangeably. The number **204** refers
  both to the worlds live after twenty hours and to the rule book's section count after twelve days.
  These are different quantities that happen to coincide.
- **Missing media.** The one-shot video and other videos are not in the capture, so claims about them
  rest on Mollick's description.

## Affected pages

- [[Automated AI Research]]
- [[Benchmark Optimization]]
- [[Anthropic]]
- [[Ethan Mollick]]
- [[Multi-Agent Coordination]]
- [[LLM-as-a-Judge]]

## Raw capture

- [[knowledge-base/raw/sources/Fable 5.2 and Jagged AGI]]

## Citations

- Canonical URL: <https://www.oneusefulthing.org/p/fable-52-and-jagged-agi> (the capture's URL
  carried a `utm_source=tldrnewsletter` parameter, removed here).
- By Ethan Mollick, published on One Useful Thing on November 10, 2026; captured November 11, 2026.

## Related pages

- [[Ethan Mollick]]
- [[Ethan Mollick - The Dot and the Swarm]]
- [[Automated AI Research]]
- [[Benchmark Optimization]]
- [[Anthropic]]
- [[Multi-Agent Coordination]]
- [[LLM-as-a-Judge]]
- [[Agent Delegation]]
- [[Zvi Mowshowitz - AI R&D Is Accelerating Towards Potential RSI in 2027]]
- [[PSI Research - A Proof of the Aaronson-Ambainis Conjecture]]
- [[@0xCodez - Build a Self-Improving Agent System with Fable 5 in 14 Steps]]
