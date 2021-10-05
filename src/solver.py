from typing import List

import numpy as np
from ortools.sat.python import cp_model

from grid import Grid, get_neighbours
from interface import GUI

EMPTY = 0
GRASS = 1
TENT = 2
TREE = 3


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, cells: List[cp_model.CpModel.NewIntVar]):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__cells = cells
        self.__solution_count = 0

    def OnSolutionCallback(self) -> None:
        self.__solution_count += 1
        for row in self.__cells:
            for cell in row:
                print(f"{self.Value(cell)} ", end=" ")
            print()
        print()

    def SolutionCount(self) -> int:
        return self.__solution_count


class CSPSolver:
    """CP-SAT wrapper to define the CSP, solve it and (optionnaly) display it."""

    def __init__(self, grid: Grid):
        self.grid = grid
        self.grid_dim = grid.dim
        self.row_constraints = grid.row_constraints
        self.col_constraints = grid.col_constraints
        self.model = self._get_model()

    def _get_model(self) -> cp_model.CpModel:
        """Define the model's constraints."""

        model = cp_model.CpModel()

        # Define variables
        self.cells = [
            [model.NewIntVar(GRASS, TREE, f"X_{i}_{j}") for j in range(self.grid_dim)]
            for i in range(self.grid_dim)
        ]
        bool_tents = [
            [model.NewBoolVar(f"bool_tents_{i}_{j}") for j in range(self.grid_dim)]
            for i in range(self.grid_dim)
        ]
        bool_trees = [
            [model.NewBoolVar(f"bool_trees_{i}_{j}") for j in range(self.grid_dim)]
            for i in range(self.grid_dim)
        ]

        # Define constraints
        # Tree cells
        for i in range(self.grid_dim):
            for j in range(self.grid_dim):
                if self.grid.grid[i][j] == TREE:
                    model.Add(self.cells[i][j] == TREE)
                else:
                    model.Add(self.cells[i][j] != TREE)

        # Set up tent and tree's boolean variables
        for i in range(self.grid_dim):
            for j in range(self.grid_dim):
                model.Add(self.cells[i][j] == TENT).OnlyEnforceIf(bool_tents[i][j])
                model.Add(self.cells[i][j] != TENT).OnlyEnforceIf(
                    bool_tents[i][j].Not()
                )
                model.Add(self.cells[i][j] == TREE).OnlyEnforceIf(bool_trees[i][j])
                model.Add(self.cells[i][j] != TREE).OnlyEnforceIf(
                    bool_trees[i][j].Not()
                )

        # Row constraints
        for i in range(self.grid_dim):
            model.Add(sum(bool_tents[i]) == self.row_constraints[i])

        # Columns constraints
        for i, col in enumerate(map(list, zip(*bool_tents))):
            model.Add(sum(col) == self.col_constraints[i])

        for i in range(self.grid_dim):
            for j in range(self.grid_dim):
                # One tent per tree
                tent_four_neighbours = get_neighbours(bool_tents, i, j)
                model.Add(sum(tent_four_neighbours) >= 1).OnlyEnforceIf(
                    bool_trees[i][j]
                )

                # One tree per tent
                tree_four_neighbours = get_neighbours(bool_trees, i, j)
                model.Add(sum(tree_four_neighbours) >= 1).OnlyEnforceIf(
                    bool_tents[i][j]
                )

                # Two tents cannot touch
                eight_neighbours = get_neighbours(bool_tents, i, j, k=8)
                model.Add(sum(eight_neighbours) == 0).OnlyEnforceIf(bool_tents[i][j])
                model.Add(sum(eight_neighbours) >= 0).OnlyEnforceIf(
                    bool_tents[i][j].Not()
                )

        return model

    def _fill_grid(self, solver: cp_model.CpSolver) -> None:
        for i in range(self.grid_dim):
            for j in range(self.grid_dim):
                self.grid.grid[i][j] = solver.Value(self.cells[i][j])

    def solve(self, use_gui: bool = False) -> None:
        """Solve the model and display a solution."""

        solver = cp_model.CpSolver()

        if use_gui:
            solver.Solve(self.model)
            self._fill_grid(solver)
            gui = GUI(self.grid)
            gui.display()
        else:
            print("Solved grid :")
            solution_printer = SolutionPrinter(self.cells)
            status = solver.SolveWithSolutionCallback(self.model, solution_printer)


if __name__ == "__main__":
    grid = Grid(10)
    print("Original grid :")
    print(grid)
    print()

    solver = CSPSolver(grid)
    solver.solve(use_gui=False)
