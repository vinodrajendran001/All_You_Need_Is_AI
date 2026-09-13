---
type: raw-source
source_id: src-2026-09-13-prabhulal-production-rag-adk
title: "How to Build Production-Grade RAG with ADK and Vertex AI RAG Engine"
author: Arjun Prabhulal
url: "https://medium.com/google-cloud/how-to-build-a-production-grade-rag-with-adk-vertex-ai-rag-engine-via-the-agent-starter-pack-7e39e9cfe856"
published: 2025-11-03
captured: 2026-09-13
created: 2026-09-13
updated: 2026-09-13
tags:
  - source/raw
  - rag
  - ai-agents
  - google-cloud
status: active
---
Retrieval-Augmented Generation (RAG) has become the foundation for enterprise-grade generative AI systems powering intelligent assistants, document search engines, and private knowledge bases. However, while building a RAG prototype is straightforward, turning it into a scalable, observable, and production-ready system requires a robust infrastructure and strong architecture backbone.

To accelerate the journey from concept to production, Google released the [**Agent Starter Pack**](https://googlecloudplatform.github.io/agent-starter-pack/), a pre-configured template that provides everything needed to build, test, and deploy **production-grade agents** on Google Cloud. Agent Starter Pack is designed precisely to bridge the gap between experimentation and production. It provides developers with a **template foundation** so they can focus on what truly matters: business logic, prompts, and tools, while the Starter Pack handles the rest:

- **Deployment & Operations:** API serving, Infrastructure-as-Code, and CI/CD pipelines.
- **Observability:** Centralized logging, tracing, and monitoring dashboards.
- **Evaluation:** Seamless integration with **Vertex AI Evaluation** for continuous quality assessment.
- **Security:** Built-in GCP IAM, data privacy, and compliance best practices.
- **Data & UI:** Connectors for data storage, vector databases, and ready-to-use UI playgrounds.

> *Agent Starter Pack is Google’s production blueprint for agentic AI systems, helping teams transition from an idea to a* ***scalable, deployable RAG application*** *in weeks, not months.*

In this article, we’ll dive into how to set up, configure, and deploy a RAG app inside the Agent Engine using the Agent Starter Pack, with Google ADK and the Vertex AI RAG Engine.

## High-Level Architecture

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*0cuoqgsolbD_TSIC)

Image from https://googlecloudplatform.github.io/agent-starter-pack/

In this article, we’ll narrow our focus to four core pillars of a production-grade RAG pipeline within the above architecture.

1. **LLM Orchestration — Google ADK**,
2. **LLM — Gemini**,
3. **Deployment — Vertex AI Agent Engine**, and
4. **Retrieval & Grounding — Vertex AI RAG Engine**

## Vertex AI Agent Engine

[**Vertex AI Agent Engine**](https://docs.cloud.google.com/agent-builder/agent-engine/overview), part of the **Google Cloud Vertex AI Platform**, offers a suite of services that enable developers to deploy, manage, and scale AI agents in production environments. It abstracts away the underlying infrastructure, allowing you to focus on building intelligent applications instead of managing runtime resources.

### Agent Engine Services:

- **Runtime:** Deploy and scale agents with a managed runtime, customizable containers, built-in security, and integrated observability.
- **Quality and Evaluation (Preview):** Evaluate and optimize agent performance using the integrated Generative AI Evaluation service and Gemini model runs.
- **Example Store (Preview):** Store and dynamically retrieve few-shot examples to enhance agent accuracy and contextual relevance.
- **Sessions (Preview):** Persist user-agent interactions to maintain conversational context across sessions.
- **Memory Bank (Preview):** Store and recall information from sessions to enable personalized, memory-aware interactions.
- **Code Execution (Preview):** Execute custom code securely within an isolated, managed sandbox environment.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*-8EyfC4L_Bq1OQ8F.png)

Image from https://docs.cloud.google.com/agent-builder/agent-engine/overview

## Vertex AI RAG Engine

[**Vertex AI RAG Engine**](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview) is also a core component of the Google Cloud Vertex AI Platform, designed to power Retrieval-Augmented Generation (RAG) workflows. It provides a fully managed vector store, seamless integration with Gemini models, and supports real-time retrieval and grounding. By enhancing large language model (LLM) outputs with relevant, contextually retrieved data, the RAG Engine enables developers to build intelligent, data-aware AI applications that deliver accurate, enterprise-grade responses. RAG Engine supports multiple vector databases and, by default, uses RagManagedDB backed by a Google Cloud Spanner instance

\[ *Basic Tier = 100 processing units and Scaled Tier = 1000 processing units for production workloads\]*

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*0ZTCX0raWKPXCtFt.png)

Image from https://cloud.google.com/vertex-ai/generative-ai/docs/rag-overview

## Implementation

Let us implement the RAG application and deploy it into Vertex AI using the Agent Starter pack.

## Pre-Requisites

