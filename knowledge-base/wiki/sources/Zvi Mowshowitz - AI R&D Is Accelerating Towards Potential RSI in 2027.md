---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-09-zvi-ai-rd-acceleration-rsi
source_title: AI R&D Is Accelerating Towards Potential RSI in 2027
source_author: Zvi Mowshowitz
source_url: https://thezvi.substack.com/p/ai-r-and-d-is-accelerating-towards
tags:
  - source/summary
  - recursive-self-improvement
  - evaluation
  - ai-governance
source_ids:
  - src-2026-11-09-zvi-ai-rd-acceleration-rsi
status: active
---

# AI R&D Is Accelerating Towards Potential RSI in 2027

## Summary

Zvi Mowshowitz comments at length on a METR report, published November 5, 2026, that assessed how much
AI is speeding up AI R&D at Anthropic, based on deep access to internal data. As quoted, METR concludes
that as of October 2026 Anthropic is likely improving its models' capabilities on well-specified tasks
at **around twice** the March 2024-October 2025 rate. It says it "would not be surprised if the true
acceleration was closer to 1.3x or 3x". It attributes **a majority, "perhaps ≈80%"**, of current
acceleration to AI and sees no clear bottlenecks over the next 12 months. Anthropic redacted "a
majority of the evidence we found most informative", so METR says the public must rely on its
judgment more than is ideal. Zvi adds his own reading: the result was predictable, full recursive
self-improvement (RSI) in 2027 is not the favorite but would no longer surprise him, and Congress
should see the unredacted report and consider banning RSI. The post also collects reactions from
METR staff, an Anthropic cofounder, critics, and policymakers. This summary keeps three layers
separate: what METR reports, what Zvi concludes, and what third parties say. The METR report itself is
not captured; everything attributed to it here comes through Zvi's quotations.

## Key claims

### What METR reports (quoted by Zvi)

- **Headline benchmark finding.** Since October 2025, Anthropic's scores on **AECI**, "Anthropic's
  version of the Epoch Capabilities Index", have grown at an estimated **1.9x** the pre-October 2025
  rate, with a **95% confidence interval of 1.5-2.8x**. METR describes this as "roughly two years of
  historical progress over the last year".
- **Not compute.** METR says it is "confident that the acceleration was not due to an acceleration in
  the scaling of training compute"; the supporting evidence is redacted.
- **Attribution.** Non-AI factors likely influenced the acceleration in late 2025, with many details
  redacted. METR guesses that a majority, "perhaps ≈80%", of the October 2026 acceleration is due to AI,
  "with substantial uncertainty".
- **Mostly assistance, not autonomy.** METR was told that R&D is accelerated mainly through AI
  assistance rather than fully autonomous contributions. Researchers described "signs of life" that
  autonomous contributions could become significant soon.
- **Uplift evidence is soft.** Interviews gave "a quite wide range of estimates, but centered around a
  2x acceleration". Claude classified the interview quotes as **2 Yes, 3 Leans yes, 4 Borderline/unclear,
  0 Leans no, 2 No**, which METR reads as "mildly in favor" of 2x or more. Slack-poll self-reports of AI
  uplift reflect "low-effort consideration" but show consistent growth, reaching **12x** in October 2026.
- **Bottlenecks.** METR saw no evidence of significant bottlenecks from algorithmic progress, training
  compute, experiment compute, or data in the next 12 months. Its understanding "changed several times"
  as it received more detail, so it is not confident.

### What METR could see, and what was redacted

- The summarized access list has **10** items. It includes internal benchmark scores and AECI for
  internal models, pretraining and RL efficiency histories, headcount and attribution, training compute
  by domain, team uplift surveys, lines of code and pull requests, agent inference spend, documents on
  autonomous contributions, and **~15** interviews with key staff.
- In exchange, Anthropic could redact anything. METR submitted a **~100-page** full report. Anthropic
  described the redactions as "aimed at removing confidential information that could accelerate other AI
  developers". METR says the public version does not achieve "transparency about evidence".
- Redacted items include more detailed acceleration estimates by pipeline stage, the compute, data, and
  algorithm breakdown, answers to limitation questions, and **forecasts for a future model**. A planned
  study of Anthropic's compute allocation was postponed, "allegedly due to concerns about focus".
