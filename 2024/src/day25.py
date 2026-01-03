import sys
import os
from itertools import product

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/25

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    keys = []
    locks = []
    for schemtic in read_file_str_sections(input_file, True):
        # transpose and drop first/last rows
        columns = list(zip(*schemtic[1:-1]))

        pin_heights = list(map(lambda c: c.count('#'), columns))
        if schemtic[0][0] == "#":
            locks.append(pin_heights)
        else:
            keys.append(pin_heights)

    return keys, locks


def part1(input):
    keys, locks = input
    result = 0

    for kl1, kl2 in product(keys, locks):
        if all(pin1 + pin2 <= 5 for pin1, pin2 in zip(kl1, kl2)):
            result += 1

    return result


def main():
    input = read_input("../data/day25.txt")
    test_input = read_input("../data/day25-test.txt")

    assert (res := part1(test_input)) == 3, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 3344


if __name__ == '__main__':
    main()
