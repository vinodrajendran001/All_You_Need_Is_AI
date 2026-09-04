import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _integrate import integrate

R = "src-2026-09-02-raschka-astra-looped-transformers"
D = "src-2026-08-31-docmilanfar-lagrangian-flow-matching"

integrate(
    "Recursive Architectures", [R],
    "The first shipped numbers: 22 layers twice, and where it stops paying",
    """
[[Sebastian Raschka - OpenAI Astra and Looped Transformers]] gives this page its first published operating point
from a released model. **Nanbeige4.2-3B**, pretrained from scratch on 28T tokens, reuses a **22-layer stack
twice for an effective 44 layers** without duplicating weights — storage and RAM stay flat while compute roughly
doubles, because the text passes through nearly twice as many layer applications. As far as the source knows it
is the first notable open-weight model to adopt the approach.

The trade-off curve is the more valuable part, because it says where the technique stops paying. Per Nanbeige's
technical report, **two passes gave the best trade-off and retained about 75% of the token efficiency** of a
standard architecture, while *"more passes gave barely any gains but made the training much slower and much more
expensive."* So recursion buys parameter efficiency at a measured cost in token efficiency, and the benefit
saturates almost immediately. That 75% figure is also evidence against the loose framing that looping "doubles
the model" — capacity gained by weight reuse is demonstrably not equivalent to capacity gained from new
parameters.

The source is equally firm about scale of the idea: reusing layers is *"just a tiny architectural tweak,"* not a
breakthrough, and the more sophisticated version already exists as the NeurIPS **Mixture-of-Recursions** work,
which adds a learned per-token router so easy tokens exit after one pass while harder tokens receive more.
Whether token-level adaptive depth beats a fixed two passes in practice, and at what routing overhead, is not
addressed.

Alongside [[Linear Attention and Recurrent Memory]]'s record of Qwen3.8's 3:1 hybrid ratio, this vault now holds
two shipped architectural operating points and **no ablation curve for either** — both are one lab's chosen point
on a curve nobody has published.
""",
    ["Sebastian Raschka - OpenAI Astra and Looped Transformers", "Linear Attention and Recurrent Memory",
     "Chain-of-Thought Monitoring", "Sebastian Raschka"],
)

integrate(
    "Linear Attention and Recurrent Memory", [R],
    "A second shipped ratio, and the same missing curve",
    """
[[Sebastian Raschka - OpenAI Astra and Looped Transformers]] adds a parallel data point to the hybrid ratio
recorded above. Where Qwen3.8 fixes a 3:1 ratio of Gated DeltaNet to Gated Attention blocks, **Nanbeige4.2-3B
reuses a 22-layer stack twice** — a different lever on the same trade, buying capacity without buying parameters.
Its published operating point is more informative than Qwen's, because it comes with a cost: **two passes
retained roughly 75% of the token efficiency** of a standard architecture, and additional passes *"gave barely any
gains but made the training much slower and much more expensive."*

The shared feature of both results is what this vault should record most carefully: **neither is accompanied by
an ablation curve.** Qwen's 3:1 and Nanbeige's ×2 are each one lab's chosen point, reported as a conclusion
rather than as a measurement, on architectural axes where the interesting question is the shape of the trade
rather than any single setting. Two independent labs converging on "a small integer works, more does not help"
is suggestive, but it is not the curve.
""",
    ["Sebastian Raschka - OpenAI Astra and Looped Transformers", "Recursive Architectures", "Sebastian Raschka"],
)

integrate(
    "Chain-of-Thought Monitoring", [R],
    "The trace shrinks with capacity, not with any one architecture",
    """
[[Sebastian Raschka - OpenAI Astra and Looped Transformers]] corrects a claim that circulated in press coverage
of OpenAI's Astra: that recurrent-depth architectures work *"in a way that obscures some or all of the AI's
reasoning."* Raschka rejects the inference directly — **"Reusing layers does not by itself suppress visible chain
of thought. It adds computation in hidden states before the next token is emitted, just as ordinary transformer
layers do."** A looped layer stack is not a mechanism for hiding reasoning; it is more of the mechanism every
transformer already has.

The correction matters because the version that survives is both weaker and more troubling for this page. The one
plausible reading he grants: a model with more computation available per token *may need to generate fewer
intermediate reasoning tokens*, pushing more of the work into latent activations that cannot be read as text. But
this is **not specific to looping** — *"we would get the same effect if we were scaling up the model size, like
GPT 5.6 Luna -> GPT 5.6 Sol."*

That reframes the monitorability problem. If legible traces thin out because capability per token rises, then
erosion of chain-of-thought monitoring is not a property of a suspect architecture that could be avoided by
choosing a different one. It is a side effect of models getting better, arriving through whichever axis of
improvement a lab happens to pursue — which makes it harder to attribute, harder to argue against on a
per-release basis, and correspondingly harder to build governance around.

Two cautions attach. The mechanism is **asserted, not measured**: no experiment here shows reasoning tokens
trading against latent computation. And the debunk is of the *reporting* — Raschka is explicit that he does not
know Astra's architecture and is reasoning from published models described similarly.
""",
    ["Sebastian Raschka - OpenAI Astra and Looped Transformers", "Recursive Architectures",
     "Latent-Space Reasoning", "Sebastian Raschka"],
)

