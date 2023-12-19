from dataclasses import dataclass
import os
import sys
import types
from collections import defaultdict

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/15

# namespace is required to use constants in match statements
# Just experimenting: obviously could just use if/else.
OP = types.SimpleNamespace()
OP.EQ = '='
OP.MINUS = '-'


@dataclass
class Step:
    label: str
    op: str
    value: int
    box_number: int


def read_input(input_file):
    return read_file_str(input_file, True)[0]


def hash(s):
    result = 0
    for c in s:
        result += ord(c)
        result *= 17
        result = result % 256

    return result


def parse(s):
    value = None

    if '=' in s:
        op = OP.EQ
        label, value = s.split(OP.EQ)
        value = int(value)
    elif '-' in s:
        op = OP.MINUS
        label, _ = s.split(OP.MINUS)
    else:
        raise Exception(f'Unknown op: {s}')

    return Step(label, op, value, hash(label))


# The solution is helped because Python dictionaries preserve insertion order.
# Updates don't change insertion order.
def update_box(step, boxes):
    match step.op:
        case OP.EQ:
            boxes[step.box_number][step.label] = step.value
        case OP.MINUS:
            boxes[step.box_number].pop(step.label, None)
        case _:
            raise Exception(f'Unknown op: {step.op}')

    return


def focusing_power(boxes):
    result = 0
    for box_number, contents in boxes.items():
        for slot, focal_length in enumerate(contents.values()):
            result += (box_number+1) * (slot+1) * focal_length

    return result


def part1(input):
    return sum(hash(step) for step in input.split(','))


def part2(input):
    boxes: dict[int, dict[str, int]] = defaultdict(dict)

    for s in input.split(','):
        step = parse(s)
        update_box(step, boxes)

    return focusing_power(boxes)


def main():
    input = read_input("../data/day15.txt")
    test_input = read_input("../data/day15-test.txt")

    assert (res := hash('HASH')) == 52, f'Actual: {res}'
    assert (res := part1(test_input)) == 1320, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 505427

    assert (res := part2(test_input)) == 145, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 243747


if __name__ == '__main__':
    main()
