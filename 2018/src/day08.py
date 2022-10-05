import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
import utils

# Puzzle description: https://adventofcode.com/2018/day/08


class Node:
    def __init__(self, child_count, metadata_count):
        self.__child_count = child_count
        self.__metadata_count = metadata_count
        self.__children = []
        self.__metadata = []

    @property
    def child_count(self): return self.__child_count

    @property
    def metadata_count(self): return self.__metadata_count

    @property
    def children(self): return self.__children

    @property
    def metadata(self): return self.__metadata

    def add_child(self, node): self.__children.append(node)

    def add_metadata(self, metadata): self.__metadata.append(metadata)

    def tree_metadata_sum(self):
        return self.metadata_sum() + sum(n.tree_metadata_sum() for n in self.children)

    def metadata_sum(self): return sum(self.metadata)

    def value(self):
        if self.child_count == 0:
            return self.metadata_sum()
        else:
            return sum(self.children[m - 1].value()
                       for m in self.metadata if 1 <= m <= self.child_count)

    def __str__(self) -> str:
        s = ' '.join(str(m) for m in self.metadata)
        return f'Child count: {self.child_count}, metadata count {self.metadata_count}, metadata:{s}'


def part1(head_node): return head_node.tree_metadata_sum()


def part2(head_node): return head_node.value()


def build_tree(input, offset=0):
    child_count = input[offset]
    metadata_count = input[offset + 1]
    node = Node(child_count, metadata_count)

    offset += 2

    if child_count > 0:
        for _ in range(child_count):
            child, offset = build_tree(input, offset)
            node.add_child(child)

    for imeta in range(offset, offset + metadata_count):
        node.add_metadata(input[imeta])

    # print(node)
    return node, offset + metadata_count


def read_input(input_file):
    input = utils.read_file_int(input_file)
    return build_tree(input)


def main():
    main_input, _ = read_input("../data/day08.txt")
    test_input, _ = read_input("../data/day08-test.txt")

    print(f'Part 1 (test) {part1(test_input)}')  # 138
    print(f'Part 1 {part1(main_input)}')  # 48155

    print(f'Part 2 (test) {part2(test_input)}')  # 66
    print(f'Part 2 {part2(main_input)}')  # 40292


if __name__ == '__main__':
    main()
