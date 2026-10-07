---
type: source-summary
created: 2026-10-07
updated: 2026-10-07
source_id: src-2026-10-05-faik-ai-native-software-factory
source_title: "How to build an AI-native software factory"
source_author: Adam Faik
source_url: https://www.theaithinker.com/p/how-to-build-an-ai-native-software
tags: [source/summary, coding-agents, sdlc, production, cost]
source_ids: [src-2026-10-05-faik-ai-native-software-factory]
status: active
---

# Adam Faik - How to Build an AI-Native Software Factory

## Summary

Faik synthesizes more than 70 sources, mostly large technology companies' self-reports, into a
software-factory adoption argument: measure the current bottleneck, buy a capable agent for
verifiable toil, start in shadow mode, and build only the infrastructure needed to remove the
measured constraint. The target is cost per accepted outcome with quality retained, not tokens
consumed or code generated. This is a secondary synthesis, not a validated rollout recipe.

## Key claims

- Faster code generation can move the bottleneck into review and CI rather than accelerate delivery.
  The article recounts Uber review waits rising from **three hours in 2024 to nine in 2026**.
  Those are reported observations, not an isolated causal estimate of agent adoption.
- Deterministic automation remains a serious baseline. An Uber JUnit migration tried generative AI
  unsuccessfully, then used Shepherd to produce **5,000+ diffs** and migrate **75,000+ test
  classes in four months**, with AI helping on failures. It was not an all-agent migration.
- The proposed buy/build split buys model/tool gateways, sandboxing, and tracing where suitable,
  while building repository-specific warm environments, context/tools, workflow blueprints, and
  promotion policy.
- Warm-start figures have different statuses: Stripe's **10 seconds** is reported behavior,
  DoorDash's **under five seconds** is a target, and Ramp's **30 minutes** is a refresh cadence,
  not a startup latency.
- Blueprints can alternate deterministic setup, checking, and submission with agent work in the
  uncertain steps. An instruction file does not enforce a stage transition or a release gate.
- Adoption rates depend on definitions. Uber's **70% agent-involved PRs in August** and **11%
  background-agent merged PRs in May** describe different categories at different dates; they
  are not a measured sixfold growth experiment.

Faik also includes an **illustrative sample of 200 merged PostHog PRs**, covering roughly
September 28-29 UTC and presented through quoted agent analysis:

| Measure | Reported result |
| --- | --- |
| Human-review median / P90 | 6.1 hours / 160.8 hours |
| No human review | 80/200, or 40% |
| More than 400 changed lines | 57/200, or 28.5% |
| Review median / P90 when bots count | 0.07 hours / 0.53 hours |

Bot reviewers are excluded from the human-review rows; **23 bot-authored PRs remain in the sample**.
Counting bots leaves no unreviewed PRs. The sample was not independently reproduced and should not
be generalized into representative company statistics.

## Why it matters

The useful adoption unit is a verified workflow with an observable queue, not a company-wide
commitment to maximum autonomy. The source supplies a deterministic counterexample to an otherwise
agent-heavy narrative and makes outcome acceptance, review capacity, and full-cost attribution part
of the architecture.

## Tensions / open questions

The article explicitly lacks an example of a 300-engineer company beginning from laptops and
following this path. Large-company success stories carry selection bias. Cost visibility and a
reported 52% cost decline co-occur; the claim that visibility did more than a cap is interpretation,
not a controlled effect. The author's explanatory six-part grouping is not identical to Uber's
original six building blocks.

Public team-thread adoption and [[Jina Yoon - We're Building Multiplayer AI]]'s private task starts
need not conflict: sharing examples, starting work, and publishing artifacts are different moments.
Neither source establishes a universal workspace default.

## Affected pages

- [[AI-Native Software Development Lifecycle]]
- [[Agent Workflow Maturity]]
- [[Coding Agent Harness]]
- [[Agent Observability]]
- [[Agent Skill]]
- [[Legacy Code Modernization with AI Agents]]
- [[AI Agents in Production]]

## Raw capture

- [[How to build an AI-native software factory]]

## Citations

- Canonical URL: <https://www.theaithinker.com/p/how-to-build-an-ai-native-software>
- Published October 5 and captured October 7, 2026.

## Related pages

- [[Simon Willison - 2026 in LLMs (so far)]]
- [[Replit - Free the Models - Harness Design at the Frontier]]
- [[Jina Yoon - We're Building Multiplayer AI]]
- [[Tool Roster Economics]]
