Below is a comprehensive collection of battle-tested templates, organized by topic. Each template includes pattern recognition signals, inline comments, and complexity analysis.

1. 📐 Sliding Window
When to Apply

Look for: contiguous subarray/substring, keywords like "maximum/minimum subarray", "at most K distinct", "longest substring without repeating", "smallest subarray with sum ≥ X". The input is linear (array/string) and you need an optimal subrange.

Template A — Variable-Width Window
def sliding_window_variable(arr, condition_arg):
    """
    Use when: window size is NOT fixed; you expand/shrink to meet a condition.
    Examples: Longest Substring Without Repeating Characters (LC 3),
              Minimum Size Subarray Sum (LC 209),
              Longest Substring with At Most K Distinct Characters (LC 340)
    """
    from collections import defaultdict
    window = defaultdict(int)          # tracks frequency (or any state) inside the window
    left = 0                           # left boundary of the window
    result = 0                         # stores the answer (max length, min length, etc.)

    for right in range(len(arr)):      # right boundary expands one element at a time
        window[arr[right]] += 1        # add the right element into the window state

        while WINDOW_IS_INVALID(window, condition_arg):  # shrink until valid
            window[arr[left]] -= 1     # remove the left element from state
            if window[arr[left]] == 0:
                del window[arr[left]]  # clean up zero-count entries
            left += 1                  # move left boundary rightward

        # window [left..right] is now valid → update answer
        result = max(result, right - left + 1)  # or min(), depending on the problem

    return result

# -------------------------------------------------------
# CUSTOMIZATION POINT — replace WINDOW_IS_INVALID:
#   LC 3:   len(window) != (right - left + 1)      → duplicate exists
#   LC 209: current_sum < target                    → (use a running sum instead of dict)
#   LC 340: len(window) > K                         → too many distinct chars
# -------------------------------------------------------

Template B — Fixed-Width Window
def sliding_window_fixed(arr, k):
    """
    Use when: window size K is given explicitly.
    Examples: Maximum Average Subarray I (LC 643),
              Max Sum Subarray of Size K,
              Permutation in String (LC 567)
    """
    window_sum = sum(arr[:k])          # initialize window with first K elements
    result = window_sum                # best answer seen so far

    for right in range(k, len(arr)):   # slide the window one step at a time
        window_sum += arr[right]       # add new element entering the window
        window_sum -= arr[right - k]   # remove the element leaving the window
        result = max(result, window_sum)  # update the best answer

    return result

Complexity: Time O(n) — each element enters/exits the window at most once. Space O(1) for fixed or O(k) for variable (where k = distinct elements tracked).

2. 🔍 Two Pointers
When to Apply

Look for: sorted array, "pair with target sum", "triplet sum", "remove duplicates in-place", "container with most water", "palindrome check". You need to compare/combine elements from two positions.

Template A — Opposite-Direction (Converging)
def two_pointer_converge(arr, target):
    """
    Use when: array is SORTED (or structure allows shrinking from both ends).
    Examples: Two Sum II (LC 167), 3Sum (LC 15), Container With Most Water (LC 11),
              Trapping Rain Water (LC 42), Valid Palindrome (LC 125)
    """
    left, right = 0, len(arr) - 1      # start from both extremes
    result = None                       # store whatever the problem asks for

    while left < right:                 # continue until pointers meet
        current = arr[left] + arr[right]  # compute the "combined" value

        if current == target:           # exact match found
            result = [left, right]      # record answer
            left += 1                   # move both to find other pairs (if needed)
            right -= 1
        elif current < target:          # need a larger sum
            left += 1                   # move left pointer rightward
        else:                           # need a smaller sum
            right -= 1                  # move right pointer leftward

    return result

Template B — Same-Direction (Fast & Slow / Read-Write)
def two_pointer_same_direction(arr):
    """
    Use when: partitioning in-place, removing elements, or detecting cycles.
    Examples: Remove Duplicates from Sorted Array (LC 26), Move Zeroes (LC 283),
              Remove Element (LC 27), Sort Colors (LC 75 — Dutch National Flag)
    """
    write = 0                           # slow pointer — next position to write

    for read in range(len(arr)):        # fast pointer — scans every element
        if SHOULD_KEEP(arr[read]):      # decide whether this element belongs
            arr[write] = arr[read]      # place it at the write position
            write += 1                  # advance write pointer

    return write                        # elements [0..write-1] are the answer

# -------------------------------------------------------
# CUSTOMIZATION POINT — replace SHOULD_KEEP:
#   LC 26: arr[read] != arr[write - 1]   → skip duplicates
#   LC 27: arr[read] != val              → skip target value
#   LC 283: arr[read] != 0              → skip zeros
# -------------------------------------------------------

Complexity: Time O(n) (single pass or converging). Space O(1).

3. ⚡ Binary Search
When to Apply

Look for: sorted array, "search in rotated sorted", "find minimum/maximum that satisfies", "kth smallest", "capacity to ship within D days". Key signal: you can eliminate half the search space each step.

Template A — Classic Binary Search (Find Exact Value)
def binary_search_exact(arr, target):
    """
    Use when: finding an exact element in a sorted array.
    Examples: Binary Search (LC 704), Search in Rotated Sorted Array (LC 33)
    """
    lo, hi = 0, len(arr) - 1            # search space: inclusive on both ends

    while lo <= hi:                      # continue while search space is non-empty
        mid = lo + (hi - lo) // 2        # avoid overflow (matters in other languages)

        if arr[mid] == target:           # found the target
            return mid
        elif arr[mid] < target:          # target is in the right half
            lo = mid + 1
        else:                            # target is in the left half
            hi = mid - 1

    return -1                            # target not found

