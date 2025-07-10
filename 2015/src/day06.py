import sys
import os
from collections import defaultdict
from enum import Enum

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2015/day/6

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


class Action(Enum):
    ON = 0
    OFF = 1
    TOGGLE = 2


def read_input(input_file):
    def action(s):
        if s.startswith('turn on'):
            return Action.ON
        if s.startswith('turn off'):
            return Action.OFF
        if s.startswith('toggle'):
            return Action.TOGGLE

        assert False

    def instruction(s):
        action_type = action(s)
        a, b, c, d = extract_ints(s)

        return action_type, (a, b), (c, d)

    return list(map(instruction, read_file_str(input_file, True)))


def part1(input):
    result = set()

    for action, a, b in input:
        for x in range(a[0], b[0] + 1):
            for y in range(a[1], b[1] + 1):
                match action: 
                    case Action.ON:
                        result.add((x, y))
                    case Action.OFF:
                        result.discard((x, y))
                    case Action.TOGGLE:
                        if (x, y) in result:
                            result.discard((x, y))
                        else:
                            result.add((x, y))

    return len(result)


def part2(input):
    result = defaultdict(int)

    for action, a, b in input:
        for x in range(a[0], b[0] + 1):
            for y in range(a[1], b[1] + 1):
                match action: 
                    case Action.ON:
                        result[(x, y)] += 1
                    case Action.OFF:
                        if result[(x, y)] > 0:
                            result[(x, y)] -= 1
                    case Action.TOGGLE:
                        result[(x, y)] += 2

    return sum(result.values())


def main():
    input = read_input("../data/day06.txt")

    print(f'Part 1 {part1(input)}')  # 377891
    print(f'Part 2 {part2(input)}')  # 14110788


if __name__ == '__main__':
    main()
