import argparse
import time
from typing import List, Dict, Any
import os

from .puzzle import Puzzle
from .search import SEARCH_ALGORITHMS
from .heuristics import HEURISTICS


def format_state(state: List[int]) -> str:
    """Format a state as a string with 'b' for the blank."""
    return "(" + " ".join(str(x) if x != 0 else "b" for x in state) + ")"


def format_path(path: List[List[int]]) -> str:
    """Format a solution path for display."""
    return " → ".join(format_state(state) for state in path)


def read_initial_states(filepath: str, size: int = 3) -> List[str]:
    """Read initial states from a file. If fewer than 5 entries exist, generate additional
    random solvable puzzles to reach a total of 5.
    
    Args:
        filepath: Path to the file containing puzzle states
        size: Size of the puzzle (3 for 8-puzzle, 4 for 15-puzzle)
    
    Returns:
        List of state strings
    """
    states = []
    # Read existing states if the file exists
    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    # Only use states that match the expected size
                    state_values = line.split()
                    expected_length = size * size
                    if len(state_values) == expected_length:
                        states.append(line)
    except FileNotFoundError:
        # If file doesn't exist, we'll generate all 5 puzzles
        pass

    # Check if we need to generate more states
    if len(states) < 5:
        from .puzzle import Puzzle

        # Calculate how many more we need
        needed = 5 - len(states)
        print(
            f"Found only {len(states)} {size}×{size} initial states, generating {needed} more random solvable puzzles..."
        )

        # Generate additional random solvable puzzles with the specified size
        new_puzzles = Puzzle.generate_random_solvable(needed, size)

        # Convert to strings and add to states list
        for puzzle in new_puzzles:
            state_str = " ".join(str(x) for x in puzzle.state)
            states.append(state_str)

        # Append to the file
        with open(filepath, "a") as f:
            # Add a newline if the file doesn't end with one and file exists and has content
            if states and len(states) > needed and not states[-needed - 1].endswith("\n"):
                f.write("\n")
            # Write each new state on a separate line
            for state_str in states[-needed:]:
                f.write(state_str + "\n")

        print(f"Added {needed} new random solvable {size}×{size} puzzles to {filepath}")

    return states


def run_experiment(
    algorithm_name: str, heuristic_name: str, initial_state: str, max_steps: int
) -> Dict[str, Any]:
    """Run a single experiment with the given parameters."""
    # Create the puzzle from the initial state
    puzzle = Puzzle.from_string(initial_state)

    # Get the search algorithm
    if algorithm_name not in SEARCH_ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {algorithm_name}")
    search_class = SEARCH_ALGORITHMS[algorithm_name]
    search = search_class(max_steps=max_steps)

    # Get the heuristic function
    if heuristic_name not in HEURISTICS:
        raise ValueError(f"Unknown heuristic: {heuristic_name}")
    heuristic_func = HEURISTICS[heuristic_name]

    # Run the search
    start_time = time.time()
    goal_node = search.search(puzzle, heuristic_func)
    elapsed_time = time.time() - start_time

    # Collect and return results
    result = {
        "algorithm": algorithm_name,
        "heuristic": heuristic_name,
        "initial_state": format_state(puzzle.state),
        "time": elapsed_time,
        "nodes_expanded": search.nodes_expanded,
        "nodes_generated": search.nodes_generated,
    }

    if goal_node:
        solution_path = goal_node.get_solution_path()
        result["solution_found"] = True
        result["solution_length"] = len(solution_path) - 1  # Exclude initial state
        result["solution_path"] = solution_path
        result["formatted_path"] = format_path(solution_path)
    else:
        result["solution_found"] = False
        result["solution_length"] = None
        result["solution_path"] = None
        result["formatted_path"] = None

    return result