Template B — Binary Search on Answer (Monotonic Predicate)
def binary_search_on_answer(lo, hi):
    """
    Use when: you're not searching an array but searching for the MINIMUM/MAXIMUM
    value that satisfies a condition (the predicate flips from False→True).
    Examples: Koko Eating Bananas (LC 875), Capacity to Ship (LC 1011),
              Split Array Largest Sum (LC 410), Minimum Days to Make Bouquets (LC 1482)
    
    Predicate landscape:  F F F F T T T T
    We want the first T:        ^
    """
    while lo < hi:                       # narrow down to a single value
        mid = lo + (hi - lo) // 2        # pick the middle candidate

        if IS_FEASIBLE(mid):             # can we achieve the goal with this value?
            hi = mid                     # yes → try smaller (look left)
        else:
            lo = mid + 1                 # no → must go bigger (look right)

    return lo                            # lo == hi == smallest feasible answer

# -------------------------------------------------------
# CUSTOMIZATION POINT — define IS_FEASIBLE(mid):
#   LC 875:  can Koko eat all bananas at speed=mid within H hours?
#   LC 1011: can we ship all packages with capacity=mid within D days?
#   LC 410:  can we split array into ≤ m parts each with sum ≤ mid?
# -------------------------------------------------------

Complexity: Time O(n log S) where S = search space size, n = cost of feasibility check. Space O(1).

4. 🌳 BFS (Breadth-First Search)
When to Apply

Look for: shortest path in unweighted graph/grid, "minimum number of steps", "level-order traversal", "nearest exit", "rotten oranges spreading". BFS guarantees shortest distance when all edges have equal weight.

Template A — Graph / Grid BFS
from collections import deque

def bfs(grid, start, end):
    """
    Use when: shortest path in unweighted graph/grid, or level-order processing.
    Examples: Shortest Path in Binary Matrix (LC 1091), Rotting Oranges (LC 994),
              Word Ladder (LC 127), 01 Matrix (LC 542), Open the Lock (LC 752)
    """
    rows, cols = len(grid), len(grid[0])
    queue = deque()                          # FIFO queue for BFS
    visited = set()                          # track visited cells to avoid cycles
    directions = [(0,1),(0,-1),(1,0),(-1,0)] # 4-directional movement (add diagonals if needed)

    # ---- INITIALIZATION: single-source or multi-source ----
    queue.append((*start, 0))                # (row, col, distance)
    visited.add(start)
    # For multi-source BFS (e.g., LC 994), enqueue ALL sources here with dist=0

    while queue:
        r, c, dist = queue.popleft()         # process the closest unvisited node

        if (r, c) == end:                    # reached the goal
            return dist

        for dr, dc in directions:            # explore all neighbors
            nr, nc = r + dr, c + dc          # compute neighbor coordinates

            if (0 <= nr < rows and            # within bounds
                0 <= nc < cols and
                (nr, nc) not in visited and   # not yet visited
                grid[nr][nc] != WALL):        # not blocked (customize this)

                visited.add((nr, nc))         # mark visited BEFORE enqueueing (important!)
                queue.append((nr, nc, dist + 1))

    return -1                                # goal unreachable

Template B — Level-Order BFS (Process Level by Level)
from collections import deque

def bfs_level_order(root):
    """
    Use when: you need to process nodes LEVEL BY LEVEL (tree or graph).
    Examples: Binary Tree Level Order Traversal (LC 102), Zigzag (LC 103),
              Right Side View (LC 199), Minimum Depth (LC 111), Rotting Oranges (LC 994)
    """
    if not root:
        return []

    queue = deque([root])                    # start with the root node
    result = []                              # stores per-level results

    while queue:
        level_size = len(queue)              # number of nodes at the CURRENT level
        current_level = []                   # collect values for this level

        for _ in range(level_size):          # process exactly this level's nodes
            node = queue.popleft()
            current_level.append(node.val)   # record node value

            if node.left:                    # enqueue children for NEXT level
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_level)         # store the completed level

    return result

Complexity: Time O(V + E) for graphs, O(m × n) for grids. Space O(V) or O(m × n).

5. 🔄 DFS (Depth-First Search)
When to Apply

Look for: explore all paths, "find all combinations", "number of islands", "connected components", "detect cycle", "path sum". DFS is preferred for exhaustive exploration and problems involving recursion on trees/graphs.

Template A — Grid DFS (Iterative with Stack)
def dfs_grid(grid):
    """
    Use when: counting connected components, flood fill, island problems.
    Examples: Number of Islands (LC 200), Max Area of Island (LC 695),
              Surrounded Regions (LC 130), Pacific Atlantic Water Flow (LC 417)
    """
    rows, cols = len(grid), len(grid[0])
    visited = set()                          # global visited set
    directions = [(0,1),(0,-1),(1,0),(-1,0)]
    result = 0                               # e.g., number of islands

    def dfs(r, c):
        stack = [(r, c)]                     # use explicit stack (avoids recursion limit)
        visited.add((r, c))
        area = 0                             # track component size if needed

        while stack:
            cr, cc = stack.pop()             # pop the top cell
            area += 1                        # process current cell

            for dr, dc in directions:
                nr, nc = cr + dr, cc + dc
                if (0 <= nr < rows and
                    0 <= nc < cols and
                    (nr, nc) not in visited and
                    grid[nr][nc] == TARGET):  # customize: '1' for islands, etc.
                    visited.add((nr, nc))     # mark before pushing
                    stack.append((nr, nc))

        return area

    for r in range(rows):                    # scan every cell as potential start
        for c in range(cols):
            if (r, c) not in visited and grid[r][c] == TARGET:
                dfs(r, c)                    # explore entire component
                result += 1                  # count it

    return result

