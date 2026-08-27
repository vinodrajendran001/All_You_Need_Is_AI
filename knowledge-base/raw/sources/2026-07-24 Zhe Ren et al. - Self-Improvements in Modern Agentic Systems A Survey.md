---
type: raw-source
title: "Self-Improvements in Modern Agentic Systems: A Survey"
source: "https://arxiv.org/html/2607.13104v1"
author:
published:
created: 2026-07-24
description:
tags:
  - "clippings"
  - "source/raw"

---
Zhe Ren <sup>1</sup>, Yimeng Chen <sup>2</sup>, Dandan Guo <sup>1,2</sup> <sup>1</sup>, Guowei Rong <sup>1</sup>, Tonghui Li <sup>1</sup>,  
R.B. Xiong <sup>3</sup>, Qingfeng Lan <sup>4</sup>, Wenyi Wang <sup>2</sup>, Li Nanbo <sup>2</sup>, Yibo Yang <sup>2</sup>,  
Mingchen Zhuge <sup>2</sup>, Jürgen Schmidhuber <sup>2,5</sup>  
<sup>1</sup> School of Artificial Intelligence, Jilin University <sup>2</sup> King Abdullah University of Science and Technology (KAUST) <sup>3</sup> Independent Researcher   <sup>4</sup> University of Alberta <sup>5</sup> The Swiss AI Lab IDSIA/USI/SUPSI  
renzhe25@mails.jlu.edu.cn, yimeng.chen@kaust.edu.sa, guodandan@jlu.edu.cn,  
{ronggw25, lith}@mails.jlu.edu.cn, rbxiong1@outlook.com, qlan3@ualberta.ca,  
{wenyi.wang, nanbo.li, yibo.yang, mingchen.zhuge, juergen.schmidhuber}@kaust.edu.sa  
Corresponding authors

###### Abstract

