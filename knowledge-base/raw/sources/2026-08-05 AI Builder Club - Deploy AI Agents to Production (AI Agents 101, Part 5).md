---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-ai-agents-101-part-5
title: Deploy AI Agents to Production (AI Agents 101, Part 5)
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/ai-agents-101-part-5
published: '2026-06-02'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Deploy AI Agents to Production (AI Agents 101, Part 5)

## You've Built the Agent. Now It Needs to Run Without You.

In [Part 1](https://www.aibuilderclub.com/blog/ai-agents-101-part-1), you built the agent loop. In [Part 2](https://www.aibuilderclub.com/blog/ai-agents-101-part-2), you gave it tools. In [Part 3](https://www.aibuilderclub.com/blog/ai-agents-101-part-3), you gave it memory. In [Part 4](https://www.aibuilderclub.com/blog/ai-agents-101-part-4), you scaled it into multi-agent systems.

All of that runs beautifully on your laptop. But a laptop agent that only works when you're watching it is a demo, not a product.

This final part of the series covers everything between "it works locally" and "it runs reliably in production." By the end, you'll have a containerised agent deployed on a VPS, structured logs you can query, health checks that catch failures before your users do, and a cost control layer that prevents a runaway agent from generating a $500 API bill overnight.

No cloud-native complexity. No Kubernetes. A single VPS, a Dockerfile, and the right observability setup — that's everything you need to ship agents that run at under $50/month.

## Why "Just Deploy It" Doesn't Work for Agents

Deploying a standard web app is predictable. You package it, run it, and it serves requests. An AI agent is different in three important ways that most deployment guides ignore:

- **Unbounded execution.** A regular endpoint takes 200ms. An agent can run for 30 seconds, 5 minutes, or infinitely if it loops. Your infrastructure needs to handle open-ended tasks without timing out.
- **Non-deterministic cost.** Each agent run costs money in API tokens. A bug can trigger thousands of LLM calls before anyone notices. You need cost guards at the infrastructure level, not just in your code.
- **Opaque failures.** When a web server fails, you see a 500 error. When an agent fails mid-task, it may look like it "completed" while producing garbage output. Observability for agents requires logging decisions, not just responses.

The deployment stack you'll build in this guide addresses all three.

## Step 1: Containerise Your Agent with Docker

Docker gives you a reproducible environment — the same Python version, the same dependencies, the same configuration — whether it runs on your laptop, a CI pipeline, or a VPS in Frankfurt.

### Project structure before containerising

bash

```
my-agent/
├── agent.py          # Main agent logic
├── tools.py          # Tool implementations
├── memory.py         # Memory layer
├── requirements.txt  # Python dependencies
├── .env              # Secrets (never committed)
└── Dockerfile        # Build instructions
```

### A production-ready Dockerfile

dockerfile

```
# Use a specific Python version — never use latest
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies first (cached layer)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies (cached if requirements.txt unchanged)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user for security
RUN useradd -m -u 1000 agent && chown -R agent:agent /app
USER agent

# Health check endpoint — more on this in Step 4
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the agent
CMD ["python", "agent.py"]
```

### The requirements.txt that matters

text

```
openai==1.30.1
anthropic==0.28.0
httpx==0.27.0
pydantic==2.7.1
python-dotenv==1.0.1
structlog==24.2.0
fastapi==0.111.0
uvicorn==0.30.1
```

Pin every version. "Latest" in production is a reliability trap — a minor version bump in the OpenAI SDK has broken production agents before.

### Build and test locally

bash

```
# Build the image
docker build -t my-agent:latest .

# Run with env vars from .env file
docker run --env-file .env -p 8000:8000 my-agent:latest

# Verify it starts
curl http://localhost:8000/health
```

## Step 2: Choose Your Runtime — VPS vs Serverless

The two realistic options for agents at the indie developer scale are a VPS (like Hetzner or DigitalOcean) or a serverless platform (like Railway, Fly.io, or AWS Lambda). Here's how to decide:

| Factor | VPS (e.g. Hetzner CX22) | Serverless (e.g. Railway) |
| --- | --- | --- |
| Monthly cost | ~$5–8/month fixed | $0–20/month based on usage |
| Task duration | Unlimited | Typically 15 min max |
| Cold start | None (always running) | 1–5 seconds |
| Setup complexity | Medium (you manage the OS) | Low (git push to deploy) |
| Best for | Long-running agents, scheduled tasks | Short webhook handlers, event-driven agents |

**The rule of thumb:** if your agent runs for more than 60 seconds or runs on a schedule, use a VPS. If it's triggered by a webhook and completes in under a minute, serverless is fine.

The rest of this guide assumes a VPS because most real agent workloads need it. The code patterns apply equally to serverless.

### Deploy to a Hetzner VPS (under $10/month)

bash

```
# On your local machine — install hcloud CLI
brew install hcloud

# Create a server (CX22 = 2 vCPU, 4GB RAM, $5.52/month)
hcloud server create \
  --name my-agent-server \
  --type cx22 \
  --image ubuntu-24.04 \
  --ssh-key my-key

# Get the IP
hcloud server list

# SSH in
ssh root@YOUR_SERVER_IP
```

## Install Docker

curl -fsSL <https://get.docker.com> | sh
systemctl enable docker
systemctl start docker

bash

```
# On the server — clone your repo and deploy
git clone https://github.com/your-username/my-agent.git
cd my-agent

# Create .env with your secrets
nano .env

# Build and run
docker build -t my-agent:latest .
docker run -d \
  --name agent \
  --restart unless-stopped \
  --env-file .env \
  -p 8000:8000 \
  my-agent:latest

# Verify it's running
docker ps
curl http://localhost:8000/health
```

The `--restart unless-stopped` flag means Docker will restart your container automatically if it crashes or if the server reboots. This is your baseline reliability mechanism.

## Step 3: Structured Logging — The Thing That Saves You at 2am

Standard print statements are useless in production. When an agent fails mid-task, you need to know: which step failed, what the agent was thinking, what tool it called, and what the tool returned. That means structured logs — JSON lines you can query and filter.

### Set up structlog

python

```
import structlog
import logging
import sys

def configure_logging():
    """Configure structured JSON logging for production."""
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),  # JSON output in production
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

    # Also configure stdlib logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

configure_logging()
logger = structlog.get_logger()
```

### Log every decision, not just every error

python

```
import uuid
from openai import OpenAI

client = OpenAI()

def run_agent_with_logging(task: str, user_id: str = None) -> str:
    """Run the agent loop with structured logging at every step."""

    run_id = str(uuid.uuid4())[:8]  # Short ID for correlating logs

    log = logger.bind(
        run_id=run_id,
        user_id=user_id,
        task=task[:100],  # Truncate for log brevity
    )

    log.info("agent_run_started")

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": task}
    ]

    step = 0
    max_steps = 10

    while step < max_steps:
        step += 1

        log.info("llm_call_started", step=step, message_count=len(messages))

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=[...],  # Your tool definitions
            )
        except Exception as e:
            log.error("llm_call_failed", step=step, error=str(e), exc_info=True)
            raise

        message = response.choices[0].message

        log.info(
            "llm_response_received",
            step=step,
            finish_reason=response.choices[0].finish_reason,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            has_tool_calls=bool(message.tool_calls),
        )

        if response.choices[0].finish_reason == "stop":
            log.info("agent_run_completed", step=step, total_steps=step)
            return message.content

        # Process tool calls
        if message.tool_calls:
            messages.append(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name

                log.info(
                    "tool_call_started",
                    step=step,
                    tool=tool_name,
                    tool_call_id=tool_call.id,
                )

                try:
                    result = execute_tool(tool_call)

                    log.info(
                        "tool_call_completed",
                        step=step,
                        tool=tool_name,
                        result_length=len(str(result)),
                    )
                except Exception as e:
                    log.error(
                        "tool_call_failed",
                        step=step,
                        tool=tool_name,
                        error=str(e),
                        exc_info=True,
                    )
                    result = f"Error: {str(e)}"

                messages.append({
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tool_call.id,
                })

    log.warning("agent_max_steps_reached", max_steps=max_steps)
    return "Task incomplete — max steps reached."
```

Every log line is a JSON object. When something goes wrong, you can filter by `run_id` to see the complete execution trace. When costs spike, you can filter by `prompt_tokens` and `completion_tokens` to find the expensive runs.

### Query logs on your VPS

bash

```
# Tail logs in real time
docker logs -f agent

# Find all failed tool calls
docker logs agent 2>&1 | grep '"event":"tool_call_failed"'

# Find all runs that hit max steps
docker logs agent 2>&1 | grep '"event":"agent_max_steps_reached"'

# Calculate total tokens used today
docker logs agent 2>&1 | python3 -c "
import sys, json
total_prompt = total_completion = 0
for line in sys.stdin:
    try:
        obj = json.loads(line)
        if obj.get('event') == 'llm_response_received':
            total_prompt += obj.get('prompt_tokens', 0)
            total_completion += obj.get('completion_tokens', 0)
    except:
        pass
print(f'Prompt tokens: {total_prompt:,}')
print(f'Completion tokens: {total_completion:,}')
print(f'Estimated cost (GPT-4o): ${(total_prompt * 0.0000025 + total_completion * 0.00001):.4f}')
"
```

## Step 4: Health Checks That Actually Work

A health check endpoint tells your infrastructure — Docker, load balancers, monitoring tools — whether the agent is alive and ready to accept work. But most health checks just return `{"status": "ok"}` without checking anything real.

Here's a health check that actually verifies your agent's dependencies:

python

```
from fastapi import FastAPI
from pydantic import BaseModel
import time
import os

app = FastAPI()

class HealthResponse(BaseModel):
    status: str  # "healthy" | "degraded" | "unhealthy"
    checks: dict
    uptime_seconds: float

START_TIME = time.time()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    checks = {}
    overall_status = "healthy"

    # Check 1: OpenAI API reachability
    try:
        import openai
        client = openai.OpenAI()
        # Use a lightweight models list call, not a chat completion
        client.models.list()
        checks["openai_api"] = "ok"
    except Exception as e:
        checks["openai_api"] = f"error: {str(e)[:50]}"
        overall_status = "degraded"

    # Check 2: Memory/database connectivity (if applicable)
    try:
        # Replace with your actual DB check
        checks["memory_store"] = "ok"
    except Exception as e:
        checks["memory_store"] = f"error: {str(e)[:50]}"
        overall_status = "unhealthy"

    # Check 3: Disk space (agents can generate a lot of temp files)
    try:
        import shutil
        usage = shutil.disk_usage("/")
        free_gb = usage.free / (1024**3)
        if free_gb < 1.0:
            checks["disk_space"] = f"low: {free_gb:.1f}GB free"
            overall_status = "degraded"
        else:
            checks["disk_space"] = f"ok: {free_gb:.1f}GB free"
    except Exception as e:
        checks["disk_space"] = f"error: {str(e)[:50]}"

    return HealthResponse(
        status=overall_status,
        checks=checks,
        uptime_seconds=round(time.time() - START_TIME, 1),
    )

# Liveness probe — just confirms the process is running
@app.get("/ping")
async def ping():
    return {"pong": True}
```

Run this FastAPI app alongside your agent (in a background thread or as a separate lightweight process). Docker's `HEALTHCHECK` directive will call `/health` every 30 seconds and restart the container if it fails 3 times in a row.

## Step 5: Cost Controls — The $50/Month Hard Limit

This is the step most deployment guides skip. Without it, a single bug — an infinite loop, a malformed tool response that confuses the agent, a user who submits a task that fans out to 100 sub-tasks — can generate hundreds of dollars in API costs overnight.

Cost controls belong at three levels:

### Level 1: Per-run token budget

python

```
class AgentConfig:
    max_steps: int = 10
    max_tokens_per_run: int = 50_000  # ~$0.50 per run on GPT-4o
    max_concurrent_runs: int = 5

class TokenBudgetExceeded(Exception):
    pass

def run_agent_with_budget(task: str, config: AgentConfig) -> str:
    total_tokens = 0

    # ... agent loop ...

    response = client.chat.completions.create(...)

    total_tokens += response.usage.total_tokens

    if total_tokens > config.max_tokens_per_run:
        logger.warning(
            "token_budget_exceeded",
            total_tokens=total_tokens,
            limit=config.max_tokens_per_run,
        )
        raise TokenBudgetExceeded(
            f"Run aborted: used {total_tokens} tokens "
            f"(limit: {config.max_tokens_per_run})"
        )

    # ... continue loop ...
```

### Level 2: Daily spend cap via a lightweight tracker

python

```
import json
from pathlib import Path
from datetime import date
from threading import Lock

SPEND_FILE = Path("/app/data/daily_spend.json")
DAILY_LIMIT_USD = 10.0  # Hard cap: $10/day
spend_lock = Lock()

# GPT-4o pricing (per token)
COST_PER_PROMPT_TOKEN = 0.0000025
COST_PER_COMPLETION_TOKEN = 0.00001

def record_spend(prompt_tokens: int, completion_tokens: int) -> float:
    """Record token usage and return today's total spend in USD."""
    cost = (
        prompt_tokens * COST_PER_PROMPT_TOKEN +
        completion_tokens * COST_PER_COMPLETION_TOKEN
    )

    today = str(date.today())

    with spend_lock:
        data = {}
        if SPEND_FILE.exists():
            data = json.loads(SPEND_FILE.read_text())

        if today not in data:
            data[today] = 0.0

        data[today] += cost
        SPEND_FILE.write_text(json.dumps(data))

        return data[today]

def check_daily_limit():
    """Raise if today's spend has hit the daily cap."""
    today = str(date.today())

    if not SPEND_FILE.exists():
        return

    data = json.loads(SPEND_FILE.read_text())
    today_spend = data.get(today, 0.0)

    if today_spend >= DAILY_LIMIT_USD:
        raise Exception(
            f"Daily spend limit reached: ${today_spend:.4f} "
            f"(cap: ${DAILY_LIMIT_USD})"
        )
```

### Level 3: OpenAI usage limits in the dashboard

Set a hard monthly budget in your OpenAI account under **Settings → Billing → Usage limits**. This is your last-resort protection. Set it to 2x your expected monthly spend. When it's hit, the API returns a `429` — your agent fails gracefully (it should, with proper error handling from Part 2) rather than continuing to accumulate cost.

## Step 6: Monitoring That Wakes You Up Before Your Users

For indie agents at this scale, you need exactly two things: something that checks your agent is alive, and something that alerts you when it's not.

### Option A: UptimeRobot (free, 5-minute checks)

Sign up at uptimerobot.com, add your `/health` endpoint as an HTTP monitor, and configure it to send you an email or Slack message when it returns anything other than 200. This costs nothing and catches the most common failure: the container crashed and nobody noticed.

### Option B: Self-hosted Uptime Kuma (one command)

bash

```
# On your VPS — run Uptime Kuma alongside your agent
docker run -d \
  --name uptime-kuma \
  --restart unless-stopped \
  -p 3001:3001 \
  -v uptime-kuma:/app/data \
  louislam/uptime-kuma:latest
```

Open `http://YOUR_SERVER_IP:3001`, add your agent's health endpoint as a monitor, configure notifications (Telegram, Slack, Discord — all free). Total setup time: 10 minutes.

### Alerting on cost spikes

Add a daily cron job on your VPS that checks yesterday's spend and alerts you if it was above threshold:

bash

```
# crontab -e
# Run every day at 08:00
0 8 * * * python3 /app/check_spend.py
```

python

```
#!/usr/bin/env python3
# /app/check_spend.py
import json
from pathlib import Path
from datetime import date, timedelta
import os
import httpx

SPEND_FILE = Path("/app/data/daily_spend.json")
ALERT_THRESHOLD_USD = 5.0
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")  # Optional

yesterday = str(date.today() - timedelta(days=1))

if SPEND_FILE.exists():
    data = json.loads(SPEND_FILE.read_text())
    spend = data.get(yesterday, 0.0)

    print(f"Yesterday's spend: ${spend:.4f}")

    if spend > ALERT_THRESHOLD_USD and SLACK_WEBHOOK:
        httpx.post(SLACK_WEBHOOK, json={
            "text": f"Agent cost alert: ${spend:.4f} spent yesterday (threshold: ${ALERT_THRESHOLD_USD})"
        })
```

## Putting It All Together: A Production Deployment Checklist

Here's the checklist you run before calling an agent "production-ready":

### Infrastructure

- [ ] Dockerfile with pinned Python version and pinned dependency versions
- [ ] Non-root user in the container
- [ ] `--restart unless-stopped` on the Docker run command
- [ ] Secrets in environment variables (never hardcoded, never in the image)

### Observability

- [ ] Structured JSON logging with `run_id`, step counts, token usage per call
- [ ] `/health` endpoint that checks real dependencies (not just "server is up")
- [ ] `/ping` liveness endpoint for fast load balancer checks
- [ ] Uptime monitoring (UptimeRobot or Uptime Kuma) on the health endpoint

### Cost controls

- [ ] Per-run token budget that aborts long/expensive runs
- [ ] Daily spend tracker written to disk
- [ ] OpenAI dashboard hard limit set to 2x expected monthly spend
- [ ] Daily spend alert cron job

### Reliability

- [ ] Max steps limit on every agent loop (never unbounded)
- [ ] Error handling on every tool call (from Part 2 of this series)
- [ ] Graceful degradation when dependencies are down (fallback responses)

## The Real $50/Month Setup

Here's what this costs when you run it properly:

- **Hetzner CX22 VPS**: $5.52/month
- **OpenAI API** (typical indie agent at ~5,000 runs/month, ~10K tokens each): ~$25–35/month
- **UptimeRobot** (free tier): $0
- **Total**: $30–40/month for a fully monitored, self-healing agent in production

The agents that blow past $50/month are always missing one thing from this guide: the per-run token budget. One stuck agent loop eats more in an hour than a week of normal operation.

## What Comes Next

This is the final part of the AI Agents 101 series. You now have everything you need to build a production agent from scratch:

- [Part 1](https://www.aibuilderclub.com/blog/ai-agents-101-part-1): The agent loop — the fundamental pattern behind every AI agent
- [Part 2](https://www.aibuilderclub.com/blog/ai-agents-101-part-2): Tools — web search, code execution, file writing with proper error handling
- [Part 3](https://www.aibuilderclub.com/blog/ai-agents-101-part-3): Memory — short-term, long-term, semantic, and episodic memory layers
- [Part 4](https://www.aibuilderclub.com/blog/ai-agents-101-part-4): Multi-agent systems — pipeline, supervisor/worker, and fan-out patterns
- Part 5 (this guide): Deploying to production — Docker, VPS, logging, health checks, cost controls

The next step is building something real with it. The AI Builder Club is where developers share what's actually working — production agents, failure post-mortems, real cost numbers, and the patterns that didn't make it into tutorials.

[Join AI Builder Club](https://www.aibuilderclub.com/auth/signin?utm_source=blog&utm_medium=article&utm_campaign=ai-agents-101-part-5) to connect with developers who are deploying agents, not just building demos.

This guide is written from hands-on testing, then cross-checked against primary sources - official documentation and first-party announcements. Field results and opinions are labeled as such. See our [editorial standards](/about).
