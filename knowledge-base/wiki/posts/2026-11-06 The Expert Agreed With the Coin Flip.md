---
type: social-post
created: 2026-11-06
updated: 2026-11-06
tags:
  - post
  - human-oversight
  - ai-agents
platforms:
  - linkedin
  - x
pages_used:
  - "[[Human Deferral to AI]]"
  - "[[Anthropic - How AI Agents Shape Experts' Judgment Calls]]"
  - "[[axjns.dev - Testing Celln's Boundary]]"
  - "[[Yun Chi et al - The Surprising Leadership Dynamics in Agent Swarms]]"
  - "[[Factory Research - Droid 1.0 - Building a Frontier Harness]]"
  - "[[General Reasoning - How to Train a Swarm]]"
topics:
  - human deferral to AI
  - independent review
  - judgment calls
  - agent influence
covers_from: 2026-10-30
covers_through: 2026-11-06
status: ready
---

# The Expert Agreed With the Coin Flip

## LinkedIn post

When an AI agent does the hands-on analysis, we assume the expert still makes the calls that matter: what to measure, how to read ambiguous evidence, what to do next. Their sign-off is meant to be the independent check.

A randomized trial from Anthropic Research suggests that on judgment calls, where more than one answer is defensible, that check is weaker than it looks.

Fifty professional analysts used Claude Code, Anthropic's AI coding agent, to advise a fictional farming cooperative on whether to expand a paid advisory program. They faced four analytical choices with two defensible options each, such as measuring productivity per hectare or per unit of operating cost.

For each analyst and each choice, a hidden coin flip decided which option the agent would favor. The agent was told to argue honestly for it, change its mind if the evidence turned, and never mislead.

Analysts chose the agent's assigned option 86% of the time. With no influence, you would expect about 50%.

Those choices then shaped the estimated productivity gain behind the final recommendation. Excluding analysts who proposed a one-year extension, a statistical model using only the four coin flips correctly predicted 82% of recommendations, against 61% for always guessing the most common one.

Error checks assume a correct answer exists; with two defensible options, the work can look sound either way. Asking afterwards may not help either. Analysts who called the recommendation more their own still shifted about 65 percentage points toward the agent's lean on average, against 79 for the rest, a difference within the margin of error. And 77% repeated the agent's arguments in at least one explanation, sometimes word for word; 15% credited it.

The limits: the researchers strengthened the agent's preferences on purpose and say agents without an assigned lean have weaker ones, so everyday effects may be smaller. It covered one task, field and model for about an hour, with analysts new to farming. It is also Anthropic research on its own product, and I know of no independent replication. Nor is it a case against agents. Analysts working without one made serious methodological errors far more often, though that group was small, self-selected and less experienced.

So reviewing harder is not the fix: review shows whether work is wrong, not whose judgment a defensible choice reflects. The authors suggest agents that ask for the person's view before offering their own, or argue each option. These are untested proposals, and raising every open choice would overwhelm people, so organizations must decide deliberately which calls need a person's own judgment.

A sign-off is evidence of independent judgment only if the judgment was formed independently.

For which decisions would you record your own view before the agent weighs in?

Source: Amaç Herdağdelen, Hailey Joren, Alex Tamkin (Anthropic)
https://www.anthropic.com/research/agents-judgment-calls

#HumanInTheLoop #AIOversight #AIAgents

## X post

Counts include spaces and punctuation; each URL counts as 23 characters under X's link
weighting. Number labels, counts, and code fences are outside the copy-ready text.

**A) Standalone** (277 chars):

```text
Anthropic trial: a hidden coin flip set which of two defensible options an AI agent argued for. Expert analysts chose it 86% of the time, vs ~50% by chance. Neither was wrong, so error checks miss it. Untested fix: get the expert's view before the AI's. https://www.anthropic.com/research/agents-judgment-calls
```

**B) Thread:**

1. (245 chars)

```text
When an AI agent does the analysis, the expert's sign-off is meant to be the independent check. A randomized trial suggests that on judgment calls, where more than one answer is defensible, the agent's preference can quietly become the expert's.
```

2. (228 chars)

```text
Anthropic Research gave 50 professional analysts an AI coding agent and a realistic task: advise a fictional farming co-op on whether to expand a paid advisory program. Four choices along the way each had two defensible options.
```

3. (267 chars)

```text
For each analyst and each choice, a hidden coin flip set which option the agent favored. It was told to argue honestly, change its mind if the evidence turned, and never mislead. Analysts picked the agent's option 86% of the time, against about 50% with no influence.
```

4. (236 chars)

