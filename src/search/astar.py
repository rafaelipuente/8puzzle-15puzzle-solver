from typing import List, Callable, Dict, Set, Optional, Tuple
import heapq
import time

from . import Search
from ..puzzle import Puzzle
from ..node import Node


class AStarSearch(Search):
    """Implementation of A* Search algorithm."""

    def search(
        self, initial_state: Puzzle, heuristic_func: Callable[[Puzzle], int]
    ) -> Optional[Node]:
        """
        Perform A* search from the initial state.

        In A* search, nodes are expanded in order of f(n) = g(n) + h(n),
        where g(n) is the cost to reach node n from the start and h(n) is
        the estimated cost from n to the goal. A* is complete and optimal
        if the heuristic is admissible.

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
        initial_h = heuristic_func(initial_state)
        initial_node = Node(state=initial_state, cost=0, heuristic=initial_h)
        self.nodes_generated += 1

        # In A*, the priority is f = g + h
        open_list = [
            (initial_node.total_cost, 0, initial_node)
        ]  # (f, tie_breaker, node)
        open_dict = {
            initial_state.get_state_tuple(): initial_node
        }  # For efficient lookup and updates

        # Keep track of visited states to avoid cycles
        closed_set = set()

        # Counter for tie-breaking when f values are equal
        counter = 1

        # Main search loop
        while open_list and self.nodes_expanded < self.max_steps:
            # Get the node with the lowest f value
            _, _, current_node = heapq.heappop(open_list)
            
            # Check if this is the goal state immediately after popping
            if current_node.state.is_goal():
                self.execution_time = time.time() - start_time
                return current_node
            
            state_tuple = current_node.state.get_state_tuple()

            # Remove from open_dict if this is the best path to this state
            if state_tuple in open_dict and open_dict[state_tuple] == current_node:
                del open_dict[state_tuple]
            else:
                # We've found a better path to this state already
                continue

            # Add the current state to the closed set
            closed_set.add(state_tuple)

            # Expand the current node only if it's not a goal state
            self.nodes_expanded += 1
            for child_node in current_node.expand(heuristic_func):
                self.nodes_generated += 1
                child_state_tuple = child_node.state.get_state_tuple()

                # Skip if we've already processed this state
                if child_state_tuple in closed_set:
                    continue

                # Check if this state is already in the open list with a better path
                if child_state_tuple in open_dict:
                    existing_node = open_dict[child_state_tuple]
                    if existing_node.cost <= child_node.cost:
                        continue

                # Add or update child in the open list
                open_dict[child_state_tuple] = child_node
                heapq.heappush(open_list, (child_node.total_cost, counter, child_node))
                counter += 1

        # If we get here, no solution was found within the step limit
        self.execution_time = time.time() - start_time
        return None