Template B — Tree DFS (Recursive)
def dfs_tree(root):
    """
    Use when: tree traversal, path sum, depth, diameter, validation.
    Examples: Maximum Depth (LC 104), Path Sum (LC 112), Diameter (LC 543),
              Validate BST (LC 98), Lowest Common Ancestor (LC 236)
    """
    def helper(node):
        if not node:                         # BASE CASE: null node
            return 0                         # return identity value (0, True, float('inf'), etc.)

        left = helper(node.left)             # recurse into left subtree
        right = helper(node.right)           # recurse into right subtree

        # ---- PROCESS CURRENT NODE ----
        # Combine left and right results with current node's value
        # Example (max depth):  return 1 + max(left, right)
        # Example (path sum):   return node.val + max(left, right)
        # Example (diameter):   self.ans = max(self.ans, left + right)  ← side effect

        return COMBINE(node.val, left, right)

    return helper(root)

Complexity: Time O(V + E) for graphs, O(n) for trees. Space O(V) or O(h) for trees (h = height).

6. 🧩 Backtracking
When to Apply

Look for: "find all combinations/permutations/subsets", "generate all valid", "N-Queens", "Sudoku solver", "word search in grid", "partition into palindromes". You need to enumerate solutions by choosing → exploring → undoing.

def backtrack(nums):
    """
    Universal backtracking framework.
    Examples: Subsets (LC 78), Permutations (LC 46), Combination Sum (LC 39),
              N-Queens (LC 51), Palindrome Partitioning (LC 131),
              Word Search (LC 79), Letter Combinations (LC 17)
    """
    result = []                              # accumulate all valid solutions

    def helper(start, path):
        # ---- BASE CASE: is `path` a complete solution? ----
        if IS_COMPLETE(path):                # e.g., len(path) == len(nums) for permutations
            result.append(path[:])           # append a COPY (path is mutable)
            return                           # stop if we only want full-length solutions
                                             # (for subsets, record BEFORE the loop, not here)

        for i in range(start, len(nums)):    # iterate over remaining CHOICES

            # ---- PRUNING: skip invalid / duplicate branches ----
            if SHOULD_SKIP(i, path, nums):   # e.g., skip duplicates: i > start and nums[i] == nums[i-1]
                continue

            path.append(nums[i])             # CHOOSE: add candidate to current path

            # RECURSE with adjusted parameters:
            #   Subsets / Combinations: helper(i + 1, path)     → don't reuse
            #   Combination Sum (reuse): helper(i, path)        → allow reuse
            #   Permutations: helper(0, path) with `used` set   → any position
            helper(i + 1, path)

            path.pop()                       # UN-CHOOSE: undo the last decision (backtrack)

    nums.sort()                              # sort to enable duplicate skipping
    helper(0, [])
    return result

# -------------------------------------------------------
# CUSTOMIZATION POINTS:
#   IS_COMPLETE:
#     Subsets:       never (record at every level before the loop)
#     Permutations:  len(path) == len(nums)
#     Combo Sum:     sum(path) == target
#
#   SHOULD_SKIP:
#     Subsets II:    i > start and nums[i] == nums[i-1]
#     Permutations:  nums[i] in used_set
#     Combo Sum:     sum(path) + nums[i] > target
#
#   NEXT INDEX:
#     No reuse:  i + 1
#     With reuse: i
# -------------------------------------------------------

Complexity: Time O(2^n) for subsets, O(n!) for permutations. Space O(n) recursion depth.

7. 📊 Dynamic Programming
When to Apply

Look for: "minimum/maximum cost", "number of ways", "is it possible", "longest/shortest sequence", overlapping subproblems + optimal substructure. If a brute-force recursive solution recomputes the same states, DP is the answer.

Template A — 1D DP (Bottom-Up)
def dp_1d(nums):
    """
    Use when: state depends on previous 1 or 2 elements or a single index.
    Examples: Climbing Stairs (LC 70), House Robber (LC 198), Coin Change (LC 322),
              Longest Increasing Subsequence (LC 300), Decode Ways (LC 91)
    """
    n = len(nums)
    dp = [0] * (n + 1)                      # dp[i] = answer for the first i elements
    dp[0] = BASE_CASE_0                     # base case (empty / starting state)
    dp[1] = BASE_CASE_1                     # base case for first element (if needed)

    for i in range(2, n + 1):               # fill table from smallest subproblem up
        # ---- RECURRENCE RELATION ----
        # Example (Climbing Stairs): dp[i] = dp[i-1] + dp[i-2]
        # Example (House Robber):    dp[i] = max(dp[i-1], dp[i-2] + nums[i-1])
        # Example (Coin Change):     dp[i] = min(dp[i - coin] + 1 for coin in coins if i >= coin)
        dp[i] = RECURRENCE(dp, nums, i)

    return dp[n]                             # answer for the full input

# --- SPACE OPTIMIZATION (when dp[i] depends only on dp[i-1] and dp[i-2]) ---
def dp_1d_optimized(nums):
    prev2, prev1 = BASE_CASE_0, BASE_CASE_1  # only keep last two states
    for i in range(2, len(nums) + 1):
        curr = RECURRENCE_USING(prev1, prev2, nums[i-1])
        prev2, prev1 = prev1, curr           # shift window forward
    return prev1