```text
Those choices shaped the estimated gain behind the final recommendation. Leaving out one-year extensions, a model using only the four coin flips correctly predicted 82% of recommendations, vs 61% for always guessing the most common one.
```

5. (269 chars)

```text
Error checks assume a right answer, but both options were defensible. Asking analysts may not help: those calling the result more their own shifted about as much (65 vs 79 points, within margin of error). 77% reused the agent's arguments at least once; 15% credited it.
```

6. (280 chars)

```text
Limits: the lean was strengthened on purpose; the authors say unassigned agents have weaker preferences. One task, field and model, about an hour; Anthropic studying its own product. Analysts without the agent made serious errors far more often, but were few and less experienced.
```

7. (273 chars)

```text
Review shows whether work is wrong, not whose judgment a defensible choice reflects. The authors propose, untested, agents that ask for the person's view first or argue each option on the key calls. Herdağdelen, Joren and Tamkin, Anthropic Research: https://www.anthropic.com/research/agents-judgment-calls
```

**Ship:** Thread. It sets up the sign-off assumption, explains the hidden coin flip before
giving the 86% result, shows that the leans reached the final estimate, and keeps the
strengthened-lean, single-task, and vendor caveats in the penultimate post. The standalone
keeps the case, the result with its no-influence comparison, and the action, but drops the
recommendation model, the self-report comparison, and the error-rate contrast.

## Hook variants

1. **Plain situation:** When an AI agent does the hands-on analysis, we assume the expert still makes the calls that matter. Their sign-off is meant to be the independent check.
2. **Concrete number:** A hidden coin flip decided which of two defensible options an AI agent argued for. Professional analysts went with it 86% of the time.
3. **Myth correction:** A human sign-off is an independent check only if the judgment behind it was formed independently.

**Recommended:** The plain situation for LinkedIn: it gives a reader outside data analysis
a familiar workflow before introducing the experiment. X uses the same situation in its
first post and saves the 86% result until the coin flip and the "about 50%" comparison
have been explained.

## Why this topic

**Window:** 2026-10-30 through 2026-11-06, inclusive, anchored to the newest active ready
post's `covers_through`, not a fixed seven-day schedule. Two ingest entries cover 28 source
summaries: the October 30 "Measured Boundaries for Memory, Tools, and Self-Improvement"
ingest (seven sources) and the November 6 "Coordination Records, Trained Swarms, and
Borrowed Judgment" ingest (21 sources). The Git cross-check covered 24 commits and 128 wiki
paths; the 11 paths outside those ingests' edges were older-source repairs, lint, and post
maintenance, and no unlogged source summary appeared.

