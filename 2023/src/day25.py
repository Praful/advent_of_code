import random
import sys
import os
import copy
import itertools
from collections import defaultdict
import queue

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2022/day/25


def read_input(input_file):
    result = defaultdict(list)
    for l in read_file_str(input_file, True):
        node, *connections = l.replace(':', '').split()

        for c in connections:
            result[node].append(c)
            result[c].append(node)

    return result


# Either find the path between source to target or find nodes connected to source.
def bfs(graph, source, target=None):
    q = queue.SimpleQueue()
    q.put((source, 0, []))
    visited = set()

    while not q.empty():
        node, steps, path = q.get()

        for adj in graph[node]:
            if target is not None and adj == target:
                return path, steps+1, len(visited)

            if adj in visited:
                continue

            visited.add(adj)
            q.put((adj, steps+1, path + [adj]))

    return [], 0, len(visited)


# We want to cut the graph into two by cutting three edges. We start by picking two random
# nodes. These nodes need to be in different subgraphs. If they are, there will be 3 paths
# between them. Each time we find a path, we remove the edges between the two nodes.
# If we've done this three times, the two nodes are in different subgraphs and we can
# find how many nodes are in each subgraph. BFS is used to find the paths between the nodes and
# to count the nodes connected to our two starting nodes.
def part1(input):

    def remove_edge(graph, path):
        for src, dst in itertools.pairwise(path):
            graph[src].remove(dst)
            graph[dst].remove(src)

    looking = True
    # keep looking until we find two nodes that are in different subgraphs
    while looking:
        graph = copy.deepcopy(input)
        source = random.choice(list(graph.keys()))
        target = random.choice(list(graph.keys()))

        for path_count in range(4):
            path, steps, _ = bfs(graph, source, target)

            if len(path) == 0:
                if path_count == 3:
                    looking = False  # we've split the graph into two subgraphs
                break

            remove_edge(graph, path)

    _, _, connections1 = bfs(graph, source)
    _, _, connections2 = bfs(graph, target)

    return connections1 * connections2


def main():
    input = read_input("../data/day25.txt")
    test_input = read_input("../data/day25-test.txt")

    assert (res := part1(test_input)) == 54, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 533628


if __name__ == '__main__':
    main()
