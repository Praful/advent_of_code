import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
import utils
from collections import defaultdict
import numpy as np
from functools import reduce

# Puzzle description: https://adventofcode.com/2022/day/2


def play(acc, round):
    shape1_scores = {'A': 1, 'B': 2, 'C': 3}
    shape2_scores = {'X': 1, 'Y': 2, 'Z': 3}
    rock = ['A', 'X']
    paper = ['B', 'Y']
    scissors = ['C', 'Z']

    game = (round.split(' '))
    shape1 = game[0]
    shape2 = game[1]
    score = shape2_scores[shape2]

    if shape1_scores[shape1] == shape2_scores[shape2]:
        score += 3
    elif shape1 in rock and shape2 in paper:
        score += 6
    elif shape1 in paper and shape2 in scissors:
        score += 6
    elif shape1 in scissors and shape2 in rock:
        score += 6

    return acc + score


# format part2 rounds to be same as part1
# input is "<shape> <outcome>"
def create_rounds(input):
    # for a given shape and outcome (lose, draw, win) find
    # needed shape. dict is (shape, outcome) = needed shape
    shape_complement = {
        ('A', 'X'): 'Z', ('A', 'Y'): 'X', ('A', 'Z'): 'Y',
        ('B', 'X'): 'X', ('B', 'Y'): 'Y', ('B', 'Z'): 'Z',
        ('C', 'X'): 'Y', ('C', 'Y'): 'Z', ('C', 'Z'): 'X'
    }

    round = input.split(' ')
    shape1 = round[0]
    output = round[1]
    return f'{shape1} {shape_complement[(shape1, output)]}'


def part1(input):
    return reduce(play, input, 0)


def part2(input):
    return reduce(play, map(create_rounds, input), 0)


def read_input(input_file):
    return utils.read_file_str(input_file, True)


def main():
    input = read_input("../data/day02.txt")
    # test_input = read_input("../data/day02-test.txt")

    # print(f'Part 1 (test) {part1(test_input)}')  # 15
    print(f'Part 1 {part1(input)}')  # 11666

    # print(f'Part 2 (test) {part2(test_input)}')  # 12
    print(f'Part 2 {part2(input)}')  # 12767


if __name__ == '__main__':
    main()
