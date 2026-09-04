import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _integrate import integrate

M = "src-2026-09-02-meta-organizational-second-brain"

integrate(
    "Retrieval-Augmented Generation", [M],
    "A criterion for what should not be retrieved",
    """
[[Meta - An Organizational Second Brain]] supplies something this page has lacked: **a rule for deciding what
belongs in a retrieval corpus at all.** In that deployment the split between a curated knowledge wiki and a RAG
corpus is made by **information density and expected usage frequency** — dense, frequently needed material is
promoted into curated files the agent reads directly; sparse or rarely consulted material stays in retrieval.
That reframes RAG as the tier for the long tail rather than as the default substrate for everything.

The routing layer is the more pointed departure. Navigation from a question's shape to the relevant files uses
**deterministic routing indexes, explicitly not embedding similarity**. The justification is verifiability: a
declared route can be checked mechanically for dangling references, file-size violations, identifier collisions,
and dependency cycles, and a nearest-neighbour result cannot be checked at all. Where correctness must be
auditable — the deployment is a compliance agent — similarity search is not merely less precise, it is
untestable.

Reported effect of the promoted tier plus progressive disclosure: roughly **80% fewer tokens per turn**. The
figure is unattributed across several simultaneous changes, so treat it as a direction rather than a coefficient.

This connects to the storage-versus-structure limit already recorded on this page. Retrieval can hold arbitrary
volume; what it cannot hold is a stance. A position file that states an organisation's decision on a question is
not a chunk to be found by similarity, because there is nothing similar to it — it is the answer. See
[[Institutional Knowledge Agents]].
""",
    ["Institutional Knowledge Agents", "Meta - An Organizational Second Brain", "Meta",
     "Schema-Driven Knowledge Base", "Persistent Wiki"],
)

integrate(
    "Agent Memory", [M],
    "Memory as a compiled, reviewable artifact",
    """
[[Meta - An Organizational Second Brain]] describes a memory system whose defining property is that **every
update is a text diff a domain expert can review in 30 seconds.** The agent's durable knowledge is 200+ structured
files — position files, taxonomies, routing indexes, gateway files — and improvement happens by compiling expert
feedback into those files rather than by writing embeddings, appending to a scratchpad, or retraining.

Two design rules distinguish it from the memory architectures already on this page.

**Memory is typed, and the types are enforced.** *Recipes* hold procedures and no domain facts; *knowledge files*
hold declarative positions and no procedures. The purpose is failure attribution: when the agent is wrong, the
type tells you whether the procedure or the knowledge is at fault. Undifferentiated memory stores cannot make
that distinction, which is why their failures are hard to fix rather than merely hard to detect.

**Memory declares its own dependency graph.** Each file names `depends_on` and `referenced_by` in frontmatter, so
the consequences of an edit are a lookup rather than an investigation — and so a deterministic linter can reject
dangling references and dependency cycles before anything is served.

The retrieval boundary is drawn by **information density and expected usage frequency**: dense, frequently needed
material is promoted into curated memory; the rest stays in a retrieval corpus. Loading that memory by
progressive disclosure rather than in full is reported to cut **tokens per turn by about 80%**.

The costs are the usual ones for curated memory, and the source does not hide them: the compile-validate-review
loop is ongoing human and machine expense, and the reported outcomes after three sprints are qualitative with no
denominators. See [[Institutional Knowledge Agents]].
""",
    ["Institutional Knowledge Agents", "Meta - An Organizational Second Brain", "Meta",
     "Schema-Driven Knowledge Base"],
)