- Models in the analysis go by METR's codenames: Unreleased 2022, **Model 2** (finished training July
  2026), **Model 3** (August-September 2026), and **Model 4** (September-October 2026). Dates use
  internal availability to most Anthropic employees rather than public release. METR says this shows
  slightly more acceleration because Anthropic now holds models longer before release.

### How fragile the AECI number is

- **Including non-Anthropic models lowers the estimate to 1.4x.** METR also suggests that Anthropic's
  earlier models may have underperformed their true capability on benchmarks.
- **Benchmarks are saturating.** Model 4 scores **above 50%** on every AECI benchmark on which it was
  tested. METR judges the measured acceleration "reasonably robust" to this.
- **Elicitation and the curve shape.** Token spend "may be too low to maximally elicit models". The
  logistic link function "could be misspecified on a few benchmarks". Alternative link functions give
  different acceleration rates and fit about equally well out of sample, and METR says it has no reason
  to prefer one. It also checked whether Anthropic could be overfitting to internal metrics.
- Charles Foster (METR) explains that each ECI point multiplies a model's odds of success. Historically,
  each **5-point** increase corresponded to roughly a doubling of time horizon.

### Is it acceleration or a one-time jump?

- **Toby Ord:** if a level shift from the Mythos pre-train is allowed as well as a slope change, the
  slope change "drops to about 1.4x". **Woody Lee:** Anthropic was running behind the composite frontier,
  and relative to that frontier the speedup is 1.4x.
- **Buck Shlegeris** replies that the graph is the only unredacted part of METR's analysis, and that
  METR's appendix says it considered and rejected the one-time-jump hypothesis for redacted reasons.
  His own phrasing is that AI R&D is "sped up 1.7x".
- **Peter Wildeford:** RL's share of compute grew from **4% to 24%** between 2024Q1 and 2025Q3. With a
  2-3 quarter lag, that lines up with a **~1.4-2.2x** speedup, and catch-up on RL may explain part of
  Anthropic's **1.9x**. The all-developer frontier still accelerated **~1.4x**. Because RL share is
  plateauing (**50% to 53% to 55%**), he predicts benchmark growth should slow by mid-2027 if RL is
  the driver. Citing METR, he notes that engineers can be sped up **~12x** while overall progress
  speeds up only **~1.4x**, because of compute limits and Amdahl's law. He trusts METR's private
  analysis that AI is responsible for at least 1.4x.
- **Ajeya Cotra (METR):** under a simple Cobb-Douglas model in which experiment compute and labor matter
  about equally, doubling overall progress needs a **(~2-3x)^2 = ~4-9x** labor speedup. Taken at face
  value with smooth acceleration, this "naively implies" extreme superintelligence within a year.
- **Ryan Greenblatt (METR),** working only from the public report, gives "a very rough estimate" of
  **~4.5x** acceleration of AI software progress (3 × 2^0.6). In the AI 2027 scenario this happens around
  March 2027. He had previously expected **1.15x-1.3x** for 2026 and says he cannot state his
  all-things-considered timelines.

### The August risk report and Anthropic's response

- METR also reviewed Anthropic's August 2026 Risk Report. That report's public version said acceleration
  was "less than a factor of 2", while the private version's figures imply **1.97**. METR says "around 2"
  would be a better description, while concluding the threshold was probably not crossed then.
- Anthropic cofounder **Sam McCandlish** says METR "had complete independence to form their own
  conclusions" and that many conclusions match his. He calls the redactions a tradeoff, made because the
  information is commercially sensitive and could give others "a roadmap" to go faster. He says Anthropic
  will publish its own analysis, including where it stands against its Responsible Scaling Policy. He
  also says this work is separate from the embedded third-party evaluators in Anthropic's commitment to
  pacing the frontier.

### Zvi's own reading and the policy debate

- Zvi says the result did not surprise him. He notes that the ~1.7x estimate in the Haiku system card
  rises to ~1.9x once internal models are included. He also observes that the report's listed upside and
  downside risks are asymmetrical.
- He presumes that METR's need to keep Anthropic's cooperation, and that of other labs, pushes it
  toward *underreporting* acceleration and danger. His guess is that Anthropic "redacted too
  aggressively". He quotes Nathan Calvin, who says labs have "swiss cheese level security" for
  everything but model weights. On Calvin's reading, the redactions are unlikely to stop determined
  leaks but do make good-faith observers less likely to believe the claims. He treats the postponed
  compute-allocation study as a setback for "pacing the frontier" proposals.
