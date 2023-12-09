import os
import sys
from itertools import pairwise
sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/09


def read_input(input_file): return read_file_int(input_file)


def next_number(history, forward=True):
    def diffs(): return [b - a for a, b in pairwise(history)]

    if not any(history):
        return 0

    i, add_minus = (-1, 1) if forward else (0, -1)

    return history[i] + (add_minus * next_number(diffs(), forward))


def part1(input): return sum(map(next_number, input))


def part2(input): return sum(map(lambda xs: next_number(xs, False), input))


def main():
    input = read_input("../data/day09.txt")
    test_input = read_input("../data/day09-test.txt")

    assert (res := part1(test_input)) == 114, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 1702218515

    assert (res := part2(test_input)) == 2, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 925


if __name__ == '__main__':
    main()
