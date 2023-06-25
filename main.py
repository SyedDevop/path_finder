from typing import List, Tuple
import pygame  # type: ignore
from queue import PriorityQueue
import runner
from runner import Spot

INPUT = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
with open("./input.txt", "r") as file:
    al_maze, al_start, al_end = runner.part_one(file.read())

WIDTH = al_maze[0].__len__() * 10
HEIGH = al_maze.__len__() * 10
WIN = pygame.display.set_mode((WIDTH, HEIGH))
pygame.display.set_caption("A* Path Finder")


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)


Grid = List[List[Spot]]


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def _algorithm(draw, grid: Grid, start: Spot, end: Spot):
    count = 0
    open_set = PriorityQueue()  # type: ignore
    open_set.put((0, count, start))
    came_from = {}  # type: ignore
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current: Spot = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()

    return False


def make_grid(rows, cols, maze, width, height) -> Grid:
    grid: Grid = []
    gap = width // cols
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            spot = Spot(i, j, gap, maze[i][j], rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, cols, width, heigh):
    gap_c = width // cols
    gap_r = heigh // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap_r), (width, i * gap_r))
        for j in range(cols):
            pygame.draw.line(win, GREY, (j * gap_c, 0), (j * gap_c, width))


def draw(win, grid: Grid, rows, cols, width, heigh):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    # draw_grid(win, rows, cols, width, heigh)
    pygame.display.update()


def get_clicked_pos(pos, rows, width) -> Tuple[int, int]:
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col


def main(win, width, heigh):
    ROWS = al_maze.__len__()
    COLS = al_maze[0].__len__()
    grid = make_grid(ROWS, COLS, al_maze, width, heigh)
    start = grid[al_start[1]][al_start[0]]
    end = grid[al_end[1]][al_end[0]]

    run = True
    started = False

    start.make_start()
    end.make_end()
    while run:
        draw(win, grid, ROWS, COLS, width, heigh)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid, al_maze)

                    runner.a_start(
                        lambda: draw(win, grid, ROWS, COLS, width, heigh),
                        grid,
                        al_maze,
                        start,
                        end,
                    )

                if event.key == pygame.K_c:
                    start = grid[al_start[1]][al_start[0]]
                    end = grid[al_end[1]][al_end[0]]
                    grid = make_grid(ROWS, COLS, al_maze, width, heigh)

    pygame.quit()


main(WIN, WIDTH, HEIGH)
