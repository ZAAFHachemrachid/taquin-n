# Project Overview Documentation

This document provides an overview of the taquin-n project, explaining the root
level files and overall project structure.

## Project Structure

```
taquin-n/
├── __init__.py           # Package initialization
├── main.py              # Main entry point
├── requirements.txt     # Project dependencies
├── common/             # Common utilities and core components
│   ├── __init__.py
│   ├── board.py        # Board state representation
│   └── utils.py        # Shared utilities
└── solvers/            # Puzzle solving algorithms
    ├── __init__.py
    ├── solver.py       # Base solver interface
    ├── astar.py        # A* search implementation
    ├── bfs.py          # Breadth-first search
    └── dfs.py          # Depth-first search
```

## Package Organization

The project follows a modular organization:

1. Root Level:
   - Main execution entry point
   - Package initialization
   - Dependency management

2. Common Module:
   - Core data structures
   - Shared utilities
   - Configuration settings

3. Solvers Module:
   - Search algorithm implementations
   - Solution tracking
   - Debug visualization

## Root Files

### main.py

The main entry point for the taquin puzzle solver:

- Puzzle initialization
- Algorithm selection
- Solution execution
- Result visualization

### requirements.txt

Project dependencies:

- Python standard library
- No external dependencies required

### **init**.py

Package initialization:

- Version information
- Public interface definitions
- Package-level imports

## Package Initialization

The root `__init__.py` file defines the public interface of the package:

```python
# Public interface exports
from .solvers import Solver, SolutionInfo, DFSSolver, BFSSolver, AStarSolver
from .common import Board, Direction

__version__ = '1.0.0'
```

## Integration Points

1. Main → Solvers:
   - Algorithm instantiation
   - Solution execution
   - Result handling

2. Main → Common:
   - Board creation
   - Move validation
   - State management

3. Package → Users:
   - Clean public interface
   - Type hints
   - Documentation

## Usage Example

```python
from taquin import Board, AStarSolver

# Create initial board state
initial_state = [
    [1, 2, 3],
    [4, 0, 6],
    [7, 5, 8]
]

# Initialize board and solver
board = Board(initial_state)
solver = AStarSolver(board)

# Find solution
solution = solver.solve()
if solution:
    print(f"Solution found: {solution}")
else:
    print("No solution found")
```

## Development Guidelines

1. Code Organization:
   - Modular structure
   - Clear separation of concerns
   - Consistent file naming

2. Documentation:
   - Docstrings
   - Type hints
   - Usage examples

3. Testing:
   - Unit tests
   - Integration tests
   - Performance benchmarks

4. Version Control:
   - Feature branches
   - Semantic versioning
   - Clear commit messages

## Future Improvements

1. Extensibility:
   - Additional solver algorithms
   - Custom heuristics
   - Board size variations

2. Performance:
   - Optimization opportunities
   - Parallel processing
   - Memory management

3. Features:
   - GUI interface
   - Solution visualization
   - Performance metrics
