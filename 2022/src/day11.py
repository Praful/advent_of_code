from dataclasses import dataclass
import os
import sys
from types import BuiltinFunctionType
from typing import Callable
sys.path.append(os.path.relpath("../../shared/python"))
import utils
import operator
import copy
from functools import reduce

# Puzzle description: https://adventofcode.com/2022/day/11


def read_input(input_file):
    def extract_num(l, s):
        return int(l[l.find(s) + len(s):].strip(' :'))

    input = utils.read_file_str(input_file, True)
    monkeys = {}

    for i in range(0, len(input), 7):
        id = extract_num(input[i], ' ')
        wll = input[i + 1]
        wl = [int(j) for j in wll[wll.find(':') + 2:].split(', ')]
        opl = input[i + 2]
        op = operator.add if opl.find('+') > -1 else operator.mul
        j = opl.find('+') if op == operator.add else opl.find('*')
        opval = opl[j + 1:].strip()
        opval = int(opval) if opval.isdigit() else opval
        td = extract_num(input[i + 3], 'by ')
        tid = extract_num(input[i + 4], 'monkey ')
        fid = extract_num(input[i + 5], 'monkey ')
        monkeys[id] = Monkey(id, wl, op, opval, td, tid, fid)

    # print(monkeys)
    return monkeys


@dataclass
class Monkey:
    id: int
    worry_levels: list[int]
    operation: Callable
    op_value: object
    test_divisor: int
    true_id: int
    false_id: int


def next_worry_level(monkey, w):
    if monkey.op_value == 'old':
        result = monkey.operation(w, w)
    else:
        result = monkey.operation(w, monkey.op_value)

    return result


def monkey_business(inspections):
    ordered = sorted(inspections)
    return ordered[-1] * ordered[-2]


def solve(input, rounds, part1=True):
    monkeys = copy.deepcopy(input)
    inspections = [0] * len(monkeys)

    # The trick for part2 is to reduce the new worry level without affecting
    # future calculations; this is done by creating a divisor that is the
    # product of all the monkeys' test divisors. See:
    # - https://en.wikipedia.org/wiki/Modular_arithmetic
    # - https://en.wikipedia.org/wiki/Chinese_remainder_theorem
    common_divisor = reduce(
        lambda a, b: a * b, [m.test_divisor for m in monkeys.values()])

    for r in range(rounds):
        for i in sorted(monkeys.keys()):
            m = monkeys[i]

            worry_levels = m.worry_levels.copy()
            m.worry_levels = []
            for w in worry_levels:
                inspections[i] += 1

                new_w = next_worry_level(m, w)
                new_w = new_w // 3 if part1 else new_w % common_divisor

                throw_id = m.true_id if new_w % m.test_divisor == 0 else m.false_id
                monkeys[throw_id].worry_levels.append(new_w)

    return monkey_business(inspections)


def part1(input, rounds):
    return solve(input, rounds)


def part2(input, rounds):
    return solve(input, rounds, False)


def main():
    input = read_input("../data/day11.txt")
    test_input = read_input("../data/day11-test.txt")

    assert part1(test_input, 20) == 10605
    print(f'Part 1 {part1(input,20)}')  # 121450

    assert part2(test_input, 10000) == 2713310158
    print(f'Part 2 {part2(input, 10000)}')  # 28244037010


if __name__ == '__main__':
    main()
