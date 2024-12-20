import sys
import os
import re
from queue import SimpleQueue

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/18

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

BYTE = '#'
FREE = '.'


def read_input(input_file):
    input = []
    for p in read_file_str(input_file, True):
        match = re.findall(r'(\d+)', p)
        # coods provided as x, y; store as r, c
        input.append((int(match[1]), int(match[0])))

    return input


def solve(grid, start, end):
    def move_condition(g, x): return g[x[0]][x[1]] == FREE
    result = set()
    q = SimpleQueue()

    q.put((start, 0))

    visited = set()
    visited.add(start)

    while not q.empty():
        pos, cost = q.get()

        for adj in neighbours(pos, grid, True, move_condition):
            if adj in visited:
                continue
            if adj == end:
                result.add(cost + 1)
            else:
                visited.add(adj)
                q.put((adj, cost + 1))

    return min(result) if len(result) > 0 else -1


def new_grid(input, grid_size, bytes):
    grid = make_grid(grid_size, grid_size, FREE)

    for p in input[0:bytes]:
        grid[p[0]][p[1]] = BYTE

    return grid


def part1(input, start, end, grid_size, bytes):
    grid = new_grid(input, grid_size, bytes)
    return solve(grid, start, end)


def part2(input, start, end, grid_size, bytes):
    grid = new_grid(input, grid_size, bytes)
    for p in input[bytes:]:
        grid[p[0]][p[1]] = '#'
        if solve(grid, start, end) == -1:
            return (p[1], p[0])  # provide as X,Y for submission

    return 0


def main():
    input = read_input("../data/day18.txt")
    test_input = read_input("../data/day18-test.txt")

    assert (res := part1(test_input, (0, 0), (6, 6), 7, 12)
            ) == 22, f'Actual: {res}'
    print(f'Part 1 {part1(input, (0, 0), (70, 70), 71, 1024)}')  # 380

    assert (res := part2(test_input, (0, 0), (6, 6), 7, 12)) == (
        6, 1), f'Actual: {res}'
    print(f'Part 2 {part2(input, (0, 0), (70, 70), 71, 1024)}')  # 26,50 (X, Y)


if __name__ == '__main__':
    main()
