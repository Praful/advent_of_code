import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
import utils
from collections import defaultdict
import numpy as np

# Puzzle description: https://adventofcode.com/2022/day/1


def part1(totals):
    return totals[-1]


def part2(totals):
    return totals[-1] + totals[-2] + totals[-3]


def read_input(input_file):
    elf_id = 1
    food_calories = []
    input = {}
    input[elf_id] = food_calories

    with open(input_file) as f:
        for line in f:
            if utils.is_blank(line):
                elf_id += 1
                food_calories = []
                input[elf_id] = food_calories
            else:
                food_calories.append(int(line.strip()))

    return sorted([sum(food_calories) for food_calories in input.values()])


def main():
    totals = read_input("../data/day01.txt")
    # test_totals = read_input("../data/day01-test.txt")

    # print(f'Part 1 (test) {part1(test_totals)}')  # 24000
    print(f'Part 1 {part1(totals)}')  # 69883

    # print(f'Part 2 (test) {part2(test_totals)}')  # 45000
    print(f'Part 2 {part2(totals)}')  # 207576


if __name__ == '__main__':
    main()
