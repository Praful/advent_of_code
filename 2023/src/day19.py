import re
import copy
import operator
import numpy as np
import math
from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
import os
import sys
from functools import reduce
from itertools import product
from operator import mul
from collections import namedtuple
from queue import SimpleQueue

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/19

Rule = namedtuple('Rule', ['category', 'operator', 'value', 'next'])
Part = namedtuple('Part', ['x', 'm', 'a', 's'])


def read_input(input_file):
    with open(input_file) as f:
        input = [l.strip().split('\n') for l in f.read().split('\n\n')]

    workflows = {}
    for s in input[0]:
        r1 = s.split('{')
        workflow = r1[0]
        rules = []
        r2 = r1[1].split('}')[0].split(',')
        last = r2[-1]
        for rule in r2[:-1]:
            m = re.findall(r'(.)([<|>])(\d*):(.*)', rule)[0]
            r = Rule(m[0], operator.lt if m[1] ==
                     '<' else operator.gt, int(m[2]), m[3])
            rules.append(r)

        rules.append(Rule(None, None, None, last))
        workflows[workflow] = rules

    parts = []
    for s in input[1]:
        m = re.findall(r'\d+', s)
        parts.append(Part(int(m[0]), int(m[1]), int(m[2]), int(m[3])))

    return (workflows, parts)


def xmas_rating(part):
    return part.x + part.m + part.a + part.s


def accepted(workflows, part):
    workflow_id = 'in'
    while True:
        if workflow_id == 'R':
            return False
        elif workflow_id == 'A':
            return True

        workflow = workflows[workflow_id]

        for rule in workflow:
            if rule.category is None:
                workflow_id = rule.next
                break
            else:
                value = getattr(part, rule.category)
                if rule.operator(value, rule.value):
                    workflow_id = rule.next
                    break


def part1(input):
    workflows, parts = input
    return sum(xmas_rating(part) for part in parts if accepted(workflows, part))


def new_range(part, rule, op):
    r = getattr(part, rule.category)

    match op:
        case '>':
            r2 = (max(r[0], rule.value+1), r[1])
        case '<':
            r2 = (r[0], min(r[1], rule.value-1))
        case '>=':
            r2 = (max(r[0], rule.value), r[1])
        case '<=':
            r2 = (r[0], min(r[1], rule.value))
        case _:
            raise Exception(f'Unknown op {op}')

    # eg if category is x, this creates a new Part namedtuple where x is the
    # newly worked out range above and m, a, s are the same; can also do
    # part._replace(x=r2) but then you'd have to check if x, m, a, s are
    # being updated
    return part._replace(**{rule.category: r2})


def split_range(part, rule):
    # return two ranges: one that passes the rule and one that fails
    # eg (1, 10) for opertor '>' and value 5 is (6, 10) and (1, 5)

    if rule.operator == operator.gt:
        return [new_range(part, rule, '>'), new_range(part, rule, '<=')]
    elif rule.operator == operator.lt:
        return [new_range(part, rule, '<'), new_range(part, rule, '>=')]
    else:
        raise Exception(f'Unknown operator {rule.operator}')


def part2(input):
    def span(part, category):
        r = getattr(part, category)
        return r[1]-r[0]+1

    workflows, _ = input

    q = SimpleQueue()
    result = 0
    workflow_id = 'in'
    START_RANGE = (1, 4000)
    part = Part(START_RANGE, START_RANGE, START_RANGE, START_RANGE)

    q.put((workflow_id, part))

    while not q.empty():
        workflow_id, part = q.get()

        if workflow_id == 'R':
            continue
        elif workflow_id == 'A':
            result += span(part, 'x') * span(part, 'm') * \
                span(part, 'a') * span(part, 's')
            continue

        workflow = workflows[workflow_id]

        for rule in workflow:
            if rule.category is None:
                q.put((rule.next, part))
                break
            else:
                true_range, false_range = split_range(part, rule)
                q.put((rule.next, true_range))
                part = false_range

    return result


def main():
    input = read_input("../data/day19.txt")
    test_input = read_input("../data/day19-test.txt")

    assert (res := part1(test_input)) == 19114, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 374873

    assert (res := part2(test_input)) == 167409079868000, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 122112157518711


if __name__ == '__main__':
    main()
