import sys
import os
import random

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2022/day/25

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

SNAFU_MAP = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
SNAFU_CHARS = list(SNAFU_MAP.keys())

EXAMPLES = [
    (1, "1"),
    (2, "2"),
    (3, "1="),
    (4, "1-"),
    (5, "10"),
    (6, "11"),
    (7, "12"),
    (8, "2="),
    (9, "2-"),
    (10, "20"),
    (15, "1=0"),
    (20, "1-0"),
    (2022, "1=11-2"),
    (12345, "1-0---0"),
    (314159265, "1121-1110-1=0")]


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input


def snafu_to_decimal(snafu):
    return sum((5**i) * SNAFU_MAP[c] for i, c in enumerate(reversed(snafu)))


# this is a sort of hillclimbing algorithm, where we randomly try snafu characters
# in each slot (starting with MSB) until we find a valid result
def decimal_to_snafu(decimal):
    result = ['0']*2*len(str(decimal))

    while (remainder := decimal - snafu_to_decimal(result)) != 0:
        p, _ = nearest_power_of(5, abs(remainder))
        i = len(result) - p - 1

        # try a different snafu char in position i
        try_char = result[i]
        while try_char == result[i]:
            try_char = random.choice(SNAFU_CHARS)

        result[i] = try_char

    return "".join(strip_leading_char(result, '0'))


def part1(input):
    result = sum(map(snafu_to_decimal, input))
    return decimal_to_snafu(result)


def test_examples():
    for example in EXAMPLES:
        print("Checking...", example)
        assert snafu_to_decimal(example[1]) == example[0]
        assert decimal_to_snafu(example[0]) == example[1]
        print("...OK")


def main():
    input = read_input("../data/day25.txt")
    test_input = read_input("../data/day25-test.txt")

    #  test_examples()

    # decimal sum: 4890 = snafu: 2=-1=0
    assert (res := part1(test_input)) == '2=-1=0', f'Actual: {res}'

    # decimal sum: 29694520452605 = snafu: 2=-0=01----22-0-1-10
    print(f'Part 1 {part1(input)}')  


if __name__ == '__main__':
    main()
