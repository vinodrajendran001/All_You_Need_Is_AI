---
type: source-summary
created: 2026-10-16
updated: 2026-10-16
source_id: src-2026-09-30-apollo-embedded-evaluations
source_title: Principles for Embedded Evaluations
source_author: Apollo Research
source_url: https://www.apolloresearch.ai/blog/principles-for-embedded-evaluations
tags: [source/summary, governance, evaluation, monitoring, assurance]
source_ids: [src-2026-09-30-apollo-embedded-evaluations]
status: active
---

# Apollo Research - Principles for Embedded Evaluations

## Summary

Apollo Research proposes ongoing, claim-based assessments by evaluators with deep access to
frontier developers' training and internal deployment. The scope is loss-of-control risk from
scheming. The proposed product is a public, qualified verdict on each predeclared claim,
not an undifferentiated "safe company" label.

This is an institutional governance proposal, not a completed evaluation, a demonstrated
incentive mechanism, or a legal requirement already in force.

## Key claims

Four criteria organize the proposal: **reduce risk, inform the public, provide good incentives,
and be fair to both sides**. Necessary means include persistent access, sufficient people and
compute, early visibility into training changes, independent funding/renewal arrangements,
protected confidential information, and rules for disagreement agreed in advance.

**Two sources of claims:** a shared standard set prevents developers from choosing only easy
tests; recommended claims address particular commitments, incidents, and emerging risks.
Recommended-but-unadopted claims should remain visible in the public report.

**Three assessment stages:**

1. Review the developer's existing evidence and its own view of counterexamples.
2. Independently gather evidence, including after a developer reports a problem.
3. If neither finds a counterexample, test whether the methods would have found one.

The third step changes the meaning of an empty incident log. For a monitoring claim, test
realistic planted attempts and coverage, rather than treating "no alerts" as adequate evidence.

| Proposed grade | Verdict | Meaning |
| --- | --- | --- |
| A | Verified | No counterexample found; methods would likely have detected one, subject to scientific uncertainty |
| B | Unrefuted | No counterexample found, but material gaps remain in detection or evidence |
| C | Self-reported | The developer supplied evidence contradicting its claim |
| D | Evaluator-found | The evaluator found a counterexample beyond what the developer disclosed |
| E | Blocked | Access was insufficient to meaningfully try to falsify the claim |

The ordering is designed to reward access and self-reporting. It is **not a risk-severity scale**:
a self-reported incident can be severe, and a blocked assessment is not proof of a particular
unsafe behavior. Reports separately state confidence, gaps, counterexample severity, and effort.

A refuted claim remains refuted. A narrower post-remediation fallback claim gets a separate
assessment; both claims and verdicts remain public.

Public reports should include scope, requested/granted/denied access, outstanding information,
evidence, verdicts, and recommended claims. They publish on an agreed schedule even if important
requests remain outstanding. Redactions should identify the kind and importance of withheld
information, without suppressing the overall conclusion. A developer may publish a rebuttal
but should not veto the evaluator's conclusion.

Serious findings receive expedited disclosure under pre-agreed rules, with the most serious
cases going directly to appropriate authorities. The proposal favors eventual legal requirements;
voluntary commitments, boards, customers, and insurers are interim levers.

## Why it matters

[[Embedded Evaluation]] extends the vault's verifier-independence principle beyond a grader
process into access, incentives, publication rights, and time. It also puts the retrospective
monitoring claims in [[OpenAI - The Hugging Face Incident and the Road Ahead]] into an assurance
framework: assess coverage and sensitivity before interpreting a quiet monitor.

## Tensions / open questions

- "Verified" is deliberately qualified, not a proof that a universal safety claim is true.
  Current scientific methods may not support high-certainty assurances.
- The evaluator still depends on the developer for evidence and access. The incentive argument
  assumes the developer values favorable verdicts; the authors do not claim resistance to a
  determined party gaming the process.
- Employee-like access without sufficient resources or publication rights can create safety
  washing rather than assurance.
- Broad negative claims need explicit scope and observation periods. Detection sensitivity,
  unmonitored activity, new architectures, and changing training methods remain uncertainties.

## Affected pages

- [[Embedded Evaluation]]
- [[Agent Security and Governance]]
- [[Chain-of-Thought Monitoring]]
- [[Benchmark Optimization]]
- [[Apollo Research]]

## Raw capture

- [[Principles for Embedded Evaluations]]

## Citations

- Canonical article: <https://www.apolloresearch.ai/blog/principles-for-embedded-evaluations>
- The public page's **September 30, 2026** publication date was recovered on October 16.
  The clipping was captured October 12 and leaves author/publication fields blank.
- Institutional attribution is to Apollo Research; no individual byline was recovered.
  The original capture is preserved without metadata edits.

## Related pages

- [[Embedded Evaluation]]
- [[Apollo Research]]
- [[Agent Security and Governance]]
- [[Chain-of-Thought Monitoring]]
- [[Benchmark Optimization]]
- [[OpenAI - The Hugging Face Incident and the Road Ahead]]
