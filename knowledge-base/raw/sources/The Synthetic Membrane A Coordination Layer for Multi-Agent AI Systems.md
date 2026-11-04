---
title: "The Synthetic Membrane: A Coordination Layer for Multi-Agent AI Systems"
source: "https://axjns.dev/research/0001-synthetic-membrane-coordination-layer"
author:
published:
created: 2026-11-04
description: "Position paper proposing a six-layer synthetic membrane architecture as a coordination layer for multi-agent AI systems, with a worked incident-response scenario and a controlled evaluation plan."
tags:
  - "clippings"
---
Alex Jones · July 2026 · Revised September 2026 · v2.2

## Abstract

Multi-agent systems need more than a way to delegate tasks. When work spans several agents, sessions, or authority boundaries, they also need a reliable account of what has been observed, what remains disputed, who owns the next action, and who may authorise it. Existing protocols, orchestration frameworks, and shared-state architectures provide many of these ingredients. The open question is how to combine them into a reusable coordination service without increasing cost or spreading errors.

This position paper proposes the **synthetic membrane**: a policy-controlled shared workspace for agents, organised around governance, discovery, selective access, persistent state, task coordination, and cross-cutting defence. Its closest architectural precedent is the blackboard. The proposed contribution is an explicit contract connecting evidence, access decisions, and action ownership across agent runtimes, together with an evaluation plan for that contract.

The paper makes a bounded hypothesis: for tasks with distributed evidence, changing membership, and constrained authority, this combination can improve completion and recovery relative to comparably resourced alternatives. Published failure analyses and blackboard experiments motivate the hypothesis; they do not validate this architecture. A worked security-incident scenario illustrates the design. No production case study or end-to-end experimental validation is claimed.

## 1\. The coordination problem

Consider an investigation involving detection, forensics, and containment agents. Detection observes suspicious traffic. Forensics learns that the affected service is carrying out a scheduled export. Containment prepares to isolate it. Each agent may reason competently from its own evidence and still contribute to a poor decision if the others cannot discover that evidence, distinguish an observation from an inference, or identify who owns the action.

Sending more messages may help. So may a better prompt, a central planner, or a shared database. The engineering problem is to make the relevant information available at the right time, under the right permissions, while preserving enough history to recover from mistakes. Transport alone does not specify those semantics; shared storage alone does not enforce them.

Here, **coordination** means managing dependencies between agents' information and actions. **Shared state** means records that authorised participants can address and update through a common interface. It does not mean that every agent reads everything or has identical beliefs. **Collective benefit** means an improvement in a specified task outcome over an explicit baseline at a comparable resource budget.

The target workload has three properties: useful evidence is distributed, participants or responsibilities change during execution, and actions have authority constraints. Short, independent subtasks may need none of this machinery. A single agent with suitable tools is the first baseline, not a stage to be outgrown automatically.

## 2\. What the evidence supports

### 2.1 Failure analysis motivates better coordination

Cemri et al.'s MAST study analyses more than 1,600 annotated execution traces across seven multi-agent frameworks. Its taxonomy distinguishes system design, inter-agent misalignment, and task verification failures. This supports examining system design alongside model capability. It does not establish that a missing shared workspace causes every failure, or that introducing one would remove them. \[1\]

Li et al.'s Superminds Test probes MoltBook, a platform hosting more than two million agents, and reports weak joint reasoning, information synthesis, and basic interaction. The platform population is not the number of agents jointly solving each test. The result challenges the expectation that scale alone produces collective capability; it is not a controlled comparison of coordination architectures. Participation, incentives, and the platform's interaction model remain possible explanations. \[2\]

These findings identify problems worth testing against. Neither isolates the synthetic membrane as the remedy.

### 2.2 Shared workspaces have relevant experimental support

Salemi et al. evaluate a blackboard system on three data-discovery benchmarks and report 13–57% relative improvements in end-to-end success over their strongest baselines. Their architecture retains a central agent that posts requests while other agents volunteer relevant contributions. The result therefore supports this particular organisation of shared work, not a general rejection of central coordination. \[3\]

Han and Zhang also investigate blackboard-based LLM collaboration and report competitive performance with lower token use on their evaluated tasks. \[4\] These are closer precedents than biological analogies because they test related mechanisms. Their results do not establish that governance, persistence, or selective access independently causes the gains.

### 2.3 Cost must be measured at the model boundary

