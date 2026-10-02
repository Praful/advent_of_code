import re
from collections import defaultdict
from itertools import combinations
from queue import SimpleQueue

from utils import aoc_input_file, read_file_str

# Puzzle description: https://adventofcode.com/2016/day/11

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

ORDINAL_TO_CARDINAL = {"first": 1, "second": 2, "third": 3, "fourth": 4}

GEN_INDEX = 0
CHIP_INDEX = 1


# Return the initial state.
#
# State data structure is:
#  (
#     elevator_floor,
#     (
#        (gen_floor, chip_floor),   eg hydrogen
#        (gen_floor, chip_floor),   eg lithium
#         ...
#     )
#  )
#
def read_input(input_file):
    elevator_floor = 1
    locations = defaultdict(lambda: [0, 0])

    input = read_file_str(aoc_input_file(__file__, input_file), True)
    for items in input:
        ordinal = re.search(r"(\w+) floor", items).group(1)
        floor = ORDINAL_TO_CARDINAL[ordinal.lower()]

        for gen in re.findall(r"(\w+) generator", items):
            locations[gen][GEN_INDEX] = floor

        for chip in re.findall(r"(\w+)-compatible", items):
            locations[chip][CHIP_INDEX] = floor

    locations_tuple = tuple(tuple(v) for v in locations.values())

    return (elevator_floor, locations_tuple)


def goal_reached(state):
    _, pairs = state
    return all(gen == chip == 4 for gen, chip in pairs)


# Return items on elevator's floor
# Preserve order (will be canonicalised later)
def items_on_floor(state):
    floor, pairs = state
    items = []

    for i, (gen, chip) in enumerate(pairs):
        if gen == floor:
            items.append((i, GEN_INDEX))
        if chip == floor:
            items.append((i, CHIP_INDEX))

    return items


def is_valid(state):
    _, pairs = state

    # Floors containing at least one generator
    generator_floors = {gen for gen, _ in pairs}

    for gen, chip in pairs:
        # An unaccompanied chip is unsafe if there is another generator on its floor.
        if chip != gen and chip in generator_floors:
            return False

    return True


# This is the key insight: the names don't matter eg
#   HG on 3rd floor and HC on 1st floor
# is the same as
#   LG on 3st floor and LC on 1st floor
# where H is hydrogen, L is lithium and G is generator, C is chip
# Canonicalise (sorting) reduces the unique states in the BFS
def canonicalise(state):
    elevator, pairs = state

    return (elevator, tuple(sorted(pairs)))


# Update the floor for new elevator load
def move(state, load, direction):
    elevator, pairs = state
    new_floor = elevator + direction

    pairs = [list(pair) for pair in pairs]

    for pair_index, item_type in load:
        pairs[pair_index][item_type] = new_floor

    pairs = tuple(tuple(pair) for pair in pairs)

    return new_floor, pairs


def generate_moves(state):
    elevator, _ = state
    items = items_on_floor(state)

    # Get all combinations of 1 or 2 items (the max load of elevator)
    loads = list(combinations(items, 1)) + list(combinations(items, 2))

    for direction in (-1, 1):
        new_floor = elevator + direction

        if not (1 <= new_floor <= 4):
            continue

        for load in loads:
            new_state = move(state, load, direction)

            if is_valid(new_state):
                yield canonicalise(new_state)


def bfs(start_state):
    queue = SimpleQueue()

    queue.put((start_state, 0))
    seen = {start_state}

    while not queue.empty():
        state, steps = queue.get()

        if goal_reached(state):
            return steps

        for new_state in generate_moves(state):
            if new_state not in seen:
                seen.add(new_state)
                queue.put((new_state, steps + 1))

    return None


def part1(start_state):
    return bfs(start_state)


def part2(start_state):
    elevator, pairs = start_state
    l = list(pairs)
    l.append((1, 1))  # add elerium generator and chip
    l.append((1, 1))  # add dilithium generator and chip

    return bfs((elevator, tuple(l)))


def main():
    input = read_input("day11.txt")
    test_input = read_input("day11-test.txt")

    assert (res := part1(test_input)) == 11, f"Actual: {res}"
    print(f"Part 1 {part1(input)}")  # 31

    print(f"Part 2 {part2(input)}")  # 55


if __name__ == "__main__":
    main()
