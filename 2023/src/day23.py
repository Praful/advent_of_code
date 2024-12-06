import sys
import os
from functools import lru_cache
import queue

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/23


@lru_cache(maxsize=400)
def tuple_to_number(two_digit_tuple):
    if len(two_digit_tuple) != 2:
        raise ValueError("Input must be a two-digit tuple")

    # Use the hash function to create a unique identifier
    unique_number = hash(two_digit_tuple)

    # Ensure the result is non-negative
    return unique_number % (10**10)


class Node:
    def __init__(self, data, visited=None, junction=None, parent=None):
        self.data = data
        #  self.children = []
        self._parent = parent
        self.junction = junction
        self.visited = set() if visited is None else visited

        #  if len(visited) == 0:
        #  self.visited.add(tuple_to_number(data))
        self.visited.add(data)

    @property
    def parent(self):
        return self._parent

    def add_child(self, child_data, split=False):
        if split:
            junction = self
            visited = None
        else:
            junction = self.junction
            visited = self.visited

        child_node = Node(child_data, visited, junction, self)
        #  self.children.append(child_node)
        return child_node

    def contains(self, value):
        if value in self.visited:
            return True

        if self.junction is not None:
            return self.junction.contains(value)

        return False

    def __repr__(self):
        return f'{self.data}, {self.visited}, {self.junction}, {self.parent}'


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input


def is_wall(g, p):
    return g[p[0]][p[1]] != '#'


def neighbours_cache(position, grid, check_in_bounds=True, condition=lambda g, x: True):
    if position in cache:
        return cache[position]

    result = neighbours(position, grid, check_in_bounds, condition)
    cache[position] = result
    return result


cache = {}


# I tried to optimize this solution by caching in the Node class. It sped
# up the solution to part 1 from 6 minutes to 3 seconds. It worked for the test input
# for part 2, but didn't work for the real input.
def solve1(grid, reverse=False, start=None, end=None):
    cache.clear()

    start = (0, 1) if start is None else start  # row, col
    end = (len(grid)-1, len(grid[0])-2) if end is None else end

    q = queue.SimpleQueue()  # position, steps, last position, position's Node
    visited = Node(start)
    q.put((start, 1, None, visited))

    result = []

    while not q.empty():
        pos, steps, last_pos, visited = q.get()
        tile = grid[pos[0]][pos[1]]

        if not reverse and tile in ">v<^":
            adjacent = [next_neighbour(pos, ARROWS_TO_DIRECTION[tile])]
        else:
            adjacent = [p for p in neighbours_cache(
                pos, grid, True, is_wall) if p != last_pos]

        for next_pos in adjacent:
            if visited.contains(next_pos):
                continue

            if next_pos == end:
                result.append(steps)
            else:
                new_visited = visited.add_child(next_pos, len(adjacent) > 1)
                q.put((next_pos, steps + 1, pos, new_visited))

    return max(result)


def dfs(graph, start, end, steps=0, visited=None):
    result = steps

    if visited is None:
        visited = set()

    for next_pos in graph[start].items():
        if next_pos[0] not in visited:
            # we add and remove node because we don't want to backtrack during dfs scan.
            visited.add(next_pos[0])
            result = max(result, dfs(
                graph, next_pos[0], end, steps + next_pos[1], visited))
            visited.remove(next_pos[0])

    return result


# Create a graph by locating junctions and finding the distances between them
def condensed_graph(grid, start, end):
    junctions = [start, end]

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] != '#':
                if len(neighbours_cache((r, c), grid, True, is_wall)) > 2:
                    junctions.append((r, c))

    graph = {j: {} for j in junctions}

    for jp in junctions:
        visited = set()
        visited.add(jp)
        q = queue.SimpleQueue()
        q.put((jp, 0))
        while not q.empty():
            pos, steps = q.get()

            if pos in junctions and jp != pos:
                graph[jp][pos] = steps
                continue

            for next_pos in neighbours_cache(pos, grid, True, is_wall):
                if next_pos in visited:
                    continue
                q.put((next_pos, steps+1))
                visited.add(next_pos)

    return graph


def solve2(grid):
    cache.clear()
    start = (0, 1)  # row, column
    end = (len(grid)-1, len(grid[0])-2)
    graph = condensed_graph(grid, start, end)
    return dfs(graph, start, end, 0, {start})


def part1(input):
    return solve1(input)


def part2(input):
    return solve2(input)


def main():
    sys.setrecursionlimit(8000)

    input = read_input("../data/day23.txt")
    test_input = read_input("../data/day23-test.txt")

    assert (res := part1(test_input)) == 94, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 2278

    assert (res := part2(test_input)) == 154, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 6734


if __name__ == '__main__':
    main()

    #  with Profile() as profile:
    #
    #  main()
    #  (
    #  Stats(profile)
    #  .strip_dirs()
    #  .sort_stats(SortKey.TIME)
    #  .print_stats()
    #  )
