import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _integrate import integrate

M = "src-2026-09-02-meta-organizational-second-brain"

integrate(
    "Schema-Driven Knowledge Base", [M],
    "An industrial instance, and three rules this schema does not have",
    """
[[Meta - An Organizational Second Brain]] is the first source in this vault describing a **schema-driven
knowledge base built by someone else, in production, for a different purpose** — a compliance-domain expert agent
over 200+ files. The convergence is close enough to be useful as a comparison: declared frontmatter, typed page
kinds, an explicit routing layer, and a maintenance pass that checks the graph rather than reading it.

Three of its rules are stronger than anything in this vault's schema.

**Declared bidirectional dependencies.** Every file names both `depends_on` and `referenced_by`. The redundancy
is deliberate: it converts "did this edit break something?" from a search into a lookup. This vault's schema
declares `source_ids` but leaves page-to-page dependency implicit in wikilinks, which is why its link checking is
a whole-vault scan rather than a local query.

**A hard separation between procedures and facts.** *Recipes* are imperative and contain no domain facts;
*knowledge files* are declarative positions and contain no procedures. The payoff is attribution — a wrong answer
is a recipe bug or a knowledge gap, and you can tell which. This vault's schema mixes the two: `CLAUDE.md` holds
workflows, and concept pages hold claims, but nothing forbids a concept page from encoding procedure.

**A deterministic linter with pass/fail semantics.** Its checks are dangling cross-references, file-size budgets,
identifier collisions, and dependency cycles — *"not probabilistic. It passes or fails."* This vault's lint pass
has grown ten mechanical checks along the same lines, but as an ad-hoc script rather than a schema-declared
contract, which is why each pass re-derives its own exclusions.

The stated design principle is the same one this schema exists to serve, and worth recording in its author's
words: **"Keep the complexity in text files, not in model weights or opaque embeddings. Every improvement is a
text edit a domain expert can review in 30 seconds."**
""",
    ["Institutional Knowledge Agents", "Meta - An Organizational Second Brain", "Meta",
     "Retrieval-Augmented Generation", "Agent Memory"],
)

integrate(
    "Persistent Wiki", [M],
    "What belongs in the wiki, and what stays in retrieval",
    """
This page has assumed the wiki is the right home for synthesis without saying what should *not* live there.
[[Meta - An Organizational Second Brain]] supplies a criterion from a production deployment: **split wiki from
retrieval by information density and expected usage frequency.** Dense material that is needed often becomes a
curated file the agent reads directly; sparse or rarely needed material stays in a retrieval corpus. That is a
resource-allocation rule rather than an architectural preference, and it makes the boundary decidable per topic
instead of per system.

The same source gives the wiki-as-context approach its first reported magnitude. Routing an agent through gateway
files and indexes rather than loading a fixed context — **progressive disclosure** — cut tokens per turn by
roughly **80%**. A curated wiki is not only better organised than a corpus; at that ratio it is materially
cheaper to consult.

It also shifts who the wiki is for. In that deployment the primary reader is an agent, and the file structure is
shaped by what an agent needs to traverse: gateway files that orient before descending, taxonomy files that fix
vocabulary, position files that each answer one question. This vault's pages are still shaped for a human reader
who happens to be assisted by a model. Whether those two audiences want the same page granularity is now an open
question with evidence on one side.

The convergence is worth noting for what it is: an independent team, a different domain, no shared code, and the
same shape. See [[Institutional Knowledge Agents]].
""",
    ["Institutional Knowledge Agents", "Meta - An Organizational Second Brain", "Meta",
     "Retrieval-Augmented Generation", "Context Engineering"],
)

