from functools import partial
from queue import SimpleQueue

from utils import (
    DIRECTIONS,
    aoc_input_file,
    next_neighbour2,
    read_file_str,
)

# Puzzle description: https://adventofcode.com/2016/day/13

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)
    return input


def print_grid(rows, cols, is_wall_func):
    print("  ", end="")
    for c in range(cols):
        print(c, end="")
    print()

    for r in range(rows):
        print(r, end=" ")

        for c in range(cols):
            ch = "#" if is_wall_func(c, r) else "."
            print(ch, end="")
        print()


def neighbours(position, is_wall_func):
    def is_valid(p):
        return not is_wall_func(p[0], p[1]) and p[0] >= 0 and p[1] >= 0

    #  functional one-liner
    #  return filter(is_valid, map(lambda d: next_neighbour2(position, d), DIRECTIONS))

    # generator
    for d in DIRECTIONS:
        neighbour = next_neighbour2(position, d)
        if is_valid(neighbour):
            yield neighbour


# x = col, y = row
def is_wall(x, y, input):
    tmp = x * x + 3 * x + 2 * x * y + y + y * y + input

    return (tmp).bit_count() % 2


def bfs(is_wall_func, start, end, max_steps=50, is_part2=False):
    q = SimpleQueue()
    q.put((start, 0))
    seen = set(start)
    visited = set()

    while not q.empty():
        p, steps = q.get()

        if is_part2:
            if steps > max_steps:
                continue
            visited.add(p)
        elif p == end:
            return steps

        for adj in neighbours(p, is_wall_func):
            if adj not in seen:
                seen.add(adj)
                q.put((adj, steps + 1))

    if is_part2:
        return len(visited)

    return None


def part1(is_wall_func, start, end):
    return bfs(is_wall_func, start, end)


def part2(is_wall_func, start, max_steps=50):
    return bfs(is_wall_func, start, max_steps, is_part2=True)


def main():
    test_input = 10
    real_input = 1358

    # use partial functions because more flexible and clearer; could also use lambdas
    test_is_wall = partial(is_wall, input=test_input)
    real_is_wall = partial(is_wall, input=real_input)

    #  print_grid(7, 10, test_is_wall)

    assert (res := part1(test_is_wall, (1, 1), (7, 4))) == 11, f"Actual: {res}"
    print(f"Part 1 {part1(real_is_wall, (1, 1), (31, 39))}")  # 96

    print(f"Part 2 {part2(real_is_wall, (1, 1))}")  # 141


if __name__ == "__main__":
    main()
