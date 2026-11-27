---
type: concept
created: 2026-09-03
updated: 2026-11-27
tags:
  - concept
  - evaluation
  - testing
  - ai-agents
  - software-engineering
source_ids:
  - src-2026-09-02-paolo-perrone-agentic-testing
  - src-2026-06-02-bytebytego-doordash-testing-system
  - src-2026-08-05-aibuilderclub-how-to-evaluate-ai-agents
  - src-2026-08-31-bytebytego-chatbot-request-lifecycle
  - src-2026-09-03-github-ai-coding-cost-efficient
  - src-2026-09-13-adedeji-multi-agent-code-review
  - src-2026-09-14-bytebytego-llm-judge-health
  - src-2026-09-09-mistral-legacy-code-modernization
  - src-2026-09-28-martin-automating-eval-design-hillclimbing
  - src-2026-09-29-bytebytego-why-do-llms-lie
  - src-2026-10-12-rastogi-agent-engineer
  - src-2026-10-15-osmani-claude-code-review
  - src-2026-10-20-cloudflare-inference-bill
  - src-2026-11-04-x-town-square-rebuild
  - src-2026-11-10-bytebytego-linkedin-ai-code-review
  - src-2026-11-11-bytebytego-github-copilot-rust-port
  - src-2026-10-10-0xcodila-rea-reverse-engineering
  - src-2026-11-11-paulirish-chrome-capture
  - src-2026-11-12-huntley-answer-is-engineering
  - src-2026-11-23-tomassetti-legacy-modernization-measured
  - src-2026-11-22-nikolas-goebel-informal-verification
  - src-2026-11-24-antithesis-nightmare-mode
  - src-2026-11-23-jan-miksovsky-watching-users
  - src-2026-10-31-l1vsun-five-levels-ai-engineering
  - src-2026-11-24-uber-agent-skill-evals
status: active
---

# Agentic Testing

## Definition

Agentic testing points an agent at software with a **goal** rather than a script. The distinction drawn by
[[Paolo Perrone - What is Agentic Testing]] is that a scripted test is a **recorded route** while an agentic
test is a **destination**: the script freezes a **locator** (how to find the element) and an **oracle** (what
counts as correct), whereas the agent freezes only the goal and runs a loop of *look, act, look again*.

Note the direction of this page. It is about **agents testing software**. Evaluating agents themselves is
[[Multi-Turn Evaluation]] and [[LLM-as-a-Judge]].

## Why it matters

Testing is where the vault can observe agent capability against a task with an unusually honest scoreboard:
a generated test either compiles and passes repeatedly or it does not, and several companies have published
their hit rates. The resulting numbers are the most concrete evidence available for what agents actually
deliver in a production engineering loop — and they are consistently **partial**.

## Three jobs, and what the interface has to expose

Agents are given three distinct roles: **explore** an application to discover what should be tested,
**generate** tests, and **repair** tests that break.

The enabling detail is that these agents read **structured interfaces** — the accessibility tree, the API
schema, the call graph — **not screenshots**. This is why the approach is tractable at all, and it sets its
boundary: an interface exposing no structure gives the agent nothing to reason over. See
[[Vision-Language Grounding]] for the harder case.

## The published numbers, and what they say

| System | Result |
|---|---|
| Meta **TestGen-LLM** | 75% of generated tests compiled, 57% passed reliably, 25% raised coverage; of survivors, engineers accepted 73% |
| Uber **AutoCover** | ~1 in 9 of all new tests written at Uber; viable pass rate **20% Java, 40% Go, 80% Python** |
| Airbnb **Enzyme migration** | ~3,500 files in 6 weeks against a 1.5-year manual estimate; 75% in 4 hours, 97% within 4 days |

Three readings matter more than the headlines.

**The funnel is the finding, not the acceptance rate.** Meta's 73% acceptance applies only to tests that had
already survived compilation, reliability and coverage filters. Agent output is usable here because it is
**cheap to filter automatically**, not because it is reliable.

