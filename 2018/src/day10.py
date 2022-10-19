from cmath import inf
import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
import utils
import re
import numpy as np

# Puzzle description: https://adventofcode.com/2018/day/10

# Whilst the points are moving towards each other, we continue
# the movements. Once they start moving apart, we assume the
# message has been created.


class Point:
    def __init__(self, x, y, vx, vy) -> None:
        self.x, self.y, self.vx, self.vy = x, y, vx, vy

    def __str__(self) -> str:
        return f'position <{self.x},{self.y}>, velocity <{self.vx}, {self.vy}>'


BLOCK = '\u2588'  # = █
# BLOCK = '#'


def print_grid(g):
    for y in range(g.shape[1]):
        print('')
        for x in range(g.shape[0]):
            print(' ' if g[x, y] == 0 else BLOCK, end='')


def print_np_info(a):
    print('-' * 20)
    print(a.size)
    print(a.shape)
    print('max:', a.max(axis=0))
    print('min:', a.min(axis=0))


def show(points):
    # rebase to [0,0]
    adjPoints = points - points.min(axis=0)

    grid = np.zeros(adjPoints.max(axis=0) + 1)
    for p in adjPoints:
        grid[p[0], p[1]] = 1

    print_grid(grid)

    return


def solve(input):
    last_dim = np.inf
    second = 0
    points = np.array([(p.x, p.y) for p in input])
    velocity = np.array([(p.vx, p.vy) for p in input])

    while True:
        second += 1
        new_position = points + (second * velocity)

        span = new_position.max(axis=0) - new_position.min(axis=0)
        diff = span[0].astype(np.int64) * span[1].astype(np.int64)
        if diff < last_dim:
            last_dim = diff
            message = new_position
        else:
            show(message)
            print(f'\nSeconds to wait for message {second - 1}')
            break


def read_input(input_file):
    def to_point(l):
        # extract digits from line eg
        #   position=< 42592, -31652> velocity=<-4,  3>
        match = re.findall(r'<\s*(-?\d*),\s*(-?\d*)>', l)
        return Point(int(match[0][0]), int(match[0][1]),
                     int(match[1][0]), int(match[1][1]))

    return [to_point(l) for l in utils.read_file_str(input_file)]


def printInput(input): [print(p) for p in input]


def main():
    main_input = read_input("../data/day10.txt")
    test_input = read_input("../data/day10-test.txt")

    # solve(test_input)  # HI, 3
    solve(main_input)  # EJXNCCNX, 10612


if __name__ == '__main__':
    main()
