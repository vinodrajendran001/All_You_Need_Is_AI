---
title: "Agents That Prove, Not Guess: A Multi-Agent Code Review System"
source: "https://medium.com/google-cloud/agents-that-prove-not-guess-a-multi-agent-code-review-system-e2c0a735e994"
author:
  - "[[Ayo Adedeji]]"
published: 2025-10-10
created: 2026-09-13
description: "More"
tags:
  - "clippings"
---
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ZembufthhBaiIF-ZYkHCSg.png)

## The LeetCode Challenge

I gave Gemini 2.5 Pro a LeetCode Hard [problem](https://leetcode.com/problems/max-points-on-a-line/): “Max Points on a Line.”

> *Given an array of* `*points*` *where* `*points[i] = [xi, yi]*` *represents a point on the X-Y plane*, *return* *the maximum number of points that lie on the same straight line*.

The model generated this solution:

```c
def maxPoints(self, points: List[List[int]]) -> int:
  # … setup code …
  dx = p2[0] - p1[0]
  dy = p2[1] - p1[1]

  if dx == 0:
    slope_key = float('inf')
  else:
    common_divisor = math.gcd(dy, dx)
    slope_key = (dy // common_divisor, dx // common_divisor)
```

It passed most test cases but failed on 13.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*0ZUa7BFpyA-8Kjx789QD0A.png)

LeetCode Test Interface

The bug? The slope representation isn’t normalized. A line with slope -1 could be stored as (1, -1) or (-1, 1) depending on which two points you pick first. The code treats these as different lines, splitting the count. This is the kind of subtle error that’s hard to spot in code review — even for experienced developers, and even for capable LLMs on their first attempt.

## The Limits of Single-Pass Generation