Bai et al. study token consumption in agentic coding and report substantial overhead and variation. Their comparison concerns agentic coding workloads; it is not a measurement of inter-agent communication overhead alone. It motivates accounting for repeated context, tool output, retries, and model calls rather than assuming that additional collaboration is inexpensive. \[5\]

A compact network payload does not necessarily reduce model tokens. The relevant quantity is the material actually presented to the model, including any summaries and the calls used to produce them. Selective retrieval is therefore a hypothesis about useful information per unit cost, not a guarantee of savings.

## 3\. Prior art and the proposed contribution

### 3.1 Protocols and frameworks are building blocks

MCP exposes tools, resources, and prompts through a client–server protocol, including negotiated subscription capabilities. A membrane service could use those interfaces. Describing MCP servers as necessarily passive or incapable of exposing shared state would misstate the protocol. \[6\]

A2A defines agent discovery and task interactions, including messages, artefacts, and lifecycle state. It can carry work between participants without prescribing this paper's evidence model or action-authorisation rules. \[7\] LangGraph provides persisted graph state, checkpoints, and replay facilities; it is a credible implementation substrate and comparison baseline. \[8\]

The distinction is between a transport or runtime and an application-level coordination contract. A sufficiently extended framework could implement the proposal. No claim is made that existing tools are incapable of it.

### 3.2 The blackboard is the closest precedent

A shared workspace to which specialised agents contribute is recognisably a blackboard architecture. The membrane inherits that idea. Access control and safety are also not new additions to this lineage: Terrarium explicitly revisits blackboards for multi-agent safety, privacy, and security research. \[9\]

The proposed contribution is consequently a synthesis: make evidence lineage, policy checks, and action ownership part of the same contract, then test whether that integration helps across runtime boundaries. This paper does not establish priority for the combination or claim a new distributed-systems primitive. If a conventional blackboard with equivalent controls performs as well with less complexity, that is evidence against a separate membrane service.

Mesh Memory Protocol is adjacent work on structured memory exchange and lineage. It is a candidate for interoperability, rather than a required dependency or an independently validated foundation of this proposal. \[10\]

### 3.3 Incident management supplies an operational model

Google's SRE incident-management guidance combines explicit roles, a living incident document, and deliberate handoffs. Those practices suggest useful agent-system requirements: make responsibilities visible, preserve the state of the investigation, and transfer ownership explicitly. They also retain an incident commander. Human incident management is not evidence that coordination can dispense with authority. \[11\]

ICS adds an explicit vocabulary for objectives, command, and transfer of responsibility. Its value here is an operational analogy with known limits: agents are not human responders, and a human span-of-control ratio is not a measured optimum for LLM teams. \[13\]

| Incident-management practice | Proposed software counterpart |
| --- | --- |
| Shared incident picture | An authorised view of evidence, hypotheses, and action status |
| Defined command and accountability | Separate proposal, approval, and execution rights |
| Transfer-of-command briefing | An acknowledged handoff tied to a state version |
| Common terminology | Typed operational records with documented meanings |

The biological term *membrane* names selective exchange across a boundary. It is a design metaphor, not an explanation of collective intelligence. Software implementations still use messages, storage, and controllers.

## 4\. Hypothesis and design contract

The hypothesis is:

> For tasks with distributed evidence, changing membership, and constrained authority, a persistent workspace with selective delivery and explicit action ownership can improve task completion and recovery at a comparable total resource budget.

This is a contingent claim about a workload class. Persistence is useful for handoffs and recovery; it is not a prerequisite for every form of collective reasoning. Typed records reduce some ambiguity but cannot ensure that two models interpret evidence correctly. Gating can reduce irrelevant context but can also hide a decisive observation.

The proposed contract has five requirements:

1. **Addressable evidence.** An observation has a stable identifier, source, scope, and observation time. Interpretations refer to evidence rather than silently replacing it.
2. **Enforced access.** The service checks identity and policy on writes, reads, and notifications. Model-generated trust scores cannot grant permissions.
3. **Explicit ownership.** An actionable task has an owner, a lease or expiry rule, and a separately recorded authorisation decision.
4. **Recoverable state.** A replacement agent can obtain an authorised snapshot and subsequent changes without replaying an entire conversation into its context window.
5. **Inspectable decisions.** The record links outputs to the evidence versions and policy decisions used. Conflicting claims remain visible until resolved.

An illustrative claim record contains an ID, incident ID, author, observation time, evidence references, assertion, status, visibility label, and superseded-record reference. These are proposed fields, not a claim of conformance to another protocol. Confidence, if included, is an agent's estimate unless separately calibrated.

