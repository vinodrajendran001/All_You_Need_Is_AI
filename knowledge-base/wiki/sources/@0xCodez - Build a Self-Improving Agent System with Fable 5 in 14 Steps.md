---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-06-11-0xcodez-fable-5-self-improving-agents
source_title: "Build self-improving agent system with Fable 5 in 14 steps : loops, dynamic workflows, routines"
source_author: "@0xCodez"
source_url: "https://x.com/0xCodez/status/2065089060104720776"
tags:
  - source/summary
  - ai-agents
  - self-improvement
  - agent-memory
  - claude-code
source_ids:
  - src-2026-06-11-0xcodez-fable-5-self-improving-agents
status: active
---

# Build a Self-Improving Agent System with Fable 5 in 14 Steps

## Summary

An X long-form post by [[@0xCodez]] presents a 14-step roadmap for building a "self-improving"
agent system around Claude Fable 5, which it says launched on June 9, 2026 as "the first publicly
available **Mythos-class model**". The roadmap stacks four layers — primitives, orchestration
(/goal, Outcomes, Dynamic Workflows, Routines), memory (a five-stage progression and a `STATE.md`
file), and self-improvement (Skills that accumulate lessons, vision self-checks, and handling of the
model's safety classifiers). Its useful core is structural: improvement comes from the system around
a frozen model — an independent grader, a persistent state file read at the start and written at the
end of each session, and lessons written back into reusable Skills. The post claims to be "sourced
from Anthropic engineering posts" and "verified against the launch documentation as of June 2026",
but it is a secondary, promotional course (it advertises the author's Substack) whose experimental
numbers are relayed without links to the underlying reports, and several of its summary claims go
beyond or contradict its own evidence.

## Key claims

### Self-improving is a system property, not weight updates

The post separates **self-learning** (updating weights, which "No publicly available model does …
in production") from **self-improving** (the system around the model changes run over run). It calls
recursive self-improvement "the long-term direction Anthropic itself warned about in May 2026". It
relays an Anthropic quote: "Rather than directly prompting and steering Fable 5, it's often better to
design loops that let the model self-correct in response to environment feedback (e.g., /goal or
Outcomes) and manage its own context (e.g., via memory)."

### Model and access claims

Fable 5 is said to sit "one rung above Opus"; Mythos Preview shipped in April through Project
Glasswing, and Mythos 5 without classifiers "remains Glasswing-only". Claimed capabilities include
days-long sessions in Claude Code or Claude Managed Agents (CMA). Pricing is given as **$10** per
million input tokens and **$50** per million output tokens, with the "existing 90%" prompt-caching
discount, on the Claude API, AWS, Amazon Bedrock, Vertex AI, Microsoft Foundry, and the Enterprise
plan.

### Route by role: orchestrator, workers, graders, fallback

"Fable 5 costs ~5× what Opus 4.8 does per token," so the recommended pattern is "orchestrator on
Fable 5, workers on Sonnet 4.6, graders on Haiku 4.5, fallback to Opus 4.8 on classifier blocks",
described as the "Same pattern Anthropic engineers use internally" without a source.

### /goal and Outcomes: the maker is not the grader

Both primitives share one shape: "an independent grader checks the work, a not-met verdict starts the
next iteration, the loop exits when the grader passes". /goal runs in Claude Code with a plain-text
goal and a model grader; Outcomes runs in CMA with a file-based rubric, a sub-agent grader, and a hard
`max_iterations` bound. The structural rule: "the agent that wrote the code is not the agent that
grades it". It relays the Claude Code team's statement, "We've found that a verifier sub-agent tends
to outperform self-critique with Fable 5", and cites Anthropic engineer Prithvi Rajasekaran on the
difficulty of self-critique.

### Parameter Golf, as relayed

In an Anthropic experiment described from a chart, Fable 5 made structural changes — `TRAIN_SEQ_LEN=2048`
(**−0.0179**), overlapped sliding-window eval (**−0.0207**), int6 QAT plus int6 export (**−0.0163**)
— and "pushed through a quantization regression", while Opus 4.7's first move (`QK_GAIN_INIT=5.0`)
led to a pattern of scalar tweaks. The run lasted "up to 8 hours on 8×H100 GPUs". The post's
conclusion that Fable 5 landed "~6× more improvement than Opus 4.7" is not traceable to a stated
figure in its prose.

### Orchestration primitives: Dynamic Workflows, worktrees, Routines

Dynamic Workflows "shipped in Claude Code on May 28, 2026"; the quoted launch post says Claude creates
"an orchestration plan that it strictly follows". Three of "six documented" patterns are recommended
(fan-out-and-synthesize, adversarial verification, loop until done); classify-and-act and tournament
are mentioned. Git worktrees isolate maker and verifier, exposed in Claude Code as `git worktree`, a
`--worktree` flag, and `isolation: worktree` on subagents. Routines, "launched April 14, 2026 in
research preview", are saved configurations that run on Anthropic-managed infrastructure on schedule,
API, or GitHub-event triggers; the example nightly routine uses an "independent Haiku sub-agent" grader.

### Memory: five stages and a state file

From Anthropic's "Continual Learning Bench 1.0", memory use is framed as **Fail → Investigate → Verify
→ Distill → Consult**. On a SQL exploration task, Sonnet 4.6 "exits at step 1"; Opus 4.7 exits at
step 3 with verification coverage of **7–33% (median ~17%)**; Fable 5 "tends to complete the
progression", reaching **73% (22 of 30)** "In its strongest runs". A `STATE.md` template maps
sections to stages (verified facts, general rules, open failures, lessons learned, last session),
with two rules: "Write before walking away" and "Read at session start".

### Skills compound; vision closes the loop; classifiers need a fallback

"After any non-trivial failure, write the lesson into the Skill itself": `STATE.md` is project-scoped,
while Skills in `~/.claude/skills/` "travel with you". The example Skill carries anti-patterns and an
eval suite in which a newly failing case is added "after Outcomes verifier confirms". A verifier
sub-agent reads screenshots to judge UI work. Fable 5's classifiers reportedly decline cyber, biology,
chemistry, and model-distillation requests and fall back to Opus 4.8; the post says to design for that
fallback and to read the "319-page system card".

## Why it matters

The post is the vault's most explicit practitioner recipe for frozen-weight improvement:
[[Loop Engineering]] gets an independent-grader loop with a hard iteration bound; [[Agent Memory]]
gets a staged account of when memory compounds; [[Agent Skill]] gets the Skill-as-lesson-store
pattern; and [[Continual Learning for Agents]] gets a concrete gate on write-backs. Its routing
recipe is proposed for [[Model Routing]], with its price contradiction kept visible.

## Tensions / open questions

- **Secondary and promotional.** Anthropic experiments, quotes, and dates are relayed without links
  to reports; the vault cannot verify them from this capture. "**9** out of 10 users" have never run
  a compounding system is unsupported.
- **Price contradiction.** "~5×" Opus 4.8 per token conflicts with the vault's
  [[AI Builder Club - Claude Fable 5 - How to Use It and What's Different]], which lists Fable 5 at
  $10/$50 and Opus 4.8 at $5/$25 per million tokens — twice the price, not five times.
- **Classifier scope differs** between sources: this post names cyber, biology, chemistry, and
  distillation; the AI Builder Club guide describes cyber and biology blocks.
- **The conclusion contradicts its evidence.** It says "The model is the same in both halves of every
  comparison", but both comparisons pit Fable 5 against Opus 4.7, so they are model comparisons. It
  also sets Fable 5's best-run **73%** against Opus 4.7's median **~17%**.
- "70%+ of Fable 5's memory advantage disappears" without `STATE.md`, "~6× more improvement", and
  "Two weeks of disciplined writing produces a Skill that materially outperforms" a fresh derivation
  have no stated measurement.
- Temporal oddity: a post dated June 11 describes "controversy in mid-June 2026". The "30-day / 2-year
  terms" for data retention are not explained.

## Affected pages

- [[Loop Engineering]]
- [[Agent Memory]]
- [[Agent Skill]]
- [[Continual Learning for Agents]]
- [[@0xCodez]]
- [[Model Routing]]

## Raw capture

- [[knowledge-base/raw/sources/Build self-improving agent system with Fable 5 in 14 steps  loops, dynamic workflows, routines]]

## Citations

- Canonical URL: <https://x.com/0xCodez/status/2065089060104720776>
- By @0xCodez on X, published June 11, 2026; captured November 11, 2026 via a newsletter link (tracking
  parameters removed). The capture's filename drops the title's colon.

## Related pages

- [[@0xCodez]]
- [[@0xCodez - Graph Engineering with Claude - 14-Step Roadmap from 0 to Graph Architect]]
- [[AI Builder Club - Claude Fable 5 - How to Use It and What's Different]]
- [[Ethan Mollick - Fable 5.2 and Jagged AGI]]
- [[Loop Engineering]]
- [[Agent Memory]]
- [[Agent Skill]]
- [[Continual Learning for Agents]]
- [[Model Routing]]
- [[Recursive Self-Improvement]]
- [[LLM-as-a-Judge]]
- [[Agent Delegation]]
- [[Anthropic]]
