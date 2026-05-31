import sys
import os
from collections import Counter

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2016/day/6

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input


def extract_char_part1(s):
    return Counter(s).most_common(1)[0][0]


def extract_char_part2(s):
    return Counter(s).most_common()[-1][0]


def solve(input, extract_char):
    columns = [""] * len(input[0])

    for s in input:
        for i, c in enumerate(s):
            columns[i] += c

    return "".join([extract_char(s) for s in columns])


def main():
    input = read_input("../data/day06.txt")
    test_input = read_input("../data/day06-test.txt")

    assert (res := solve(test_input, extract_char_part1)
            ) == "easter", f'Actual: {res}'
    print(f'Part 1 {solve(input, extract_char_part1)}')  # xhnqpqql

    assert (res := solve(test_input, extract_char_part2)
            ) == "advent", f'Actual: {res}'
    print(f'Part 2 {solve(input, extract_char_part2)}')  # brhailro


if __name__ == '__main__':
    main()
