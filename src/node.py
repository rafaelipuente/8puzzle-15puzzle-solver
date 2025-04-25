from dataclasses import dataclass, field
from typing import Optional, List, Callable, Any
from .puzzle import Puzzle


@dataclass
class Node:
    """Represents a node in the search tree."""

    # The puzzle state at this node
    state: Puzzle

    # Cost to reach this node from the start (g value)
    cost: int = 0

    # Heuristic value (h value)
    heuristic: int = 0

    # Parent node
    parent: Optional["Node"] = None

    # Move that led to this state from the parent
    move: Optional[str] = None

    # Total estimated cost (f = g + h)
    total_cost: int = field(init=False)

    def __post_init__(self):
        """Calculate the total cost after initialization."""
        self.total_cost = self.cost + self.heuristic

    def __lt__(self, other):
        """Compare nodes based on total cost for priority queue."""
        if not isinstance(other, Node):
            return NotImplemented
        return self.total_cost < other.total_cost

    def __eq__(self, other):
        """Check if two nodes have the same state."""
        if not isinstance(other, Node):
            return False
        return self.state == other.state

    def __hash__(self):
        """Hash function for using Node objects in sets."""
        return hash(self.state)

    def get_path(self) -> List["Node"]:
        """Get the path from the start node to this node."""
        path = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return path[::-1]  # Reverse to get start-to-goal path

    def get_solution_path(self) -> List[List[int]]:
        """Get the solution path as a list of puzzle states.
        
        Returns:
            A list of puzzle states from start to goal (inclusive).
            Note: The length of this list is the number of states, not the number of moves.
            The number of moves is len(solution_path) - 1.
        """
        return [node.state.state for node in self.get_path()]

    def get_moves_path(self) -> List[str]:
        """Get the sequence of moves from the start to this node."""
        path = self.get_path()
        return [node.move for node in path[1:]]  # Skip the first node (no move)

    def get_path_cost(self) -> int:
        """Get the total cost of the path to this node."""
        return self.cost

    def expand(self, heuristic_func: Callable[[Puzzle], int]) -> List["Node"]:
        """Expand the node by generating all possible child nodes."""
        children = []

        for move in self.state.get_legal_moves():
            # Apply the move to get a new state
            new_state = self.state.apply_move(move)

            # Create a child node
            child = Node(
                state=new_state,
                cost=self.cost + 1,  # Increment cost by 1
                heuristic=heuristic_func(new_state),
                parent=self,
                move=move,
            )

            children.append(child)

        return children
