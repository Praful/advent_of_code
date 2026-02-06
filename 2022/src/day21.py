import sys
import os
import re
import copy
from operator import add, mul, sub, floordiv

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2022/day/21

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': floordiv
}


def read_input(input_file):
    equations = {}
    values = {}
    for s in read_file_str(input_file, True):
        parts = s.split(': ')
        if re.match(r'\d+', parts[1]):
            values[parts[0]] = int(parts[1])
        else:
            v1, op, v2 = parts[1].split(' ')
            equations[parts[0]] = (v1, OPERATORS[op], v2)

    return values, equations


def part1(input):
    values_original, equations = input
    values = copy.deepcopy(values_original)

    while 'root' not in values:
        for k, v in equations.items():
            if k in values:
                continue

            v1, op, v2 = v
            if v1 in values and v2 in values:
                values[k] = op(values[v1], values[v2])

    return values['root']


# solve x = v1 op v2 where x and one of v1 or v2 are known
def solve_equation(x, op, v1_name, v2_name, v1, v2):
    assert ((v1 is None) != (v2 is None)), "Exactly one of v1 or v2 must be known."

    if op == add:
        return (v2_name, x - v1) if v1 is not None else (v1_name, x - v2)

    if op == sub:
        return (v2_name, v1 - x) if v1 is not None else (v1_name, x + v2)

    if op == mul:
        return (v2_name, x // v1) if v1 is not None else (v1_name, x // v2)

    if op == floordiv:
        return (v2_name, v1 // x) if v1 is not None else (v1_name, x * v2)

    raise ValueError("Unknown operator", op)


def part2(input):
    values_original, equations_original = input
    values = copy.deepcopy(values_original)
    equations = copy.deepcopy(equations_original)

    values.pop('humn')

    while 'humn' not in values:
        remove = []
        for k, v in equations.items():
            v1, op, v2 = v

            # for root, if we know one of the values, the other is the same
            if k == 'root' and (v1 not in values) ^ (v2 not in values):
                if v1 in values:
                    values[v2] = values[v1]
                elif v2 in values:
                    values[v1] = values[v2]

            # we know one of the values and k: find other value
            if k in values and ((v1 in values) ^ (v2 in values)):
                res_v, res_value = solve_equation(
                    values[k], op, v1, v2, values.get(v1), values.get(v2))
                values[res_v] = res_value

            # both values are known: solve
            if v1 in values and v2 in values:
                remove.append(k)
                values[k] = op(values[v1], values[v2])

        # remove solved equations
        for r in remove:
            equations.pop(r)

    return values['humn']


def main():
    input = read_input("../data/day21.txt")
    test_input = read_input("../data/day21-test.txt")

    assert (res := part1(test_input)) == 152, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 51928383302238

    assert (res := part2(test_input)) == 301, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 3305669217840


if __name__ == '__main__':
    main()
