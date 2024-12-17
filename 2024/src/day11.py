import sys
import os
from functools import lru_cache

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/11


def read_input(input_file):
    result = LinkedList()
    for s in read_file_str(input_file, True)[0].split():
        result.append(int(s))

    return result


@lru_cache(maxsize=None)
def count_stones(stones, blinks):
    if blinks == 0:
        return 1

    str_stones = str(stones)
    if stones == 0:
        return count_stones(1, blinks-1)
    elif len(str_stones) % 2 == 0:
        mid = len(str_stones) // 2
        left = int(str_stones[:mid])
        right = int(str_stones[mid:])
        return count_stones(left, blinks-1) + count_stones(right, blinks-1)
    else:
        return count_stones(stones * 2024, blinks-1)


# It turns out that the stones are independent of each other so you can
# calculate them in any order and add up eg
# calc(stone1, blinks) + calc(stone2, blinks) + ...
# Caching (stones, blinks) result cuts down the time.
def part2(input, blinks):
    node = input.head
    result = 0
    while node:
        result += count_stones(node.data, blinks)
        node = node.next

    return result


# I used linked lists expecting it would be able to cope with inserting 
# elements more quickly. However, the stones increased exponentially.
# So I abandoned this for part2.
def part1(input, blinks):
    node = input.head
    for b in range(blinks):
        node = input.head
        while node:
            sdata = str(node.data)
            if node.data == 0:
                node.data = 1
            elif len(sdata) % 2 == 0:
                mid = len(sdata) // 2
                left = int(sdata[:mid])
                right = int(sdata[mid:])
                node.data = left
                node = input.insert_after(node, right)
            else:
                node.data = node.data * 2024

            node = node.next

    return input.count


def main():
    test_input = read_input("../data/day11-test.txt")
    assert (res := part1(test_input, 6)) == 22, f'Actual: {res}'

    # reread input since part1() updates the linked list
    test_input = read_input("../data/day11-test.txt")
    assert (res := part1(test_input, 25)) == 55312, f'Actual: {res}'

    input = read_input("../data/day11.txt")
    print(f'Part 1 {part1(input, 25)}')  # 203228

    test_input = read_input("../data/day11-test.txt")
    assert (res := part2(test_input, 25)) == 55312, f'Actual: {res}'

    input = read_input("../data/day11.txt")
    print(f'Part 2 {part2(input, 75)}')  # 240884656550923


if __name__ == '__main__':
    main()
