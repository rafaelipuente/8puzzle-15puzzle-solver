from typing import List, Callable, Dict, Set, Optional, Tuple
import heapq
import time

from . import Search
from ..puzzle import Puzzle
from ..node import Node


class BestFirstSearch(Search):
    """Implementation of Best-First Search algorithm."""

    def search(
        self, initial_state: Puzzle, heuristic_func: Callable[[Puzzle], int]
    ) -> Optional[Node]:
        """
        Perform best-first search from the initial state.

        In best-first search, nodes are expanded in order of their heuristic value,
        ignoring the path cost. This is a greedy approach where we always choose the
        node that looks most promising according to the heuristic.

        Args:
            initial_state: The initial puzzle state
            heuristic_func: The heuristic function to use

        Returns:
            The goal node if found, None otherwise
        """
        # Reset statistics
        self.nodes_expanded = 0
        self.nodes_generated = 0
        self.execution_time = 0

        # Record start time
        start_time = time.time()

        # Check if the initial state is solvable
        if not initial_state.is_solvable():
            print("Warning: The puzzle is not solvable!")
            self.execution_time = time.time() - start_time
            return None

        # Check if the initial state is already the goal state
        if initial_state.is_goal():
            self.execution_time = time.time() - start_time
            return Node(state=initial_state, heuristic=0)

        # Initialize the open list (priority queue) with the initial node
        # For best-first search, priority is based solely on heuristic value
        initial_h = heuristic_func(initial_state)
        initial_node = Node(state=initial_state, cost=0, heuristic=initial_h)
        self.nodes_generated += 1

        # In best-first search, the priority is only the heuristic value, not g + h
        # So we need a custom priority queue that uses only h as the priority
        open_list = [(initial_h, 0, initial_node)]  # (h, tie_breaker, node)
        open_set = {initial_state.get_state_tuple()}  # For efficient membership testing

        # Keep track of visited states to avoid cycles
        closed_set = set()

        # Counter for tie-breaking when heuristic values are equal
        counter = 1

        # Main search loop
        while open_list and self.nodes_expanded < self.max_steps:
            # Get the node with the lowest heuristic value
            _, _, current_node = heapq.heappop(open_list)
            state_tuple = current_node.state.get_state_tuple()
            open_set.remove(state_tuple)

            # Check if this is the goal state
            if current_node.state.is_goal():
                self.execution_time = time.time() - start_time
                return current_node

            # Add the current state to the closed set
            closed_set.add(state_tuple)

            # Expand the current node
            self.nodes_expanded += 1
            for child_node in current_node.expand(heuristic_func):
                self.nodes_generated += 1
                child_state_tuple = child_node.state.get_state_tuple()

                # Skip if we've already processed this state
                if child_state_tuple in closed_set:
                    continue

                # Skip if this state is already in the open list
                if child_state_tuple in open_set:
                    continue

                # Add child to the open list
                # For best-first search, we only care about the heuristic value
                heapq.heappush(open_list, (child_node.heuristic, counter, child_node))
                open_set.add(child_state_tuple)
                counter += 1

        # If we get here, no solution was found within the step limit
        self.execution_time = time.time() - start_time
        return None
