Recursive self-improvement (RSI) had quite a week. An Anthropic researcher Jacob Coxon [resigned and warned](https://x.com/hilbertspaess/status/2097476196791709843?utm_campaign=fod-167-what-is-recursive-about-recursive-self-improvement&utm_medium=referral&utm_source=www.turingpost.com) that AI labs were racing toward self-improving superintelligence. Other researchers put surprisingly high numbers on the possibility that such systems could eventually cause catastrophic harm. Dario Amodei [argued](https://x.com/DarioAmodei/status/2098773920774074715?utm_campaign=fod-167-what-is-recursive-about-recursive-self-improvement&utm_medium=referral&utm_source=www.turingpost.com) that capability development should slow down enough to give safeguards time to catch up.

The discussion quickly became a discussion about whether AI could kill us. Before going to the extremes, let’s discuss the mechanism everyone is so worried about. What exactly is recursive self-improvement, and how different is it from the AI-assisted research that is already happening?

The simplest version of it is familiar to everyone. Give an AI some code and ask it to improve it. The AI proposes a change, we run the new version, test whether it still works, measure its performance and decide whether to keep it. Then we can do another round.

We already see early versions of this in practice. AI systems are being used to optimize kernels, modify agent scaffolding, propose experiments and make changes to machine-learning code. [AI4AI-Bench](https://arxiv.org/abs/2608.20318?utm_campaign=fod-167-what-is-recursive-about-recursive-self-improvement&utm_medium=referral&utm_source=www.turingpost.com), for example, gives an agent several hours to modify real training algorithms and then evaluates the resulting algorithm by running it again from scratch.

This can be seen as an early form of recursive self-improvement: AI is being used to improve AI. But “improvement” still has to be defined in a way that can be tested. The agent works on a specific task, can change only _certain_ parts of the system, and is evaluated against criteria that remain fixed. That is what makes it possible to compare one iteration with the next.

And what makes one iteration “better” than the other? The definition of “better” really depends on what we are trying to improve. It might mean using less compute, producing more correct code, scoring higher on a benchmark or finding a better way to train another model. Progress on one measure does not necessarily mean progress on the others, so the loop needs a way to evaluate each new version.

But what if we can make the loop more interesting.

![RSI loop](https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,quality=80,format=auto,onerror=redirect/uploads/asset/file/6ba88121-0e4a-434a-96d6-09528470debb/ChatGPT_Image_Sep_14__2026__04_00_52_PM.jpg?t=1789416967)

Instead of asking the AI only to improve a training algorithm, we could let it improve the method it uses to search for changes. We could let it design more of its own experiments, choose which experiments deserve more compute, or develop new ways of evaluating their results. An improved version could then use those new methods during the next round.

This is where recursion begins to mean more than repeated optimization. The object being improved increasingly includes the process responsible for producing the next improvement.

There are already useful distinctions emerging in the research literature around this. A recent paper, with the clickable title [_The Last AI Built by Humans_](https://arxiv.org/abs/2609.11873?utm_campaign=fod-167-what-is-recursive-about-recursive-self-improvement&utm_medium=referral&utm_source=www.turingpost.com), separates several kinds of autonomy involved in self-improvement: carrying out an improvement, choosing an improvement strategy, acquiring useful experience, adapting the environment and eventually improving the improvement process itself. The paper [Recursive Criticality](https://arxiv.org/abs/2609.00137v1?utm_campaign=fod-167-what-is-recursive-about-recursive-self-improvement&utm_medium=referral&utm_source=www.turingpost.com) makes a related distinction: fast AI progress is not necessarily recursive self-improvement. AI development can become increasingly automated while some parts of the improvement loop remain fixed.

![Minimal AI self-improvement loop](https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,quality=80,format=auto,onerror=redirect/uploads/asset/file/bd74bb7e-7b1b-4aba-ab27-be261dfe2c8c/Screenshot_2026-09-14_at_4.15.40_PM.png?t=1789417063)

Image Credit: Recursive Criticality of AI Self-Improvement paper

This brings us back to one of the questions raised last week: **where, in this improvement loop, can the process be interrupted?**

As far as we know, in current systems, stopping is usually quite straightforward: an experiment may reach its compute limit, fail a test or perform worse on another evaluation. A result may also fail to hold up in a different setting. In those cases, researchers can reject the change and return to an earlier version because parts of the process, including the evaluation, remain outside the system being improved.

**The situation changes if those pieces also become editable.**

![What remains outside the system’s permission to change?](https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,quality=80,format=auto,onerror=redirect/uploads/asset/file/db875c93-665f-49b0-880d-bf32187833b8/ChatGPT_Image_Sep_14__2026__04_04_51_PM.jpg?t=1789416998)

Suppose an AI develops a new evaluator and that evaluator says its latest research strategy is better. We now need some reason to trust the new evaluator. Perhaps we compare it against human judgments, protected test data or another independent evaluation. But if the system can eventually modify that process as well, we have simply moved the same question one level higher.

**This is one reason verification is becoming so central to discussions of AI-assisted research.** Some improvements are relatively easy to check. Code can be tested. A kernel can be measured for speed and separately checked for correctness. Some mathematical results can be formally verified. It is much harder to establish that a new research strategy is genuinely better, or that an experiment the system has decided to pursue is the right experiment in the first place.

**None of this requires the AI to secretly want something, resist its operators or develop an instinct for self-preservation.** There is a more ordinary problem underneath it. If a system repeatedly optimizes against a particular measurement, we need to know whether that measurement still represents what we care about. If parts of the measurement process can also be changed by the system, **we need another way to check the result.**

So “AI improves AI” is already here. What I’m more interested is is the gradual expansion of what AI is allowed to change.

This gives us a more practical way to think about recursive self-improvement. When a new result appears, we can ask a few specific questions:

**What is the AI changing, how do we know the change is actually an improvement, and what still remains outside the loop?**

Those questions give us a clearer sense of what these systems can actually do today.

_More sources about RSI:_

- [AI 101: What is Recursive Self-Improvement?](https://www.turingpost.com/p/what-is-recursive-self-improvement)
    
- [9 Paths Toward True Recursive Self-Improvement](https://www.turingpost.com/p/9-paths-toward-true-recursive-self-improvement)
    
- [∇ Guide: The Missing Pieces in Recursive Self-Improvement](https://www.turingpost.com/p/missing-pieces-in-recursive-self-improvement)