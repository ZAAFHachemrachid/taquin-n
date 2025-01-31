# Sliding Puzzle Solvers Documentation

This document describes the implementation of different solving algorithms for
the sliding puzzle game.

## Base Classes

### `Solver` (Abstract Base Class)

Base class for all puzzle solvers located in `solvers/solver.py`.

#### Methods

- `__init__(initial_board)` - Initialize solver with starting board state
- `get_inversions() -> int` - Count inversions in board state to check
  solvability
- `is_solvable() -> bool` - Determine if puzzle is solvable from current state
- `solve(optimal_length: Optional[int]) -> Optional[SolutionInfo]` - Abstract
  method to find solution

### `SolutionInfo`

Data class storing information about a found solution.

#### Attributes

- `status: SolutionStatus` - Current solution status (SOLVED, ALREADY_SOLVED,
  UNSOLVABLE, NO_SOLUTION)
- `moves: Optional[List[Direction]]` - List of moves to reach solution
- `optimal_length: Optional[int]` - Known optimal solution length for validation

## Solver Implementations

### DFS Solver (`DFSSolver`)

Located in `solvers/dfs.py`, implements iterative deepening DFS with
optimizations.

#### Features

- Iterative deepening to find shortest solutions first
- Move ordering prioritizing UP and LEFT moves
- Cycle detection to avoid revisiting states
- Reverse move prevention
- Path state tracking

#### Key Methods

- `get_ordered_moves(state)` - Returns moves in optimized order (UP, LEFT, DOWN,
  RIGHT)
- `is_reverse_move(last_move, new_move)` - Checks if a move undoes the previous
  move
- `dfs_with_depth_limit()` - Core DFS algorithm with depth limiting
- `solve()` - Main solving method implementing iterative deepening

### BFS Solver (`BFSSolver`)

Located in `solvers/bfs.py`, implements level-order search.

#### Features

- Guaranteed to find shortest solution
- Level-by-level exploration
- Complete state tracking

#### Key Methods

- Uses queue-based implementation
- Tracks levels explicitly for visualization
- Similar debug output to DFS

### A* Solver (`AStarSolver`)

Located in `solvers/astar.py`, implements A* search with Manhattan distance
heuristic.

#### Features

- Heuristic-guided search
- Priority queue based on f-cost (g + h)
- Optimized for finding shortest paths

#### Key Methods

- Priority queue based exploration
- Maintains g-cost (actual) and h-cost (heuristic)
- Similar debugging capabilities to other solvers

## Common Components

### `State` Class

Represents a puzzle state, common to all solvers.

#### Attributes

- `state: List[int]` - Current board configuration
- `blank_pos: int` - Position of blank tile
- `size: int` - Board size (e.g., 3 for 3x3)
- `path: List[Direction]` - Moves taken to reach this state

#### Methods

- `from_board(board)` - Create state from Board object
- `manhattan_distance()` - Calculate heuristic value
- `is_goal()` - Check if state is solved
- `get_possible_moves()` - Get valid moves
- `make_move(direction)` - Apply move to create new state
- `display()` - Create string representation of board

### Utilities

#### `Direction` Enum

Possible move directions:

- `UP`
- `DOWN`
- `LEFT`
- `RIGHT`

#### `ColoredText`

Terminal color formatting for debug output:

- `GREEN` - Success messages
- `RED` - Error/unsolvable messages
- `YELLOW` - Warnings
- `BLUE` - Progress updates
- `CYAN` - Board visualization

#### `Config`

Global configuration settings:

```python
ITERATION_DELAY = 1.0  # Delay between steps
MAX_DEPTH_DFS = 30    # Maximum DFS depth
MAX_DEPTH_BFS = 30    # Maximum BFS depth
```

## Usage Example

```python
from common.board import Board
from solvers.dfs import DFSSolver

# Create initial board state
board = Board(initial_state)

# Initialize solver
solver = DFSSolver(board)

# Find solution
solution = solver.solve()

if solution:
    if solution.status == SolutionStatus.SOLVED:
        print(f"Solution found in {len(solution.moves)} moves")
        print(f"Moves: {', '.join(move.name for move in solution.moves)}")
    else:
        print(solution)  # Prints status message
```
