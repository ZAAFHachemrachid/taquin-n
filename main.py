#!/usr/bin/env python3
from typing import List, Optional

from common.board import Board
from common.utils import ColoredText, Config
from solvers.solver import SolutionInfo
from solvers.dfs import DFSSolver
from solvers.bfs import BFSSolver
from solvers.astar import AStarSolver


def print_solution(solution: SolutionInfo, board: Board) -> None:
    """Display the solution steps with the board state at each move."""
    if not solution.moves:
        print("\nPuzzle is already solved!")
        return

    print(f"\nSolution found in {len(solution.moves)} moves:")
    current = Board(board.get_state())
    print("\nStarting position:")
    print(current)

    for i, move in enumerate(solution.moves, 1):
        print(f"\nStep {i}: {move.name}")
        current.make_move(move)
        print(current)


def get_algorithm_choice() -> str:
    """Get the user's choice of algorithm."""
    while True:
        print(ColoredText.cyan("\nChoose a solving algorithm:"))
        print("1. Depth-First Search (DFS)")
        print("2. Breadth-First Search (BFS)")
        print("3. A* Search")
        choice = input("\nEnter your choice (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            return {"1": "dfs", "2": "bfs", "3": "astar"}[choice]
        print(ColoredText.red("\nInvalid choice. Please enter 1, 2, or 3."))


def get_initial_state() -> List[List[int]]:
    """Get the initial puzzle state from the user or use a default state."""
    print(ColoredText.cyan("\nChoose initial puzzle state:"))
    print("1. Simple puzzle: One move from solution")
    print("2. Medium puzzle: Few moves from solution")
    print("3. Complex puzzle: Many moves from solution")

    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        if choice == "1":
            return [
                [1, 2, 3],
                [4, 0, 6],  # 0 represents the empty space
                [7, 5, 8],
            ]
        elif choice == "2":
            return [
                [1, 2, 3],
                [0, 4, 6],
                [7, 5, 8],
            ]
        elif choice == "3":
            return [
                [7, 2, 4],
                [5, 0, 6],
                [8, 3, 1],
            ]
        print(ColoredText.red("\nInvalid choice. Please enter 1, 2, or 3."))


def get_speed_setting() -> None:
    """Let user adjust the visualization speed."""
    print(ColoredText.cyan("\nChoose visualization speed:"))
    print("1. Fast (0.2 seconds)")
    print("2. Medium (0.5 seconds)")
    print("3. Slow (1.0 seconds)")

    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        if choice == "1":
            Config.ITERATION_DELAY = 0.2
            break
        elif choice == "2":
            Config.ITERATION_DELAY = 0.5
            break
        elif choice == "3":
            Config.ITERATION_DELAY = 1.0
            break
        print(ColoredText.red("\nInvalid choice. Please enter 1, 2, or 3."))


def main() -> None:
    """Main function to demonstrate the puzzle solver."""
    print(ColoredText.cyan("=== Sliding Puzzle Solver ==="))

    # Get initial settings
    initial_state = get_initial_state()
    board = Board(initial_state)
    print("\nInitial board state:")
    print(board)

    # Get speed setting
    get_speed_setting()

    # Get algorithm choice and solve
    algorithm = get_algorithm_choice()
    print(f"\nSolving puzzle using {algorithm.upper()}...")

    solver = {
        "dfs": DFSSolver,
        "bfs": BFSSolver,
        "astar": AStarSolver,
    }[algorithm](board)

    # Attempt to solve
    solver.solve()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(ColoredText.yellow("\n\nSolver stopped by user."))
    except Exception as e:
        print(ColoredText.red(f"\nError: {e}"))