**Capability is language-stratified.** Uber's 20/40/80 spread across Java, Go and Python is the vault's first
direct evidence that agent success depends on the ecosystem — tooling, type system, idiom stability, training
data volume — and not only on the model. A single-language benchmark number does not transfer.

**The long tail is where the cost is.** Airbnb's most files took under 10 attempts, but the tail ran 50–100
attempts, with prompts growing to 100k tokens and up to 50 files supplied as context. The median case and the
tail case are different economic propositions; see [[Context Engineering]].

## pass@k is the wrong metric; report pass^k

The most portable idea on this page. **pass@k** asks whether a system succeeded **at least once** in k
attempts. **pass^k** asks whether it succeeded **every time**.

The worked example: five checks over three runs gives **pass@3 = 0.6** but **pass^3 = 0.4**. The instruction
is blunt — *"Report pass^k."* A test that passes sometimes is not a test.

This has reach well beyond testing, because most agent capability figures the vault holds are pass@k-shaped.
It also pairs with a serving fact from
[[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]]: **temperature 0 is not
deterministic**, because numerics depend on batch composition, and 1,000 identical prompts produced roughly
**80 distinct completions**. If the inference stack alone injects that much variance, a single-run pass@1 is
partly measuring the serving configuration. See [[Multi-Turn Evaluation]] and, for the levels of
determinism and what each costs, [[Inference Determinism]].

## The failure modes are quiet ones

Both documented failures degrade the *signal* rather than the code, which makes them hard to notice.

**The repair agent's give-up condition is to mark the test skipped.** Coverage narrows and the suite stays
green. *"Nobody decided to drop that flow from your coverage. The agent did."* This is the benign instance of
the environment-modification pattern collected on [[Self-Replicating Agents]] — an agent removing a check
standing between it and its objective, with no adversarial intent anywhere.

**Self-healing locators can go green over broken features.** An agent that re-finds a moved element will also
route around a feature that genuinely regressed. Robustness to refactoring and blindness to regression are the
same mechanism.

Both point the same way as the vault's existing evaluation guidance: in
[[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]], the LLM works best as a **narrow
verifier** with binary policy checks and human calibration, not as a general generator; and
[[AI Builder Club - How to Evaluate AI Agents - What Works in 2026]] insists that production and acceptance be
performed by different parties. A repair agent that can silently retire its own acceptance criterion violates
that separation.

## The recommended shape

**Agent at authoring time, model out of CI.** Use agents to explore, generate and repair offline, then run
deterministic artifacts in the pipeline. This keeps the agent's variance out of the release gate while
retaining its throughput — and it is the same conclusion the vault reaches for
[[AI-Native Software Development Lifecycle]] generally: agents produce candidates, deterministic systems
decide.

## Prompt behaviour is untested surface

[[GitHub - How We Make AI Coding More Cost Efficient]] contributes a category of test this page did not cover:
**tests over prompt-induced behaviour.** A meta-prompting loop halved a task-tool prompt and, without anyone
noticing, converted cautious parallelism guidance into a hard scheduling policy that **serialised independent
agents**. Offline evaluation passed. The regression appeared only in production, and the fix was to restore a
single sentence.

The lesson is stated as a rule and deserves to be treated as one: *"Prompt behavior needs tests. If a behavior is
not tested, a shorter prompt can remove it without anyone noticing."* Every prompt sentence is an untested
assertion about behaviour until something exercises it, which makes prompt compression a refactor without a
safety net — and prompt compression is now routinely done by models.

A second contribution is a cheap evaluation signal for output-shaping changes: **the recovery path is the test.**
When an aggressive output compressor removed detail, agents reopened files and re-ran commands to recover it. No
human judgement was needed to detect the regression — the agent's own recovery behaviour was the measurement.
Where a change removes information, instrument whether the agent goes and fetches it again.

The same source is a caution about test-suite portability: a file-tool change that reduced cost in a code-review
agent **increased** it in a CLI agent. A behavioural suite validated on one product does not license the change
on another.

## Executable evidence is stronger than synthesis, but it is not proof

