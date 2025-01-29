# Common Package Documentation

This document details the implementation of the common utilities and core
components in the `common/` directory.

## Overview

The common package provides essential functionality used across the project:

- Board state representation and manipulation
- Direction enumeration
- Utility functions and configurations
- Terminal output formatting

## board.py

The `Board` class is the core data structure representing the puzzle state.

### Key Features

1. Board State Management:

```python
class Board:
    def __init__(self, initial_state: List[List[int]]):
        self.size = len(initial_state)
        self.state = []  # 1D internal representation
        self.blank_pos = 0  # Position of empty tile
```

2. State Representation:

- Internal 1D array for efficient operations
- 2D representation for display/user interaction
- Zero (0) represents the blank space

3. Move Operations:

- Validation of possible moves
- State transitions via tile swapping
- Direction-based movement (UP, DOWN, LEFT, RIGHT)

4. Heuristic Calculation:

```python
def manhattan_distance(self) -> int:
    """Calculate total Manhattan distance of tiles from goal positions"""
```

5. State Utilities:

- Deep copying via `clone()`
- Equality comparison
- Hash function for set/dict usage
- String representation with box drawing

## utils.py

Provides shared utilities and configurations.

### Configuration

The `Config` class manages global settings:

```python
class Config:
    ITERATION_DELAY = 1.0  # Delay between iterations
    MAX_DEPTH_DFS = 20    # DFS depth limit
    MAX_DEPTH_BFS = 30    # BFS depth limit
```

### Terminal Output Formatting

The `ColoredText` class provides ANSI color formatting:

```python
class ColoredText:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
```

Methods for each color:

- `blue()`: Process/status information
- `green()`: Success messages
- `yellow()`: Warnings
- `red()`: Errors/failures
- `cyan()`: UI elements

### Performance Utilities

The `with_delay` decorator:

- Controls execution speed
- Enables step-by-step visualization
- Configurable delay duration

## Direction Enumeration

The `Direction` enum in board.py defines possible moves:

```python
class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
```

## Integration Points

1. Board → Solvers:

- Provides state representation
- Manages move validity
- Calculates heuristics

2. Utils → All:

- Global configuration
- Visual formatting
- Timing control

3. Direction → All:

- Move representation
- State transitions
- Path tracking

## Best Practices

The common package implements several important design principles:

1. Separation of Concerns:

- Board logic separate from visualization
- Configuration separate from implementation
- Utilities separate from core logic

2. Immutability:

- Board states can be cloned
- Moves create new states
- Enums for direction constants

3. Efficiency:

- 1D internal representation
- Cached blank position
- Optimized distance calculations

4. Debugging:

- Rich string representations
- Colored output
- Configurable delays
