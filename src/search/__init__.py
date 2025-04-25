from abc import ABC, abstractmethod
from typing import List, Callable, Dict, Set, Optional, Tuple
import heapq
import time

from ..puzzle import Puzzle
from ..node import Node


class Search(ABC):
    """Base class for search algorithms."""

    def __init__(self, max_steps: int = 10000):
        """
        Initialize search algorithm.

        Args:
            max_steps: Maximum number of steps before giving up
        """
        self.max_steps = max_steps
        self.nodes_expanded = 0
        self.nodes_generated = 0
        self.execution_time = 0

    @abstractmethod
    def search(
        self, initial_state: Puzzle, heuristic_func: Callable[[Puzzle], int]
    ) -> Optional[Node]:
        """Search for a solution from the initial state."""
        pass

    def get_statistics(self) -> Dict[str, any]:
        """Get search statistics."""
        return {
            "nodes_expanded": self.nodes_expanded,
            "nodes_generated": self.nodes_generated,
            "execution_time": self.execution_time,
        }


# Import search algorithms for easy access
from .best_first import BestFirstSearch
from .astar import AStarSearch

# Export classes
__all__ = ["Search", "BestFirstSearch", "AStarSearch"]

# Map of algorithm names to classes for easy lookup
SEARCH_ALGORITHMS = {"best-first": BestFirstSearch, "astar": AStarSearch}