1. **Python 3.10+** installed
2. **GOOGLE\_API\_KEY** [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### Step 1: Install the UV package manager

Ensure [UV](https://github.com/astral-sh/uv) is installed.

```c
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Install Agent Starter pack using UVX

Authenticate with your GCP Project and create the rag agent demo

```c
#Authenticate GCP login
gcloud auth login

#Set default GCP Project ID
gcloud config set project YOUR_PROJECT_ID
```
```c
#Agent Starter Pack using rag Template identifier 
uvx agent-starter-pack create rag-agent-demo -a adk@rag
```

The **“-a”** flag specifies the Template identifier to use.

Here, we use **adk@rag** template, which fetches RAG template from [google/adk-samples](https://github.com/google/adk-samples/tree/main/python/agents/RAG.)

![](https://miro.medium.com/v2/resize:fit:1344/format:webp/1*s_oLhDTHQhMIlw1jMppvxw.gif)

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*5KaR7dWxPv66yW3GM0WUrw.png)

### Step 3. Enable Vertex AI APIs

```c
gcloud services enable \
  aiplatform.googleapis.com \
  discoveryengine.googleapis.com \
  cloudbuild.googleapis.com
```

### Step 4: Create RAG Corpus and Ingest documents

Upload a PDF or Word document to a GCS bucket, then ingest it using the default chunk size, overlap, and embedding rate limits.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*WMNeVmKvUyd2IUqCjV4teA.gif)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*vLLb55OKl0kRe2o-Zs34NA.png)

### Step 5: Create a.env file

```c
# Copy as .env file and fill your values below
# Run ./update_dotenv_example.sh to update .env-example from your .env file.

# Choose Model Backend: 0 -> ML Dev, 1 -> Vertex
GOOGLE_GENAI_USE_VERTEXAI=1

# ML Dev backend config
GOOGLE_API_KEY=

# Vertex backend config
# Rag Engine only works with Vertex. So we should configure it to use Vertex:
GOOGLE_CLOUD_PROJECT=PROJECT_ID
GOOGLE_CLOUD_LOCATION=us-central1

# Existing corpus in Vertex RAG Engine to be used by RAG agent
# e.g. projects/123/locations/us-central1/ragCorpora/456
RAG_CORPUS=projects/gcp-project/locations/us-central1/ragCorpora/resourceID

# Staging bucket name for ADK agent deployment to Vertex AI Agent Engine 
STAGING_BUCKET=gs://bucket-name

# Agent Engine ID in the following format: projects/<PROJECT_NUMBER>/locations/us-central1/reasoningEngines/<AGENT_ENGINE_ID>
# Can be updated post-deployment 
AGENT_ENGINE_ID=
```

### Step 6: Install package dependencies

```c
cd rag-agent-demo/

#install the packages 
make install
```
![](https://miro.medium.com/v2/resize:fit:1338/format:webp/1*qsQjaVVvY7al73tMqLGvyA.png)

### Step 7: Verify local setup

This ensures the RAG application can connect to Corpus

```c
make playground
```
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*M1fJzSeEUDhlNMyKlcJvgA.png)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*JUCHLeVMGoUpSszWfB_qcA.png)

### Step 8: Deploy to Agent Engine

Before deployment, grant the Agent Engine service account permission to query the RAG corpus

```c
## Setting Up Permissions

### Step 1: Create Custom IAM Role

gcloud iam roles create ragCorpusQueryRole \
  --project=your-project-id \
  --title="RAG Corpus Query Role" \
  --permissions="aiplatform.ragCorpora.query"

### Step 2: Grant Role to Service Account

PROJECT_NUMBER=$(gcloud projects describe your-project-id --format="value(projectNumber)")

gcloud projects add-iam-policy-binding your-project-id \
  --member="serviceAccount:@gcp-sa-aiplatform-re.iam.gserviceaccount.com">service-${PROJECT_NUMBER}@gcp-sa-aiplatform-re.iam.gserviceaccount.com" \
  --role="projects/your-project-id/roles/ragCorpusQueryRole"
```
```c
make deploy
```
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*enftYCr1I4jXxKatw1Cbog.png)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*3A1JAuT19S1674ybIK0UVg.png)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*PJW5Qiuf0s37RhNVdL2lhQ.png)

After deployment `deployment_metadata.json` is updated with the `remote_agent_engine_id`, which you’ll use to connect to the remote Agent Engine.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*yt7_hjiWuXzrLzJXuVt0qQ.png)

### Step 9: Demo — Verify Agent Engine

You can verify Agent Engine (ReasoningEngine) connectivity via Jupyter Notebooks, curl, or a Python client.

Verifying Agent Engine through Jupyter Notebooks

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*SiC58hsh6CO4i6sDViYV7w.gif)

Verifying through a Jupyter notebook

Verifying Agent Engine through a programmatic way

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*pBC-dgvyeqAhwWMS6lXmGw.gif)

Verifying through a Programmatic way, connecting to Agent Engine

Also, check **observability** by verifying LLM invocation calls through Cloud Traces — each session ID corresponds to a unique span.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*1ZT9urmgCapIbKzLzTTWtw.png)

Tracing — Span ID based on the invocation each session ID

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Wre0Vn6vWQkE9amyHIDC5A.png)

TracingDetails

## Conclusion

In this article, we walked through the process of setting up, configuring, and deploying a RAG application on Google Cloud using the Agent Starter Pack, Google ADK, and the Vertex AI RAG Engine, with minimal coding and infrastructure setup.

By leveraging the Agent Starter Pack, developers can accelerate the journey from prototype to production with pre-built scaffolding for deployment, observability, evaluation, and security.

In the next part of this series, we’ll go deeper into

- Deploying the **Vertex AI RAG Engine** through Cloud Run
- Deploying **Agentic RAG** with **Vertex AI Search** via Agent Engine