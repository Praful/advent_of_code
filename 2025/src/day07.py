import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2025/day/7

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(input_file, True)
    start = find_in_grid(input, 'S')
    return input, start[0]


def find_splitters(line):
    return [i for i, c in enumerate(line) if c == '^']


def part1(input):
    result = 0
    grid, start = input
    # = 0 if no beam in col, else = 1
    beam_col = [0] * len(grid[0])
    beam_col[start[1]] = 1

    row = start[0]+1
    while row < len(grid):
        splitters = find_splitters(grid[row])

        if len(splitters) > 0:
            for n in splitters:
                if beam_col[n] == 1:
                    beam_col[n] = 0
                    result += 1

                    if n > 0:
                        beam_col[n-1] = 1
                    if n < len(beam_col)-1:
                        beam_col[n+1] = 1

        row += 1

    return result

def part2(input):
    grid, start = input
    # = 0 if no beam in col, else > 0
    beam_col = [0] * len(grid[0])
    beam_col[start[1]] = 1

    row = start[0]+1
    while row < len(grid):
        splitters = find_splitters(grid[row])

        if len(splitters) > 0:
            for n in splitters:
                if beam_col[n] > 0:
                    beams = beam_col[n]
                    beam_col[n] = 0

                    if n > 0:
                        beam_col[n-1] += beams
                    if n < len(beam_col)-1:
                        beam_col[n+1] += beams 

        row += 1

    return sum(beam_col)


def main():
    input = read_input("../data/day07.txt")
    test_input = read_input("../data/day07-test.txt")

    assert (res := part1(test_input)) == 21, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 1615

    assert (res := part2(test_input)) == 40, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 43560947406326


if __name__ == '__main__':
    main()
