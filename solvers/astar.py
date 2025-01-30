from typing import List, Optional, Set, Tuple
from dataclasses import dataclass
import heapq
from common.board import Board, Direction
from common.utils import ColoredText, Config, with_delay
from solvers.solver import Solver, SolutionInfo


@dataclass
class State:
    """State class for A* search."""

    state: List[int]
    blank_pos: int
    size: int
    path: List[Direction]
    g_cost: int  # Cost from start to current node
    h_cost: int  # Heuristic cost (Manhattan distance)

    def __lt__(self, other: "State") -> bool:
        """
        Compare states for priority queue ordering.
        Lower f_cost = higher priority.
        If f_costs are equal, prefer higher g_cost (deeper nodes).
        """
        if not isinstance(other, State):
            return NotImplemented
        self_f = self.f_cost()
        other_f = other.f_cost()
        if self_f == other_f:
            return (
                self.g_cost > other.g_cost
            )  # Prefer deeper nodes when f-costs are equal
        return self_f < other_f

    def f_cost(self) -> int:
        """Calculate f-cost (g_cost + h_cost)."""
        return self.g_cost + self.h_cost

    @staticmethod
    def from_board(board: Board) -> "State":
        """Create a State instance from a Board."""
        state = sum(board.get_state(), [])  # Flatten 2D list to 1D
        return State(
            state=state,
            blank_pos=board.blank_pos,
            size=board.get_size(),
            path=[],
            g_cost=0,
            h_cost=board.manhattan_distance(),
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

        new_g_cost = self.g_cost + 1
        next_state = State(
            state=new_state,
            blank_pos=new_pos,
            size=self.size,
            path=new_path,
            g_cost=new_g_cost,
            h_cost=0,  # Will be calculated after creation
        )
        next_state.h_cost = next_state.manhattan_distance()
        return next_state

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


class AStarSolver(Solver):
    """A* Search solver implementation with debug output."""

    def __init__(self, initial_board: Board):
        """Initialize A* solver with initial board state."""
        super().__init__(initial_board)

    @staticmethod
    def evaluate_move(
        current: State, next_state: State, closed_set: Set[Tuple[int, ...]]
    ) -> Tuple[str, str]:
        """Evaluate a potential move and provide debug information."""
        f_cost = next_state.f_cost()
        current_f = current.f_cost()

        if tuple(next_state.state) in closed_set:
            return "BAD", "Already explored"
        elif f_cost < current_f:
            return "BEST", f"F-cost: {current_f} -> {f_cost}"
        elif f_cost == current_f:
            return "MID", f"F-cost unchanged: {f_cost}"
        else:
            return "BAD", f"F-cost: {current_f} -> {f_cost}"

    @with_delay
    def debug_print(
        self,
        current: State,
        moves: List[Tuple[Direction, State, str, str]],
        closed_set: Set[Tuple[int, ...]],
        nodes_visited: int,
    ) -> None:
        """Print debug information about current search state."""
        print(
            f"\nExploring State (f={current.f_cost()}, g={current.g_cost}, h={current.h_cost})"
        )
        print(current.display())

        print("\nPossible moves from this state:")
        for direction, new_state, quality, _ in moves:
            move_str = {
                Direction.UP: "Up   ",
                Direction.DOWN: "Down ",
                Direction.LEFT: "Left ",
                Direction.RIGHT: "Right",
            }[direction]
            selected = (
                "=> Selected"
                if quality != "BAD" and tuple(new_state.state) not in closed_set
                else ""
            )
            print(f"- {move_str} {selected}")

        print(f"States explored: {len(closed_set)}")
        print(f"Nodes visited: {nodes_visited}")

    def solve(self, optimal_length: Optional[int] = None) -> Optional[SolutionInfo]:
        """
        Find a solution using A* Search with debug output.

        Args:
            optimal_length: Optional known optimal solution length

        Returns:
            SolutionInfo if solution is found, None otherwise
        """
        initial_state = State.from_board(self.initial_board)
        open_set = []  # Priority queue of states to explore
        closed_set = set()  # Set of visited states
        nodes_visited = 0

        # Add initial state to open set
        heapq.heappush(open_set, initial_state)

        while open_set:
            current_state = heapq.heappop(open_set)
            nodes_visited += 1

            # Skip if we've already explored this state
            if tuple(current_state.state) in closed_set:
                continue

            # Evaluate and collect possible moves
            possible_moves = []
            for direction in current_state.get_possible_moves():
                if next_state := current_state.make_move(direction):
                    quality, reason = self.evaluate_move(
                        current_state, next_state, closed_set
                    )
                    possible_moves.append((direction, next_state, quality, reason))

            # Debug output for current state
            self.debug_print(current_state, possible_moves, closed_set, nodes_visited)

            # Check if we've reached the goal
            if current_state.is_goal():
                print(ColoredText.green("\n🎉 GOAL STATE REACHED! 🎉"))
                print(f"A*: Visited {nodes_visited} nodes")
                return SolutionInfo(current_state.path, optimal_length)

            # Add current state to closed set
            closed_set.add(tuple(current_state.state))

            # Generate and explore successors
            for direction, next_state, quality, _ in possible_moves:
                if quality != "BAD" and tuple(next_state.state) not in closed_set:
                    heapq.heappush(open_set, next_state)

        return None  # No solution found
