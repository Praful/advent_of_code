import sys
import os
from collections import namedtuple

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/9


def read_input(input_file):
    return read_file_str(input_file, True)[0]


def is_file(x): return x % 2 == 0


def checksum(disk): return sum(i*v for i, v in enumerate(disk) if v)


# have two pointers: one at front, the other at back; move each towards each other;
# the front fills in the disk; when it hits space it grabs from back pointer
def part1(input):
    def file_id(x): return x//2

    fill_block_index = 0
    move_block_index = len(input)-1
    move_block_size = int(input[move_block_index])

    disk = []

    while fill_block_index < move_block_index:
        fill_block_size = int(input[fill_block_index])
        if is_file(fill_block_index):
            disk.extend([file_id(fill_block_index)]*fill_block_size)
        else:  # free block: fill it
            for _ in range(fill_block_size):
                if move_block_size < 1:  # grab next block to move
                    move_block_index -= 2
                    move_block_size = int(input[move_block_index])

                if move_block_index > fill_block_index:
                    move_block_size -= 1
                    disk.append(file_id(move_block_index))

        fill_block_index += 1

    # mop up the remaining blocks if any
    if move_block_index >= fill_block_index and move_block_size > 0:
        disk.extend([move_block_index//2]*move_block_size)

    return checksum(disk)


class FreeBlockMap(LinkedList):
    def __init__(self):
        super().__init__()

    def find_space(self, space_required):
        current = self.head
        while current:
            if current.data.size >= space_required:
                return current
            current = current.next
        return False


BlockInfo = namedtuple("BlcokInfo", ["index", "size"])


class Disk():
    def __init__(self):
        self.data = []
        self.files = {}
        self.free_blocks = FreeBlockMap()

    def display(self):
        for s in self.data:
            if s is None:
                print(".", end="")
            else:
                print(s, end="")
        print()

    def append(self, block_count, value):
        self.data.extend([value]*block_count)

    def move(self, from_, to, block_count):
        self.data[to:to+block_count] = self.data[from_:from_+block_count]
        self.data[from_:from_+block_count] = [None]*block_count

    def write_file(self, id, size):
        self.files[id] = BlockInfo(self.last_index, size)
        self.append(size, id)

    def write_empty_blocks(self, size):
        self.free_blocks.append(BlockInfo(self.last_index, size))
        self.append(size, None)

    def defragment(self):
        # move complete files to beginning of disk
        for id in list(reversed(self.files.keys())):
            file_size = self.files[id].size
            free_space = self.free_blocks.find_space(file_size)
            if free_space and free_space.data.index < self.files[id].index:
                self.move(self.files[id].index,
                          free_space.data.index, file_size)
                # reduce free block count
                free_space.data = BlockInfo(free_space.data.index + file_size,
                                            free_space.data.size - file_size)

    def checksum(self):
        return checksum(self.data)

    @property
    def last_index(self):
        return len(self.data)


def part2(input):
    disk = Disk()

    # populate disk with input data
    for i, block_size in enumerate(input):
        size = int(block_size)
        if is_file(i):
            disk.write_file(i//2, size)
        else:
            disk.write_empty_blocks(size)

    disk.defragment()

    return disk.checksum()


def main():
    input = read_input("../data/day09.txt")
    test_input = read_input("../data/day09-test.txt")

    assert (res := part1(test_input)) == 1928, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 6310675819476

    assert (res := part2(test_input)) == 2858, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 6335972980679


if __name__ == '__main__':
    main()
