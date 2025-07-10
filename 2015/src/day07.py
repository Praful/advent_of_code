import sys
import os
import re
from collections import namedtuple
import operator

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2015/day/7

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

Expression = namedtuple(
    'Expression', ['operand1', 'operand2', 'operator', 'output'])


def convert(s):
    return int(s) if s.isnumeric() else s


def create_expression(e, operator):
    return Expression(convert(e[0]), convert(e[2]), operator, e[4])


def parse(s):
    assignment = r'^\w+\s*->\s*\w+$'
    e = s.split(' ')

    if 'AND' in s:
        return create_expression(e, operator.and_)
    elif 'OR' in s:
        return create_expression(e, operator.or_)
    elif 'LSHIFT' in s:
        return create_expression(e, operator.lshift)
    elif 'RSHIFT' in s:
        return create_expression(e, operator.rshift)
    elif 'NOT' in s:
        return Expression(convert(e[1]), None, operator.not_, e[3])
    elif re.match(assignment, s):
        return Expression(convert(e[0]), None, None, e[2])
    else:
        assert False, f'Unknown expression {s}'


def read_input(input_file):
    input = read_file_str(input_file, True)
    return list(map(parse, input))


def can_evaluate(wires, e):
    if e.operator in [operator.and_, operator.or_, operator.lshift, operator.rshift]:
        if (isinstance(e.operand1, int) or e.operand1 in wires.keys()) and \
                (isinstance(e.operand2, int) or e.operand2 in wires.keys()):
            return True
    elif e.operator == operator.not_ or e.operator is None:
        return isinstance(e.operand1, int) or e.operand1 in wires.keys()
    else:
        assert False, f'Unknown operator {e.operator}'


def solve(input, wires=None):
    if wires is None:
        wires = {}

    def value(operand):
        if isinstance(operand, int):
            return operand
        else:
            return wires[operand]

    part2 = len(wires) > 0

    while True:
        all_evaluated = True
        for e in input:
            if not can_evaluate(wires, e):
                all_evaluated = False
                continue

            match e.operator:
                case None:  # assignment
                    if not part2 or (part2 and e.output != 'b'):
                        wires[e.output] = value(e.operand1)
                case operator.not_:
                    wires[e.output] = ~value(wires[e.operand1])
                case operator.and_ | operator.or_ | operator.lshift | operator.rshift:
                    wires[e.output] = e.operator(
                        value(e.operand1), value(e.operand2))
                case _:
                    assert False, f'Unknown operator {e.operator}'

            # handle overflow for 16-bit integers 0 to 65535
            if wires[e.output] < 0:
                wires[e.output] += 65536

        if all_evaluated:
            break

    return wires


def part1(input):
    return solve(input)


def part2(input):
    wires = solve(input)
    return solve(input, {'b': wires['a']})


def main():
    input = read_input("../data/day07.txt")
    #  test_input = read_input("../data/day07-test.txt")

    #  print(part1(test_input))
    print(f'Part 1 {part1(input)["a"]}')  # 46065
    print(f'Part 2 {part2(input)["a"]}')  # 14134


if __name__ == '__main__':
    main()
