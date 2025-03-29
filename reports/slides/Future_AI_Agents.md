---
theme: consult
height: 540
margin: 0
maxScale: 4
---
<!-- slide template="[[tpl-con-title]]" -->

## The Future of AI Agents is Event-Driven
::: block
Vinod
:::
::: block

:::
::: block
###### Reference: https://seanfalconer.medium.com/the-future-of-ai-agents-is-event-driven-9e25124060d6
:::


---

<!-- slide template="[[tpl-con-splash]]" -->

# **The First Wave of AI**

---

<!-- slide template="[[tpl-con-default-box]]" -->

::: title
### **Predictive Models**
:::

-   Centered on conventional ML techniques
-   Optimized for narrow, task-specific predictions
-   Heavily reliant on domain expertise
-   Limited scalability, slowing broader adoption
<center>
![[Pasted image 20250327160838.png | 300]]

*Fig1: The traditional machine learning workflow*
</center>

---
<!-- slide template="[[tpl-con-splash]]" -->

# **The Second Wave of AI**

---
<!-- slide template="[[tpl-con-default-box]]" -->

::: title
### **Generative Models**
:::

-   Learned from vast, diverse datasets → enhanced generalization across contexts
-   Capable of generating text, images, videos → unlocking new possibilities
-   Static in nature → struggles with incorporating real-time information
-   Challenging to adapt → fine-tuning can address domain-specific needs, but it’s expensive and error-prone 
<center>
![[Pasted image 20250327161558.png]]
*Fig2: Simple prompt and response with an LLM*
</center>

---
<!-- slide template="[[tpl-con-splash]]" -->

# **Compound AI Bridges the Gap**

---
<!-- slide template="[[tpl-con-default-box]]" -->

::: title
### **Compund AI**
:::

-  [Compound AI](https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/) systems integrate generative models with programmatic logic, data retrieval, and validation layers.
	-   Enables AI to fetch relevant data, combine tools, and produce more tailored outputs.
- **Example**: Insurance recommendation

 ![[Pasted image 20250327162618.png | 300]]
 _Fig3: Simple RAG architecture_
- This process, known as **Retrieval-Augmented Generation (RAG)**, dynamically incorporates external data into AI workflows..
	- However, it depends on **fixed workflows**, requiring predefined execution paths for every interaction.
---
<!-- slide template="[[tpl-con-splash]]" -->

# **The Rise of Agentic AI**

---
<!-- slide template="[[tpl-con-3-2]]" -->

::: title
### **Agentic AI**
:::

::: left
-   **Agents enable dynamic, context-driven workflows**
    -   Unlike fixed paths, they determine next steps in real time, adapting to changing situations.

-   **Shifting control logic**
    -   Agents can **reason, utilize tools, and access memory** dynamically, redefining traditional AI workflows.
:::<!-- element pad="0 0 0 20px" -->

