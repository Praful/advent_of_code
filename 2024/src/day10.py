import sys
import os
from queue import SimpleQueue

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/10


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input, find_in_grid(input, '0')


# use bfs to find all trails: part 1 requires unique destinations from trailheads
# and part 2 requires unique routes from trailheads to destinations
def solve(input, part2=False):
    result = 0
    grid, trailheads = input
    q = SimpleQueue()

    for pos in trailheads:
        q.put((pos, 0, pos))

    visited = set()

    while not q.empty():
        pos, height, trailhead = q.get()

        for adj in neighbours(pos, grid, True, lambda g, x: int(g[x[0]][x[1]]) == height + 1):
            if grid[adj[0]][adj[1]] == '9':
                if part2 or (trailhead, adj) not in visited:
                    result += 1
                    visited.add((trailhead, adj))
            else:
                q.put((adj, height + 1, trailhead))

    return result


def part1(input):
    return solve(input)


def part2(input):
    return solve(input, True)


def main():
    input = read_input("../data/day10.txt")
    test_input = read_input("../data/day10-test.txt")

    assert (res := part1(test_input)) == 36, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 744

    assert (res := part2(test_input)) == 81, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 1651


if __name__ == '__main__':
    main()
