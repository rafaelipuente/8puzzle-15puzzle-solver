import unittest
from src.puzzle import Puzzle


class TestPuzzle(unittest.TestCase):
    """Test cases for the Puzzle class."""

    def test_puzzle_initialization(self):
        """Test that a puzzle can be initialized correctly."""
        state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        puzzle = Puzzle(state)
        self.assertEqual(puzzle.state, state)
        self.assertEqual(puzzle.blank_pos, 8)

    def test_from_string(self):
        """Test creating a puzzle from a string."""
        state_str = "1 2 3 4 5 6 7 8 0"
        puzzle = Puzzle.from_string(state_str)
        self.assertEqual(puzzle.state, [1, 2, 3, 4, 5, 6, 7, 8, 0])

        # Test with a different state
        state_str = "4 5 0 6 1 8 7 3 2"
        puzzle = Puzzle.from_string(state_str)
        self.assertEqual(puzzle.state, [4, 5, 0, 6, 1, 8, 7, 3, 2])
        self.assertEqual(puzzle.blank_pos, 2)

    def test_legal_moves(self):
        """Test getting legal moves from a state."""
        # Blank in the middle
        puzzle = Puzzle([1, 2, 3, 4, 0, 6, 7, 8, 5])
        moves = puzzle.get_legal_moves()
        self.assertEqual(sorted(moves), sorted(["up", "down", "left", "right"]))

        # Blank in the top-left corner
        puzzle = Puzzle([0, 2, 3, 4, 5, 6, 7, 8, 1])
        moves = puzzle.get_legal_moves()
        self.assertEqual(sorted(moves), sorted(["down", "right"]))

        # Blank in the bottom-right corner
        puzzle = Puzzle([1, 2, 3, 4, 5, 6, 7, 8, 0])
        moves = puzzle.get_legal_moves()
        self.assertEqual(sorted(moves), sorted(["up", "left"]))

    def test_apply_move(self):
        """Test applying moves to a puzzle state."""
        puzzle = Puzzle([1, 2, 3, 4, 0, 6, 7, 8, 5])

        # Test moving up
        new_puzzle = puzzle.apply_move("up")
        self.assertEqual(new_puzzle.state, [1, 0, 3, 4, 2, 6, 7, 8, 5])

        # Test moving down
        new_puzzle = puzzle.apply_move("down")
        self.assertEqual(new_puzzle.state, [1, 2, 3, 4, 8, 6, 7, 0, 5])

        # Test moving left
        new_puzzle = puzzle.apply_move("left")
        self.assertEqual(new_puzzle.state, [1, 2, 3, 0, 4, 6, 7, 8, 5])

        # Test moving right
        new_puzzle = puzzle.apply_move("right")
        self.assertEqual(new_puzzle.state, [1, 2, 3, 4, 6, 0, 7, 8, 5])

    def test_is_goal(self):
        """Test checking if a state is the goal state."""
        # Goal state
        puzzle = Puzzle([1, 2, 3, 4, 5, 6, 7, 8, 0])
        self.assertTrue(puzzle.is_goal())

        # Not the goal state
        puzzle = Puzzle([1, 2, 3, 4, 0, 6, 7, 8, 5])
        self.assertFalse(puzzle.is_goal())

    def test_is_solvable(self):
        """Test checking if a puzzle is solvable."""
        # Solvable puzzles
        self.assertTrue(Puzzle([1, 2, 3, 4, 5, 6, 7, 8, 0]).is_solvable())
        self.assertFalse(
            Puzzle([1, 2, 3, 4, 0, 6, 7, 8, 5]).is_solvable()
        )  # Has 1 inversion: 8 before 5
        self.assertFalse(
            Puzzle([4, 5, 0, 6, 1, 8, 7, 3, 2]).is_solvable()
        )  # Has 15 inversions (odd number)

        # Unsolvable puzzles (odd number of inversions)
        self.assertFalse(
            Puzzle([1, 2, 3, 4, 5, 6, 8, 7, 0]).is_solvable()
        )  # 1 inversion: 8 before 7
        self.assertTrue(
            Puzzle([8, 1, 2, 7, 0, 3, 6, 5, 4]).is_solvable()
        )  # 14 inversions (even number)


class TestRandomPuzzleGeneration(unittest.TestCase):
    """Tests for the random puzzle generation functionality."""

    def test_generate_random_solvable(self):
        """Test generating random solvable puzzles."""
        # Run the test multiple times
        for _ in range(3):
            # Generate 10 random solvable puzzles
            n = 10
            puzzles = Puzzle.generate_random_solvable(n)

            # Check that we got the correct number of puzzles
            self.assertEqual(len(puzzles), n)

            # Check that all puzzles are solvable
            for puzzle in puzzles:
                self.assertTrue(puzzle.is_solvable())

            # Check that all puzzles are unique
            unique_states = set(puzzle.get_state_tuple() for puzzle in puzzles)
            self.assertEqual(len(unique_states), n)
