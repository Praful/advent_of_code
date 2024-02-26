import sys
import os
import re
from itertools import combinations
import numpy as np

# for profiling
#  from cProfile import Profile
#  from pstats import Stats, SortKey

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402
from visualisations import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/24


class Hailstone:
    def __init__(self, pos, vel):
        self.position = pos  # (x,y,z)
        self.velocity = vel  # (vx,vy,vz)
        self._line = None

    @property
    def next_xy(self):
        return (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

    @property
    def pos_xy(self):
        return self.position[:2]

    @property
    def line(self):
        if self._line is None:
            self._line = equation_of_line_coefficients(
                self.pos_xy, self.next_xy)
        return self._line

    def __repr__(self):
        return f'Hailstone({self.position}, {self.velocity})'


def read_input(input_file):
    result = []
    for s in read_file_str(input_file, True):
        nums = list(map(int, re.findall(r'-?\d+', s)))
        result.append(Hailstone(tuple(nums[0:3]), tuple(nums[3:6])))
    return result


def in_test_area(p, lower, upper):
    return lower <= p[0] <= upper and lower <= p[1] <= upper


def in_future(hailstone, p2):
    p1 = hailstone.pos_xy
    future_x = (hailstone.velocity[0] * (p2[0] - p1[0])) > 0
    future_y = (hailstone.velocity[1] * (p2[1] - p1[1])) > 0

    return future_x and future_y


def part1(input, lower, upper):
    result = 0
    xs = []
    ys = []
    for hailstone1, hailstone2 in combinations(input, 2):
        intersection = intersection_point(hailstone1.line, hailstone2.line)
        if intersection is not None:
            if in_test_area(intersection, lower, upper):
                if in_future(hailstone1, intersection) and in_future(hailstone2, intersection):
                    xs.append(intersection[0])
                    ys.append(intersection[1])
                    result += 1

    #  plot_2D(xs, ys)
    return result


def gaussian_elimination(Ab):
    A = np.array(Ab[:, :-1])
    b = np.array(Ab[:, -1]).reshape(-1, 1)
    result = np.linalg.solve(A, b)
    return result[0, -1], result[1, -1]

# If the rock is at X, Y, Z starting position, and has VX, VY, VZ velocity, we
# know the following at some time t:
#
#   X + t.VX = x + t.vx
#
# For a hailstone x,y,z with velocity vx, vy, vz. The same is true for Y and Z.
#
# So we have X  + t.VX = x + t.vx, and Y + t.VY = y + t.vy, and Z + t.VZ = z + t.vz
#
# Moving t to one side and taking the equations for X and Y, we get:
#
#  (X-x)/(vx-DX) = (Y-y)/(vy-VY)
#
# Expanding this out and shuffling the terms, we get:
#
#  Y.VX - X.VY = -Vy.X + vx.Y + y.VX - x.VY + (x.vy - y.vx)  (1)
#
# Below, by taking away the last hailstone (it Would be any) from four hailstones, we eliminate
# unknown Y.VX-X.VY, which is the same for all hailstones. So we're left with
#
#   -vy.X + vx.Y + y.VX - x.VY + (x.vy - y.vx) = 0  (2)
#
#  The LHS in (2) is the result of the subtraction and therefore different from
#  the RHS (1). I've kept the variable names the same so that it's clear where
#  the values are coming from below.
#
# From (2), moving the constant to the right so that we have a linear equation in
# the form AR=b (where A and b are known and R is the vector of unknown values
# for the rock), we get:
#
#   -vy.X + vx.Y + y.VX - x.VY  = (y.vx - x.vy)
#
# We want form AR = b so that we can use gaussian elimination to find R. I found a clear
# explanation of it here:  https://youtu.be/RgnWMBpQPXk?si=r3J20-QqFs3HstZl
#
# To summarise, the order of coefficients (A) below is: X, Y, VX, VY (which are
# R). Last entry is constant (b) in AR=b.

# Since we have four unknowns, we need to look at only four hailstones.


def linear_equation_coefficients(input, x, y, vx, vy):
    Ab = [[-h.velocity[vy], h.velocity[vx], h.position[y], -h.position[x],
          h.position[y]*h.velocity[vx] - h.position[x]*h.velocity[vy]] for h in input]
    last = Ab[-1]
    return np.array([row - last for row in np.array(Ab[:4])])


# There is a good explanation of this algorithm here:
#    https://www.reddit.com/r/adventofcode/comments/18q40he/2023_day_24_part_2_a_straightforward_nonsolver/
def part2(input):
    #  np.set_printoptions(suppress=True,precision=2)
    #  np.set_printoptions(formatter={'float': '{: 0.2f}'.format})

    #  x = [h.position[0] for h in input]
    #  y = [h.position[1] for h in input]
    #  z = [h.position[2] for h in input]
    #  plot_3D(x, y, z)

    A = linear_equation_coefficients(input, 0, 1, 0, 1)  # for X and Y
    X, Y = gaussian_elimination(A)

    A = linear_equation_coefficients(input, 2, 1, 2, 1)  # for Z and Y
    Z, _ = gaussian_elimination(A)

    return round(X + Y + Z)


def main():
    input = read_input("../data/day24.txt")
    test_input = read_input("../data/day24-test.txt")

    assert (res := part1(test_input, 7, 27)) == 2, f'Actual: {res}'
    print(f'Part 1 {part1(input, 200000000000000, 400000000000000)}')  # 28174

    assert (res := part2(test_input)) == 47, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 568386357876600


if __name__ == '__main__':
    main()

    #  with Profile() as profile:
    #
    #  main()
    #  (
    #  Stats(profile)
    #  .strip_dirs()
    #  .sort_stats(SortKey.TIME)
    #  .print_stats()
    #  )
