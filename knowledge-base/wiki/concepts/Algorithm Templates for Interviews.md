---
type: concept
created: 2026-05-21
updated: 2026-05-21T13:36+08:00
tags:
  - concept
  - algorithms
  - data-structures
  - interview-prep
source_ids:
  - src-2026-05-21-leetcode-templates
  - src-2026-05-18-hanfang-pytorch-practice
status: active
---

# Algorithm Templates for Interviews

The template-based approach to interview preparation treats coding problems as **recognition tasks before they become implementation tasks**. Instead of deriving every solution from first principles under time pressure, the candidate learns to classify the prompt, select the right reusable pattern, and then customize the pattern's invariants, state, and stopping conditions.

## Core workflow

A durable interview loop emerges across both DSA and ML-engineering coding rounds:

1. **Recognize the signal** — contiguous range, sorted input, monotonic predicate, graph traversal, reversible search, overlapping subproblems, top-`k`, or stateful design prompt.
2. **Select the template** — sliding window, two pointers, binary search, BFS/DFS, backtracking, DP, heap, trie, Union-Find, and so on.
3. **Customize the moving parts** — validity condition, update rule, recurrence, comparator, node state, or class API.
4. **State complexity clearly** — good interview performance depends not just on passing code, but on explaining why the chosen template has the right time/space profile.

[[Universal LeetCode Templates]] makes this workflow explicit for algorithmic coding rounds, while [[Han Fang - PyTorch Practice]] applies a similar pattern in ML-oriented rounds by turning common PyTorch interview tasks into repeatable implementation drills.

## Template Arsenal (20 patterns with code)

### 1. 📐 Sliding Window

**When to apply:** contiguous subarray/substring, "maximum/minimum subarray", "at most K distinct", "longest substring without repeating".

```python
def sliding_window_variable(arr, condition_arg):
    from collections import defaultdict
    window = defaultdict(int)
    left = 0
    result = 0

    for right in range(len(arr)):
        window[arr[right]] += 1

        while WINDOW_IS_INVALID(window, condition_arg):  # shrink until valid
            window[arr[left]] -= 1
            if window[arr[left]] == 0:
                del window[arr[left]]
            left += 1

        result = max(result, right - left + 1)

    return result

# CUSTOMIZATION: replace WINDOW_IS_INVALID
#   LC 3:   len(window) != (right - left + 1)   → duplicate exists
#   LC 340: len(window) > K                      → too many distinct chars
```

**Complexity:** O(n) time, O(k) space.

---

### 2. 🔍 Two Pointers

**When to apply:** sorted array, "pair with target sum", "remove duplicates in-place", "container with most water", "palindrome check".

```python
# Converging (sorted array)
def two_pointer_converge(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        current = arr[left] + arr[right]
        if current == target:
            return [left, right]
        elif current < target:
            left += 1
        else:
            right -= 1
    return None

# Same-direction (in-place partition)
def two_pointer_same_direction(arr):
    write = 0
    for read in range(len(arr)):
        if SHOULD_KEEP(arr[read]):
            arr[write] = arr[read]
            write += 1
    return write
```

**Complexity:** O(n) time, O(1) space.

---

### 3. ⚡ Binary Search

**When to apply:** sorted array, "find minimum/maximum that satisfies", "capacity to ship within D days". Key signal: can eliminate half the search space each step.

```python
# Classic — find exact value
def binary_search_exact(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

# On Answer — monotonic predicate (F F F T T T → find first T)
def binary_search_on_answer(lo, hi):
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if IS_FEASIBLE(mid):
            hi = mid          # try smaller
        else:
            lo = mid + 1      # must go bigger
    return lo                 # smallest feasible answer
```

**Complexity:** O(n log S) time, O(1) space.

---

### 4. 🌳 BFS (Breadth-First Search)

**When to apply:** shortest path in unweighted graph/grid, "minimum number of steps", "level-order traversal".

```python
from collections import deque

def bfs(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    queue = deque([(*start, 0)])
    visited = {start}
    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    while queue:
        r, c, dist = queue.popleft()
        if (r, c) == end:
            return dist
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols and
                (nr, nc) not in visited and grid[nr][nc] != WALL):
                visited.add((nr, nc))        # mark BEFORE enqueueing
                queue.append((nr, nc, dist + 1))
    return -1
```