def run_all_experiments(
    states: List[str], max_steps: int
) -> Dict[str, List[Dict[str, Any]]]:
    """Run all combinations of algorithms and heuristics on all states."""
    results = {}

    for algorithm_name in SEARCH_ALGORITHMS:
        for heuristic_name in HEURISTICS:
            key = f"{algorithm_name}-{heuristic_name}"
            results[key] = []

            for state in states:
                try:
                    result = run_experiment(
                        algorithm_name=algorithm_name,
                        heuristic_name=heuristic_name,
                        initial_state=state,
                        max_steps=max_steps,
                    )
                    results[key].append(result)
                except Exception as e:
                    print(f"Error running {key} on {state}: {e}")

    return results


def print_results(results: Dict[str, List[Dict[str, Any]]]):
    """Print formatted results to the console."""
    for key, experiments in results.items():
        if "-" in key:
            algorithm, heuristic = key.rsplit("-", 1)
        else:
            algorithm, heuristic = key, ""

        print(f"\n{algorithm.upper()} SEARCH:")
        print(f"Heuristic: {heuristic}")

        # Calculate average steps
        successful_experiments = [exp for exp in experiments if exp["solution_found"]]
        if successful_experiments:
            avg_steps = sum(
                exp["solution_length"] for exp in successful_experiments
            ) / len(successful_experiments)
            print(f"Average number of steps: {avg_steps:.2f}\n")
        else:
            print("No successful solutions found.\n")

        # Print individual experiment results
        for i, exp in enumerate(experiments):
            print(f"Initial state {i+1}: {exp['initial_state']}")
            if exp["solution_found"]:
                print(f"Solution found in {exp['solution_length']} steps")
                print(f"Solution path: {exp['formatted_path']}")
            else:
                print("No solution found within the step limit.")
            print(f"Nodes expanded: {exp['nodes_expanded']}")
            print(f"Nodes generated: {exp['nodes_generated']}")
            print(f"Time taken: {exp['time']:.3f} seconds\n")


def generate_markdown_report(
    results: Dict[str, List[Dict[str, Any]]], output_path: str, size: int = 3
):
    """Generate a Markdown report of the experiment results."""
    with open(output_path, "w" if size == 3 else "a") as f:
        if size == 3:
            f.write("# 8-Puzzle Solver Experiment Results\n\n")
        else:  # size == 4
            f.write("\n\n# Extra Credit: 15-Puzzle (4×4) Results\n\n")

        # Summarize the heuristics used
        f.write("## Heuristics Used\n\n")
        f.write("### Heuristic 1: Misplaced Tiles\n")
        f.write("Counts the number of tiles that are not in their goal position.\n\n")

        f.write("### Heuristic 2: Manhattan Distance\n")
        f.write(
            "Sums the Manhattan distance (|x1 - x2| + |y1 - y2|) for each tile from its current position to its goal position.\n\n"
        )

        f.write("### Heuristic 3: Linear Conflict\n")
        f.write(
            "Combines Manhattan distance with a penalty for linear conflicts. A linear conflict occurs when two tiles are in their goal row/column but in the wrong order.\n\n"
        )

        # Results for each algorithm and heuristic
        # Get unique algorithms and heuristics from the keys
        algorithms = set()
        heuristics = set()

        for key in results.keys():
            if "-" in key:
                algorithm, heuristic = key.rsplit("-", 1)
                algorithms.add(algorithm)
                heuristics.add(heuristic)

        # Use the discovered algorithms and heuristics
        for algorithm in algorithms:
            f.write(f"## {algorithm.upper()} Search\n\n")

            for heuristic in heuristics:
                key = f"{algorithm}-{heuristic}"
                if key not in results:
                    continue

                experiments = results[key]
                f.write(f"### Heuristic: {heuristic}\n\n")

                # Calculate average steps
                successful_experiments = [
                    exp for exp in experiments if exp["solution_found"]
                ]
                if successful_experiments:
                    avg_steps = sum(
                        exp["solution_length"] for exp in successful_experiments
                    ) / len(successful_experiments)
                    f.write(f"Average number of steps: {avg_steps:.2f}\n\n")
                else:
                    f.write("No successful solutions found.\n\n")

                # Write individual experiment results
                for i, exp in enumerate(experiments):
                    f.write(f"#### Initial state {i+1}: {exp['initial_state']}\n")
                    if exp["solution_found"]:
                        f.write(f"Solution found in {exp['solution_length']} steps\n\n")
                        f.write(
                            f"Solution path:\n```\n{exp['formatted_path']}\n```\n\n"
                        )
                    else:
                        f.write("No solution found within the step limit.\n\n")
                    f.write(f"Nodes expanded: {exp['nodes_expanded']}\n")
                    f.write(f"Nodes generated: {exp['nodes_generated']}\n")
                    f.write(f"Time taken: {exp['time']:.3f} seconds\n\n")


