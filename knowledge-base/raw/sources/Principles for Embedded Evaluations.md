---
title: "Principles for Embedded Evaluations"
source: "https://www.apolloresearch.ai/blog/principles-for-embedded-evaluations?utm_source=substack&utm_medium=email"
author:
published:
created: 2026-10-12
description: "A framework for embedded evaluations of frontier AI developers, centered on claim-based, publicly reported assessments."
tags:
  - "clippings"
---
Table of Contents

Introduction

Part 1: Criteria for effective embedded evaluations

Reduces risk

Informs the public

Part 2: Our proposal

Verdicts

Public report

Conclusion

## Introduction

In September 2026, leaders of frontier AI companies [called for pacing the frontier](https://darioamodei.com/post/we-must-pace-the-frontier) of AI development, with embedded evaluators as the first step. Frontier AI companies committed to giving outside evaluators employee-like access to their training, evaluation, and deployment, and some have since published [principles for third-party assessments](https://openai.com/index/priorities-principles-third-party-assessments/).

We are very excited about this development. Public third-party assessments of how frontier AI is developed are urgently needed, and embedded evaluations are a good first step. But their impact will depend heavily on implementation. If evaluators lack necessary access, if they are given too few resources, or if their findings carry little weight in actual decisions about frontier development, embedded evaluations may not amount to much.

This post sets out our current thinking on core principles for embedded evaluations that assess [loss of control](https://www.apolloresearch.ai/governance/loss-of-control) risks from [scheming](https://www.antischeming.ai/), i.e., AI models covertly subverting their developers in pursuit of unintended goals. We first describe at a high level what effective embedded evaluations should achieve. We then propose a concrete design based on verifying or falsifying developers' safety claims, which we hope developers and evaluators will adopt. We see these principles as a minimal starting point rather than a complete framework. Many of them build on established practice for independent auditing in other high-stakes industries, adapted to the specific challenges of frontier AI.

## Part 1: Criteria for effective embedded evaluations

We think an embedded evaluation must meet four criteria:

1. **Reduces risk.** It meaningfully reduces risk from frontier AI.
2. **Informs the public.** It informs the public about the development of frontier AI.
3. **Good incentives.** It gives both parties incentives that favor safety.
4. **Fair to both sides.** It is fair to the developer and the evaluator.
![](https://cdn.prod.website-files.com/6a2bd279c59d9c01b2a20237/6abd01067335224c397ba36b_01d_criteria_icons.svg)

### Reduces risk

The main reason to embed evaluators inside frontier developers is to make AI development safer. Embedded evaluations can do this both by increasing visibility into developers and easing race dynamics, and by more directly improving safety practices. For the more direct route, embedded evaluations should:

- **Catch problems early.** Warning signs of loss of control, such as models subverting their training or evading monitoring, could appear during training and internal deployment, long before release. We therefore believe evaluators should have ongoing access to information including but not limited to all training data, rollouts, checkpoints, and details of internal deployment.
- **Strengthen safety practices.** Evaluators should actively red-team the developer's alignment training, monitoring, and control measures.
- **Investigate incidents thoroughly.** Each serious incident should be examined for its cause, why safety measures failed, and whether similar incidents went unnoticed. The [METR and Redwood Research investigation](https://www.lesswrong.com/posts/nB8KKapnWGBXtKKiM/brief-independent-investigation-of-agents-behavior-reasoning) of the OpenAI–Hugging Face incident was a good first step, but we believe significantly more access is required in the future. For example, future investigations should have more time and access to all relevant data, and should allow follow-up experiments on the main model involved.
- **Preempt new risks.** New training methods bring novel failure modes. An evaluator who had seen the multi-agent training behind the OpenAI–Hugging Face incident early might have predicted that it rewarded agents for coordinating to subvert their oversight, and looked for this behavior in training before the incident. Evaluators should therefore learn about experimental training methods while they are still in development, early enough for their results to shape model development.
- **Be sufficiently resourced.** Doing all of the above across training, evaluations, and internal deployment is a large amount of work, and it needs substantial investment from both the evaluator and the model developer in terms of people and compute.

### Informs the public

Frontier developers are [getting rapidly closer to the point](https://www.anthropic.com/institute/recursive-self-improvement) where AI can automate AI research itself. As progress speeds up, the public and the government [may be left increasingly in the dark](https://casp.ac/reports/intelligence-explosion) as to what is happening inside AI companies. To help prevent this, embedded evaluations should:

- **Publish by default.** Given the power of AI technology, the public should get insight into its safety. Public reports should give clear overviews of what was investigated, what the conclusion was, and enough of the evidence for outside researchers to judge that conclusion.
- **Apply meta-transparency to redactions.** A developer may redact sensitive details, but the report should make clear what type of information was redacted, and whether it was important for the evaluator's final conclusion. A developer cannot redact the evaluator's overall conclusion.
- **State scope clearly.** A failure mode of embedded evaluation is one where evaluators see only a narrow slice of data, find nothing concerning while other safety concerns go unnoticed, and give the public a false sense of security. Reports should make clear what access the evaluator was given or denied.
- **Keep pace with development.** Reports should come out on a fixed schedule that matches the development cycle, and more often as AI research is automated and those cycles get shorter. If information central to the assessment is still outstanding or awaiting approval when a report is due, the report should say so rather than stall.
- **Disclose serious findings quickly.** Some findings, such as a model trying to copy its weights to external servers, are too serious to wait for the next scheduled report. We believe these should be directly disclosed within a short, pre-agreed window. Delays should be allowed only for real security risks or third-party concerns.
- **Make results comparable.** Developers should be assessed against a common set of specific claims about their safety, so they can be compared with each other and over time. Some claims will still be specific to one developer, such as claims about a company-specific incident or technique.

#### Good incentives

The evaluator will have far fewer resources than the developer and will depend on it for access and most of the evidence. The incentives introduced by the embedded evaluation policy should ideally lead the developer to share all relevant evidence and invest sufficiently in embedded evaluations, and should make high safety standards the easiest way to a favorable assessment. To move toward this, embedded evaluations should:

- **Agree on scope and access up front.** Unclear scope may invite disagreement later on, for example, a developer may want to limit scope if it learns of concerning findings. Scope and access should therefore be agreed and announced publicly before the investigation begins.
- **Expand scope for unforeseen findings.** The evaluator can still request more scope later, for example when a concerning finding turns out to warrant a full incident investigation. The public report should say what was requested, whether it was granted, and why. Any access that is withdrawn or not provided should also be made public. If the developer does not respond in a timely manner, the request should be treated as granted.
- **Reward self-reporting.** A developer should be incentivized to proactively report problems, rather than delaying until an evaluator finds the evidence at a later point.
- **Reward incremental safety progress.** The evaluator should assess gradual improvements in the developer's ability to detect and prevent problems, so that this progress is reflected in the report even when no problems have been found.
- **Maintain evaluator independence.** What the evaluator finds should not affect its funding, whether its contract is renewed, or how much access it is given in future evaluations.

We believe purely voluntary commitments are unlikely to be sufficient to ensure these incentives. We therefore believe embedded evaluations should eventually be required by law rather than left to voluntary commitments. Until such requirements exist, additional voluntary mechanisms can still strengthen these incentives. A developer could commit in its safety framework that certain claims must hold up under embedded evaluation before, for example, a model is deployed internally at scale. Its board or a safety committee could then have responsibility for enforcing that commitment. Insurers and large customers could also take the results into account in their own decisions, and public scrutiny adds to the cost of refusing access.

#### Fair to both sides

A developer needs to be able to protect confidential intellectual property, and an evaluator needs enough access to form a reliable picture of what is happening. To achieve this, embedded evaluations should:

- **Ensure persistent, deep access.** When an evaluator isn't given sufficient access to assess safety, it should say so publicly without needing the developer's agreement. Persistent, deep access includes insight into the developer's training methods and planned changes in architecture or paradigm, so the evaluator has the situational awareness to account for unknown unknowns. Not everyone at the evaluator needs this. For example, it may be unreasonable to tell everyone evaluating monitorability about planned architectural changes. But someone at the evaluator must know about them, so they can judge whether a change would break assumptions the monitorability evaluations rest on.
- **Protect confidential intellectual property.** Evaluators will work with several developers, so training data, transcripts, and details of training methods should stay on each developer's systems. Likewise, the evaluator's intellectual property should be protected, even when good parts of it may be on the developer's systems.
- **Avoid undue restrictions on the evaluator.** The developer should not restrict the evaluator beyond what is needed to protect its confidential intellectual property. For example, contracts should not lock evaluator staff into working with a single developer, since that prevents them from rotating between developers. Rotations between companies are typical and encouraged in other third-party testing industries, e.g., to prevent collusion risks between specific individuals.
- **Redact sparingly.** A developer should redact only security, legal, commercial, or third-party sensitive information, as Anthropic CEO Dario Amodei's [commitment](https://darioamodei.com/post/we-must-pace-the-frontier) allows Anthropic to do, and never redact findings because they are unfavorable to the developer.
- **Keep developer burden proportionate.** A developer with strong safeguards should need fewer resources and less effort for its assessment than one without.
- **Set rules for disagreements in advance.** Disagreements should not be decided by whichever party has more leverage at the time. We believe a developer should be able to respond publicly to an overall assessment it disagrees with, but not veto it.

### Part 2: Our proposal

The rest of this post describes a design that we think meets these criteria for ongoing evaluations of the safety measures a developer takes. Evaluators carry out *claim-based assessments*, meaning they assess specific claims that are fixed in advance rather than give an overall judgment of the developer. If something unforeseen comes up during the assessment, the evaluators can propose additional claims, and these are added by default unless the developer has a good reason to reject them. The evaluator reports a verdict for each claim, and the tiers of verdicts are ranked such that giving access and proactively reporting problems is the developer's best strategy, given that the developer is motivated to get high-ranking verdicts. The assessment is published by default, and the developer is able to add written rebuttals to the public version of the assessment when it disagrees with the evaluators.

![](https://cdn.prod.website-files.com/6a2bd279c59d9c01b2a20237/6abd00daf393a0226abd19cb_00a_overview_line.svg)

While we focus primarily on claim-based assessments in this post, embedded evaluators should also do other kinds of work, such as investigating serious incidents or critiquing safety cases. Much of our proposal carries over to critiquing safety cases, since recommended claims can be taken from the claims a safety case relies on, and a negative verdict on one of them is a public sign that the safety case does not hold up at that point. Incident investigations are also closely tied to claim-based assessments, since a serious counterexample found while assessing a claim will often turn into an incident investigation, though they have slightly different design considerations that we don't go into in this post.

#### Claims

An embedded evaluation should assess specific claims, such as "No subversion was attempted in monitored internal deployment activity," rather than give an overall verdict on the developer. A claim-based assessment defines in advance what counts as a positive or negative result, makes results comparable across developers and over time, and makes it possible to publish a meaningful result even when some evidence needs to be redacted to preserve sensitive details.

We propose having two sources of claims:

- **Standard claims.** A set of standard claims that every frontier developer has embedded evaluators assess. These would cover properties that any safe developer should be able to demonstrate. A shared set keeps developers from choosing only the claims they know they will pass, and lets the public compare developers directly. The standard claims follow state-of-the-art research, for example from academia, governments and third parties, and are published so that anyone can see what developers are assessed on.
- **Recommended claims.** A set of recommended claims, which can be specific to one developer. These come from the developer's own public commitments (for example, in its safety framework) and the claims its safety case relies on, from what the embedded evaluators observe, from emerging risks, or from problems the developer has had in the past. The public report lists every recommended claim and whether the developer adopted it as in scope for the next assessment period. A recommendation based on internal information could reveal confidential details, so it can be redacted under the same meta-transparency rules as other observations.

A good claim is specific enough to assess and important enough that falsifying it would point to clear risks or new unknowns about the safety of current or future models. Examples that meet both conditions, and could be part of a standard set, include:

- Agents never attacked or accessed external services without authorization.
- Models never attempted to undermine their own safety training.
- Models could not have undermined alignment training or safeguards even if they had tried.
- Agents never set up a rogue deployment, either within the developer's infrastructure or externally.
- Models never attempted to disable or evade their monitoring during internal deployment.
- The developer’s alignment training and control methods remain effective at the capability level of planned models.
- Employees never attempted to insert backdoors or hidden loyalties into models.

The full standard set would be significantly larger than this. This builds on regulation in other dangerous industries, like nuclear power. There, auditors compare the operation of a plant to a written list of standards and best practices and identify any places where the plant is falling short.

#### Assessments

We propose assessing each claim in three steps. The evaluator first reviews the evidence the developer already has, then gathers new evidence of its own, and finally assesses whether the evidence is adequate. The goal behind this procedure is to assess as quickly as possible to what extent the claim is true. The first two steps aim to do this by looking for a direct counterexample. But if no such counterexample is found, this is not sufficient to establish the claim as true. We also need confidence that the developer's methods of inquiry are actually able to find counterexamples. The third step checks whether those methods would have found a counterexample if one existed. We note that with the field's current scientific understanding of AI, we often cannot establish a safety claim with high confidence. We can merely say that we tried hard to rule it out and failed.

![](https://cdn.prod.website-files.com/6a2bd279c59d9c01b2a20237/6abd019a154c12fe5cffdf86_03a_three_steps_line.svg)

1. **Review Evidence.** The developer presents the evidence it already has, such as incident records, monitoring results, and evaluation results, and states whether it considers the claim falsified.
2. **Gather Evidence.** The evaluator looks for new evidence that falsifies the claim, using its own methods, such as model graders over training data, independent evaluations, transcript searches, interviews with employees of the developer, and targeted experiments. The evaluator does this even if the developer has already reported a counterexample, because there may be further and possibly more severe counterexamples that the developer did not find.
3. **Assess Evidence Adequacy.** If neither party has falsified the claim, the evaluator tests whether the developer's methods would have found a counterexample if one existed.

As a worked example, consider the claim "Models never attempted to disable or evade their monitoring during internal deployment." In Review Evidence, the developer shares its monitoring logs and flagged incidents and states that none of them involved such behavior. In Gather Evidence, the evaluator runs its own graders over transcripts to search for actions like spoofing tool calls or tampering with logs, and may ask engineers whether they have seen similar behavior or know of mechanisms a model could exploit or has exploited. If neither finds a counterexample, the evaluator checks in Assess Evidence Adequacy whether the monitors would have caught an attempt at all. It might insert realistic evasion attempts into transcripts to see how many the monitors flag, and check how much deployment activity is monitored. If the monitors catch most attempts and cover nearly all activity, the absence of flagged incidents is meaningful evidence. If not, the developer can use these findings to improve its monitors and rerun them over past transcripts to look for attempts the original monitors may have missed.

## Verdicts

Each claim ends up with one of five verdicts, graded from A (best for the developer) to E (worst). Which one it gets depends on whether a counterexample was found, who found it, whether the developer's methods would have found one if it existed, and whether the evaluator had sufficient access.

![](https://cdn.prod.website-files.com/6a2bd279c59d9c01b2a20237/6abd01de1dff24ad195356ad_03d_three_steps_outcomes.svg)

1. **Verified.** No counterexample was found, and the evaluator found that the developer's methods would likely have found one if it existed. This verdict is subject to the uncertainties of current AI safety methods, which, as mentioned, are often inadequate for high-certainty safety guarantees, and it should be interpreted in that light.
2. **Unrefuted.** No counterexample was found, but the evaluator found gaps in the developer's methods, so the absence of counterexamples is weaker evidence.
3. **Self-reported.** The developer's own evidence contradicts the claim, and the developer reported this.
4. **Evaluator-found.** The evaluator found evidence contradicting the claim that goes beyond what the developer reported, such as instances the developer missed or a substantially more severe or widespread version of a problem it reported.
5. **Blocked.** The developer did not give the evaluator enough access to meaningfully try to falsify the claim.

Each verdict is accompanied by a section of the assessment report describing what the evaluator investigated, what it found, and how it reached the verdict, in enough detail for others to judge the verdict for themselves. This section also states the evaluator's confidence in the verdict and a list of known or plausible gaps in the evidence, meaning ways the claim could still be false that the assessment did not rule out. For verdicts with a counterexample, it states how severe the counterexample seems to the evaluator and how much effort it took to find.

Once a counterexample is found, the original claim is refuted. This may lead to an extended incident investigation into its causes and possible remedies. In addition to this, we think the developer should be able to respond with a weaker fallback claim for further investigation. For example, if the claim "Agents never set up a rogue deployment" is refuted, the fallback claim could be "No rogue deployment has occurred since we fixed its cause, and current models no longer attempt one when placed in similar situations." The fallback claim goes through the full process and gets its own verdict, and the public report states both claims and verdicts.

We believe this design gives the developer good incentives to grant access and to report safety lapses proactively. To see why, consider a developer that simply wants its claims to get the best verdicts possible. First, it has to give the evaluator enough access, because otherwise the claim is *Blocked* (E), the worst verdict. Once access is given, holding back evidence may be a bad bet. If the evaluator later finds a counterexample the developer knew about, the claim ends up as *Evaluator-found* (D) rather than *Self-reported* (C). The developer also pays a reputational cost, because it looks either careless or evasive for not having reported the problem itself. Once access is given and evidence is shared, the main way the developer can keep its claims from being refuted is to actually improve its safety measures. When those measures are good enough that neither the developer nor the evaluator can find counterexamples, the focus shifts to raising assurance in the claims from *Unrefuted* (B) to *Verified* (A), which pushes the developer to upgrade its safeguards even further, for example with more realistic evaluations, improved alignment training, and more comprehensive monitoring. Taken together, these incentives are a reasonable starting point, though we don't expect them to hold up against a developer that is determined to game the system.

## Public report

The public report is how the public can judge whether AI development is being done responsibly. Each assessment produces two reports. A confidential report for the developer contains the full findings, including sensitive details and preliminary findings that are not yet clear enough to publish. The public report gives the verdict for each claim and the evidence behind it, with sensitive details redacted.

![](https://cdn.prod.website-files.com/6a2bd279c59d9c01b2a20237/6abd02084c4c72642ceb643a_09d_public_report_rules.svg)

We propose that the following always be included in the public report:

- **The claims themselves**, publicly announced before the assessment begins.
- **The verdict for each claim**, using the grades above, together with the evaluator's confidence, the known or plausible gaps in the evidence behind it, and for counterexamples, their severity.
- **The access the evaluator asked for and the access it received**, described by the evaluator, with specifics such as dates and durations.
- **A description of the evidence**, detailed enough for external researchers to judge the verdict, including how much effort each counterexample took to find.
- **Any outstanding requests for information** that are central to the verdict on a claim, and how long they have been outstanding.
- **Every claim the evaluator recommended,** and whether the developer adopted it, with redactions following the same meta-transparency rules as other observations.

Public reports come out on a fixed schedule agreed in advance, matching the developer's development cycle and becoming more frequent as that cycle shortens. If information central to a verdict is still outstanding when a report is due, the report is published anyway and lists the outstanding request. This ensures regular updates and keeps reports from stalling.

The developer and the evaluator will sometimes disagree on things such as the evidence required to falsify claims, the adequacy of methods, or appropriate levels of access. We propose that in each of these cases the evaluator publishes its verdict and the developer can include a short statement in the public report explaining why it disagrees.

Some findings are too serious to wait for the next scheduled report. We propose two levels of expedited disclosure, with the bar for each roughly agreed on in advance. The first level covers serious incidents such as the OpenAI–Hugging Face incident. For these, the evaluator investigates the incident, including but not limited to a timeline of events, its root cause and why safety measures failed to prevent it, and publishes a report within a pre-agreed window after discovery. The window can be extended in some cases to allow for remediation, such as patching vulnerabilities before they are made public. The second level covers findings as egregious as a model actually trying to synthesize a biological weapon, or a model covertly training a successor to pass on its own goals. For these, the evaluator reports directly to the relevant authorities and informs the developer at the same time, without needing the developer's agreement. Confidentiality duties for financial auditors, lawyers and doctors, as well as nondisclosure agreements, have similar exceptions when serious harm is at stake.

## Conclusion

Embedded evaluators have the potential to strengthen the safety measures at frontier developers and greatly increase the public's trust in the safety of AI systems. Whether they do comes down to implementation. If evaluators see only a small fraction of internal information, if developers allow too few evaluators to be embedded or allocate them too little compute to do the work, or if developers lack sufficient incentive to make the collaboration succeed, embedded evaluations could give a false sense of security and in the worst case contribute to safety washing.

We have argued that effective embedded evaluations should reduce risk, inform the public, be implemented with good incentives for both parties, and be fair to both. Our proposal aims to meet these goals in three ways. Evaluators assess specific claims that are fixed in advance. Verdicts are ranked so that giving access and proactively reporting problems are in the developer's interest. And verdicts are published by default, together with a description of the access the evaluator received.

We see this proposal as a starting point. We expect the methodology to evolve as Apollo Research and other evaluators gain experience, and we welcome feedback from developers, other evaluators, and policymakers. We hope the first embedded evaluation agreements set a high bar for those that follow.

Share this article