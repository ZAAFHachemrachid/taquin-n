from enum import Enum
from typing import List, Optional
from dataclasses import dataclass


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class Board:
    def __init__(self, initial_state: List[List[int]]):
        """
        Initialize the board with a 2D list representing the initial state.
        0 represents the blank space.
        """
        self.size = len(initial_state)
        self.state = []
        self.blank_pos = 0

        # Convert 2D state to 1D and find blank position
        for i in range(self.size):
            for j in range(self.size):
                value = initial_state[i][j]
                if value == 0:
                    self.blank_pos = i * self.size + j
                self.state.append(value)

    def get_state(self) -> List[List[int]]:
        """Convert the internal 1D state back to 2D for display/usage."""
        result = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(self.state[i * self.size + j])
            result.append(row)
        return result

    def get_size(self) -> int:
        """Return the size of the board (N for an NxN board)."""
        return self.size

    def is_goal(self) -> bool:
        """Check if the current state is the goal state."""
        expected = 1
        for i in range(len(self.state)):
            if i == len(self.state) - 1:
                if self.state[i] != 0:
                    return False
            elif self.state[i] != expected:
                return False
            expected += 1
        return True

    def get_possible_moves(self) -> List[Direction]:
        """Get a list of all possible moves from the current state."""
        moves = []
        row = self.blank_pos // self.size
        col = self.blank_pos % self.size

        if row > 0:
            moves.append(Direction.UP)
        if row < self.size - 1:
            moves.append(Direction.DOWN)
        if col > 0:
            moves.append(Direction.LEFT)
        if col < self.size - 1:
            moves.append(Direction.RIGHT)

        return moves

    def make_move(self, direction: Direction) -> bool:
        """
        Make a move in the given direction.
        Returns True if the move was successful, False otherwise.
        """
        row = self.blank_pos // self.size
        col = self.blank_pos % self.size

        new_pos = None
        if direction == Direction.UP and row > 0:
            new_pos = self.blank_pos - self.size
        elif direction == Direction.DOWN and row < self.size - 1:
            new_pos = self.blank_pos + self.size
        elif direction == Direction.LEFT and col > 0:
            new_pos = self.blank_pos - 1
        elif direction == Direction.RIGHT and col < self.size - 1:
            new_pos = self.blank_pos + 1
        else:
            return False

        # Swap blank with the adjacent tile
        self.state[self.blank_pos], self.state[new_pos] = (
            self.state[new_pos],
            self.state[self.blank_pos],
        )
        self.blank_pos = new_pos
        return True

    def manhattan_distance(self) -> int:
        """Calculate the Manhattan distance heuristic for the current state."""
        distance = 0
        for pos in range(len(self.state)):
            value = self.state[pos]
            if value != 0:  # Skip blank tile
                current_row = pos // self.size
                current_col = pos % self.size
                expected_row = (value - 1) // self.size
                expected_col = (value - 1) % self.size
                distance += abs(current_row - expected_row) + abs(
                    current_col - expected_col
                )
        return distance

    def __str__(self) -> str:
        """Create a string representation of the board with a box drawing."""
        result = ["┌" + "───┬" * (self.size - 1) + "───┐"]

        for i in range(self.size):
            row = ["│"]
            for j in range(self.size):
                value = self.state[i * self.size + j]
                if value == 0:
                    row.append(" _ │")
                else:
                    row.append(f" {value} │")
            result.append("".join(row))

            if i < self.size - 1:
                result.append("├" + "───┼" * (self.size - 1) + "───┤")

        result.append("└" + "───┴" * (self.size - 1) + "───┘")
        return "\n".join(result)

    def __eq__(self, other) -> bool:
        """Compare two boards for equality."""
        if not isinstance(other, Board):
            return False
        return self.state == other.state

    def __hash__(self) -> int:
        """Hash the board state for use in sets/dicts."""
        return hash(tuple(self.state))

    def clone(self) -> "Board":
        """Create a deep copy of the board."""
        return Board(self.get_state())
