import re
from collections import defaultdict
import os
import sys

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/04


def read_input(input_file):
    input = read_file_str(input_file, True)

    winning_cards = {}
    my_cards = {}
    for line in input:
        parts = line.split(':')
        id = int(re.findall(r'\d+', parts[0])[0])
        numbers = parts[1].split('|')
        winning_numbers = list(map(int, numbers[0].split()))
        my_numbers = list(map(int, numbers[1].split()))

        winning_cards[id] = winning_numbers
        my_cards[id] = my_numbers

    return (winning_cards, my_cards)


def solve(input):
    pass


def part1(input):
    winning_cards, my_cards = input
    result = 0

    for id, my_numbers in my_cards.items():
        winning_numbers = winning_cards[id]
        my_winning_numbers = set(my_numbers) & set(winning_numbers)
        if len(my_winning_numbers) > 0:
            result += 2 ** (len(my_winning_numbers)-1)
    return result


def part2(input):
    winning_cards, my_cards = input
    my_scratchcards = defaultdict(lambda: 1)

    for id, my_numbers in my_cards.items():
        _ = my_scratchcards[id]  # access to initialise
        winning_numbers = winning_cards[id]
        my_winning_numbers = set(my_numbers) & set(winning_numbers)

        if len(my_winning_numbers) > 0:
            for i in range(id+1, id + len(my_winning_numbers)+1):
                my_scratchcards[i] += my_scratchcards[id]

    return sum(my_scratchcards.values())


def main():
    input = read_input("../data/day04.txt")
    test_input = read_input("../data/day04-test.txt")

    assert (res := part1(test_input)) == 13, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 21138

    assert (res := part2(test_input)) == 30, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 7185540


if __name__ == '__main__':
    main()
