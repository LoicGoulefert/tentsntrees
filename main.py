import argparse

from grid import Grid
from solver import solve
from interface import GUI


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-gd", "--grid-dimension", help="specify the grid dimension", type=int)
    
    args = parser.parse_args()
    
    if args.grid_dimension:
        grid = Grid(args.grid_dimension)
    else:
        grid = Grid()

    solved_grid = solve(grid)
    gui = GUI(solved_grid)
    gui.display()


if __name__ == "__main__":
    main()
