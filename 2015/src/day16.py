import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2015/day/16

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

ALL_POSSESSIONS = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def possessions(s):
    e = s.split(':')
    return (e[0].strip(), int(e[1]))


def parse(s):
    # intput eg Sue 1: goldfish: 6, trees: 9, akitas: 0
    e = s.partition(':')
    sue_id = e[0].split(' ')[1]
    return (sue_id, dict(map(possessions, e[2].split(','))))


def read_input(input_file):
    input = read_file_str(input_file, True)
    return dict(map(parse, input))


def compare1(possession, aunt_value, all_possessions_value):
    return aunt_value == all_possessions_value


def compare2(possession, aunt_value, all_possessions_value):
    if possession in ['cats', 'trees']:
        return aunt_value > all_possessions_value
    elif possession in ['pomeranians', 'goldfish']:
        return aunt_value < all_possessions_value
    else:
        return aunt_value == all_possessions_value


def solve(input, compare):
    result = 0

    for id, aunt_possessions in input.items():
        if all(compare(possession, aunt_possessions[possession], ALL_POSSESSIONS[possession])
               for possession in aunt_possessions):

            result = id

    return result


def main():
    input = read_input("../data/day16.txt")

    print(f'Part 1 {solve(input, compare1)}')  # 103
    print(f'Part 2 {solve(input, compare2)}')  # 405


if __name__ == '__main__':
    main()
