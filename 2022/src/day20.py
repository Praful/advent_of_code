import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2022/day/20

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

DECRYPTION_KEY = 811589153


def read_input(input_file):
    return list(map(int, read_file_str(input_file, True)))


class Node:
    def __init__(self, value):
        self.value = value
        self.next = self
        self.prev = self

    def __str__(self):
        return str(f'value={self.value}, prev={self.prev.value}, next={self.next.value}')


class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append_node(self, node):
        if not self.head:
            self.head = node
        else:
            tail = self.head.prev
            tail.next = node
            node.prev = tail
            node.next = self.head
            self.head.prev = node

        self.size += 1

    def move(self, node, n):
        if self.size <= 1 or n == 0:
            return

        forward = n > 0

        # The -1 is significant for part 2 but not part 1. Removing the node
        # from the list (as we do to move it) reduces the size of the list
        # by 1. For some reason, this is masked when the numbers are small (as
        # in part 1) but not when they are large (as in part 2).
        step = abs(n) % (self.size - 1)

        if step == 0:
            return

        target = node
        if forward:
            for _ in range(step):
                target = target.next
        else:
            for _ in range(step+1):
                target = target.prev

        if target is node:
            return

        # detach
        node.prev.next = node.next
        node.next.prev = node.prev

        original_next = node.next

        # insert after target
        node.prev = target
        node.next = target.next
        target.next.prev = node
        target.next = node

        if node is self.head:
            self.head = original_next

    def __str__(self):
        if not self.head:
            return "[]"

        current = self.head
        out = []

        while True:
            out.append(current.value)
            current = current.next
            if current is self.head:
                break

        return out.__str__()


def nth_node(node, n, size):
    steps = n % size
    for _ in range(steps):
        node = node.next

    return node.value


def solve(input, rounds=1, decryption_key=1):
    cll = CircularLinkedList()
    orig_order = {}
    zero_node = None
    for i in range(len(input)):
        node = Node(input[i] * decryption_key)
        orig_order[i] = node
        cll.append_node(node)

        if node.value == 0:
            zero_node = node

    for _ in range(rounds):
        for i in range(len(input)):
            node = orig_order[i]
            cll.move(node, node.value)

    v1 = nth_node(zero_node, 1000, len(input))
    v2 = nth_node(zero_node, 2000, len(input))
    v3 = nth_node(zero_node, 3000, len(input))

    return v1 + v2 + v3


def main():
    input = read_input("../data/day20.txt")
    test_input = read_input("../data/day20-test.txt")

    assert (res := solve(test_input)) == 3, f'Actual: {res}'
    print(f'Part 1 {solve(input)}')  # 8372

    assert (res := solve(test_input, 10, DECRYPTION_KEY)
            ) == 1623178306, f'Actual: {res}'
    print(f'Part 2 {solve(input, 10, DECRYPTION_KEY)}')  # 7865110481723


if __name__ == '__main__':
    main()