## 5\. Architecture and consistency

The architecture has five functional layers and a sixth, cross-cutting defence responsibility. Observability spans all six. The numbering retains the original proposal's labels; it does not prescribe a network stack or six separately deployed services.

| Responsibility | Interface and state | Boundary it must preserve |
| --- | --- | --- |
| Governance (L−1) | Policy, approval, escalation, halt | Agreement among agents does not grant authority |
| Discovery (L0) | Identity, capability, availability, task history | A capability claim is not proof of competence or permission |
| Permeability (L1) | Publish, query, subscribe, filter | Relevance ranking cannot bypass access control |
| Shared medium (L2) | Evidence, claims, projections, history | Convergent records need not contain true conclusions |
| Coordination (L3) | Claim, renew, release, propose, execute | Concurrent workers cannot independently acquire the same exclusive authority |
| Defence (cross-cutting) | Quarantine, revoke, invalidate, investigate | A suspect claim and its derivatives remain distinguishable from trusted evidence |

### 5.1 Governance and discovery

Governance defines who may propose, approve, and execute each action. A human or designated service can suspend execution, narrow access, or assume ownership. The suspension must be enforced at the execution boundary; recording a halt in shared memory is insufficient if workers continue using cached authority.

Discovery records authenticated identity, supported task types, availability, and relevant performance history. Observed performance may improve routing, but its value needs testing against declared capabilities. New agents need a path to participate, and past success on one task class does not establish general reliability. Routing and authorisation remain separate decisions.

### 5.2 Permeability separates permission from usefulness

Access defaults to deny unless a policy grants it. Within the authorised set, subscriptions and retrieval select potentially useful information under a context budget. These are separate operations: an agent may ask for more relevant evidence, but it cannot override the service's access policy.

Notifications should carry bounded summaries or record references, with access checked again when content is retrieved. Retractions, changed action ownership, and policy updates need explicit delivery and acknowledgement rules. A relevance filter must not silently discard them. Experiments should measure both noise reduction and missed critical information.

Evidence and interpretation remain distinct. A concise summary can point to a retained source so that another agent can inspect it. Repeated summaries of the same source are dependent reports, not independent corroboration.

### 5.3 Shared state needs more than convergence

The proposed starting point is a durable event history with materialised views for incidents, claims, and tasks. Append-only history supports audit and recovery, while retention rules govern how long sensitive payloads remain available. Corrections append a superseding or retracting record; ordinary queries should make the current status clear.

CRDTs are an option for data that can merge under defined rules, such as sets of observations or collaborative annotations. Their convergence guarantees depend on the data type and replication assumptions. They do not resolve contradictory diagnoses or enforce arbitrary cross-record invariants. \[12\]

Exclusive task ownership, approval, and budget reservation require stronger coordination. A first implementation can use transactional updates within an incident partition, with version checks and lease fencing. It should fail closed for actions when it cannot confirm current authority. Read-only investigation may continue on explicitly stale state where policy permits.

Content hashes help identify bytes and detect changes; they do not establish truth or authorship. Authenticated writes supply attribution. Recorded input references supply declared dependencies. Neither makes an event graph a complete causal explanation of failure: unrecorded observations, model behaviour, and tool effects may matter. Causal attribution requires additional assumptions and, where possible, interventions.

### 5.4 Coordination governs effects

An agent discovers a task, acquires a time-bounded claim, and proposes an action against an identified state version. Before execution, the responsible service checks ownership, policy, and any required approval. The action receives an idempotency key and a recorded outcome.

A lease alone cannot prevent an expired worker from acting. The executor must reject stale fencing tokens or equivalent obsolete authority. An idempotency key only prevents duplicate effects if the downstream system honours it; otherwise recovery must reconcile external state before retrying.

Quorum thresholds can trigger review or group formation. They are not proof that a conclusion is correct: agents may share models, prompts, and evidence. Dissent and common provenance should be shown alongside agreement. Team size and supervisory fan-out are tunable parameters, not constants imported from human cognition.

### 5.5 Defence and observability

Shared state can amplify both useful evidence and malicious content. Retrieved text remains untrusted data. It must not be allowed to rewrite access rules or confer execution authority. Quarantine should mark suspect entries, suppress their routine retrieval, and identify derived claims that require review. Revocation cannot erase information already delivered to an agent; sensitive work may require terminating affected sessions and rebuilding their context.

