import sys
import os
import re

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2025/day/6

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(input_file, False)

    data = [list(map(int, l))
            for l in map(lambda s: re.findall(r'\d+', s), input[:-1])]
    ops = re.findall(r'\S+', input[-1])
    return data, ops, input[:-1]


def calc(data, op):
    result = 0 if op == '+' else 1
    for d in data:
        if op == '*':
            result *= d
        else:
            result += d

    return result


def part1(input):
    data, ops, _ = input
    result = 0

    for c in range(len(data[0])):
        # slower way of getting col n from data
        # result += calc(list(zip(*data))[c], ops[c])

        result += calc([data[r][c] for r in range(len(data))], ops[c])

    return result


def op_data(str_data, pos, num_len, op):
    values = [str_data[r][pos:pos + num_len] for r in range(len(str_data))]

    # transpose:
    #  "123"
    #  " 45"
    #  "  6"
    # into 356, 24, 1
    return [int("".join(col)) for col in zip(*values)]


def part2(input):
    data, ops, str_data = input
    result = 0

    col_pos = 0

    for c in range(len(data[0])):
        num_len = max(len(str(data[r][c])) for r in range(len(data)))
        operands = op_data(str_data, col_pos, num_len, ops[c])
        col_pos += num_len + 1

        result += calc(operands, ops[c])

    return result


def main():
    input = read_input("../data/day06.txt")
    test_input = read_input("../data/day06-test.txt")

    assert (res := part1(test_input)) == 4277556, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 6371789547734

    assert (res := part2(test_input)) == 3263827, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 11419862653216


if __name__ == '__main__':
    main()
