---
type: source-summary
created: 2026-10-27
updated: 2026-10-27
source_id: src-2026-10-16-west-eval-engineering-lessons
source_title: "Four evaluation engineering lessons learned from building agent plugins"
source_author: Casey West
source_url: https://cloud.google.com/blog/topics/developers-practitioners/four-eval-engineering-lessons/
tags: [source/summary, evaluation, ai-agents, llm-as-a-judge, observability, google-cloud]
source_ids:
  - src-2026-10-16-west-eval-engineering-lessons
status: active
---

# Casey West - Four Evaluation Engineering Lessons from Building Agent Plugins

## Summary

A Google Cloud blog post by Casey West, Developer Relations Lead for AI Infrastructure & Applied
Engineering, published 16 October 2026. It draws four lessons from evaluating the newly released
Google Cloud Developer plugin for AI coding agents. The opening thesis is "The real challenge of
building an agentic system isn't the construction, it's the measurement."

All four lessons are about what an evaluation looks at:

- the execution trajectory rather than the closing message;
- turn structure rather than a flat list of events;
- a live run alongside a plan-only run;
- golden sets covering the whole harness, model, and tools stack, run as continuous integration.

The evidence is single examples from Google's own build. Apart from an 11-prompt suite, it reports
no counts or aggregate results.

## Key claims

**1. Grade what the agent did, not what it said.** An LLM judge scored the agent's final reply
against a checklist. On the initial 11-prompt suite it marked the plugin as failing three prompts,
but the raw tool-call logs showed all three had passed. One was a Cloud Run cleanup whose rubric
required checking command syntax before running anything. The agent's first step was
`gcloud help run services list`, but its final message warned about permanent data loss instead of
reporting the check. "The grader penalized the agent for doing the right thing simply because it
didn't brag about it in the summary." If a rubric line asks whether the agent ran something, a
judge "is guessing unless you evaluate the actual tool-call trajectory".

**2. A flattened event log hides parallel dispatch.** Harnesses often batch several tool calls into
one assistant turn. In one evaluation, a skill-loading call and two documentation searches were
sent in a single `tool_calls` payload. Activating a skill takes two steps: the first call returns a
short launch stub, and the next turn injects the full instructions. The guidance meant to govern
the searches therefore arrived after they had run. A telemetry extractor that merges calls into a
flat timeline makes this look like an agent ignoring clear instructions. The remedy is to keep turn
structure in the extracted traces.

**3. Run live and plan-only conditions side by side.** Live runs use real, sandboxed credentials
and execute commands. They test whether syntax works, whether parameters serialize cleanly, and
whether the agent holds back before destructive actions. They also "frequently hit an unexpected
permission error on step two and abort" before the behavior under test is reached. Plan-only runs
remove the credentials and ask the agent to explain what it would do, which exposes its reasoning
and routing intent. "Roughly half our most important findings came from the delta between the
two." In one onboarding prompt, the live run was blocked at once on a project-list call. The
plan-only run produced an 8,000-character plan that ignored organization policies, admin approvals,
and governance.

**4. Golden sets for the whole stack, run as CI.** Models, harnesses, and plugin manifest standards
keep changing, so the team treated evaluations as continuous integration. They stress-tested the
harness, the live model, and the tools together on realistic tasks. Each run captures the whole
trajectory and is scored against "golden sets curated by real human experts who know what the
ideal path looks like". A one-shot demo, such as a prompt that builds a 3D game in a single pass,
"is just a vanity metric".

## Why it matters

[[LLM-as-a-Judge]] gains a concrete case of a judge pointed at the wrong artifact. A correct agent
was graded as failing on three of eleven prompts because the judge read a summary, not the
execution record.

[[Multi-Turn Evaluation]] gains two construction rules. The thing being scored is the trajectory.
A second, credential-free condition separates reasoning failures from environment failures.

[[Agent Observability]] gains a requirement on trace format. The extracted record has to keep turn
boundaries, or concurrent dispatch disappears from view.

[[Google Cloud]] gains a first-party account of evaluating one of its own agent products, which
that page's caveat about Google publications covers.

## Tensions / open questions

- **Examples, not results.** Beyond the 11-prompt suite and its three misgraded prompts, the post
  gives no pass rates, no suite sizes for the later lessons, and no before/after comparison. The
  share of findings attributed to the live/plan-only difference is a rough estimate.
- **Self-evaluation.** Google evaluates a Google plugin on Google's blog, with product links. The
  methods transfer; the plugin's quality is not established here.
- **Plan-only changes two things at once.** In the vault's reading, removing credentials and asking
  for an explanation changes the prompt as well as the environment. The difference between
  conditions therefore mixes environment effects with instruction effects.
- **Golden sets need someone to define the ideal path.** Open-ended tasks can have several
  acceptable trajectories, and the post does not say how alternatives get credit.
- **The parallel-dispatch failure starts in the harness.** The post's takeaway sits on the
  evaluation side, in telemetry, while the cause is a skill that never got its own turn.

## Affected pages

- [[LLM-as-a-Judge]]
- [[Multi-Turn Evaluation]]
- [[Agent Observability]]
- [[Google Cloud]]

## Raw capture

- [[Four eval engineering lessons  Google Cloud Blog]]

## Citations

- Canonical URL:
  https://cloud.google.com/blog/topics/developers-practitioners/four-eval-engineering-lessons/
  (email tracking parameters removed).
- Published 16 October 2026. The page title is "Four eval engineering lessons"; the article
  headline, used as `source_title`, is "Four evaluation engineering lessons learned from building
  agent plugins". Author and role come from the byline in the capture. Figures are image-only and
  were not captured as text.

## Related pages

- [[LLM-as-a-Judge]]
- [[Multi-Turn Evaluation]]
- [[Agent Observability]]
- [[Google Cloud]]
- [[Agentic Testing]]
- [[Agent Skill]]
- [[Coding Agent Harness]]
- [[Tool Use and Function Calling]]
- [[Model Context Protocol]]
- [[AI Knowledge Base Overview]]
