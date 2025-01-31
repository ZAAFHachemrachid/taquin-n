"""Shared utilities for the taquin package."""

import time
from typing import Any, Callable


# Global configuration
class Config:
    """Global configuration settings."""

    ITERATION_DELAY = 1.0  # Delay between iterations (seconds)
    MAX_DEPTH_DFS = 30  # Maximum search depth for DFS
    MAX_DEPTH_BFS = 30  # Maximum search depth for BFS


class ColoredText:
    """ANSI color codes for terminal output."""

    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

    @staticmethod
    def blue(text: str) -> str:
        return f"{ColoredText.BLUE}{text}{ColoredText.RESET}"

    @staticmethod
    def green(text: str) -> str:
        return f"{ColoredText.GREEN}{text}{ColoredText.RESET}"

    @staticmethod
    def yellow(text: str) -> str:
        return f"{ColoredText.YELLOW}{text}{ColoredText.RESET}"

    @staticmethod
    def red(text: str) -> str:
        return f"{ColoredText.RED}{text}{ColoredText.RESET}"

    @staticmethod
    def cyan(text: str) -> str:
        return f"{ColoredText.CYAN}{text}{ColoredText.RESET}"


def with_delay(func: Callable) -> Callable:
    """Decorator to add delay after function execution."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)
        time.sleep(Config.ITERATION_DELAY)
        return result

    return wrapper
