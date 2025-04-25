from ..puzzle import Puzzle
from .manhattan import manhattan_distance


def linear_conflict(puzzle: Puzzle) -> int:
    """
    Heuristic function that combines Manhattan distance with linear conflicts.

    This is our custom third heuristic. It builds upon the Manhattan distance
    by adding a penalty for linear conflicts. A linear conflict occurs when two
    tiles are in their goal row/column but are in the wrong order, requiring at
    least two moves to resolve.

    Linear conflicts make the heuristic more accurate but still admissible,
    as each conflict requires at least two additional moves to resolve.

    Args:
        puzzle: The current puzzle state

    Returns:
        Manhattan distance plus 2 times the number of linear conflicts
    """
    size = puzzle.size
    # Start with the Manhattan distance
    result = manhattan_distance(puzzle)
    conflicts = 0

    # Check for row conflicts
    for row in range(size):
        # Get all tiles in this row
        tiles_in_row = [
            (i % size, puzzle.state[row * size + i % size])
            for i in range(size)
            if puzzle.state[row * size + i] != 0
        ]

        # Check each pair of tiles
        for i in range(len(tiles_in_row)):
            pos_i, tile_i = tiles_in_row[i]
            # Goal row for this tile
            goal_row_i = (tile_i - 1) // size

            # If tile is in its goal row
            if goal_row_i == row:
                for j in range(i + 1, len(tiles_in_row)):
                    pos_j, tile_j = tiles_in_row[j]
                    goal_row_j = (tile_j - 1) // size

                    # If second tile is also in its goal row
                    if goal_row_j == row:
                        # Goal columns
                        goal_col_i = (tile_i - 1) % size
                        goal_col_j = (tile_j - 1) % size

                        # Check if there's a conflict (tiles are in wrong order)
                        if goal_col_i > goal_col_j and pos_i < pos_j:
                            conflicts += 1
                        elif goal_col_i < goal_col_j and pos_i > pos_j:
                            conflicts += 1

    # Check for column conflicts
    for col in range(size):
        # Get all tiles in this column
        tiles_in_col = [
            (i // size, puzzle.state[i * size + col])
            for i in range(size)
            if puzzle.state[i * size + col] != 0
        ]

        # Check each pair of tiles
        for i in range(len(tiles_in_col)):
            pos_i, tile_i = tiles_in_col[i]
            # Goal column for this tile
            goal_col_i = (tile_i - 1) % size

            # If tile is in its goal column
            if goal_col_i == col:
                for j in range(i + 1, len(tiles_in_col)):
                    pos_j, tile_j = tiles_in_col[j]
                    goal_col_j = (tile_j - 1) % size

                    # If second tile is also in its goal column
                    if goal_col_j == col:
                        # Goal rows
                        goal_row_i = (tile_i - 1) // size
                        goal_row_j = (tile_j - 1) // size

                        # Check if there's a conflict (tiles are in wrong order)
                        if goal_row_i > goal_row_j and pos_i < pos_j:
                            conflicts += 1
                        elif goal_row_i < goal_row_j and pos_i > pos_j:
                            conflicts += 1

    # Each conflict requires at least 2 additional moves to resolve
    return result + 2 * conflicts