**Complexity:** O(V + E) time, O(V) space.

---

### 5. 🔄 DFS (Depth-First Search)

**When to apply:** "find all paths", "number of islands", "connected components", "detect cycle", "path sum".

```python
# Grid DFS (iterative)
def dfs_grid(grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    directions = [(0,1),(0,-1),(1,0),(-1,0)]
    result = 0

    def dfs(r, c):
        stack = [(r, c)]
        visited.add((r, c))
        while stack:
            cr, cc = stack.pop()
            for dr, dc in directions:
                nr, nc = cr + dr, cc + dc
                if (0 <= nr < rows and 0 <= nc < cols and
                    (nr, nc) not in visited and grid[nr][nc] == TARGET):
                    visited.add((nr, nc))
                    stack.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r][c] == TARGET:
                dfs(r, c)
                result += 1
    return result

# Tree DFS (recursive)
def dfs_tree(root):
    def helper(node):
        if not node:
            return 0
        left = helper(node.left)
        right = helper(node.right)
        return COMBINE(node.val, left, right)
    return helper(root)
```

**Complexity:** O(V + E) time, O(V) space.

---

### 6. 🧩 Backtracking

**When to apply:** "find all combinations/permutations/subsets", "generate all valid", "N-Queens", "word search".

```python
def backtrack(nums):
    result = []

    def helper(start, path):
        if IS_COMPLETE(path):
            result.append(path[:])
            return

        for i in range(start, len(nums)):
            if SHOULD_SKIP(i, path, nums):
                continue
            path.append(nums[i])         # CHOOSE
            helper(i + 1, path)          # RECURSE (i for reuse, i+1 for no reuse)
            path.pop()                   # UN-CHOOSE (backtrack)

    nums.sort()
    helper(0, [])
    return result

# CUSTOMIZATION:
#   IS_COMPLETE: len(path) == len(nums) for permutations; sum(path) == target for combo sum
#   SHOULD_SKIP: i > start and nums[i] == nums[i-1] for dedup
#   NEXT INDEX: i+1 (no reuse), i (with reuse)
```

**Complexity:** O(2^n) subsets, O(n!) permutations. Space O(n).

---

### 7. 📊 Dynamic Programming

**When to apply:** "minimum/maximum cost", "number of ways", overlapping subproblems + optimal substructure.

```python
# 1D Bottom-Up
def dp_1d(nums):
    n = len(nums)
    dp = [0] * (n + 1)
    dp[0] = BASE_CASE_0
    for i in range(1, n + 1):
        dp[i] = RECURRENCE(dp, nums, i)
    return dp[n]

# 2D Bottom-Up
def dp_2d(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

# Top-Down Memoization
from functools import lru_cache
def dp_top_down(nums, target):
    @lru_cache(maxsize=None)
    def helper(index, remaining):
        if remaining == 0: return True
        if index >= len(nums) or remaining < 0: return False
        return helper(index + 1, remaining - nums[index]) or helper(index + 1, remaining)
    return helper(0, target)
```

**Complexity:** O(n × S) time and space where S = state space size.

---

### 8. 🗂️ Monotonic Stack

**When to apply:** "next greater/smaller element", "largest rectangle in histogram", "daily temperatures".

```python
def monotonic_stack(arr):
    n = len(arr)
    result = [-1] * n
    stack = []                               # stores indices; decreasing order of values

    for i in range(n):
        while stack and arr[stack[-1]] < arr[i]:  # change < to > for "next smaller"
            idx = stack.pop()
            result[idx] = arr[i]
        stack.append(i)

    return result
```

**Complexity:** O(n) time, O(n) space.

---

### 9. 🏔️ Heap / Priority Queue (Top-K)

**When to apply:** "Kth largest/smallest", "top K frequent", "merge K sorted lists", "median from data stream".

