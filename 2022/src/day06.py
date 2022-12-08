import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
import utils
from collections import defaultdict
import numpy as np

# Puzzle description: https://adventofcode.com/2022/day/6


class MarkerWatcher:
    def __init__(self, marker_length) -> None:
        self.buffer = []
        self.marker_length = marker_length

    def new_char(self, c):
        if c in self.buffer:
            self.buffer = self.buffer[self.buffer.index(c) + 1:]

        self.buffer.append(c)

    @property
    def marker_detected(self):
        return (len(self.buffer) >= self.marker_length)


def solve(input, marker_length=4):
    watcher = MarkerWatcher(marker_length)

    for i, c in enumerate(input):
        watcher.new_char(c)
        if watcher.marker_detected:
            return i + 1

    raise Exception('start-of-packet not found')


def read_input(input_file):
    return utils.read_file_str(input_file, True)[0]


def main():
    input = read_input("../data/day06.txt")

    assert solve("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
    assert solve("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert solve("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert solve("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    assert solve("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11

    print(f'Part 1 {solve(input)}')  # 1100

    assert solve("mjqjpqmgbljsphdztnvjfqwrcgsmlb",14) == 19
    assert solve("bvwbjplbgvbhsrlpgdmjqwftvncz",14) == 23
    assert solve("nppdvjthqldpwncqszvftbrmjlhg",14) == 23
    assert solve("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",14) == 29
    assert solve("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",14) == 26
    
    print(f'Part 2 {solve(input, 14)}')  # 2421


if __name__ == '__main__':
    main()
