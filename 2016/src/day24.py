import itertools
import math
from queue import SimpleQueue

from utils import aoc_input_file, make_grid, neighbours, read_file_str

# Puzzle description: https://adventofcode.com/2016/day/24

DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None


def find_numbers(grid):
    result = {}
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (grid[r][c]).isdigit():
                result[int(grid[r][c])] = (r, c)
    return result


def read_input(input_file):
    grid = read_file_str(aoc_input_file(__file__, input_file), True)
    return grid, find_numbers(grid)


def bfs(grid, start, end):
    q = SimpleQueue()
    q.put((start, 0))
    visited = set(start)

    while not q.empty():
        p, steps = q.get()

        if p == end:
            return steps

        for adj in neighbours(p, grid, True, lambda g, p: g[p[0]][p[1]] != "#"):
            if adj not in visited:
                visited.add(adj)
                q.put((adj, steps + 1))

    raise RuntimeError("No path found")


def solve(input, part2=False):
    grid, number_locations = input
    num_count = len(number_locations)
    distances = make_grid(num_count, num_count, 0)
    pairs = list(itertools.combinations(range(num_count), 2))

    # for each pair, find shortest distance between them using bfs
    for nodes in pairs:
        start = number_locations[nodes[0]]
        end = number_locations[nodes[1]]
        distance = bfs(grid, start, end)
        distances[nodes[0]][nodes[1]] = distance
        distances[nodes[1]][nodes[0]] = distance

    # find all perms of nodes (1..n)
    perms = list(itertools.permutations(range(1, num_count)))

    # shortest path to visit all the nodes for each perm
    result = math.inf
    for path in perms:
        path_steps = 0
        prev_node = 0
        for node in path:
            path_steps += distances[prev_node][node]
            prev_node = node

        if part2:
            path_steps += distances[prev_node][0]

        result = min(result, path_steps)

    return result


def main():
    input = read_input("day24.txt")
    test_input = read_input("day24-test.txt")

    assert (res := solve(test_input)) == 14, f"Actual: {res}"
    print(f"Part 1 {solve(input)}")  # 490

    print(f"Part 2 {solve(input, True)}")  # 744


if __name__ == "__main__":
    main()
