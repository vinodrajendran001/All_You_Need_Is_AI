---
type: raw-source
source_id: src-2026-09-13-nevsky-gemini-multi-agent-system
title: "Building a Multi-Agent AI System with Gemini 3 and Google Cloud: From Single Agent to Orchestrated Intelligence"
author: Alex Nevsky
url: "https://medium.com/google-cloud/build-multi-agent-ai-system-with-gemini-3-1-google-cloud-single-bot-orchestrated-intelligence-dc0c111e30e7"
published: 2026-03-18
captured: 2026-09-13
created: 2026-09-13
updated: 2026-09-13
tags:
  - source/raw
  - ai-agents
  - multi-agent
  - google-cloud
status: active
---
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*TPhovPgAkNFbL7PECX7-wg.png)

## Why One Agent Isn’t Enough

In the previous posts in this series, we built a [customer support agent](https://medium.com/google-cloud/building-an-intelligent-customer-support-agent-with-googles-gemini-2-5-10df5baa4c1d), [optimized its prompts to 95% automation](https://medium.com/google-cloud/advanced-prompt-engineering-from-90-to-95-automation-the-100k-difference-c4008398ee14), and [added RAG for factual grounding](https://medium.com/@anevsky/building-a-rag-pipeline-with-gemini-2-5-91546c2ceaf6).

That agent handles single-turn support queries well. But real business workflows aren’t single-turn.

Consider an e-commerce order issue: a customer writes “I got the wrong item and I want a refund, but I also need the right item shipped today.” That’s three tasks — verify the order, process the return, and expedite a replacement — each requiring different data sources, different policies, and different actions. A single monolithic prompt trying to handle all of this becomes brittle, slow, and error-prone.

The solution? **Multi-agent systems** — specialized agents that each handle one part of the workflow, coordinated by an orchestrator.

In this post, I’ll show how to build a production multi-agent system on Google Cloud using the Gemini 3.1 series and Google’s Agent Development Kit (ADK), where specialized agents collaborate to handle complex workflows that no single agent can reliably manage.

**What You’ll Learn:**

- Why multi-agent architectures outperform monolithic prompts on complex tasks
- Designing agent roles with clear responsibility boundaries
- Building an orchestrator that routes, delegates, and synthesizes
- Inter-agent communication patterns on Google Cloud
- When to use multi-agent vs. single-agent (it’s not always better)

## The Problem: Monolithic Prompts Don’t Scale

As we added capabilities to our support agent — RAG retrieval, emotional intelligence, self-correction — the system prompt grew past 3,000 tokens. Each new capability introduced edge cases that interfered with existing ones.

The symptoms:

- **Constraint bleed** — Rules for handling refunds leaked into unrelated scenarios, causing the model to apply refund logic to simple product questions
- **Attention dilution** — The model’s attention is a finite resource. A 3,000-token prompt forces it to spread that budget across dozens of instructions, most irrelevant to any given query
- **Debugging nightmares** — When something went wrong, which part of the 3,000-token prompt caused it?
- **Rigid routing** — Every query hit the same pipeline regardless of complexity

By moving to specialized agents, you give each model 100% of its attention budget for the specific task at hand — only thinking about refund policies when processing refunds, only checking tone when doing QA.

Google’s [Agent Development Kit (ADK)](https://google.github.io/adk-docs/) is built on this principle. Its [AutoFlow](https://google.github.io/adk-docs/agents/multi-agents/) mechanism handles the handoff between specialists automatically: when an orchestrator agent has sub-agents, ADK injects a `transfer_to_agent()` tool and generates descriptions of all available specialists, giving the orchestrator "meta-cognition" — awareness of its team and which specialist can handle each task.

## Architecture Overview

Instead of one massive prompt, we use a modular hierarchy where a central orchestrator delegates to specialist sub-agents:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*a_BJGvrlqrPBjfdql0tXHA.png)

**Agent roles and model selection:**

Not every agent needs the same model. Use the strongest reasoning model where it matters (orchestration, QA) and the fastest/cheapest where speed is king (triage):

- **Orchestrator** — High-level planning and delegation. *Model:* Gemini 3.1 Pro. *Tools:* Specialist agents.
- **Triage Agent** — Sentiment analysis and intent routing. *Model:* Gemini 3.1 Flash-Lite. *Tools:* NLP classifiers.
- **Research Agent** — Fact-finding and context retrieval. *Model:* Gemini 3.1 Flash. *Tools:* Vertex Search, CRM API.
- **Action Agent** — Executing transactions (refunds, updates). *Model:* Gemini 3.1 Flash. *Tools:* Order API, Payment API.
- **QA Agent** — Fact-checking and policy compliance. *Model:* Gemini 3.1 Pro. *Tools:* Policy knowledge base.

Our earlier articles used Gemini 2.5 Flash for single-agent workflows — and it’s still a great workhorse. But for multi-agent systems where reasoning quality directly impacts routing decisions, the Gemini 3.1 series (GA as of early 2026) is the better fit, especially for the orchestrator and QA roles.

**Key Google Cloud services:**

- **Gemini 3.1 Series** — The core “brains,” optimized for tool use and reasoning
- [**Agent Development Kit (ADK)**](https://google.github.io/adk-docs/) — The framework managing handoffs between agents via AutoFlow
- [**Vertex AI Agent Engine**](https://docs.cloud.google.com/agent-builder/agent-engine/overview) — Managed runtime for deploying and scaling agents in production
- **Firestore** — The shared session state where agents read/write conversation memory
- **Vertex AI Vector Search** — RAG retrieval (from our previous article)

## Step 1: Setting Up the Agent Development Kit (30 minutes)

Google’s [ADK](https://google.github.io/adk-docs/) provides the scaffolding for multi-agent systems, including the AutoFlow handoff pattern where one agent can literally “transfer the call” to another.

Install the dependencies:

```c
pip install google-adk google-generativeai google-cloud-firestore pydantic
```

> ***Note:*** *ADK uses Pydantic models under the hood for agent input/output schemas. Including it explicitly ensures version compatibility.*

Define your project structure. Multi-agent systems fail most often at the boundaries — Agent A sends a `refund_id` as an integer, but Agent B expects a string. A flat structure with shared schemas prevents this:

```c
support_agents/
├── main.py              # Entry point for Cloud Run
├── common/
│   ├── __init__.py
│   └── schemas.py       # Shared Pydantic models (the "handshake")
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── triage.py
│   ├── research.py
│   ├── action.py
│   └── qa.py
└── config.py            # Environment & project IDs
```

Think of it like a hospital. The orchestrator is the triage nurse, the research agent is the lab tech, and the action agent is the surgeon. They don’t all talk to the patient at once — they read and update the patient’s chart (Firestore). The `schemas.py` file is the chart format everyone agrees on.

## Step 2: Building the Triage Agent (30 minutes)

The triage agent is your system’s “air traffic control.” It doesn’t solve problems — it ensures they’re routed to the right specialist with the right priority.

In production multi-agent systems, raw string outputs between agents are a recipe for breakage. We use Pydantic schemas to enforce a strict contract — the orchestrator receives a validated Python object, not a string it has to parse.

```c
# common/schemas.py
from pydantic import BaseModel, Field

class TriageResult(BaseModel):
    intents: list[str] = Field(description="List of detected customer goals")
    urgency: str = Field(pattern="^(low|medium|high|critical)$")
    sentiment: str = Field(description="Current emotional state of the user")
    required_agents: list[str] = Field(
        description="List of sub-agents needed (research, action, etc.)"
    )
```
```c
# agents/triage.py
from google.adk.agents import LlmAgent
from common.schemas import TriageResult

triage_agent = LlmAgent(
    name="triage_agent",
    model="gemini-3.1-flash-lite",  # Fast and cheap for classification
    instruction="""You are a triage specialist. Analyze the customer's
    message and categorize it accurately.

    Urgency rules:
    - critical: Active outages or safety threats
    - high: Frustrated users or financial issues > $100
    - medium: Standard requests needing action
    - low: General info/feedback

    You must NOT attempt to solve the problem. Only classify it.""",
    output_schema=TriageResult,  # Force structured JSON output
    output_key="triage_data"
)
```

The key design principles:

- **Single responsibility** — The triage agent doesn’t answer questions or take actions. It only classifies. This keeps its prompt short and its accuracy high.
- **Structured output** — `output_schema` forces the model to return valid JSON matching `TriageResult`. ADK validates it with Pydantic automatically.
- **Multi-intent support** — `intents: list[str]` handles "I need to update my address *and* check my last bill" — a single-string classifier would fail here.
- **State handoff** — `output_key="triage_data"` stores the result in the session state. The orchestrator accesses it via `session.state['triage_data']`.

## Step 3: Building the Research Agent (30 minutes)

The research agent is the “investigator.” It gathers raw data from Firestore and the RAG pipeline, then synthesizes it into a structured brief for the action agent.

First, define the output schema — this is the contract between the research and action agents:

```c
# common/schemas.py (add to existing file)

class ResearchBrief(BaseModel):
    order_status: str = Field(description="Current order state")
    customer_tier: str = Field(description="e.g. Gold, Standard")
    applicable_policy: str = Field(description="Relevant policy text")
    can_refund: bool = Field(description="Whether a refund is allowed")
    reasoning: str = Field(description="Why this conclusion was reached")
```

Then define the tools and agent:

```c
# agents/research.py
from google.adk.agents import LlmAgent
from google.cloud import firestore
from common.schemas import ResearchBrief

db = firestore.Client()

def lookup_order(order_id: str) -> dict:
    """Fetch real-time shipping status and line items for an order ID."""
    doc = db.collection('orders').document(order_id).get()
    if doc.exists:
        return doc.to_dict()
    return {"error": f"Order {order_id} not found"}

def lookup_customer(customer_id: str) -> dict:
    """Retrieve customer profile, tier, and interaction history."""
    doc = db.collection('customers').document(customer_id).get()
    if doc.exists:
        return doc.to_dict()
    return {"error": f"Customer {customer_id} not found"}

def search_knowledge_base(query: str) -> list:
    """Search product docs and company policies via RAG pipeline."""
    # Uses the RAG pipeline from our previous article
    from rag_pipeline import pipeline
    result = pipeline.query(query, top_k=5)
    return result['sources']

research_agent = LlmAgent(
    name="research_agent",
    model="gemini-3.1-flash",
    instruction="""You are a research specialist.
    1. Extract identifiers (Order ID, Customer ID) from the triage data.
    2. Use tools to gather order history and relevant company policies.
    3. If policy info is missing, use search_knowledge_base.

    CRITICAL: Do not answer the customer. Output a formal ResearchBrief.""",
    tools=[lookup_order, lookup_customer, search_knowledge_base],
    output_schema=ResearchBrief,
    output_key="research_brief"
)
```

> ***How state flows:*** *When the research agent runs, ADK automatically injects the* `*triage_data*` *from the previous step into its context. The agent "sees" that it needs to look up Order #12345 because the triage agent already identified that intent. Each agent builds on the last without redundant work.*
> 
> ***Tip:*** *ADK auto-wraps plain functions as* `*FunctionTool*` *objects. For production, you can explicitly wrap them with* `*from google.adk.tools import FunctionTool*` *to get better latency tracking and token usage logging in Vertex AI Agent Engine.*

## Step 4: Building the Action Agent (30 minutes)

The action agent is the only specialist with “write access” to your business APIs. Because it executes high-stakes operations, we use strict schemas and explicit guardrails.

First, the output schema:

```c
# common/schemas.py (add to existing file)

class ActionSummary(BaseModel):
    actions_taken: list[str] = Field(description="List of actions executed")
    refund_id: str | None = Field(default=None, description="Refund ID if issued")
    escalated: bool = Field(default=False)
    escalation_reason: str | None = Field(default=None)
```

Then the agent with human-in-the-loop confirmation for high-value operations:

```c
# agents/action.py
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from common.schemas import ResearchBrief, ActionSummary

def process_refund(order_id: str, amount: float, reason: str) -> dict:
    """Process a financial refund. Required: valid order_id and amount."""
    # In production: call your payment API
    return {
        "status": "processed",
        "refund_id": f"REF-{order_id}",
        "amount": amount
    }

def create_replacement_order(
    order_id: str,
    item_id: str,
    shipping_speed: str
) -> dict:
    """Create a replacement order with specified shipping speed."""
    # In production: call your order management API
    return {
        "status": "created",
        "new_order_id": f"REPL-{order_id}",
        "estimated_delivery": "2 business days"
    }

def escalate_to_human(reason: str, priority: str) -> dict:
    """Escalate to a human agent with full context."""
    return {
        "status": "escalated",
        "queue": "priority" if priority == "high" else "standard"
    }

# Wrap refund tool with human confirmation for high-value transactions
refund_tool = FunctionTool(
    func=process_refund,
    require_confirmation=True  # Pauses for human approval before executing
)

action_agent = LlmAgent(
    name="action_agent",
    model="gemini-3.1-flash",
    instruction="""You are an action specialist.
    Review the 'research_brief' in the session state.

    CRITICAL RULES:
    1. Only refund if 'can_refund' is True in the research brief
    2. If amount > $500, you MUST use escalate_to_human
    3. You must call tools for every action — do not just tell the user
       it happened
    4. If information is missing from the brief, escalate""",
    tools=[refund_tool, create_replacement_order, escalate_to_human],
    input_schema=ResearchBrief,   # Only sees research data, not raw chat
    output_schema=ActionSummary,
    output_key="action_result"
)
```

> ***Why*** `***require_confirmation***`***?*** *In production, you rarely let an agent process a refund purely on prompt instructions. ADK's* [*tool confirmation flow*](https://google.github.io/adk-docs/tools-custom/confirmation/) *pauses execution and waits for a human "Approve" before the function actually runs. The orchestrator sees a "pending" status and can route it to a staff member's dashboard.*
> 
> ***Why*** `***input_schema***`***?*** *Without it, the action agent can see the entire conversation history — including outdated messages from earlier turns. Restricting input to* `*ResearchBrief*` *prevents "context bleed" and ensures decisions are based on the freshest data.*

Note that `escalate_to_human` isn't a failure state — it's a deliberate business rule. The orchestrator can see exactly why the agent stopped and route the ticket to a human with the complete research brief attached.

## Step 5: Building the QA Agent (30 minutes)

The QA agent is the final gatekeeper. It doesn’t just check grammar — it cross-references the action result against the research brief to ensure the “doing” matched the “knowing.”

We use Gemini 3.1 Pro here because QA requires the model to hold the entire conversation state and spot subtle contradictions — a task where Pro consistently outperforms Flash. We also enable its [thinking mode](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/thinking) for deeper self-reflection before approving a response.

```c
# common/schemas.py (add to existing file)

class QAReview(BaseModel):
    is_approved: bool = Field(description="True if the response meets all criteria")
    feedback: str = Field(description="Specific corrections if not approved")
    final_text: str = Field(description="The customer-facing message")
```
```c
# agents/qa.py
from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai.types import ThinkingConfig
from common.schemas import QAReview

qa_agent = LlmAgent(
    name="qa_agent",
    model="gemini-3.1-pro",
    instruction="""You are a senior QA auditor. Compare the 'action_result'
    against the 'research_brief' in the session state.

    CRITICAL CHECKS:
    1. Did the Action Agent refund the EXACT amount listed in the brief?
    2. Does the response cite the policy found during research?
    3. Is the tone empathetic but professional?
    4. Are ALL intents from the triage classification addressed?
    5. No unauthorized promises, discounts, or policy exceptions

    If any check fails, set is_approved to False with specific feedback.""",
    output_schema=QAReview,
    output_key="qa_review",
    # MEDIUM for routine QA; switch to HIGH for edge cases or audits
    planner=BuiltInPlanner(
        thinking_config=ThinkingConfig(thinking_level="MEDIUM")
    )
)
```

> ***The correction loop:*** *If* `*qa_review.is_approved*` *is* `*False*`*, the orchestrator doesn't just fail — it reads the* `*feedback*` *field and re-routes to the action agent (or research agent) with specific corrections. This "self-correction loop" is what separates production agents from demo scripts. We cap it at 2 revision cycles before escalating to a human (see the orchestrator in Step 6).*

## Step 6: The Orchestrator — Bringing It All Together (1 hour)

The orchestrator doesn’t “do” research or “take” action — it manages state and ensures the specialists talk to each other in the right order.

In ADK, when you give an agent `sub_agents`, AutoFlow automatically injects a `transfer_to_agent()` tool. The orchestrator's LLM decides who to call next based on its instructions and the current session state:

```c
# agents/orchestrator.py
from google.adk.agents import LlmAgent
from agents.triage import triage_agent
from agents.research import research_agent
from agents.action import action_agent
from agents.qa import qa_agent

orchestrator = LlmAgent(
    name="support_orchestrator",
    model="gemini-3.1-pro",  # Best reasoning for delegation decisions
    instruction="""You are the lead coordinator of a customer support team.
    Use the following specialists in order:
    1. triage_agent: to classify the intent and urgency
    2. research_agent: to gather order data and relevant policies
    3. action_agent: to execute the required operations
    4. qa_agent: to verify the final response

    Special cases:
    - If triage classifies as 'critical': bypass the chain and escalate
    - If QA returns is_approved=False: re-route to the responsible agent
      with the feedback (maximum 2 revision cycles, then escalate)
    - If any agent fails: escalate to human with full context

    You must never respond to the customer directly.
    Always route through the specialist pipeline.""",
    sub_agents=[triage_agent, research_agent, action_agent, qa_agent]
)
```

## Running the Orchestrator

ADK uses a `Runner` to handle the execution loop — it knows how to pause when an agent calls a tool, wait for the result, and wake the agent back up:

```c
# main.py
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agents.orchestrator import orchestrator

APP_NAME = "customer_support"
USER_ID = "system"

# For production, replace with a Firestore-backed session service
session_service = InMemorySessionService()

runner = Runner(
    agent=orchestrator,
    app_name=APP_NAME,
    session_service=session_service
)

async def handle_customer_message(customer_id: str, message: str):
    """
    Entry point for customer messages.
    """
    session_id = f"support-{customer_id}"

    # Ensure session exists
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_id
    )
    if not session:
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )

    # run_async yields events as agents execute
    final_response = None
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=message
    ):
        if event.is_final_response():
            final_response = event

    return {
        "response": final_response.content.parts[0].text if final_response else None,
        "session_id": session_id
    }
```

> ***Why*** `***Runner***` ***instead of calling agents directly?*** *The Runner handles the full execution loop: it manages session persistence, tracks which agent is active, processes tool calls, and logs every step. Because each agent stores its output in the session state via* `*output_key*`*, the Runner ensures the research brief is available when the action agent needs it — without you writing any plumbing code.*
> 
> ***Traceability for free:*** *Every agent call, tool invocation, and handoff is logged as an event. This is the “debugging nightmare” fix from the intro — when something goes wrong, you can trace exactly which agent made which decision and why.*

## Step 7: Deploying to Production (30 minutes)

You have two paths: **Vertex AI Agent Engine** for a fully managed runtime, or **Cloud Run** for custom control.

## Option A: Vertex AI Agent Engine (Recommended)

The low-ops route. Deploy your ADK agents directly to Google’s managed runtime with a single command:

```c
PROJECT_ID=your-project-id
LOCATION_ID=us-central1
```
```c
adk deploy agent_engine \
  --project=$PROJECT_ID \
  --region=$LOCATION_ID \
  --display_name="Customer Support Team" \
  support_agents
```

Agent Engine handles scaling, session persistence, and agent-specific trace logging automatically. No Dockerfile, no session management code, no infrastructure to maintain.

## Option B: Cloud Run (Custom Control)

Use this if you need custom system libraries, specific networking (like VPC-SC), or non-ADK components. We use [Quart](https://github.com/pallets/quart) instead of Flask — it has identical syntax but handles `async/await` natively, avoiding the `asyncio.run()` anti-pattern that creates a new event loop per request:

```c
# server.py
from quart import Quart, request, jsonify
from main import handle_customer_message

app = Quart(__name__)

@app.route("/support", methods=["POST"])
async def support():
    data = await request.get_json()
    # No asyncio.run needed — Quart handles the event loop
    result = await handle_customer_message(
        data["customer_id"],
        data["message"]
    )
    return jsonify(result)

@app.route("/health", methods=["GET"])
async def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```
```c
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["python", "server.py"]
```
```c
gcloud run deploy support-agents \
  --source . \
  --region us-central1 \
  --memory 4Gi \
  --cpu 2 \
  --allow-unauthenticated
```

## Which should you choose?

**Cloud Run** — Medium setup effort (Dockerfile + API). Manual state management (Firestore/Redis). Standard Cloud Logging. Best for custom runtimes and frameworks.

**Vertex AI Agent Engine** — Low setup effort (single command). Native built-in sessions. Agent-specific trace logs. Best for ADK-native agents and fast scaling.

## Step 8: Persistent Sessions for Multi-Turn Conversations (30 minutes)

In Step 6, we used `InMemorySessionService` — fine for testing, but everything is lost when the process restarts. For production, ADK offers two persistent options:

## Option A: Vertex AI Session Service (Recommended with Agent Engine)

If you deployed via Agent Engine, sessions are managed automatically:

```c
# config.py
from google.adk.sessions import VertexAiSessionService

session_service = VertexAiSessionService(
    project="your-project-id",
    location="us-central1",
    agent_engine_id="your-agent-engine-id"  # From adk deploy output
)
```

Agent Engine handles persistence, summarization of long histories, and cleanup — no Firestore code needed.

## Option B: Database Session Service (For Cloud Run deployments)

For Cloud Run, use `DatabaseSessionService` with a PostgreSQL or SQLite backend:

```c
# config.py
from google.adk.sessions import DatabaseSessionService

# PostgreSQL for production
session_service = DatabaseSessionService(
    db_url="postgresql+asyncpg://user:pass@host:5432/agents"
)

# Or SQLite for development
session_service = DatabaseSessionService(
    db_url="sqlite+aiosqlite:///sessions.db"
)
```

The session service creates the necessary tables automatically on initialization. Swap this into the `Runner` from Step 6 and session state persists across restarts.

## How State Flows Between Agents

You don’t need manual `get()` / `set()` calls. Each agent's `output_key` automatically writes to the session state, and downstream agents read from it:

```c
triage_agent (output_key="triage_data")
    ↓ writes to session.state["triage_data"]
research_agent (reads triage_data, output_key="research_brief")
    ↓ writes to session.state["research_brief"]
action_agent (input_schema=ResearchBrief, output_key="action_result")
    ↓ writes to session.state["action_result"]
qa_agent (reads action_result + research_brief, output_key="qa_review")
```

The Runner persists this entire state to whichever session service you configured — Firestore, PostgreSQL, or Agent Engine.

## Memory Design Principles

**Summarization** — Don’t store every raw API response. Summarize it. Otherwise you’ll hit the LLM’s context window limit (context bloat).

**TTL (Time to Live)** — Support sessions should expire. Set a 24–48 hour TTL to keep your database lean and secure.

**Privacy** — Never store raw PII (SSNs, passwords) in shared state. Mask it before the research agent writes to the session.

## When Multi-Agent Beats Single-Agent (And When It Doesn’t)

Multi-agent isn’t always the right choice. Here’s a practical decision framework:

- **Simple FAQ / status check** — Use single agent. Lowest latency and cost; no complex reasoning needed.
- **Data enrichment (3–5 tool lookups)** — Use single agent. One LLM call handles basic tool use efficiently.
- **Regulated workflows** — Use multi-agent. Isolation: keep “action” logic separate from user input to prevent prompt injection.
- **Ambiguous routing** — Use multi-agent. A dedicated triage agent specializes in intent-mapping, reducing constraint bleed.
- **High-stakes actions (>$500)** — Use multi-agent. Enables a double-check pattern (QA agent) before hitting an API.
- **Audit trail requirements** — Use multi-agent. Each agent’s input/output is logged separately.

**Rule of thumb:** If your single-agent prompt is approaching 3,000 tokens (where we hit constraint bleed and attention dilution), or if you need different tools for different parts of the workflow, it’s time to decompose into agents.

## Common Pitfalls and Solutions

**The “Everything Agent”** — *Symptom:* Performance drops when a single agent has 10+ tools — research shows LLMs start focusing on tool selection instead of the user’s intent. *Solution:* Decompose by capability. If an agent needs refund, shipping, and legal tools, give them to three specialists.

**Context hyper-inflation** — *Symptom:* Every agent sees the full 10-turn chat history; token costs explode. *Solution:* Use state compaction. The triage agent passes only the detected intent, not the customer’s entire conversation.

**Infinite handoff loops** — *Symptom:* Agent A sends to Agent B, which sends back to Agent A, burning tokens in a circle. *Solution:* Implement a max handoff counter in the orchestrator (we use 2 cycles before human escalation).

**Unclear boundaries** — *Symptom:* Two agents try to handle the same task, or a task falls between agents. *Solution:* Define explicit `input_schema` / `output_schema` contracts; no overlapping responsibilities.

**Ignoring latency** — *Symptom:* Sequential pipeline adds 4–6s vs. 1–2s for single-agent. *Solution:* Use ADK’s `ParallelAgent` to fan out independent tasks. Running research and compliance checks in parallel can cut 30–40% of total latency.

## Performance Expectations

Multi-agent systems trade latency for reliability on complex tasks. Based on published benchmarks and industry experience with agentic architectures:

**Where multi-agent excels:**

- **Complex task accuracy** — Decomposing multi-step problems into focused subtasks consistently outperforms monolithic approaches. Google’s ADK documentation reports improved task completion rates when agents have focused responsibilities.
- **Error isolation** — When one component fails, the blast radius is contained to that agent, not the entire response.
- **Auditability** — Each agent’s input/output is logged separately, making debugging and compliance straightforward.

**The cost:**

- **Latency** — Expect 3–8s total for a full 5-agent pipeline (vs. 1–2s for single-agent). Sequential agent calls are the primary bottleneck.
- **API costs** — More agents = more Gemini API calls. A 5-agent system (orchestrator + 4 specialists) costs roughly 4–5x a single-agent call per query, but model mixing keeps this manageable. By routing simple triage to Flash-Lite ($0.25/1M input) and reserving Pro ($2/1M input) for orchestration and QA only, the blended cost per interaction stays under $0.01.
- **Thinking token tax** — Pro’s extended thinking (`thinking_level="HIGH"`) can add ~20K tokens to a response. These are billed at the output token rate ($12/1M), so a single QA review with deep reasoning costs ~$0.24 in thinking tokens alone. Use HIGH thinking selectively — most QA passes work fine with MEDIUM.
- **Complexity** — More moving parts to monitor and maintain. Worth it for complex workflows; overkill for simple ones.

## Approximate Monthly Cost (100K complex queries/month)

- **Orchestrator (routing decisions):** Gemini 3.1 Pro — ~$80
- **Triage Agent:** Gemini 3.1 Flash-Lite — ~$20
- **Research Agent:** Gemini 3.1 Flash — ~$40
- **Action Agent:** Gemini 3.1 Flash — ~$40
- **QA Agent (with MEDIUM thinking):** Gemini 3.1 Pro — ~$100
- **Cloud Run (2 vCPU, 2 GiB):** ~$120
- **Database sessions (PostgreSQL):** ~$30
- **Vector Search (RAG, shared with single-agent):** ~$100
- **Total: ~$530/month**

The key insight: **model mixing is the cost lever.** Only ~30% of agent calls hit Pro pricing (orchestrator + QA). The rest use Flash or Flash-Lite, which are 8–50x cheaper per token. Unit cost per complex interaction: ~$0.005.

Estimates based on [Google Cloud’s published pricing](https://cloud.google.com/vertex-ai/pricing). Actual costs vary with query complexity, thinking level, and agent call depth.

## What’s Next

This concludes our five-part series on architecting production-grade AI on Google Cloud:

1. **Deployment:** [Setting up the foundation on Cloud Run](https://medium.com/google-cloud/how-to-deploy-your-first-google-cloud-app-in-minutes-f5cec4645198)
2. **Interaction:** [Building your first agent with Gemini](https://medium.com/google-cloud/building-an-intelligent-customer-support-agent-with-googles-gemini-2-5-10df5baa4c1d)
3. **Optimization:** [Masterclass in Prompt Engineering](https://medium.com/google-cloud/advanced-prompt-engineering-from-90-to-95-automation-the-100k-difference-c4008398ee14)
4. **Grounding:** [Building a high-density RAG Pipeline with Vertex AI Vector Search](https://medium.com/@anevsky/building-a-rag-pipeline-with-gemini-2-5-91546c2ceaf6)
5. **Orchestration:** Moving to Multi-Agent Systems with ADK (this post)

Each layer builds on the last. Start with a single agent, optimize its logic, ground it with RAG, and only decompose into specialists once your system prompt grows too long or your tasks too diverse for a single model to handle reliably.

## Conclusion

Multi-agent systems aren’t about making AI more complicated — they’re about making complex workflows predictable. This is the **microservices moment for AI**: moving from a monolithic prompt to a distributed architecture where each component has a single responsibility.

A single agent attempting to handle triage, research, action, and quality control simultaneously is like asking one person to be the receptionist, the lead analyst, the technician, and the auditor all at once. It works in a startup of one; it fails in an enterprise.

By providing each agent with a focused responsibility, specialized tools, and a shared memory layer, you create a system that is:

- **Accurate** — Focused prompts reduce logic drift across unrelated tasks.
- **Debuggable** — You can see exactly which specialist failed and why.
- **Cost-efficient** — Running a 5-agent system on the Gemini 3.1 series costs ~$0.005 per complex interaction — less than a single minute of a human agent’s time.

The future of this architecture is even more expansive. With the [Agent-to-Agent (A2A) protocol](https://google.github.io/adk-docs/a2a/), an open standard governed by the Linux Foundation, the system we built today can eventually negotiate with agents from your vendors or partners — for example, your Support Agent talking directly to a Shipping Provider’s Agent to resolve a lost package without human intervention.

**Start simple.** Build a single agent. When the prompt grows too long or the tasks too diverse, decompose. Your production metrics — and your future self — will thank you.

*About the Author*

I’m Alex Nevsky, Software Engineer with 15+ years of software development experience and specialization in AI/Web/Cloud, including Google Cloud AI technologies and AWS.

I help people leverage cutting-edge AI to solve real-world problems.

Currently focusing on Gemini API implementations, Vertex AI MLOps, and scalable cloud architectures.

Connect with me:

- [LinkedIn](https://www.linkedin.com/in/anevsky/)
- [GitHub](https://github.com/anevsky)
- [Twitter/X](https://x.com/anevsky)