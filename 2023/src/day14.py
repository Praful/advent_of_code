import numpy as np
import os
import sys

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/14

EMPTY = '.'
ROUND_ROCK = 'O'
CUBIC_ROCK = '#'
ROCKS = [ROUND_ROCK, CUBIC_ROCK]
MAX_CYCLES = 10**9


def read_input(input_file):
    return to_numpy_array(read_file_str(input_file, True))


def load(a): return sum(np.count_nonzero(
    a[row] == ROUND_ROCK) * (a.shape[0]-row) for row in range(a.shape[0]))


def roll(input):
    row_count = input.shape[0]
    col_count = input.shape[1]

    for col in range(col_count):
        for row in range(row_count):
            if input[row, col] == ROUND_ROCK:
                min_row = -1
                for free_row in range(row-1, -1, -1):
                    if input[free_row, col] in ROCKS:
                        break

                    if input[free_row, col] == EMPTY:
                        min_row = free_row

                if min_row != -1:
                    input[min_row, col] = ROUND_ROCK
                    input[row, col] = EMPTY

    return input


def part1(input):
    return load(roll(input))


def part2(input):
    cycle = 0
    states = {cycle: np.copy(input)}
    repeat_cycles = 0
    while cycle < MAX_CYCLES:
        cycle += 1
        for _ in range(4):
            input = roll(input)
            input = np.rot90(input, 3)  # rotate clockwise: W, S, E, N

        if repeat_cycles < 1:
            for k, v in states.items():
                if np.array_equal(input, v):
                    repeat_cycles = cycle - k
                    # bump up cycle number to just below MAX_CYCLES since we have
                    # found a repeating pattern
                    cycle += ((MAX_CYCLES - cycle)//repeat_cycles) * repeat_cycles
                    break

            states[cycle] = np.copy(input)

    return load(input)


def main():
    input = read_input("../data/day14.txt")
    test_input = read_input("../data/day14-test.txt")

    assert (res := part1(np.copy(test_input))) == 136, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 105461

    assert (res := part2(np.copy(test_input))) == 64, f'Actual: {res}'
    print(f'Part 2 {part2(np.copy(input))}')  # 102829


if __name__ == '__main__':
    main()
