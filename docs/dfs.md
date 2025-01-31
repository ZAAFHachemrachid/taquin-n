# Depth-First Search Solver Documentation

## Overview

The DFS solver implements an iterative deepening depth-first search algorithm
with several optimizations to solve the sliding puzzle efficiently.

## Implementation Details

### Class Structure

```python
class DFSSolver(Solver):
    """Depth-First Search solver implementation."""
    def __init__(self, initial_board: Board):
        super().__init__(initial_board)
        self.max_depth = Config.MAX_DEPTH_DFS  # Set to 30
```

### Key Features

#### 1. Iterative Deepening

- Gradually increases search depth from 1 to MAX_DEPTH_DFS
- Resets visited states at each depth to ensure complete search
- Helps find shorter solutions first

```python
for depth_limit in range(1, self.max_depth + 1):
    visited = set()  # Fresh start at each depth
    current_path = {tuple(initial_state.state)}
```

#### 2. Move Ordering

```python
def get_ordered_moves(self, state: State) -> List[Direction]:
    """Get list of possible moves in a fixed priority order."""
    priority = [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT]
    possible = state.get_possible_moves()
    return [move for move in priority if move in possible]
```

- Prioritizes UP and LEFT moves
- Helps find natural solutions (tends to move blank space up and left first)
- Fixed ordering to avoid comparison issues

#### 3. Cycle Detection

```python
def is_reverse_move(self, last_move: Optional[Direction], new_move: Direction) -> bool:
    """Check if a move reverses the previous move."""
    if last_move is None:
        return False
    return (
        (last_move == Direction.UP and new_move == Direction.DOWN)
        or (last_move == Direction.DOWN and new_move == Direction.UP)
        or (last_move == Direction.LEFT and new_move == Direction.RIGHT)
        or (last_move == Direction.RIGHT and new_move == Direction.LEFT)
    )
```

- Prevents immediate reversals of moves
- Tracks path states to avoid cycles
- Uses both global and path-specific state tracking

#### 4. State Management

Two levels of state tracking:

1. `current_path`: Set of states in current search path
   - Prevents cycles in current branch
   - Reset for each depth-limited search
2. `visited`: Set of all explored states
   - Reset for each depth iteration
   - Prevents redundant exploration

### Core Search Algorithm

```python
def dfs_with_depth_limit(
    self,
    state: State,
    visited: Set[Tuple[int, ...]],
    current_path: Set[Tuple[int, ...]],
    depth_limit: int,
    nodes_visited: int,
) -> Tuple[Optional[State], int]:
    """DFS with depth limit, cycle detection, and state tracking."""
```

Key steps:

1. Check for goal state
2. Check depth limit
3. Get possible moves in optimized order
4. Filter out reverse moves and visited states
5. Recursively explore valid moves
6. Track and backtrack states in current path

### Early Termination Conditions

1. Goal state reached
2. Already solved state
3. Unsolvable configuration
4. Maximum depth reached
5. All moves exhausted

### Debug Output

```python
@with_delay
def debug_print(self, current: State, moves: List[Tuple], visited: Set, depth: int):
    """Print debug information about current search state."""
```

Features:

- Current depth level
- Board visualization
- Available moves
- Move selection indicators
- Visited state count

### Solution Status Tracking

Returns `SolutionInfo` with:

- Status (SOLVED, ALREADY_SOLVED, UNSOLVABLE, NO_SOLUTION)
- Move sequence if solution found
- Optional optimal length information

## Usage Example

```python
from common.board import Board
from solvers.dfs import DFSSolver

# Create puzzle with initial state
board = Board([
    [1, 2, 3],
    [4, 0, 6],  # 0 represents blank space
    [7, 5, 8]
])

# Initialize DFS solver
solver = DFSSolver(board)

# Find solution
result = solver.solve()

if result:
    if result.status == SolutionStatus.SOLVED:
        print(f"Solution found in {len(result.moves)} moves:")
        print(f"Moves: {', '.join(move.name for move in result.moves)}")
    else:
        print(f"Status: {result.status.value}")
```

## Configuration

Located in `common/utils.py`:

```python
class Config:
    ITERATION_DELAY = 1.0  # Visualization delay
    MAX_DEPTH_DFS = 30    # Maximum search depth
```

## Key Improvements

Recent enhancements:

1. Unsolvable state detection using inversion count
2. Already-solved state quick check
3. Enhanced move ordering for efficiency
4. Reset visited states per depth iteration
5. Better path cycle detection
