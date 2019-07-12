import pygame
from grid import Grid
from solver import solve

main_resolution = (640, 550)
grid_resolution = (500, 500)
green = (63, 224, 87)
black = (14, 15, 18)
white = (235, 242, 252)
blue = (73, 85, 196)
red = (209, 46, 46)
purple = (138, 5, 153)

def draw_grid(grid, window):
    grid_size = grid.dim
    width, height = grid_resolution
    offset = 10
    margin = 4
    cell_size = int((width - 2 * offset - (grid_size - 1) * margin) / grid_size)
    step = cell_size + 5
    coord_x, coord_y = 0, 0

    for x in range(offset, height - cell_size, step):
        coord_y = 0
        for y in range(offset, width - cell_size, step):
            cell = pygame.Rect(x, y, cell_size, cell_size)
            if grid.grid[coord_x][coord_y] == 0:
                pygame.draw.rect(window, black, cell)
            if grid.grid[coord_x][coord_y] == 1:
                pygame.draw.rect(window, green, cell)
            if grid.grid[coord_x][coord_y] == 2:
                pygame.draw.rect(window, red, cell)
            if grid.grid[coord_x][coord_y] == 3:
                pygame.draw.rect(window, purple, cell)
            coord_y += 1
        coord_x += 1
    
    for x in range(offset, height - cell_size, step):
        for y in range(offset, width - cell_size, step):
            cell = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(window, black, cell, 2)

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode(main_resolution)
    window.fill(green)
    grid = Grid(5)
    solve(grid)

    draw_grid(grid, window)

    pygame.display.flip()  # Actualise l'affichage

    launched = True

    while launched:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False
