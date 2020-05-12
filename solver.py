import numpy as np
from ortools.sat.python import cp_model

from grid import Grid, get_neighbours
from interface import GUI


EMPTY = 0
GRASS = 1
TENT = 2
TREE = 3

k4_neighbours_coords = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def naive_solve(grid):
    """ Simple algorithm using the rules of the game to solve the grid. 

    This is often not enough to solve an instance of the problem.
    """

    dim = grid.dim
    solved = False
    previous_grid = np.copy(grid.grid)

    while not solved:
        # Placing grass cells according to constraints
        # Row constraints (empty)
        for x in range(dim):
            if grid.row_constraints[x] == 0:
                for y in range(dim):
                    if grid.grid[x][y] == EMPTY:
                        grid.grid[x][y] = GRASS

        # Row constraints (full)
        for x in range(dim):
            tents_count = np.sum([1 for cell in grid.grid[x] if cell == TENT])
            if tents_count == grid.row_constraints[x]:
                for y in range(dim):
                    if grid.grid[x][y] == EMPTY:
                        grid.grid[x][y] = GRASS

        # Column constraints (empty)
        for y in range(dim):
            if grid.col_constraints[y] == 0:
                for x in range(dim):
                    if grid.grid[x][y] == EMPTY:
                        grid.grid[x][y] = GRASS

        # Column constraints (full)
        for y in range(dim):
            tents_count = np.sum(
                [1 for cell in grid.grid.T[y] if cell == TENT])
            if tents_count == grid.col_constraints[y]:
                for x in range(dim):
                    if grid.grid[x][y] == EMPTY:
                        grid.grid[x][y] = GRASS

        # Placing grass cells according to 4-neighbours
        for x in range(dim):
            for y in range(dim):
                if grid.grid[x][y] == EMPTY:
                    neighbours = get_neighbours(
                        grid.grid, x, y, filter_none_values=False)
                    if TREE not in neighbours:
                        grid.grid[x][y] = GRASS

        # Placing tents according to constraints
        # Row constraints
        for x in range(dim):
            empty_count = np.sum([1 for cell in grid.grid[x] if cell == EMPTY])
            tents_count = np.sum([1 for cell in grid.grid[x] if cell == TENT])
            if empty_count == grid.row_constraints[x] - tents_count:
                for y in range(dim):
                    if grid.grid[x][y] == EMPTY:
                        grid.grid[x][y] = TENT

        # Column constrains
        for x in range(dim):
            empty_count = np.sum(
                [1 for cell in grid.grid.T[x] if cell == EMPTY])
            tents_count = np.sum(
                [1 for cell in grid.grid.T[x] if cell == TENT])
            if empty_count == grid.col_constraints[x] - tents_count:
                for y in range(dim):
                    if grid.grid.T[x][y] == EMPTY:
                        grid.grid.T[x][y] = TENT

        # Placing grass near tents
        for x in range(dim):
            for y in range(dim):
                if grid.grid[x][y] == EMPTY:
                    neighbours = get_neighbours(
                        grid.grid, x, y, filter_none_values=False, k=8)
                    if TENT in neighbours:
                        grid.grid[x][y] = GRASS

        # Placing tent next to tree if there's only 1 option
        for x in range(dim):
            for y in range(dim):
                if grid.grid[x][y] == TREE:
                    neighbours = get_neighbours(
                        grid.grid, x, y, filter_none_values=False)
                    empty_count = np.sum(
                        [1 for cell in neighbours if cell == EMPTY])
                    if TENT not in neighbours and empty_count == 1:
                        empty_index = neighbours.index(EMPTY)
                        n_x = x + k4_neighbours_coords[empty_index][0]
                        n_y = y + k4_neighbours_coords[empty_index][1]
                        grid.grid[n_x][n_y] = TENT

        if np.array_equal(previous_grid, grid.grid):
            print("Couldn't solve.")
            break
        else:
            previous_grid = np.copy(grid.grid)
        solved = not any(0 in cell for cell in grid.grid)

    if solved is True:
        print("Solved !")

    return grid


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, cells):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__cells = cells
        self.__solution_count = 0

    def OnSolutionCallback(self):
        self.__solution_count += 1
        for row in self.__cells:
            for cell in row:
                print(f"{self.Value(cell)} ", end=' ')
            print()
        print()

    def SolutionCount(self):
        return self.__solution_count


class CSPSolver():
    """ CP-SAT wrapper to define the CSP, solve it and (optionnaly) display it. """

    def __init__(self, grid):
        self.grid = grid
        self.grid_dim = grid.dim
        self.row_constraints = grid.row_constraints
        self.col_constraints = grid.col_constraints
        self.model = self._get_model()

    def _get_model(self):
        """ Define the model's constraints. """

        model = cp_model.CpModel()

        # Define variables
        self.cells = [[model.NewIntVar(GRASS, TREE, f"X_{i}_{j}") for j in range(
            self.grid_dim)] for i in range(self.grid_dim)]
        bool_tents = [[model.NewBoolVar(f"bool_tents_{i}_{j}") for j in range(
            self.grid_dim)] for i in range(self.grid_dim)]
        bool_trees = [[model.NewBoolVar(f"bool_trees_{i}_{j}") for j in range(
            self.grid_dim)] for i in range(self.grid_dim)]

        # Define constraints
        # Tree cells
        for i in range(self.grid_dim):
            for j in range(self.grid_dim):
                if self.grid.grid[i][j] == TREE:
                    model.Add(self.cells[i][j] == TREE)
                else:
                    model.Add(self.cells[i][j] != TREE)

        # Set up tent and tree's boolean variables
        for i in range(self.grid_dim):
            for j in range(self.grid_dim):
                model.Add(self.cells[i][j] == TENT).OnlyEnforceIf(
                    bool_tents[i][j])
                model.Add(self.cells[i][j] != TENT).OnlyEnforceIf(
                    bool_tents[i][j].Not())
                model.Add(self.cells[i][j] == TREE).OnlyEnforceIf(
                    bool_trees[i][j])
                model.Add(self.cells[i][j] != TREE).OnlyEnforceIf(
                    bool_trees[i][j].Not())

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
                model.Add(sum(tent_four_neighbours) >=
                          1).OnlyEnforceIf(bool_trees[i][j])

                # One tree per tent
                tree_four_neighbours = get_neighbours(bool_trees, i, j)
                model.Add(sum(tree_four_neighbours) >=
                          1).OnlyEnforceIf(bool_tents[i][j])

                # Two tents cannot touch
                eight_neighbours = get_neighbours(bool_tents, i, j, k=8)
                model.Add(sum(eight_neighbours) ==
                          0).OnlyEnforceIf(bool_tents[i][j])
                model.Add(sum(eight_neighbours) >= 0).OnlyEnforceIf(
                    bool_tents[i][j].Not())

        return model

    def _fill_grid(self, solver):
        for i in range(self.grid_dim):
            for j in range(self.grid_dim):
                self.grid.grid[i][j] = solver.Value(self.cells[i][j])

    def solve(self, use_gui=False):
        """ Solve the model and display a solution. """

        solver = cp_model.CpSolver()

        if use_gui:
            solver.Solve(self.model)
            self._fill_grid(solver)
            gui = GUI(self.grid)
            gui.display()
        else:
            print("Solved grid :")
            solution_printer = SolutionPrinter(self.cells)
            status = solver.SolveWithSolutionCallback(
                self.model, solution_printer)


if __name__ == "__main__":
    grid = Grid(10)
    print("Original grid :")
    print(grid)
    print()

    solver = CSPSolver(grid)
    solver.solve(use_gui=False)
