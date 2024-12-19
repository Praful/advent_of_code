import sys
import os
from dataclasses import dataclass
from queue import PriorityQueue

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/16

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

WALL = '#'
FREE = '.'


@dataclass
class Reindeer:
    pos: tuple
    cost: int
    direction: tuple
    visited: set

    def __hash__(self):
        return hash((self.pos, self.cost, self.direction))

    def __repr__(self):
        return f'Reindeer({self.pos}, {self.cost}, {self.direction})'

    # this allows PriorityQueue to compare two items in the queue and pick the one
    # with the lower cost
    def __lt__(self, other):
        return self.cost < other.cost


def read_input(input_file):
    input = read_file_str(input_file, True)
    start = find_in_grid(input, 'S')
    end = find_in_grid(input, 'E')
    return input, start[0], end[0]


def new_cost(reindeer, p2):
    result = reindeer.cost
    if direction(p2, reindeer.pos) != reindeer.direction:
        result += 1000
    return result+1


# this produces the results instantly for part 1 because the junction key
# is reindeer position; however for part 2 (see solve() below, the key needs to be
# (position, direction), which slows it down.
def part1(input):
    result = []
    grid, start, end = input
    def move_condition(g, x): return tile(g, x) != WALL

    q = PriorityQueue()
    q.put(Reindeer(start, 0, EAST, set()))

    min_cost = float('inf')
    junction_lowest = {}

    while not q.empty():
        reindeer = q.get()
        adjacent = neighbours(reindeer.pos, grid, True, move_condition)

        if reindeer.cost > min_cost:
            continue

        #  check if another reindeer has incurred a lower cost getting to
        #  this junction; if so, we don't need to continue
        if len(adjacent) > 1:
            least = junction_lowest.get(reindeer.pos)
            if least is not None and least < reindeer.cost:
                continue

            junction_lowest[reindeer.pos] = reindeer.cost

        for adj in adjacent:
            if adj == end:
                result.append(new_cost(reindeer, adj))
            elif adj not in reindeer.visited:
                visited2 = reindeer.visited.copy()
                visited2.add(adj)
                cost2 = new_cost(reindeer, adj)
                if len(result) == 0 or cost2 < min(result):
                    q.put(Reindeer(adj, cost2, direction(
                        adj, reindeer.pos), visited2))

    return min(result)


# Solves parts 1 and 2. This could be optimised for part1 (as above) but we would still
# have to wait for part2, which is slowed down by using (position, direction) as key
# for the junction_costs dictionary
def solve(input):
    grid, start, end = input
    def move_condition(g, x): return tile(g, x) != WALL

    q = PriorityQueue()
    q.put(Reindeer(start, 0, EAST, set()))

    tile_costs = {}
    min_cost = float('inf')
    min_paths = set()

    while not q.empty():
        reindeer = q.get()

        for adj in neighbours(reindeer.pos, grid, True, move_condition):

            if reindeer.cost > min_cost:
                continue

            if tile_costs.get((reindeer.pos, reindeer.direction), float('inf')) < reindeer.cost:
                continue

            tile_costs[(reindeer.pos, reindeer.direction)] = reindeer.cost

            cost = new_cost(reindeer, adj)
            dir = direction(adj, reindeer.pos)

            if adj == end:
                if cost < min_cost:
                    min_cost = cost
                    min_paths = set(reindeer.visited)
                elif cost == min_cost:
                    min_paths |= reindeer.visited
            elif adj not in reindeer.visited:
                visited2 = reindeer.visited.copy()
                visited2.add(adj)
                if cost < min_cost:
                    q.put(Reindeer(adj, cost, dir, visited2))

    return min_cost, len(min_paths)+2  # add 2 for start and end


def main():
    input = read_input("../data/day16.txt")
    test_input = read_input("../data/day16-test.txt")
    test_input2 = read_input("../data/day16-test2.txt")

    #  assert (res := part1(test_input)) == 7036, f'Actual: {res}'
    #  assert (res := part1(test_input2)) == 11048, f'Actual: {res}'
    #  print(f'Part 1 {part1(input)}')  # 99488

    assert (res := solve(test_input)) == (7036, 45), f'Actual: {res}'
    assert (res := solve(test_input2)) == (11048, 64), f'Actual: {res}'

    print(f'Parts 1 & 2 {solve(input)}')  # 99488, 516


if __name__ == '__main__':
    main()
