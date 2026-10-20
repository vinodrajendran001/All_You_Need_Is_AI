---
title: "How Uber Built a Genie to Answer Questions Correctly"
source: "https://blog.bytebytego.com/p/how-uber-built-a-genie-to-answer-051?utm_source=post-email-title&publication_id=817132&post_id=220742828&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-10-19
created: 2026-10-20
description: "In this article, we will understand how Genie prepares knowledge, retrieves it, and generates answers."
tags:
  - "clippings"
---
## \[Webinar\] How to stop rewriting your agent’s code (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!sUYZ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F32e352bc-8d61-45d7-a2d8-9722952b4f18_1600x900.png)

Right now, you’re your agent’s context engine. You write the rules files, maintain the skills, and paste in the Slack thread it missed.

But hand-curated context goes stale. And when there are conflicting answers, your agent can’t tell which is right. You pay for it in higher token bills and longer reviews.

[Join us live on Oct 28 (FREE)](https://go.bytebytego.com/unblocked_101926) to see:

- The 8-levels of AI maturity and where teams get stuck
- How a context engine curates context and resolves conflicts before your agent writes a line of code
- Live demo: token savings in the same coding task, and use cases beyond code gen

Bonus: 2 open source tools you can use today.

---

Genie is Uber’s internal AI assistant for answering engineering support questions. It finds relevant information in Uber’s documentation, uses a language model to explain that information, and gives engineers a way to continue the conversation or ask a human for help.

The interesting part about Genie is how Uber has connected multiple capabilities into building a working support system that fits seamlessly into an engineer’s workflow.

In this article, we will understand how Genie prepares knowledge, retrieves it, and generates answers. Here’s what we will cover:

- The problem that Genie is trying to solve
- What does Genie do?
- How Genie gains knowledge
- How Genie finds specific information from that knowledge
- How Genie handles user questions
- What does a typical Genie workflow look like
- How Genie makes sure the answer is correct
- What if Genie isn’t able to answer something
- How Genie collects feedback
- How Uber evaluates Genie’s performance

![](https://substackcdn.com/image/fetch/$s_!jaok!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F817bc699-3845-414a-ab7d-ad62b1644fcc_4392x1626.png)

*Disclaimer: This post is based on publicly shared details from various sources. References at the end. Please comment if you notice any inaccuracies.*

## The Problem Genie Is Trying to Solve

The problem starts with how engineering teams support one another.

In a large software-driven company, many teams build platforms that other developers use to perform their jobs. A platform might provide tools for various activities such as software deployment, data processing, or working with ML workflows. Developers from other teams making use of these platforms inevitably need help with configuration, errors, or understanding unfamiliar features.

In a typical setup, the team responsible for managing a platform assigns an engineer to handle incoming issues during a particular period. This responsibility is commonly about providing on-call support. Although on-call work can definitely involve urgent production incidents, the problem Genie is trying to solve is geared towards everyday tech support that developers on platform teams provide through Slack channels.

![](https://substackcdn.com/image/fetch/$s_!l2sY!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd6877af9-38e8-423a-b078-ff68b2300c33_2590x996.png)

For example, a developer from a product team might ask how to configure a platform feature. The on-call engineer reads the question and requests more details. The person asking responds, then waits again. Eventually, the on-call engineer identifies the relevant documentation or explains the required steps. Even a relatively straightforward question can involve several rounds of back-and-forth conversation and waiting.

Uber reports that its internal support channels received approximately 45K questions each month. At that volume, repeated questions consume considerable engineering time that the platform teams could utilize for better stuff.

Much of the information needed to answer such questions already exists somewhere. However, it is often scattered across Engwiki, which is Uber’s internal engineering wiki, or its internal Stack Overflow, and other documents. Finding the right information becomes difficult enough that it is much easier to ask another person.

Genie is designed to make that existing knowledge available through the Slack channels where developers already ask for help.

## What does Genie do?

Genie combines finding information with explaining it.

A large language model (LLM) can produce readable explanations and answer technical questions. However, its general training doesn’t automatically give it knowledge of Uber’s private platforms, internal procedures, or documentation.

Therefore, Uber needed a way to connect a language model to its internal knowledge base. Two approaches help with this: fine-tuning and retrieval-augmented generation (RAG).

Fine-tuning means further training an existing model using examples selected for a particular purpose. Uber explains that this approach would require a collection of high-quality, varied training examples, along with sufficient computing resources to update the base model as new examples come up.

On the other hand, RAG supplies relevant information when a question is asked. The system first searches a knowledge collection, retrieves useful passages, and then gives those passages to the LLM along with the question. The model uses all this information to generate its answer.

For example, suppose a developer asks how to change a setting in an internal platform. A RAG system searches the platform’s documentation, finds the passage explaining that setting, and gives it to the model. The model turns the retrieved information into a response appropriate to the question.

Uber chose RAG for Genie because it could begin with existing documentation and be ready for launch sooner without the need to first assemble a fine-tuning dataset. This still needed a lot of work to collect, prepare, and evaluate the documentation. It also meant that updating the external knowledge collection could improve the information available to Genie without retraining the model for every change in documentation.

![](https://substackcdn.com/image/fetch/$s_!TzDy!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F178d92d2-f2c7-45db-98c5-98cde006623d_4392x1626.png)

## How Genie Gains the Required Knowledge

Preparing knowledge happens separately from answering questions. Before Genie can retrieve useful information, Uber must turn its scattered documents into a searchable collection. This preparation happens using an ETL pipeline.

ETL stands for extract, transform, and load.

- Extraction means fetching content from internal sources.
- Transformation means preparing that content for retrieval, including breaking it into pieces and generating numerical representations.
- Loading means making the resulting data available to the search infrastructure.

Uber engineering team uses Apache Spark to run this work. For reference, Spark is a system for processing data across multiple workers, allowing a large preparation job to be divided into smaller pieces of work.

![](https://substackcdn.com/image/fetch/$s_!s6sR!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F80a6e43e-fdb5-4f34-9ea4-4096970ef227_2596x2224.png)

The pipeline fetches content through interfaces provided by sources such as Engwiki and Uber’s internal Stack Overflow. It places the results into a Spark DataFrame. Think of it as a table with rows and columns.

At this stage, a row contains information such as the document’s source URL, its text, and additional metadata. Here, metadata is information that describes the document rather than the content of that document.

Keeping the source URL alongside the text is important throughout the system. This is because Genie needs to eventually connect an answer back to the real documentation that supports it. Preserving this relationship during the preparation phase makes it easy to perform source attribution later on.

## How Genie Finds Specific Information

Embeddings allow Genie to search for related meaning within its knowledge base. Once Uber has collected all the documentation, the next challenge is finding the passages that relate to a user’s question.

The system first divides documents into smaller pieces called chunks. For example, a long document might contain installation instructions, configuration options, and troubleshooting guidance. However, a question about one configuration option may only need a small part of that document. Chunking makes those smaller passages available as individual retrieval candidates.

Uber uses LangChain to chunk its wiki content. It then uses an OpenAI embedding model to generate an embedding for each chunk. An embedding is a list of numbers that represents aspects of a piece of text’s meaning. An embedding model is designed so that related texts have representations that can be found through similarity search. This helps a system find relevant information even when a question and a document use different wording. For example, a question might refer to a job “taking too long,” while a relevant document discusses an “execution time limit.” These phrases are just examples, but they show why searching for related meaning can be a game-changer when exact keywords differ.

The resulting data keeps each chunk associated with its embedding and source information. The original text still remains essential. The embedding simply helps the search system locate a passage. The passage itself supplies information for the language model to read.

Uber generates embeddings using custom Python functions executed through Spark. This lets embedding generation fit into the same data-processing pipeline as document collection and preparation.

## How Genie Handles User Questions

Uber prepares the search infrastructure to serve questions. Creating embeddings produces searchable data, but that data still has to reach the systems that handle live requests. This is handled through the Pusher stage.

Two internal systems are used here:

- **Sia:** This is Uber’s internal vector database solution. A vector database supports searching numerical representations such as embeddings.
- **Terrablob:** This is Uber’s blob storage, which holds stored data and files used by the pipeline and serving infrastructure.

![](https://substackcdn.com/image/fetch/$s_!ZK2R!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffa33cd5a-57b2-46da-8142-7060da0fc39f_3332x1824.png)

A bootstrap job ingests data into Sia, followed by Spark jobs that build and merge an index that organizes data for efficient searching.

The resulting index data is stored in Terrablob. Serving machines, called leaves, download the base index and synchronize snapshot data. These leaves handle searches against the loaded index when requests arrive.

This separates the work of building searchable knowledge from the work of answering an individual question.

- Document preparation and index construction happen through the ingestion pipeline.
- Live requests use the index made available to the serving machines.

## What Does a Typical Genie Workflow Look Like

Each incoming question goes through retrieval before generation. Once the knowledge collection is ready, Genie can answer questions. The central backend component for this is Uber’s Knowledge Service.

![](https://substackcdn.com/image/fetch/$s_!0FSu!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02678ce4-076e-4583-a6a2-533f2f1ee85b_3460x1848.png)

Here’s how it works:

- When someone posts a question in Slack, the Genie bot sends it to Knowledge Service. The service converts that question into an embedding.
- It then searches the vector database for document chunks with related embeddings.
- The search returns relevant passages associated with their source information. Those passages become part of the material sent to the LLM, together with the user’s question and instructions for answering.
- Next, the model generates a response, which is returned through Genie to Slack.

There are two distinct model responsibilities in this flow.

The embedding model produces numerical representations that support retrieval. On the other hand, the LLM reads the retrieved text and produces the written response.

This difference is useful when dealing with failures. Genie might retrieve unsuitable passages, or it might retrieve useful passages and still generate an inadequate answer. Improving the system requires checking both stages.

## How Genie Makes Sure the Answer is Correct

Uber gives the model explicit boundaries for generating its answers. An LLM can generate a plausible statement that is incorrect or unsupported. This behavior is commonly called hallucination. In an internal support system, an invented instruction could send a developer in the wrong direction.

Uber addresses this partly through how it constructs the model’s input.

Each retrieved result is presented as a separate sub-context, together with its source URL. A sub-context is simply a clearly identified piece of supporting material within the larger prompt. The model is instructed to answer using the provided sub-contexts and to provide source URLs as citations. This gives it explicit evidence to work from and gives the user a way to check the supporting documentation. For example, if several passages discuss different parts of a configuration process, preserving each passage’s source helps the generated explanation remain traceable to the actual source.

These measures reduce the risk of unsupported answers, but a source link doesn’t guarantee that every statement is correct. The retrieved passage must be relevant, the underlying document must be accurate, and the model must represent it faithfully. This is why evaluation remains an essential part of the architecture.

Uber also restricts the knowledge available to Genie. The team preselects sources that are broadly available to Uber developers because some internal information would be inappropriate to expose through model processing or Slack responses.

## What if Genie Isn’t Able to Answer Something

The conversation includes a clear path to human support. A support interaction often continues after the first answer. Someone may need clarification, discover that the suggested information doesn’t quite address their situation, or require an action that documentation cannot provide.

Uber redesigned Genie’s interaction flow to deal with these possibilities. Its responses include action buttons that let users ask a follow-up question, mark the issue as resolved, or contact human support.

If Genie lacks enough information to answer, it tells the user and directs them to the on-call developers responsible for the platform. When a user escalates an interaction to human support, the human developer takes over while Genie stays muted. This keeps the conversation focused while an engineer handles the issue.

This feature is really important because successful support involves more than producing a paragraph of text. The user needs to understand what to do next. An answer that helps only partially can still be valuable if it leads smoothly into clarification or human assistance.

## How Genie Collects Feedback

User feedback measures the impact of the answer. Uber collects feedback directly in Slack, where users can select a response category.

- **Resolved:** The answer completely resolved the issue.
- **Helpful:** The answer provided some help, but more assistance is needed.
- **Not Helpful:** The answer was wrong or didn’t address the question.
- **Not Relevant:** The request requires human help that Genie cannot provide, such as a code review.

The differentiation between these categories is very important. Partial help differs from complete resolution. Similarly, an incorrect answer differs from a request that falls outside what a documentation assistant can accomplish.

When a user submits feedback, a Slack plugin collects it together with relevant metadata. It sends that information through a Kafka topic, which acts as a stream of events, into a Hive table, where it can be stored and analyzed in the future. Uber then displays the resulting metrics in a dashboard.

This creates a record of how Genie performs in real use. Without such a record, a system could answer many questions while its operators had little visibility into whether those answers actually helped anyone.

## How Uber Evaluates the Performance of Genie

Uber evaluates both the answers and the documents behind them. User feedback provides direct evidence of Genie’s usefulness. However, Uber also supports custom evaluations of qualities such as hallucination and answer relevance.

For these evaluations, a separate pipeline retrieves Genie’s recorded context and responses from Hive. It combines them with relevant information such as Slack metadata and user feedback, then prepares the data for an evaluator.

The evaluator uses an “LLM as a judge” approach. This means a language model receives an evaluation prompt that tells it how to assess the material. Its task is to examine an existing answer against the chosen criteria. For example, an evaluation prompt could ask whether an answer addresses the question and whether its claims are supported by the supplied context.

![](https://substackcdn.com/image/fetch/$s_!Yaox!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F54448ffc-cd5c-4a37-9b3f-bee89b966dc3_4038x2124.png)

The evaluation results are processed into metrics and published in a report available through the interface. Uber says these evaluations can help plan improvements to both retrieval and generation steps.

The evaluation can also extend to the source documents themselves. This is a particularly useful part of the design because answer quality depends on the material available for retrieval. If a document is unclear, incomplete, or inaccurate, retrieving it successfully may still produce a poor support experience.

Uber’s document evaluation pipeline represents each document as a row in a Spark dataframe. It sends the document and a custom evaluation prompt to an LLM judge. The model returns a score, an explanation of that score, and actionable suggestions for improving the document. These results are published in a report that is also accessible through the Michelangelo interface. For example, a document might describe a procedure while leaving prerequisites unclear. Improving that document can give Genie better material to retrieve and explain, while also helping developers who read the documentation directly.

To summarize, the two evaluation processes examine different parts of the system. Answer evaluation checks what Genie produces in a particular interaction. Document evaluation checks the quality of the knowledge from which future answers will be constructed.

## Conclusion

Genie was launched in September 2023. Within a year, Uber reported 154 Slack channels using Genie. More than 70K questions were answered during this time. The overall helpfulness rate was 48.9%, which is like a full-resolution rate, with engineering time savings of around 13000 hours.

This cost tracking is generated by following calls through the system. Running a model-backed service across many support channels also requires visibility into its costs. Uber provides that visibility by carrying an identifier through the request flow.

![](https://substackcdn.com/image/fetch/$s_!x6bS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3f8dfdba-37b0-434b-a055-8cb3e3afa76e_2648x1626.png)

When a Slack client or another platform calls Knowledge Service, it passes a UUID. Knowledge Service forwards this identifier in request metadata to Michelangelo Gateway. The identifier can be included in an audit log and used to track costs associated with it.

Genie is a cutting-edge bot with the goal of streamlining on-call management, optimizing incident response, and improving team collaboration. It has the potential to change the entire experience of how users and on-call developers of any platform interact and engage within the respective platform’s Slack channel.

**References:**

- [Genie: Uber’s Gen AI On-Call Copilot](https://www.uber.com/us/en/blog/genie-ubers-gen-ai-on-call-copilot/)
- [Meet Michelangelo: Uber’s Machine Learning Platform](https://www.uber.com/in/en/blog/michelangelo-machine-learning-platform/)

---

∙