import sys
import os
import re
import copy
from collections import namedtuple
import queue

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/22

Point = namedtuple("Point", ["x", "y", "z"])


class Brick:
    def __init__(self, id, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2
        self.id = id
        self.bricks_above = set()
        self.bricks_below = set()
        self._supporting = None
        self._supported_by = None

    def on_ground(self):
        return self.lowest_point() == 1

    def highest_point(self):
        return max(self.pos1.z, self.pos2.z)

    def lowest_point(self):
        return min(self.pos1.z, self.pos2.z)

    def ranges_overlap(self, r1, r2):
        return not (r1[1] < r2[0] or r1[0] > r2[1])

    def overlaps(self,  other):
        x1, y1, z1 = self.pos1
        x2, y2, z2 = self.pos2
        x_range1 = (min(x1, x2), max(x1, x2))
        y_range1 = (min(y1, y2), max(y1, y2))
        z_range1 = (min(z1, z2), max(z1, z2))

        x3, y3, z3 = other.pos1
        x4, y4, z4 = other.pos2
        x_range2 = (min(x3, x4), max(x3, x4))
        y_range2 = (min(y3, y4), max(y3, y4))
        z_range2 = (min(z3, z4), max(z3, z4))

        # Check for overlap in x, y, and z
        overlap_x = self.ranges_overlap(x_range1, x_range2)
        overlap_y = self.ranges_overlap(y_range1, y_range2)
        overlap_z = self.ranges_overlap(z_range1, z_range2)

        return (overlap_x, overlap_y, overlap_z)

    def is_level_below(self, other):
        return self.highest_point() == other.lowest_point()-1

    def supported_by(self):
        if self._supported_by is None:
            self._supported_by = [
                b for b in self.bricks_below if b.is_level_below(self)]

        return self._supported_by

    def supporting(self):
        if self._supporting is None:
            self._supporting = [
                b for b in self.bricks_above if self.is_level_below(b)]

        return self._supporting

    def is_under(self, other):
        x_overlap, y_overlap, _ = self.overlaps(other)
        return x_overlap and y_overlap

    def drop(self, amount=1):
        self.pos1 = Point(self.pos1.x, self.pos1.y, self.pos1.z - amount)
        self.pos2 = Point(self.pos2.x, self.pos2.y, self.pos2.z - amount)

    def __repr__(self):
        return f'Brick {self.id}: {self.pos1}, {self.pos2}'


def read_input(input_file):
    result = []
    id = 0
    for l in read_file_str(input_file, True):
        val = list(map(int, re.findall(r'\d+', l)))
        result.append(
            Brick(id, Point(val[0], val[1], val[2]), Point(val[3], val[4], val[5])))
        id += 1

    return result


def drop_bricks(input):
    #  pprint(bricks)
    bricks = copy.deepcopy(input)
    bricks.sort(key=lambda b: b.lowest_point())

    for falling in bricks:
        if falling.on_ground():
            continue

        highest_point = 1  # highest z for bricks below

        lower_bricks = [
            lower for lower in bricks if lower.lowest_point() < falling.lowest_point()]

        if not lower_bricks:
            continue

        for lower in lower_bricks:
            if lower.is_under(falling):
                falling.bricks_below.add(lower)
                lower.bricks_above.add(falling)
                highest_point = max(highest_point, lower.highest_point()+1)

        if falling.lowest_point() > highest_point:
            falling.drop(falling.lowest_point() - highest_point)

    bricks.sort(key=lambda b: b.lowest_point())
    return bricks


def disintegrate(removed_brick):
    for above in removed_brick.supporting():
        if len(above.supported_by()) == 1:
            return 0

    return 1


def disintegrate_chain_reaction(removed_brick):
    def can_disintegrate(count, brick):
        return count == len(brick.supported_by())

    q = queue.SimpleQueue()
    q.put(removed_brick)
    disintegrated = {removed_brick.id: True}

    while not q.empty():
        brick = q.get()
        for above in brick.supporting():
            if above.id in disintegrated:
                continue

            supports_disintegrated_count = sum(
                1 for a in above.supported_by() if a.id in disintegrated)

            if can_disintegrate(supports_disintegrated_count, above):
                disintegrated[above.id] = True

            q.put(above)

    return len(disintegrated)-1


def solve(input, process):
    resting = drop_bricks(input)
    return sum(process(b) for b in resting)


def main():
    input = read_input("../data/day22.txt")
    test_input = read_input("../data/day22-test.txt")

    assert (res := solve(test_input, disintegrate)) == 5, f'Actual: {res}'
    print(f'Part 1 {solve(input, disintegrate)}')  # 490

    assert (res := solve(test_input, disintegrate_chain_reaction)
            ) == 7, f'Actual: {res}'
    print(f'Part 2 {solve(input, disintegrate_chain_reaction)}')  # 96356


if __name__ == '__main__':
    main()
