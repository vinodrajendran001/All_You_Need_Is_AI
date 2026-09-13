---
type: raw-source
source_id: src-2026-09-13-sumit-scaling-distributed-systems
title: "Scaling Simplified: How Distributed Systems Handle Millions"
author: Sumit K
url: "https://medium.com/google-cloud/scaling-simplified-how-distributed-systems-handle-millions-2854aa1024c6"
published: 2025-01-05
captured: 2026-09-13
created: 2026-09-13
updated: 2026-09-13
tags:
  - source/raw
  - distributed-systems
  - scalability
  - system-design
status: active
---
![](https://miro.medium.com/v2/resize:fit:1280/format:webp/0*zuvEcVCtPs_UYi6K.gif)

Scalability is one of the cornerstone principles of system design, especially in distributed systems. It measures the system’s ability to handle increasing amounts of work or accommodate growth. In this article, we’ll explore scalability in detail, clarify common misconceptions, and analyze why it’s not just about adding more resources. We’ll also delve into real-world analogies, examine the trade-offs, and understand scalability’s role in monolithic and microservices architectures.

## What is Scalability?

In general, scalability refers to the ability to grow or expand something efficiently while maintaining the performance. Scalability is about handling growth while preserving or enhancing performance and [reliability](https://medium.com/google-cloud/building-reliable-infrastructure-in-google-cloud-b46ac43cbf70). It’s not just about “getting bigger” it’s about doing so in a way that aligns with your goals ensuring a seamless experience for everyone involved. In the context of distributed system design, it signifies a system’s ability to grow in capacity without degrading performance or reliability. A system must be scalable to accommodate growing user traffic, data volumes, or computing demands without suffering a major performance hit or necessitating a total redesign.

**Lets understand with real world example:**

consider a play school that starts with a single branch, serving 30 children providing them with quality education and personalized attention. As the reputation of the school grows, so does the demand. To meet this demand, the school scales its operations, opening branches across multiple location of the city and eventually serving 300 or even 3,000 children. Despite the significant increase in the number of children, the school ensures that the quality of education, teacher-student interactions, and the overall customer experience remain as excellent as they were when it was a single branch.

In system design, scalability mirrors this scenario: it’s about growing intelligently without compromising the quality of service.

## Scalability Strategies

Many people mistakenly equate scalability with just vertical (adding resources) or horizontal (adding instances) scaling, but scalability is more nuanced and often relies on intelligent solutions beyond these traditional approaches. In the real world, **scalability is increasingly handled through innovative technologies like Content Delivery Networks (CDNs). Yes, you heard that right** — for data-centric applications like Facebook, Google, Instagram, Amazon, or Netflix, most of your requests are served through CDNs. we will discuss CDN in details further in this article.

## 1\. Vertical Scaling (Scaling Up)

Vertical Scaling refers to adding more power (CPU, RAM, Storage) to your existing servers. While this can be a quick solution to handle a growing workload but it is limited to certain extent of the server. it can’t go beyond at certain limit. Sometime it could be expensive solution and may requires downtime for upgrades. Vertical Scaling are simple to implement without much changes required in the system architecture however it is limited by hardware constraint and single point of failure.

- Upgrading a database server from 16 GB RAM to 64 GB RAM.
- Moving from a single-core processor to a multi-core processor.
![](https://miro.medium.com/v2/resize:fit:1214/format:webp/1*z1wr8n-aICfJS3tg4RvcmA.png)

Vertical Scaling — More resources

## 2\. Horizontal Scaling (Scaling Out)

Horizontal scaling means adding more instances or nodes to your system and distributing the load on multiple nodes. This is one of best way and widely adopted by organization to improve the extensive systems. By leveraging horizontal scaling, organizations can handle increased demand efficiently, ensure high availability, and minimize the risk of bottlenecks. In my experience, horizontal scaling has proven to be a reliable solution for scaling large-scale systems. With horizontal scaling you can get virtually unlimited scalability with HA and Fault tolerance but it requires changes in the architecture like load balancing, maintaining sync nodes etc. For example:

- Adding more servers to a web server cluster to handle additional requests. Sharding a database to distribute data across multiple machines. complexity in managing stateful templates requires careful handling of user data, sessions and of course monitoring more servers than before.

> Sharding is a database scaling technique that divides large datasets into smaller, more manageable pieces, called shards, which are distributed across multiple servers

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*aQmy1OgMFHNnvy_iTLn5Bg.png)

Horizontal Scaling — More Servers

## 3\. Diagonal Scaling

A hybrid approach that combines vertical and horizontal scaling. Start by scaling vertically to a threshold, then scale horizontally as needed.

## 4\. Load Balancing:

**Load balancing** is a fundamental component in distributed system design that ensures efficient distribution of incoming traffic across multiple servers or nodes. This not only prevents individual servers from becoming overwhelmed but also improves performance. In nutshell, Load balancing is the essential component of scalability in distributed system design as no system can grow effectively without it.

Let’s understand how Cloud providers scale their load balancing solutions to handle massive traffic efficiently by using both **regional** and **global** load-balancers. All regional and global load balancers themselves run on compute resources managed by cloud provider only. Cloud providers like Google, AWS, and Azure scale their load balancing services by leveraging their global infrastructure, distributed systems, and dynamic provisioning of resources. So being a managed service, it is automatically managed by service provider. This means the user doesn’t need to manage the scaling of the load balancer itself, the cloud provider handles that complexity through their orchestrated and automated systems

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*uFnKHwdKqg6EpfDEc804Ug.png)

Load Balancer — Scalability

## 4\. Caching

Caching is important because it makes your website faster. It decreases load time which in turn creates a better user experience. **Caching** plays a pivotal role in system design s it store frequently accessed data in memory to reduce database load and improve response times. By storing frequently accessed data in a temporary storage layer (cache), systems can retrieve that data much faster than querying databases.This approach not only speeds up the system but also helps reduce the load on backend resources, which **contributes significantly to scalability**. For example A user requests a product detail page, and the application checks if the data is available in the cache. If it is, the data is served instantly from the cache, instead of hitting the database. Caching can be deployed at different layers or combination of layers within a system depending on application design sensitivity to the latency and performance.

- **Application-level caching**: Data such as user sessions, product catalogs, or frequently accessed files are cached in-memory within the application
- **Client-side caching**: Frequently used data can be cached on the user’s device reducing load on the server.
- **Database query caching**: Results of frequently queried data are cached, preventing the database from being overwhelmed by repetitive queries.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Vv8ckOKd8oJRJQMHMs0UoA.png)

