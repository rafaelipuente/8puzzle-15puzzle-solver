from ..puzzle import Puzzle


def misplaced_tiles(puzzle: Puzzle) -> int:
    """
    Heuristic function that counts the number of misplaced tiles.

    This is the first heuristic described in the textbook. It counts the number of tiles
    that are not in their goal position (excluding the blank).

    Args:
        puzzle: The current puzzle state

    Returns:
        The number of misplaced tiles
    """
    # Generate the goal state based on puzzle size
    size_squared = puzzle.size * puzzle.size
    goal_state = list(range(1, size_squared)) + [0]
    count = 0

    for i, tile in enumerate(puzzle.state):
        if tile != 0 and tile != goal_state[i]:
            count += 1

    return count
