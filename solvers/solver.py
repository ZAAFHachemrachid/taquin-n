from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from common.board import Direction


@dataclass
class SolutionStatus(Enum):
    """Enum for solution status."""

    SOLVED = "solved"
    ALREADY_SOLVED = "already_solved"
    UNSOLVABLE = "unsolvable"
    NO_SOLUTION = "no_solution"


@dataclass
class SolutionInfo:
    """Class to store information about a found solution."""

    status: SolutionStatus
    moves: Optional[List[Direction]] = None
    optimal_length: Optional[int] = None

    def __str__(self) -> str:
        """Convert solution information to string."""
        if self.status == SolutionStatus.ALREADY_SOLVED:
            return "Puzzle is already in solved state!"
        elif self.status == SolutionStatus.UNSOLVABLE:
            return "Puzzle is unsolvable from this configuration!"
        elif self.status == SolutionStatus.NO_SOLUTION:
            return "No solution found within search limits"
        else:
            moves_str = (
                ", ".join(move.name for move in self.moves) if self.moves else ""
            )
            result = f"Solution found in {len(self.moves)} moves: {moves_str}"
            if self.optimal_length is not None:
                result += f"\nOptimal solution length: {self.optimal_length}"
            return result


class Solver(ABC):
    """Abstract base class for puzzle solvers."""

    def __init__(self, initial_board):
        """Initialize solver with initial board state."""
        self.initial_board = initial_board

    def get_inversions(self) -> int:
        """
        Count inversions in the current board state.
        An inversion is when a tile precedes another tile with a lower number.
        """
        state = sum(self.initial_board.get_state(), [])  # Flatten 2D to 1D
        inversions = 0
        for i in range(len(state)):
            if state[i] == 0:  # Skip blank
                continue
            for j in range(i + 1, len(state)):
                if state[j] == 0:  # Skip blank
                    continue
                if state[j] < state[i]:
                    inversions += 1
        return inversions

    def is_solvable(self) -> bool:
        """
        Check if the puzzle is solvable from its current state.
        """
        size = self.initial_board.get_size()
        inversions = self.get_inversions()
        blank_row = self.initial_board.blank_pos // size

        if size % 2 == 1:  # Odd size board
            return inversions % 2 == 0
        else:  # Even size board
            blank_from_bottom = size - blank_row
            return (inversions + blank_from_bottom) % 2 == 0

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
