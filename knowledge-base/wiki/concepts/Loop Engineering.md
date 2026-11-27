---
type: concept
created: 2026-08-05
updated: 2026-11-27
tags:
  - concept
  - ai-agents
  - orchestration
  - evaluation
source_ids:
  - src-2026-08-05-aibuilderclub-loop-engineering-guide-2026
  - src-2026-08-05-aibuilderclub-loop-engineering-anthropic-playbook
  - src-2026-08-05-aibuilderclub-loop-engineering-karpathy
  - src-2026-08-05-aibuilderclub-loops-md-karpathy
  - src-2026-08-05-aibuilderclub-types-of-agentic-loops
  - src-2026-08-05-aibuilderclub-loop-engineering-addy-osmani
  - src-2026-08-05-aibuilderclub-self-improving-agent-loops
  - src-2026-08-05-aibuilderclub-loop-engineering-case-study
  - src-2026-08-12-yoko-li-loop-convergence
  - src-2026-08-20-liquid-ai-production-loops
  - src-2026-07-16-lilian-weng-harness-engineering
  - src-2026-10-29-decagon-autoresearch-inference
  - src-2026-10-29-factory-droid-frontier-harness
  - src-2026-06-11-0xcodez-fable-5-self-improving-agents
  - src-2026-07-20-0xcodez-graph-engineering-roadmap
  - src-2026-11-11-wills-levels-agentic-engineering
  - src-2026-11-12-huntley-answer-is-engineering
  - src-2026-10-31-l1vsun-five-levels-ai-engineering
  - src-2026-11-13-william-hu-always-on-agents
  - src-2026-11-25-frank-rousseau-agentic-coding-open-source
  - src-2026-11-20-ankit-gupta-vibecoding-inference-chip
status: active
---

# Loop Engineering

Loop engineering is the design of a repeated agent cycle around an objective: what triggers it, what state it reads and writes, how it plans and acts, what verifies progress, when it retries or escalates, and what stops it. It extends the basic [[Agentic Loop]] from control flow into an operating discipline for unattended or repeatedly invoked work.

## The verifier is the scarce component

Generating another candidate is usually cheap. Determining whether that candidate improved the world is harder. A useful loop therefore needs an operational verifier rather than a request to "review your own work":

- deterministic checks such as tests, schemas, type checks, or policy rules;
- behavioral checks that operate the artifact through its real interface;
- external signals such as conversion, incident, or quality metrics;
- rubric-based model judges where deterministic truth is unavailable;
- human review for ambiguous or high-impact decisions.

Generation and evaluation should be separated when possible. A fresh evaluator still has blind spots, but it avoids inheriting the producer's full reasoning path and assumptions.

[[Geoffrey Huntley - The Answer to AI Is Engineering]] frames the verifier as **back pressure**: "Ralph
was never just about loops. It was about stopping the loop from closing on bad code." His checks are
deterministic ("These aren't skills. This is engineering again."): hooks that block a push when the
build fails, static domain-coupling rules, and NixOS VM tests that bring up production-shaped
infrastructure, for example HAProxy in front of a hello-world server across two VLANs. When the agent
finishes a unit of work, he tests it "on exactly what would be production infrastructure", because the
infrastructure is defined as code and the same Nix flakes can run production. His property-based
testing material adds generated counterexamples as a further verifier type; the libraries he promotes
come from his employer, [[Antithesis]] (see [[Agentic Testing]]). This is a practitioner talk with no
measured comparison of loop outcomes with and without these checks.

## Loop contract

A durable loop makes six things explicit:

1. **Objective** — the state to improve, not merely an activity to perform.
2. **Trigger** — turn, goal, schedule, event, or external signal.
3. **State and artifacts** — inspectable files, records, or checkpoints shared across iterations.
4. **Actions** — bounded tools and permissions available to the worker.
5. **Verifier** — evidence that distinguishes progress from plausible output.
6. **Exit and escalation** — success, budget exhaustion, repeated failure, or human handoff.

Open loops permit exploration under budgets and quality floors. Closed loops converge toward explicit pass criteria. Self-improving loops add another risk: the system can modify prompts, skills, or harness rules, so proposed changes need held-out regressions and rollback rather than self-approval.

