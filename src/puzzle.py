from typing import List, Tuple, Optional, Set
import copy
import random


class Puzzle:
    """Represents the 8-puzzle state and operations."""

    def __init__(self, state: List[int]):
        """
        Initialize a puzzle with the given state.
        State is a list of integers where 0 represents the blank space.
        Can be 9 elements (3×3) or 16 elements (4×4) for 8-puzzle or 15-puzzle respectively.
        """
        # Determine the size based on state length
        if len(state) == 9:
            self.size = 3  # 3×3 grid (8-puzzle)
            max_value = 8
        elif len(state) == 16:
            self.size = 4  # 4×4 grid (15-puzzle)
            max_value = 15
        else:
            raise ValueError("State must have exactly 9 elements (8-puzzle) or 16 elements (15-puzzle)")

        # Check that state contains exactly the numbers 0 through max_value
        expected_values = list(range(len(state)))
        if sorted([x for x in state if x >= 0 and x <= max_value]) != expected_values:
            raise ValueError(f"State must contain exactly the numbers 0-{max_value}")

        self.state = state

        # Find the blank position
        self.blank_pos = self.state.index(0)

    @classmethod
    def from_string(cls, state_str: str) -> "Puzzle":
        """
        Create a Puzzle from a string representation.
        Expected format: "4 5 0 6 1 8 7 3 2" where 0 is the blank
        """
        try:
            state = [int(x) for x in state_str.strip().split()]
            return cls(state)
        except ValueError:
            raise ValueError("Invalid state string format")

    def __str__(self) -> str:
        """
        String representation of the puzzle for display.
        """
        result = ""
        for i in range(3):
            row = self.state[i * 3 : (i + 1) * 3]
            result += " ".join(str(x) if x != 0 else "b" for x in row) + "\n"
        return result.strip()

    def __eq__(self, other) -> bool:
        """
        Check if two puzzle states are equal.
        """
        if not isinstance(other, Puzzle):
            return False
        return self.state == other.state

    def __hash__(self) -> int:
        """
        Hash function for using Puzzle objects in sets and as dict keys.
        """
        return hash(tuple(self.state))

    def get_blank_position(self) -> Tuple[int, int]:
        """
        Get the position of the blank space as (row, col).
        """
        row = self.blank_pos // self.size
        col = self.blank_pos % self.size
        return (row, col)

    def get_legal_moves(self) -> List[str]:
        """
        Return a list of legal moves from the current state.
        Moves are represented as 'up', 'down', 'left', 'right'.
        """
        row, col = self.get_blank_position()
        moves = []

        # Check if blank can move up
        if row > 0:
            moves.append("up")

        # Check if blank can move down
        if row < self.size - 1:
            moves.append("down")

        # Check if blank can move left
        if col > 0:
            moves.append("left")

        # Check if blank can move right
        if col < self.size - 1:
            moves.append("right")

        return moves

    def apply_move(self, move: str) -> "Puzzle":
        """
        Apply a move to the current state and return a new Puzzle instance.
        """
        if move not in self.get_legal_moves():
            raise ValueError(f"Illegal move: {move}")

        # Create a new state by copying the current one
        new_state = copy.deepcopy(self.state)
        row, col = self.get_blank_position()
        blank_pos = row * self.size + col

        # Calculate the position to swap with the blank
        if move == "up":
            swap_pos = blank_pos - self.size
        elif move == "down":
            swap_pos = blank_pos + self.size
        elif move == "left":
            swap_pos = blank_pos - 1
        else:  # move == 'right'
            swap_pos = blank_pos + 1

        # Swap the blank with the appropriate tile
        new_state[blank_pos], new_state[swap_pos] = (
            new_state[swap_pos],
            new_state[blank_pos],
        )

        return Puzzle(new_state)

    def is_goal(self) -> bool:
        """
        Check if the current state is the goal state (tiles in order, blank at the end).
        Works for both 8-puzzle and 15-puzzle.
        """
        # Create the goal state based on the puzzle size
        size_squared = self.size * self.size
        goal_state = list(range(1, size_squared)) + [0]
        return self.state == goal_state

    def is_solvable(self) -> bool:
        """
        Check if the puzzle is solvable using the inversion count method.

        For the standard 8-puzzle (3×3), a puzzle is solvable if the number of inversions is even.
        For the 15-puzzle (4×4), a puzzle is solvable if:
        - the blank is on an even row (from the bottom) and the number of inversions is odd, or
        - the blank is on an odd row (from the bottom) and the number of inversions is even.

        An inversion is when a tile with a higher number precedes a tile with a lower number
        in the linearized representation of the state (ignoring the blank/0).
        """
        # Count inversions (excluding the blank)
        tiles = [t for t in self.state if t != 0]  # Remove the blank
        inversions = 0

        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                if tiles[i] > tiles[j]:
                    inversions += 1

        # For 3×3 puzzle (8-puzzle)
        if self.size == 3:
            return inversions % 2 == 0
        # For 4×4 puzzle (15-puzzle)
        elif self.size == 4:
            # Calculate the row of the blank from the bottom (indexed 1-4 from bottom)
            blank_row, _ = self.get_blank_position()
            blank_row_from_bottom = self.size - blank_row
            
            # If blank is on an even row from bottom, inversions must be odd
            if blank_row_from_bottom % 2 == 0:
                return inversions % 2 == 1
            # If blank is on an odd row from bottom, inversions must be even
            else:
                return inversions % 2 == 0
        else:
            raise ValueError(f"Unsupported puzzle size: {self.size}×{self.size}")

    def get_state_tuple(self) -> Tuple[int, ...]:
        """
        Return the state as a tuple for use in hashing.
        """
        return tuple(self.state)
        
    def neighbors(self) -> List[Tuple[str, "Puzzle"]]:
        """
        Generate and return all valid neighboring puzzle states.
        
        Returns:
            A list of tuples, where each tuple contains the move direction
            ("up", "down", "left", "right") and the resulting Puzzle state.
        """
        neighbors = []
        legal_moves = self.get_legal_moves()
        
        # Generate all valid neighbor states by applying each legal move
        for move in legal_moves:
            neighbor = self.apply_move(move)
            neighbors.append((move, neighbor))
            
        return neighbors

    @staticmethod
    def generate_random_solvable(n: int, size: int = 3) -> List["Puzzle"]:
        """
        Generate n distinct, solvable puzzle states through random shuffling.

        This method repeatedly shuffles a solved puzzle state until it has
        generated n unique, solvable puzzle configurations. It uses the
        is_solvable() method to check if a shuffled state is solvable.

        Args:
            n: The number of distinct, solvable puzzles to generate
            size: Size of the puzzle grid (3 for 8-puzzle, 4 for 15-puzzle)

        Returns:
            A list containing n distinct Puzzle instances with solvable states

        Raises:
            ValueError: If n <= 0 or size is not supported
        """
        if n <= 0:
            raise ValueError("Number of puzzles must be positive")
            
        if size not in [3, 4]:
            raise ValueError("Only puzzles of size 3 (8-puzzle) or 4 (15-puzzle) are supported")

        # Create the goal state based on size
        size_squared = size * size
        goal_state = list(range(1, size_squared)) + [0]

        # Set to track unique puzzle states
        unique_states = set()
        result = []

        while len(result) < n:
            # Create a shuffled copy of the goal state
            shuffled = goal_state.copy()
            random.shuffle(shuffled)

            # Create a puzzle from the shuffled state
            puzzle = Puzzle(shuffled)

            # Check if it's solvable and not already in our collection
            state_tuple = puzzle.get_state_tuple()
            if puzzle.is_solvable() and state_tuple not in unique_states:
                unique_states.add(state_tuple)
                result.append(puzzle)

        return result
