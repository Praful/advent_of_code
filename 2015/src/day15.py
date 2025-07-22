import sys
import os
import math

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2015/day/15

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

TEASPOONS = 100
CALORIES = 500


def parse(s):
    e = s.replace(',', '').replace(':', '').split(' ')
    return (e[0], (int(e[2]), int(e[4]), int(e[6]), int(e[8]), int(e[10])))


# eg return  {'Butterscotch': (-1, -2, 6, 3, 8), 'Cinnamon': (2, 3, -2, -1, 3)}
# last property is calories: butterscotch 8 and cinnamon 3)
def read_input(input_file):
    input = read_file_str(input_file, True)
    return dict(map(parse, input))


# calories must be 500 for score to be valid
def cookie_score2(teaspoons, amounts):
    if sum(w * e[4] for w, e in zip(teaspoons, amounts)) == CALORIES:
        return cookie_score(teaspoons, amounts)
    else:
        return [0, 0, 0, 0]


def cookie_score(teaspoons, amounts):
    return [
        # max ensures score is never negative
        max(sum(w * e[i] for w, e in zip(teaspoons, amounts)), 0) for i in range(4)
    ]


def score(teaspoons, amounts, score_fn=cookie_score):
    return math.prod(score_fn(teaspoons, amounts))


def solve(input, cookie_score_fn=cookie_score):
    # Generator for all combinations where sum is 100.
    # This is not pre-created so doesn't take up memory.
    teaspoon_combinations = (
        (n, m, q, TEASPOONS - n - m - q)
        for n in range(TEASPOONS + 1)
        for m in range(TEASPOONS + 1 - n)
        for q in range(TEASPOONS + 1 - n - m)
    )

    property_amounts = input.values()

    # Use max() with key to find best scoring weight tuple
    best_teaspoon_combo = max(
        teaspoon_combinations, key=lambda w: score(w, property_amounts, cookie_score_fn))
    return score(best_teaspoon_combo, property_amounts, cookie_score_fn)


def main():
    input = read_input("../data/day15.txt")
    test_input = read_input("../data/day15-test.txt")

    assert (res := solve(test_input)) == 62842880, f'Actual: {res}'
    print(f'Part 1 {solve(input)}')  # 21367368

    assert (res := solve(test_input, cookie_score2)) == 57600000, f'Actual: {res}'
    print(f'Part 2 {solve(input, cookie_score2)}')  # 1766400


if __name__ == '__main__':
    main()
