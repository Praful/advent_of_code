import sys
import os
from collections import Counter

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2022/day/23

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

ELVES = '#'
GROUND = '.'

# index of neighbours
N, E, S, W, NE, SE, SW, NW = 0, 1, 2, 3, 4, 5, 6, 7

PROPOSED_MOVES = [(N, NE, NW), (S, SE, SW), (W, NW, SW), (E, NE, SE)]


def read_input(input_file):
    input = read_file_str(input_file, True)
    result = set()
    for r, v in enumerate(input):
        for c, v2 in enumerate(v):
            if v2 == ELVES:
                result.add((r, c))
    return result


def solve(input, part2=False):
    grove = input
    proposed = 0
    round_ = 1

    while True:
        #  print_points(grove)
        
        new_grove = set()
        proposed_moves = {}
        for p in grove:
            adj = neighbours(p, None, False, include_diagonal=True)

            if set(adj).isdisjoint(grove):
                new_grove.add(p)
                continue

            try_proposed = proposed
            can_move = False
            # check can move N, S, W, E
            for _ in range(4):
                if all(adj[check] not in grove for check in PROPOSED_MOVES[try_proposed]):
                    proposed_moves[p] = adj[PROPOSED_MOVES[try_proposed][0]]
                    can_move = True
                    break

                try_proposed = (try_proposed + 1) % 4

            if not can_move:
                new_grove.add(p)

        clashes = set(p for p, c in Counter(
            proposed_moves.values()).items() if c > 1)

        for current_p, proposed_p in proposed_moves.items():
            if proposed_p in clashes:
                new_grove.add(current_p)
            else:
                new_grove.add(proposed_p)

        proposed = (proposed + 1) % 4

        if part2:
            if grove == new_grove:
                return round_
        else:
            if round_ == 10:
                return empty_ground(new_grove)

        grove = new_grove

        round_ += 1


def empty_ground(points):
    rs = [r for r, _ in points]
    cs = [c for _, c in points]

    min_r, max_r = min(rs), max(rs)
    min_c, max_c = min(cs), max(cs)

    return (max_r - min_r + 1) * (max_c - min_c + 1) - len(points)


def main():
    input = read_input("../data/day23.txt")
    #  test_input = read_input("../data/day23-test.txt")
    test_input2 = read_input("../data/day23-test2.txt")

    #  assert (res := solve(test_input)) == 0, f'Actual: {res}'
    assert (res := solve(test_input2)) == 110, f'Actual: {res}'
    print(f'Part 1 {solve(input)}')  # 4116

    assert (res := solve(test_input2, True)) == 20, f'Actual: {res}'
    print(f'Part 2 {solve(input, True)}')  # 984


if __name__ == '__main__':
    main()
