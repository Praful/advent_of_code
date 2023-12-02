import re
import os
import sys

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/1


def read_input(input_file): return read_file_str(input_file, True)


numbers_as_words = ['one', 'two', 'three', 'four',
                    'five', 'six', 'seven', 'eight', 'nine']


def to_digit(c, s):
    # if c is a digit eg "3", return it
    # else if s starts with a number word eg "seven", return the number ("7" in this
    # case)

    if c.isdigit():
        return c
    else:
        for idx, word in enumerate(numbers_as_words, 1):
            if s.startswith(word):
                return str(idx)
    return ''


def map_calibration(calibration):
    # map a calibration to all numbers eg
    #   one2sevenxyzeight maps to 1278
    #   2fiveightwo2 maps to 25822
    # Unmapped letters (such as x) are removed.
    return ''.join(to_digit(c, calibration[idx:]) for idx, c in enumerate(calibration))


def part2(input):
    # Replace number words (eg one, three, five) with their digit equivalent (in this
    # case 1, 3, 5). Then call the solution to part 1.

    return part1(map(map_calibration, input))


def value(calibration):
    digits = re.findall(r'\d', calibration)
    return int(digits[0] + digits[-1])


def part1(input):
    return sum(value(calibration) for calibration in input)


def main():
    input = read_input("../data/day01.txt")
    test_input_1 = read_input("../data/day01-test-1.txt")
    test_input_2 = read_input("../data/day01-test-2.txt")

    assert (res := part1(test_input_1)
            ) == 142, f'Actual: {res}'
    print(f'Part 1 {part1(input )}')  # 54632

    assert (res := part2(test_input_2)) == 281, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 54019


if __name__ == '__main__':
    main()