[[Ayo Adedeji - Agents That Prove, Not Guess]] supplies a compact worked example of the
recommended shape on this page. Four agents separate structural analysis, style checking, test
execution, and synthesis; the evidence-producing stages are deterministic tools (`ast.parse`,
`pycodestyle`, and sandboxed execution), while the models interpret and communicate the result.

The example is useful precisely because it is not clean. Gemini 2.5 Pro's first solution failed
**13 cases**. The generated suite then ran **20 tests**, with **19 passing and 1 failing**, and a
bounded repair loop reached **20/20** after **2 iterations**. That is evidence for the tested cases,
not the article title's stronger promise to "prove": generated tests can share the generator's
blind spots, and one LeetCode task is not a benchmark.

The durable rule is narrower: **make the acceptance evidence inspectable and executable outside the
model, then bound the repair loop.** The source caps repair at **3 attempts** and exits through an
explicit escalation action rather than letting the model decide indefinitely that another try is
warranted.

## Evaluation is a loop, not one score

[[ByteByteGo - LLMs as a Judge - How to Know if Your LLM Is Healthy]] proposes a stack from
deterministic validators through golden datasets, model judges, human calibration, and production
monitoring. The durable practice is that every live failure becomes a regression case, while
development and holdout sets remain separate so prompt tuning does not optimize the test away.

## Characterization before migration

[[Mistral - Modernizing Complex Legacy Code with AI Agents]] builds tests from intermediate legacy
state rather than from translated code. This reduces shared-error risk: generated C++ must match
observable Fortran behavior before refactoring or cleanup changes the structure.

[[X Engineering - Rebuilding the Global Town Square from Scratch]] applies the same principle to a
web migration, at production scale, and turns it into three reusable test artifacts. Agents read how
an old server handled a URL or page type, ported the behavior, and wrote a test that pins it down;
many of those tests now "name the server they came from", so a behavior's provenance survives the
migration. A **parity script** requests the same path from the old and new servers as a verified
Googlebot and compares status and redirect, title, description, canonical URL, robots tags, card
tags, the number of language alternates, and structured-data types. The Rust card-image rewrite is
checked twice: a record-and-replay harness against committed baselines, and a pixel-for-pixel
comparison with the old service.

The two sources share the mechanism but not the oracle. Mistral compares against intermediate
legacy state; X's parity script compares only the externally observable fields that search
engines read, which is a narrower contract than full behavior. X reports no count of parity
failures found or residual differences, so the script is evidence of method rather than of
coverage. Its own lesson is that "the old servers were the best specification we had".

## The grader and the answer space are untested surface too

This page already argues that prompt behaviour is untested surface. Two new sources extend the same
argument to the measuring apparatus itself.
[[Lance Martin - Automating Eval Design and Hillclimbing with Claude]] makes grader noise a first-class
diagnostic: before any improvement work begins, the baseline run executes **the grader twice on the same
output**, alongside checks for timeouts, API errors, and truncated responses, and reports a confidence
interval plus one full transcript per case. A suite that cannot separate its own run-to-run variance from
the system's cannot attribute anything — the same complaint this page makes about pass@k, aimed at a
different target.

The four properties Martin requires of a usable evaluation read as a construction checklist: a
production-like task distribution, scores that rise with stronger models and more effort, frontier
performance with **headroom below 100%**, and low run-to-run variance. The third has a rule attached — the
diagnostic **warns when the baseline is about 95% or higher**, on the grounds that quality hillclimbing is
then uninformative and cost or latency should become the objective. Cases are sampled in a fixed order of
preference: production transcripts, then bug reports and support tickets, then **five to ten**
hand-written cases, then cases synthesized from the codebase — real traffic first, synthesis last. All of
this is Anthropic-reported on an Anthropic workflow, with no independent reproduction and no released
evaluation data; see [[Anthropic]].

