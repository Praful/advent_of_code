import sys
import os
import re
import math
from collections import defaultdict
from collections import deque

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/19

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


# Return [ore robot cost, clay robot cost, obsidian robot cost ores,
# obsidian robot cost clay, geode robot cost ores, geode robot cost obsidian]
def read_input(input_file):
    def parse(s):
        return list(map(int, re.findall(r'\d+', s)))

    return list(map(parse, read_file_str(input_file, True)))


ORE, CLAY, OBSIDIAN, GEODE = 0, 1, 2, 3

ORE_ROBOT_COST = 0
CLAY_ROBOT_COST = 1
OBSIDIAN_ROBOT_COST_ORES = 2
OBSIDIAN_ROBOT_COST_CLAY = 3
GEODE_ROBOT_COST_ORES = 4
GEODE_ROBOT_COST_OBSIDIAN = 5


# This optimisation from suggestion 2 here:
#  https://www.reddit.com/r/adventofcode/comments/zpy5rm/2022_day_19_what_are_your_insights_and/
def should_build(num_robots, num_resources, max_needed, time_remaining):
    return num_robots * time_remaining + num_resources < time_remaining * max_needed


def collect(robots, resources):
    return [resources[ORE] + robots[ORE],
            resources[CLAY] + robots[CLAY],
            resources[OBSIDIAN] + robots[OBSIDIAN],
            resources[GEODE] + robots[GEODE]]


def build_and_collect(robots, resources, blueprint, robot_to_build, resource1, cost1,
                      resource2=None, cost2=None):

    new_robots = robots.copy()
    new_robots[robot_to_build] += 1
    new_resources = resources.copy()
    new_resources[resource1] -= blueprint[cost1]

    if resource2:
        new_resources[resource2] -= blueprint[cost2]

    new_resources = collect(robots, new_resources)

    return (new_robots, new_resources)


def solve(robots, resources, blueprint, time_allowed):
    result = 0
    q = deque([(robots, resources, 0)])
    history = set()
    best_time = defaultdict(int)

    max_ores_needed = max(blueprint[GEODE_ROBOT_COST_ORES], blueprint[OBSIDIAN_ROBOT_COST_ORES],
                          blueprint[CLAY_ROBOT_COST], blueprint[ORE_ROBOT_COST])

    while q:
        robots, resources, minute = q.popleft()

        if minute >= time_allowed:
            result = max(result, resources[GEODE])
            continue

        best_time[minute] = max(best_time[minute], resources[GEODE])
        if best_time[minute] != resources[GEODE]:
            continue

        state = (tuple(robots), tuple(resources), minute)
        if state in history:
            continue

        history.add(state)

        # just collect resources
        q.append((robots, collect(robots, resources.copy()), minute + 1))

        # build ore robot
        need_more_ore = should_build(
            robots[ORE], resources[ORE], max_ores_needed, time_allowed - minute)

        if need_more_ore and resources[ORE] >= blueprint[ORE_ROBOT_COST]:
            new_robots, new_resources = build_and_collect(
                robots, resources, blueprint, ORE, ORE, ORE_ROBOT_COST)

            q.appendleft((new_robots, new_resources, minute + 1))

        # build clay robot
        need_more_clay = should_build(
            robots[CLAY], resources[CLAY], blueprint[OBSIDIAN_ROBOT_COST_CLAY], time_allowed - minute)

        if need_more_clay and resources[ORE] >= blueprint[CLAY_ROBOT_COST]:
            new_robots, new_resources = build_and_collect(
                robots, resources, blueprint, CLAY, ORE, CLAY_ROBOT_COST)

            q.appendleft((new_robots, new_resources, minute + 1))

        # build obsidian robot
        need_more_obsidian = should_build(
            robots[OBSIDIAN], resources[OBSIDIAN], blueprint[GEODE_ROBOT_COST_OBSIDIAN],
            time_allowed - minute)

        if need_more_obsidian and resources[ORE] >= blueprint[OBSIDIAN_ROBOT_COST_ORES] and \
                resources[CLAY] >= blueprint[OBSIDIAN_ROBOT_COST_CLAY]:

            new_robots, new_resources = build_and_collect(
                robots, resources, blueprint, OBSIDIAN, ORE, OBSIDIAN_ROBOT_COST_ORES,
                CLAY, OBSIDIAN_ROBOT_COST_CLAY)

            q.appendleft((new_robots, new_resources, minute + 1))

        # build geode robot
        if resources[ORE] >= blueprint[GEODE_ROBOT_COST_ORES] and \
                resources[OBSIDIAN] >= blueprint[GEODE_ROBOT_COST_OBSIDIAN]:

            new_robots, new_resources = build_and_collect(
                robots, resources, blueprint, GEODE, ORE, GEODE_ROBOT_COST_ORES,
                OBSIDIAN, GEODE_ROBOT_COST_OBSIDIAN)

            q.appendleft((new_robots, new_resources, minute + 1))

    #  print(result)
    return result


def process_blueprint(blueprint, time_allowed):
    return solve([1, 0, 0, 0], [0, 0, 0, 0], blueprint, time_allowed)


def part1(input):
    return sum((i + 1) * process_blueprint(blueprint[1:], 24) for i, blueprint in enumerate(input))


def part2(input):
    return math.prod(process_blueprint(blueprint[1:], 32) for blueprint in input[:3])


def main():
    input = read_input("../data/day19.txt")
    test_input = read_input("../data/day19-test.txt")

    assert (res := part1(test_input)) == 33, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 817

    assert (res := part2(test_input)) == 3472, f'Actual: {res}'
    print(f'Part 2 {part2(input[:3])}')  # 4216


if __name__ == '__main__':
    main()
