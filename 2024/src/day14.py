import sys
import os
import re
import copy
import math
from collections import namedtuple

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402
from visualisations import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2022/day/14

Robot = namedtuple('Robot', 'p v')

FREE = ' '


def read_input(input_file):
    def config(line):
        a = list(map(int, re.findall(r'([-]?\d+)', line)))
        return Robot((a[1], a[0]), (a[3], a[2]))

    with open(input_file, "r") as file:
        input = [config(line) for line in file]

    return input


def move_robot(robot, grid):
    r, c = robot.p[0]+robot.v[0], robot.p[1]+robot.v[1]
    if not in_grid((r, c), grid):
        h = len(grid)-1
        w = len(grid[0])-1
        r = into_range(r, 0, h)
        c = into_range(c, 0, w)

    return (r, c)


def print_robots(input, grid_dims):
    grid = make_grid(grid_dims[0], grid_dims[1], FREE)

    for robot in input:
        grid[robot.p[0]][robot.p[1]] = '#'

    print_grid(grid)


def safety_factor(input, grid_dims):
    result = [0]*4
    mid_h = grid_dims[0]//2
    mid_w = grid_dims[1]//2

    for robot in input:
        if robot.p[0] < mid_h and robot.p[1] < mid_w:
            result[0] += 1
        elif robot.p[0] < mid_h and robot.p[1] > mid_w:
            result[1] += 1
        elif robot.p[0] > mid_h and robot.p[1] < mid_w:
            result[2] += 1
        elif robot.p[0] > mid_h and robot.p[1] > mid_w:
            result[3] += 1

    return math.prod(result)


def solve(input, grid_dims, time=100):
    grid = make_grid(grid_dims[0], grid_dims[1], FREE)
    part1, part2 = 0, 0
    min_safety_factor = 3e10
    part2_robots = None

    #  ts = []
    #  sfs = []
    for t in range(10200):
        #  print(f'Time {t+1}', '-'*150)
        for i, robot in enumerate(input):
            new_pos = move_robot(robot, grid)
            input[i] = Robot(new_pos, robot.v)

        #  print_robots(input, grid_dims)
        if (sf := safety_factor(input, grid_dims)) < min_safety_factor:
            min_safety_factor = sf
            part2 = t + 1
            part2_robots = copy.deepcopy(input)

        if t+1 == time:
            part1 = sf

        #  ts.append(t)
        #  sfs.append(sf)

    #  plot_2D(ts, sfs)

    return part1, part2, part2_robots


def main():
    input = read_input("../data/day14.txt")
    test_input = read_input("../data/day14-test.txt")

    assert (res := solve(test_input, (7, 11))[0]) == 12, f'Actual: {res}'

    input_dims = (103, 101)
    # 219150360, 8053 (christmas tree)
    part1, part2, robots = solve(input, input_dims)
    print(f'Part 1 {part1}, Part 2 {part2}')
    print_robots(robots, input_dims)


if __name__ == '__main__':
    main()
