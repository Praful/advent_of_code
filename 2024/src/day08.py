import sys
import os
from itertools import combinations
from pprint import pprint

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/8

EMPTY = '.'
ANTINODE = '#'


def read_input(input_file):
    antennas = {}
    input = read_file_str(input_file, True)
    for r, row in enumerate(input):
        for c, _ in enumerate(row):
            if row[c] != EMPTY:
                antennas.setdefault(row[c], []).append((r, c))

    return input, antennas


def print_antinodes(grid, antinodes):
    print(antinodes)
    for antinode in antinodes:
        grid[antinode[0]] = replace(grid[antinode[0]], antinode[1], ANTINODE)

    pprint(grid)


def solve(input, part2=False):
    grid, antennas = input
    antinodes = set()

    def add_antinode(p):
        if in_grid(p, grid):
            antinodes.add(p)

    for antenna in antennas.keys():
        points = antennas[antenna]
        point_combinations = list(combinations(points, 2))
        for p1, p2 in point_combinations:
            # vector from p1 to p2
            vx = p2[0] - p1[0]
            vy = p2[1] - p1[1]

            n = 1
            while True:
                # extend in the direction of p2
                p3 = (p2[0] + n * vx, p2[1] + n*vy)
                # extend in the opposite direction of p1
                p4 = (p1[0] - n*vx, p1[1] - n*vy)

                add_antinode(p3)
                add_antinode(p4)

                if part2:
                    add_antinode(p1)
                    add_antinode(p2)

                if not part2 or (not in_grid(p3, grid) and not in_grid(p4, grid)):
                    break

                n += 1

    #  print_antinodes(grid, antinodes)
    return len(antinodes)


def part1(input):
    return solve(input)


def part2(input):
    return solve(input, True)


def main():
    input = read_input("../data/day08.txt")
    test_input = read_input("../data/day08-test.txt")
    test_input2 = read_input("../data/day08-test2.txt")

    assert (res := part1(test_input)) == 14, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 285

    assert (res := part2(test_input2)) == 9, f'Actual: {res}'
    assert (res := part2(test_input)) == 34, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 944


if __name__ == '__main__':
    main()
