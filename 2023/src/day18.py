from dataclasses import dataclass
import os
import sys

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/18


@dataclass
class DigInstruction:
    direction: str
    distance: int
    colour: str


def read_input(input_file):
    def parse(l):
        dir, count, colour = l.split()
        return DigInstruction(dir, int(count), colour)

    return list(map(parse, read_file_str(input_file, True)))


def test():
    a = [(1, 6), (3, 1), (7, 2), (4, 4), (8, 5)]
    print(shoelace_area(a))


def part1(input):
    pos = (0, 0)
    boundary_points = [pos]
    boundary_length = 0

    for instr in input:
        boundary_length += instr.distance
        match instr.direction:
            case 'R':
                pos = (pos[0] + instr.distance, pos[1])
            case 'L':
                pos = (pos[0] - instr.distance, pos[1])
            case 'U':
                pos = (pos[0], pos[1] - instr.distance)
            case 'D':
                pos = (pos[0], pos[1] + instr.distance)

        boundary_points.append(pos)

    return int(internal_area(boundary_points, boundary_length) + boundary_length)


def part2(input):
    dir_map = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}

    def parse(di):
        return DigInstruction(dir_map[di.colour[7]], hex_to_dec(di.colour[2:7]), None)

    return part1(list(map(parse, input)))


def main():
    input = read_input("../data/day18.txt")
    test_input = read_input("../data/day18-test.txt")

    assert (res := part1(test_input)) == 62, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 70026

    assert (res := part2(test_input)) == 952408144115, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 68548301037382


if __name__ == '__main__':
    main()