Template B — 2D DP
def dp_2d(text1, text2):
    """
    Use when: two sequences/strings, grid-based, or two constraining dimensions.
    Examples: Longest Common Subsequence (LC 1143), Edit Distance (LC 72),
              Unique Paths (LC 62), Minimum Path Sum (LC 64),
              0/1 Knapsack, Interleaving String (LC 97)
    """
    m, n = len(text1), len(text2)
    # dp[i][j] = answer considering text1[0..i-1] and text2[0..j-1]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # ---- BASE CASES ----
    # Fill dp[0][j] and dp[i][0] if needed (e.g., Edit Distance initializes to i and j)

    for i in range(1, m + 1):               # iterate over first dimension
        for j in range(1, n + 1):           # iterate over second dimension

            if text1[i-1] == text2[j-1]:    # characters match (or condition met)
                dp[i][j] = dp[i-1][j-1] + 1  # extend the diagonal
            else:                            # characters don't match
                dp[i][j] = max(dp[i-1][j],   # skip from text1
                               dp[i][j-1])   # skip from text2
                # Edit Distance: min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1

    return dp[m][n]                          # answer for full inputs

Template C — Top-Down Memoization (when bottom-up is hard to formulate)
from functools import lru_cache

def dp_top_down(nums, target):
    """
    Use when: state space is complex, sparse, or hard to order bottom-up.
    Examples: Word Break (LC 139), Partition Equal Subset Sum (LC 416),
              Target Sum (LC 494), Stone Game (LC 877)
    """
    @lru_cache(maxsize=None)                 # memoize to avoid recomputation
    def helper(index, remaining):
        # ---- BASE CASES ----
        if remaining == 0:                   # goal reached
            return True                      # or 1 (counting) or 0 (cost)
        if index >= len(nums) or remaining < 0:
            return False                     # or float('inf') / 0

        # ---- RECURSIVE CHOICES ----
        take = helper(index + 1, remaining - nums[index])  # include nums[index]
        skip = helper(index + 1, remaining)                # exclude nums[index]

        return take or skip                  # combine: or / + / min / max

    return helper(0, target)

Complexity: Time O(n × S) where S = state space size. Space same or optimizable to O(S).

8. 🗂️ Monotonic Stack
When to Apply

Look for: "next greater/smaller element", "largest rectangle in histogram", "daily temperatures", "stock span", "trapping rain water". The stack maintains a monotonically increasing or decreasing order.

def monotonic_stack(arr):
    """
    Use when: for each element, find the NEXT or PREVIOUS greater/smaller element.
    Examples: Next Greater Element (LC 496/503), Daily Temperatures (LC 739),
              Largest Rectangle in Histogram (LC 84), Stock Span (LC 901),
              Trapping Rain Water (LC 42)
    """
    n = len(arr)
    result = [-1] * n                        # default: no next greater element found
    stack = []                               # stores INDICES (not values)
                                             # maintains monotonic DECREASING order of values

    for i in range(n):                       # scan left to right
        # Pop elements that are SMALLER than current (finding their "next greater")
        while stack and arr[stack[-1]] < arr[i]:  # change < to > for "next smaller"
            idx = stack.pop()                # this element's next greater is arr[i]
            result[idx] = arr[i]             # record the answer for that element

        stack.append(i)                      # push current index onto the stack

    return result

# -------------------------------------------------------
# VARIATIONS:
#   Next Greater:   pop when stack[-1] < arr[i]   (stack is decreasing)
#   Next Smaller:   pop when stack[-1] > arr[i]   (stack is increasing)
#   Previous Greater/Smaller: scan right to left, same logic
#   Circular array (LC 503): loop i from 0 to 2n-1, use i % n
# -------------------------------------------------------

Complexity: Time O(n) — each element pushed/popped at most once. Space O(n).

9. 🏔️ Heap / Priority Queue (Top-K Pattern)
When to Apply

Look for: "Kth largest/smallest", "top K frequent", "merge K sorted lists", "median from data stream", "task scheduler", "meeting rooms". You need efficient access to the extreme element.

Template A — Top-K Elements
import heapq

def top_k(nums, k):
    """
    Use when: finding k largest, k most frequent, k closest points.
    Examples: Kth Largest Element (LC 215), Top K Frequent Elements (LC 347),
              K Closest Points to Origin (LC 973), Find K Pairs with Smallest Sums (LC 373)
    """
    # MIN-HEAP of size K → top of heap is the Kth largest
    min_heap = []

    for num in nums:
        heapq.heappush(min_heap, num)        # push current element
        if len(min_heap) > k:                # if heap exceeds size k
            heapq.heappop(min_heap)          # remove the smallest (not in top-k)

    return min_heap[0]                       # top of heap = Kth largest

    # NOTE: For Kth smallest, use a MAX-HEAP (negate values):
    #   heapq.heappush(max_heap, -num)

Template B — Merge K Sorted Streams
import heapq

def merge_k_sorted(lists):
    """
    Use when: merging multiple sorted sources into one sorted output.
    Examples: Merge K Sorted Lists (LC 23), Smallest Range Covering K Lists (LC 632),
              Kth Smallest in Sorted Matrix (LC 378)
    """
    min_heap = []
    result = []

    # ---- INITIALIZATION: push the first element from each list ----
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(min_heap, (lst[0], i, 0))  # (value, list_index, element_index)

    while min_heap:
        val, list_i, elem_i = heapq.heappop(min_heap)  # smallest across all lists
        result.append(val)                               # add to merged output

        if elem_i + 1 < len(lists[list_i]):             # if this list has more elements
            next_val = lists[list_i][elem_i + 1]
            heapq.heappush(min_heap, (next_val, list_i, elem_i + 1))  # push the next one

    return result

Complexity: Top-K: Time O(n log k), Space O(k). Merge-K: Time O(N log k) where N = total elements, Space O(k).

10. 🔗 Linked List
When to Apply

