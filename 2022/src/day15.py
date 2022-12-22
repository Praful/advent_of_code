from dataclasses import dataclass
from email.policy import default
import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
from utils import *
from collections import defaultdict
from pprint import pprint
from dataclasses import dataclass
import math
import numpy as np
import operator
import copy
import re

# Puzzle description: https://adventofcode.com/2022/day/15


# the dataclass options allow Point to be hashable
@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int

    def distance_to(self, p):
        return manhattan_distance(self.x, self.y, p.x, p.y)


@dataclass
class Sensor:
    location: Point
    closest_beacon: Point
    md: int
    intersects: bool

    def __init__(self, location, closest, line_y) -> None:
        self.location = location
        self.closest_beacon = closest
        self.md = location.distance_to(closest)
        self.intersects = abs(location.y - line_y) <= self.md


def read_input(input_file, line_y):

    maxX, minX, maxY, minY = -math.inf, math.inf, -math.inf, math.inf

    def to_sensor(l):
        nonlocal maxX, minX, maxY, minY
        match = re.findall(r'x=(-?\d*), y=(-?\d*)', l)
        res = Sensor(Point(int(match[0][0]), int(match[0][1])),
                     Point(int(match[1][0]), int(match[1][1])), line_y)
        minX = min(minX, res.location.x - res.md)
        maxX = max(maxX, res.location.x + res.md)
        return res

    res = list(map(to_sensor, read_file_str(input_file, True)))
    return (minX, maxX), res


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def tuning_frequency(x, y):
    # print(x, y)
    return (x * 4_000_000) + y


# This is quite slow and could not be used as the basis of part 2!
def part1(file, line_y):
    minmax_x, sensors = read_input(file, line_y)

    no_beacons = set()
    objects_on_row = set()
    for s in sensors:
        if not s.intersects:
            continue

        if s.location.y == line_y:
            objects_on_row.add(s.location)
        if s.closest_beacon.y == line_y:
            objects_on_row.add(s.closest_beacon)

        for x in range(minmax_x[0], minmax_x[1] + 1):
            p2 = Point(x, line_y)
            if s.location.distance_to(p2) <= s.md:
                no_beacons.add(p2)

    return len(no_beacons) - len(objects_on_row)


# Look just outside the perimeter of each sensor's rhomboid and check if those
# points are within range of any other sensor. If not, we've found the target beacon.
def part2(file, xy_range):
    _, sensors = read_input(file, 0)

    def detected(x, y):
        if x < xy_range[0] or x > xy_range[1] or y < xy_range[0] or y > xy_range[1]:
            return None

        for s in sensors:
            if manhattan_distance(s.location.x, s.location.y, x, y) <= s.md:
                return None

        return Point(x, y)

    for s in sensors:
        x = s.md + 1
        y = 0
        while x > -1:
            res = [
                detected(s.location.x + x, s.location.y + y),
                detected(s.location.x - x, s.location.y + y),
                detected(s.location.x + x, s.location.y - y),
                detected(s.location.x - x, s.location.y - y)
            ]

            if found := list(filter(lambda r: r is not None, res)):
                return tuning_frequency(found[0].x, found[0].y)

            x -= 1
            y += 1

    raise Exception('Beacon not found')


def main():
    input = "../data/day15.txt"
    test_input = "../data/day15-test.txt"

    assert (res := part1(test_input, 9)) == 25, f'Actual: {res}'
    assert (res := part1(test_input, 10)) == 26, f'Actual: {res}'
    assert (res := part1(test_input, 11)) == 27, f'Actual: {res}'
    print(f'Part 1 {part1(input, 2000000)}')  # 5181556

    assert (res := part2(test_input, (0, 20))
            ) == 56000011, f'Actual: {res}'  # (14,11)
    #
    # 12817603219131  (3204400, 3219131)
    print(f'Part 2 {part2(input, (0,4_000_000))}')


if __name__ == '__main__':
    main()
