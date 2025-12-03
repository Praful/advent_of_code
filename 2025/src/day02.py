import sys
import os
import re

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2025/day/2

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):

    def id_range(id_range):
        start, end = id_range.split('-')
        return (int(start), int(end))

    return list(map(id_range, read_file_str(input_file, True)[0].split(',')))


def solve(input, regex):
    result = 0

    for id_range in input:
        for id in range(id_range[0], id_range[1] + 1):
            if regex.search(str(id)):
                result += id

    return result


def main():
    input = read_input("../data/day02.txt")
    test_input = read_input("../data/day02-test.txt")

    REGEX_PART1 = re.compile(r"^(\d+?)\1$")
    REGEX_PART2 = re.compile(r"^(\d+?)\1+$")

    assert (res := solve(test_input, REGEX_PART1)) == 1227775554, f'Actual: {res}'
    print(f'Part 1 {solve(input, REGEX_PART1)}')  # 23039913998

    assert (res := solve(test_input, REGEX_PART2)) == 4174379265, f'Actual: {res}'
    print(f'Part 2 {solve(input, REGEX_PART2)}')  # 35950619148


if __name__ == '__main__':
    main()