Operational traces should record tool calls, retrieved record versions, policy outcomes, ownership changes, and external effects. Short decision rationales can assist review. Exhaustive internal reasoning traces are neither assumed available nor required. Audit retention itself creates privacy and security obligations, so payload access and deletion policies belong in the design.

## 6\. Worked example: a suspected ransomware incident

This is a hypothetical walkthrough of the proposed contract, not an observed deployment or a validated response procedure.

At 02:17 UTC, a detection agent opens an incident after suspicious activity on an endpoint. It records the original alert as evidence and proposes a ransomware hypothesis. The hypothesis remains unconfirmed. Discovery identifies available forensics, containment, threat-intelligence, and communications agents with the relevant permissions.

The forensics agent adds a finding associated with malicious tooling. The finding strengthens the case for compromise but does not, by itself, establish ransomware. A second hypothesis remains open. Both claims refer to their supporting evidence, so the incident view can present uncertainty without collapsing it into one confidence score.

The containment agent proposes isolation. The forensics agent records that isolation may disrupt evidence collection. An authorised incident lead chooses the next action under the response policy, including any urgency rule. The system records the evidence versions, disagreement, approval, and action owner. The example's purpose is to expose the decision boundary, not prescribe which operational choice is correct.

Before acting, the executor verifies that the approval and ownership are current. If the containment agent has restarted and its lease has expired, the old request is rejected. A replacement agent reads the current incident view and the outstanding action record. It reconciles the endpoint's actual state before attempting a retry.

The communications agent receives a restricted summary suitable for its role. It does not gain access to raw endpoint evidence merely because all agents participate in the same incident. If evidence is later retracted, dependent conclusions are flagged for review and any affected action is escalated; the system cannot undo an external effect by editing the record.

A conventional incident database and workflow engine could implement this sequence. The research question is whether a reusable contract improves cross-agent operation enough to justify the additional service boundary.

## 7\. Evaluation plan

### 7.1 Compare against capable alternatives

Evaluation should use a fixed task suite with both coordination-heavy incidents and independent subtasks. Synthetic incident scenarios need explicit ground truth, observable action outcomes, and authority rules. They should include ambiguous evidence, delayed updates, agent restarts, and duplicate requests.

Compare four configurations: a single agent with tools; a central orchestrator with persistent state; a blackboard with comparable access and ownership controls; and the membrane implementation. Give each access to the same underlying evidence and tools, subject to the task's role restrictions. Use the same model versions and total resource limits. Document prompt differences and give all configurations a comparable tuning budget.

Run repeated, paired trials on held-out scenarios. Choose trial counts through pilot variance estimates, then freeze the evaluation protocol before the final runs. Report uncertainty intervals and per-scenario results, not just a pooled mean. A favourable result on one model or incident family establishes only that scope.

### 7.2 Measure outcomes, cost, and failure

| Question | Measurement |
| --- | --- |
| Does coordination improve the task? | Ground-truth completion, correct synthesis of distributed evidence, harmful or unauthorised actions |
| Does it recover? | Successful continuation after restart, duplicated effects, time to reconcile state |
| Is delivery selective without hiding essentials? | Irrelevant context delivered and critical evidence missed before decisions |
| What does it cost? | All model tokens and charges, summarisation and gating calls, tool and storage overhead, wall-clock latency |
| Can failures be investigated? | Attribution on controlled fault injections, including ambiguous or multiple-cause cases |

Where model pricing differs, compare both tokens and monetary cost. Evaluate quality under a fixed budget and cost at a predefined quality threshold. Longer conversations, higher event counts, and more agents are not success measures in themselves.

### 7.3 Isolate the mechanisms

Ablate persistence, selective delivery, and explicit ownership separately while retaining equivalent safety controls for external actions. Compare fixed subscriptions with adaptive relevance gating, and vary team size and context budgets. Test whether the gains come from the architecture, a better prompt, extra computation, or simply providing an explicit task state.

Inject stale evidence, a poisoned claim, a failed notification, and a worker crash between approval and execution. Use isolated test systems. Record whether the system rejects obsolete authority, propagates retractions, and recovers without duplicate effects. Fault-injection attribution scores describe that injection set, not arbitrary production failures.

### 7.4 What would count against the hypothesis?

Evidence against the proposal would include no completion or recovery gain over the strongest matched baseline, benefits that disappear when total compute is equalised, or selective delivery that repeatedly suppresses decisive evidence. If a controlled blackboard matches the membrane with lower overhead, the separate abstraction has not earned its place.

