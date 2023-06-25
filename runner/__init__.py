import math
from typing import List, Tuple
import pygame  # type: ignore
from queue import PriorityQueue

Maze = list[list[str]]
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
YELLOW = (255,255,0)

class Spot:
    def __init__(self, row, col, width, letter, total_rows) -> None:
        c = ((ord(letter) - 97) * 255) // 25

        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = col * width
        self.y = row * width
        self.color = (c, c, c)
        self.neighbors: List[Spot] = []
        self.letter = letter

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
        self.color = YELLOW

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid, maze):
        y, x = self.get_pos()
        cur_car = ord(self.letter)

        if y < maze.__len__() - 1 and ord(maze[y + 1][x]) <= cur_car + 1:  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        # /////////-----___-----////////
        if y > 0 and ord(maze[y - 1][x]) <= cur_car + 1:  # Up
            self.neighbors.append(grid[self.row - 1][self.col])
        # /////////-----___-----////////
        if x < maze[y].__len__() - 1 and ord(maze[y][x + 1]) <= cur_car + 1:  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        # /////////-----___-----////////
        if x > 0 and ord(maze[y][x - 1]) <= cur_car + 1:  # LEST
            self.neighbors.append(grid[self.row][self.col - 1])
        # /////////-----___-----////////

    def __lt__(self, other):
        return False

    def __str__(self):
        return f"Spot: {self.letter} : r = {self.row} c ={self.col} "

    def __repr__(self):
        return f"Spot: {self.letter} : r = {self.row} c ={self.col} "


def get_start_pos(maze: Maze) -> Tuple[int, int] | None:
    """
    This function returns the starting position of S in the maze as a tuple of (x, y)
    coordinates.

    :param maze: A Maze object representing the maze.
    :return: A tuple of (x, y) coordinates representing the starting position of the
    maze,or `None` if the starting position is not found.
    """
    for y in range(maze.__len__()):
        for x in range(maze[y].__len__()):
            if ord(maze[y][x]) == ord("S"):
                return (x, y)
    return None


Grid = list[list[Spot]]


def get_end_pos(maze: Maze) -> Tuple[int, int] | None:
    """
    This function returns the ending position of E in the maze as a tuple of (x, y)
    coordinates.

    :param maze: A Maze object representing the maze.
    :return: A tuple of (x, y) coordinates representing the ending position of the
    maze,or `None` if the starting position is not found.
    """
    for y in range(maze.__len__()):
        for x in range(maze[y].__len__()):
            if ord(maze[y][x]) == ord("E"):
                return (x, y)
    return None


def get_neighbors(cur: Spot, grid: Grid, maze: Maze) -> List[Spot]:
    nei_list = []
    x, y = cur.get_pos()
    letter = maze[y][x]
    cur_car = ord(letter)

    if y < maze.__len__() - 1 and ord(maze[y + 1][x]) <= cur_car + 1:  # DOWN
        nei_list.append(grid[y + 1][x])
    if y > 0 and ord(maze[y - 1][x]) <= cur_car + 1:  # UP
        nei_list.append(grid[y - 1][x])
    if x < maze[y].__len__() - 1 and ord(maze[y][x + 1]) <= cur_car + 1:  # RIGHT
        print(grid[cur.row].__len__(), "grid len")
        print(cur.col + 1, "Cur num ")
        nei_list.append(grid[cur.row][cur.col + 1])
    if x > 0 and ord(maze[y][x - 1]) <= cur_car + 1:  # LEFT
        print(grid[cur.row].__len__())
        print(cur.col - 1)
        nei_list.append(grid[cur.row][cur.col - 1])
    return nei_list


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def a_start(draw, grid: Grid, maze: Maze, start: Spot, end: Spot):
    open_set = PriorityQueue()  # type: ignore
    open_set.put((0, start))
    came_from = {}  # type: ignore
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}
    while not open_set.empty():
        current: Spot = open_set.get()[1]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()

        for neighbour in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(
                    neighbour.get_pos(), end.get_pos()
                )
                if neighbour not in open_set_hash:
                    open_set.put((f_score[neighbour], neighbour))
                    open_set_hash.add(neighbour)
    return 0.0


# def dijkstra(grid: Grid, maze: Maze, start: Tuple[int, int], end: Tuple[int, int]):
#     open_set = PriorityQueue()  # type: ignore
#     open_set.put((0, start))
#     came_from = {}  # type: ignore
#     g_score = {spot: float("inf") for row in grid for spot in row}
#     g_score[start] = 0
#     open_set_hash = {start}
#     while not open_set.empty():
#         current = open_set.get()[1]
#         open_set_hash.remove(current)
#
#         # if current == end:
#         #     path = []
#         #     while current in came_from:
#         #         current = came_from[current]
#         #         path.append(current)
#         #     path.reverse()
#         #     return path.__len__()
#
#         for neighbour in get_neighbors(current, maze):
#             temp_g_score = g_score[current] + 1
#
#             if temp_g_score < g_score[neighbour]:
#                 came_from[current] = neighbour
#                 g_score[neighbour] = temp_g_score
#                 if neighbour not in open_set_hash:
#                     open_set.put((g_score[neighbour], neighbour))
#                     open_set_hash.add(neighbour)
#     cur = (5, 3)
#     path = []
#     print(cur)
#     print(came_from.__len__())
#     while cur in came_from:
#         cur = came_from[cur]
#         path.append(cur)
#     print(path.__len__())
#     return


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)


Star = Tuple[int, int]
End = Tuple[int, int]


def part_one(data: str) -> Tuple[Maze, Star, End]:
    maze: Maze = [[*i] for i in data.split("\n") if i.__len__() > 0]
    start = get_start_pos(maze) or (0, 0)
    end = get_end_pos(maze) or (0, 0)

    # if start and end:
    maze[start[1]][start[0]] = "a"
    maze[end[1]][end[0]] = "z"
    #     return algorithm(grid, maze, start, end)
    return (maze, start, end)
