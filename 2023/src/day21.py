import os
import sys

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/21

#  For part 2, my solution is based on the quadratic insight from
#  https://github.com/bsadia/aoc_goLang/blob/master/day21/main.go


def read_input(input_file):
    input = read_file_str(input_file, True)
    start = (0, 0)
    for r, l in enumerate(input):
        if (c := l.find('S')) > 0:
            start = (r, c)
            break

    return start, input


# map coord outside our starting grid into grid to check if it's a rock
def is_rock2(g, p):
    r, c = p
    if p[1] < 0 or p[1] >= len(g[0]):
        c = into_range(p[1], 0, len(g[0])-1)
    if p[0] < 0 or p[0] >= len(g):
        r = into_range(p[0], 0, len(g)-1)

    return is_rock1(g, (r, c))


def is_rock1(g, p):
    return g[p[0]][p[1]] != '#'


def walk2(input, steps):
    result = 0
    polynomial = []
    target = steps

    start, grid = input
    grid_len = len(grid)

    q = set()
    next_q = set([start])

    for step in range(steps):
        q = next_q
        next_q = set()

        for position in q:
            for tile in neighbours(position, grid, False, is_rock2):
                next_q.add(tile)

        if step % grid_len == target % grid_len:
            polynomial.append(len(q))

            if len(polynomial) == 3:
                # we are solving quadratic equation of the form: ax^2 + bx + c
                x = target // grid_len
                c = polynomial[0]
                a = (polynomial[2] + c - 2*polynomial[1]) // 2
                b = polynomial[1] - c - a

                result = a * x**2 + b*x + c
                break

    return result


def walk1(input, steps):
    start, grid = input

    q = set()
    next_q = set([start])

    for steps in range(steps):
        q = next_q
        next_q = set()
        for position in q:
            for tile in neighbours(position, grid, True, is_rock1):
                next_q.add(tile)

    return len(next_q)


def part1(input, steps):
    return walk1(input, steps)


def part2(input, steps):
    return walk2(input, steps)


def main():
    input = read_input("../data/day21.txt")
    test_input = read_input("../data/day21-test.txt")

    assert (res := part1(test_input, 6)) == 16, f'Actual: {res}'
    print(f'Part 1 {part1(input, 64)}')  # 3617
    print(f'Part 2 {part2(input, 26501365)}')  # 596857397104703


if __name__ == '__main__':
    main()
