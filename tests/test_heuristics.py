import unittest
from src.puzzle import Puzzle
from src.heuristics.misplaced import misplaced_tiles
from src.heuristics.manhattan import manhattan_distance
from src.heuristics.linear_conflict import linear_conflict


class TestHeuristics(unittest.TestCase):
    """Test cases for the heuristic functions."""

    def setUp(self):
        """Set up test cases with various puzzle configurations."""
        # 8-puzzle (3×3) test cases
        # Goal state: [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.goal_state_8 = Puzzle([1, 2, 3, 4, 5, 6, 7, 8, 0])
        
        # One move away (misplaced: 1, manhattan: 1, linear_conflict: 1)
        self.one_move_8 = Puzzle([1, 2, 3, 4, 5, 6, 7, 0, 8])
        
        # Multiple misplaced tiles but no linear conflicts
        # (misplaced: 3, manhattan: 3, linear_conflict: 3)
        self.medium_state_8 = Puzzle([1, 2, 3, 0, 5, 6, 4, 7, 8])
        
        # State with linear conflicts (row and column conflicts)
        # (misplaced: 8, manhattan: 16, linear_conflict: 18)
        self.complex_state_8 = Puzzle([8, 7, 6, 5, 4, 3, 2, 1, 0])
        
        # 15-puzzle (4×4) test cases
        # Goal state: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
        self.goal_state_15 = Puzzle([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0])
        
        # One move away (misplaced: 1, manhattan: 1, linear_conflict: 1)
        self.one_move_15 = Puzzle([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 15])
        
        # Multiple misplaced tiles
        # (misplaced: 2, manhattan: 3, linear_conflict: 3)
        self.medium_state_15 = Puzzle([1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 11, 12, 13, 14, 10, 15])

    def test_misplaced_tiles_8puzzle(self):
        """Test the misplaced tiles heuristic for 8-puzzle."""
        # Goal state should have 0 misplaced tiles
        self.assertEqual(misplaced_tiles(self.goal_state_8), 0)
        
        # One tile misplaced
        self.assertEqual(misplaced_tiles(self.one_move_8), 1)
        
        # Multiple tiles misplaced
        self.assertEqual(misplaced_tiles(self.medium_state_8), 3)
        
        # All tiles misplaced
        self.assertEqual(misplaced_tiles(self.complex_state_8), 8)

    def test_manhattan_distance_8puzzle(self):
        """Test the Manhattan distance heuristic for 8-puzzle."""
        # Goal state should have 0 manhattan distance
        self.assertEqual(manhattan_distance(self.goal_state_8), 0)
        
        # One tile out of place by 1 position
        self.assertEqual(manhattan_distance(self.one_move_8), 1)
        
        # Multiple tiles out of place
        self.assertEqual(manhattan_distance(self.medium_state_8), 3)
        
        # Completely reversed state
        self.assertEqual(manhattan_distance(self.complex_state_8), 16)

    def test_linear_conflict_8puzzle(self):
        """Test the linear conflict heuristic for 8-puzzle."""
        # Goal state should have 0 conflicts
        self.assertEqual(linear_conflict(self.goal_state_8), 0)
        
        # One tile out of place with no linear conflicts
        self.assertEqual(linear_conflict(self.one_move_8), 1)  # Just the manhattan distance
        
        # Multiple tiles out of place but no linear conflicts
        self.assertEqual(linear_conflict(self.medium_state_8), 3)  # Just the manhattan distance
        
        # State with multiple linear conflicts
        self.assertEqual(linear_conflict(self.complex_state_8), 18)  # Manhattan + conflicts

    def test_misplaced_tiles_15puzzle(self):
        """Test the misplaced tiles heuristic for 15-puzzle."""
        # Goal state should have 0 misplaced tiles
        self.assertEqual(misplaced_tiles(self.goal_state_15), 0)
        
        # One tile misplaced
        self.assertEqual(misplaced_tiles(self.one_move_15), 1)
        
        # Multiple tiles misplaced
        self.assertEqual(misplaced_tiles(self.medium_state_15), 2)

    def test_manhattan_distance_15puzzle(self):
        """Test the Manhattan distance heuristic for 15-puzzle."""
        # Goal state should have 0 manhattan distance
        self.assertEqual(manhattan_distance(self.goal_state_15), 0)
        
        # One tile out of place by 1 position
        self.assertEqual(manhattan_distance(self.one_move_15), 1)
        
        # Multiple tiles out of place
        self.assertEqual(manhattan_distance(self.medium_state_15), 3)

    def test_linear_conflict_15puzzle(self):
        """Test the linear conflict heuristic for 15-puzzle."""
        # Goal state should have 0 conflicts
        self.assertEqual(linear_conflict(self.goal_state_15), 0)
        
        # One tile out of place with no linear conflicts
        self.assertEqual(linear_conflict(self.one_move_15), 1)  # Just the manhattan distance
        
        # Tiles out of place with linear conflicts
        self.assertEqual(linear_conflict(self.medium_state_15), 3)  # Manhattan + 2*conflicts

    def test_heuristic_admissibility(self):
        """Test that heuristics never overestimate the true cost."""
        puzzles = [
            self.goal_state_8, 
            self.one_move_8, 
            self.medium_state_8, 
            self.complex_state_8,
            self.goal_state_15,
            self.one_move_15,
            self.medium_state_15
        ]
        
        for puzzle in puzzles:
            # Misplaced tiles should be <= Manhattan distance
            self.assertLessEqual(misplaced_tiles(puzzle), manhattan_distance(puzzle))
            
            # Manhattan distance should be <= Linear conflict
            self.assertLessEqual(manhattan_distance(puzzle), linear_conflict(puzzle))


if __name__ == "__main__":
    unittest.main()
