import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from grid import Grid

main_resolution = (600, 600)
grid_resolution = (500, 500)

green = (63, 224, 87)
black = (14, 15, 18)
white = (235, 242, 252)
blue = (73, 85, 196)
red = (209, 46, 46)
purple = (138, 5, 153)

EMPTY = 0
GRASS = 1
TENT = 2
TREE = 3

class GUI:
    def __init__(self, grid):
        self.grid = grid

        pygame.init()
        self.window = pygame.display.set_mode(main_resolution)
        self.window.fill(green)

    def _draw_grid(self):
        grid_size = self.grid.dim
        width, height = grid_resolution
        offset = 50
        margin = 4
        cell_size = int((width - 2 * offset - (grid_size - 1) * margin) / grid_size)
        step = cell_size + 5
        font = pygame.font.SysFont("ubuntumono", cell_size // 2)

        # Draw cells' colors
        coord_x = offset
        for y in range(grid_size):
            coord_y = offset
            for x in range(grid_size):
                cell = pygame.Rect(coord_x, coord_y, cell_size, cell_size)
                if self.grid.grid[x][y] == EMPTY:
                    pygame.draw.rect(self.window, black, cell)
                elif self.grid.grid[x][y] == GRASS:
                    pygame.draw.rect(self.window, green, cell)
                elif self.grid.grid[x][y] == TENT:
                    pygame.draw.rect(self.window, red, cell)
                elif self.grid.grid[x][y] == TREE:
                    pygame.draw.rect(self.window, purple, cell)
                coord_y += step
            coord_x += step
        
        # Draw cells' borders
        for x in range(offset, height - offset, step):
            for y in range(offset, width - offset, step):
                cell = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(self.window, black, cell, 2)

        start = offset + (cell_size // 4)
        stop = height - cell_size
        # Display row constraints
        for y, row_constraint in zip(range(start, stop, step), self.grid.row_constraints):
            text = font.render(str(row_constraint), True, black)
            self.window.blit(text, [offset - 2 * text.get_width(), y])
        
        start = offset + (cell_size // 3)
        stop = width - cell_size
        # Display col constraints
        for x, col_constraint in zip(range(start, stop, step), self.grid.col_constraints):
            text = font.render(str(col_constraint), True, black)
            self.window.blit(text, [x, offset - text.get_height()])
    
    def display(self):
        pygame.init()
        window = pygame.display.set_mode(main_resolution)
        window.fill(green)

        self._draw_grid()
        pygame.display.flip()  # Refresh display
        
        launched = True
        while launched:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    launched = False
                if event.type == pygame.KEYUP: 
                    if event.key == pygame.K_ESCAPE:
                        launched = False
