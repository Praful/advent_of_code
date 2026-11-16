from functools import cache
from heapq import heappop, heappush

from utils import (
    aoc_input_file,
    extract_ints,
    manhattan_distance,
    neighbours,
    read_file_str,
)

# Puzzle description: https://adventofcode.com/2018/day/22

DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None

START = (0, 0)

# values represent risk levels and region_types, which happen to be the same
ROCKY, WET, NARROW = 0, 1, 2

# random values
NEITHER, TORCH, CLIMBING_GEAR = 0, 1, 2


def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)
    depth = extract_ints(input[0])[0]
    target = tuple(extract_ints(input[1]))

    return target, depth


def check(input):
    target, depth = input

    assert geologic_index((0, 0), target, depth) == 0
    assert geologic_index((1, 0), target, depth) == 16807
    assert geologic_index((0, 1), target, depth) == 48271
    assert geologic_index((1, 1), target, depth) == 145722555
    assert geologic_index((10, 10), target, depth) == 0

    assert erosion_level((0, 0), target, depth) == 510
    assert erosion_level((1, 0), target, depth) == 17317
    assert erosion_level((0, 1), target, depth) == 8415
    assert erosion_level((1, 1), target, depth) == 1805
    assert erosion_level((10, 10), target, depth) == 510


@cache
def erosion_level(p, target, depth):
    return (geologic_index(p, target, depth) + depth) % 20183


def region_type(p, target, depth):
    return erosion_level(p, target, depth) % 3


# value for both risk level and region type are the same
risk_level = region_type


def geologic_index(p, target, depth):
    erosion_level_xy = lambda x, y: erosion_level((x, y), target, depth)

    x, y = p
    if p == START or p == target:
        return 0
    elif y == 0:
        return x * 16807
    elif x == 0:
        return y * 48271
    else:
        return erosion_level_xy(x - 1, y) * erosion_level_xy(x, y - 1)


def allowed_tools(region_type):
    if region_type == ROCKY:
        return [TORCH, CLIMBING_GEAR]
    elif region_type == WET:
        return [CLIMBING_GEAR, NEITHER]
    elif region_type == NARROW:
        return [TORCH, NEITHER]
    else:
        raise ValueError(f"Unknown region type: {region_type}")


# Use A* with priority queue to find shortest path to target.
# An alternative is to use Dijkstra, in which case priority would
# be time without using manhattan_distance. Dijkstra is much slower in this
# case and visits more states.
def astar(target, depth):
    def best(state):
        return best_time.get(state, float("inf"))

    def enqueue_if_better(pos, time, tool):
        state = (pos, tool)

        if time < best(state):
            best_time[state] = time

            # use manhattan distance as estimate for remaining time to target
            estimate = manhattan_distance(pos, target) + (7 if tool != TORCH else 0)

            priority = time + estimate

            heappush(q, (priority, time, pos, tool))

    best_time = {}
    q = []

    enqueue_if_better(START, 0, TORCH)

    while q:
        priority, time, pos, tool = heappop(q)

        state = (pos, tool)
        if time > best(state):
            continue

        if state == (target, TORCH):
            return time

        # change equipment without moving
        for new_tool in allowed_tools(region_type(pos, target, depth)):
            if new_tool != tool:
                enqueue_if_better(pos, time + 7, new_tool)

        # move without changing equipment
        for adj in neighbours(pos, None, False, lambda g, p: p[0] >= 0 and p[1] >= 0):
            if tool in allowed_tools(region_type(adj, target, depth)):
                enqueue_if_better(adj, time + 1, tool)

    raise ValueError("No path found")


def part1(input):
    target, depth = input
    result = 0
    for x in range(target[0] + 1):
        for y in range(target[1] + 1):
            result += risk_level((x, y), target, depth)
    return result


def part2(input):
    target, depth = input
    return astar(target, depth)


def main():
    input = read_input("day22.txt")
    test_input = [(10, 10), 510]

    check(test_input)

    assert (res := part1(test_input)) == 114, f"Actual: {res}"
    print(f"Part 1 {part1(input)}")  # 6318

    assert (res := part2(test_input)) == 45, f"Actual: {res}"
    print(f"Part 2 {part2(input)}")  # 1075


if __name__ == "__main__":
    main()