Self-improving autonomous agents are moving from research prototypes to deployed systems. The primary goal is controllable evolution, or adaptation, from experience with minimal or even no human input. This survey frames modern self-improving agents as adaptive systems that convert experience into accumulated capability gains. We offer a system-level framework that represents a modern agent as a configuration coupling a foundation model with an operational scaffold of prompts, memory, tools, and control logic. Within this framework, self-improvement is formalized as a self-induced update operator that obtains and commits updates to model parameters or scaffold components. We organize prior work by update target and by the signals that drive change, then review applications and discuss evaluation, before closing with open problems and future directions. For convenience, we track technical updates on [this GitHub page](https://github.com/selfimproving-agent/awesome-Self-Improving-Agents).

| [Self-Improving-Agents](https://github.com/selfimproving-agent/awesome-Self-Improving-Agents) | [Project Page](https://selfimproving-agent.github.io/) |
| --- | --- |

![Refer to caption](https://arxiv.org/html/2607.13104v1/x1.png)

Figure 1: Overview of self-improvement paradigms for modern AI agents. We categorize existing methods into two primary pathways according to what is modified. The first pathway is Foundation Model Improvement, where the model parameters are updated from θ t \\theta\_{t} to + 1 \\theta\_{t+1} using intrinsic generative demonstrations 𝒟 \\mathcal{D}\_{t}, intrinsic evaluative feedback e e\_{t}, or extrinsic exploratory experience τ \\tau\_{t}. The second pathway is Scaffolding Improvement, where the operational scaffold is updated from Σ \\Sigma\_{t} \\Sigma\_{t+1} through non-parametric changes. Across scaffold components, a generic update signal 𝒮 \\mathcal{S}\_{t} is instantiated to drive improvements in prompts p p\_{t}, memory m m\_{t}, tools 𝒯 \\mathcal{T}\_{t}, or the full scaffolding.

## 1 Introduction

The development of artificial intelligence (AI) technology has driven a paradigm shift in agentic systems [^280] [^187] [^349] [^380] [^327], from earlier narrow systems built around task-specific models or hand-engineered modules to modern agentic systems powered by foundation models (FMs), including large language models (LLMs) and vision-language models (VLMs), where natural language serves as a shared interface for representation, reasoning, and control. Progress in foundation models has produced a qualitative shift in generalization, yielding striking successes across a wide range of domains, most notably code generation [^35], language understanding [^114], and mathematical and formal reasoning [^343]. These advances have brought a long-standing question to the foreground: the prospect of AI systems that improve themselves. Fundamentally, self-improvement is an inherently self-referential process. It defines a system’s capacity to autonomously inspect, evaluate, and deliberately modify its own underlying optimization mechanisms and operational logic. Good articulated possible consequences of machine self-improvement [^94], describing the possibility of an “Intelligence Explosion” once machines acquire the capacity to design more capable successors. Early work on concrete self-improvement algorithms dates back to Schmidhuber’s self-referential learning framework [^256], which introduced mechanisms in which a system generates and evaluates modified descendant versions of itself. Establishing the theoretical ceiling of this pursuit, the Gödel Machine [^264] introduced a fully self-referential algorithm designed to rewrite its own code whenever it can mathematically prove an expected-utility improvement. While a persistent lineage of research successfully demonstrated neural networks (NNs) learning to program other networks via fast weights [^260], advancing to self-referential systems capable of modifying themselves [^261] [^132], and acting as meta-learning systems to discover their own learning algorithms [^116] [^265] [^143] [^144] [^130], parallel efforts introduced incremental self-improvement, establishing the ability to enforce long-term reward accelerations through the success-story algorithm for undoing policy self-modifications through backtracking [^248] [^247] [^254]. However, scaling these visionary mechanisms into open-ended agents was historically constrained. Traditionally, systems were forced to search through vast, low-level spaces of assembly-like code or raw synaptic weights. Today, modern FMs alleviate this historical bottleneck by introducing natural language as a unified, highly capable semantic medium for reasoning, policy execution, and self-modification. By drastically reducing the search space for viable modifications, this language-native paradigm has drawn intense recent attention, with growing evidence demonstrating that FM-based self-improving agents can yield substantial empirical gains [^389] [^2] [^216] [^405].

To function autonomously in concrete environments, the FM serving as the cognitive core is typically enveloped by an operational scaffold, a structured framework comprising instruction schemes [^391] [^101], memory systems [^44] [^410], tool interfaces [^223], and control logic [^119] [^435] [^362]. Recently, such an operational scaffold is often also referred to as an agent harness [^228] [^318] [^402] [^424], while this survey uses the term scaffold to emphasize the modifiable structures surrounding the foundation model. Operationally, this scaffold acts as a controller that constructs context, selects actions, and enforces constraints. This modern architecture was conceptually foreshadowed by the "learning to think" framework [^270], where a general-purpose controller learned to dynamically query, or "prompt," a predictive world model to generate reasoning sequences akin to a modern "chain of thought" [^343]. Building upon this core-and-scaffold architecture, the integration of these classical control principles has crystallized into an emergent paradigm, which we refer to as FM-based self-improving agents. Because modern agentic systems comprise both the aforementioned neural core and scaffold, we organize this survey around a unified taxonomy with two primary pathways, as illustrated in Fig. 1 and summarized chronologically in Fig. 2. The first pathway, which we call foundation model improvement, aims to achieve a slower but more stable form of long-term consolidation by updating the underlying model, thereby amortizing capability gains across varied tasks [^124] [^418] [^326] [^360] [^27]. The second pathway, which we call scaffold improvement, is typically faster and more easily reversible; it improves the agent by updating structural components, including prompts, memory, tool interfaces, and end-to-end control logic, to reshape the agent’s effective observation and action semantics [^78] [^44] [^405] [^26]. Although these pathways differ in their targets of modification, both are fundamentally driven by learning signals extracted during interaction. Accordingly, our taxonomy further refines these methods by separating what is updated from where the improvement signals originate, providing a common language for comparing disparate methods on a consistent footing. Fig. 3 provides a unified taxonomy of this survey.

| black!4cyan!8 Dimension | Ours (2026) | [^81] | [^71] | [^311] |
| --- | --- | --- | --- | --- |
| black!4Agent formulation | $\checkmark$ | $\checkmark$ | $\checkmark$ | $\circ$ |
| black!4Definition scope | $\checkmark$ | $\checkmark$ | $\circ$ | $\circ$ |
| black!4Historical roots | $\checkmark$ | – | $\circ$ | $\circ$ |
| black!4Signal lens | $\checkmark$ | $\circ$ | $\checkmark$ | $\checkmark$ |
| black!4Update substrate | $\checkmark$ | $\checkmark$ | $\checkmark$ | $\circ$ |
| black!4Evaluation lens | $\checkmark$ | $\checkmark$ | $\checkmark$ | $\checkmark$ |
| black!4Domain coverage | $\checkmark$ | $\circ$ | $\circ$ | – |
| black!4Outlook & issues | $\checkmark$ | $\circ$ | $\checkmark$ | $\circ$ |

$\checkmark$ primary   $\circ$ secondary  – not focus

Table 1: Comparison of organizing emphases across related surveys.

Despite the rapid proliferation of such empirical frameworks, the broader research landscape remains highly fragmented in both terminology and scope. Closely related ideas are often described under different labels (e.g., self-correction, meta-prompting, or self-play), obscuring underlying mechanistic similarities. Recent surveys have provided valuable perspectives by organizing self-evolving agents along dimensions such as what to evolve, when to evolve, and how to evolve [^81] [^71], or by focusing specifically on the autonomous learning capabilities of static LLMs [^311]. However, existing reviews often treat foundation model fine-tuning and agent scaffolding as isolated topics, lacking a unified formal perspective. Furthermore, few trace the conceptual roots of self-improvement back to classical AI. To bridge this gap, our survey provides a rigorous and systematic positioning of these modern agentic systems. We offer a comprehensive taxonomy under a unified formalization, clarifying their historical evolution and providing a clear, forward-looking roadmap for self-improvement. Concretely, our main contributions are as follows:

- Historical Context and Evolution. We trace the evolutionary roots of self-improving systems from classical AI to modern FM-based agents, establishing a clear trajectory for how foundational learning mechanisms have adapted to the agentic era.
- A Unified Formalization and Systematic Taxonomy. Under our proposed formulation, we systematically categorize mechanisms into two distinct pathways: foundation model improvement and scaffold improvement (covering prompt optimization, memory evolution, tool governance, and full-scaffold redesign).
- Empirical Landscape, Evaluation Paradigms, and Frontiers. We integrate the classification system with practical applications (such as software engineering, web navigation, and scientific discovery) and critically analyze current evaluation protocols. By comparing mechanism-level benchmarking and end-to-end evaluation, we highlight the security factors and challenges that need to be considered in achieving reliable, continuous self-improvement.

The remainder of this survey is organized as follows. Section 2 traces the historical context and theoretical foundations of self-improving systems. Section 3 introduces the systems view of foundation-model-based agents and formalizes the problem setting. Section 4 presents our unified taxonomy, outlining the two primary pathways for improvement. These pathways are subsequently surveyed in depth: Section 5 covers updates to the underlying foundation model, while Section 6 focuses on structural modifications to the surrounding scaffold. Section 7 reviews practical instantiations across representative domains. Section 8 discusses protocols and benchmarks for evaluating these systems. Finally, Section 9 synthesizes open problems and safety considerations, followed by concluding remarks in Section 10.

![Refer to caption](https://arxiv.org/html/2607.13104v1/x2.png)

Figure 2: Timeline and taxonomy of self-improvement in foundation-model-based agents (2023–2026). Representative works are positioned by publication year. The left lane denotes foundation-model improvement ( θ \\theta ), while the right lane denotes scaffolding improvement ( Σ \\Sigma ). The AGI signpost highlights the field’s long-term aspiration toward increasingly general agentic intelligence.

Figure 3: A unified taxonomy of self-improving agents spanning foundation-model updates, scaffold updates, and evaluation benchmarks.

## 2 Historical Context and Theoretical Foundations

Self-improvement is not unique to modern foundation models; it is a foundational objective of artificial intelligence. Whereas standard machine learning optimizes parameters within a fixed architecture, true self-improvement demands that a system explicitly inspect and rewrite its own operational logic, heuristics, or learning algorithms. As illustrated in Figure 4, the mechanisms have been successfully instantiated across several historical paradigms. By tracing this intellectual lineage, we clarify how earlier systems achieved self-improvement within bounded domains, and how modern foundation models now provide a highly expressive, general-purpose substrate to scale these established principles into open-ended and real-world environments.

![Refer to caption](https://arxiv.org/html/2607.13104v1/x3.png)

Figure 4: A timeline of theoretical roots and idealized models for self-improving agents, from the late 1790s to the present.

### 2.1 Foundational Concepts (1790s-1960s)

The mathematical roots of error-driven adaptation extend back to early optimization frameworks. The method of least squares [^153] [^86] <sup>1</sup> demonstrated how parameters of what’s now known as “linear neural networks” can be systematically adjusted to minimize errors. As highlighted in historical retrospectives, this established a mechanism that is still heavily used today and serves as the very foundation of all neural networks, including deeper ones [^252].

Throughout the mid-20th century, these concepts of adaptation continued to evolve, acting as conceptual precursors. Cybernetics popularized the feedback view of adaptive behavior in closed-loop systems [^347], while Ashby’s work on homeostasis emphasized internal state adjustment to maintain viability under perturbations [^12]. Alan Turing’s “child machine” proposed a model whose internal configuration could be shaped through training and external feedback, such as reward and punishment [^319] [^320]. Early systems, from Rosenblatt’s perceptron [^239] to Samuel’s checkers program [^243], provided concrete demonstrations of how performance feedback could change future behavior. However, while these mid-century milestones demonstrated that behavior could optimize over time, their underlying architectures and learning algorithms themselves remained strictly fixed. Consequently, they are best understood as advanced learning systems, rather than fully self-referential, self-improving systems.

The formal basis for transcending fixed learning rules and enabling true self-reference followed a distinct trajectory. In the early 1930s, Kurt Gödel founded modern theoretical computer science and identified fundamental limits of any type of computation-based AI [^91]. He introduced a universal coding language based on integers, using it to represent both data and programs in axiomatic form. By famously constructing formal statements that talk about the computation of other formal statements—especially self-referential statements—Gödel provided the theoretical blueprint for programs capable of manipulating their own code [^252]. In the 1960s, Good [^94] introduced the visionary prospect of an “Intelligence Explosion,” hypothesizing that machines might one day acquire the capacity to autonomously design more capable successors. However, while this narrative highlighted self-improvement as an ultimate pursuit in AI, it remained a conceptual idea without a formal mathematical or algorithmic framework. Translating this speculative concept into actual deployable mechanisms would require the subsequent development of explicit structural and algorithmic self-modification frameworks.

### 2.2 Symbolism and Heuristic Self-Modification (1960s–1980s)

As symbolic AI rose to prominence, self-improvement was reinterpreted as the ability to manipulate explicit representations of knowledge and strategy. A key conceptual precursor was von Neumann’s theory of self-reproducing automata. Originating in the late 1940s and later published in 1966, it distinguished a constructive mechanism from a symbolic description that can be copied and varied [^321]. [^191] abstracted self-reproduction into a rigorous formal framework, emphasizing how systems can use symbolic descriptions to generate copies or variants of themselves. Together, these concepts clarified how a system can generate successive versions of increasing complexity by editing the descriptions it interprets. A similar approach in symbolic artificial intelligence is to treat problem-solving heuristics as first-class objects that can be examined, modified, and recombined.

Lenat’s Automated Mathematician (AM) system exemplified this approach by using heuristics to propose, extend, and evaluate candidate concepts, effectively searching over symbolic programs that encode mathematical ideas [^156]. EURISKO pushed further by representing heuristics themselves as manipulable Lisp objects, allowing the system to generate, modify, and test its own problem-solving strategies [^155] [^154]. However, as emphasized by [^256], the practical success of systems like EURISKO depended heavily on the user serving as an external evaluation signal, interpreting outputs and manually pruning unproductive heuristic drift, rather than on the system possessing a truly autonomous closed-loop credit assignment mechanism. This historical limitation underscores a challenge that persists in modern agentic systems, namely the need for robust internal evaluation signals and verification procedures to sustain autonomous recursive self-improvement.

### 2.3 Connectionism and the Emergence of Meta-Learning (1980s–2000s)

The resurgence of connectionism shifted the emphasis from hand-coded heuristics to learning dynamics as the substrate of improvement. Self-improvement was consequently reframed as explicitly optimizing the learning process itself, encompassing the optimizer, inductive biases, and adaptation rules. [^256] introduced self-referential learning frameworks in which evolutionary processes could optimize not only candidate solutions but also the learning procedures that generate them, making the learning system itself the object of search. Along a complementary line, [^21] demonstrated that synaptic learning rules need not be fixed; by parameterizing these rules, the optimizer itself becomes a learnable object.

Schmidhuber introduced fast-weight programmers (FWPs) as a broad class of networks [^246] [^260] [^261]. A representative early instance—retrospectively identified as the 1991 unnormalized linear Transformer (ULTRA) [^245] —features a “slow” neural network that learns by gradient descent to program the “fast weights” of another network through additive outer-product updates. The explicitly self-referential version followed in work on self-referential weight matrices, where a network learns to modify its own fast weights while receiving feedback signals such as errors or rewards as inputs, making the learning dynamics themselves part of what is optimized [^261]. This line is important for self-improvement because it moves self-modification into a continuous program space, rather than restricting it to symbolic code rewriting. Recent work has revisited this direction in scalable self-referential neural architectures, including modern self-referential weight matrices that learn to modify themselves [^132], recurrent fast-weight programmers and their self-referential extensions [^129] [^131], and self-referential networks that meta-learn continual learning algorithms [^130]. Such mechanisms suggest a possible additional meta-level for self-improving foundation models, where the foundation model itself may become part of the modifiable substrate rather than remaining only a frozen component.

This period also consolidated learning to learn as a framing for self-improvement. In reinforcement learning (RL), the 1994 paper introduced an RL machine as an early recursive self-improving agent that alter parts of their own learning strategy to shift inductive bias over a single lifelong interaction stream [^248]. The same underlying idea was later described using related terminology, including environment-independent reinforcement acceleration and the success-story algorithm [^348] [^247] [^255] [^254]. Thrun and Pratt likewise emphasized learning reusable inductive biases across task distributions [^312]. Related neuroevolution work such as NeuroEvolution of Augmenting Topologies (NEAT) improved neural architectures by expanding network topology under performance-driven selection [^297]. AIXI formalized an uncomputable upper bound on optimal sequential decision-making in computable environments [^128]. Furthermore, [^264] introduced the Gödel Machine, a fully self-referential, self-improving machine that is theoretically optimal. A Gödel Machine operates in a single-life reinforcement learning environment [^248] and iteratively searches for candidate self-modifications, adopting a modification only when it can prove that doing so will improve its expected cumulative future reward. To establish this improvement, the proof must reason about future rewards while accounting for all possible subsequent self-modifications. The machine is fully self-referential in the sense that every component of the Gödel Machine is itself subject to modification, including the self-modification generator and the theorem prover.

### 2.4 Formal and Architecture-Level Self-Improvement (2000s-2020s)

From the mid-2000s onward, research followed two main tracks: (i) analyzing the theoretical limits of self-improvement, and (ii) building practical mechanisms to automate architecture design. Philosophical analyses began to explore the trajectory of these systems, debating the existential risks of the technological singularity [^301]. In theory, Orseau and Ring pointed out that when agents interact with limited resources and irreversible actions, they face significant risks such as self-deception, reward tampering, and fatal errors [^199]. Related research formalized how agents can safely model their environments and themselves without generating logical paradoxes. For instance, Fallenstein et al. [^70] introduced reflective oracles to reason about probabilistic programs that call themselves, while logical induction offered a mathematical approach to updating beliefs under self-referential uncertainty [^85]. Complementary work on proof-producing reflection in higher-order logic studied how reflective reasoning can be embedded in formal proof systems, providing a technical route for agents or theorem provers to reason about their own reasoning steps [^68].

Together, these frameworks clarified the gap between ideal models and practical deployments, demonstrating the necessity of safe and constrained self-modification. Early attempts to bridge this gap computationally, such as the endeavor to implement Gödel machines, sought architectures where agents could mathematically prove the optimality of their own code updates [^299]. At the architecture level, Nivel et al. proposed bounded recursive self-improvement, where reflective mechanisms and value-driven scheduling support self-modification under designer-imposed constraints [^195]. In engineering, automated design has matured into Neural Architecture Search (NAS), where controller learning proposes architectures that can directly optimize task performance [^439]. Meanwhile, scalable algorithms such as self-play in reinforcement learning demonstrated how agents can generate increasingly difficult curricula from their own behavior, thus achieving continuous capability growth without human supervision [^287]. Ultimately, these theoretical and engineering advances have laid the foundation for modern agent systems centered on foundation models.

### 2.5 Scalable Foundation Models and Agentic Systems (2020s–Present)

The classical vision of autonomous agents—capable of perceiving, acting, and learning in open-ended environments—found a scalable, modern substrate in foundation models (FMs). Powered by the immense knowledge compressed during large-scale pretraining and the flexibility of a unified natural-language interface, FMs function as the cognitive engines of contemporary agentic systems. Crucially, the emergence of these systems fundamentally reshaped the paradigm of self-improvement, decoupling it into two distinct but complementary mechanisms: rapid, training-free adaptation and persistent parameter optimization.

Within this modern paradigm, the most immediate form of self-improvement occurs without computationally expensive weight updates. Because scalable sequence models facilitate broad generalization, agents can achieve rapid, training-free adaptation by dynamically revising their plans, prompts, and memory representations on the fly. This short-horizon self-improvement relies heavily on in-context learning, which effectively functions as a form of meta-learning. Mechanistically, this adaptation is mediated by the attention mechanism’s key-value cache, acting as an associative memory that generates transient, context-dependent weight changes during sequence processing. This functional equivalence directly connects modern in-context learning to the 1991 fast-weight programmers (formally identified as unnormalized linear Transformers), in which networks similarly learned to induce rapid parameter changes during inference without requiring standard gradient descent [^246] [^260] [^261] [^245].

Complementing this fast, in-context adaptation are slow improvement loops designed to permanently internalize new capabilities. Reinforcement learning from human feedback (RLHF) and its variants achieved this by converting interaction traces and preference signals into persistent parameter updates [^202]. Parallel methodologies advanced partially self-supervised alignment by enabling models to critique their own outputs and provide AI feedback [^19]. Meanwhile, frameworks like Reasoning and Acting (ReAct) and Reflexion build these loops on top of contextual execution, converting execution errors into natural-language reflections [^380] [^279]. Recent systems pushed this further by maintaining skill libraries, curricula, and evaluation harnesses, spanning open-ended embodied learning [^324], software-engineering agents with instrumented interfaces [^375] [^405] [^332], and explicitly self-improving computer-use agents that iterate data, reward models, and policies over generations [^360] [^305]. Overall, the modern era reframes self-improvement as nested loops across parameters and scaffolding, renewing classical questions about control, evaluation, and safety at scale.

## 3 Definitions

### 3.1 Formulation of Agentic Systems

We begin by clarifying the formal definition of an agent. The core of an autonomous agent lies in perceiving its environment, updating its internal state, and performing actions to achieve a specific goal. While such systems have driven decades of AI research, this survey focuses exclusively on a contemporary class: foundation-model-based agents, which utilize large foundation models as their central cognitive engines. Crucially, they leverage natural language as a unified interface to integrate perception, reasoning, and tool manipulation. Because a foundation model fundamentally operates as a stateless inference engine, achieving autonomy requires coupling this cognitive core with a persistent, interactive scaffold. Therefore, we formally define the configuration of a foundation-model-based agent at time step $t$ as:

$$
\mathcal{A}_{t}\;=\;(\theta_{t},\;\Sigma_{t}),
$$

where $\theta_{t}$ encapsulates the neural parameters of the foundation model, and $\Sigma_{t}$ denotes the agent’s dynamic operational scaffold. The scaffold $\Sigma_{t}$ specifies how the foundation model is conditioned, grounded, and connected to the external world. Concretely, it can be decomposed as

$$
\Sigma_{t}:=(p_{t},\,m_{t},\,\mathcal{T}_{t},\,g_{t}),
$$

where $p_{t}$ denotes structured prompts or system instructions, $m_{t}$ denotes memory mechanisms and their retrieval and update policies, $\mathcal{T}_{t}$ denotes the set of external tools together with their invocation interfaces, and $g_{t}$ denotes additional control logic such as routing, scheduling, or safety constraints. The interaction between these components and the model’s internal parameters is illustrated in Figure 5, which provides a schematic overview of an FM-based agent within our proposed formalism. Together, $\theta_{t}$ and $\Sigma_{t}$ determine how the agent reasons, plans, and acts.

During execution, to bridge this intrinsic configuration with the external environment, the agent maintains an ephemeral execution state $X_{t}$ (e.g., key-value caches, intermediate plans, or short-term working memory) that evolves as it processes an interaction stream. To connect this structural definition to observable behavior, it is beneficial to clarify how the agent’s configuration generates its action selection mechanism. Although the foundation model parameters $\theta_{t}$ implement a general generative distribution, the agent’s realized behavior is jointly determined by both $\theta_{t}$ and its operational scaffold $\Sigma_{t}$. Accordingly, we denote the induced policy of the agent based on the foundation model as:

$$
\pi_{\theta_{t},\Sigma_{t}}(A_{t}\mid X_{t}),
$$

where $A_{t}$ denotes the action produced by the system at time step $t$. Here, the conditioning on $X_{t}$ captures the transient context of the ongoing interaction. While $X_{t}$ may strongly influence immediate behavior, it is inherently ephemeral. It is typically discarded or reset once an immediate goal is reached or an external task boundary is crossed, and therefore does not constitute part of the agent’s intrinsic architecture. In contrast, the parameters $(\theta_{t},\Sigma_{t})$ represent the agent’s intrinsic configuration over time. While a standard agent may adapt to novel situations by dynamically updating its transient state $X_{t}$ (e.g., in-context examples), its underlying capabilities remain bounded by its fixed initial setup.

![Refer to caption](https://arxiv.org/html/2607.13104v1/x4.png)

Figure 5: Schematic of an FM-based agent under our formalism.

### 3.2 Formal Definition of Self-Improvement

Building upon the formal configuration $\mathcal{A}_{t}=(\theta_{t},\Sigma_{t})$, we formalize self-improvement in foundation-model-based agents (SI-FMA) as a process of persistent, endogenous adaptation. Rooted in the foundational principles of explicitly self-referential meta-learning [^256] [^261] [^254], a self-improving agent actively leverages signals induced by its own execution—such as interaction outcomes, critiques, verification results, or proposed edits—to durably modify its underlying computational components.

##### Self-improvement as a self-induced operator.

We conceptualize self-improvement through a *self-induced* operator $\mathcal{U}$ that updates the agent’s intrinsic configuration. Let $\pi_{\theta_{t},\Sigma_{t}}$ denote the agent’s induced policy. We formalize this process by factorizing the self-improvement step into an execution phase and an update phase:

$$
\mathcal{A}_{t+1}\;=\;\mathcal{U}\Big(\mathcal{A}_{1:t},\;\mathcal{E}\big(\pi_{\theta_{t},\Sigma_{t}};\Sigma_{t},\mathcal{C}_{t}\big)\Big),
$$

where $\mathcal{E}$ denotes an *agent-executed* procedure that produces a learning signal (e.g., interaction trajectories, reflections, critiques, or proposed edits) by running the induced policy against a task context $\mathcal{C}_{t}$ (e.g., a task distribution, a user interaction stream, or a self-play environment). The scaffold $\Sigma_{t}$ is included as an explicit argument to $\mathcal{E}$ to permit direct self-inspection (e.g., critiquing prompt templates or auditing tool configurations).

The system-level update rule $\mathcal{U}$ then applies this self-generated signal to modify the agent’s intrinsic components ($\theta$ or $\Sigma$). Unlike the routine evolution of the transient state $X_{t}$ (e.g., merely accumulating dialogue history or working memory), the operator $\mathcal{U}$ commits durable changes. Crucially, in line with lifelong meta-learning principles, while these updates are not strictly irreversible and may be undone, they allow the agent to consolidate successful strategies into an increasingly stable policy over its interaction stream [^248] [^262] [^348] [^247].

##### Two modes of self-reference in SI-FMA.

SI-FMA may be self-referential in multiple, qualitatively distinct senses. In the first mode, the agent’s policy is executed to *indirectly induce* improvement by generating experience or auxiliary artifacts that serve as learning signals. Self-generated trajectories, evaluations, preferences, or synthetic labels give rise to a learning objective that is subsequently consumed by an update rule, such as an external optimization procedure acting on the foundation model parameters $\theta_{t}$. This mode realizes self-improvement at the *distributional* level: the agent’s behavior shapes the data and supervision that determine its future parameters.

In the second mode, the agent’s policy is executed to *directly implement* improvements by modifying components of its own operational definition. Through its actions, the agent may edit prompt templates, manage or reorganize memory, reconfigure tool interfaces, or alter control logic, thereby explicitly updating the scaffolding $\Sigma_{t}$ that governs future execution. In this case, self-improvement is realized through direct, action-level self-modification.

These two modes correspond to distinct but complementary paradigms. *Foundation model improvement* realizes self-improvement through self-induced learning in parameter space, whereas *scaffolding improvement* realizes self-improvement through direct self-modification in execution space. Together, they capture the principal mechanisms by which FM-based agents may alter themselves over time.

##### Foundation model improvement.

In foundation model improvement, self-improvement targets the parameters of the underlying foundation model while holding the agent-level scaffolding fixed. Starting from an induced policy $\pi_{\theta_{t},\Sigma_{t}}$, the agent is repeatedly executed in the environment, generating self-induced experience through its own interaction trajectories.

We abstract this process by a self-induced update operator that maps the agent’s current configuration to an updated set of model parameters:

$$
\theta_{t+1}=\mathcal{U}_{\theta}\bigl(\theta_{1:t},\;\mathcal{E}(\pi_{\theta_{t},\Sigma_{t}};\Sigma_{t},\mathcal{C}_{t})\bigr),\quad\Sigma_{t+1}=\Sigma_{t},
$$

where $\mathcal{C}_{t}$ is the task or deployment context defined above, $\mathcal{E}$ denotes the execution of the agent under its induced policy in $\mathcal{C}_{t}$, producing learning signals such as rewards, preference comparisons, synthetic labels, critiques, or verification outcomes, and $\mathcal{U}_{\theta}$ denotes a parameter-learning procedure that updates the foundation model parameters based on these signals.

Importantly, while the construction of these learning signals may involve rule-based evaluators, learned reward models, or auxiliary model invocations, the underlying data distribution is induced by the agent’s own policy. The operator $\mathcal{U}_{\theta}$ may instantiate policy-gradient methods, offline or online reinforcement learning, preference optimization, or other parameter-learning algorithms. Foundation model improvement typically operates on longer time scales, incurs substantial computational cost, and leads to stable, global changes in the agent’s internal representations, generalization behavior, and capabilities.

##### Scaffolding improvement.

In *scaffolding improvement*, self-improvement targets the agent-level structures surrounding the foundation model while keeping the model parameters $\theta$ fixed. The scaffolding $\Sigma_{t}$ governs how histories are converted into the conditioning context for the foundation model, how tool calls are specified and executed, how memory is stored and retrieved, and more generally how token sequences are constrained such that they correspond to valid, executable actions. Through these mechanisms, $\Sigma_{t}$ shapes the agent’s effective observation and action semantics, as well as the construction and evolution of the agent state $X_{t}$ during execution.

Formally, scaffolding improvement can be expressed as a self-induced update in which an *agent-executed* procedure produces a meta-level signal that is then applied as an intrinsic update:

$$
\Sigma_{t+1}\;=\;\mathcal{U}_{\Sigma}\Big(\Sigma_{1:t},\;\mathcal{E}\big(\pi_{\theta_{t},\Sigma_{t}};\Sigma_{t},\mathcal{C}_{t}\big)\Big),\qquad\theta_{t+1}=\theta_{t},
$$

where $\mathcal{E}$ denotes the execution of the agent (possibly under a meta-objective) to generate update-relevant artifacts, such as proposed prompt edits, memory reorganizations, tool-interface changes, or new control routines, and $\mathcal{U}_{\Sigma}$ denotes the system-level mechanism that commits these artifacts as structural scaffolding updates. Unlike the transient evolution of $X_{t}$, the update above is intended to endure beyond individual task boundaries.

These updates modify the induced policy $\pi_{\theta,\Sigma}$ by reshaping (i) the conditioning context supplied to the foundation model, (ii) the effective action space via admissibility constraints and tool schemas, and (iii) the execution semantics by which token sequences are parsed and grounded into environment actions. Compared to foundation model improvement, scaffolding improvement is typically faster, more reversible, and more context-dependent, yet it can produce substantial changes in the agent’s effective behavior and problem-solving strategies.

##### Skill as a reusable update.

The two modes of self-reference above realize self-improvement either indirectly, through self-generated signals that an update rule consolidates into the parameters $\theta$, or directly, through actions that edit the scaffold $\Sigma$; a skill cuts across this distinction. We model a *skill* as a reusable instance of the self-induced update operator $\mathcal{U}$: a named update to the agent’s own configuration $\mathcal{A}_{t}$ that it retains and reuses. Acquiring a skill serializes this update into one of $\mathcal{A}_{t}$ ’s substrates: a tool and its calling convention ($\mathcal{T}$), an instruction or workflow ($p$), a memory entry ($m$), consolidated weights ($\theta$), or control logic ($g$). The skill’s identity is the update it encodes; the substrate only names where it is stored. This is what makes “skill” orthogonal to the substrate axis of our taxonomy. A skill library is then a structured store of, and retrieval policy over, these serialized updates; the same store-and-retrieve structure recurs across substrates, which is why it surfaces in both tool routing and memory organization.

Reusability takes two forms. A skill may be invoked repeatedly, as a retained routine called many times across tasks, or applied once in the manner of an installer: a single update whose value lies in the persistent change it leaves behind, but which remains a portable artifact, reusable across agents and sessions. Either way, a skill is a first-class, serialized operator, in contrast to an ad hoc one-off action that leaves no retained trace.

We further distinguish two scopes according to what an invoked skill acts on. An *object-level* skill acts on the task or world state: invoking it runs a (typically multi-step) routine through the execution operator $\mathcal{E}$ to carry out a sub-task (e.g., a learned collect-wood routine), the agentic analog of a temporally extended option in hierarchical reinforcement learning [^307] [^18]. Here the $\mathcal{U}$ step lies in acquisition, which writes the routine into its substrate (e.g., $\mathcal{T}$), not in invocation. A *meta-level* skill instead acts on the agent’s own configuration $\mathcal{A}_{t}$: invoking it edits a component of $\Sigma_{t}$ or triggers a parameter update (e.g., writing a new tool, refactoring a prompt, consolidating experience into memory, or patching one’s own scaffold). The installer-like skills above are inherently meta-level. For self-improvement, the meta-level scope is the central one. Because a meta-level skill both acts on $\mathcal{A}_{t}$ and is itself serialized back into $\mathcal{A}_{t}$, the operator can become part of its own operand. Once such a skill is in turn improved, we recover the self-referential loop in which the improver evolves together with the system it improves [^256] [^261] [^264].

Later sections describe how skills are serialized in recent works: as tools (Section 6.3), as memory workflows (Section 6.2); the application sections illustrate how acquired skills are invoked and reused across tasks.

### 3.3 Connections to Related Learning Paradigms

Because the SI-FMA paradigm is deeply rooted in established learning paradigms, examining it through the lens of these foundational theories offers critical insights. We map SI-FMA onto classical frameworks to clarify where self-improving FM-based agents inherit existing assumptions, where they recombine familiar mechanisms, and where agent architecture makes these mechanisms operationally distinct in practice.

Relation to Reinforcement Learning (RL). Classical reinforcement learning provides a natural reference frame for SI-FMA: it formalizes how an agent improves its policy through interaction, and recent work on Agentic RL [^401] extends this view to foundation-model-based agents. Mapping SI-FMA onto this frame clarifies which channels of self-improvement inherit standard RL machinery and which lie outside its formulation. Specifically, updates to $\theta$ correspond to standard policy optimization under a fixed decision process, whereas updates to $\Sigma$ lie outside the standard RL formulation, reshaping the decision process in which the policy operates.

- Parameter updates ($\theta$). When improvement targets the foundation model parameters using interaction trajectories, the process aligns with standard policy optimization. The foundation model acts as a large-scale policy network $\pi_{\theta}$, and techniques such as RLHF [^45] [^202] or self-play optimize $\pi_{\theta}$ via algorithms like Proximal Policy Optimization (PPO) [^272] or Direct Preference Optimization (DPO) [^227].
- Scaffolding updates ($\Sigma$). When improvement targets the scaffolding, the agent performs a form of structural meta-learning that has no direct counterpart in classical RL. First, whereas classical RL assumes a fixed action space and state representation, updating $\Sigma$ (e.g., adding tools or modifying memory) dynamically alters the effective state-action space and the observation processing logic, thereby reshaping the underlying Markov decision process (MDP) itself. Second, the optimization target itself differs in kind: $\Sigma$ comprises discrete, structured artifacts such as prompts, memory entries, and routing rules, which are typically updated through search, generation, or symbolic edits rather than gradient descent, and which remain explicit and inspectable rather than absorbed into network weights.

SI-FMA also departs from classical RL along a second axis: the source of the learning signal. While classical RL relies on external scalar rewards, self-improving agents increasingly utilize self-generated supervision, where the agent acts as its own critic to synthesize feedback signals from its own trajectories, judgments, or verifier modules.

Relation to Online Learning. Online learning [^167] [^117] studies sequential decision or prediction under a data stream [^216], where the learner updates each round and performance is assessed through cumulative loss or regret. SI-FMA intersects with this view when an agent is updated repeatedly during deployment and evaluation tracks an improvement trajectory rather than a single endpoint, though it is not restricted to the online setting—many self-improvement pipelines operate in batched or offline regimes. Where the paradigms meet, the two channels relate to online learning asymmetrically: $\theta$ updates recover the classical view of updating a hypothesis under a non-stationary stream, whereas $\Sigma$ updates enact a system-level analogue that shifts adaptation to explicit, inspectable components.

- Parameter updates ($\theta$). These inherit the standard stability challenges of online learning, including distribution shift and catastrophic forgetting. Systems mitigate these risks through controlled update operators such as replay or rehearsal [^238], regularization [^142] [^229], parameter-efficient tuning [^120], and explicit versioning with rollback.
- Scaffolding updates ($\Sigma$). These provide a channel for rapid adaptation through prompting policies, memory read-write rules, tool routing, and orchestration logic. Externalizing adaptation in this way improves transparency and control, but does not eliminate forgetting and introduces its own failure modes such as memory poisoning, drift in tool semantics, and brittle template dependence.

Relation to Active Learning. Active learning studies how a learner selects queries under a labeling budget to maximize information gain, typically by requesting labels from an external oracle [^233]. SI-FMA intersects with this view when an agent actively controls its data-acquisition process—for example, by targeting frequent failure modes, seeking environments that maximize verifier disagreement, or explicitly requesting human feedback. However, because modern agents often rely on self-generated verification or critiques rather than oracle labels, this behavior transcends standard active learning. It connects SI-FMA directly to classical artificial-curiosity frameworks, in which systems are explicitly designed to actively construct experiments that maximize learning progress, Bayesian surprise, or compression progress [^258] [^300] [^266] [^268] [^115]. This perspective places self-improvement within a broader family of curiosity-driven exploration mechanisms, emphasizing that the key design choices are the query policy, the intrinsic objective, and the trustworthiness of the resulting feedback.

## 4 A Taxonomy of Existing Approaches

Building on the definitions introduced in Section 3, we now introduce a taxonomy to organize existing approaches to self-improvement in FM-based agents. This section serves as a *methodological classification* that provides a common reference frame for comparing a rapidly growing and heterogeneous literature. In the remainder of this section, we use $\operatorname{\mathtt{IMPROVE}}_{target}(\,\cdot\,;\mathcal{S}_{t})$ to denote an abstract self-improvement procedure in the sense of SI-FMA. Here $\mathcal{S}_{t}$ denotes an update signal produced through the agent’s own execution (the operator $\mathcal{E}$ in Section 3), such as interaction trajectories, critiques, preferences, or other self-generated artifacts. This notation organizes existing approaches first by the target of modification, separating foundation-model updates from scaffolding updates. Within each target, approaches are further distinguished by the form of the self-induced learning signal that drives the update. For scaffolding improvement, we additionally group methods by the scaffold component being modified, such as prompts, memory, tools, or full scaffolding.

### 4.1 Foundation Model Improvement

Foundation model improvement targets the parameters of the underlying foundation model while leaving the agent-level scaffold unchanged:

$$
\theta_{t+1}=\operatorname{\mathtt{IMPROVE}}_{\theta}(\theta_{1:t};\mathcal{S}_{t}),\qquad\Sigma_{t+1}=\Sigma_{t}.
$$

In this paradigm, the agent’s own execution under its induced policy $\pi_{\theta_{t},\Sigma_{t}}$ generates learning signals that are subsequently consumed by a parameter-update procedure. By committing the update directly into $\theta_{t}$, the agent internalizes the learned capabilities. This allows the adaptation cost to be amortized across future interactions, though such parametric updates typically operate on longer time scales and incur higher computational overhead. $\theta_{1:t}$ denotes the parameter history, enabling validation and rollback (e.g., reverting to a prior checkpoint) when a proposed update degrades performance or violates constraints.

##### Classification by signal form.

As detailed in Section 5, we further categorize foundation model improvement according to the form of the self-induced signal $\mathcal{S}_{t}$:

- Intrinsic Generative Demonstrations (primary update signal: $\mathcal{D}_{t}$): the agent synthesizes explicit training instances (e.g., demonstrations or augmented datasets) that are used for supervised-style learning [^335] [^179] [^418] [^277].
- Intrinsic Evaluative Feedback (primary update signal: $e_{t}$): the agent constructs supervisory signals such as scalar rewards, preference pairs, or critiques to guide optimization and alignment [^93] [^126] [^19] [^22] [^398].
- Extrinsic Exploratory Experience (primary update signal: $\tau_{t}$): the agent learns from interaction trajectories and environment-grounded outcomes produced during execution [^342] [^61] [^48] [^305].

### 4.2 Scaffolding Improvement

Scaffolding improvement targets the agent’s operational scaffold while keeping the foundation model parameters fixed:

$$
\Sigma_{t+1}=\operatorname{\mathtt{IMPROVE}}_{\Sigma}(\Sigma_{1:t};\mathcal{S}_{t}),\qquad\theta_{t+1}=\theta_{t}.
$$

Here, $\operatorname{\mathtt{IMPROVE}}$ commits structural changes into $\Sigma_{t}=(p_{t},m_{t},\mathcal{T}_{t},g_{t})$, thereby reshaping how the frozen model is conditioned, grounded, and constrained during all subsequent executions. This paradigm typically yields fast, reversible, and task-specific adaptation without the risks of catastrophic forgetting.

##### Classification by scaffold component.

Crucially, each of the following modifications represents a structural update to the agent’s intrinsic configuration, distinguishing it from transient shifts in working memory. As detailed in Section 6, we further decompose scaffolding improvement according to which component of $\Sigma_{t}$ is targeted:

- Prompt Optimization ($p_{t}\rightarrow p_{t+1}$): edits to structured prompts or in-context exemplars, $p_{t+1}=\operatorname{\mathtt{IMPROVE}}_{p}(p_{1:t};\mathcal{S}_{t})$ [^391] [^101] [^78] [^430].
- Memory Evolution ($m_{t}\rightarrow m_{t+1}$): updates to how experience is stored, consolidated, and retrieved, $m_{t+1}=\operatorname{\mathtt{IMPROVE}}_{m}(m_{1:t};\mathcal{S}_{t})$ [^44] [^341] [^400] [^425].
- Tool Governance ($\mathcal{T}_{t}\rightarrow\mathcal{T}_{t+1}$): refinement or expansion of the agent’s action space through tool creation or selection, $\mathcal{T}_{t+1}=\operatorname{\mathtt{IMPROVE}}_{\mathcal{T}}(\mathcal{T}_{1:t};\mathcal{S}_{t})$ [^106] [^329] [^61] [^411].
- Full Scaffolding Update ($\Sigma_{t}\rightarrow\Sigma_{t+1}$): holistic reconfiguration of the agent’s operational architecture, $\Sigma_{t+1}=\operatorname{\mathtt{IMPROVE}}_{\Sigma}(\Sigma_{1:t};\mathcal{S}_{t})$ [^121] [^405] [^197] [^359].

## 5 Foundation Model Improvement

Input: Initial agent state $\mathcal{A}_{0}=(\theta_{0},\Sigma)$; maximum iterations $T$ Output: Improved agent $\mathcal{A}_{T}=(\theta_{T},\Sigma)$ for *$t\leftarrow 0$ to $T-1$* do        // 1) Construct or collect learning signal $\mathcal{S}_{t}$     $\mathcal{S}_{t}\leftarrow\emptyset$    if *subcategory includes intrinsic generative demonstrations* then        $\mathcal{S}_{t}\leftarrow\mathcal{S}_{t}\cup\textsc{GenerateDemonstrations}(\mathcal{A}_{t})$;        // §5.1           if *subcategory includes intrinsic evaluative feedback* then        $\mathcal{S}_{t}\leftarrow\mathcal{S}_{t}\cup\textsc{GenerateEvaluativeFeedback}(\mathcal{A}_{t})$;        // §5.2           if *subcategory includes extrinsic exploratory experience* then        $\mathcal{S}_{t}\leftarrow\mathcal{S}_{t}\cup\textsc{CollectExperience}(\mathcal{A}_{t},\text{env})$;        // §5.3               // Optional: quality control / weighting of signals     $\mathcal{S}_{t}\leftarrow\textsc{FilterOrWeight}(\mathcal{S}_{t})$    // 2) Parameter update     $\theta_{t+1}\leftarrow\textsc{Update}(\theta_{1:t},\mathcal{S}_{t})$    // 3) State update     $\mathcal{A}_{t+1}\leftarrow(\theta_{t+1},\Sigma)$    if *Converged($\mathcal{A}_{t+1}$)* then       break     return *$\mathcal{A}_{T}$* Algorithm 1 Foundation-Model Improvement

Foundation-model-based self-improvement constitutes one of the most direct pathways for enhancing an agent’s intrinsic capabilities. This approach targets the agent’s core, namely the parameter set $\theta_{t}$ of its underlying FM, and updates these parameters to internalize new behaviors and reasoning patterns [^335] [^19] [^273] [^22] [^61] [^340] [^429]. Such updates are typically achieved through gradient-based optimization, resulting in stable changes to the model weights. In this sense, the FM is treated as a continually learnable system that stores improvements in its parametric memory, rather than relying solely on transient execution states. Because the model parameters compress the agent’s learned representations and behavioral priors, updating them allows the agent to fundamentally refine its policy, reduce systematic errors, and improve alignment with target objectives. In practice, the agent effectively serves as its own source of supervision: it uses its own execution to generate training signals—such as demonstrations, evaluations, or interaction trajectories—and applies learning algorithms to these self-induced signals to systematically improve its capabilities over successive updates.

To systematically analyze FM-based self-improvement, we classify existing methods by the nature of how the learning signal $\mathcal{S}_{t}$ is used to update the foundation-model parameters under our formalism. Consistent with the history-aware operator in Section 3, we write the transition as $\mathcal{A}_{t+1}=\text{IMPROVE}(\mathcal{A}_{1:t};\mathcal{S}_{t})$ with $\theta_{t+1}=\text{IMPROVE}_{\theta}(\theta_{1:t};\mathcal{S}_{t})$ and $\Sigma_{t+1}=\Sigma_{t}$, allowing validation and rollback to prior checkpoints when necessary. This taxonomy yields three principal subcategories: (i) Intrinsic generative demonstrations (§5.1), where the learning signal is instantiated as $\mathcal{S}_{t}\approx\mathcal{D}_{t}$: the FM-based agent generates explicit examples, demonstrations, or task–solution pairs that are used for parameter updates. (ii) Intrinsic evaluative feedback (§5.2), where the learning signal is instantiated as $\mathcal{S}_{t}\approx e_{t}$: the FM-based agent or an internal evaluator judges candidate behavior through scores, preferences, confidence estimates, consistency signals, critiques, or revisions, which are then used to update the foundation model. (iii) Extrinsic exploratory experience (§5.3), where the learning signal is instantiated as $\mathcal{S}_{t}\approx\tau_{t}$: the agent collects trajectories, rewards, observations, or executable outcomes through interaction with external or simulated environments. These subcategories are not mutually exclusive in deployed systems. Many practical pipelines mix intrinsic demonstrations, intrinsic evaluations, and exploratory experience within a single improvement cycle; for clarity, we categorize methods by the dominant signal source and objective used in their update operator. Algorithm 1 summarizes the generic update loop of foundation-model improvement under self-generated learning signals.

![Refer to caption](https://arxiv.org/html/2607.13104v1/x5.png)

Figure 6: Overview of foundation model improvement under agent-induced learning signals. The agent improves the foundation model by generating intrinsic demonstrations, producing intrinsic evaluative feedback, or collecting extrinsic exploratory experience, each forming a distinct parameter-update loop.

### 5.1 Intrinsic Generative Demonstrations

The remarkable capabilities of modern foundation models are fundamentally driven by their massive parameter scales, which inherently demand vast quantities of high-quality training data to continuously optimize and align [^418] [^80]. The methods in this category fall into the group of internal generative processes, where FMs act simultaneously as the cognitive learner and the data synthesizer [^418] [^441]. Leveraging the semantic priors already compressed within their weights, FM-based agents can autonomously construct intrinsic generative demonstrations in forms such as instruction-response pairs, reasoning trajectories, and execution logs, without requiring new external observations [^418] [^277] [^290]. By casting the agent as its own data provider, this paradigm shifts the bottleneck of parameter updates from the costly acquisition of human annotations to the design of effective generation strategies and internal filtering mechanisms [^220].

Formally, as illustrated in Fig. 6 (a), under foundation-model improvement we treat these intrinsic generative demonstrations as the learning signal, i.e., $\mathcal{S}_{t}\approx\mathcal{D}_{t}$. At iteration $t$, the agent state $\mathcal{A}_{t}=(\theta_{t},\Sigma_{t})$ induces a generative distribution $\mathcal{P}_{\mathrm{gen}}(x,y\mid\mathcal{A}_{t})$ and samples an intrinsic dataset

$$
\mathcal{D}^{\mathrm{gen}}_{t}=\{(x_{i},y_{i})\}_{i=1}^{n_{t}}\sim\mathcal{P}_{\mathrm{gen}}(\cdot\mid\mathcal{A}_{t}).
$$

Optionally, a quality-control operator $\Phi_{t}$ filters or weights examples [^136] to yield $\tilde{\mathcal{D}}^{\mathrm{gen}}_{t}=\Phi_{t}(\mathcal{D}^{\mathrm{gen}}_{t})$. The effective training set (and hence the learning signal) is then $\mathcal{D}_{t}=\mathcal{D}^{\mathrm{base}}_{t}\cup\tilde{\mathcal{D}}^{\mathrm{gen}}_{t}$, where $\mathcal{D}^{\mathrm{base}}_{t}$ denotes any existing data.

The parameter update can be written compactly as $\theta_{t+1}=\operatorname{\mathtt{IMPROVE}}_{\theta}(\theta_{1:t};\mathcal{D}_{t})$, where $\operatorname{\mathtt{IMPROVE}}_{\theta}$ denotes the outcome of optimizing an empirical objective on $\mathcal{D}_{t}$ (typically initialized at the current active checkpoint $\theta_{t}$). We write this objective as $\mathcal{L}(\theta;\mathcal{D}_{t})$, with $\Omega(\theta,\theta_{0})$ an optional regularizer around an initialization $\theta_{0}$ and $\lambda\geq 0$ its coefficient:

$$
\theta_{t+1}=\arg\min_{\theta}\;\mathcal{L}(\theta;\mathcal{D}_{t})+\lambda\,\Omega(\theta,\theta_{0}).
$$

In practice, $\operatorname{\mathtt{IMPROVE}}_{\theta}$ is implemented via iterative fine-tuning with a gradient-based optimizer. Let $\theta_{t}^{(0)}=\theta_{t}$, and let $\mathcal{B}_{t}^{(k)}$ denote a minibatch drawn from $\mathcal{D}_{t}$ according to the weighting induced by $\Phi_{t}$. Using step size $\eta_{k}$ at inner step $k$ and the gradient operator $\nabla_{\theta}$ with respect to $\theta$, for $k=0,\dots,K_{t}-1$,

$$
\theta_{t}^{(k+1)}=\theta_{t}^{(k)}-\eta_{k}\,\nabla_{\theta}\mathcal{L}\big(\theta_{t}^{(k)};\mathcal{B}_{t}^{(k)}\big),
$$

and the outer-loop update is $\theta_{t+1}=\theta_{t}^{(K_{t})}$. To systematically explore this approach, we consider three key aspects: the strategy used to generate these intrinsic demonstrations, the format of the generated data, and the challenges that arise in closing the self-improvement loop.

##### Generation strategies.

The strategy of data generation is a critical factor for the quality and scalability of a self-improvement loop. The underlying techniques start with a small set of example seeds and then build a larger instruction-output pair corpus.[^335] [^418]. Methods such as Evol-Instruct [^363] go beyond simple volume expansion. They drive complexity evolution by using LLM to rewrite instructions and gradually increase the difficulty of the instructions, thereby overcoming the limitations of humans in building highly complex scenes. To improve data quality, more sophisticated methods have added a refining or filtering stage. [^124] employs self-consistency to filter high-confidence inference paths, while [^292] uses external verifiers like unit tests to select only correct solutions from the model’s attempts. In addition to bootstrapping and filtering, some approaches conceptualize data generation as a form of curriculum learning. [^290] create a learning curriculum by recursively decomposing complex problems into simpler sub-problems, and [^220] explicitly introduce mechanisms to expand the sample pool to counteract the risk of diminished output diversity over time. More recently, Test-Time Self-Improvement (TT-SI) [^2] shifts the paradigm from massive offline generation to highly sample-efficient, on-the-fly adaptation. By detecting weak cases at inference time via uncertainty estimation, the agent self-generates targeted training examples for its specific blind spots and performs targeted low-rank adaptation (LoRA) fine-tuning; this yields immediate, per-instance improvements with a fraction of the data cost.

Each of these strategies has distinct strengths and failure modes. For example, self-consistency filtering rests on the assumption that correct reasoning tends to be self-agreeing. It can break down when the model is confidently wrong, because repeated reasoning may repeatedly converge to the same incorrect conclusion [^33] [^104]. Curriculum-based generation can significantly improve learning performance for complex tasks, but it becomes vulnerable when the chosen decomposition method is flawed or ignores necessary contextual information. For example, this can occur when the subproblems are constructed in a way that no longer preserves the constraints of the original task [^426] [^363]. Interactive refinement also depends on the model’s ability to detect and correct its own errors. When certain types of errors are beyond the model’s perception range, the improvement process may exacerbate these errors rather than eliminate them [^279] [^125]. Therefore, choosing an appropriate generative strategy requires matching the method to the model’s current capabilities while avoiding mechanisms that focus on or amplify existing blind spots in the model.

##### Data formats.

These intrinsic demonstrations take various forms, ranging from simple input-output pairs to complex, structured artifacts designed to supervise specific cognitive abilities. Basic forms include simple instruction-response pairs, often with explicit reasoning traces added (e.g., chain-of-thought explanations) to make the model’s intermediate reasoning steps transparent and trainable [^124]. However, in scenarios involving multi-step decision-making or tool usage, agents often struggle with long-term tasks because suboptimal behaviors accumulate, eventually causing them to deviate from the correct path. To address this issue, the generated data should capture structured trajectories, rather than the final result. For example, tool application programming interface (API) calls or code execution sequences, combined with intermediate environment feedback and validation labels [^277] [^292], can provide fine-grained supervision, teaching agents how to handle dependencies and recover from errors.

This inherent generative paradigm also extends to multimodal scenarios, where agents synthesize training samples, combining visual inputs such as images or videos with textual descriptions and reasoning to improve performance on tasks including visual reasoning [^412]. At a higher level of abstraction, these demonstrations can take the form of metacognitive artifacts. For example, decomposed problem trees [^290] and self-editing instructions [^441], both of which can support complex planning and self-modification. More generally, the choice of data format should be consistent with the target capability, as different formats encode different types of supervisory information. Inference trajectories are suited for logical reasoning, code combined with tests is well-suited for programming, and structured action logs provide supervision for tool usage.

##### Challenges and safeguards.

This intrinsic generative paradigm still faces considerable challenges despite its success. First, recursively training the model on the generated corpus introduces the risk of model collapse and forgetting [^283] [^282]. If the model generates defective, biased, or erroneous samples, it will internalize these errors during fine-tuning, creating a negative feedback loop that degrades model performance [^418] [^335]. Insufficient diversity in generated demonstrations also narrows the solution space and leads to pattern collapse during iterations. In fact, agents may get trapped in knowledge bubbles and repeatedly generate data, which reinforces their existing biases and traits instead of generating genuine new capabilities [^353] [^390].

To make these inherent generation loops more stable and reliable, several safeguards have been proposed. A simple and effective safeguard is to retain artificially generated benchmark data and accumulate generated demonstration data on top of it, which can prevent collapse under repeated training [^88]. Another work strengthens quality control by using more robust checkers to verify generated samples. These checkers include external validators specifically designed for model-generated content [^381] and formal systems for inference verification, such as theorem provers [^150]. Complementary data-centric safeguards focus on selecting and filtering the training corpus to remove low-quality or harmful examples. To address diversity loss and pattern collapse, diversity-aware pooling expansion and selection mechanisms have been shown to maintain exploratory nature during the iterative process [^220]. Furthermore, shifting from large-scale offline generation to proactive, uncertainty-driven generation during testing naturally mitigates the accumulation of redundant data by focusing computational resources only on out-of-distribution or challenging samples [^2]. Finally, because automated evaluators and validation processes can be unreliable or drift over time, recent research emphasizes human auditing and human-computer interaction to improve evaluation criteria as practical safeguards [^56] [^59].

### 5.2 Intrinsic Evaluative Feedback

Just as massive parameter scales demand vast quantities of demonstration data, aligning and refining these capabilities requires high-quality supervisory signals. The bottleneck in traditional supervisory signal acquisition lies in the high cost of manually labeled preferences and human evaluation. To overcome this limitation, the methods in this category drive a paradigm shift by reframing the acquisition of supervision as an internal evaluative process. In this regime, FMs act not only as the output generator and the self-evaluator, but ultimately as the cognitive learner that internalizes its own judgments. Leveraging their language-native capabilities to follow rubrics, compare alternatives, and articulate reasoning, FM-based agents can autonomously produce intrinsic evaluative feedback, such as scalar scores, preference pairs, consistency signals, and natural language critiques, without requiring new environment interaction. Unlike intrinsic generative demonstrations (Section 5.1) that provide examples, or extrinsic exploratory experience (Section 5.3) derived from environment-grounded outcomes, the dominant learning signal here is the agent’s endogenous judgment of its own candidate behaviors. By treating the agent as a critic of itself, this paradigm shifts the bottleneck of parameter updates to the design of robust internal evaluation rubrics and critique mechanisms.

Formally, let $\mathcal{A}_{t}=(\theta_{t},\Sigma_{t})$ denote the current agent configuration. Given an input or task context $x$, the agent samples a set of candidate outputs

$$
\mathcal{Y}_{t}(x)=\{y_{t}^{(1)},\ldots,y_{t}^{(K)}\},\qquad y_{t}^{(k)}\sim\pi_{\theta_{t},\Sigma_{t}}(\cdot\mid x).
$$

An intrinsic evaluator $\phi_{t}$, which may be implemented by the current model, an auxiliary judge model, a learned reward model, or a fixed scaffolded critique procedure, maps the task, candidates, and evaluation criteria $\kappa_{t}$ into an evaluative signal:

$$
e_{t}=\phi_{t}(x,\mathcal{Y}_{t}(x);\kappa_{t}).
$$

Here, $\phi_{t}$ is the source of feedback rather than the target of the update in this subsection. When an auxiliary evaluator is itself trained, we treat it as part of the feedback-construction pipeline; the method is classified here because the resulting evaluative signal is used to update the foundation model. The signal $e_{t}$ may instantiate a scalar reward $r_{t}$, a preference relation $y^{+}\succ y^{-}$, a confidence or uncertainty score, a textual critique $c_{t}$, or a refined target $y_{t}^{\ast}$. Under foundation-model improvement, this feedback becomes the update signal, $\mathcal{S}_{t}\approx e_{t}$, and the parameter update is written as

$$
\theta_{t+1}=\operatorname{\mathtt{IMPROVE}}_{\theta}(\theta_{1:t};e_{t}),\qquad\Sigma_{t+1}=\Sigma_{t}.
$$

Depending on the form of $e_{t}$, the update may be implemented through reinforcement learning, preference optimization, reward-model training, critique-conditioned fine-tuning, or supervised fine-tuning on revised outputs.

##### Rubric feedback.

A first family of methods derives evaluative feedback by asking a model to judge candidate outputs against explicit criteria. The criteria may be task instructions, grading rubrics, safety principles, constitutional rules, or domain-specific preferences. In this setting, the evaluation standard $\kappa_{t}$ serves as the context for judgment: candidate outputs are scored, ranked, or compared according to how well they satisfy the stated criteria. The evaluator may also produce a brief rationale for its judgment, but the primary learning signal is the score, ranking, or preference relation rather than an open-ended revision.

Constitutional AI is a representative early example of this pattern. Instead of relying only on direct human preference labels, the model critiques and ranks outputs according to a set of written principles, producing AI feedback that can be used to train a preference model and subsequently optimize the policy through reinforcement learning [^19]. Recent self-improvement methods extend this judge-based loop more directly into parameter-updating systems. Meta-Rewarding trains a model to act, judge its own responses, and further evaluate its own judgments, turning both judgments and meta-judgments into preference pairs for iterative alignment improvement [^352]. [^289] show that LLM judges can provide reward signals without reference solutions, enabling reinforcement learning from model-generated judgments in reasoning domains where programmatic rewards are difficult to specify. Self-Evolved Reward Learning further studies a learned reward model that labels additional data for its own improvement and supports reinforcement learning from self-feedback [^122]. Together, these methods illustrate how explicit principles, rubrics, or judge prompts can transform natural-language evaluation standards into scalable supervision for foundation-model improvement. The main advantage is flexibility, since the same model-based evaluator can be conditioned to assess helpfulness, harmlessness, factuality, reasoning quality, or format compliance. The main limitation is reliability, since ambiguous criteria or biased judges may reward superficial compliance rather than genuine improvement.

##### Consistency feedback.

A second family of methods exploits the stochastic behavior of foundation models to derive feedback signals for self-improvement. When ground-truth labels or reliable external verifiers are unavailable, the agent can generate multiple candidate solutions for the same task and use agreement among them as an intrinsic signal. The underlying assumption is not that consistency guarantees correctness, but that agreement, entropy, or self-certainty can provide a useful weak signal for ranking or weighting candidates.

Concretely, the agent samples $\mathcal{Y}_{t}(x)=\{y_{t}^{(1)},\ldots,y_{t}^{(K)}\}$ and applies an aggregation operator $C$ to produce a confidence or reward-like signal:

$$
e_{t}=C(\mathcal{Y}_{t}(x)).
$$

For example, majority voting can identify a consensus answer, predictive entropy can be used as a confidence score, and agreement among independent reasoning paths can be used to construct preference or reward signals. TTRL [^440] uses majority voting over multiple generated answers at test time to produce reward signals for reinforcement learning. SRT [^273] similarly investigates whether self-consistency can support self-improvement without ground-truth labels. EMPO [^408] encourages reasoning behavior through entropy-based signals, while INTUITOR [^420] uses self-certainty as an intrinsic reward. In these methods, the agent does not primarily learn from newly generated demonstrations; rather, it learns from evaluative structure extracted from its own distribution over answers.

The strength of this family is that it can be applied broadly, including in domains where labels are expensive and formal verification is unavailable. However, consistency is only a proxy for correctness. If a model is systematically biased or confidently wrong, repeated sampling may amplify the same error. Confidence-derived feedback also depends on calibration: a model’s expressed certainty may not align with actual correctness. These issues make consistency-based self-improvement methods, while useful, quite fragile, especially when model errors are correlated across different samples. [^309] [^77] [^314] [^104].

##### Corrective feedback.

A third family of methods treats natural-language critique or modification itself as the core evaluation outcome. Unlike rubric-based judging (whose main output is a score or preference under a stated criterion), error-correcting feedback methods require the model to identify specific flaws in candidate outputs and propose modifications. Therefore, this feedback is corrective, not merely comparative.

Let $R$ denote a critique-and-revision operator. Given a candidate output $y_{t}$, the agent produces

$$
e_{t}=R(x,y_{t}),
$$

where $e_{t}$ is composed of $c_{t}$ and $y_{t}^{\ast}$, $c_{t}$ is a critique and $y_{t}^{\ast}$ is a revised output. The pair $(y_{t},y_{t}^{\ast})$ can instantiate a preference signal $y_{t}^{\ast}\succ y_{t}$, while the critique $c_{t}$ can be used as explanatory supervision or as a natural-language training signal. “ReST meets react” [^7] combines agentic reasoning and self-training to improve multi-step problem solving. SELF [^179] uses language feedback to iteratively refine generated answers, transforming model-produced critiques and revisions into signals for self-improvement. RISE [^226] uses interaction-based recursive self-reflection and fine-tunes based on improved predictions. Reflect, Retry, Reward [^22] follows a similar loop in which the model reflects on failures, retries the task, and uses the resulting feedback to guide reinforcement learning. The AlphaAllM approach [^313] further integrates search and critique, using model-generated evaluations during the search process to construct stronger training signals. These methods exploit the ability of foundation models to provide semantic, actionable, and informative feedback that is richer than simple scalar rewards. A critique can identify missing constraints, unsupported claims, incorrect reasoning steps, or unsafe implications, thus providing a richer signal for parameter updates. This flexibility also introduces failure modes since the model may produce plausible but incorrect critiques, or learn to satisfy the surface form of the critique rather than its underlying goals. Therefore, critique-based feedback is more reliable for parameter-level self-improvement when combined with safeguards such as comparing the original and modified outputs, filtering low-quality critiques, using heterogeneous critique models, or combining internal critiques with external validation when available.

##### Trade-offs and safeguards.

The advantage of intrinsic evaluation feedback lies in reducing reliance on human annotation and converting the agent’s own output into a learning signal that can be directly used by the parameter update algorithm. Its main risk is that the evaluator is often tightly coupled with the policy to be improved, so this loop may reinforce common blind spots, reward outputs that conform to the model’s existing preferences, overfit superficial evaluation criteria, or become biased with repeated use and reinterpretation of the evaluation criteria. Signals based on confidence and consistency increase vulnerability when the model is poorly calibrated or when there are correlations between its samples. Therefore, reliable use of this paradigm requires safeguards such as separating the generator and evaluator at different checkpoints or model families, maintaining external anchors by retaining human annotations or context-based validation, treating disagreements between evaluators as signals of uncertainty, and regularly reviewing the scoring criteria, rewarding the model, and evaluating quality. In practice, intrinsic evaluation feedback can be viewed as a component of a broader improvement loop, supplemented by demonstrations, external validation, and exploratory experiences, rather than as the only source of supervision.

### 5.3 Extrinsic Exploratory Experience

The preceding two subsections focused on intrinsic self-improvement signals, where the agent improves the foundation model using its own generated demonstrations (§5.1) or evaluative judgments (§5.2). Extrinsic exploratory experience differs in that the learning signal is grounded in what happens after the agent acts. Under our foundation-model improvement formalism, the learning signal is instantiated as experience, $\mathcal{S}_{t}\approx\tau_{t}$, where $\tau_{t}$ denotes trajectories collected by executing the policy $\pi_{\theta_{t},\Sigma_{t}}$ in a task environment or its learned proxy. The parameter update can be written as $\theta_{t+1}=\text{IMPROVE}_{\theta}(\theta_{1:t};\tau_{t})$, with $\Sigma_{t+1}=\Sigma_{t}$. While this view connects self-improvement back to the classical reinforcement learning framework [^288] [^416], experience for foundation-model agents is not just a stream of state-action-reward tuples $(s,a,r,s^{\prime})$. A trajectory may contain web pages, screenshots, code logs, compiler errors, tool calls, and intermediate reasoning traces. Because these artifacts are readable by foundation models, the same experience can be flexibly reused across reinforcement learning, supervised fine-tuning, preference construction, and failure analysis. However, acquiring and utilizing this rich experience introduces distinct difficulties: interaction can be slow or costly, rewards may be sparse or delayed, verifiers can be gamed, and learned world models [^257] [^270] [^193] may produce plausible but counterfactual transitions.

To address these challenges, we organize existing methods by how the exploratory experience is obtained. For interaction with grounded task environments, the agent acts in real, sandboxed, or rule-based task settings, and the learning signal comes directly from the task environment (e.g., state changes, unit tests, or task-specific verifiers). For interaction with simulated proxy environments, a learned world model serves as a proxy for the task environment, generating predicted states, rollouts, or outcomes for policy improvement. Notably, these two modes are not mutually exclusive. In fact, as demonstrated by early controller-world-model architectures [^257], a system may use grounded interaction to collect data and update its world model, and subsequently use simulated interaction to plan, explore, or improve its policy.

#### 5.3.1 Interaction with Grounded Task Environments.

In this mode, the agent learns by directly acting in a task environment. Typical settings include code interpreters for coding agents, web APIs for web agents, mobile user interfaces (UIs) for GUI agents, and physical environments for embodied agents. The learning signal comes from the environment’s response—such as state changes, execution traces, or unit tests. Training then proceeds by collecting these interaction trajectories and updating the foundation-model policy using reinforcement learning methods like PPO [^272], or preference-based objectives like DPO [^227] when successful and unsuccessful trajectories can be contrasted. A useful way to organize this line of work is by the source of feedback:

(1) Programmatic verifiers provide the clearest form of grounded signal. When a task admits an executable check, the agent can be trained without learning a separate reward model. Code generation is the canonical case, since unit tests provide direct pass or fail feedback for proposed programs. Agent-RLVR [^48], for example, uses unit-test outcomes to guide policy optimization, contrasting successful programs against failed attempts. The same pattern extends beyond code whenever an output can be checked by an external procedure, including structured query language (SQL) execution, theorem proving, tool use with checkable post-conditions, and structured tasks with deterministic success criteria.

(2) Learned reward models evaluate trajectories collected from the task environment. In this setting, the task environment naturally produces the trajectory, while the learned evaluator only scores its success. WebRL [^216] trains an outcome-supervised reward model to label web-navigation trajectories automatically, reducing reliance on hand-crafted success criteria or human annotation. UI-Genie [^360] couples policy learning with reward-model refinement, using validated trajectories to train the agent and step-level labels from both successful and failed trajectories to improve the evaluator. Related work such as MobileGUI-RL [^278] adapts Group Relative Policy Optimization (GRPO) to mobile GUI navigation with trajectory-aware advantages and rewards that combine task success with execution efficiency. Across these methods, the feature is that feedback is computed over rich linguistic or visuolinguistic trajectories, which makes it natural to construct rewards, preferences, and step-level supervision from the same interaction record.

A third approach leverages (3) self-generated tasks to acquire grounded experience. In these systems, the agent may propose new tasks or goals, but the learning signal remains extrinsic because candidate solutions are accepted or rejected by execution, verification, or environmental feedback. Absolute Zero [^417] uses self-play to generate tasks and solutions in an open-ended environment, while execution-based validation determines which solutions are retained for learning. ETO [^295] learns more conservatively from contrasts between successful and failed trajectories in fixed environments. These methods blur the boundary between intrinsic and extrinsic signals at the level of task selection, but not at the level of supervision. The agent may choose what to try, while the environment determines whether the attempt succeeds.

Finally, standardized platforms have emerged to facilitate research across these grounded interaction modes. For example, AgentGym [^357] provides unified APIs for interaction, evaluation, and training across multiple agent tasks. Such platforms significantly reduce the engineering cost of iterative experience collection, making it easier to compare reward sources, training objectives, and update procedures under shared environmental feedback.

#### 5.3.2 Interaction with Simulated Proxy Environments

The simulated-interaction mode equips the agent with an internal predictive model of the environment. A typical pipeline first collects interaction trajectories from a task environment, then trains a world model to predict the environment’s response to the agent’s actions [^257] [^103]. Abstractly, this can be written as a learned dynamics model $W(s_{k+1},r_{k}\mid s_{k},a_{k})$, which predicts the next state and reward from the current state and action at step $k$ of a trajectory. The policy can then obtain additional experience by interacting with this learned proxy instead of repeatedly querying the original task environment. This internal simulation improves sample efficiency and reduces the cost or risk of exploration, especially when direct interaction is slow, expensive, or unsafe [^58] [^235].

While classical world models successfully predict transitions over both compact state vectors and raw pixel spaces [^103], what distinguishes foundation-model agents is the extensive prior knowledge embedded in the learned dynamics. In FM-based systems, the world model is typically a generative language, vision-language, or video model that predicts high-dimensional observations—such as the next web page or video frame—in the exact format consumed by the policy. This design offers two practical advantages. First, large-scale generative pretraining provides a powerful prior over environment dynamics, significantly reducing the task-specific interaction needed to fit a useful proxy environment. Second, because generated observations lie in the same representation space as the policy input, simulated experience can be used directly without a separate representation-alignment step. This holds true for both linguistic web models and pixel-space video models like WMPO [^432]. Together, these advantages make FM-based world models effective for planning, trajectory synthesis, and failure analysis.

This pattern is most developed in web navigation, where direct interaction can be slow and search over action sequences can be expensive. WebEvolver [^73] trains a coevolving world model to predict next web observations and uses simulated rollouts to refine the agent policy. WebSynthesis [^83] uses a learned web world model for reversible, search-based trajectory synthesis, while WebDreamer [^99] leverages a web transition model for model-based planning to guide action selection. Beyond web navigation, SPA [^36] learns explicit state-estimation and transition models through self-play fine-tuning, using them to initialize and stabilize downstream policy optimization. In embodied control, WMPO [^432] learns a pixel-space world model and optimizes the policy over imagined rollouts to avoid costly physical trial-and-error. A related direction uses structured memories of prior interaction rather than full generative dynamics. GLoW [^141] maintains a dual-scale textual world memory—consisting of a global frontier of high-value discoveries and local advantage reflections—to guide a Go-Explore-style agent in text-based games, achieving strong performance with 100–800 $\times$ fewer real environment interactions than RL baselines.

##### Challenges.

Across extrinsic exploratory experience, foundation-model agents inherit classical difficulties of RL, including sparse and delayed rewards, low-throughput real interaction, overfitting to imperfect proxy environments. They also introduce failure modes specific to this setting. Reward hacking through language is more readily available than in classical RL: a foundation-model agent can satisfy the literal condition of a verifier (e.g., exploiting prompt loopholes in an LLM judge) without solving the underlying task, because the verifier’s specification is itself a linguistic object that the agent can manipulate. Capability regression arises because extensive RL updates on narrow extrinsic rewards can erode the broader competencies the foundation model acquired in pretraining, a tension absent in agents trained from scratch. Hallucinated dynamics pose a distinctive risk for world-model approaches, since generative simulators can fabricate plausible but incorrect transitions that the policy then learns to exploit. Finally, the linguistic, multimodal nature of trajectories creates a trajectory-length and context-window tension unique to this setting: long-horizon experience must be compressed or summarized to fit within the model’s context before it can be used as a learning signal. Current research therefore emphasizes more reliable extrinsic verifiers and reward models, world models with calibrated uncertainty over their own predictions, and training procedures that update the foundation model on extrinsic experience without sacrificing its general capabilities.

<svg id="S5.SS3.SSS2.Px1.p2.pic1" height="145.02" overflow="visible" version="1.1" viewBox="0 0 600 145.02" width="600"><g style="--ltx-stroke-color:#000000;--ltx-fill-color:#000000;" transform="translate(0,145.02) matrix(1 0 0 -1 0 0)" fill="#000000" stroke="#000000" stroke-width="0.4pt"><g style="--ltx-fill-color:#002060;" fill="#002060" fill-opacity="1.0"><path style="stroke:none" d="M 0 5.91 L 0 139.12 C 0 142.38 2.64 145.02 5.91 145.02 L 594.09 145.02 C 597.36 145.02 600 142.38 600 139.12 L 600 5.91 C 600 2.64 597.36 0 594.09 0 L 5.91 0 C 2.64 0 0 2.64 0 5.91 Z"></path></g><g style="--ltx-fill-color:#F5F6F9;" fill="#F5F6F9" fill-opacity="1.0"><path style="stroke:none" d="M 1.97 5.91 L 1.97 120.91 L 598.03 120.91 L 598.03 5.91 C 598.03 3.73 596.27 1.97 594.09 1.97 L 5.91 1.97 C 3.73 1.97 1.97 3.73 1.97 5.91 Z"></path></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 21.65 129.51)"><foreignObject style="--ltx-fg-color:#FFFFFF;--ltx-fo-width:40.23em;--ltx-fo-height:0.69em;--ltx-fo-depth:0.19em;" width="556.69" height="12.3" transform="matrix(1 0 0 -1 0 9.61)" overflow="visible" color="#FFFFFF"><span id="S5.SS3.SSS2.Px1.p2.pic1.1.1.1.1.1" style="width:40.23em;"><span id="S5.SS3.SSS2.Px1.p2.pic1.1.1.1.1.1.1">Takeaway</span> </span></foreignObject></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 21.65 16.47)"><foreignObject style="--ltx-fg-color:#000000;--ltx-fo-width:40.23em;--ltx-fo-height:6.69em;--ltx-fo-depth:0.19em;" width="556.69" height="95.32" transform="matrix(1 0 0 -1 0 92.63)" overflow="visible" color="#000000"><span id="S5.SS3.SSS2.Px1.p2.pic1.2.2.2.1.1" style="width:40.23em;"><span id="S5.SS3.SSS2.Px1.p2.pic1.2.2.2.1.1.1">This section reviewed parameter-centric FM-based self-improvement, where agents refine their foundation models via intrinsic demonstrations, intrinsic evaluative feedback, or extrinsic experience. This paradigm allows learned behaviors to be broadly encoded into foundation model weights. However, success depends on managing the reliability of self-generated signals, mitigating distribution shift, and balancing the computational demands of iterative training.</span></span></foreignObject></g></g></svg>

## 6 Scaffolding Improvement

This section analyzes the scaffolding improvement paradigm for FM-based agents, where we approach this by decomposing the agent’s operational scaffold into core components. This workflow begins with receiving and interpreting instructions, then contextualizes them using internal knowledge and memory, proceeds to executing actions in the world, and ultimately evolves the overall operational structure.

Formally, as established in Section 3, scaffolding improvement corresponds to transitions that modify the operational scaffold while explicitly keeping the foundation-model parameters frozen ($\theta_{t+1}=\theta_{t}$). Driven by an execution-derived learning signal $\mathcal{S}_{t}$ (e.g., task outcomes, critique, or execution errors), the update is formalized as $\Sigma_{t+1}=\operatorname{\mathtt{IMPROVE}}_{\Sigma}(\Sigma_{1:t};\mathcal{S}_{t})$. By maintaining a version history ($\Sigma_{1:t}$), the system inherently supports validation and rollback against harmful modifications across all components. We structure the discussion by increasing depth of architectural intervention. Concretely, we instantiate the scaffolding as $\Sigma_{t}:=(p_{t},m_{t},\mathcal{T}_{t},g_{t})$, where $p_{t}$ denotes the prompt template, $m_{t}$ the internal memory, $\mathcal{T}_{t}$ the external tool set, and $g_{t}$ the control logic. Algorithm 2 summarizes the generic improvement loop across these components:

- Prompt-based improvement (Section 6.1) targets the agent’s input and instruction layer, formalized as $p_{t+1}=\operatorname{\mathtt{IMPROVE}}_{p}(p_{1:t};\mathcal{S}_{t})$. As the primary semantic interface through which the agent perceives its tasks, optimizing the prompt provides a direct way to refine task communication, objectives, and constraints without altering the internal parameters of the foundation model.
- Memory-based improvement (Section 6.2) equips the agent with an evolving internal cognitive resource, updated via $m_{t+1}=\operatorname{\mathtt{IMPROVE}}_{m}(m_{1:t};\mathcal{S}_{t})$. By dynamically storing, pruning, and retrieving past experiences, the agent shifts from memoryless execution to cumulative learning, supporting long-horizon reasoning and trustworthy adaptation.
- Tool-based improvement (Section 6.3) strengthens the agent’s execution interface through the update $\mathcal{T}_{t+1}=\operatorname{\mathtt{IMPROVE}}_{\mathcal{T}}(\mathcal{T}_{1:t};\mathcal{S}_{t})$. By autonomously refining and managing external callable modules (e.g., web search, code interpreters), the agent translates internal decisions into precise, executable actions, effectively extending its capabilities beyond the native limits of the foundation model.
- Full scaffolding improvement (Section 6.4) represents the most profound level of architectural intervention, formalized as $\Sigma_{t+1}=\operatorname{\mathtt{IMPROVE}}_{\Sigma}(\Sigma_{1:t};\mathcal{S}_{t})$. By treating the entire codebase and operational logic as a mutable substrate, the agent dynamically reconfigures how its perception, reasoning, and execution faculties are integrated into a coherent whole.

Crucially, these intervention types are compositional rather than mutually exclusive: a single update can edit multiple scaffold components simultaneously, and full-scaffolding methods naturally subsume component-level edits while adding archive-based exploration and stronger acceptance tests.

Input: Initial agent state $\mathcal{A}_{0}=(\theta,\Sigma_{0})$; max iterations $T$ Output: Improved agent $\mathcal{A}_{T}=(\theta,\Sigma_{T})$ for *$t\leftarrow 0$ to $T-1$* do        // 1) Collect scaffolding learning signal $\mathcal{S}_{t}$     $\mathcal{S}_{t}\leftarrow\textsc{InteractAndEvaluate}(\mathcal{A}_{t},\text{env})$;     // traces, critiques, success/failure, cost        // Optional: quality control / weighting of signals     $\mathcal{S}_{t}\leftarrow\textsc{FilterOrWeight}(\mathcal{S}_{t})$    // 2) Scaffolding update (keep $\theta$ fixed)     if *subcategory = Full scaffolding* then        $\Sigma_{t+1}\leftarrow\operatorname{\mathtt{IMPROVE}}_{\Sigma}(\Sigma_{1:t};\mathcal{S}_{t})$;        // § 6.4            else        $p_{t+1}\leftarrow p_{t}$; $m_{t+1}\leftarrow m_{t}$; $\mathcal{T}_{t+1}\leftarrow\mathcal{T}_{t}$       if *subcategory includes Prompt-based* then           $p_{t+1}\leftarrow\operatorname{\mathtt{IMPROVE}}_{p}(p_{t};\mathcal{S}_{t})$;           // § 6.1                 if *subcategory includes Memory-based* then           $m_{t+1}\leftarrow\operatorname{\mathtt{IMPROVE}}_{m}(m_{t};\mathcal{S}_{t})$;           // § 6.2                 if *subcategory includes Tool-based* then           $\mathcal{T}_{t+1}\leftarrow\operatorname{\mathtt{IMPROVE}}_{\mathcal{T}}(\mathcal{T}_{t};\mathcal{S}_{t})$;           // § 6.3                         $\Sigma_{t+1}\leftarrow(p_{t+1},\,m_{t+1},\,\mathcal{T}_{t+1})$        // 3) State update     $\mathcal{A}_{t+1}\leftarrow(\theta,\Sigma_{t+1})$ return *$\mathcal{A}_{T}$* Algorithm 2 Scaffolding Improvement

### 6.1 Prompt

The prompt serves as the agent’s core behavioral prior, defining how the foundation model parses its environment. Prompt optimization is therefore a central and highly accessible form of scaffolding improvement. While early methods relied on manual heuristic tuning, the field is rapidly developed toward automated, signal-driven improvement loops. Central to this development is the transition from scalar-based feedback to rich, structured linguistic critiques. By leveraging natural-language gradients, these systems now facilitate targeted, iterative updates that mirror the precision of gradient-based optimization in higher-dimensional strategy spaces.

In this section, prompt primarily refers to structural instruction layers that are reused across interactions, such as system prompts or stable policy templates. A closely related line of work optimizes context construction, including exemplar selection, retrieval assembly, and the maintenance of long-term playbooks. Although both are scaffold-level updates, they differ in target: optimizing a system prompt alters the agent’s core behavioral prior, whereas context optimization refines the dynamic conditioning of specific interactions. When discussing representative systems, we will explicitly indicate which object is updated.

As shown in Fig. 7, we categorize prompt refinement methods based on the form and richness of the learning signal $\mathcal{S}_{t}$. This yields four paradigms: (1) Scalar-Feedback Optimization, where $\mathcal{S}_{t}$ is a scalar performance score such as accuracy or reward; (2) Qualitative-Feedback Refinement, where $\mathcal{S}_{t}$ is a natural-language critique or suggestion for providing interpretable revision guidance; (3) Population-Based Evolution, where $\mathcal{S}_{t}$ consists of population-level fitness evaluation and selection signals over a set of candidate prompts; and (4) Textual Gradient Optimization, where $\mathcal{S}_{t}$ is structured directional guidance, often expressed as a textual gradient that specifies how the prompt should be revised. As listed in Table 2, we further summarize representative systems and trade-offs across paradigms.

![Refer to caption](https://arxiv.org/html/2607.13104v1/x6.png)

Figure 7: Prompt refinement as a self-improvement loop and its four paradigms, organized by the learning signal 𝒮 t \\mathcal{S}\_{t}.

#### 6.1.1 Scalar-Feedback Optimization

Early approaches to prompt optimization usually rely on task-level quantitative metrics to evaluate candidates [^430]. The core objective can be formally defined as finding an optimal prompt $p^{*}$ from a discrete space of possible prompts $\mathcal{P}$ that maximizes a scalar performance score (e.g., task accuracy or reward):

$$
p^{*}=\arg\max_{p\in\mathcal{P}}f(p),
$$

where $f(p)$ represents the evaluation function. In the context of our scaffolding improvement framework, this scalar score is used to constitutes the learning signal ($\mathcal{S}_{t}=f(p_{t})$). Considering $\mathcal{S}_{t}$ is non-directional, providing only a magnitude of success without explanatory context, these methods typically rely on structured search algorithms to navigate the discrete text space. APE pioneered this paradigm by using an LLM to propose instruction candidates, subsequently selecting the best one based on empirical evaluation scores via simple search [^430]. Building on this, OPRO formalized a more contextualized search by constructing a meta-prompt that includes a trajectory of previously evaluated prompts alongside their scalar scores, indirectly guiding the LLM to propose higher-scoring candidates in subsequent iterations [^373].

Besides, researchers have adapted advanced derivative-free optimization algorithms to operate strictly on scalar feedback. For instance, RL-based frameworks like RLPrompt treat prompt generation as a discrete reinforcement learning problem, directly optimizing a reward signal derived from downstream task accuracy [^52]. Similarly, to improve the sample efficiency of exploring the discrete text space, methods like InstructZero map prompts into a continuous latent space, leveraging Bayesian Optimization to predict and maximize scalar task rewards efficiently [^34]. Recent systems like BPO (Black-Box Prompt Optimization) further extend this score-driven paradigm to human preference alignment, using scalar preference scores to optimize user inputs without altering the underlying model weights [^41].

#### 6.1.2 Qualitative-Feedback Refinement

Building upon scalar-driven methods, a more nuanced approach focuses on iterative refinement using qualitative, interpretable feedback. Instead of a single score, the learning signal ($\mathcal{S}_{t}$) manifests as a textual critique, error analysis, or natural-language suggestion, denoted as $c_{t}$. This richer signal allows for a targeted revision process, formally modeled as an iterative loop where each new prompt $p_{t+1}$ is a function of the previous prompt $p_{t}$ and its corresponding qualitative feedback $c_{t}$:

$$
p_{t+1}=\text{Refine}(p_{t},c_{t}),
$$

where $c_{t}$ is typically generated by an evaluator or the LLM itself based on historical execution: $c_{t}=\text{Critique}(\text{Output}(p_{t}))$. While foundational paradigms like Self-Refine [^186] and multi-agent debate [^65] demonstrated the power of self-critique for transient output correction, recent scaffolding improvements persist this qualitative feedback to update the agent’s prompting policy or instructional context. One prominent direction leverages error-driven qualitative analysis. Reflexion, for example, enables an agent to generate “verbal introspection” upon task failure, storing these qualitative reflections in memory to explicitly guide and constrain subsequent prompting attempts [^279]. Expanding on this diagnostic capability, MAPS introduces an automated, LLM-tailored prompt optimization framework that explicitly induces and validates reusable natural-language rules from failure cases. By iteratively injecting these qualitative insights into the prompt, MAPS substantially optimizes the policy for complex tasks like unit test generation [^82]. Similarly, inspired by Chain of Hindsight (CoH), agents can learn from textual contrasts by reviewing a history of past attempts accompanied by qualitative evaluations [^170]. Another critical direction involves evolving the instructional context. To manage the growing complexity of text-based critiques, ACE introduces an agentic context engineering framework with a modular Generator–Reflector–Curator pipeline. ACE treats prompts and memory as evolving text playbooks, actively curating qualitative feedback while mitigating brevity bias and context collapse [^409]. In specific domain applications, systems like Scrable utilize continuous qualitative evaluation to iteratively refine the structural system prompt for customer review generation, halting only when the textual quality reaches a predefined standard [^16].

Table 2: Comparison of prompt optimization paradigms in prompt-based self-improvement. As learning signals become more structured and informative, optimization becomes less heuristic and more automated. ①: Scalar-feedback optimization; ②: Qualitative-feedback refinement; ③: Population-based evolution; ④: Textual-gradient optimization.

| ID | Signal $\mathcal{S}_{t}$ | Objective | Representative Systems | Advantages | Limitations |
| --- | --- | --- | --- | --- | --- |
| $\rightarrow$ | lightBlue!12 Scalar score | lightBlue!8 $\arg\max_{p\in\mathcal{P}}f(p)$ | lightBlue!6 RLPrompt [^52] BBT [^303] APE [^430] OPRO [^373] Dspy [^140] | +  Model-agnostic  +  Simple to deploy  +  No internal access | –  Low interpretability  –  Sample-inefficient  –  Sensitive to search |
| $\rightarrow$ | lightBlue!12 Text critique | lightBlue!8 $\text{Refine}(p_{t},c_{t})$ | lightBlue!6 Self-Refine [^186] Reflexion [^279] Critic [^96] ACE [^409] | +  Interpretable edits  +  Targeted correction  +  Reusable feedback | –  Critique can be noisy  –  May drift  –  Validator-dependent |
| $\rightarrow$ | lightBlue!12 Selection signal | lightBlue!8 $\text{Evolve}(P_{t},\text{Fit})$ | lightBlue!6 Promptbreeder [^78] STOP [^392] GPTSwarm [^435] AutoDAN [^174] Evol-Instruct [^363] GEPA [^4] | +  Strong exploration  +  Maintains diversity  +  Escapes local optima | –  Compute-heavy  –  Fitness is domain-tuned  –  Population drift |
| $\rightarrow$ | lightBlue!12 Textual gradient | lightBlue!8 $p_{t}\oplus g(p_{t})$ | lightBlue!6 APO [^213] TextGrad [^391] metaTextGrad [^364] SkillOpt [^379] | +  Directional updates  +  Often sample-efficient  +  Highly automated | –  Brittle gradients  –  Quality varies by LLM  –  Limited guarantees |

#### 6.1.3 Population-Based Evolution

To introduce more structured exploration and mitigate the risk of converging to local optima, researchers have adapted principles from evolutionary biology. In this paradigm, the learning signal $\mathcal{S}_{t}$ manifests as population-level fitness evaluations and selection pressures over a diverse pool of candidate prompts. Formally, these methods treat prompts as “genes” within a population $P_{t}=\{p_{t}^{(i)}\}_{i=1}^{N}$ at generation $t$. The evolutionary update leverages LLMs to apply semantic operators rather than simple string manipulations, following three key steps:

1. Selection: A subset of prompts survives based on a fitness evaluation function, which translates task performance into selection pressure ($\mathcal{S}_{t}$).
2. Crossover: The LLM intelligently merges the semantic strengths of two parent prompts, generating offspring: $p_{\text{child}}=\text{Crossover}(p_{t}^{(i)},p_{t}^{(j)})$.
3. Mutation: The LLM introduces semantic variations to explore new instructional phrasing: $p^{\prime}=\text{Mutate}(p)$.

The subsequent generation, $P_{t+1}$, is formed from the fittest individuals and their offspring. Foundational frameworks like EvoPrompt [^101] pioneered this by explicitly guiding LLMs to act as evolutionary operators, yielding crossover and mutation steps that are semantically meaningful and far surpass classical random character edits. Expanding the depth of this standard evolutionary search, frameworks like Promptbreeder [^78] introduces a profound self-referential mechanism where the LLM evolves not only the task prompts but also the "mutation prompts" (the instructions governing how new offspring are generated). Addressing scenarios where scalar fitness scores are unavailable, DEEVO creatively structures $\mathcal{S}_{t}$ through multi-agent debates, utilizing the win-rate of LLM-driven argumentation as the evolutionary fitness signal [^192]. Crucially, demonstrating the compositional nature of scaffolding improvement, recent work integrates population-based search with qualitative feedback. In reflective prompt evolution frameworks like GEPA [^4], the evolutionary process is guided not merely by a scalar fitness score, but by a meta-level reflection step. After evaluating a generation, a reflector LLM analyzes successes and failures to generate textual critiques. This qualitative feedback explicitly informs the next generation’s mutation and crossover operators, making the search highly targeted and sample-efficient. The success of such hybrid approaches highlights the distinct advantage of replacing opaque scalar rewards with directional, semantic guidance—directly paving the way for the formalized textual gradient methods discussed next.

#### 6.1.4 Textual Gradient Optimization

The most recent paradigm is distinguished by a formal, mathematically-inspired treatment of the feedback signal, drawing direct analogies to gradient descent in continuous optimization. Rather than relying on heuristic edits or scalar search, the learning signal ($\mathcal{S}_{t}$) is formalized as a textual gradient—a structured, directional feedback message that explicitly diagnoses why an output is incorrect and prescribes a precise revision vector. This optimization process can be expressed with an analogous update rule:

$$
p_{t+1}=p_{t}\oplus g(p_{t}),
$$

where the textual gradient $g(p_{t})$ serves directly as our learning signal ($\mathcal{S}_{t}=g(p_{t})$). The $\oplus$ operator denotes a textual update step, where an LLM acts as the optimizer to semantically apply the gradient’s guidance and revise the prompt. While the foundational concept of a “textual gradient” was introduced in Automatic Prompt Optimization (APO) [^213], this direction has been significantly advanced by framing agentic workflows as computational graphs. TextGrad, for instance, operationalized this by introducing automatic differentiation via text, allowing qualitative gradients to backpropagate through complex, multi-component language systems [^391]. Concurrently, semantic backpropagation frameworks have further formalized this process, executing first-order-like optimization on text nodes to achieve principled prompt refinement [^331]. The sophistication of this paradigm is profoundly underscored by meta-level frameworks like MetaTextGrad. Rather than solely optimizing task prompts, it uses an LLM to dynamically optimize the “optimizer prompts” (the instructions dictating how the textual gradients are computed and applied), effectively allowing the agent to self-improve its own improvement process [^364]. Looking forward, this formal feedback mechanism could bridge the gap between scaffolding and parameter-based learning: a textual gradient might be translated into low-rank parameter updates, seamlessly integrating prompt engineering with model fine-tuning.

<svg id="S6.SS1.SSS4.p2.pic1" height="161.63" overflow="visible" version="1.1" viewBox="0 0 600 161.63" width="600"><g style="--ltx-stroke-color:#000000;--ltx-fill-color:#000000;" transform="translate(0,161.63) matrix(1 0 0 -1 0 0)" fill="#000000" stroke="#000000" stroke-width="0.4pt"><g style="--ltx-fill-color:#002060;" fill="#002060" fill-opacity="1.0"><path style="stroke:none" d="M 0 5.91 L 0 155.72 C 0 158.98 2.64 161.63 5.91 161.63 L 594.09 161.63 C 597.36 161.63 600 158.98 600 155.72 L 600 5.91 C 600 2.64 597.36 0 594.09 0 L 5.91 0 C 2.64 0 0 2.64 0 5.91 Z"></path></g><g style="--ltx-fill-color:#F5F6F9;" fill="#F5F6F9" fill-opacity="1.0"><path style="stroke:none" d="M 1.97 5.91 L 1.97 137.52 L 598.03 137.52 L 598.03 5.91 C 598.03 3.73 596.27 1.97 594.09 1.97 L 5.91 1.97 C 3.73 1.97 1.97 3.73 1.97 5.91 Z"></path></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 21.65 146.11)"><foreignObject style="--ltx-fg-color:#FFFFFF;--ltx-fo-width:40.23em;--ltx-fo-height:0.69em;--ltx-fo-depth:0.19em;" width="556.69" height="12.3" transform="matrix(1 0 0 -1 0 9.61)" overflow="visible" color="#FFFFFF"><span id="S6.SS1.SSS4.p2.pic1.2.2.2.1.1" style="width:40.23em;"><span id="S6.SS1.SSS4.p2.pic1.2.2.2.1.1.1">Takeaway</span> </span></foreignObject></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 21.65 16.47)"><foreignObject style="--ltx-fg-color:#000000;--ltx-fo-width:40.23em;--ltx-fo-height:7.89em;--ltx-fo-depth:0.19em;" width="556.69" height="111.93" transform="matrix(1 0 0 -1 0 109.24)" overflow="visible" color="#000000"><span id="S6.SS1.SSS4.p2.pic1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1" style="width:40.23em;"><span id="S6.SS1.SSS4.p2.pic1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1">Prompt-based self-improvement turns prompt optimization from an ad hoc practice into a signal-driven improvement loop. In existing approaches, the learning signal (<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline" data-latex="\mathcal{S}_{t}"><semantics><msub><mi>𝒮</mi> <mi>t</mi></msub> <annotation encoding="application/x-tex">\mathcal{S}_{t}</annotation></semantics></math>) becomes progressively richer, evolving from scalar scores to qualitative critiques, and further to population-level selection and structured directional guidance. As feedback grows in informational content, prompt updates become less heuristic and more targeted, enabling increasingly automated and sample-efficient refinement without changing the foundation-model parameters.</span></span></foreignObject></g></g></svg>

### 6.2 Memory

The memory system serves as the core cognitive scaffolding for long-horizon agentic behavior. Traditional memory architectures often rely on raw content logging alongside fixed schemas, resulting in rigid, static organizations. Such append-only designs quickly succumb to context-window constraints and retrieval degradation, rendering them ill-suited for dynamically changing environments [^190] [^107] [^204]. In contrast, self-improving agents treat memory not merely as a passive storage mechanism, but as an actively evolving scaffold. By continuously assessing the value, relevance, and strength of stored information, these agents autonomously reconstruct and expand their memory representations based on the flow of experience [^66] [^365]. This shift from static storage to dynamic self-organization enhances the agent’s generality, establishing a foundation for open-ended autonomy [^369] [^244] [^162].

To systematically analyze this paradigm, we decompose memory-based improvement into three core dimensions: Memory Objects (the units of stored information), Memory Structure (the topological organization and indexing schema), and Memory Processing (the mechanisms for creation, retrieval, updating, and forgetting). Formally, we conceptualize the memory scaffold as a dynamic state $m_{t}:=(\text{object}_{t},\text{structure}_{t})$, specifying the currently stored objects and their overarching organization. Driven by an execution-derived learning signal $\mathcal{S}_{t}$ (e.g., retrieval failures, task feedback, or capacity limits), memory evolution is formalized as:

$$
m_{t+1}=\text{IMPROVE}m(m_{t};\mathcal{S}t).
$$

This update is instantiated through the memory processing module—a signal-driven family of operations (Write, Read, Update, Delete) parameterized by $\mathcal{S}_{t}$ that governs what to consolidate into $\text{object}_{t+1}$ and how to reorganize $\text{structure}_{t+1}$. Finally, it is crucial to note the scope of our discussion. While some literature considers knowledge internalized within the foundation model’s weights as "parametric memory" [^354] [^110] [^415], this section focuses on non-parametric, externalized memory embedded within the agent’s scaffold, maintaining the core assumption of a frozen foundation model.

![Refer to caption](https://arxiv.org/html/2607.13104v1/x7.png)

Figure 8: Overview of memory for self-improving agent.

#### 6.2.1 Memory Object

Table 3: Memory-object scorecard (qualitative). Blue squares indicate an ordinal, literature-grounded assessment (1=low, 5=high) of typical tendencies for each memory object type, synthesized from representative system designs and reported failure analyses rather than from a single standardized benchmark.

| Object type | Best-for persistence | Fidelity | Interpre- tability | Compact | Write cost | Audit- tability | Most common failure modes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Processed trails | $\bullet$  lessons $\bullet$  routines $\bullet$  summaries |  |  |  |  |  | $\blacktriangleright$  summary bias $\blacktriangleright$  stale heuristics $\blacktriangleright$  weak credit assignment |
| Curated raw content | $\bullet$  evidence $\bullet$  exact artifacts |  |  |  |  |  | $\blacktriangleright$  context bloat $\blacktriangleright$  retrieval noise $\blacktriangleright$  privacy leakage surface |
| Integrated external knowledge | $\bullet$  shared factual state $\bullet$  grounding |  |  |  |  |  | $\blacktriangleright$  grounding failure $\blacktriangleright$  staleness / inconsistency $\blacktriangleright$  tool brittleness |
| Latent embeddings | $\bullet$  associative carryover $\bullet$  fast recall |  |  |  |  |  | $\blacktriangleright$  drift / contamination $\blacktriangleright$  hard-to-debug retrieval $\blacktriangleright$  silent corruption |

Recalling our formal decomposition of memory state, this subsection focuses on $\text{object}_{t}$, i.e., *what* is stored within the agent’s memory scaffold. The design of the memory object is paramount, as it directly governs storage efficiency, representation fidelity, and the capacity for cross-context knowledge transfer [^146]. Moving beyond raw, exhaustive interaction trails (e.g., infinite chat histories), self-improving agents increasingly favor storing processed, high-density abstractions [^230] [^55]. By utilizing execution feedback ($\mathcal{S}_{t}$) to filter or compress experiences, agents effectively mitigate context-window limitations and storage costs [^31]. These memory objects can be fundamentally categorized into explicit and implicit representations.

- Explicit Objects. Explicit objects are human-readable and directly manipulable, which makes them the default choice when interpretability, attribution, and safety auditing are important. Their main advantage is controllability: developers can inspect, correct, and selectively expose them to the model. Their main limitation is scalability, since verbose or weakly curated memories tend to increase retrieval noise and context pressure as the memory grows.
	A first and widely used manifestation stores processed interaction trails that compresses raw trajectories into reusable, semantically meaningful units (e.g., distilled routines, heuristics, or reflections). Driven by task success/failure signals, agents abstract generalizable strategies from experience or maintain note-like intermediate traces to support long-horizon reasoning [^341] [^203] [^148] [^151] [^177].
	A second manifestation retains curated raw content. Certain scenarios require preserving exact surface details that are hard to summarize without loss (e.g., code snippets, formulas, or screenshots). Rather than storing everything, self-improving agents selectively write back only high-value artifacts validated during trial-and-error, distilling dynamic “cheatsheets” for future reuse [^416] [^308].
	A third manifestation integrates external knowledge. Agents can integrate and maintain facts from external repositories. Grounding memory in shared references rather than free-form recollection enhances verifiability. Crucially, unlike static retrieval systems, self-improving agents utilize utility-based feedback to dynamically update, annotate, or prune these retrieved domain references (e.g., codebases or task-specific documents), thereby mitigating error propagation in downstream reasoning [^316] [^406] [^211].
- Implicit Objects. Implicit objects store memory in machine-native latent representations, including latent tokens, hidden states, and key–value cache augmentations. Their primary advantage is compactness and fast associative access, which makes them appealing under strict context limits or latency budgets. Their primary drawback is limited interpretability, which complicates debugging, targeted correction, and safety auditing, and can lead to representation drift when the memory is repeatedly rewritten or composed.
	Recent advancements explore several mechanisms for implicit memory scaffolding without altering the base FM parameters. Generative latent memory constructs latent sequences to enrich reasoning beyond text-based retrieval [^400]. Latent state reconstruction captures and reintegrates hidden representations to improve context retention [^57]. A related line augments the decoding process via offline coprocessors that inject latent embeddings directly into the KV cache to boost generation fidelity [^171] [^304]. Finally, maintaining self-updatable latent memory pools offers a practical compromise between persistent state tracking and strict capacity control [^337] [^338].

##### Trade-offs.

Explicit memory objects offer high interpretability and controllability, simplifying debugging and safety auditing, but require rigorous curation to avoid overwhelming the context budget. Among them, processed trails favor generalization, curated artifacts favor precision, and integrated external knowledge favors verifiability. Conversely, implicit memory objects provide compact, high-speed associative access and mitigate context length issues, but are difficult to inspect, correct, and are susceptible to representation drift over long horizons. We summarize these qualitative trade-offs and common failure modes in Table 3.

![Refer to caption](https://arxiv.org/html/2607.13104v1/x9.png)

Table 4: Memory architecture and processing operators. Checkmarks indicate the memory object and structure choices reported by each system. Dots denote the relative emphasis of a mechanism as primary ( ∙ \\bullet ), secondary ( ), or absent/unclear ( ). Processing is summarized by CRUD (Create, Read, Update, Delete). We further characterize governance along two dimensions: Select, which determines what information is written and retrieved based on saliency and utility, and Maintain, which sustains memory quality over long horizons through consolidation, refresh, and forgetting.

[^1]: LLM-deliberation: evaluating LLMs with interactive multi-agent negotiation game. In ICLR 2024 Workshop on Large Language Model (LLM) Agents, External Links: [Link](https://openreview.net/forum?id=eE1WHn6qlk) Cited by: §8.2.2.

[^2]: Self-improving llm agents at test-time. External Links: 2510.07841, [Link](https://arxiv.org/abs/2510.07841) Cited by: §1, §5.1, §5.1.

[^3]: Agent s: an open agentic framework that uses computers like a human. In The Thirteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=lIVRgt4nLv) Cited by: §7.6.

[^4]: GEPA: reflective prompt evolution can outperform reinforcement learning. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=RQm2KQTM5r) Cited by: §6.1.3, Table 2.

[^5]: TDD-bench verified: can llms generate tests for issues before they get resolved?. External Links: 2412.02883, [Link](https://arxiv.org/abs/2412.02883) Cited by: §8.2.2.

[^6]: AutoRT: embodied foundation models for large scale orchestration of robotic agents. In First Workshop on Vision-Language Models for Navigation and Manipulation at ICRA 2024, External Links: [Link](https://openreview.net/forum?id=DYcCveNeR1) Cited by: §7.5, §7.5.

[^7]: ReST meets react: self-improvement for multi-step reasoning LLM agent. In ICLR 2024 Workshop on Large Language Model (LLM) Agents, External Links: [Link](https://openreview.net/forum?id=7xknRLr7QE) Cited by: §5.2.

[^8]: SWE-bench+: enhanced coding benchmark for llms. External Links: 2410.06992, [Link](https://arxiv.org/abs/2410.06992) Cited by: §7.1, §8.1.1, §8.2.1, §8.2.2.

[^9]: Planning to explore: curiosity-driven planning for llm test generation. arXiv preprint arXiv:2604.05159. Cited by: §7.1.

[^10]: Concrete problems in ai safety. External Links: 1606.06565, [Link](https://arxiv.org/abs/1606.06565) Cited by: §8.1.1.

[^11]: Causal and chronological relationships predict memory organization for nonlinear narratives. Journal of cognitive neuroscience 36 (11), pp. 2368–2385. Cited by: 1st item.

[^12]: Design for a brain: the origin of adaptive behavior. Wiley, New York. Cited by: §2.1.

[^13]: RACAS: controlling diverse robots with a single agentic system. arXiv preprint arXiv:2603.05621. Cited by: §7.5.

[^14]: Human memory: a proposed system and its control processes. In Psychology of learning and motivation, Vol. 2, pp. 89–195. Cited by: 2nd item.

[^15]: Reflection-based memory for web navigation agents. External Links: 2506.02158, [Link](https://arxiv.org/abs/2506.02158) Cited by: §7.2.

[^16]: Self-improving customer review response generation based on LLMs. In Proceedings of the Seventh Workshop on e-Commerce and NLP @ LREC-COLING 2024, S. Malmasi, B. Fetahu, N. Ueffing, O. Rokhlenko, E. Agichtein, and I. Guy (Eds.), Torino, Italia, pp. 40–57. External Links: [Link](https://aclanthology.org/2024.ecnlp-1.5/) Cited by: §6.1.2.

[^17]: PBFT-backed semantic voting for multi-agent memory pruning. Adv Mach Lear Art Inte 6 (3), pp. 01–15. Cited by: §6.2.3.

[^18]: The option-critic architecture. In Proceedings of the AAAI conference on artificial intelligence, Cited by: §3.2.

[^19]: Constitutional ai: harmlessness from ai feedback. arXiv preprint arXiv:2212.08073. Cited by: §2.5, 2nd item, §5.2, §5, §8.1.1.

[^20]: Agents of change: self-evolving llm agents for strategic planning. External Links: 2506.04651, [Link](https://arxiv.org/abs/2506.04651) Cited by: §7.3.

[^21]: Learning a synaptic learning rule. In IJCNN-91-Seattle International Joint Conference on Neural Networks, Vol. ii, pp. 969 vol.2–. External Links: [Document](https://dx.doi.org/10.1109/IJCNN.1991.155621) Cited by: §2.3.

[^22]: Reflect, retry, reward: self-improving llms via reinforcement learning. External Links: 2505.24726, [Link](https://arxiv.org/abs/2505.24726) Cited by: 2nd item, §5.2, §5.

[^23]: Clembench-2024: a challenging, dynamic, complementary, multilingual benchmark and underlying flexible framework for llms as multi-action agents. CoRR abs/2405.20859. External Links: [Link](https://doi.org/10.48550/arXiv.2405.20859) Cited by: §8.2.2.

[^24]: Autonomous chemical research with large language models. Nature 624 (7992), pp. 570–578. Cited by: §7.4.

[^25]: Windows agent arena: evaluating multi-modal OS agents at scale. In Forty-second International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=W9s817KqYf) Cited by: §7.6, §8.2.2.

[^26]: RoboPhD: self-improving text-to-sql through autonomous agent evolution. External Links: 2601.01126, [Link](https://arxiv.org/abs/2601.01126) Cited by: §1.

[^27]: AlignUSER: human-aligned llm agents via world models for recommender system evaluation. External Links: 2601.00930, [Link](https://arxiv.org/abs/2601.00930) Cited by: §1.

[^28]: RoboCat: a self-improving generalist agent for robotic manipulation. Transactions on Machine Learning Research. Note: External Links: ISSN 2835-8856, [Link](https://openreview.net/forum?id=vsCpILiWHu) Cited by: §7.5.

[^29]: AstaBench: rigorous benchmarking of AI agents with a scientific research suite. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=M7TNf5J26u) Cited by: §8.2.2.

[^30]: Large language models as tool makers. In The Twelfth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=qV83K9d5WB) Cited by: §6.3.3.

[^31]: Infiniteicl: breaking the limit of context window size via long short-term memory transformation. In Findings of the Association for Computational Linguistics: ACL 2025, pp. 11402–11415. Cited by: §6.2.1.

[^32]: Clembench: using game play to evaluate chat-optimized language models as conversational agents. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, Singapore, pp. 11174–11219. External Links: [Link](https://aclanthology.org/2023.emnlp-main.689) Cited by: §8.2.2.

[^33]: Two failures of self-consistency in the multi-step reasoning of llms. CoRR abs/2305.14279. External Links: [Link](https://doi.org/10.48550/arXiv.2305.14279) Cited by: §5.1.

[^34]: InstructZero: efficient instruction optimization for black-box large language models. In Forty-first International Conference on Machine Learning, Cited by: §6.1.1.

[^35]: Evaluating large language models trained on code. arXiv preprint arXiv:2107.03374. Cited by: §1.

[^36]: Internalizing world models via self-play finetuning for agentic rl. External Links: 2510.15047, [Link](https://arxiv.org/abs/2510.15047) Cited by: §5.3.2.

[^37]: PhysGym: benchmarking LLMs in interactive physics discovery with controlled priors. In The Thirty-ninth Annual Conference on Neural Information Processing Systems Datasets and Benchmarks Track, External Links: [Link](https://openreview.net/forum?id=w8uII2qAmd) Cited by: §8.2.2.

[^38]: How much can we trust llm search agents? measuring endorsement vulnerability to web content manipulation. arXiv preprint arXiv:2606.16821. Cited by: §7.2.

[^39]: Multi-agent evolve: llm self-improve through co-evolution. External Links: 2510.23595, [Link](https://arxiv.org/abs/2510.23595) Cited by: 2nd item.

[^40]: Xmem: long-term video object segmentation with an atkinson-shiffrin memory model. In European conference on computer vision, pp. 640–658. Cited by: 2nd item.

[^41]: Black-box prompt optimization: aligning large language models without model training. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 3201–3219. Cited by: §6.1.1.

[^42]: Self-playing adversarial language game enhances LLM reasoning. In The Thirty-eighth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=oCGkSH7ys2) Cited by: §7.3.

[^43]: Evolving in tasks: empowering the multi-modality large language model as the computer use agent. External Links: 2508.04037, [Link](https://arxiv.org/abs/2508.04037) Cited by: §7.6.

[^44]: Mem0: building production-ready ai agents with scalable long-term memory. External Links: 2504.19413, [Link](https://arxiv.org/abs/2504.19413) Cited by: §1, 2nd item, 3rd item, §6.2.3.

[^45]: Deep reinforcement learning from human preferences. Advances in neural information processing systems 30. Cited by: 1st item.

[^46]: GraphVideoAgent: enhancing long-form video understanding with entity relation graphs. In Proceedings of the 33rd ACM International Conference on Multimedia, MM ’25, New York, NY, USA, pp. 4639–4648. External Links: ISBN 9798400720352, [Link](https://doi.org/10.1145/3746027.3755537), [Document](https://dx.doi.org/10.1145/3746027.3755537) Cited by: 3rd item.

[^47]: GameBench: evaluating strategic reasoning abilities of LLM agents. In Language Gamification - NeurIPS 2024 Workshop, External Links: [Link](https://openreview.net/forum?id=qrzKE533Jr) Cited by: §8.2.2.

[^48]: Agent-rlvr: training software engineering agents via guidance and environment rewards. External Links: 2506.11425, [Link](https://arxiv.org/abs/2506.11425) Cited by: 3rd item, §5.3.1.

[^49]: ORGANA: a robotic assistant for automated chemistry experimentation and characterization. CoRR abs/2401.06949. External Links: [Link](https://doi.org/10.48550/arXiv.2401.06949) Cited by: §7.4.

[^50]: The evolution of evolvability. In Artificial life, pp. 201–220. Cited by: §6.4.

[^51]: The browsergym ecosystem for web agent research. Transactions on Machine Learning Research. Note: Expert Certification External Links: ISSN 2835-8856, [Link](https://openreview.net/forum?id=5298fKGmv3) Cited by: §7.2.

[^52]: Rlprompt: optimizing discrete text prompts with reinforcement learning. In Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing, pp. 3369–3391. Cited by: §6.1.1, Table 2.

[^53]: SWE-bench pro: can ai agents solve long-horizon software engineering tasks?. CoRR abs/2509.16941. External Links: [Link](https://doi.org/10.48550/arXiv.2509.16941) Cited by: §7.1.

[^54]: Mind2web: towards a generalist agent for the web. Advances in Neural Information Processing Systems 36, pp. 28091–28114. Cited by: §7.2, §8.1.1, §8.2.2.

[^55]: Towards human-centered proactive conversational agents. In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval, pp. 807–818. Cited by: §6.2.1.

[^56]: Principles and guidelines for the use of llm judges. In Proceedings of the 2025 International ACM SIGIR Conference on Innovative Concepts and Theories in Information Retrieval (ICTIR), ICTIR ’25, New York, NY, USA, pp. 218–229. External Links: ISBN 9798400718618, [Link](https://doi.org/10.1145/3731120.3744588), [Document](https://dx.doi.org/10.1145/3731120.3744588) Cited by: §5.1.

[^57]: Contextual memory reweaving in large language models using layered latent state reconstruction. External Links: 2502.02046, [Link](https://arxiv.org/abs/2502.02046) Cited by: 2nd item.

[^58]: Understanding world or predicting future? a comprehensive survey of world models. ACM Computing Surveys 58 (3), pp. 1–38. Cited by: §5.3.2.

[^59]: Generate, evaluate, iterate: synthetic data for human-in-the-loop refinement of llm judges. CoRR abs/2511.04478. External Links: [Link](https://doi.org/10.48550/arXiv.2511.04478) Cited by: §5.1.

[^60]: Helping llms improve code generation using feedback from testing and static analysis. External Links: 2412.14841, [Link](https://arxiv.org/abs/2412.14841) Cited by: §6.3.2.

[^61]: Tool-star: empowering llm-brained multi-tool reasoner via reinforcement learning. External Links: 2505.16410, [Link](https://arxiv.org/abs/2505.16410) Cited by: 3rd item, 3rd item, §5, §6.3.1.

[^62]: Re-ReST: reflection-reinforced self-training for language agents. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, Y. Al-Onaizan, M. Bansal, and Y. Chen (Eds.), Miami, Florida, USA, pp. 15394–15411. External Links: [Link](https://aclanthology.org/2024.emnlp-main.861/), [Document](https://dx.doi.org/10.18653/v1/2024.emnlp-main.861) Cited by: §9.1.

[^63]: WorkArena: how capable are web agents at solving common knowledge work tasks?. In Proceedings of the 41st International Conference on Machine Learning, R. Salakhutdinov, Z. Kolter, K. Heller, A. Weller, N. Oliver, J. Scarlett, and F. Berkenkamp (Eds.), Proceedings of Machine Learning Research, Vol. 235, pp. 11642–11662. External Links: [Link](https://proceedings.mlr.press/v235/drouin24a.html) Cited by: §7.2.

[^64]: WorkArena: how capable are web agents at solving common knowledge work tasks?. In Forty-first International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=BRfqYrikdo) Cited by: §7.2, §8.1.1.

[^65]: Improving factuality and reasoning in language models through multiagent debate. In Proceedings of the 41st International Conference on Machine Learning, ICML’24. Cited by: §6.1.2.

[^66]: Rethinking memory in ai: taxonomy, operations, topics, and future directions. External Links: 2505.00675, [Link](https://arxiv.org/abs/2505.00675) Cited by: §6.2.

[^67]: GTBench: uncovering the strategic reasoning limitations of llms via game-theoretic evaluations. External Links: 2402.12348, [Link](https://arxiv.org/abs/2402.12348) Cited by: §8.2.2.

[^68]: Proof-producing reflection for hol: with an application to model polymorphism. In International Conference on Interactive Theorem Proving, pp. 170–186. Cited by: §2.4.

[^69]: Vingean reflection: reliable reasoning for self-improving agents. Technical Report 2015-2. Cited by: §9.1.

[^70]: Reflective oracles: a foundation for classical game theory. External Links: 1508.04145, [Link](https://arxiv.org/abs/1508.04145) Cited by: §2.4.

[^71]: A comprehensive survey of self-evolving ai agents: a new paradigm bridging foundation models and lifelong agentic systems. External Links: 2508.07407, [Link](https://arxiv.org/abs/2508.07407) Cited by: Table 1, §1.

[^72]: LightMem: lightweight and efficient memory-augmented generation. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=dyJ0GWpjJB) Cited by: §6.2.3.

[^73]: WebEvolver: enhancing web agent self-improvement with co-evolving world model. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, pp. 8970–8986. Cited by: §5.3.2, §9.1.

[^74]: SeRL: self-play reinforcement learning for large language models with limited data. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=ZF93vyH9He) Cited by: §7.3.

[^75]: MCP-zero: active tool discovery for autonomous llm agents. External Links: 2506.01056, [Link](https://arxiv.org/abs/2506.01056) Cited by: §6.3.1.

[^76]: AgentOCR: reimagining agent history via optical self-compression. External Links: 2601.04786, [Link](https://arxiv.org/abs/2601.04786) Cited by: 1st item.

[^77]: Rethinking LLM uncertainty: a multi-agent approach to estimating black-box model uncertainty. In Findings of the Association for Computational Linguistics: EMNLP 2025, C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.), Suzhou, China, pp. 12349–12375. External Links: [Link](https://aclanthology.org/2025.findings-emnlp.660/), [Document](https://dx.doi.org/10.18653/v1/2025.findings-emnlp.660), ISBN 979-8-89176-335-7 Cited by: §5.2.

[^78]: Promptbreeder: self-referential self-improvement via prompt evolution. In Forty-first International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=9ZxnPZGmPU) Cited by: §1, 1st item, §6.1.3, Table 2.

[^79]: Gaia2: benchmarking LLM agents on dynamic and asynchronous environments. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=9gw03JpKK4) Cited by: 3rd item.

[^80]: Towards a theoretical understanding of synthetic data in llm post-training: a reverse-bottleneck perspective. External Links: 2410.01720, [Link](https://arxiv.org/abs/2410.01720) Cited by: §5.1.

[^81]: A survey of self-evolving agents: what, when, how, and where to evolve on the path to artificial super intelligence. Transactions on Machine Learning Research. Note: Survey Certification External Links: ISSN 2835-8856, [Link](https://openreview.net/forum?id=CTr3bovS5F) Cited by: Table 1, §1, §6.3.3.

[^82]: The prompt alchemist: automated llm-tailored prompt optimization for test case generation. External Links: 2501.01329, [Link](https://arxiv.org/abs/2501.01329) Cited by: §6.1.2.

[^83]: WebSynthesis: world-model-guided mcts for efficient webui-trajectory synthesis. External Links: 2507.04370, [Link](https://arxiv.org/abs/2507.04370) Cited by: §5.3.2.

[^84]: Saving swe-bench: a benchmark mutation approach for realistic agent evaluation. External Links: 2510.08996, [Link](https://arxiv.org/abs/2510.08996) Cited by: §7.1.

[^85]: Logical induction. External Links: 1609.03543, [Link](https://arxiv.org/abs/1609.03543) Cited by: §2.4.

[^86]: Theoria motus corporum coelestium in sectionibus conicis solem ambientium. Perthes et Besser. Cited by: §2.1.

[^87]: The theory of facilitated variation. Proceedings of the National Academy of Sciences 104 (suppl\_1), pp. 8582–8589. Cited by: §6.4.

[^88]: Is model collapse inevitable? breaking the curse of recursion by accumulating real and synthetic data. In First Conference on Language Modeling, External Links: [Link](https://openreview.net/forum?id=5B2K4LRgmz) Cited by: §5.1.

[^89]: SciAgents: automating scientific discovery through multi-agent intelligent graph reasoning. External Links: 2409.05556, [Link](https://arxiv.org/abs/2409.05556) Cited by: §7.4.

[^90]: Self-improving embodied foundation models. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=KXMIIVUB9U) Cited by: §7.5.

[^91]: Über formal unentscheidbare sätze der principia mathematica und verwandter systeme i. Monatshefte für mathematik und physik 38 (1), pp. 173–198. Cited by: §2.1.

[^92]: Training long-context, multi-turn software engineering agents with reinforcement learning. External Links: 2508.03501, [Link](https://arxiv.org/abs/2508.03501) Cited by: §7.1.

[^93]: STRIVE: structured reasoning for self-improvement in claim verification. Machine Intelligence Research 23 (1), pp. 185–199. External Links: ISSN 2731-5398, [Link](http://dx.doi.org/10.1007/s11633-025-1598-5), [Document](https://dx.doi.org/10.1007/s11633-025-1598-5) Cited by: 2nd item.

[^94]: Speculations concerning the first ultraintelligent machine. In Advances in computers, Vol. 6, pp. 31–88. Cited by: §1, §2.1.

[^95]: Towards an ai co-scientist. External Links: 2502.18864, [Link](https://arxiv.org/abs/2502.18864) Cited by: §7.4.

[^96]: Critic: large language models can self-correct with tool-interactive critiquing. In International Conference on Learning Representations, Vol. 2024, pp. 57734–57811. Cited by: Table 2.

[^97]: Robot-powered data flywheels: deploying robots in the wild for continual data collection and foundation model adaptation. External Links: 2511.19647, [Link](https://arxiv.org/abs/2511.19647) Cited by: §7.5.

[^98]: ManiSkill2: a unified benchmark for generalizable manipulation skills. In The Eleventh International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=b_CQDy9vrD1) Cited by: §7.5, §8.1.1, §8.2.2.

[^99]: Is your LLM secretly a world model of the internet? model-based planning for web agents. Transactions on Machine Learning Research. Note: External Links: ISSN 2835-8856, [Link](https://openreview.net/forum?id=c6l7yA0HSq) Cited by: §5.3.2.

[^100]: Richelieu: self-evolving llm-based agents for ai diplomacy. Advances in Neural Information Processing Systems 37, pp. 123471–123497. Cited by: §7.3.

[^101]: Connecting large language models with evolutionary algorithms yields powerful prompt optimizers. In The Twelfth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=ZG3RaNIsO8) Cited by: §1, 1st item, §6.1.3.

[^102]: SE-agent: self-evolution trajectory optimization in multi-step reasoning with LLM-based agents. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=isATAFP71B) Cited by: §7.1.

[^103]: World models. arXiv preprint arXiv:1803.10122 2 (3). Cited by: §5.3.2, §5.3.2.

[^104]: Complementing self-consistency with cross-model disagreement for uncertainty quantification. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=lOoRJo8xWy) Cited by: §5.1, §5.2.

[^105]: VerifiAgent: a unified verification agent in language model reasoning. External Links: 2504.00406, [Link](https://arxiv.org/abs/2504.00406) Cited by: §8.1.2.

[^106]: Advanced tool learning and selection system (atlass): a closed-loop framework using llm. External Links: 2503.10071, [Link](https://arxiv.org/abs/2503.10071) Cited by: 3rd item, §6.3.3.

[^107]: Ma-lmm: memory-augmented large multimodal model for long-term video understanding. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pp. 13504–13514. Cited by: §6.2.

[^108]: OpenWebVoyager: building multimodal web agents via iterative real-world exploration, feedback and optimization. External Links: 2410.19609, [Link](https://arxiv.org/abs/2410.19609) Cited by: §7.2.

[^109]: Efficient agent training for computer use. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=cDuA6ZNvCl) Cited by: §7.6.

[^110]: Human-inspired perspectives: a survey on ai long-term memory. External Links: 2411.00489, [Link](https://arxiv.org/abs/2411.00489) Cited by: §6.2.

[^111]: SIA: self improving ai with harness & weight updates. arXiv preprint arXiv:2605.27276. Cited by: 3rd item.

[^112]: Decentralizing ai memory: shimi, a semantic hierarchical memory index for scalable agent reasoning. External Links: 2504.06135, [Link](https://arxiv.org/abs/2504.06135) Cited by: 2nd item.

[^113]: Evolvability as the proper focus of evolutionary developmental biology. Evolution & development 9 (4), pp. 393–401. Cited by: §6.4.

[^114]: Measuring massive multitask language understanding. arXiv preprint arXiv:2009.03300. Cited by: §1.

[^115]: Interestingness as an inductive heuristic for future compression progress. arXiv preprint arXiv:2605.14831. Cited by: §3.3.

[^116]: Learning to learn using gradient descent. In International conference on artificial neural networks, pp. 87–94. Cited by: §1.

[^117]: Online learning: a comprehensive survey. Neurocomputing 459, pp. 249–289. Cited by: §3.3.

[^118]: DeepEyesV2: toward agentic multimodal model. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=yDKawwfJ5O) Cited by: §6.3.1.

[^119]: MetaGPT: meta programming for a multi-agent collaborative framework. In The twelfth international conference on learning representations, Cited by: §1.

[^120]: Lora: low-rank adaptation of large language models.. ICLR 1 (2), pp. 3. Cited by: 1st item.

[^121]: Automated design of agentic systems. In The Thirteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=t9U3LW7JVX) Cited by: 4th item, §6.4.

[^122]: SELF-EVOLVED REWARD LEARNING FOR LLMS. In The Thirteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=Zonhl0c9I0) Cited by: §5.2.

[^123]: A survey of foundation model-powered recommender systems: from feature-based, generative to agentic paradigms. External Links: 2504.16420, [Link](https://arxiv.org/abs/2504.16420) Cited by: §6.3.

[^124]: Large language models can self-improve. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pp. 1051–1068. Cited by: §1, §5.1, §5.1.

[^125]: Large language models cannot self-correct reasoning yet. In The Twelfth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=IkmD3fKBPQ) Cited by: §5.1.

[^126]: Beyond accuracy: the role of calibration in self-improving large language models. External Links: 2504.02902, [Link](https://arxiv.org/abs/2504.02902) Cited by: 2nd item.

[^127]: MetaTool benchmark for large language models: deciding whether to use tools and which to use. External Links: 2310.03128, [Link](https://arxiv.org/abs/2310.03128) Cited by: §8.2.1, §8.2.2.

[^128]: A theory of universal artificial intelligence based on algorithmic complexity. External Links: cs/0004001, [Link](https://arxiv.org/abs/cs/0004001) Cited by: §2.3.

[^129]: Practical computational power of linear transformers and their recurrent and self-referential extensions. External Links: 2310.16076, [Link](https://arxiv.org/abs/2310.16076) Cited by: §2.3.

[^130]: Metalearning continual learning algorithms. External Links: 2312.00276, [Link](https://arxiv.org/abs/2312.00276) Cited by: §1, §2.3.

[^131]: Going beyond linear transformers with recurrent fast weight programmers. External Links: 2106.06295, [Link](https://arxiv.org/abs/2106.06295) Cited by: §2.3.

[^132]: A modern self-referential weight matrix that learns to modify itself. In International conference on machine learning, pp. 9660–9677. Cited by: §1, §2.3.

[^133]: RLBench: the robot learning benchmark & learning environment. IEEE Robotics and Automation Letters. Cited by: §7.5.

[^134]: DiscoveryWorld: a virtual environment for developing and evaluating automated scientific discovery agents. In The Thirty-eight Conference on Neural Information Processing Systems Datasets and Benchmarks Track, External Links: [Link](https://openreview.net/forum?id=cDYqckEt6d) Cited by: §8.2.2.

[^135]: OSWorld-MCP: benchmarking MCP tool invocation in computer-use agents. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=rceD6wwt4B) Cited by: §7.6.

[^136]: Importance weighting can help large language models self-improve. In Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 39, pp. 24257–24265. Cited by: §5.1.

[^137]: SWE-bench: can language models resolve real-world github issues?. In The Twelfth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=VTF8yNQM66) Cited by: §7.1, §8.2.2.

[^138]: STELLA: self-evolving llm agent for biomedical research. External Links: 2507.02004, [Link](https://arxiv.org/abs/2507.02004) Cited by: §6.3.2, §6.3.3.

[^139]: Memory os of ai agent. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, pp. 25972–25981. Cited by: §6.2.3.

[^140]: Dspy: compiling declarative language model calls into self-improving pipelines. arXiv preprint arXiv:2310.03714. Cited by: Table 2.

[^141]: Dual-scale world models for LLM agents towards hard-exploration problems. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=bH5uHIVtTe) Cited by: §5.3.2.

[^142]: Overcoming catastrophic forgetting in neural networks. Proceedings of the national academy of sciences 114 (13), pp. 3521–3526. Cited by: 1st item.

[^143]: Meta learning backpropagation and improving it. Advances in Neural Information Processing Systems 34, pp. 14122–14134. Cited by: §1.

[^144]: Eliminating meta optimization through self-referential meta learning. arXiv preprint arXiv:2212.14392. Cited by: §1.

[^145]: VisualWebArena: evaluating multimodal agents on realistic visual web tasks. In ICLR 2024 Workshop on Large Language Model (LLM) Agents, External Links: [Link](https://openreview.net/forum?id=RPKxrKTJbj) Cited by: §7.2, §8.2.2.

[^146]: SALM: a multi-agent framework for language model-driven social network simulation. External Links: 2505.09081, [Link](https://arxiv.org/abs/2505.09081) Cited by: 2nd item, §6.2.1.

[^147]: ComputerRL: scaling end-to-end online reinforcement learning for computer use agents. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=oEVfNf0w4B) Cited by: §7.6.

[^148]: Learning to reason and memorize with self-notes. In Thirty-seventh Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=ZFwNdsDCRL) Cited by: 1st item, 1st item.

[^149]: ShinkaEvolve: towards open-ended and sample-efficient program evolution. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=lKEdGCoDNC) Cited by: §6.4, §8.1.1.

[^150]: Theorem prover as a judge for synthetic data generation. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 29941–29977. External Links: [Link](http://dx.doi.org/10.18653/v1/2025.acl-long.1448), [Document](https://dx.doi.org/10.18653/v1/2025.acl-long.1448) Cited by: §5.1.

[^151]: A human-inspired reading agent with gist memory of very long contexts. In Forty-first International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=OTmcsyEO5G) Cited by: 1st item.

[^152]: Explore, select, derive, and recall: augmenting llm with human-like memory for mobile task automation. External Links: 2312.03003, [Link](https://arxiv.org/abs/2312.03003) Cited by: 2nd item.

[^153]: Nouvelles méthodes pour la détermination des orbites des comètes; par am legendre... chez Firmin Didot, libraire pour lew mathematiques, la marine, l …. Cited by: §2.1.

[^154]: Why am and eurisko appear to work. Artificial intelligence 23 (3), pp. 269–294. Cited by: §2.2.

[^155]: EURISKO: a program that learns new heuristics and domain concepts: the nature of heuristics iii: program design and results. Artificial intelligence 21 (1-2), pp. 61–98. Cited by: §2.2.

[^156]: Automated theory formation in mathematics. Automated Theorem Proving: After 25 Years: After 25 Years 89, pp. 287. Cited by: §2.2.

[^157]: ST-webagentbench: a benchmark for evaluating safety and trustworthiness in web agents. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=MuCDzH0ctf) Cited by: §8.1.1, §8.2.2, §8.2.2.

[^158]: Retrieval-augmented generation for knowledge-intensive nlp tasks. In Proceedings of the 34th International Conference on Neural Information Processing Systems, NIPS ’20, Red Hook, NY, USA. External Links: ISBN 9781713829546 Cited by: 4th item.

[^159]: Iterative tool usage exploration for multimodal agents via step-wise preference tuning. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=yKUwkihcsi) Cited by: §6.3.1.

[^160]: DeepAgent: a general reasoning agent with scalable toolsets. External Links: 2510.21618, [Link](https://arxiv.org/abs/2510.21618) Cited by: §6.3.1.

[^161]: A vision for access control in llm-based agent systems. External Links: 2510.11108, [Link](https://arxiv.org/abs/2510.11108) Cited by: §9.1.

[^162]: MemOS: a memory os for ai system. External Links: 2507.03724, [Link](https://arxiv.org/abs/2507.03724) Cited by: §6.2.

[^163]: In-the-flow agentic system optimization for effective planning and tool use. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=Mf5AleTUVK) Cited by: §6.3.1.

[^164]: Self-evolving agents with reflective and memory-augmented abilities. In LLM-based Multi-Agent Systems: Towards Responsible, Reliable, and Scalable Agentic Systems, External Links: [Link](https://openreview.net/forum?id=6Mw2fO3ejN) Cited by: §6.2.3, §6.2.3.

[^165]: MassTool: a multi-task search-based tool retrieval framework for large language models. External Links: 2507.00487, [Link](https://arxiv.org/abs/2507.00487) Cited by: §6.3.1.

[^166]: From knowledge to noise: CTIM-rover and the pitfalls of episodic memory in software engineering agents. In Proceedings of the 1st Workshop for Research on Agent Language Models (REALM 2025), E. Kamalloo, N. Gontier, X. H. Lu, N. Dziri, S. Murty, and A. Lacoste (Eds.), Vienna, Austria, pp. 411–427. External Links: [Link](https://aclanthology.org/2025.realm-1.30/), [Document](https://dx.doi.org/10.18653/v1/2025.realm-1.30), ISBN 979-8-89176-264-0 Cited by: 4th item.

[^167]: Learning quickly when irrelevant attributes abound: a new linear-threshold algorithm. Machine learning 2 (4), pp. 285–318. Cited by: §3.3.

[^168]: SPIRAL: self-play on zero-sum games incentivizes reasoning via multi-agent multi-turn reinforcement learning. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=7Yayy5fNLg) Cited by: §7.3.

[^169]: WebCoach: self-evolving web agents with cross-session memory guidance. External Links: 2511.12997, [Link](https://arxiv.org/abs/2511.12997) Cited by: §7.2.

[^170]: Chain of hindsight aligns language models with feedback. In The Twelfth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=6xfe4IVcOu) Cited by: §6.1.2.

[^171]: Deliberation in latent space via differentiable cache augmentation. In Forty-second International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=IaUJl5RCOu) Cited by: 2nd item.

[^172]: Odyssey: empowering minecraft agents with open-world skills. External Links: 2407.15325, [Link](https://arxiv.org/abs/2407.15325) Cited by: §7.3.

[^173]: Position: truly self-improving agents require intrinsic metacognitive learning. In Forty-second International Conference on Machine Learning Position Paper Track, External Links: [Link](https://openreview.net/forum?id=4KhDd0Ozqe) Cited by: §6.3.

[^174]: Autodan: generating stealthy jailbreak prompts on aligned large language models. In International Conference on Learning Representations, Vol. 2024, pp. 56174–56194. Cited by: Table 2.

[^175]: ToolNet: connecting large language models with massive tools via tool graph. External Links: 2403.00839, [Link](https://arxiv.org/abs/2403.00839) Cited by: §6.3.1.

[^176]: Tool-planner: task planning with clusters across multiple tools. In The Thirteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=dRz3cizftU) Cited by: §6.3.1.

[^177]: Seeing, listening, remembering, and reasoning: a multimodal agent with long-term memory. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=PMz29A7Muq) Cited by: 1st item.

[^178]: The ai scientist: towards fully automated open-ended scientific discovery. External Links: 2408.06292, [Link](https://arxiv.org/abs/2408.06292) Cited by: §7.4, §7.4.

[^179]: SELF: self-evolution with language feedback. External Links: 2310.00533, [Link](https://arxiv.org/abs/2310.00533) Cited by: 1st item, §5.2.

[^180]: WebLINX: real-world website navigation with multi-turn dialogue. In Forty-first International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=mUSPhG4uDW) Cited by: §8.1.1.

[^181]: OrchDAG: complex tool orchestration in multi-turn interactions with plan DAGs. In First Workshop on Multi-Turn Interactions in Large Language Models, External Links: [Link](https://openreview.net/forum?id=uZE8mTYvHE) Cited by: §6.3.1.

[^182]: MemTool: optimizing short-term memory management for dynamic tool calling in llm agent multi-turn conversations. External Links: 2507.21428, [Link](https://arxiv.org/abs/2507.21428) Cited by: §6.3.1.

[^183]: Tool-to-agent retrieval: bridging tools and agents for scalable llm multi-agent systems. External Links: 2511.01854, [Link](https://arxiv.org/abs/2511.01854) Cited by: §6.3.1.

[^184]: From correction to mastery: reinforced distillation of large language model agents. External Links: [Link](https://openreview.net/forum?id=n4Er2o4BFB) Cited by: §9.1.

[^185]: Augmenting large language models with chemistry tools. Nature Machine Intelligence 6 (5), pp. 525–535. Cited by: §7.4.

[^186]: Self-refine: iterative refinement with self-feedback. In Thirty-seventh Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=S37hOerQLB) Cited by: §6.1.2, Table 2.

[^187]: Agents that reduce work and information overload. Communications of the ACM 37 (7), pp. 30–40. Cited by: §1.

[^188]: Isaac gym: high performance GPU based physics simulation for robot learning. In Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2), External Links: [Link](https://openreview.net/forum?id=fgFBtYgJQX_) Cited by: §7.5.

[^189]: GAIA: a benchmark for general AI assistants. In The Twelfth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=fibxvahvs3) Cited by: §8.1.1.

[^190]: RET-LLM: towards a general read-write memory for large language models. In ICLR 2024 Workshop: How Far Are We From AGI, External Links: [Link](https://openreview.net/forum?id=Z7tBs47cSH) Cited by: §6.2.

[^191]: The abstract theory of self-reproduction. Views on general systems theory, pp. 106–118. Cited by: §2.2.

[^192]: Tournament of prompts: evolving LLM instructions through structured debates and elo ratings. In First International KDD Workshop on Prompt Optimization, 2025, External Links: [Link](https://openreview.net/forum?id=Z9OsLgBCDG) Cited by: §6.1.3.

[^193]: FACTS: a factored state-space framework for world modelling. In International Conference on Learning Representations, Vol. 2025, pp. 68955–68983. Cited by: §5.3.

[^194]: GitTaskBench: a benchmark for code agents solving real-world tasks through code repository leveraging. External Links: 2508.18993, [Link](https://arxiv.org/abs/2508.18993) Cited by: §8.1.1, §8.2.1.

[^195]: Bounded recursive self-improvement. arXiv preprint arXiv:1312.6764. Cited by: §2.4.

[^196]: Skill set optimization: reinforcing language model behavior via transferable skills. In Forty-first International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=9laB7ytoMp) Cited by: §7.3.

[^197]: AlphaEvolve: a coding agent for scientific and algorithmic discovery. External Links: 2506.13131, [Link](https://arxiv.org/abs/2506.13131) Cited by: 4th item, §6.4.

[^198]: Dota 2 with large scale deep reinforcement learning. External Links: 1912.06680, [Link](https://arxiv.org/abs/1912.06680) Cited by: §7.3.

[^199]: Self-modification and mortality in artificial agents. In International Conference on Artificial General Intelligence, pp. 1–10. Cited by: §2.4.

[^200]: Symbolic learning enables self-evolving agents. AI Open. Cited by: §6.4.

[^201]: Code2MCP: transforming code repositories into mcp services. External Links: 2509.05941, [Link](https://arxiv.org/abs/2509.05941) Cited by: §6.3.3.

[^202]: Training language models to follow instructions with human feedback. Advances in neural information processing systems 35, pp. 27730–27744. Cited by: §2.5, 1st item.

[^203]: ReasoningBank: scaling agent self-evolving with reasoning memory. External Links: 2509.25140, [Link](https://arxiv.org/abs/2509.25140) Cited by: 1st item, §6.2.3.

[^204]: MemGPT: towards llms as operating systems. External Links: 2310.08560, [Link](https://arxiv.org/abs/2310.08560) Cited by: §6.2.

[^205]: Training software engineering agents and verifiers with SWE-gym. In Proceedings of the 42nd International Conference on Machine Learning, A. Singh, M. Fazel, D. Hsu, S. Lacoste-Julien, F. Berkenkamp, T. Maharaj, K. Wagstaff, and J. Zhu (Eds.), Proceedings of Machine Learning Research, Vol. 267, pp. 47717–47737. External Links: [Link](https://proceedings.mlr.press/v267/pan25g.html) Cited by: §9.

[^206]: WebCanvas: benchmarking web agents in online environments. In Agentic Markets Workshop at ICML 2024, External Links: [Link](https://openreview.net/forum?id=O1FaGasJob) Cited by: §8.2.2.

[^207]: Generative agents: interactive simulacra of human behavior. In Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology, UIST ’23, New York, NY, USA. External Links: ISBN 9798400701320, [Link](https://doi.org/10.1145/3586183.3606763), [Document](https://dx.doi.org/10.1145/3586183.3606763) Cited by: 4th item, §6.2.3.

[^208]: MrSteve: instruction-following agents in minecraft with what-where-when memory. In The Thirteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=CjXaMI2kUH) Cited by: 4th item.

[^209]: Large language models can self-improve at web agent tasks. External Links: 2405.20309, [Link](https://arxiv.org/abs/2405.20309) Cited by: §7.2.

[^210]: The berkeley function calling leaderboard (BFCL): from tool use to agentic evaluation of large language models. In Forty-second International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=2GmDdhBdDk) Cited by: §8.2.1, §8.2.2.

[^211]: Check your facts and try again: improving large language models with external knowledge and automated feedback. External Links: 2302.12813, [Link](https://arxiv.org/abs/2302.12813) Cited by: 1st item.

[^212]: Survey of genai for automotive software development: from requirements to executable code. In 2025 2nd International Generative AI and Computational Language Modelling Conference (GACLM), Vol., pp. 184–197. External Links: [Document](https://dx.doi.org/10.1109/GACLM67198.2025.11232000) Cited by: §6.3.2.

[^213]: Automatic prompt optimization with “gradient descent” and beam search. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, H. Bouamor, J. Pino, and K. Bali (Eds.), Singapore, pp. 7957–7968. External Links: [Link](https://aclanthology.org/2023.emnlp-main.494/), [Document](https://dx.doi.org/10.18653/v1/2023.emnlp-main.494) Cited by: §6.1.4, Table 2.

[^214]: Agent q: advanced reasoning and learning for autonomous ai agents. External Links: 2408.07199, [Link](https://arxiv.org/abs/2408.07199) Cited by: §7.2.

[^215]: LLM coaching LLM in self-play training. External Links: [Link](https://openreview.net/forum?id=NnEfjLA50a) Cited by: §7.3.

[^216]: WebRL: training LLM web agents via self-evolving online curriculum reinforcement learning. In The Thirteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=oVKEAFjEqv) Cited by: §1, §3.3, §5.3.1, §7.2.

[^217]: CREATOR: tool creation for disentangling abstract and concrete reasoning of large language models. In Findings of the Association for Computational Linguistics: EMNLP 2023, H. Bouamor, J. Pino, and K. Bali (Eds.), Singapore, pp. 6922–6939. External Links: [Link](https://aclanthology.org/2023.findings-emnlp.462/), [Document](https://dx.doi.org/10.18653/v1/2023.findings-emnlp.462) Cited by: §6.3.3.

[^218]: MetaAgent: toward self-evolving agent via tool meta-learning. External Links: 2508.00271, [Link](https://arxiv.org/abs/2508.00271) Cited by: §6.3.1.

[^219]: AutoAct: automatic agent learning from scratch for QA via self-planning. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), L. Ku, A. Martins, and V. Srikumar (Eds.), Bangkok, Thailand, pp. 3003–3021. External Links: [Link](https://aclanthology.org/2024.acl-long.165/), [Document](https://dx.doi.org/10.18653/v1/2024.acl-long.165) Cited by: §6.3.1.

[^220]: Dive: diversified iterative self-improvement. arXiv preprint arXiv:2501.00747. Cited by: §5.1, §5.1, §5.1.

[^221]: AgentDistill: training-free agent distillation with generalizable mcp boxes. External Links: 2506.14728, [Link](https://arxiv.org/abs/2506.14728) Cited by: §9.1.

[^222]: Alita-g: self-evolving generative agent for agent generation. External Links: 2510.23601, [Link](https://arxiv.org/abs/2510.23601) Cited by: §6.3.3.

[^223]: Alita: generalist agent enabling scalable agentic reasoning with minimal predefinition and maximal self-evolution. External Links: 2505.20286, [Link](https://arxiv.org/abs/2505.20286) Cited by: §1, §6.3.3, §6.3.3, 3rd item.

[^224]: LoCoBench-agent: an interactive benchmark for llm agents in long-context software engineering. External Links: 2511.13998, [Link](https://arxiv.org/abs/2511.13998) Cited by: §8.2.2.

[^225]: From exploration to mastery: enabling LLMs to master tools via self-driven interactions. In The Thirteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=QKBu1BOAwd) Cited by: §6.3.2.

[^226]: Recursive introspection: teaching language model agents how to self-improve. In The Thirty-eighth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=DRC9pZwBwR) Cited by: §5.2.

[^227]: Direct preference optimization: your language model is secretly a reward model. Advances in neural information processing systems 36, pp. 53728–53741. Cited by: 1st item, §5.3.1.

[^228]: Harness design for long-running application development. Note: [https://www.anthropic.com/engineering/harness-design-long-running-apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) Anthropic Engineering Blog. Cited by: §1.

[^229]: Learning to forget: continual learning with adaptive weight decay. arXiv preprint arXiv:2604.27063. Cited by: 1st item.

[^230]: Zep: a temporal knowledge graph architecture for agent memory. External Links: 2501.13956, [Link](https://arxiv.org/abs/2501.13956) Cited by: 3rd item, §6.2.1.

[^231]: LLMLOOP: improving llm-generated code and tests through automated iterative feedback loops. In 2025 IEEE International Conference on Software Maintenance and Evolution (ICSME), Vol., pp. 930–934. External Links: [Document](https://dx.doi.org/10.1109/ICSME64153.2025.00109) Cited by: §6.3.2.

[^232]: Agentic retrieval-augmented generation for time series analysis. External Links: 2408.14484, [Link](https://arxiv.org/abs/2408.14484) Cited by: 4th item.

[^233]: A survey of deep active learning. ACM computing surveys (CSUR) 54 (9), pp. 1–40. Cited by: §3.3.

[^234]: GateMem: benchmarking memory governance in multi-principal shared-memory agents. External Links: 2606.18829, [Link](https://arxiv.org/abs/2606.18829) Cited by: §8.2.1.

[^235]: General agents need world models. In Forty-second International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=dlIoumNiXt) Cited by: §5.3.2.

[^236]: NeuralOS: towards simulating operating systems via neural generative models. External Links: 2507.08800, [Link](https://arxiv.org/abs/2507.08800) Cited by: 3rd item.

[^237]: A self-improving coding agent. External Links: 2504.15228, [Link](https://arxiv.org/abs/2504.15228) Cited by: §9.

[^238]: Catastrophic forgetting, rehearsal and pseudorehearsal. Connection Science 7 (2), pp. 123–146. Cited by: 1st item.

[^239]: The perceptron: a probabilistic model for information storage and organization in the brain.. Psychological review 65 (6), pp. 386. Cited by: §2.1.

[^240]: Identifying the risks of LM agents with an LM-emulated sandbox. In The Twelfth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=GEcwtMk1uA) Cited by: §8.1.1, §8.2.1, §8.2.2.

[^241]: An automatic end-to-end chemical synthesis development platform powered by large language models. Nature communications 15 (1), pp. 10160. Cited by: §7.4.

[^242]: MemInsight: autonomous memory augmentation for LLM agents. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.), Suzhou, China, pp. 33136–33152. External Links: [Link](https://aclanthology.org/2025.emnlp-main.1683/), [Document](https://dx.doi.org/10.18653/v1/2025.emnlp-main.1683), ISBN 979-8-89176-332-6 Cited by: §6.2.3.

[^243]: Some studies in machine learning using the game of checkers. IBM Journal of research and development 3 (3), pp. 210–229. Cited by: §2.1.

[^244]: Beyond pipelines: a survey of the paradigm shift toward model-native agentic ai. External Links: 2510.16720, [Link](https://arxiv.org/abs/2510.16720) Cited by: §6.2, §6.3.

[^245]: Linear transformers are secretly fast weight programmers. In International conference on machine learning, pp. 9355–9366. Cited by: §2.3, §2.5.

[^246]: Learning to control fast-weight memories: an alternative to recurrent nets. Technical report Technical Report FKI-147-91, Institut für Informatik, Technische Universität München. Cited by: §2.3, §2.5.

[^247]: Simple principles of metalearning. Technical report IDSIA 69, pp. 1–23. Cited by: §1, §2.3, §3.2.

[^248]: On learning how to learn learning strategies. External Links: [Link](https://api.semanticscholar.org/CorpusID:59806870) Cited by: §1, §2.3, §2.3, §3.2, §7.6, §8.1.

[^249]: A general method for incremental self-improvement and multi-agent learning. In Evolutionary Computation: Theory and Applications, pp. 81–123. Cited by: §7.6, §8.1.

[^250]: Exploring the predictable. In Advances in evolutionary computing: theory and applications, pp. 579–612. Cited by: §7.4.

[^251]: Goedel machines: self-referential universal problem solvers making provably optimal self-improvements. External Links: cs/0309048, [Link](https://arxiv.org/abs/cs/0309048) Cited by: §7.6.

[^252]: Annotated history of modern ai and deep learning. arXiv preprint arXiv:2212.11279. Cited by: §2.1, §2.1, footnote 1.

[^253]: Reinforcement learning with self-modifying policies. In Learning to learn, pp. 293–309. Cited by: §7.6, §8.1.

[^254]: Shifting inductive bias with success-story algorithm, adaptive levin search, and incremental self-improvement. Machine Learning 28 (1), pp. 105–130. Cited by: §1, §2.3, §3.2, §7.6, §8.1.

[^255]: Multi-agent learning with the success-story algorithm. In Workshop on Learning in Distributed Artificial Intelligence Systems, pp. 82–93. Cited by: §2.3.

[^256]: Evolutionary principles in self-referential learning, or on learning how to learn: the meta-meta-… hook. Diploma thesis, Institut für Informatik, Technische Universität München. Cited by: §1, §2.2, §2.3, §3.2, §3.2, §6.4.

[^257]: Making the world differentiable: on using fully recurrent self-supervised neural networks for dynamic reinforcement learning and planning in non-stationary environments. Institut für Informatik, Technische Universität München. Technical Report FKI-126 90. Cited by: §5.3.2, §5.3, §5.3, §7.4.

[^258]: A possibility for implementing curiosity and boredom in model-building neural controllers. In Proc. of the international conference on simulation of adaptive behavior: From animals to animats, pp. 222–227. Cited by: §3.3, 2nd item.

[^259]: Curious model-building control systems. In Proc. international joint conference on neural networks, pp. 1458–1463. Cited by: §7.4.

[^260]: Learning to control fast-weight memories: an alternative to dynamic recurrent networks. Neural Computation 4 (1), pp. 131–139. Cited by: §1, §2.3, §2.5.

[^261]: A ‘self-referential’weight matrix. In International conference on artificial neural networks, pp. 446–450. Cited by: §1, §2.3, §2.5, §3.2, §3.2.

[^262]: Beyond $\backslash$ genetic programming": incremental self-improvement. In Proc. Workshop on Genetic Programming at ML95, pp. 42–49. Cited by: §3.2.

[^263]: What”s interesting?. Istituto Dalle Molle Di Studi Sull Intelligenza Artificiale. Cited by: §7.4.

[^264]: Gödel machines: self-referential universal problem solvers making provably optimal self-improvements. arXiv preprint cs/0309048. Cited by: §1, §2.3, §3.2.

[^265]: Optimal ordered problem solver. Machine Learning 54 (3), pp. 211–254. Cited by: §1.

[^266]: Developmental robotics, optimal artificial curiosity, creativity, music, and the fine arts. Connection Science 18 (2), pp. 173–187. Cited by: §3.3.

[^267]: Simple algorithmic principles of discovery, subjective beauty, selective attention, curiosity & creativity. In International conference on discovery science, pp. 26–38. Cited by: §7.4.

[^268]: Formal theory of creativity, fun, and intrinsic motivation (1990–2010). IEEE transactions on autonomous mental development 2 (3), pp. 230–247. Cited by: §3.3, §7.4.

[^269]: Powerplay: training an increasingly general problem solver by continually searching for the simplest still unsolvable problem. Frontiers in psychology 4, pp. 313. Cited by: §7.4, §7.4.

[^270]: On learning to think: algorithmic information theory for novel combinations of reinforcement learning controllers and recurrent neural world models. arXiv preprint arXiv:1511.09249. Cited by: §1, §5.3, §7.4.

[^271]: Mastering atari, go, chess and shogi by planning with a learned model. Nature 588 (7839), pp. 604–609. External Links: ISSN 1476-4687, [Link](http://dx.doi.org/10.1038/s41586-020-03051-4), [Document](https://dx.doi.org/10.1038/s41586-020-03051-4) Cited by: §7.3.

[^272]: Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347. Cited by: 1st item, §5.3.1.

[^273]: Can large reasoning models self-train?. arXiv preprint arXiv:2505.21444. Cited by: §5.2, §5.

[^274]: Conceptual framework for autonomous cognitive entities. arXiv preprint arXiv:2310.06775. Cited by: §6.3.

[^275]: Self-improving robots: end-to-end autonomous visuomotor reinforcement learning. In Conference on Robot Learning, pp. 3292–3308. Cited by: §7.5.

[^276]: Taskbench: benchmarking large language models for task automation. Advances in Neural Information Processing Systems 37, pp. 4540–4574. Cited by: §8.2.1.

[^277]: Taskcraft: automated generation of agentic tasks. arXiv preprint arXiv:2506.10055. Cited by: 1st item, §5.1, §5.1.

[^278]: MobileGUI-rl: advancing mobile gui agent through reinforcement learning in online environment. arXiv preprint arXiv:2507.05720. Cited by: §5.3.1.

[^279]: Reflexion: language agents with verbal reinforcement learning. Advances in neural information processing systems 36, pp. 8634–8652. Cited by: §2.5, §5.1, §6.1.2, Table 2.

[^280]: Agent-oriented programming. Artificial intelligence 60 (1), pp. 51–92. Cited by: §1.

[^281]: SWE-rm: execution-free feedback for software engineering agents. External Links: 2512.21919, [Link](https://arxiv.org/abs/2512.21919) Cited by: §7.1.

[^282]: The curse of recursion: training on generated data makes models forget. External Links: 2305.17493, [Link](https://arxiv.org/abs/2305.17493) Cited by: §5.1.

[^283]: AI models collapse when trained on recursively generated data. Nature 631 (8022), pp. 755–759. Cited by: §5.1.

[^284]: CORE-bench: fostering the credibility of published research through a computational reproducibility agent benchmark. Transactions on Machine Learning Research. Note: External Links: ISSN 2835-8856, [Link](https://openreview.net/forum?id=BsMMc4MEGS) Cited by: §8.1.1, §8.2.2.

[^285]: Mastering chess and shogi by self-play with a general reinforcement learning algorithm. External Links: 1712.01815, [Link](https://arxiv.org/abs/1712.01815) Cited by: §7.3.

[^286]: A general reinforcement learning algorithm that masters chess, shogi, and go through self-play. Science 362 (6419), pp. 1140–1144. Cited by: §7.3.

[^287]: Mastering the game of go without human knowledge. nature 550 (7676), pp. 354–359. Cited by: §2.4.

[^288]: Welcome to the era of experience. Google AI 1. Cited by: §5.3.

[^289]: Self rewarding self improving. arXiv preprint arXiv:2505.08827. Cited by: §5.2.

[^290]: LADDER: self-improving LLMs through recursive problem decomposition. External Links: 2503.00735 Cited by: §5.1, §5.1, §5.1.

[^291]: Agentic retrieval-augmented generation: a survey on agentic rag. External Links: 2501.09136, [Link](https://arxiv.org/abs/2501.09136) Cited by: 4th item.

[^292]: Beyond human data: scaling self-training for problem-solving with language models. Transactions on Machine Learning Research. Note: Expert Certification External Links: ISSN 2835-8856, [Link](https://openreview.net/forum?id=lNAyUngGFK) Cited by: §5.1, §5.1.

[^293]: Moviechat: from dense token to sparse memory for long video understanding. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pp. 18221–18232. Cited by: 2nd item.

[^294]: Scene-driven multimodal knowledge graph construction for embodied ai. IEEE Transactions on Knowledge and Data Engineering 36 (11), pp. 6962–6976. External Links: [Document](https://dx.doi.org/10.1109/TKDE.2024.3399746) Cited by: 3rd item.

[^295]: Trial and error: exploration-based trajectory optimization of llm agents. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 7584–7600. Cited by: §5.3.1.

[^296]: Learning to generalize with object-centric agents in the open world survival game crafter. IEEE Transactions on Games 16 (2), pp. 384–395. Cited by: §7.3, §7.3.

[^297]: Evolving neural networks through augmenting topologies. Evolutionary computation 10 (2), pp. 99–127. Cited by: §2.3.

[^298]: PaperBench: evaluating ai’s ability to replicate ai research. External Links: 2504.01848, [Link](https://arxiv.org/abs/2504.01848) Cited by: §8.2.2.

[^299]: Towards an actual gödel machine implementation: a lesson in self-reflective systems. In Theoretical Foundations of Artificial General Intelligence, pp. 173–195. Cited by: §2.4.

[^300]: Reinforcement driven information acquisition in non-deterministic environments. In Proceedings of the international conference on artificial neural networks, Paris, Vol. 2, pp. 159–164. Cited by: §3.3, §7.4, §7.4.

[^301]: Science fiction and philosophy: from time travel to superintelligence. JSTOR. Cited by: §2.4.

[^302]: Hierarchical memory for high-efficiency long-term reasoning in llm agents. External Links: 2507.22925, [Link](https://arxiv.org/abs/2507.22925) Cited by: 1st item, 2nd item.

[^303]: Black-box tuning for language-model-as-a-service. In International Conference on Machine Learning, pp. 20841–20855. Cited by: Table 2.

[^304]: Enhancing latent computation in transformers with latent tokens. External Links: 2505.12629, [Link](https://arxiv.org/abs/2505.12629) Cited by: 2nd item.

[^305]: SEAgent: self-evolving computer use agent with autonomous learning from experience. External Links: 2508.04700, [Link](https://arxiv.org/abs/2508.04700) Cited by: §2.5, 3rd item, §7.6.

[^306]: Memory poisoning attack and defense on memory based llm-agents. External Links: 2601.05504, [Link](https://arxiv.org/abs/2601.05504) Cited by: 3rd item.

[^307]: Between mdps and semi-mdps: a framework for temporal abstraction in reinforcement learning. Artificial intelligence 112 (1-2), pp. 181–211. Cited by: §3.2.

[^308]: Dynamic cheatsheet: test-time learning with adaptive memory. External Links: 2504.07952, [Link](https://arxiv.org/abs/2504.07952) Cited by: 1st item, §6.2.3.

[^309]: Too consistent to detect: a study of self-consistent errors in LLMs. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.), Suzhou, China, pp. 4755–4765. External Links: [Link](https://aclanthology.org/2025.emnlp-main.238/), [Document](https://dx.doi.org/10.18653/v1/2025.emnlp-main.238), ISBN 979-8-89176-332-6 Cited by: §5.2.

[^310]: In prospect and retrospect: reflective memory management for long-term personalized dialogue agents. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), W. Che, J. Nabende, E. Shutova, and M. T. Pilehvar (Eds.), Vienna, Austria, pp. 8416–8439. External Links: [Link](https://aclanthology.org/2025.acl-long.413/), [Document](https://dx.doi.org/10.18653/v1/2025.acl-long.413), ISBN 979-8-89176-251-0 Cited by: 4th item.

[^311]: A survey on self-evolution of large language models. External Links: 2404.14387, [Link](https://arxiv.org/abs/2404.14387) Cited by: Table 1, §1.

[^312]: Learning to learn: introduction and overview. In Learning to learn, pp. 3–17. Cited by: §2.3.

[^313]: Toward self-improvement of LLMs via imagination, searching, and criticizing. In The Thirty-eighth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=tPdJ2qHkOB) Cited by: §5.2.

[^314]: Teaming llms to detect and mitigate hallucinations. External Links: 2510.19507, [Link](https://arxiv.org/abs/2510.19507) Cited by: §5.2.

[^315]: Autonomous ‘self-driving’laboratories: a review of technology and policy implications. Royal Society Open Science 12 (7), pp. 250646. Cited by: §7.4.

[^316]: PRIME: planning and retrieval-integrated memory for enhanced reasoning. External Links: 2509.22315, [Link](https://arxiv.org/abs/2509.22315) Cited by: 1st item.

[^317]: AppWorld: a controllable world of apps and people for benchmarking interactive coding agents. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), L. Ku, A. Martins, and V. Srikumar (Eds.), Bangkok, Thailand, pp. 16022–16076. External Links: [Link](https://aclanthology.org/2024.acl-long.850/), [Document](https://dx.doi.org/10.18653/v1/2024.acl-long.850) Cited by: §8.2.2.

[^318]: The anatomy of an agent harness. Note: [https://www.langchain.com/blog/the-anatomy-of-an-agent-harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness) LangChain Blog. Cited by: §1.

[^319]: Intelligent machinery. Technical report National Physical Laboratory. Note: Unpublished report (typescript). Original held at King’s College, Cambridge (Turing Digital Archive, AMT/C/11). External Links: [Link](https://dn790006.ca.archive.org/0/items/turing1948/turing1948_text.pdf) Cited by: §2.1.

[^320]: Computing machinery and intelligence. Mind LIX (236), pp. 433–460. External Links: [Document](https://dx.doi.org/10.1093/mind/LIX.236.433) Cited by: §2.1.

[^321]: Theory of self-reproducing automata. University of Illinois press Urbana. Cited by: §2.2.

[^322]: EvalAgent: discovering implicit evaluation criteria from the web. External Links: 2504.15219, [Link](https://arxiv.org/abs/2504.15219) Cited by: §8.1.2.

[^323]: SCM: enhancing large language model with self-controlled memory framework. External Links: 2304.13343, [Link](https://arxiv.org/abs/2304.13343) Cited by: 1st item, §6.2.3.

[^324]: Voyager: an open-ended embodied agent with large language models. External Links: 2305.16291, [Link](https://arxiv.org/abs/2305.16291) Cited by: §2.5, §6.3.1, §6.3.2, §7.3.

[^325]: Toward a theory of agents as tool-use decision-makers. External Links: 2506.00886, [Link](https://arxiv.org/abs/2506.00886) Cited by: §6.3.

[^326]: Improving model alignment through collective intelligence of open-source llms. External Links: 2505.03059, [Link](https://arxiv.org/abs/2505.03059) Cited by: §1.

[^327]: A survey on large language model based autonomous agents. Frontiers of Computer Science 18 (6). External Links: ISSN 2095-2236, [Link](http://dx.doi.org/10.1007/s11704-024-40231-1), [Document](https://dx.doi.org/10.1007/s11704-024-40231-1) Cited by: §1.

[^328]: CausalRAG: integrating causal graphs into retrieval-augmented generation. In Findings of the Association for Computational Linguistics: ACL 2025, W. Che, J. Nabende, E. Shutova, and M. T. Pilehvar (Eds.), Vienna, Austria, pp. 22680–22693. External Links: [Link](https://aclanthology.org/2025.findings-acl.1165/), [Document](https://dx.doi.org/10.18653/v1/2025.findings-acl.1165), ISBN 979-8-89176-256-5 Cited by: 3rd item.

[^329]: ToolGen: unified tool retrieval and calling via generation. In The Thirteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=XLMAMmowdY) Cited by: 3rd item, §6.3.1.

[^330]: MCP-flow: facilitating llm agents to master real-world, diverse and scaling mcp tools. External Links: 2510.24284, [Link](https://arxiv.org/abs/2510.24284) Cited by: §6.3.1.

[^331]: How to correctly do semantic backpropagation on language-based agentic systems. External Links: 2412.03624, [Link](https://arxiv.org/abs/2412.03624) Cited by: §6.1.4.

[^332]: Huxley-g\\”odel machine: human-level coding agent development by an approximation of the optimal self-improving machine. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=T0EiEuhOOL) Cited by: §2.5, §6.4, §7.1.

[^333]: MINT: evaluating LLMs in multi-turn interaction with tools and language feedback. In The Twelfth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=jp3gWrMuIZ) Cited by: §8.1.1, §8.2.1.

[^334]: MetaGen: self-evolving roles and topologies for multi-agent llm reasoning. External Links: 2601.19290, [Link](https://arxiv.org/abs/2601.19290) Cited by: 2nd item.

[^335]: Self-instruct: aligning language models with self-generated instructions. arXiv preprint arXiv:2212.10560. Cited by: 1st item, §5.1, §5.1, §5.

[^336]: MIRIX: multi-agent memory system for llm-based agents. External Links: 2507.07957, [Link](https://arxiv.org/abs/2507.07957) Cited by: 4th item.

[^337]: MEMORYLLM: towards self-updatable large language models. External Links: 2402.04624, [Link](https://arxiv.org/abs/2402.04624) Cited by: 2nd item.

[^338]: M+: extending MemoryLLM with scalable long-term memory. In Proceedings of the 42nd International Conference on Machine Learning, A. Singh, M. Fazel, D. Hsu, S. Lacoste-Julien, F. Berkenkamp, T. Maharaj, K. Wagstaff, and J. Zhu (Eds.), Proceedings of Machine Learning Research, Vol. 267, pp. 63308–63323. External Links: [Link](https://proceedings.mlr.press/v267/wang25au.html) Cited by: 2nd item.

[^339]: RoboGen: towards unleashing infinite data for automated robot learning via generative simulation. In Proceedings of the 41st International Conference on Machine Learning, ICML’24. Cited by: §7.5.

[^340]: RAGEN: understanding self-evolution in llm agents via multi-turn reinforcement learning. External Links: 2504.20073, [Link](https://arxiv.org/abs/2504.20073) Cited by: §5.

[^341]: Agent workflow memory. In Proceedings of the 42nd International Conference on Machine Learning, A. Singh, M. Fazel, D. Hsu, S. Lacoste-Julien, F. Berkenkamp, T. Maharaj, K. Wagstaff, and J. Zhu (Eds.), Proceedings of Machine Learning Research, Vol. 267, pp. 63897–63911. External Links: [Link](https://proceedings.mlr.press/v267/wang25bx.html) Cited by: 2nd item, 1st item, §6.2.3.

[^342]: CodeARC: benchmarking reasoning capabilities of LLM agents for inductive program synthesis. In Second Conference on Language Modeling, External Links: [Link](https://openreview.net/forum?id=Q5pVZCrrKr) Cited by: 3rd item.

[^343]: Chain-of-thought prompting elicits reasoning in large language models. Advances in neural information processing systems 35, pp. 24824–24837. Cited by: §1, §1.

[^344]: AutoTIR: autonomous tools integrated reasoning via reinforcement learning. External Links: 2507.21836, [Link](https://arxiv.org/abs/2507.21836) Cited by: §6.3.1.

[^345]: SWE-RL: advancing LLM reasoning via reinforcement learning on open software evolution. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=ULblO61XZ0) Cited by: §7.1.

[^346]: Webagent-r1: training web agents via end-to-end multi-turn reinforcement learning. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, pp. 7920–7939. Cited by: §7.2.

[^347]: Cybernetics: or control and communication in the animal and the machine. John Wiley & Sons, New York. Note: UK edition commonly listed as Chapman & Hall, London Cited by: §2.1.

[^348]: Solving pomdps with levin search and EIRA. In Machine Learning, Proceedings of the Thirteenth International Conference (ICML ’96), Bari, Italy, July 3-6, 1996, L. Saitta (Ed.), pp. 534–542. Cited by: §2.3, §3.2.

[^349]: Intelligent agents: theory and practice. The knowledge engineering review 10 (2), pp. 115–152. Cited by: §1.

[^350]: GUI-reflection: empowering multimodal GUI models with self-reflection behavior. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=qup6v4WnYX) Cited by: §7.6.

[^351]: Avatar: optimizing llm agents for tool usage via contrastive reasoning. Advances in Neural Information Processing Systems 37, pp. 25981–26010. Cited by: §9.1.

[^352]: Meta-rewarding language models: self-improving alignment with LLM-as-a-meta-judge. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.), Suzhou, China, pp. 11537–11554. External Links: [Link](https://aclanthology.org/2025.emnlp-main.583/), [Document](https://dx.doi.org/10.18653/v1/2025.emnlp-main.583), ISBN 979-8-89176-332-6 Cited by: §5.2.

[^353]: Progress or regress? self-improvement reversal in post-training. In The Thirteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=RFqeoVfLHa) Cited by: §5.1.

[^354]: From human memory to ai memory: a survey on memory mechanisms in the era of llms. External Links: 2504.15965, [Link](https://arxiv.org/abs/2504.15965) Cited by: §6.2.

[^355]: SGMem: sentence graph memory for long-term conversational agents. External Links: 2509.21212, [Link](https://arxiv.org/abs/2509.21212) Cited by: 3rd item.

[^356]: OS-copilot: towards generalist computer agents with self-improvement. External Links: 2402.07456, [Link](https://arxiv.org/abs/2402.07456) Cited by: §6.3.3.

[^357]: Agentgym: evolving large language model-based agents across diverse environments. arXiv preprint arXiv:2406.04151. Cited by: §5.3.1, §8.1.1, §8.2.2, §9.1.

[^358]: Agentless: demystifying llm-based software engineering agents. External Links: 2407.01489, [Link](https://arxiv.org/abs/2407.01489) Cited by: §7.1.

[^359]: Live-swe-agent: can software engineering agents self-evolve on the fly?. External Links: 2511.13646, [Link](https://arxiv.org/abs/2511.13646) Cited by: 4th item, §6.4, §7.1, 1st item.

[^360]: UI-genie: a self-improving approach for iteratively boosting MLLM-based mobile GUI agents. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=3uUmJzSSOW) Cited by: §1, §2.5, §5.3.1, §7.6.

[^361]: Osworld: benchmarking multimodal agents for open-ended tasks in real computer environments. Advances in Neural Information Processing Systems 37, pp. 52040–52094. Cited by: §7.6, §8.2.2, §9.

[^362]: Beyond outlining: heterogeneous recursive planning for adaptive long-form writing with language models. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, pp. 24689–24725. Cited by: §1, §7.4.

[^363]: WizardLM: empowering large pre-trained language models to follow complex instructions. In The Twelfth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=CfXh93NDgH) Cited by: §5.1, §5.1, Table 2.

[^364]: MetaTextGrad: automatically optimizing language model optimizers. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=10s01YrlKp) Cited by: §6.1.4, Table 2.

[^365]: SEDM: scalable self-evolving distributed memory for agents. arXiv preprint arXiv:2509.09498. Cited by: §6.2.

[^366]: SEDM: scalable self-evolving distributed memory for agents. External Links: 2509.09498, [Link](https://arxiv.org/abs/2509.09498) Cited by: §6.2.3.

[^367]: Learning to align multi-faceted evaluation: a unified and robust framework. In Findings of the Association for Computational Linguistics: ACL 2025, W. Che, J. Nabende, E. Shutova, and M. T. Pilehvar (Eds.), Vienna, Austria, pp. 9488–9502. External Links: [Link](https://aclanthology.org/2025.findings-acl.494/), [Document](https://dx.doi.org/10.18653/v1/2025.findings-acl.494), ISBN 979-8-89176-256-5 Cited by: §8.1.2.

[^368]: DipLLM: fine-tuning LLM for strategic decision-making in diplomacy. In Forty-second International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=hfPaOxDWfI) Cited by: §7.3.

[^369]: A-mem: agentic memory for llm agents. External Links: 2502.12110, [Link](https://arxiv.org/abs/2502.12110) Cited by: §6.2.3, §6.2.3, §6.2.

[^370]: Language agents with reinforcement learning for strategic play in the werewolf game. In Forty-first International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=usUPvQH3XK) Cited by: §7.3.

[^371]: The ai scientist-v2: workshop-level automated scientific discovery via agentic tree search. External Links: 2504.08066, [Link](https://arxiv.org/abs/2504.08066) Cited by: §7.4, §7.4.

[^372]: From seed ai to technological singularity via recursively self-improving software. arXiv preprint arXiv:1502.06512. Cited by: §9.

[^373]: Large language models as optimizers. In The Twelfth International Conference on Learning Representations, Cited by: §6.1.1, Table 2.

[^374]: TTCS: test-time curriculum synthesis for self-evolving. External Links: 2601.22628, [Link](https://arxiv.org/abs/2601.22628) Cited by: 1st item.

[^375]: Swe-agent: agent-computer interfaces enable automated software engineering. Advances in Neural Information Processing Systems 37, pp. 50528–50652. Cited by: §2.5, §7.1.

[^376]: SWE-bench multimodal: do AI systems generalize to visual software domains?. In The Thirteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=riTiq3i21b) Cited by: §7.1.

[^377]: EmbodiedBench: comprehensive benchmarking multi-modal large language models for vision-driven embodied agents. In Forty-second International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=DgGF2LEBPS) Cited by: §8.2.2.

[^378]: DrunkAgent: stealthy memory corruption in llm-powered recommender agents. External Links: 2503.23804, [Link](https://arxiv.org/abs/2503.23804) Cited by: §8.1.1, §8.2.1.

[^379]: SkillOpt: executive strategy for self-evolving agent skills. External Links: 2605.23904, [Link](https://arxiv.org/abs/2605.23904) Cited by: Table 2.

[^380]: React: synergizing reasoning and acting in language models. In The eleventh international conference on learning representations, Cited by: §1, §2.5.

[^381]: Escaping model collapse via synthetic data verification: near-term improvements and long-term convergence. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=yfk6c39omW) Cited by: §5.1.

[^382]: SafeAgentBench: a benchmark for safe task planning of embodied llm agents. External Links: 2412.13178, [Link](https://arxiv.org/abs/2412.13178) Cited by: §8.1.1, §8.2.2, §8.2.2.

[^383]: Gödel agent: a self-referential agent framework for recursively self-improvement. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), W. Che, J. Nabende, E. Shutova, and M. T. Pilehvar (Eds.), Vienna, Austria, pp. 27890–27913. External Links: [Link](https://aclanthology.org/2025.acl-long.1354/), [Document](https://dx.doi.org/10.18653/v1/2025.acl-long.1354), ISBN 979-8-89176-251-0 Cited by: §6.3.

[^384]: Gödel agent: a self-referential agent framework for recursively self-improvement. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 27890–27913. Cited by: §6.4.

[^385]: Agent-as-a-judge. External Links: 2601.05111, [Link](https://arxiv.org/abs/2601.05111) Cited by: §8.1.2.

[^386]: Meta-world: a benchmark and evaluation for multi-task and meta reinforcement learning. In Conference on robot learning, pp. 1094–1100. Cited by: §7.5.

[^387]: MARS: reinforcing multi-agent reasoning of LLMs through self-play in strategic games. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=GCd5v3ehmr) Cited by: §7.3.

[^388]: CRAFT: customizing LLMs by creating and retrieving from specialized toolsets. In The Twelfth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=G0vdDSt9XM) Cited by: §6.3.3.

[^389]: Self-rewarding language models. arXiv preprint arXiv:2401.10020. Cited by: §1.

[^390]: Superficial self-improved reasoners benefit from model merging. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, pp. 5912–5932. Cited by: §5.1.

[^391]: TextGrad: automatic "differentiation" via text. External Links: 2406.07496, [Link](https://arxiv.org/abs/2406.07496) Cited by: §1, 1st item, §6.1.4, Table 2.

[^392]: Self-taught optimizer (STOP): recursively self-improving code generation. In First Conference on Language Modeling, External Links: [Link](https://openreview.net/forum?id=46Zgqo4QIU) Cited by: §6.4, Table 2.

[^393]: On the structural memory of llm agents. External Links: 2412.15266, [Link](https://arxiv.org/abs/2412.15266) Cited by: §6.2.2.

[^394]: ToolACE-r: model-aware iterative training and adaptive refinement for tool learning. External Links: 2504.01400, [Link](https://arxiv.org/abs/2504.01400) Cited by: §6.3.1.

[^395]: InjecAgent: benchmarking indirect prompt injections in tool-integrated large language model agents. External Links: 2403.02691, [Link](https://arxiv.org/abs/2403.02691) Cited by: §9.1.

[^396]: Large language model-brained GUI agents: a survey. Transactions on Machine Learning Research. Note: External Links: ISSN 2835-8856, [Link](https://openreview.net/forum?id=xChvYjvXTp) Cited by: §6.3.

[^397]: Evaluation agent: efficient and promptable evaluation framework for visual generative models. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), W. Che, J. Nabende, E. Shutova, and M. T. Pilehvar (Eds.), Vienna, Austria, pp. 7561–7582. External Links: [Link](https://aclanthology.org/2025.acl-long.374/), [Document](https://dx.doi.org/10.18653/v1/2025.acl-long.374), ISBN 979-8-89176-251-0 Cited by: §8.1.2.

[^398]: Adaptive self-improvement LLM agentic system for ML library development. In Forty-second International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=gdsZ3uMPsY) Cited by: 2nd item.

[^399]: G-memory: tracing hierarchical memory for multi-agent systems. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=mmIAp3cVS0) Cited by: 3rd item, §6.2.3.

[^400]: MemGen: weaving generative latent memory for self-evolving agents. External Links: 2509.24704, [Link](https://arxiv.org/abs/2509.24704) Cited by: 2nd item, 2nd item, §6.2.3.

[^401]: The landscape of agentic reinforcement learning for LLMs: a survey. Transactions on Machine Learning Research. Note: Survey Certification External Links: ISSN 2835-8856, [Link](https://openreview.net/forum?id=RY19y2RI1O) Cited by: §3.3.

[^402]: Self-harness: harnesses that improve themselves. External Links: 2606.09498, [Link](https://arxiv.org/abs/2606.09498) Cited by: §1.

[^403]: Agent security bench (ASB): formalizing and benchmarking attacks and defenses in LLM-based agents. In The Thirteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=V4y0CpX4hK) Cited by: §9.1.

[^404]: Honeycomb: a flexible llm-based agent system for materials science. In Findings of the Association for Computational Linguistics: EMNLP 2024, pp. 3369–3382. Cited by: §7.4.

[^405]: Darwin gödel machine: open-ended evolution of self-improving agents. In The Fourteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=pUpzQZTvGY) Cited by: §1, §1, §2.5, 4th item, §6.4, §6.4, §7.1.

[^406]: CodeAgent: enhancing code generation with tool-integrated agent systems for real-world repo-level coding challenges. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), L. Ku, A. Martins, and V. Srikumar (Eds.), Bangkok, Thailand, pp. 13643–13658. External Links: [Link](https://aclanthology.org/2024.acl-long.737/), [Document](https://dx.doi.org/10.18653/v1/2024.acl-long.737) Cited by: 1st item.

[^407]: MLC-agent: cognitive model based on memory-learning collaboration in llm empowered agent simulation environment. External Links: 2507.20215, [Link](https://arxiv.org/abs/2507.20215) Cited by: §6.2.3.

[^408]: Right question is already half the answer: fully unsupervised LLM reasoning incentivization. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=k8Mim6RI5O) Cited by: §5.2.

[^409]: Agentic context engineering: evolving contexts for self-improving language models. External Links: 2510.04618, [Link](https://arxiv.org/abs/2510.04618) Cited by: §6.1.2, §6.2.3, Table 2.

[^410]: MemRL: self-evolving agents via runtime reinforcement learning on episodic memory. External Links: 2601.03192, [Link](https://arxiv.org/abs/2601.03192) Cited by: §1.

[^411]: AgentOrchestra: orchestrating hierarchical multi-agent intelligence with the tool-environment-agent(tea) protocol. External Links: 2506.12508, [Link](https://arxiv.org/abs/2506.12508) Cited by: 3rd item, §6.3.3.

[^412]: Will pre-training ever end? a first step toward next-generation foundation mllms via self-improving systematic cognition. arXiv preprint arXiv:2503.12303. Cited by: §5.1.

[^413]: AskToAct: enhancing LLMs tool use via self-correcting clarification. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.), Suzhou, China, pp. 13484–13511. External Links: [Link](https://aclanthology.org/2025.emnlp-main.682/), [Document](https://dx.doi.org/10.18653/v1/2025.emnlp-main.682), ISBN 979-8-89176-332-6 Cited by: §6.3.1.

[^414]: Enhancing language agent strategic reasoning through self-play in adversarial games. External Links: 2510.16761, [Link](https://arxiv.org/abs/2510.16761) Cited by: §7.3.

[^415]: A survey on the memory mechanism of large language model-based agents. ACM Transactions on Information Systems 43 (6), pp. 1–47. Cited by: §6.2.

[^416]: Expel: llm agents are experiential learners. In Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 38, pp. 19632–19642. Cited by: §5.3, 1st item, §7.3.

[^417]: Absolute zero: reinforced self-play reasoning with zero data. arXiv preprint arXiv:2505.03335. Cited by: §5.3.1.

[^418]: SELF-guide: better task-specific instruction following via self-synthetic finetuning. External Links: 2407.12874, [Link](https://arxiv.org/abs/2407.12874) Cited by: §1, 1st item, §5.1, §5.1, §5.1.

[^419]: PyVision: agentic vision with dynamic tooling. External Links: 2507.07998, [Link](https://arxiv.org/abs/2507.07998) Cited by: §6.3.2, §6.3.3.

[^420]: Learning to reason without external rewards. arXiv preprint arXiv:2505.19590. Cited by: §5.2.

[^421]: Curious causality-seeking agents in open-ended worlds. Advances in Neural Information Processing Systems 38, pp. 153856–153893. Cited by: 2nd item.

[^422]: SkillWeaver: web agents can self-improve by discovering and honing skills. External Links: 2504.07079, [Link](https://arxiv.org/abs/2504.07079) Cited by: §6.3.2.

[^423]: GPT-4v(ision) is a generalist web agent, if grounded. In Forty-first International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=piecKJ2DlB) Cited by: §7.2.

[^424]: AI harness engineering: a runtime substrate for foundation-model software agents. External Links: 2605.13357, [Link](https://arxiv.org/abs/2605.13357) Cited by: §1.

[^425]: Memorybank: enhancing large language models with long-term memory. In Proceedings of the AAAI conference on artificial intelligence, Vol. 38, pp. 19724–19731. Cited by: 2nd item, 4th item.

[^426]: Least-to-most prompting enables complex reasoning in large language models. In The Eleventh International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=WZH7099tgfM) Cited by: §5.1.

[^427]: Memento: fine-tuning llm agents without fine-tuning llms. External Links: 2508.16153, [Link](https://arxiv.org/abs/2508.16153) Cited by: §6.2.3.

[^428]: WebArena: a realistic web environment for building autonomous agents. In The Twelfth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=oKn9c6ytLx) Cited by: §7.2, §8.2.2.

[^429]: Self-challenging language model agents. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=9yusqX9DpR) Cited by: §5.

[^430]: Large language models are human-level prompt engineers. In The eleventh international conference on learning representations, Cited by: 1st item, §6.1.1, §6.1.1, Table 2.

[^431]: AURA: autonomous upskilling with retrieval-augmented agents. External Links: 2506.02507, [Link](https://arxiv.org/abs/2506.02507) Cited by: §7.5.

[^432]: WMPO: world model-based policy optimization for vision-language-action models. External Links: 2511.09515, [Link](https://arxiv.org/abs/2511.09515) Cited by: §5.3.2, §5.3.2.

[^433]: H2HMem: a multimodal memory benchmark for agents in human-human interactions. External Links: 2606.09461, [Link](https://arxiv.org/abs/2606.09461) Cited by: §8.2.1.

[^434]: Mindstorms in natural language-based societies of mind. arXiv preprint arXiv:2305.17066. Cited by: §7.3.

[^435]: GPTSwarm: language agents as optimizable graphs. In Proceedings of the 41st International Conference on Machine Learning, ICML’24. Cited by: §1, Table 2.

[^436]: AI with recursive self-improvement. In ICLR 2026 Workshop Proposals, Cited by: §9.2.

[^437]: Agent-as-a-judge: evaluate agents with agents. External Links: 2410.10934, [Link](https://arxiv.org/abs/2410.10934) Cited by: §8.1.2.

[^438]: Neural computers. arXiv preprint arXiv:2604.06425. Cited by: 3rd item.

[^439]: Neural architecture search with reinforcement learning. In International Conference on Learning Representations, Cited by: §2.4.

[^440]: TTRL: test-time reinforcement learning. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=VuVhgEiu20) Cited by: §5.2.

[^441]: Self-adapting language models. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=JsNUE84Hxi) Cited by: §5.1, §5.1.