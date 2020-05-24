import argparse
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from grid import Grid
from solver import naive_solve, CSPSolver
from interface import GUI


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-gd", "--grid-dimension",
                        help="specify the grid dimension", type=int)
    parser.add_argument(
        "-s", "--solver", choices=["naive", "cpsat"], help="specify the solver to use", type=str)

    args = parser.parse_args()

    if args.grid_dimension:
        grid = Grid(args.grid_dimension)
    else:
        grid = Grid()

    if args.solver == "naive":
        solved_grid = naive_solve(grid)
        gui = GUI(solved_grid)
        gui.display()
    else:
        solver = CSPSolver(grid)
        solver.solve(use_gui=True)


if __name__ == "__main__":
    main()
