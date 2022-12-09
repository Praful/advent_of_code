import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
import utils
from collections import defaultdict
import numpy as np

# Puzzle description: https://adventofcode.com/2022/day/07


class Dir:
    def __init__(self, name, parent_dir=None) -> None:
        self.name = name
        self.subdirs = []
        self.files = []
        self.parent_dir = parent_dir

    def __str__(self) -> str:
        return f'{self.name}'

    def find_subdir(self, dir):
        for d in self.subdirs:
            if d.name == dir:
                return d
        raise Exception(f'Dir {dir} not a subdir of {self.name}')

    @property
    def tree_size(self):
        return sum([f.size for f in self.files]) + \
            sum(d.tree_size for d in self.subdirs)


class File:
    def __init__(self, name, size) -> None:
        self.name = name
        self.size = size

    def __str__(self) -> str:
        return f'{self.name} (size={self.size})'


SEP = '.'


def print_tree(dir, indent_level=1):
    print(SEP * indent_level, 'Dir', dir.name)
    [print_tree(d, indent_level + 1) for d in dir.subdirs]
    [print(SEP * (indent_level + 1), 'File', f.name, f.size)
     for f in dir.files]


# return tree sizes for dir and subdirs and sub-subdirs, and ,,,
def all_dir_sizes(dir):
    sizes = [dir.tree_size]

    for d in dir.subdirs:
        sizes += all_dir_sizes(d)

    return sizes


def part1(dir):
    return sum(n for n in all_dir_sizes(dir) if n <= 100000)


AVAILABLE = 70000000
REQUIRED = 30000000


def part2(dir):
    unused = AVAILABLE - dir.tree_size
    target = REQUIRED - unused
    return min(n for n in all_dir_sizes(dir) if n >= target)


def parse(input):
    root = Dir('/')
    current_dir = None

    for line in input:
        t = line.split(' ')
        if t[1] == 'cd':
            dir = t[2]
            if dir == '/':
                current_dir = root
            elif dir == '..':
                current_dir = current_dir.parent_dir
            else:
                current_dir = current_dir.find_subdir(dir)
        elif t[0].isdigit():
            current_dir.files.append(File(t[1], int(t[0])))
        elif t[0] == 'dir':
            current_dir.subdirs.append(Dir(t[1], current_dir))

    # print_tree(root)
    return root


def read_input(input_file):
    return parse(utils.read_file_str(input_file, True))


def main():
    input = read_input("../data/day07.txt")
    test_input = read_input("../data/day07-test.txt")

    assert part1(test_input) == 95437
    print(f'Part 1 {part1(input)}')  # 1723892

    assert part2(test_input) == 24933642
    print(f'Part 2 {part2(input)}')  # 8474158


if __name__ == '__main__':
    main()
