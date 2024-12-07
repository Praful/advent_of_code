import sys
import os
from itertools import product
import operator

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2022/day/7


def read_input(input_file):
    result = []
    with open(input_file) as f:
        for line in f:
            s = line.split(':')
            operands = (list(map(int, s[1].split())))
            result.append((int(s[0]), operands))

    return result


def generate_operator_permutations(operators, n):
    # Generate all permutations of operators of length n
    return list(product(operators, repeat=n))


def solve(input, operators):
    total_calibration_result = 0
    for test_value, operands in input:
        permutations = generate_operator_permutations(
            operators, len(operands)-1)
        for ops in permutations:
            result = operands[0]
            for i, op in enumerate(ops):
                if op == operator.or_:
                    result = int(f'{result}{operands[i + 1]}')
                else:
                    result = op(result, operands[i + 1])

                if result > test_value:
                    break

            if result == test_value:
                total_calibration_result += test_value
                break

    return total_calibration_result


def part1(input):
    return solve(input, [operator.mul, operator.add])


def part2(input):
    return solve(input, [operator.mul, operator.add, operator.or_])


def main():
    input = read_input("../data/day07.txt")
    test_input = read_input("../data/day07-test.txt")

    assert (res := part1(test_input)) == 3749, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 20665830408335

    assert (res := part2(test_input)) == 11387, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 354060705047464


if __name__ == '__main__':
    main()
