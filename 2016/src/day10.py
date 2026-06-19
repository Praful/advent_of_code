import sys
import os
import math
from collections import defaultdict
from collections import namedtuple
import queue

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2016/day/10

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

Gives = namedtuple('Gives', ['low', 'high'])
Value = namedtuple('Values', ['value', 'bot'])


def read_input(input_file):
    bots_giving = {}
    values = []
    for line in read_file_str(input_file, True):
        if line.startswith("value"):
            words = line.split(" ")
            n = list(extract_ints(line))
            values.append(Value(n[0], f'{words[4]} {n[1]}'))
        elif line.startswith("bot"):
            n = list(extract_ints(line))
            words = line.split(" ")
            bots_giving[f'{words[0]} {n[0]}'] = Gives(
                f'{words[5]} {n[1]}', f'{words[10]} {n[2]}')
        else:
            raise ValueError(line)

    return bots_giving, values


def solve(input, comparing=None):
    def process_gives(bot_giving):
        if len(holding[bot_giving]) == 2 and bot_giving in bots_giving:
            low_value = min(holding[bot_giving])
            high_value = max(holding[bot_giving])

            low_bot = bots_giving[bot_giving].low
            high_bot = bots_giving[bot_giving].high

            holding[low_bot].append(low_value)
            holding[high_bot].append(high_value)

            holding[bot_giving] = []

            if low_bot.startswith("output"):
                low_bot = None
            if high_bot.startswith("output"):
                high_bot = None

            return low_bot, high_bot
        else:
            return None, None

    target = None if not comparing else sorted(comparing)
    bots_giving, values = input
    holding = defaultdict(list)
    q = queue.Queue()

    for value in values:
        holding[value.bot].append(value.value)
        if len(holding[value.bot]) == 2:
            q.put(value.bot)

    while not q.empty():

        bot = q.get()
        if comparing:  # part 1
            if sorted(holding[bot]) == target:
                return list(extract_ints(bot))[0]

        low_bot, high_bot = process_gives(bot)
        if low_bot:
            q.put(low_bot)
        if high_bot:
            q.put(high_bot)

    if comparing:  # part 1: we shouldn't get to this point
        assert False
    else:  # part 2: return output after all holdings have been processed
        return math.prod(holding[f"output {i}"][0] for i in range(3))


def main():
    input = read_input("../data/day10.txt")
    test_input = read_input("../data/day10-test.txt")

    assert (res := solve(test_input, [2, 5])) == 2, f'Actual: {res}'
    print(f'Part 1 {solve(input, [17, 61])}')  # 141
    print(f'Part 2 {solve(input)}')  # 1209


if __name__ == '__main__':
    main()
