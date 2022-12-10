import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
import utils
import numpy as np

# Puzzle description: https://adventofcode.com/2022/day/8


# check if values either side of index i are less than tree height
def in_tree_line(v, i, tree_height):
    def lr_visible(subvector):
        return len(subvector[subvector < tree_height]) == len(subvector)

    return lr_visible(v[0:i]) or lr_visible(v[i + 1:])


def is_visible(row, col, prow, pcol, tree_height):
    return in_tree_line(row, pcol, tree_height) or \
        in_tree_line(col, prow, tree_height)


def calc_score(v, i, tree_height):
    def sub_score(indexes):
        score = 0
        for j in indexes:
            score += 1
            if v[j] >= tree_height:
                break
        return score

    left_range = range(i - 1, -1, -1)
    right_range = range(i + 1, len(v))

    return sub_score(left_range) * sub_score(right_range)


def score(row, col, tree_row, tree_col, tree_height):
    return calc_score(row, tree_col, tree_height) * \
        calc_score(col, tree_row, tree_height)


# tree_row and tree_col are the y and x coords in forest
# the algorithm to parts 1 and 2 are similar; they're differentiated
# only by the count of visible trees and scores, which is
# determined by the calc_function
def calculate(forest, tree_row, tree_col, calc_function):
    tree_height = forest[tree_row, tree_col]

    row = forest[tree_row, :]
    col = forest[:, tree_col]
    return calc_function(row, col, tree_row, tree_col, tree_height)


def solve(input):
    m = np.array(input)
    h, w = m.shape
    visible_count = (2 * h) + (2 * w) - 4
    scores = []

    for r in range(1, h - 1):
        for c in range(1, w - 1):
            visible_count += calculate(m, r, c, is_visible)
            scores.append(calculate(m, r, c, score))

    return visible_count, max(scores)


def read_input(input_file):
    return [list(map(int, list(e))) for e in utils.read_file_str(input_file, True)]


def main():
    input = read_input("../data/day08.txt")
    test_input = read_input("../data/day08-test.txt")

    test_part1, test_part2 = solve(test_input)
    part1, part2 = solve(input)

    assert test_part1 == 21
    print(f'Part 1 {part1}')  # 1832

    assert test_part2 == 8
    print(f'Part 2 {part2}')  # 157320


if __name__ == '__main__':
    main()