Look for: "reverse linked list", "detect cycle", "merge two lists", "remove nth from end", "find middle", "reorder list". Pointer manipulation on singly/doubly linked nodes.

Template A — Fast & Slow Pointers (Floyd's)
def linked_list_cycle(head):
    """
    Use when: detecting cycles, finding the cycle start, finding the middle node.
    Examples: Linked List Cycle (LC 141), Linked List Cycle II (LC 142),
              Middle of Linked List (LC 876), Happy Number (LC 202)
    """
    slow = fast = head                       # both start at head

    while fast and fast.next:                # fast moves 2x speed
        slow = slow.next                     # slow moves one step
        fast = fast.next.next                # fast moves two steps

        if slow == fast:                     # cycle detected!
            # To find cycle START: reset one pointer to head, then both move at speed 1
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow                      # meeting point = cycle start

    return None                              # no cycle; slow is at MIDDLE if needed

Template B — Reverse a Linked List (Iterative)
def reverse_linked_list(head):
    """
    Use when: reversing entire list or a portion of it.
    Examples: Reverse Linked List (LC 206), Reverse Linked List II (LC 92),
              Reverse Nodes in K-Group (LC 25), Palindrome Linked List (LC 234)
    """
    prev = None                              # previous node (will become new head)
    curr = head                              # current node being processed

    while curr:                              # traverse the entire list
        nxt = curr.next                      # save next node before overwriting
        curr.next = prev                     # reverse the pointer
        prev = curr                          # advance prev
        curr = nxt                           # advance curr

    return prev                              # prev is the new head

Template C — Dummy Head (Merge / Partition / Build)
def merge_two_sorted(l1, l2):
    """
    Use when: building a new list by stitching together existing nodes.
    Examples: Merge Two Sorted Lists (LC 21), Partition List (LC 86),
              Add Two Numbers (LC 2), Sort List (LC 148)
    """
    dummy = ListNode(0)                      # dummy head avoids edge cases with empty lists
    tail = dummy                             # tail always points to the last node of result

    while l1 and l2:                         # while both lists have nodes
        if l1.val <= l2.val:                 # pick the smaller node
            tail.next = l1                   # attach it to the result
            l1 = l1.next                     # advance that list
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next                     # advance the result tail

    tail.next = l1 or l2                     # attach the remaining nodes

    return dummy.next                        # skip the dummy; return real head

Complexity: All templates: Time O(n), Space O(1).

11. 🌲 Trie (Prefix Tree)
When to Apply

Look for: "prefix search", "autocomplete", "word dictionary with wildcards", "word search II", "longest common prefix", "add and search words". You're dealing with a collection of strings with shared prefixes.

class TrieNode:
    def __init__(self):
        self.children = {}                   # char → TrieNode mapping
        self.is_end = False                  # marks the end of a complete word
        # self.word = None                   # optionally store the full word here (useful for LC 212)

class Trie:
    """
    Universal Trie supporting insert, search, startsWith, and wildcard search.
    Examples: Implement Trie (LC 208), Add and Search Word (LC 211),
              Word Search II (LC 212), Replace Words (LC 648),
              Longest Word in Dictionary (LC 720)
    """
    def __init__(self):
        self.root = TrieNode()               # root represents empty prefix

    def insert(self, word):
        node = self.root                     # start from root
        for ch in word:                      # process each character
            if ch not in node.children:      # create node if path doesn't exist
                node.children[ch] = TrieNode()
            node = node.children[ch]         # move to child
        node.is_end = True                   # mark word boundary

    def search(self, word):
        node = self._traverse(word)          # follow the path
        return node is not None and node.is_end  # must exist AND be a complete word

    def starts_with(self, prefix):
        return self._traverse(prefix) is not None  # just needs to exist as a path

    def _traverse(self, text):
        node = self.root
        for ch in text:
            if ch not in node.children:      # path doesn't exist
                return None
            node = node.children[ch]
        return node                          # return the final node

    # ---- WILDCARD SEARCH (LC 211) ----
    def search_with_wildcard(self, word):
        def dfs(index, node):
            if index == len(word):           # reached end of pattern
                return node.is_end

            ch = word[index]
            if ch == '.':                    # wildcard: try ALL children
                return any(dfs(index + 1, child) for child in node.children.values())
            else:
                if ch not in node.children:
                    return False
                return dfs(index + 1, node.children[ch])

        return dfs(0, self.root)

Complexity: Insert/Search: Time O(L) per word (L = word length). Space O(N × L) total for N words.

12. 🔀 Union-Find (Disjoint Set Union)
When to Apply

Look for: "connected components", "are two nodes connected", "redundant connection", "accounts merge", "number of provinces", "earliest time all connected". Dynamic connectivity queries.

class UnionFind:
    """
    Universal Union-Find with path compression + union by rank.
    Examples: Number of Provinces (LC 547), Redundant Connection (LC 684),
              Accounts Merge (LC 721), Number of Connected Components (LC 323),
              Graph Valid Tree (LC 261), Earliest Moment Friends (LC 1101)
    """
    def __init__(self, n):
        self.parent = list(range(n))         # each node is its own parent initially
        self.rank = [0] * n                  # rank (tree height) for union by rank
        self.components = n                  # total number of connected components

    def find(self, x):
        if self.parent[x] != x:             # if x is not the root
            self.parent[x] = self.find(self.parent[x])  # PATH COMPRESSION: flatten tree
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)  # find roots of both elements

        if rx == ry:                         # already in the same component
            return False                     # useful for cycle detection (return False = redundant edge)

        # UNION BY RANK: attach smaller tree under larger tree
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx                  # ensure rx has higher rank
        self.parent[ry] = rx                 # make rx the root of ry
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1               # increase rank only when equal

        self.components -= 1                 # one fewer component
        return True                          # union was successful

    def connected(self, x, y):
        return self.find(x) == self.find(y)  # same root = same component

