import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/18

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

ON = '#'
OFF = '.'


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input


def next_state(input, row, col):
    def state(is_on):
        return ON if is_on else OFF

    is_on = input[row][col] == ON
    adj = neighbours2((row, col), input)
    neighbours_on = sum(1 for (r, c) in adj if input[r][c] == ON)

    if is_on:
        return state(neighbours_on in [2, 3])
    else:
        return state(neighbours_on == 3)


def print_lights(input):
    for row in input:
        print(row)


def solve(input, steps, part2=False):
    corners = []

    # corners are always on
    if part2:
        corners = [(0, 0), (0, len(input[0]) - 1), (len(input) - 1, 0),
                   (len(input) - 1, len(input[0]) - 1)]
        input[0] = ON + input[0][1:-1] + ON
        input[-1] = ON + input[-1][1:-1] + ON

    for _ in range(steps):
        next_config = []
        for row in range(len(input)):
            next_row = ''
            for col in range(len(input[row])):
                if part2 and (row, col) in corners:
                    new_light = ON
                else:
                    new_light = next_state(input, row, col)
                next_row += new_light
            next_config.append(next_row)

        input = next_config

    return len(find_in_grid(input, ON))


def main():
    input = read_input("../data/day18.txt")
    test_input = read_input("../data/day18-test.txt")

    assert (res := solve(test_input, 4)) == 4, f'Actual: {res}'
    print(f'Part 1 {solve(input, 100)}')  # 821

    assert (res := solve(test_input, 5, True)) == 17, f'Actual: {res}'
    print(f'Part 2 {solve(input, 100, True)}')  # 886


if __name__ == '__main__':
    main()
