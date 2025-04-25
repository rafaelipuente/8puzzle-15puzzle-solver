from .misplaced import misplaced_tiles
from .manhattan import manhattan_distance
from .linear_conflict import linear_conflict

# Export all heuristic functions
__all__ = ["misplaced_tiles", "manhattan_distance", "linear_conflict"]

# Map of heuristic names to functions for easy lookup
HEURISTICS = {
    "misplaced": misplaced_tiles,
    "manhattan": manhattan_distance,
    "linear_conflict": linear_conflict,
}
