import sys
import os
from collections import namedtuple
from functools import lru_cache
from itertools import combinations


sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2025/day/10

# Solution based on this post: https://redd.it/1pk87hl

DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None


Machine = namedtuple('Machine', 'lights buttons joltage')


def read_input(input_file):
    def to_tuple(s): return tuple(map(int, s.split(',')))

    def to_machine(s):
        lights = ""
        buttons = joltage = []
        for p in s.split(' '):
            match p[0]:
                case '[':
                    lights = p[1:-1]
                case '(':
                    buttons.append(to_tuple(p[1:-1]))
                case '{':
                    joltage = to_tuple(p[1:-1])
                case _:
                    assert False, f'Unknown: {p}'

        return Machine(lights, buttons, joltage)

    return list(map(to_machine, read_file_str(input_file, True)))


@lru_cache(maxsize=None)
def combos_for_lights(lights, buttons):
    light_count = len(lights)
    result = []

    for r in range(len(buttons) + 1):
        for combo in combinations(buttons, r):
            acc = [0]*light_count

            for button in combo:
                for v in button:
                    acc[v] ^= 1

            if lights == "".join("#" if b == 1 else "." for b in acc):
                result.append(combo)

    return result


def to_lights(joltage):
    return "".join("." if b % 2 == 0 else "#" for b in joltage)


@lru_cache(maxsize=None)
def min_joltage(joltage, buttons):
    if not any(joltage):
        return 0

    result = 1e9
    for combo in combos_for_lights(to_lights(joltage), buttons):
        starting_joltage = list(joltage)
        for button in combo:
            for i in button:
                starting_joltage[i] -= 1

        if any(j < 0 for j in starting_joltage):
            continue

        new_joltage = tuple(j//2 for j in starting_joltage)
        new_joltage_press_count = min_joltage(new_joltage, buttons)
        starting_joltage_press_count = len(
            combo) + (2 * new_joltage_press_count)

        result = min(result, starting_joltage_press_count)

    return result


def part1(input):
    def min_presses(machine):
        return min(len(c) for c in combos_for_lights(machine.lights, frozenset(machine.buttons)))

    return sum(min_presses(m) for m in input)


def part2(input):
    return sum(min_joltage(m.joltage, frozenset(m.buttons)) for m in input)


def main():
    input = read_input("../data/day10.txt")
    test_input = read_input("../data/day10-test.txt")

    assert (res := part1(test_input)) == 7, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 396

    assert (res := part2(test_input)) == 33, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 15688


if __name__ == '__main__':
    main()
