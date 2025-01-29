"""
Python implementation of the sliding tile puzzle (taquin) solver.
Provides DFS, BFS, and A* search algorithms for finding solutions.
"""

from .common import Board, Direction
from .solvers import Solver, SolutionInfo, DFSSolver, BFSSolver, AStarSolver

__version__ = "0.1.0"
__all__ = [
    "Board",
    "Direction",
    "Solver",
    "SolutionInfo",
    "DFSSolver",
    "BFSSolver",
    "AStarSolver",
]
