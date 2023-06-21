from typing import List, Tuple

from queue import PriorityQueue

Maze = list[list[str]]
Grid = list[list[Tuple[int, int]]]


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


def get_neighbors(cur: Tuple[int, int], maze: Maze) -> List[Tuple[int, int]]:
    nei_list = []
    x, y = cur
    letter = maze[y][x]
    cur_car = ord(letter)

    if y < maze.__len__() - 1 and ord(maze[y + 1][x]) <= cur_car + 1:  # DOWN
        nei_list.append((x, y + 1))
    if y > 0 and ord(maze[y - 1][x]) <= cur_car + 1:  # UP
        nei_list.append((x, y - 1))
    if x < maze[y].__len__() - 1 and ord(maze[y][x + 1]) <= cur_car + 1:  # RIGHT
        nei_list.append((x + 1, y))
    if x > 0 and ord(maze[y][x - 1]) <= cur_car + 1:  # LEFT
        nei_list.append((x - 1, y))
    return nei_list


def a_start(grid: Grid, maze: Maze, start: Tuple[int, int], end: Tuple[int, int]):
    open_set = PriorityQueue()  # type: ignore
    open_set.put((0, start))
    came_from = {}  # type: ignore
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start, end)
    open_set_hash = {start}
    while not open_set.empty():
        current = open_set.get()[1]
        open_set_hash.remove(current)

        if current == end:
            path = []
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path.__len__()

        for neighbour in get_neighbors(current, maze):
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour, end)
                if neighbour not in open_set_hash:
                    open_set.put((f_score[neighbour], neighbour))
                    open_set_hash.add(neighbour)
    return 0.0


def dijkstra(grid: Grid, maze: Maze, start: Tuple[int, int], end: Tuple[int, int]):
    open_set = PriorityQueue()  # type: ignore
    open_set.put((0, start))
    came_from = {}  # type: ignore
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    open_set_hash = {start}
    while not open_set.empty():
        current = open_set.get()[1]
        open_set_hash.remove(current)

        # if current == end:
        #     path = []
        #     while current in came_from:
        #         current = came_from[current]
        #         path.append(current)
        #     path.reverse()
        #     return path.__len__()

        for neighbour in get_neighbors(current, maze):
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[current] = neighbour
                g_score[neighbour] = temp_g_score
                if neighbour not in open_set_hash:
                    open_set.put((g_score[neighbour], neighbour))
                    open_set_hash.add(neighbour)
    cur = (5, 3)
    path = []
    print(cur)
    print(came_from.__len__())
    while cur in came_from:
        cur = came_from[cur]
        path.append(cur)
    print(path.__len__())
    return


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