def main():
    parser = argparse.ArgumentParser(description="Puzzle Solver (8-puzzle or 15-puzzle)")
    parser.add_argument(
        "--algorithm", choices=["best-first", "astar"], help="Search algorithm to use"
    )
    parser.add_argument(
        "--heuristic",
        choices=["misplaced", "manhattan", "linear_conflict"],
        help="Heuristic function to use",
    )
    parser.add_argument(
        "--state", type=str, help="Initial state (space-separated, use 0 for blank)"
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=10000,
        help="Maximum number of steps before giving up",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all combinations of algorithms and heuristics on all states",
    )
    parser.add_argument(
        "--size",
        type=int,
        choices=[8, 15],
        default=8,
        help="Puzzle size (8 for 8-puzzle, 15 for 15-puzzle)",
    )

    args = parser.parse_args()

    # Get the base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Convert size parameter to grid size (3 for 8-puzzle, 4 for 15-puzzle)
    grid_size = 3 if args.size == 8 else 4
    
    # Select appropriate files based on puzzle size
    states_file = os.path.join(base_dir, "data", f"initial_states_{args.size}.txt")
    report_file = os.path.join(base_dir, "reports", "results.md")

    if args.all:
        # Run all experiments
        states = read_initial_states(states_file, grid_size)
        print(f"Running all experiments on {len(states)} initial states ({grid_size}×{grid_size} grid)...")
        results = run_all_experiments(states, args.max_steps)
        print_results(results)
        generate_markdown_report(results, report_file, grid_size)
        print(f"\nDetailed report saved to {report_file}")
    elif args.algorithm and args.heuristic:
        # Run a single experiment
        if args.state:
            state = args.state
        else:
            # Use the first state from the file
            states = read_initial_states(states_file, grid_size)
            
            # Default state based on puzzle size
            default_state = "1 2 3 4 5 6 7 8 0" if grid_size == 3 else "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0"
            state = states[0] if states else default_state

        print(
            f"Running {args.algorithm} search with {args.heuristic} heuristic on state: {state}"
        )
        result = run_experiment(
            algorithm_name=args.algorithm,
            heuristic_name=args.heuristic,
            initial_state=state,
            max_steps=args.max_steps,
        )

        # Print result
        print(f"\nInitial state: {result['initial_state']}")
        if result["solution_found"]:
            print(f"Solution found in {result['solution_length']} steps")
            print(f"Solution path: {result['formatted_path']}")
        else:
            print("No solution found within the step limit.")
        print(f"Nodes expanded: {result['nodes_expanded']}")
        print(f"Nodes generated: {result['nodes_generated']}")
        print(f"Time taken: {result['time']:.3f} seconds")
    else:
        # Default: run all experiments
        states = read_initial_states(states_file, grid_size)
        print(f"Running all experiments on {len(states)} initial states ({grid_size}×{grid_size} grid)...")
        results = run_all_experiments(states, args.max_steps)
        print_results(results)
        generate_markdown_report(results, report_file, grid_size)
        print(f"\nDetailed report saved to {report_file}")


if __name__ == "__main__":
    main()
