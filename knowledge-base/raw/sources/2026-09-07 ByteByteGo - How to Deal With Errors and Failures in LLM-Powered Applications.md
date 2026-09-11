---
type: raw-source
source_id: src-2026-09-07-bytebytego-llm-error-handling
captured: 2026-09-11
title: "How to Deal With Errors and Failures in LLM-Powered Applications"
source: "https://blog.bytebytego.com/p/how-to-deal-with-errors-and-failures?utm_source=post-email-title&publication_id=817132&post_id=214198535&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-09-07
created: 2026-09-08
description: "Apart from normal processing, the application also sends data to a large language model (LLM). It then uses the model’s response to carry out a task."
tags:
  - "clippings"
  - "topic/production"
  - "topic/reliability"
  - "source/raw"
---
## The all-in-one intelligent cloud (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!13at!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F78221da1-407f-4337-a6d2-ce28cdac9566_1600x840.svg)

Writing code is fast, shipping it is still hard. Railway’s push-button compute, storage, and networking is built for both small and hyperscale software.

Humans and agents alike operate on one vertically integrated system on our own hardware. Get superior speed, better economics, and a lot more calm.

Sign up with the link below for free cloud credits and let your agents cook.

---

What is an LLM-powered application?

It’s just like any software application. But there is one major difference. Apart from normal processing, the application also sends data to a large language model (LLM). It then uses the model’s response to carry out a task. For example, a customer support chatbot might depend on an LLM to answer user queries. A document-processing system can use an LLM to extract names, dates, and invoice amounts from the uploaded documents. A coding assistant might ask an LLM to write a piece of code and integrate it into the logical flow.

On face value, we might feel that building such an application is quite simple:

- The user sends a request.
- The application sends a prompt to an LLM.
- The LLM returns an answer.
- The application displays that answer or uses the same for some other processing.

However, there are chances that any of these steps can fail. The network might be unavailable. The LLM provider might reject the user request for various reasons. The request might go through, but the model might return invalid JSON. The LLM can misunderstand the instructions and invent false information due to hallucinations. They might also take a long time to respond.

The techniques for resiliency and error handling help prepare the application to handle these situations in the best possible manner. Here’s what we will cover in the article:

- What is the meaning of error handling and resiliency?
- Why do LLM applications need special treatment for error handling?
- How does a request flow in an LLM-powered application?
- Main types of errors and failures
- How to classify failures to take appropriate action?
- How to retry a request correctly?
- How to manage timeouts and deadlines?
- How to deal with business rules in an LLM-powered application?
- How to manage fallbacks and graceful degradation?
- How do circuit breakers work in this setup?
- Rate limiting, queues, and concurrency control
- How to make LLM tool calls safe with idempotency?
- How to stream the responses from the LLM?

