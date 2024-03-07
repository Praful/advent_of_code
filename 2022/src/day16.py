import os
import sys
import queue
import re
from dataclasses import dataclass
from itertools import combinations
sys.path.append(os.path.relpath("../../shared/python"))


# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2022/day/16


@dataclass
class Valve:
    id: str
    flow_rate: int
    neighbours: list
    is_open: bool = False
    minute_opened: int = 0

    def __hash__(self):
        return hash(self.id)


def read_input(input_file):
    valves = {}
    for l in read_file_str(input_file, True):
        match = re.search(
            r'^Valve (..) has flow rate=(\d*).* valves? (.*)$', l)
        if match:
            # print(match.group(0))
            id = match.group(1)
            valves[id] = Valve(id, int(match.group(2)),
                               match.group(3).split(', '))

    return valves, valve_distances(valves)


def valve_distances(input):
    distance = {}
    for v1 in input.keys():
        for v2 in input.keys():
            if v1 != v2 and (v1, v2) not in distance:
                distance[(v1, v2)] = distance[(v2, v1)
                                              ] = calculate_distance(input, v1, v2)

    return distance


# calc distance between two valves using BFS
def calculate_distance(input, start, end):
    q = queue.SimpleQueue()
    visited = set()
    q.put((start, 0))
    values = []

    while not q.empty():
        valve, distance = q.get()
        if valve == end:
            values.append(distance)
            continue
        for neighbour in input[valve].neighbours:
            if not neighbour in visited:
                visited.add(neighbour)
                q.put((neighbour, distance + 1))

    return min(values)


def calculate_pressure(time_left, pressure, valves, start, distances):
    if time_left <= 0:
        return pressure

    if start.flow_rate > 0:
        time_left -= 1
        pressure += (start.flow_rate * time_left)

    if len(valves) == 0:
        return pressure

    result = pressure

    for next_valve in valves:
        if next_valve.id == start.id or distances[(next_valve.id, start.id)] >= time_left:
            continue

        to_visit = [v for v in valves if next_valve.id != v.id and
                    v.flow_rate > 0]

        valve_pressure = calculate_pressure(time_left - distances[(next_valve.id, start.id)],
                                            pressure, to_visit, next_valve, distances)
        result = max(result, valve_pressure)

    return result


def valves_to_tuple(valves):
    return tuple(sorted([valve.id for valve in valves]))


def print_valves(s, valves):
    print(s, valves_to_tuple(valves))


def part1(input, distances):
    return calculate_pressure(30, 0, input.values(), input['AA'], distances)


def part2(input, distances):
    def calc(valves):
        key = valves_to_tuple(valves)
        if key in cache:
            result = cache[key]
        else:
            result = calculate_pressure(26, 0, valves, input['AA'], distances)
            cache[key] = result

        return result

    cache = {}
    # ignore valves with flow rate 0 since they won't add to total pressure released
    pressured_valves = set(
        [valve for valve in input.values() if valve.flow_rate > 0])
    result = 0

    # Generate all possible combinations of valves and paritition them betwen person
    # and elephant
    for i in range(1, len(pressured_valves) + 1):
        for person_valves in combinations(pressured_valves, i):
            elephant_valves = pressured_valves - set(person_valves)
            pressure = calc(person_valves) + calc(elephant_valves)

            result = max(result, pressure)

    return result


def main():
    input = read_input("../data/day16.txt")
    test_input = read_input("../data/day16-test.txt")

    assert (res := part1(*test_input)) == 1651, f'Actual: {res}'
    print(f'Part 1 {part1(*input)}')  # 1789

    assert (res := part2(*test_input)) == 1707, f'Actual: {res}'
    print(f'Part 2 {part2(*input)}')  # 2496


if __name__ == '__main__':
    main()