Gemini 2.5 Pro is incredibly [capable](https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/#gemini-2-5-pro?utm_campaign=CDR_0x8f8b61f4_default&utm_medium=external&utm_source=blog). When given the [code execution](https://ai.google.dev/gemini-api/docs/code-execution?utm_campaign=CDR_0x8f8b61f4_default&utm_medium=external&utm_source=blog) tool, it can iteratively test and refine solutions — I verified this by giving it the same LeetCode problem, and it solved it correctly.

But even with these capabilities, there are architectural trade-offs. Code execution happens within a single model context. The iteration is internal and opaque. You get the final answer, but the validation steps aren’t exposed as observable state that other systems can consume. Every step of the process — analysis, testing, synthesis — happens in one model invocation with no separation of concerns.

These aren’t failures of the model. They’re inherent architectural characteristics of integrated code execution.

What if we wanted something different? Explicit pipelines where each validation step is observable and replayable. Where you can mix deterministic tools (AST parsing, pycodestyle) with LLM reasoning strategically. Where a fast model handles mechanical tasks while a powerful model tackles complex synthesis. Where state is explicit, inspectable, and persistent across agent boundaries.

That’s what a multi-agent architecture provides: transparency, composability, and control.

## A Different Approach: Multi-Agent System

I submitted the same code to a multi-agent [system](https://github.com/ayoisio/adk-code-review-assistant) built with Google’s [Agent Development Kit](https://google.github.io/adk-docs/) (ADK). The system breaks code review into four specialized agents, each with specific tools and responsibilities.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*xWpK7RmqTJBbDyKw.png)

Code Review (SequentialAgent) Architecture

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*M91ZAVaenp2xFs9uuEFvXQ.gif)

Code Review (SequentialAgent) In Action

### Agent 1: Code Analyzer — Structural Verification

The first [agent](https://github.com/ayoisio/adk-code-review-assistant/blob/main/code_review_assistant/sub_agents/review_pipeline/code_analyzer.py) uses Python’s `ast.parse()` to analyze the code structure. The tool performs actual [Abstract Syntax Tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree) validation, confirming the code contains valid Python syntax with one class, one method called maxPoints, and proper dependencies on the math and typing modules.

This deterministic check establishes a baseline: the code is syntactically valid before we proceed with deeper analysis.

### Agent 2: Style Checker — Quality Baseline

The second [agent](https://github.com/ayoisio/adk-code-review-assistant/blob/main/code_review_assistant/sub_agents/review_pipeline/style_checker.py) runs [pycodestyle](https://pycodestyle.pycqa.org/en/latest/), the standard PEP 8 linter for Python. The tool scored the code at 90 out of 100, noting good naming conventions, proper spacing, and clear logic flow. This provides measurable compliance with common standards.

### Agent 3: Test Runner — Executable Proof

This is where the system reveals its power. The third [agent](https://github.com/ayoisio/adk-code-review-assistant/blob/main/code_review_assistant/sub_agents/review_pipeline/test_runner.py) generates **20** comprehensive test cases and executes them in a sandboxed Python environment using the [BuiltInCodeExecutor](https://google.github.io/adk-docs/tools/built-in-tools/#code-execution) tool.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*xlmo6zuEFqkWsc-ERRcOpw.gif)

Test Runner Agent In Action

The results: 19 tests passed, 1 failed. The test actually ran and produced concrete output.

The failing test case was `points = [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]`. The code returned 3, but the correct answer is 4. The agent identified the root cause: when calculating the line through points (1,4) and (4,1), the slope is represented as (3,-3) which simplifies to (1,-1). But when calculating the same line through points (4,1) and (1,4), the slope is (-3,3) which simplifies to (-1,1). The system treats these as different lines even though they’re geometrically identical.

The test demonstrates the bug exists, and the failure mode is completely understood.

### Agent 4: Feedback Synthesizer — Clear Reporting

The fourth [agent](https://github.com/ayoisio/adk-code-review-assistant/blob/main/code_review_assistant/sub_agents/review_pipeline/feedback_synthesizer.py) reads all three analyses from the shared state and synthesizes them into a comprehensive, human-readable report. The synthesizer structures findings with clear sections, headers for scannability, and specific actionable recommendations.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*q_DyuxEOozBa7R6iD6aq4g.gif)

Code Review Report

The report opens with a summary: 19 out of 20 tests passed with one critical bug found. It identifies the “Non-Canonical Slope Representation” issue, explains that (1,-1) and (-1,1) represent the same line but are treated differently, and recommends the exact fix:

```c
if simplified_dx < 0:
  simplified_dy *= -1
  simplified_dx *= -1
```

The report is specific, actionable, and includes the failing test case for verification. Every claim is backed by executable evidence from the tools.

## The Fix Pipeline: Addressing Iterative Refinement

Most code review systems stop at identifying problems. This system includes an automated fix [pipeline](https://github.com/ayoisio/adk-code-review-assistant/blob/main/code_review_assistant/agent.py#L33) that addresses the iterative refinement limitation of single-pass generation.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*HOGGdib4p-f-B3t_.png)

Fix Pipeline (LoopAgent) Architecture

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*q6GdXpeFl3c3_9bbf3TYZQ.gif)

Fix Pipeline In Action

The **Code Fixer** [agent](https://github.com/ayoisio/adk-code-review-assistant/blob/main/code_review_assistant/sub_agents/fix_pipeline/code_fixer.py) reads the bug report from state and generates a correction. It adds the normalization logic that ensures dx is always positive, flipping the signs of both dy and dx when necessary. This guarantees that slopes like (1,-1) and (-1,1) always get stored as the same tuple.

The **Fix Test Runner** [agent](https://github.com/ayoisio/adk-code-review-assistant/blob/main/code_review_assistant/sub_agents/fix_pipeline/fix_test_runner.py) then re-executes all 20 test cases against the corrected code. This time, all tests pass — the pass rate improved from 90% to 100%.

The **Fix Validator** [agent](https://github.com/ayoisio/adk-code-review-assistant/blob/main/code_review_assistant/sub_agents/fix_pipeline/fix_validator.py) checks whether the success criteria are met. All tests are passing, which means the functional requirements are satisfied. The agent calls the `exit_fix_loop()` tool, which sets `tool_context.actions.escalate = True`. This signals the loop to exit successfully.

The loop exited after two iterations because the functional and style requirements were met. If tests had still failed, the system would have retried with refined fixes, up to 3 times total. This automatic retry mechanism enables learning from failures and improving iteratively.

```c
fix_attempt_loop = LoopAgent(
    name="FixAttemptLoop",
    sub_agents=[
        code_fixer_agent,
        fix_test_runner_agent,
        fix_validator_agent
    ],
    max_iterations=3  # Try up to 3 times to get a successful fix
)
```

After the loop completes (either through successful escalation or reaching the maximum number of iterations), the **Fix Synthesizer** [agent](https://github.com/ayoisio/adk-code-review-assistant/blob/main/code_review_assistant/sub_agents/fix_pipeline/fix_synthesizer.py) runs exactly once. It reads the final state, compares before and after metrics, and presents a comprehensive report showing what was fixed, how the fix was validated, and what improvements were achieved.

## The Architecture: Two Pipelines Working Together

An orchestrator coordinates two distinct pipelines, each optimized for its specific purpose.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*La49vWDhG5EMtKB1.png)

Full Code Review Assistant Architecture

## Four Core Patterns

### Pattern 1: Tools Provide Proof, LLMs Provide Synthesis

The fundamental insight of this architecture is the division of labor between tools and language models. Tools perform deterministic operations — parsing ASTs, running linters, executing tests — and return concrete, verifiable results. Language models ***synthesize*** these results into human-readable explanations, connecting the technical findings to actionable recommendations.

### Pattern 2: State as Communication Layer

Agents in this system don’t communicate through direct message passing. Instead, they read and write to a shared state object using well-defined keys. This pattern enables several important properties.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*LCElTxKU_xLggJBz8Rhbxg.gif)

State Flow in Code Review Pipeline

First, **agents become decoupled** — they don’t need to know about each other’s existence or implementation details. The code analyzer doesn’t know or care that a style checker will read its output; it simply writes to `StateKeys.CODE_TO_REVIEW` and moves on. This makes the system easier to extend and modify.

Second, **debugging becomes straightforward**. Because state is explicit and persistent, you can inspect it at any stage of the pipeline to understand what data was available when a particular agent made a decision.

Third, **composition becomes natural**. New agents can be added to the pipeline without modifying existing ones, as long as they follow the state key contracts. Want to add a security scanner? Have it read `CODE_TO_REVIEW` and write `SECURITY_FINDINGS` to state. The existing agents continue working unchanged.

The system uses constants to define state keys rather than raw strings.

```c
# Without constants - typo breaks silently
state["test_results"] = {…}
data = state["test_ressults"] # Returns None, no error
# With constants - typo caught immediately
state[StateKeys.TEST_RESULTS] = {…}
data = state[StateKeys.TEST_RESSULTS] # IDE error immediately
```

When four or more agents share state, a single typo in a string key can break the entire pipeline silently. The code runs, but one agent writes to `TEST_RESULTS` while another reads from `TEST_RESSULTS`, getting None and producing incorrect output. With constants, your IDE catches the typo before the code ever runs. This pattern becomes essential at scale.

### Pattern 3: Loop Exit via Escalation

The fix pipeline’s loop needs a way to signal successful completion. The ADK provides an escalation mechanism specifically for this purpose.

Any tool in the loop can set `tool_context.actions.escalate = True` to signal that the loop should exit after completing the current iteration. In our fix validator, the logic is straightforward:

```c
def fix_validator_tool(tool_context):
  if all_tests_pass and style_acceptable:
    # Signal the loop to exit successfully
    tool_context.actions.escalate = True
    return {"status": "SUCCESSFUL"}
```

If tests don’t all pass, the tool simply returns without setting the flag, and the loop continues to the next iteration. This approach has several advantages over alternatives like returning special sentinel values or throwing exceptions to break the loop.

The escalation flag is **explicit and semantic** — when you see `escalate = True`, you immediately understand that the loop is exiting because success criteria were met. The flag stays **separate from return values** — the tool can return detailed status information while still signaling loop exit.

The three exit conditions provide comprehensive control. **Success exit** happens when a tool sets the escalate flag — this is the happy path where the fix worked. **Safety exit** happens when the loop reaches its maximum iteration count (3 in this case) — this prevents infinite loops when fixes aren’t converging. **Error exit** happens when an unhandled exception occurs — this ensures the system fails fast rather than continuing in an undefined state.

### Pattern 4: Sandboxed Code Execution

The test runner’s ability to actually execute code is what transforms this from a static analysis tool into a true validation system. The BuiltInCodeExecutor provides a sandboxed Python environment with carefully controlled capabilities.

The sandbox provides **isolation** — code runs in a separate environment that can’t access your local filesystem, environment variables, or other system resources. It enforces **network restrictions** — the code can’t make HTTP requests, open sockets, or communicate with external services. It prevents **package installation** — only the Python standard library and a few pre-installed [packages](https://ai.google.dev/gemini-api/docs/code-execution#supported-libraries?utm_campaign=CDR_0x8f8b61f4_default&utm_medium=external&utm_source=blog) like numpy and pandas are available. And it implements **time limits** — if code runs too long, execution is terminated automatically.

These restrictions are essential for safely running untrusted code. When a user submits potentially buggy code for review, you need to execute it to verify behavior. But you can’t risk that code accessing sensitive data, consuming infinite resources, or attacking your infrastructure. The sandbox provides the isolation necessary to execute code safely.

The executor returns actual stdout and stderr, so when a test fails, you get the real Python traceback. The test runner shows you exactly what Python produced when it ran the code.

## Production Observability

When you [deploy](https://medium.com/google-cloud/choosing-the-right-deployment-path-for-your-google-adk-agents-86c89c251ab5?utm_campaign=CDR_0x8f8b61f4_default&utm_medium=external&utm_source=blog) this system to production with the ***trace-to-cloud*** [flag](https://google.github.io/adk-docs/observability/cloud-trace/#overview), every operation is automatically traced to [Cloud Trace](https://cloud.google.com/trace/docs?utm_campaign=CDR_0x8f8b61f4_default&utm_medium=external&utm_source=blog). The ADK framework handles this automatically without requiring additional instrumentation.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*70CMO-eh45fcFsREdJcp-g.png)

Example Cloud Trace Waterfall Chart

The trace view shows you the complete execution timeline as a waterfall chart. The root agent span represents the entire request, lasting 2 mins and 28 seconds in this example. Nested under it are spans for each sub-agent — the Code Analyzer took 4.7 seconds, the Style Checker took 5.3 seconds, the Test Runner took 1 min 28 seconds, and the Feedback Synthesizer took 47.89 seconds.

This visibility reveals that test execution accounts for approximately 59% of the total request time for code review— making it the obvious target if you need to optimize latency.

The trace captures **token usage for each LLM call**, showing exactly how many input and output tokens were consumed. This lets you track costs at a granular level and identify opportunities to optimize prompts or switch to smaller models for specific tasks.

![](https://miro.medium.com/v2/resize:fit:1312/format:webp/1*_EIeIY6JAP0Nhe_Ose4Qww.png)

Example Code Analyzer Token Usage

And you can see **loop iterations** nested in the LoopAgent. If the fix loop ran two times before succeeding, you’ll see two complete cycles through the Code Fixer, Fix Test Runner, and Fix Validator, each with its own metrics. This makes it easy to understand how the system converged to a solution.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*qfBSv1f2b6rvZpJOlVqtVQ.png)

LoopAgent Iterations before Final Report Generation

You can **optimize based on evidence**. Rather than guessing where time is spent, you look at the trace and see exactly what’s slow. Rather than wondering why a particular agent behaved unexpectedly, you examine its inputs and outputs in the trace. Production observability transforms debugging from guesswork into forensic analysis.

## Integration Patterns

This code review system integrates naturally into broader AI development workflows.

### Agent-to-Agent (A2A)

The Code Review Assistant can be exposed as a remote A2A service, allowing other agents across different systems, teams, or languages to consume it over the network.

Expose your agent as an [A2A](https://google.github.io/adk-docs/a2a/) service:

```c
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from code_review_assistant.agent import root_agent

# Expose the code review assistant via A2A
# This auto-generates an agent card and serves it on port 8001
a2a_app = to_a2a(root_agent, port=8001)
```

Then run it with uvicorn:

```c
uvicorn your_module:a2a_app --host localhost --port 8001
```

Now other agents can consume it remotely:

```c
from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH

# Connect to the remote code review service
code_review_remote = RemoteA2aAgent(
    name="code_review_assistant",
    description="Remote code review validation service",
    agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}"
)
# Use it in a deployment pipeline
deployment_agent = Agent(
    name="DeploymentPipeline",
    model="gemini-2.5-flash",
    sub_agents=[code_review_remote],  # Remote agent, not local
    instruction="Validate all generated code before deployment"
)
```

In this pattern, the deployment agent communicates with the code review service over HTTP using the A2A Protocol. The deployment agent doesn’t need to understand the validation logic — it delegates to the remote service and receives structured results back.

This composition pattern is particularly valuable when:

- The code review service is maintained by a different team
- Multiple systems need to share the same validation logic
- The service needs independent scaling and deployment
- You want to enforce a formal API contract between systems

Want to add security scanning? Expose a security agent as another A2A service. Want API compatibility checks? Build and expose a compatibility checker. The system composes naturally across network boundaries.

### Model Context Protocol (MCP)

The Code Review Assistant can be exposed as an [MCP](https://google.github.io/adk-docs/tools/mcp-tools/) server, making its validation capabilities available to any MCP client — including the Gemini CLI, Claude Desktop, or other AI development tools.

**Exposing the Assistant as an MCP Server:**

Using [FastMCP](https://developers.googleblog.com/en/gemini-cli-fastmcp-simplifying-mcp-server-development?utm_campaign=CDR_0x8f8b61f4_default&utm_medium=external&utm_source=blog), you can wrap your code review tools:

```c
from fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("code-review-assistant")
@mcp.tool()
def review_code(code: str) -> dict:
    """Analyze Python code for structure, style, and correctness."""
    # Delegates to code_review_pipeline
    result = code_review_pipeline.run(code)
    return result
@mcp.tool()
def fix_code(code: str, issues: dict) -> str:
    """Automatically fix identified code issues."""
    # Delegates to code_fix_pipeline
    fixed = code_fix_pipeline.run(code, issues)
    return fixed
```

**Consuming from Gemini CLI:**

With FastMCP v2.12.3+, installation is automatic:

```c
# Install FastMCP if you haven't already
pip install fastmcp>=2.12.3

# Automatically configure the MCP server for Gemini CLI
fastmcp install gemini-cli code_review_assistant/mcp_server.py
```

Once configured, the Gemini model in the CLI can use these tools during code generation:

```c
User: Write a function to find max points on a line
```
```c
Gemini: [Generates code]
         [Automatically calls review_code tool to validate]
         [Sees test failures in the response]
         [Calls fix_code tool with the issues]
         [Returns validated, corrected code]
```

The model decides when to use validation based on the task context. For complex problems, it can validate its own code before presenting it to you. For educational scenarios, it can show both the initial attempt and the validated version.

This pattern addresses a common pain point: how do you trust AI-generated code at scale? Instead of manual review or hoping the model got it right, the model can validate its own work using deterministic tools exposed via MCP.

## What You’ve Learned

This code review system demonstrates a fundamental principle in AI engineering: **architecture is a matter of production, not just a capability question.**

Gemini 2.5 Pro with code execution can solve LeetCode Hard problems. But when you need transparency in production, when you need to debug why a validation failed, when you need to modify just the style checker without touching test generation, when you need to optimize costs by using different models for different tasks — explicit architecture wins.

The patterns transfer immediately:

- **Sequential pipelines** for ordered workflows with dependent data flow — the orchestrator runs agents in sequence, each reading and writing to shared state
- **Loop agents** for iterative refinement until success criteria are met
- **Tool integration** for mixing deterministic validation with LLM reasoning
- **State management** for observable, debuggable multi-agent communication

The 90-minute [codelab](https://codelabs.developers.google.com/adk-code-reviewer-assistant/instructions?utm_campaign=CDR_0x8f8b61f4_default&utm_medium=external&utm_source=blog) builds this complete system from scratch — real tools, real tests, real Cloud deployment. You’ll see exactly how these patterns compose into production systems.

**This is production AI development:** making architectural choices that prioritize observability, composability, and control. Once you understand these patterns, you can architect any multi-agent system — document processing pipelines, data analysis workflows, customer support systems, creative content generation, and more.

Your code review assistant is just the beginning.