integrate(
    "Continual Learning for Agents", [M],
    "Learning with the weights frozen",
    """
Every mechanism on this page so far updates parameters. [[Meta - An Organizational Second Brain]] reports a
deployed agent that improved over three two-week sprints **with no model retraining at all** — the update surface
is 200+ text files, and learning means compiling expert feedback into them under regression tests.

The trade is explicit and worth stating as such. Weight updates can absorb signal no one can articulate; text
updates cannot. In exchange, text updates are **diffable, attributable, revertible, and reviewable by the domain
expert whose judgement is being encoded** — none of which a gradient step offers. For a compliance domain, where
the value being captured is precisely a set of articulable positions, that trade is favourable. For domains whose
expertise is tacit, it may not be.

The loop also answers the question this page leaves open about *which part of an agent should learn*. Meta's
answer is a typed one: procedures are learned as recipes, facts as knowledge files, and the diagnosis step routes
each failure to one or the other by asking **"could the agent have reached the correct conclusion from its source
materials?"** A yes means the procedure is wrong; a no means knowledge is missing; expert disagreement means the
position itself is undecided. That is a more precise localisation than a gradient update, which distributes the
correction everywhere.

The safety architecture this page describes has a direct counterpart: deterministic linting, blind regression
replay where neither agent nor judge knows what changed, and independent adversarial review of the diffs. The
reported "zero regressions" should be read against the fact that the suite is written by the same loop it
validates. See [[Institutional Knowledge Agents]].
""",
    ["Institutional Knowledge Agents", "Meta - An Organizational Second Brain", "Meta",
     "Agent Memory", "LLM-as-a-Judge"],
)

integrate(
    "Recursive Self-Improvement", [M],
    "A self-improvement loop with the model held fixed",
    """
[[Meta - An Organizational Second Brain]] is a useful boundary case for this page: a genuine improvement loop in
which **the model never changes.** Over three two-week sprints, the only thing that improved was a body of 200+
text files, compiled from expert feedback under regression tests. It supports this page's existing position that
parameters and scaffold are separate update surfaces, by showing the scaffold surface moving alone.

What makes it more than an anecdote is that the loop is defended at every stage, and each defence targets a
failure mode this page has recorded elsewhere:

- **Against misattributed fixes:** diagnosis asks *"could the agent have reached the correct conclusion from its
  source materials?"* — separating a broken procedure from missing knowledge from an organisational position
  nobody has actually decided.
- **Against self-serving justification:** an **independent adversarial reviewer** sees only the diffs, with no
  knowledge of the rationale, and argues against them. Withholding the story is the mechanism.
- **Against silent capability trades:** every fix becomes a permanent regression test, and validation replay is
  **blind on both sides** — the agent does not know it is being tested, the judge does not know what changed.
- **Against unverifiable structure:** a deterministic linter that passes or fails on dangling references,
  file-size budgets, identifier collisions, and dependency cycles.

The honest reading of the results is that they do not yet demonstrate much. "Useful almost all the time," "days
to minutes," and **"zero regressions"** are qualitative, without baselines, task counts, or comparison against
fine-tuning on the same workload — and the zero-regression claim is measured by a suite the loop itself wrote. As
evidence of a *design* for constrained self-improvement it is valuable; as evidence of *effectiveness* it is not
yet decisive. See [[Institutional Knowledge Agents]].
""",
    ["Institutional Knowledge Agents", "Meta - An Organizational Second Brain", "Meta",
     "Continual Learning for Agents", "LLM-as-a-Judge"],
)

integrate(
    "LLM-as-a-Judge", [M],
    "Blind on both sides, and a second judge that argues against",
    """
[[Meta - An Organizational Second Brain]] contributes two protocol details that sharpen how a judge is deployed
inside a maintenance loop, rather than how a judge is built.

**Targeted replay is blind on both sides.** When a knowledge change is validated, the agent under test does not
know it is being tested, and the judge does not know what changed. Both halves are load-bearing. An agent aware
of evaluation is a different agent; a judge told what changed will look for its effect and find it. This is a
stricter protocol than the production judging arrangements already on this page, most of which score outputs
whose provenance the judge can see.

**A second agent judges the diff adversarially.** Independent review is performed by an agent given **only the
diffs and no knowledge of the rationale**, with the explicit task of arguing against the change. Withholding the
motivating story is the design: a reviewer who knows why a change was made tends to reconstruct its
justification. This is a judge used as an opponent rather than as a scorer, and it is a role this page has not
previously recorded.

Sitting underneath both is a division of labour worth preserving: the **deterministic linter runs first** —
dangling cross-references, file-size budgets, identifier collisions, dependency cycles, *"not probabilistic, it
passes or fails"* — and only what it cannot decide reaches a model judge. Given this page's finding that a
judge's noise floor bounds what an experiment can detect, moving every mechanically checkable property out of the
judge's remit is the cheapest available precision gain.
""",
    ["Institutional Knowledge Agents", "Meta - An Organizational Second Brain", "Meta",
     "Recursive Self-Improvement", "Agentic Testing"],
)
