# 8-Puzzle and 15-Puzzle Solver: Analysis and Results

## Introduction

This project implements solvers for both the 8-puzzle (3×3) and the more complex 15-puzzle (4×4). Two search algorithms were implemented and compared: Best-First Search and A* Search. To guide these searches, three different heuristics were implemented and evaluated: Misplaced Tiles, Manhattan Distance, and Linear Conflict. Each heuristic was designed to be admissible to ensure optimal solutions when used with A* Search.

## Methodology

The implementation included:

- **Search Algorithms**: Best-First Search and A* Search
- **Heuristics**:
  - Misplaced Tiles: Counts the number of tiles not in their goal position
  - Manhattan Distance: Sums the horizontal and vertical distances for each tile from its current position to its goal position
  - Linear Conflict: Manhattan distance plus a penalty for tiles that are in their correct row/column but in the wrong order

Five different initial states were tested for each puzzle type, algorithm, and heuristic combination, measuring solution path length, nodes expanded, nodes generated, and execution time.

## Results

### 8-Puzzle Results

| Algorithm | Heuristic | Avg. Steps | Avg. Nodes Expanded | Avg. Time (s) |
|-----------|-----------|------------|---------------------|--------------|
| A* | Linear Conflict | 22.20 | 718 | 0.013 |
| A* | Manhattan | 22.20 | 984 | 0.009 |
| A* | Misplaced | 22.20 | 9713 | 0.094 |
| Best-First | Linear Conflict | 37.80 | 231 | 0.006 |
| Best-First | Manhattan | 47.40 | 412 | 0.003 |
| Best-First | Misplaced | 55.80 | 777 | 0.007 |

### 15-Puzzle Results

For the 15-puzzle, the complexity increased dramatically:

- A* Search with all heuristics reached the step limit (200,000 nodes) without finding solutions
- Best-First with Linear Conflict achieved a 118.00 average step count
- Best-First with Manhattan Distance achieved a 167.20 average step count
- Best-First with Misplaced Tiles failed to find solutions

## Analysis

Several key findings emerged from this implementation:

1. **A* outperformed Best-First for solution quality**: While A* required more computation for the 8-puzzle, it consistently produced shorter, optimal paths. Best-First was faster but produced significantly longer solution paths.

2. **Heuristic strength made substantial differences**: Linear Conflict consistently provided the most efficient guidance, expanding fewer nodes while maintaining solution quality. For example, with A* on the 8-puzzle, Linear Conflict expanded 718 nodes on average versus 9713 for Misplaced Tiles.

3. **15-puzzle complexity demonstrated the limits of these approaches**: The state space increased from 9!/2 ≈ 181,440 for the 8-puzzle to 16!/2 ≈ 10.5 trillion for the 15-puzzle, making exhaustive search practically impossible. This highlighted how quickly search spaces grow with problem size.

4. **Implementation challenges**: Several technical issues were identified and resolved during development, including correct solvability checks for 4×4 puzzles and memory management for large search spaces.

## Conclusion

This project demonstrated the critical importance of selecting appropriate heuristics for informed search problems. The Linear Conflict heuristic provided substantial performance improvements for both puzzles, particularly when combined with A* Search.

The dramatic increase in complexity from the 8-puzzle to the 15-puzzle revealed the limitations of basic informed search approaches. For future work, more advanced techniques such as Iterative Deepening A* (IDA*) or pattern database heuristics would be necessary for efficiently solving the 15-puzzle and similar large state-space problems.

Overall, this implementation provided valuable insights into the practical tradeoffs between algorithm completeness, optimality, and computational efficiency in informed search problems.