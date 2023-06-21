from typing import List, Tuple
import pygame  # type: ignore
from queue import PriorityQueue
import runner

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
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


class Spot:
    def __init__(self, row, col, width, total_rows) -> None:
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors: List[Spot] = []

    def get_pos(self) -> Tuple[int, int]:
        return (self.row, self.col)

    def is_closed(self) -> bool:
        return self.color == RED

    def is_open(self) -> bool:
        return self.color == GREEN

    def is_barrier(self) -> bool:
        return self.color == BLACK

    def is_start(self) -> bool:
        return self.color == ORANGE

    def is_end(self) -> bool:
        return self.color == TURQUOISE

    def reset(self) -> None:
        self.color = WHITE

    def make_start(self) -> None:
        self.color = ORANGE

    def make_closed(self) -> None:
        self.color = RED

    def make_open(self) -> None:
        self.color = GREEN

    def make_barrier(self) -> None:
        self.color = BLACK

    def make_end(self) -> None:
        self.color = TURQUOISE

    def make_path(self) -> None:
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        if (
            self.row < self.total_rows - 1
            and not grid[self.row + 1][self.col].is_barrier()
        ):  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        # /////////-----___-----////////
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # Up
            self.neighbors.append(grid[self.row - 1][self.col])
        # /////////-----___-----////////
        if (
            self.col < self.total_rows - 1
            and not grid[self.row][self.col + 1].is_barrier()
        ):  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        # /////////-----___-----////////
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEST
            self.neighbors.append(grid[self.row][self.col - 1])
        # /////////-----___-----////////

    def __lt__(self, other):
        return False

    def __str__(self):
        return "Spot"


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


def make_grid(rows, cols, width) -> Grid:
    grid: Grid = []
    gap = width // cols
    for i in range(cols):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, cols, width):
    gap = width // cols
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(cols):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid: Grid, rows, cols, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, cols, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width) -> Tuple[int, int]:
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col


INPUT = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


def main(win, width):
    al_maze, al_start, al_end = runner.part_one(INPUT)
    ROWS = al_maze.__len__()
    COLS = al_maze[0].__len__()
    grid = make_grid(ROWS, COLS, width)
    start = grid[al_start[1]][al_start[0]]
    end = grid[5][2]
    run = True
    started = False
    print(al_end)
    start.make_start()
    end.make_end()
    while run:
        draw(win, grid, ROWS, COLS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            # if pygame.mouse.get_pressed()[0]:
            #     pos = pygame.mouse.get_pos()
            #     row, col = get_clicked_pos(pos, ROWS, width)
            #     spot = grid[row][col]
            #     if not start and spot != end:
            #         start = spot
            #         start.make_start()
            #
            #     elif not end and spot != start:
            #         end = spot
            #         end.make_end()
            #
            #     elif spot not in [end, start]:
            #         spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    # algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, COLS, width)

    pygame.quit()


main(WIN, WIDTH)
