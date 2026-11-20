---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-18-pueyo-hardware-is-software
source_title: "Hardware Is Software"
source_author: "Tomas Pueyo"
source_url: "https://unchartedterritories.tomaspueyo.com/p/hardware-is-software"
tags:
  - source/summary
  - hardware
  - manufacturing
  - accelerators
  - forecasting
  - opinion
source_ids:
  - src-2026-11-18-pueyo-hardware-is-software
status: active
---

# Tomas Pueyo - Hardware Is Software

## Summary

An **opinion and forecasting essay** from Tomas Pueyo's newsletter *Uncharted Territories*. The
subtitle is "What happens when silicon gods gobble up atoms too". His argument is that AI will make
hardware engineering behave like software engineering, then remove most human cost from
manufacturing. In his view this cuts prices across whole value chains, shifts cost toward raw
materials, energy and capital, and destroys many manufacturing jobs. The evidence is a chain of quoted
claims: a CEO's post, a 2022 NASA paper, a founder's side project, and an X post predicting NVIDIA's
moat is gone. To these he adds his own back-of-envelope arithmetic. He discloses investments in two
of the companies he cites, and points readers to upcoming articles on humanoid robots and on mining
(the mining one labelled premium).

## Key claims

### Hardware design is calculation (first-party CEO claim)

Pueyo quotes Blake Scholl, founder and CEO of Boom Supersonic: "Most hardware engineering is actually
software engineering in disguise", done in spreadsheets "with the software sophistication of a script
kiddie". Boom's rule is "don't design the hardware, design the \*algorithm\* for designing the
hardware." Scholl claims "a turbomachinery design tool that lets one engineer do in realtime what
previously took 100 engineers six months". He says another tool "auto-generates 65% of entire aircraft
structure", and cites "A boomless supersonic airplane built by 50. A full scale supersonic turbine made
by 150." These are **unverified first-party statements**. Pueyo footnotes Boom: "I'm a very tiny
investor."

Pueyo then says "NASA proved this is the case". He describes a 2022 paper in which AI-designed parts
were "40% cheaper, 66% lighter, 85% faster to design, and more robust" than expert-designed parts. The
paper was not read during ingest.

### Hardware design by a general model (anecdote and prediction)

Casey Handmer, founder of Terraform ("I'm an investor"), reportedly asked Claude to "Design a printed
circuit board that can use radar to detect my heart rate". Pueyo says Claude produced the circuit,
layout, firmware and software. His statement that Handmer "got it back for a couple hundred bucks" is
introduced with "I assume". Handmer's description of the device: "It can tell if I'm speaking but not
what I'm saying."

Pueyo then quotes a Handmer prediction, made "after Jensen Huang stepped down from NVIDIA": "GPU
design and CUDA were insurmountable moats 12 months ago, now a Fable-class model can independently
rebuild both for <$1m token spend." (Pueyo's bracketed glosses are omitted.) Pueyo adds that NVIDIA designs but does not fabricate its GPUs. He
also notes that Google used AI for chip design (AlphaChip) to build its TPUs. "Now, everybody can do
it." The leadership change and the <$1m figure are both **unverified** in this vault.

### From R&D to the whole value chain (author's arithmetic)

- R&D is "~ 5-20%" of a manufacturing company's revenue, depending on industry. Pueyo argues AI will
  eliminate it and go beyond it, into requirements, documentation, certification and qualification.
- Solar costs fell "12% per year" for 50 years. At 20% a year the same point would have arrived "20
  years earlier", and at 30% a year "32 years earlier".
- **Idiot Index:** Musk found raw materials were "2%" of a rocket's price. Falcon Heavy "reduced costs
  by 98%" and Starship "will further reduce costs by 93%, for a total of ~99.9%" (forward-looking).
- Human labour is "25%" of manufacturing costs in section 5 and "~26%" in section 6. The rest of the
  budget is parts and materials (~62%), machinery (~3%), energy (~1.8%), maintenance (~1.5%), and land
  (~1.4%).
- He removes the human share and assumes parts fall by 12 percentage points, reaching "~37%" per firm.
  He says competition passes this into prices. Suppliers do the same, and "If you push this across the
  entire value chain, you end up with a total cost reduction of 74%!" "The remaining 25%" is raw
  materials, energy and residual human work.
- Takeaways: AI cuts "~20%-25% of human costs in every step", adding up to "~65-75% of all the costs
  across the value chain". Blue-collar automation follows humanoid robots, which he expects "in the
  next 2-5 years". He forecasts "an absolute carnage in the blue- and white-collar manufacturing
  jobs".
- Two schools of thought give "5-20 years" (slow adoption, physical testing) or "the next 1-4 years"
  (AI labs or private equity running factories) for the transition.

## Why it matters

The essay is a strong statement of a claim the vault can test against measured externalization costs.
[[Accelerator Software Externalization]] records what it actually took to make TPUs usable from
PyTorch: an itemized framework bill, a 4.1x hand-tuning gap after the port, and first-party coverage
figures. Handmer's "<$1m token spend" to rebuild GPU design and CUDA is a prediction with no stated
pass criterion, set against that evidence. For [[NVIDIA]], it is a direct challenge to the
documentation-and-software moat the entity page describes, from a secondhand X post.

## Tensions / open questions

- **Internal inconsistencies.** Labour is "25%" in one place and "~26%" in another. The takeaways say
  "~20%-25%" of human costs per step. The value-chain total is "74%" in the body and "~65-75%" in the
  takeaways. The step from 37% per firm to 74% across the chain is not shown. It matches about three
  compounded tiers (1 − 0.63³ ≈ 0.75), but that is this summary's inference, not the author's.
- Takeaway 2 says "employment in these companies will growth", while takeaway 8 predicts job
  "carnage" and says sales growth is unlikely to outweigh "the job destruction". The first may be a
  garbled sentence about capital cost. It is recorded as written.
- "NASA proved this is the case" generalises from one 2022 parts-design paper to manufacturing as a
  whole.
- Financial interests: Pueyo invests in Boom and Terraform, the two companies whose results anchor
  sections 1 and 2. He also says his mining research changed his investments.
- A one-off hobby PCB says little about certifiable, high-volume hardware. Physical testing, which
  his own "first school" cites, is outside the AI-speed argument.

## Affected pages

- [[Accelerator Software Externalization]]
- [[NVIDIA]]

## Raw capture

- [[knowledge-base/raw/sources/Hardware Is Software]]

## Citations

- Raw capture: Tomas Pueyo, "Hardware Is Software", *Uncharted Territories*, published 2026-11-18
  (source ID date), captured 2026-11-20. The canonical URL drops the newsletter `utm_source`
  parameter.
- Quoted or linked but not read: Blake Scholl's X post; the NASA 2022 NTRS paper; Handmer's X posts;
  a Capgemini physical-AI report (an image in the capture); an NSF R&D statistic; the Wired 2012 Musk
  interview; DeepMind's AlphaChip post.
- The NVIDIA market-cap aside ("four trillion" reasons) is footnoted "As I write this in November,
  2026".

## Related pages

- [[Accelerator Software Externalization]]
- [[NVIDIA]]
- [[AI Accelerator Architecture]]
- [[Robot Training Data]]
- [[Sergey Tselovalnikov - How to Be a 10x Engineer in 2027 and Beyond]]
