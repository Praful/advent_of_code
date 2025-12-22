import sys
import os
from functools import lru_cache
from queue import SimpleQueue

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2025/day/11

DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    result = {}
    for line in read_file_str(input_file, True):
        result[line.split(': ')[0]] = line.split(': ')[1].split(' ')

    return result


def part1(graph):
    result = 0
    queue = SimpleQueue()
    queue.put("you")
    while queue.qsize() > 0:
        device = queue.get()
        for output in graph[device]:
            if output == 'out':
                result += 1
            else:
                queue.put(output)

    return result


def part2(graph):

    @lru_cache(maxsize=None)
    # uses dfs
    def scan(device, dac_fft_visited):
        result = 0

        for output in graph[device]:
            if output == "out":
                if all(dac_fft_visited):
                    result += 1
            else:
                dac_visited = dac_fft_visited[0] or output == "dac"
                fft_visited = dac_fft_visited[1] or output == "fft"
                result += scan(output, (dac_visited, fft_visited))

        return result

    return scan("svr", (False, False))


def main():
    input = read_input("../data/day11.txt")
    test_input = read_input("../data/day11-test.txt")
    test_input2 = read_input("../data/day11-test2.txt")

    assert (res := part1(test_input)) == 5, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 615

    assert (res := part2(test_input2)) == 2, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 303012373210128


if __name__ == '__main__':
    main()
