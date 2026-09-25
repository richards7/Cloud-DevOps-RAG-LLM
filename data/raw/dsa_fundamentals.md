# Data Structures & Algorithms — Fundamentals

## Core data structures
- **Array**: fixed or dynamic-size sequential collection, O(1) index access, O(n)
  insertion/deletion in the middle.
- **Linked List**: nodes linked via pointers, O(1) insertion/deletion at a known
  position, O(n) access (no random indexing).
- **Stack**: LIFO (last in, first out) — push/pop. Use case: undo functionality,
  function call stacks, balanced-parentheses checking.
- **Queue**: FIFO (first in, first out) — enqueue/dequeue. Use case: task scheduling,
  BFS traversal, message queues (conceptually related to SQS/Kafka).
- **Hash Map/Dictionary**: key-value store, average O(1) lookup/insert via hashing.
  Use case: caching, counting frequencies, fast lookups by ID.
- **Tree**: hierarchical structure (each node has children). Binary Search Tree keeps
  left < node < right for O(log n) average search.
- **Graph**: nodes (vertices) connected by edges — models networks, dependencies,
  relationships. Directed vs undirected; weighted vs unweighted.

## Big-O complexity (how you talk about performance)
- **O(1)**: constant — doesn't grow with input size (e.g. hash map lookup).
- **O(log n)**: logarithmic — grows slowly (e.g. binary search).
- **O(n)**: linear — grows proportionally (e.g. a single loop through a list).
- **O(n log n)**: typical of efficient sorting algorithms (merge sort, quicksort avg).
- **O(n²)**: quadratic — nested loops over the same data (e.g. bubble sort).

## Common algorithms
- **Binary search**: find a value in a SORTED array in O(log n) by repeatedly halving
  the search range.
```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```
- **BFS (Breadth-First Search)**: explores a graph/tree level by level, using a queue
  — finds the shortest path in an unweighted graph.
- **DFS (Depth-First Search)**: explores as far as possible down one branch before
  backtracking, using a stack (or recursion) — used for cycle detection, topological
  sort, exploring all paths.
- **Two-pointer technique**: use two indices moving through a sequence (often from
  opposite ends) to solve problems in O(n) that naively look O(n²) — common in
  array/string problems.

## Common patterns in easy-medium interview problems
```python
# Frequency counting (Counter is the Pythonic way)
from collections import Counter
counts = Counter("hello")   # {'l': 2, 'h': 1, 'e': 1, 'o': 1}

# Two-sum (hash map for O(n) instead of O(n^2) nested loop)
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Reversing a string/list
s = "hello"
reversed_s = s[::-1]
```

## Why this comes up in DevOps/Cloud interviews
Even in infrastructure-heavy roles, basic DSA questions test general problem-solving
ability and code fluency — expect easy-to-medium array/string/hash map questions
rather than deep graph theory, unless the role is more software-engineering focused.

## Common errors & fixes (when solving DSA problems)
- **Off-by-one errors in loops/binary search**: carefully check boundary conditions
  (`<` vs `<=`), especially in binary search's `lo`/`hi` updates.
- **Modifying a list while iterating over it**: causes skipped elements or runtime
  errors — iterate over a copy (`for x in list[:]`) or build a new list instead.
- **Using a list where a set/dict would give O(1) lookup**: if you're checking
  "does X exist in this collection?" repeatedly, a list gives O(n) per check — use a
  set/dict for O(1).
- **Stack overflow from deep recursion**: Python's default recursion limit is ~1000 —
  convert to an iterative approach with an explicit stack for very deep recursion.