::: right
 ![[Pasted image 20250328094219.png | 260]]
 Fig4: Control logic, programmatic versus agentic_
 ![[Pasted image 20250328094331.png | 290]]
 _Fig5: Agent architecture (Inspired by_ [_https://arxiv.org/pdf/2304.03442_](https://arxiv.org/pdf/2304.03442)_)_ 
 
:::<!-- element pad="0 0 0 10px"-->

---
<!-- slide template="[[tpl-con-splash]]" -->

# **How Design Patterns Shape Smarter Agents**
---
<!-- slide template="[[tpl-con-default-box]]" -->

::: title
### **Reflection**
:::

- Agents assess and enhance their outputs before taking action or finalizing responses.
	- Enables agents to catch and correct mistakes, refine their reasoning, and ensure higher-quality outcomes.
![[Pasted image 20250328095055.png | 450]] 
_Fig6: Reflection design pattern for agents_

---
<!-- slide template="[[tpl-con-default-box]]" -->

::: title
### **Tool Use Expands Agent Capabilities**
:::

- Interfacing with external tools extends an agent’s functionality, allowing it to perform tasks like retrieving data, automating processes, or executing deterministic workflows.
- Tool use bridges the gap between flexible decision-making and predictable, reliable execution.
![[Pasted image 20250328095347.png | 500]]
_Fig7: Tool use design pattern for agents_

---
<!-- slide template="[[tpl-con-default-box]]" -->

::: title
### **Planning Turns Goals Into Actions**
:::

- Agents with planning capabilities can break down high-level objectives into actionable steps, organizing tasks in a logical sequence.
- Useful for solving multi-step problems or managing workflows with dependencies.
![[Pasted image 20250328100028.png | 600]]
_Fig8: Planning design pattern for agents_

---
<!-- slide template="[[tpl-con-default-box]]" -->

::: title
### **Multi-Agent Collaboration: Modular Thinking**
:::

- Multi-agent systems take a modular approach to problem-solving by assigning specific tasks to specialized agents.
- The modular design reduces complexity for individual agents by keeping their context focused on their specific tasks.
- A related technique is [Mixture-of-Experts (MoE)](https://huggingface.co/blog/moe), which employs specialized submodels, or “experts,” within a single framework.
	- MoE dynamically routes tasks to the most relevant expert, optimizing computational resources and enhancing performance.
![[Pasted image 20250328100348.png | 290]]
_Fig9: Multi-agent collaboration design pattern for agents_

---
<!-- slide template="[[tpl-con-splash]]" -->

# **Agentic RAG: Adaptive and Context-Aware Retrieval**
---
<!-- slide template="[[tpl-con-default-box]]" -->

::: title
### **Agentic RAG**
:::

- Agents can determine in real time what data they need, where to find it, and how to refine their queries based on the task at hand.
- Well-suited for handling complex, multi-step workflows that require responsiveness and adaptability.
- **Example**: An agent creating a marketing strategy 

![[Pasted image 20250328101149.png | 300]]
_Fig10: Agentic RAG design pattern_

---

<!-- slide template="[[tpl-con-splash]]" -->

# **The Challenges with Scaling Intelligent Agents**
---
<!-- slide template="[[tpl-con-3-2]]" -->

::: title
### **Challenges**
:::

::: left
 - Scaling agents — whether a single agent or a collaborative system — hinges on their ability to access and share data effortlessly.
- Connecting agents to the tools and data they need is fundamentally a **distributed systems problem**.
	- Mirrors the challenges faced in designing microservices, where components must communicate efficiently without creating bottlenecks or rigid dependencies.
-  You could connect agents and tools through RPC and APIs, but that’s a recipe for tightly coupled systems.
	- Tight coupling makes it harder to scale, adapt, or support multiple consumers of the same data.

#### 📝**Agents need flexibility in accessing other agents, services, and platforms without any rigid dependencies.**

:::<!-- element pad="0 0 0 0" -->

::: right
![[Pasted image 20250328102800.png | 500]] 
_Fig11: Single agent dependencies_
:::<!-- element pad="0 0 0 0"-->

---

<!-- slide template="[[tpl-con-splash]]" -->

# **What's the Solution?**
---
<!-- slide template="[[tpl-con-3-2]]" -->

::: title
### **Event-Driven Architectures (EDA)**
:::

::: left
 - In the early days, software systems were monoliths -> Everything lived in a single, tightly integrated codebase.
- Microservices changed this
	- By breaking applications into smaller, independently deployable component but comes with a challenge of **Tight coupling**
-  EDA solved the problem.
	- EDA enables components to communicate asynchronously through events.
	- Services don’t wait on each other — they react to what’s happening in real-time.

#### 📝The future of AI isn’t just about building smarter agents — it’s about creating systems that can evolve and scale as the technology advances -> EDA is the foundation for this future**

:::<!-- element pad="0 0 0 0" -->

::: right
![[Pasted image 20250328103825.png | 300]]
_Fig12: Tightly-coupled Microservices_
![[Pasted image 20250328103834.png]]
_Fig13: Event-Driven Architecture_
:::<!-- element pad="0 0 0 0"-->

---
<!-- slide template="[[tpl-con-default-box]]" -->

::: title
### **Agents as Microservices with Informational Dependencies**
:::

- Agents are similar to microservices but they go further.
	- While microservices typically process discrete operations, agents rely on shared, context-rich information to reason, make decisions, and collaborate.
- For instance, an agent might pull customer data from a CRM, analyze live analytics, and use external tools — all while sharing updates with other agents.
	- EDA can solve this challenge by acting as a **central nervous system** for data.

![[Pasted image 20250328104605.png | 200]]
_Fig14: An Event-Driven architecture for AI agents_

---

<!-- slide template="[[tpl-con-default-box]]" -->

::: title
### **Decoupling While Keeping Context Intact**
:::

- Today's AI stack involves MLOps managing pipelines, data scientists selecting models, and developers building interfaces.
- A tightly coupled design creates dependencies, slowing delivery and adaptability.
- EDA ensures that workflows stay loosely coupled, allowing each team to innovate independently.
	- Application layers don’t need to understand the AI’s internals — they simply consume results when needed.

---
<!-- slide template="[[tpl-con-3-2]]" -->

::: title
### **Scaling Agents with Event-Driven Architecture**
:::

::: left
 - EDA is the backbone of this transition to agentic systems.
- As discussed [here](https://hubertdulay.substack.com/p/event-driven-agent-mesh), platforms like Kafka exemplify the advantages of EDA in an agent-driven system:
	- Horizontal Scalability
	- Low Latency
	- Loose Coupling
	- Event Persistence
-  This architecture is a natural fit for frameworks like Anthropic’s [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) (MCP).
	- MCP provides a universal standard for integrating AI systems with external tools, data sources, and applications, ensuring secure and seamless access to up-to-date information.
	- MCP reduces development effort while enabling context-aware decision-making.

#### 📝**EDA addresses many of the challenges MCP aims to solve**

:::<!-- element pad="0 0 0 0" -->

::: right

![[Pasted image 20250328104544.png]]
_Fig15: Agents as event producers and consumers on a real-time streaming platform_

:::<!-- element pad="0 0 0 0"-->

---
<!-- slide template="[[tpl-con-default-box]]" -->

::: title
### **Event-Driven Agents Will Define the Future of AI**
:::

- AI architectures must evolve to keep up with rapid advancements.
- [Survey](https://www.forumvc.com/2024-the-rise-of-agentic-ai-in-the-enterprise) says 48% of senior IT leaders are ready to integrate AI agents, showing strong demand.
- Event-Driven Architecture (EDA) enables flexible, scalable, and resilient AI systems.
- EDA ensures seamless integration and real-time workflows.
- Adopting EDA provides a competitive edge—those who don’t risk falling behind.

