import re
import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
from utils import *

# Puzzle description: https://adventofcode.com/2015/day/2


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input


def solve(input, calc):
    return sum(calc(present) for present in input)


def dimensions(present):
    l, w, h = re.findall(r'\d+', present)
    return int(l), int(w), int(h)


def surface_area(present):
    l, w, h = dimensions(present)
    return 2*l*w + 2*w*h + 2*h*l + min(l*w, w*h, h*l)


def ribbon_length(present):
    l, w, h = dimensions(present)
    dim_list = sorted([l, w, h])
    return l*w*h + dim_list[0]*2 + dim_list[1]*2


def part1(input):
    return solve(input, surface_area)


def part2(input):
    return solve(input, ribbon_length)


def main():
    input = read_input("../data/day02.txt")

    assert (res := part1(['2x3x4'])) == 58, f'Actual: {res}'
    assert (res := part1(['1x1x10'])) == 43, f'Actual: {res}'

    print(f'Part 1 {part1(input)}')  # 1598415

    assert (res := part2(['2x3x4'])) == 34, f'Actual: {res}'
    assert (res := part2(['1x1x10'])) == 14, f'Actual: {res}'

    print(f'Part 2 {part2(input)}')  # 3812909


if __name__ == '__main__':
    main()