# ---- USAGE PATTERN ----
# uf = UnionFind(n)
# for u, v in edges:
#     if not uf.union(u, v):               # if union returns False → cycle / redundant edge
#         return [u, v]
# return uf.components                      # number of connected components

Complexity: Time O(α(n)) ≈ O(1) per operation (amortized). Space O(n).

13. 📈 Prefix Sum
When to Apply

Look for: "subarray sum equals K", "range sum query", "count subarrays with sum", "pivot index", "product except self". You need to quickly compute sums over arbitrary ranges.

def prefix_sum_subarray_count(nums, k):
    """
    Use when: counting subarrays with a given sum, or any subarray sum query.
    Examples: Subarray Sum Equals K (LC 560), Continuous Subarray Sum (LC 523),
              Path Sum III (LC 437), Find Pivot Index (LC 724),
              Product of Array Except Self (LC 238), Range Sum Query (LC 303)
    """
    from collections import defaultdict
    prefix_count = defaultdict(int)          # maps prefix_sum → how many times it's occurred
    prefix_count[0] = 1                      # empty prefix has sum 0 (important base case!)
    current_sum = 0                          # running prefix sum
    result = 0                               # count of valid subarrays

    for num in nums:
        current_sum += num                   # extend prefix sum by current element

        # If (current_sum - k) was seen before, those positions are valid subarray starts
        # Because: prefix[j] - prefix[i] = k  →  subarray (i, j] has sum k
        result += prefix_count[current_sum - k]

        prefix_count[current_sum] += 1       # record this prefix sum

    return result

# -------------------------------------------------------
# VARIATION — Range Sum Query (precompute, then O(1) per query):
# prefix = [0] * (n + 1)
# for i in range(n):
#     prefix[i+1] = prefix[i] + nums[i]
# range_sum(l, r) = prefix[r+1] - prefix[l]
# -------------------------------------------------------

Complexity: Time O(n). Space O(n).

14. 🧮 Topological Sort
When to Apply

Look for: "course prerequisites", "task scheduling with dependencies", "build order", "detect cycle in directed graph", "alien dictionary". DAG + ordering constraints.

from collections import deque, defaultdict

def topological_sort(num_nodes, prerequisites):
    """
    Kahn's Algorithm (BFS-based topological sort).
    Use when: ordering tasks with dependencies, detecting cycles in directed graphs.
    Examples: Course Schedule (LC 207), Course Schedule II (LC 210),
              Alien Dictionary (LC 269), Parallel Courses (LC 1136),
              Minimum Height Trees (LC 310 — uses similar degree logic)
    """
    graph = defaultdict(list)                # adjacency list: prerequisite → dependent courses
    in_degree = [0] * num_nodes              # count of incoming edges for each node

    # ---- BUILD THE GRAPH ----
    for dest, src in prerequisites:          # src must come before dest
        graph[src].append(dest)              # directed edge: src → dest
        in_degree[dest] += 1                 # dest has one more prerequisite

    # ---- INITIALIZE: enqueue all nodes with no prerequisites ----
    queue = deque()
    for node in range(num_nodes):
        if in_degree[node] == 0:             # no incoming edges = ready to process
            queue.append(node)

    order = []                               # stores the topological ordering

    while queue:
        node = queue.popleft()               # process a "ready" node
        order.append(node)                   # add to the topological order

        for neighbor in graph[node]:         # for each dependent node
            in_degree[neighbor] -= 1         # one fewer prerequisite remaining
            if in_degree[neighbor] == 0:     # all prerequisites met
                queue.append(neighbor)       # it's now ready to process

    if len(order) == num_nodes:              # all nodes processed = valid DAG
        return order
    else:
        return []                            # CYCLE DETECTED — topological sort impossible

Complexity: Time O(V + E). Space O(V + E).

15. 💰 Greedy (Interval Problems)
When to Apply

Look for: "merge intervals", "minimum meeting rooms", "non-overlapping intervals", "insert interval", "minimum arrows to burst balloons". Problems involving intervals with start/end times.

Template A — Merge Intervals
def merge_intervals(intervals):
    """
    Use when: merging overlapping intervals.
    Examples: Merge Intervals (LC 56), Insert Interval (LC 57)
    """
    intervals.sort(key=lambda x: x[0])      # sort by start time
    merged = [intervals[0]]                  # initialize with the first interval

    for start, end in intervals[1:]:         # scan remaining intervals
        if start <= merged[-1][1]:           # overlaps with the last merged interval
            merged[-1][1] = max(merged[-1][1], end)  # extend the end time
        else:
            merged.append([start, end])      # no overlap → start a new interval

    return merged

Template B — Interval Scheduling (Maximum Non-Overlapping)
def interval_scheduling(intervals):
    """
    Use when: maximize non-overlapping intervals, or minimize removals.
    Examples: Non-overlapping Intervals (LC 435), Minimum Arrows (LC 452),
              Meeting Rooms (LC 252), Activity Selection
    """
    intervals.sort(key=lambda x: x[1])       # sort by END time (greedy choice!)
    count = 0                                # number of selected intervals
    last_end = float('-inf')                 # end time of the last selected interval

    for start, end in intervals:
        if start >= last_end:                # no overlap with the last selected
            count += 1                       # select this interval
            last_end = end                   # update the boundary

    return count                             # max non-overlapping intervals
    # For "min removals" (LC 435): return len(intervals) - count

Template C — Meeting Rooms / Sweep Line
import heapq