Database Caching

- **Edge caching**: Content Delivery Networks (CDNs) cache content at the edge of the network, bringing data closer to the user. will discuss this shortly.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*VKyAp6LFampfGIemkcJYFQ.png)

CDN

## 5\. Database Sharding or Partitioning

Sharding is a database partitioning technique where large datasets are split into smaller pieces called **shards.** Each shard is stored on a separate database server or node(also called physical shard). This technique allows you to distribute the database load across multiple servers, improving performance and scalability. Think of sharding as dividing a massive library into multiple smaller sections (shards), with each section housed in a separate room (server). When you need a book (data), you can go directly to the right room, making it much faster to find the book compared to searching through the entire library in one room.

Sharding is essential when a database reaches a size or traffic level that a single server cannot handle. It allows businesses to scale without encountering performance bottlenecks, ensuring the database can handle more data and traffic while keeping response times low.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*FIh6tWEY-CFJEoQcymQ_jg.png)

Database Sharding

Sharding was one of the first ways databases were distributed to improve performance. Recent innovations have made it one of the best.How can we handle this incredible volume of traffic when it reaches the database cluster? The answer could be sharding

Not all organizations need to implement sharding. For smaller systems with low to moderate traffic and smaller datasets, a single server may suffice. However, for **large enterprises** or applications with massive datasets and high throughput (like social networks, e-commerce sites) **sharding is crucial**. It ensures the database can continue to perform well as the system grows in size and complexity.

Sharding is a complex topic. There are multiple types of sharding I will dedicate a separate in-depth article with detailed analysis and explanations.

## 6\. Asynchronous Processing or event driven processing

Asynchronous processing is a technique in system design where tasks are executed independently of the main application flow. Instead of waiting for a task to complete before moving on to the next, the system triggers the task and continues with other operations. Once the task is finished, the system is notified. Asynchronous Processing is heavily used in microservice architecture where each service is responsible for specific functionality and often needs to interact with other services. Although microservices can directly interact with one another but its might reduce the performance when you expect 100 and 1000s of request per second. Aysnc processing allow microservice to be loosely couples. Instead of waiting for a response from one service before moving to another, a service can queue requests or events and continue working on other tasks. This reduces dependency and makes services more resilient to failures and scale seamlessly without becoming overburdened. Again this is huge topic, will discuss in a separate article.

