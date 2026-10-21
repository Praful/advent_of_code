import copy
from collections import deque

from utils import aoc_input_file, neighbours, print_grid, read_file_str, replace, tile

# Puzzle description: https://adventofcode.com/2018/day/15

DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None

WALL = "#"
OPEN = "."
ELF = "E"
GOBLIN = "G"


class Unit:
    def __init__(self, pos, type):
        self.pos = pos
        self.type = type
        self.hp = 200
        self.attack_power = 3

    @property
    def is_alive(self):
        return self.hp > 0

    @property
    def r(self):
        return self.pos[0]

    @property
    def c(self):
        return self.pos[1]

    def is_enemy(self, other):
        return self.type != other.type

    def __str__(self):
        return f"Unit({self.pos}, {self.type}, {self.hp}, {self.attack_power})"

    def __repr__(self):
        return self.__str__()


def find_units(input):
    units = {}
    for r in range(len(input)):
        for c in range(len(input[r])):
            if input[r][c] in [ELF, GOBLIN]:
                units[(r, c)] = Unit((r, c), input[r][c])

    return units


def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)
    units = find_units(input)
    return input, units


def is_open(g, x):
    return tile(g, x) == OPEN


def is_not_wall(g, x):
    return tile(g, x) != WALL


# find candidate open spaces to move into
def find_targets(grid, unit, units):
    result = set()
    for target in units.values():
        if unit == target or not target.is_alive or not target.is_enemy(unit):
            continue

        for adj in neighbours(target.pos, grid, True, is_open):
            result.add(adj)

    return result


# find distances from start to all open spaces
def bfs(grid, start):
    distances = {start: 0}
    queue = deque([start])

    while queue:
        pos = queue.popleft()

        for adj in neighbours(pos, grid, True, is_open):
            if adj not in distances:
                distances[adj] = distances[pos] + 1
                queue.append(adj)

    return distances


# find next move for unit
def find_move(grid, unit, units):
    targets = find_targets(grid, unit, units)

    # First BFS: distances to reachable squares from the unit
    distances = bfs(grid, unit.pos)

    reachable = targets & distances.keys()

    if not reachable:
        return None

    # Shortest distance, then destination reading order
    destination = min(reachable, key=lambda p: (distances[p], p))

    # Second BFS: distances from chosen destination (distances back toward unit)
    reverse_distances = bfs(grid, destination)

    # Adjacent open squares where the unit could move
    first_steps = neighbours(unit.pos, grid, True, is_open)

    # Choose first step on a shortest path, then reading order.
    # The -1 is because the distance to p is one less than the distance to destination
    candidates = [
        p
        for p in first_steps
        if p in reverse_distances and reverse_distances[p] == distances[destination] - 1
    ]

    return min(candidates) if candidates else None


def adjacent_enemies(grid, unit, units):
    return [
        adj
        for adj in neighbours(unit.pos, grid, True, is_not_wall)
        if adj in units and units[adj].is_enemy(unit)
    ]


# check if we can attack by looking for adjacent enemies
# if so, attack the one with the lowest hp
# if tie for lowest hp, attack the one in reading order
def attack(unit, grid, units):
    enemies = adjacent_enemies(grid, unit, units)

    if enemies:
        # find min hp and, if tie, reading order
        target = min(enemies, key=lambda pos: (units[pos].hp, pos))
        units[target].hp -= unit.attack_power

        if not units[target].is_alive:
            killed_type = units[target].type
            grid[target[0]] = replace(grid[target[0]], target[1], OPEN)
            del units[target]
            return killed_type

    return None


# Make a single move for unit; update grid if necesary to reflect move, which
# helps visualise the combat for debugging
def take_turn(unit, grid, units):
    if not adjacent_enemies(grid, unit, units):
        next_move = find_move(grid, unit, units)
        if next_move is not None:
            del units[unit.pos]
            grid[unit.r] = replace(grid[unit.r], unit.c, OPEN)

            unit.pos = next_move
            units[unit.pos] = unit
            grid[unit.r] = replace(grid[unit.r], unit.c, unit.type)

    return attack(unit, grid, units)


def is_combat_over(units):
    return len({u.type for u in units.values()}) <= 1


def outcome(units, rounds_completed):
    return rounds_completed * sum(u.hp for u in units.values())


def simulate_combat(grid, units, stop_on_elf_death=False):
    rounds_completed = 0
    while True:
        turn_order = sorted(units.values(), key=lambda u: (u.r, u.c))
        for unit in turn_order:
            if not unit.is_alive:
                continue

            if is_combat_over(units):
                return rounds_completed

            killed_type = take_turn(unit, grid, units)

            if stop_on_elf_death and killed_type == ELF:
                return None

        rounds_completed += 1


def part1(input):
    grid, units = input
    test_grid = copy.copy(grid)
    test_units = copy.deepcopy(units)

    #  print_grid(grid, True)

    rounds_completed = simulate_combat(test_grid, test_units)

    #  print_grid(grid, True)

    return outcome(test_units, rounds_completed)


def part2(input):
    grid, units = input

    for attack_power in range(4, 201):
        test_units = copy.deepcopy(units)
        test_grid = copy.copy(grid)

        for unit in test_units.values():
            if unit.type == ELF:
                unit.attack_power = attack_power

        rounds_completed = simulate_combat(test_grid, test_units, True)

        if rounds_completed is not None:
            return outcome(test_units, rounds_completed)

    raise RuntimeError("No elf victory without casualties for attack power 4–200")


def main():
    input = read_input("../data/day15.txt")
    test_input2 = read_input("../data/day15-test2.txt")
    test_input3 = read_input("../data/day15-test3.txt")
    test_input4 = read_input("../data/day15-test4.txt")
    test_input5 = read_input("../data/day15-test5.txt")
    test_input6 = read_input("../data/day15-test6.txt")
    test_input7 = read_input("../data/day15-test7.txt")

    # Part 1 ========================================================

    # 47 * 590
    assert (res := part1(test_input2)) == 27730, f"Actual: {res}"

    # 37 rounds * 982 total hp
    assert (res := part1(test_input3)) == 36334, f"Actual: {res}"

    # 46 rounds * 859 total hp
    assert (res := part1(test_input4)) == 39514, f"Actual: {res}"

    # 35 rounds * 793 total hp
    assert (res := part1(test_input5)) == 27755, f"Actual: {res}"

    # 54 rounds * 536 total hp
    assert (res := part1(test_input6)) == 28944, f"Actual: {res}"

    # 20 rounds * 937 total hp
    assert (res := part1(test_input7)) == 18740, f"Actual: {res}"

    print(f"Part 1 {part1(input)}")  # 215168

    # Part 2 ========================================================

    # 29 rounds * 172 total hp
    assert (res := part2(test_input2)) == 4988, f"Actual: {res}"

    # 33 rounds * 948 total hp
    assert (res := part2(test_input4)) == 31284, f"Actual: {res}"

    # 37 rounds * 94 total hp
    assert (res := part2(test_input5)) == 3478, f"Actual: {res}"

    # 39 rounds * 166 total hp
    assert (res := part2(test_input6)) == 6474, f"Actual: {res}"

    # 30 rounds * 38 total hp
    assert (res := part2(test_input7)) == 1140, f"Actual: {res}"

    print(f"Part 2 {part2(input)}")  # 52374


if __name__ == "__main__":
    main()
