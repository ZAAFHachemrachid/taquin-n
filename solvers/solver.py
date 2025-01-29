from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from taquin.common.board import Direction


@dataclass
class SolutionInfo:
    """Class to store information about a found solution."""

    moves: List[Direction]
    optimal_length: Optional[int] = None

    def __str__(self) -> str:
        """Convert solution information to string."""
        moves_str = ", ".join(move.name for move in self.moves)
        result = f"Solution found in {len(self.moves)} moves: {moves_str}"
        if self.optimal_length is not None:
            result += f"\nOptimal solution length: {self.optimal_length}"
        return result


class Solver(ABC):
    """Abstract base class for puzzle solvers."""

    def __init__(self, initial_board):
        """Initialize solver with initial board state."""
        self.initial_board = initial_board

    @abstractmethod
    def solve(self, optimal_length: Optional[int] = None) -> Optional[SolutionInfo]:
        """
        Find a solution for the puzzle.

        Args:
            optimal_length: Optional known optimal solution length for validation

        Returns:
            SolutionInfo if solution is found, None otherwise
        """
        pass
