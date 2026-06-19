import sys
import os
import re

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2016/day/9

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    return read_file_str(input_file, True)[0]


RE_MARKER = r'\((\d+)x(\d+)\)'

def marker(s):
        return re.search(RE_MARKER, s)

def decompress1(s):
    remaining = s

    result = ""

    while len(remaining) > 0:
        m = marker(remaining)
        if m is None:
            result += remaining
            break

        count = int(m.group(1))
        repeat = int(m.group(2))

        if m.start() > 0:
            result += remaining[:m.start()]

        section = remaining[m.end():m.end() + count]
        result += section * repeat

        remaining = remaining[m.end() + count:]

    return result


def decompress2(s):
    remaining = s
    result = 0

    while len(remaining) > 0:
        m = marker(remaining)
        if m is None:
            result += len(remaining)
            break

        count = int(m.group(1))
        repeat = int(m.group(2))

        if m.start() > 0:
            result += len(remaining[:m.start()])

        section = remaining[m.end():m.end() + count]

        if marker(section) is not None:
            result += repeat * decompress2(section)
        else:
            result += repeat * len(section)

        remaining = remaining[m.end() + count:]

    return result


def part1(input):
    return len((decompress1(input)))


def part2(input):
    return decompress2(input)


def main():
    input = read_input("../data/day09.txt")

    assert (res := part1("ADVENT")) == 6, f'Actual: {res}'
    assert (res := part1("(3x3)XYZ")) == 9, f'Actual: {res}'
    assert (res := part1("A(2x2)BCD(2x2)EFG")) == 11, f'Actual: {res}'
    assert (res := part1("(6x1)(1x3)A")) == 6, f'Actual: {res}'
    assert (res := part1("X(8x2)(3x3)ABCY")) == 18, f'Actual: {res}'

    print(f'Part 1 {part1(input)}')  # 99145

    assert (res := part2("(3x3)XYZ")) == 9, f'Actual: {res}'
    assert (res := part2("X(8x2)(3x3)ABCY")) == 20, f'Actual: {res}'
    assert (res := part2("(27x12)(20x12)(13x14)(7x10)(1x12)A")
            ) == 241920, f'Actual: {res}'
    assert (res := part2(
        "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN")) == 445, f'Actual: {res}'

    print(f'Part 2 {part2(input)}')  # 10943094568


if __name__ == '__main__':
    main()