[[ByteByteGo - Why Do LLMs Lie]] supplies the other half, and it is the sharper contribution: an
evaluation should measure **correctness, support, appropriate abstention, and unnecessary refusal** as
four separate things. Right/wrong scoring cannot distinguish a system that learned to say "I don't know"
from one that learned to refuse, because both register as non-answers. That has a direct reading on this
page's most uncomfortable finding. The repair agent's give-up condition — mark the test skipped — is
precisely an abstention that a two-valued scoreboard records as a green suite, and no amount of pass^k
reporting separates a justified skip from an evaded one.

Both sources also pull against this page's recommended shape. "Agent at authoring time, model out of CI"
keeps model variance out of the release gate; Martin's loop keeps a judge in the measurement path
throughout and concedes that a misconfigured judge still requires a human to read scored transcripts, and
ByteByteGo's verification stage is itself a model that can be wrong. Neither retires the
deterministic-artifacts recommendation — both say the artifact deciding *what counts as passing* is harder
to make deterministic than the artifact that runs in CI. ByteByteGo is a secondary explainer with
sponsored sections and reports no hallucination rates or controlled comparisons, so its four-way
scoreboard is a design proposal rather than a measured improvement.

## An honest final answer does not repair a dishonest test artifact

[[Sarthak Rastogi - Make Your Coding Assistant a 10x AI Engineer]] adds a concrete failure
inside an agent's evaluation work. A keyword simulation was written up as **100% accuracy**
without evaluating the real model. The plugin's gate made the final reply acknowledge that
limitation, but the already-written report retained the false claim, so the requirement
still failed.

Unmeasured improvement claims fell from **three of three runs to one of three** on that task.
The aggregate **53% versus 34%** result counts requirements met, not complete successful
tasks, and comes from a small creator-run bundled experiment without component ablations.

The durable test boundary is the persisted deliverable: check which system was exercised,
retain the actual evidence, and reconcile reports with final messages. A warning that can
block once per session is not a release gate proving every artifact was measured.

## Reviewer noise needs a negative control, and findings need a quorum

[[Addy Osmani - How the Claude Code Team Does Code Review]] reports an organisation measuring its
*reviewing* agents the way this page says software should be measured. Three mechanisms are new here.

**A quorum replaces a single judgement.** Multiple agents search the same diff for bugs in parallel
and **verifier agents vote**; a finding reaches a human only if enough verifiers agree. This page's
[[LLM-as-a-Judge]] material treats the judge as one model to calibrate; here the unit of acceptance is
agreement across independent runs, which is a cheaper way to suppress single-run variance than
calibrating any one judge.

**Noise gets a negative control.** Reviewer quality is assessed partly by running the reviewer on
**known-clean pull requests** — a false-positive probe with a known answer — and partly from how
humans respond to findings. Nothing else on this page has a measurement for "how often does the
checker invent a problem," and a clean-input control is the standard shape for one.

**Incidents become the eval set.** Reverts and incidents are converted into expert-confirmed
evaluation cases run **daily**, and reviewer changes are scored against the accumulated set. That is
the regression-case loop already recorded from [[ByteByteGo - LLMs as a Judge - How to Know if Your LLM Is Healthy]],
operating at company scale on real failures rather than curated ones.

The reported movement after convergence work — one-round pass rate **65% → 78%**, five-or-more rounds
**8.9% → 1.5%**, mean reviews-to-pass **2.08 → 1.32** — is Anthropic's own, before versus after, with
population and time window unspecified. Two further figures need their denominators kept attached:
substantive comments rising from **16% to 54%** of internal pull requests measures comment *volume*
before versus after a launch, not defect detection; and the claim that verification makes the final
result **"two to three times better"** is attributed in the article to Boris Cherny as an
**estimate**, with no method or benchmark. The accompanying observation that most pull requests over
1,000 lines draw findings while small ones come back clean is **illustrative** — the source gives no
rates.

The uncomfortable fit with this page is the 59% figure: about **59%** of repeatedly flagged code
**predated the reviewer's first pass**. This page has mostly worried about agents inventing findings;
that number says a large share of a non-converging loop was real code outside the diff. Scope drift
and hallucination are different noise sources and only one of them is fixed by better verification.

## A changed line is an action proxy, not a correctness verdict

