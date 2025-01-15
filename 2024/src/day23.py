import sys
import os
from collections import defaultdict

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/23

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    result = defaultdict(list)
    for a, b in [s.split('-') for s in read_file_str(input_file, True)]:
        result[a].append(b)
        result[b].append(a)

    return result


# quick and dirty
def part1(links):
    def found(c): return any(i.startswith('t') for i in c)

    three_links = set()
    for k, v in links.items():
        for i in v:
            for j in links[i]:
                if k in links[j]:
                    three_links.add(tuple(sorted([k, i, j])))

    return sum([1 for c in three_links if found(c)])


def all_linked(links, inspect, connected):
    global visited
    key = tuple(sorted(connected | set([inspect])))
    if key in visited:
        return []

    visited.add(key)

    result = []
    for i in links[inspect]:
        if all(i in links[c] for c in connected):
            conn2 = connected | set([i])
            if (res := all_linked(links, i, conn2)):
                result += res
            else:
                result.append(conn2)

    return result

def part2(links):
    global visited
    visited = set()
    connected = []

    for computer, connections in links.items():
        for c in connections:
            for r in all_linked(links, c, set([computer, c])):
                connected.append(r)

    largest = max(connected, key=len)
    return ",".join(sorted(largest))


def main():
    input = read_input("../data/day23.txt")
    test_input = read_input("../data/day23-test.txt")

    assert (res := part1(test_input)) == 7, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 1215

    assert (res := part2(test_input)) == "co,de,ka,ta", f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # bm,by,dv,ep,ia,ja,jb,ks,lv,ol,oy,uz,yt

if __name__ == '__main__':
    main()
