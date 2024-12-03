import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/2


def read_input(input_file):
    input = read_file_int(input_file)
    return input


def both_positive_or_negative(a, b):
    return (a > 0 and b > 0) or (a < 0 and b < 0)


def safe(report):
    report_diff = report[0] - report[1]
    if report_diff == 0:
        return False

    safe = True
    for i in range(len(report) - 1):
        level_diff = report[i] - report[i + 1]

        if not (0 < abs(level_diff) < 4 and both_positive_or_negative(report_diff, level_diff)):
            safe = False
            break

    return safe


# Create a new array excluding the element at index i
def remove_element(original_array, i):
    return original_array[:i] + original_array[i+1:]


def part1(input):
    return sum(1 for report in input if safe(report))


def part2(input):
    result = 0

    for report in input:
        if safe(report):
            result += 1
            continue

        for i in range(len(report)):
            if safe(remove_element(report, i)):
                result += 1
                break

    return result


def main():
    input = read_input("../data/day02.txt")
    test_input = read_input("../data/day02-test.txt")

    assert (res := part1(test_input)) == 2, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 670

    assert (res := part2(test_input)) == 4, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 700


if __name__ == '__main__':
    main()