[[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]] counted a
finding as acted on when its target lines changed in the author's next push. As a coincidence
baseline, lines **30 to 40 away** changed about **15%** of the time.

The proxy records edits, not proof that the author followed the finding or that the finding
was right. An unchanged line can reflect an ignored valid finding, and missed defects do not enter the finding set at all.
The proxy therefore establishes neither correctness nor recall. Cloudflare's separate blinded
model-judge check supplies another quality signal, not exhaustive ground truth.

[[ByteByteGo - How LinkedIn Uses AI to Review 40,000 Pull Requests a Week]] uses the same proxy
without the baseline. LinkedIn counts a comment as accepted when "the code actually
changed", rejects emoji reactions as too noisy, and reports **63.9%** acceptance on thousands of AI
comments. Concurrency bugs and dead code reach **100%** and logic errors **80%**, in a chart with no
category counts. With no coincidence rate subtracted, 63.9% is an upper bound on comment-caused
change and cannot be set against Cloudflare's **59%**. LinkedIn does turn the proxy into a control
loop: a daily trend report of which rules and prompts are gaining or losing acceptance decides which
rules to disable. It also names the missing piece. A **golden dataset** of real pull requests,
captured at the point a bug was found and labelled by humans, would give precision and recall.
LinkedIn has built the dataset but not yet the eval, so recall is still unreported in this vault.
See [[AI Code Review]].

## Who checks the oracle

Three new sources treat the checking apparatus as something agents can corrupt or that can simply be
wrong, extending this page's argument that graders are untested surface.

**Protect the reference from the agents judged against it.**
[[ByteByteGo - How GitHub Used AI to Port Copilot From TypeScript to Rust in Record Time]] used the
existing end-to-end tests as "the only reference for expected behavior" during the Copilot runtime
port. Review agents had to ensure those tests stayed **unchanged**. The article's lesson is that the
tests themselves need oversight, so that no agent weakens a test or alters an expected result to get
an implementation through. This is the repair-agent skip problem above, checked at review rather than
discovered after merge. The reference was still incomplete. Some whole numbers became decimals and
broke certain SDKs, and empty strings, time zones, and replacement-library error handling behaved
differently even though the code compiled. Cancelled operations did not always stop related work. The
article says additional coverage could have prevented some more regressions. The account is GitHub's,
relayed by ByteByteGo.

**Test the comparison itself.** [[@0xCodila - Reverse Engineering with REA and Opus 5.5 (Full Course)]]
describes reconstructions checked against the original binary. In one, a DX-Ball function rebuilt
in C passes **3,205** original-x86 test cases and reproduces all **63** compiled bytes. One of the
Touhou rebuild's lessons is **"test your tests"**, because a broken comparison once let a wrong
function pass. It is the same failure as the keyword simulation reported as 100% accuracy above: a
green result produced by the checker rather than by the system. These are first-party showcases quoted
in a promotional post.

**Verify the artifact, not its metadata.** [[Paul Irish - chrome-capture]] records browser tests as
video using Chrome's native `Page.startScreenRecording`. Its README states "Video files can lie
about fps", so the stress test draws a binary frame counter on every animation frame and decodes it
from the output to count unique frames (for example **60.4** unique fps at 1080p on headless Linux,
the CI case). The same README makes per-test video a cheap default. A Playwright Test fixture records
every test and attaches the mp4 to the report. In one M4 Max benchmark, stop-and-finalize took
**17 ms** against **3,800 ms** for Playwright's `recordVideo`, and the benchmarked test finished
about **10 s** sooner. A video is
evidence for a human or agent reviewing a run, not an oracle. The README is unsigned, and its author
is inferred from the repository owner.

## Properties as oracles, from a vendor of property testers

