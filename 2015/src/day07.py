import sys
import os
import re
import copy
import math
import itertools
import functools
import collections
from collections import defaultdict
from collections import namedtuple
from dataclasses import dataclass
from functools import lru_cache
from functools import reduce
from itertools import product
from operator import mul
from pprint import pprint
import numpy as np
import operator
import queue
from queue import SimpleQueue

# for profiling
from cProfile import Profile
from pstats import Stats, SortKey

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


def read_input(input_file):
    input = read_file_str(input_file, True)

    #  assignment = r'^\d+\s*->\s*\w$'
    assignment = r'^\w+\s*->\s*\w+$'

    result = []
    for s in input:
        if 'AND' in s:
            e = s.split(' ')
            result.append(Expression(
                convert(e[0]), convert(e[2]), operator.and_, e[4]))
        elif 'OR' in s:
            e = s.split(' ')
            result.append(Expression(
                convert(e[0]), convert(e[2]), operator.or_, e[4]))
        elif 'LSHIFT' in s:
            e = s.split(' ')
            result.append(Expression(
                convert(e[0]), convert(e[2]), operator.lshift, e[4]))
        elif 'RSHIFT' in s:
            e = s.split(' ')
            result.append(Expression(
                convert(e[0]), convert(e[2]), operator.rshift, e[4]))
        elif 'NOT' in s:
            e = s.split(' ')
            result.append(Expression(convert(e[1]), None, operator.not_, e[3]))
        elif re.match(assignment, s):
            e = s.split(' ')
            result.append(Expression(convert(e[0]), None, None, e[2]))
        else:
            assert False, f'Unknown expression {s}'

    return result


def can_evaluate(wires, e):
    if e.operator in [operator.and_, operator.or_, operator.lshift, operator.rshift]:
        if (isinstance(e.operand1, int) or e.operand1 in wires.keys()) and \
                (isinstance(e.operand2, int) or e.operand2 in wires.keys()):
            return True
    elif e.operator == operator.not_ or e.operator is None:
        return isinstance(e.operand1, int) or e.operand1 in wires.keys()
    else:
        assert False, f'Unknown operator {e.operator}'


def part1(input):
    def value(operand):
        if isinstance(operand, int):
            return operand
        else:
            return wires[operand]

    result = 0
    #  pprint(input)
    wires = {}

    while True:
        all_evaluated = True
        for e in input:
            if not can_evaluate(wires, e):
                all_evaluated = False
                continue

            match e.operator:
                case None:
                    wires[e.output] = value(e.operand1)
                case operator.not_:
                    wires[e.output] = ~value(wires[e.operand1])
                case operator.and_ | operator.or_ | operator.lshift | operator.rshift:
                    wires[e.output] = e.operator(
                        value(e.operand1), value(e.operand2))
                case _:
                    assert False, f'Unknown operator {e.operator}'

            if wires[e.output] < 0:
                wires[e.output] += 65536

        if all_evaluated:
            break

    #  print(wires)
    return wires


def part2(input):
    result = 0
    return result


def main():
    input = read_input("../data/day07.txt")
    test_input = read_input("../data/day07-test.txt")

    print(part1(test_input))
    print(f'Part 1 {part1(input)["a"]}')  # 46065

    #  assert (res := part2(test_input)) == 0, f'Actual: {res}'
    # print(f'Part 2 {part2(input)}')  #


if __name__ == '__main__':
    #  sys.setrecursionlimit(999999)

    main()

    #  with Profile() as profile:
    #
    #  main()
    #  (
    #  Stats(profile)
    #  .strip_dirs()
    #  .sort_stats(SortKey.TIME)
    #  .print_stats()
    #  )
