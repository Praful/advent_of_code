import sys
import os
from queue import SimpleQueue

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/12


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input


def corner_count(pos, neighbours, garden):
    def to_plant(p): return garden[p[0]][p[1]] if in_grid(p, garden) else None

    def is_same_plant(p, delta, plant):
        return to_plant(add_pos(p, delta)) == plant

    def is_adj(p, delta):
        p2 = add_pos(p, delta)
        return in_grid(p2, garden) and p2 in neighbours

    # check L shape not block of four
    def true_corner_count():
        corners = 0
        if (N and E) and not NE:
            corners += 1
        if (S and E) and not SE:
            corners += 1
        if (S and W) and not SW:
            corners += 1
        if (N and W) and not NW:
            corners += 1

        return corners

    plant = to_plant(pos)

    # Find out if we have the same plant around us. Note the neighbours list is for N, E, S, W.
    # So we revert to looking at the whole garden for diagonals NE, SE, SW, NW
    N = is_adj(pos, NORTH)
    S = is_adj(pos, SOUTH)
    E = is_adj(pos, EAST)
    W = is_adj(pos, WEST)
    NE = is_same_plant(pos, NORTHEAST, plant)
    SE = is_same_plant(pos, SOUTHEAST, plant)
    SW = is_same_plant(pos, SOUTHWEST, plant)
    NW = is_same_plant(pos, NORTHWEST, plant)

    match len(neighbours):
        case 0:
            return 4
        case 1:
            return 2
        case 2:
            # differentiate between a corner (returns 2: inside and outside corner) and
            # a block (returns 1), ie
            #  XX vs XX
            #  X     XX
            #  the corner may be concave or convex
            corners = 0
            if (N and E) or (S and E) or (S and W) or (N and W):
                corners = 1

            return corners + true_corner_count()
        case 3 | 4:
            return true_corner_count()
        case _:
            assert False, "Unexpected number of neighbours"


# Use BFS to find region
def find_region(garden, p, regions_found):
    q = SimpleQueue()
    MAX_NEIGHBOURS = 4
    def is_neighbour(g, x): return g[x[0]][x[1]] == plant

    plant = garden[p[0]][p[1]]
    q.put((p, plant))

    visited = set()
    visited.add(p)

    corners = 0
    perimeter = 0

    while not q.empty():
        pos, plant = q.get()

        valid_neighbours = neighbours(pos, garden, True, is_neighbour)
        perimeter += MAX_NEIGHBOURS - len(valid_neighbours)
        corners += corner_count(pos, valid_neighbours, garden)

        for adj in valid_neighbours:
            if adj not in visited and adj not in regions_found:
                visited.add(adj)
                q.put((adj, plant))

    if len(visited) == 1 and p in regions_found:
        return (None, None, None)
    else:
        return visited, perimeter, corners


def solve(input):
    part1 = 0
    part2 = 0
    regions_found = set()
    for r, row in enumerate(input):
        for c, _ in enumerate(row):
            region, perimeter, corners = find_region(
                input, (r, c), regions_found)
            if region:
                regions_found |= region
                part1 += len(region) * perimeter
                part2 += len(region) * corners

    return part1, part2


def main():
    input = read_input("../data/day12.txt")
    test_input = read_input("../data/day12-test.txt")
    test_input2 = read_input("../data/day12-test2.txt")
    test_input3 = read_input("../data/day12-test3.txt")
    test_input4 = read_input("../data/day12-test4.txt")
    test_input5 = read_input("../data/day12-test5.txt")

    assert (res := solve(test_input)[0]) == 140, f'Actual: {res}'
    assert (res := solve(test_input4)[0]) == 692, f'Actual: {res}'
    assert (res := solve(test_input2)[0]) == 772, f'Actual: {res}'
    assert (res := solve(test_input3)[0]) == 1930, f'Actual: {res}'
    print(f'Part 1 {solve(input)[0]}')  # 1400386

    assert (res := solve(test_input)[1]) == 80, f'Actual: {res}'
    assert (res := solve(test_input2)[1]) == 436, f'Actual: {res}'
    assert (res := solve(test_input3)[1]) == 1206, f'Actual: {res}'
    assert (res := solve(test_input4)[1]) == 236, f'Actual: {res}'
    assert (res := solve(test_input5)[1]) == 368, f'Actual: {res}'
    print(f'Part 2 {solve(input)[1]}')  # 851994


if __name__ == '__main__':
    main()
