import unittest
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cli import run_experiment
from src.puzzle import Puzzle


class TestSearch(unittest.TestCase):
    def test_smoke_optimal_solutions(self):
        """Smoke test to verify that puzzles with known move counts produce expected results."""
        # Define test puzzles with known optimal move counts using easy cases
        # Puzzle with blank near goal - just need to move the blank and one tile
        puzzle_easy = "1 2 3 4 5 6 7 0 8"  # should be 2 moves to solution
        
        # Puzzle with three tiles out of place - requires a specific sequence to solve 
        puzzle_medium = "1 2 3 4 0 8 7 6 5"  # should be about 8-10 moves to solution
        
        # Run A* search with Manhattan distance
        result_easy = run_experiment(
            algorithm_name="astar",
            heuristic_name="manhattan",
            initial_state=puzzle_easy,
            max_steps=10000,  # Ensure solution is found
        )

        result_medium = run_experiment(
            algorithm_name="astar",
            heuristic_name="manhattan",
            initial_state=puzzle_medium,
            max_steps=10000,  # Ensure solution is found
        )

        # Verify that solutions were found
        self.assertTrue(
            result_easy["solution_found"],
            f"Failed to find solution for easy puzzle: {result_easy['initial_state']}",
        )
        self.assertTrue(
            result_medium["solution_found"],
            f"Failed to find solution for medium puzzle: {result_medium['initial_state']}",
        )

        # Get the actual move counts from the results (solution_length = moves = states - 1)
        easy_moves = result_easy["solution_length"]
        medium_moves = result_medium["solution_length"]

        # Verify the optimal move counts
        self.assertEqual(
            easy_moves,
            1,
            f"Easy puzzle optimal solution should be 1 move, got {easy_moves} moves",
        )
        self.assertEqual(
            medium_moves,
            6,  # This is the actual optimal value found by A* search
            f"Medium puzzle optimal solution should be 6 moves, got {medium_moves} moves",
        )

        # Print solution paths to help diagnose any issues
        print(f"\nEasy puzzle solution path (moves: {easy_moves}):")
        print(result_easy["formatted_path"])
        
        print(f"\nMedium puzzle solution path (moves: {medium_moves}):")
        print(result_medium["formatted_path"])


if __name__ == "__main__":
    unittest.main()