![](https://substackcdn.com/image/fetch/$s_!npF1!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a3cc7fe-fa4a-48bd-b3f7-fe81e2b6b080_3536x2118.png)

## Meaning of Error Handling and Resiliency

Before we get into the details, let us understand what error handling and resiliency exactly mean.

You can think of error handling as a part of the program responsible for deciding the appropriate action when something goes wrong. For example, consider an application that calls an LLM API. If the request is successful, the program processes the response in a normal way. But if it fails, the program might have to choose from various options, such as retrying the request, showing an explanatory message, using a backup model, or recording the failure for further investigation.

Any of these approaches is much better than allowing the entire application to crash. But we also cannot treat every problem in the same manner. A real production application should be able to distinguish between different types of failures so that we can take the right action. Therefore, good error handling needs an understanding of what failed and why.

In contrast, resiliency is an application’s ability to continue doing its job even when some parts of the system are failing. We don’t need an application to operate perfectly to be resilient. Failures are fine. But they should happen in a controlled manner. This is also known as graceful degradation.

For example, consider a travel assistant that uses an LLM to build personalized itineraries for travellers. If the primary LLM it depends on is unavailable, the application can use a smaller backup model for creating the itineraries. If that model also becomes unavailable, the application can display previously created destination guides for the same locations. Of course, these answers won’t be personalized, but the user won’t just see a useless error message.

While error handling deals with an individual failure, resiliency is more concerned about the behavior of the entire system even when things are failing.

## Why do LLM Applications Need Special Treatment for Error Handling?

Traditional software apps work according to well-defined rules. If we write a function that adds 5 and 7, it will always return 12. If the function returns successfully, the result is deemed valid.

With LLMs, we don’t have this luxury. This is because the output from LLMs is probabilistic. In other words, the same prompt can produce different answers every single time. Also, a successful API request to an LLM doesn’t guarantee that the response we receive is correct or even usable. For all we know, the response might be utterly gibberish. This means that an LLM API call might appear successful based on status code, but it might be a failure in logical terms. There are several things that could be wrong with the response:

- The model might have ignored some part of the instructions.
- It might have returned a pure text response when the application expected JSON.
- The LLM might hallucinate and invent a product, policy, or piece of information that has no basis in real data.
- The model might return an incomplete response because it reached its token limit.
- The LLM can refuse a harmless request because it misunderstood the context.
- The LLM might select the wrong tool or call a tool with invalid arguments.
- Lastly, the LLM might return an answer that violates some important business rule.

We can broadly notice two categories of failures over here:

- **Technical Failures:** They happen when the system can’t even complete the operation. This involves stuff like network errors, timeouts, unavailable service, invalid credentials, and so on.
- **Semantic Failures:** These types of failures show up even when the operation is technically successful. But the result might be incorrect, unsafe, irrelevant, or even unusable.

Conventional error handling focuses on dealing with technical failures. However, LLM-powered applications need to handle both technical and semantic failures.

## How Does a Request Flow in an LLM-powered App?

LLM-powered apps contain much more than an LLM. We have many different components that come together to make an application complete. See the diagram below:

![](https://substackcdn.com/image/fetch/$s_!ssQz!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F69c05e69-245b-42d6-9fc1-46aad86d054f_3142x2072.png)

As an example, consider a shopping chatbot that checks products based on the user’s preference. It first runs a search on a product database and gives the results back to an LLM. It then asks the model to select the right products for a particular user and then calls an inventory API to find out the availability of those products.

We can have failures at every boundary within this application. The user might provide some invalid information. The product search may return no results. The request to the LLM might time out due to external reasons. The model may return an unknown product identifier. The inventory service might go down. Lastly, even if the response is somehow generated, it might be interrupted while streaming to the user.

To make an application truly resilient, we can’t treat the LLM as an isolated component. We need to consider the path of the request from the beginning to the end and identify potential problems.

## Main Types of Errors and Failures

Let us now look at the main types of errors and failures that can occur in such an application.

### Invalid User Input

Some failures can show up even before the LLM is called. For example, a user may submit an empty message, upload an unacceptable file format, provide an extremely large document, or enter an invalid date.

In such cases, the application should be able to validate obvious requirements. There is no need to call an LLM to find out if a mandatory email address is missing or if an uploaded file exceeds the size limit. If we reject invalid requests early, we can save time and processing costs. We can also provide much clearer error messages to the users since the rules are fixed.

### Network and Connection Failures

An application talks to an LLM provider over the internet. However, the connections can be interrupted. We can have DNS lookup failures. Responses might be lost.

Such type of failures are temporary. We can retry the request. But the application cannot retry indefinitely. We also need to consider whether it is safe to repeat the operation and whether there are any unforeseen side effects.

### Timeouts

In this case, the LLM may take longer to respond than the application can wait. If there’s no timeout, the request can remain stuck while consuming resources.

The timeout value defines how long the application can wait. For example, an interactive chat application might have a timeout of 20 seconds. But an offline document-analysis job might allow several minutes. Also, the timeout should depend on the user experience. For example, a user waiting on a screen should have a shorter deadline than a background task that runs overnight.

### Rate Limits

LLM providers have a limit to how many requests or tokens a specific account can use within a time period. If the application goes above this limit, the LLM provider may return a rate-limit error. This is represented by the HTTP status code 429.

Getting a rate limit response doesn’t mean that the service is broken. It means that our application is making more requests than what the provider can handle at a given point in time. To handle this, the application may need to delay the requests, reduce concurrency, put the work in a queue, or switch to another model that might have available capacity.

### Provider and Server Failures

In certain situations, the LLM provider might be down due to a temporary internal problem. These failures are commonly represented by HTTP 5xx status codes.

In this case, a limited retry attempt could be a good idea because the failure might vanish quickly. However, if the failures continue, repeated retry calls only increase the load upon an already struggling service. is reasonable because the failure may disappear quickly. The application should stop retrying and switch to an alternative execution path if possible.

### Authentication and Permission Failures

If the application provides an expired or invalid API key, it might also result in a 401 or 403 response from the LLM provider.

In this case, there is very little point to retrying. The application should record the failure, alert the relevant parties, and return an appropriate message to the user. It must take care not to expose API keys or other internal security details to the user.

### Context-length Failures

Every language model has a limit on how much text it can process in one request. The prompt, conversation history, retrieved documents, tool definitions, and expected answer are all part of this context window and consume space.

If the application sends a lot of information to the LLM, the LLM may reject the request, or it may have too little space for the answer. An application designed with resiliency in mind usually counts tokens before sending the request. It can also remove old conversation messages, summarize earlier content, retrieve fewer documents, or divide a large job into smaller pieces to stay within the limit.

### Malformed or Unexpected Output

Let’s say our application expects a result in the following format.

```markup
{
  “customer_name”: “Adam Smith”,
  “priority”: “high”
}
```

However, the model might reply something like: “The customer’s name appears to be Adam Smith, and this looks urgent.

Such an answer might make sense to a human being, but the application that expects a JSON response can’t process it. To get around this, the application should use a structured-output feature if the model provider supports it. It should also validate the response against a schema before using it.

### Incorrect or Invented Information

The most dangerous LLM failures happen in the form of plausible answers that are completely wrong. This occurs due to model hallucination.

For example, a customer-support assistant might invent a refund policy that doesn’t exist. A research tool might generate a source that doesn’t exist. An inventory assistant might recommend a product that is not even there in the catalog.

Such problems can’t be detected by catching exceptions because no technical exception occurred. To handle these types of issues, the application needs additional checks, trusted data sources, or some form of human intervention to proceed further.

### Tool Failures and Partial Completion

LLMs are also now used as agents that can make API calls, search databases, send messages, or perform transactions. This gives rise to a major problem. The specific action taken by the LLM might succeed even when the surrounding workflow fails.

For example, suppose the LLM assistant calls a payment service. The payment succeeds, but the network connection breaks before the application gets the confirmation. If the application retries the payment blindly, we might end up charging the customer twice.

This is the reason tool-based systems need idempotency, state tracking, and recovery mechanisms.

## How to Classify Failures to Take Appropriate Action

So how do we deal with all these different types of errors in an LLM-powered application?

The first step is to classify them. There are main categories:

- A transient error is temporary and usually disappears if we attempt the operation again. For example, network problems, rate limits, and server failures.
- A permanent error continues until there is a change in the request or the system. Such errors include invalid credentials, unsupported file types, permission issues, and malformed requests.
- A semantic error occurs when the response is technically correct, but doesn’t solve the application’s requirements. Examples are invalid JSON, unsupported tool arguments, hallucinations, and so on.

Once we are able to classify an error, we can deal with it appropriately. For a transient error, we should retry after a short delay or use a fallback. For permanent errors, we need to report to the concerned parties who can correct the problem. For semantic errors, we need to validate, repair, or request human review.

Of course, not every error also fits neatly into a single category. For example, a context-length error is permanent for the current prompt. However, it can be solved by making the prompt shorter.

## How To Retry a Request Correctly?

Let us look at some techniques to deal with failures. The first one to check out is retrying a request.

Retries are one of the simplest ways to improve an application’s resiliency. If an operation fails because of a brief network problem, chances are that it will work fine once the application waits for a while and tries again.

![](https://substackcdn.com/image/fetch/$s_!91E9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e764a6e-d992-4edc-a554-c42ad4bfb27d_3902x2144.png)

The main thing to guard against is creating an infinite retry loop. It can increase costs and make the outage worse. A safer approach to retrying limits the number of attempts. The time delay between each attempt should increase after each failure. This technique is known as exponential backoff. A simple approach could be to wait 1 second before the first retry, 2 seconds before the second, and 4 seconds before the third, and so on.

![](https://substackcdn.com/image/fetch/$s_!YGNy!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F762eb24e-5fdb-4aa1-a554-5a25a7b98c7e_3008x1710.png)

Applications also often add a small random amount of time to each delay. This is known as jitter. Without jitter, thousands of failed requests may all retry at the same time. This can cause another traffic spike and negate the benefit of retrying.

![](https://substackcdn.com/image/fetch/$s_!JasR!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F281bf6ca-5a90-4ae7-bbaf-892a770dd446_3240x1588.png)

Retries should be used for timeouts, temporary network failures, 429 responses, and some specific 5xx responses. We shouldn’t use them for failures such as invalid credentials, prohibited requests, bad input, or other problems that will produce the same result every single time.

## How to Manage Fallbacks and Graceful Degradation?

In an application, the fallback path is an alternative path. It is used when the normal preferred path fails due to some failure.

An application can use the fallback approach in the following manner:

- Attempt to use the primary model, which is usually of high quality.
- If that model is unavailable, switch to a smaller backup model.
- If no model is available, return a pre-defined fallback response or cached information.
- Lastly, if the request can’t be handled safely through any option, transfer it to a human for further action.

See the diagram below:

![](https://substackcdn.com/image/fetch/$s_!zALE!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a8bb6dc-ea20-4b78-a687-c2295e88e14b_3710x1922.png)

The best fallback approach depends on the task. For example, we might be okay to use a smaller model for summarizing an internal meeting. However, it might not be a good choice for interpreting a complicated legal document. Similarly, a cached response may be good enough for a general FAQ type scenario. But it won’t be suitable for something like the current account balance.

In other words, the fallback strategy should not violate the original requirements of the operation. We can’t just plug any available model into the flow. It’s also important to avoid dependency on a single point of failure. For example, if both the primary and backup models are accessed through the same provider, an outage can disable both. For real redundancy, we should have separation between the two pathways.

## How Do Circuit Breakers Work in this Setup?

Consider a scenario where the LLM provider is unavailable. Every request is timing out. In such cases, it is not wise to keep sending more requests. They only waste resources and make users wait for failures.

A circuit breaker can temporarily stop calls to a failing service. It commonly has three states:

- In the closed state, we can send the requests at normal cadence.
- In the open state, requests get rejected or redirected immediately. This is because the service is considered unhealthy.
- In the half-open state, a small number of test requests are allowed to go through. They help determine whether the service has recovered to some extent.

![](https://substackcdn.com/image/fetch/$s_!VPTM!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd4c6a6a-e14a-4698-b41c-1c222d7c2eac_2448x1992.png)

If the test requests in the half-open state succeed, the circuit can close. But if they fail, the circuit goes back to the open state. In this way, circuit breakers help get rid of repeated failures from infecting the rest of the application. They also let us configure the appropriate fallback behaviour.

## Rate Limiting, Queues, and Concurrency Control

An LLM-powered application can’t accept unlimited LLM work just because users can submit it from the UI.

For example, if 10K requests arrive at once, forwarding all of them to the LLM provider immediately might exhaust provider limits, database connections, memory, or the application’s budget.

Using rate limiting, we can control how frequently a user or client can submit requests. With concurrency control, we can limit how frequently a user or client might submit requests. Also, concurrency control puts a cap on how many requests the application can process simultaneously. A queue stores extra work until capacity becomes available.

Interactive requests where a user is waiting for the response should usually receive higher priority over background work. For example, a user waiting for a chat response should not be blocked because thousands of documents are being summarized in the background.

The application should also place limits on token usage, document size, number of retrieved passages, number of tool calls, and total workflow duration.

## Conclusion

In this article, we have taken a detailed look at resiliency and error handling aspects when it comes to LLM-powered applications.

The key takeaway is that LLM-powered applications can have failures that are different from traditional applications. This is because of the inherent probabilistic approach of the LLMs. The important thing is to classify the type of failure so that proper action can be taken by the application.

Despite the differences in the types of errors, we can still borrow many of the techniques for error handling from traditional applications. For example, things like retries, fallbacks, circuit breakers, rate limiting, and queuing can help.

---

∙