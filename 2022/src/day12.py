import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
import utils
import queue
import math

# Puzzle description: https://adventofcode.com/2022/day/12


def read_input(input_file):
    start = ()
    end = ()
    input = utils.read_file_str(input_file, True)
    for r, v in enumerate(input):
        if (c := v.find('E')) > -1:
            end = (r, c)
            input[r] = utils.replace(input[r], c, 'z')
        if (c := v.find('S')) > -1:
            start = (r, c)
            input[r] = utils.replace(input[r], c, 'a')

    return (input, start, end)


def adjacent_squares(height_map, p):
    height = height_map[p[0]][p[1]]

    def check(adj):
        r, c = p[0] + adj[0], p[1] + adj[1]
        if 0 <= r < len(height_map) and 0 <= c < len(height_map[0]):
            if ord(height_map[r][c]) <= ord(height) + 1:
                return (r, c)
        return None

    return filter(lambda v: v is not None, [check((delta[0], delta[1]))
                                            for delta in [(0, 1), (0, -1), (1, 0), (-1, 0)]])


def solve(height_map, start, end):
    # Use BFS, see https://en.wikipedia.org/wiki/Breadth-first_search
    q = queue.SimpleQueue()
    q.put((start, 0))
    visited = set()
    visited.add(start)

    while not q.empty():
        p, steps = q.get()
        if p == end:
            return steps

        for adj in adjacent_squares(height_map, p):
            if adj not in visited:
                visited.add(adj)
                q.put((adj, steps + 1))

    # for part 2, some starting points don't have a path to the end
    # raise Exception(f'{end} not found')
    return math.inf


def part1(input):
    return solve(*input)


def part2(input):
    m = input[0]
    return min(solve(m, (r, c), input[2]) for r in range(len(m))
               for c in range(len(m[0])) if m[r][c] == 'a')


def main():
    input = read_input("../data/day12.txt")
    test_input = read_input("../data/day12-test.txt")

    assert part1(test_input) == 31
    print(f'Part 1 {part1(input)}')  # 408

    assert part2(test_input) == 29
    print(f'Part 2 {part2(input)}')  # 399


if __name__ == '__main__':
    main()
