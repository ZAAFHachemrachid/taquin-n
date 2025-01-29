# Solvers Implementation Documentation

This document provides a detailed explanation of the solver implementations in
the `solvers/` directory.

## Overview

The solvers package implements three different search algorithms for solving the
taquin (sliding puzzle) problem:

- A* Search (astar.py)
- Breadth-First Search (bfs.py)
- Depth-First Search (dfs.py)

All solvers inherit from a common base class (`Solver`) defined in solver.py.

## Common Features

Each solver implementation shares these common features:

- State representation using a `State` dataclass
- Manhattan distance heuristic calculation
- Colored debug output
- Move evaluation and validation
- Path tracking
- Goal state checking

## solver.py

The base `Solver` class provides the framework for puzzle solvers:

```python
class Solver(ABC):
    def __init__(self, initial_board)
    @abstractmethod
    def solve(self, optimal_length: Optional[int] = None) -> Optional[SolutionInfo]
```

The `SolutionInfo` class stores information about found solutions:

- List of moves taken
- Optional optimal solution length for comparison

## astar.py - A* Search Implementation

The A* search algorithm combines the best of breadth-first and depth-first
approaches using a heuristic function.

Key features:

- Uses priority queue for frontier management
- f_cost = g_cost + h_cost
  - g_cost: Actual cost from start to current node
  - h_cost: Estimated cost (Manhattan distance) to goal
- Prefers deeper nodes when f-costs are equal
- Implements best-first node expansion

Example state evaluation:

```python
def f_cost(self) -> int:
    return self.g_cost + self.h_cost  # Total estimated cost
```

## bfs.py - Breadth-First Search Implementation

BFS explores the search space level by level, guaranteeing the optimal solution.

Key features:

- Uses queue (FIFO) for frontier management
- Tracks search level/depth
- Implements level-order traversal
- Maximum depth limit to prevent excessive memory usage

Level tracking example:

```python
while queue:
    current_state, level = queue.popleft()
    if level > current_level:
        print(ColoredText.blue("\nMoving to next level..."))
        current_level = level
```

## dfs.py - Depth-First Search Implementation

DFS explores as far as possible along each branch before backtracking.

Key features:

- Uses stack (LIFO) for frontier management
- Tracks search depth
- Implements depth-first node expansion
- Maximum depth limit to prevent infinite recursion
- Reverse ordering of successors for consistent exploration

Depth management example:

```python
if len(current_state.path) >= self.max_depth:
    print(ColoredText.yellow("\nMax depth reached at this branch..."))
    continue
```

## Performance Comparison

1. A* Search (astar.py):
   - Best overall performance for finding optimal solutions
   - Uses heuristic to guide search
   - Memory usage scales with problem size

2. BFS (bfs.py):
   - Guarantees optimal solution
   - Complete for finite search spaces
   - High memory usage (stores all nodes at current level)

3. DFS (dfs.py):
   - Memory efficient (stores only current path)
   - May not find optimal solution
   - Can get stuck in deep branches

## Debug Features

All solvers include comprehensive debugging features:

- Colored console output
- Move quality evaluation (BEST/MID/BAD)
- State visualization
- Search progress tracking
- Node expansion visualization
