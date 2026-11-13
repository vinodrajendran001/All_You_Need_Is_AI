---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-06-psi-aaronson-ambainis-proof
source_title: A proof of the Aaronson-Ambainis conjecture
source_author: PSI Research
source_url: https://psi.inc/research/aaronson-ambainis/
tags:
  - source/summary
  - mathematics
  - automated-research
  - formal-verification
source_ids:
  - src-2026-11-06-psi-aaronson-ambainis-proof
status: active
---

# A Proof of the Aaronson-Ambainis Conjecture

## Summary

Physical Superintelligence (PSI) announces that a research system it built in-house, using instances
of a non-public Anthropic model, found a proof of the Aaronson-Ambainis conjecture. The conjecture has
been open since 2008 and concerns whether quantum computers can be exponentially faster than ordinary
computers on random inputs. PSI says the system had a complete proof during the third day of the run,
that the Lean proof assistant accepted it, and that the system later improved the result twice, with
Lean accepting the final version. If the result holds, quantum computers are at most polynomially
faster on yes-or-no questions about random inputs. The post names the human contributors: one staff
member scoped the problem, ran the system, prompted the model to draft the paper, reviewed it, and
is responsible for its correctness, and two advisors audited the proof and the formalization. The
announcement is first-party. The Stanford researchers who proved a special case in August 2026 are
reading the proof and praise it, but the capture records no completed peer review.

## Key claims

### What was found, and how it was checked

- PSI says the system ran on its own infrastructure, had a complete proof "during the third day of the
  run", and that Lean, "a proof assistant in which a computer checks every step", accepted it.
- PSI then set the system on related open problems. "Along the way, the system improved the result
  twice, and Lean accepted the final version."
- The post does not describe the system's architecture, which Anthropic model it used, how many
  instances ran, or how much compute the run took.

### The human role

- **David Turturean** (Member of Technical Staff) led the work. He developed the research system,
  scoped the problem and ran the system on it, prompted the model to package the results into a first
  draft of the paper, reviewed the draft, and "is responsible for the paper's correctness".
- **Jim Halverson** (Advisor) audited the proof. **Phiala Shanahan** (Advisor) commented on the Lean
  formalization.

### Outside reaction so far

- In August 2026, Guy Blanc, Jordan Docter, Carmen Strassle, and Li-Yang Tan of Stanford settled a
  special case: no exponential speedup on random inputs for quantum algorithms that read their input in
  a fixed number of parallel rounds.
- PSI says they have been reading the full proof, have sent comments, and are writing a shorter
  exposition for experts. Their quoted assessment: "This is a huge result... Everything is brought
  together in a rather magical way."

### The mathematics, as stated

- Building on Beals, Buhrman, Cleve, Mosca, and de Wolf, a quantum algorithm's acceptance probability
  after **T** queries is a polynomial of degree at most **2T** with values between 0 and 1. Aaronson and
  Ambainis showed that if every such bounded low-degree polynomial has an influential variable, an
  ordinary computer can imitate the quantum one with few queries on most inputs.
- PSI's bound: if the polynomial is not constant, some bit i has
  **Inf_i(f) ≥ c·v^(5/2)/d^6 ≥ (v/d)^7**, where v is the variance, d the degree, and
  **c = 8√15/(125π^4), about 0.0025**. Earlier bounds for general polynomials decayed exponentially in
  the degree.
- Consequence: the number of classical queries needed grows at most like a fixed power of T, for any
  fixed error and fraction of inputs, rather than exponentially.
- Method: the proof follows a plan of Shachar Lovett and Jiapeng Zhang, replacing the inequality they
  left as a conjecture with a new inequality proved in the manuscript. The new inequality uses a
  one-to-one pairing of input settings produced by a determinant. David Reimer's Butterfly Lemma
  already gives a weaker pairing; the new one also limits how often paired settings agree on each bit.
  It also uses results of Agarwal and Ben-David, Kulkarni and Tal, and Filmus, Hatami, Keller, and
  Lifshitz.

## Why it matters

[[AI for Mathematical Discovery]] gains its clearest case: a named open conjecture, a machine-checked
proof, and a stated division of human labor. It contrasts with the vault's Navier-Stokes account,
which had no formal acceptance. [[Automated AI Research]] gains an example outside AI R&D where the
system did the search but a human chose the problem, ran the system, and took responsibility for
correctness. That pattern matches the page's execution-versus-taste distinction. [[Anthropic]]
gains a record of a non-public model of its own being used by an outside lab for frontier
mathematics.

## Tensions / open questions

- **First-party and preliminary.** The announcement comes from the organization that built the system.
  The capture does not link the manuscript or the Lean code, and records no journal or completed peer
  review. The Stanford group's comments and praise are reported by PSI, and their exposition is still
  being written.
- **What Lean verified is not shown.** A Lean check guarantees the formal proof matches the formal
  statement. The capture does not show the Lean statement, so it cannot confirm that the formal
  statement matches the conjecture as mathematicians state it. Shanahan's comments on the formalization
  are mentioned but not described.
- **The AI contribution is not measured.** The post does not say how much human guidance was given
  during the run, whether earlier runs failed, or which model it was. So it cannot support claims about
  how general the system is.
- **No personal byline.** The capture is attributed to "PSI Research" with no individual author at
  the top; the contributions section names three people.
- An inline interactive figure (an SVG of bit influences) was skipped. Its example polynomial is stated
  in prose but adds nothing to the claims.

## Affected pages

- [[AI for Mathematical Discovery]]
- [[Automated AI Research]]
- [[Anthropic]]

## Raw capture

- [[knowledge-base/raw/sources/A proof of the Aaronson-Ambainis conjecture]]

## Citations

- Canonical URL: <https://psi.inc/research/aaronson-ambainis/> (the capture's URL carried a
  `utm_source=tldrai` parameter, removed here).
- Attributed to PSI Research (Physical Superintelligence); no personal byline at the top. Published
  November 6, 2026; captured November 10, 2026. The contributions section names David Turturean,
  Jim Halverson, and Phiala Shanahan.

## Related pages

- [[AI for Mathematical Discovery]]
- [[Automated AI Research]]
- [[Anthropic]]
- [[Recursive Self-Improvement]]
- [[Test-Time Scaling]]
- [[Ethan Mollick - The Dot and the Swarm]]
- [[Ramez Naam - Can a Million AI Agents Create Superintelligence]]
- [[James Tillman - Two Kinds of Test-Time Scaling]]
- [[Ethan Mollick - Fable 5.2 and Jagged AGI]]
