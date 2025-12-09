import sys
import os
import re
from itertools import combinations
from collections import defaultdict
from math import dist, prod

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2025/day/8

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(input_file, True)
    return [tuple(map(int, l)) for l in map(lambda s: re.findall(r'\d+', s), input)]


def calc_part1(circuits, points):
    active_circuits = [v for k, v in circuits.items() if k in set(points.values())]
    return prod(map(len, sorted(active_circuits, key=len, reverse=True)[:3]))


def solve(input, connections=1000):
    def circuit(x, id):
        return circuits[id] if points[x] is not None else set([x])

    circuit_id = 1
    part1, part2 = None, None
    circuits = {}
    points = defaultdict(lambda: None)
    ordered_pairs = sorted(combinations(input, 2), key=lambda pq: dist(*pq))

    i = 0
    while True:
        p, q = ordered_pairs[i]
        i += 1

        p_circuit_id, q_circuit_id = points[p], points[q]
        p_circuit, q_circuit = circuit(p, p_circuit_id), circuit(q, q_circuit_id)

        circuit_id += 1
        circuits[circuit_id] = p_circuit | q_circuit

        if len(circuits[circuit_id]) == len(input):
            part2 = p[0]*q[0]

        points[p] = points[q] = circuit_id

        # update other points to this circuit
        for r in points:
            if points[r] in [p_circuit_id, q_circuit_id]:
                points[r] = circuit_id

        if i == connections:
            part1 = calc_part1(circuits, points)

        if part1 is not None and part2 is not None:
            break

    return part1, part2


def main():
    input = read_input("../data/day08.txt")
    test_input = read_input("../data/day08-test.txt")

    assert (res := solve(test_input, 10)) == (40, 25272), f'Actual: {res}'
    print(f'Part 1 and 2 {solve(input, 1000)}')  # 42840, 170629052


if __name__ == '__main__':
    main()
