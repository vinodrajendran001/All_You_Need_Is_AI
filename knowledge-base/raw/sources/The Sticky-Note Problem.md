---
title: "The Sticky-Note Problem"
source: "https://axjns.dev/blog/sticky-note-problem"
author:
published:
created: 2026-11-04
description: "Why agent handoffs lose context, and what shared evidence, explicit ownership, and incident-management practice can improve."
tags:
  - "clippings"
---
Making Agent Handoffs Reliable

## A handoff without a shared picture

Imagine an incident at 2:47 AM. A detection agent flags unusual outbound traffic from a production database. A forensics agent has found a scheduled export that could explain it. A containment agent is preparing to isolate the server. Each has useful information; none has a reliable view of the others' findings or intentions.

The risk is easy to see. Containment could interrupt a legitimate export, or the team could dismiss an actual compromise without checking the explanation. This is a hypothetical example, but it captures a concrete design failure: decisions depend on information that exists somewhere in the system and never reaches the decision-maker.

I call it the sticky-note problem. A handoff says what one participant thought was worth passing on at a particular moment. It rarely tells the next participant what has changed since, which assumptions remain open, or who now owns the action. Add more agents and those omissions can become harder to find.

## The missing contract

Messages are necessary. The question is what the system makes durable around them. In an incident, an agent needs to distinguish an observation from a hypothesis, find the evidence behind a recommendation, and check whether somebody else has already claimed the next step.

Frameworks can support this. [LangGraph has persistent state and checkpoints](https://docs.langchain.com/oss/python/langgraph/persistence); a shared database can carry incident records; a workflow engine can enforce transitions. [A2A](https://a2a-protocol.org/latest/specification/) provides agent and task interactions, while [MCP](https://modelcontextprotocol.io/specification/2025-11-25/architecture) can expose the tools and resources used to inspect shared work. The problem is not that these systems only move strings. It is that the application still has to define what a finding, a handoff, or an approval means.

That contract is easy to leave implicit. A paragraph marked “done” might mean the investigation is complete, the current subtask is complete, or the agent has run out of useful ideas. A downstream agent should not have to infer which interpretation authorises a production action.

## What the research tells us

The [MAST study](https://arxiv.org/html/2503.13657v3) gives this discussion a firmer basis. It examines more than 1,600 annotated traces across seven multi-agent frameworks and groups failures into system design, inter-agent misalignment, and task verification. The practical lesson is that individual model capability is only part of the problem.

A failure taxonomy does not tell us which architecture will fix it. An agent can have the right evidence and still reason badly. A verifier can inspect the result and still accept an error. Better shared state is a candidate intervention, not an explanation for every failure in the dataset.

There is more direct evidence from [Salemi and colleagues' blackboard experiments](https://arxiv.org/abs/2510.01285v2). Agents contribute through a shared board, and the authors report improved success on their data-discovery benchmarks. That is a useful precedent for organising shared work. It does not prove that every task should use a blackboard, or that central coordination is the enemy: their design still has a central agent posting requests.

## Incident management offers a useful pattern

Human incident response has a vocabulary for this problem. The [Incident Command System](https://training.fema.gov/emiweb/is/icsresource/assets/ics%20review%20document.pdf) makes objectives, responsibilities, and transfers of command explicit. It combines shared information with a defined authority structure. That is a more useful lesson than the idea that a team should somehow coordinate without anyone being responsible.

Google's [SRE incident-management guidance](https://sre.google/sre-book/managing-incidents/) makes the pattern tangible through a living incident document, clear roles, and deliberate handoffs. A replacement responder can recover the state of the incident without asking every participant to retell the story.

For agents, I would translate that into a small set of records: evidence with a source and timestamp; hypotheses linked to that evidence; actions with an owner and an approval state; and a current incident view that preserves unresolved disagreement. The important property is that the next agent can inspect these records and act under the same rules.

This does not require copying a human organisation chart. The right team size, escalation threshold, and division of work need to be measured for the models and tasks involved. Human doctrine supplies design questions, not experimentally established constants for LLMs.

## From shared records to a synthetic membrane

The synthetic membrane is my proposal for making that contract reusable. Its shared workspace holds evidence and task state. A discovery service helps agents find relevant work. Access controls determine who may see or change a record; subscriptions determine which authorised changes deserve attention. Governance connects proposed actions to explicit authority.

Those responsibilities matter together. A shared board without access controls can expose sensitive evidence. A board without ownership can send two agents to execute the same action. A board without retractions can keep circulating a conclusion after its supporting evidence has been withdrawn.

The design also needs restraint. An agent should receive enough context to make its decision, not every thought produced by the team. Summaries should retain links to their evidence. A repeated claim should not become more credible merely because several agents copied it. Permission to read a recommendation should never imply permission to execute it.

## Put the handoff to the test

Return to the database incident. The detection agent publishes its alert. The forensics agent adds the scheduled-export evidence as a possible explanation. The containment agent proposes isolation, and the authorised incident lead can inspect both accounts before deciding. A restart should preserve the action owner and the unresolved question, rather than forcing a new agent to guess from a transcript.

That is the behaviour I want to test through Sympozium. It is also behaviour that a well-designed workflow and database could provide. The comparison has to include that alternative. The membrane earns its place only if making the contract reusable improves completion, recovery, or operator control enough to cover its cost.

The [position paper](https://axjns.dev/research/0001-synthetic-membrane-coordination-layer) develops the architecture and evaluation plan. The question behind it is practical: when one agent leaves and another arrives, can the system preserve the evidence, uncertainty, and responsibility needed to carry on?[Implementation](https://github.com/sympozium-ai/sympozium)

[

sympozium-ai / sympozium

github.com →

](https://github.com/sympozium-ai/sympozium)[

Research

AlexsJones / research

github.com →

](https://github.com/AlexsJones/research)[

Paper

Full paper (v2.2), read on site

axjns.dev →

](https://axjns.dev/research/0001-synthetic-membrane-coordination-layer)