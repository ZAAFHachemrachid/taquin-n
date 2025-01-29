from typing import List, Optional, Set, Tuple
from dataclasses import dataclass
from taquin.common.board import Board, Direction
from taquin.common.utils import ColoredText, Config, with_delay
from taquin.solvers.solver import Solver, SolutionInfo


@dataclass
class State:
    """State class for DFS search."""

    state: List[int]
    blank_pos: int
    size: int
    path: List[Direction]

    @staticmethod
    def from_board(board: Board) -> "State":
        """Create a State instance from a Board."""
        return State(
            state=sum(board.get_state(), []),  # Flatten 2D list to 1D
            blank_pos=board.blank_pos,
            size=board.get_size(),
            path=[],
        )

    def manhattan_distance(self) -> int:
        """Calculate Manhattan distance heuristic."""
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

    def is_goal(self) -> bool:
        """Check if current state is the goal state."""
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
        """Get list of possible moves from current state."""
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

    def make_move(self, direction: Direction) -> Optional["State"]:
        """Make a move in the given direction, returning new state if valid."""
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
            return None

        new_state = self.state.copy()
        new_state[self.blank_pos], new_state[new_pos] = (
            new_state[new_pos],
            new_state[self.blank_pos],
        )

        new_path = self.path.copy()
        new_path.append(direction)

        return State(state=new_state, blank_pos=new_pos, size=self.size, path=new_path)

    def display(self) -> str:
        """Create a string representation of the board state."""
        result = [ColoredText.cyan("┌───┬───┬───┐")]
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
                result.append(ColoredText.cyan("├───┼───┼───┤"))
        result.append(ColoredText.cyan("└───┴───┴───┘"))
        return "\n".join(result)


class DFSSolver(Solver):
    """Depth-First Search solver implementation."""

    def __init__(self, initial_board: Board):
        """Initialize DFS solver with initial board state."""
        super().__init__(initial_board)
        self.max_depth = Config.MAX_DEPTH_DFS

    @staticmethod
    def evaluate_move(
        current: State, next_state: State, visited: Set[Tuple[int, ...]]
    ) -> Tuple[str, str]:
        """Evaluate a potential move and provide debug information."""
        current_dist = current.manhattan_distance()
        new_dist = next_state.manhattan_distance()

        if tuple(next_state.state) in visited:
            return "BAD", "Already visited"
        elif new_dist < current_dist:
            return "BEST", f"Manhattan distance: {current_dist} -> {new_dist}"
        elif new_dist == current_dist:
            return "MID", f"Manhattan distance unchanged: {current_dist}"
        else:
            return "BAD", f"Manhattan distance: {current_dist} -> {new_dist}"

    @with_delay
    def debug_print(
        self,
        current: State,
        moves: List[Tuple[Direction, State, str, str]],
        visited: Set[Tuple[int, ...]],
        depth: int,
    ) -> None:
        """Print debug information about current search state."""
        print(f"\nExploring Depth {depth}")
        print(current.display())

        print("\nPossible moves at this depth:")
        for direction, new_state, quality, reason in moves:
            move_str = {
                Direction.UP: "Up   ",
                Direction.DOWN: "Down ",
                Direction.LEFT: "Left ",
                Direction.RIGHT: "Right",
            }[direction]

            if quality == "BEST":
                colored_move = ColoredText.green(f"{move_str} [{quality}]")
            elif quality == "MID":
                colored_move = ColoredText.yellow(f"{move_str} [{quality}]")
            else:
                colored_move = ColoredText.red(f"{move_str} [{quality}]")

            print(f"- {colored_move} | {reason}")

        print(f"Total states visited: {len(visited)}")

    def solve(self, optimal_length: Optional[int] = None) -> Optional[SolutionInfo]:
        """
        Find a solution using Depth-First Search with debug output.

        Args:
            optimal_length: Optional known optimal solution length

        Returns:
            SolutionInfo if solution is found, None otherwise
        """
        stack = []  # Stack of states to explore
        visited = set()  # Set of visited states
        nodes_visited = 0

        # Initialize starting state
        initial_state = State.from_board(self.initial_board)
        stack.append(initial_state)
        visited.add(tuple(initial_state.state))

        while stack:
            current_state = stack.pop()
            nodes_visited += 1

            # Evaluate and collect possible moves
            possible_moves = []
            for direction in current_state.get_possible_moves():
                if next_state := current_state.make_move(direction):
                    quality, reason = self.evaluate_move(
                        current_state, next_state, visited
                    )
                    possible_moves.append((direction, next_state, quality, reason))

            # Debug output for current state
            self.debug_print(
                current_state, possible_moves, visited, len(current_state.path)
            )

            # Check if we've reached the goal
            if current_state.is_goal():
                print(ColoredText.green("\n🎉 GOAL STATE REACHED! 🎉"))
                print(f"DFS: Visited {nodes_visited} nodes")
                return SolutionInfo(current_state.path, optimal_length)

            # Skip if we've exceeded max depth
            if len(current_state.path) >= self.max_depth:
                print(ColoredText.yellow("\nMax depth reached at this branch..."))
                continue

            # Add states to stack in reverse order (for consistent exploration)
            next_states = []
            for direction, next_state, quality, _ in possible_moves:
                if quality != "BAD" and tuple(next_state.state) not in visited:
                    visited.add(tuple(next_state.state))
                    next_states.append(next_state)

            next_states.sort(key=lambda x: len(x.path), reverse=True)
            stack.extend(next_states)

        return None  # No solution found
