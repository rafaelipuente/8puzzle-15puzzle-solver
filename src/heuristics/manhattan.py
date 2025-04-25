from ..puzzle import Puzzle


def manhattan_distance(puzzle: Puzzle) -> int:
    """
    Heuristic function that calculates the sum of Manhattan distances.

    This is the second heuristic described in the textbook. It calculates the sum
    of Manhattan distances (|x1 - x2| + |y1 - y2|) for each tile from its current
    position to its goal position (excluding the blank).

    Args:
        puzzle: The current puzzle state

    Returns:
        The sum of Manhattan distances
    """
    size = puzzle.size
    total_distance = 0

    # For each tile, calculate its Manhattan distance to its goal position
    for i, tile in enumerate(puzzle.state):
        if tile == 0:  # Skip the blank
            continue

        # Current position
        current_row = i // size
        current_col = i % size

        # Goal position: for tile N, it should be at index (N-1)
        goal_idx = tile - 1
        goal_row = goal_idx // size
        goal_col = goal_idx % size

        # Calculate Manhattan distance: |row1 - row2| + |col1 - col2|
        distance = abs(current_row - goal_row) + abs(current_col - goal_col)

        total_distance += distance

    return total_distance
