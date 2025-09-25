from itertools import combinations, chain, product
import sys
import os
import math
from itertools import product
from pprint import pprint


sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2015/day/21

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

COST = "Cost"
DAMAGE = "Damage"
ARMOR = "Armor"
HIT_POINTS = "Hit Points"

# values: (cost, damage, armor)
#
WEAPONS = {
    "Dagger": (8, 4, 0),
    "Shortsword": (10, 5, 0),
    "Warhammer": (25, 6, 0),
    "Longsword": (40, 7, 0),
    "Greataxe": (74, 8, 0)
}

ARMORS = {
    "Leather": (13, 0, 1),
    "Chainmail": (31, 0, 2),
    "Splintmail": (53, 0, 3),
    "Bandedmail": (75, 0, 4),
    "Platemail": (102, 0, 5)
}
RINGS = {
    "Damage +1": (25, 1, 0),
    "Damage +2": (50, 2, 0),
    "Damage +3": (100, 3, 0),
    "Defense +1": (20, 0, 1),
    "Defense +2": (40, 0, 2),
    "Defense +3": (80, 0, 3)
}


#  Format
#  Hit Points: n1
#  Damage: n2
#  Armor: n3
def parse(s):
    e = s.split(': ')
    return (e[0], int(e[1]))


def read_input(input_file):
    return dict(map(parse, read_file_str(input_file, True)))


# return list of valid combinations of weapons, armors, and rings
# each item makes up a player to try
def all_combinations():

    # 1 from weapons
    weapon_items = list(WEAPONS.items())

    # 0 or 1 from armors
    armor_combos = chain.from_iterable(
        combinations(ARMORS.items(), r) for r in range(0, 2)
    )

    # 0, 1, or 2 from rings
    ring_combos = chain.from_iterable(
        combinations(RINGS.items(), r) for r in range(0, 3)
    )

    results = []
    for d1, d2, d3 in product(weapon_items, armor_combos, ring_combos):
        combo = dict([d1] + list(d2) + list(d3))
        results.append(combo)

    return results


# return true if player won
def play(boss, player, player_points=100):
    while True:
        boss[HIT_POINTS] -= max(1, player[DAMAGE] - boss[ARMOR])
        if boss[HIT_POINTS] <= 0:
            return True

        player_points -= max(1, boss[DAMAGE] - player[ARMOR])
        if player_points <= 0:
            return False


def create_player(combo):
    cost = damage = armor = 0
    for item in combo.values():
        cost += item[0]
        damage += item[1]
        armor += item[2]

    return {COST: cost, DAMAGE: damage, ARMOR: armor}


def part1(boss):
    available_combos = all_combinations()
    result = math.inf

    for combo in available_combos:
        player = create_player(combo)
        if play(boss.copy(), player):
            result = min(result, player[COST])

    return result


def part2(boss):
    available_combos = all_combinations()
    result = 0

    for combo in available_combos:
        player = create_player(combo)
        if not play(boss.copy(), player):
            result = max(result, player[COST])

    return result


def main():
    input = read_input("../data/day21.txt")

    print(f'Part 1 {part1(input)}')  # 111
    print(f'Part 2 {part2(input)}')  # 188


if __name__ == '__main__':
    main()
