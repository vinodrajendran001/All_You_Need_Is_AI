---
title: "Jev Explained for Normies"
source: "https://x.com/matthewcanham/status/2102077098756280413?utm_source=www.theaivalley.com&utm_medium=newsletter&utm_campaign=ai-is-now-building-the-next-ai&_bhlid=a29e6d0c7e83402529064bfbc071198a4b5ac89c"
author:
  - "[[@matthewcanham]]"
published: 2026-09-22
created: 2026-09-23
description: "If you’ve been hanging out on the internet the past few days, you’ve probably come across Jev, a new AI model that’s taken the AI community ..."
tags:
  - "clippings"
---
![Image](https://pbs.twimg.com/media/HSwSyiyb0AIiVi9?format=jpg&name=large)

If you’ve been hanging out on the internet the past few days, you’ve probably come across Jev, a new AI model that’s taken the AI community by storm. Jev is not a traditional LLM. It’s built for making decisions, not for writing text. Having gone deep on Jev over the past few days, I really do believe the hype is real and there’s huge potential here for product builders.

[As I’ve previously said](https://x.com/matthewcanham/status/2098824717725806834?s=20), it’s critical that everyone learn how the technology behind AI actually works, even those in non-technical roles. Understanding how an agentic system works allows you to apply the technology thoughtfully to your own products.

I’ve had multiple people reach out explaining that they’ve read everything out there on Jev and they still don’t understand what it actually is. So this article is for them. It’s a guide to Jev for the normies out there. If everything else that you’ve read about Jev has left you with more questions than answers, this article will be different. By the end you’ll have a foundational understanding of what Jev is, how it’s different to an LLM, and how you can apply it to the products that you build.

# The importance of decisions in software

Software is full of decisions. Does this customer message require urgent attention? Is this payment fraudulent? Should we render the page in English or French?

A product might need to make decisions like this millions of times per day.

But the complexity of decisions that computers are able to make is limited. The questions above can be answered with some simple rules. For example, we could determine whether to render the page in English or French based on the user’s language setting or maybe their IP address. But not all questions are so simple.

Take, for example, a picture of a hotdog. No set of simple rules will allow a computer to identify whether my picture does in fact contain a hotdog.

So computer scientists came up with a new method for computers to make more complex decisions: machine learning. It turns out that by combining some neat algorithms with many many examples of pictures containing hotdogs, a computer can in fact become quite proficient in identifying pictures with hotdogs.

<video preload="auto" tabindex="-1" playsinline="" aria-label="Embedded video" poster="https://pbs.twimg.com/tweet_video_thumb/HSwQQLEbYAAaEYP.jpg" src="https://video.twimg.com/tweet_video/HSwQQLEbYAAaEYP.mp4" type="video/mp4" style="width: 100%; height: 100%; position: absolute; background-color: black; top: 0%; left: 0%; transform: rotate(0deg) scale(1.005);"></video>

GIF

Our hotdog model is a type of model called a classifier. It's called this because it classifies things. Classifiers are used extensively in software today to make complex decisions.

But the problem with classifiers is that they don’t generalize outside of the domain they were trained on. My classifier that can identify pictures of hotdogs won’t be able to help me identify fraudulent transactions. And because of the data and expertise required to train a classifier, there were many types of problems that computers were not able to solve. That is until…

# The large language model

When OpenAI released ChatGPT in November 2022 it took the world by storm. The reason it became so popular was not because of its outright intelligence but instead because of its ability to generalize.

ChatGPT had a foundational understanding of the world that meant it could have a conversation about hotdogs and fraudulent transactions, all in one.

Large language models like ChatGPT, Claude, Grok, and Kimi have the primary function of generating text. But anyone who’s used these models knows they can think, reason, and ultimately make decisions. As an example, here’s how an LLM might make a decision about whether a given image is a hotdog or not.

<video preload="auto" tabindex="-1" playsinline="" aria-label="Embedded video" poster="https://pbs.twimg.com/tweet_video_thumb/HSwJQAbboAAvyN7.jpg" src="https://video.twimg.com/tweet_video/HSwJQAbboAAvyN7.mp4" type="video/mp4" style="width: 100%; height: 100%; position: absolute; background-color: black; top: 0%; left: 0%; transform: rotate(0deg) scale(1.005);"></video>

![](https://pbs.twimg.com/tweet_video_thumb/HSwJQAbboAAvyN7.jpg?name=large)

GIF

Yes, large language models are able to make decisions. And they can make decisions across a wide range of knowledge domains.

Could LLMs be the holy grail? Could we finally have a general decision making model to apply to decisions in software today?

Well, not practically. LLMs, for all of their incredible power, are relatively slow and expensive. Far too slow and expensive to use in most of the types of applications software would be applied to.

If only we had a model that could make decisions across a broad range of general knowledge domains and do it fast and cheap…

# Introducing Jev, a classifier that generalizes

Jev is a new class of model that’s optimized for making decisions rather than generating text.

Jev retains the property of generalizing like an LLM while being relatively fast and cheap like a classifier. The claims are that Jev is 20-200x faster and 40-400x cheaper than comparable LLMs.

This is achieved because Jev doesn’t return an answer token by token like an LLM, it simply returns a decision.

And this is why engineers are so excited by it. It’s not that Jev is a new level of intelligence never before seen; it’s that it’s a level of intelligence never before seen operating this fast and this cheap.

You can’t chat with Jev. It’s not a chatbot. Jev expects three things as input:

- The question you want to answer
- The set of possible answers to that question
- The context needed to answer the question (Jev calls this “state”)

And Jev will then give you the following as an output:

- The answer it has selected
- The probability that answer is correct

That's it. No chatting, just a decision.

Jev supports three types of decisions:

- **Yes/no**, what Jev calls a “Noul”: returns the estimated probability that a statement is true
- **Choice**: selects from up to 255 multiple choice options and provides probabilities that each is correct
- **Score**: rates something against a scale of 2 to 10 levels

These choices enable advanced decision making in a fraction of the time and cost of previous approaches. Let’s take a look at an example of each.

## The noul (yes/no)

Say I’ve opened a new hotdog stand and I want to review customer feedback as it comes in so that I can react or respond accordingly.

For each review, let’s first ask the simple question of whether the review is a complaint about the food. The input to Jev might look something like this.

```json
{
  "model": "jev-latest",
  "state": "Waited twenty minutes, but the hotdog was worth it. Would come back if the queue was shorter.",
  "questions": {
    "food_complaint": {
      "type": "noul",
      "instructions": "Does this review express dissatisfaction with the food itself?",
      "criteria": {
        "true": "Complains about the taste, temperature, or quality of the food.",
        "false": "Does not complain about the food. Complaints only about queues or service do not count."
      }
    }
  }
}
```

You can see we’ve defined the question we want to answer (the "instructions"), the criteria for when to pick yes or no, and the state needed for Jev to make an accurate decision.

So we give the question above to Jev. Jev then outputs the following.

```json
{
  "answers": {
    "food_complaint": {
      "type": "noul",
      "noul": 0.04
    }
  }
}
```

Jev determines this particular feedback is only 4% likely to be complaining about the food. So we might classify this review as lower priority and follow up when we have time.

## Choice

Let’s understand each feedback item a little more by asking Jev to put the feedback into a category. Here's what our request to Jev might look like.

```json
{
  "model": "jev-latest",
  "state": "Waited twenty minutes, but the hotdog was worth it. Would come back if the queue was shorter.",
  "questions": {
    "main_topic": {
      "type": "choice",
      "instructions": "What is the main topic of this review? Select the option that best captures its primary focus.",
      "criteria": {
        "queue": "Queue length or waiting time is the main focus.",
        "food": "The taste, temperature, or quality of the food is the main focus.",
        "service": "Staff friendliness, helpfulness, or how they handled the order is the main focus. Comments only about waiting time belong under queue.",
        "other": "The main focus is something other than food, waiting time, or staff service."
      }
    }
  }
}
```

We’ve defined each choice that Jev can make with a description of when to use each (the "criteria"). Jev returns the following.

```json
{
  "answers": {
    "main_topic": {
      "type": "choice",
      "choice": "queue",
      "probabilities": {
        "queue": 0.80,
        "food": 0.15,
        "service": 0.03,
        "other": 0.02
      },
      "confidence": 0.60
    }
  }
}
```

Ok, Jev has chosen “queue” as the answer. You can also see it attaches probabilities to each of the choices.

## Score

Now let’s get Jev to rate how satisfied the customer is with the overall experience at our hotdog stand across five defined levels.

```json
{
  "model": "jev-latest",
  "state": "Waited twenty minutes, but the hotdog was worth it. Would come back if the queue was shorter.",
  "questions": {
    "overall_satisfaction": {
      "type": "score",
      "instructions": "How satisfied is this customer with their overall experience? Consider both positive and negative comments.",
      "criteria": [
        "Very dissatisfied: strongly negative about the experience overall.",
        "Dissatisfied: mostly negative, despite any positives.",
        "Mixed: meaningful positives and negatives, with neither clearly dominating.",
        "Satisfied: mostly positive, despite some complaints.",
        "Very satisfied: strongly positive, with no meaningful complaints."
      ]
    }
  }
}
```

Again, we provide a clear question, set of possible answers, and state. Jev returns the following.

```json
{
  "answers": {
    "overall_satisfaction": {
      "type": "score",
      "score": 2.1,
      "probabilities": {
        "0": 0.05,
        "1": 0.15,
        "2": 0.50,
        "3": 0.25,
        "4": 0.05
      }
    }
  }
}
```

2.1 out of 4, room for improvement.

The magic of Jev is that it’s able to make these decisions much faster and cheaper than an LLM. Here’s a side by side comparison of reviewing 60 feedback items that have been left for our hotdog stand. On the left is Jev, on the right is an LLM (gpt-5.6 Luna).

<video preload="none" tabindex="-1" playsinline="" aria-label="Embedded video" poster="https://pbs.twimg.com/amplify_video_thumb/2102066068433092608/img/83i6VO4GWOatvrUv.jpg" style="width: 100%; height: 100%; position: absolute; background-color: black; top: 0%; left: 0%; transform: rotate(0deg) scale(1.005);"></video>

![](https://pbs.twimg.com/amplify_video_thumb/2102066068433092608/img/83i6VO4GWOatvrUv.jpg?name=large)

Jev’s speed and cost advantage lowers the barrier to making decisions with software.

# Applying Jev

Anywhere in your product a decision could be made to improve an outcome for a user, consider applying Jev. Here are some examples.

Use **Yes/No** anywhere knowing whether something is true or false allows you to change the action taken.

- Does this customer’s message suggest they’re about to cancel their subscription?
- Does this supplier update suggest a shipment will miss its deadline?
- Does this student’s explanation reveal a misconception worth addressing?
- Does this meeting transcript contain a commitment nobody has been assigned to own?
- Does this player’s message suggest they’re stuck and could use a hint?

Use **Choice** anywhere selecting from a set of options allows you to decide what happens next.

- Which specialist team should handle this unusual customer request?
- Which product tutorial best matches what this user is trying to accomplish?
- Which character in a game should respond to what the player just said?
- Which museum audio-guide segment best answers a visitor’s question?
- Which available substitute best preserves a missing ingredient’s role in a recipe?

Use **Score** anywhere judging how much, how well, or how closely something meets a criterion allows you to prioritize or adjust an action.

- How disruptive is this software bug to the customer’s actual workflow?
- How closely does this travel itinerary match someone’s idea of a good holiday?
- How much does this customer interview support a particular product hypothesis?
- How far does this scene’s dialogue stray from the character’s established voice?
- How revealing would this game hint be, given what the player already knows?

# Time to build with Jev

Jev has opened up a world of new possibilities in the kinds of software and experiences that we can build for users.

Now that you know what Jev is and how it works, how are you going to apply this to the products you are building?