## Terminology and prior art

"Loop engineering" is useful vocabulary, but much of the machinery predates the label: control loops, CI, workflow engines, retry policies, state machines, and optimization systems already encode objectives, feedback, state, and stop conditions. The durable contribution is the emphasis on verification as the autonomy bottleneck, not a claim that repeated workflows were invented in 2026.

## Convergence and stopping economics

[[Yoko Li - Knowing When to Stop - The Art of Making a Loop Converge]] sharpens the loop contract into four convergence conditions: a target state, observable current state, precise local actions, and an external stopping rule. Editability and verifiability are properties of the task representation, so reframing an opaque output as structured code, SVG paths, or a scene graph can move a task into a regime where repair is possible.

Completion is also economic. Loops need impossibility detection, diminishing-return limits, cost per iteration, and progress per dollar. Otherwise a verifier can repeatedly reject a correct ceiling diagnosis while the growing transcript makes every unproductive iteration more expensive.

## Production-scale execution as specification discovery

[[Liquid AI - Designing Loops for Production-Grade Work]] shows why an executable target is part of the specification. Coding agents building a tokenizer trainer cleared obvious functional tests but encountered encoding, memory, parallelism, tokenization, ordering, and duplicate-input failures only against real datasets and external reference implementations.

The resulting pattern is:

- specify interfaces and invariants without prescribing the implementation;
- run against representative production-scale inputs;
- keep the acceptance harness outside the agent's write boundary;
- feed exact failures back into bounded iterations;
- stop only on externally measured behavior.

The case study does not prove universal autonomy, but it demonstrates that iteration can convert production failures into missing requirements that a one-shot prompt never contained.

## Where the loop sits on the optimization ladder

[[Lilian Weng - Harness Engineering for Self-Improvement]] places workflow design on a five-rung ladder
— prompts, structured context, **workflow**, harness code, optimizer code — and shows that the
workflow rung is now a target for automated search rather than hand design. **AFlow** runs Monte Carlo
tree search over workflow graphs; **ADAS** searches over agent designs directly.

Weng's three recurring harness patterns are the hand-designed vocabulary that search operates over:
**workflow automation** (turning a repeated manual sequence into a durable procedure), **the file
system as persistent memory**, and **sub-agents or backend jobs** that isolate work so it does not
contaminate the parent context.

The caution attached is the one that governs the whole ladder: automated workflow search only helps if
the base model can propose good candidates. STOP improved with GPT-4 and **degraded** with GPT-3.5 and
Mixtral. See [[Harness Optimization]].

## A winning iteration needs both a moving working baseline and a fixed campaign reference

[[Pavi Dhiman and Cyrus Asgari - Building an Inference Stack That Improves Itself]] supplies
a production-inference loop contract. Humans choose the campaign; specialists propose
falsifiable interventions; a single orchestrator runs scored trials against the same replay,
schedule, and latency/error constraints. Repeated baselines establish the noise floor.

Its verdicts distinguish **Better, Same, Worse, and Invalid**. Invalid means the experiment
cannot support a conclusion, not that the hypothesis failed. A confirmed win becomes the
next working baseline, while the original configuration remains the reference for the whole
campaign. This prevents a sequence of local improvements from losing its comparison point;
combined changes still need ablations.

GPU, time, GPU-hour, and training-variant budgets bound exploration. Pinned recipes and
checkpoints, CPU checks, and a 50-step GPU rehearsal reduce expensive invalid runs. Lossless
and lossy changes have different acceptance requirements, and a human approves production
promotion. These are reported process controls, not evidence that the benchmark is
technically immutable or that repeated replay consultation cannot overfit it.

## A product that runs its own improvement loop