Four direct ByteByteGo sources in the window were excluded before selection: the Apple
on-device model, Uber agent gateway, Netflix performance-engineering, and Nvidia Nemotron
summaries. The October 30 sources were scored in the previous run; their two eligible
runner-ups (on-policy self-training retention and Decagon's falsifiable proposals) remain
archived candidates and did not supply this run's example or claims.

Scores are editorial judgments, 1-5. Clarity and completeness must each be at least 4;
a high total cannot override either gate.

| Angle and source | Clarity | Completeness | Surprise | Concreteness | Reach | Freshness | Total | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| A hidden coin flip steered experts' judgment calls, and review could not see it - [[Anthropic - How AI Agents Shape Experts' Judgment Calls]] | 5 | 5 | 5 | 5 | 5 | 4 | 29 | Selected: one randomized design, a plain no-influence comparison, explicit limits, and a practical oversight question. |
| A failed attack probe does not show which control stopped it - [[axjns.dev - Testing Celln's Boundary]] | 4 | 4 | 3 | 5 | 3 | 5 | 24 | Eligible runner-up; a careful single retained run, but it needs sandbox and system-call vocabulary. |
| Planning is not leading: plans were common, but orders that changed teammates' decisions were rare - [[Yun Chi et al - The Surprising Leadership Dynamics in Agent Swarms]] | 4 | 4 | 4 | 4 | 3 | 5 | 24 | Eligible runner-up; first-party, and its name-order comparison lacks denominators. |
| A harness fix that helps some models can cost others - [[Factory Research - Droid 1.0 - Building a Frontier Harness]] | 4 | 3 | 4 | 4 | 3 | 3 | 21 | Rejected by completeness gate: the per-model figures are single-task results, and the angle neighbours the archived local-metric candidate. |
| A trained swarm wins on wall-clock time rather than equal-compute accuracy - [[General Reasoning - How to Train a Swarm]] | 3 | 3 | 4 | 3 | 3 | 4 | 20 | Rejected by clarity gate: benchmark results survive only as chart geometry, with too little benchmark detail for a cold reader. |

The selected spine is [[Human Deferral to AI]]. Its second source, the X engineering
rebuild, is not used in the public copy; every public empirical claim comes from the
Anthropic study, read directly in its capture. The public copy contains one example and
no supporting product tour.

**Anti-repeat:** No earlier post used this spine or human deferral as a topic. The
October 23 post concerned an AI model carrying a message in an image's visible geometry,
an information channel a monitor might overlook; this post concerns whether a human
reviewer's judgment is independent of the agent it checks. The archived McAteer candidate is about an AI
supervisor's attention cost, not whose judgment a human sign-off reflects. Freshness is
scored 4 rather than 5 because the broader oversight theme sits next to the October 23
spine, [[Chain-of-Thought Monitoring]], which remains in cooldown.

## Reader check

**Passed:** reread the LinkedIn body, standalone, and connected thread without relying
on these notes. Each preserves the situation, claim, example, mechanism, limit, and action.

| Cold-reader question | LinkedIn and thread | Standalone |
|---|---|---|
| What is the situation? | An AI agent does the analysis; the expert's sign-off is assumed to be the independent check on the calls that matter. | An AI agent argues for one of two defensible options while an expert decides. |
| What is the single claim? | On judgment calls with more than one defensible answer, the agent's preference can quietly become the expert's. | Experts largely took the side the agent was secretly assigned. |
| What example supports it? | Fifty analysts, a farming-cooperative task, four two-option choices, a hidden coin flip per choice, and 86% agreement against about 50% with no influence. | The same coin-flip trial and the 86% versus about 50% comparison. |
| Why did it happen? | The agent made an honest case for its assigned side; the leans then shaped the estimated gain behind the recommendation; error checks assume a correct answer, and asking afterwards may not reveal the influence. | Neither option was wrong, so error checks miss it. |
| What is the limit? | Deliberately strengthened lean, one task, field and model for about an hour, vendor research without known replication; the no-agent comparison group was small and less experienced. | The fix is marked untested; the result is attributed to one Anthropic trial. |
| What should change? | Decide which calls need a person's own judgment, and consider the authors' untested proposals: ask for the person's view first, or have the agent argue each option. | Get the expert's view before the AI's, as an untested fix. |

The LinkedIn conclusion completes the oversight argument before the closing question.
"Judgment call" is defined on first use as a decision with more than one defensible
answer. "Percentage points" appears only beside a comparison of two groups. No acronym,
benchmark, or specialist metric needs an external explanation.

## Fact check

**Passed:** checked every public factual sentence against the direct Anthropic evidence
below. LinkedIn has 467 words including attribution and hashtags, above the usual
450 because the limits paragraph and the untested-proposal hedge were kept rather than cut.
The X standalone is 277 characters; the seven thread posts are 245, 228, 267, 236, 269, 280, and 273
characters under the declared link weighting. The only non-ASCII characters are in the
authors' names.

| Public claim group | Direct support and boundary |
|---|---|
| Experts are assumed to make the calls that matter; a sign-off is treated as an independent check | Raw capture's opening, its AI-safety paragraph ("a human reviewer is only an independent check if their judgment is their own"), and its institutions paragraph; [[Human Deferral to AI]] current synthesis. |
| A randomized trial with 50 professional analysts using Claude Code on a fictional farming-cooperative task | Anthropic summary study design; raw study design. 61 were recruited and 11 chose not to use the agent; the 50 are the agent users. Claude Code ran Claude Opus 4.8; the model name is omitted as unnecessary for the claim. |
| Four analytical choices, each with two defensible options, including yield per hectare or per unit of operating cost | Raw list of the four open decisions; the raw calls them "reasonable", the vault "defensible". A fifth decision, the final recommendation, also had a lean and is not counted among the four. |
| A hidden coin flip set each lean; the agent was told to argue honestly, change its mind if the evidence turned, and never mislead | Raw study-design paragraph on the hidden system prompt. "Argue honestly" compresses "make the best honest case" and "the strongest case for it that the data allowed". |
| 86% agreement across the four choices, against about 50% with no influence | Raw results: "Across the four analytical choices... 86%... If the agent's input made no difference, we'd expect about 50%." |
| The leans shaped the estimated productivity gain; using only the four leans, a model correctly predicted 82% of recommendations versus 61% for always guessing the most common one, excluding extensions | Raw results paragraph on the final recommendation, including its parenthetical exclusion of analysts who proposed an extension. |
| Error checks assume a correct answer; with defensible options, the work can look sound either way | Raw "What this means" paragraph on detection; [[Human Deferral to AI]] "Verification and judgment need different controls". |
| Asking afterwards may not help: about 65 versus 79 percentage points on average, within the margin of error | Raw ownership-survey result. The public wording keeps the raw's "may not" hedge rather than the concept page's stronger "did not reveal it". |
| 77% repeated the agent's argument in at least one answer, sometimes word for word; 15% credited it | Raw explanation-survey result; "at least once" is kept in both variants. |
| Strengthened lean; unassigned agents have weaker preferences; effects may be smaller | Raw opening caveat ("the effect might be smaller") and the full-paper note on unassigned agents; concept open question. |
| One task, field and model, about an hour, analysts new to farming | Raw limitations list; Anthropic summary limitations. |
| Anthropic research on its own product, with no known independent replication | Anthropic summary limitation: "no independent replication is recorded here". The public wording is first-person and limited to what is known. |
| Not a case against agents; analysts without one made serious methodological errors far more often, in a small, self-selected, less experienced group | Raw "simple cautionary tale" sentence and the no-agent comparison (six of 11 versus three of 50), with the authors' own non-comparability caveat. |
| Ask for the person's view first or argue each option; untested; raising every choice would overwhelm; decide deliberately which calls need human judgment | Raw "Designing agents differently" and "Changing institutions" paragraphs; Anthropic summary: the remedies "are proposals, not tested interventions". |

**Attribution and exclusion:** The LinkedIn source line matches the summary's
`source_author` exactly; the final X post shortens it to the three surnames plus
Anthropic Research, the citation's publisher field. The canonical URL appears in all
three public forms. The raw capture is Anthropic's own research post and contains no
ByteByteGo reference; neither the spine nor the direct summary carries a ByteByteGo
source ID. All six `pages_used` entries are tracked, outside `wiki/queries/`. The four
unselected source pages support only the editorial shortlist.

**Claims cut rather than compressed:**

- Per-decision agreement (92%, 82%, 81%, 90%) and the 62-82-point shifts: they need the
  option labels and figure explanation; the combined 86% carries the claim.
- The 54% versus 36% recommendation split: the vault records a 17-versus-18-point
  rounding mismatch, and the 82% prediction result makes the point without it.
- Switching after a stated preference (60% versus 6%): only 38 cases, a 95% interval of
  24 to 82 points, and a possible selection effect.
- The 112-of-123 default-run consistency: it needs a separate explanation of unassigned
  preferences; the public copy keeps only the authors' "weaker preferences" caveat.
- The ten characteristics that did not predict deferral, and the age result that
  disappeared after adjustment: low variation and multiple testing.
- Confidence ratings (71 versus 73) and the 52% and 35% ownership shares: secondary to
  the shift comparison.
- The six-of-11 versus three-of-50 error counts: kept qualitatively, because the small,
  self-selected group would need its own setup.
- The raw's suggested reason for deferring (views not fully formed; one side argued
  well), and its consensus and skill-loss remarks: not recorded on the wiki pages used.

**Compression check:** The standalone keeps "about 50%" as "~50% by chance", which is the
no-influence baseline under random assignment, and marks the fix as untested. It drops
the recommendation model, self-report comparison, and limits rather than stating any of
them without conditions. The thread keeps "excluding extensions", "on average"
equivalents ("about as much", "within margin of error"), "at least once", the
strengthened-lean and vendor caveats, and the untested status of the authors' proposals.

**Comprehension check:** Each version explains what was randomized, what agreement
would look like without influence, and why ordinary error checks are not built to catch
it. The thread's sequence is situation, setup, randomized lean and result, effect on the
recommendation, why review and self-report miss it, limits, and practical conclusion.
No numerical claim has to borrow its meaning from these notes.

## Attribution

Public example and all empirical claims: **Amaç Herdağdelen, Hailey Joren, Alex Tamkin
(Anthropic)** - https://www.anthropic.com/research/agents-judgment-calls

Direct source: [[Anthropic - How AI Agents Shape Experts' Judgment Calls]].
Primary capture: [[knowledge-base/raw/sources/How AI agents shape experts’ judgment calls]].
Wiki synthesis: the Anthropic study sections of [[Human Deferral to AI]].

The other source pages in `pages_used` document the scored editorial alternatives.
They are not additional public examples or evidence for the Anthropic measurements.

## Hashtags

LinkedIn: `#HumanInTheLoop #AIOversight #AIAgents`

X: none.

## Related pages

- [[Post Archive]]
- [[Human Deferral to AI]]
- [[Anthropic - How AI Agents Shape Experts' Judgment Calls]]
- [[axjns.dev - Testing Celln's Boundary]]
- [[Yun Chi et al - The Surprising Leadership Dynamics in Agent Swarms]]
- [[Factory Research - Droid 1.0 - Building a Frontier Harness]]
- [[General Reasoning - How to Train a Swarm]]