integrate(
    "Latent-Space Reasoning", [R],
    "Layer reuse is not latent reasoning",
    """
[[Sebastian Raschka - OpenAI Astra and Looped Transformers]] draws a boundary this page needs. Looped
transformers are frequently listed as latent-reasoning architectures, but reusing a layer stack is *"just reusing
layers in the transformer block"* — it adds computation in hidden states before the next token is emitted,
**exactly as ordinary layers do.** By that standard every transformer reasons latently, and the label stops
distinguishing anything.

The distinction that survives is quantitative rather than architectural. More computation available per token
means a model *may* need fewer explicit intermediate tokens to reach the same answer, shifting work into
activations that cannot be read as text. Raschka's crucial qualification is that this follows from capacity, not
from recurrence: **"we would get the same effect if we were scaling up the model size."** Latent reasoning, on
this reading, is a continuum every capability increase moves along, not a design choice a lab makes.

The concrete numbers are worth carrying: Nanbeige4.2-3B runs a **22-layer stack twice**, and its technical report
found **two passes optimal, retaining ~75% of token efficiency**, with more passes giving *"barely any gains."*
If extra latent passes were straightforwardly substituting for explicit reasoning tokens, one would expect the
benefit to continue; it does not. See [[Recursive Architectures]].
""",
    ["Sebastian Raschka - OpenAI Astra and Looped Transformers", "Recursive Architectures",
     "Chain-of-Thought Monitoring", "Sebastian Raschka"],
)

integrate(
    "Reasoning Trace Privacy", [R],
    "The trace may thin out on its own",
    """
This page treats the reasoning trace as something providers deliberately withhold, encrypt, or summarize.
[[Sebastian Raschka - OpenAI Astra and Looped Transformers]] raises a different route to the same end state:
**the trace may simply get shorter as models get more capable.** More computation available per token can mean
fewer intermediate reasoning tokens are needed, with the work moving into latent activations that no envelope,
policy, or extraction technique can recover — because they were never emitted.

He is careful about what this is not. Layer reuse does not itself suppress visible reasoning; recurrence *"adds
computation in hidden states before the next token is emitted, just as ordinary transformer layers do."* And the
effect is not architecture-specific: **"we would get the same effect if we were scaling up the model size, like
GPT 5.6 Luna -> GPT 5.6 Sol."**

For this page the implication is that trace access has two independent failure modes. One is a **policy**
boundary — encryption, summarization, opaque blobs — which is contestable, negotiable, and, as this page
documents, sometimes circumventable. The other is a **capability** boundary, where there is progressively less
trace to access at all. Techniques that defeat the first do nothing about the second. The mechanism is asserted
rather than measured, but it is the version of the concern that survives Raschka's correction of the press
coverage.
""",
    ["Sebastian Raschka - OpenAI Astra and Looped Transformers", "Chain-of-Thought Monitoring",
     "Latent-Space Reasoning", "Recursive Architectures", "Sebastian Raschka"],
)

integrate(
    "Sebastian Raschka", [R],
    "Debunking as a contribution",
    """
[[Sebastian Raschka - OpenAI Astra and Looped Transformers]] is a different kind of post from his usual
implementation-first explainers, and useful to this vault for that reason: it is a **short corrective written
against press coverage.** The claim under repair was that OpenAI's Astra uses a "recurrent depth" technique that
obscures the model's chain of thought. His reply separates two things the coverage had merged — that looping is
*"just reusing layers,"* and that reducing legible reasoning is a consequence of capacity rather than of
recurrence, since *"we would get the same effect if we were scaling up the model size."*

The characteristic discipline is intact. He states what he is reasoning from (published models described
similarly, not Astra itself), relays Nanbeige's **~75% token-efficiency retention at two passes** as the
publisher's figure rather than as verified, allows that the journalist may have meant a different technique, and
labels the latent-computation account as *"the only plausible interpretation"* rather than as fact. His verdict
is proportionate rather than dismissive: *"Astra may be a really good model, but this shouldn't be about this
'looped transformer aspect,' which is just a tiny architectural tweak."*

He anchors [[Recursive Architectures]] with this vault's first shipped configuration for layer reuse, and
supplies the correction that reframes [[Chain-of-Thought Monitoring]].
""",
    ["Sebastian Raschka - OpenAI Astra and Looped Transformers", "Recursive Architectures",
     "Chain-of-Thought Monitoring", "Latent-Space Reasoning"],
)
