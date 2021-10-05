import argparse
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from grid import Grid
from solver import CSPSolver


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-gd", "--grid-dimension", help="specify the grid dimension", type=int
    )
    args = parser.parse_args()

    if args.grid_dimension:
        grid = Grid(args.grid_dimension)
    else:
        grid = Grid(dim=7)

    solver = CSPSolver(grid)
    solver.solve(use_gui=True)


if __name__ == "__main__":
    main()
