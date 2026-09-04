import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _integrate import integrate

HP = "src-2026-09-02-can-boluk-harness-playbook"
GH = "src-2026-09-03-github-ai-coding-cost-efficient"

integrate(
    "Agentic Testing", [GH],
    "Prompt behaviour is untested surface",
    """
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
""",
    ["Tool Roster Economics", "GitHub - How We Make AI Coding More Cost Efficient", "GitHub"],
)

integrate(
    "Benchmark Optimization", [GH],
    "When the metric is cost, the local-versus-global gap is measurable",
    """
This page's recurring theme — that a number can improve while the thing it stands for does not — has its cleanest
non-capability instance in [[GitHub - How We Make AI Coding More Cost Efficient]]. An output compressor optimised
the per-response token count, the metric it was built to move, and **total cost went up**, because agents
reopened files and re-ran commands to recover what had been compressed away: *"We saved tokens locally and spent
more globally."*

This is the same failure as benchmark overfitting with the incentive inverted. Nobody was gaming anything; the
metric was simply local to a component while the cost was global to the loop. The correction was not a better
compressor but a **narrower mandate** — preserve source-like output, reorganise search results losslessly, and
compress only repetitive build noise — arrived at because *"that is what the evaluations supported"* rather than
because conservatism was the goal.

Two further disciplines from the same source belong on this page's list of what makes a number reportable. The
four shipped wins (**3.1%, 5.5%, 2.9%, 2.3%** on an AI-credit metric) are published with an explicit statement
that **they are not additive**, which is the caveat most likely to be dropped when a result is quoted. And the
same change measured on two products gave **opposite signs** — a file-tool migration cut code-review cost by
about 20% and raised CLI cost — establishing that the workload is part of the result, not context for it.
""",
    ["Tool Roster Economics", "GitHub - How We Make AI Coding More Cost Efficient", "GitHub"],
)

integrate(
    "Small Language Models", [HP],
    "Small models as harness infrastructure",
    """
[[Can Bölük - The Harness Playbook]] describes a deployment role for small models that is neither on-device
assistance nor cost-reduced chat: **small local models as harness plumbing.** Session titles, message
classification, and text-to-speech are jobs a harness performs constantly, none require frontier capability, and
each currently costs a provider roundtrip. Running them on a small local model (LiquidAI's are named) removes
latency and cost from paths the user never thinks of as inference.

The framing matters because it decouples the small-model case from capability arguments entirely. The question is
not whether a small model can do the task as well as a large one — it is whether the task ever needed a large
model, and whether a roundtrip is an acceptable price for something that decorates a UI. See
[[Tool Roster Economics]] for the same logic applied to tools rather than models.
""",
    ["Tool Roster Economics", "Harness State Authority", "Can Bölük - The Harness Playbook", "Can Bölük"],
)
