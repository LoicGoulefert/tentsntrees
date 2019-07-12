import numpy as np

MAX_TRIES = 10

class BadGenerationException(Exception):
    """ Get raised if we fail to generate a valid grid
    within MAX_TRIES tentatives.
    """
    pass


class Grid():
    def __init__(self, dim):
        """ Creates an empty grid with row and col constraints.
        0 -> BLANK
        1 -> GRASS
        2 -> TENT
        3 -> TREE
        """
        self.dim = dim
        self.nb_tents = int(3.16 * dim - 10.83)
        done_generating = False
        while done_generating is False:
            try:
                self.grid = np.zeros((dim, dim), dtype=int)
                self._place_tents(self.nb_tents)
                self.row_constraints, self.col_constraints = self._get_row_col_constraints()
                self._place_trees()
                self._remove_tents()
                done_generating = True
            except BadGenerationException:
                print("Generating again...")
        self.graph = self._build_graph()


    def __str__(self):
        res = str(self.grid)
        res += "\nrow: {}".format(self.row_constraints)
        res += "\ncol: {}".format(self.col_constraints)
        # res += "\ngraph: {}".format(self.graph)
        return res

    def _place_tents(self, nb_tents):
        for _ in range(nb_tents):
            placed = False
            tries = 0
            while placed is False:
                if tries > MAX_TRIES:
                    raise BadGenerationException
                
                x = np.random.randint(0, self.dim)
                y = np.random.randint(0, self.dim)
                neighbours = self.get_neighbours(x, y, k=8)
                if self.grid[x][y] != 2 and 2 not in neighbours:
                    self.grid[x][y] = 2
                    placed = True
                tries += 1


    def _place_trees(self):
        for x in range(self.dim):
            for y in range(self.dim):
                if self.grid[x][y] == 2:
                    neighbours = self.get_neighbours(x, y)
                    placed = False
                    tries = 0
                    while placed is False:
                        if tries > MAX_TRIES:
                            raise BadGenerationException
                        
                        i = np.random.randint(0, 4)
                        if neighbours[i] == 0:
                            if i == 0:
                                self.grid[x-1][y] = 3
                            if i == 1:
                                self.grid[x][y+1] = 3
                            if i == 2:
                                self.grid[x+1][y] = 3
                            if i == 3:
                                self.grid[x][y-1] = 3
                            placed = True
                        tries += 1


    def _remove_tents(self):
        for x in range(self.dim):
            for y in range(self.dim):
                if self.grid[x][y] == 2:
                    self.grid[x][y] = 0


    def _get_row_col_constraints(self):
        row_constraints = []
        col_constraints = []
        for r in self.grid:
            row_constraints.append(np.sum([1 for i in r if i == 2], dtype=int))
        for c in self.grid.T:
            col_constraints.append(np.sum([1 for i in c if i == 2], dtype=int))

        return row_constraints, col_constraints


    def _build_graph(self):
        graph = dict()

        for x in range(self.dim):
            for y in range(self.dim):
                graph[(x, y)] = self.get_neighbours(x, y, k=8)
        
        return graph
    

    def get_neighbours(self, x, y, k=4):
        """ Returns a list of 4 (k=4) or 8 (k=8) neighbours
        of the cell (x, y).
        
        k = 4       k = 8
        _ 0 _       0 1 2
        3 x 1       7 x 3
        _ 2 _       6 5 4

        """
        neighbours = []
        if k == 4:
            if x - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append(self.grid[x-1][y])
            if y + 1 >= self.dim:
                neighbours.append(None)
            else:
                neighbours.append(self.grid[x][y+1])
            if x + 1 >= self.dim:
                neighbours.append(None)
            else:
                neighbours.append(self.grid[x+1][y])
            if y - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append(self.grid[x][y-1])
            
        else:
            # k == 8
            if x - 1 < 0 or y - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append(self.grid[x-1][y-1])
            
            if x - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append(self.grid[x-1][y])
            
            if x - 1 < 0 or y + 1 >= self.dim:
                neighbours.append(None)
            else:
                neighbours.append(self.grid[x-1][y+1])
            
            if y + 1 >= self.dim:
                neighbours.append(None)
            else:
                neighbours.append(self.grid[x][y+1])
            
            if x + 1 >= self.dim or y + 1 >= self.dim:
                neighbours.append(None)
            else:
                neighbours.append(self.grid[x+1][y+1])
            
            if x + 1 >= self.dim:
                neighbours.append(None)
            else:
                neighbours.append(self.grid[x+1][y])
            
            if x + 1 >= self.dim or y - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append(self.grid[x+1][y-1])
            
            if y - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append(self.grid[x][y-1])
            
        return neighbours


if __name__ == "__main__":
    grid = Grid(5)
    print(grid)