def min_meeting_rooms(intervals):
    """
    Use when: finding maximum concurrent events / minimum resources needed.
    Examples: Meeting Rooms II (LC 253), Car Pooling (LC 1094),
              My Calendar (LC 729/731), Corporate Flight Bookings (LC 1109)
    """
    intervals.sort(key=lambda x: x[0])       # sort by start time
    heap = []                                # min-heap of end times (ongoing meetings)

    for start, end in intervals:
        if heap and heap[0] <= start:        # earliest ending meeting finishes before this starts
            heapq.heappop(heap)              # that room is freed up → reuse it

        heapq.heappush(heap, end)            # allocate a room for this meeting

    return len(heap)                         # heap size = peak concurrent meetings

Complexity: All templates: Time O(n log n) (dominated by sort). Space O(n).

16. 📊 Bit Manipulation
When to Apply

Look for: "single number", "power of two", "count bits", "subsets using bitmask", "XOR tricks". Operating at the binary digit level.

def bit_manipulation_patterns(nums):
    """
    Universal bit manipulation toolkit.
    Examples: Single Number (LC 136), Number of 1 Bits (LC 191),
              Counting Bits (LC 338), Power of Two (LC 231),
              Missing Number (LC 268), Reverse Bits (LC 190)
    """

    # ---- PATTERN 1: XOR to find the unique element ----
    # XOR of a number with itself = 0; XOR with 0 = itself
    # So XOR-ing all numbers cancels out duplicates, leaving the single one
    result = 0
    for num in nums:
        result ^= num                        # duplicates cancel; unique remains
    return result
    # Works for: LC 136 (single number), LC 268 (missing number: XOR indices too)

    # ---- PATTERN 2: Check power of two ----
    # Powers of 2 have exactly one bit set: n & (n-1) == 0
    def is_power_of_two(n):
        return n > 0 and (n & (n - 1)) == 0

    # ---- PATTERN 3: Count set bits (Brian Kernighan's) ----
    def count_bits(n):
        count = 0
        while n:
            n &= (n - 1)                    # clear the lowest set bit
            count += 1
        return count

    # ---- PATTERN 4: Get / Set / Clear a specific bit ----
    def get_bit(n, i):   return (n >> i) & 1       # extract bit at position i
    def set_bit(n, i):   return n | (1 << i)       # set bit at position i to 1
    def clear_bit(n, i): return n & ~(1 << i)      # set bit at position i to 0

    # ---- PATTERN 5: Iterate all subsets of a bitmask ----
    def subsets_bitmask(nums):
        n = len(nums)
        result = []
        for mask in range(1 << n):           # 2^n possible subsets
            subset = []
            for i in range(n):
                if mask & (1 << i):          # if bit i is set, include nums[i]
                    subset.append(nums[i])
            result.append(subset)
        return result

Complexity: XOR/Power: O(n) / O(1). Count bits: O(k) where k = set bits. Subsets: O(2^n × n).

17. 🔄 Graph — Dijkstra's (Weighted Shortest Path)
When to Apply

Look for: "shortest path with weighted edges", "minimum cost to reach", "network delay time", "cheapest flights". Edges have non-negative weights (use Bellman-Ford for negative weights).

import heapq
from collections import defaultdict

def dijkstra(n, edges, src, dst):
    """
    Use when: shortest path in weighted graph with non-negative edges.
    Examples: Network Delay Time (LC 743), Path with Minimum Effort (LC 1631),
              Cheapest Flights Within K Stops (LC 787 — modified),
              Swim in Rising Water (LC 778), Path with Maximum Probability (LC 1514)
    """
    graph = defaultdict(list)                # adjacency list with weights
    for u, v, w in edges:
        graph[u].append((v, w))              # directed edge u → v with weight w
        # graph[v].append((u, w))            # uncomment for undirected graph

    dist = [float('inf')] * n               # shortest distance from src to each node
    dist[src] = 0                            # distance to source is 0
    min_heap = [(0, src)]                    # (distance, node) — min-heap by distance

    while min_heap:
        d, u = heapq.heappop(min_heap)       # get the unvisited node with smallest distance

        if d > dist[u]:                      # stale entry (already found a shorter path)
            continue                         # skip it — this replaces a "visited" set

        if u == dst:                         # early termination if we only need one destination
            return d

        for v, w in graph[u]:                # explore all neighbors
            new_dist = d + w                 # candidate distance through u
            if new_dist < dist[v]:           # found a shorter path to v
                dist[v] = new_dist           # update shortest distance
                heapq.heappush(min_heap, (new_dist, v))  # enqueue with new distance

    return dist[dst] if dist[dst] != float('inf') else -1  # or return dist for all nodes

Complexity: Time O((V + E) log V) with binary heap. Space O(V + E).

18. 🪟 Deque / Monotonic Deque
When to Apply

Look for: "sliding window maximum/minimum", "max of all subarrays of size k", "shortest subarray with sum ≥ k (with negatives)". You need the extreme value in a sliding window in O(1).

from collections import deque

def sliding_window_maximum(nums, k):
    """
    Use when: finding max/min in every window of size k efficiently.
    Examples: Sliding Window Maximum (LC 239),
              Shortest Subarray with Sum at Least K (LC 862),
              Jump Game VI (LC 1696), Longest Continuous Subarray (LC 1438)
    """
    dq = deque()                             # stores INDICES; front = index of current max
    result = []

    for i in range(len(nums)):
        # ---- REMOVE elements that fell out of the window ----
        while dq and dq[0] < i - k + 1:     # front is outside window [i-k+1, i]
            dq.popleft()

        # ---- MAINTAIN monotonic DECREASING order ----
        while dq and nums[dq[-1]] <= nums[i]:  # remove smaller elements from back
            dq.pop()                         # they'll never be the max while nums[i] exists

        dq.append(i)                         # add current index to back

        # ---- RECORD result once window is fully formed ----
        if i >= k - 1:                       # window has k elements
            result.append(nums[dq[0]])       # front of deque = max of current window

    return result

