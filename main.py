import pygame

from grid import Grid
from solver import solve
from interface import GUI


def main():
    # TODO: Use argparse at some point
    grid = Grid(10)
    solved_grid = solve(grid)
    gui = GUI(solved_grid)
    gui.display()


if __name__ == "__main__":
    main()
