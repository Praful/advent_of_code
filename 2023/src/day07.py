from dataclasses import dataclass
import os
import sys
from enum import Enum
from collections import Counter
from functools import cmp_to_key

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/07

# This is long-winded.
# For part2, we remove the jokers from the hand then use part1's hand_type
# function; then we check for jokers to find the strongest hand.


class HandType(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIRS = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


@dataclass
class Hand:
    hand: str
    bid: int
    type: HandType

    def __init__(self, hand, bid, part2=False):
        self.hand = hand
        self.bid = bid
        self.type = Hand.hand_type2(hand) if part2 else Hand.hand_type(hand)

    def __str__(self):
        return f"hand: {self.hand}, bid: {self.bid}, type: {self.type}"

    def __repr__(self):
        return str(self)

    @classmethod
    def strengthen(cls, hand, type):
        count = hand.count('J')
        if type == HandType.FOUR_OF_A_KIND:
            return HandType.FIVE_OF_A_KIND
        elif type == HandType.FULL_HOUSE or type == HandType.THREE_OF_A_KIND:
            if count == 1:
                return HandType.FOUR_OF_A_KIND
            else:
                return HandType.FIVE_OF_A_KIND
        elif type == HandType.TWO_PAIRS:
            return HandType.FULL_HOUSE
        elif type == HandType.ONE_PAIR:
            if count == 1:
                return HandType.THREE_OF_A_KIND
            elif count == 2:
                return HandType.FOUR_OF_A_KIND
            else:
                return HandType.FIVE_OF_A_KIND
        elif type == HandType.HIGH_CARD:
            if count == 1:
                return HandType.ONE_PAIR
            elif count == 2:
                return HandType.THREE_OF_A_KIND
            elif count == 3:
                return HandType.FOUR_OF_A_KIND
            else:
                return HandType.FIVE_OF_A_KIND
        else:
            return type

    @classmethod
    def hand_type(cls, hand):
        counts = Counter(hand).most_common(2)

        if counts[0][1] == 5:
            return HandType.FIVE_OF_A_KIND
        elif counts[0][1] == 4:
            return HandType.FOUR_OF_A_KIND
        elif counts[0][1] == 3:
            if counts[1][1] == 2:
                return HandType.FULL_HOUSE
            else:
                return HandType.THREE_OF_A_KIND
        elif counts[0][1] == 2:
            if counts[1][1] == 2:
                return HandType.TWO_PAIRS
            else:
                return HandType.ONE_PAIR
        else:
            return HandType.HIGH_CARD

    @classmethod
    def hand_type2(cls, hand):
        if 'J' not in hand:
            return Hand.hand_type(hand)

        # remove jokers
        DUMMY = 'VWXYZ'
        new_hand = []
        for i in range(len(hand)):
            if hand[i] == 'J':
                new_hand.append(DUMMY[i])
            else:
                new_hand.append(hand[i])

        type = Hand.hand_type(''.join(new_hand))
        return Hand.strengthen(hand, type)

    MAPPING = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
    MAPPING2 = {'A': 14, 'K': 13, 'Q': 12, 'J': 1,  'T': 10}

    @classmethod
    def score(cls, card, mapping):
        return int(card) if card.isnumeric() else mapping[card]

    # when we have a tie, compare each card in the hands
    @classmethod
    def card_compare(cls, hand1, hand2, part2):
        mapping = cls.MAPPING2 if part2 else cls.MAPPING
        for i in range(5):
            a = cls.score(hand1[i], mapping)
            b = cls.score(hand2[i], mapping)

            if a > b:
                return 1
            elif a < b:
                return -1

        raise Exception("cards can't have equal score: ", hand1, hand2)

    @classmethod
    def hand_compare(cls, hand1, hand2, part2=False):
        if hand1.type == hand2.type:
            return cls.card_compare(hand1.hand, hand2.hand, part2)
        else:
            if hand1.type.value > hand2.type.value:
                return 1
            else:
                return -1

    @classmethod
    def hand_compare2(cls, hand1, hand2):
        return cls.hand_compare(hand1, hand2, True)


def read_input(input_file, part2=False):
    input = read_file_str(input_file, True)
    result = []
    for line in input:
        s = line.split()
        result.append(Hand(s[0], int(s[1]), part2))

    cmp_fn = cmp_to_key(Hand.hand_compare2) if part2 else cmp_to_key(
        Hand.hand_compare)
    return sorted(result, key=cmp_fn)


def solve(input):
    return sum(i * hand.bid for i, hand in enumerate(input, 1))


def main():
    input = read_input("../data/day07.txt")
    input2 = read_input("../data/day07.txt", True)
    test_input = read_input("../data/day07-test.txt")
    test_input2 = read_input("../data/day07-test.txt", True)

    assert (res := solve(test_input)) == 6440, f'Actual: {res}'

    print(f'Part 1 {solve(input)}')  # 250453939

    assert (res := solve(test_input2)) == 5905, f'Actual: {res}'

    print(f'Part 2 {solve(input2)}')  # 248652697


if __name__ == '__main__':
    main()