- Reactions range widely. Jake Mendel now puts superintelligence within 18 months, absent a slowdown, at
  more than 50%. Benjamin Todd extrapolates to Claude leading internal research by mid-2027. Dylan
  Bowman (Apollo Research) says he "learned approximately nothing" because of redactions, puts Apollo's
  internal uplift at ~1.5-2x, and names data uplift as an unaddressed alternative explanation.
- On policy, Kelsey Piper wants Congress to read the unredacted report and ban RSI if it holds up. Alex
  Bores and Rep. Greg Casar call for a ban. Neil Chilson defines RSI narrowly as fully relinquishing AI
  R&D to AI "with no ability to monitor and stop the process". Zvi argues that such a narrow definition
  would permit a 99.9%-automated process with only an illusion of control, and that legal definitions
  must be robust.

## Why it matters

This is the vault's first quantitative, deep-access estimate of AI accelerating a frontier lab's own
R&D. It moves [[Recursive Self-Improvement]] from argument toward measurement and directly challenges
the forecast of no sustained ECI acceleration recorded there. [[Automated AI Research]] gains interview
and survey evidence that the gain comes from assistance, faster experiments, and cheaper
implementation rather than autonomy. [[Benchmark Optimization]] gains a case in which saturation,
link-function choice, and internal-metric overfitting all sit under one headline number. [[Anthropic]]
and [[METR]] each gain a record of how access, redaction, and disclosure wording shaped a public safety
claim. [[Epoch AI]] supplies the index that AECI forks, and [[Embedded Evaluation]] is the access model
both McCandlish and the critics are arguing about.

## Tensions / open questions

- **Secondhand throughout.** The METR report, Cotra's post, and the threads are not captured. Every METR
  claim here is as quoted by Zvi, who argues for a strong conclusion and explicitly favors short
  timelines.
- **The numbers do not reconcile cleanly.** The conclusion says "around twice" with a 1.3x-3x range. The
  AECI finding is 1.9x with a 95% CI of 1.5-2.8x. Shlegeris says 1.7x, Zvi writes METR's bounds as
  "something like [1.3, 2.8]", and alternatives give 1.4x. They measure different things or come from
  different sources and should not be merged.
- **Self-reported uplift is weak evidence.** METR calls the Slack polls low-effort. One interviewee
  guesses only 15-20% is due to AI and does not believe self-reported productivity increases.
- **The decisive evidence is redacted**, including the reasons for rejecting the one-time-jump
  explanation. Outsiders cannot test it. Anthropic is the subject and controlled the redactions, while
  METR and Anthropic both describe METR's conclusions as independent.
- **Benchmark acceleration is not real-world impact.** METR names reasons it could overstate or
  understate real-world effects. Saturation and the choice of link function remain open.
- **Typos in the capture:** "verificable" (quoting an Anthropic post) and "verison".

## Affected pages

- [[Recursive Self-Improvement]]
- [[Automated AI Research]]
- [[Benchmark Optimization]]
- [[Anthropic]]
- [[METR]]
- [[Epoch AI]]
- [[Embedded Evaluation]]
- [[Ramez Naam]]

## Raw capture

- [[knowledge-base/raw/sources/AI R&D Is Accelerating Towards Potential RSI in 2027]]

## Citations

- Canonical URL: <https://thezvi.substack.com/p/ai-r-and-d-is-accelerating-towards> (the capture's URL
  carried a `utm_source=tldrai` parameter, removed here).
- By Zvi Mowshowitz, published on his Substack on November 9, 2026; captured November 11, 2026.
- The underlying report is METR's Anthropic AI R&D acceleration assessment, dated November 5, 2026 in
  its URL, together with METR's review of the August 2026 Anthropic Risk Report. Neither is captured.

## Related pages

- [[Recursive Self-Improvement]]
- [[Automated AI Research]]
- [[Benchmark Optimization]]
- [[Anthropic]]
- [[METR]]
- [[Epoch AI]]
- [[Embedded Evaluation]]
- [[Ramez Naam]]
- [[Ramez Naam - Can a Million AI Agents Create Superintelligence]]
- [[James Tillman - Two Kinds of Test-Time Scaling]]
- [[Ethan Mollick - Fable 5.2 and Jagged AGI]]
- [[OpenAI - The Hugging Face Incident and the Road Ahead]]
