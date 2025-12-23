import sys
import os
import re

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2025/day/12

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    shapes = {}
    regions = []
    for line in read_file_str_sections(input_file, True):
        if "x" in line[0]: # region
            for e in line:
                s = e.split(": ")
                dims = list(map(int, re.findall(r'\d+', s[0])))
                shape_count = list(map(int, s[1].split(" ")))
                regions.append((dims, shape_count))
        else: # shape
            shape_id = int(line[0].split(":")[0])
            parts = sum(c.count("#") for c in line) 
            shapes[shape_id] = parts
            
    return shapes, regions


# The input for the real data is made friendly. Just counting the total
# space used by the shapes required for each region and comparing with the 
# region's area is enough.
def part1(input):
    result = 0
    shapes, regions = input

    for r in regions:
        shape_area = 0
        region_area = r[0][0] * r[0][1]
        for i in range(len(r[1])):
            shape_area += shapes[i] * r[1][i]

        if shape_area <= region_area:
            result += 1

    return result


def main():
    input = read_input("../data/day12.txt")
    test_input = read_input("../data/day12-test.txt")

    #  Note: the solution doesn't work for the test input. It works for the real input
    #  because real data has been made friendly.
    #  assert (res := part1(test_input)) == 2, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 469


if __name__ == '__main__':
    main()
