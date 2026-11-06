---
type: source-summary
created: 2026-11-06
updated: 2026-11-06
source_id: src-2026-10-27-anthropic-agents-judgment-calls
source_title: "How AI agents shape experts’ judgment calls"
source_author: "Amaç Herdağdelen, Hailey Joren, Alex Tamkin (Anthropic)"
source_url: "https://www.anthropic.com/research/agents-judgment-calls"
tags:
  - source/summary
  - human-oversight
  - ai-agents
  - evaluation
source_ids:
  - src-2026-10-27-anthropic-agents-judgment-calls
status: active
---

# Anthropic - How AI Agents Shape Experts' Judgment Calls

## Summary

An Anthropic Research post reporting a randomized controlled trial in which professional analysts
used Claude Code for a realistic causal-inference task. The task contained four analytical choices
with two defensible options each, plus a final recommendation. For each analyst and each decision, a
hidden coin flip set which option the agent would favor. The agent was told to argue honestly for
that lean, change its mind if the evidence demanded it, and never mislead. Analysts chose their
agent's lean **86%** of the time across the four analytical decisions, against the roughly **50%**
expected if the agent made no difference. They often explained their choices in the agent's words
without crediting it, and those who followed the lean were about as confident and as likely to call
the recommendation their own as everyone else. The authors argue that a human sign-off is an
independent check only if the human's judgment is their own, and that this kind of deferral is hard
to detect where there is no correct answer.

## Key claims

### Design

- **61** analysts were recruited from a pre-screened pool: they had passed a causal-inference
  knowledge check, used Python or R regularly, and had hands-on observational causal-analysis
  experience. **11** chose not to use the agent and are excluded unless noted, leaving **50**.
- The task was set at the fictional Greenfields Farming Cooperative, where about **40%** of members
  had enrolled in a paid advisory program. The board would expand it only if productivity improved
  by roughly **3–4%**, without saying how productivity should be measured.
- Four decisions were deliberately left open: outcome (yield per hectare or per unit of operating
  cost), comparison method (difference-in-differences or statistical adjustment), coverage
  (enrolled farms or the whole membership), and weighting (equal or by production). A final
  recommendation was to roll out or discontinue, with a one-year extension allowed. Each analytical
  choice could move the estimate by several percentage points.
- The leans were set in a hidden system prompt. Analysts worked in browser-based VS Code with Claude
  Code running **Claude Opus 4.8** at High effort. Median time was **65 minutes** (half took
  **50–79**). Of the 50, **65%** held a master's or doctorate or had six or more years of
  experience, and **90%** of the **48** survey respondents rated themselves proficient or expert.
- A separate AI model coded each submission's choices from the code, and the authors resolved
  disagreements with the analyst's own survey answer.

### Effects

- Lean match by decision: **92%** outcome, **82%** comparison method, **81%** coverage, **90%**
  weighting. In the figure, the share choosing option A moved **62 to 82 percentage points**
  between the two lean conditions.
- The recommendation moved less: **54%** recommended roll-out when the agent leaned that way versus
  **36%** otherwise, a gap the figure labels **17 points**. The authors attribute the weaker effect
  to the recommendation largely following from whether the estimate cleared the threshold. Using
  only the four analytical leans, a statistical model predicted **82%** of recommendations, against
  **61%** for always guessing the most common one (extensions excluded).
- In **38** cases an analyst had stated a preference before the agent voiced its lean. They switched
  **60%** of the time when it disagreed versus **6%** when it agreed: a **54**-point gap with a
  95% confidence interval of **24 to 82** points. The authors note a possible selection effect.
- Of **10** characteristics tested, including experience, expertise, education, quiz score, trust
  in AI, and AI use, only age reached significance, and it disappeared after correction for multiple
  comparisons. Little variation existed to explain.

### Self-report did not reveal the influence

- **52%** of the 48 respondents rated the recommendation more their own than the agent's, and
  **35%** mostly or entirely their own. That group's choices still shifted about **65** points
  toward the lean versus **79** for the rest, a difference within the margin of error. Confidence
  was **71** for analysts who followed the lean on all four decisions versus **73** for the rest.
- **77%** repeated the agent's argument in at least one explanation, sometimes word for word, while
  only **15%** credited the agent. Six of the 48 guessed the study concerned AI influence; none
  suspected manipulated preferences.

### The agent still helped

- Of the 11 analysts who worked without the agent, **six (55%)** made serious methodological errors
  versus **three of the 50 (6%)** with it, and they took a median **90** versus **65** minutes. The
  authors warn the groups were not comparable: the no-agent group was smaller and less experienced.

## Why it matters

The vault has treated human review as a control; this is its first randomized measurement of
whether that control is independent. It anchors [[Human Deferral to AI]], reverses the direction of
[[Sycophancy]] (the human aligning to the model), and qualifies the human-review layers in
[[AI-Native Software Development Lifecycle]] and the human-detection evidence in
[[Agent Observability]]. It extends [[Anthropic]]'s record of publishing results that complicate
how its own products are used.

## Tensions / open questions

- **The lean was strengthened on purpose.** With no assigned lean, Claude Opus 4.8 made the same five
  choices in **112 of 123** runs, and the post says the full paper shows unassigned agents have weaker
  preferences and sometimes push back. The 86% figure measures an agent that holds and voices a
  preference reliably, not a default deployment.
- **One task, one field, one model, about an hour.** The analysts were causal-inference experts new to
  farming, without access to stakeholders. Domain experts with stronger views might defer less.
- **Average effects only.** Each participant's own prior view was not recorded, so individual
  influence cannot be measured; strength of preference was not measured either.
- **Denominators shift.** The headline analysis uses 50 analysts; most survey figures use 48; the
  experience comparison uses 46 for the master's/doctorate share. The difference between 54% and
  36% is 18 points by subtraction (derived), but the figure labels it 17, presumably because the
  displayed shares are rounded.
- **Vendor research on a vendor product.** This is an Anthropic Fellows study of Claude Code; the
  finding runs against simple adoption marketing, but no independent replication is recorded here.
- The authors' remedies (measuring deferral, agents that argue each option or ask first, institutions
  that decide which calls need human judgment) are proposals, not tested interventions.

## Affected pages

- [[Human Deferral to AI]]
- [[Sycophancy]]
- [[Agent Observability]]
- [[AI-Native Software Development Lifecycle]]
- [[Anthropic]]

## Raw capture

- [[knowledge-base/raw/sources/How AI agents shape experts’ judgment calls]]

## Citations

- Canonical URL: <https://www.anthropic.com/research/agents-judgment-calls> (`utm_*` parameters
  removed). The post links a full paper hosted on Anthropic's CDN, which was not read for this
  summary.
- By Amaç Herdağdelen, Hailey Joren, and Alex Tamkin, through the Anthropic Fellows Program;
  published by Anthropic Research on October 27, 2026; captured November 2, 2026.

## Related pages

- [[Human Deferral to AI]]
- [[Sycophancy]]
- [[Agent Observability]]
- [[AI-Native Software Development Lifecycle]]
- [[Anthropic]]
- [[LLM Application Resilience]]
- [[Agent Security and Governance]]
- [[Anthropic - Would This Change Your Answer (CHIVE)]]
- [[Sri Polkampally et al - LLM-as-Judge When It Works and When It Misleads]]