integrate(
    "Index and Log", [M],
    "Deterministic routing, and the log as a regression suite",
    """
[[Meta - An Organizational Second Brain]] independently arrives at both halves of this page and pushes each one
further.

**Routing indexes are deterministic, not similarity-based.** In that deployment, the path from a question's shape
to the relevant files is a lookup structure, explicitly not an embedding neighbourhood. This is the design choice
that makes mechanical checking possible at all: a declared route can be tested for dangling references, and a
nearest-neighbour result cannot. It is the same reason this vault's `index.md` is a written catalog rather than a
generated one, but the argument here is sharper — determinism is not a stylistic preference, it is the
precondition for the linter.

**The change record can be more than chronology.** This vault's `log.md` preserves what happened. In Meta's loop
every fix is **folded back into a regression suite**, so the record of past failures is executable: it prevents
the loop from silently trading an old capability for a new one. That is the capability this page's log does not
have — it can tell you when a claim was added, but nothing replays whether the claim still holds.

Alongside it sits a validation practice worth naming: **targeted replay is blind.** The agent does not know it is
being tested, and the judge does not know what changed. Both halves matter, and both are absent from a purely
chronological log.
""",
    ["Institutional Knowledge Agents", "Meta - An Organizational Second Brain", "Meta", "LLM-as-a-Judge"],
)

integrate(
    "Ingest Query Lint Loop", [M],
    "Maintenance as compilation",
    """
[[Meta - An Organizational Second Brain]] describes the same loop from an industrial deployment and frames it
differently: **maintenance is a compilation problem.** Expert feedback is the source language, the knowledge base
is the target, and the pipeline has four staged steps — diagnose, compile, validate, expert review — each with a
specific defence.

**Diagnosis needs the right question, and the obvious one fails.** Classifying failures by conversational form
did not work. The test that did: **"Could the agent have reached the correct conclusion from its source
materials?"** If yes and it erred, the procedure is wrong. If no, knowledge is missing. If the experts disagree
with each other, the underlying position is ambiguous and the fix is a decision, not an edit. That third branch
is the one this vault's lint pass has no vocabulary for — it records contradictions but cannot distinguish a
contradiction between sources from an unmade decision.

**Compilation is reviewed adversarially.** A second agent sees only the diffs, with no knowledge of the rationale
that motivated them, and argues against the change. Withholding the story is the point: a reviewer who knows why
a change was made will reconstruct its justification.

**Validation is two-layered**: a deterministic linter that passes or fails (dangling cross-references, file-size
budgets, identifier collisions, dependency cycles), then blind regression replay where the agent does not know it
is under test and the judge does not know what changed.

Read against this vault's loop, the gaps are specific. Ingest and lint exist here; **compile** is implicit,
**adversarial review** is absent, and **regression replay** has no analogue at all — this vault's lint checks
structure but never re-asks a question it previously answered. The reported outcome ("zero regressions" over
three sprints) also carries its own caveat: it is measured by a suite the same loop wrote, so a failure the
diagnosis step never characterised would not be in it.
""",
    ["Institutional Knowledge Agents", "Meta - An Organizational Second Brain", "Meta",
     "LLM-as-a-Judge", "Recursive Self-Improvement"],
)

integrate(
    "Andrej Karpathy", [M],
    "The LLM Wiki idea, built at industrial scale",
    """
[[Meta - An Organizational Second Brain]] explicitly cites Karpathy's **LLM Wiki** proposal as prior art,
alongside Google's Open Knowledge Format, for a production deployment of 200+ structured knowledge files backing
a compliance-domain expert agent. This vault is itself an instance of the same proposal, so the citation is the
first outside evidence that the idea generalises past a personal knowledge base into an organisational one.

What the industrial version adds to Karpathy's sketch is the maintenance machinery: bidirectional
`depends_on`/`referenced_by` declarations, deterministic routing indexes rather than embedding similarity, a
pass/fail linter, and blind regression replay — plus the claim that the whole thing improves **without model
retraining**, which is the strongest form of Karpathy's original argument that the knowledge belongs in text
rather than in weights. See [[Institutional Knowledge Agents]].
""",
    ["Institutional Knowledge Agents", "Meta - An Organizational Second Brain", "Meta"],
)
