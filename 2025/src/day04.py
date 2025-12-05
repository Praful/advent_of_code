import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/4

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input


def accessible(input):
    result = []
    for r in range(0, len(input)):
        for c in range(0, len(input[r])):
            if tile(input, (r, c)) == '.':
                continue

            adj = neighbours((r, c), input, include_diagonal=True)

            if sum(tile(input, pos) == '@' for pos in adj) < 4:
                result.append((r, c))

    return result


def part1(input):
    return len(accessible(input))


def part2(input):
    result = 0

    while True:
        removable = accessible(input)

        if len(removable) == 0:
            break

        result += len(removable)

        for pos in removable:
            input[pos[0]] = replace(input[pos[0]], pos[1], '.')

    return result


def main():
    input = read_input("../data/day04.txt")
    test_input = read_input("../data/day04-test.txt")

    assert (res := part1(test_input)) == 13, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 1397

    assert (res := part2(test_input)) == 43, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 8758


if __name__ == '__main__':
    main()
