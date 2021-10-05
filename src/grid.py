from typing import List, Tuple

import numpy as np

MAX_TRIES = 10
EMPTY = 0
GRASS = 1
TENT = 2
TREE = 3


class BadGenerationException(Exception):
    """Get raised if we fail to generate a valid grid within MAX_TRIES tentatives."""

    pass


class Grid:
    def __init__(self, dim: int):
        """Creates an empty grid with row and col constraints."""

        self.dim = dim
        self.nb_tents = int(3.16 * dim - 10.83)
        done_generating = False

        while not done_generating:
            try:
                self.grid = np.zeros((dim, dim), dtype=int)
                self._place_tents(self.nb_tents)
                (
                    self.row_constraints,
                    self.col_constraints,
                ) = self._get_row_col_constraints()
                self._place_trees()
                self._remove_tents()
                done_generating = True
            except BadGenerationException:
                pass

    def __str__(self) -> str:
        res = str(self.grid)
        res += "\nrow: {}".format(self.row_constraints)
        res += "\ncol: {}".format(self.col_constraints)

        return res

    def _place_tents(self, nb_tents: int):
        for _ in range(nb_tents):
            placed = False
            tries = 0
            while not placed:
                if tries > MAX_TRIES:
                    raise BadGenerationException

                x = np.random.randint(0, self.dim)
                y = np.random.randint(0, self.dim)
                neighbours = get_neighbours(
                    self.grid, x, y, filter_none_values=False, k=8
                )
                if self.grid[x][y] != TENT and TENT not in neighbours:
                    self.grid[x][y] = TENT
                    placed = True
                tries += 1

    def _place_trees(self):
        for x in range(self.dim):
            for y in range(self.dim):
                if self.grid[x][y] == TENT:
                    neighbours = get_neighbours(
                        self.grid, x, y, filter_none_values=False
                    )
                    placed = False
                    tries = 0
                    while placed is False:
                        if tries > MAX_TRIES:
                            raise BadGenerationException

                        i = np.random.randint(0, 4)
                        if neighbours[i] == 0:
                            if i == 0:
                                self.grid[x - 1][y] = TREE
                            if i == 1:
                                self.grid[x][y + 1] = TREE
                            if i == 2:
                                self.grid[x + 1][y] = TREE
                            if i == 3:
                                self.grid[x][y - 1] = TREE
                            placed = True
                        tries += 1

    def _remove_tents(self):
        for x in range(self.dim):
            for y in range(self.dim):
                if self.grid[x][y] == TENT:
                    self.grid[x][y] = EMPTY

    def _get_row_col_constraints(self) -> Tuple[List[int], List[int]]:
        row_constraints = []
        col_constraints = []
        for r in self.grid:
            row_constraints.append(np.sum([1 for i in r if i == TENT], dtype=int))
        for c in self.grid.T:
            col_constraints.append(np.sum([1 for i in c if i == TENT], dtype=int))

        return row_constraints, col_constraints


def get_neighbours(
    array: List[List[int]], x: int, y: int, filter_none_values: bool = True, k: int = 4
) -> List[int]:
    """Returns a list of 4 (k=4) or 8 (k=8) neighbours
    of the cell (x, y).

    k = 4       k = 8
    _ 0 _       0 1 2
    3 x 1       7 x 3
    _ 2 _       6 5 4

    """
    dim = len(array)
    neighbours = []
    if k == 4:
        if x - 1 < 0:
            neighbours.append(None)
        else:
            neighbours.append(array[x - 1][y])
        if y + 1 >= dim:
            neighbours.append(None)
        else:
            neighbours.append(array[x][y + 1])
        if x + 1 >= dim:
            neighbours.append(None)
        else:
            neighbours.append(array[x + 1][y])
        if y - 1 < 0:
            neighbours.append(None)
        else:
            neighbours.append(array[x][y - 1])

    else:
        # k == 8
        if x - 1 < 0 or y - 1 < 0:
            neighbours.append(None)
        else:
            neighbours.append(array[x - 1][y - 1])

        if x - 1 < 0:
            neighbours.append(None)
        else:
            neighbours.append(array[x - 1][y])

        if x - 1 < 0 or y + 1 >= dim:
            neighbours.append(None)
        else:
            neighbours.append(array[x - 1][y + 1])

        if y + 1 >= dim:
            neighbours.append(None)
        else:
            neighbours.append(array[x][y + 1])

        if x + 1 >= dim or y + 1 >= dim:
            neighbours.append(None)
        else:
            neighbours.append(array[x + 1][y + 1])

        if x + 1 >= dim:
            neighbours.append(None)
        else:
            neighbours.append(array[x + 1][y])

        if x + 1 >= dim or y - 1 < 0:
            neighbours.append(None)
        else:
            neighbours.append(array[x + 1][y - 1])

        if y - 1 < 0:
            neighbours.append(None)
        else:
            neighbours.append(array[x][y - 1])

    if filter_none_values:
        neighbours = [n for n in neighbours if n]

    return neighbours
