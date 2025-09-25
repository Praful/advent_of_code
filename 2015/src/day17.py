import sys
import os
import math
from itertools import combinations

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2015/day/17

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    return list(map(int, read_file_str(input_file, True)))


def part1(containers, target):
    return sum(
        1
        for i in range(1, len(containers) + 1)
        for c in combinations(containers, i)
        if sum(c) == target
    )


def find_minimum(containers, target):
    return min(
        (len(c) for i in range(1, len(containers) + 1)
         for c in combinations(containers, i)
         if sum(c) == target),
        default=math.inf
    )


def part2(containers, target):
    minimum_containers = find_minimum(containers, target)

    return sum(
        1
        for i in range(1, len(containers) + 1)
        for c in combinations(containers, i)
        if len(c) == minimum_containers and sum(c) == target
    )


def main():
    input = read_input("../data/day17.txt")
    test_input = read_input("../data/day17-test.txt")

    assert (res := part1(test_input, 25)) == 4, f'Actual: {res}'
    print(f'Part 1 {part1(input, 150)}')  # 1304

    assert (res := part2(test_input, 25)) == 3, f'Actual: {res}'
    print(f'Part 2 {part2(input, 150)}')  # 18


if __name__ == '__main__':
    main()