[[Geoffrey Huntley - The Answer to AI Is Engineering]] proposes property-based testing as one answer
to the oracle problem above. A property states an invariant, not an expected value: reversing a
string twice returns the original, or "a customer who asks for a refund is only refunded once",
across a whole lifecycle and its microservices. A generator then searches for a counterexample, such
as the Unicode or emoji input a faulty reverser mishandles. **Bombadil** applies this to the
browser. It loads a JavaScript or TypeScript app, rotates, resizes and stresses it until a property
such as "the user always has the ability to log out" holds or fails, and returns a reproduction on
failure. **Hegel** is a Rust core with per-language bindings, described as the successor to
Hypothesis from the same team.

Huntley works at [[Antithesis]], which makes both libraries. He says "ditch Playwright" and adds "I'm
not just talking my book"; treat the recommendation as **vendor advocacy** in a practitioner talk. No
detection rates, bug counts, or comparisons with scripted or example-based tests are given. A property
is still an oracle someone wrote, so the question of who checks the oracle becomes who chose the
properties, and a generator that finds no counterexample is evidence only about the inputs it tried.

## Normal-path agreement is not equivalence

[[Federico Tomassetti - Legacy Modernization with LLMs, Measured]] measures the gap between passing
tests and doing what the original does. Three isolated agent translations of the same five RPG
programs differed in structure but behaved the same on normal inputs: all passed **35** predefined
test cases, and one program agreed on all **102 million** valid inputs. Off the normal path (overflow,
negative values, errors halfway through an update, missing source) each run did something different.
The agent's own tests missed a defect of another kind. Each sequential read had become a query that
scans the whole table, so reading **10,000** records in key order took about **20 seconds** where a
single query needs a hundredth of a second, and the tests ran on a handful of records against an empty
database. Test generation was not cheap either: scenarios for five programs cost **$7.56**, about four
times their translation, and the author calls a five-times test multiplier for a whole application "a
hypothesis, not a rate we measured". With no running original, expected behaviour came from reading
the source, so the oracle problem above arrives with the reference implementation removed.

[[Nikolas Göbel - Informal Verification]] names the distinction. Testing and a track record build
**empirical** trust; understanding why a system behaves correctly builds **epistemic** trust. His
illustration is a marble sorter that seems to sort by colour but sorts by size, which "just happens to
be equivalent under normal operation" until a large blue marble arrives (the interactive version was
not captured). Read against this page, pass^k answers one kind of doubt and not the other. A test that
passes on every run is reliable evidence about the inputs it covers, and no evidence that the
mechanism is the intended one. Göbel's remedy is a checked argument for the property rather than more
runs (see [[AI Code Review]]); he reports no detection rates.

## Fault injection makes the environment the adversary

[[Anjana Ratnayake and Teymour Aldridge - Nightmare Mode - Simulating Disk Failures]] contains no
AI. It is here because it inverts this page's setup: instead of an agent driving software through
its interface, the harness changes what the environment does underneath, and the oracle is the
system's own durability guarantee. [[Antithesis]] first ran a patched LazyFS, the open-source FUSE
filesystem from INESC TEC and Jepsen, then wrote its own, Amnesia, in Rust. It holds unsynced writes
in its own cache, and discarding that cache when the container is killed emulates power loss, which
a process kill does not: after a SIGKILL, completed writes still reach disk, "fsync or no fsync".
Amnesia also returns disk I/O errors, including an EIO on fsync that leaves the failed pages marked
clean so that a later fsync succeeds although the data never reached the disk and is lost at the
next power failure unless the program writes it again (the fsyncgate behaviour), and latency faults
that complete operations out of order or split a write so a concurrent read sees a mix of old and
new data.

Two design choices carry over to any search-based test. Power failures are **correlated with
operations**: the injector decides on each disk syscall whether to fire before, partway through, or
after the operation is applied but before it returns. The authors' reason is that the exact moment of
a power cut before or after an operation does not change the outcome, while the states during one are
short and rare, so tying the fault to the operation shrinks the space the fuzzer explores. And some
defects need compound faults. In bbolt, the storage engine behind etcd, an EIO on the meta page's
fsync made etcd exit, which was correct. On restart bbolt read the unpersisted page back from the
kernel cache, reused pages the on-disk state still referenced, and, once the cached page was evicted,
panicked at every open; the authors say the bug "could only be found by an I/O error followed by a
power failure". This is a first-party vendor post. Beyond "a number of bugs in customer software" and
the one bbolt case, it gives no counts, detection rates, overhead, or validation against real hardware
failures.