```python
import heapq

# Top-K
def top_k(nums, k):
    min_heap = []
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    return min_heap[0]  # Kth largest

# Merge K Sorted
def merge_k_sorted(lists):
    min_heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(min_heap, (lst[0], i, 0))
    result = []
    while min_heap:
        val, list_i, elem_i = heapq.heappop(min_heap)
        result.append(val)
        if elem_i + 1 < len(lists[list_i]):
            heapq.heappush(min_heap, (lists[list_i][elem_i + 1], list_i, elem_i + 1))
    return result
```

**Complexity:** Top-K: O(n log k). Merge-K: O(N log k).

---

### 10. 🔗 Linked List

**When to apply:** "reverse linked list", "detect cycle", "merge two lists", "find middle".

```python
# Floyd's Cycle Detection
def linked_list_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow  # cycle start
    return None

# Reverse (iterative)
def reverse_linked_list(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev

# Dummy Head (merge/build)
def merge_two_sorted(l1, l2):
    dummy = ListNode(0)
    tail = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1; l1 = l1.next
        else:
            tail.next = l2; l2 = l2.next
        tail = tail.next
    tail.next = l1 or l2
    return dummy.next
```

**Complexity:** O(n) time, O(1) space.

---

### 11. 🌲 Trie (Prefix Tree)

**When to apply:** "prefix search", "autocomplete", "word dictionary with wildcards", "word search II".

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        node = self._traverse(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        return self._traverse(prefix) is not None

    def _traverse(self, text):
        node = self.root
        for ch in text:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
```

**Complexity:** O(L) per operation, O(N × L) total space.

---

### 12. 🔀 Union-Find (Disjoint Set Union)

**When to apply:** "connected components", "redundant connection", "accounts merge", "number of provinces".

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False  # cycle / redundant edge
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.components -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

**Complexity:** O(α(n)) ≈ O(1) amortized per operation.

---

### 13. 📈 Prefix Sum

**When to apply:** "subarray sum equals K", "range sum query", "count subarrays with sum", "pivot index".

```python
def prefix_sum_subarray_count(nums, k):
    from collections import defaultdict
    prefix_count = defaultdict(int)
    prefix_count[0] = 1
    current_sum = 0
    result = 0

    for num in nums:
        current_sum += num
        result += prefix_count[current_sum - k]
        prefix_count[current_sum] += 1

    return result
```

**Complexity:** O(n) time, O(n) space.

---

### 14. 🧮 Topological Sort

**When to apply:** "course prerequisites", "task scheduling with dependencies", "build order", "detect cycle in directed graph".

```python
from collections import deque, defaultdict

def topological_sort(num_nodes, prerequisites):
    graph = defaultdict(list)
    in_degree = [0] * num_nodes

    for dest, src in prerequisites:
        graph[src].append(dest)
        in_degree[dest] += 1

    queue = deque(node for node in range(num_nodes) if in_degree[node] == 0)
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == num_nodes else []  # empty = cycle detected
```

**Complexity:** O(V + E) time and space.

---

### 15. 💰 Greedy (Interval Problems)

**When to apply:** "merge intervals", "minimum meeting rooms", "non-overlapping intervals".

```python
# Merge Intervals
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

# Maximum Non-Overlapping (sort by END time)
def interval_scheduling(intervals):
    intervals.sort(key=lambda x: x[1])
    count, last_end = 0, float('-inf')
    for start, end in intervals:
        if start >= last_end:
            count += 1
            last_end = end
    return count

# Minimum Meeting Rooms
import heapq
def min_meeting_rooms(intervals):
    intervals.sort(key=lambda x: x[0])
    heap = []
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)
        heapq.heappush(heap, end)
    return len(heap)
```

**Complexity:** O(n log n) time, O(n) space.

---

### 16. 📊 Bit Manipulation

**When to apply:** "single number", "power of two", "count bits", "subsets using bitmask", "XOR tricks".

```python
# XOR — find unique element (duplicates cancel)
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num
    return result

# Power of two: exactly one bit set
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

# Count set bits (Brian Kernighan's)
def count_bits(n):
    count = 0
    while n:
        n &= (n - 1)  # clear lowest set bit
        count += 1
    return count

# Enumerate all subsets via bitmask
def subsets_bitmask(nums):
    n = len(nums)
    return [[nums[i] for i in range(n) if mask & (1 << i)] for mask in range(1 << n)]
