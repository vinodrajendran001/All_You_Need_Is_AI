# DeepSeek

Vinod

---
## Understanding MDP

>A Markov decision process (MDP) is defined as a stochastic decision-making process that uses a mathematical framework to model the decision-making of a dynamic system in scenarios where the results are either random or controlled by a decision maker, which makes sequential decisions over time.

---
## MDP Background


<grid drag="50 50" drop="5 10" bg="red">
60 x 55
</grid>

<grid drag="40 50" drop="-5 10" style=bg="green">

'''
Prompt (Initial State):  
"Solve this math problem: What is 12 + 15?"  
  
Possible Actions (Next Tokens):  
- "Let's"  
- "The"  
- "12"  
- ...  
  
Trajectory Example:  
"Let's solve this step by step:  
1) First, we have 12  
2) Adding 15 to it  
3) 12 + 15 = 27  
Therefore, the answer is 27."
}
```
</grid>

<grid drag="90 20" drop="5 -10" bg="gray">
90  x 20
</grid>



---

## LLM-MDP (as used in DeepSeek R1)

![[Pasted image 20250304231944.png | 512 512]]

---
## PPO vs GRPO

![[Pasted image 20250304232043.png]]

---
