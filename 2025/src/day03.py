import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2025/day/3

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    return read_file_str(input_file, True)


def solve(input, digits_required=12):
    result = 0
    for bank in input:
        # sort into descending order (index, value)
        ordered_bank = sorted(enumerate(map(int, bank)),
                              key=lambda x: x[1], reverse=True)

        joltage = []
        previous_index = -1
        for digit_index in range(digits_required):
            for i, d in enumerate(ordered_bank):
                # the max index needs to leave enough room for the remaining digits
                max_index = len(bank) - digits_required + digit_index + 1

                if previous_index < d[0] < max_index:
                    joltage.append(d[1])
                    previous_index = d[0]
                    # remove found digit
                    ordered_bank = ordered_bank[:i] + ordered_bank[i+1:]
                    break

        result += list_to_int(joltage)

    return result


def main():
    input = read_input("../data/day03.txt")
    test_input = read_input("../data/day03-test.txt")

    assert (res := solve(test_input, 2)) == 357, f'Actual: {res}'
    print(f'Part 1 {solve(input, 2)}')  # 17100

    assert (res := solve(test_input)) == 3121910778619, f'Actual: {res}'
    print(f'Part 2 {solve(input)}')  # 170418192256861


if __name__ == '__main__':
    main()