# For sliding window MINIMUM: change <= to >= in the inner while condition

Complexity: Time O(n) — each element enters/exits deque at most once. Space O(k).

19. 🔢 Math Patterns
When to Apply

Look for: "GCD/LCM", "prime numbers", "factorial", "modular arithmetic", "fast exponentiation". Pure mathematical computation.

# ---- PATTERN 1: GCD and LCM ----
import math
def gcd(a, b): return math.gcd(a, b)                     # built-in (or Euclidean)
def lcm(a, b): return a * b // math.gcd(a, b)            # LCM formula

# ---- PATTERN 2: Sieve of Eratosthenes ----
def sieve(n):
    """Find all primes up to n. Example: Count Primes (LC 204)"""
    is_prime = [True] * (n + 1)              # assume all are prime
    is_prime[0] = is_prime[1] = False        # 0 and 1 are not prime

    for i in range(2, int(n**0.5) + 1):      # only check up to √n
        if is_prime[i]:                      # i is prime
            for j in range(i*i, n + 1, i):   # mark all multiples starting from i²
                is_prime[j] = False

    return [i for i in range(n + 1) if is_prime[i]]  # collect primes

# ---- PATTERN 3: Fast Modular Exponentiation ----
def power_mod(base, exp, mod):
    """Compute (base^exp) % mod efficiently. Example: Super Pow (LC 372)"""
    result = 1
    base %= mod                              # handle base > mod
    while exp > 0:
        if exp & 1:                          # if current bit is set
            result = result * base % mod     # multiply into result
        exp >>= 1                            # shift exponent right (divide by 2)
        base = base * base % mod             # square the base
    return result

# ---- PATTERN 4: Integer to digits / Digit manipulation ----
def reverse_integer(x):
    """LC 7: Reverse Integer"""
    sign = -1 if x < 0 else 1
    x = abs(x)
    rev = 0
    while x:
        rev = rev * 10 + x % 10             # extract last digit and append
        x //= 10                            # remove last digit
    result = sign * rev
    return result if -2**31 <= result < 2**31 else 0  # overflow check


20. 🗃️ Design / Data Structure Problems
When to Apply

Look for: "design a data structure", "implement LRU cache", "min stack", "design HashMap". Build a class with specific time-complexity guarantees.

Template — LRU Cache (combines HashMap + Doubly Linked List)
from collections import OrderedDict

class LRUCache:
    """
    Least Recently Used Cache — O(1) get and put.
    Examples: LRU Cache (LC 146), LFU Cache (LC 460 — extend with freq map)
    """
    def __init__(self, capacity: int):
        self.cache = OrderedDict()           # maintains insertion order; acts as HashMap + DLL
        self.capacity = capacity             # maximum number of entries

    def get(self, key: int) -> int:
        if key not in self.cache:            # cache miss
            return -1
        self.cache.move_to_end(key)          # mark as recently used (move to back)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)      # update position to most recent
        self.cache[key] = value              # insert or update value

        if len(self.cache) > self.capacity:  # over capacity
            self.cache.popitem(last=False)   # evict LEAST recently used (front of order)

Template — Min Stack
class MinStack:
    """
    Stack supporting push, pop, top, and getMin — all in O(1).
    Example: Min Stack (LC 155)
    """
    def __init__(self):
        self.stack = []                      # (value, current_minimum) pairs

    def push(self, val: int) -> None:
        current_min = min(val, self.stack[-1][1] if self.stack else val)
        self.stack.append((val, current_min)) # store value alongside the running min

    def pop(self) -> None:
        self.stack.pop()                     # removes both value and its min snapshot

    def top(self) -> int:
        return self.stack[-1][0]             # the value

    def getMin(self) -> int:
        return self.stack[-1][1]             # the tracked minimum

Complexity: LRU Cache: O(1) per operation, O(capacity) space. Min Stack: O(1) per operation, O(n) space.

🗺️ Quick Reference — Pattern Recognition Cheat Sheet


|**Signal in Problem**|**Template**|
|---|---|
|Contiguous subarray/substring, optimal range|Sliding Window|
|Sorted array + pair/target|Two Pointers|
|Sorted / search space halving / min-max feasibility|Binary Search|
|Shortest path (unweighted), level-by-level|BFS|
|Explore all paths, connected components, trees|DFS|
|"All" combinations / permutations / subsets|Backtracking|
|Min/max cost, number of ways, overlapping subproblems|Dynamic Programming|
|Next greater/smaller element|Monotonic Stack|
|Top-K, merge K sorted, median stream|Heap|
|Reverse, cycle, merge linked lists|Linked List|
|Prefix matching, word dictionary|Trie|
|Dynamic connectivity, redundant edges|Union-Find|
|Subarray sum = K, range queries|Prefix Sum|
|Task ordering, prerequisites, DAG|Topological Sort|
|Overlapping intervals, meeting rooms|Greedy (Intervals)|
|XOR tricks, bitmask subsets, powers of 2|Bit Manipulation|
|Weighted shortest path|Dijkstra|
|Sliding window max/min in O(1)|Monotonic Deque|
|Custom data structure with O(1) guarantees|Design|



Each template is designed so that the structure stays identical — you only swap out the clearly marked customization points (capitalized placeholders like WINDOW_IS_INVALID, IS_FEASIBLE, SHOULD_KEEP, COMBINE, etc.) to solve a different problem within the same family.