---
title: "Does Scaling Web-Video Pre-training Help Real Robots Do Real Work?"
source: "https://www.rhoda.ai/research/scaling-web-video-pretraining?utm_source=tldrai"
author:
published:
created: 2026-09-14
description: "We investigate scaling model size and pre-training compute for video-based robot policies, and benchmark on a real industrial manipulation task."
tags:
  - "clippings"
---
We investigate scaling model size and pre-training compute for video-based robot policies, and benchmark on a real industrial manipulation task.

Video pre-training has recently become a cornerstone of robot foundation models, and with it, a widely held belief: **scaling web-video pre-training leads to better downstream robot task performance.** This belief has not been rigorously tested. Few studies examine the effect of *scaling* model size and compute, instead often substituting a binary comparison against a model trained from scratch. Fewer still have stepped beyond proxy metrics and simple lab tasks to investigate scaling on complex, long-horizon tasks representative of real-world use cases.

We put this belief to the test with [Direct Video-Action models (DVA)](https://www.rhoda.ai/research/direct-video-action). Web video is abundant enough that supply is never the constraint, so pre-training on it leaves a team two decisions: how large a model to train, and how much compute to spend training it. We vary both, post-train each pre-trained model on robot demonstrations of the same industrial task, and evaluate the resulting policies on a real robot under a metric meaningful to our customer.

**What we found:**

- Larger pre-trained video models consistently yield better robot policies, and the trend continues to hold at the largest size we tested.
- Increasing pre-training compute improves robot policies at every amount of robot demonstration data we tested for post-training, with the largest gains when robot data is scarce.
- Better prediction of held-out web video at a pre-training checkpoint correlates with better robot policies across all the model sizes and compute budgets we tested (see [Figure 1](#figure-1)).

These findings required over 200 hours of real-robot evaluation time. Because a physical evaluation can fail in many ways that have nothing to do with the policy, we treat our evaluation protocol as a result of this work in its own right. It is summarized in [How we ran the evaluation](#how-we-ran-the-evaluation) and given in full in [Appendix A](#appendix-a-evaluation-protocol).

![Figure 1: Pre-training quality vs. task performance](https://www.rhoda.ai/images/scaling/pretrain-metric-vs-task-performance__task__fd_dinov2__100pct.svg)

Figure 1: Pre-training quality vs. task performance

**Figure 1.** *Seven pre-training checkpoints, each post-trained once on the full robot demonstration set. Labels are model sizes, from XS to L. The four M points are one model at 0.08×, 0.18×, 0.37× and 1× of its full pre-training compute. x-axis: [DINO FD](#measuring-pre-training-quality) (Fréchet distance), how well the model predicted held-out web video at a pre-training checkpoint, reversed so that quality increases to the right. y-axis: [at-speed completion rate](#how-we-score-a-trial), the percentage of trials that met every requirement within the time limit. Bars are 95% credible intervals.*

## The question

The world wants to believe that scaling video pre-training aids robot task performance. We seek to investigate this claim in depth. Formally, we ask:

Does scaling **pre-training on general web video** measurably improve **a complex manipulation task in real deployment**, holding everything else fixed?

- **The pre-training data.** We pre-train on general web video, not on video selected for manipulation, such as egocentric or robot videos.<sup><a href="#note-1" aria-label="Note 1">1</a></sup> Our pre-training data is video-only, and contains no actions.
- **The task.** We measure on a complex manipulation task from a real customer use case, scored against a stricter version of that customer's requirements.
- **The pre-training metric.** We score each pre-trained video model on how well it predicts held-out web video, using the DINO FD (Fréchet distance) defined in [Measuring pre-training quality](#measuring-pre-training-quality), and test whether it predicts task performance on the robot.

## What we tested

### Model setup

We perform all experiments using the [**Direct Video-Action model (DVA)**](https://www.rhoda.ai/research/direct-video-action). At its core, the DVA is a causal video model, pre-trained on general web video and post-trained on task-specific robot video. A separate inverse dynamics model turns its predicted frames into robot actions.

In this post, we study how scaling the two quantities that set a web-video pre-training run's cost, the video model's parameter count and its pre-training compute, affects on-robot task performance. The inverse dynamics model is trained once on a broader multi-robot dataset, and is held fixed alongside the task, post-training procedure and evaluation protocol across all experiments. Every model also runs at the same inference frequency.

![Figure 2: DVA training and evaluation](https://www.rhoda.ai/images/scaling/dva-training-and-evaluation.svg)

Figure 2: DVA training and evaluation

**Figure 2.** *Our training and evaluation pipeline. Stage 1 pre-trains a video model on general web video, and Stage 2 post-trains it on robot demonstrations of the bearing-unpacking task. At evaluation, the post-trained model predicts future frames from what the robot sees, a separate inverse dynamics model turns them into actions, and the loop repeats. The same inverse dynamics model is used in every evaluation in this post. Only the pre-trained video model varies, in size and in pre-training compute. Result 2 also varies the amount of post-training data.*

### Measuring pre-training quality

Scaling studies in language modeling have demonstrated that pre-training loss improves predictably with scale ([Kaplan et al.](https://arxiv.org/abs/2001.08361)), and downstream task performance has been shown to follow it ([Gadre et al.](https://arxiv.org/abs/2403.08540)). A video model needs the same kind of metric, one that measures a pre-trained video model at a pre-training checkpoint, before post-training and before it has seen the task. For this, we use DINO FD (Fréchet distance). To compute this metric, we take clips of web video held out from model training, let the model predict how each clip continues from the frames before it, embed the predicted frames and the true frames with a fixed DINOv2 encoder, and measure the distance between the two feature distributions. Lower metric values are better. The held-out clips contain none of the task the models were later post-trained on, and the score is cheap enough to log throughout pre-training. Details are included in [Appendix F](#appendix-f-how-dino-fd-is-computed). Every policy in this post has a DINO FD score for the pre-training checkpoint it was post-trained from (shown in [Figure 1](#figure-1)).

### A real industrial task

We want to study pre-training scaling on **complex manipulation tasks corresponding to real-world customer use cases**. A representative example is *industrial unpacking*: removing products, raw materials, or parts from cartons, crates, and bags. One such task we have adopted from a customer is unpacking bearings and sorting the packaging waste. All robot evaluations in this post are conducted on this task. The video below shows the task.

<iframe src="https://player.vimeo.com/video/1225466741?h=a3db90a443&amp;title=0&amp;byline=0&amp;portrait=0&amp;vimeo_logo=0&amp;dnt=1" frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media" allowfullscreen=""></iframe>

**Description.** These bearings arrive in disposable packaging and must be manually unpacked before use. Every day, more than 1000 boxes are unpacked by hand at one of our customer sites. The packaging is made of several materials, each of which must be recycled separately.

**Challenges.**

- Each box weighs 10 kg.
- The strap can tear during lifting.
- Pulling out the tab requires precise control.
- The plastic bag is transparent and hard to grasp.
- Packaging paper can get stuck inside the bag.

**Task procedure.** Fourteen steps, grouped into the six sub-tasks we score. Packaging is sorted into three bins: cardboard, plastic, and paper.

1. **Lifting the box from the tote to the table**
	- Grasp the strap.
		- Lift the box out of the box tote and place it on the table.
2. **Turning the box to find the tab†**
	- Rotate the box until the tab faces the robot.
3. **Opening the lid and side flaps**
	- Pull out the tab.
		- Open the lid.
		- Unfold the side flaps so they stay up.
4. **Putting the top packaging paper in the paper bin**
	- Open the plastic bag.
		- Take out the top packaging paper and put it in the paper bin.
5. **Dumping the bearings and sorting the packaging**
	- Dump the bearings into the bearing tote.
		- Put the empty box in the cardboard bin.
		- Pull the plastic bag out of the bearing pile and put it in the plastic bin.
		- Fish the second packaging paper out of the bearings and put it in the paper bin.
6. **Wrapping up†**
	- Dig through the bearings for leftover packaging.
		- If the box tote is empty, press the button to bring the next one.

† Only for some boxes: the box is turned only when the tab faces away, and the button is pressed only after the last box of a tote. These two sub-tasks are not shown in the per-sub-task figures.

Besides being a real-world use case, the industrial unpacking task has a few additional properties that make it a good candidate for our evaluation.

**It is long-horizon.** The full task requires dozens of individual manipulation motions and takes over a minute even when an expert operates the robot. Due to its length, errors early in the episode can propagate into later sub-tasks. For example, rotating a box incorrectly at the beginning of the task makes the subsequent manipulations more difficult.

**The required movements are complex and demand both precision and dexterity.** Grasping thin flat straps, rotating boxes, opening boxes and bags, and fishing paper out of bearing packaging all go beyond simple pick-and-place.

**The post-training data is high-quality.** Nearly every trajectory was collected by an experienced robot operator with a researcher observing, and edge cases and failure-recovery behavior are covered deliberately. If the demonstrations encode a bad strategy, a model that fits them better may perform *worse*, which would defeat the purpose of this study.

### How we score a trial

In a real deployment there are at least two metrics that we need to track:

1. **Completion.** Were *all of* the goals achieved (e.g., the items unpacked *and* the waste sorted correctly) without a human stepping in?
2. **Cycle time.** How long did the robot take to process one package?

We therefore report the **at-speed completion rate**: the fraction of trials the robot completed, and completed within the time limit. Throughout this post, we use *task performance* to refer to this number. A trial counts as a *completion* only if every goal of the task is achieved with no human intervention. For bearing unpacking, that means bearings are dumped into the correct tote, no bearings are lost, and all packaging waste is sorted into the correct bins. A trial counts as *at speed* only if the cycle time is under 100 seconds, a threshold we set so that the score separates the models instead of saturating. A trial that fails to meet either the completion criterion or the speed criterion counts as a failure.

We find that at-speed completion is a more discriminative metric than average cycle time or a plain task completion rate. Average cycle time tends to be dominated by a handful of catastrophic trials, and a plain completion rate hides differences when the post-training data contains good failure recovery, because the policy retries until it succeeds.

For finer-grained analysis, we split the task at its natural pauses into the six sub-tasks listed in [the task box above](#task-box), and score each sub-task the same way, with its own time limit. The two sub-tasks marked † apply only to some boxes, so the per-sub-task figures report the other four.

### Choosing which checkpoint to evaluate

Different checkpoints from the same post-training run can differ substantially in task performance. In one run of the M-size model, two checkpoints differed in at-speed completion rate by 28 points ([Figure 12](#figure-12)), and others have reported the same kind of variation ([Mandlekar et al.](https://arxiv.org/abs/2108.03298), [Chi et al.](https://arxiv.org/abs/2303.04137)). Which checkpoint we evaluate is therefore a deliberate choice. In general, validation loss is a poor checkpoint selector. Others have found that it tracks real-robot success weakly or not at all ([Mandlekar et al.](https://arxiv.org/abs/2108.03298), [Lin et al.](https://arxiv.org/abs/2410.18647), [Allshire et al.](https://arxiv.org/abs/2606.27375)), and our experiments concur ([Figure 12](#figure-12)). Instead we track a proxy metric during post-training, and this metric needs no robot trials. The checkpoint where the proxy metric is lowest is the one we evaluate on the robot. Where the proxy is flat or noisy across several checkpoints, we evaluate those on the robot and report the best. [Appendix D](#appendix-d-checkpoint-selection) shows that run in [Figure 12](#figure-12), with the five evaluated checkpoints against both metrics.

### How we ran the evaluation

Every number in the results below was produced under the following conditions.

- Over 200 hours of real-robot evaluation in total, with one hundred to a few hundred trials per policy.
- Every evaluation session follows the same standard operating procedure (SOP), from hardware calibration and object preparation to grading and intervention rules, and starts with a pre-flight checklist.
- Evaluators are certified before their first real trial, after practice trials under a researcher's observation.
- Every trial is recorded and can be re-examined afterwards.
- Trials flagged by the evaluator and statistical outliers are audited from the recordings. Exclusions are decided by how a trial was set up, never by how it ended.

[Appendix A](#appendix-a-evaluation-protocol) gives the full protocol and the rules by which trials are counted.

### How to read the charts

Many published robot manipulation results rest on tens of trials per experimental setting. We ran one hundred to a few hundred per policy, and we show each result the way the Toyota Research Institute's [Large Behavior Models paper](https://arxiv.org/abs/2507.05331) does: as a violin over the true at-speed completion rate, with a bar at the observed rate and letters marking which policies the data can tell apart. [Figure 3](#figure-3) walks through the elements on three real policies from this study. [Appendix B](#appendix-b-statistical-treatment) has the statistics.

![Figure 3: How to read the violin charts](https://www.rhoda.ai/images/scaling/violin-example__task.svg)

Figure 3: How to read the violin charts

**Figure 3.** *How to read the violin charts in this post, on three real policies from the study. Each violin is the Beta(k+1, n−k+1) posterior over a policy's true at-speed completion rate after k at-speed completions in n trials, drawn over its central 99.75% credible range. The bar is the observed rate k/n, and the label gives that rate and n. Letters are significance groups from pairwise two-sided Fisher exact tests, Holm-corrected within the chart: policies with no letter in common differ at 95% confidence. Policies that share a letter are not separated at that level, which is not the same as performing equally.*

## Result 1: bigger models are better

We first examine model size. We pre-trained four models of increasing size (XS, S, M, and L) with one recipe, each trained to convergence on a sufficiently large dataset, the setup under which [Kaplan et al.](https://arxiv.org/abs/2001.08361) measured their model-size law. Based on our internal scaling-law analysis, every one of the four models is trained past its compute-optimal point ([Kaplan et al.](https://arxiv.org/abs/2001.08361), [Hoffmann et al.](https://arxiv.org/abs/2203.15556)). Overtraining the smaller models this way also matches modern practice, where small models are trained well past compute-optimal to cut inference cost ([Sardana et al.](https://arxiv.org/abs/2401.00448), [Gadre et al.](https://arxiv.org/abs/2403.08540)). We describe the full pre-training setup in [Appendix C](#appendix-c-pre-training-setup-for-the-two-sweeps). Each model was then post-trained on the same bearing-unpacking dataset, with checkpoints chosen as described in [Choosing which checkpoint to evaluate](#choosing-which-checkpoint-to-evaluate).

![Figure 4: Task performance](https://www.rhoda.ai/images/scaling/model-size__task.svg)

Figure 4: Task performance

**Figure 4.** *Four video models (XS, S, M, L), pre-trained with one recipe and each post-trained once on the full demonstration set. Violins are posteriors over the true rate. Policies with no letter in common differ at 95% confidence (explained in Figure 3).*

![Figure 5, panel 1: Lifting the box from the tote to the table](https://www.rhoda.ai/images/scaling/model-size__subtask__box_on_table.svg)

Figure 5, panel 1: Lifting the box from the tote to the table

![Figure 5, panel 2: Opening the lid and side flaps](https://www.rhoda.ai/images/scaling/model-size__subtask__side_flaps_open.svg)

Figure 5, panel 2: Opening the lid and side flaps

![Figure 5, panel 3: Putting the top packaging paper in the paper bin](https://www.rhoda.ai/images/scaling/model-size__subtask__s1st_paper_in_trash_bin.svg)

Figure 5, panel 3: Putting the top packaging paper in the paper bin

![Figure 5, panel 4: Dumping the bearings and sorting the packaging](https://www.rhoda.ai/images/scaling/model-size__subtask__box_bag_2nd_paper.svg)

Figure 5, panel 4: Dumping the bearings and sorting the packaging

Scroll sideways for the remaining panels.

**Figure 5.** *The four policies of Figure 4 scored on the four sub-tasks that every box requires, each within that sub-task's own time limit. Each sub-task is scored on its own valid trials, so n varies by panel and can be lower or higher than the task-level n. [Appendix A](#appendix-a-evaluation-protocol) explains how sub-task trials are counted.*

At-speed completion rate rises with model size: 4% → 65% → 75% → 85% for XS → S → M → L. Four of six pairwise comparisons separate after Holm correction, and every sub-task shows the same performance pattern: XS far behind, S in the middle, M and L on top. The rate is still climbing at L, so the largest model we trained has not saturated the metric, and we predict that an even larger model would score higher. A higher at-speed completion rate can come from fewer mistakes or from more speed. To see which, [Figure 6](#figure-6) breaks each model's trials down by the requirement they missed.

![Figure 6: Failure breakdown by model size](https://www.rhoda.ai/images/scaling/failure-breakdown__B_model_size.svg)

Figure 6: Failure breakdown by model size

**Figure 6.** *Each policy's trials broken down by outcome, the requirement they missed or completed at speed, for S, M, and L on the full demonstration set (XS omitted, since at 4% nearly every trial is a failure). Bearing lost: a bearing ended up outside the tote. Waste mis-sorted: packaging in the wrong bin. Human intervention: the policy got stuck and an operator had to step in. Completed but over 100 s: every requirement met except the time limit. The gray number in parentheses under each share is the number of trials behind it. Requirements are not mutually exclusive, so a model's bars need not sum to 100%, and an intervened trial ends early, so it can under-count the other failures. Counts are small so no significance tests were run.*

**Where the gain comes from.** Model size mainly affects time to completion, not correctness ([Figure 6](#figure-6)). In the recordings, larger models' actions succeed on the first attempt more often, so they retry less, which is the main reason their cycles are shorter. Their motions are also faster. Waste mis-sorting is the one failure that rises with size, within noise. There, faster motion commits the policy to a wrong sorting action, such as pulling the paper out with the bag, before it has observed enough to revise it, while slower motion leaves time to change course.

**Takeaway 1.** Making the pre-trained video model larger improves on-robot task performance, monotonically, on a real customer task.

## Result 2: more pre-training compute is better

Our second experiment scales pre-training compute instead. Result 1 varied the model. Here we keep the model the same and change only how long it trained. We use the M-size model, one size below the largest we trained, and post-train four checkpoints at 0.08×, 0.18×, 0.37× and 1× total compute of its one pre-training run. The pre-training dataset was large enough that validation loss never rose at any of the four. By the same internal scaling-law analysis as in Result 1, M is the compute-optimal size at the three smaller budgets and is trained past its compute-optimal point at the full one, like every model in Result 1. The full setup is in [Appendix C](#appendix-c-pre-training-setup-for-the-two-sweeps).

![Figure 7: Pre-training compute](https://www.rhoda.ai/images/scaling/pretrain-compute__task.svg)

Figure 7: Pre-training compute

**Figure 7.** *The M-size model, one size below the largest we trained, at four pre-training compute budgets, 0.08×, 0.18×, 0.37× and 1× of the full run, each post-trained once on the full demonstration set. Model size is held fixed, and only pre-training compute varies. Violins are posteriors over the true rate. Policies with no letter in common differ at 95% confidence (explained in Figure 3).*

![Figure 8, panel 1: Lifting the box from the tote to the table](https://www.rhoda.ai/images/scaling/pretrain-compute__subtask__box_on_table.svg)

Figure 8, panel 1: Lifting the box from the tote to the table

![Figure 8, panel 2: Opening the lid and side flaps](https://www.rhoda.ai/images/scaling/pretrain-compute__subtask__side_flaps_open.svg)

Figure 8, panel 2: Opening the lid and side flaps

![Figure 8, panel 3: Putting the top packaging paper in the paper bin](https://www.rhoda.ai/images/scaling/pretrain-compute__subtask__s1st_paper_in_trash_bin.svg)

Figure 8, panel 3: Putting the top packaging paper in the paper bin

![Figure 8, panel 4: Dumping the bearings and sorting the packaging](https://www.rhoda.ai/images/scaling/pretrain-compute__subtask__box_bag_2nd_paper.svg)

Figure 8, panel 4: Dumping the bearings and sorting the packaging

Scroll sideways for the remaining panels.

**Figure 8.** *The four compute budgets of Figure 7 scored on the four sub-tasks that every box requires, each within that sub-task's own time limit. Each sub-task is scored on its own valid trials, so n varies by panel and can be lower or higher than the task-level n. [Appendix A](#appendix-a-evaluation-protocol) explains how sub-task trials are counted.*

At-speed completion rate rises with pre-training compute (58% → 67% → 74% → 75% from 0.08× to 1×), and the rise is front-loaded: nine points from 0.08× to 0.18×, seven more to 0.37×, and one more from 0.37× to 1×, the largest step in compute of the three. The smallest budget is clearly behind the two largest, but from 0.37× to 1× the curve is flat.

As a side observation, during post-training the four runs' validation-loss and proxy metric curves have the same shape and sit in compute order from start to finish ([Appendix E](#appendix-e-post-training-curves-across-pre-training-budgets), [Figure 13](#figure-13)). At every step of post-training, the run from the larger pre-training budget has the lower validation loss and the lower proxy metric value, and the differences present at the first step are still there at the end.

Read on its own, the flat step from 0.37× to 1× says pre-training compute has saturated and further scaling is wasted. However, we hypothesize that our post-training dataset already covers most of the strategies the bearing-unpacking task needs, so a better prior learned through more pre-training has less left to contribute. Thus, the plateau may be a property of our post-training dataset, not of pre-training.

We tested this by post-training three of the four pre-trained checkpoints, the 0.18×, 0.37× and 1× budgets, on 100%, 50%, 25%, and 12.5% of the bearing-unpacking dataset. We left out the 0.08× budget since it was clearly already behind at full data.

![Figure 9: Pre-training compute × post-training data](https://www.rhoda.ai/images/scaling/pretrain-postdata__task.svg)

Figure 9: Pre-training compute × post-training data

**Figure 9.** *Three of the M-size compute budgets of Figure 7 (0.18×, 0.37×, 1×), each post-trained once on 12.5%, 25%, 50% and 100% of the demonstration set. Lines connect one budget across fractions. Violins are posteriors over the true rate. Policies with no letter in common differ at 95% confidence (explained in Figure 3). Letters compare the three budgets within one data fraction only.*

![Figure 10, panel 1: Lifting the box from the tote to the table](https://www.rhoda.ai/images/scaling/pretrain-postdata__subtask__box_on_table.svg)

Figure 10, panel 1: Lifting the box from the tote to the table

![Figure 10, panel 2: Opening the lid and side flaps](https://www.rhoda.ai/images/scaling/pretrain-postdata__subtask__side_flaps_open.svg)

Figure 10, panel 2: Opening the lid and side flaps

![Figure 10, panel 3: Putting the top packaging paper in the paper bin](https://www.rhoda.ai/images/scaling/pretrain-postdata__subtask__s1st_paper_in_trash_bin.svg)

Figure 10, panel 3: Putting the top packaging paper in the paper bin

![Figure 10, panel 4: Dumping the bearings and sorting the packaging](https://www.rhoda.ai/images/scaling/pretrain-postdata__subtask__box_bag_2nd_paper.svg)

Figure 10, panel 4: Dumping the bearings and sorting the packaging

Scroll sideways for the remaining panels.

**Figure 10.** *The compute-by-data sweep of Figure 9 scored on the four sub-tasks that every box requires, each within that sub-task's own time limit. Each sub-task is scored on its own valid trials, so n varies by panel and can be lower or higher than the task-level n. [Appendix A](#appendix-a-evaluation-protocol) explains how sub-task trials are counted. Letters compare the three budgets within one data fraction only.*

[Figure 9](#figure-9) shows the result. At full data the three budgets tie, as in [Figure 7](#figure-7). With less post-training data they separate: the 0.18× budget falls behind the 1× budget at 50% and behind both larger budgets at 25% and 12.5%, while 1× and 0.37× remain tied at every data fraction. The gap between the largest and smallest budget widens from 8 points at full data to 31 at 25%. Pre-training compute matters more when post-training data is limited. [Appendix B](#appendix-b-statistical-treatment) tests the widening as a single interaction across all twelve policies (p = 0.07).

At 12.5%, where every policy is poor,<sup><a href="#note-2" aria-label="Note 2">2</a></sup> the gap narrows to 14 points but does not close. Even at the smallest fraction we tried, more pre-training compute still helps. It just no longer helps *more*.

This is the result with the clearest practical consequence, because of how a robotics team pays for the two inputs. Pre-training compute is bought once and amortized across every task the team will ever deploy. Demonstrations are bought per task, per site, per product, by trained operators working in real time.

**Takeaway 2.** More pre-training compute helped at every post-training data fraction we tested, and the benefit was largest when task data was scarce.

## Result 3: pre-training quality predicts task performance

Results 1 and 2 each varied pre-training in some way and measured the on-robot task performance. The third hypothesis we set out to test is whether pre-training quality, measured as DINO FD on held-out web video before the task-specific data is involved, predicts on-robot task performance after post-training. As [Figure 1](#figure-1) shows, model size and pre-training compute each improved task performance, and each also improved pre-training quality. We test the hypothesis by plotting each post-trained policy's task performance against its pre-training quality. If it holds, the points should follow one trend regardless of whether the quality came from a larger model or from more pre-training compute.

![Figure 11: Pre-training quality vs. task performance](https://www.rhoda.ai/images/scaling/pretrain-metric-vs-task-performance__task__fd_dinov2.svg)

Figure 11: Pre-training quality vs. task performance

**Figure 11.** *Figure 1 with the lower post-training fractions added. Circles are the full-data policies of Figure 1. Squares, triangles, and diamonds are the three M-size compute budgets of Figure 9 post-trained on 50%, 25% and 12.5% of the demonstrations. One post-training run per point. Bars are 95% credible intervals.*

[Figure 11](#figure-11) shows a correlation between pre-training quality and task performance, independent of whether that performance was achieved through scaling compute or model size. At full post-training data, the seven checkpoints (XS, S, the four M compute budgets, and L) fall in strict DINO FD order on task performance: lower DINO FD, higher at-speed completion rate, from 4% at the left edge to 85% at the right, with the model-size points and the compute points interleaved. L has the best pre-training quality and the highest at-speed completion rate, ten points above the next policy, and the four M compute budgets fall in DINO FD order. *Two models with similar pre-training quality but different sizes also performed similarly on the robot.* S, a smaller model at its full pre-training budget, and the 0.08× M checkpoint, a larger model early in its pre-training, are the closest pair on the DINO FD axis, and their policies are not separated in task performance on the robot (65% and 58%, not distinguishable at 95% confidence). Whether size or compute produced the pre-training quality makes little difference to where a policy lands.

The lower post-training fractions shift every point down and widen the spread, up to a point. Over the DINO FD range of the three M budgets, at-speed completion rate spans 8 points at 100% data, 18 at 50%, and 31 at 25%. At 12.5% every policy is poor and the spread falls back to 14 points, though the order holds. The benefit of better pre-training is therefore largest at 25% of our demonstrations, smaller at 50% and at 12.5%, where every policy is poor, and smallest at 100%, where post-training data can do most of the work. This is Result 2 seen on the pre-training-quality axis. We ran the data sweep only for compute. Because task performance follows pre-training quality whichever way it was improved, we expect the same widening for model size.

Despite the clear correlation shown, there are two caveats. First, the relationship is a correlation across seven pre-training checkpoints of one architecture family, each with a single post-training run, so its exact shape is not established. This is why we say pre-training quality predicts task performance rather than determines it. Second, DINO FD measures video prediction, not manipulation. The observation that it predicts task performance at all is the interesting result, not a foregone conclusion.

**Takeaway 3.** Pre-training quality, measured on held-out web video at a pre-training checkpoint before post-training or task-specific data is involved, predicts task performance independently of whether model size or compute resulted in the improvement.

## What this means if you pre-train video models for robots

Based on these conclusions, we suggest two improvements in practice for training video models for robotics. Both are stated for the setup we tested, a video model pre-trained on general web video, post-trained on high-quality demonstrations of one task, with actions decoded by a separate inverse dynamics model. We have not tested beyond this setting, and the practices below do not extrapolate past it (see [Limitations](#limitations)).

### Robot performance correlates with pre-training quality

Pre-training quality, measured on held-out web video before post-training, ranked our seven checkpoints in the same order as the robot did, whatever their size or training length (Result 3). The ranking is a correlation within one architecture family on one task, and it gives an order, not a level. What a given pre-training quality is worth on the task is still measured on the robot. Even so, a team comparing its own checkpoints can rank them before any robot trial and spend the trials on the candidates that matter.

### Compare pre-trained models on the robot with limited task data

Differences between pre-trained models are largest when the post-training data is limited but sufficient. At 100% of our demonstrations the three compute budgets were within 8 points and not separated. At 25% they were 31 points apart. At 12.5%, where every policy was poor, the spread shrank to 14. We therefore suggest the following practice: first compare models after post-training on the full demonstration set. If the candidate models cannot be differentiated by metrics there, subsample the demonstrations for post-training and compare again, stopping before every candidate becomes poor and the differences compress again.

## Limitations

The first three limitations below have the same cause. **Real-robot trials are the scarce resource in this study.** Every policy we report cost between 100 and 260 trials on a real robot shared with many other development projects, except XS, which we stopped after 27 trials once it was clearly worse than the rest. In total, these evaluations took over 200 robot hours. At these counts only large differences are detectable: two policies at 75% and 60% on 100 trials each give p ≈ 0.03 before the multiple-comparison correction, and two at 75% and 65% give p ≈ 0.16 ([Appendix B](#appendix-b-statistical-treatment)). Each entry below is marked as a cost, a deliberate choice, or a property of the study's size.

**One task, one embodiment, one setup.** *Cost.* A second task would roughly double the trial count, and it would need post-training data of the same quality to be a fair comparison. Splitting the same trials over two tasks would have halved the trials per condition. At half our counts, even a 20-point difference would not separate. What "one task" means here: the full episode decomposes into six sub-tasks, several containing multiple distinct manipulation motions, so the range of behavior inside it is comparable to that of a suite of several short tasks.

**One training run per condition.** *Cost.* Every violin is one post-trained policy, so the intervals reflect variation between trials, not variation between training runs, which we did not measure. Repeating a condition costs another post-training run and another few hundred robot trials. We spent those on more conditions instead.

**Checkpoint selection is correlational.** *Cost.* Establishing that the minimum of our proxy metric reliably picks the best checkpoint would require evaluating many checkpoints per run on the robot, which is the expense the metric exists to avoid.

**The model-size sweep is not compute-matched.** *Deliberate.* The four sizes share one recipe, so the larger models also saw more video and used more compute, and the gain that [Takeaway 1](#takeaway-1) attributes to model size is the joint effect of model size, tokens, and compute. The sweep cannot separate them. This is the setup under which [Kaplan et al.](https://arxiv.org/abs/2001.08361) measured their model-size law. It trains all the models past their compute-optimal point, which is also what modern practice does, to cut inference cost. Result 2 shows that compute matters at a fixed size. A sweep of size at a fixed compute budget would show how much of Result 1's gain comes from size alone.

**The time limit is stricter than the customer's.** *Deliberate.* We set the 100-second cycle-time limit stricter than the customer's requirement so that the score separates the models instead of saturating. A different threshold would change the absolute numbers and could change the differences between policies. [Figure 6](#figure-6) shows, for the model-size sweep, how many completed trials the limit alone excluded.

**The relationship between pre-training quality and task performance is only a correlation.** *A property of the study's size.* Result 3 rests on seven pre-training checkpoints of one architecture family, each a single post-training run, on one task. We did not pick DINO FD after seeing which metric agreed best with the robot. It was the metric we already logged during pre-training, before any robot evaluation. The relationship held for every checkpoint we built. Whether it holds for a different pre-training dataset or a different architecture is untested.

## Conclusion

Does scaling web-video pre-training help real robots do real work? On the evidence here, one industrial task scored against a stricter version of the customer's requirements, yes. **Across model sizes and training durations, improvements to pre-training quality translated to robot performance.**

Scaling pre-training on general web video, little of it about robots, improved robot policies at a real customer's task, and a model's ability to predict that video tracked how its policy performed on the robot. That is the core hypothesis behind [DVA](https://www.rhoda.ai/research/direct-video-action), and this report is our first rigorous public measurement of it on real robots doing real work.

## References

1. Rhoda AI Team. [Causal Video Models Are Data-Efficient Robot Policy Learners](https://www.rhoda.ai/research/direct-video-action). 2026.
2. Generalist AI. [GEN-0](https://generalistai.com/blog/gen-0). 2025.
3. Dyna Robotics. [Dyna-2](https://www.dyna.co/dyna-2). 2026.
4. NVIDIA GEAR. [EgoScale: Scaling Human Video to Unlock Dexterous Robot Intelligence](https://research.nvidia.com/labs/gear/egoscale/). 2026.
5. Kaplan, J. et al. [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361). arXiv 2020.
6. Gadre, S. Y. et al. [Language models scale reliably with over-training and on downstream tasks](https://arxiv.org/abs/2403.08540). ICLR 2025.
7. TRI LBM Team. [A Careful Examination of Large Behavior Models for Multitask Dexterous Manipulation](https://arxiv.org/abs/2507.05331). *Science Robotics*, 11(113), 2026.
8. Mandlekar, A. et al. [What Matters in Learning from Offline Human Demonstrations for Robot Manipulation](https://arxiv.org/abs/2108.03298). CoRL 2021.
9. Chi, C. et al. [Diffusion Policy: Visuomotor Policy Learning via Action Diffusion](https://arxiv.org/abs/2303.04137). RSS 2023.
10. Lin, F. et al. [Data Scaling Laws in Imitation Learning for Robotic Manipulation](https://arxiv.org/abs/2410.18647). ICLR 2025.
11. Allshire, A. et al. [Scalable Behavior Cloning with Open Data, Training, and Evaluation](https://arxiv.org/abs/2606.27375). arXiv 2026.
12. Hoffmann, J. et al. [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556). arXiv 2022.
13. Sardana, N. et al. [Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws](https://arxiv.org/abs/2401.00448). ICML 2024.
14. Fisher, R. A. [On the Interpretation of χ² from Contingency Tables, and the Calculation of P](https://doi.org/10.2307/2340521). *Journal of the Royal Statistical Society*, 85(1), 87–94, 1922.
15. Holm, S. [A Simple Sequentially Rejective Multiple Test Procedure](https://www.jstor.org/stable/4615733). *Scandinavian Journal of Statistics*, 6(2), 65–70, 1979.
16. McCandlish, S. et al. [An Empirical Model of Large-Batch Training](https://arxiv.org/abs/1812.06162). arXiv 2018.

## Acknowledgments

This post rests on work from across Rhoda. The infrastructure and software teams built the systems that trained the models, ran the policies on the robot, and logged every trial. The application engineering, operations, and business teams brought the customer's task into our cell, kept a shared robot available for over 200 hours of evaluation, and collected the demonstrations. We thank the operators and evaluators who set up, ran, and graded every trial, especially Michael Phan, Shwe Moe, Anthony Legrama, and Kyle Lam, and we thank Ali Ahmad, Alex Bergman, Eric Chan, Changan Chen, Leo Dong, David Lindell, Adam Patni, Jagdeep Singh, Joanne Truong, and Gordon Wetzstein for their comments on drafts of this post.

## Appendix A: evaluation protocol

[How we ran the evaluation](#how-we-ran-the-evaluation) lists the conditions every result in this post was produced under. This appendix gives the protocol behind each condition and explains which recorded trials count toward which figure.

**Standard operating procedure and pre-flight checklist.** The SOP covers hardware calibration, robot software setup, model inference setup, environment setup, object preparation, grading guidelines, intervention guidelines and incident resolution. Each evaluation session starts with the pre-flight checklist.

**Certified evaluators and supporters.** Evaluators grade trials and intervene when necessary. Supporters set up the robot and reset the environment and objects. Both roles go through the same onboarding and complete a set number of practice trials, with a researcher observing and giving feedback, before they run a real evaluation.

**The grading interface.** It has to capture enough information for later analysis without overloading the evaluator. We have revised it many times to balance the two, and it includes a low-friction way to flag unexpected events mid-trial.

**Post-evaluation audit.** Every trial's record links to its recording. Two categories are re-examined from the recordings: trials the evaluator flagged, which usually means something unexpected happened, such as a visitor interacting with the robot, and statistical outliers, such as a trial taking three times the average duration. The audits have caught several systematic errors, including environments set up incorrectly for a whole evaluation session.

**Trial exclusions.** When the audit finds that a trial was not a valid test, most often because the environment was not prepared to the SOP at the start (so the policy was never given the task as defined), we exclude it from the whole-task figures. A sub-task panel keeps the trial if that sub-task's own setup was correct.

**Why n differs between the whole-task chart and the sub-task panels.** The whole-task chart drops a trial if any sub-task was set up incorrectly or if the trial's overall outcome or time was not recorded. A sub-task panel keeps every trial in which that sub-task ran with a correct setup and a recorded outcome and time.

A sub-task's n is higher than the whole-task n when the trial was dropped from the whole-task chart for a reason that does not affect this sub-task, for example:

- another sub-task was set up incorrectly
- the trial's overall outcome was not recorded

It is lower when this sub-task is dropped but the whole trial is kept, for example:

- the trial ended before reaching the sub-task, e.g.,
	- the policy made an unrecoverable mistake, such as pushing the whole box into the trash bin
		- the robot failed, such as a 3D-printed gripper mount breaking
		- a person made a mistake, such as hitting the emergency stop by accident
		- something interrupted the trial, such as a visitor walking in
- the policy skipped the sub-task altogether
- the sub-task ran but its outcome was not recorded

## Appendix B: statistical treatment

**Posterior violins.** For a policy with k at-speed completions out of n trials, we draw the Beta(k+1, n−k+1) posterior over the true at-speed completion rate, which is the posterior under a uniform prior, over its central 99.75% credible range. The bars on the scatter charts (Figures 1 and 11) are the central 95% interval of the same posterior. The horizontal bar is the observed rate k/n. With 70 at-speed completions in 100 trials, the central 95% of the posterior runs from 60% to 78%. The violins capture uncertainty from the robot trials only. Each condition is a single post-training run with one checkpoint selected as described in [Appendix D](#appendix-d-checkpoint-selection), so the intervals are conditional on that run and that checkpoint. They do not include variation across training seeds or across checkpoints within a run.

**Pairwise tests.** Every pair of policies within a chart is compared with a two-sided [Fisher's exact test](https://doi.org/10.2307/2340521) on the counts of trials that did and did not complete at speed. For example, two policies at 75% and 65% on 100 trials each give p ≈ 0.16, a gap two equivalent policies would produce about one time in six. Two policies at 75% and 60% respectively give p ≈ 0.03.

**Multiple comparisons.** Four policies means six pairwise tests. If the six tests are run independently at the 5% level, the chance of at least one false "significant" pair is about 26%. We apply [Holm's correction](https://www.jstor.org/stable/4615733), which holds the family-wise false-positive rate per chart at 5%. Letters are assigned from the corrected results and are not comparable across charts.

**Interaction test ([Figure 9](#figure-9)).** The letters in [Figure 9](#figure-9) compare the three compute budgets within one data fraction at a time. The claim that the gap between budgets widens as data shrinks spans all four fractions, so we test it with a single logistic regression fitted to every trial in the figure at once. It predicts at-speed completion from log2 compute share, log2 data fraction, and their product. The product term measures how much the compute effect changes with each halving of the data. Zero would mean the compute effect is the same at every fraction. Its estimate is −0.09 (standard error 0.05), in the direction of the widening. A likelihood-ratio test against the model without it gives χ²(1) = 3.2, p = 0.07. A widening this large would arise about one time in fourteen if the compute effect were the same at every fraction.

## Appendix C: pre-training setup for the two sweeps

**The recipe shared by both sweeps.** Every pre-training run in this post used the same pre-training video dataset and a global batch size that followed the critical batch size. The critical batch size is the point beyond which a larger batch stops saving steps in proportion ([McCandlish et al.](https://arxiv.org/abs/1812.06162)). [Kaplan et al.](https://arxiv.org/abs/2001.08361) find that it depends on the loss alone and grows steeply as the loss falls. We measured it in the same way, taking training runs at several batch sizes, fitting the step-versus-data tradeoff at each loss level, and then fitting the result as a function of the loss. The batch size used the estimated value for most of training. Near the end, when the estimate exceeded the largest batch our compute allowed, we held the batch at that size. The pre-training dataset was large enough that validation loss never rose in any pre-training run.

**The model-size sweep (Result 1).** Kaplan et al. state their model-size law for models trained to convergence on a sufficiently large dataset, and their runs implement that as one fixed step budget for every model size. We did the same. Every model was trained for the same fixed number of gradient steps, and the budget was large enough that every model's validation loss had flattened by the end of it. The four losses flattened after a similar number of steps, consistent with Kaplan et al.'s observation that training curves have a shape roughly independent of model size. The step budget and the dataset are therefore shared across sizes. Batch size and model size are not. Because the batch size follows the loss, and larger models reach lower loss, the larger models saw more tokens, at a higher cost per token. The sweep is neither compute-matched nor token-matched, by design (see [Limitations](#limitations)). The variable is model size under one training recipe.

**The compute sweep (Result 2).** The four budgets are checkpoints of the M-size model's pre-training run, specifically the run that produced the M model of Result 1, so they share the dataset, the data order and every hyperparameter. They are spaced roughly evenly in log compute, each between two and three times the one before. With the model fixed, more compute means more video processed. Budgets are labeled by cumulative training compute rather than by step count because the batch size changed over the run.

## Appendix D: checkpoint selection

[Figure 12](#figure-12) shows the run behind the selection rule in [Choosing which checkpoint to evaluate](#choosing-which-checkpoint-to-evaluate). Validation loss bottoms out near the worst checkpoint we evaluated (48%), and rises through the best ones. The proxy's minimum falls among the three checkpoints tied at the top, 74% to 76%.

![Figure 12: Checkpoint selection](https://www.rhoda.ai/images/scaling/checkpoint-selection__task.svg)

Figure 12: Checkpoint selection

**Figure 12.** *Five checkpoints of one post-training run of the M-size model, each evaluated on the robot (left axis: at-speed completion rate), against two training-time metrics on the right axis, validation loss and our proxy metric, each shown as percent above its own minimum. The marker on each curve is its minimum, the point that metric would pick. Violins are posteriors over the true rate. Policies with no letter in common differ at 95% confidence (explained in Figure 3).*

## Appendix E: post-training curves across pre-training budgets

In [Figure 13](#figure-13) the four curves have the same shape and differ only in position. They fall, bottom out and rise together, and they never cross. More pre-training compute does not change the shape of the post-training curve. It lowers the whole curve, and the gap between budgets at the start of post-training is still present at the end. The order of the four curves is the order of the four policies on the robot in [Figure 7](#figure-7). The two metrics disagree on the best checkpoint in every run, as [Figure 12](#figure-12) ([Appendix D](#appendix-d-checkpoint-selection)) shows on the robot for one of them.

![Figure 13: Post-training curves by pre-training compute](https://www.rhoda.ai/images/scaling/posttrain-curves__val-loss-and-proxy.svg)

Figure 13: Post-training curves by pre-training compute

**Figure 13.** *Validation loss (left) and our proxy metric (right) over post-training for the four M-size runs of Figure 7, one per pre-training compute budget, each post-trained on the full demonstration set. Markers show each curve's own minimum. The proxy is shown relative to the best run's minimum, and the start of each run is cropped.*

## Appendix F: how DINO FD is computed

The held-out clips are a fixed split of the same video dataset the models were pre-trained on, set aside before training, and they share no recordings with the post-training robot task data. Every window of a clip is predicted independently from ground-truth context, so the score does not measure long rollouts. Predicted and true frames are both decoded through the video tokenizer before embedding, so the score reflects the model's prediction rather than the tokenizer's reconstruction. Frames are embedded with a frozen DINOv2 ViT-L/14 (CLS token), one Gaussian is fitted per side, and the standard Fréchet distance is taken over 400,000 frames per side for every model. Values are the ones logged during pre-training, on the exponential moving average (EMA) weights. The evaluation is deterministic, so each value is a single number with no error bar. As a guide to how firm it is, the value at a neighboring pre-training checkpoint differs by 1 to 3%. The model predicts several frames at a time, but the score treats each frame on its own. All predicted frames form one distribution and all true frames another, so temporal coherence and frame order do not have any effect.

**Citation**

Please cite this work as:

```latex
@article{rhoda2026webvideo,
  author = {Rhoda AI Team},
  title = {Does Scaling Web-Video Pre-training Help Real Robots Do Real Work?},
  journal = {Rhoda AI Blog},
  year = {2026},
  note = {https://www.rhoda.ai/research/scaling-web-video-pretraining}
}
```