[[Factory Research - Droid 1.0 - Building a Frontier Harness]] describes a self-improving
loop in which the product improves itself. [[Factory AI]]'s "Agent Factory" adds each new
model to Droid, checks it against behavioral assertions ("the minimum, not the bar for
release"), then gathers live-environment results, QA, daily benchmark runs, error logs, and
user friction. An agent looks for causes that repeat across tasks and models and turns each
into a proposed change that states its hypothesis; a controlled experiment measures the
change on every model it touches. "Droid runs every step itself, and nothing ships until an
engineer reviews and merges it. The improved Droid then runs the next loop."

Against the loop contract above, the human merge step answers self-approval, and each
proposal is checked against five written principles as well as its experiment. Two parts of
the contract are not described: a held-out regression set kept apart from the benchmark runs
that feed the loop, and a rollback path after a merged change. The proposer is also the
product being improved, so on this page's reading a change to Droid can also alter the agent
that proposes the next change. The post reports outcomes of the loop — prompt-cache fixes,
Script-mode tuning across four model families — but no rate of accepted versus rejected
proposals. See [[Harness Optimization]] and [[Benchmark Optimization]].

## Harness primitives now package the verifier and the stop rule

Two influencer-style courses by [[@0xCodez]] show the loop contract above appearing as named features
of the Claude tooling rather than as code a team writes. Their mechanisms are concrete, but most of
their performance claims are unsourced.

[[@0xCodez - Build a Self-Improving Agent System with Fable 5 in 14 Steps]] describes `/goal` in
Claude Code and Outcomes in Claude Managed Agents as "two near-identical primitives" with one shape:
"an independent grader checks the work, a not-met verdict starts the next iteration, the loop exits
when the grader passes." The difference is where the contract lives. `/goal` takes a plain-text goal
and a model grader for an in-session loop; Outcomes adds a file-based rubric with gradable criteria, a
sub-agent grader, and a hard `max_iterations` bound, which covers the verifier and exit items of the
contract explicitly. The post relays a Claude Code team line, "a verifier sub-agent tends to outperform
self-critique with Fable 5", as confirmation of this page's separation rule, but reports no numbers.
Routines then supply the trigger item: saved configurations that run in the cloud on a schedule, an
API call, or a GitHub event. The post's examples are a 7 am eval rerun, a CI failure that fires an
investigation, and a merge that writes new patterns back into a Skill.

[[@0xCodez - Graph Engineering with Claude - 14-Step Roadmap from 0 to Graph Architect]] supplies a
stopping rule for loops whose size is unknown in advance, such as a bug sweep. "Loop-until-dry" keeps
spawning finder agents "until K consecutive rounds surface nothing new"; the example stops after **2**
empty rounds. The detail it singles out is what counts as new: "Dedupe against everything seen, not
just against confirmed results", or rejected findings return every round and the loop never runs dry.
The example also checks each fresh finding through three lenses and keeps it if at least two judges
call it real. It has no iteration or budget cap, although the course warns that a cycle that does not
converge "spawns agents until your budget is gone". By this page's stopping economics, a dry-round
count is a diminishing-return limit, and it still needs a budget bound beside it.

## Done means delivered: CI-triggered agents and a release watcher

[[Zach Wills - The Levels of Agentic Engineering]] extends the loop contract past merge. At his level
3, CI is both a check and a **trigger**. If a pull request arrives "without an end-to-end test for the
new flow", the check does not just fail; it "triggers an agent to write the test". He calls CI "the
best enforcement point you have" because every change passes through it, whatever local prompts
people use. He asks agents for "irrefutable proof", including a recorded video of the feature working,
and warns that agents "will happily generate filler unit tests that don't protect anything". At level 5
a release-watcher agent checks behaviour in production and returns failed work to the board: "'Merged
to prod' and 'mission complete' are two different things."

In this page's terms, the verifier moves from the repository to production, and the exit condition
becomes business value. The essay does not say how that value is specified or measured, so the release
watcher's own pass criterion is unstated. The source is experience-based opinion with no outcome data.

## Brakes, timers, and a per-model audit loop

[[@L1vsun - Prompt, Context, Harness, Loop, Graph - The 5 Levels of AI Engineering]] lists four brakes
for a loop on a timer, because such a loop "can spend money all night":

- a done check that runs outside the model, such as a Stop hook that blocks completion until tests pass;
- a budget of maximum runs, tokens, or dollars;
- a dry-round rule: "stop after two rounds that find nothing new";
- state written after every step, so a crash resumes instead of starting over.

The dry-round rule is the same stopping rule as the **2**-empty-round example above, and the budget is
the bound that example lacked, so together they meet this page's stopping economics. The post's loop
anatomy relays the same Osmani essay as
[[AI Builder Club - Addy Osmani's Loop Engineering - The 5 Components]], so the two are not independent
confirmations. It also says Claude Code's `/loop` runs a task on an interval, or at the model's own pace
when no interval is given. Its summary line is "The loop removes the typing, not the thinking."

[[William Hu - Building Always-On Agents]] supplies the trigger mechanism behind scheduled and
self-scheduled loops. A **follow-up** is a deadline the agent sets for itself; a **schedule** is a
recurring task. Both live in a timer store separate from the event inbox. A scheduler polls, marks
follow-ups done or advances schedules, then adds an event to the inbox and wakes the worker, so a timer
never starts a run directly. Because each inbox has only one active worker, and the guide starts with
one inbox per user, two wakes for the same user cannot run at once. For loops that message people, its
advice is to "start quiet and then earn more of the user's attention over time", tuned by evals for
message volume that it does not describe.

[[Frank Rousseau - Agentic Coding on an Open-Source Project]] runs one maintenance loop by hand. A full
audit on **8 aspects** (architecture, bugs, security, cleanliness, test coverage, performance,
documentation, dependencies) produces a to-do list; he prunes it, then runs it as a loop that commits
each improvement, and repeats the cycle "whenever a new model comes out". His pruning is the gate
between finder and executor. The evidence is his own account, and it records a limit: outside security
researchers later reported three holes that the audits missed.

## Shortening the inner loop can move cost into the outer one

[[Ankit Gupta - Vibecoding an Inference Chip]] gives a hardware case of the trade between a fast loop
and a thorough verifier. A coding agent optimizing an FPGA decoder under a bit-exact contract had a
cycle-accurate simulation running for about 24 hours when outside advice told it to stop doing things
"that take a lot of times". It switched at once to a short loop of C tests, synthesis and a logic-depth
check, with one place-and-route per integration. The agent's retrospective says this process advice
changed things "right away", while the advisers' design ideas were mostly already planned.

The same retrospective names a possible price that it "can't prove": two hangs that only RTL simulation
could have shown reached the board, and the big integration lost **38 hours** to them. Late in the run,
a soak test found random faults at the fastest clock, and the final image shipped at a lower one.
*Reviewer inference:* a faster inner loop still needs a slower check somewhere before hardware.

## Open questions

- How should loops verify strategic or long-horizon work when feedback arrives late?
- How can teams detect proxy optimization when the measured verifier diverges from the real objective?
- What evidence should be required before a loop earns more permissions, budget, or runtime?

## Related pages

- [[@0xCodez - Build a Self-Improving Agent System with Fable 5 in 14 Steps]]
- [[@0xCodez - Graph Engineering with Claude - 14-Step Roadmap from 0 to Graph Architect]]
- [[@0xCodez]]
- [[Pavi Dhiman and Cyrus Asgari - Building an Inference Stack That Improves Itself]]
- [[Decagon]]
- [[Serving Benchmarks and Goodput]]
- [[Persistent Wiki]]
- [[Agentic Loop]]
- [[Graph Engineering]]
- [[Multi-Turn Evaluation]]
- [[Coding Agent Harness]]
- [[Agent Planning]]
- [[Agent Skill]]
- [[Agent Security and Governance]]
- [[AI Builder Club - Build AI Agents]]
- [[Yoko Li - Knowing When to Stop - The Art of Making a Loop Converge]]
- [[Test-Time Scaling]]
- [[Liquid AI - Designing Loops for Production-Grade Work]]
- [[Harness Optimization]]
- [[Lilian Weng]]
- [[Lilian Weng - Harness Engineering for Self-Improvement]]
- [[Factory Research - Droid 1.0 - Building a Frontier Harness]]
- [[Factory AI]]
- [[Benchmark Optimization]]
- [[Zach Wills - The Levels of Agentic Engineering]]
- [[Geoffrey Huntley - The Answer to AI Is Engineering]]
- [[Agentic Testing]]
- [[@L1vsun - Prompt, Context, Harness, Loop, Graph - The 5 Levels of AI Engineering]]
- [[William Hu - Building Always-On Agents]]
- [[Frank Rousseau - Agentic Coding on an Open-Source Project]]
- [[Antithesis]]
- [[Ankit Gupta - Vibecoding an Inference Chip]]
