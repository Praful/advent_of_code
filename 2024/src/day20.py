import sys
import os
from collections import Counter
from queue import SimpleQueue

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/20

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

WALL = '#'
TRACK = '.'


def read_input(input_file):
    input = read_file_str(input_file, True)
    start = find_in_grid(input, 'S')
    end = find_in_grid(input, 'E')
    return input, start[0], end[0]


def find_track(grid, start, end):
    result = [start]
    def not_wall(g, x): return tile(g, x) != WALL

    q = SimpleQueue()
    q.put(start)
    visited = set([start])

    while not q.empty():
        pos = q.get()
        for adj in neighbours(pos, grid, True, not_wall):
            if adj == end:
                result.append(adj)
                break
            else:
                if not adj in visited:
                    visited.add(adj)
                    q.put(adj)
                    result.append(adj)

    return result


def cheat_savings1(grid, shortest_path, time_saving_required):
    def is_wall(g, x): return tile(g, x) == WALL
    def is_track(g, x): return not is_wall(g, x)

    savings = {}
    for t_to_cheat, p in enumerate(shortest_path):
        for wall in neighbours(p, grid, True, is_wall):
            for adj in neighbours(wall, grid, True, is_track):
                savings[(p, wall, adj)] = shortest_path.index(adj) - t_to_cheat - 2  # 2 = num moves

    return sum(1 for saving in savings.values() if saving >= time_saving_required)


def cheat_savings2(shortest_path, cheat_time, time_saving_required):
    savings = {}
    for cheat_start_index, cheat_start_pos in enumerate(shortest_path):
        for cheat_end_index in range(cheat_start_index + 1, len(shortest_path)):
            cheat_end_pos = shortest_path[cheat_end_index]
            distance = manhattan_distance(cheat_start_pos, cheat_end_pos)
            if distance <= cheat_time and cheat_end_index-cheat_start_index > distance:
                saving = cheat_end_index - cheat_start_index - distance
                if saving > 0:
                    savings[(cheat_start_index, cheat_end_index)] = saving

    #  for showing results for test input savings of 50 or more
    #  for saving, count in sorted((Counter(savings.values())).items()):
        #  if saving >= 50:
            #  print(count, saving)

    return sum(1 for saving in savings.values() if saving >= time_saving_required)


def part1(grid, start, end, time_saving_required):
    shortest_path = find_track(grid, start, end)
    return cheat_savings1(grid, shortest_path, time_saving_required)


def part2(grid, start, end, cheat_time, time_saving_required):
    shortest_path = find_track(grid, start, end)
    return cheat_savings2(shortest_path, cheat_time, time_saving_required)


def main():
    input = read_input("../data/day20.txt")
    test_input = read_input("../data/day20-test.txt")

    assert (res := part1(*test_input, 50)) == 1, f'Actual: {res}'
    print(f'Part 1 {part1(*input, 100)}')  # 1402
    #  print(f'Part 1 {part2(*input, 2, 100)}')  # 1402 (using part 2 solution for part 1)

    assert (res := part2(*test_input, 20, 50)) == 285, f'Actual: {res}'
    print(f'Part 2 {part2(*input, 20, 100)}')  # 1020244


if __name__ == '__main__':
    main()
