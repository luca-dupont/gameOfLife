import pygame as pg
import numpy as np
from random import randint

W, H = 600, 600

pg.init()
pg.font.init()

font = pg.font.Font(None, 35)
smallFont = pg.font.Font(None, 25)

screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()

pg.key.set_repeat(200, 50)

BLACK = (0, 0, 0)
GREY = (200, 200, 200)

running = True

GRID_SIZE = 100

CELL_WIDTH = W / GRID_SIZE
CELL_HEIGHT = H / GRID_SIZE


framerate = 60


def reset():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    # seed
    for row in range(GRID_SIZE):
        for column in range(GRID_SIZE):
            if randint(0, 10) == 0:
                grid[row][column] = 1
    return grid


def reset_glider():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    # Glider pattern
    glide1 = [
        [1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1],
    ]

    glider2 = [
        [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            0,
            1,
            1,
            1,
            1,
            1,
            0,
            0,
            0,
            1,
            1,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            0,
            1,
            1,
            1,
            1,
            1,
        ]
    ]

    # Place the glider pattern in the grid
    start_row = 30  # Starting row index for the glider
    start_column = 50  # Starting column index for the glider
    for i in range(len(glider2)):
        for j in range(len(glider2[0])):
            grid[start_row + j][start_column + i] = glider2[i][j]

    return grid


# initialize
grid = reset_glider()


def check_neighbours(row, column):
    # Initialize live neighbor count
    live = 0

    # Loop through the neighborhood
    for i in range(max(0, row - 1), min(GRID_SIZE, row + 2)):
        for j in range(max(0, column - 1), min(GRID_SIZE, column + 2)):
            # Exclude the current cell
            if i != row or j != column:
                # Count live neighbors
                if 0 <= i < grid.shape[0] and 0 <= j < grid.shape[1]:
                    live += grid[i][j]

    # Apply the rules of Conway's Game of Life
    if grid[row][column] == 1:
        if live < 2 or live > 3:
            return 0  # Cell dies due to underpopulation or overpopulation
        else:
            return 1  # Cell survives
    else:
        if live == 3:
            return 1  # Cell becomes alive due to reproduction
        else:
            return 0  # Cell remains dead


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                grid = reset()
            elif event.key == pg.K_RETURN:
                framerate = 5 if framerate == 60 else 60

    # Create a new grid to hold the updated values
    new_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

    # update each cell
    for row in range(GRID_SIZE):
        for column in range(GRID_SIZE):
            new_grid[row][column] = check_neighbours(row, column)

    # Update the original grid with the changes
    grid = new_grid.copy()

    # Draw the updated grid
    for row in range(GRID_SIZE):
        for column in range(GRID_SIZE):
            color = GREY if grid[row][column] == 1 else BLACK
            pg.draw.rect(
                screen,
                color,
                (row * CELL_WIDTH, column * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT),
            )

    change_speed_text = smallFont.render("Press ENTER to change speed.", True, "white")
    reset_text = smallFont.render("Press SPACE to reset generation.", True, "white")

    speed_text = font.render("Slow" if framerate == 5 else "Normal", True, "white")

    screen.blit(change_speed_text, (10, 10))
    screen.blit(reset_text, (10, 35))

    screen.blit(speed_text, (W // 2 - 40, H - 30))

    clock.tick(framerate)
    pg.display.flip()

pg.quit()
