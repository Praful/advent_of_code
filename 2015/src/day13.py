import sys
import os
import itertools

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2015/day/13

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def parse(s):
    def happiness(a, b):
        value = int(b)
        if a == 'gain':
            return value
        elif a == 'lose':
            return -value
        else:
            assert False, f'Unknown happiness {a, b}'

    e = s.split(' ')
    return (e[0], e[10][:-1]), happiness(e[2], e[3])


def read_input(input_file):
    input = read_file_str(input_file, True)
    return dict(map(parse, input))


def circular_permutations(guests):
    # Fix the first element so that seating arrangement that are
    # rotations of each other are considered the same
    first = guests[0]
    rest = guests[1:]
    return [[first] + list(p) for p in itertools.permutations(rest)]


def solve(input, part2=False):
    def pair_score(pair):
        return input.get(pair, 0) + input.get((pair[1], pair[0]), 0)

    def seating_score(seating):
        # adding first to end allows pairwise to pair the last with
        # the first to complete the circle
        seating.append(seating[0])
        return sum(map(pair_score, itertools.pairwise(seating)))

    guests = set().union(*input.keys())
    if part2:
        guests.add('me')

    seatings = circular_permutations(list(guests))

    return max(map(seating_score, seatings))


def main():
    input = read_input("../data/day13.txt")
    test_input = read_input("../data/day13-test.txt")

    assert (res := solve(test_input)) == 330, f'Actual: {res}'
    print(f'Part 1 {solve(input)}')  # 709

    print(f'Part 2 {solve(input, True)}')  # 668


if __name__ == '__main__':
    main()
