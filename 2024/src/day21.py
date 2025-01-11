import sys
import os
import copy
from itertools import pairwise
import numpy as np
from queue import SimpleQueue

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/21

DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None

#  +---+---+---+
#
#  | 7 | 8 | 9 |
#  +---+---+---+
#  | 4 | 5 | 6 |
#  +---+---+---+
#  | 1 | 2 | 3 |
#  +---+---+---+
#      | 0 | A |
#      +---+---+
#
# ----------------------
#      +---+---+
#      | ^ | A |
#  +---+---+---+
#  | < | v | > |
#  +---+---+---+


def map_pad(pad):
    result = {}
    for r, row in enumerate(pad):
        for c, ch in enumerate(row):
            result[ch] = (r, c)

    return result


def read_input(input_file):
    global NUMPAD_GRID, DIRPAD_GRID, NUMPAD_MAP, DIRPAD_MAP
    input = read_file_str(input_file, True)
    NUMPAD_MAP = map_pad(["789", "456", "123", "#0A"])
    DIRPAD_MAP = map_pad(["#^A", "<v>"])
    NUMPAD_GRID = ["789", "456", "123", "#0A"]
    DIRPAD_GRID = ["#^A", "<v>"]
    return input, NUMPAD_GRID, DIRPAD_GRID, NUMPAD_MAP, DIRPAD_MAP


def reset_caches():
    global cache1
    global cache2
    global cache3
    cache1 = {}
    cache2 = {}
    cache3 = {}


def shortest_keypresses(list):
    min_len = len(min(list, key=len))
    return [s for s in list if len(s) == min_len]


def complexity(code, keypress_count):
    return int(code.replace("A", ""))*keypress_count


# Use BFS to find all buttons pressed to get from start to end
def find_keypresses(start, end, pad, is_numpad=False):
    if (key := (is_numpad, start, end)) in cache1:
        return cache1[key]

    if start == end:
        return []

    q = SimpleQueue()
    q.put((start, set(start), ""))
    all_keypresses = []

    while not q.empty():
        pos, visited, keypresses = q.get()
        for adj in neighbours(pos, pad, True, lambda g, x: g[x[0]][x[1]] != '#'):
            dir = DIRECTION2_TO_ARROWS[direction(adj, pos)]
            if adj in visited:
                continue
            if adj == end:
                all_keypresses.append(keypresses + dir)
            else:
                visited2 = copy.deepcopy(visited)
                visited2.add(adj)
                q.put((adj, visited2, keypresses + dir))

    if len(all_keypresses) > 0:
        all_keypresses = shortest_keypresses(all_keypresses)
        cache1[(is_numpad, start, end)] = all_keypresses
        return all_keypresses

    assert False, f'No path from {start} to {end}'


# This was the part 1 solution that built up a tree of all sequences and picked the shortest.
# Too slow for part 2.
def buttons1(code, map, grid):
    top = TreeNode("")
    poss = [top]

    for (ch1, ch2) in pairwise(code):
        steps = find_keypresses(map[ch1], map[ch2], grid)
        new_poss = []
        for p in poss:
            if steps:
                for s in steps:
                    new_poss += [p.add_child(s+"A")]
            else:
                new_poss += [p.add_child("A")]

        poss = new_poss
    return shortest_keypresses(top.get_all_paths())


# Return all combinations of buttons presses for a code eg for 1234, find buttons pressed
# for 1 to 2, 2 to 3, 3 to 4
def buttons(code, map, grid, is_numpad=False):
    if (key := (is_numpad, code)) in cache2:
        return cache2[key]

    result = []
    for (ch1, ch2) in pairwise(code):
        keypresses = find_keypresses(map[ch1], map[ch2], grid, is_numpad)
        keypress_result = []
        if len(keypresses) == 0:
            keypress_result.append("A")
        else:
            for keypress in keypresses:
                keypress_result.append(keypress+"A")

        result.append(keypress_result)

    cache2[(is_numpad, code)] = result

    return result


# DFS each pair of buttons
def button_count(all_keypresses, map, grid, robots, is_numpad=False):
    if robots == 0:
        return sum(len(keypress[0]) for keypress in all_keypresses)

    result = 0
    for keypresses in all_keypresses:
        keypress_count = 1e20
        for keypress in keypresses:
            if (key := (is_numpad, keypress, robots)) in cache3:
                subkeypress_count = cache3[key]
            else:
                subkeypresses = buttons("A" + keypress, map, grid, is_numpad)
                subkeypress_count = button_count(subkeypresses, map, grid, robots - 1, is_numpad)

            keypress_count = min(keypress_count, subkeypress_count)
            cache3[(is_numpad, keypress, robots)] = keypress_count

        result += keypress_count
    return result


def solve(input, robots=2):
    codes, NUMPAD_GRID, DIRPAD_GRID, NUMPAD_MAP, DIRPAD_MAP = input
    result = 0

    for code in codes:
        reset_caches()
        all_keypresses = buttons("A" + code, NUMPAD_MAP, NUMPAD_GRID, True)
        keypress_count = button_count(all_keypresses, DIRPAD_MAP, DIRPAD_GRID, robots)

        result += complexity(code, keypress_count)

    return result


def part1(input):
    return solve(input)


def part2(input):
    return solve(input, 25)


def main():
    input = read_input("../data/day21.txt")
    test_input = read_input("../data/day21-test.txt")

    assert (res := part1(test_input)) == 126384, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 231564

    #  assert (res := part2(test_input)) == 0, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 281212077733592


if __name__ == '__main__':
    main()