Success requires an improvement on a preregistered primary outcome, within a predefined cost ceiling and without a worse rate of harmful actions. The numerical margins should follow pilot measurements and operational requirements; they are not established here. Passing this evaluation would support the bounded hypothesis. It would not show that membranes are necessary for collective intelligence in general.

## 8\. Implementation path and limits

Sympozium is the intended integration setting. This paper proposes an implementation path; it does not assert that every component described above is already shipped. A useful first milestone is one incident partition, a transactional store, a small set of typed records, enforced read/write policy, task leases, and an executor that validates approval. Cross-runtime adapters and replicated annotation state can follow once the contract works end to end.

Kubernetes resources could represent durable incident identity, policy, and lifecycle. High-volume evidence and event histories need a storage design evaluated for their access patterns; placing every observation in one expanding custom resource is not the proposal. Checkpoints, bounded queries, and authorised change feeds should make recovery possible without sending the entire log to each model.

Let N agents each contribute F facts. An all-to-all exchange can require O(N²F) deliveries. A shared store reduces publication to O(NF), but if every agent reads every fact, read volume remains O(N²F). Selectivity and reuse, rather than shared storage alone, determine savings. Replication, indexing, invalidation, and recovery also consume resources.

The main limits are semantic and operational. Agents can agree on a false claim. Access restrictions can prevent useful synthesis. A central service can become a bottleneck or failure domain. Partitions force tradeoffs between availability and exclusive authority. Behavioural reputation can encode past selection bias. Persisted mistakes can outlive the agent that made them.

These are reasons to keep the prototype small and the baselines strong. Adaptive reputation, latent-state exchange, and autonomous reorganisation are later research questions, not prerequisites for testing the core contract.

## 9\. Conclusion

The synthetic membrane proposes a reusable way to connect shared evidence, selective access, and action ownership across agents. Its value would be practical: a participant can discover relevant work, inspect the evidence behind it, contribute under clear permissions, and hand off responsibility without losing the investigation's state.

The supporting literature makes that direction plausible. It does not establish the proposed architecture's necessity or superiority. The next contribution must be a reproducible comparison showing where this contract improves outcomes, what it costs, and when a simpler system is sufficient.

## References

1. Cemri, M. et al. (2025). [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/html/2503.13657v3) arXiv:2503.13657, v3.
2. Li, X. et al. (2026). [Superminds Test: Actively Evaluating Collective Intelligence of Agent Society via Probing Agents](https://arxiv.org/abs/2604.22452). arXiv:2604.22452.
3. Salemi, A. et al. (2025; revised 2026). [LLM-Based Multi-Agent Blackboard System for Information Discovery in Data Science](https://arxiv.org/abs/2510.01285v2). arXiv:2510.01285, v2.
4. Han, B. and Zhang, S. (2025). [Exploring Advanced LLM Multi-Agent Systems Based on Blackboard Architecture](https://arxiv.org/abs/2507.01701). arXiv:2507.01701.
5. Bai, L. et al. (2026). [How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks](https://arxiv.org/abs/2604.22750). arXiv:2604.22750.
6. Model Context Protocol. [Architecture, specification dated 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/architecture).
7. A2A Project. [Agent2Agent Protocol Specification](https://a2a-protocol.org/latest/specification/). Accessed September 2026.
8. LangChain. [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence). Accessed September 2026.
9. Nakamura, M. et al. (2025). [Terrarium: Revisiting the Blackboard for Multi-Agent Safety, Privacy, and Security Studies](https://arxiv.org/abs/2510.14312). arXiv:2510.14312.
10. Xu, H. (2026). [Mesh Memory Protocol: Semantic Infrastructure for Multi-Agent LLM Systems](https://arxiv.org/abs/2604.19540). arXiv:2604.19540.
11. Google. [Managing Incidents](https://sre.google/sre-book/managing-incidents/). Site Reliability Engineering.
12. Shapiro, M., Preguiça, N., Baquero, C., and Zawirski, M. (2011). [Conflict-Free Replicated Data Types](https://pages.lip6.fr/Marek.Zawirski/papers/CRDTs-SSS2011.pdf). SSS 2011.
13. FEMA (2018). [ICS Review Document](https://training.fema.gov/emiweb/is/icsresource/assets/ics%20review%20document.pdf). Extracted from ICS 300.