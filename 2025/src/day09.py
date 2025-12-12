import sys
import os
from itertools import combinations
from itertools import pairwise

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402
from visualisations import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2025/day/9

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_point(input_file)
    #  plot_polygon(input)
    return input


def area(p1, p2):
    return (abs(p1[0]-p2[0])+1) * (abs(p1[1]-p2[1])+1)


def ordered_areas(input):
    return sorted(combinations(input, 2), key=lambda pq: area(*pq), reverse=True)


def ordered_rect(x1, y1, x2, y2):
    return [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)]


def part1(input):
    ordered = ordered_areas(input)
    return area(*ordered[0])


def part2(input):
    result = 0
    ordered_input = ordered_areas(input)
    for (x1, y1), (x2, y2) in ordered_input:
        rect = ordered_rect(x1, y1, x2, y2)
        fits_inside = True

        # check if any line of the polygon is inside or crosses the rectangle
        for (lx1, ly1), (lx2, ly2) in pairwise(input+[input[0]]):
            line = ordered_rect(lx1, ly1, lx2, ly2)
            if line[0] < rect[2] and line[1] < rect[3] and line[2] > rect[0] and line[3] > rect[1]:
                fits_inside = False
                break

        if fits_inside:
            #  plot_polygon_plus(input, rect)
            result = area((x1, y1), (x2, y2))
            break

    return result


def main():
    input = read_input("../data/day09.txt")
    test_input = read_input("../data/day09-test.txt")

    assert (res := part1(test_input)) == 50, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 4749672288

    #  assert (res := part2(test_input)) == 24, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 1479665889


if __name__ == '__main__':
    main()
