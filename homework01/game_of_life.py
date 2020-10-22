from typing import Tuple, Set, List

# Homework 01 - Game of life
# 
# Your task is to implement part of the cell automata called
# Game of life. The automata is a 2D simulation where each cell
# on the grid is either dead or alive.
# 
# State of each cell is updated in every iteration based state of neighbouring cells.
# Cell neighbours are cells that are horizontally, vertically, or diagonally adjacent.
#
# Rules for update are as follows:
# 
# 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# 2. Any live cell with two or three live neighbours lives on to the next generation.
# 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
# 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
#
# 
# Our implementation will use coordinate system will use grid coordinates starting from (0, 0) - upper left corner.
# The first coordinate is row and second is column.
# 
# Do not use wrap around (toroid) when reaching edge of the board.
# 
# For more details about Game of Life, see Wikipedia - https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

neighbours = {(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, 1), (1, -1)}


def count_neighbours(alive: Set[Tuple[int, int]], current: Tuple[int, int]) -> int:
    count = 0
    for (y, x) in neighbours:
        if (current[0] + y, current[1] + x) in alive:
            count += 1
    return count


def update(alive: Set[Tuple[int, int]], size: Tuple[int, int], iter_n: int) -> Set[Tuple[int, int]]:
    if iter_n == 0:
        return alive
    new_alive = set()
    for y in range(size[0]):
        for x in range(size[1]):
            cn = count_neighbours(alive, (y, x))
            if cn == 3 or ((y, x) in alive and cn == 2):
                new_alive.add((y, x))
    return update(new_alive, size, iter_n - 1)


def draw(alive: Set[Tuple[int, int]], size: Tuple[int, int]) -> str:
    output: List[str] = ['+']
    for x in range(size[1]):
        output.append('-')
    output.append("+\n")
    for y in range(size[0]):
        output.append('|')
        for x in range(size[1]):
            if (y, x) in alive:
                output.append('X')
            else:
                output.append(' ')
        output.append("|\n")
    output.append('+')
    for x in range(size[1]):
        output.append('-')
    output.append("+")
    return ''.join(output)
