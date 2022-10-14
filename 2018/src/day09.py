import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
import utils

# Puzzle description: https://adventofcode.com/2018/day/09


class Marble:
    def __init__(self, value):
        self.value = value
        self.next = self
        self.prev = self

    # insert self after marble m
    def insert_after(self, m):
        self.next = m.next
        self.prev = m
        m.next.prev = self
        m.next = self

    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        return self.value

    def __str__(self) -> str:
        return str(self.value)

    def circle(self) -> str:
        result = str(self.value)
        m = self.next
        while m != self:
            result = f'{result}, {m.value}'
            m = m.next

        return result


def part2(num_players, num_marbles):
    print('*' * 40)
    print(f'Players: {num_players}, marbles: {num_marbles}')
    scores = [0] * num_players
    start = current = Marble(0)
    player = 0

    for m in range(1, num_marbles + 1):
        if m % 23 == 0:
            current = current.prev.prev.prev.prev.prev.prev
            # print(f'removing {current.prev}')
            scores[player] += m + current.prev.remove()
        else:
            new_marble = Marble(m)
            new_marble.insert_after(current.next)
            current = new_marble

        # print(player, start.circle(), "current", current)

        player = (player + 1) % num_players

    return max(scores)


def part1(num_players, num_marbles):
    print('*' * 40)
    print(f'Players: {num_players}, marbles: {num_marbles}')
    circle = [0]
    scores = [0] * num_players
    index = 0
    player = 0
    for m in range(1, num_marbles + 1):
        if m % 23 == 0:
            index = index - 7
            if index < 0:
                index = len(circle) + index

            scores[player] += m + circle.pop(index)

        else:
            index = ((index + 1) % len(circle)) + 1
            circle.insert(index, m)

        # print(player, circle, index, circle[index])

        player = (player + 1) % num_players

    return max(scores)


def main():
    # print(f'Part 1 (test) {part1(9, 25)}')  # 32
    # print(f'Part 1 (test) {part1(10, 1618)}')  # 8317
    # print(f'Part 1 (test) {part1(13, 7999)}')  # 146373
    # print(f'Part 1 (test) {part1(17, 1104)}')  #2764
    # print(f'Part 1 (test) {part1(21, 6111)}')  # 54718
    # print(f'Part 1 (test) {part1(30, 5807)}')  # 37305
    print(f'Part 1 (main) {part1(430, 71588)}')  # 422748

    # print(f'Part 2 (test) {part2(9, 25)}')  #
    # print(f'Part 2 (test) {part2(13, 7999)}')  #
    print(f'Part 2 (main) {part2(430, 71588*100)}')  # 3412522480


if __name__ == '__main__':
    main()