```

**Complexity:** XOR O(n), count bits O(k), subsets O(2^n × n).

---

### 17. 🔄 Dijkstra's (Weighted Shortest Path)

**When to apply:** "shortest path with weighted edges", "minimum cost to reach", "network delay time". Non-negative edge weights.

```python
import heapq
from collections import defaultdict

def dijkstra(n, edges, src, dst):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))

    dist = [float('inf')] * n
    dist[src] = 0
    min_heap = [(0, src)]

    while min_heap:
        d, u = heapq.heappop(min_heap)
        if d > dist[u]:
            continue               # stale entry
        if u == dst:
            return d
        for v, w in graph[u]:
            new_dist = d + w
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(min_heap, (new_dist, v))

    return dist[dst] if dist[dst] != float('inf') else -1
```

**Complexity:** O((V + E) log V) time, O(V + E) space.

---

### 18. 🪟 Monotonic Deque (Sliding Window Max/Min)

**When to apply:** "sliding window maximum/minimum", "max of all subarrays of size k".

```python
from collections import deque

def sliding_window_maximum(nums, k):
    dq = deque()  # stores indices; front = index of current max
    result = []

    for i in range(len(nums)):
        while dq and dq[0] < i - k + 1:      # remove out-of-window
            dq.popleft()
        while dq and nums[dq[-1]] <= nums[i]: # maintain decreasing order
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])        # front = max of window

    return result
# For minimum: change <= to >= in inner while
```

**Complexity:** O(n) time, O(k) space.

---

### 19. 🔢 Math Patterns

**When to apply:** "GCD/LCM", "prime numbers", "modular arithmetic", "fast exponentiation".

```python
import math

def gcd(a, b): return math.gcd(a, b)
def lcm(a, b): return a * b // math.gcd(a, b)

# Sieve of Eratosthenes
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]

# Fast modular exponentiation
def power_mod(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        exp >>= 1
        base = base * base % mod
    return result
```

---

### 20. 🗃️ Design / Data Structure Problems

**When to apply:** "design a data structure", "implement LRU cache", "min stack", "design HashMap".

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # evict LRU (front)
```

**Complexity:** O(1) get and put.

## Why this matters for interviews

Algorithm interviews reward **fast pattern recognition under ambiguity**. The strongest candidates usually do three things well:

- infer the hidden structural signal in the prompt,
- pick a template whose invariant matches that signal, and
- explain the tradeoff between alternative templates before coding.

That is why template study is more than memorization. It is a way to internalize which invariants matter: window validity, pointer movement rules, BFS frontier levels, DP state definitions, monotonic stack ordering, or heap size constraints.

## DSA templates vs. ML interview implementations

The new LeetCode source and the existing Han Fang source cover **complementary halves of technical interview preparation**:

- [[Universal LeetCode Templates]] emphasizes abstract algorithm families, asymptotic complexity, and problem classification.
- [[Han Fang - PyTorch Practice]] emphasizes hands-on PyTorch mechanics such as autograd, normalization, attention, optimizers, and training loops.

For ML-engineering interviews, both matter. DSA rounds often test whether the candidate can quickly map a prompt to a canonical algorithmic skeleton; ML rounds often test whether the candidate can implement or explain model-training components inside a concrete framework. The two study modes reinforce each other because both reward reusable mental templates rather than ad hoc coding.

## Meta-strategies

- **Listen for trigger phrases** such as “contiguous,” “shortest path,” “at most `k`,” “minimum feasible,” “top `k`,” or “design a class.”
- **Name the invariant before writing code**: what must stay true about the window, stack, heap, graph frontier, or DP table?
- **Identify customization points** early: predicate, recurrence, merge rule, state update, or data-structure API.
- **Say the complexity out loud** before and after implementation; interviewers use this to judge whether the template choice was principled.
- **Practice paired coverage**: algorithm templates for general coding rounds, and framework-specific drills for ML rounds.

## Related pages

- [[Universal LeetCode Templates]]
- [[Han Fang - PyTorch Practice]]
- [[Neural Network Fundamentals]]
- [[AI Knowledge Base Overview]]
- [[index|Knowledge Base Index]]
