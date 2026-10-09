from itertools import combinations

from utils import aoc_input_file, extract_ints, make_grid, read_file_str

# Puzzle description: https://adventofcode.com/2016/day/22

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

# indexes for input list
X = 0
Y = 1
SIZE = 2
USED = 3
AVAIL = 4
USE_PERCENT = 5


def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)
    return list(map(extract_ints, input))


def is_viable(nodes):
    a, b = nodes
    if not a or not b:
        return False

    if a[USED] == 0:
        return False

    return a[USED] <= b[AVAIL]


def viable_count(nodes):
    result = 0
    if is_viable(nodes):
        result += 1

    if is_viable((nodes[1], nodes[0])):
        result += 1

    return result


def part1(input):
    return sum(viable_count(nodes) for nodes in combinations(input, 2))


# The input has been designed to let you solve part 2 by printing out
# the grid and solving it by hand. We need to move G to F (finish).
#
# Once we have drawn the grid we work out how to move the empty
# node (E) just to the left of G. Then we can move G into the empty node.
# In our input, there is a wall of non-viable nodes (X) that we need
# to move around. Something like this:
#
# F..............................G
# ................................
# ................................
# ................................
# ................................
# .........XXXXXXXXXXXXXXXXXXXXXXX
# ................................
# ................................
# ................................
# ........................E.......
# ................................
# ................................
#
#
# To get the empty node to the first target spot (next to G) takes
# 60 steps with our input: move up to wall, left around wall,
# up past wall, right along the wall then up to the first row.
#
# Then we move G once to the left into the empty node. 1 step.
# We then require 4 steps to make the node empty to the left of G again.
# We need to do this 30 times and move G 30 times. That is 5 moves
# for each G move left.
# Altogether that's 60 + 1 + (5 * 30) = 211 moves, which is our answer.
#
def print_grid(input):
    max_cols = max(node[X] for node in input if node)
    max_rows = max(node[Y] for node in input if node)

    grid = make_grid(max_rows + 1, max_cols + 1, ".")

    grid[0][max_cols] = "G"  # start
    grid[0][0] = "F"  # finish

    # find hole
    empty_node = None
    for node in input:
        if node and node[USED] == 0:
            empty_node = node
            break

    if not empty_node:
        raise ValueError("No hole found")

    grid[empty_node[Y]][empty_node[X]] = "E"

    for node in input:
        if not node or node == empty_node:
            continue

        if not is_viable((node, empty_node)):
            grid[node[Y]][node[X]] = "X"

    for row in grid:
        print("".join(row))


def part2(input):
    print_grid(input)


def main():
    input = read_input("day22.txt")

    print(f"Part 1 {part1(input)}")  # 872
    print(f"Part 2 {part2(input)}")  # 211


if __name__ == "__main__":
    main()
