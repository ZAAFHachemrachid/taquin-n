from typing import List, Optional, Set, Tuple
from dataclasses import dataclass
from common.board import Board, Direction
from common.utils import ColoredText, Config, with_delay
from solvers.solver import Solver, SolutionInfo, SolutionStatus


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
        if tuple(next_state.state) in visited:
            return "BAD", "Already visited"
        return "VALID", "New state"

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
        for direction, new_state, quality, _ in moves:
            move_str = {
                Direction.UP: "Up   ",
                Direction.DOWN: "Down ",
                Direction.LEFT: "Left ",
                Direction.RIGHT: "Right",
            }[direction]
            selected = (
                "=> Selected"
                if quality != "BAD" and tuple(new_state.state) not in visited
                else ""
            )
            print(f"- {move_str} {selected}")

        print(f"Total states visited: {len(visited)}")

    def get_ordered_moves(self, state: State) -> List[Direction]:
        """Get list of possible moves in a fixed priority order."""
        # Fixed priority ordering favoring UP and LEFT moves first
        priority = [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT]

        possible = state.get_possible_moves()
        # Return moves in priority order if they are possible
        return [move for move in priority if move in possible]

    def is_reverse_move(
        self, last_move: Optional[Direction], new_move: Direction
    ) -> bool:
        """Check if a move reverses the previous move."""
        if last_move is None:
            return False
        return (
            (last_move == Direction.UP and new_move == Direction.DOWN)
            or (last_move == Direction.DOWN and new_move == Direction.UP)
            or (last_move == Direction.LEFT and new_move == Direction.RIGHT)
            or (last_move == Direction.RIGHT and new_move == Direction.LEFT)
        )

    def dfs_with_depth_limit(
        self,
        state: State,
        visited: Set[Tuple[int, ...]],
        current_path: Set[Tuple[int, ...]],
        depth_limit: int,
        nodes_visited: int,
    ) -> Tuple[Optional[State], int]:
        """DFS with depth limit, cycle detection, and state tracking."""
        if state.is_goal():
            return state, nodes_visited

        if len(state.path) >= depth_limit:
            return None, nodes_visited

        # Get last move to prevent reversals
        last_move = state.path[-1] if state.path else None

        # Try moves in optimized order (based on Manhattan distance)
        moves_to_try = self.get_ordered_moves(state)

        # Debug output - show all potential moves
        possible_moves = []
        for direction in moves_to_try:
            if next_state := state.make_move(direction):
                next_state_tuple = tuple(next_state.state)
                quality = (
                    "VALID"
                    if not self.is_reverse_move(last_move, direction)
                    and next_state_tuple not in current_path
                    and next_state_tuple not in visited
                    else "BAD"
                )
                possible_moves.append((direction, next_state, quality, "New state"))
        self.debug_print(state, possible_moves, visited, len(state.path))

        # Actually try the valid moves
        for direction in moves_to_try:
            # Skip reverse moves
            if self.is_reverse_move(last_move, direction):
                continue

            if next_state := state.make_move(direction):
                next_state_tuple = tuple(next_state.state)

                # Skip if state is in current path or globally visited
                if next_state_tuple in current_path or next_state_tuple in visited:
                    continue

                nodes_visited += 1
                visited.add(next_state_tuple)
                current_path.add(next_state_tuple)

                result, nodes_visited = self.dfs_with_depth_limit(
                    next_state, visited, current_path, depth_limit, nodes_visited
                )

                if result is not None:
                    return result, nodes_visited

                current_path.remove(next_state_tuple)

        return None, nodes_visited

    def solve(self, optimal_length: Optional[int] = None) -> Optional[SolutionInfo]:
        """
        Find a solution using iterative deepening DFS with optimizations.

        Args:
            optimal_length: Optional known optimal solution length

        Returns:
            SolutionInfo containing solution status and path if found
        """
        # Check if puzzle is already solved
        initial_state = State.from_board(self.initial_board)
        if initial_state.is_goal():
            print(ColoredText.green("\n🎉 PUZZLE ALREADY SOLVED! 🎉"))
            return SolutionInfo(status=SolutionStatus.ALREADY_SOLVED)

        # Check if puzzle is solvable
        if not self.is_solvable():
            print(ColoredText.red("\n❌ PUZZLE IS UNSOLVABLE! ❌"))
            return SolutionInfo(status=SolutionStatus.UNSOLVABLE)

        total_nodes_visited = 0

        # Iterative deepening
        for depth_limit in range(1, self.max_depth + 1):
            print(ColoredText.blue(f"\nTrying depth limit: {depth_limit}"))
            # Reset visited set for each depth level to give a fresh start
            visited = set()
            current_path = {tuple(initial_state.state)}
            nodes_visited = 0

            solution, new_nodes = self.dfs_with_depth_limit(
                initial_state, visited, current_path, depth_limit, nodes_visited
            )
            total_nodes_visited += new_nodes

            if solution:
                print(ColoredText.green("\n🎉 GOAL STATE REACHED! 🎉"))
                print(f"DFS: Visited {total_nodes_visited} nodes")
                return SolutionInfo(
                    status=SolutionStatus.SOLVED,
                    moves=solution.path,
                    optimal_length=optimal_length,
                )

        print(ColoredText.yellow("\n⚠️ NO SOLUTION FOUND! ⚠️"))
        return SolutionInfo(status=SolutionStatus.NO_SOLUTION)
