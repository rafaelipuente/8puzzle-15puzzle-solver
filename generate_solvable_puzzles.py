#!/usr/bin/env python3
"""Script to generate solvable puzzles and update initial_states.txt"""

from src.puzzle import Puzzle


def format_state(state):
    """Format a state list as a string with '0' for the blank"""
    return " ".join(str(x) for x in state)


def main():
    # Generate 5 random solvable puzzles
    solvable_puzzles = Puzzle.generate_random_solvable(5)

    # Convert them to string format
    puzzle_strings = [format_state(puzzle.state) for puzzle in solvable_puzzles]

    # Prepare the file content with header comments
    file_content = [
        "# Format: Each line represents one initial state",
        "# Use 0 to represent the blank tile",
        "# The goal state is always: 1 2 3 4 5 6 7 8 0",
        "",
    ]
    file_content.extend(puzzle_strings)

    # Write to the initial_states.txt file
    with open("data/initial_states.txt", "w") as f:
        f.write("\n".join(file_content))

    print("Successfully updated initial_states.txt with 5 random solvable puzzles.")


if __name__ == "__main__":
    main()
