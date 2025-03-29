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
	- They identify mistakes, refine reasoning, and ensure high-quality outcomes.
![[Pasted image 20250328095055.png | 450]] 
_Fig6: Reflection design pattern for agents_

---
<!-- slide template="[[tpl-con-default-box]]" -->

::: title
### **Tool Use Expands Agent Capabilities**
:::

- Agents can interact with external tools to retrieve data, automate tasks, and execute workflows.
- Tool usage combines adaptive decision-making with predictable execution.
![[Pasted image 20250328095347.png | 500]]
_Fig7: Tool use design pattern for agents_

---
<!-- slide template="[[tpl-con-default-box]]" -->

::: title
### **Planning Turns Goals Into Actions**
:::

- Agents decompose high-level goals into structured, actionable steps.
- Ideal for multi-step problem-solving and handling task dependencies.
![[Pasted image 20250328100028.png | 600]]
_Fig8: Planning design pattern for agents_

---
<!-- slide template="[[tpl-con-default-box]]" -->

::: title
### **Multi-Agent Collaboration: Modular Thinking**
:::

- Assigns specific tasks to specialized agents for efficient problem-solving.
- Keeps individual agents focused, reducing complexity.
- A related technique is [Mixture-of-Experts (MoE)](https://huggingface.co/blog/moe), which employs specialized submodels, or “experts”, within a single framework.
	- Dynamically routes tasks to specialized submodels, optimizing resources and performance.
![[Pasted image 20250328100348.png | 295]]
_Fig9: Multi-agent collaboration design pattern for agents_

---
<!-- slide template="[[tpl-con-splash]]" -->

# **Agentic RAG: Adaptive and Context-Aware Retrieval**
---
<!-- slide template="[[tpl-con-default-box]]" -->

::: title
### **Agentic RAG**
:::

- Agents can instantly assess the data required, identify its sources, and adjust their queries based on the task at hand.
- Ideal for managing intricate, multi-step processes that demand flexibility and quick adaptability.
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
 - Scaling agents — whether individually or within a collaborative system, depends on their ability to seamlessly access and share data.
- Connecting agents to necessary tools and data is essentially a **distributed systems challenge**.
	- This resembles the complexities of designing microservices, where components must communicate efficiently while avoiding bottlenecks and rigid dependencies.
-  While connecting agents and tools via RPC and APIs is possible, it often leads to tightly coupled systems.
	- Tight coupling can hinder scalability, adaptability, and the ability to support multiple data consumers.

#### 📝**Agents must have the flexibility to access other agents, services, and platforms without being constrained by rigid dependencies.**

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
 - In the early days, software systems were monolithic — everything existed within a single, tightly integrated codebase.
- Microservices revolutionized this by breaking applications into smaller, independently deployable components, though it introduced the challenge of tight coupling.
-  EDA solved the problem.
	- EDA allows components to communicate asynchronously via events.
	-  Services no longer depend on each other’s completion — they react to real-time events as they happen.

#### 📝The future of AI isn’t just about building smarter agents; it’s about creating systems that can evolve and scale with advancing technology — EDA forms the foundation for this future.

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

- Agents share similarities with microservices but go a step further.
	- While microservices handle discrete operations, agents leverage shared, context-rich information to reason, make decisions, and collaborate.
- For example, an agent could pull customer data from a CRM, analyze live analytics, and interact with external tools, all while updating other agents.
	- Event-Driven Architecture (EDA) can address this challenge by serving as the central nervous system for data.

![[Pasted image 20250328104605.png | 200]]
_Fig14: An Event-Driven architecture for AI agents_

---

<!-- slide template="[[tpl-con-default-box]]" -->

::: title
### **Decoupling While Keeping Context Intact**
:::

- Today’s AI stack includes MLOps managing pipelines, data scientists selecting models, and developers building interfaces.
- Tightly coupled designs introduce dependencies that slow down delivery and hinder adaptability.
- Event-Driven Architecture (EDA) keeps workflows loosely coupled, enabling each team to innovate independently.
	- Application layers don't need to know the inner workings of AI — they simply consume results as needed.

---
<!-- slide template="[[tpl-con-3-2]]" -->
::: title
### **Scaling Agents with Event-Driven Architecture**
:::
::: left
- Event-Driven Architecture (EDA) is the backbone of the transition to agent-based systems.
- As discussed [here](https://hubertdulay.substack.com/p/event-driven-agent-mesh), platforms like Kafka demonstrate the key benefits of EDA in an agent-driven system:
	- Horizontal Scalability
	- Low Latency
	- Loose Coupling
	- Event Persistence
-  This architecture is a natural fit for frameworks like Anthropic’s [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) (MCP).
	- MCP offers a universal standard for integrating AI systems with external tools, data sources, and applications, ensuring secure, real-time access to the latest information.
	- MCP minimizes development effort while enabling context-aware decision-making.

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