In the Picture below, you can see how the order processing flow from receiving an order, checking the inventory and completing the payment. All can be handled asynchronously through events, ensuring the system remains efficient, scalable, and resilient.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*w2EW-oN861eB6sThCzeWIg.png)

Async processing of events or messages — loosely couplesd and scalable

## Scalability vs. Performance

Scalability and performance are often intertwined but distinct concepts. Performance means How efficiently a system handles a given workload andScalability is how well a system handles increased workload while maintaining performance. A system can perform well with a small user base but fail to scale under a larger load. Conversely, a scalable system may initially perform poorly but is designed to handle growth effectively. **Example:** A website might load quickly for 100 users (good performance) but crash when 10,000 users access it simultaneously (poor scalability).

## Challenges in Scalability

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*de58Ns2BjFelv4CtzC2MDA.gif)

Scaling a system from a few hundred users to millions introduces several challenges. Scaling a system from a few hundred users to millions👥 introduces several challenges. As systems grow, complexity increases due to the need for maintaining consistency, handling failures, and coordinating distributed nodes. Data management becomes more difficult, with techniques like sharding, replication, and eventual consistency adding layers of complexity. Latency can also rise as systems expand, resulting from network hops, data replication, and inter-service communication. Small errors in one service can propagate throughout the system, leading to widespread issues. Additionally, scaling incurs significant infrastructure and operational costs, requiring efficient strategies to minimize expenses while maintaining performance.

## Not Every Service Needs to Scale

It’s important to understand that not all applications or services require massive scalability. Scalability is a critical design consideration, but it should align with the specific needs and goals of the application. For example let say Services like **inventory management**, **orders**, **payments**, and **cart management** need robust scalability due to their critical role in handling real-time user actions. For example, during a flash sale or holiday season, these services experience heavy traffic as thousands or even millions of users browse, add items to their carts, place orders, and make payments simultaneously. On the other hand, services like **product reviews** or **user profiles** typically don’t experience the same level of traffic intensity.

## Scalability — Monoliths vs Microservices

**Monoliths**, while often criticized, can scale effectively to a certain extent. However, monoliths face bottlenecks beyond a certain scale due to single points of failure and resource limitations. different modules in the ecommerce application correspond to business logic for payment, delivery, and order management. All of these modules are packaged and deployed as a single logical executable. Monolithic applications can be difficult to scale when different modules have conflicting resource requirements. For example, one module might implement CPU-intensive image-processing logic. Another module might be an in-memory database. Because these modules are deployed together, you have to compromise on the choice of hardware.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*5hDIRx2Pb6JKh2M2JQ791A.png)

Typical Monolithic Application — All service scales together (Tightly coupled)

**Microservices** are designed with scalability in mind. Each service can scale independently based on its workload. Microservices are ideal for systems serving millions or billions of users but come with increased architectural complexity. Each microservice is a mini-application that has its own architecture and business logic. The microservices architecture pattern significantly changes the relationship between the application and the database. Microservices architecture lets you scale each service independently. When you scale services independently, you help increase the availability and the reliability of the entire system. To learn more about reliability, 👉 [click here](https://medium.com/google-cloud/building-reliable-infrastructure-in-google-cloud-b46ac43cbf70)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*-uhLBOsn5zoaTGit79Ao3w.png)

Microservice Application — each service can scale independently (loosely coupled)

## Conclusion

Scalability is not a one-size-fits-all solution but a tailored approach based on the needs of your system and users. While monolithic applications can handle small to medium-scale workloads effectively, microservices architectures shine when dealing with massive user bases and high growth potential. As systems scale, complexity grows, but with thoughtful design, efficient strategies, and the right tools, it’s possible to build systems that not only scale but thrive under pressure.

Remember, scalability isn’t just about adding resources — it’s about creating resilient, adaptive systems that deliver consistent performance at any scale.

*Thanks for Reading! I hope you have enjoyed reading this article, show your support by hitting the “Clap” button! You can clap up to 50 times — so don’t hold back! 😊 If you Like it, please share it with others*