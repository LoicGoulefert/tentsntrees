import pygame
from grid import Grid
from solver import solve

main_resolution = (720, 640)
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
    offset = 50
    margin = 4
    cell_size = int((width - 2 * offset - (grid_size - 1) * margin) / grid_size)
    step = cell_size + 5
    font = pygame.font.SysFont("ubuntumono", cell_size // 2)

    # Draw cells' colors
    coord_x = offset
    for y in range(grid.dim):
        coord_y = offset
        for x in range(grid.dim):
            cell = pygame.Rect(coord_x, coord_y, cell_size, cell_size)
            if grid.grid[x][y] == 0:
                pygame.draw.rect(window, black, cell)
            if grid.grid[x][y] == 1:
                pygame.draw.rect(window, green, cell)
            if grid.grid[x][y] == 2:
                pygame.draw.rect(window, red, cell)
            if grid.grid[x][y] == 3:
                pygame.draw.rect(window, purple, cell)
            coord_y += step
        coord_x += step
    
    # Draw cells' borders
    for x in range(offset, height - offset, step):
        for y in range(offset, width - offset, step):
            cell = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(window, black, cell, 2)

    start = offset + (cell_size // 4)
    stop = height - cell_size
    # Display row constraints
    for y, row_constraint in zip(range(start, stop, step), grid.row_constraints):
        text = font.render(str(row_constraint), True, black)
        window.blit(text, [offset // 3, y])
    
    start = offset + (cell_size // 3)
    stop = width - cell_size
    # Display col constraints
    for x, col_constraint in zip(range(start, stop, step), grid.col_constraints):
        text = font.render(str(col_constraint), True, black)
        window.blit(text, [x, offset - text.get_height()])


if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode(main_resolution)
    window.fill(green)
    grid = Grid(10)
    solve(grid)

    draw_grid(grid, window)

    pygame.display.flip()  # Actualise l'affichage

    launched = True

    while launched:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False
