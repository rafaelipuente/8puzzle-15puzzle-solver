# 8-Puzzle Solver

This project implements both Best-First Search and A* Search algorithms to solve the 8-puzzle problem using three different heuristics.

## Setup

1. Ensure you have Python 3.8+ installed
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Solver

To run the solver with default settings:

```bash
python -m src.cli
```

This will run both search algorithms with all three heuristics on the five initial states defined in `data/initial_states.txt`.

### Command Line Options

```bash
python -m src.cli --algorithm best-first --heuristic misplaced --state "4 5 0 6 1 8 7 3 2"
```

Options:
- `--algorithm`: Choose search algorithm (`best-first` or `astar`)
- `--heuristic`: Choose heuristic (`misplaced`, `manhattan`, or `linear_conflict`)
- `--state`: Provide a specific initial state (space-separated, use 0 for the blank)
- `--max-steps`: Maximum number of steps before stopping (default: 10000)
- `--all`: Run all combinations of algorithms and heuristics on all initial states

### Running Tests

```bash
pytest
```

## Project Structure

- `src/`: Contains the main code
  - `puzzle.py`: Puzzle state representation and operations
  - `node.py`: Search node implementation
  - `heuristics/`: Different heuristic implementations
  - `search/`: Search algorithm implementations
  - `cli.py`: Command-line interface
- `data/`: Contains test data
- `reports/`: Contains experiment results
- `tests/`: Contains unit tests
