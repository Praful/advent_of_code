import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2015/day/8

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    return read_file_str(input_file, True)


def part1(input):
    result = 0

    for s in input:
        # treat backslash as escape in s
        processed = (s[1:-1]).encode().decode('unicode-escape')
        result += len(s) - len(processed)

    return result


def part2(input):
    result = 0
    for s in input:
        processed = s.replace('\\', '\\\\').replace('"', '\\"')
        result += len(processed) + 2 - len(s)

    return result


def main():
    input = read_input("../data/day08.txt")
    test_input = read_input("../data/day08-test.txt")

    assert (res := part1(test_input)) == 12, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 1342

    assert (res := part2(test_input)) == 19, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 2074


if __name__ == '__main__':
    main()
