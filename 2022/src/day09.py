import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
import utils
from utils import point
import numpy as np
import copy

# Puzzle description: https://adventofcode.com/2022/day/9

direction_delta = {'R': point(1, 0),
        'L': point(-1, 0),
        'U': point(0, 1),
        'D': point(0, -1),
        'NE': point(1, 1),
        'SE': point(1, -1),
        'NW': point(-1, 1),
        'SW': point(-1, -1),
        }


# This works for part1 only; solve() is a general solution for both parts.
def part1(input):
    head = point()
    tail = point()
    visited = set()
    visited.add(tuple(tail))

    prev_head = head
    for m in input:
        dir, steps = m.split()
        for _ in range(int(steps)):
            prev_head = head
            head = head + direction_delta[dir]
            if not near_by(head, tail):
                tail = prev_head if are_diagonal(
                    head, tail) else tail + direction_delta[dir]

            visited.add(tuple(tail))

    return len(visited)


def draw(rope):
    PADDING = 5
    m = np.array(rope)
    min = np.amin(m, axis=0)
    start = point()
    if any(min < 0):
        m = m + np.abs(min)
        start = np.abs(min)

    max = np.amax(m, axis=0) + start + PADDING
    grid = np.full(tuple(max), '.')

    for i, p in enumerate(m):
        grid[p[0], p[1]] = i

    grid[start[0], start[1]] = 's'
    [print(''.join(l)) for l in np.rot90(grid)]
    # print(rope)


def are_diagonal(head, back):
    return not any(head == back)


def near_by(head, back):
    return np.array_equal(head, back) or utils.is_adjacent(head, back)


def move_direction(front, back):
    x, y = front - back
    dir = ''
    if are_diagonal(front, back):
        if x >= 0:
            dir = 'NE' if y >= 0 else 'SE'
        else:
            dir = 'NW' if y >= 0 else 'SW'
    else:
        if x == 0:
            dir = 'D' if y < 0 else 'U'
        else:
            dir = 'L' if x < 0 else 'R'

    return direction_delta[dir]


# This works for both parts 1 and 2
def solve(input, knots):
    rope = [point() for _ in range(knots)]
    visited = set()
    TAIL_INDEX = knots - 1
    HEAD_INDEX = 0
    visited.add(tuple(rope[TAIL_INDEX]))

    for direction in input:
        dir, steps = direction.split()
        for _ in range(int(steps)):
            rope[HEAD_INDEX] += direction_delta[dir]

            for i in range(1, len(rope)):
                if not near_by(rope[i - 1], rope[i]):
                    rope[i] += move_direction(rope[i - 1], rope[i])

            visited.add(tuple(rope[TAIL_INDEX]))

        # draw(body)

    return len(visited)


def read_input(input_file):
    input = utils.read_file_str(input_file, True)
    return input


def main():
    input = read_input("../data/day09.txt")
    test_input = read_input("../data/day09-test.txt")
    test_input2 = read_input("../data/day09-test2.txt")

    assert part1(test_input) == 13
    assert solve(test_input, 2) == 13
    # print(f'Part 1 {part1(input)}')  # 6357
    print(f'Part 1 {solve(input,2)}')  # 6357

    # assert solve(test_input, 10) == 1
    assert solve(test_input2, 10) == 36
    print(f'Part 2 {solve(input,10)}')  # 2627


if __name__ == '__main__':
    main()