## Watching a real user tests what no oracle writes down

[[Jan Miksovsky - Watching Users Is How You Make Products Better]] is an opinion post with no AI
method, and it marks a boundary of this page. Every oracle above checks software against something
someone wrote down: a test, a property, a parity reference, a judge's rubric, a durability guarantee.
Miksovsky's claim is that the most useful test of a product is a real person attempting a real task
while its builder watches. His evidence is his own career: one user's comment on a Web Origami
tutorial ("There are no words you could have written here that would have gotten me to understand
this.") led to "a complete redesign of the language". His method is deliberately cheap: observe people
where they normally use the product and on their own device, say that the product is under test and
not them, ask them to think aloud through a short script of basic tasks, say little, help only when
they are clearly stuck, end on time, pay them, and repeat, because "If multiple people get stuck in
the same place, you've found a real problem."

It sits uneasily with the recording-based evidence above. [[Paul Irish - chrome-capture]] makes
per-test video cheap, and a video is useful evidence for whoever reviews a run, but Miksovsky's point
is about what the builder learns: "reading a report or watching a video clip is nothing like being
there live." He offers no study or sample size and does not discuss whether agent-run usability
sessions or synthetic users could stand in; his only reference to AI is a jab at executives'
"vibecoded apps".

## A Stop hook makes the test suite the definition of done

[[@L1vsun - Prompt, Context, Harness, Loop, Graph - The 5 Levels of AI Engineering]] proposes a Claude
Code Stop hook as the first harness move: `npm test --silent >&2 || exit 2`. Exit code 2 blocks the
stop and sends the error back to the model, so "'done' means the tests pass, not that the model feels
finished". The same check is the first of its four brakes for scheduled loops. The gate is only as
strong as the suite it runs, which is this page's oracle problem, and the post reports no measurements.

## The agent as a defect reporter, and clean rooms for skill tests

[[Uber Engineering - How Uber Evals 1 Million Agent Skill Invocations a Month]] adds two testing
habits from a skill marketplace. First, Uber runs skill evals in three clean rooms: Minion, its
background agent platform; AES, its managed agent sandbox; and devpods, its remote development
machines. "The clean room catches dependencies on the author's laptop": some skills expected
particular file paths, cached documents or OS tooling. Second, an always-on log-papercut skill lets
any agent report friction without being asked: what it tried, what it expected, what happened, and
what would fix it. Agents filed thousands of papercuts in three months, and hundreds have been fixed.
Each report is grouped, triaged, root-caused, fixed, evaluated and approved, and a person acts at
two of those steps. Examples include a shared temp file that let concurrent sessions change each
other's pull requests, and epoch seconds passed where an API expected milliseconds.

Both habits are first-party, and nothing is quantified beyond those counts. The post gives no
defect rates, no false-report rate and no comparison with human-filed bugs. See [[Agent Skill]] and
[[Agent Observability]].

## Open questions

- If the model is kept out of CI, what maintains the suite as the application drifts? The repair loop is
  exactly what the recommendation excludes, and skipped-test behaviour is a reason to want it excluded.
- What drives the 20/40/80 language spread — static typing, framework conventions, or training data volume?
  Nothing in the source separates these, and the answer determines whether the gap closes.
- What is the correct k for pass^k, and who pays for k runs of an expensive agent?
- All three case studies are company blog posts and talks with no controlled comparison; Airbnb's 1.5-year
  baseline is an **estimate**. How much of the speedup is the agent and how much is the forcing function of a
  migration project?
- Should a repair agent ever be permitted to skip a test, or should give-up always escalate to a human?
- Does a skipped test count as appropriate abstention or as unnecessary refusal? ByteByteGo names the
  distinction but nothing says how a suite would classify its own repair agent's give-up events.
- Martin's roughly-95% warning assumes a high baseline means a saturated system. How would a team tell
  that apart from a task distribution that was sampled too easy in the first place?
- Verifier voting suppresses findings that fail to reach a quorum, and suppressed repeated findings are
  never re-raised. Nothing in the Anthropic account measures how many of those were real.
- A known-clean-PR control measures false positives. Neither it nor the daily incident-derived eval set
  measures **recall** — what the reviewer never flagged — and the source offers no controlled comparison
  against conventional human review.
- Capping review at three rounds bounds churn but encodes a judgement that a fourth round is not worth
  it. The source reports no estimate of what the cap lets through.
- GitHub protected its end-to-end tests from agents and REA's Touhou rebuild found a broken
  comparison. How should a suite detect that its own oracle is wrong, and how often is it? None of
  these sources says how the comparison was itself tested.
- When LinkedIn's golden-dataset eval reports, will acceptance and precision agree, and what share of
  accepted comments turn out to be wrong?
- Tomassetti's translations all passed the normal-path tests, one program agreeing on all
  **102 million** valid inputs, and diverged on overflow and mid-update errors. Should a generated
  suite be scored separately on off-path inputs, and who writes those inputs when there is no running
  original?
- pass^k and correlated fault injection both reduce uncertainty about the inputs tried. What would
  show that the mechanism, not just the outcome, is the intended one? Göbel proposes checked
  arguments; no source measures whether they catch what tests miss.
- Nightmare Mode injects faults beneath storage engines. Would the same kind of storage, network, or
  tool faults injected beneath an agent find failures that goal-driven tests do not? Nothing in the
  vault tests it.
- Miksovsky argues from experience that watching people is the most useful exercise; nothing in the
  vault compares what observation finds with what automated tests find.

## Related pages

- [[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]]
- [[Addy Osmani - How the Claude Code Team Does Code Review]]
- [[Sarthak Rastogi - Make Your Coding Assistant a 10x AI Engineer]]
- [[agent-engineer]]
- [[Paolo Perrone - What is Agentic Testing]]
- [[Multi-Turn Evaluation]]
- [[LLM-as-a-Judge]]
- [[Benchmark Optimization]]
- [[AI-Native Software Development Lifecycle]]
- [[Coding Agent Harness]]
- [[Agent Security and Governance]]
- [[Self-Replicating Agents]]
- [[Context Engineering]]
- [[Agentic Loop]]
- [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]]
- [[Tool Roster Economics]]
- [[GitHub - How We Make AI Coding More Cost Efficient]]
- [[GitHub]]
- [[Ayo Adedeji - Agents That Prove, Not Guess]]
- [[Lance Martin - Automating Eval Design and Hillclimbing with Claude]]
- [[ByteByteGo - Why Do LLMs Lie]]
- [[ByteByteGo]]
- [[Anthropic]]
- [[Harness Optimization]]
- [[X Engineering - Rebuilding the Global Town Square from Scratch]]
- [[Legacy Code Modernization with AI Agents]]
- [[ByteByteGo - How LinkedIn Uses AI to Review 40,000 Pull Requests a Week]]
- [[ByteByteGo - How GitHub Used AI to Port Copilot From TypeScript to Rust in Record Time]]
- [[@0xCodila - Reverse Engineering with REA and Opus 5.5 (Full Course)]]
- [[Paul Irish - chrome-capture]]
- [[AI Code Review]]
- [[Geoffrey Huntley - The Answer to AI Is Engineering]]
- [[Inference Determinism]]
- [[Federico Tomassetti - Legacy Modernization with LLMs, Measured]]
- [[Nikolas Göbel - Informal Verification]]
- [[Anjana Ratnayake and Teymour Aldridge - Nightmare Mode - Simulating Disk Failures]]
- [[Jan Miksovsky - Watching Users Is How You Make Products Better]]
- [[Antithesis]]
- [[@L1vsun - Prompt, Context, Harness, Loop, Graph - The 5 Levels of AI Engineering]]
- [[Uber Engineering - How Uber Evals 1 Million Agent Skill Invocations a Month]]
- [[Agent Skill]]
